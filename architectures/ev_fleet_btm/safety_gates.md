# Safety gates — EV depot BTM

**Not legal advice. Not a substitute for AHJ review.**

Checklist themes inspectors typically care about (map to local NEC/NFPA editions):

- [ ] E-stop and interlock paths demonstrated and logged
- [ ] Battery enclosure / fire detection coordination documented
- [ ] Working clearances and labeling verified
- [ ] Grounding / bonding inspection recorded as Evidence or SAT fail
- [ ] Energization clearance only after Commissioned state

## SAT `gate_id` mapping

Machine-readable source: [`sat_gate_map.json`](./sat_gate_map.json).

| Safety gate | SAT `gate_id` | SAT step | Evidence catalog / types | Ledger linkage |
|---|---|---:|---|---|
| BESS pre-commissioning checks completed before charger load support | `ev_fleet_btm.bess_precommission` | 2 | `bess-commissioning`: `CellVoltageInBand`, `InsulationResistanceOk`, `ThermalStable` | `ReadyForCommission -> Commissioned` |
| E-stop, interlock, and charger communication loop demonstrated | `ev_fleet_btm.charger_loop_estop` | 3 | `ev_fleet_btm-local`: `ChargerCommunicationLoopOk`, `EmergencyStopTripVerified` | `ReadyForCommission -> Commissioned` |
| Working clearances, labels, and battery enclosure coordination recorded | `ev_fleet_btm.install_clearance_review` | 1 | `bess-commissioning`: `InspectionPass`; `ev_fleet_btm-local`: `ClearanceLabelingRecorded` | `ReadyForCommission -> Commissioned` |
| Grounding and bonding inspection outcome recorded | `ev_fleet_btm.grounding_bonding_review` | 1 | `bess-commissioning`: `InspectionPass`, `InsulationResistanceOk` | `ReadyForCommission -> Commissioned` |
| Integrated BESS and charger load step completed before handoff | `ev_fleet_btm.integrated_run_support` | 4 | `bess-commissioning`: `CellVoltageInBand`, `ThermalStable`; `ev_fleet_btm-local`: `ChargerLoadStepSupported` | `ReadyForCommission -> Commissioned` |

Record outcomes in `sat_event_log.json`; do not rely on chat or unmarked PDFs.

## Pack-local Evidence types

These IDs follow the catalog naming convention but stay local because they describe EVSE/depot integration details rather than reusable BESS commissioning facts:

| `evidence_type` | Source | Meaning |
|---|---|---|
| `ClearanceLabelingRecorded` | human | Field walkdown records working clearances, labels, and battery/charger enclosure coordination for the depot layout. |
| `ChargerCommunicationLoopOk` | machine | Charger controller telemetry or commissioning tool confirms the command/status loop is online for the tested EVSE group. |
| `EmergencyStopTripVerified` | machine | E-stop or interlock actuation is observed by the charger controller/safety relay path, not only signed off verbally. |
| `ChargerLoadStepSupported` | machine | Charger load-step request is served while BESS voltage and thermal evidence remain in band. |
