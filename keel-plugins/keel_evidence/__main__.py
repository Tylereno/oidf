"""keel-evidence — official Evidence validation Plugin (subprocess worker).

Protocol: JSON lines on stdin/stdout.
  <- {"op":"start","descriptor":{...}}
  -> {"status":"ok"}
  <- {"op":"event","event":{...}}
  -> {"status":"ok","publish":[event drafts...]}
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12]}"


def validate_evidence(event: dict[str, Any]) -> list[dict[str, Any]]:
    if event.get("type") != "EvidenceSubmitted":
        return []
    p = event.get("payload") or {}
    et = p.get("evidence_type")
    # Minimal rule: known types with non-empty evidence_id pass
    ok = bool(et) and bool(p.get("evidence_id")) and et in {
        "InspectionPass",
        "TorqueReport",
        "Permit",
        # BESS lighthouse catalog (RFC 0021)
        "CellVoltageInBand",
        "InsulationResistanceOk",
        "ThermalStable",
        "ContactorClosedFeedback",
    }
    now = utcnow()
    if ok:
        draft = {
            "id": new_id("evt"),
            "type": "EvidenceValidated",
            "spec_version": "1.0.0",
            "occurred_at": now,
            "recorded_at": now,
            "actor_id": "plugin:keel-evidence",
            "deployment_id": event.get("deployment_id"),
            "asset_id": event.get("asset_id"),
            "caused_by_event_id": event.get("id"),
            "payload": {
                "evidence_id": p["evidence_id"],
                "evidence_type": et,
                "subject_kind": p.get("subject_kind", "Asset"),
                "subject_id": p.get("subject_id"),
                "validator_id": "keel-evidence",
            },
        }
    else:
        draft = {
            "id": new_id("evt"),
            "type": "EvidenceRejected",
            "spec_version": "1.0.0",
            "occurred_at": now,
            "recorded_at": now,
            "actor_id": "plugin:keel-evidence",
            "deployment_id": event.get("deployment_id"),
            "asset_id": event.get("asset_id"),
            "caused_by_event_id": event.get("id"),
            "payload": {
                "evidence_id": p.get("evidence_id", "unknown"),
                "evidence_type": et or "unknown",
                "subject_kind": p.get("subject_kind", "Asset"),
                "subject_id": p.get("subject_id", "unknown"),
                "reason_code": "InvalidEvidence",
                "reason_detail": "failed keel-evidence rules",
            },
        }
    return [{k: v for k, v in draft.items() if v is not None}]


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        op = msg.get("op")
        if op == "start":
            sys.stdout.write(json.dumps({"status": "ok"}) + "\n")
            sys.stdout.flush()
        elif op == "stop":
            sys.stdout.write(json.dumps({"status": "ok"}) + "\n")
            sys.stdout.flush()
            return
        elif op == "event":
            try:
                pubs = validate_evidence(msg["event"])
                sys.stdout.write(json.dumps({"status": "ok", "publish": pubs}) + "\n")
                sys.stdout.flush()
            except Exception as exc:  # noqa: BLE001
                sys.stdout.write(json.dumps({"status": "error", "reason": str(exc)}) + "\n")
                sys.stdout.flush()
        else:
            sys.stdout.write(json.dumps({"status": "error", "reason": "unknown_op"}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
