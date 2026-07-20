# AHJ guides — OIDF for permitting and inspection

**Audience:** Authorities Having Jurisdiction (building, fire, electrical), utility acceptance engineers, owner reps  
**Disclaimer:** Not legal advice. Not a substitute for adopted codes (NEC, NFPA, local amendments) or utility tariffs. OIDF records proof; it does not grant permits.

## Purpose

Translate OIDF artifacts — evidence catalogs, state machines, SAT logs, and handoff ledgers — into language that traditional compliance bodies can use without needing to become cryptographers.

## Documents

| Guide | Use when |
|---|---|
| [01 Inspector briefing](./01_inspector_briefing.md) | First conversation with an AHJ or owner about OIDF |
| [02 Reading a handoff ledger](./02_reading_a_handoff_ledger.md) | Walking an exported ledger during inspection |
| [03 BESS evidence for fire & electrical](./03_bess_evidence_fire_electrical.md) | Storage / BESS commissioning acceptance |
| [04 Solar inverter evidence](./04_solar_inverter_evidence.md) | PCS / inverter grid-tie acceptance |
| [05 FAQ](./05_faq.md) | Short answers to common objections |

## Core idea in one sentence

**OIDF does not replace your code authority — it makes the commissioning narrative replayable so you can see what passed, what failed, and what Evidence unlocked each state change.**

## Maintainer note — catalog changes

When `core_schemas/evidence-catalog/` changes, keep this AHJ pack in sync before release:

- Follow [`../normative/EVIDENCE-CATALOG-COMPATIBILITY.md`](../normative/EVIDENCE-CATALOG-COMPATIBILITY.md) and ADR-0018 for add/deprecate/remove decisions.
- Update guide 03 or 04 when a BESS or solar/PCS Evidence type is added, deprecated, or reworded.
- If a new architecture pack introduces local Evidence types that inspectors may see, add a short inspector-language note or FAQ entry.
- Confirm the examples still show the same `baseline_id`, catalog ID, and catalog version that Keel pins for the project.
- Re-run the schema and architecture validators listed in `CONTRIBUTING.md`.
