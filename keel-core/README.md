# keel-core — Production Microkernel (Phase 6)

**Baseline:** `KEEL-SPEC-BASELINE-2026.07.20`

## Layout

```
src/keel_core/
  ports/       # Hexagonal ports (incl. EventStorePort, SigningPort)
  app/         # Event/State/Sync/Authorize/PluginRuntime/Kernel
  adapters/
    memory.py           # test doubles
    file_event_store.py # append-only JSONL durability
    ed25519_signing.py  # ADR-0017 Signed Events
```

## Run tests

```bash
pip install -e 'keel-core[dev]'
pytest keel-core/tests -q
```

## Rules

- Core application code does not import cloud/broker SDKs.
- Production Plugin Runtime uses subprocess isolation (ADR-0016).
- High-assurance profiles may set `require_signatures=True` on CoreKernel.
