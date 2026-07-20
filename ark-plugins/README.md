# ark-plugins

**Ownership:** ARK Plugin maintainers  
**Normative authority:** `ark-specs`  
**Integration surface:** `ark-sdk`

## Responsibility

Official plugins. Each plugin integrates an external system by subscribing to and publishing events.

## Boundaries

- Plugins are isolated and may fail independently.
- Plugins never modify ARK Core.
- Plugins never directly mutate another capability’s datastore.
- May depend on `ark-sdk` and approved contracts in `ark-specs`.
- Must not be depended upon by `ark-core` or `ark-sdk`.

## Status

Topology reserved. Packaging granularity (mono-package vs per-plugin repos) is deferred to a later ADR.
