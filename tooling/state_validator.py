#!/usr/bin/env python3
"""Lightweight lab helper: verify claimed equipment state matches handoff ledger.

Usage:
  python tooling/state_validator.py path/to/handoff_ledger.json [--expect Energized]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def latest_state(ledger: dict) -> str | None:
    entries = ledger.get("entries") or []
    if not entries:
        return None
    last = max(entries, key=lambda e: e.get("seq", 0))
    return last.get("to_state")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("ledger", type=Path)
    p.add_argument("--expect", help="Expected to_state of latest entry")
    args = p.parse_args()

    ledger = json.loads(args.ledger.read_text())
    state = latest_state(ledger)
    if state is None:
        print("FAIL: ledger has no entries", file=sys.stderr)
        return 1
    print(f"latest_state={state}")
    if args.expect and state != args.expect:
        print(f"FAIL: expected {args.expect}", file=sys.stderr)
        return 2
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
