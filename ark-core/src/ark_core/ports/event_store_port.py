"""Outbound event durability port — adapters implement persistence products."""

from __future__ import annotations

from typing import Any, Iterable, Optional, Protocol, runtime_checkable


@runtime_checkable
class EventStorePort(Protocol):
    def load_all(self) -> list[dict[str, Any]]:
        ...

    def append_persisted(self, event: dict[str, Any]) -> None:
        """Persist after in-memory accept; must be durable before return."""
        ...

    def get(self, event_id: str) -> Optional[dict[str, Any]]:
        ...
