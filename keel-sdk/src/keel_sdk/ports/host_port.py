"""Plugin host port — Event in/out only (RFC 0007, ADR-0016)."""

from __future__ import annotations

from typing import Any, Callable, Protocol, runtime_checkable


@runtime_checkable
class PluginHostPort(Protocol):
    """Host APIs visible to Plugins. No StateEnginePort exposure."""

    def register_capability(self, descriptor: dict[str, Any]) -> None:
        ...

    def publish(self, event_draft: dict[str, Any]) -> dict[str, Any]:
        """Publish via EventPort subject to allowlist."""
        ...

    def subscribe(self, filter_expr: dict[str, Any], handler: Callable[[dict[str, Any]], None]) -> str:
        """Register handler; returns subscription id."""
        ...

    def read_config(self, keys: list[str]) -> dict[str, Any]:
        ...

    def report_health(self, status: dict[str, Any]) -> None:
        ...
