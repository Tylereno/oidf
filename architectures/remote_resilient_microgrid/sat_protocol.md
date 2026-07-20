# SAT protocol — remote resilient microgrid

1. **Diesel baseline** — load bank / governor checks as SAT events (may start human-observed; prefer instrumented). Gate ID: `remote_resilient_microgrid.diesel_baseline`.
2. **COTS inverter join** — communication + anti-island settings logged. Gate ID: `remote_resilient_microgrid.cots_inverter_join`.
3. **Hybrid mode** — diesel + storage handoff; each transition evidence-gated. Gate ID: `remote_resilient_microgrid.hybrid_handoff`.
4. **DDIL drill** — disconnect uplink; continue local ledger progress; sync on reconnect (Keel). Gate ID: `remote_resilient_microgrid.ddil_drill`.
5. **Export** — handoff ledger for mission owner, not a screenshot dump. Gate ID: `remote_resilient_microgrid.owner_handoff_export`.
