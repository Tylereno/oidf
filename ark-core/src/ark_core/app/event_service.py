"""Event Engine application service — RFC 0006, ADR-0016, ADR-0017."""

from __future__ import annotations

from threading import Lock
from typing import Any, Iterable, Optional
from uuid import uuid4

from ark_core.domain.errors import PluginAllowlistError
from ark_core.ports.clock_port import ClockPort
from ark_core.ports.event_store_port import EventStorePort
from ark_core.ports.signing_port import SigningPort


class MemoryEventStore:
    """Ephemeral store (tests)."""

    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []
        self._by_id: dict[str, dict[str, Any]] = {}

    def load_all(self) -> list[dict[str, Any]]:
        return list(self._events)

    def append_persisted(self, event: dict[str, Any]) -> None:
        self._events.append(event)
        self._by_id[event["id"]] = event

    def get(self, event_id: str) -> Optional[dict[str, Any]]:
        return self._by_id.get(event_id)


class EventService:
    """Event Engine logic. Durability via EventStorePort; signing via SigningPort."""

    CORE_PRIVILEGED_TYPES = frozenset({"StateAdvanced", "TransitionRejected"})

    def __init__(
        self,
        clock: ClockPort,
        *,
        store: EventStorePort | None = None,
        signing: SigningPort | None = None,
        require_signatures: bool = False,
        plugin_allowlists: dict[str, set[str]] | None = None,
    ) -> None:
        self._clock = clock
        self._store: EventStorePort = store or MemoryEventStore()
        self._signing = signing
        self._require_signatures = require_signatures
        self._events: list[dict[str, Any]] = []
        self._by_id: dict[str, dict[str, Any]] = {}
        self._sequences: dict[str, int] = {}
        self._lock = Lock()
        self._plugin_allowlists = plugin_allowlists or {}
        self._reload_from_store()

    def _reload_from_store(self) -> None:
        self._events = []
        self._by_id = {}
        self._sequences = {}
        for e in self._store.load_all():
            self._index(e)

    def _index(self, stored: dict[str, Any]) -> None:
        self._events.append(stored)
        self._by_id[stored["id"]] = stored
        subject = stored.get("asset_id") or stored.get("deployment_id") or "_global"
        seq = int(stored.get("sequence", 0))
        self._sequences[subject] = max(self._sequences.get(subject, 0), seq)

    def set_plugin_allowlist(self, plugin_id: str, types: set[str]) -> None:
        self._plugin_allowlists[plugin_id] = set(types)

    def append(self, event: dict[str, Any], *, publisher_plugin_id: Optional[str] = None) -> dict[str, Any]:
        if publisher_plugin_id is not None:
            allowed = self._plugin_allowlists.get(publisher_plugin_id, set())
            et = event.get("type")
            if et not in allowed:
                raise PluginAllowlistError(
                    f"plugin {publisher_plugin_id} may not publish {et}"
                )

        with self._lock:
            eid = event["id"]
            if eid in self._by_id:
                return self._by_id[eid]
            subject = event.get("asset_id") or event.get("deployment_id") or "_global"
            seq = self._sequences.get(subject, 0) + 1
            self._sequences[subject] = seq
            stored = dict(event)
            stored["sequence"] = seq
            if "recorded_at" not in stored:
                stored["recorded_at"] = self._clock.now_rfc3339()

            if self._signing is not None:
                ph = self._signing.payload_hash(stored.get("payload") or {})
                stored["payload_hash"] = ph
                actor = stored.get("actor_id")
                if self._require_signatures or "signature" in event:
                    if not actor or not self._signing.has_key(actor):
                        if self._require_signatures:
                            raise PermissionError(f"missing signing key for {actor}")
                    else:
                        stored["signature"] = event.get("signature") or self._signing.sign(actor, ph)
                        if not self._signing.verify(actor, ph, stored["signature"]):
                            raise PermissionError("invalid event signature")

            self._store.append_persisted(stored)
            self._index(stored)
            return stored

    def read(self, *, subject_key: Optional[str] = None, after_sequence: int = 0) -> Iterable[dict[str, Any]]:
        for e in self._events:
            if subject_key is not None:
                sk = e.get("asset_id") or e.get("deployment_id") or "_global"
                if sk != subject_key:
                    continue
            if int(e.get("sequence", 0)) <= after_sequence:
                continue
            yield e

    def get(self, event_id: str) -> Optional[dict[str, Any]]:
        return self._by_id.get(event_id)

    def all_events(self) -> list[dict[str, Any]]:
        return list(self._events)

    @staticmethod
    def new_id(prefix: str = "evt") -> str:
        return f"{prefix}-{uuid4().hex[:12]}"
