# ADR-0013 — Subject Single-Flight & Acyclic Dependencies

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0005, 0011; Failure Modes: Transition Race, Gate Deadlock  

## Context

Concurrent evaluators on one subject and circular `AssetStateIn` graphs create races and permanent stalls.

## Decision

1. State Engine MUST serialize transition evaluation per subject (single-flight / compare-and-append on subject stream).
2. MachineDefinition publication MUST reject dependency cycles among AssetStateIn/DeploymentStateIn edges.
3. Idempotency keys remain mandatory (0014 G2 / IDL).

## Alternatives

- Optimistic concurrency only (still need deterministic conflict Events).
- Allow cycles with timeout (nondeterministic ops burden).

## Tradeoffs

Lower parallelism per subject; higher correctness.

## Consequences

Core State port documents single-flight; Config validation includes cycle check; new TS cases.
