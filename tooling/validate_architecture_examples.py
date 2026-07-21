#!/usr/bin/env python3
"""Validate architecture pack example ledgers/SAT logs against core schemas.

Also resolves sat_gate_map evidence_catalogs / evidence_types against
core_schemas/evidence-catalog/ so ghost *-local catalogs fail CI.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_DIR = ROOT / "core_schemas" / "evidence-catalog"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def schema_errors(jsonschema, schema: dict, doc: dict):
    validator = jsonschema.Draft202012Validator(schema)
    return sorted(validator.iter_errors(doc), key=lambda e: e.path)


def print_schema_errors(label: str, errors) -> None:
    print(f"FAIL {label}")
    for error in errors:
        print(f"  - {error.message}")


def load_evidence_catalogs() -> tuple[dict[str, set[str]], int]:
    """Return catalog_id -> evidence_type set. Fail on malformed catalog files."""
    catalogs: dict[str, set[str]] = {}
    failed = 0
    if not CATALOG_DIR.is_dir():
        print(f"FAIL evidence-catalog: missing directory {CATALOG_DIR}")
        return catalogs, 1

    for path in sorted(CATALOG_DIR.glob("*.json")):
        try:
            doc = load_json(path)
        except json.JSONDecodeError as exc:
            print(f"FAIL evidence-catalog/{path.name}: invalid JSON ({exc})")
            failed += 1
            continue

        catalog_id = doc.get("catalog_id")
        types = doc.get("types")
        if not isinstance(catalog_id, str) or not catalog_id:
            print(f"FAIL evidence-catalog/{path.name}: missing catalog_id")
            failed += 1
            continue
        if path.stem != catalog_id:
            print(
                f"FAIL evidence-catalog/{path.name}: filename stem must match "
                f"catalog_id {catalog_id!r}"
            )
            failed += 1
        if not isinstance(types, list) or not types:
            print(f"FAIL evidence-catalog/{path.name}: types[] must be non-empty")
            failed += 1
            continue

        type_names: set[str] = set()
        for entry in types:
            if not isinstance(entry, dict):
                print(f"FAIL evidence-catalog/{path.name}: type entry must be object")
                failed += 1
                continue
            name = entry.get("evidence_type")
            if not isinstance(name, str) or not name:
                print(f"FAIL evidence-catalog/{path.name}: missing evidence_type")
                failed += 1
                continue
            if name in type_names:
                print(f"FAIL evidence-catalog/{path.name}: duplicate evidence_type {name!r}")
                failed += 1
            type_names.add(name)

        if catalog_id in catalogs:
            print(f"FAIL evidence-catalog: duplicate catalog_id {catalog_id!r}")
            failed += 1
        catalogs[catalog_id] = type_names

    if not failed:
        print(f"OK   evidence-catalog: {len(catalogs)} catalogs loaded")
    return catalogs, failed


def validate_gate_catalog_refs(
    pack: str, gate_map: dict, catalogs: dict[str, set[str]]
) -> int:
    """Every evidence_catalogs entry and evidence_types name must resolve."""
    failed = 0
    for gate in gate_map["gates"]:
        gate_id = gate["gate_id"]
        catalog_ids = gate.get("evidence_catalogs") or []
        evidence_types = gate.get("evidence_types") or []

        if evidence_types and not catalog_ids:
            print(
                f"FAIL {pack}/sat_gate_map.json: gate_id {gate_id!r} lists "
                f"evidence_types but no evidence_catalogs"
            )
            failed += 1
            continue

        resolved: set[str] = set()
        for catalog_id in catalog_ids:
            if catalog_id not in catalogs:
                print(
                    f"FAIL {pack}/sat_gate_map.json: gate_id {gate_id!r} "
                    f"unknown evidence catalog {catalog_id!r}"
                )
                failed += 1
                continue
            resolved |= catalogs[catalog_id]

        for evidence_type in evidence_types:
            if evidence_type not in resolved:
                print(
                    f"FAIL {pack}/sat_gate_map.json: gate_id {gate_id!r} "
                    f"evidence_type {evidence_type!r} not in cited catalogs "
                    f"{list(catalog_ids)!r}"
                )
                failed += 1

    if not failed:
        print(f"OK   {pack}: evidence catalog/type resolve")
    return failed


def validate_gate_map(
    jsonschema, pack_dir: Path, gate_map_schema: dict, catalogs: dict[str, set[str]]
) -> tuple[dict | None, int]:
    pack = pack_dir.name
    gate_map_path = pack_dir / "sat_gate_map.json"
    if not gate_map_path.is_file():
        print(f"FAIL {pack}: missing sat_gate_map.json")
        return None, 1

    gate_map = load_json(gate_map_path)
    errors = schema_errors(jsonschema, gate_map_schema, gate_map)
    if errors:
        print_schema_errors(f"{pack}/sat_gate_map.json", errors)
        return gate_map, 1

    failed = 0
    if gate_map["pack_id"] != pack:
        print(f"FAIL {pack}/sat_gate_map.json: pack_id must be {pack!r}")
        failed += 1
    if gate_map["gate_namespace"] != pack:
        print(f"FAIL {pack}/sat_gate_map.json: gate_namespace must be {pack!r}")
        failed += 1

    seen_gate_ids: set[str] = set()
    for gate in gate_map["gates"]:
        gate_id = gate["gate_id"]
        if gate_id in seen_gate_ids:
            print(f"FAIL {pack}/sat_gate_map.json: duplicate gate_id {gate_id!r}")
            failed += 1
        seen_gate_ids.add(gate_id)
        if not gate_id.startswith(f"{gate_map['gate_namespace']}."):
            print(f"FAIL {pack}/sat_gate_map.json: gate_id {gate_id!r} outside namespace")
            failed += 1

    failed += validate_gate_catalog_refs(pack, gate_map, catalogs)

    if not failed:
        print(f"OK   {pack}/sat_gate_map.json")
    return gate_map, failed


def validate_gate_links(pack: str, ledger: dict, sat_log: dict, gate_map: dict) -> int:
    failed = 0
    gates_by_id = {gate["gate_id"]: gate for gate in gate_map["gates"]}
    event_by_id: dict[str, dict] = {}

    for event in sat_log["events"]:
        event_id = event["event_id"]
        if event_id in event_by_id:
            print(f"FAIL {pack}/sat_event_log.json: duplicate event_id {event_id!r}")
            failed += 1
        event_by_id[event_id] = event

        gate_id = event["gate_id"]
        gate = gates_by_id.get(gate_id)
        if gate is None:
            print(f"FAIL {pack}/sat_event_log.json: undeclared gate_id {gate_id!r}")
            failed += 1
            continue

        if event["result"] != gate["required_result"]:
            print(
                f"FAIL {pack}/sat_event_log.json: gate_id {gate_id!r} result "
                f"{event['result']!r} != required_result {gate['required_result']!r}"
            )
            failed += 1

        evidence_type = event.get("evidence_type")
        allowed_evidence = set(gate["evidence_types"])
        if evidence_type and allowed_evidence and evidence_type not in allowed_evidence:
            print(
                f"FAIL {pack}/sat_event_log.json: gate_id {gate_id!r} evidence_type "
                f"{evidence_type!r} not in {sorted(allowed_evidence)!r}"
            )
            failed += 1

    event_gate_ids = {event["gate_id"] for event in sat_log["events"]}
    required_gate_ids = {
        gate["gate_id"] for gate in gate_map["gates"] if gate.get("example_required", False)
    }
    for gate_id in sorted(required_gate_ids - event_gate_ids):
        print(f"FAIL {pack}/sat_event_log.json: missing required example gate_id {gate_id!r}")
        failed += 1

    linked_event_ids: set[str] = set()
    for entry in ledger["entries"]:
        for event_id in entry.get("sat_event_ids", []):
            linked_event_ids.add(event_id)
            if event_id not in event_by_id:
                print(f"FAIL {pack}/handoff_ledger.json: unknown sat_event_id {event_id!r}")
                failed += 1

    for event_id in sorted(set(event_by_id) - linked_event_ids):
        print(f"FAIL {pack}/handoff_ledger.json: SAT event {event_id!r} is not linked")
        failed += 1

    if not failed:
        print(f"OK   {pack}: SAT gate map links")
    return failed


def main() -> int:
    try:
        import jsonschema
    except ImportError:
        print("pip install jsonschema", file=sys.stderr)
        return 2

    ledger_schema = json.loads((ROOT / "core_schemas/handoff_ledger.json").read_text())
    sat_schema = json.loads((ROOT / "core_schemas/sat_event_log.json").read_text())
    gate_map_schema = load_json(ROOT / "core_schemas/architecture_sat_gate_map.json")
    catalogs, catalog_failures = load_evidence_catalogs()
    examples = sorted(ROOT.glob("architectures/*/examples/handoff_ledger.json"))
    if not examples:
        print("ERROR: no architecture examples found", file=sys.stderr)
        return 2

    failed = catalog_failures
    for ledger_path in examples:
        sat_path = ledger_path.with_name("sat_event_log.json")
        pack_dir = ledger_path.parent.parent
        pack = pack_dir.name
        gate_map, gate_map_failures = validate_gate_map(
            jsonschema, pack_dir, gate_map_schema, catalogs
        )
        failed += gate_map_failures

        ledger_doc: dict | None = None
        sat_doc: dict | None = None
        for path, schema in ((ledger_path, ledger_schema), (sat_path, sat_schema)):
            if not path.is_file():
                print(f"FAIL {pack}: missing {path.name}")
                failed += 1
                continue
            doc = load_json(path)
            errors = schema_errors(jsonschema, schema, doc)
            if errors:
                failed += 1
                print_schema_errors(f"{pack}/{path.name}", errors)
            else:
                print(f"OK   {pack}/{path.name}")
                if path == ledger_path:
                    ledger_doc = doc
                elif path == sat_path:
                    sat_doc = doc

        if gate_map and ledger_doc and sat_doc:
            failed += validate_gate_links(pack, ledger_doc, sat_doc, gate_map)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
