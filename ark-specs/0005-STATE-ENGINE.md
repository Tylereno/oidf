# RFC 0005 — State Engine

**Status:** Proposed  
**Phase:** 1  
**Depends on:** 0000, 0002, 0003, 0004  

## Purpose

Specify the deterministic State Engine: how Deployments and Assets transition under Evidence and Dependencies.

## Goals

- Deterministic finite state machines for Deployments and Assets.
- Evidence-gated, dependency-aware, auditable, replayable transitions.
- Explicit reject semantics for Invalid Transitions.
- Rollback only as modeled transitions—never history mutation.

## Non-Goals

- Universal state catalogs for all Asset classes
- UI for transition requests
- Persistence product choice
- Learning/adaptive transition policies

## Requirements

1. Every Asset SHALL exist in exactly one Current State per its machine.
2. Every Deployment SHALL have a machine governing Deployment-level lifecycle State.
3. A State Transition SHALL occur only when:
   - the transition is legal in the machine definition,
   - required Evidence is present and validated,
   - declared Dependencies hold,
   - the actor is authorized (0009/0012).
4. Successful transitions SHALL emit Events and append immutable history.
5. Failed attempts SHALL be rejected without changing Current State and SHALL be observable.
6. Replay of Event history SHALL reconstruct the same Current State (determinism).
7. Where rollback applies, it SHALL be an explicit legal transition (or compensated path), not Event deletion.

## Constraints

- State Engine MUST NOT call enterprise APIs; it consumes Evidence and Events only.
- State Engine MUST NOT own Plugin-specific validation logic beyond configured rule references.
- Machine definitions are data/configuration (0011), not hard-coded Core branches per vendor.

## Machine Model

```
MachineDefinition
├── subject kind: Deployment | Asset
├── states[] (named, discrete)
├── transitions[]
│   ├── from, to
│   ├── evidence requirements[]
│   ├── dependencies[]
│   └── authorization requirements
└── terminal states[]
```

### Dependency kinds (initial set)

| Kind | Meaning |
|---|---|
| EvidenceSufficient | Required Evidence types validated for subject |
| AssetStateIn | Named peer Asset(s) must be in allowed State set |
| DeploymentStateIn | Deployment must be in allowed State set |
| CdoRevisionPinned | Evaluation bound to specified CDO revision |

## Transition Algorithm (Normative Sketch)

Given subject S, requested transition T, context C:

1. Load MachineDefinition for S (via Configuration + CDO policy refs).
2. Derive Current State of S from Event history.
3. If T.from ≠ Current State → reject (`InvalidTransition`).
4. Verify authorization for actor in C via the Core `Authorize` policy port (ADR-0007).
5. Verify Dependencies in T against derived world state + Evidence store projections.
6. Verify Evidence requirements (presence + validation status).
7. If any check fails → reject; append `TransitionRejected` (ADR-0003). Preview/dry-run MUST NOT append.
8. If all pass → append `StateAdvanced`; record CDO + Configuration revision pins (ADR-0008); Current State becomes T.to by projection.
9. Return success with transition identity and Event identity.

External callers do not invoke this algorithm via a public sync RPC as the control plane. They publish `TransitionRequested` (ADR-0001). An in-Core adapter may call `EvaluateTransition` after appending/reading that Event.

Steps 1–8 MUST be free of wall-clock nondeterminism except for recording timestamps; decision logic MUST NOT depend on unreproducible entropy.

## Evidence Interaction

- EvidenceSubmitted does not advance State.
- EvidenceValidated (or equivalent validation outcome) updates sufficiency projections.
- State Engine reads sufficiency; Evidence validation may be performed by an Evidence capability/Plugin emitting validation Events.

## Rollback

- Permitted only if MachineDefinition includes an explicit reverse/compensate transition.
- Rollback transition has its own Evidence/Dependency requirements.
- Event history remains append-only.

## Interfaces (Abstract)

| Interface | Purpose |
|---|---|
| EvaluateTransition(subject, transition, actor, cdo_revision) | **Internal** Core port (ADR-0001) |
| GetCurrentState(subject) | Derived Current State (projection; ADR-0009) |
| GetMachine(subject) | Resolve MachineDefinition |
| PreviewTransition(subject, transition) | Dry-run validation without append |

## Examples

### Accept

Asset `SWGR-1` in `Installed`. Evidence `TorqueReport` and `InspectionPass` validated. Dependency `AssetStateIn(BUS-1, Energized)` holds. Transition `Installed → Commissioned` accepted; Event appended.

### Reject

Same Asset, missing `InspectionPass`. Engine rejects; Current State remains `Installed`.

## Open Questions

1. Hierarchical state machines (nested regions): required in v1 or deferred?  
   **Working assumption (unchanged):** flat machines in v1; hierarchy allowed later without changing Evidence-gated principles.

## Phase 2 Amendments

- ADR-0001, ADR-0003, ADR-0007, ADR-0008, ADR-0010.

## Future Extensions

- Parallel regions / Harel-style hierarchy
- Time-based guards only if made deterministic relative to event time, not live clock races

## Related RFCs

0004 CDO · 0006 Event Model · 0007 Plugin System · 0011 Configuration · 0012 Security
