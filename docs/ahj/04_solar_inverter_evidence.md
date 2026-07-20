# 04 — Solar inverter / PCS evidence for AHJs

**Catalog:** [`../../core_schemas/evidence-catalog/solar-inverter-commissioning.json`](../../core_schemas/evidence-catalog/solar-inverter-commissioning.json)  
**Disclaimer:** Not legal advice. Utility interconnection rules and local electrical codes remain controlling.

---

## Why inverters need their own catalog

A second lighthouse domain exists so OIDF is not “the BESS format.” Solar / power-conversion system (PCS) commissioning stresses **grid-interface** facts: voltage, frequency, and anti-islanding behavior.

## Evidence types → inspector language

| OIDF `evidence_type` | Source | What to ask in the field |
|---|---|---|
| `GridVoltageInBand` | machine | Inverter / meter reports AC voltage inside the configured commission band. |
| `FrequencyInBand` | machine | Frequency inside band for the required samples. |
| `AntiIslandingOk` | machine | Anti-islanding or grid-tie protection self-test reports OK — not a checkbox that someone “verified islanding.” |
| `PhaseSyncInTolerance` | machine | PCS or synchronizer reports phase angle, voltage, and frequency deltas inside configured close/transfer tolerance. |
| `InspectionPass` | human | Optional dual-control; never alone on the happy path. |

## Utility and AHJ concerns this supports

- Demonstrable protection self-test before declaring ready to export  
- Traceable commission window for voltage/frequency  
- Machine-backed synchronization tolerance before close, transfer, or return  
- Clear separation between **human witness** and **machine measurement**  
- Ledger export suitable for interconnection closeout packets

## Suggested walkthrough

1. Confirm machine definition lists the inverter asset and required Evidence.  
2. On transition into `Commissioned`, verify machine Evidence types above appear in `evidence_refs`.  
3. Open linked SAT events — anti-islanding gate should be `pass` with timestamp.  
4. Keep utility-required forms; attach or reference the ledger so sequence is unambiguous.

## Stance

If anti-islanding is only attested by a signature on a form, you have theater. If it is machine Evidence in the catalog, you have a fact the commissioning runtime was not allowed to skip.
