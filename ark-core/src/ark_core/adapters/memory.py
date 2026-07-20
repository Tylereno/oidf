"""Memory/dev doubles — NOT production infrastructure adapters.

Forbidden here: Postgres, SQLite files as product lock-in, NATS, MQTT, cloud SDKs.
These doubles exist so CoreKernel can run conformance tests without I/O products.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional


class SystemClock:
    def now_rfc3339(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class FixedClock:
    def __init__(self, ts: str) -> None:
        self._ts = ts

    def now_rfc3339(self) -> str:
        return self._ts

    def set(self, ts: str) -> None:
        self._ts = ts


class MemoryIdentity:
    """Dev identity double — always verifies unless node revoked."""

    def __init__(self) -> None:
        self.revoked: set[str] = set()
        self.fail_integrity = False

    def authenticate(self, credential_ctx: dict[str, Any]) -> dict[str, Any]:
        return {
            "principal_id": credential_ctx.get("principal_id", "unknown"),
            "issued_at": SystemClock().now_rfc3339(),
            "expires_at": SystemClock().now_rfc3339(),
            "issuer": "memory",
        }

    def resolve(self, principal_id: str) -> Optional[dict[str, Any]]:
        return {"id": principal_id, "kind": "human"}

    def is_node_revoked(self, node_id: str) -> bool:
        return node_id in self.revoked

    def verify_batch_integrity(self, batch: dict[str, Any]) -> bool:
        return not self.fail_integrity


class MemoryConfig:
    def __init__(self) -> None:
        self._docs: dict[str, dict[str, Any]] = {}

    def resolve(self, domain: str, *, revision: Optional[int] = None) -> dict[str, Any]:
        doc = self._docs.get(domain)
        if not doc:
            return {}
        if revision is not None and doc.get("revision") != revision:
            return {}
        return dict(doc.get("body", {}))

    def current_revision(self, domain: str) -> int:
        return int(self._docs.get(domain, {}).get("revision", 0))

    def propose(self, document: dict[str, Any]) -> dict[str, Any]:
        self._docs[document["domain"]] = document
        return document
