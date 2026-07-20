# SAT protocol — EV depot BTM

1. **Delivery / install** — mechanical install evidence before any commission gate. Gate IDs: `ev_fleet_btm.install_clearance_review`, `ev_fleet_btm.grounding_bonding_review`.
   - Ledger fields: the eventual `handoff_ledger.json` entry must carry `from_state`, `to_state`, `evidence_refs`, and the installation SAT `sat_event_ids`.
   - Evidence types: use BESS `InspectionPass` / `InsulationResistanceOk` where applicable; use pack-local `ClearanceLabelingRecorded` for EVSE clearances and labels.
2. **BESS pre-commission** — all three BESS catalog machine facts must exist before charger load support: `CellVoltageInBand`, `InsulationResistanceOk`, and `ThermalStable`. Gate ID: `ev_fleet_btm.bess_precommission`.
   - Ledger fields: each fact gets an immutable evidence ref, and the state transition remains `ReadyForCommission -> Commissioned` only when all related SAT events pass.
3. **Charger loop** — communication, interlock, and E-stop path verified; log as SAT events. Gate ID: `ev_fleet_btm.charger_loop_estop`.
   - Evidence types: use pack-local `ChargerCommunicationLoopOk` and `EmergencyStopTripVerified`, because these are EVSE controls rather than BESS catalog facts.
4. **Integrated run** — BESS supports charger load step; both assets’ ledger entries reference shared SAT event ids. Gate ID: `ev_fleet_btm.integrated_run_support`.
   - Evidence types: combine BESS `CellVoltageInBand` / `ThermalStable` with pack-local `ChargerLoadStepSupported`.
5. **Handoff export** — emit `handoff_ledger.json` for owner / AHJ packet with `sat_event_ids` pointing back to every required gate in `sat_gate_map.json`.

Fail any machine gate → state does **not** advance (Principle 4).
