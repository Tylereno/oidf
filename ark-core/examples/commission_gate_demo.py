#!/usr/bin/env python3
"""Commissioning gate demo — Evidence Packet artifact.

Shows Principle 4 in ~60 seconds of terminal output:

  1. Attempt Installed → Commissioned without TorqueVerified → MissingEvidence
  2. Submit-only Evidence does not satisfy the gate (ADR-0012)
  3. EvidenceValidated for TorqueVerified
  4. Same transition succeeds → StateAdvanced; asset is Commissioned

Run from repo root:

  pip install -e ark-core
  python ark-core/examples/commission_gate_demo.py
"""

from __future__ import annotations

import json
import sys
from typing import Any

from ark_core.app.event_service import EventService
from ark_core.app.kernel import CoreKernel

DEPLOYMENT_ID = "DEP-BESS-01"
ASSET_ID = "SWGR-A1"
MACHINE_ID = "asset.switchgear.commission.v1"

MACHINE = {
    "id": MACHINE_ID,
    "version": "1.0.0",
    "subject_kind": "Asset",
    "initial_state": "Installed",
    "states": ["Installed", "Commissioned"],
    "terminal_states": ["Commissioned"],
    "transitions": [
        {
            "id": "install_to_commission",
            "from": "Installed",
            "to": "Commissioned",
            "evidence_requirements": [
                {"evidence_type": "TorqueVerified", "min_count": 1},
            ],
            "dependencies": [],
        }
    ],
}


def _banner(title: str) -> None:
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def _show(label: str, event: dict[str, Any]) -> None:
    payload = event.get("payload") or {}
    summary = {
        "type": event.get("type"),
        "reason_code": payload.get("reason_code"),
        "missing": payload.get("reason_detail"),
        "to_state": payload.get("to_state"),
        "pins": payload.get("pins"),
    }
    # Drop empty keys for readable asciinema output
    summary = {k: v for k, v in summary.items() if v is not None}
    print(f"\n{label}")
    print(json.dumps(summary, indent=2, sort_keys=True))


def _envelope(
    etype: str,
    actor: str,
    payload: dict[str, Any],
    *,
    asset_id: str = ASSET_ID,
    deployment_id: str = DEPLOYMENT_ID,
) -> dict[str, Any]:
    event = {
        "id": EventService.new_id("evt"),
        "type": etype,
        "spec_version": "1.0.0",
        "occurred_at": "2026-07-20T15:00:00.000000Z",
        "recorded_at": "2026-07-20T15:00:00.000000Z",
        "actor_id": actor,
        "payload": payload,
        "asset_id": asset_id,
        "deployment_id": deployment_id,
    }
    return event


def _request(kernel: CoreKernel, key: str, actor: str = "commissioner-1") -> dict[str, Any]:
    return kernel.state.ingest_event(
        _envelope(
            "TransitionRequested",
            actor,
            {
                "subject_kind": "Asset",
                "subject_id": ASSET_ID,
                "transition_id": "install_to_commission",
                "from_state": "Installed",
                "to_state": "Commissioned",
                "idempotency_key": key,
            },
        )
    )


def main() -> int:
    kernel = CoreKernel(
        grants=[{"principal_id": "commissioner-1", "actions": ["transition.request"]}],
        node_id="edge-yard-01",
    )
    kernel.state.register_machine(MACHINE)
    kernel.state.bind_subject(ASSET_ID, MACHINE_ID)

    _banner("ARK commissioning gate demo")
    print(f"Baseline:     {kernel.baseline_id}")
    print(f"Deployment:   {DEPLOYMENT_ID}")
    print(f"Asset:        {ASSET_ID} (switchgear)")
    print(f"Machine:      {MACHINE_ID}")
    print(f"Current state:{kernel.state.current_state(ASSET_ID)}")
    print("Rule:         Installed → Commissioned requires TorqueVerified")
    print("Principle 4:  Nothing advances because a user clicked a button.")

    _banner("Step 1 — Transition without evidence")
    rejected = _request(kernel, key="attempt-no-evidence")
    _show("Result:", rejected)
    assert rejected["type"] == "TransitionRejected"
    assert rejected["payload"]["reason_code"] == "MissingEvidence"
    assert kernel.state.current_state(ASSET_ID) == "Installed"
    print(f"State unchanged: {kernel.state.current_state(ASSET_ID)}")

    _banner("Step 2 — EvidenceSubmitted alone (not enough)")
    kernel.state.ingest_event(
        _envelope(
            "EvidenceSubmitted",
            "tech-field-07",
            {
                "evidence_id": "evd-torque-1",
                "evidence_type": "TorqueVerified",
                "subject_kind": "Asset",
                "subject_id": ASSET_ID,
                "notes": "tech claims torque complete",
            },
        )
    )
    still_rejected = _request(kernel, key="attempt-submitted-only")
    _show("Result after submit-only:", still_rejected)
    assert still_rejected["payload"]["reason_code"] == "MissingEvidence"
    print("ADR-0012: only EvidenceValidated satisfies gates.")

    _banner("Step 3 — EvidenceValidated (authorized validator)")
    kernel.state.ingest_event(
        _envelope(
            "EvidenceValidated",
            "validator-qa-1",
            {
                "evidence_id": "evd-torque-1",
                "evidence_type": "TorqueVerified",
                "subject_kind": "Asset",
                "subject_id": ASSET_ID,
                "validator_id": "validator-qa-1",
                "method": "calibrated_torque_wrench_log",
            },
        )
    )
    print("Validated evidence on the log. State still Installed until transition.")
    print(f"Current state: {kernel.state.current_state(ASSET_ID)}")

    _banner("Step 4 — Transition with sufficient evidence")
    advanced = _request(kernel, key="attempt-with-evidence")
    _show("Result:", advanced)
    assert advanced["type"] == "StateAdvanced"
    assert kernel.state.current_state(ASSET_ID) == "Commissioned"
    print(f"Asset state: {kernel.state.current_state(ASSET_ID)}")
    print("Replayable history length:", len(kernel.events.all_events()))

    _banner("Done")
    print("Clicks do not commission assets. Validated evidence does.")
    print("Air-gapped: no cloud control plane was required for this advance.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"DEMO FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
