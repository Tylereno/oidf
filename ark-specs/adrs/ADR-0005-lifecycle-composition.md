# ADR-0005 — Lifecycle Is Composition, Not an Engine

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0000, 0001, 0003, 0014  

## Context

Constitution Core engines omit Lifecycle; topology/reference architecture listed Lifecycle alongside engines.

## Decision

Lifecycle is Core composition policy (ordered start/stop, health supervision). It is not a constitutional domain engine and adds no enterprise/integration knowledge.

## Alternatives

- Add Lifecycle Engine to Constitution (unnecessary Core growth).
- Remove all Lifecycle mentions (under-specifies runtime composition).

## Tradeoffs

Requires careful wording so Lifecycle is not mistaken for a feature sink.

## Consequences

0001/0003 wording clarified. Prime Directive still applies to composition policy growth.
