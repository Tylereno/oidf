# RFC 0016 — Test Specifications (Phase 4)

**Status:** Accepted (Phase 4)  
**Phase:** 4  
**Depends on:** 0005–0012, 0015, ADR-0001–0011  

## Purpose

Define normative behavioral test specifications for Keel Core. No production implementation required to satisfy this phase—reference implementations MUST pass these suites.

## Non-Goals

- Performance benchmarks
- Chaos/network simulation beyond sync merge cases
- UI tests
- Vendor Plugin conformance (separate future suite)

## Conventions

- **Given / When / Then**
- Event types and payloads MUST validate against `keel-specs/idl/`
- Suites are named `TS-####`

---

## TS-0001 — State Engine: Evidence Gate

**Given** Asset `A1` in `Installed` with machine transition `Installed→Commissioned` requiring Evidence type `InspectionPass`  
**And** principal `P1` is authorized for `transition.request`  
**And** no validated `InspectionPass` exists for `A1`  
**When** `TransitionRequested` is appended for that transition  
**Then** exactly one `TransitionRejected` is appended with `reason_code=MissingEvidence`  
**And** Current State of `A1` remains `Installed`

## TS-0002 — State Engine: Successful Advance

**Given** TS-0001 setup  
**And** `EvidenceSubmitted` + `EvidenceValidated` for `InspectionPass` on `A1`  
**When** `TransitionRequested` with new `idempotency_key`  
**Then** `StateAdvanced` is appended with `from_state=Installed`, `to_state=Commissioned`  
**And** payload `pins` include concrete `cdo_revision` and `config_revision`  
**And** Current State of `A1` is `Commissioned`

## TS-0003 — Idempotent Transition Request

**Given** TS-0002 succeeded with `idempotency_key=K1` producing Event `E_adv`  
**When** identical `TransitionRequested` with `idempotency_key=K1` is appended again  
**Then** no second `StateAdvanced` is created for a duplicate success path  
**And** the engine returns/references the original result associated with `K1`

## TS-0004 — Idempotency Conflict

**Given** prior request with `idempotency_key=K2` for transition T1  
**When** a new `TransitionRequested` uses `K2` but different `to_state`  
**Then** `TransitionRejected` with `reason_code=IdempotencyConflict`

## TS-0005 — Unauthorized Transition

**Given** principal `P_denied` has no `transition.request` grant  
**When** `TransitionRequested` by `P_denied`  
**Then** `TransitionRejected` with `reason_code=Unauthorized`  
**And** State unchanged

## TS-0006 — Dependency AssetStateIn

**Given** transition requires `AssetStateIn(BUS-1, Energized)`  
**And** `BUS-1` Current State is `Installed`  
**When** transition requested for dependent Asset  
**Then** `TransitionRejected` with `reason_code=DependencyUnsatisfied`

## TS-0007 — Invalid Transition Edge

**Given** Asset in `Planned`  
**When** request claims `from_state=Installed`  
**Then** `TransitionRejected` with `reason_code=InvalidTransition`

## TS-0008 — Replay Determinism

**Given** a sequence of Events leading to Current States S  
**When** Event log is replayed on a fresh engine with same machines/CDO/config pins  
**Then** derived Current States equal S  
**And** no additional Events are appended by pure Replay

## TS-0009 — Event Envelope Validation

**Given** an Event missing `actor_id`  
**When** Append is attempted  
**Then** Append is rejected (does not enter history)

## TS-0010 — Unknown Event Property Rejected

**Given** Event envelope with unknown top-level property `foo`  
**When** schema validation runs  
**Then** validation fails (`additionalProperties: false`)

## TS-0011 — Sync Merge Idempotent Event IDs

**Given** local history contains Event `E1`  
**When** SyncBatch imports the same `E1` id  
**Then** history remains single-copy for `E1`  
**And** Replay State unchanged

## TS-0012 — Sync Merge Deterministic Order

**Given** two concurrent EvidenceValidated Events on same subject with distinct ids  
**When** merged with ordering key `(subject, occurred_at, actor_id, event_id)`  
**Then** both nodes Replay to identical Current State

## TS-0013 — Affinity Breach Recovery

**Given** Deployment affinity primary = Edge-A  
**And** Edge-B incorrectly accepted Evidence for that Deployment’s Asset  
**When** batches merge  
**Then** Events are preserved (no silent drop)  
**And** Replay yields a single deterministic State

## TS-0014 — Plugin Failure Isolation

**Given** Plugin Runtime hosts Plugin X subscribed to `EvidenceSubmitted`  
**When** Plugin X crashes on dispatch  
**Then** Event history remains intact  
**And** State Engine still accepts unrelated transitions

## TS-0015 — Authorize Deny by Default

**Given** empty AuthorizationPolicy grants  
**When** any `transition.request` is authorized  
**Then** decision is `Deny`

## TS-0016 — Configuration Pin on Advance

**Given** Config revision 12 active at evaluate time  
**When** State advances  
**Then** `StateAdvanced.pins.config_revision == 12`  
**When** Config later moves to revision 40 and history is Replayed  
**Then** evaluation still uses recorded pin semantics for historical Events (State projection from Events does not re-open policy)

## TS-0017 — Bootstrap Deployment Create

**Given** Deployment machine with create transition declaring empty Evidence requirements  
**And** principal authorized  
**When** bootstrap `TransitionRequested` / create path runs  
**Then** `DeploymentCreated` (and/or `StateAdvanced` per machine) appears  
**And** no Evidence Events are required

## TS-0018 — CDO Content Hash Mismatch on Same Revision

**Given** SyncBatch claims CDO revision N with hash H1  
**And** local CDO revision N has hash H2≠H1  
**When** ImportBatch runs  
**Then** batch is quarantined (hard fault)

## TS-0019 — Projection Cache Rebuild

**Given** Current State projection cache is deleted  
**When** Replay runs  
**Then** cache rebuild matches prior Current States

## TS-0020 — External Sync Port Not Required for Offline Advance

**Given** Edge fully air-gapped  
**When** Evidence + TransitionRequested processed locally  
**Then** State advances without Cloud Control Plane contact

---

## Conformance

A reference or production Core claims Phase 4 conformance only if all TS-0001–TS-0020 pass.

## Phase 4 Scorecard

| Quality | Score |
|---|---|
| Testability | 9 |
| Documentation | 9 |
| Cognitive Load | 8 |
| Offline capability | 9 |
| Security | 8 |

## Related

Implemented by `keel-reference` Phase 5 suite.
