# RFC 0001 — Top-Level Repository Topology

**Status:** Proposed  
**Phase:** 0  
**Role:** Repository Architect  
**Depends on:** 0000-CONSTITUTION  

## Purpose

Define the complete top-level repository topology for ARK.

This RFC establishes:
- Folder hierarchy
- Repository responsibilities
- Boundaries
- Ownership
- Dependency graph

It does not define APIs, schemas, technologies, or internal package layouts.

## Goals

- Split ARK into strict repositories from day one.
- Keep specifications separate from implementation.
- Make ownership and dependency direction unambiguous.
- Protect ARK Core by isolating integrations, samples, and documentation.

## Non-Goals

- Internal directory layouts within each repository
- Language, build system, or packaging choices
- Plugin inventory beyond constitutional examples
- Interface definitions or IDL selection
- CI/CD, release, or hosting details

## Assumptions (Explicit)

1. The workspace root `ark/` is an umbrella containing sibling repositories.
2. Each sibling listed below is a distinct repository with independent ownership and release cadence.
3. Until remotes are split, siblings may live as directories under one working tree; topology and boundaries remain identical.
4. `ark-specs` is the source of truth. Code repositories consume approved specifications; they do not redefine them.

## Folder Hierarchy

```
ark/
├── ark-specs/          # RFCs, ADRs, standards, glossary
├── ark-core/           # State engine & microkernel
├── ark-sdk/            # Plugin interfaces and developer SDK
├── ark-plugins/        # Official plugins
├── ark-reference/      # Sample implementations
├── ark-docs/           # User and operator documentation
└── ark-examples/       # Example deployments and tutorials
```

No other top-level product repositories are authorized by this RFC.

## Repository Responsibilities

### ark-specs

**Responsibility:** Architectural source of truth.

**Contains:**
- Constitution
- RFCs
- Architecture Decision Records (ADRs)
- Ubiquitous language glossary
- Interface specifications (IDL) once approved
- Architectural scorecards and governance artifacts

**Does not contain:**
- Application code
- Plugin implementations
- Operator runbooks that describe product usage rather than architecture

### ark-core

**Responsibility:** ARK microkernel and only the engines named by the Constitution.

**Contains (conceptually):**
- State Engine
- Event Engine
- Plugin Runtime
- Synchronization Engine
- Identity Interfaces
- Versioning
- Configuration
- Lifecycle composition policy (startup/shutdown/health ordering — not a domain engine; ADR-0005)

**Does not contain:**
- Transport protocols
- Persistence engines
- Cloud vendor integrations
- Enterprise product integrations
- UI
- Domain plugins
- Messaging, database, or serialization implementations

### ark-sdk

**Responsibility:** Contracts and tooling for building against ARK without modifying Core.

**Contains:**
- Plugin interfaces
- Developer SDK surfaces derived from approved specs
- Client helpers for publishing/subscribing to events as defined by specs

**Does not contain:**
- Core engine implementations
- Official plugin business logic
- Vendor-specific adapters

### ark-plugins

**Responsibility:** Official plugins that integrate external systems via events.

**Contains:**
- Isolated plugin packages (e.g. GIS, Primavera, SAP, Procore, OPC-UA, MQTT, SCADA, evidence, documents)

**Does not contain:**
- Changes to ARK Core
- Shared mutable Core state access
- Cross-plugin direct database writes

### ark-reference

**Responsibility:** Sample implementations that demonstrate correct composition of Core, SDK, and plugins.

**Contains:**
- Reference deployments
- Non-production sample stacks
- Teaching implementations aligned to approved RFCs

**Does not contain:**
- Production-hardened deployments
- New architectural contracts (those belong in ark-specs)

### ark-docs

**Responsibility:** Human documentation for users and operators.

**Contains:**
- User guides
- Operator guides
- Conceptual overviews derived from approved specs

**Does not contain:**
- Normative architecture (normative text lives in ark-specs)
- Implementation source of truth

### ark-examples

**Responsibility:** Example deployments and tutorials.

**Contains:**
- Tutorial scenarios
- Example Canonical Deployment Objects (once defined)
- Walkthroughs for common infrastructure deployment patterns

**Does not contain:**
- Core or plugin source of truth
- Normative specifications

## Boundaries

| Boundary | Rule |
|---|---|
| Specs ↔ Code | Specifications are normative. Code must reference approved RFCs. Code may not invent behavior absent an RFC. |
| Core ↔ Plugins | Plugins never modify Core. Plugins communicate only through events and approved SDK interfaces. |
| Core ↔ Persistence/Transport | Core knows nothing of concrete databases, brokers, clouds, or enterprise products. |
| Capability data | Each capability owns its data. No repository may directly mutate another capability’s datastore. |
| Docs ↔ Specs | Docs explain; specs govern. On conflict, ark-specs wins. |
| Reference/Examples ↔ Production | Reference and examples are illustrative. They are not production authorities. |

## Ownership

| Repository | Owns | Does not own |
|---|---|---|
| ark-specs | Architectural truth, RFCs, ADRs, glossary, IDL contracts | Runtime behavior |
| ark-core | Microkernel engines listed above | Integrations, UI, vendor adapters |
| ark-sdk | Developer-facing contracts and SDK | Core internals, plugin domain logic |
| ark-plugins | Official external integrations | Core, cross-cutting platform engines |
| ark-reference | Sample compositions | Normative contracts |
| ark-docs | User/operator documentation | Normative architecture |
| ark-examples | Tutorials and example deployments | Platform engines or plugin authority |

Ownership of a repository implies sole authority to change its public surface. Cross-repo changes require an approved RFC when they affect contracts.

## Dependency Graph

Dependency arrows mean “may depend on / consume contracts from.”

```
ark-specs
    ^
    |
    +------------------+------------------+
    |                  |                  |
ark-core            ark-sdk           ark-docs
    ^                  ^                  ^
    |                  |                  |
    |            ark-plugins              |
    |                  ^                  |
    |                  |                  |
    +-------> ark-reference <-------------+
                       ^
                       |
                 ark-examples
```

### Allowed dependencies

| From | To | Nature |
|---|---|---|
| ark-core | ark-specs | Implements approved Core specs |
| ark-sdk | ark-specs | Exposes approved interfaces |
| ark-plugins | ark-sdk, ark-specs | Implements plugins against SDK/contracts |
| ark-reference | ark-core, ark-sdk, ark-plugins, ark-specs | Composes for demonstration |
| ark-docs | ark-specs (required); others as descriptive sources | Documents |
| ark-examples | ark-reference, ark-sdk, ark-specs; optionally ark-plugins | Teaches |

### Forbidden dependencies

- ark-specs → any code repository
- ark-core → ark-plugins
- ark-core → ark-sdk (SDK adapts to Core/contracts; Core must not depend on SDK)
- ark-core → ark-reference, ark-docs, ark-examples
- ark-sdk → ark-plugins
- Any repository → another repository’s datastore

### Clarification: Core vs SDK

- **ark-core** implements the microkernel.
- **ark-sdk** is the outward contract surface for plugin authors and integrators.
- Core must remain free of SDK packaging concerns. SDK may wrap or mirror Core-facing contracts defined in ark-specs without becoming a Core dependency.

## Constraints

1. No additional top-level repositories without an ADR amending this RFC.
2. No mixing of specification and implementation in the same repository.
3. No technology choices are implied by repository names.
4. Internal layouts are deferred; this RFC defines topology only.

## Open Questions

1. Should `ark-plugins` be one repository with multiple packages, or one repository per plugin?  
   **Deferred.** Topology treats `ark-plugins` as the official plugin home; packaging granularity requires a later ADR.
2. When should sibling directories become separate remotes?  
   **Deferred.** Operational concern; does not change topological boundaries.

## Future Extensions

- Per-repository internal layout RFCs
- IDL repository placement refinement (remain under ark-specs unless an ADR says otherwise)
- Plugin packaging ADR
- Release and versioning topology ADR

## Architectural Scorecard (Phase 0)

| Quality | Score (1–10) | Notes |
|---|---|---|
| Modularity | 9 | Seven clear repositories with single responsibilities |
| Coupling | 9 | Specs-down dependency rules; Core isolated from plugins |
| Cohesion | 9 | Each repo has one job |
| Replaceability | 9 | Implementations are swappable behind specs |
| Testability | 8 | Topology enables isolated testing; harnesses not yet defined |
| Offline capability | 8 | Topology does not obstruct offline design; engines not yet specified |
| Security | 8 | Boundaries support Zero Trust later; no security design yet |
| Observability | 7 | No observability topology yet — deferred to later RFCs |
| Extensibility | 9 | Plugins and SDK are first-class extension paths |
| Documentation | 8 | Docs/examples separated from normative specs |
| Cognitive Load | 9 | Seven concepts; no premature internal complexity |

No score is below 8 except Observability (7), which is expected before Event/Security RFCs. Recommendation: proceed after Phase 0 acceptance; address observability in later specification phases, not by expanding topology now.
