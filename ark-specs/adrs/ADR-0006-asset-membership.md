# ADR-0006 — Singular Asset–Deployment Membership

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0002, 0004, 0014  

## Context

Glossary required one Deployment membership and simultaneously left multi-membership open.

## Decision

An Asset belongs to exactly one Deployment at any time. Transfer between Deployments is a modeled transition sequence, not shared mutable ownership.

## Alternatives

- Allow multi-Deployment membership (complicates State/Dependencies/sync affinity).
- Defer indefinitely (blocks CDO/State specs).

## Tradeoffs

Transfer workflows need explicit modeling; State machines stay tractable.

## Consequences

Glossary open question removed; CDO membership changes require revisioned CDO Events.
