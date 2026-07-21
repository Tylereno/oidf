# Architecture blueprints

Deliverable-centric packs. Each pack has overview, SAT protocol, safety gates, and a machine-readable SAT gate map.

| Pack | Intent |
|---|---|
| [`ev_fleet_btm/`](./ev_fleet_btm/) | EV depot behind-the-meter (BESS + chargers) |
| [`hyperscale_island/`](./hyperscale_island/) | Data center microgrid / island |
| [`remote_resilient_microgrid/`](./remote_resilient_microgrid/) | Defense / autonomous edge (legacy diesel + COTS) |

These are **lab blueprints**, not certified designs. Safety gates are checklists — not AHJ approvals.

Each pack includes a **redacted worked example** under `examples/`:

- `handoff_ledger.json`
- `sat_event_log.json`

Each pack also includes `sat_gate_map.json`, which declares the SAT `gate_id` namespace, expected Evidence types, required result for handoff examples, and ledger transition linkage.

Canonical equipment path: [`../core_schemas/equipment_state.yaml`](../core_schemas/equipment_state.yaml) (`equipment-lifecycle` catalog). Packs specialize `SatSuitePass` on `ReadyForCommission -> Commissioned` via their gate maps; CI fails if a pack is missing from `pack_sat_specialization` or lacks covering gates.

Validate:

```bash
pip install jsonschema
python tooling/validate_architecture_examples.py
```
