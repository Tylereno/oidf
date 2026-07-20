# BESS lighthouse — operator runbook

**Audience:** engineers running the Keel lab wedge  
**Normative spec:** [`../keel-specs/0021-LIGHTHOUSE-PILOT.md`](../keel-specs/0021-LIGHTHOUSE-PILOT.md)  
**Example code:** [`../keel-examples/bess-lighthouse/`](../keel-examples/bess-lighthouse/)

## Purpose

Demonstrate **machine Evidence** commissioning: cell voltage, insulation resistance, and thermal stability must be ingested and validated before the BESS asset may advance. No click-to-advance.

Evidence types (machine-sourced): `CellVoltageInBand`, `InsulationResistanceOk`, `ThermalStable` via telemetry → evidence plugins.

## Preconditions

1. Repo uses **Keel** paths (`keel-core`, not legacy `ark-core`).
2. Python 3.11+ with `keel-core[dev]` installed (see [`QUICKSTART.md`](./QUICKSTART.md)).
3. Writable output directory (example uses `/tmp/keel-bess-lighthouse`).

## Procedure

```bash
# from oidf repo root
python keel-examples/bess-lighthouse/run_e2e.py /tmp/keel-bess-lighthouse
```

Inspect the output directory for durable event/log artifacts produced by file adapters.

Automated coverage:

```bash
pytest keel-core/tests/test_lighthouse_bess.py -q
```

## Pass / fail

| Result | Meaning |
|---|---|
| Exit 0 + tests green | Happy-path Evidence satisfied; state advanced per machine |
| Rejection / failed gate | Missing or invalid Evidence — **expected** when inputs are wrong; do not bypass in demos |
| Import errors for `ark_*` | Stale checkout — pull `main` (Keel rename landed) |

## Operator cautions

- This is a **lab** path, not a field commissioning product claim.
- Do not point demos at real customer site identifiers or coordinates.
- Contracts change in `keel-specs` / evidence catalog first; runtime follows.
- Second lighthouse domains (non-BESS) are backlog — do not expand this runbook into a platform tour.

## Next engineering (suggested)

1. Durable adapter crash/recovery tests (`keel-core`)
2. Evidence catalog expansion beyond BESS (`keel-specs/evidence-catalog`)
3. Second lighthouse path under `keel-examples/` once catalog exists
