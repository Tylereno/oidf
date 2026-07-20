# RFC 0015 — Interface Definitions (IDL)

**Status:** Accepted (Phase 3)  
**Phase:** 3  
**Depends on:** 0003–0014, ADR-0011  

## Purpose

Define strict, technology-agnostic interface schemas for Keel Core contracts. No business logic. No persistence/transport products.

## Goals

- Zero ambiguity on field types, nullability, requiredness.
- Cover Event envelope, CDO, State Engine messages, Plugin host messages, SyncBatch, Identity, Configuration, Authorize.
- Enable Phase 4 tests and Phase 5 reference validation.

## Non-Goals

- Code generation frameworks
- Wire transport mapping
- Complete domain Evidence payload catalogs
- Production storage layouts

## Requirements

1. Normative schemas SHALL use JSON Schema 2020-12 (ADR-0011).
2. Core envelopes SHALL set `"additionalProperties": false` unless an explicit `extensions` map is defined.
3. Required fields SHALL be listed in `required`.
4. Nullable fields SHALL use type unions including `"null"` only when null is meaningful; prefer omission + required rules.
5. Every Event payload type in the normative set SHALL have a schema.
6. Schema `$id` values SHALL be stable URIs under `https://keel.dev/schemas/`.

## Layout

```
keel-specs/idl/
├── common/
│   ├── identifier.json
│   ├── timestamp.json
│   └── revision_pin.json
├── event/
│   ├── envelope.json
│   └── payloads/*.json
├── cdo/
│   └── canonical_deployment_object.json
├── state/
│   ├── machine_definition.json
│   ├── transition_requested.json
│   ├── state_advanced.json
│   └── transition_rejected.json
├── plugin/
│   └── capability_descriptor.json
├── sync/
│   └── sync_batch.json
├── identity/
│   ├── principal.json
│   └── identity_assertion.json
├── config/
│   └── configuration_document.json
└── security/
    └── authorize_request.json
```

## Unknown Field Policy

- Default: reject unknown properties on Core envelopes.
- Extension map field `extensions` (object of string→JSON) MAY carry non-authoritative annotations; Core MUST ignore unknown extension keys for decision logic.

## Versioning

Each schema file documents `x-keel-schema-version`. Event `spec_version` references the event model version (`1.0.0` for this phase).

## Open Questions

None blocking. Protobuf dual-publish deferred.

## Related

Phase 4 test specs consume these schemas; Phase 5 reference validates them.
