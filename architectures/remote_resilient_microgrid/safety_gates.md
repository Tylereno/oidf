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
| Generator protective relays, overspeed paths, and load-bank baseline demonstrated | `remote_resilient_microgrid.diesel_baseline` | 1 | `remote_resilient_microgrid-local`: `DieselLoadBankBaselineRecorded`, `GovernorFrequencyResponseInBand`, `ProtectiveRelayTripVerified` | `ReadyForCommission -> Commissioned` |
| COTS inverter anti-island and transfer sequence verified | `remote_resilient_microgrid.cots_inverter_join` | 2 | `solar-inverter-commissioning`: `AntiIslandingOk`, `GridVoltageInBand`, `FrequencyInBand`; `remote_resilient_microgrid-local`: `TransferSwitchPositionVerified` | `ReadyForCommission -> Commissioned` |
| Diesel and storage handoff completed with evidence-gated transitions | `remote_resilient_microgrid.hybrid_handoff` | 3 | `bess-commissioning`: `CellVoltageInBand`; `solar-inverter-commissioning`: `GridVoltageInBand`; `remote_resilient_microgrid-local`: `HybridHandoffSequenceOk` | `ReadyForCommission -> Commissioned` |
| Offline ledger integrity checked after disconnect and reconnect | `remote_resilient_microgrid.ddil_drill` | 4 | `remote_resilient_microgrid-local`: `LocalLedgerAppendProof`, `ReconnectSyncProof` | `ReadyForCommission -> Commissioned` |
| Mission-owner handoff export generated from ledger and SAT log artifacts | `remote_resilient_microgrid.owner_handoff_export` | 5 | `remote_resilient_microgrid-local`: `OwnerHandoffManifestGenerated` | `ReadyForCommission -> Commissioned` |

## Analog -> digital gate conversion

| Analog field proof | Digital `evidence_type` | SAT `gate_id` |
|---|---|---|
| Load-bank sheet or meter photo redacted into a commissioning record | `DieselLoadBankBaselineRecorded` | `remote_resilient_microgrid.diesel_baseline` |
| Tach/governor observation or frequency trace | `GovernorFrequencyResponseInBand` | `remote_resilient_microgrid.diesel_baseline` |
| Relay/overspeed trip witness or controller record | `ProtectiveRelayTripVerified` | `remote_resilient_microgrid.diesel_baseline` |
| Transfer switch position witness during inverter join | `TransferSwitchPositionVerified` | `remote_resilient_microgrid.cots_inverter_join` |
| Operator-observed diesel/storage source handoff | `HybridHandoffSequenceOk` | `remote_resilient_microgrid.hybrid_handoff` |
| Uplink disconnected while local commissioning events continue | `LocalLedgerAppendProof` | `remote_resilient_microgrid.ddil_drill` |
| Reconnect confirms local ledger events sync without rewriting history | `ReconnectSyncProof` | `remote_resilient_microgrid.ddil_drill` |
| Owner packet request becomes a structured manifest | `OwnerHandoffManifestGenerated` | `remote_resilient_microgrid.owner_handoff_export` |

## Pack-local Evidence types

These IDs remain local because they describe legacy diesel, DDIL, and mission-owner handoff behavior that is not covered by the current BESS or solar/PCS catalogs:

| `evidence_type` | Source | Meaning |
|---|---|---|
| `DieselLoadBankBaselineRecorded` | human | Redacted load-bank baseline record is attached or referenced as an immutable Evidence item. |
| `GovernorFrequencyResponseInBand` | machine | Instrumented frequency/governor response remains inside the configured band during the load step. |
| `ProtectiveRelayTripVerified` | machine | Relay or overspeed trip path reports the expected trip/clear state during the test. |
| `TransferSwitchPositionVerified` | machine | Switch controller or commissioning input records the expected transfer position, not only a verbal witness. |
| `HybridHandoffSequenceOk` | machine | Controller or ledger trace confirms diesel/storage handoff completed in the approved order. |
| `LocalLedgerAppendProof` | machine | Local ledger accepts SAT events while disconnected from the uplink. |
| `ReconnectSyncProof` | machine | Reconnection sync preserves locally appended event IDs and ordering. |
| `OwnerHandoffManifestGenerated` | machine | Export manifest references the handoff ledger and SAT log artifacts for the mission owner. |
