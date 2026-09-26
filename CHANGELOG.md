# Changelog

All notable OIDF format changes are recorded here.

## [Unreleased]

### Format namespace — single authority host

- **Breaking (identifier) change:** all schema `$id` values move to one authority host,
  `https://tylereno.me/oidf/schemas/…`, served by GitHub Pages from this
  repository. The previous `oidf.dev` and `keel.dev` hosts are unregistered; the split had
  already broken in tree (18 IDL files on `oidf.dev`, two on `keel.dev`). See
  [`docs/normative/SCHEMA-ID-NAMESPACES.md`](docs/normative/SCHEMA-ID-NAMESPACES.md).
- Added `tooling/verify_pages_ids.py`: enforces that every published `$id` equals the Pages
  base plus the path at which the file is served, and (in CI) that the file is staged.
- `.github/workflows/pages.yml` now publishes the schema tree alongside the commissioning
  explorer, so every `$id` dereferences instead of 404ing.
- **Consumer follow-up (required before the next Keel pin bump):** Keel must accept the new
  host — by re-pinning past this change, or by dual-loading both hosts.

## [4.7.0-format-baseline] - 2026-08-20

- Maintain front-door schemas for handoff ledgers, SAT logs, site state, and
  event logs.
- Maintain equipment lifecycle and BESS/solar evidence catalogs.
- Maintain three lab architecture packs with SAT gate maps and examples.
- Maintain the read-only commissioning explorer.

OIDF remains a format and contract surface. Keel remains the runtime authority.
