"""Append-only JSONL event store — durable adapter, no DB product."""

from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Any, Optional


class FileEventStore:
    """Persists each Event as one JSON line. Air-gap friendly. Not a cloud product."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.touch()
        self._lock = Lock()
        self._by_id: dict[str, dict[str, Any]] = {}
        self._events: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        self._events = []
        self._by_id = {}
        with self._path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                ev = json.loads(line)
                self._events.append(ev)
                self._by_id[ev["id"]] = ev

    def load_all(self) -> list[dict[str, Any]]:
        return list(self._events)

    def append_persisted(self, event: dict[str, Any]) -> None:
        with self._lock:
            if event["id"] in self._by_id:
                return
            with self._path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, separators=(",", ":"), sort_keys=True))
                f.write("\n")
                f.flush()
            self._events.append(event)
            self._by_id[event["id"]] = event

    def get(self, event_id: str) -> Optional[dict[str, Any]]:
        return self._by_id.get(event_id)
