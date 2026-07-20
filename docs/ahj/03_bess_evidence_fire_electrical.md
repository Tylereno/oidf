# 03 — BESS evidence for fire and electrical AHJs

**Catalog:** [`../../core_schemas/evidence-catalog/bess-commissioning.json`](../../core_schemas/evidence-catalog/bess-commissioning.json)  
**Architecture pack (themes):** [`../../architectures/ev_fleet_btm/`](../../architectures/ev_fleet_btm/)  
**Disclaimer:** Not legal advice. Map themes to your adopted NEC / NFPA editions.

---

## Why storage projects need structured Evidence

Battery Energy Storage Systems concentrate electrical and thermal risk. Traditional packets prove that *someone signed that something was done*. OIDF’s BESS catalog requires **machine-class facts** before commissioning states advance — so “contactor closed” cannot mean “we sent the command.”

## Evidence types → inspector language

| OIDF `evidence_type` | Source | What to ask in the field |
|---|---|---|
| `CellVoltageInBand` | machine | Show BMS / telemetry that pack or cell voltages were inside the commission band when Evidence was emitted. |
| `InsulationResistanceOk` | machine | Show the insulation measurement (or instrument feed) meeting the project threshold — not a verbal “megger was fine.” |
| `ThermalStable` | machine | Show temperature remained in band for the required sample window before the transition. |
| `ContactorClosedFeedback` | machine | Show **feedback** that the contactor closed — command-only is insufficient. |
| `InspectionPass` | human | Optional dual-control. Useful. **Not sufficient alone** on the lighthouse happy path. |

## Mapping to familiar gate themes

OIDF architecture packs list safety-gate *themes* (checklists), not code citations that pretend to be universal:

- E-stop / interlock demonstration logged as SAT events  
- Enclosure / fire detection coordination documented  
- Working clearances and labeling verified  
- Grounding / bonding recorded as Evidence or SAT fail  
- Energization only after `Commissioned` + clearance Evidence  

Record outcomes in `sat_event_log.json`. Chat messages and unmarked photos are not SAT events.

## Suggested AHJ posture

1. Accept the ledger as a **navigational aid** into the contractor’s proof.  
2. Spot-check machine Evidence against instruments or historian extracts.  
3. Reject state claims that skip catalog requirements.  
4. Retain authority to fail the inspection regardless of ledger content — OIDF does not constrain your veto.

## Honest limit

OIDF cannot see a cell that the BMS never reported. Garbage telemetry in, garbage Evidence out. Your inspection still validates that the **sensing path** is trustworthy. The format forces the commissioning system to *ask* for the right class of fact before advancing state.
