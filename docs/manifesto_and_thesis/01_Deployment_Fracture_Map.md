# 01 — Deployment Fracture Map

**Status:** Accepted doctrine  
**Audience:** EPCs, owners, OT/IT architects, commissioning leads

---

## Claim

Critical infrastructure deployment fails as a **coordination and proof** problem, not a Gantt problem.

Project controls tools already track dates, documents, and dollars. What they do not hold — and what commissioning actually requires — is **attributable proof that an asset may advance state**. Without that proof, “complete” is a social agreement, not an engineering fact.

## The cloud-tethered failure mode

Most modern construction and commissioning platforms assume:

- continuous connectivity to a vendor cloud,
- humans as the primary Evidence factory (forms, photos, signatures),
- the cloud record as the source of truth.

That model collapses on the sites that matter most: air-gapped substations, contested logistics corridors, expedition microgrids, data-center islands during black-start drills, and any plant under DDIL (denied, disrupted, intermittent, limited) connectivity.

When the uplink dies, cloud-tethered truth dies with it. Crews keep working. States advance in notebooks and chat. On reconnect, the system invents a reconciliation story. Regulators inherit the fiction.

OIDF rejects that architecture. **Edge-local progress is first-class. Sync is a transport problem, not a truth problem.**

## Four fractures

### 1. Evidence theater

Humans click “complete” without machine-attributable facts. Inspection forms become the gate. Principle 4 of the charter is absolute: *no click-to-advance*. A pilot that only uses human `InspectionPass` is evidence theater and fails RFC 0021.

OIDF labels Evidence with `source_class`: `machine` or `human`. The lighthouse catalogs require machine Evidence on the happy path (e.g. `CellVoltageInBand`, `ThermalStable`, `AntiIslandingOk`).

### 2. Offline amnesia

Edge sites progress while disconnected. Tools that cannot export a coherent local ledger force operators to choose between stopping work and forging the record later. OIDF assumes durable local events and a later sync batch. Inspectors ask for the **export covering the inspection window**, not a live dashboard.

### 3. Handoff opacity

As-built packages are PDF piles. Owners and AHJs cannot replay *Procured → … → Energized* with the Evidence that authorized each step. OIDF’s `handoff_ledger.json` is the immutable digital as-built: sequenced state transitions bound to `evidence_refs` and optional `sat_event_ids`.

### 4. Integration sprawl

SCADA, ERP, CAD, and PM tools each own a slice. None owns **deployment state** as a first-class, exchangeable object. OIDF does not replace those systems. It defines the contracts they must satisfy when they claim an asset advanced.

## What OIDF is for

| Artifact | Role |
|---|---|
| Machine definitions (`idl/state/`) | Deterministic allowed transitions + Evidence requirements |
| Evidence catalogs | Typed, versioned meanings for facts that unlock transitions |
| SAT event log | Pass / fail / blocked gates with timestamps and metrics |
| Handoff ledger | Replayable as-built for owners and AHJs |
| Architecture packs | Deliverable-centric SAT sequences and safety-gate checklists |

## What OIDF is not

- Not Procore, Primavera, or schedule optimization  
- Not SCADA, ERP, or CAD  
- Not VITO (sovereign edge node — separate product)  
- Not a claim that paperwork disappears — a claim that **proof becomes structured**

## Consequence

If your commissioning process cannot answer, offline, *what state is this asset in and which Evidence authorized the last transition*, you do not have a commissioning system. You have a document vault with aspirations. OIDF exists to close that gap.
