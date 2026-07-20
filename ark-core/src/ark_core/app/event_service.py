"""Event Engine application service — RFC 0006, ADR-0016."""

from __future__ import annotations

from threading import Lock
from typing import Any, Iterable, Optional
from uuid import uuid4

from ark_core.domain.errors import PluginAllowlistError
from ark_core.ports.clock_port import ClockPort


class EventService:
    """In-process Event Engine logic. Persistence is injected via replaceable store hooks.

    This service holds an append-only list by default; production adapters may
    wrap the same API without Core knowing the storage product.
    """

    CORE_PRIVILEGED_TYPES = frozenset({"StateAdvanced", "TransitionRejected"})

    def __init__(
        self,
        clock: ClockPort,
        *,
        plugin_allowlists: dict[str, set[str]] | None = None,
    ) -> None:
        self._clock = clock
        self._events: list[dict[str, Any]] = []
        self._by_id: dict[str, dict[str, Any]] = {}
        self._sequences: dict[str, int] = {}
        self._lock = Lock()
        self._plugin_allowlists = plugin_allowlists or {}

    def set_plugin_allowlist(self, plugin_id: str, types: set[str]) -> None:
        self._plugin_allowlists[plugin_id] = set(types)

    def append(self, event: dict[str, Any], *, publisher_plugin_id: Optional[str] = None) -> dict[str, Any]:
        if publisher_plugin_id is not None:
            allowed = self._plugin_allowlists.get(publisher_plugin_id, set())
            et = event.get("type")
            if et not in allowed:
                raise PluginAllowlistError(
                    f"plugin {publisher_plugin_id} may not publish {et}"
                )
            if et in self.CORE_PRIVILEGED_TYPES and et not in allowed:
                raise PluginAllowlistError(f"privileged type denied: {et}")

        with self._lock:
            eid = event["id"]
            if eid in self._by_id:
                return self._by_id[eid]
            subject = event.get("asset_id") or event.get("deployment_id") or "_global"
            seq = self._sequences.get(subject, 0) + 1
            self._sequences[subject] = seq
            stored = dict(event)
            stored["sequence"] = seq
            if "recorded_at" not in stored:
                stored["recorded_at"] = self._clock.now_rfc3339()
            self._events.append(stored)
            self._by_id[eid] = stored
            return stored

    def read(self, *, subject_key: Optional[str] = None, after_sequence: int = 0) -> Iterable[dict[str, Any]]:
        for e in self._events:
            if subject_key is not None:
                sk = e.get("asset_id") or e.get("deployment_id") or "_global"
                if sk != subject_key:
                    continue
            if int(e.get("sequence", 0)) <= after_sequence:
                continue
            yield e

    def get(self, event_id: str) -> Optional[dict[str, Any]]:
        return self._by_id.get(event_id)

    def all_events(self) -> list[dict[str, Any]]:
        return list(self._events)

    @staticmethod
    def new_id(prefix: str = "evt") -> str:
        return f"{prefix}-{uuid4().hex[:12]}"
