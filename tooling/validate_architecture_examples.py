#!/usr/bin/env python3
"""Validate architecture pack example ledgers/SAT logs against core schemas."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        import jsonschema
    except ImportError:
        print("pip install jsonschema", file=sys.stderr)
        return 2

    ledger_schema = json.loads((ROOT / "core_schemas/handoff_ledger.json").read_text())
    sat_schema = json.loads((ROOT / "core_schemas/sat_event_log.json").read_text())
    examples = sorted(ROOT.glob("architectures/*/examples/handoff_ledger.json"))
    if not examples:
        print("ERROR: no architecture examples found", file=sys.stderr)
        return 2

    failed = 0
    for ledger_path in examples:
        sat_path = ledger_path.with_name("sat_event_log.json")
        pack = ledger_path.parent.parent.name
        for path, schema in ((ledger_path, ledger_schema), (sat_path, sat_schema)):
            if not path.is_file():
                print(f"FAIL {pack}: missing {path.name}")
                failed += 1
                continue
            doc = json.loads(path.read_text())
            errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(doc), key=lambda e: e.path)
            if errors:
                failed += 1
                print(f"FAIL {pack}/{path.name}")
                for e in errors:
                    print(f"  - {e.message}")
            else:
                print(f"OK   {pack}/{path.name}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
