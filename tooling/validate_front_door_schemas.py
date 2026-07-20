#!/usr/bin/env python3
"""Validate OIDF front-door JSON schemas and their examples."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "core_schemas"
EXAMPLES = SCHEMAS / "examples"

FRONT_DOOR = [
    "handoff_ledger.json",
    "sat_event_log.json",
    "architecture_sat_gate_map.json",
    "site_state.json",
    "site_event_log.json",
]

EXAMPLE_PAIRS = [
    ("site_state.json", "site_state.example.json"),
    ("site_event_log.json", "site_event_log.example.json"),
]


def main() -> int:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print("ERROR: jsonschema not installed", file=sys.stderr)
        return 2

    errors: list[str] = []

    for name in FRONT_DOOR:
        path = SCHEMAS / name
        if not path.is_file():
            errors.append(f"missing schema: {path}")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: {exc}")

    for schema_name, example_name in EXAMPLE_PAIRS:
        schema = json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8"))
        example_path = EXAMPLES / example_name
        if not example_path.is_file():
            errors.append(f"missing example: {example_path}")
            continue
        instance = json.loads(example_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
            errors.append(f"{example_path}: {err.message}")

    # Negative check: assist must not authorize power_tier_changed
    bad = {
        "log_id": "bad",
        "spec_version": "1.0.0",
        "site_id": "x",
        "events": [
            {
                "event_id": "e1",
                "occurred_at": "2026-07-20T00:00:00Z",
                "kind": "power_tier_changed",
                "actor": {"kind": "assist"},
                "suggestion_only": True,
                "to_value": "survival",
            }
        ],
    }
    sat = json.loads((SCHEMAS / "site_event_log.json").read_text(encoding="utf-8"))
    bad_errors = list(Draft202012Validator(sat).iter_errors(bad))
    if not bad_errors:
        errors.append("expected rejection of assist-authorized power_tier_changed")

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"OK: {len(FRONT_DOOR)} front-door schemas; examples + ADR-0019 negative check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
