# Architecture: EV Depot Behind-The-Meter

**Status:** Lab blueprint  
**Assets:** BESS + EV chargers (BTM)

## Intent

Commission a depot microgrid slice where charger energization and BESS readiness share an OIDF ledger — not a spreadsheet of “done” checkboxes.

## Related contracts

- Evidence catalog: `core_schemas/evidence-catalog/bess-commissioning.json`
- Keel lighthouse: `Tylereno/keel` → `keel-examples/bess-lighthouse/`

## Pack contents

- [`sat_protocol.md`](./sat_protocol.md) — testing sequence
- [`safety_gates.md`](./safety_gates.md) — NEC/NFPA-oriented checklist (not legal advice)
