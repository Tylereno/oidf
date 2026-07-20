#!/usr/bin/env python3
"""Validate OIDF JSON Schema IDL files (Wave 1 CI).

Checks:
  1. Each file parses as JSON
  2. Draft 2020-12 metaschema validation (when jsonschema is installed)
  3. Relative $ref targets exist on disk
  4. $id values are unique across the tree
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


META_DRAFT = "https://json-schema.org/draft/2020-12/schema"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_schemas(root: Path) -> list[Path]:
    return sorted(root.rglob("*.json"))


def check_relative_refs(path: Path, doc: Any, errors: list[str]) -> None:
    def walk(node: Any) -> None:
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str) and not ref.startswith("#") and "://" not in ref:
                target = (path.parent / ref).resolve()
                if not target.is_file():
                    errors.append(f"{path}: missing $ref target {ref} -> {target}")
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(doc)


def validate_metaschema(path: Path, doc: Any, errors: list[str]) -> None:
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError:
        errors.append("jsonschema package not installed (pip install jsonschema)")
        return

    try:
        Draft202012Validator.check_schema(doc)
    except Exception as exc:  # noqa: BLE001 — surface any schema error
        errors.append(f"{path}: metaschema validation failed: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default="core_schemas/idl",
        type=Path,
        help="Directory of JSON Schema files (default: core_schemas/idl)",
    )
    args = parser.parse_args()
    root = args.root
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 2

    files = collect_schemas(root)
    if not files:
        print(f"ERROR: no JSON files under {root}", file=sys.stderr)
        return 2

    errors: list[str] = []
    ids: dict[str, Path] = {}

    for path in files:
        try:
            doc = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue

        if not isinstance(doc, dict):
            errors.append(f"{path}: top-level value must be an object")
            continue

        schema_uri = doc.get("$schema")
        if schema_uri and schema_uri != META_DRAFT:
            errors.append(f"{path}: unexpected $schema {schema_uri!r} (want {META_DRAFT})")

        sid = doc.get("$id")
        if isinstance(sid, str) and sid:
            # Normalize path-ish ids for duplicate detection
            key = sid
            parsed = urlparse(sid)
            if parsed.scheme and parsed.path:
                key = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if key in ids:
                errors.append(f"{path}: duplicate $id {sid!r} (also {ids[key]})")
            else:
                ids[key] = path

        check_relative_refs(path, doc, errors)
        validate_metaschema(path, doc, errors)

    if errors:
        print(f"FAILED ({len(errors)} issue(s)) under {root}:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: {len(files)} schemas validated under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
