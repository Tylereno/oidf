#!/usr/bin/env python3
"""Validate a handoff ledger against schema (+ optional expected state / machine).

Usage:
  python tooling/state_validator.py path/to/handoff_ledger.json [--expect Commissioned]
  python tooling/state_validator.py path/to/handoff_ledger.json --machine path/to/machine.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "core_schemas" / "handoff_ledger.json"


def latest_state(ledger: dict) -> str | None:
    entries = ledger.get("entries") or []
    if not entries:
        return None
    last = max(entries, key=lambda e: e.get("seq", 0))
    return last.get("to_state")


def schema_errors(ledger: dict) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema not installed (pip install jsonschema)"]
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    return [e.message for e in sorted(validator.iter_errors(ledger), key=lambda e: list(e.path))]


def machine_errors(ledger: dict, machine: dict) -> list[str]:
    errors: list[str] = []
    states = set(machine.get("states") or [])
    for entry in ledger.get("entries") or []:
        for key in ("from_state", "to_state"):
            val = entry.get(key)
            if states and val not in states:
                errors.append(f"entry seq={entry.get('seq')}: {key}={val!r} not in machine states")
        if not entry.get("evidence_refs"):
            errors.append(f"entry seq={entry.get('seq')}: empty evidence_refs")
    mid = ledger.get("machine_definition_id")
    if mid and machine.get("id") and mid != machine.get("id") and mid != f"{machine.get('id')}":
        # Allow either exact id or id@version style; warn only on hard mismatch of prefix
        if not str(mid).startswith(str(machine.get("id"))):
            errors.append(f"machine_definition_id {mid!r} does not match machine id {machine.get('id')!r}")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("ledger", type=Path)
    p.add_argument("--expect", help="Expected to_state of latest entry")
    p.add_argument("--machine", type=Path, help="Optional machine_definition JSON")
    p.add_argument("--skip-schema", action="store_true")
    args = p.parse_args()

    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    failed = False

    if not args.skip_schema:
        errs = schema_errors(ledger)
        if errs:
            failed = True
            print("FAIL: schema", file=sys.stderr)
            for e in errs:
                print(f"  - {e}", file=sys.stderr)

    state = latest_state(ledger)
    if state is None:
        print("FAIL: ledger has no entries", file=sys.stderr)
        return 1
    print(f"latest_state={state}")

    if args.expect and state != args.expect:
        print(f"FAIL: expected {args.expect}", file=sys.stderr)
        failed = True

    if args.machine:
        machine = json.loads(args.machine.read_text(encoding="utf-8"))
        merrs = machine_errors(ledger, machine)
        if merrs:
            failed = True
            print("FAIL: machine checks", file=sys.stderr)
            for e in merrs:
                print(f"  - {e}", file=sys.stderr)

    if failed:
        return 2
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
