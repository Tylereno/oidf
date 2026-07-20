# ADR-0019 — AI-Assistive, Not AI-Authoritative (OT / DDIL)

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0000, 0005, 0006, 0012; ADR-0002, ADR-0012, ADR-0018  
**Cross-stack:** enotech `docs/adrs/0001-vito-oidf-evidence-boundary.md`

## Context

Edge products for Denied / Degraded / Intermittent / Limited (DDIL) and operational-technology (OT) sites need durable site state, deterministic shed/recovery policy, and attributable decisions. Marketing and prototype UIs often center a “crew” of LLM agents that discuss and act. That pattern is unsafe as a control architecture: model availability, non-determinism, and unauditable authority fail the same environments OIDF exists to harden.

OIDF already treats commissioning progression as evidence-gated state advance (ADR-0002). Sovereign edge operation needs the same discipline for **site operational state** (power tier, backhaul mode, alarms, committed config) — whether or not a commissioning runtime is co-located.

## Decision

1. **OIDF defines** front-door contracts for sovereign-node operational truth:
   - `core_schemas/site_state.json` — current durable site state  
   - `core_schemas/site_event_log.json` — append-only decisions and transitions  
   Normative profile prose: `docs/normative/SOVEREIGN-NODE-PROFILE.md`.

2. **AI (LLMs / agent frameworks) MAY** provide assistive interfaces: explain state, summarize telemetry, draft suggestions, crew Q&A. Assist outputs are **non-authoritative**.

3. **AI MUST NOT** be the sole authority for safety- or continuity-critical actions, including but not limited to: power-tier / load-shed changes, watchdog-driven recovery, service stop/start that implements shed policy, backhaul mode flips that drop safety monitoring, or commit of last-known-good configuration.

4. In `site_event_log`, events that change power tier, execute service shed/recovery actions, or record watchdog recovery **MUST** set `authority` to `policy`, `operator`, or `system`. `assist` may appear only as `actor.kind` on **suggestion** events (`kind = assist_suggestion`, `suggestion_only = true`).

5. Edge nodes (including VITO) and runtimes (including Keel) that claim OT/DDIL or sovereign-node profile conformance **MUST** implement durable site state + event log shapes compatible with these schemas (file, sqlite, or equivalent). Chat transcripts and in-memory agent sessions are **not** systems of record.

6. Named “agent” personas are **presentation or module labels only**. They are not OIDF types and MUST NOT appear as required actors in normative contracts.

## Alternatives

- **LLM-centric control plane** — Rejected for OT/DDIL: non-deterministic authority, fails closed poorly when models or GPUs are unavailable.  
- **VITO-only private state dialect** — Rejected: breaks portable handoff and multi-runtime review; OIDF owns truth shapes (ADR-0018 spirit).  
- **No AI allowed ever** — Over-restrictive. Assistive UI is valuable if bound to read APIs and suggestion events.

## Tradeoffs

Nodes must persist and validate site state even in a No-AI profile. Assist features need clear UX that suggestions are not commits. In return: replayable operations, AHJ-defensible continuity claims, and a product that survives dark sites.

## Consequences

- VITO architecture centers **state + policy + actuators**; optional Operator Assist binds to those contracts.  
- Keel may import/validate `site_state` / `site_event_log` artifacts when staged from an edge node; Keel remains commissioning authority for equipment state machines.  
- Public and internal prose: sovereign node ≠ multi-agent debate club.  
- Catalog/evidence additions for site continuity remain separate PRs when typed Evidence is required for commissioning gates.
