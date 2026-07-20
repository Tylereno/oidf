# 02 — Reading a handoff ledger

**Schema:** [`../../core_schemas/handoff_ledger.json`](../../core_schemas/handoff_ledger.json)  
**Companion:** SAT log [`../../core_schemas/sat_event_log.json`](../../core_schemas/sat_event_log.json)

---

## What the file is

A handoff ledger is the **digital as-built for commissioning state**. It is JSON. You do not need to like JSON — you need to know which fields answer inspection questions.

### Top-level fields

| Field | Question it answers |
|---|---|
| `ledger_id` | Which export is this? |
| `spec_version` | Which OIDF ledger version? (currently `1.0.0`) |
| `subject.kind` / `subject.id` | Asset or Deployment — and which one |
| `created_at` | When was this export assembled? |
| `baseline_id` | Which specification baseline was pinned? |
| `machine_definition_id` | Which state machine governed transitions? |
| `entries[]` | The ordered history |

### Each entry

| Field | Question it answers |
|---|---|
| `seq` | Order (1, 2, 3…) — replay in this order |
| `occurred_at` | When did this transition happen? |
| `from_state` → `to_state` | What changed? |
| `actor_id` | Which principal requested/recorded it? |
| `evidence_refs` | Which Evidence IDs unlocked it? |
| `sat_event_ids` | Which SAT gate results are linked? |
| `notes` | Free text — never a substitute for Evidence |

## How to walk an inspection

1. Confirm `subject.id` matches the nameplate / tag you are standing in front of.  
2. Sort by `seq`. Find the latest `to_state`. That is the claimed current state.  
3. For any transition into `Commissioned` or `Energized`, demand non-empty `evidence_refs`.  
4. Cross-check `sat_event_ids` against the SAT event log: every cited gate should exist with `result: pass` (or an explicit waiver process your AHJ accepts — OIDF itself has fail/blocked).  
5. If the contractor claims Energized, confirm the canonical path required `EnergizationClearance`-class Evidence (see `equipment_state.yaml`).

## Red flags

- Latest state advanced with **empty** `evidence_refs`  
- Only human inspection Evidence on a path that catalogs mark as machine-required  
- SAT events missing, or cited IDs that do not appear in the SAT log  
- Ledger `subject.id` does not match the physical asset  
- “The cloud shows commissioned” but no export for the offline window

## Relationship to PDFs

Keep the stamped drawings and test reports. The ledger does not replace them. It **indexes the commissioning story** so you can find which test unlocked which state — instead of hunting a binder for an unspoken sequence.
