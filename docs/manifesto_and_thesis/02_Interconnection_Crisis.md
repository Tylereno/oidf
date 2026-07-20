# 02 — Interconnection Crisis

**Status:** Accepted doctrine (cite primary sources before external publication of specific statistics)  
**Audience:** Owners, developers, utility interconnection stakeholders, EPCs

---

## The problem

Utility interconnection and commissioning queues stretch across years for large projects. Industry analyses from LBNL / DOE and related queue studies have documented multi-year median wait times for significant segments of the interconnection pipeline. Specific headline figures (including widely circulated “~55-month” class summaries) **must be verified against the latest primary report** before use in external filings or marketing.

Whatever the exact median this year, the structural fact is stable: **capital sits idle while proof and process crawl**.

That delay is not only a transmission-planning bottleneck. A material share of late-stage friction is **handoff and acceptance**: owners, AHJs, and utilities cannot replay what was tested, when, against which machine definition, with which Evidence.

## Why a format matters here

Interconnection packages today are heterogeneous: studies, one-lines, test reports, emails, and stamped PDFs. They are necessary. They are not sufficient as a **state ledger**.

OIDF contributes three portable artifacts that sit beside (not instead of) utility process:

1. **Equipment state machine** — explicit path from `Procured` through `Energized` (`core_schemas/equipment_state.yaml`), specialized per architecture pack.  
2. **SAT event log** — each gate records `pass` / `fail` / `blocked` with time and optional metrics (`sat_event_log.json`).  
3. **Handoff ledger** — sequenced transitions with `evidence_refs` for the acceptance window (`handoff_ledger.json`).

These do not approve interconnection. They make the commissioning narrative **auditable**.

## Honest boundary

OIDF does not shorten study timelines, award queue positions, or certify NEC/IEEE compliance. Those authorities remain with utilities and AHJs. OIDF makes it harder to lose the proof trail that those authorities eventually demand.

## Stance

Every month of idle capital that traces to missing, contradictory, or unreplayable commissioning evidence is a format failure. Fix the format. Then enforce it with a runtime (Keel or equivalent). Do not confuse a prettier PDF packet with progress.
