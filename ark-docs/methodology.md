# Commissioning methodology (Evidence Packet)

**Audience:** hiring panels, primes, owner’s engineers, EnoTech capability statements.  
**Normative authority:** `ark-specs` (this page explains; specs govern).

## Thesis

The failure mode that matters in physical commissioning is not the Gantt chart — it is **state drift**: assets marked complete without the evidence that should have gated energization or handoff.

ARK’s operating discipline:

1. Every asset has exactly one current state in a declared machine.
2. Transitions are deterministic and replayable.
3. **Evidence precedes progression** — UI clicks, verbal claims, and unvalidated submissions do not advance state.
4. Offline / air-gapped sites retain local progression authority; cloud is optional.
5. Audit is the event history, not a mutable status column.

## What “evidence-gated” means in practice

| Attempt | Outcome |
|---|---|
| Tech marks “done” in a checklist UI | Not Evidence — cannot satisfy a gate |
| `EvidenceSubmitted` without validation | Logged claim only — gate still closed (ADR-0012) |
| Authorized `EvidenceValidated` for required type | Counts toward the transition |
| Transition with insufficient evidence | `TransitionRejected` / `MissingEvidence`; state unchanged |
| Transition with sufficient evidence + deps | `StateAdvanced`; history pinned to CDO/config/machine revisions |

Runnable proof: `python ark-core/examples/commission_gate_demo.py`

## Positioning (use the right vehicle)

### Technical PM / commissioning hire

> I don’t just update schedules. I engineer evidence-gated commissioning: sites cannot advance until required validated evidence exists. ARK is the open methodology and kernel I use to prove that discipline.

### EnoTech / CAGE capability statement (one bullet)

> **Evidence-gated commissioning architecture (ARK):** deployment state advances only when required validated evidence exists; supports offline/air-gapped progression with an immutable event history suitable for audit and handoff packages.

### Not yet — standalone software sale

Do not pitch ARK as a SaaS product until a real site checklist is mapped and durable storage + at least one Evidence source plugin exist. Until then, ARK is a **methodology artifact and kernel**, not a fielded product SKU.

## Honest limitations (say these out loud)

- No production persistence/transport adapters yet (in-memory for Core demos).
- Signed Events / crypto profile deferred — do not claim cryptographic attestation.
- Official OT/enterprise plugins are not shipped; machine Evidence must be integrated per site.
- Humans can still produce Evidence; the kernel prevents **status-click theater**, not automatically **evidence theater**, until validators and plugins are real.

## Where to go next in the repo

| Artifact | Path |
|---|---|
| Demo script | `ark-core/examples/commission_gate_demo.py` |
| Air-gapped walkthrough | `ark-examples/airgapped-commission.md` |
| Constitution | `ark-specs/0000-CONSTITUTION.md` |
| Evidence trust ADR | `ark-specs/adrs/ADR-0012-evidence-trust-freshness.md` |
| Failure modes | `ark-specs/ARCHITECTURAL_FAILURE_MODES.md` |
