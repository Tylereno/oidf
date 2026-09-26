#!/usr/bin/env python
"""Acceptance test: every published OIDF schema `$id` maps to a served path.

Two checks, both derived from `.github/workflows/pages.yml` staging:

1. Mapping — every `$id` under ``core_schemas/`` equals the Pages base plus the
   path at which that file is served (``idl/`` flattened away).
2. Artifact — with ``--public <dir>``, every file that declares an `$id` exists
   in the staged Pages artifact at that served path, so no published `$id` 404s.
   Only files that declare an `$id` are required to be served: that set *is* the
   published identifier namespace.

Usage::

    python tooling/verify_pages_ids.py                  # mapping only (fast)
    python tooling/verify_pages_ids.py --public public  # + staged artifact check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BASE = "https://openlexicon.github.io/oidf/schemas/"
DEFAULT_ROOT = Path("core_schemas")
STAGED_SUFFIXES = (".json", ".yaml", ".yml")


def served_rel(path: Path, root: Path) -> str:
    """Return the Pages-relative served path for a schema file."""
    rel = path.relative_to(root)
    parts = list(rel.parts)
    if parts and parts[0] == "idl":
        parts = parts[1:]
    return "/".join(["schemas", *parts])


def load_id(path: Path) -> str | None:
    if path.suffix.lower() == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"FAIL  {path}: unreadable JSON ({exc})")
            return None
        return data.get("$id") if isinstance(data, dict) else None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("$id:"):
            return stripped.split(":", 1)[1].strip().strip("\"'")
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--public", default=None,
                        help="staged Pages artifact directory to verify")
    parser.add_argument("--base", default=BASE)
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"FAIL  schema root not found: {root}")
        return 2

    files = sorted(p for p in root.rglob("*")
                   if p.is_file() and p.suffix.lower() in STAGED_SUFFIXES
                   and p.name != "README.md")
    problems: list[str] = []
    ids_checked = 0
    artifacts_checked = 0

    for path in files:
        rel = served_rel(path, root)
        schema_id = load_id(path)
        if not schema_id:
            continue
        ids_checked += 1
        expected = args.base + rel[len("schemas/"):]
        if not schema_id.startswith(args.base):
            problems.append(
                f"{path}: $id is outside the authority host\n"
                f"      got      {schema_id}\n"
                f"      expected {args.base}…"
            )
        elif schema_id != expected:
            problems.append(
                f"{path}: $id does not match its served path\n"
                f"      got      {schema_id}\n"
                f"      expected {expected}"
            )
        if args.public:
            artifacts_checked += 1
            artifact = Path(args.public) / rel
            if not artifact.is_file():
                problems.append(
                    f"{path}: not staged — {artifact} missing "
                    f"(published $id would 404)"
                )

    print(f"schemas scanned  : {len(files)}")
    print(f"$id declared     : {ids_checked}")
    print(f"authority host   : {args.base}")
    if args.public:
        print(f"$id staged       : {artifacts_checked}")
        print(f"staged artifact  : {args.public}")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for item in problems:
            print(f"  - {item}")
        return 1
    print("\nOK: every published $id maps to its served path")
    return 0


if __name__ == "__main__":
    sys.exit(main())
