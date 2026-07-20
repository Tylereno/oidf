from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from keel_reference.schema import validate


@dataclass
class AuthorizePort:
    """Core policy port (ADR-0007). Deny by default."""

    grants: list[dict[str, Any]] = field(default_factory=list)

    def authorize(self, request: dict[str, Any]) -> dict[str, str]:
        validate("security/authorize_request.json", request)
        pid = request["principal_id"]
        action = request["action"]
        for g in self.grants:
            if g.get("principal_id") != pid:
                continue
            if action in g.get("actions", []):
                return {"decision": "Allow"}
        return {"decision": "Deny", "reason_code": "NoGrant"}
