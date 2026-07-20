# ADR-0004 — v1 Deployment Write Affinity

**Status:** Accepted
**Date:** 2026-07-20  
**Related RFCs:** 0008, 0011, 0014  

## Context

Conflict merge examples implied multi-writer Edges while the working assumption was single-writer affinity.

## Decision

v1 assigns primary write affinity for each Deployment to one Edge Node. Non-primary nodes are read/forward unless a future RFC enables multi-writer mode. Conflict Resolution remains mandatory to recover from affinity breaches and partitioned ingest anomalies.

## Alternatives

- Multi-writer from day one (higher cognitive/operational load).
- No merge algorithm (unsafe under real partitions).

## Tradeoffs

Simpler v1 reasoning; merge complexity retained only for recovery correctness.

## Consequences

Configuration carries affinity assignments. 0008 examples distinguish normal sync vs recovery.
