"""Event Bus / Event Engine port — RFC 0006, ADR-0001, ADR-0016."""

from __future__ import annotations

from typing import Any, Iterable, Optional, Protocol, runtime_checkable


@runtime_checkable
class EventPort(Protocol):
    """Append-only event log port.

    Implementations MUST:
    - validate envelopes against idl/event/envelope.json
    - assign per-subject monotonic sequence
    - enforce Plugin publish allowlists (ADR-0016) when publisher is a Plugin
    - remain durable for audit/replay (adapter concern; port assumes durability contract)
    """

    def append(self, event: dict[str, Any], *, publisher_plugin_id: Optional[str] = None) -> dict[str, Any]:
        """Append event; idempotent on event id. Returns stored event including sequence."""
        ...

    def read(self, *, subject_key: Optional[str] = None, after_sequence: int = 0) -> Iterable[dict[str, Any]]:
        """Read events for replay/catch-up."""
        ...

    def get(self, event_id: str) -> Optional[dict[str, Any]]:
        """Fetch by id."""
        ...
