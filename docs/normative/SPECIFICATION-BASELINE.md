# Keel Specification Baseline

**Status:** Accepted  
**Baseline ID:** `KEEL-SPEC-BASELINE-2026.07.20`  
**Source of truth:** `docs/normative/` + `core_schemas/` on `Tylereno/oidf` `main`  
**Governing charter:** [0000-CONSTITUTION.md](./0000-CONSTITUTION.md)

## Purpose

Declare the immutable Phase 0–5 specification baseline for Keel prior to Phase 6 production Core implementation.

## Included Artifacts

| Artifact | Role |
|---|---|
| 0000 Constitution | Immutable charter |
| 0001 Topology | Repository boundaries |
| 0002 Glossary | Locked ubiquitous language |
| 0003–0012 Architecture RFCs | Accepted baseline |
| 0013–0014 Phase reviews | Historical governance |
| 0015 IDL | Normative JSON Schema contracts |
| 0016 Test specs TS-0001–0020 | Conformance requirements |
| 0017 Phase 5 reference notes | Non-production reference scope |
| ADR-0001–0011 | Accepted decisions |
| `idl/` | Machine-readable contracts |
| `core_schemas/evidence-catalog/` | Canonical Evidence-type catalogs |
| `EVIDENCE-CATALOG-COMPATIBILITY.md` | Catalog additive/deprecation/removal rules |

## Hexagonal / Ports & Adapters Compliance Audit

**Result: PASS (with residual Phase 6 risks documented in ARCHITECTURAL_FAILURE_MODES.md).**

| Check | Result |
|---|---|
| Core RFCs name no concrete DB/broker/cloud products as dependencies | PASS — named only as forbidden knowledge / non-goals |
| IDL schemas are technology-agnostic | PASS — JSON Schema only; no SQL/Kafka types |
| Event/State/Sync/Identity/Authorize expressed as ports | PASS — abstract interfaces in RFCs; production ports scaffolded in Phase 6 topology |
| Plugins own integrations | PASS — 0007 |
| Reference impl may use in-memory structures | PASS — explicitly non-production (0017); not part of Core contract |
| No adapter code in `keel-core` production tree at baseline lock | PASS — adapters deferred |

## ADR Lock Register

| ADR | Title | Status |
|---|---|---|
| 0001 | Event boundaries vs in-Core ports | Accepted |
| 0002 | StateAdvanced sole transition authority | Accepted |
| 0003 | Rejections are Events | Accepted |
| 0004 | v1 Deployment write affinity | Accepted |
| 0005 | Lifecycle is composition, not an engine | Accepted |
| 0006 | Singular Asset–Deployment membership | Accepted |
| 0007 | Authorize as Core policy port | Accepted |
| 0008 | Evaluate-time revision pinning | Accepted |
| 0009 | Projection caches non-authoritative | Accepted |
| 0010 | Bootstrap transitions via machines | Accepted |
| 0011 | Normative IDL: JSON Schema 2020-12 | Accepted |

Post-baseline ADRs (0012+) amend the baseline and require explicit acceptance before Core merge.

## Immutability Rule

After merge to `main`:

1. Behavioral changes to baseline RFCs/IDL require a new ADR + RFC amendment.
2. Phase 6 code MUST reference this Baseline ID in module headers / package metadata.
3. Conformance claim requires TS-0001–TS-0020 against the locked IDL.
4. Evidence catalog changes follow [EVIDENCE-CATALOG-COMPATIBILITY.md](./EVIDENCE-CATALOG-COMPATIBILITY.md); Keel pins the OIDF commit or annotated baseline tag plus catalog IDs and versions.

## Related

- [ARCHITECTURAL_FAILURE_MODES.md](./ARCHITECTURAL_FAILURE_MODES.md)
- [0018-PHASE-5-TO-6-TRANSITION.md](./0018-PHASE-5-TO-6-TRANSITION.md)
- [EVIDENCE-CATALOG-COMPATIBILITY.md](./EVIDENCE-CATALOG-COMPATIBILITY.md)
