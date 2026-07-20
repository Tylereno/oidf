# ark-core examples

Runnable teaching scripts for the Phase 6 Core. Not production deployments.

## Commissioning gate demo

Shows Principle 4: a switchgear asset cannot move `Installed → Commissioned` until `TorqueVerified` Evidence is validated.

```bash
pip install -e ark-core
python ark-core/examples/commission_gate_demo.py
```

Expected arc:

1. Transition without evidence → `TransitionRejected` / `MissingEvidence`
2. `EvidenceSubmitted` alone still rejected (ADR-0012)
3. `EvidenceValidated` recorded
4. Transition succeeds → `StateAdvanced`

Record with Asciinema for portfolio / interview use:

```bash
asciinema rec ark-commission-gate.cast -c "python ark-core/examples/commission_gate_demo.py"
```
