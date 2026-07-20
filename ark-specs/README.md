# ark-specs

**Ownership:** ARK Architecture maintainers  
**Role:** Source of truth  
**Baseline:** [`SPECIFICATION-BASELINE.md`](./SPECIFICATION-BASELINE.md) (`ARK-SPEC-BASELINE-2026.07.20`)

## Responsibility

RFCs, ADRs, standards, glossary, and interface specifications for ARK.

## Boundaries

- Contains no application code (IDL schemas are contracts, not runtime).
- Must not depend on any code repository.
- All other repositories consume approved artifacts from here.

## Index

| Document | Title | Phase |
|---|---|---|
| [0000-CONSTITUTION.md](./0000-CONSTITUTION.md) | Master Architectural Charter | — |
| [0001](./0001-REPOSITORY-TOPOLOGY.md)–[0012](./0012-SECURITY.md) | Architecture RFCs (Accepted Baseline) | 0–1 |
| [0002-UBIQUITOUS-LANGUAGE.md](./0002-UBIQUITOUS-LANGUAGE.md) | Ubiquitous Language Glossary | 0.5 |
| [0013](./0013-PHASE-1-SCORECARD.md)–[0014](./0014-PHASE-2-CONTRADICTION-REVIEW.md) | Phase reviews | 1–2 |
| [0015-INTERFACE-DEFINITIONS.md](./0015-INTERFACE-DEFINITIONS.md) | Interface Definitions (IDL) | 3 |
| [0016-TEST-SPECIFICATIONS.md](./0016-TEST-SPECIFICATIONS.md) | Test Specifications | 4 |
| [0017-PHASE-5-REFERENCE.md](./0017-PHASE-5-REFERENCE.md) | Phase 5 Reference Notes | 5 |
| [0018-PHASE-5-TO-6-TRANSITION.md](./0018-PHASE-5-TO-6-TRANSITION.md) | Phase 5→6 Transition Report | 5→6 |
| [0019-PHASE-6-APP-SERVICES.md](./0019-PHASE-6-APP-SERVICES.md) | Phase 6 Application Services | 6 |
| [SPECIFICATION-BASELINE.md](./SPECIFICATION-BASELINE.md) | Locked baseline declaration | 5→6 |
| [ARCHITECTURAL_FAILURE_MODES.md](./ARCHITECTURAL_FAILURE_MODES.md) | Red Team failure register | 5→6 |
| [idl/](./idl/) | JSON Schema contracts | 3 |

## ADRs

| ADR | Title |
|---|---|
| [0001](./adrs/ADR-0001-event-boundaries.md)–[0011](./adrs/ADR-0011-json-schema-idl.md) | Baseline decisions (Accepted) |
| [0012](./adrs/ADR-0012-evidence-trust-freshness.md) | Evidence trust chain & freshness |
| [0013](./adrs/ADR-0013-single-flight-acyclic-deps.md) | Subject single-flight & acyclic deps |
| [0014](./adrs/ADR-0014-sync-fencing-ordering.md) | Sync fencing & ordering authority |
| [0015](./adrs/ADR-0015-node-trust-rotation.md) | Node trust rotation & revocation |
| [0016](./adrs/ADR-0016-plugin-isolation-allowlists.md) | Plugin isolation floor & allowlists |
| [0017](./adrs/ADR-0017-signed-events-ed25519.md) | Signed Events cryptography (Ed25519) |

## Status

Specification Baseline locked in-branch. Phase 6 application logic awaits Transition Report approval ([0018](./0018-PHASE-5-TO-6-TRANSITION.md)).
