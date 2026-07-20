# ark-core — Production Microkernel (Phase 6)

**Baseline:** `ARK-SPEC-BASELINE-2026.07.20`  
**Status:** Application services implemented behind ports. No concrete infra adapters.

## Layout

```
src/ark_core/
  baseline.py
  domain/
  ports/                 # Hexagonal ports
  app/                   # State/Event/Sync/Authorize/Kernel services
  adapters/memory.py     # test/dev doubles only (NOT Postgres/NATS/MQTT)
```

## Run tests

```bash
pip install -e ark-core[dev]
pytest ark-core/tests -q
```

## Rules

- Core contains zero knowledge of storage/transport/cloud products.
- Plugins never receive StateEngine internal ports.
- ADR-0012–0016 enforced in app services.
