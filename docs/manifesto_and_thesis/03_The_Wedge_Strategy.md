# 03 — The Wedge Strategy

**Status:** Accepted doctrine  
**Related:** [`../normative/0021-LIGHTHOUSE-PILOT.md`](../normative/0021-LIGHTHOUSE-PILOT.md)

---

## Principle

Do not ship a “platform for all critical infrastructure” on day one. Ship a **narrow, machine-Evidence path** that proves Principle 4 in the field, then widen.

Site Acceptance Testing is the door. Owners, EPCs, and AHJs already expect gates. OIDF turns those gates into typed Evidence and ledger events instead of spreadsheet theater.

## First wedge

| Dimension | Choice |
|---|---|
| Asset | BESS / storage skid |
| Evidence | Machine telemetry (not form checkboxes alone) |
| Constraint | Intermittent or air-gapped edge |
| Success | `Installed → Commissioned` only after validated machine Evidence |
| Second path | Solar / PCS inverter (proves the format is not BESS-only) |

### BESS evidence catalog (normative types)

From `core_schemas/evidence-catalog/bess-commissioning.json`:

| Type | Source | Meaning |
|---|---|---|
| `CellVoltageInBand` | machine | Pack/cell voltage in commission band |
| `InsulationResistanceOk` | machine | Insulation threshold met |
| `ThermalStable` | machine | Temp in band for required samples |
| `ContactorClosedFeedback` | machine | Close confirmed by feedback, not command alone |
| `InspectionPass` | human | Optional dual-control; **never alone** on happy path |

### Solar inverter catalog

From `core_schemas/evidence-catalog/solar-inverter-commissioning.json`:

| Type | Source | Meaning |
|---|---|---|
| `GridVoltageInBand` | machine | AC voltage in band |
| `FrequencyInBand` | machine | Frequency in band |
| `AntiIslandingOk` | machine | Anti-islanding / grid-tie self-test OK |
| `InspectionPass` | human | Optional dual-control; never alone on happy path |

## Why this wedge

- **Sell adjacent to PM tools.** They hold schedule and docs. OIDF/Keel hold **truth of state**.  
- **Machine Evidence defeats theater.** Telemetry crossing a threshold produces Evidence without a form.  
- **Offline is the product constraint.** 72-hour disconnect with local progress and clean sync is a lighthouse criterion (RFC 0021).

## Non-goals (wedge)

Fleet SaaS, OEM certification programs, replacing Primavera, VITO dashboard work, universal OT suites.

## Adoption sequence

1. Pin OIDF baseline + machine definition for one asset class.  
2. Map SAT gates → `sat_event_log` + evidence catalog.  
3. Run a compliant runtime (Keel lighthouse paths exist for BESS and solar inverter).  
4. Export handoff ledger for owner / AHJ packet.  
5. Widen catalogs and architecture packs only after the first path is boringly reliable.

## Stance

A format that cannot win one vertical will not win the industry. The wedge is discipline, not lack of ambition.
