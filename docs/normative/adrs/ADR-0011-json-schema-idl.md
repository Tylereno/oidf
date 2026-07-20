# ADR-0011 — Normative IDL: JSON Schema 2020-12

**Status:** Accepted
**Date:** 2026-07-20  
**Related RFCs:** 0000, 0004, 0006, 0010, 0015  

## Context

Constitution requires a strict IDL (Protobuf or JSON Schema) with zero ambiguity on types, nullability, and required fields. Phase 3 must define interfaces without business logic.

## Decision

Use **JSON Schema Draft 2020-12** as the normative IDL for Keel contracts in `keel-specs/idl/`.

## Alternatives

1. **Protocol Buffers** — excellent evolution tooling; requires codegen and `.proto` toolchain in every consumer.
2. **JSON Schema** — human-readable, validates without codegen, fits Zero Magic and offline edge nodes.
3. **Both** — Protobuf wire + JSON Schema docs (higher maintenance).

## Tradeoffs

- JSON Schema is easier to audit and validate in reference implementations without reflection magic.
- Protobuf may be added later as a wire encoding ADR without changing conceptual contracts, if needed.
- Unknown-field policy: additionalProperties false on Core envelopes unless a schema explicitly allows extension maps.

## Consequences

- All Phase 3 contracts live under `keel-specs/idl/`.
- Phase 5 reference validates against these schemas.
- A future ADR may introduce Protobuf bindings that map 1:1 to these schemas.
