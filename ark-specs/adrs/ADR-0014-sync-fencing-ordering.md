# ADR-0014 — Sync Fencing & Ordering Authority

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0006, 0008, 0010; Failure Modes: Split-Brain, Clock Drift  

## Context

Write-affinity alone does not fence stale primaries. `occurred_at` clock skew can invert merge order.

## Decision

1. Each Deployment affinity assignment carries an **epoch (fencing token)**; SyncBatches from a node MUST include epoch for subjects claimed.
2. `StateAdvanced` from a non-primary or stale epoch is **quarantined**, not merged into authoritative history, until governance accepts a rebinding Event.
3. Conflict ordering authority for concurrent Events is: subject stream sequence after deterministic assign, then `(occurred_at, actor_id, event_id)` only as tie-break among truly unordered facts — **never wall clock alone**.
4. Nodes MUST tolerate clock skew; security profiles MAY bound maximum accepted skew for `valid_until` checks.

## Alternatives

- Last-writer-wins (rejected — destroys audit).
- Require centralized sequencer always (rejected — breaks air-gap).

## Tradeoffs

More quarantine states; clearer operator recovery.

## Consequences

SyncBatch IDL gains optional `affinity_epochs`; Sync port enforces fencing; docs update 0008 examples.
