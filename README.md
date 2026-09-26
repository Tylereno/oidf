# OIDF — Open Infrastructure Deployment Format

**OIDF is the format.** Schemas, ledgers, SAT gates, and architecture blueprints for evidence-gated commissioning.

Runtime that *implements* OIDF lives in a separate repo: **[`Tylereno/keel`](https://github.com/Tylereno/keel)**.  
VITO (sovereign edge node) lives in `ark-node`. VITO ≠ Keel ≠ OIDF.

> Progress only when the plant proves it.

## Repository map

```
docs/                 # Wiki front-end (why + how)
core_schemas/         # Machine-readable contracts (physics & state)
architectures/        # Deliverable-centric blueprints
tooling/              # Field execution helpers (open wedge)
tooling/UI_mockups/    # Read-only commissioning explorer
.github/              # Issue / PR templates
```

Baseline id: `KEEL-SPEC-BASELINE-2026.07.20` — see [`docs/normative/SPECIFICATION-BASELINE.md`](./docs/normative/SPECIFICATION-BASELINE.md).

Normative RFCs and JSON Schema IDL that Keel consumes live under `docs/normative/` and `core_schemas/idl/` (formerly `keel-specs/`).

## Start here

| Audience | Read |
|---|---|
| Anyone | [`docs/index.md`](./docs/index.md) |
| Strategy | [`docs/manifesto_and_thesis/`](./docs/manifesto_and_thesis/) |
| EPCs / field | [`docs/guides/getting_started.md`](./docs/guides/getting_started.md) |
| Schemas | [`core_schemas/`](./core_schemas/) |
| Blueprints | [`architectures/`](./architectures/) |
| Naming lock | [`NAMING.md`](./NAMING.md) |

## Honest status

- Normative RFCs, IDL, and evidence catalogs: **strong (lab)**
- Manifesto / offline sovereignty / attestation doctrine: **Phase 2 complete** (`docs/manifesto_and_thesis/`)
- AHJ compliance pack: **Phase 2 complete** (`docs/ahj/`)
- Keel lighthouse e2e: runs from **`Tylereno/keel`**, pinned to this repo’s contracts
- Not a SaaS, not Procore, not VITO

## Public transition

OIDF is being prepared for OpenLexicon stewardship. The format surface — the schema tree
and the read-only commissioning explorer — is published to **GitHub Pages** from this
repository by [`.github/workflows/pages.yml`](.github/workflows/pages.yml), so schema `$id`
values dereference against the public host `https://tylereno.me/oidf/`.

Repository ownership transfer, visibility, and onboarding of any external adopter remain
separate founder actions; this repository stays private until they complete.

## License

Apache 2.0 — see [`LICENSE`](./LICENSE), [`NOTICE`](./NOTICE). The license governs the format
and tooling in this repository regardless of hosting; only the repository's visibility is a
pending founder decision.
