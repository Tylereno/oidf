#!/usr/bin/env python3
"""OIDF Translator — converts native platform payloads to canonical OIDF format"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Union

from oidf_registry import OIDFRegistry


class OIDFTranslator:
    """Translates native platform data to canonical OIDF format."""

    def __init__(self, registry: Optional[OIDFRegistry] = None):
        self.registry = registry or OIDFRegistry()

    def translate(self, provider: str, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Translate a native platform payload to canonical OIDF format.

        Args:
            provider: Source platform ('jira', 'asana', 'github', etc.)
            raw_payload: Raw data from the platform API

        Returns:
            Dictionary with canonical OIDF keys
        """
        translated = {}
        provider_lower = provider.lower()

        for native_key, value in raw_payload.items():
            canonical_key = self.registry.get_canonical(provider_lower, native_key)

            if canonical_key:
                # Ensure nested structure exists
                self._set_nested(translated, canonical_key, value)
            else:
                # Pass through unmapped keys with provider prefix
                self._set_nested(translated, f"dynamic.metadata.{provider_lower}.{native_key}", value)

        return translated

    def translate_batch(self, provider: str, raw_payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Translate multiple payloads."""
        return [self.translate(provider, payload) for payload in raw_payloads]

    def translate_jira_issue(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Specialized translation for Jira issue objects with nested fields."""
        translated = self.translate("jira", issue)

        # Handle nested Jira fields
        fields = issue.get("fields", {})
        if fields:
            field_translations = self.translate("jira", fields)
            translated.update(field_translations)

        # Extract changelog if present
        if "changelog" in issue:
            translated["lifecycle.history"] = self._translate_jira_changelog(issue["changelog"])

        return translated

    def translate_asana_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Specialized translation for Asana task objects."""
        translated = self.translate("asana", task)

        # Handle custom fields
        if "custom_fields" in task:
            custom = {}
            for cf in task["custom_fields"]:
                gid = cf.get("gid")
                value = cf.get("text_value") or cf.get("number_value") or cf.get("enum_value", {}).get("name")
                if gid and value is not None:
                    custom[gid] = value
            translated["dynamic.custom_field_value"] = custom

        return translated

    def translate_github_issue(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Specialized translation for GitHub issue objects."""
        translated = self.translate("github", issue)

        # Extract repository info
        if "repository" in issue:
            repo = issue["repository"]
            translated["containers.project"] = {
                "id": f"github-repo-{repo.get('id')}",
                "name": repo.get("full_name"),
                "source_system_id": str(repo.get("id")),
            }

        # Extract labels as tags
        if "labels" in issue:
            translated["dynamic.tag"] = [
                {"id": f"github-label-{lbl.get('id')}", "name": lbl.get("name"), "color": lbl.get("color")}
                for lbl in issue["labels"]
            ]

        return translated

    def _translate_jira_changelog(self, changelog: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Translate Jira changelog to lifecycle history."""
        history = []
        for entry in changelog.get("histories", []):
            for item in entry.get("items", []):
                history.append({
                    "lifecycle.transition.id": item.get("field"),
                    "lifecycle.transition.from": item.get("fromString"),
                    "lifecycle.transition.to": item.get("toString"),
                    "lifecycle.transition.timestamp": entry.get("created"),
                    "lifecycle.transition.author": entry.get("author", {}).get("accountId"),
                })
        return history

    def _set_nested(self, obj: Dict[str, Any], path: str, value: Any) -> None:
        """Set a value in a nested dictionary using dot notation."""
        parts = path.split(".")
        current = obj

        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                # Overwrite non-dict with dict to allow nesting
                current[part] = {}
            current = current[part]

        current[parts[-1]] = value

    def reverse_translate(self, provider: str, canonical_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert canonical OIDF payload back to provider-specific format.
        Uses reverse mapping from canonical keys to native keys.
        """
        reverse_mappings = {
            "jira": {
                "containers.project.id": "projectId",
                "containers.project.key": "projectKey",
                "containers.task.id": "id",
                "containers.task.key": "key",
                "containers.task.title": "summary",
                "containers.task.description": "description",
                "containers.task.type": "issuetype",
                "lifecycle.status.name": "status",
                "lifecycle.priority.level": "priority",
                "actors.assignee.user_id": "assignee",
                "actors.user.id": "reporter",
                "containers.task.created_at": "created",
                "containers.task.updated_at": "updated",
                "containers.task.due_date": "duedate",
                "graph.parent_child.parent_id": "parent",
                "graph.attachment.id": "attachment",
                "graph.comment.id": "comment",
                "dynamic.custom_field.id": "customfield_",
                "dynamic.tag.id": "labels",
            },
            "asana": {
                "containers.project.id": "gid",
                "containers.project.name": "name",
                "containers.project.description": "notes",
                "actors.user.id": "owner",
                "containers.project.created_at": "created_at",
                "containers.project.updated_at": "modified_at",
                "actors.team.id": "workspace",
                "actors.assignee.user_id": "assignee",
                "containers.task.due_date": "due_on",
                "containers.task.completed_at": "completed_at",
                "dynamic.tag.id": "tags",
                "dynamic.custom_field.id": "custom_fields",
                "graph.blocks.blocker_id": "dependencies",
                "graph.blocks.blocked_id": "dependents",
            },
            "github": {
                "containers.task.id": "id",
                "containers.task.key": "number",
                "containers.task.title": "title",
                "containers.task.description": "body",
                "lifecycle.status.name": "state",
                "dynamic.label.id": "labels",
                "actors.assignee.user_id": "assignee",
                "actors.user.id": "author",
                "containers.task.created_at": "created_at",
                "containers.task.updated_at": "updated_at",
                "containers.task.completed_at": "closed_at",
                "containers.milestone.id": "milestone",
                "containers.project.id": "project",
                "graph.comment.id": "comments",
            },
        }

        mappings = reverse_mappings.get(provider.lower(), {})
        result = {}

        def flatten(d: Dict[str, Any], prefix: str = "") -> Dict[str, str]:
            """Flatten nested dict to dot-notation paths."""
            flat = {}
            for k, v in d.items():
                path = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict) and v:
                    flat.update(flatten(v, path))
                else:
                    flat[path] = v
            return flat

        flat_canonical = flatten(canonical_payload)

        for canonical_key, value in flat_canonical.items():
            native_key = mappings.get(canonical_key)
            if native_key:
                # Set value at native key path
                self._set_nested(result, native_key, value)
            else:
                # Fallback: use canonical key in metadata
                self._set_nested(result, f"oidf.{canonical_key}", value)

        return result


def main():
    """CLI entry point for testing."""
    import sys
    import json

    if len(sys.argv) < 3:
        print("Usage: python oidf_translator.py <provider> <input.json>")
        return 1

    provider = sys.argv[1]
    input_file = sys.argv[2]

    with open(input_file, "r") as f:
        raw = json.load(f)

    registry = OIDFRegistry()
    translator = OIDFTranslator(registry)

    if isinstance(raw, list):
        result = translator.translate_batch(provider, raw)
    else:
        result = translator.translate(provider, raw)

    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    exit(main())