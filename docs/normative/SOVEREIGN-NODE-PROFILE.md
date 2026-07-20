# Sovereign node profile (OT / DDIL)

**Status:** Normative (profile)  
**Baseline:** `KEEL-SPEC-BASELINE-2026.07.20` and successors  
**Schemas:** [`site_state.json`](../../core_schemas/site_state.json), [`site_event_log.json`](../../core_schemas/site_event_log.json)  
**ADR:** [ADR-0019](./adrs/ADR-0019-ai-assistive-not-authoritative.md)

## Intent

A **sovereign node** keeps a site useful when backhaul and cloud control planes are gone. OIDF does not prescribe containers, LLMs, or product UI. It does prescribe **durable operational truth** and **who may authorize** continuity actions.

## Required capabilities (profile)

1. **Durable `site_state`** — survives process restart and power cycle (NVMe/disk or equivalent).  
2. **Append-only `site_event_log`** — every material tier/mode/alarm/config/service decision is recorded.  
3. **Deterministic policy path** for shed, store-and-forward, and recovery — thresholds and actuators that run without a model.  
4. **No-AI mode** — profile remains operable with assist disabled or unavailable.  
5. **Assistive AI optional** — may read state and emit `assist_suggestion` events; must not be sole `authority` on safety/continuity events (ADR-0019).

## Layering (informative)

| Layer | Responsibility |
|---|---|
| State | Current tier, backhaul mode, alarms, last-known-good |
| Policy | When to shed, store-forward, reboot |
| Actuators | Service stop/start, queue writes, watchdog |
| Assist | Explain / suggest / Q&A bound to state APIs |

## Relationship to commissioning

- **Equipment / commissioning state** remains handoff ledger + SAT + evidence catalogs (Keel and peers).  
- **Site operational state** is this profile.  
- An edge node may **stage** OIDF evidence files for later Keel validation; it does not become the commissioning authority (see cross-stack VITO/OIDF boundary ADR in `enotech-site`).

## Out of scope

- Named multi-agent casts as normative architecture  
- Requiring GPU/LLM for field operation  
- Replacing Keel state advance with chat consensus  
