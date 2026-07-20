# UI mockups — field commissioning tablet

Wireframes for a tablet-friendly commissioning app that **submits Evidence** and displays state — never click-to-advance.

**Status:** Static wireframes only. No runtime UI, click-through prototype, or state-advance simulator belongs here.

Runtime UX experiments belong with product demos; normative behavior stays in OIDF schemas + Keel.

## Files

| File | Purpose |
|---|---|
| [`evidence_submit_tablet.svg`](./evidence_submit_tablet.svg) | Static tablet layout for selecting a gate, attaching Evidence, validating locally, and exporting a receipt. |
| [`static_wireframes.md`](./static_wireframes.md) | Human-readable notes for the same screens, including boundaries and non-goals. |

## Guardrails

- The operator may submit Evidence, attach files, scan an asset tag, and export a receipt.
- The operator may not tap a button that directly advances the state machine.
- State shown in the UI is read-only output from validated OIDF/Keel state, not a local wizard state.
- Mockups must use synthetic asset IDs, no real site imagery, no customer data, and no PII.
