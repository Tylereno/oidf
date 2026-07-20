"""Concrete infra adapters are forbidden in this package until separately authorized.

Only `memory` doubles for conformance/dev are permitted.
"""

from ark_core.adapters.memory import FixedClock, MemoryConfig, MemoryIdentity, SystemClock

__all__ = ["SystemClock", "FixedClock", "MemoryIdentity", "MemoryConfig"]
