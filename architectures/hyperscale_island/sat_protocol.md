# SAT protocol — hyperscale island

1. **Fuel cell string ready** — manufacturer start interlocks logged as SAT events. Gate ID: `hyperscale_island.fuel_cell_string_ready`.
2. **BESS phase-sync** — sync metrics as machine Evidence (not operator eyeball). Gate ID: `hyperscale_island.bess_phase_sync`.
3. **Island transfer drill** — controlled island; ledger records from/to states. Gate IDs: `hyperscale_island.island_transfer_drill`, `hyperscale_island.ups_ridethrough_review`.
4. **Resync / return** — fail closed if Evidence missing. Gate ID: `hyperscale_island.resync_return`.
5. **Handoff** — export ledger covering black-start window.
