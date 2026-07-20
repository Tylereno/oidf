# ADR-0017 — Signed Events Cryptography: Ed25519

**Status:** Accepted  
**Date:** 2026-07-20  
**Related RFCs:** 0006, 0012, ADR-0015; Failure Modes: Forged Evidence, Sync Key Compromise  

## Context

Security requires Signed Events and node authenticity without selecting a cloud KMS. Air-gapped Edges must verify offline.

## Decision

1. **Signature scheme:** Ed25519 (pure EdDSA).
2. **Payload binding:** signature covers `payload_hash` where hash is SHA-256 over canonical JSON UTF-8 bytes of the `payload` object (sorted keys, no insignificant whitespace).
3. **Envelope fields:** existing `payload_hash` + `signature` (base64url, no padding).
4. **Key material:** adapters/Plugins hold private keys; Core verifies via IdentityPort / SigningPort — Core does not embed a cloud KMS.
5. High-assurance profile MAY require signatures on Evidence and Transition result Events.

## Alternatives

- HMAC-only (weaker non-repudiation).
- RSA / ECDSA P-256 (larger keys / more moving parts for v1).

## Tradeoffs

Ed25519 is widely available and offline-friendly; algorithm agility later via Versioning if needed.

## Consequences

`SigningPort` added; file/memory key adapters allowed; tests cover sign/verify round-trip.
