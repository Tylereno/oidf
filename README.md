# OIDF + Keel

**OIDF** is the format. **Keel** is the runtime.  
Repository: `Tylereno/oidf` · Naming lock: [`NAMING.md`](./NAMING.md)

Keel is an offline-first **commissioning / deployment kernel** for physical infrastructure. Assets advance only when attributable, validated **Evidence** satisfies deterministic state machines — including on air-gapped Edge Nodes. Progress is represented and exchanged as **OIDF** contracts (IDL, CDO, events, machines).

> Progress only when the plant proves it.

**Not** project-management SaaS. **Not** Procore/Primavera. **Not** VITO (VITO is the sovereign edge node in `ark-node`).

| Keel / OIDF is | Keel / OIDF is not |
|---|---|
| Evidence-gated state orchestration | Procore / Primavera replacement |
| Offline-first Edge + optional cloud sync | A schedule optimizer |
| Specs (OIDF) + thin Core (Keel) + Plugins | SCADA / ERP / CAD |
| Truth of **state** | Docs & Gantt UX |
| Sibling to VITO in the EnoTech stack | The VITO dashboard / crew runtime |

Buyers: commissioning leads, OT/IT architects, utility/data-center buildout ops — not generic PMs.

## Current wedge (Lighthouse)

**BESS commissioning** with **machine telemetry Evidence** (RFC 0021) — not “platform for all critical infrastructure” yet.

```bash
pip install -e 'keel-core[dev]'
python keel-examples/bess-lighthouse/run_e2e.py /tmp/keel-bess-lighthouse
```

## Repository map

```
NAMING.md         # Locked product names (read this first)
keel-specs/        # OIDF source of truth (RFCs, ADRs, IDL)
keel-core/         # Keel microkernel + ports + file/Ed25519 adapters
keel-sdk/          # Plugin host contracts
keel-plugins/      # keel_evidence, keel_telemetry
keel-reference/    # Earlier conformance sketch
keel-examples/     # BESS lighthouse path
```

Baseline id: `KEEL-SPEC-BASELINE-2026.07.20` — see `keel-specs/SPECIFICATION-BASELINE.md`.

## Honest status

- OIDF specs and Keel ports/services: **strong**
- Durable JSONL log + Signed Events (Ed25519) + subprocess plugins: **working**
- First machine-Evidence path (telemetry → validate → commission): **working (lab)**
- Postgres/NATS/MQTT brokers, UI, fleet SaaS, OEM cert program: **not yet**

Principle 4 blocks click-to-advance. It only removes humans as the *Evidence factory* when Plugins ingest OT/IT facts — that is what the lighthouse wedge is for.

## Specs

- Naming: [`NAMING.md`](./NAMING.md) · [`keel-specs/0022-PRODUCT-NAMING.md`](./keel-specs/0022-PRODUCT-NAMING.md)
- Charter: [`keel-specs/0000-CONSTITUTION.md`](./keel-specs/0000-CONSTITUTION.md)
- Specs index: [`keel-specs/README.md`](./keel-specs/README.md)
