# Example: Air-gapped Asset Commission

Teaching walkthrough aligned with Phase 6 Core semantics (Principle 4 + ADR-0012).

**Runnable companion:** `python ark-core/examples/commission_gate_demo.py`

## Scenario

- Deployment `DEP-BESS-01` on Edge Node `edge-yard-01`
- Asset `SWGR-A1` (switchgear), machine `asset.switchgear.commission.v1`
- Gate: `Installed → Commissioned` requires validated `TorqueVerified` Evidence
- No Cloud Control Plane available (air-gapped)

## Steps

1. **Bind** the asset to the machine on the Edge Node (Configuration / CDO revision already loaded).
2. **Request transition** without evidence → observe `TransitionRejected` with `MissingEvidence`. State remains `Installed`.
3. **Submit** field claim as `EvidenceSubmitted` → still insufficient. Submissions alone never open gates.
4. **Validate** evidence as `EvidenceValidated` from an authorized validator principal (e.g. calibrated torque log review).
5. **Request the same transition** again → observe `StateAdvanced` with revision pins (`cdo_revision`, `config_revision`, `machine_definition_version`).
6. **Later**, when a sync window exists, export a `SyncBatch` for the control plane. Local commission already happened offline.

## What this teaches

- Clicks and status fields are not Evidence.
- Validated Evidence enables; the State Engine transitions.
- Machine and Evidence rules are Configuration/data — not Core code.
- Offline progression does not wait for cloud status sync.

## Non-claims

This example does not demonstrate Signed Events, durable Postgres storage, or OT plugins. Those are deferred implementation work; the gate logic itself is what the demo proves today.
