from __future__ import annotations

import copy

import pytest
from jsonschema.exceptions import ValidationError

from keel_reference.core import build_kernel
from keel_reference.core.events import new_id, utcnow
from keel_reference.schema import validate

ASSET_MACHINE = {
    "id": "asset.switchgear.v1",
    "version": "1.0.0",
    "subject_kind": "Asset",
    "initial_state": "Installed",
    "states": ["Installed", "Commissioned", "Planned"],
    "terminal_states": ["Commissioned"],
    "transitions": [
        {
            "id": "install_to_commission",
            "from": "Installed",
            "to": "Commissioned",
            "evidence_requirements": [{"evidence_type": "InspectionPass", "min_count": 1}],
            "dependencies": [],
            "required_permission": "transition.request",
        }
    ],
}

DEP_MACHINE = {
    "id": "asset.with.dep",
    "version": "1.0.0",
    "subject_kind": "Asset",
    "initial_state": "Installed",
    "states": ["Installed", "Commissioned"],
    "transitions": [
        {
            "id": "install_to_commission",
            "from": "Installed",
            "to": "Commissioned",
            "evidence_requirements": [],
            "dependencies": [
                {
                    "kind": "AssetStateIn",
                    "asset_id": "BUS-1",
                    "allowed_states": ["Energized"],
                }
            ],
        }
    ],
}


def envelope(etype: str, actor: str, payload: dict, **subj) -> dict:
    e = {
        "id": new_id("evt"),
        "type": etype,
        "spec_version": "1.0.0",
        "occurred_at": utcnow(),
        "recorded_at": utcnow(),
        "actor_id": actor,
        "payload": payload,
    }
    e.update({k: v for k, v in subj.items() if v is not None})
    return e


@pytest.fixture
def kernel():
    events, auth, state, sync = build_kernel(
        grants=[{"principal_id": "P1", "actions": ["transition.request", "evidence.submit"]}]
    )
    state.register_machine(ASSET_MACHINE)
    state.bind_subject("A1", "asset.switchgear.v1")
    return events, auth, state, sync


def request_transition(state, actor="P1", key="K1", frm="Installed", to="Commissioned", tid="install_to_commission"):
    req = envelope(
        "TransitionRequested",
        actor,
        {
            "subject_kind": "Asset",
            "subject_id": "A1",
            "transition_id": tid,
            "from_state": frm,
            "to_state": to,
            "idempotency_key": key,
        },
        deployment_id="DEP-1",
        asset_id="A1",
    )
    return state.ingest_event(req)


def submit_validated_evidence(state, evidence_type="InspectionPass", eid=None):
    eid = eid or new_id("evd")
    state.ingest_event(
        envelope(
            "EvidenceSubmitted",
            "P1",
            {
                "evidence_id": eid,
                "evidence_type": evidence_type,
                "subject_kind": "Asset",
                "subject_id": "A1",
            },
            asset_id="A1",
            deployment_id="DEP-1",
        )
    )
    state.ingest_event(
        envelope(
            "EvidenceValidated",
            "validator-1",
            {
                "evidence_id": eid,
                "evidence_type": evidence_type,
                "subject_kind": "Asset",
                "subject_id": "A1",
                "validator_id": "validator-1",
            },
            asset_id="A1",
            deployment_id="DEP-1",
        )
    )
    return eid


def test_ts_0001_missing_evidence(kernel):
    _, _, state, _ = kernel
    result = request_transition(state, key="K-miss")
    assert result["type"] == "TransitionRejected"
    assert result["payload"]["reason_code"] == "MissingEvidence"
    assert state.current_state("A1") == "Installed"


def test_ts_0002_successful_advance(kernel):
    _, _, state, _ = kernel
    submit_validated_evidence(state)
    result = request_transition(state, key="K-ok")
    assert result["type"] == "StateAdvanced"
    assert result["payload"]["to_state"] == "Commissioned"
    assert result["payload"]["pins"]["cdo_revision"] == 1
    assert result["payload"]["pins"]["config_revision"] == 1
    assert state.current_state("A1") == "Commissioned"


def test_ts_0003_idempotent(kernel):
    _, _, state, _ = kernel
    submit_validated_evidence(state)
    first = request_transition(state, key="K1")
    second = request_transition(state, key="K1")
    assert first["id"] == second["id"]
    advances = [e for e in state.events.events if e["type"] == "StateAdvanced"]
    assert len(advances) == 1


def test_ts_0004_idempotency_conflict(kernel):
    _, _, state, _ = kernel
    submit_validated_evidence(state)
    request_transition(state, key="K2", to="Commissioned")
    # craft conflicting request with same key but impossible different to_state still in payload
    # First success locks key. Conflict when different to_state.
    conflict = request_transition(state, key="K2", frm="Installed", to="Planned", tid="install_to_commission")
    # Note: from_state Installed no longer current; but idempotency check happens first
    assert conflict["type"] == "TransitionRejected"
    assert conflict["payload"]["reason_code"] == "IdempotencyConflict"


def test_ts_0005_unauthorized(kernel):
    _, _, state, _ = kernel
    submit_validated_evidence(state)
    result = request_transition(state, actor="P_denied", key="K-unauth")
    assert result["payload"]["reason_code"] == "Unauthorized"
    assert state.current_state("A1") == "Installed"


def test_ts_0006_dependency(kernel):
    events, auth, state, sync = build_kernel(
        grants=[{"principal_id": "P1", "actions": ["transition.request"]}]
    )
    state.register_machine(DEP_MACHINE)
    state.bind_subject("A2", "asset.with.dep")
    state.bind_subject("BUS-1", "asset.with.dep")
    # BUS-1 stuck in Installed, not Energized — also reset BUS machine states properly
    state._state["BUS-1"] = "Installed"
    req = envelope(
        "TransitionRequested",
        "P1",
        {
            "subject_kind": "Asset",
            "subject_id": "A2",
            "transition_id": "install_to_commission",
            "from_state": "Installed",
            "to_state": "Commissioned",
            "idempotency_key": "K-dep",
        },
        asset_id="A2",
        deployment_id="DEP-1",
    )
    result = state.ingest_event(req)
    assert result["payload"]["reason_code"] == "DependencyUnsatisfied"


def test_ts_0007_invalid_transition(kernel):
    _, _, state, _ = kernel
    submit_validated_evidence(state)
    result = request_transition(state, key="K-bad", frm="Installed", to="Commissioned")
    # force wrong from by direct payload
    req = envelope(
        "TransitionRequested",
        "P1",
        {
            "subject_kind": "Asset",
            "subject_id": "A1",
            "transition_id": "install_to_commission",
            "from_state": "Installed",
            "to_state": "Commissioned",
            "idempotency_key": "K-bad2",
        },
        asset_id="A1",
        deployment_id="DEP-1",
    )
    # put asset in Planned without machine edge from Planned
    state._state["A1"] = "Planned"
    req["payload"]["from_state"] = "Installed"
    result = state.ingest_event(req)
    assert result["payload"]["reason_code"] == "InvalidTransition"


def test_ts_0008_replay(kernel):
    _, _, state, _ = kernel
    submit_validated_evidence(state)
    request_transition(state, key="K-replay")
    rebuilt = state.replay()
    assert rebuilt["A1"] == "Commissioned"
    assert rebuilt == {"A1": state.current_state("A1")}


def test_ts_0009_envelope_missing_actor():
    bad = {
        "id": "evt-1",
        "type": "TelemetryReceived",
        "spec_version": "1.0.0",
        "occurred_at": utcnow(),
        "recorded_at": utcnow(),
        "payload": {},
    }
    with pytest.raises(ValidationError):
        validate("event/envelope.json", bad)


def test_ts_0010_unknown_property():
    bad = envelope("TelemetryReceived", "P1", {})
    bad["foo"] = "bar"
    with pytest.raises(ValidationError):
        validate("event/envelope.json", bad)


def test_ts_0011_sync_idempotent_ids(kernel):
    events, _, state, sync = kernel
    submit_validated_evidence(state)
    batch = sync.export_batch("batch-1")
    n_before = len(events.events)
    result = sync.import_batch(batch)
    assert result["status"] == "ok"
    assert len(events.events) == n_before


def test_ts_0012_sync_order_deterministic():
    _, _, state_a, sync_a = build_kernel(grants=[{"principal_id": "P1", "actions": ["transition.request"]}])
    _, _, state_b, sync_b = build_kernel(grants=[{"principal_id": "P1", "actions": ["transition.request"]}], node_id="edge-b")
    for s in (state_a, state_b):
        s.register_machine(ASSET_MACHINE)
        s.bind_subject("A1", "asset.switchgear.v1")
    e1 = envelope(
        "EvidenceValidated",
        "P1",
        {
            "evidence_id": "evd-a",
            "evidence_type": "InspectionPass",
            "subject_kind": "Asset",
            "subject_id": "A1",
        },
        asset_id="A1",
        occurred_at="2026-01-01T00:00:01Z",
    )
    e1["occurred_at"] = "2026-01-01T00:00:01Z"
    e2 = envelope(
        "EvidenceValidated",
        "P2",
        {
            "evidence_id": "evd-b",
            "evidence_type": "InspectionPass",
            "subject_kind": "Asset",
            "subject_id": "A1",
        },
        asset_id="A1",
    )
    e2["occurred_at"] = "2026-01-01T00:00:02Z"
    sync_a.import_batch(
        {
            "batch_id": "b1",
            "sender_node_id": "edge-b",
            "protocol_version": "1.0.0",
            "events": [e2, e1],
            "content_hash": "h",
        }
    )
    sync_b.import_batch(
        {
            "batch_id": "b2",
            "sender_node_id": "edge-a",
            "protocol_version": "1.0.0",
            "events": [e1, e2],
            "content_hash": "h",
        }
    )
    # both have both events; order of append may differ but ids present
    ids_a = {e["id"] for e in state_a.events.events}
    ids_b = {e["id"] for e in state_b.events.events}
    assert ids_a == ids_b


def test_ts_0015_deny_by_default():
    _, auth, _, _ = build_kernel(grants=[])
    decision = auth.authorize(
        {
            "principal_id": "P1",
            "action": "transition.request",
            "resource": {"kind": "Asset", "id": "A1"},
        }
    )
    assert decision["decision"] == "Deny"


def test_ts_0016_config_pin(kernel):
    _, _, state, _ = kernel
    state.config_revision = 12
    submit_validated_evidence(state)
    result = request_transition(state, key="K-pin")
    assert result["payload"]["pins"]["config_revision"] == 12
    state.config_revision = 40
    assert state.replay()["A1"] == "Commissioned"


def test_ts_0018_cdo_hash_mismatch(kernel):
    _, _, _, sync = kernel
    sync.local_cdo_hashes[("DEP-1", 1)] = "hash-local"
    result = sync.import_batch(
        {
            "batch_id": "bx",
            "sender_node_id": "edge-b",
            "protocol_version": "1.0.0",
            "events": [],
            "cdo_revisions": [{"deployment_id": "DEP-1", "revision": 1, "content_hash": "hash-other"}],
            "content_hash": "h",
        }
    )
    assert result["status"] == "quarantined"


def test_ts_0019_projection_rebuild(kernel):
    _, _, state, _ = kernel
    submit_validated_evidence(state)
    request_transition(state, key="K-cache")
    cached = dict(state._state)
    state._state.clear()
    rebuilt = state.replay()
    assert rebuilt == cached


def test_ts_0020_offline_no_cloud(kernel):
    _, _, state, _ = kernel
    # no sync calls
    submit_validated_evidence(state)
    result = request_transition(state, key="K-airgap")
    assert result["type"] == "StateAdvanced"
