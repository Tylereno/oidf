# RFC 0018 — Phase 5-to-6 Transition Report

**Status:** Awaiting Approval  
**Date:** 2026-07-20  
**Roles:** Core Architect · Governance Guardian · Red Team Lead  
**Baseline:** `ARK-SPEC-BASELINE-2026.07.20`  
**Repo:** Tylereno/oidf (consolidates PR #6 stack + this transition)

---

## 1. Spec & ADR Consolidation Status

### Audit of PR #6 stack

| Area | Result |
|---|---|
| RFCs 0001–0017 + Constitution | Present and cross-linked |
| ADR-0001–0011 | Present; Status set to **Accepted** |
| JSON Schema IDL under `ark-specs/idl/` | Present; amended for Evidence freshness + Sync fencing |
| Test specs TS-0001–0020 (RFC 0016) | Present; reference suite 17 automated tests green |
| Hexagonal boundary (no concrete storage/transport/cloud in Core contracts) | **PASS** — vendors appear only as forbidden knowledge / Plugin examples |

### Consolidation actions completed

1. Declared [`SPECIFICATION-BASELINE.md`](./SPECIFICATION-BASELINE.md) with Baseline ID.
2. Marked architecture RFCs **Accepted (Specification Baseline)**.
3. Locked ADR-0001–0011 as **Accepted**.
4. Added baseline amendments ADR-0012–0016 from Red Team (Accepted).
5. Staged production port topology under `ark-core/` and `ark-sdk/` (**no adapters**).

### Immutability

Once merged to `main`, behavioral changes require ADR + RFC amendment. Phase 6 modules MUST embed `SPEC_BASELINE_ID`.

---

## 2. Red Team Discoveries & Failure Modes Updates

Document: [`ARCHITECTURAL_FAILURE_MODES.md`](./ARCHITECTURAL_FAILURE_MODES.md)

### Stress coverage

| Theme | Critical outcomes |
|---|---|
| Evidence-gated transitions | Forged `EvidenceValidated`, stale Evidence reuse, transition races, dependency deadlocks |
| Offline & sync | Split-brain multi-writer, clock-drift ordering, affinity epoch fencing, node key compromise |
| Plugin isolation | Host crash propagation, memory exhaustion, publish privilege escalation |

### Contract amendments (Accepted)

| ADR | Mitigation |
|---|---|
| 0012 | Evidence trust chain + freshness windows |
| 0013 | Per-subject single-flight + acyclic MachineDefinition deps |
| 0014 | Sync fencing epochs + ordering authority clarification |
| 0015 | Node trust rotation / revocation control plane |
| 0016 | Production isolation floor + publish allowlists |

### IDL deltas

- `evidence_submitted` / `evidence_validated`: optional `valid_from` / `valid_until`
- `sync_batch`: optional `affinity_epochs` map

### Verdict

Architecture is viable for Phase 6 **ports** only if ADR-0012–0016 are enforced before adapters. Red Team does **not** authorize production application logic or infrastructure adapters in this step.

---

## 3. Proposed Phase 6 Production `ark-core` Package Topology

```
ark-core/src/ark_core/
  baseline.py          # SPEC_BASELINE_ID
  domain/              # identifiers, errors (pure)
  ports/               # Event, State, PluginRuntime, Sync, Identity, Authorize, Config, Clock
  app/                 # EMPTY — awaiting approval
  adapters/            # EMPTY / forbidden for concrete infra this phase

ark-sdk/src/ark_sdk/
  ports/host_port.py   # PluginHostPort (Event in/out only)
  ports/capability.py  # descriptor shape checks
```

### Ports (match approved IDLs / RFCs)

| Port | File | Primary RFCs/ADRs |
|---|---|---|
| EventPort | `ports/event_port.py` | 0006, 0016 |
| StateEnginePort | `ports/state_port.py` | 0005, 0001, 0012, 0013 |
| PluginRuntimePort | `ports/plugin_runtime_port.py` | 0007, 0016 |
| SyncEnginePort | `ports/sync_port.py` | 0008, 0014, 0015 |
| IdentityPort | `ports/identity_port.py` | 0009, 0015 |
| AuthorizePort | `ports/authorize_port.py` | 0012, 0007 |
| ConfigPort | `ports/config_port.py` | 0011, 0008 |
| ClockPort | `ports/clock_port.py` | testability / freshness |
| PluginHostPort (SDK) | `ark_sdk/ports/host_port.py` | 0007 |

### Conformance commitment

Production Core application services (when approved) MUST pass TS-0001–TS-0020 against locked IDL + ADR-0012–0016 rules.

### Explicitly NOT done (awaiting approval)

- Application service implementations in `ark_core.app`
- Any SQLite/Postgres/NATS/MQTT/cloud adapter code
- Crypto algorithm selection ADR
- Official Plugin implementations

---

## Approval Gate

**Request:** Approve this Transition Report to authorize writing production application services behind the ports (still without concrete infra adapters unless separately approved).

Until approval: no production application code beyond this ports scaffold.
