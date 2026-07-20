"""State Engine application service — RFC 0005 + ADR-0012/0013/0008."""

from __future__ import annotations

from datetime import datetime
from threading import Lock
from typing import Any, Optional

from keel_core.app.event_service import EventService
from keel_core.domain.errors import InvalidTransitionError
from keel_core.ports.authorize_port import AuthorizePort
from keel_core.ports.clock_port import ClockPort


def _parse_ts(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _graph_has_cycle(graph: dict[str, set[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(n: str) -> bool:
        if n in visiting:
            return True
        if n in visited:
            return False
        visiting.add(n)
        for m in graph.get(n, ()):
            if dfs(m):
                return True
        visiting.remove(n)
        visited.add(n)
        return False

    return any(dfs(n) for n in list(graph))


class StateEngineService:
    def __init__(
        self,
        events: EventService,
        authorize: AuthorizePort,
        clock: ClockPort,
        *,
        cdo_revision: int = 1,
        config_revision: int = 1,
    ) -> None:
        self._events = events
        self._authorize = authorize
        self._clock = clock
        self.cdo_revision = cdo_revision
        self.config_revision = config_revision
        self._machines: dict[str, dict[str, Any]] = {}
        self._subject_machine: dict[str, str] = {}
        self._state: dict[str, str] = {}
        self._evidence: dict[str, dict[str, Any]] = {}
        self._idempotency: dict[str, dict[str, Any]] = {}
        self._subject_locks: dict[str, Lock] = {}
        self._global = Lock()
        # explicit dependency edges asset->asset declared on transitions via owner_asset_id
        self._dep_edges: dict[str, set[str]] = {}

    def _lock_for(self, subject_id: str) -> Lock:
        with self._global:
            if subject_id not in self._subject_locks:
                self._subject_locks[subject_id] = Lock()
            return self._subject_locks[subject_id]

    def register_machine(self, machine_definition: dict[str, Any]) -> None:
        """Register machine; reject cyclic AssetStateIn graphs (ADR-0013).

        Transitions may set `dependency_owner_asset_id` to declare which asset
        owns the dependency edge for cycle detection at publish time.
        """
        provisional = {k: set(v) for k, v in self._dep_edges.items()}
        for t in machine_definition.get("transitions", []):
            owner = t.get("dependency_owner_asset_id")
            if not owner:
                continue
            for dep in t.get("dependencies", []):
                if dep.get("kind") == "AssetStateIn":
                    provisional.setdefault(owner, set()).add(dep["asset_id"])
        if _graph_has_cycle(provisional):
            raise InvalidTransitionError("cyclic AssetStateIn dependencies in MachineDefinition")
        self._machines[machine_definition["id"]] = machine_definition
        self._dep_edges = provisional

    def bind_subject(self, subject_id: str, machine_id: str) -> None:
        self._subject_machine[subject_id] = machine_id
        m = self._machines[machine_id]
        if subject_id not in self._state:
            self._state[subject_id] = m["initial_state"]

    def current_state(self, subject_id: str) -> Optional[str]:
        return self._state.get(subject_id)

    def ingest_event(self, event: dict[str, Any]) -> dict[str, Any]:
        stored = self._events.append(event)
        et = stored["type"]
        payload = stored["payload"]
        if et == "EvidenceValidated":
            self._evidence[payload["evidence_id"]] = payload
        elif et == "TransitionRequested":
            subject = payload["subject_id"]
            with self._lock_for(subject):
                return self._handle_transition_requested(stored)
        return stored

    def preview_transition(self, request_payload: dict[str, Any], actor_id: str) -> dict[str, Any]:
        fake = {"id": "preview", "actor_id": actor_id, "payload": request_payload}
        code = self._evaluate_only(fake)
        return {"ok": code is None, "reason_code": code}

    def _evaluate_only(self, req_event: dict[str, Any]) -> str | None:
        p = req_event["payload"]
        machine = self._machine_for(p["subject_id"])
        if machine is None:
            return "MachineNotFound"
        auth = self._authorize.authorize(
            {
                "principal_id": req_event["actor_id"],
                "action": "transition.request",
                "resource": {"kind": p["subject_kind"], "id": p["subject_id"]},
            }
        )
        if auth["decision"] != "Allow":
            return "Unauthorized"
        current = self._state.get(p["subject_id"])
        if current is None or p["from_state"] != current:
            return "InvalidTransition"
        transition = self._find_transition(machine, p["transition_id"], p["from_state"], p["to_state"])
        if transition is None:
            return "InvalidTransition"
        if self._missing_evidence(p["subject_id"], transition):
            return "MissingEvidence"
        if self._dependency_error(transition):
            return "DependencyUnsatisfied"
        return None

    def _pins(self, machine: dict[str, Any]) -> dict[str, Any]:
        return {
            "cdo_revision": self.cdo_revision,
            "config_revision": self.config_revision,
            "machine_definition_version": machine["version"],
        }

    def _handle_transition_requested(self, req_event: dict[str, Any]) -> dict[str, Any]:
        p = req_event["payload"]
        key = p["idempotency_key"]
        if key in self._idempotency:
            prev = self._idempotency[key]
            prev_p = prev["payload"]
            if (
                prev_p.get("transition_id") == p["transition_id"]
                and prev_p.get("to_state") == p["to_state"]
                and prev_p.get("from_state") == p["from_state"]
            ):
                return prev
            return self._reject(req_event, p, None, "IdempotencyConflict", "key reused with different intent")

        machine = self._machine_for(p["subject_id"])
        if machine is None:
            return self._reject(req_event, p, None, "MachineNotFound", "no machine")

        auth = self._authorize.authorize(
            {
                "principal_id": req_event["actor_id"],
                "action": "transition.request",
                "resource": {"kind": p["subject_kind"], "id": p["subject_id"]},
            }
        )
        if auth["decision"] != "Allow":
            return self._reject(req_event, p, machine, "Unauthorized", "deny by default or no grant")

        current = self._state.get(p["subject_id"])
        if current is None or p["from_state"] != current:
            return self._reject(req_event, p, machine, "InvalidTransition", f"current={current}")

        transition = self._find_transition(machine, p["transition_id"], p["from_state"], p["to_state"])
        if transition is None:
            return self._reject(req_event, p, machine, "InvalidTransition", "edge not in machine")

        missing = self._missing_evidence(p["subject_id"], transition)
        if missing:
            return self._reject(req_event, p, machine, "MissingEvidence", ",".join(missing))

        dep_err = self._dependency_error(transition)
        if dep_err:
            return self._reject(req_event, p, machine, "DependencyUnsatisfied", dep_err)

        satisfied = [
            e["evidence_id"]
            for e in self._evidence.values()
            if e["subject_id"] == p["subject_id"] and self._evidence_fresh(e)
        ]
        now = self._clock.now_rfc3339()
        advanced = {
            "id": EventService.new_id("adv"),
            "type": "StateAdvanced",
            "spec_version": "1.0.0",
            "occurred_at": now,
            "recorded_at": now,
            "actor_id": req_event["actor_id"],
            "deployment_id": req_event.get("deployment_id"),
            "asset_id": p["subject_id"] if p["subject_kind"] == "Asset" else req_event.get("asset_id"),
            "caused_by_event_id": req_event["id"],
            "correlation_id": req_event.get("correlation_id", req_event["id"]),
            "payload": {
                "subject_kind": p["subject_kind"],
                "subject_id": p["subject_id"],
                "transition_id": p["transition_id"],
                "from_state": p["from_state"],
                "to_state": p["to_state"],
                "pins": self._pins(machine),
                "idempotency_key": key,
                "satisfied_evidence_ids": satisfied,
            },
        }
        advanced = {k: v for k, v in advanced.items() if v is not None}
        stored = self._events.append(advanced)
        self._state[p["subject_id"]] = p["to_state"]
        self._idempotency[key] = stored
        return stored

    def _reject(
        self,
        req_event: dict[str, Any],
        p: dict[str, Any],
        machine: dict[str, Any] | None,
        code: str,
        detail: str,
    ) -> dict[str, Any]:
        pins = (
            self._pins(machine)
            if machine
            else {"cdo_revision": self.cdo_revision, "config_revision": self.config_revision}
        )
        now = self._clock.now_rfc3339()
        rejected = {
            "id": EventService.new_id("rej"),
            "type": "TransitionRejected",
            "spec_version": "1.0.0",
            "occurred_at": now,
            "recorded_at": now,
            "actor_id": req_event["actor_id"],
            "deployment_id": req_event.get("deployment_id"),
            "asset_id": p["subject_id"] if p.get("subject_kind") == "Asset" else req_event.get("asset_id"),
            "caused_by_event_id": req_event["id"],
            "correlation_id": req_event.get("correlation_id", req_event["id"]),
            "payload": {
                "subject_kind": p["subject_kind"],
                "subject_id": p["subject_id"],
                "transition_id": p["transition_id"],
                "from_state": p["from_state"],
                "to_state": p["to_state"],
                "reason_code": code,
                "reason_detail": detail,
                "pins": pins,
                "idempotency_key": p["idempotency_key"],
            },
        }
        rejected = {k: v for k, v in rejected.items() if v is not None}
        return self._events.append(rejected)

    def _machine_for(self, subject_id: str) -> dict[str, Any] | None:
        mid = self._subject_machine.get(subject_id)
        if mid:
            return self._machines.get(mid)
        if len(self._machines) == 1:
            return next(iter(self._machines.values()))
        return None

    def _find_transition(
        self, machine: dict[str, Any], tid: str, frm: str, to: str
    ) -> dict[str, Any] | None:
        for t in machine["transitions"]:
            if t["id"] == tid and t["from"] == frm and t["to"] == to:
                return t
        return None

    def _evidence_fresh(self, ev: dict[str, Any]) -> bool:
        now = _parse_ts(self._clock.now_rfc3339())
        frm = ev.get("valid_from")
        until = ev.get("valid_until")
        if frm and now < _parse_ts(frm):
            return False
        if until and now > _parse_ts(until):
            return False
        return True

    def _missing_evidence(self, subject_id: str, transition: dict[str, Any]) -> list[str]:
        missing: list[str] = []
        for req in transition.get("evidence_requirements", []):
            et = req["evidence_type"]
            need = req.get("min_count", 1)
            have = sum(
                1
                for e in self._evidence.values()
                if e["subject_id"] == subject_id
                and e["evidence_type"] == et
                and self._evidence_fresh(e)
            )
            if have < need:
                missing.append(et)
        return missing

    def _dependency_error(self, transition: dict[str, Any]) -> str | None:
        for dep in transition.get("dependencies", []):
            kind = dep["kind"]
            if kind == "AssetStateIn":
                aid = dep["asset_id"]
                allowed = set(dep.get("allowed_states", []))
                cur = self._state.get(aid)
                if cur not in allowed:
                    return f"AssetStateIn:{aid}:{cur}"
            elif kind == "DeploymentStateIn":
                did = dep["deployment_id"]
                allowed = set(dep.get("allowed_states", []))
                cur = self._state.get(did)
                if cur not in allowed:
                    return f"DeploymentStateIn:{did}:{cur}"
            elif kind == "CdoRevisionPinned":
                if dep.get("cdo_revision") != self.cdo_revision:
                    return "CdoRevisionPinned"
        return None

    def replay(self) -> dict[str, str]:
        states: dict[str, str] = {}
        for sid, mid in self._subject_machine.items():
            states[sid] = self._machines[mid]["initial_state"]
        for e in self._events.all_events():
            if e["type"] == "StateAdvanced":
                p = e["payload"]
                states[p["subject_id"]] = p["to_state"]
        return states
