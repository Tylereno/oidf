# OIDF governance

OIDF is the format layer: schemas, evidence catalogs, state vocabulary, SAT
contracts, and replayable handoff artifacts. Keel is the separate runtime.

## Stewardship

OIDF is currently maintained by Tyler Eno under EnoTech. It is being prepared
for possible public stewardship under OpenLexicon. A GitHub organization or
repository transfer does not itself transfer copyright, trademarks, or create a
legal entity; those decisions require separate documentation.

## Normative authority

The source-of-truth order is:

1. `core_schemas/` and `docs/normative/`
2. evidence catalogs, architecture packs, and SAT gate maps
3. validators and field tooling
4. read-only explorer and other presentation surfaces

Keel must not redefine OIDF contracts locally. Any breaking contract change
requires a coordinated Keel pin/update plan.

## Review classes

- Editorial and example fixes: maintainer review plus green CI.
- Additive schema/catalog changes: compatibility note, validator coverage, and
  Keel impact assessment.
- State, evidence, ledger, SAT, or gate changes: RFC-style issue, explicit
  safety analysis, migration note, and maintainer approval.

OIDF must not gain daemons, runtime services, device adapters, persistence
layers, commissioning dashboards, or control loops. Those belong to Keel,
VITO, or a dedicated product surface.

## Contribution path

1. Open an issue describing the contract problem and affected consumers.
2. Submit a focused PR using the template.
3. Run the documented validators and field-tooling tests.
4. Include a Keel follow-up when runtime behavior must change.
5. Use DCO sign-off; no CLA is required at this stage.

As independent maintainers and adopters join, this provisional process can move
to a maintainer council or a neutral standards organization.
