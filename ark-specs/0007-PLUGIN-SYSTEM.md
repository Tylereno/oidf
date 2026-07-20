# RFC 0007 — Plugin System

**Status:** Accepted (Specification Baseline)  
**Phase:** 1  
**Depends on:** 0000, 0002, 0003, 0006  

## Purpose

Specify the Plugin ecosystem and Plugin Runtime: how ARK extends without enlarging Core.

## Goals

- Isolate Plugins from Core and from each other.
- Event-in / Event-out integration model.
- Independent failure domains.
- Clear path: feature attempts to be a Plugin before becoming Core.

## Non-Goals

- Concrete process/container/WASM technology choice
- Complete official plugin catalog
- Marketplace economics
- UI plugin frameworks

## Requirements

1. Everything external SHALL be a Plugin (Constitution Principle 6).
2. Plugins SHALL publish and/or subscribe to Events; they SHALL NOT modify ARK Core.
3. Plugins SHALL fail independently; Plugin failure SHALL NOT corrupt Core Event history.
4. Plugins SHALL own their integration data; they SHALL NOT write to another capability’s datastore.
5. Plugin Runtime SHALL mediate lifecycle: discover, start, stop, health, contract binding.
6. A Capability Registry SHALL record what each Plugin provides to mitigate plugin explosion.
7. Official Plugins live under `ark-plugins` (packaging granularity per ADR deferred in 0001).

## Constraints

- Plugin Runtime is in Core; Plugin business logic is not.
- Runtime MUST NOT become a disguised enterprise SDK (no SAP/Primavera types in Core).
- SDK (`ark-sdk`) exposes contracts; Core MUST NOT depend on SDK packaging.

## Isolation Model

```
 +---- Plugin A ----+   +---- Plugin B ----+
 | private data     |   | private data     |
 | private deps     |   | private deps     |
 +--------^---------+   +--------^---------+
          | Events / approved host calls
 +--------v----------------------v---------+
 |           Plugin Runtime (Core)         |
 |  registry · lifecycle · mediation       |
 +------------------+----------------------+
                    |
              Event Engine
```

Minimum isolation properties:

| Property | Requirement |
|---|---|
| Fault | Crash/timeout contained |
| Data | Separate persistence authority |
| Authority | Only granted Event publish/subscribe + declared host APIs |
| Upgrade | Plugin version upgrade without Core rebuild |

## Capability Registry

Each Plugin registers:

- plugin identity + version
- capabilities provided (e.g. `evidence.validate`, `gis.reference`, `schedule.mirror`)
- event types published/consumed
- required configuration keys
- identity/authorization needs

Core and other Plugins discover capabilities via registry—not by hard-coded imports.

## Host APIs (Abstract; minimal)

| API | Purpose |
|---|---|
| RegisterCapability(desc) | Announce capability |
| Publish(event draft) | Append via Event Engine (authorized) |
| Subscribe(filter) | Receive Events |
| ReadConfig(keys) | Resolve Plugin configuration |
| ReportHealth(status) | Runtime supervision |

No host API may expose another Plugin’s datastore.

## Failure Behavior

1. Plugin panic/timeout → Runtime marks unhealthy; unsubscribes or quarantines per policy.
2. In-flight publish either commits as Event or fails closed; no partial silent Core mutation.
3. `PluginError` (or equivalent) MAY be emitted for observation.
4. State Engine continues for paths not dependent on the failed Plugin’s Evidence.

## Official Plugin Examples (Non-normative list)

`ark-gis`, `ark-primavera`, `ark-sap`, `ark-procore`, `ark-ai`, `ark-datadog`, `ark-sentry`, `ark-opcua`, `ark-mqtt`, `ark-scada`, `ark-document`, `ark-evidence`

Presence in this list does not mandate implementation in Phase 1.

## Prime Directive Test

Before adding any feature to Core, ask:

1. Can it be a Plugin?
2. Can it be Configuration?
3. Can it be data?

If yes to any, it MUST NOT enter Core without an ADR defeating this presumption.

## Interfaces (Abstract)

Covered by Host APIs above; SDK maps them for developers. IDL in Phase 3.

## Examples

### Evidence Plugin

Subscribes to `EvidenceSubmitted`, validates payload against configured rules, publishes `EvidenceValidated` or `EvidenceRejected`. Owns validation rule cache in its datastore. State Engine never imports its code.

### SCADA Plugin

Publishes `TelemetryReceived` from OT adapters. Does not advance State directly. Separate Evidence/transition path decides whether telemetry constitutes sufficient Evidence.

## Open Questions

1. In-process vs out-of-process Plugins for v1 isolation floor?  
   **Working assumption:** architecture requires failure isolation equivalent to out-of-process; implementation mechanism deferred to Level 4 with ADR.
2. May Plugins call other Plugins synchronously?  
   **Working assumption:** no; compose only via Events/capabilities registry to avoid hidden coupling.

## Future Extensions

- Signed plugin packages and capability attestations
- Resource quotas / backpressure classes

## Related RFCs

0005 State Engine · 0006 Event Model · 0009 Identity · 0011 Configuration · 0012 Security
