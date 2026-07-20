# SAT protocol — EV depot BTM

1. **Delivery / install** — mechanical install evidence before any commission gate.
2. **BESS pre-commission** — insulation, cell voltage band, thermal stable (machine Evidence).
3. **Charger loop** — communication + E-stop path verified; log as SAT events.
4. **Integrated run** — BESS supports charger load step; both assets’ ledger entries reference shared SAT event ids.
5. **Handoff export** — emit `handoff_ledger.json` for owner / AHJ packet.

Fail any machine gate → state does **not** advance (Principle 4).
