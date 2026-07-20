# ADR-0007 — Authorize as Core Policy Port

**Status:** Accepted
**Date:** 2026-07-20  
**Related RFCs:** 0005, 0009, 0011, 0012, 0014  

## Context

Security requirements need `Authorize`, but adding a Security Engine would enlarge Core beyond the Constitution list.

## Decision

`Authorize(principal, action, resource)` is a Core policy port. Evaluation uses Identity assertions + versioned Configuration policy data. Enterprise directories sync inward via Plugins. RFC 0012 defines security requirements; it does not create a Core Security Engine.

## Alternatives

- Security Engine in Core (Prime Directive violation risk).
- Authorization only as Plugin (offline/transition path depends on Plugin availability).

## Tradeoffs

Policy data must be cached offline; evaluation logic stays small and data-driven.

## Consequences

State Engine/Event Engine call `Authorize` before consequential accepts. No vendor IAM types in Core.
