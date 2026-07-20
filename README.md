# ARK — Autonomous Resilient Kernel

**An open, evidence-driven platform specification for deterministic physical infrastructure deployment.**

ARK is not project-management SaaS. It is a **deployment OS / commissioning kernel**: assets advance only when attributable, validated **Evidence** satisfies deterministic state machines — including on air-gapped Edge Nodes.

> Progress only when the plant proves it.

## What it is (and is not)

| ARK is | ARK is not |
|---|---|
| Evidence-gated state orchestration | Procore / Primavera replacement |
| Offline-first Edge + optional cloud sync | A schedule optimizer |
| Specs + thin Core + Plugins | SCADA / ERP / CAD |
| Truth of **state** | Docs & Gantt UX |

Buyers: commissioning leads, OT/IT architects, utility/data-center buildout ops — not generic PMs.

## Current wedge (Lighthouse)

**BESS commissioning** with **machine telemetry Evidence** (RFC 0021) — not “platform for all critical infrastructure” yet.

```bash
pip install -e 'ark-core[dev]'
python ark-examples/bess-lighthouse/run_e2e.py /tmp/ark-bess-lighthouse
```

## Repository map

```
ark-specs/       # Source of truth (constitution, RFCs, ADRs, IDL)
ark-core/        # Microkernel + ports + file/Ed25519 adapters
ark-sdk/         # Plugin host contracts
ark-plugins/     # ark-evidence, ark-telemetry
ark-reference/   # Earlier conformance sketch
ark-examples/    # BESS lighthouse path
```

Baseline: `ARK-SPEC-BASELINE-2026.07.20` — see `ark-specs/SPECIFICATION-BASELINE.md`.

## Honest status

- Specs and Core ports/services: **strong**
- Durable JSONL log + Signed Events (Ed25519) + subprocess plugins: **working**
- First machine-Evidence path (telemetry → validate → commission): **working (lab)**
- Postgres/NATS/MQTT brokers, UI, fleet SaaS, OEM cert program: **not yet**

Principle 4 blocks click-to-advance. It only removes humans as the *Evidence factory* when Plugins ingest OT/IT facts — that is what the lighthouse wedge is for.
