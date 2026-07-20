"""Subprocess Plugin Runtime — ADR-0016 isolation floor."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class PluginProcess:
    plugin_id: str
    descriptor: dict[str, Any]
    proc: Optional[subprocess.Popen] = None
    quarantined: bool = False
    module: str = ""


@dataclass
class SubprocessPluginRuntime:
    """Hosts Plugins as child processes speaking JSON-lines on stdio."""

    python_executable: str = field(default_factory=lambda: sys.executable)
    extra_pythonpath: list[str] = field(default_factory=list)
    _plugins: dict[str, PluginProcess] = field(default_factory=dict)
    publish_callback: Callable[[dict[str, Any], str], dict[str, Any]] | None = None

    def register(self, capability_descriptor: dict[str, Any]) -> None:
        pid = capability_descriptor["plugin_id"]
        self._plugins[pid] = PluginProcess(plugin_id=pid, descriptor=capability_descriptor)

    def start(self, plugin_id: str, module: str) -> None:
        entry = self._plugins[plugin_id]
        if entry.quarantined:
            raise RuntimeError(f"plugin quarantined: {plugin_id}")
        env = os.environ.copy()
        paths = list(self.extra_pythonpath) + env.get("PYTHONPATH", "").split(os.pathsep)
        env["PYTHONPATH"] = os.pathsep.join([p for p in paths if p])
        proc = subprocess.Popen(
            [self.python_executable, "-m", module],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )
        entry.proc = proc
        entry.module = module
        self._send(proc, {"op": "start", "descriptor": entry.descriptor})
        resp = self._recv(proc)
        if not resp or resp.get("status") != "ok":
            err = ""
            if proc.stderr:
                err = proc.stderr.read()
            self.quarantine(plugin_id, f"start_failed:{err}")
            raise RuntimeError(f"plugin start failed: {resp} stderr={err}")

    def stop(self, plugin_id: str) -> None:
        entry = self._plugins.get(plugin_id)
        if not entry or not entry.proc:
            return
        try:
            self._send(entry.proc, {"op": "stop"})
        except BrokenPipeError:
            pass
        entry.proc.terminate()
        try:
            entry.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            entry.proc.kill()
        entry.proc = None

    def quarantine(self, plugin_id: str, reason: str) -> None:
        entry = self._plugins[plugin_id]
        entry.quarantined = True
        if entry.proc and entry.proc.poll() is None:
            entry.proc.kill()
            entry.proc = None

    def health(self, plugin_id: str) -> dict[str, Any]:
        entry = self._plugins[plugin_id]
        alive = bool(entry.proc and entry.proc.poll() is None)
        return {
            "plugin_id": plugin_id,
            "alive": alive,
            "quarantined": entry.quarantined,
            "reason_note": "ok" if alive else "stopped",
        }

    def publish_allowlist(self, plugin_id: str) -> list[str]:
        return list(self._plugins[plugin_id].descriptor.get("publishes", []))

    def dispatch_event(self, plugin_id: str, event: dict[str, Any]) -> list[dict[str, Any]]:
        entry = self._plugins[plugin_id]
        if entry.quarantined or not entry.proc:
            return []
        try:
            self._send(entry.proc, {"op": "event", "event": event})
            resp = self._recv(entry.proc)
        except Exception as exc:  # noqa: BLE001
            self.quarantine(plugin_id, f"crash:{exc}")
            return []
        if not resp:
            self.quarantine(plugin_id, "no_response")
            return []
        if resp.get("status") == "error":
            self.quarantine(plugin_id, resp.get("reason", "error"))
            return []
        drafts = resp.get("publish", [])
        stored: list[dict[str, Any]] = []
        if self.publish_callback:
            for d in drafts:
                stored.append(self.publish_callback(d, plugin_id))
        return stored

    @staticmethod
    def _send(proc: subprocess.Popen, msg: dict[str, Any]) -> None:
        assert proc.stdin is not None
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()

    @staticmethod
    def _recv(proc: subprocess.Popen) -> dict[str, Any] | None:
        assert proc.stdout is not None
        line = proc.stdout.readline()
        if not line:
            return None
        return json.loads(line)
