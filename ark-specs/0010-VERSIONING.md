# RFC 0010 — Versioning

**Status:** Accepted (Specification Baseline)  
**Phase:** 1  
**Depends on:** 0000, 0002, 0003, 0004, 0006  

## Purpose

Make versioning a first-class Core concern so Replay, Synchronization, and schema evolution remain correct across years.

## Goals

- Version specs, event payloads, CDO revisions, machines, and Plugins coherently.
- Fail closed on incompatible interpretation.
- Enable historical reproducibility.

## Non-Goals

- Choosing SemVer tooling products
- CI release automation
- Unlimited forever backward compatibility without migration

## Requirements

1. Every Event SHALL carry a `spec_version` covering envelope interpretation and payload schema identity.
2. Every CDO revision SHALL carry a content revision and a schema/spec version.
3. Synchronization SHALL negotiate protocol and schema versions before merge.
4. Replay SHALL select interpreters compatible with the Event’s recorded versions.
5. MachineDefinitions and Configuration documents SHALL be versioned.
6. Plugin contracts SHALL declare versioned capabilities.

## Constraints

- Versioning MUST NOT require Core to know product release channels of cloud vendors.
- Breaking changes require RFC/ADR; silent breaks are Specification Drift failures.

## Versioned Artifacts

| Artifact | Version fields |
|---|---|
| Event envelope | event model version |
| Event payload | type + schema version |
| CDO | schema version + revision number + content hash |
| MachineDefinition | definition version |
| SyncBatch | protocol version |
| Plugin capability | plugin version + capability version |
| Configuration document | config schema version |

## Compatibility Rules

1. **Additive optional fields** may be compatible if unknown-field policy is defined (Phase 3).
2. **Breaking changes** require new schema version; old Events still replay with old interpreter.
3. Peers that cannot interpret a required version MUST QuarantineBatch / reject append.
4. Core engines themselves have interface versions distinct from Deployment data versions.

## Interfaces (Abstract)

| Interface | Purpose |
|---|---|
| Negotiate(local, remote) → Agreement \| Incompatible | Sync handshake |
| ResolveInterpreter(artifact_type, version) | Replay/runtime binding |
| RegisterSchema(type, version, descriptor) | Schema registry port (adapter outside Core knowledge of storage) |

## Examples

Edge on event model `1.3` syncs to Control Plane on `1.4` with backward read of `1.3`. A `2.0` breaking Edge batch is quarantined until Control Plane upgrades interpreters.

## Open Questions

1. Central schema registry capability vs schemas only in `ark-specs` releases?  
   **Working assumption:** normative schemas live in `ark-specs`; runtime registry caches those artifacts locally for offline use.
2. Maximum unsupported-version retention?  
   **Deferred** to operations policy; architecture requires retention sufficient for audit obligations.

## Future Extensions

- Automated migration projections for read models (never rewrite audit Events)

## Related RFCs

0004 CDO · 0006 Event Model · 0008 Synchronization · 0007 Plugin System
