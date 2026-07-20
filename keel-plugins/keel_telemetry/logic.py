"""Shared telemetry→evidence logic (importable without running worker)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

DEFAULT_RULES = {
    "pack_voltage_v": {
        "evidence_type": "CellVoltageInBand",
        "min": 700.0,
        "max": 900.0,
    },
    "insulation_mohm": {
        "evidence_type": "InsulationResistanceOk",
        "min": 100.0,
        "max": None,
    },
    "temp_c": {
        "evidence_type": "ThermalStable",
        "min": 15.0,
        "max": 35.0,
    },
    "contactor_closed": {
        "evidence_type": "ContactorClosedFeedback",
        "equals": True,
    },
}

DESCRIPTOR = {
    "plugin_id": "keel-telemetry",
    "plugin_version": "0.1.0",
    "capabilities": ["telemetry.evidence"],
    "publishes": ["EvidenceSubmitted"],
    "subscribes": ["TelemetryReceived"],
    "config_keys": ["rules"],
}


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12]}"


def _match(rule: dict[str, Any], value: Any) -> bool:
    if "equals" in rule:
        return value == rule["equals"]
    try:
        num = float(value)
    except (TypeError, ValueError):
        return False
    if rule.get("min") is not None and num < float(rule["min"]):
        return False
    if rule.get("max") is not None and num > float(rule["max"]):
        return False
    return True


def telemetry_to_evidence(event: dict[str, Any], rules: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    if event.get("type") != "TelemetryReceived":
        return []
    rules = rules or DEFAULT_RULES
    payload = event.get("payload") or {}
    metrics = payload.get("metrics") or payload
    subject_id = payload.get("subject_id") or event.get("asset_id")
    subject_kind = payload.get("subject_kind", "Asset")
    drafts: list[dict[str, Any]] = []
    now = utcnow()
    for key, rule in rules.items():
        if key not in metrics:
            continue
        if not _match(rule, metrics[key]):
            continue
        draft = {
            "id": new_id("evt"),
            "type": "EvidenceSubmitted",
            "spec_version": "1.0.0",
            "occurred_at": now,
            "recorded_at": now,
            "actor_id": "plugin:keel-telemetry",
            "deployment_id": event.get("deployment_id"),
            "asset_id": event.get("asset_id") or subject_id,
            "caused_by_event_id": event.get("id"),
            "payload": {
                "evidence_id": new_id("evd"),
                "evidence_type": rule["evidence_type"],
                "subject_kind": subject_kind,
                "subject_id": subject_id,
                "attributes": {
                    "source_class": "machine",
                    "metric": key,
                    "metric_value": metrics[key],
                    "telemetry_event_id": event.get("id"),
                },
            },
        }
        drafts.append({k: v for k, v in draft.items() if v is not None})
    return drafts
