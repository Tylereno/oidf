"""Smoke: commissioning gate demo exits 0 and prints the reject→accept arc."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

DEMO = Path(__file__).resolve().parents[1] / "examples" / "commission_gate_demo.py"


def test_commission_gate_demo_runs():
    proc = subprocess.run(
        [sys.executable, str(DEMO)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    out = proc.stdout
    assert "MissingEvidence" in out
    assert "EvidenceValidated" in out or "Validated evidence" in out
    assert "StateAdvanced" in out
    assert "Commissioned" in out
