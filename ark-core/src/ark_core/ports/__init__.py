"""Outbound/inbound ports for ARK Core (Hexagonal).

These Protocols are the only I/O boundary Core application services may use.
Concrete adapters (DB, broker, cloud) are forbidden in this scaffold phase.
Schemas: ark-specs/idl/ (ADR-0011).
"""

from ark_core.ports.authorize_port import AuthorizePort
from ark_core.ports.clock_port import ClockPort
from ark_core.ports.config_port import ConfigPort
from ark_core.ports.event_port import EventPort
from ark_core.ports.event_store_port import EventStorePort
from ark_core.ports.identity_port import IdentityPort
from ark_core.ports.plugin_runtime_port import PluginRuntimePort
from ark_core.ports.signing_port import SigningPort
from ark_core.ports.state_port import StateEnginePort
from ark_core.ports.sync_port import SyncEnginePort

__all__ = [
    "EventPort",
    "EventStorePort",
    "StateEnginePort",
    "PluginRuntimePort",
    "SyncEnginePort",
    "IdentityPort",
    "AuthorizePort",
    "ConfigPort",
    "ClockPort",
    "SigningPort",
]
