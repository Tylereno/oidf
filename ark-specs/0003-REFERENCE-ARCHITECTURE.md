# RFC 0003 — Reference Architecture

**Status:** Proposed  
**Phase:** 1  
**Depends on:** 0000-CONSTITUTION, 0001-REPOSITORY-TOPOLOGY, 0002-UBIQUITOUS-LANGUAGE  

## Purpose

Define the Level 2 reference architecture for ARK: the microkernel, its engines, surrounding capabilities, and the flows that connect Cloud Control Plane, Edge Nodes, Field Devices, and Plugins.

## Goals

- Show how constitutional principles become a concrete system shape.
- Place every Core engine and mark what must remain outside Core.
- Establish control flow (Events) and authority flow (Evidence → State Transition).
- Provide the map that subsequent Phase 1 RFCs detail.

## Non-Goals

- IDL schemas, wire formats, or storage engines
- Plugin inventory completeness
- UI architecture
- Technology selections (brokers, databases, clouds, languages)

## Requirements

1. ARK Core SHALL be a microkernel composed only of: State Engine, Event Engine, Plugin Runtime, Synchronization Engine, Identity Interfaces, Versioning, Configuration, and Lifecycle coordination among these.
2. All cross-capability control SHALL occur through Events.
3. State progression SHALL require sufficient Evidence; user gestures alone SHALL NOT advance State.
4. The system SHALL operate Connected, Intermittently Connected, or Fully Air-Gapped without loss of local orchestration authority.
5. Plugins SHALL integrate external systems and non-core functions; none of those integrations SHALL reside in Core.
6. Current State SHALL be derived from Event history; Past States SHALL be immutable.

## Constraints

- Core knows nothing of concrete transports, persistence products, cloud vendors, enterprise products, messaging products, databases, serialization formats, or authentication providers.
- Capabilities own their data; no capability may directly mutate another’s datastore.
- Interfaces are forever; implementations are replaceable.
- Specs in `ark-specs` govern; code repositories implement.

## System Context

```
                    [ External Enterprise / OT / IT Systems ]
                     GIS | ERP | PM | SCADA | OPC-UA | MQTT | ...
                                      |
                                 [ Plugins ]
                                      |
                              (Events only)
                                      |
 +-------------------- ARK Core (microkernel) ---------------------+
 |  Identity Interfaces   Configuration   Versioning   Lifecycle   |
 |                                                                 |
 |   Event Engine  <-->  State Engine  <-->  Plugin Runtime        |
 |         ^                                                       |
 |         +------------- Synchronization Engine ------------------+
 +-------------------------------+---------------------------------+
                                 |
              store-and-forward / conflict-resolved sync
                                 |
         +-----------------------+-----------------------+
         |                       |                       |
 [Cloud Control Plane]    [Edge Node]            [Edge Node]
 (optional)               (site runtime)         (air-gapped ok)
                                 |
                          [ Field Devices ]
                       (via Plugins, not Core)
```

## Logical Components

| Component | Location | Authority |
|---|---|---|
| State Engine | Core | Accept/reject State Transitions |
| Event Engine | Core | Accept, order, persist-abstractly, dispatch Events |
| Plugin Runtime | Core | Isolate and mediate Plugins |
| Synchronization Engine | Core | Offline-tolerant sync semantics |
| Identity Interfaces | Core (abstract) | Principal attribution contracts |
| Versioning | Core | Spec/schema/artifact version discipline |
| Configuration | Core | Declarative behavior without Core growth |
| CDO | Spec + projections | Canonical Deployment representation |
| Plugins | Outside Core | Integrations and non-core capabilities |
| Digital Twin projection | Derived | Event-derived view of Deployment/Assets |

## Control and Data Flows

### Evidence-driven progression

1. Evidence is submitted (typically via Plugin or authorized principal).
2. Event Engine records EvidenceSubmitted (and later EvidenceValidated as applicable).
3. State Engine evaluates Transition rules, Evidence sufficiency, and Dependencies.
4. On success: State advances; StateAdvanced (or equivalent) is emitted; history persists.
5. On failure: transition is rejected; Current State unchanged; rejection is observable.

### Cross-capability communication

- Publishers emit Events; subscribers react.
- No service directly controls another service.
- Plugins never call into Core internals beyond approved Runtime/SDK contracts.

### Synchronization flow

- Edge Nodes progress locally using the same Core engines.
- Synchronization Engine exchanges Event batches under store-and-forward.
- Conflict Resolution yields a deterministic, replayable history.

## Deployment Topologies

| Topology | Cloud Control Plane | Edge Node | Requirement |
|---|---|---|---|
| Connected | Present | Present | Continuous or frequent sync |
| Intermittent | Sometimes reachable | Present | Local progress + catch-up sync |
| Air-gapped | Absent or unreachable | Present | Full local authority; optional sneakernet sync later |

## Interfaces (Abstract)

| Interface | Provider | Consumer | Purpose |
|---|---|---|---|
| EventPublish | Event Engine | Core engines, Plugins (via Runtime/SDK) | Append immutable Events |
| EventSubscribe | Event Engine | Core engines, Plugins | React to Events |
| TransitionEvaluate | State Engine | Authorized callers via Core | Attempt evidence-gated transition |
| PluginHost | Plugin Runtime | Plugins | Lifecycle, isolation, contract binding |
| SyncExchange | Synchronization Engine | Peers (Cloud/Edge) | Exchange Event sets |
| Identify | Identity Interfaces | All engines | Attribute actors to actions |
| ConfigResolve | Configuration | All engines | Resolve declarative settings |
| VersionNegotiate | Versioning | Sync + Runtime | Ensure compatible interpretation |

Concrete IDL for these interfaces is Phase 3.

## Examples

### Example A — Air-gapped substation Deployment

Edge Node hosts Core. Inspection Evidence arrives via an evidence Plugin from a field tablet. State Engine advances an Asset when Evidence validates. No cloud contact occurs. Months later, Synchronization Engine exports Event history to a Control Plane when a sync window exists.

### Example B — Plugin isolation failure

An ERP Plugin crashes. Plugin Runtime contains the failure. State Engine and Event Engine continue. ERP-related Evidence ingestion pauses; other Evidence paths remain available.

## Open Questions

1. Are Digital Twin projections a Core-owned read model or a Plugin capability?  
   **Working assumption:** Core guarantees Event history sufficiency for twin derivation; materializing rich twin views MAY be a Plugin or reference projection outside Core, to keep Core small.
2. Is Lifecycle a separate engine or a coordination responsibility of Core composition?  
   **Working assumption:** Lifecycle is Core composition policy (startup, shutdown, engine health), not a ninth domain engine.

## Future Extensions

- Hierarchical multi-site Deployments
- Federation between organizations
- Hardware-backed identity binding (see Security RFC)

## Related RFCs

0004 CDO · 0005 State Engine · 0006 Event Model · 0007 Plugin System · 0008 Synchronization · 0009 Identity · 0010 Versioning · 0011 Configuration · 0012 Security
