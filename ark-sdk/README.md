# ark-sdk

**Ownership:** ARK SDK maintainers  
**Normative authority:** `ark-specs`

## Responsibility

Plugin interfaces and developer SDK for building against ARK without modifying Core.

## Boundaries

- Must not implement Core engines.
- Must not contain official plugin domain logic or vendor adapters.
- Must not depend on `ark-plugins`.
- May depend only on approved contracts in `ark-specs`.

## Status

Topology reserved. No implementation until authorized by later phases and approved RFCs.
