"""Plugin Runtime port — RFC 0007, ADR-0016."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class PluginRuntimePort(Protocol):
    """Host lifecycle, isolation, and capability registry.

    Production implementations MUST provide a separate failure domain from Core
    engines (ADR-0016). Reference/dev profiles may be in-process but cannot
    claim production conformance.
    """

    def register(self, capability_descriptor: dict[str, Any]) -> None:
        """Register CapabilityDescriptor (idl/plugin/capability_descriptor.json)."""
        ...

    def start(self, plugin_id: str) -> None:
        ...

    def stop(self, plugin_id: str) -> None:
        ...

    def quarantine(self, plugin_id: str, reason: str) -> None:
        """Isolate plugin after fault/quota/allowlist abuse."""
        ...

    def health(self, plugin_id: str) -> dict[str, Any]:
        ...

    def publish_allowlist(self, plugin_id: str) -> list[str]:
        """Event types this plugin may publish."""
        ...
