# RFC 0006 — Event Model

**Status:** Proposed  
**Phase:** 1  
**Depends on:** 0000, 0002, 0003  

## Purpose

Define the canonical Event model: the sole cross-capability communication and history substrate for ARK.

## Goals

- Immutable, timestamped, attributable Events.
- Deterministic ordering sufficient for replay.
- Technology-agnostic event envelope.
- Clear separation between envelope and payload contracts.

## Non-Goals

- Choosing Kafka/NATS/RabbitMQ/etc.
- Final IDL syntax (Phase 3)
- Complete closed enum of all future event types
- Exactly-once delivery product guarantees (semantics specified abstractly)

## Requirements

1. Every Event SHALL be immutable after append.
2. Every Event SHALL include: event identity, event type, timestamp, actor/provenance, subject references as applicable, schema/spec version, and payload.
3. Event history for a subject scope SHALL be orderable for Replay such that State derivation is deterministic.
4. Capabilities SHALL communicate by publishing and reacting to Events; they SHALL NOT directly control one another.
5. Events SHALL be syncable via the Synchronization Engine (0008).
6. Signed Events SHALL be supported as a Security profile (0012) without hard-wiring a crypto library into the model.

## Constraints

- Event Engine MUST NOT know concrete brokers or serialization products.
- Payload types are versioned contracts in `ark-specs`; Core routes opaque typed payloads per registry.
- No silent event mutation, compaction that destroys audit meaning, or history rewrite.

## Envelope (Conceptual)

```
Event
├── id                  # globally unique within trust domain
├── type                # e.g. EvidenceSubmitted, StateAdvanced
├── spec_version        # event model / payload schema version
├── time
│   ├── occurred_at     # domain time of fact
│   └── recorded_at     # engine append time
├── actor               # principal via Identity Interfaces
├── subject
│   ├── deployment_id?
│   ├── asset_id?
│   └── other refs?
├── causation
│   ├── caused_by_event_id?
│   └── correlation_id?
├── integrity
│   ├── payload_hash
│   └── signature?      # optional per security profile
└── payload             # typed by `type` + spec_version
```

## Ordering

1. **Primary:** per-subject sequence (logical clock / monotonic sequence allocated by Event Engine for that subject stream).
2. **Secondary:** `occurred_at` for domain interpretation; MUST NOT alone define conflict winners across partitions.
3. Sync conflict rules (0008) operate on these ordering fields deterministically.

## Illustrative Event Types

Normative initial set (names locked; payloads Phase 3):

| Type | Emitted when |
|---|---|
| DeploymentCreated | Deployment/CDO established |
| DeploymentRevised | CDO revision published |
| EvidenceSubmitted | Evidence received |
| EvidenceValidated | Evidence accepted by validator |
| EvidenceRejected | Evidence failed validation |
| TransitionRejected | State Engine rejected attempt |
| StateAdvanced | Successful State Transition |
| InspectionFailed | Domain inspection failure recorded as fact |
| PermitExpired | Permit expiry fact recorded |
| AssetCommissioned | Convenience/domain event if distinct from StateAdvanced (see Open Questions) |
| TelemetryReceived | Telemetry fact ingested (does not imply State advance) |
| MaterialDelivered | Delivery fact recorded |
| ScheduleUpdated | External schedule fact mirrored via Plugin |
| PluginError | Plugin failure surfaced for observation |
| SyncBatchCommitted | Sync acceptance boundary |

Additional types require an RFC or controlled registry extension via Configuration governance—not ad-hoc Core commits.

## Delivery Semantics (Abstract)

| Semantic | Requirement |
|---|---|
| Append durability | Once accepted by Event Engine, Event is durable for audit/replay |
| At-least-once dispatch to Plugins | Subscribers MUST be idempotent |
| Fan-out isolation | Slow/failed Plugin MUST NOT block Core append path beyond defined backpressure policy |

## Interfaces (Abstract)

| Interface | Purpose |
|---|---|
| Append(event) | Persist and assign ordering |
| Read(stream, from) | Replay/catch-up read |
| Subscribe(filter) | Register reactive consumer |
| Acknowledge(consumer, position) | Consumer cursor (plugin-facing) |

## Examples

Evidence arrives → `EvidenceSubmitted` → validator Plugin emits `EvidenceValidated` → caller requests transition → `StateAdvanced`. Each step is a distinct Event; none overwrite prior Events.

## Open Questions

1. Should domain convenience events like `AssetCommissioned` exist separately from `StateAdvanced`, or be projections only?  
   **Working assumption:** `StateAdvanced` is normative; domain aliases may be derived projections to avoid duplicate authority.
2. Multi-timestamp (`occurred_at` vs `recorded_at`) conflict in Evidence: which feeds Transition guards?  
   **Working assumption:** guards use validated Evidence content and State Engine evaluation time rules defined per machine; envelope times support audit/sync.

## Future Extensions

- Event archival tiers that preserve replay equivalence
- Cross-organization event exchange with explicit trust domains

## Related RFCs

0005 State Engine · 0007 Plugin System · 0008 Synchronization · 0009 Identity · 0010 Versioning · 0012 Security
