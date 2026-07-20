# 05 — Offline-First Sovereignty

**Status:** Accepted doctrine  
**Related:** Sync RFCs, lighthouse DDIL criteria, VITO as sibling edge product (not this format)

---

## Thesis

**Sovereignty at the edge means the plant can tell the truth about itself without asking permission from a cloud.**

OIDF is designed so that:

1. State transitions are valid locally when Evidence is present.  
2. Events and ledgers are durable on-site.  
3. Reconnect sync merges history; it does not invent missing proof.  
4. AHJs and owners consume **exports**, not live SaaS sessions, for acceptance.

If your commissioning format requires continuous cloud reachability to advance state, it is not suitable for critical infrastructure under DDIL. Full stop.

## What “offline-first” means for the format

| Concern | OIDF stance |
|---|---|
| Source of truth during disconnect | Local event log + machine definition + Evidence |
| Human workflow | Sensors and policy approval allowed; click-to-advance forbidden |
| Inspection | Present the handoff ledger / SAT log for the window under review |
| Sync | Transport and merge; never a substitute for Evidence |
| Identity / signing | Must verify offline (see [06](./06_Attestation_and_Portability.md)) |

## Relationship to VITO

**VITO** is EnoTech’s sovereign edge *node* (crew ops, load-shed, persistence). OIDF is the *format* for commissioning truth. They compose; they are not aliases. A site may run VITO without OIDF, or an OIDF-compliant runtime without VITO. The format does not embed VITO APIs.

## Anti-patterns we refuse

- “We’ll backfill the ledger when Wi-Fi returns.”  
- “The dashboard is the record.”  
- “Sign the PDF; state will catch up.”  
- Treating sync conflicts as an excuse to drop Evidence requirements.

## Stance

Offline is not a degraded mode. For the missions that matter, offline is the design center. OIDF encodes that center in contracts so runtimes cannot quietly re-cloud the truth.
