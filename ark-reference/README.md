# ARK Reference (Phase 5)

Non-production in-memory microkernel demonstrating approved RFCs.

## Scope

- Event Engine (append-only, schema-validated envelopes)
- State Engine (evidence-gated transitions, idempotency, pins)
- Authorize policy port (deny by default)
- Sync merge + CDO hash quarantine

## Normative inputs

- `../ark-specs/` RFCs and `idl/` JSON Schemas
- Test specs: `../ark-specs/0016-TEST-SPECIFICATIONS.md`

## Run tests

```bash
pip install -e ark-reference jsonschema pytest
pytest ark-reference/tests -q
```

## Non-goals

Not a production Core. No durable storage, no network transport, no real Plugins.
