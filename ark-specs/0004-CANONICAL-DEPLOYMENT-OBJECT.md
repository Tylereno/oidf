# RFC 0004 — Canonical Deployment Object (CDO)

**Status:** Proposed  
**Phase:** 1  
**Depends on:** 0000, 0002, 0003  

## Purpose

Define the technology-agnostic Canonical Deployment Object: the authoritative structured representation of a Deployment for orchestration.

## Goals

- One canonical aggregate for Deployment orchestration data.
- Implementation-independent conceptual model.
- Clear boundary between CDO content and Event history.
- Prepare for strict IDL in Phase 3 without choosing Protobuf vs JSON Schema now.

## Non-Goals

- Concrete schemas, field encodings, or database tables
- Complete Asset-class taxonomies
- CAD/GIS geometry authority
- Schedule optimization or ERP document models

## Requirements

1. Every Deployment SHALL have exactly one CDO identity (Working assumption from glossary: Deployment ID ≡ CDO ID).
2. The CDO SHALL declare the Deployment’s managed Asset set and structural relationships needed for orchestration.
3. The CDO SHALL reference or embed planned Future State intent at a granularity sufficient for Dependency evaluation—without treating plan as Current State.
4. Current State of Deployment and Assets SHALL NOT be stored as authoritative mutable fields that bypass Event history; Current State is derived from Events. Non-authoritative projection caches are permitted if rebuildable by Replay (ADR-0009).
5. The CDO SHALL be versioned (see 0010) so sync and replay interpret it correctly.
6. The CDO specification SHALL be expressible in a strict IDL later with zero ambiguity about types, nullability, and required fields.
7. Transition evaluation SHALL pin concrete CDO (and Configuration) revisions at evaluate time and record those pins on result Events (ADR-0008).

## Constraints

- CDO is not a replacement for CAD, GIS, ERP, or simulation models; it may reference external identifiers owned by those systems via Plugins.
- CDO must not embed vendor-specific resource shapes (no AWS/Azure/SAP-native documents as normative CDO structure).
- Evidence payloads are not the CDO; Evidence may reference CDO identities.

## Conceptual Model

```
CDO
├── identity (Deployment/CDO ID)
├── metadata (name, classification, labels — non-authoritative for State)
├── revision (CDO content revision; distinct from Event time)
├── assets[]
│   ├── asset identity
│   ├── asset class (opaque to Core beyond registry config)
│   ├── parent/child relations (optional hierarchy)
│   └── external references[] (system, foreign id) — via Plugin domains
├── plan
│   ├── intended topology / grouping
│   └── planned milestones as Future State intents (not current)
├── transition policy refs
│   └── machine definition refs / evidence requirements refs
└── integrity
    ├── content hash / signature hooks (see 0012)
    └── spec version
```

## What the CDO Owns vs What Events Own

| Concern | Authority |
|---|---|
| Which Assets are in scope | CDO (revisioned) |
| Structural relationships for orchestration | CDO |
| Planned Future State intents | CDO plan section |
| Current State | Event-derived projection |
| Evidence records | Event history (+ Evidence capability storage) |
| Transition decisions | State Engine outputs as Events |

## CDO Revision Rules

1. A CDO change that alters Asset membership, structure, or transition policy refs SHALL produce a new CDO revision.
2. CDO revision publication SHALL emit an Event (e.g. DeploymentRevised) so history remains complete.
3. State Engines SHALL evaluate transitions against a concrete CDO revision resolved at evaluate time. “Latest” means pin-at-evaluate-time; the pin MUST be recorded on the result Event (ADR-0008).
4. Historical replay SHALL use the CDO revision applicable at event time, negotiated via Versioning (0010).

## Interfaces (Abstract)

| Interface | Purpose |
|---|---|
| CdoGet(id, revision?) | Retrieve CDO content revision |
| CdoPut(id, content) | Propose new revision (authorized; emits Event) |
| CdoDiff(id, from, to) | Compare revisions for sync/audit |
| CdoPin(transition_ctx, revision) | Bind evaluation to a revision |

Storage adapters implement these behind Core-facing ports; Core must not know the engine.

## Examples

### Example — Microgrid Deployment

CDO lists Assets: generator, battery, switchgear, feeder. Plan marks Future State intents for commission order. External references point to GIS feature IDs and ERP equipment IDs. Current “commissioned” vs “installed” is not a CDO mutable flag; it appears only after Evidence-validated Transitions in Event history.

## Open Questions

1. Are large binary artifacts (drawings, photos) inside CDO or only referenced?  
   **Working assumption:** referenced only; binaries live in evidence/document capabilities.
2. Is Asset class taxonomy global-config or per-Deployment?  
   **Deferred** to Configuration + domain packs; CDO stores class identifiers, not taxonomy logic.

## Future Extensions

- Multi-Deployment programs (portfolio objects) without collapsing into one CDO
- Signed CDO revisions as Evidence of approved design baselines

## Related RFCs

0005 State Engine · 0006 Event Model · 0008 Synchronization · 0010 Versioning · 0012 Security
