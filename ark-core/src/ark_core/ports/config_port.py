"""Configuration port — RFC 0011, ADR-0008."""

from __future__ import annotations

from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class ConfigPort(Protocol):
    """Versioned configuration resolution with pin support."""

    def resolve(self, domain: str, *, revision: Optional[int] = None) -> dict[str, Any]:
        ...

    def current_revision(self, domain: str) -> int:
        ...

    def propose(self, document: dict[str, Any]) -> dict[str, Any]:
        """Authorized config revise; emits ConfigurationRevised via EventPort in app layer."""
        ...
