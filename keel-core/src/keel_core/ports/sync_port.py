"""Synchronization Engine port — RFC 0008, ADR-0014, ADR-0015."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SyncEnginePort(Protocol):
    """Store-and-forward sync without transport knowledge.

    Implementations MUST:
    - export/import SyncBatch (idl/sync/sync_batch.json)
    - enforce affinity epochs / fencing (ADR-0014)
    - verify node trust / revocation (ADR-0015) via IdentityPort hooks
    - quarantine on CDO hash mismatch or integrity failure
    - never delete audit Events
    """

    def export_batch(self, batch_id: str, *, since_cursor: str | None = None) -> dict[str, Any]:
        ...

    def import_batch(self, batch: dict[str, Any]) -> dict[str, Any]:
        """Returns status: ok | quarantined and reason metadata."""
        ...

    def sync_status(self, peer_node_id: str) -> dict[str, Any]:
        ...

    def set_affinity(self, deployment_id: str, primary_node_id: str, epoch: int) -> None:
        """Assign write affinity + fencing epoch (ADR-0004, ADR-0014)."""
        ...
