# 06 — Attestation and Data Portability

**Status:** Accepted doctrine  
**Related:** ADR-0017 (Ed25519 Signed Events), handoff ledger schema, IDL event envelopes

---

## Cryptographic attestation (honest scope)

OIDF’s security posture for high-assurance profiles centers on **Signed Events** that can be verified without a cloud KMS:

- **Scheme:** Ed25519 (ADR-0017)  
- **Binding:** signature over `payload_hash` (SHA-256 of canonical JSON payload)  
- **Verification:** offline at the edge via identity / signing ports in a compliant runtime  
- **Profile:** high-assurance MAY require signatures on Evidence and transition-result events; lab paths may omit until regulated pilots demand them

### What we claim

Events can be **integrity-checked and attributable to a key** under the high-assurance profile. That supports non-repudiation of *what was asserted* in the log.

### What we do not claim

- OIDF is not a PKI product, not a hardware security module vendor, and not “blockchain for batteries.”  
- A signature does not prove physics. It proves the envelope was produced by a holder of a key. Machine Evidence still has to mean something in the catalog (voltage in band, insulation OK, etc.).  
- Do not market Signed Events as a substitute for AHJ inspection.

Attestation without Evidence types is theater with better math. Evidence types without integrity are forgeable theater. OIDF requires both in the high-assurance path.

## Data portability

Deployment truth that cannot leave a vendor silo is not infrastructure — it is lock-in.

OIDF mandates **open, versioned, machine-readable artifacts**:

| Artifact | Portability role |
|---|---|
| JSON Schema IDL (`core_schemas/idl/`) | Validate events and machines anywhere |
| Evidence catalogs (JSON) | Exchange typed meanings across runtimes |
| `handoff_ledger.json` | Owner / AHJ as-built independent of UI |
| `sat_event_log.json` | Gate outcomes independent of chat or email |
| Specification baseline id | Pin contract generations across repos |

A compliant runtime (Keel today) must be able to export these artifacts. A second implementation must be able to validate them against the same schemas. **The format is the product; implementations are replaceable** (constitution).

## Canonical state vocabulary

Front-door equipment path (`equipment_state.yaml`):

`Procured → Delivered → Installed → ReadyForCommission → Commissioned → Energized`

Architecture packs specialize Evidence. They do not invent private state languages for the same physics.

## Stance

If you cannot export a ledger, verify a signature offline, and validate against published schemas, you do not have an open format. You have a captive application. OIDF exists to prevent that outcome for commissioning truth.
