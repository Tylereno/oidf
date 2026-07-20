# Keel / OIDF — operator quickstart

**OIDF** is the format. **Keel** is the runtime.  
Read [`../NAMING.md`](../NAMING.md) before changing names.

## What you get

Keel advances physical assets only when validated **Evidence** satisfies OIDF state machines. The first lab wedge is **BESS commissioning** (RFC 0021).

## Install (lab)

Python ≥ 3.11. From the `oidf` repo root:

```bash
pip install -e 'keel-core[dev]' -e keel-sdk -e keel-reference
```

Lighthouse plugins under `keel-plugins/` (`keel_evidence`, `keel_telemetry`) are subprocess modules loaded by the example — not separate pip packages.
## Run tests

```bash
PYTHONPATH=keel-plugins pytest keel-core/tests keel-reference/tests -q
```

(`keel-plugins` must be on `PYTHONPATH` so lighthouse tests can import `keel_telemetry` / `keel_evidence`.)

## Run BESS lighthouse (end-to-end)

```bash
python keel-examples/bess-lighthouse/run_e2e.py /tmp/keel-bess-lighthouse
```

Details: [`LIGHTHOUSE-OPERATOR.md`](./LIGHTHOUSE-OPERATOR.md).

## Where truth lives

| Concern | Location |
|---|---|
| OIDF contracts (RFCs, IDL, evidence catalog) | `keel-specs/` |
| Keel runtime | `keel-core/` |
| Plugin host contracts | `keel-sdk/` |
| Operator docs (this tree) | `keel-docs/` |
| VITO edge dashboard / crew | **`ark-node`** (not this repo) |

## Honest limits

- Lab / lighthouse path works; fleet SaaS, Postgres/NATS brokers, and OEM cert programs are **not** shipped.
- Signed events use Ed25519 adapters in-tree — do not market as “cryptographic attestation product” beyond what the adapters actually do.
- VITO ≠ Keel ≠ OIDF.
