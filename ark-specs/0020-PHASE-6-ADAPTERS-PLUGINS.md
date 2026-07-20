# RFC 0020 — Durable Adapters, Signed Events, Plugin Runtime

**Status:** Accepted  
**Phase:** 6  
**Depends on:** 0019, ADR-0016, ADR-0017  

## Delivered

1. **FileEventStore** (`adapters/file_event_store.py`) — append-only JSONL durability behind `EventStorePort`.
2. **Ed25519SigningAdapter** + **ADR-0017** — Signed Events hash/sign/verify.
3. **SubprocessPluginRuntime** — out-of-process isolation floor (ADR-0016).
4. **ark-evidence** — first official Plugin validating `EvidenceSubmitted`.

## Non-goals (still deferred)

- Postgres/NATS/MQTT/cloud adapters
- Hardware-backed keys
- Full Evidence type registry UI/ops

## Tests

`pytest ark-core/tests` covers file persistence, signatures, and ark-evidence subprocess path.
