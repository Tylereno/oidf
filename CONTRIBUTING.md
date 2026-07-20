# Contributing to OIDF

OIDF is the **format**. Changes here redefine contracts that Keel and field tooling must obey.

## Governance (benevolent dictator)

Until a public standards body exists, the founder accepts or rejects contract changes. Prefer small, evidence-backed PRs.

## Rules

1. **Safety / state compliance** — PRs that change state machines, evidence types, or ledgers must show how invalid advances are still blocked.
2. **No duplicate SoT** — Machine contracts live in `core_schemas/`. Do not redefine them in Keel or VITO.
3. **Honest language** — Lab vs production. No CAGE, real coords, mesh IDs, or Tailscale IPs in git.
4. **Runtime code belongs in Keel** — `Tylereno/keel`. This repo is docs, schemas, architectures, and field tooling only.
5. **VITO is out of scope** — Edge dashboard / crew runtime → `ark-node`.

## PR checklist

Use [`.github/PULL_REQUEST.md`](./.github/PULL_REQUEST.md). Issue templates cover field failures and hardware edge cases.

## Schema CI

PRs that touch `core_schemas/` must keep IDL green:

```bash
pip install 'jsonschema>=4.0'
python tooling/validate_json_schemas.py core_schemas/idl
python tooling/validate_architecture_examples.py
python -m unittest tooling.test_field_tooling -v
```

Field helpers:

- `ledger_generator.py` — schema-valid ledgers; rejects empty `evidence_refs` on commission/energize
- `state_validator.py` — schema + optional machine checks
- `sat_event_log.py` — create / append / validate SAT logs

GitHub Action: `.github/workflows/json-schema.yml`.
