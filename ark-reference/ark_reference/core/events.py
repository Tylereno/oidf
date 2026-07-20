from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ark_reference.schema import validate


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def new_id(prefix: str = "evt") -> str:
    return f"{prefix}-{uuid4().hex[:12]}"


@dataclass
class EventEngine:
    """Append-only in-memory Event log with per-subject sequences."""

    events: list[dict[str, Any]] = field(default_factory=list)
    _sequences: dict[str, int] = field(default_factory=dict)
    _by_id: dict[str, dict[str, Any]] = field(default_factory=dict)
    validate_schema: bool = True

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        if self.validate_schema:
            validate("event/envelope.json", event)
        eid = event["id"]
        if eid in self._by_id:
            return self._by_id[eid]  # idempotent by id
        subject = event.get("asset_id") or event.get("deployment_id") or "_global"
        seq = self._sequences.get(subject, 0) + 1
        self._sequences[subject] = seq
        stored = dict(event)
        stored["sequence"] = seq
        if "recorded_at" not in stored:
            stored["recorded_at"] = utcnow()
        self.events.append(stored)
        self._by_id[eid] = stored
        return stored

    def read_all(self) -> list[dict[str, Any]]:
        return list(self.events)

    def get(self, event_id: str) -> dict[str, Any] | None:
        return self._by_id.get(event_id)
