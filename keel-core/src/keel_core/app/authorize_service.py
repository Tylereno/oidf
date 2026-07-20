"""Authorize policy service — ADR-0007, deny by default."""

from __future__ import annotations

from typing import Any


class AuthorizeService:
    def __init__(self, grants: list[dict[str, Any]] | None = None) -> None:
        self._grants = list(grants or [])

    def set_grants(self, grants: list[dict[str, Any]]) -> None:
        self._grants = list(grants)

    def authorize(self, request: dict[str, Any]) -> dict[str, Any]:
        pid = request["principal_id"]
        action = request["action"]
        for g in self._grants:
            if g.get("principal_id") != pid:
                continue
            if action in g.get("actions", []):
                return {"decision": "Allow"}
        return {"decision": "Deny", "reason_code": "NoGrant"}
