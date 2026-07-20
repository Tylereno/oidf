from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from keel_reference.core.authorize import AuthorizePort
from keel_reference.core.events import EventEngine, new_id, utcnow
from keel_reference.schema import validate


@dataclass
class StateEngine:
    """Deterministic evidence-gated state transitions (RFC 0005)."""

    events: EventEngine
    authorize: AuthorizePort
    machines: dict[str, dict[str, Any]] = field(default_factory=dict)
    cdo_revision: int = 1
    config_revision: int = 1
    # subject_id -> current state
    _state: dict[str, str] = field(default_factory=dict)
    # evidence_id -> validated record
    _evidence: dict[str, dict[str, Any]] = field(default_factory=dict)
    # idempotency_key -> result event
    _idempotency: dict[str, dict[str, Any]] = field(default_factory=dict)

    def register_machine(self, machine: dict[str, Any]) -> None:
        validate("state/machine_definition.json", machine)
        self.machines[machine["id"]] = machine
        # note: subjects get initial state on first ensure

    def ensure_subject(self, subject_id: str, machine_id: str) -> None:
        if subject_id not in self._state:
            m = self.machines[machine_id]
            self._state[subject_id] = m["initial_state"]

    def current_state(self, subject_id: str) -> str | None:
        return self._state.get(subject_id)

    def ingest_event(self, event: dict[str, Any]) -> dict[str, Any]:
        """Project evidence and handle TransitionRequested."""
        stored = self.events.append(event)
        et = stored["type"]
        payload = stored["payload"]
        if et == "EvidenceValidated":
            self._evidence[payload["evidence_id"]] = payload
        elif et == "TransitionRequested":
            return self._handle_transition_requested(stored)
        return stored

    def _pins(self, machine: dict[str, Any]) -> dict[str, Any]:
        return {
            "cdo_revision": self.cdo_revision,
            "config_revision": self.config_revision,
            "machine_definition_version": machine["version"],
        }

    def _handle_transition_requested(self, req_event: dict[str, Any]) -> dict[str, Any]:
        p = req_event["payload"]
        validate("state/transition_requested.json", p)
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
            rejected = self._reject(req_event, p, None, "IdempotencyConflict", "key reused with different intent")
            return rejected

        machine = self._machine_for_subject(p["subject_id"])
        if machine is None:
            return self._reject(req_event, p, None, "MachineNotFound", "no machine for subject")

        auth = self.authorize.authorize(
            {
                "principal_id": req_event["actor_id"],
                "action": "transition.request",
                "resource": {"kind": p["subject_kind"], "id": p["subject_id"]},
            }
        )
        if auth["decision"] != "Allow":
            return self._reject(req_event, p, machine, "Unauthorized", "deny by default or no grant")

        current = self._state.get(p["subject_id"])
        if current is None:
            return self._reject(req_event, p, machine, "InvalidTransition", "unknown subject")
        if p["from_state"] != current:
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
            if e["subject_id"] == p["subject_id"]
        ]
        advanced = {
            "id": new_id("adv"),
            "type": "StateAdvanced",
            "spec_version": "1.0.0",
            "occurred_at": utcnow(),
            "recorded_at": utcnow(),
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
        # drop Nones for schema
        advanced = {k: v for k, v in advanced.items() if v is not None}
        validate("state/state_advanced.json", advanced["payload"])
        stored = self.events.append(advanced)
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
        rejected = {
            "id": new_id("rej"),
            "type": "TransitionRejected",
            "spec_version": "1.0.0",
            "occurred_at": utcnow(),
            "recorded_at": utcnow(),
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
        validate("state/transition_rejected.json", rejected["payload"])
        stored = self.events.append(rejected)
        # Only store idempotency for conflicts and successful paths;
        # for IdempotencyConflict we still record under key if not present
        if code == "IdempotencyConflict":
            pass
        elif p["idempotency_key"] not in self._idempotency:
            # first rejection for key — allow retry with same key after fixing evidence
            # per G2: identical intent returns original; we treat rejection as retryable
            # unless conflict. Do not lock key on MissingEvidence.
            pass
        return stored

    def _machine_for_subject(self, subject_id: str) -> dict[str, Any] | None:
        # reference maps one machine registered under subject via side table
        mid = self._subject_machine.get(subject_id) if hasattr(self, "_subject_machine") else None
        if mid:
            return self.machines.get(mid)
        # fallback: single machine
        if len(self.machines) == 1:
            return next(iter(self.machines.values()))
        return self.machines.get(getattr(self, "_default_machine_id", ""), None)

    def bind_subject(self, subject_id: str, machine_id: str) -> None:
        if not hasattr(self, "_subject_machine"):
            self._subject_machine = {}
        self._subject_machine[subject_id] = machine_id
        self.ensure_subject(subject_id, machine_id)

    def _find_transition(
        self, machine: dict[str, Any], tid: str, frm: str, to: str
    ) -> dict[str, Any] | None:
        for t in machine["transitions"]:
            if t["id"] == tid and t["from"] == frm and t["to"] == to:
                return t
        return None

    def _missing_evidence(self, subject_id: str, transition: dict[str, Any]) -> list[str]:
        missing: list[str] = []
        for req in transition.get("evidence_requirements", []):
            et = req["evidence_type"]
            need = req.get("min_count", 1)
            have = sum(
                1
                for e in self._evidence.values()
                if e["subject_id"] == subject_id and e["evidence_type"] == et
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
        """Rebuild projection from Event history (pure read of log)."""
        states: dict[str, str] = {}
        # rebuild from machines initial + StateAdvanced
        subject_machine = getattr(self, "_subject_machine", {})
        for sid, mid in subject_machine.items():
            states[sid] = self.machines[mid]["initial_state"]
        for e in self.events.events:
            if e["type"] == "StateAdvanced":
                p = e["payload"]
                states[p["subject_id"]] = p["to_state"]
        return states
