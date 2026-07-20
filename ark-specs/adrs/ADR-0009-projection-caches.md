# ADR-0009 — Projection Caches Are Non-Authoritative

**Status:** Accepted
**Date:** 2026-07-20  
**Related RFCs:** 0004, 0005, 0006, 0014  

## Context

Forbidding all storage of Current State would preclude practical read models; allowing mutable authoritative State would bypass Event sourcing.

## Decision

Derived projection caches (including Current State read models and Digital Twin views) are permitted. They MUST be rebuildable by Replay and MUST NOT be treated as source of truth.

## Alternatives

- Recompute always from full history (correct but potentially costly).
- Authoritative mutable State fields (violates Constitution).

## Tradeoffs

Implementations may cache aggressively; correctness tests must prove rebuild equivalence.

## Consequences

0004 clarified. Twin materialization may live outside Core (0003) while still being a projection.
