# Example: Air-gapped Asset Commission

Normative walkthrough using Phase 5 reference semantics.

1. Load CDO revision for Deployment `DEP-1` with Asset `A1`.
2. On Edge Node, append `EvidenceSubmitted` + `EvidenceValidated` for `InspectionPass`.
3. Publish `TransitionRequested` (`Installed` → `Commissioned`) with idempotency key.
4. Observe `StateAdvanced` with revision pins — no Cloud Control Plane required.
5. Later, export `SyncBatch` when a sync window exists.

Machine and Evidence rules are Configuration/data, not Core code.
