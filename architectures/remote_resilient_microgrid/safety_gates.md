# Safety gates — remote resilient microgrid

**Not legal advice.**

- [ ] Generator protective relays / overspeed paths demonstrated
- [ ] Fuel handling and spill controls documented (ops, not OIDF)
- [ ] COTS inverter anti-island / transfer switch sequence verified
- [ ] Offline ledger integrity checked after reconnect
- [ ] No conflation with VITO crew UI — commissioning truth stays OIDF/Keel

## SAT `gate_id` mapping

Machine-readable source: [`sat_gate_map.json`](./sat_gate_map.json).

| Safety gate | SAT `gate_id` | SAT step | Evidence catalog / types | Ledger linkage |
|---|---|---:|---|---|
| Generator protective relays, overspeed paths, and load-bank baseline demonstrated | `remote_resilient_microgrid.diesel_baseline` | 1 | `bess-commissioning`: `InspectionPass` | `ReadyForCommission -> Commissioned` |
| COTS inverter anti-island and transfer sequence verified | `remote_resilient_microgrid.cots_inverter_join` | 2 | `solar-inverter-commissioning`: `AntiIslandingOk`, `GridVoltageInBand`, `FrequencyInBand` | `ReadyForCommission -> Commissioned` |
| Diesel and storage handoff completed with evidence-gated transitions | `remote_resilient_microgrid.hybrid_handoff` | 3 | `bess-commissioning`, `solar-inverter-commissioning`: `InspectionPass`, `CellVoltageInBand`, `GridVoltageInBand` | `ReadyForCommission -> Commissioned` |
| Offline ledger integrity checked after disconnect and reconnect | `remote_resilient_microgrid.ddil_drill` | 4 | `bess-commissioning`: `InspectionPass` | `ReadyForCommission -> Commissioned` |
| Mission-owner handoff export generated from ledger and SAT log artifacts | `remote_resilient_microgrid.owner_handoff_export` | 5 | `bess-commissioning`: `InspectionPass` | `ReadyForCommission -> Commissioned` |
