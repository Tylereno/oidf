"""Ed25519 signing adapter — ADR-0017."""

from __future__ import annotations

import base64
import hashlib
import json
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)


def _b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64u_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


class Ed25519SigningAdapter:
    def __init__(self) -> None:
        self._private: dict[str, Ed25519PrivateKey] = {}
        self._public: dict[str, Ed25519PublicKey] = {}

    def generate(self, identity_id: str) -> dict[str, str]:
        priv = Ed25519PrivateKey.generate()
        pub = priv.public_key()
        self._private[identity_id] = priv
        self._public[identity_id] = pub
        return {
            "identity_id": identity_id,
            "public_key": _b64u(
                pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
            ),
            "private_key": _b64u(
                priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
            ),
        }

    def load_private(self, identity_id: str, private_key_b64: str) -> None:
        priv = Ed25519PrivateKey.from_private_bytes(_b64u_decode(private_key_b64))
        self._private[identity_id] = priv
        self._public[identity_id] = priv.public_key()

    def load_public(self, identity_id: str, public_key_b64: str) -> None:
        self._public[identity_id] = Ed25519PublicKey.from_public_bytes(
            _b64u_decode(public_key_b64)
        )

    def payload_hash(self, payload: dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def sign(self, principal_or_node_id: str, payload_hash: str) -> str:
        priv = self._private[principal_or_node_id]
        return _b64u(priv.sign(payload_hash.encode("utf-8")))

    def verify(self, principal_or_node_id: str, payload_hash: str, signature: str) -> bool:
        pub = self._public.get(principal_or_node_id)
        if pub is None:
            return False
        try:
            pub.verify(_b64u_decode(signature), payload_hash.encode("utf-8"))
            return True
        except (InvalidSignature, ValueError):
            return False

    def has_key(self, principal_or_node_id: str) -> bool:
        return principal_or_node_id in self._private or principal_or_node_id in self._public
