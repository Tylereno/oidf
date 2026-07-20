#!/usr/bin/env python3
"""Lab helper: build a minimal handoff_ledger.json from field-ish inputs.

Usage:
  python tooling/ledger_generator.py --subject BESS-1 --from Installed --to Commissioned \\
    --evidence ev-1 ev-2 -o /tmp/handoff_ledger.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--subject", required=True)
    p.add_argument("--kind", default="Asset", choices=["Asset", "Deployment"])
    p.add_argument("--from", dest="from_state", required=True)
    p.add_argument("--to", dest="to_state", required=True)
    p.add_argument("--evidence", nargs="+", default=[])
    p.add_argument("-o", "--output", type=Path, required=True)
    args = p.parse_args()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    ledger = {
        "ledger_id": f"led-{uuid4().hex[:12]}",
        "spec_version": "1.0.0",
        "subject": {"kind": args.kind, "id": args.subject},
        "created_at": now,
        "baseline_id": "KEEL-SPEC-BASELINE-2026.07.20",
        "entries": [
            {
                "seq": 1,
                "occurred_at": now,
                "from_state": args.from_state,
                "to_state": args.to_state,
                "evidence_refs": list(args.evidence),
            }
        ],
    }
    args.output.write_text(json.dumps(ledger, indent=2) + "\n")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
