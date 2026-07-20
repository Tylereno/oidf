# ark-core — Production Microkernel Topology (Phase 6)

**Baseline:** `ARK-SPEC-BASELINE-2026.07.20`  
**Status:** Scaffold only — ports & package topology. **No adapters. No application workflows.**

## Hexagonal Layout

```
ark-core/
├── README.md
├── pyproject.toml                 # packaging metadata only
└── src/ark_core/
    ├── __init__.py
    ├── baseline.py                # Baseline ID constant
    ├── domain/                    # pure domain types (no I/O)
    │   ├── __init__.py
    │   ├── identifiers.py
    │   └── errors.py
    ├── ports/                     # inbound/outbound port interfaces
    │   ├── __init__.py
    │   ├── event_port.py          # Event Bus / Event Engine port
    │   ├── state_port.py          # State Engine port
    │   ├── plugin_runtime_port.py
    │   ├── sync_port.py
    │   ├── identity_port.py
    │   ├── authorize_port.py
    │   ├── config_port.py
    │   └── clock_port.py          # abstract time (testability; no NTP vendor)
    ├── app/                       # application services (empty stub packages)
    │   └── __init__.py            # reserved — no logic until approval
    └── adapters/                  # FORBIDDEN for concrete infra in this phase
        └── __init__.py            # placeholder explaining ban
```

## Rules

1. `ports/` define Protocols matching `ark-specs/idl/` and RFCs.
2. `adapters/` MUST NOT contain Postgres/NATS/MQTT/etc. implementations until separately authorized.
3. Production Plugin Runtime MUST satisfy ADR-0016 isolation floor.
4. Conformance target: TS-0001–TS-0020.
