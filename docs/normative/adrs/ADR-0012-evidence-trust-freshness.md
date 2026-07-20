# ADR-0012 — Evidence Trust Chain & Freshness

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0005, 0006, 0012, 0015; Failure Modes: Forged Evidence, Stale Evidence  

## Context

Red Team showed unsigned/`EvidenceValidated` spoofing and indefinite reuse of old Evidence break Principle 4.

## Decision

1. State Engine MUST count only Evidence that has a corresponding `EvidenceValidated` Event from an authorized validator principal.
2. `EvidenceSubmitted` alone NEVER satisfies gates.
3. Evidence payloads MUST support optional `valid_from` / `valid_until`; when present, evaluation MUST reject outside the window.
4. High-assurance Deployments REQUIRE Signed Events for Evidence and Transitions (profile via Configuration).

## Alternatives

- Trust all EvidenceSubmitted (rejected — trivial forge).
- Always require wall-clock online OCSP (rejected — breaks air-gap).

## Tradeoffs

Slightly richer Evidence schema; offline TTL requires clock sanity (see ADR-0014).

## Consequences

IDL Evidence payloads amended; Phase 6 State port enforces validation chain; TS suite gains forged/stale cases.
