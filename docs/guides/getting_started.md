# Getting started — map a project to OIDF

For EPCs standing up a first OIDF-aligned commissioning path.

## Steps

1. **Read the why** — start with [`../manifesto_and_thesis/00_PREAMBLE.md`](../manifesto_and_thesis/00_PREAMBLE.md) and the [wedge](../manifesto_and_thesis/03_The_Wedge_Strategy.md).  
2. **Pick one asset class** — BESS or solar inverter (`core_schemas/evidence-catalog/`).  
3. **Pin a machine definition** — states and Evidence requirements must be explicit (`core_schemas/equipment_state.yaml` and `core_schemas/idl/state/`).  
4. **Log SAT gates** — each pass/fail/blocked becomes a `sat_event_log` record, not a chat message.  
5. **Export a handoff ledger** — lab helper `tooling/ledger_generator.py`, or a compliant runtime sync export after reconnect.  
6. **Validate** — `tooling/state_validator.py` checks claimed physical state against ledger entries.  
7. **Brief the AHJ** — use [`../ahj/01_inspector_briefing.md`](../ahj/01_inspector_briefing.md); bring the export, not a dashboard.

## Runtime

To *enforce* evidence-gated transitions, use a compliant runtime such as **Keel** (separate repository). This repo is format only.

## Do not

- Click-to-advance state without Evidence  
- Treat human `InspectionPass` as sufficient alone on lighthouse happy paths  
- Put mesh IPs, CAGE, or real site coordinates in git  
- Redefine IDL inside a runtime repo — contracts stay here
