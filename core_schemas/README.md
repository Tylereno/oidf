# core_schemas — machine-readable OIDF

Front-door schemas for field and runtime consumers. Deep IDL (JSON Schema Draft 2020-12) lives in [`idl/`](./idl/).

| File | Role |
|---|---|
| [`canonical/dictionary.yaml`](./canonical/dictionary.yaml) | OIDF Canonical Data Dictionary — 322 normalized elements across 6 domains for PM platform integration |
| [`canonical/README.md`](./canonical/README.md) | Dictionary documentation and tooling usage |
| [`equipment_state.yaml`](./equipment_state.yaml) | Canonical equipment state machine (Procured → Energized); types in `equipment-lifecycle` |
| [`handoff_ledger.json`](./handoff_ledger.json) | Immutable digital as-built / handoff package |
| [`sat_event_log.json`](./sat_event_log.json) | Pass/fail SAT gate event schema |
| [`site_state.json`](./site_state.json) | Durable sovereign-node operational state (OT/DDIL profile) |
| [`site_event_log.json`](./site_event_log.json) | Append-only site decisions (AI assist never sole authority) |
| [`examples/`](./examples/) | Redacted front-door examples (including site state/log) |
| [`idl/`](./idl/) | Full normative JSON Schema set (CDO, events, state, sync, …) |
| [`evidence-catalog/`](./evidence-catalog/) | Typed evidence catalogs (equipment-lifecycle, BESS, solar, pack-local, …) |

**Baseline:** `KEEL-SPEC-BASELINE-2026.07.20`
**Catalog compatibility:** [`../docs/normative/EVIDENCE-CATALOG-COMPATIBILITY.md`](../docs/normative/EVIDENCE-CATALOG-COMPATIBILITY.md)
**Sovereign node profile:** [`../docs/normative/SOVEREIGN-NODE-PROFILE.md`](../docs/normative/SOVEREIGN-NODE-PROFILE.md) · [ADR-0019](../docs/normative/adrs/ADR-0019-ai-assistive-not-authoritative.md)
**Schema `$id` namespaces:** [`../docs/normative/SCHEMA-ID-NAMESPACES.md`](../docs/normative/SCHEMA-ID-NAMESPACES.md)
**Keel consumption:** pin this commit or an annotated baseline tag via submodule or `OIDF_ROOT`, then record the `baseline_id`, `catalog_id`, and catalog `version` in the project/machine configuration.

## Schema `$id` namespace

Every schema in this directory uses one authority host —
`https://openlexicon.github.io/oidf/schemas/…` — served by GitHub Pages from this repository,
so each `$id` dereferences to the file that declares it.

| Artifact | On-disk path | `$id` suffix |
|---|---|---|
| Front-door contracts | `core_schemas/<name>.json` | `schemas/<name>.json` |
| Normative IDL | `core_schemas/idl/<sub>/<name>.json` | `schemas/<sub>/<name>.json` |

The `idl/` segment is not part of the ID namespace; Pages staging flattens it away to match.
CI enforces the mapping with [`../tooling/verify_pages_ids.py`](../tooling/verify_pages_ids.py).

**Policy and rationale:** [`../docs/normative/SCHEMA-ID-NAMESPACES.md`](../docs/normative/SCHEMA-ID-NAMESPACES.md)
(single authority host; published `$id` values are frozen identifiers).

