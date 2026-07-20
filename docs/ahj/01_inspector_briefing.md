# 01 — Inspector briefing

**For:** Fire marshals, electrical inspectors, building officials, utility field acceptance  
**Goal:** Explain OIDF in five minutes without jargon theater

---

## What you are looking at

OIDF (Open Infrastructure Deployment Format) is a **structured commissioning record**, not a software login and not a replacement for the NEC or NFPA.

When a contractor says an asset is “commissioned,” OIDF expects them to show:

1. **What state the asset is in** (e.g. `Installed`, `Commissioned`, `Energized`).  
2. **What Evidence unlocked the last transition** (typed facts — voltage in band, insulation OK, anti-islanding OK, etc.).  
3. **What SAT gates passed or failed** (pass / fail / blocked with timestamps).  
4. **A handoff ledger** — a sequenced digital as-built for the inspection window.

You still apply your adopted codes. OIDF makes the *proof trail* inspectable.

## How this differs from a PDF packet

| Traditional packet | OIDF packet |
|---|---|
| Photos, signed forms, scattered reports | Same materials *plus* a structured ledger |
| Hard to replay order of events | `seq` ordered transitions with times |
| “Complete” checkbox | Evidence types required by a machine definition |
| Cloud screenshot | Offline **export** you can take with you |

Ask for the **export**, not a live dashboard. Sites may have been offline during commissioning. That is expected.

## Words you will see

| Term | Plain meaning |
|---|---|
| **State** | Named step in the commissioning path (Installed, Commissioned, …) |
| **Evidence** | A typed fact that must exist before a state may change |
| **Machine Evidence** | Fact from instruments / BMS / inverter — not a human checkbox alone |
| **SAT event** | Result of a Site Acceptance Test gate: pass, fail, or blocked |
| **Handoff ledger** | Append-only list of state changes with links to Evidence |
| **Signed Event** (high-assurance) | Cryptographic integrity on log entries (Ed25519) — optional on early lab paths; may be required on regulated pilots |

## What OIDF does *not* do

- Does not issue permits or energization authority  
- Does not replace your inspection judgment  
- Does not prove that a measurement was physically correct — it proves the commissioning system *required* and *recorded* that class of fact  
- Does not require you to approve blockchain, clouds, or vendor lock-in

## Suggested inspection ask-list

1. Show the **machine definition** (allowed states and required Evidence).  
2. Show the **handoff ledger** for this asset covering today’s window.  
3. For the latest transition, show the **Evidence types** and SAT events cited.  
4. Confirm energization clearance Evidence exists before `Energized` (canonical path).  
5. If high-assurance: confirm signatures verify on the exported batch (runtime tooling).

## Bottom line

Treat OIDF like a **structured logbook that cannot quietly skip gates**. Your authority stays yours. The format exists so “we tested it” can be replayed instead of asserted.
