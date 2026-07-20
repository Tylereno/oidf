"""Signing / verification port — ADR-0017. No KMS vendor types."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class SigningPort(Protocol):
    def payload_hash(self, payload: dict) -> str:
        ...

    def sign(self, principal_or_node_id: str, payload_hash: str) -> str:
        ...

    def verify(self, principal_or_node_id: str, payload_hash: str, signature: str) -> bool:
        ...

    def has_key(self, principal_or_node_id: str) -> bool:
        ...
