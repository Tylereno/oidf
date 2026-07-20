#!/usr/bin/env python3
"""Solar / PCS inverter lighthouse end-to-end path (second domain beyond BESS).

Machine Evidence only on happy path. No click-to-advance.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "keel-core" / "src"))
sys.path.insert(0, str(ROOT / "keel-plugins"))

from keel_core.adapters.file_event_store import FileEventStore
from keel_core.app.event_service import EventService
from keel_core.app.kernel import CoreKernel
from keel_evidence import DESCRIPTOR as EVIDENCE_DESC
from keel_telemetry import DESCRIPTOR as TELEMETRY_DESC


def load_machine() -> dict:
    return json.loads((Path(__file__).parent / "machine_inverter.json").read_text())


def envelope(etype: str, actor: str, payload: dict, **subj) -> dict:
    e = {
        "id": EventService.new_id("evt"),
        "type": etype,
        "spec_version": "1.0.0",
        "occurred_at": "2026-07-20T12:00:00.000000Z",
        "recorded_at": "2026-07-20T12:00:00.000000Z",
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
        node_id="edge-inv-1",
    )
    machine = load_machine()
    k.state.register_machine(machine)
    k.state.bind_subject("INV-1", machine["id"])

    plugins = str(ROOT / "keel-plugins")
    k.plugins.extra_pythonpath.append(plugins)
    k.plugins.register(TELEMETRY_DESC)
    k.plugins.register(EVIDENCE_DESC)
    k.plugins.start("keel-telemetry", "keel_telemetry")
    k.plugins.start("keel-evidence", "keel_evidence")

    try:
        bad = envelope(
            "TelemetryReceived",
            "pcs",
            {
                "subject_kind": "Asset",
                "subject_id": "INV-1",
                "metrics": {
                    "grid_voltage_v": 100.0,
                    "grid_frequency_hz": 55.0,
                    "anti_islanding_ok": False,
                },
            },
            asset_id="INV-1",
            deployment_id="DEP-INV-1",
        )
        k.events.append(bad)
        for d in k.plugins.dispatch_event("keel-telemetry", bad):
            k.plugins.dispatch_event("keel-evidence", d)

        good = envelope(
            "TelemetryReceived",
            "pcs",
            {
                "subject_kind": "Asset",
                "subject_id": "INV-1",
                "metrics": {
                    "grid_voltage_v": 230.0,
                    "grid_frequency_hz": 60.0,
                    "anti_islanding_ok": True,
                },
            },
            asset_id="INV-1",
            deployment_id="DEP-INV-1",
        )
        k.events.append(good)
        submitted = k.plugins.dispatch_event("keel-telemetry", good)
        assert submitted, "expected EvidenceSubmitted from machine telemetry"
        for s in submitted:
            validated = k.plugins.dispatch_event("keel-evidence", s)
            for v in validated:
                k.state.ingest_event(v)

        r1 = k.state.ingest_event(
            envelope(
                "TransitionRequested",
                "commissioner",
                {
                    "subject_kind": "Asset",
                    "subject_id": "INV-1",
                    "transition_id": "installed_to_ready",
                    "from_state": "Installed",
                    "to_state": "ReadyForCommission",
                    "idempotency_key": "inv-ready-1",
                },
                asset_id="INV-1",
                deployment_id="DEP-INV-1",
            )
        )
        assert r1["type"] == "StateAdvanced", r1

        r2 = k.state.ingest_event(
            envelope(
                "TransitionRequested",
                "commissioner",
                {
                    "subject_kind": "Asset",
                    "subject_id": "INV-1",
                    "transition_id": "ready_to_commissioned",
                    "from_state": "ReadyForCommission",
                    "to_state": "Commissioned",
                    "idempotency_key": "inv-comm-1",
                },
                asset_id="INV-1",
                deployment_id="DEP-INV-1",
            )
        )
        assert r2["type"] == "StateAdvanced", r2
        assert k.state.current_state("INV-1") == "Commissioned"

        print(
            json.dumps(
                {
                    "ok": True,
                    "final_state": k.state.current_state("INV-1"),
                    "events": len(k.events.all_events()),
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
        k.plugins.stop("keel-telemetry")
        k.plugins.stop("keel-evidence")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/keel-solar-inverter")
    out.mkdir(parents=True, exist_ok=True)
    main(out)
