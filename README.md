# ARK

**Autonomous Resilient Kernel** — offline-first deployment operating system for physical infrastructure.

ARK orchestrates bringing assets from planned to commissioned condition using deterministic state machines, event sourcing, and **evidence-gated** transitions. It is not project management software. It is not another Procore or Primavera.

> Nothing advances because a user clicked a button.  
> Everything advances because sufficient evidence exists.

## The problem

Commissioning and startup on physical sites still advance on **human status declarations** — workflow buttons, verbal claims, pencil-whipped checklists. That produces state drift, weak audit trails, and broken offline operation.

ARK replaces status theater with machine rules: a transition is legal only when typed, attributable, **validated** Evidence (and peer dependencies) are satisfied. Current state is a projection of an immutable event history — not a field someone edited.

## 60-second demo

```bash
pip install -e ark-core
python ark-core/examples/commission_gate_demo.py
```

You will see:

1. `Installed → Commissioned` **rejected** — missing `TorqueVerified`
2. Submit-only evidence still rejected (clicks / claims are not gates)
3. `EvidenceValidated` accepted
4. Same transition **advances** — asset Commissioned, no cloud required

Narrative walkthrough: [`ark-examples/airgapped-commission.md`](./ark-examples/airgapped-commission.md)  
Methodology (hire / bid framing): [`ark-docs/methodology.md`](./ark-docs/methodology.md)

## What exists today

| Layer | Status |
|---|---|
| Specs (constitution, RFCs, ADRs, IDL, test specs) | Locked baseline `ARK-SPEC-BASELINE-2026.07.20` |
| Phase 6 Core app services (State / Event / Sync / Authorize) | Working behind ports |
| Commissioning gate demo | Runnable |
| Conformance tests | `pytest` green on core + reference |
| Production adapters (Postgres, NATS, MQTT, crypto) | Deferred |
| Official plugins / operator UI | Not built yet |

Honest scope: this is a **working microkernel + specification**, not a fielded Edge product. Signed Events and durable storage are next implementation work — do not claim cryptographic attestation until those land.

## Quick start (tests)

```bash
pip install -e "ark-core[dev]" -e ark-reference
pytest ark-core/tests ark-reference/tests -q
```

## Topology

```
ark/
├── ark-specs/          # RFCs, ADRs, IDL (source of truth)
├── ark-core/           # State engine & microkernel (Phase 6+)
├── ark-sdk/            # Plugin interfaces and developer SDK
├── ark-plugins/        # Official plugins (reserved)
├── ark-reference/      # Phase 5 reference + conformance tests
├── ark-docs/           # User / operator / methodology docs
└── ark-examples/       # Teaching walkthroughs
```

## Charter

- Constitution: [`ark-specs/0000-CONSTITUTION.md`](./ark-specs/0000-CONSTITUTION.md)
- Glossary: [`ark-specs/0002-UBIQUITOUS-LANGUAGE.md`](./ark-specs/0002-UBIQUITOUS-LANGUAGE.md)
- Specs index: [`ark-specs/README.md`](./ark-specs/README.md)
