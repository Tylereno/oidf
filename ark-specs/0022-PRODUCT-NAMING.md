# RFC 0022 — Product Naming: OIDF (format) + Keel (runtime)

**Status:** Accepted  
**Date:** 2026-07-20  
**Related:** Constitution (branding only); [`../NAMING.md`](../NAMING.md)

## Context

This repository was branded “ARK (Autonomous Resilient Kernel).” That name:

1. Collides with an older edge project that was renamed to **VITO** (to avoid biblical implications).
2. Blurs the distinction between **durable contracts** and **replaceable runtime** (Constitution: the specification is the product; implementations are replaceable).
3. Confuses multi-repo agents that also mount `ark-node` (VITO).

## Decision

1. **OIDF** is the name of the **format and specification surface** (IDL, CDO, events, machines, evidence catalogs).
2. **Keel** is the name of the **runtime product** that implements and enforces OIDF (Core, Edge Node software in this repo, plugins hosted here).
3. **VITO** remains a **separate** product in `ark-node` and is not an alias for Keel or OIDF.
4. **ARK** is deprecated in new prose. Existing specs may still say ARK until a mechanical sweep; readers MUST treat ARK as a historical alias for Keel/OIDF per [`NAMING.md`](../NAMING.md).
5. Repository name stays `oidf`. Directory prefixes `ark-*` may remain until a dedicated path-migration RFC.

## Consequences

- README and agent onboarding lead with OIDF + Keel.
- Capability statements may say “OIDF-compliant commissioning history” and “Keel runtime.”
- Cross-repo work: VITO UI/API → `ark-node`; commissioning kernel → this repo.

## Non-goals

- Renaming Python packages or folder paths in this RFC.
- Merging VITO and Keel into one product.
