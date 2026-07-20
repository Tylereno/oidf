"""Sync Engine application service — RFC 0008, ADR-0014/0015."""

from __future__ import annotations

from typing import Any

from keel_core.app.event_service import EventService
from keel_core.ports.identity_port import IdentityPort


def order_key(event: dict[str, Any]) -> tuple:
    subject = event.get("asset_id") or event.get("deployment_id") or ""
    return (subject, event.get("occurred_at", ""), event.get("actor_id", ""), event["id"])


class SyncEngineService:
    def __init__(
        self,
        events: EventService,
        identity: IdentityPort,
        *,
        local_node_id: str = "edge-a",
    ) -> None:
        self._events = events
        self._identity = identity
        self.local_node_id = local_node_id
        self.affinity_primary: dict[str, str] = {}
        self.affinity_epochs: dict[str, int] = {}
        self.local_cdo_hashes: dict[tuple[str, int], str] = {}
        self.quarantined: list[dict[str, Any]] = []

    def set_affinity(self, deployment_id: str, primary_node_id: str, epoch: int) -> None:
        self.affinity_primary[deployment_id] = primary_node_id
        self.affinity_epochs[deployment_id] = epoch

    def export_batch(self, batch_id: str, *, since_cursor: str | None = None) -> dict[str, Any]:
        return {
            "batch_id": batch_id,
            "sender_node_id": self.local_node_id,
            "protocol_version": "1.0.0",
            "events": self._events.all_events(),
            "cdo_revisions": [
                {"deployment_id": d, "revision": r, "content_hash": h}
                for (d, r), h in self.local_cdo_hashes.items()
            ],
            "summary_clock": {},
            "affinity_epochs": dict(self.affinity_epochs),
            "content_hash": f"hash-{batch_id}",
        }

    def import_batch(self, batch: dict[str, Any]) -> dict[str, Any]:
        sender = batch.get("sender_node_id", "")
        if self._identity.is_node_revoked(sender):
            self.quarantined.append(batch)
            return {"status": "quarantined", "reason": "NodeRevoked"}
        if not self._identity.verify_batch_integrity(batch):
            self.quarantined.append(batch)
            return {"status": "quarantined", "reason": "IntegrityFailure"}

        for ref in batch.get("cdo_revisions", []):
            key = (ref["deployment_id"], ref["revision"])
            local = self.local_cdo_hashes.get(key)
            if local is not None and local != ref["content_hash"]:
                self.quarantined.append(batch)
                return {"status": "quarantined", "reason": "CdoHashMismatch"}

        # ADR-0014 fencing: StateAdvanced for deployment with stale/foreign epoch → quarantine event
        sender_epochs = batch.get("affinity_epochs") or {}
        merged = 0
        skipped = 0
        for e in sorted(batch.get("events", []), key=order_key):
            if e.get("type") == "StateAdvanced":
                dep = e.get("deployment_id")
                if dep and dep in self.affinity_epochs:
                    claimed = sender_epochs.get(dep)
                    local_epoch = self.affinity_epochs[dep]
                    primary = self.affinity_primary.get(dep)
                    if claimed is None or claimed < local_epoch or (
                        primary and sender != primary and claimed == local_epoch
                    ):
                        skipped += 1
                        continue
            before = len(self._events.all_events())
            self._events.append(e)
            if len(self._events.all_events()) > before:
                merged += 1
        return {"status": "ok", "merged": merged, "fenced_skipped": skipped}

    def sync_status(self, peer_node_id: str) -> dict[str, Any]:
        return {
            "peer_node_id": peer_node_id,
            "local_events": len(self._events.all_events()),
            "quarantined": len(self.quarantined),
        }
