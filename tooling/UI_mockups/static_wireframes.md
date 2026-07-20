# Static wireframes - evidence-submit tablet

These wireframes describe a tablet field tool for collecting and submitting OIDF Evidence. They are intentionally static. They do not define product behavior, runtime state transitions, or a click-to-advance flow.

## Screen A - Gate evidence inbox

Purpose: help the operator find the next Evidence item the machine definition expects.

Elements:

- Header with project, asset tag, current read-only state, and pinned baseline ID.
- Gate list grouped by SAT step.
- Each gate row shows required `evidence_type`, source class, and whether local artifacts are attached.
- Warning banner: "Submitting Evidence does not advance state. Keel advances only after validation and policy checks."
- Offline indicator showing last catalog sync commit/tag.

Operator actions:

- Scan asset tag.
- Select a gate to prepare Evidence.
- Open catalog definition for the Evidence type.
- Export read-only current ledger snapshot.

## Screen B - Evidence submission form

Purpose: capture one Evidence assertion with enough context for local validation and later AHJ review.

Elements:

- Read-only gate context: `gate_id`, expected `evidence_type`, source class, catalog ID, catalog version.
- Source details: instrument ID, adapter ID, or inspector principal depending on source class.
- Measurement / attachment area for telemetry, photos, signed forms, or historian extracts.
- Local validation checklist:
  - Catalog type exists under pinned version.
  - Source class matches catalog.
  - Asset ID matches current machine definition.
  - Required timestamps are present.
  - Attachment hashes are calculated.
- Submit Evidence button.

Operator actions:

- Attach artifact.
- Add measurement metadata.
- Run local validation.
- Submit Evidence.

Non-action:

- No "advance", "commission", "energize", "force pass", or wizard-next control.

## Screen C - Submission receipt

Purpose: give the field crew and AHJ a compact receipt without implying approval.

Elements:

- Evidence ID and content hash.
- Validation result: accepted locally, rejected locally, or queued for sync.
- Linked SAT gate if present.
- Read-only state after validation response.
- Export/share options for the receipt and current ledger fragment.
- Boundary note: "This receipt records Evidence handling. It is not AHJ approval or utility permission to operate."

## Static SVG

See [`evidence_submit_tablet.svg`](./evidence_submit_tablet.svg) for a single-page visual representation of these three screens.
