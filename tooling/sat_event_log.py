#!/usr/bin/env python3
"""Create, append, and validate OIDF sat_event_log.json files.

Usage:
  python tooling/sat_event_log.py create --subject dep-1 -o /tmp/sat.json \\
    --event sat-1 --gate pack.gate --result pass --evidence-type InspectionPass

  python tooling/sat_event_log.py append /tmp/sat.json \\
    --event sat-2 --gate pack.gate2 --result fail --failure-code Timeout

  python tooling/sat_event_log.py validate /tmp/sat.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "core_schemas" / "sat_event_log.json"


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


def schema_errors(doc: dict) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema not installed (pip install jsonschema)"]
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    return [e.message for e in sorted(validator.iter_errors(doc), key=lambda e: list(e.path))]


def make_event(args: argparse.Namespace) -> dict:
    event: dict = {
        "event_id": args.event or f"sat-{uuid4().hex[:10]}",
        "gate_id": args.gate,
        "occurred_at": args.occurred_at or utcnow(),
        "result": args.result,
    }
    if args.evidence_type:
        event["evidence_type"] = args.evidence_type
    if args.actor:
        event["actor_id"] = args.actor
    if args.failure_code:
        event["failure_code"] = args.failure_code
    if args.notes:
        event["notes"] = args.notes
    return event


def cmd_create(args: argparse.Namespace) -> int:
    doc = {
        "log_id": args.log_id or f"satlog-{uuid4().hex[:12]}",
        "spec_version": "1.0.0",
        "subject_id": args.subject,
        "events": [make_event(args)],
    }
    errs = schema_errors(doc)
    if errs:
        print("FAIL: schema", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1
    dump(args.output, doc)
    print(f"wrote {args.output}")
    return 0


def cmd_append(args: argparse.Namespace) -> int:
    doc = load(args.path)
    doc.setdefault("events", []).append(make_event(args))
    errs = schema_errors(doc)
    if errs:
        print("FAIL: schema", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1
    dump(args.path, doc)
    print(f"appended → {args.path} ({len(doc['events'])} events)")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    doc = load(args.path)
    errs = schema_errors(doc)
    if errs:
        print("FAIL", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK ({len(doc.get('events') or [])} events)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create", help="Create a new SAT event log")
    c.add_argument("--subject", required=True)
    c.add_argument("-o", "--output", type=Path, required=True)
    c.add_argument("--log-id", default="")
    c.add_argument("--event", default="")
    c.add_argument("--gate", required=True)
    c.add_argument("--result", required=True, choices=["pass", "fail", "blocked"])
    c.add_argument("--evidence-type", default="")
    c.add_argument("--actor", default="")
    c.add_argument("--failure-code", default="")
    c.add_argument("--notes", default="")
    c.add_argument("--occurred-at", default="")
    c.set_defaults(func=cmd_create)

    a = sub.add_parser("append", help="Append an event to an existing log")
    a.add_argument("path", type=Path)
    a.add_argument("--event", default="")
    a.add_argument("--gate", required=True)
    a.add_argument("--result", required=True, choices=["pass", "fail", "blocked"])
    a.add_argument("--evidence-type", default="")
    a.add_argument("--actor", default="")
    a.add_argument("--failure-code", default="")
    a.add_argument("--notes", default="")
    a.add_argument("--occurred-at", default="")
    a.set_defaults(func=cmd_append)

    v = sub.add_parser("validate", help="Validate a SAT event log against schema")
    v.add_argument("path", type=Path)
    v.set_defaults(func=cmd_validate)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
