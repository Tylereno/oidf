# RFC 0019 — Phase 6 Application Services

**Status:** Accepted  
**Phase:** 6  
**Depends on:** 0018 (Approved), ADR-0012–0016, Baseline `KEEL-SPEC-BASELINE-2026.07.20`

## Purpose

Record that production Core application services now exist behind hexagonal ports without concrete infrastructure adapters.

## Delivered

| Service | Module | Enforces |
|---|---|---|
| EventService | `keel_core.app.event_service` | Append, sequences, plugin allowlists |
| StateEngineService | `keel_core.app.state_service` | EvidenceValidated-only, freshness, single-flight, pins, acyclic deps |
| SyncEngineService | `keel_core.app.sync_service` | Fencing epochs, revocation, CDO quarantine |
| AuthorizeService | `keel_core.app.authorize_service` | Deny-by-default |
| CoreKernel | `keel_core.app.kernel` | Composition root |

## Explicitly deferred

- Postgres/NATS/MQTT/cloud adapters
- Crypto algorithm ADR / Signed Events implementation
- Out-of-process Plugin Runtime host

## Conformance

`pytest keel-core/tests` + `keel-reference/tests` — green at acceptance.
