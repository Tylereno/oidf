# ark-sdk — Plugin & Integrator Contracts (Phase 6 scaffold)

**Baseline:** `ARK-SPEC-BASELINE-2026.07.20`

## Purpose

Developer-facing surface for Plugins. Mirrors Core Event host rules without exposing State Engine internals (ADR-0001, ADR-0016).

## Layout

```
ark-sdk/
├── README.md
├── pyproject.toml
└── src/ark_sdk/
    ├── __init__.py
    ├── baseline.py
    ├── types/          # typed dict helpers aligned to IDL (optional aids)
    └── ports/
        ├── host_port.py          # PluginHostPort — publish/subscribe/config/health
        └── capability.py         # CapabilityDescriptor helpers
```

## Rules

- SDK does not depend on adapter implementations.
- Core MUST NOT depend on SDK packaging.
- Plugins request transitions only by publishing `TransitionRequested`.
