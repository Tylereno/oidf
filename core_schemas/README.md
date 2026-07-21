# core_schemas — machine-readable OIDF

Front-door schemas for field and runtime consumers. Deep IDL (JSON Schema Draft 2020-12) lives in [`idl/`](./idl/).

| File | Role |
|---|---|
| [`equipment_state.yaml`](./equipment_state.yaml) | Canonical equipment state machine (Procured → Energized class) |
| [`handoff_ledger.json`](./handoff_ledger.json) | Immutable digital as-built / handoff package |
| [`sat_event_log.json`](./sat_event_log.json) | Pass/fail SAT gate event schema |
| [`site_state.json`](./site_state.json) | Durable sovereign-node operational state (OT/DDIL profile) |
| [`site_event_log.json`](./site_event_log.json) | Append-only site decisions (AI assist never sole authority) |
| [`examples/`](./examples/) | Redacted front-door examples (including site state/log) |
| [`idl/`](./idl/) | Full normative JSON Schema set (CDO, events, state, sync, …) |
| [`evidence-catalog/`](./evidence-catalog/) | Typed evidence catalogs (BESS, solar inverter, …) |

**Baseline:** `KEEL-SPEC-BASELINE-2026.07.20`  
**Catalog compatibility:** [`../docs/normative/EVIDENCE-CATALOG-COMPATIBILITY.md`](../docs/normative/EVIDENCE-CATALOG-COMPATIBILITY.md)  
**Sovereign node profile:** [`../docs/normative/SOVEREIGN-NODE-PROFILE.md`](../docs/normative/SOVEREIGN-NODE-PROFILE.md) · [ADR-0019](../docs/normative/adrs/ADR-0019-ai-assistive-not-authoritative.md)  
**Keel consumption:** pin this commit or an annotated baseline tag via submodule or `OIDF_ROOT`, then record the `baseline_id`, `catalog_id`, and catalog `version` in the project/machine configuration.

## Schema `$id` namespaces (deferred unification)

Front-door artifacts in this directory use `https://oidf.dev/schemas/…` (`handoff_ledger`, `sat_event_log`, `site_state`, `site_event_log`, gate maps). Normative IDL under [`idl/`](./idl/) remains on `https://keel.dev/schemas/…` per [RFC 0015](../docs/normative/0015-INTERFACE-DEFINITIONS.md).

**Deferred:** collapsing to a single authority host is intentionally not done in P1.A. Renaming IDL `$id` values would break Keel and other consumers that pin `keel.dev` URIs. Track as a coordinated migration with Keel pin updates; do not rewrite `$id` ad hoc.
