# OIDF Canonical Data Dictionary

Machine-readable canonical schema for cross-platform project management integration.

## Overview

The OIDF Canonical Data Dictionary (`dictionary.yaml`) defines a unified, deterministic data model that normalizes fragmented data from disparate project management platforms (Jira, Asana, GitHub, Trello) and operational telemetry into a single canonical format.

This dictionary serves as the target schema for the **Keel** translation engine (separate repo: `Tylereno/keel`).

## Structure

The dictionary is organized into **6 domains**, each containing typed objects with canonical fields:

| Domain | Prefix | Scope |
|---|---|---|
| `containers` | `containers.` | Projects, Epics, Tasks, Sprints, Milestones, Releases |
| `actors` | `actors.` | Users, Teams, Roles, Permissions, Auth Scopes, Assignees |
| `lifecycle` | `lifecycle.` | Status, Transitions, Severity, Priority, SLAs, Metrics |
| `graph` | `graph.` | Parent/Child, Blocks, Relates-To, Cross-links, Attachments, Comments |
| `dynamic` | `dynamic.` | Custom fields, Tags, Labels, Components, Versions, Metadata |
| `telemetry` | `telemetry.` | Webhook events, Event state, System health, Release feeds, Audit logs |

### Canonical Key Format

All keys follow deterministic dot-notation: `{domain}.{object}.{attribute}`

```
containers.project.id
actors.user.email
lifecycle.status.name
graph.parent_child.parent_id
dynamic.custom_field.key
telemetry.webhook_event.provider
```

## Field Specification

Each field is defined with:

- **`type`**: Data type (`uuid`, `string`, `enum`, `timestamp_iso8601`, `date_iso8601`, `boolean`, `integer`, `number`, `array`, `object`)
- **`description`**: Concise definition of the canonical element
- **`values`**: (enum only) Allowed values
- **`items`**: (array only) Item type reference
- **`properties`**: (object only) Nested property definitions

## Tooling

The `tooling/` directory provides:

- **`oidf_registry.py`** — Loads the dictionary, builds O(1) lookup indexes, resolves provider-native keys to canonical keys
- **`oidf_translator.py`** — Translates native platform payloads (Jira/Asana/GitHub) to canonical OIDF format and back

### CLI Usage

```bash
# Show summary
python tooling/oidf_registry.py

# Resolve a canonical key
python tooling/oidf_registry.py resolve containers.project.id

# Look up provider-native key
python tooling/oidf_registry.py lookup jira summary

# List all keys in a domain
python tooling/oidf_registry.py list containers

# Translate a native payload
python tooling/oidf_translator.py jira test_jira_issue.json
```

## Validation

```bash
# Registry summary
python tooling/oidf_registry.py

# Translate test payload
python tooling/oidf_translator.py jira test_jira_issue.json

# Unit tests
python -m unittest tooling.test_oidf_canonical -v
```

## Relationship to Keel

OIDF is the **format**. Keel is the **runtime** that implements it. This dictionary defines the canonical schema that Keel's prism-translation engine resolves against. Provider-specific source mappings live in `oidf_registry.py` as lookup tables, not in the dictionary itself, to keep the dictionary platform-agnostic.

**Baseline:** `KEEL-SPEC-BASELINE-2026.07.20`
