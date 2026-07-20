# ark-examples

**Ownership:** ARK Examples maintainers  
**Normative authority:** `ark-specs`

## Responsibility

Example deployments and tutorials.

## Boundaries

- Teaching artifacts only.
- Must not redefine Core, SDK, or plugin behavior.
- May depend on `ark-reference`, `ark-sdk`, `ark-specs`, and optionally `ark-plugins`.
- Runnable Core demos live under `ark-core/examples/` (topology: examples do not import `ark-core`).

## Contents

| Artifact | Purpose |
|---|---|
| [`airgapped-commission.md`](./airgapped-commission.md) | Narrative: Installed → Commissioned offline with evidence gates |
| [`capability-statement-bullet.md`](./capability-statement-bullet.md) | Copy for EnoTech / CAGE one-pagers |

## Run the companion demo

```bash
pip install -e ark-core
python ark-core/examples/commission_gate_demo.py
```
