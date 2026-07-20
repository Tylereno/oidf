# RFC 0021 — Lighthouse Pilot: BESS Commissioning Wedge

**Status:** Accepted  
**Phase:** Field wedge (post–Phase 6)  
**Baseline:** `ARK-SPEC-BASELINE-2026.07.20`  

## Purpose

Define the **first paid/field path** for ARK: one vertical, one Evidence source class, one offline-capable Edge — not the universal deployment OS.

## Strategic Constraints (from product review)

- Specs are mature; **implementation debt is the risk**.
- Principle 4 only defeats human-input dependency when Evidence is **machine-sourced**.
- Next work is adapters + plugins + one end-to-end path — **not more Core RFCs**.
- Sell adjacent to Procore/Primavera: they hold docs/schedule; ARK holds **truth of state**.

## Wedge

| Dimension | Choice |
|---|---|
| Asset class | Battery Energy Storage System (BESS) / containerized storage skid |
| Site constraint | Intermittent or air-gapped Edge Node |
| Evidence source | Telemetry / MQTT-class measurements (machine), not form checkboxes |
| Human role | May install sensors and approve *policy*; must not click state forward |
| Success metric | `Installed → Commissioned` only after validated machine Evidence; 72h disconnect with local progress + clean sync |

## Non-goals (pilot)

- Full OT suite, digital twin UI, SAP/Primavera plugins
- Multi-vendor certification program
- Fleet SaaS control plane
- Replacing scheduling tools

## Minimum Lovable Deployment (MLD)

1. `FileEventStore` (or successor) durable log  
2. `StateEngineService` + Authorize + MachineDefinition for BESS  
3. Telemetry ingest → Evidence path (`ark-telemetry` + `ark-evidence`)  
4. Ed25519 Signed Events on high-assurance profile (optional for lab, required for regulated pilot)  
5. `SyncEngineService.export_batch` after reconnect  

## Pilot Evidence Types (default catalog)

See [`evidence-catalog/bess-commissioning.json`](./evidence-catalog/bess-commissioning.json).

Initial set:

| Type | Machine meaning | Typical source |
|---|---|---|
| `CellVoltageInBand` | Pack voltages within commission band | BMS / MQTT |
| `InsulationResistanceOk` | Insulation test threshold met | Test set / MQTT |
| `ThermalStable` | Temp within band for N samples | Sensors / MQTT |
| `ContactorClosedFeedback` | Close command confirmed by feedback | PLC / MQTT |
| `InspectionPass` | Optional dual-control human inspection (explicitly labeled human) | Tablet → still Evidence, never a state click |

**Rule:** At least one transition on the happy path MUST require a **non-human** Evidence type. A pilot that only uses `InspectionPass` is **evidence theater** and fails this RFC.

## Machine sketch (normative intent)

```
Planned → Installed
  evidence: ContactorClosedFeedback? (site-specific) OR empty bootstrap per ADR-0010

Installed → ReadyForCommission
  evidence: CellVoltageInBand, InsulationResistanceOk

ReadyForCommission → Commissioned
  evidence: ThermalStable
  optional dual-control: InspectionPass (human) AND ThermalStable (machine)
```

Exact MachineDefinition JSON lives in `ark-examples/bess-lighthouse/`.

## Lighthouse success criteria

| ID | Criterion |
|---|---|
| L1 | State does not advance on UI/API “complete” without EvidenceValidated |
| L2 | Telemetry threshold crossing produces Evidence without human form entry |
| L3 | Missing/stale Evidence → TransitionRejected; state unchanged |
| L4 | File-backed Event log survives process restart |
| L5 | Optional: 72h offline local advances; SyncBatch import does not diverge subject state |
| L6 | Case study write-up with Event IDs and machine pins |

## Falsification

Stop or reposition if:

- Pilot still requires daily human status entry to move state, or  
- Buyer demands click-to-advance overrides that gut Principle 4.

## GTM note

This RFC is the **Lighthouse** seed — not OEM SDK strategy and not Open Core licensing. Those follow after L1–L6 evidence exists.

## Related

- ADR-0012 Evidence trust · ADR-0016 Plugin isolation · ADR-0017 Ed25519  
- Plugins: `ark-telemetry`, `ark-evidence`  
- Example: `ark-examples/bess-lighthouse/`
