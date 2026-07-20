from __future__ import annotations

import json
from pathlib import Path

from keel_telemetry.logic import telemetry_to_evidence


def test_telemetry_emits_machine_evidence():
    event = {
        "id": "tel-1",
        "type": "TelemetryReceived",
        "asset_id": "BESS-1",
        "payload": {
            "subject_id": "BESS-1",
            "subject_kind": "Asset",
            "metrics": {"pack_voltage_v": 800, "insulation_mohm": 200, "temp_c": 22},
        },
    }
    drafts = telemetry_to_evidence(event)
    types = {d["payload"]["evidence_type"] for d in drafts}
    assert "CellVoltageInBand" in types
    assert "InsulationResistanceOk" in types
    assert "ThermalStable" in types
    assert all(d["payload"]["attributes"]["source_class"] == "machine" for d in drafts)


def test_out_of_band_emits_nothing():
    event = {
        "id": "tel-2",
        "type": "TelemetryReceived",
        "payload": {"subject_id": "BESS-1", "metrics": {"pack_voltage_v": 10}},
    }
    assert telemetry_to_evidence(event) == []


def test_bess_e2e_script(tmp_path: Path):
    import runpy
    import sys

    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "keel-core" / "src"))
    sys.path.insert(0, str(root / "keel-plugins"))
    script = root / "keel-examples" / "bess-lighthouse" / "run_e2e.py"
    ns = runpy.run_path(str(script))
    ns["main"](tmp_path)
    assert (tmp_path / "events.jsonl").exists()
    lines = (tmp_path / "events.jsonl").read_text().strip().splitlines()
    assert len(lines) >= 5
