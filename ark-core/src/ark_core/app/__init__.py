"""Phase 6 application services — production Core logic behind ports.

No concrete infrastructure adapters (Postgres/NATS/MQTT/cloud).
In-memory doubles live under ark_core.adapters.memory for tests/dev only.
"""

from ark_core.app.authorize_service import AuthorizeService
from ark_core.app.event_service import EventService
from ark_core.app.kernel import CoreKernel
from ark_core.app.plugin_runtime import SubprocessPluginRuntime
from ark_core.app.state_service import StateEngineService
from ark_core.app.sync_service import SyncEngineService

__all__ = [
    "AuthorizeService",
    "EventService",
    "StateEngineService",
    "SyncEngineService",
    "SubprocessPluginRuntime",
    "CoreKernel",
]
