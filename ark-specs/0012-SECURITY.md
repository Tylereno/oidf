# RFC 0012 — Security Architecture

**Status:** Proposed  
**Phase:** 1  
**Depends on:** 0000, 0002, 0003, 0006, 0008, 0009  

## Purpose

Define ARK’s security architecture: Zero Trust posture, immutable audit, Signed Events, authorization, and offline-safe controls.

## Goals

- Never assume continuous connectivity or trusted networks.
- Make every progression attributable and auditable.
- Support Signed Events and future hardware-backed identity.
- Enforce authorization on Evidence and Transitions.

## Non-Goals

- Selecting SIEM/SOAR vendors
- Full cryptographic primitive choices (algorithms via later ADR)
- Physical site security procedures
- Replacing enterprise IAM products (integrate via Plugins/adapters)

## Requirements

1. Zero Trust: network location SHALL NOT grant authority.
2. Audit logs SHALL be immutable and sufficient to explain every State Transition.
3. Events SHALL support signatures for integrity and attribution (Signed Events).
4. Role-based authorization SHALL gate Evidence submission, Config changes, and Transitions.
5. Security controls SHALL function air-gapped using local verification material.
6. SyncBatches SHALL be integrity-protected; failed verification → quarantine.

## Constraints

- Core MUST NOT hard-depend on a cloud IAM product.
- Security MUST NOT require phoning home.
- Encryption-at-rest/transport implementations are adapters; Core specifies need for confidentiality ports where required, not products.

## Threat-Oriented Controls

| Risk | Control |
|---|---|
| Spoofed Evidence | AuthN + AuthZ + Signed Evidence/Events |
| History tampering | Append-only Events + hashes + optional signatures |
| Plugin compromise | Isolation + least-privilege publish rights + quarantine |
| Sync injection | Batch integrity + version negotiate + auth between nodes |
| Offline privilege escalation | Cached grants with expiry; fail closed on unknown principals |
| Silent State advance | Evidence requirements + Transition authorization |

## Authorization Model (Initial)

- Principals have roles (data).
- Roles grant permissions on actions: `evidence.submit`, `evidence.validate`, `transition.request`, `config.revise`, `sync.import`, `plugin.admin`.
- State Engine and Event Engine enforce checks before accepting consequential operations.
- Enterprise role sources sync inward via Plugins into Configuration policy data (0009/0011).

## Signed Events

1. Producer computes payload hash; signs with principal/node key.
2. Verifiers validate signature before treating Event as authoritative under high-security profiles.
3. Profile may be required for air-gap Deployments and optional for low-risk labs—policy as Configuration.

## Immutable Audit

- Event history is the audit log.
- Compaction that removes audit meaning is forbidden.
- Derived indexes allowed; they are not authoritative.

## Interfaces (Abstract)

| Interface | Purpose |
|---|---|
| Authorize(principal, action, resource) → Allow\|Deny | Policy gate |
| SignEvent(event) / VerifyEvent(event) | Integrity |
| VerifyBatch(batch) | Sync integrity |
| AuditRead(filter) | Audit query port (read-only projection) |

## Examples

Air-gapped Edge rejects `transition.request` from an expired cached grant. Inspector renews locally via offline credential ceremony Plugin; new grant Evidence recorded; subsequent Transition proceeds with Signed Events.

## Open Questions

1. Algorithm suite (e.g. signature schemes) — **ADR required before implementation.**
2. Is Deny-by-default absolute for all actions in v1?  
   **Working assumption:** yes for transition/config/sync import; read-only local projections may be broader per policy.

## Future Extensions

- Hardware-backed identity and measured boot attestation for Edge Nodes
- Confidentiality classifications for Evidence payloads

## Related RFCs

0005 State Engine · 0006 Event Model · 0007 Plugin System · 0008 Synchronization · 0009 Identity · 0011 Configuration
