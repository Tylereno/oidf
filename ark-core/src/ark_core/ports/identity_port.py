"""Identity port — RFC 0009, ADR-0015."""

from __future__ import annotations

from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class IdentityPort(Protocol):
    """Abstract identity — no IdP product types.

    Concrete authentication providers are adapters/Plugins outside Core knowledge.
    """

    def authenticate(self, credential_ctx: dict[str, Any]) -> dict[str, Any]:
        """Return IdentityAssertion (idl/identity/identity_assertion.json)."""
        ...

    def resolve(self, principal_id: str) -> Optional[dict[str, Any]]:
        """Return Principal profile or None."""
        ...

    def is_node_revoked(self, node_id: str) -> bool:
        """Revocation check for SyncBatch verification (ADR-0015)."""
        ...

    def verify_batch_integrity(self, batch: dict[str, Any]) -> bool:
        """Verify SyncBatch signature/hash against non-revoked node keys."""
        ...
