# 01 — Deployment Fracture Map

**Status:** Working thesis (lab)  
**Audience:** EPCs, owners, OT/IT architects

## Claim

Critical infrastructure deployment fails as a **coordination and proof** problem, not a Gantt problem. Schedules and document vaults exist; **attributable proof that an asset may advance state** does not.

## Four fractures

1. **Evidence theater** — Humans click “complete” without machine-attributable facts.
2. **Offline amnesia** — Edge sites progress offline; cloud tools cannot be the source of truth during DDIL.
3. **Handoff opacity** — As-built packages are PDF piles; AHJs and owners cannot replay state.
4. **Integration sprawl** — SCADA, ERP, CAD, and PM tools each own a slice; none owns **deployment state**.

## What OIDF is for

OIDF defines the **contracts** for state machines, evidence types, handoff ledgers, and SAT event logs so any compliant runtime (starting with Keel) can advance assets only when proof exists.

## What OIDF is not

Not Procore. Not Primavera. Not VITO. Not a schedule optimizer.
