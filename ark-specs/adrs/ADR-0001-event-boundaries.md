# ADR-0001 — Event Boundaries vs In-Core Ports

**Status:** Accepted
**Date:** 2026-07-20  
**Related RFCs:** 0000, 0003, 0005, 0006, 0014  

## Context

Principle 2 requires Event communication and forbids services directly controlling one another. Phase 1 also defined synchronous `EvaluateTransition`. These conflict if external callers use the sync port as the control path.

## Decision

1. Cross-capability control MUST use Events only.
2. In-Core engines MAY expose synchronous ports to each other.
3. External transition intent MUST enter as `TransitionRequested`.
4. `EvaluateTransition` is an internal Core port only.

## Alternatives

- All-Events including in-Core (higher latency/complexity inside microkernel).
- External sync Transition API (violates Principle 2).

## Tradeoffs

Events-only externally preserves loose coupling; internal ports keep Core simple and testable.

## Consequences

- Event catalog gains `TransitionRequested`.
- SDKs/Plugins request transitions by publishing Events, not by linking Core internals.
