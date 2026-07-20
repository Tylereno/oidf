# 02 — Interconnection Crisis

**Status:** Working thesis (lab)  
**Claim level:** Industry-context framing — cite primary sources before external publication.

## Problem

Utility interconnection and commissioning queues stretch measured in **years**, not weeks. Published LBNL / DOE interconnection analyses have documented multi-year median wait times for large projects (often summarized in industry briefings as ~multi-year / ~55-month class delays for some segments — **verify the exact figure against the latest LBNL queue report before citing externally**).

## Why OIDF cares

Every month of idle capital is partly a **proof and handoff** problem: owners, AHJs, and utilities lack a replayable ledger of what was tested, when, and against which machine definition.

## OIDF response

- Immutable **handoff ledger** (`core_schemas/handoff_ledger.json`)
- **SAT event log** schema for pass/fail gates
- Architecture blueprints with explicit safety gates (NEC/NFPA-oriented checklists — not legal advice)

Runtime enforcement is Keel’s job; this repo only defines the contracts.
