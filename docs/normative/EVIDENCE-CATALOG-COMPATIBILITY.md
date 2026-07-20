# Evidence Catalog Compatibility

**Status:** Accepted baseline amendment  
**Baseline:** `KEEL-SPEC-BASELINE-2026.07.20`  
**Authority:** [ADR-0018 Evidence-Type Registry Authority](./adrs/ADR-0018-evidence-type-registry-authority.md)  
**Related:** [RFC 0010 Versioning](./0010-VERSIONING.md), [SPECIFICATION-BASELINE.md](./SPECIFICATION-BASELINE.md)

## Purpose

Evidence catalogs in `core_schemas/evidence-catalog/` are OIDF contract artifacts. They define the portable names and meanings of facts that unlock state transitions, SAT gates, ledgers, and AHJ review. A catalog change must preserve replay for older ledgers unless the change explicitly declares a breaking catalog version and migration guidance.

## Version model

Catalogs use `version` as a semantic compatibility version:

| Change class | Version impact | Rule |
|---|---|---|
| Patch | `x.y.Z` | Editorial description fixes that do not change the asserted fact, source class, or gate semantics. |
| Minor | `x.Y.z` | Additive Evidence types and non-breaking metadata. Existing ledgers and gate maps continue to replay. |
| Major | `X.y.z` | Removals, renames, source-class changes, semantic redefinitions, or stricter required interpretation. |

The `catalog_id` is stable across compatible minor and patch releases. A new `catalog_id` is reserved for a materially different domain, not for normal version evolution.

## Adding an Evidence type

A type MAY be added in a minor catalog version when all of the following are true:

1. The type name is globally unambiguous within the catalog and follows the existing PascalCase convention.
2. The proposal states the physical or documentary fact asserted, `source_class`, intended gates or transitions, and why existing types are insufficient.
3. Existing type meanings, source classes, and required happy-path gates are unchanged.
4. Architecture SAT gate maps, examples, AHJ docs, and validators are updated in the same PR when they cite or depend on the new type.
5. Keel and other runtimes can reject the unknown new type while still replaying ledgers pinned to older catalog versions.

Additive type releases are compatible for consumers that pin an older catalog because those consumers are not required to accept the new type. They are not a license to silently widen a previously locked machine definition.

## Deprecating an Evidence type

A type MAY be deprecated in a minor catalog version when a replacement or retirement reason is documented. Deprecation means:

1. The type remains in `types[]` with the same `evidence_type`, `source_class`, and asserted fact.
2. New architecture packs SHOULD stop using the type unless they document why no replacement applies.
3. Existing ledgers, SAT logs, and machine definitions that reference the type MUST continue to replay under their pinned catalog.
4. AHJ-facing docs SHOULD note the deprecation only when inspectors may see the type in exports.

Deprecation is a warning for future authoring. It is not removal and it does not invalidate historical Evidence.

## Removing or redefining an Evidence type

A type MUST NOT be removed, renamed, moved to a different `source_class`, or redefined within the same major catalog version. Those actions are breaking changes and require:

1. A new major catalog version.
2. An ADR or RFC amendment accepted by the OIDF format authority.
3. Migration and replay guidance for ledgers, SAT logs, architecture packs, AHJ docs, and Keel pins.
4. A clear statement of whether old ledgers remain valid only under the previous catalog or can be projected into the new catalog without rewriting audit Events.

Historical audit artifacts are never rewritten to use the replacement type. Replay selects the interpreter and catalog compatible with the recorded baseline and catalog version.

## Keel catalog pinning

Keel consumes OIDF catalogs; it does not define canonical Evidence types. For every project or release path, Keel SHOULD pin:

1. The OIDF git commit or annotated baseline tag.
2. The `baseline_id` recorded in handoff ledgers.
3. Each catalog `catalog_id` and `version` used by the machine definition and SAT gate map.

When online, Keel may cache newer OIDF catalogs for authoring or validation previews. During replay and state advancement, it MUST use the catalog version pinned by the machine definition / project configuration, fail closed on unknown required types, and preserve older interpreters for audit retention.

## Pack-local catalogs

Architecture packs MAY cite a pack-local catalog whose `catalog_id` ends in `-local`
(for example `ev_fleet_btm-local`). Pack-local catalogs:

1. Live under `core_schemas/evidence-catalog/` with filename stem equal to `catalog_id`.
2. Are first-class registry entries under ADR-0018 (not informal markdown-only names).
3. MUST resolve in CI: every `sat_gate_map.json` `evidence_catalogs` entry and each
   listed `evidence_types` name must exist in the cited catalog(s).

Prefer promoting reusable types into shared catalogs (BESS, solar/PCS, …) when the
fact is no longer pack-specific.

## PR checklist for catalog changes

- [ ] State whether the change is patch, minor, or major.
- [ ] Link ADR-0018 and this compatibility document.
- [ ] Update `core_schemas/evidence-catalog/` and any affected SAT gate maps, examples, AHJ docs, and validator expectations.
- [ ] If citing a `*-local` catalog, ensure the catalog file exists and CI resolve passes (`python3 tooling/validate_architecture_examples.py`).
- [ ] Explain Keel pinning impact: no runtime change, cache update only, or required Keel follow-up.
- [ ] Run `python3 tooling/validate_json_schemas.py core_schemas` and `python3 tooling/validate_architecture_examples.py`.
