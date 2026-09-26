#!/usr/bin/env python3
"""Re-point the OIDF published namespace from the assumed org host to the
live GitHub Pages host that actually serves this repository today.

Why: `Tylereno/oidf` is served by Pages at https://tylereno.me/oidf/ (the
account-level Pages custom domain; `tylereno.github.io/oidf/` 301-redirects
there). `openlexicon.github.io/oidf/` is a 404 because the repository is not
(in the free-plan) OpenLexicon org. $id values must resolve.

Deterministic, idempotent, no semantic edits: literal string replacement only.

  python repoint_to_live_host.py            # dry run
  python repoint_to_live_host.py --apply    # write
"""
from __future__ import annotations

import sys
from pathlib import Path

# Script lives in tooling/ : the repo root is one level up. Get this wrong and the
# sweep silently scans a single directory, so assert the marker file exists.
ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / "core_schemas").is_dir():
    raise SystemExit(f"refusing to run: {ROOT} does not look like the OIDF repo root")
OLD_HOST = "openlexicon.github.io/oidf"
NEW_HOST = "tylereno.me/oidf"

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
SKIP_SUFFIX = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".woff", ".woff2", ".zip", ".pyc"}


def walk() -> list[Path]:
    out: list[Path] = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in SKIP_SUFFIX:
            continue
        if p.name == Path(__file__).name:
            continue
        out.append(p)
    return out


def main() -> int:
    apply = "--apply" in sys.argv
    total = 0
    touched = 0
    for p in walk():
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        n = text.count(OLD_HOST)
        if not n:
            continue
        rel = p.relative_to(ROOT).as_posix()
        print(f"  {n:>3}  {rel}")
        total += n
        touched += 1
        if apply:
            p.write_text(text.replace(OLD_HOST, NEW_HOST), encoding="utf-8", newline="")

    mode = "APPLIED" if apply else "DRY RUN"
    print(f"\n{mode}: {total} occurrence(s) in {touched} file(s)")
    print(f"  {OLD_HOST}  ->  {NEW_HOST}")
    if not apply:
        print("\nRe-run with --apply to write.")
        return 0

    # Post-conditions: old host gone everywhere; new host present where expected.
    leftovers = []
    new_hits = 0
    for p in walk():
        try:
            t = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if OLD_HOST in t:
            leftovers.append(p.relative_to(ROOT).as_posix())
        new_hits += t.count(NEW_HOST)
    print(f"\nVERIFY old host remaining: {leftovers or 'none'}")
    print(f"VERIFY new host occurrences: {new_hits}")
    return 0 if not leftovers else 1


if __name__ == "__main__":
    raise SystemExit(main())
