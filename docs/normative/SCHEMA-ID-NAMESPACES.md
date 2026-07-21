# Schema `$id` namespaces (alias map)

**Status:** Accepted documentation (unification deferred)  
**Baseline:** `KEEL-SPEC-BASELINE-2026.07.20`  
**Related:** [RFC 0015](./0015-INTERFACE-DEFINITIONS.md), [RFC 0022](./0022-PRODUCT-NAMING.md), [`core_schemas/README.md`](../../core_schemas/README.md)

## Two authority hosts today

| Host | Where used | Consumer expectation |
|---|---|---|
| `https://oidf.dev/schemas/…` | Front-door artifacts under `core_schemas/` (`handoff_ledger`, `sat_event_log`, `site_state`, `site_event_log`, `architecture_sat_gate_map`) | Field/AHJ-facing packages and architecture packs |
| `https://keel.dev/schemas/…` | Normative IDL under `core_schemas/idl/` | Keel runtime and other consumers that pin RFC 0015 URIs |

This split is intentional for P1.A. Front-door contracts are OIDF-branded; IDL `$id` values remain stable under `keel.dev` so existing Keel pins keep resolving.

## Alias table (non-breaking)

Aliases are **documentation and adapter hints only**. They do not change on-disk `$id` strings and MUST NOT be treated as a second registry (see ADR-0018 §6).

| Conceptual artifact | Canonical `$id` today | Documented alias / future host |
|---|---|---|
| Handoff ledger | `https://oidf.dev/schemas/handoff_ledger.json` | (already oidf.dev) |
| SAT event log | `https://oidf.dev/schemas/sat_event_log.json` | (already oidf.dev) |
| Site state / site event log | `https://oidf.dev/schemas/site_*.json` | (already oidf.dev) |
| Architecture SAT gate map | `https://oidf.dev/schemas/architecture_sat_gate_map.json` | (already oidf.dev) |
| Machine definition (IDL) | `https://keel.dev/schemas/state/machine_definition.json` | `https://oidf.dev/schemas/idl/state/machine_definition.json` (not published; do not rewrite until Keel migrates) |
| Other IDL envelopes | `https://keel.dev/schemas/…` | `https://oidf.dev/schemas/idl/…` path-preserving alias (deferred) |

Front-door YAML `equipment_state.yaml` is not itself a JSON Schema `$id`; its normative shape is the IDL `MachineDefinition` above, and its Evidence names resolve via `evidence-catalog/equipment-lifecycle.json`.

## Unification policy (deferred)

Collapsing to a single authority host requires a coordinated Keel pin update:

1. Publish oidf.dev mirrors or redirect rules for every `keel.dev` IDL `$id`.
2. Bump Keel / vendor pins to accept the new host (or dual-load both).
3. Only then rewrite in-repo IDL `$id` values in a baseline-tagged PR.

Until that migration lands, **do not** rename IDL `$id` ad hoc. Prefer this alias document and consumer-side dual registration if a tool must accept both hosts.
