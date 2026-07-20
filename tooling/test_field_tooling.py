#!/usr/bin/env python3
"""Unit tests for ledger / SAT tooling (stdlib unittest)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLING = ROOT / "tooling"


class LedgerGeneratorTests(unittest.TestCase):
    def test_rejects_empty_evidence_on_commission(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "led.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(TOOLING / "ledger_generator.py"),
                    "--subject",
                    "BESS-1",
                    "--from",
                    "ReadyForCommission",
                    "--to",
                    "Commissioned",
                    "-o",
                    str(out),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("evidence_refs required", proc.stderr)

    def test_schema_rejects_empty_evidence_refs(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema = json.loads((ROOT / "core_schemas" / "handoff_ledger.json").read_text())
        doc = {
            "ledger_id": "led-empty",
            "spec_version": "1.0.0",
            "subject": {"kind": "Asset", "id": "BESS-1"},
            "created_at": "2026-07-20T00:00:00Z",
            "entries": [
                {
                    "seq": 1,
                    "occurred_at": "2026-07-20T00:00:00Z",
                    "from_state": "ReadyForCommission",
                    "to_state": "Commissioned",
                    "evidence_refs": [],
                }
            ],
        }
        errors = list(jsonschema.Draft202012Validator(schema).iter_errors(doc))
        self.assertTrue(errors, "empty evidence_refs must fail handoff_ledger schema")

    def test_writes_schema_valid_ledger(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "led.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(TOOLING / "ledger_generator.py"),
                    "--subject",
                    "BESS-1",
                    "--from",
                    "ReadyForCommission",
                    "--to",
                    "Commissioned",
                    "--evidence",
                    "ev-1",
                    "ev-2",
                    "-o",
                    str(out),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            doc = json.loads(out.read_text())
            self.assertEqual(doc["entries"][0]["to_state"], "Commissioned")
            val = subprocess.run(
                [sys.executable, str(TOOLING / "state_validator.py"), str(out), "--expect", "Commissioned"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(val.returncode, 0, val.stderr)


class SatEventLogTests(unittest.TestCase):
    def test_create_append_validate(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sat.json"
            create = subprocess.run(
                [
                    sys.executable,
                    str(TOOLING / "sat_event_log.py"),
                    "create",
                    "--subject",
                    "dep-1",
                    "-o",
                    str(path),
                    "--gate",
                    "pack.gate",
                    "--result",
                    "pass",
                    "--evidence-type",
                    "InspectionPass",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(create.returncode, 0, create.stderr)
            append = subprocess.run(
                [
                    sys.executable,
                    str(TOOLING / "sat_event_log.py"),
                    "append",
                    str(path),
                    "--gate",
                    "pack.gate2",
                    "--result",
                    "fail",
                    "--failure-code",
                    "Timeout",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(append.returncode, 0, append.stderr)
            val = subprocess.run(
                [sys.executable, str(TOOLING / "sat_event_log.py"), "validate", str(path)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(val.returncode, 0, val.stderr)
            doc = json.loads(path.read_text())
            self.assertEqual(len(doc["events"]), 2)


if __name__ == "__main__":
    unittest.main()
