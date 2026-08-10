# UI mockups — field commissioning tablet

Wireframes for a tablet-friendly commissioning app that **submits Evidence** and displays state — never click-to-advance.

**Status:** Static wireframes only. No runtime UI, click-through prototype, or state-advance simulator belongs here.

Runtime UX experiments belong with product demos; normative behavior stays in OIDF schemas + Keel.

## Files

| File | Purpose |
|---|---|
| [`commissioning_explorer.html`](./commissioning_explorer.html) | Read-only design explorer for OIDF/Keel states, evidence vocabulary, and event types — for founder/product conversations, not runtime. |
| [`evidence_submit_tablet.svg`](./evidence_submit_tablet.svg) | Static tablet layout for selecting a gate, attaching Evidence, validating locally, and exporting a receipt. |
| [`static_wireframes.md`](./static_wireframes.md) | Human-readable notes for the same screens, including boundaries and non-goals. |

## Commissioning explorer (local preview)

From this directory:

```bash
python3 -m http.server 8765
```

Open [http://localhost:8765/commissioning_explorer.html](http://localhost:8765/commissioning_explorer.html).

**Purpose:** Help non-developers understand what words like `CellVoltageInBand`, `SatSuitePass`, and `StateAdvanced` mean, and how pack machines relate to the canonical equipment lifecycle — without reading raw JSON/YAML.

**Normative authority:** OIDF schemas (`core_schemas/`, evidence catalogs, IDL) remain the source of truth for vocabulary and contracts. **Keel** remains the runtime authority for state advancement, evidence validation, and event append. This HTML mockup does not implement, simulate, or replace either layer; it cannot advance an asset or emit an event.

**Audience:** Founder, product buyer, and UI/UX decisions — not a field debugger or certification claim.

## Guardrails

- The operator may submit Evidence, attach files, scan an asset tag, and export a receipt.
- The operator may not tap a button that directly advances the state machine.
- State shown in the UI is read-only output from validated OIDF/Keel state, not a local wizard state.
- Mockups must use synthetic asset IDs, no real site imagery, no customer data, and no PII.
