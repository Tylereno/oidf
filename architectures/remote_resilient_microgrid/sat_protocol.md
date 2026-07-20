# SAT protocol — remote resilient microgrid

1. **Diesel baseline** — load bank / governor checks as SAT events (may start human-observed; prefer instrumented).
2. **COTS inverter join** — communication + anti-island settings logged.
3. **Hybrid mode** — diesel + storage handoff; each transition evidence-gated.
4. **DDIL drill** — disconnect uplink; continue local ledger progress; sync on reconnect (Keel).
5. **Export** — handoff ledger for mission owner, not a screenshot dump.
