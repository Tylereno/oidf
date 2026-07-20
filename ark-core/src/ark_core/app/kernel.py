"""Compose Core application services for a node (no infra products)."""

from __future__ import annotations

from typing import Any

from ark_core.adapters.memory import MemoryIdentity, SystemClock
from ark_core.app.authorize_service import AuthorizeService
from ark_core.app.event_service import EventService
from ark_core.app.state_service import StateEngineService
from ark_core.app.sync_service import SyncEngineService
from ark_core.baseline import SPEC_BASELINE_ID
from ark_core.ports.clock_port import ClockPort
from ark_core.ports.identity_port import IdentityPort


class CoreKernel:
    """Production Core composition root (ports wired to app services)."""

    def __init__(
        self,
        *,
        grants: list[dict[str, Any]] | None = None,
        node_id: str = "edge-a",
        clock: ClockPort | None = None,
        identity: IdentityPort | None = None,
    ) -> None:
        self.baseline_id = SPEC_BASELINE_ID
        self.clock = clock or SystemClock()
        self.identity = identity or MemoryIdentity()
        self.authorize = AuthorizeService(grants=grants)
        self.events = EventService(self.clock)
        self.state = StateEngineService(self.events, self.authorize, self.clock)
        self.sync = SyncEngineService(self.events, self.identity, local_node_id=node_id)
