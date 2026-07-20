# Contributing to OIDF

OIDF is the **format**. Changes here redefine contracts that Keel and field tooling must obey.

## Governance (benevolent dictator)

Until a public standards body exists, the founder accepts or rejects contract changes. Prefer small, evidence-backed PRs.

## Format-only repo rules

This repository contains the OIDF contract surface:

- Normative docs and ADRs in `docs/normative/`
- JSON schemas and evidence catalogs in `core_schemas/`
- Architecture packs and examples in `architectures/`
- Small artifact tooling used to validate or generate OIDF files in `tooling/`

It does **not** contain runtime implementations. Do not add daemons, control loops, device adapters, persistence layers, network services, or product UI here. Runtime code belongs in [`Tylereno/keel`](https://github.com/Tylereno/keel). VITO / crew edge runtime work belongs in `ark-node`.

## Contribution rules

1. **Safety / state compliance** — PRs that change state machines, evidence types, or ledgers must show how invalid advances are still blocked.
2. **No duplicate SoT** — Machine contracts live in `core_schemas/`. Do not redefine them in Keel or VITO.
3. **Honest language** — Lab vs production. No CAGE, real coords, mesh IDs, Tailscale IPs, customer secrets, or real site coordinates in git.
4. **Format before runtime** — If a change needs Keel behavior, update OIDF contracts here and link the Keel follow-up instead of embedding runtime logic in this repo.
5. **Examples must replay** — Architecture example ledgers and SAT logs must validate against the checked-in schemas.

## PR checklist

Use [`.github/PULL_REQUEST_TEMPLATE.md`](./.github/PULL_REQUEST_TEMPLATE.md). Issue templates cover field failures and hardware edge cases.

Every PR should include:

- A short summary of the contract/doc change
- Contract impact: schemas, evidence catalogs, architecture packs, docs-only, or tooling
- Safety/state impact for any state machine, evidence type, ledger, SAT, or gate change
- Proof that schema CI is green, or the exact local validator output if CI is unavailable
- Links to Keel follow-up PRs/issues when runtime behavior must consume the new format

## Running validation locally

Install the one required validator dependency:

```bash
python -m pip install "jsonschema>=4.0"
```

Run the validators before opening a PR and after any schema, catalog, architecture example, or tooling change:

```bash
python tooling/validate_json_schemas.py core_schemas/idl
python tooling/validate_architecture_examples.py
```

Field tooling unit tests are also run by CI:

```bash
python -m unittest tooling.test_field_tooling -v
```

Field helpers:

- `ledger_generator.py` — schema-valid ledgers; rejects empty `evidence_refs` on commission/energize
- `state_validator.py` — schema + optional machine checks
- `sat_event_log.py` — create / append / validate SAT logs

GitHub Action: `.github/workflows/json-schema.yml`.
