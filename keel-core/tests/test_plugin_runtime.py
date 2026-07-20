from __future__ import annotations

from pathlib import Path

import pytest

from keel_core.app.kernel import CoreKernel

DESCRIPTOR = {
    "plugin_id": "keel-evidence",
    "plugin_version": "0.1.0",
    "capabilities": ["evidence.validate"],
    "publishes": ["EvidenceValidated", "EvidenceRejected"],
    "subscribes": ["EvidenceSubmitted"],
    "config_keys": ["allowed_evidence_types"],
}


@pytest.fixture
def plugins_path() -> str:
    return str(Path(__file__).resolve().parents[2] / "keel-plugins")


def test_keel_evidence_subprocess(plugins_path: str):
    k = CoreKernel(grants=[{"principal_id": "P1", "actions": ["transition.request"]}])
    k.plugins.extra_pythonpath.append(plugins_path)
    k.plugins.register(DESCRIPTOR)
    k.plugins.start("keel-evidence", "keel_evidence")
    try:
        health = k.plugins.health("keel-evidence")
        assert health["alive"] is True
        submitted = {
            "id": "evt-sub-1",
            "type": "EvidenceSubmitted",
            "spec_version": "1.0.0",
            "occurred_at": "2026-07-20T00:00:00Z",
            "recorded_at": "2026-07-20T00:00:00Z",
            "actor_id": "P1",
            "asset_id": "A1",
            "deployment_id": "DEP-1",
            "payload": {
                "evidence_id": "evd-1",
                "evidence_type": "InspectionPass",
                "subject_kind": "Asset",
                "subject_id": "A1",
            },
        }
        k.events.append(submitted)
        published = k.plugins.dispatch_event("keel-evidence", submitted)
        assert len(published) == 1
        assert published[0]["type"] == "EvidenceValidated"
        assert published[0]["payload"]["evidence_id"] == "evd-1"
        # allowlist prevents privileged publish
        k.events.set_plugin_allowlist("keel-evidence", set(DESCRIPTOR["publishes"]))
    finally:
        k.plugins.stop("keel-evidence")


def test_plugin_quarantine_on_bad_module(plugins_path: str):
    k = CoreKernel()
    k.plugins.extra_pythonpath.append(plugins_path)
    k.plugins.register(
        {
            "plugin_id": "bad",
            "plugin_version": "0",
            "capabilities": [],
            "publishes": [],
            "subscribes": [],
        }
    )
    with pytest.raises(RuntimeError):
        k.plugins.start("bad", "does_not_exist_module_zz")
    assert k.plugins.health("bad")["quarantined"] is True
