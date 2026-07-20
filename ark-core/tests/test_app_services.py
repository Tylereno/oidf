from __future__ import annotations

import pytest

from ark_core.app.event_service import EventService
from ark_core.app.kernel import CoreKernel
from ark_core.adapters.memory import FixedClock, MemoryIdentity
from ark_core.baseline import SPEC_BASELINE_ID
from ark_core.domain.errors import InvalidTransitionError, PluginAllowlistError

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
        }
    ],
}


def envelope(etype, actor, payload, **subj):
    e = {
        "id": EventService.new_id("evt"),
        "type": etype,
        "spec_version": "1.0.0",
        "occurred_at": "2026-07-20T00:00:00.000000Z",
        "recorded_at": "2026-07-20T00:00:00.000000Z",
        "actor_id": actor,
        "payload": payload,
    }
    e.update({k: v for k, v in subj.items() if v is not None})
    return e


@pytest.fixture
def kernel():
    k = CoreKernel(grants=[{"principal_id": "P1", "actions": ["transition.request"]}])
    k.state.register_machine(ASSET_MACHINE)
    k.state.bind_subject("A1", "asset.switchgear.v1")
    return k


def validate_evidence(k, eid="evd-1", **extra):
    payload = {
        "evidence_id": eid,
        "evidence_type": "InspectionPass",
        "subject_kind": "Asset",
        "subject_id": "A1",
        "validator_id": "validator-1",
    }
    payload.update(extra)
    return k.state.ingest_event(
        envelope("EvidenceValidated", "validator-1", payload, asset_id="A1", deployment_id="DEP-1")
    )


def request_transition(k, key="K1", actor="P1", **overrides):
    payload = {
        "subject_kind": "Asset",
        "subject_id": "A1",
        "transition_id": "install_to_commission",
        "from_state": "Installed",
        "to_state": "Commissioned",
        "idempotency_key": key,
    }
    payload.update(overrides)
    return k.state.ingest_event(
        envelope("TransitionRequested", actor, payload, asset_id="A1", deployment_id="DEP-1")
    )


def test_baseline_id(kernel):
    assert kernel.baseline_id == SPEC_BASELINE_ID


def test_ts_missing_evidence(kernel):
    r = request_transition(kernel, key="miss")
    assert r["type"] == "TransitionRejected"
    assert r["payload"]["reason_code"] == "MissingEvidence"


def test_ts_advance_and_pins(kernel):
    validate_evidence(kernel)
    r = request_transition(kernel, key="ok")
    assert r["type"] == "StateAdvanced"
    assert r["payload"]["pins"]["cdo_revision"] == 1
    assert kernel.state.current_state("A1") == "Commissioned"


def test_submitted_alone_insufficient(kernel):
    # ADR-0012: EvidenceSubmitted does not satisfy gates
    kernel.state.ingest_event(
        envelope(
            "EvidenceSubmitted",
            "P1",
            {
                "evidence_id": "evd-x",
                "evidence_type": "InspectionPass",
                "subject_kind": "Asset",
                "subject_id": "A1",
            },
            asset_id="A1",
        )
    )
    r = request_transition(kernel, key="sub-only")
    assert r["payload"]["reason_code"] == "MissingEvidence"


def test_stale_evidence_rejected():
    clock = FixedClock("2026-07-20T12:00:00.000000Z")
    k = CoreKernel(
        grants=[{"principal_id": "P1", "actions": ["transition.request"]}],
        clock=clock,
    )
    k.state.register_machine(ASSET_MACHINE)
    k.state.bind_subject("A1", "asset.switchgear.v1")
    validate_evidence(k, valid_until="2026-07-19T00:00:00.000000Z")
    r = request_transition(k, key="stale")
    assert r["payload"]["reason_code"] == "MissingEvidence"


def test_idempotent(kernel):
    validate_evidence(kernel)
    a = request_transition(kernel, key="K1")
    b = request_transition(kernel, key="K1")
    assert a["id"] == b["id"]


def test_unauthorized(kernel):
    validate_evidence(kernel)
    r = request_transition(kernel, key="u", actor="NOPE")
    assert r["payload"]["reason_code"] == "Unauthorized"


def test_deny_by_default():
    k = CoreKernel(grants=[])
    d = k.authorize.authorize(
        {
            "principal_id": "P1",
            "action": "transition.request",
            "resource": {"kind": "Asset", "id": "A1"},
        }
    )
    assert d["decision"] == "Deny"


def test_replay(kernel):
    validate_evidence(kernel)
    request_transition(kernel, key="rp")
    assert kernel.state.replay()["A1"] == "Commissioned"


def test_cyclic_machine_rejected(kernel):
    cyclic = {
        "id": "cyclic",
        "version": "1",
        "subject_kind": "Asset",
        "initial_state": "A",
        "states": ["A", "B"],
        "transitions": [
            {
                "id": "t1",
                "from": "A",
                "to": "B",
                "dependency_owner_asset_id": "X",
                "dependencies": [{"kind": "AssetStateIn", "asset_id": "Y", "allowed_states": ["B"]}],
            },
            {
                "id": "t2",
                "from": "A",
                "to": "B",
                "dependency_owner_asset_id": "Y",
                "dependencies": [{"kind": "AssetStateIn", "asset_id": "X", "allowed_states": ["B"]}],
            },
        ],
    }
    with pytest.raises(InvalidTransitionError):
        kernel.state.register_machine(cyclic)


def test_plugin_allowlist(kernel):
    kernel.events.set_plugin_allowlist("plug-a", {"TelemetryReceived"})
    with pytest.raises(PluginAllowlistError):
        kernel.events.append(
            envelope("StateAdvanced", "plug-a", {"x": 1}),
            publisher_plugin_id="plug-a",
        )


def test_sync_cdo_quarantine(kernel):
    kernel.sync.local_cdo_hashes[("DEP-1", 1)] = "local"
    r = kernel.sync.import_batch(
        {
            "batch_id": "b",
            "sender_node_id": "edge-b",
            "protocol_version": "1.0.0",
            "events": [],
            "cdo_revisions": [{"deployment_id": "DEP-1", "revision": 1, "content_hash": "other"}],
            "content_hash": "h",
        }
    )
    assert r["status"] == "quarantined"


def test_sync_revoked_node(kernel):
    identity = kernel.identity
    assert isinstance(identity, MemoryIdentity)
    identity.revoked.add("evil")
    r = kernel.sync.import_batch(
        {
            "batch_id": "b",
            "sender_node_id": "evil",
            "protocol_version": "1.0.0",
            "events": [],
            "content_hash": "h",
        }
    )
    assert r["reason"] == "NodeRevoked"


def test_fencing_skips_stale_epoch(kernel):
    kernel.sync.set_affinity("DEP-1", "edge-a", epoch=5)
    validate_evidence(kernel)
    adv = request_transition(kernel, key="fence")
    # import same advance from non-primary with stale epoch
    k2 = CoreKernel(node_id="edge-b")
    k2.sync.set_affinity("DEP-1", "edge-a", epoch=5)
    batch = {
        "batch_id": "bx",
        "sender_node_id": "edge-b",
        "protocol_version": "1.0.0",
        "events": [adv],
        "affinity_epochs": {"DEP-1": 4},
        "content_hash": "h",
    }
    r = k2.sync.import_batch(batch)
    assert r["status"] == "ok"
    assert r["fenced_skipped"] == 1
