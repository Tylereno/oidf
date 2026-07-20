# Safety gates — hyperscale island

**Not legal advice.**

- [ ] Phase-sync tolerances documented and met (machine Evidence)
- [ ] Island transition EOP reviewed; SAT pass recorded
- [ ] Fire / gas detection coordination for fuel cells documented
- [ ] UPS / ride-through expectations explicit in machine definition
- [ ] No Energized without Commissioned + clearance Evidence

## SAT `gate_id` mapping

Machine-readable source: [`sat_gate_map.json`](./sat_gate_map.json).

| Safety gate | SAT `gate_id` | SAT step | Evidence catalog / types | Ledger linkage |
|---|---|---:|---|---|
| Fuel-cell string start interlocks and fire or gas detection coordination recorded | `hyperscale_island.fuel_cell_string_ready` | 1 | `bess-commissioning`: `InspectionPass` | `ReadyForCommission -> Commissioned` |
| Phase-sync tolerances documented and met with machine Evidence | `hyperscale_island.bess_phase_sync` | 2 | `solar-inverter-commissioning`: `FrequencyInBand`, `GridVoltageInBand` | `ReadyForCommission -> Commissioned` |
| Controlled island transition drill passed under the approved EOP | `hyperscale_island.island_transfer_drill` | 3 | `bess-commissioning`, `solar-inverter-commissioning`: `InspectionPass`, `FrequencyInBand`, `GridVoltageInBand` | `ReadyForCommission -> Commissioned` |
| UPS and ride-through expectations are explicit in the machine definition | `hyperscale_island.ups_ridethrough_review` | 3 | `bess-commissioning`: `InspectionPass`, `ThermalStable` | `ReadyForCommission -> Commissioned` |
| Resync and return sequence completed with fail-closed behavior if Evidence is missing | `hyperscale_island.resync_return` | 4 | `solar-inverter-commissioning`: `FrequencyInBand`, `GridVoltageInBand`, `InspectionPass` | `ReadyForCommission -> Commissioned` |
