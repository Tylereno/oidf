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
| Fuel-cell string start interlocks and fire or gas detection coordination recorded | `hyperscale_island.fuel_cell_string_ready` | 1 | `hyperscale_island-local`: `FuelCellStartInterlocksOk`, `GasDetectionLoopOk` | `ReadyForCommission -> Commissioned` |
| Phase-sync tolerances documented and met with machine Evidence | `hyperscale_island.bess_phase_sync` | 2 | `solar-inverter-commissioning`: `PhaseSyncInTolerance`, `FrequencyInBand`, `GridVoltageInBand` | `ReadyForCommission -> Commissioned` |
| Controlled island transition drill passed under the approved EOP | `hyperscale_island.island_transfer_drill` | 3 | `solar-inverter-commissioning`: `FrequencyInBand`, `GridVoltageInBand`; `hyperscale_island-local`: `IslandTransferSequenceOk` | `ReadyForCommission -> Commissioned` |
| UPS and ride-through expectations are explicit in the machine definition | `hyperscale_island.ups_ridethrough_review` | 3 | `hyperscale_island-local`: `UpsRideThroughDurationMet` | `ReadyForCommission -> Commissioned` |
| Resync and return sequence completed with fail-closed behavior if Evidence is missing | `hyperscale_island.resync_return` | 4 | `solar-inverter-commissioning`: `PhaseSyncInTolerance`, `FrequencyInBand`, `GridVoltageInBand`; `hyperscale_island-local`: `ResyncReturnSequenceOk` | `ReadyForCommission -> Commissioned` |

## Pack-local Evidence types

These IDs stay local because they describe data-center islanding and fuel-cell integration checks that are not yet reusable BESS or solar/PCS catalog facts:

| `evidence_type` | Source | Meaning |
|---|---|---|
| `FuelCellStartInterlocksOk` | machine | Fuel-cell controller reports manufacturer start permissives and shutdown interlocks clear for the tested string. |
| `GasDetectionLoopOk` | machine | Gas/fire detection input path reports healthy and coordinated with the fuel-cell shutdown loop. |
| `IslandTransferSequenceOk` | machine | Controller or historian trace confirms the approved island-transfer sequence completed in order. |
| `UpsRideThroughDurationMet` | machine | UPS/runtime telemetry shows ride-through duration met or exceeded the machine-definition threshold during transfer. |
| `ResyncReturnSequenceOk` | machine | Return-to-grid sequence completed with close permissives satisfied and no missing Evidence override. |
