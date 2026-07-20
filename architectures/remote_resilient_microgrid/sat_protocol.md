# SAT protocol — remote resilient microgrid

1. **Diesel baseline** — load-bank, governor, and protective-relay checks become digital SAT events. Gate ID: `remote_resilient_microgrid.diesel_baseline`.
   - Analog proof: load-bank sheet, panel meter, tach/governor observation, relay trip witness.
   - Digital evidence: pack-local `DieselLoadBankBaselineRecorded`, `GovernorFrequencyResponseInBand`, and `ProtectiveRelayTripVerified` with immutable `evidence_refs`.
2. **COTS inverter join** — communication, anti-island settings, and transfer switch position logged. Gate ID: `remote_resilient_microgrid.cots_inverter_join`.
   - Analog proof: switch position/witnessed transfer and local meter readings.
   - Digital evidence: solar/PCS `AntiIslandingOk`, `GridVoltageInBand`, `FrequencyInBand`, plus pack-local `TransferSwitchPositionVerified`.
3. **Hybrid mode** — diesel + storage handoff; each transition evidence-gated. Gate ID: `remote_resilient_microgrid.hybrid_handoff`.
   - Analog proof: operator-observed source handoff and load acceptance.
   - Digital evidence: pack-local `HybridHandoffSequenceOk` plus BESS `CellVoltageInBand` and PCS `GridVoltageInBand`.
4. **DDIL drill** — disconnect uplink; continue local ledger progress; sync on reconnect (Keel). Gate ID: `remote_resilient_microgrid.ddil_drill`.
   - Analog proof: observed uplink disconnect/reconnect window.
   - Digital evidence: pack-local `LocalLedgerAppendProof` during disconnect and `ReconnectSyncProof` after reconnect.
5. **Export** — handoff ledger for mission owner, not a screenshot dump. Gate ID: `remote_resilient_microgrid.owner_handoff_export`.
   - Analog proof: paper/USB packet request.
   - Digital evidence: pack-local `OwnerHandoffManifestGenerated` referencing the ledger and SAT log artifacts.
