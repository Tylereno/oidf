# RFC 0009 — Identity Interfaces

**Status:** Accepted (Specification Baseline)  
**Phase:** 1  
**Depends on:** 0000, 0002, 0003, 0012  

## Purpose

Define Core Identity Interfaces: abstract contracts for principals, attribution, and authentication-provider independence.

## Goals

- Attribute every Evidence submission, Event, and Transition attempt to a principal.
- Keep authentication providers outside Core knowledge.
- Support offline attribution.
- Leave room for hardware-backed identity later.

## Non-Goals

- Selecting OIDC, mTLS vendors, LDAP, or HSM products
- Full RBAC policy language (see Security 0012 for requirements; detailed policy RFC may follow)
- Human UX for login

## Requirements

1. Core SHALL depend only on Identity Interfaces, never on a named authentication product.
2. Every Event SHALL identify an actor principal (human, service, Plugin, or node).
3. Identity verification SHALL work in Connected, Intermittent, and Air-Gapped modes using previously established credentials/keys as applicable.
4. Plugins that authenticate external users SHALL map them into ARK principals without embedding IdP logic in Core.
5. Future hardware-backed identity SHALL be representable without breaking the interface.

## Constraints

- No Auth0/Okta/AzureAD/Keycloak types in Core.
- Identity Interfaces MUST NOT become a user directory implementation inside Core.
- Authorization decisions consume identity + policy; Identity Interfaces provide identity assertions. Policy evaluation uses the Core `Authorize` port (ADR-0007), not a Security Engine.

## Concepts

| Concept | Meaning |
|---|---|
| Principal | Stable actor identity within a trust domain |
| Credential | Secret/key/token proving principal (handled by providers/Plugins) |
| IdentityAssertion | Result of verifying a credential: principal id, attributes, validity window |
| Node Identity | Principal representing an Edge Node or Control Plane instance |
| Plugin Identity | Principal representing a Plugin instance |

## Interfaces (Abstract)

| Interface | Purpose |
|---|---|
| Authenticate(credential_ctx) → IdentityAssertion | Verify via bound provider adapter |
| Resolve(principal_id) → PrincipalProfile | Fetch non-secret profile attributes |
| BindPlugin(plugin_id) → Plugin Identity | Runtime identity for Plugin actions |
| SignAs(principal, bytes) / Verify(…) | Optional hooks for Signed Events (0012) |

Provider adapters implement Authenticate behind the interface; Core calls only the interface.

## Offline Behavior

1. Edge Nodes cache required public keys / principal grants needed for local operation.
2. New unknown principals MAY be rejected offline (fail closed) or accepted into a quarantine principal class per Configuration—default **fail closed**.
3. Sync later distributes identity directory fragments as Configuration/Evidence—not as Core IdP logic.

## Examples

Inspector authenticates via site-local credential Plugin → IdentityAssertion for `principal:inspector:42` → EvidenceSubmitted actor set → State Engine authorization checks role from policy.

## Open Questions

1. Principal ID format?  
   **Deferred to Phase 3 IDL.**

## Phase 2 Amendments

- ADR-0007 Authorize port.

## Future Extensions

- Hardware-backed keys / TPM attestation
- Cross-organization federated principals

## Related RFCs

0006 Event Model · 0007 Plugin System · 0011 Configuration · 0012 Security
