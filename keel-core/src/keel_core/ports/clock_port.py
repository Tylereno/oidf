"""Clock port — abstract time for determinism tests; not an NTP vendor."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ClockPort(Protocol):
    def now_rfc3339(self) -> str:
        """UTC timestamp string for recorded_at / evaluation freshness checks."""
        ...
