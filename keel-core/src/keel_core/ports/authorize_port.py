"""Authorize policy port — RFC 0012, ADR-0007."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class AuthorizePort(Protocol):
    """Deny-by-default authorization using Configuration policy data."""

    def authorize(self, request: dict[str, Any]) -> dict[str, Any]:
        """Validate idl/security/authorize_request.json → AuthorizeResponse."""
        ...
