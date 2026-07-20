# SAT protocol — hyperscale island

1. **Fuel cell string ready** — manufacturer start permissives, shutdown interlocks, and gas/fire detection loops logged as SAT events. Gate ID: `hyperscale_island.fuel_cell_string_ready`.
   - Evidence types: pack-local `FuelCellStartInterlocksOk` and `GasDetectionLoopOk`.
2. **BESS / PCS phase-sync** — sync metrics as machine Evidence (not operator eyeball). Gate ID: `hyperscale_island.bess_phase_sync`.
   - Evidence types: solar/PCS `PhaseSyncInTolerance`, `FrequencyInBand`, and `GridVoltageInBand`.
3. **Island transfer drill** — controlled island; ledger records `from_state`, `to_state`, `evidence_refs`, and SAT `sat_event_ids`. Gate IDs: `hyperscale_island.island_transfer_drill`, `hyperscale_island.ups_ridethrough_review`.
   - Evidence types: pack-local `IslandTransferSequenceOk` and `UpsRideThroughDurationMet` plus PCS voltage/frequency evidence during the drill window.
4. **Resync / return** — fail closed if Evidence missing. Gate ID: `hyperscale_island.resync_return`.
   - Evidence types: solar/PCS `PhaseSyncInTolerance`, `GridVoltageInBand`, `FrequencyInBand`, and pack-local `ResyncReturnSequenceOk`.
5. **Handoff** — export ledger covering black-start window with every required SAT gate linked.
