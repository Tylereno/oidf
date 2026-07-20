#!/usr/bin/env python3
"""BESS lighthouse end-to-end path (RFC 0021).

Machine Evidence only on happy path: telemetry → ark-telemetry → ark-evidence → transitions.
No click-to-advance.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ark-core" / "src"))
sys.path.insert(0, str(ROOT / "ark-plugins"))

from ark_core.adapters.file_event_store import FileEventStore
from ark_core.app.event_service import EventService
from ark_core.app.kernel import CoreKernel
from ark_evidence import DESCRIPTOR as EVIDENCE_DESC
from ark_telemetry import DESCRIPTOR as TELEMETRY_DESC
from ark_telemetry.logic import telemetry_to_evidence


def load_machine() -> dict:
    return json.loads((Path(__file__).parent / "machine_bess.json").read_text())


def envelope(etype: str, actor: str, payload: dict, **subj) -> dict:
    e = {
        "id": EventService.new_id("evt"),
        "type": etype,
        "spec_version": "1.0.0",
        "occurred_at": "2026-07-20T10:00:00.000000Z",
        "recorded_at": "2026-07-20T10:00:00.000000Z",
        "actor_id": actor,
        "payload": payload,
    }
    e.update({k: v for k, v in subj.items() if v is not None})
    return e


def main(data_dir: Path) -> None:
    store = FileEventStore(data_dir / "events.jsonl")
    k = CoreKernel(
        grants=[{"principal_id": "commissioner", "actions": ["transition.request"]}],
        store=store,
        node_id="edge-bess-1",
    )
    machine = load_machine()
    k.state.register_machine(machine)
    k.state.bind_subject("BESS-1", machine["id"])

    plugins = str(ROOT / "ark-plugins")
    k.plugins.extra_pythonpath.append(plugins)
    k.plugins.register(TELEMETRY_DESC)
    k.plugins.register(EVIDENCE_DESC)
    k.plugins.start("ark-telemetry", "ark_telemetry")
    k.plugins.start("ark-evidence", "ark_evidence")

    try:
        # Telemetry that fails thresholds → no commission path
        bad = envelope(
            "TelemetryReceived",
            "bms",
            {
                "subject_kind": "Asset",
                "subject_id": "BESS-1",
                "metrics": {"pack_voltage_v": 100.0, "insulation_mohm": 1.0, "temp_c": 50.0},
            },
            asset_id="BESS-1",
            deployment_id="DEP-BESS-1",
        )
        k.events.append(bad)
        for d in k.plugins.dispatch_event("ark-telemetry", bad):
            k.plugins.dispatch_event("ark-evidence", d)

        # Machine Evidence: in-band metrics
        good = envelope(
            "TelemetryReceived",
            "bms",
            {
                "subject_kind": "Asset",
                "subject_id": "BESS-1",
                "metrics": {
                    "pack_voltage_v": 800.0,
                    "insulation_mohm": 250.0,
                    "temp_c": 25.0,
                    "contactor_closed": True,
                },
            },
            asset_id="BESS-1",
            deployment_id="DEP-BESS-1",
        )
        k.events.append(good)
        submitted = k.plugins.dispatch_event("ark-telemetry", good)
        assert submitted, "expected EvidenceSubmitted from machine telemetry"
        assert all(
            s["payload"]["attributes"]["source_class"] == "machine" for s in submitted
        )
        for s in submitted:
            validated = k.plugins.dispatch_event("ark-evidence", s)
            for v in validated:
                k.state.ingest_event(v)

        # Advance Installed → ReadyForCommission
        r1 = k.state.ingest_event(
            envelope(
                "TransitionRequested",
                "commissioner",
                {
                    "subject_kind": "Asset",
                    "subject_id": "BESS-1",
                    "transition_id": "installed_to_ready",
                    "from_state": "Installed",
                    "to_state": "ReadyForCommission",
                    "idempotency_key": "bess-ready-1",
                },
                asset_id="BESS-1",
                deployment_id="DEP-BESS-1",
            )
        )
        assert r1["type"] == "StateAdvanced", r1

        # Thermal already validated → Commissioned
        r2 = k.state.ingest_event(
            envelope(
                "TransitionRequested",
                "commissioner",
                {
                    "subject_kind": "Asset",
                    "subject_id": "BESS-1",
                    "transition_id": "ready_to_commissioned",
                    "from_state": "ReadyForCommission",
                    "to_state": "Commissioned",
                    "idempotency_key": "bess-comm-1",
                },
                asset_id="BESS-1",
                deployment_id="DEP-BESS-1",
            )
        )
        assert r2["type"] == "StateAdvanced", r2
        assert k.state.current_state("BESS-1") == "Commissioned"

        batch = k.sync.export_batch("lighthouse-1")
        print(
            json.dumps(
                {
                    "ok": True,
                    "final_state": k.state.current_state("BESS-1"),
                    "events": len(k.events.all_events()),
                    "sync_batch_id": batch["batch_id"],
                    "machine_evidence_types": sorted(
                        {
                            e["payload"]["evidence_type"]
                            for e in k.events.all_events()
                            if e["type"] == "EvidenceValidated"
                            and e["payload"].get("evidence_type") != "InspectionPass"
                        }
                    ),
                },
                indent=2,
            )
        )
    finally:
        k.plugins.stop("ark-telemetry")
        k.plugins.stop("ark-evidence")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/ark-bess-lighthouse")
    out.mkdir(parents=True, exist_ok=True)
    main(out)
