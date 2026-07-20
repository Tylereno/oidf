# ADR-0002 — StateAdvanced Is Sole Transition Authority

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0005, 0006, 0014  

## Context

0006 listed `AssetCommissioned` in the normative event set while stating `StateAdvanced` should be the sole authority.

## Decision

`StateAdvanced` is the only normative Event meaning a successful State Transition. Domain aliases (e.g. “commissioned”) are derived projections, not parallel authorities.

## Alternatives

- Dual-emit `StateAdvanced` + domain event (duplicate authority risk).
- Replace `StateAdvanced` with per-domain types (Core absorbs domain taxonomy).

## Tradeoffs

Slightly less convenient for domain consumers; avoids split-brain history.

## Consequences

Remove `AssetCommissioned` from normative Core event set. Projections may label transitions using machine metadata.
