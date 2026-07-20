# ark-core

**Ownership:** ARK Core maintainers  
**Normative authority:** `ark-specs`

## Responsibility

ARK microkernel. Implements only:

- State Engine
- Event Engine
- Plugin Runtime
- Synchronization Engine
- Identity Interfaces
- Versioning
- Configuration
- Lifecycle

## Boundaries

- Must not contain transport, persistence, cloud, or enterprise product integrations.
- Must not depend on `ark-plugins`, `ark-sdk`, `ark-reference`, `ark-docs`, or `ark-examples`.
- May depend only on approved contracts in `ark-specs`.

## Status

Topology reserved. No implementation until authorized by later phases and approved RFCs.
