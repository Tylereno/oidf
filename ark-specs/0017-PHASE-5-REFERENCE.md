# RFC 0017 — Phase 5 Reference Implementation Notes

**Status:** Accepted (Phase 5)  
**Phase:** 5  
**Depends on:** 0015, 0016  

## Purpose

Record what the `ark-reference` package implements and what it deliberately omits.

## Implemented

| Area | Location | RFCs |
|---|---|---|
| Event append + id idempotency | `ark_reference/core/events.py` | 0006 |
| State transitions + pins + rejection Events | `ark_reference/core/state.py` | 0005, ADR-0001/3/8 |
| Authorize deny-by-default | `ark_reference/core/authorize.py` | 0012, ADR-0007 |
| Sync merge + CDO quarantine | `ark_reference/core/sync.py` | 0008 |
| JSON Schema validation | `ark_reference/schema.py` | 0015, ADR-0011 |
| Conformance tests | `ark-reference/tests/` | 0016 |

## Explicitly Not Implemented (Phase 6+)

- Durable persistence adapters
- Network transports
- Cryptographic Signed Events
- Out-of-process Plugin Runtime
- Full Digital Twin materialization
- Production identity providers

## Conformance

`pytest ark-reference/tests` exercises the Phase 4 suite subset automated in-repo.

## Scorecard (Phase 5)

| Quality | Score | Notes |
|---|---|---|
| Replaceability | 9 | In-memory only; ports obvious |
| Testability | 9 | Conformance tests green |
| Offline capability | 9 | No cloud dependency in advance path |
| Cognitive Load | 8 | Small surface |
| Documentation | 8 | README + this RFC |

Prime Directive: reference code stays thin; no enterprise integrations in Core.
