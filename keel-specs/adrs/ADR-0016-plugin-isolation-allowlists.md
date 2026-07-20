# ADR-0016 — Plugin Isolation Floor & Publish Allowlists

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0007, 0006, 0012; Failure Modes: Host Crash, Memory Exhaustion, Privilege Escalation  

## Context

In-process Plugins can crash Core, exhaust memory, or emit privileged Events.

## Decision

1. Production Plugin Runtime isolation floor: **separate failure domain** from Core engines (process or equivalent sandbox). In-process is allowed only for reference/dev profiles, never production conformance.
2. Runtime MUST enforce resource quotas from Configuration; breach quarantines Plugin.
3. Event Engine MUST enforce per-Plugin **publish allowlists** from CapabilityDescriptor; attempts to publish `StateAdvanced` or other Core-privileged types are rejected unless explicitly granted (default: deny).
4. Plugins NEVER receive State Engine internal ports—only Event publish/subscribe host APIs.

## Alternatives

- Trust Plugin authors (rejected).
- Shared-memory in-process production (rejected).

## Tradeoffs

Higher ops complexity; matches Constitution isolation requirements.

## Consequences

Plugin Runtime port includes quarantine/quota; SDK documents allowlist rules; production profile ≠ reference profile.
