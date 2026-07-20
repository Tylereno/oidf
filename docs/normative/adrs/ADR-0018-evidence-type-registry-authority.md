# ADR-0018 — Evidence-Type Registry Authority

**Status:** Accepted
**Date:** 2026-07-20
**Related RFCs:** 0002, 0003, 0010, 0015; ADR-0011, ADR-0012  
**Compatibility rules:** [Evidence Catalog Compatibility](../EVIDENCE-CATALOG-COMPATIBILITY.md)

## Context

Evidence types are contract terms. If a runtime can invent or redefine them locally, a handoff ledger may replay differently across Keel versions, field tools, AHJ review, and future implementations. That would turn evidence-gated progression into product-specific behavior instead of an OIDF format guarantee.

The current registries are the evidence catalogs in `core_schemas/evidence-catalog/`. Keel and field tooling consume those catalogs to validate submissions, SAT gate maps, and ledgers.

## Decision

1. The **OIDF format authority** owns the canonical Evidence-type registry. Until a separate standards body exists, that authority is the OIDF Architecture maintainers under the governance in `CONTRIBUTING.md`.
2. Runtime implementations, including Keel, **consume** OIDF evidence catalogs. They may cache catalogs, pin versions, and reject unknown types, but they do not define canonical Evidence types outside OIDF.
3. New Evidence types are proposed as OIDF PRs that update `core_schemas/evidence-catalog/` and, when relevant, architecture SAT gate maps, examples, AHJ docs, and validators.
4. A proposal must state the type name, source class, physical or documentary fact asserted, intended gates/transitions, and why existing types are insufficient.
5. Compatibility follows RFC 0010 (`docs/normative/0010-VERSIONING.md`) and [Evidence Catalog Compatibility](../EVIDENCE-CATALOG-COMPATIBILITY.md): additive new types may be compatible within a catalog version policy; renames, removals, or semantic redefinitions are breaking changes and require a new version plus migration/replay guidance.
6. Runtime-specific aliases or UI labels may exist only as presentation or adapter mappings. They must not change ledger semantics or be treated as canonical registry entries.

## Alternatives

- **Runtime-owned registry** — Keel ships the authoritative list and OIDF documents it later. Rejected because replay and AHJ review would depend on one implementation.
- **Per-deployment free-form types** — fastest for pilots, but creates non-portable ledgers and weakens Evidence sufficiency checks.
- **External standards body now** — desirable later, but premature before the OIDF catalog stabilizes.

## Tradeoffs

OIDF PR review slows down additions, especially during pilots. In return, Evidence names remain portable, replayable, and inspectable across runtimes and over time.

## Consequences

- Keel treats OIDF evidence catalogs as input contracts, not as runtime-owned source of truth.
- Architecture packs that cite Evidence types must use cataloged names or propose catalog additions in the same PR.
- Unknown Evidence types are compatibility and validation questions, not runtime feature flags.
- Future catalog governance can move to a formal committee without changing the authority boundary: the format owns the registry; runtimes consume it.
