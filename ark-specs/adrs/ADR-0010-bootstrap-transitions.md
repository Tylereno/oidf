# ADR-0010 — Bootstrap Transitions Are Machine-Defined

**Status:** Accepted
**Date:** 2026-07-20  
**Related RFCs:** 0000, 0005, 0006, 0011, 0014  

## Context

Principle 4 (Evidence precedes progression) appears to conflict with creating a Deployment (`DeploymentCreated`) before Evidence exists.

## Decision

Creation and other bootstrap steps are ordinary transitions of a MachineDefinition. Evidence requirements may be empty only if explicitly declared in that machine. Authorization still applies. UI clicks never bypass the machine.

## Alternatives

- Hard-code Core bootstrap exceptions (Core growth / special cases forever).
- Require Evidence even for empty Deployment create (often artificial Evidence).

## Tradeoffs

Allows minimal create machines; keeps all progression data-driven.

## Consequences

`DeploymentCreated` remains an Event accompanying/resulting from bootstrap transition per machine design; Phase 3 will define exact emission pairing.
