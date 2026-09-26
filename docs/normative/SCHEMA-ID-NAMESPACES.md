# Schema `$id` namespaces (single authority host)

**Status:** Accepted — single authority host
**Supersedes:** the two-host `oidf.dev` / `keel.dev` split (unification deferred). Both prior
hosts were unregistered; see *Migration record* below.
**Related:** [RFC 0015](./0015-INTERFACE-DEFINITIONS.md), [RFC 0022](./0022-PRODUCT-NAMING.md),
[`core_schemas/README.md`](../../core_schemas/README.md)

## One authority host

Every OIDF schema `$id` uses:

```
https://openlexicon.github.io/oidf/schemas/…
```

served by GitHub Pages directly from this repository, so each `$id` dereferences to the file that
declares it. CI enforces this with [`tooling/verify_pages_ids.py`](../../tooling/verify_pages_ids.py);
staging is defined by [`.github/workflows/pages.yml`](../../.github/workflows/pages.yml).

### Why this host

- `oidf.dev`, `openeno.dev`, and `keel.dev` are **not registered** — the previous namespaces were
  dead identifiers, not just unreachable ones.
- The two-host split had already broken in tree: 18 IDL files carried `oidf.dev` while
  `state/transition_requested.json` and `sync/sync_batch.json` still carried `keel.dev`.
  A single host removes the ambiguity that produced it.
- The `github.io` path is free and HTTPS, and needs no domain or DNS operation. A vanity domain
  added later MUST **mirror this path**, never replace it — see *Frozen identifiers*.

## Served paths

| Artifact | On-disk path | Served path (`$id` suffix) |
|---|---|---|
| Front-door contracts | `core_schemas/<name>.json` | `schemas/<name>.json` |
| Normative IDL | `core_schemas/idl/<sub>/<name>.json` | `schemas/<sub>/<name>.json` |

The `idl/` path segment is **not part of the ID namespace**: IDL `$id` values have always read
`…/schemas/<sub>/<name>.json`. Pages staging therefore flattens `idl/` away to match, and the
withdrawn `…/schemas/idl/…` alias is not resurrected.

## Migration record

| Step | State |
|---|---|
| Replace dead hosts with the Pages host in tree | **Done** — 30 files, `cursor/pages-namespace-1c3b` |
| Publish the schema tree on Pages so every `$id` dereferences | **This change** (`.github/workflows/pages.yml` + `verify_pages_ids.py`) |
| Keel pin accepts the new host | **Open — required before Keel's next pin bump** |

**Keel follow-up.** Keel consumes OIDF by submodule/`OIDF_ROOT` and pins this repo's baseline, with
resolution tests asserting RFC 0015 URIs. Keel is a private consumer and its current pin is
unaffected, but before it re-pins it must accept `https://openlexicon.github.io/oidf/schemas/…`,
either by re-pinning past this change or by dual-loading both hosts. This is the coordinated
consumer step the previous policy deferred; it is now a tracked follow-up rather than a blocker.

## Frozen identifiers

An `$id` that has been published is a **frozen identifier**. Do not rename `$id` values ad hoc; a
change requires the same three-step migration (serve the new host → consumer dual-loads → a
baseline-tagged in-repo rewrite). Adding a vanity domain does not rename anything: point it at the
same served paths and keep the `github.io` `$id` canonical.
