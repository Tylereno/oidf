# 0014 — Phase 2 Contradiction Review

**Status:** Accepted (Phase 2)  
**Phase:** 2  
**Depends on:** 0000–0013  
**Role:** Architectural Governance  

## Purpose

Review every Keel specification for contradictions, hidden assumptions, and unresolved dual meanings. Record findings, lock resolutions via ADRs, and list residual risks for Phase 3+.

## Method

1. Cross-read Constitution, topology, glossary, and RFCs 0003–0013.
2. Classify each issue: **Contradiction**, **Ambiguity**, **Gap**, or **Non-issue**.
3. For Contradictions and binding Ambiguities: resolve with ADR + RFC patch.
4. Stop short of IDL (Phase 3) and implementation.

## Findings Summary

| ID | Class | Severity | Topic | Resolution |
|---|---|---|---|---|
| C1 | Contradiction | High | Events-only control vs synchronous `EvaluateTransition` | ADR-0001 + patches |
| C2 | Contradiction | High | `AssetCommissioned` listed as normative while also “projection only” | ADR-0002 + patch 0006 |
| C3 | Contradiction | Medium | Rejection “Event or side-channel” vs durability requirement | ADR-0003 + patch 0005 |
| C4 | Contradiction | Medium | Single-writer affinity vs dual-Edge advance example | ADR-0004 + patch 0008 |
| C5 | Contradiction | Medium | Lifecycle listed as Core contents vs Constitution engine list | ADR-0005 + patches |
| C6 | Contradiction | Low | Glossary Asset MUST single-Deployment + open question | ADR-0006 + patch 0002 |
| A1 | Ambiguity | High | Where `Authorize()` lives (Security engine vs Config+Identity) | ADR-0007 + patches |
| A2 | Ambiguity | Medium | CDO “latest” revision vs replay determinism | ADR-0008 + patches |
| A3 | Ambiguity | Medium | Projection caches vs “Current State not stored” | ADR-0009 + patch 0004 |
| A4 | Ambiguity | Low | Circular `Depends on` headers (0009↔0012) | Non-normative; document only |
| G1 | Gap | Medium | Bootstrap/`DeploymentCreated` vs Evidence-precedes-progression | ADR-0010 |
| G2 | Gap | Medium | Idempotency of transition requests under at-least-once | Deferred Phase 3/4 with rule sketch |
| G3 | Gap | Low | Evidence-type authority (glossary OQ) | Deferred; no conflict yet |
| N1 | Non-issue | — | Twin rich views outside Core vs twin concept | Compatible |
| N2 | Non-issue | — | Identity Interfaces vs “no auth providers in Core” | Compatible (ports vs products) |
| N3 | Non-issue | — | Signed Events “support” vs optional profile | Compatible |

## Detailed Findings

### C1 — Principle 2 vs Transition API

**Where:** Constitution Principle 2; 0003 “All cross-capability control SHALL occur through Events”; 0005 `EvaluateTransition` callable interface.

**Conflict:** External callers advancing State via a synchronous Core API looks like direct control, not Event communication.

**Resolution (ADR-0001):**  
- **Cross-capability** (Plugins, external systems, other capabilities): Events only.  
- **In-Core** engine ports may be synchronous.  
- External transition intent enters as `TransitionRequested`. State Engine consumes it and emits `StateAdvanced` or `TransitionRejected`.  
- `EvaluateTransition` remains an **internal** Core port (and may be used by a thin Core command adapter that only appends/consumes Events).

### C2 — Duplicate State authority in Event types

**Where:** 0006 normative table includes `AssetCommissioned`; Open Questions say `StateAdvanced` is sole normative authority.

**Resolution (ADR-0002):** Remove `AssetCommissioned` from the normative Core event set. Domain convenience names are projections only.

### C3 — Rejection observability channel

**Where:** 0005 algorithm step 7 allows “Event or structured rejection record”; Open Question prefers Events; 0003 requires observable rejection; sync needs durability.

**Resolution (ADR-0003):** `TransitionRejected` MUST be an Event. No side-channel-only rejections for consequential attempts.

### C4 — Affinity vs example

**Where:** 0008 Open Question assumes single-writer Deployment affinity; example “Two Edges accept different Evidence… for same Asset” implies concurrent writers.

**Resolution (ADR-0004):** v1 **normative** primary write affinity per Deployment to one Edge. Conflict merge remains mandatory for recovery (misconfiguration, partitioned Evidence ingest Plugins, or affinity breaches). Example retitled as recovery scenario.

### C5 — Lifecycle vs Constitution Core list

**Where:** Constitution Core list omits Lifecycle; 0001/0003 include Lifecycle.

**Resolution (ADR-0005):** Lifecycle is **Core composition policy** (startup/shutdown/health ordering), not a domain engine and not an expansion of constitutional engines. Wording aligned in 0001/0003.

### C6 — Asset membership MUST vs open question

**Where:** 0002 Asset MUST “Belong to exactly one Deployment” while Open Questions leave multi-membership open.

**Resolution (ADR-0006):** Lock singular membership at any time. Transfer is a modeled transition. Remove the conflicting open question.

### A1 — Authorization ownership

**Where:** 0009 vs 0012 both describe policy evaluation; Constitution has no Security Engine.

**Resolution (ADR-0007):** No Security Engine in Core. `Authorize` is a Core **policy port** evaluated from Configuration policy data + Identity assertions. 0012 remains the requirements RFC for controls; it does not add an engine.

### A2 — CDO “latest” vs determinism

**Where:** 0004 allows “pinned or explicitly latest per policy.”

**Resolution (ADR-0008):** “Latest” means pin-at-evaluate-time. The pinned CDO revision and Configuration revision MUST be recorded on the resulting Event for Replay.

### A3 — Storing Current State

**Where:** 0004 forbids mutable Current State fields bypassing history.

**Resolution (ADR-0009):** Derived projection caches are allowed. They are non-authoritative and MUST be rebuildable by Replay.

### G1 — Bootstrap vs Evidence principle

**Where:** Principle 4 vs `DeploymentCreated`.

**Resolution (ADR-0010):** Bootstrap transitions are defined by MachineDefinition. They MAY require Evidence like any transition. A minimal create transition MAY require only authorization if the machine explicitly declares empty Evidence requirements—still machine-data, not a UI click bypass.

### G2 — Idempotency

**Gap:** At-least-once dispatch + transition requests need idempotency keys.

**Phase 2 rule sketch (normative intent, IDL in Phase 3):** Transition requests carry `idempotency_key`. Duplicate keys with identical intent yield the original result Event; conflicting intent under same key is rejected.

## ADRs Produced

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

## Patches Applied This Phase

- 0002, 0001, 0003, 0004, 0005, 0006, 0008, 0009, 0012 (normative clarifications)
- README index update

## Residual Open Items (Not Contradictions)

1. Plugin packaging granularity (0001) — ADR later  
2. Crypto algorithm suite (0012) — ADR before implementation  
3. Evidence-type authority registry owner — Phase 3/Plugin RFC  
4. In-process vs out-of-process isolation mechanism — Level 4 ADR  
5. Transition idempotency IDL fields — Phase 3  

## Architectural Scorecard (Phase 2)

| Quality | Score | Notes |
|---|---|---|
| Modularity | 9 | Boundaries clarified (Events vs ports) |
| Coupling | 9 | C1 resolved without Core→Plugin coupling |
| Cohesion | 9 | Duplicate event authority removed |
| Replaceability | 9 | Unchanged |
| Testability | 9 | Mandatory rejection Events + pins improve replay tests |
| Offline capability | 9 | Affinity clarified; merge retained for recovery |
| Security | 8 | Authorize port clarified; crypto ADR still pending |
| Observability | 9 | Rejections uniformly in Event history |
| Extensibility | 9 | Unchanged |
| Documentation | 9 | Contradictions recorded with ADRs |
| Cognitive Load | 8 | More precise rules; slightly more concepts (TransitionRequested) |

No score below 8.

## Recommendation

Phase 2 resolutions are locked. Ready for Phase 3 (interface definitions / IDL) after acceptance.
