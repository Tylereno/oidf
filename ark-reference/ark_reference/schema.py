from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

SPECS_ROOT = Path(__file__).resolve().parents[2] / "ark-specs" / "idl"


def _load_registry() -> Registry:
    registry = Registry()
    for path in SPECS_ROOT.rglob("*.json"):
        with path.open() as f:
            schema = json.load(f)
        if "$id" in schema:
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry


@lru_cache(maxsize=1)
def registry() -> Registry:
    return _load_registry()


@lru_cache(maxsize=32)
def _validator(schema_path: str) -> Draft202012Validator:
    path = SPECS_ROOT / schema_path
    with path.open() as f:
        schema = json.load(f)
    return Draft202012Validator(schema, registry=registry())


def validate(schema_relpath: str, instance: dict[str, Any]) -> None:
    _validator(schema_relpath).validate(instance)
