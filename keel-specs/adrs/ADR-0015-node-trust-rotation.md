# ADR-0015 — Node Trust Rotation & Revocation

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0008, 0009, 0012; Failure Modes: Sync Key Compromise  

## Context

Stolen Edge node identity can inject poison SyncBatches into peers.

## Decision

1. Node identities use rotatable keys; revocation lists are Configuration artifacts synced/store-and-forwarded.
2. ImportBatch MUST verify batch integrity against non-revoked node keys; failure → quarantine.
3. Offline Edges cache last-known revocation list; if list expired per policy, import of *new* trust roots fails closed (local progression under existing trust continues).
4. Algorithm suite remains a future crypto ADR; this ADR locks the *control plane* for trust lifecycle.

## Alternatives

- Long-lived never-rotated node keys (rejected).
- Always-online CRL (rejected — air-gap).

## Tradeoffs

Operators must plan revocation distribution for sneakernet.

## Consequences

Identity/Sync ports expose revoke/verify hooks; no concrete crypto library in Core.
