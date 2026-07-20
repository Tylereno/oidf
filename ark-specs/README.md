# ark-specs

**Ownership:** ARK Architecture maintainers  
**Role:** Source of truth

## Responsibility

RFCs, ADRs, standards, glossary, and interface specifications for ARK.

## Boundaries

- Contains no application code.
- Must not depend on any code repository.
- All other repositories consume approved artifacts from here.

## Index

| Document | Title | Phase |
|---|---|---|
| [0000-CONSTITUTION.md](./0000-CONSTITUTION.md) | Master Architectural Charter | — |
| [0001-REPOSITORY-TOPOLOGY.md](./0001-REPOSITORY-TOPOLOGY.md) | Top-Level Repository Topology | 0 |
| [0002-UBIQUITOUS-LANGUAGE.md](./0002-UBIQUITOUS-LANGUAGE.md) | Ubiquitous Language Glossary | 0.5 |
| [0003-REFERENCE-ARCHITECTURE.md](./0003-REFERENCE-ARCHITECTURE.md) | Reference Architecture | 1 |
| [0004-CANONICAL-DEPLOYMENT-OBJECT.md](./0004-CANONICAL-DEPLOYMENT-OBJECT.md) | Canonical Deployment Object | 1 |
| [0005-STATE-ENGINE.md](./0005-STATE-ENGINE.md) | State Engine | 1 |
| [0006-EVENT-MODEL.md](./0006-EVENT-MODEL.md) | Event Model | 1 |
| [0007-PLUGIN-SYSTEM.md](./0007-PLUGIN-SYSTEM.md) | Plugin System | 1 |
| [0008-SYNCHRONIZATION-ENGINE.md](./0008-SYNCHRONIZATION-ENGINE.md) | Synchronization & Edge | 1 |
| [0009-IDENTITY.md](./0009-IDENTITY.md) | Identity Interfaces | 1 |
| [0010-VERSIONING.md](./0010-VERSIONING.md) | Versioning | 1 |
| [0011-CONFIGURATION.md](./0011-CONFIGURATION.md) | Configuration | 1 |
| [0012-SECURITY.md](./0012-SECURITY.md) | Security Architecture | 1 |
| [0013-PHASE-1-SCORECARD.md](./0013-PHASE-1-SCORECARD.md) | Phase 1 Scorecard | 1 |
| [0014-PHASE-2-CONTRADICTION-REVIEW.md](./0014-PHASE-2-CONTRADICTION-REVIEW.md) | Phase 2 Contradiction Review | 2 |

## ADRs

| ADR | Title |
|---|---|
| [ADR-0001](./adrs/ADR-0001-event-boundaries.md) | Event boundaries vs in-Core ports |
| [ADR-0002](./adrs/ADR-0002-state-advanced-authority.md) | StateAdvanced sole transition authority |
| [ADR-0003](./adrs/ADR-0003-rejection-events.md) | Rejections are Events |
| [ADR-0004](./adrs/ADR-0004-write-affinity.md) | v1 Deployment write affinity |
| [ADR-0005](./adrs/ADR-0005-lifecycle-composition.md) | Lifecycle is composition, not an engine |
| [ADR-0006](./adrs/ADR-0006-asset-membership.md) | Singular Asset–Deployment membership |
| [ADR-0007](./adrs/ADR-0007-authorize-port.md) | Authorize as Core policy port |
| [ADR-0008](./adrs/ADR-0008-revision-pinning.md) | Evaluate-time revision pinning |
| [ADR-0009](./adrs/ADR-0009-projection-caches.md) | Projection caches non-authoritative |
| [ADR-0010](./adrs/ADR-0010-bootstrap-transitions.md) | Bootstrap transitions via machines |

## Status

Phases 0–2 proposed/accepted in-branch. Phase 3 (interface definitions) requires explicit authorization.
