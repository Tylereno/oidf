# ADR-0003 — Transition Rejections Are Events

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0003, 0005, 0006, 0008, 0014  

## Context

0005 allowed rejection via Event or non-Event side channel. Sync, audit, and offline reproducibility require durable rejections.

## Decision

Consequential transition failures MUST append `TransitionRejected`. Side-channel logs MAY exist but are not authoritative.

## Alternatives

- Local-only rejection logs (fails sync/audit).
- Optional Events (non-uniform observability).

## Tradeoffs

More Events under abuse/retry load; mitigations via rate policy and idempotency (G2).

## Consequences

0005 algorithm emits `TransitionRejected` on failure. Preview/dry-run remains non-appending.
