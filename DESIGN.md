---
version: alpha
name: OIDF Canonical Schema
description: Deterministic data model for cross-platform project management integration.
colors:
  primary: "#0A2540"
  secondary: "#475569"
  accent: "#2563EB"
  neutral: "#F8FAFC"
typography:
  header:
    fontFamily: Inter
    fontSize: 1.5rem
    fontWeight: 600
  body:
    fontFamily: Inter
    fontSize: 1rem
  code:
    fontFamily: "JetBrains Mono"
    fontSize: 0.9rem
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
---

## Overview

The Open Integration Data Format (OIDF) provides a canonical schema and DSL for normalizing fragmented data from project management platforms (Jira, Asana, GitHub, Trello) and operational telemetry. This model is intended for consumption by the Keel translation engine, enabling deterministic data interchange in systems architecture.

## Canonical Domains

The OIDF taxonomy is organized into six functional domains:

1. **Containers**: Hierarchical organization (Projects, Epics, Sprints).
2. **Actors**: Governance and identity (Users, Teams, Roles).
3. **Lifecycle**: Workflow state transitions and performance metrics.
4. **Graph**: Network topology (Dependencies, Blocks, Links).
5. **Dynamic**: Extensible metadata (Tags, Custom fields).
6. **Telemetry**: Operational logs and system health metadata.

## Schema Implementation

The schema utilizes a dot-notation pathing strategy: `{domain}.{object}.{attribute}`. 

### Implementation Example

```yaml
oidf_key: "containers.project.id"
data_type: "uuid"
description: "Canonical project identifier."
source_mappings:
  jira: "projectId"
  asana: "gid"
  github: "project_id"
```

## Governance

- **Deterministic**: Every OIDF field maps directly to source attributes.
- **Extensible**: Use the `dynamic` domain for platform-specific telemetry.
- **Interoperable**: Designed for consumption by the Keel translation engine.
