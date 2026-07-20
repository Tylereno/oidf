# RFC 0011 — Configuration

**Status:** Proposed  
**Phase:** 1  
**Depends on:** 0000, 0002, 0003, 0005, 0007  

## Purpose

Specify Configuration as a Core capability: declarative data that changes behavior without enlarging Core code.

## Goals

- Prefer configuration over Core features (Prime Directive).
- Versioned, attributable, syncable configuration documents.
- MachineDefinitions, evidence requirements, and feature flags as data.

## Non-Goals

- Hot-reload product choice
- Secret management vendor selection (secrets are constrained; see Security)
- Unlimited dynamic scripting inside Core (Zero Magic Policy)

## Requirements

1. Behavior that can be Configuration SHALL be Configuration before it becomes Core code.
2. Configuration documents SHALL be versioned and attributable.
3. Changes to transition-affecting configuration SHALL be auditable via Events.
4. Configuration resolution SHALL work offline from local cache.
5. Configuration MUST NOT allow arbitrary remote code execution or reflective magic inside Core.

## Constraints

- No hidden convention-over-configuration that obscures behavior (Zero Magic).
- Configuration is data, not Plugins; Plugins may supply configuration adapters for enterprise sources.
- Secrets SHOULD NOT live in general Configuration documents; use Identity/Security secret ports.

## Configuration Domains (Initial)

| Domain | Examples |
|---|---|
| MachineDefinitions | States, transitions, evidence requirements |
| Authorization policy data | Role grants for transitions |
| Sync policy | Affinity, batch sizes, quarantine behavior |
| Plugin enablement | Which Plugins run on a node |
| Feature flags | Explicit boolean/tri-state flags—no scripting |

## Change Flow

1. Authorized principal proposes ConfigRevision.
2. Event `ConfigurationRevised` (illustrative) appended.
3. Engines resolve Config via ConfigResolve at evaluation time, pinning as required for determinism (especially State Engine).

## Determinism Rule

State Transition evaluation SHALL pin the Configuration revision used, and record that pin in the resulting Event metadata so Replay is reproducible.

## Interfaces (Abstract)

| Interface | Purpose |
|---|---|
| ConfigResolve(domain, key, at_revision?) | Read effective config |
| ConfigPropose(document) | Authorized revision publish |
| ConfigPin(ctx, revision) | Bind evaluation |

## Examples

Transition `Installed → Commissioned` requires Evidence types listed in MachineDefinition config revision `12`. Replay of a year-old Event uses revision `12`, not today’s revision `40`.

## Open Questions

1. Are MachineDefinitions part of CDO or global Configuration?  
   **Working assumption:** referenced by CDO (policy refs) and stored as versioned Configuration documents; CDO does not inline entire machines by necessity.
2. Cross-node config authority in multi-writer future?  
   **Deferred;** v1 follows Deployment affinity from 0008.

## Future Extensions

- Signed configuration baselines as Evidence of approved process

## Related RFCs

0005 State Engine · 0007 Plugin System · 0008 Synchronization · 0009 Identity · 0010 Versioning · 0012 Security
