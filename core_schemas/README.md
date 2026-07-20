# core_schemas — machine-readable OIDF

Front-door schemas for field and runtime consumers. Deep IDL (JSON Schema Draft 2020-12) lives in [`idl/`](./idl/).

| File | Role |
|---|---|
| [`equipment_state.yaml`](./equipment_state.yaml) | Canonical equipment state machine (Procured → Energized class) |
| [`handoff_ledger.json`](./handoff_ledger.json) | Immutable digital as-built / handoff package |
| [`sat_event_log.json`](./sat_event_log.json) | Pass/fail SAT gate event schema |
| [`idl/`](./idl/) | Full normative JSON Schema set (CDO, events, state, sync, …) |
| [`evidence-catalog/`](./evidence-catalog/) | Typed evidence catalogs (BESS, solar inverter, …) |

**Baseline:** `KEEL-SPEC-BASELINE-2026.07.20`  
**Keel consumption:** pin this commit via submodule or `OIDF_ROOT`.
