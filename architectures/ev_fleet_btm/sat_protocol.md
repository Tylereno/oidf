# SAT protocol — EV depot BTM

1. **Delivery / install** — mechanical install evidence before any commission gate. Gate IDs: `ev_fleet_btm.install_clearance_review`, `ev_fleet_btm.grounding_bonding_review`.
2. **BESS pre-commission** — insulation, cell voltage band, thermal stable (machine Evidence). Gate ID: `ev_fleet_btm.bess_precommission`.
3. **Charger loop** — communication + E-stop path verified; log as SAT events. Gate ID: `ev_fleet_btm.charger_loop_estop`.
4. **Integrated run** — BESS supports charger load step; both assets’ ledger entries reference shared SAT event ids. Gate ID: `ev_fleet_btm.integrated_run_support`.
5. **Handoff export** — emit `handoff_ledger.json` for owner / AHJ packet.

Fail any machine gate → state does **not** advance (Principle 4).
