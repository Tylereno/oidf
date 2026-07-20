# ADR-0008 — Evaluate-Time Revision Pinning

**Status:** Accepted
**Date:** 2026-07-20  
**Related RFCs:** 0004, 0005, 0010, 0011, 0014  

## Context

Allowing evaluation against “latest” CDO/Config without recording the pin threatens Replay determinism.

## Decision

Any transition evaluation resolves concrete CDO and Configuration revisions at evaluate time and MUST record those pins on `StateAdvanced` / `TransitionRejected`. “Latest” is syntactic sugar for pin-at-evaluate-time, never an unbound moving reference in history.

## Alternatives

- Always require callers to pass explicit revisions (stricter UX).
- Allow unbound latest (breaks determinism).

## Tradeoffs

Events carry more metadata; Replay becomes reliable.

## Consequences

Phase 3 IDL must include pin fields on transition result Events.
