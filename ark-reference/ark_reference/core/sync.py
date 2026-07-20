from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ark_reference.core.events import EventEngine


def order_key(event: dict[str, Any]) -> tuple:
    subject = event.get("asset_id") or event.get("deployment_id") or ""
    return (subject, event.get("occurred_at", ""), event.get("actor_id", ""), event["id"])


@dataclass
class SyncEngine:
    """Minimal store-and-forward merge (RFC 0008) for reference."""

    events: EventEngine
    affinity_primary: dict[str, str] = field(default_factory=dict)  # deployment_id -> node_id
    local_node_id: str = "edge-a"
    quarantined: list[dict[str, Any]] = field(default_factory=list)
    local_cdo_hashes: dict[tuple[str, int], str] = field(default_factory=dict)

    def export_batch(self, batch_id: str) -> dict[str, Any]:
        return {
            "batch_id": batch_id,
            "sender_node_id": self.local_node_id,
            "protocol_version": "1.0.0",
            "events": self.events.read_all(),
            "cdo_revisions": [
                {"deployment_id": d, "revision": r, "content_hash": h}
                for (d, r), h in self.local_cdo_hashes.items()
            ],
            "summary_clock": {},
            "content_hash": f"hash-{batch_id}",
        }

    def import_batch(self, batch: dict[str, Any]) -> dict[str, Any]:
        # CDO hard fault
        for ref in batch.get("cdo_revisions", []):
            key = (ref["deployment_id"], ref["revision"])
            local = self.local_cdo_hashes.get(key)
            if local is not None and local != ref["content_hash"]:
                self.quarantined.append(batch)
                return {"status": "quarantined", "reason": "CdoHashMismatch"}

        incoming = sorted(batch.get("events", []), key=order_key)
        merged = 0
        for e in incoming:
            before = len(self.events.events)
            self.events.append(e)
            if len(self.events.events) > before:
                merged += 1
        return {"status": "ok", "merged": merged}
