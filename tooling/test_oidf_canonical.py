#!/usr/bin/env python3
"""Unit tests for OIDF Canonical Registry and Translator (stdlib unittest)."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLING = ROOT / "tooling"
sys.path.insert(0, str(TOOLING))

from oidf_registry import OIDFRegistry
from oidf_translator import OIDFTranslator


class OIDFRegistryTests(unittest.TestCase):
    """Tests for the canonical dictionary loader and key resolver."""

    def setUp(self):
        self.registry = OIDFRegistry()

    def test_loads_all_six_domains(self):
        expected_domains = {
            "containers",
            "actors",
            "lifecycle",
            "graph",
            "dynamic",
            "telemetry",
        }
        self.assertEqual(set(self.registry.domains.keys()), expected_domains)

    def test_key_count_exceeds_300(self):
        """Dictionary must meet the 300+ element density target."""
        total = len(self.registry.key_index)
        self.assertGreaterEqual(total, 300, f"Only {total} canonical keys loaded")

    def test_resolve_known_key(self):
        result = self.registry.resolve_key("containers.project.id")
        self.assertIsNotNone(result)
        self.assertEqual(result["domain"], "containers")
        self.assertEqual(result["type"], "uuid")

    def test_resolve_unknown_key_returns_none(self):
        self.assertIsNone(self.registry.resolve_key("nonexistent.field.key"))

    def test_lookup_jira_summary(self):
        canonical = self.registry.get_canonical("jira", "summary")
        self.assertEqual(canonical, "containers.task.title")

    def test_lookup_jira_accountId(self):
        canonical = self.registry.get_canonical("jira", "accountId")
        self.assertEqual(canonical, "actors.user.id")

    def test_lookup_github_title(self):
        canonical = self.registry.get_canonical("github", "title")
        self.assertEqual(canonical, "containers.task.title")

    def test_lookup_asana_gid(self):
        canonical = self.registry.get_canonical("asana", "gid")
        self.assertEqual(canonical, "containers.project.id")

    def test_lookup_unknown_provider_returns_none(self):
        self.assertIsNone(self.registry.get_canonical("trello", "unknown_field"))

    def test_lookup_unknown_native_key_returns_none(self):
        self.assertIsNone(self.registry.get_canonical("jira", "nonexistent_field"))

    def test_list_keys_by_domain(self):
        container_keys = self.registry.list_keys("containers")
        self.assertTrue(all(k.startswith("containers.") for k in container_keys))
        self.assertGreater(len(container_keys), 10)

    def test_list_keys_all(self):
        all_keys = self.registry.list_keys()
        self.assertEqual(len(all_keys), len(self.registry.key_index))

    def test_validate_key_format_valid(self):
        self.assertTrue(self.registry.validate_key_format("containers.project.id"))

    def test_validate_key_format_invalid(self):
        self.assertFalse(self.registry.validate_key_format("invalid"))
        self.assertFalse(self.registry.validate_key_format("unknown.field.key"))

    def test_get_domain_schema(self):
        schema = self.registry.get_domain_schema("containers")
        self.assertIsNotNone(schema)
        self.assertIn("project", schema)

    def test_get_domain_schema_unknown(self):
        self.assertIsNone(self.registry.get_domain_schema("nonexistent"))

    def test_all_keys_follow_dot_notation(self):
        """Every canonical key must follow domain.object.attribute format."""
        for key in self.registry.key_index:
            parts = key.split(".")
            self.assertGreaterEqual(len(parts), 3, f"Key '{key}' has fewer than 3 segments")
            self.assertIn(parts[0], self.registry.domains, f"Key '{key}' has unknown domain '{parts[0]}'")


class OIDFTranslatorTests(unittest.TestCase):
    """Tests for the native-to-canonical translation engine."""

    def setUp(self):
        self.registry = OIDFRegistry()
        self.translator = OIDFTranslator(self.registry)
        self.test_payload = {
            "projectId": "10001",
            "summary": "Implement OIDF canonical schema",
            "description": "Create unified data dictionary for PM platform integration",
            "issuetype": "Story",
            "status": {"name": "In Progress", "statusCategory": "indeterminate"},
            "priority": {"name": "High"},
            "assignee": {"accountId": "5b10a2d44c8b490b0079425f", "displayName": "Tyler Eno"},
            "reporter": {"accountId": "5b10a2d44c8b490b0079425f", "displayName": "Tyler Eno"},
            "created": "2026-07-29T15:30:00.000Z",
            "updated": "2026-07-29T16:45:00.000Z",
            "duedate": "2026-08-15",
            "customfield_10002": "8",
            "labels": ["oidf", "canonical", "schema"],
        }

    def test_translate_jira_basic(self):
        result = self.translator.translate("jira", self.test_payload)
        self.assertIn("containers", result)
        self.assertIn("lifecycle", result)
        self.assertIn("actors", result)

    def test_translate_jira_summary_to_title(self):
        result = self.translator.translate("jira", self.test_payload)
        self.assertEqual(
            result["containers"]["task"]["title"],
            "Implement OIDF canonical schema",
        )

    def test_translate_jira_project_id(self):
        result = self.translator.translate("jira", self.test_payload)
        self.assertEqual(result["containers"]["project"]["id"], "10001")

    def test_translate_jira_created_at(self):
        result = self.translator.translate("jira", self.test_payload)
        self.assertEqual(
            result["containers"]["task"]["created_at"],
            "2026-07-29T15:30:00.000Z",
        )

    def test_translate_jira_unmapped_fields_pass_through(self):
        result = self.translator.translate("jira", self.test_payload)
        # customfield_10002 is not in the lookup table, should pass through
        self.assertIn("dynamic", result)
        self.assertIn("metadata", result["dynamic"])
        self.assertIn("jira", result["dynamic"]["metadata"])
        self.assertEqual(
            result["dynamic"]["metadata"]["jira"]["customfield_10002"],
            "8",
        )

    def test_translate_jira_labels(self):
        result = self.translator.translate("jira", self.test_payload)
        self.assertEqual(
            result["dynamic"]["tag"]["id"],
            ["oidf", "canonical", "schema"],
        )

    def test_translate_jira_issue_specialized(self):
        issue = {"fields": self.test_payload, "changelog": {"histories": []}}
        result = self.translator.translate_jira_issue(issue)
        self.assertIn("containers", result)
        self.assertEqual(
            result["containers"]["task"]["title"],
            "Implement OIDF canonical schema",
        )

    def test_translate_jira_changelog(self):
        issue = {
            "fields": {"summary": "Test"},
            "changelog": {
                "histories": [
                    {
                        "created": "2026-07-29T16:00:00.000Z",
                        "items": [
                            {
                                "field": "status",
                                "fromString": "To Do",
                                "toString": "In Progress",
                            }
                        ],
                    }
                ]
            },
        }
        result = self.translator.translate_jira_issue(issue)
        self.assertIn("lifecycle", result)
        self.assertIn("history", result["lifecycle"])

    def test_translate_github_issue(self):
        github_payload = {
            "title": "Fix bug in translator",
            "body": "The translator has a bug",
            "state": "open",
            "labels": [{"id": "1", "name": "bug", "color": "f00"}],
            "created_at": "2026-07-29T10:00:00Z",
            "repository": {"id": "123", "full_name": "Tylereno/oidf"},
        }
        result = self.translator.translate_github_issue(github_payload)
        self.assertEqual(result["containers"]["task"]["title"], "Fix bug in translator")
        self.assertEqual(result["containers"]["project"]["name"], "Tylereno/oidf")
        self.assertEqual(result["dynamic"]["tag"][0]["name"], "bug")

    def test_translate_asana_task(self):
        asana_payload = {
            "name": "Asana task",
            "notes": "Task description",
            "assignee": {"gid": "user-1"},
            "custom_fields": [
                {"gid": "cf-1", "text_value": "custom value"},
            ],
        }
        result = self.translator.translate_asana_task(asana_payload)
        self.assertEqual(result["containers"]["task"]["title"], "Asana task")
        self.assertIn("custom_field_value", result["dynamic"])

    def test_translate_batch(self):
        payloads = [self.test_payload, {"summary": "Second task"}]
        results = self.translator.translate_batch("jira", payloads)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["containers"]["task"]["title"], "Implement OIDF canonical schema")
        self.assertEqual(results[1]["containers"]["task"]["title"], "Second task")

    def test_reverse_translate_jira(self):
        canonical = {
            "containers": {
                "project": {"id": "10001"},
                "task": {"title": "Test task", "type": "Story"},
            },
            "lifecycle": {"status": {"name": "In Progress"}},
        }
        result = self.translator.reverse_translate("jira", canonical)
        self.assertEqual(result["projectId"], "10001")
        self.assertEqual(result["summary"], "Test task")
        self.assertEqual(result["issuetype"], "Story")

    def test_translate_empty_payload(self):
        result = self.translator.translate("jira", {})
        self.assertEqual(result, {})

    def test_translate_case_insensitive_provider(self):
        result_lower = self.translator.translate("jira", {"summary": "Test"})
        result_upper = self.translator.translate("JIRA", {"summary": "Test"})
        self.assertEqual(
            result_lower["containers"]["task"]["title"],
            result_upper["containers"]["task"]["title"],
        )


class OIDFIntegrationTests(unittest.TestCase):
    """Integration tests using the checked-in test payload file."""

    def setUp(self):
        self.registry = OIDFRegistry()
        self.translator = OIDFTranslator(self.registry)
        self.test_file = ROOT / "test_jira_issue.json"

    def test_test_payload_file_exists(self):
        self.assertTrue(self.test_file.is_file(), "test_jira_issue.json must exist")

    def test_translate_test_payload_file(self):
        with open(self.test_file) as f:
            raw = json.load(f)
        result = self.translator.translate("jira", raw)
        self.assertEqual(
            result["containers"]["task"]["title"],
            "Implement OIDF canonical schema",
        )
        self.assertEqual(result["containers"]["project"]["id"], "10001")
        self.assertEqual(result["containers"]["task"]["type"], "Story")

    def test_translate_test_payload_reverse(self):
        """Round-trip: translate to canonical, then back to Jira format."""
        with open(self.test_file) as f:
            raw = json.load(f)
        canonical = self.translator.translate("jira", raw)
        reversed_payload = self.translator.reverse_translate("jira", canonical)
        # Core fields should survive the round-trip
        self.assertEqual(reversed_payload["summary"], raw["summary"])
        self.assertEqual(reversed_payload["description"], raw["description"])
        self.assertEqual(reversed_payload["issuetype"], raw["issuetype"])


if __name__ == "__main__":
    unittest.main()
