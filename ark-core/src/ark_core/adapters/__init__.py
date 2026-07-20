"""Adapters: durable/file + crypto. No cloud/broker products required for v1.

- memory: test doubles
- file_event_store: append-only JSONL
- ed25519_signing: ADR-0017
"""

from ark_core.adapters.ed25519_signing import Ed25519SigningAdapter
from ark_core.adapters.file_event_store import FileEventStore
from ark_core.adapters.memory import FixedClock, MemoryConfig, MemoryIdentity, SystemClock

__all__ = [
    "SystemClock",
    "FixedClock",
    "MemoryIdentity",
    "MemoryConfig",
    "FileEventStore",
    "Ed25519SigningAdapter",
]
