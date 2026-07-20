"""Compose Core application services for a node."""

from __future__ import annotations

from typing import Any

from ark_core.adapters.memory import MemoryIdentity, SystemClock
from ark_core.app.authorize_service import AuthorizeService
from ark_core.app.event_service import EventService
from ark_core.app.plugin_runtime import SubprocessPluginRuntime
from ark_core.app.state_service import StateEngineService
from ark_core.app.sync_service import SyncEngineService
from ark_core.baseline import SPEC_BASELINE_ID
from ark_core.ports.clock_port import ClockPort
from ark_core.ports.event_store_port import EventStorePort
from ark_core.ports.identity_port import IdentityPort
from ark_core.ports.signing_port import SigningPort


class CoreKernel:
    """Production Core composition root."""

    def __init__(
        self,
        *,
        grants: list[dict[str, Any]] | None = None,
        node_id: str = "edge-a",
        clock: ClockPort | None = None,
        identity: IdentityPort | None = None,
        store: EventStorePort | None = None,
        signing: SigningPort | None = None,
        require_signatures: bool = False,
    ) -> None:
        self.baseline_id = SPEC_BASELINE_ID
        self.clock = clock or SystemClock()
        self.identity = identity or MemoryIdentity()
        self.authorize = AuthorizeService(grants=grants)
        self.events = EventService(
            self.clock,
            store=store,
            signing=signing,
            require_signatures=require_signatures,
        )
        self.state = StateEngineService(self.events, self.authorize, self.clock)
        self.sync = SyncEngineService(self.events, self.identity, local_node_id=node_id)
        self.plugins = SubprocessPluginRuntime()

        def _publish(draft: dict[str, Any], plugin_id: str) -> dict[str, Any]:
            self.events.set_plugin_allowlist(
                plugin_id, set(self.plugins.publish_allowlist(plugin_id))
            )
            return self.events.append(draft, publisher_plugin_id=plugin_id)

        self.plugins.publish_callback = _publish
