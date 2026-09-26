# RFC 0022 — Product Naming: OIDF (format) + Keel (runtime)

**Status:** Accepted  
**Date:** 2026-07-20  
**Related:** Constitution (branding); [`../NAMING.md`](../NAMING.md)

## Context

This repository was branded “ARK (Autonomous Resilient Kernel).” That name:

1. Collided with an older edge project that was renamed to **VITO** (to avoid biblical implications).
2. Blurred the distinction between **durable contracts** and **replaceable runtime** (the specification is durable; implementations are replaceable).
3. Confused multi-repo agents that also mount `ark-node` (VITO).

## Decision

1. **OIDF** is the name of the **format and specification surface** (IDL, CDO, events, machines, evidence catalogs).
2. **Keel** is the name of the **runtime product** that implements and enforces OIDF (Core, Edge Node software in this repo, plugins hosted here).
3. **VITO** remains a **separate** product in `ark-node` and is not an alias for Keel or OIDF.
4. **ARK** is deprecated. Do not use it in new prose.
5. Repository GitHub name stays `oidf`.
6. In-repo directory and package prefixes are **`keel-*` / `keel_*`** (migrated from `ark-*` / `ark_*`). Baseline id string is `KEEL-SPEC-BASELINE-…`. Schema `$id` host is `https://tylereno.me/oidf/schemas/…`. Extension field is `x-keel-schema-version`.

## Consequences

- README and agent onboarding lead with OIDF + Keel.
- Capability statements may say “OIDF-compliant commissioning history” and “Keel runtime.”
- Cross-repo work: VITO UI/API → `ark-node`; commissioning kernel → this repo.
- Imports use `keel_core`, `keel_sdk`, etc.

## Non-goals

- Renaming the GitHub repo `oidf` or the external repo `ark-node`.
- Merging VITO and Keel into one product.
