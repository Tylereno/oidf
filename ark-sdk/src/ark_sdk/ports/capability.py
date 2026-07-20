"""Capability descriptor validation hook — schema lives in ark-specs/idl."""

from __future__ import annotations

from typing import Any


REQUIRED_KEYS = ("plugin_id", "plugin_version", "capabilities", "publishes", "subscribes")


def assert_capability_shape(descriptor: dict[str, Any]) -> None:
    missing = [k for k in REQUIRED_KEYS if k not in descriptor]
    if missing:
        raise ValueError(f"CapabilityDescriptor missing keys: {missing}")
