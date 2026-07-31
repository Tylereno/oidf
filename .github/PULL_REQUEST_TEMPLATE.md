## Summary

## Contract impact

- [ ] Touches `core_schemas/` schemas or evidence catalogs
- [ ] Touches architecture packs, SAT gate maps, or examples
- [ ] Touches normative docs / ADRs
- [ ] Touches validation or field tooling
- [ ] Docs-only, no contract change

## Safety / state compliance

If this changes state machines, evidence types, ledgers, SAT gates, or architecture examples, explain how invalid advances remain blocked:

## Schema CI / validation

- [ ] GitHub Actions schema CI is green on this PR
- [ ] `python tooling/validate_json_schemas.py core_schemas/idl`
- [ ] `python tooling/validate_architecture_examples.py`
- [ ] `python -m unittest tooling.test_field_tooling -v` or explained why not applicable
- [ ] `python -m unittest tooling.test_oidf_canonical -v` or explained why not applicable

## Runtime boundary

- [ ] No runtime implementation, daemon, adapter, persistence layer, network service, or product UI was added to OIDF
- [ ] Keel runtime follow-up is linked or explicitly not needed

## Hygiene

- [ ] No secrets, real site coordinates, mesh IDs, CAGE data, Tailscale IPs, or customer identifiers added
- [ ] Lab vs production status is stated honestly
