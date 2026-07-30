#!/usr/bin/env python3
"""OIDF Canonical Registry — loads and resolves canonical keys from dictionary.yaml"""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional


class OIDFRegistry:
    """Registry for OIDF canonical keys and their metadata."""

    def __init__(self, schema_path: str = "core_schemas/canonical/dictionary.yaml"):
        self.schema_path = Path(schema_path)
        self.domains: Dict[str, Any] = {}
        self.key_index: Dict[str, Dict[str, Any]] = {}  # flat index: "domain.object.field" -> metadata
        self._load_schemas()

    def _load_schemas(self) -> None:
        """Load the canonical dictionary and build lookup indexes."""
        if not self.schema_path.is_file():
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")

        with open(self.schema_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.domains = data.get("oidf_registry", {}).get("domains", {})

        # Build flat index for O(1) lookups
        for domain_name, domain_data in self.domains.items():
            self._index_domain(domain_name, domain_data)

    def _index_domain(self, domain_name: str, domain_data: Any, prefix: str = "") -> None:
        """Recursively index all fields in a domain."""
        if isinstance(domain_data, dict):
            for key, value in domain_data.items():
                current_path = f"{prefix}.{key}" if prefix else f"{domain_name}.{key}"
                if isinstance(value, dict) and "type" in value:
                    # This is a field definition
                    self.key_index[current_path] = {
                        "domain": domain_name,
                        "path": current_path,
                        "type": value.get("type"),
                        "description": value.get("description", ""),
                        "values": value.get("values", []),
                        "properties": value.get("properties", {}),
                        "items": value.get("items", {}),
                    }
                elif isinstance(value, dict):
                    # Nested object, recurse
                    self._index_domain(domain_name, value, current_path)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            self._index_domain(domain_name, item, current_path)

    def get_canonical(self, provider: str, native_key: str) -> Optional[str]:
        """
        Resolve a provider-specific native key to its canonical OIDF key.
        Uses a mapping table for known provider -> canonical mappings.
        """
        # Provider-specific mapping tables
        provider_mappings = {
            "jira": {
                "projectId": "containers.project.id",
                "projectKey": "containers.project.key",
                "summary": "containers.task.title",
                "description": "containers.task.description",
                "issuetype": "containers.task.type",
                "status": "lifecycle.status.name",
                "priority": "lifecycle.priority.level",
                "assignee": "actors.assignee.user_id",
                "reporter": "actors.user.id",
                "created": "containers.task.created_at",
                "updated": "containers.task.updated_at",
                "duedate": "containers.task.due_date",
                "parent": "graph.parent_child.parent_id",
                "subtasks": "graph.parent_child.child_id",
                "issuelinks": "graph.blocks.blocker_id",
                "attachment": "graph.attachment.id",
                "comment": "graph.comment.id",
                "customfield_": "dynamic.custom_field.id",
                "labels": "dynamic.tag.id",
                "components": "dynamic.component.id",
                "fixVersions": "dynamic.version.id",
                "worklog": "lifecycle.metrics.time_spent",
                "watches": "graph.watcher.user_id",
                "votes": "dynamic.metadata.value",
            },
            "asana": {
                "gid": "containers.project.id",
                "name": "containers.project.name",
                "notes": "containers.project.description",
                "owner": "actors.user.id",
                "created_at": "containers.project.created_at",
                "modified_at": "containers.project.updated_at",
                "workspace": "actors.team.id",
                "assignee": "actors.assignee.user_id",
                "due_on": "containers.task.due_date",
                "completed_at": "containers.task.completed_at",
                "projects": "containers.project.id",
                "memberships": "actors.team.members",
                "tags": "dynamic.tag.id",
                "custom_fields": "dynamic.custom_field.id",
                "dependencies": "graph.blocks.blocker_id",
                "dependents": "graph.blocks.blocked_id",
                "stories": "containers.task.id",
                "sections": "containers.sprint.id",
            },
            "github": {
                "id": "containers.task.id",
                "number": "containers.task.key",
                "title": "containers.task.title",
                "body": "containers.task.description",
                "state": "lifecycle.status.name",
                "labels": "dynamic.label.id",
                "assignee": "actors.assignee.user_id",
                "author": "actors.user.id",
                "created_at": "containers.task.created_at",
                "updated_at": "containers.task.updated_at",
                "closed_at": "containers.task.completed_at",
                "milestone": "containers.milestone.id",
                "project": "containers.project.id",
                "repository": "containers.project.id",
                "comments": "graph.comment.id",
                "reactions": "dynamic.metadata.value",
                "timeline": "telemetry.audit_log.id",
            },
        }

        mappings = provider_mappings.get(provider.lower(), {})
        return mappings.get(native_key)

    def resolve_key(self, canonical_key: str) -> Optional[Dict[str, Any]]:
        """Look up metadata for a canonical key."""
        return self.key_index.get(canonical_key)

    def list_keys(self, domain: Optional[str] = None) -> List[str]:
        """List all canonical keys, optionally filtered by domain."""
        if domain:
            prefix = f"{domain}."
            return [k for k in self.key_index.keys() if k.startswith(prefix)]
        return list(self.key_index.keys())

    def get_domain_schema(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get the full schema for a domain."""
        return self.domains.get(domain)

    def validate_key_format(self, key: str) -> bool:
        """Validate canonical key follows domain.object.field format."""
        parts = key.split(".")
        return len(parts) >= 3 and parts[0] in self.domains


def main():
    """CLI entry point for testing."""
    import sys

    registry = OIDFRegistry()

    if len(sys.argv) > 1:
        if sys.argv[1] == "lookup":
            if len(sys.argv) < 4:
                print("Usage: python oidf_registry.py lookup <provider> <native_key>")
                return 1
            provider, native_key = sys.argv[2], sys.argv[3]
            result = registry.get_canonical(provider, native_key)
            print(result or "NOT FOUND")
        elif sys.argv[1] == "resolve":
            if len(sys.argv) < 3:
                print("Usage: python oidf_registry.py resolve <canonical_key>")
                return 1
            result = registry.resolve_key(sys.argv[2])
            print(yaml.dump(result) if result else "NOT FOUND")
        elif sys.argv[1] == "list":
            domain = sys.argv[2] if len(sys.argv) > 2 else None
            for key in registry.list_keys(domain):
                print(key)
        else:
            print("Usage: python oidf_registry.py [lookup|resolve|list] ...")
            return 1
    else:
        print(f"Loaded {len(registry.key_index)} canonical keys across {len(registry.domains)} domains")
        for domain in registry.domains:
            count = len(registry.list_keys(domain))
            print(f"  {domain}: {count} keys")

    return 0


if __name__ == "__main__":
    exit(main())