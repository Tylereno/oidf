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
- Public wiki / manifesto / AHJ guides: **skeleton — fill as wedge hardens**
- Keel lighthouse e2e: runs from **`Tylereno/keel`**, pinned to this repo’s contracts
- Not a SaaS, not Procore, not VITO

## License

Apache 2.0 — see [`LICENSE`](./LICENSE). Repo remains **private** until the founder flips visibility.
