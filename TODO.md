# OIDF — engineering TODO

Focused engineering backlog for **format/contracts work only** in this repo. Runtime, product UI, and global platform live elsewhere.

**Last reviewed:** 2026-08-10 · **main:** `9e01d89` (`feat(oidf): canonical registry + translator with full dictionary`)

---

## Current state

| Area | Status |
|---|---|
| **Role** | OIDF is the **format** — schemas, ledgers, SAT gates, architecture blueprints, and field tooling. Keel is the **runtime** that implements it ([`Tylereno/keel`](https://github.com/Tylereno/keel)). |
| **Baseline** | `KEEL-SPEC-BASELINE-2026.07.20` — normative RFCs + IDL under `docs/normative/` and `core_schemas/idl/` |
| **Front-door schemas** | `handoff_ledger`, `sat_event_log`, `site_state`, `site_event_log`, `equipment_state.yaml` — `$id` under `https://oidf.dev/schemas/…` |
| **IDL** | Full JSON Schema 2020-12 set under `core_schemas/idl/` — `$id` remains `https://keel.dev/schemas/…` (alias map in [`docs/normative/SCHEMA-ID-NAMESPACES.md`](docs/normative/SCHEMA-ID-NAMESPACES.md); unification deferred until coordinated Keel pin migration) |
| **Evidence catalogs** | `equipment-lifecycle` + BESS, solar, and three architecture-pack-local catalogs under `core_schemas/evidence-catalog/`; additive/deprecation rules in [`docs/normative/EVIDENCE-CATALOG-COMPATIBILITY.md`](docs/normative/EVIDENCE-CATALOG-COMPATIBILITY.md) |
| **Architecture packs** | Three lab blueprints (`ev_fleet_btm`, `hyperscale_island`, `remote_resilient_microgrid`) with SAT gate maps, redacted examples, and CI validation via `tooling/validate_architecture_examples.py` |
| **ADR-0019** | Accepted — AI assistive, not authoritative; `site_state` / `site_event_log` are front-door contracts for sovereign-node OT/DDIL truth |
| **Canonical dictionary + translator** | `core_schemas/canonical/dictionary.yaml` (322 elements, 6 domains) + `tooling/oidf_registry.py` / `tooling/oidf_translator.py`; unit tests in `tooling/test_oidf_canonical.py` |
| **Keel pin relationship** | Keel consumes OIDF via submodule or `OIDF_ROOT`; pins `baseline_id`, `catalog_id`, and catalog `version` in machine/project config. OIDF does not ship runtime. Any IDL `$id` or catalog breaking change requires explicit Keel follow-up before merge. |
| **CI** | `json-schema.yml` validates IDL, front-door schemas, architecture examples, field tooling, and canonical/translator tests. `gitleaks.yml` secret scan — **failing on PRs** (permission gap; see Now). |

---

## Now

### 1. Review and merge commissioning explorer PR #32

- **Work:** Review [`PR #32`](https://github.com/Tylereno/oidf/pull/32) (`cursor/oidf-commissioning-explorer-1c3b`) — read-only HTML explorer under `tooling/UI_mockups/commissioning_explorer.html` for founder/product vocabulary conversations.
- **Checks:** No state advancement or event emission; vocabulary matches normative schemas/catalogs; guardrails in `tooling/UI_mockups/README.md` are accurate.
- **Done when:** PR merged to `main`; JSON Schema CI green on merge commit.
- **Evidence:** Merge commit on `main`; [`json-schema.yml`](.github/workflows/json-schema.yml) run success on that commit.

### 2. Fix gitleaks workflow permissions (if still failing)

- **Work:** [`gitleaks.yml`](.github/workflows/gitleaks.yml) currently sets `permissions: contents: read` only. `gitleaks-action@v2` calls `GET /repos/.../pulls/{n}/commits` on `pull_request` events and returns **403 Resource not accessible by integration** (observed on PR #32, run `31381827281`).
- **Fix:** Add `pull-requests: read` (or equivalent minimal scope) at workflow or job level; re-run on an open PR to confirm.
- **Done when:** Secret scan workflow completes successfully on a `pull_request` event without 403.
- **Evidence:** Green [`gitleaks.yml`](.github/workflows/gitleaks.yml) run on PR #32 or a follow-up test PR.

### 3. Keep commissioning explorer aligned to normative schemas

- **Work:** After merge, treat explorer copy as **derived documentation**. When evidence catalogs, `equipment_state.yaml`, or pack gate maps change, update explorer terminology in the same PR (or immediately after).
- **Done when:** Explorer state/evidence/event terms match `core_schemas/` and pack `sat_gate_map.json` files at pinned `main`; no orphan vocabulary.
- **Evidence:** Diff in schema/catalog PR includes explorer updates where terms changed; local smoke (`python3 -m http.server 8765` in `tooling/UI_mockups/`) shows updated labels.

---

## Next

### 4. Coordinate baseline changes with Keel before merge

- **Work:** Any change to IDL `$id` hosts, evidence catalog semantics (non-additive), machine-definition shapes, or baseline register entries must be paired with a Keel pin/update plan per [`core_schemas/README.md`](core_schemas/README.md) and [`EVIDENCE-CATALOG-COMPATIBILITY.md`](docs/normative/EVIDENCE-CATALOG-COMPATIBILITY.md).
- **Done when:** OIDF PR checklist marks Keel follow-up linked or explicitly not needed; Keel repo records new pin if required.
- **Evidence:** Linked Keel PR/issue or PR template checkbox with rationale; updated pin commit hash in Keel if applicable.

### 5. Decide whether canonical Jira/Asana/GitHub translator has a buyer

- **Work:** Dictionary + translator exist on `main` (`9e01d89`). Before expanding provider mappings, registry entries, or export surfaces, confirm an external or Keel-integrated consumer (buyer/use case). No scope expansion without that decision.
- **Done when:** Written decision (issue, ADR note, or Keel backlog item): **adopt** (name consumer + minimal MVP) or **hold** (maintain tests only, no new providers).
- **Evidence:** GitHub issue or linked Keel task with decision date and named stakeholder.

### 6. Maintain schema/catalog CI on every contract change

- **Work:** Keep `json-schema.yml` green for all touches to `core_schemas/`, `architectures/`, and `tooling/` validators. Run locally before push:
  ```bash
  pip install jsonschema pyyaml
  python tooling/validate_json_schemas.py core_schemas/idl
  python tooling/validate_front_door_schemas.py
  python tooling/validate_architecture_examples.py
  python -m unittest tooling.test_field_tooling tooling.test_oidf_canonical -v
  ```
- **Done when:** Every contract PR passes CI; no skipped validators.
- **Evidence:** Green JSON Schema CI run attached to PR; local command output matches CI job steps.

### 7. Publish/adoption work only with external users

- **Work:** Repo visibility, public docs polish, outreach, or “production-ready” claims wait until a named external adopter (EPC, AHJ pilot, Keel lighthouse operator) is committed. Internal/founder use does not trigger publish scope.
- **Done when:** Named adopter + minimal success criteria documented; publish checklist executed only for that engagement.
- **Evidence:** Signed-off adoption brief (issue or private doc link in PR); no premature public claims in README or docs.

---

## Explicitly deferred (do not pull into this repo)

| Item | Owner / rationale |
|---|---|
| **Runtime / state engine / event append** | Keel — OIDF defines contracts only |
| **Field UI runtime, click-through prototypes, state-advance simulators** | Keel or product demos — `tooling/UI_mockups/` stays static/read-only |
| **Global platform (SaaS, multi-tenant ops, arbitrary integrations)** | Out of scope — not OIDF’s charter |
| **Arbitrary new standards or greenfield RFCs** | Require constitution/baseline amendment; no drive-by specs |
| **Unrequested translator scope** (new PM providers, bidirectional sync, production ETL) | Blocked until task 5 buyer decision |
| **IDL `$id` host collapse (`keel.dev` → `oidf.dev`)** | Coordinated Keel migration — see [`SCHEMA-ID-NAMESPACES.md`](docs/normative/SCHEMA-ID-NAMESPACES.md) |
| **VITO / sovereign-node product implementation** | `ark-node` — OIDF supplies `site_state` / `site_event_log` shapes only |

---

## Quick reference

```bash
# Local validation (same as CI)
pip install jsonschema pyyaml
python tooling/validate_json_schemas.py core_schemas/idl
python tooling/validate_front_door_schemas.py
python tooling/validate_architecture_examples.py
python -m unittest tooling.test_field_tooling tooling.test_oidf_canonical -v

# Commissioning explorer preview (post–PR #32)
cd tooling/UI_mockups && python3 -m http.server 8765
```
