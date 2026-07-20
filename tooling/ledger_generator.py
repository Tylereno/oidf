#!/usr/bin/env python3
"""Build a schema-valid handoff_ledger.json from field-ish inputs.

Rejects empty evidence_refs when advancing into commission/energize states.

Usage:
  python tooling/ledger_generator.py --subject BESS-1 --from ReadyForCommission --to Commissioned \\
    --evidence ev-1 ev-2 -o /tmp/handoff_ledger.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "core_schemas" / "handoff_ledger.json"

# States that require at least one evidence ref on the advancing entry.
EVIDENCE_REQUIRED_TO_STATES = frozenset(
    {
        "Commissioned",
        "Energized",
        "ReadyForCommission",
        "Operational",
    }
)


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_ledger(ledger: dict) -> list[str]:
    errors: list[str] = []
    try:
        import jsonschema
    except ImportError:
        return errors
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    errors.extend(e.message for e in sorted(validator.iter_errors(ledger), key=lambda e: list(e.path)))
    return errors


def build_ledger(
    *,
    subject: str,
    kind: str,
    from_state: str,
    to_state: str,
    evidence: list[str],
    actor_id: str | None = None,
    baseline_id: str = "KEEL-SPEC-BASELINE-2026.07.20",
) -> dict:
    if to_state in EVIDENCE_REQUIRED_TO_STATES and not evidence:
        raise ValueError(
            f"evidence_refs required when advancing to {to_state} "
            "(pass --evidence id1 id2 …)"
        )
    if any(not e.strip() for e in evidence):
        raise ValueError("evidence_refs must be non-empty strings")

    now = utcnow()
    entry: dict = {
        "seq": 1,
        "occurred_at": now,
        "from_state": from_state,
        "to_state": to_state,
        "evidence_refs": list(evidence),
    }
    if actor_id:
        entry["actor_id"] = actor_id

    return {
        "ledger_id": f"led-{uuid4().hex[:12]}",
        "spec_version": "1.0.0",
        "subject": {"kind": kind, "id": subject},
        "created_at": now,
        "baseline_id": baseline_id,
        "entries": [entry],
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--subject", required=True)
    p.add_argument("--kind", default="Asset", choices=["Asset", "Deployment"])
    p.add_argument("--from", dest="from_state", required=True)
    p.add_argument("--to", dest="to_state", required=True)
    p.add_argument("--evidence", nargs="+", default=[])
    p.add_argument("--actor", default="")
    p.add_argument("-o", "--output", type=Path, required=True)
    p.add_argument("--skip-schema", action="store_true", help="Skip JSON Schema validation")
    args = p.parse_args()

    try:
        ledger = build_ledger(
            subject=args.subject,
            kind=args.kind,
            from_state=args.from_state,
            to_state=args.to_state,
            evidence=list(args.evidence),
            actor_id=args.actor or None,
        )
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2

    if not args.skip_schema:
        errors = validate_ledger(ledger)
        if errors:
            print("FAIL: schema validation", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            return 1

    args.output.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
