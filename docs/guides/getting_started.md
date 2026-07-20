# Getting started — map a project to OIDF

For EPCs standing up a first OIDF-aligned commissioning path.

## Steps

1. **Pick one asset class** — start with BESS or solar inverter (see evidence catalogs under `core_schemas/evidence-catalog/`).
2. **Pin a machine definition** — states and evidence requirements must be explicit (see `core_schemas/equipment_state.yaml` and IDL under `core_schemas/idl/state/`).
3. **Log SAT gates** — each pass/fail becomes a `sat_event_log` record, not a chat message.
4. **Export a handoff ledger** — use `tooling/ledger_generator.py` (lab) or Keel sync export after reconnect.
5. **Validate** — `tooling/state_validator.py` checks claimed physical state against ledger events.

## Runtime

To *run* evidence-gated transitions, use **Keel**:

```bash
# in Tylereno/keel, with OIDF available as sibling or submodule
pip install -e 'keel-core[dev]'
python keel-examples/bess-lighthouse/run_e2e.py /tmp/keel-bess-lighthouse
```

## Do not

- Click-to-advance state in any UI without Evidence
- Put mesh IPs, CAGE, or real site coords in git
- Mix VITO dashboard work into this repo
