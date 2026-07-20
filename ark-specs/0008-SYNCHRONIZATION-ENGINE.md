# RFC 0008 — Synchronization Engine & Edge Architecture

**Status:** Proposed  
**Phase:** 1  
**Depends on:** 0000, 0002, 0003, 0006, 0010  

## Purpose

Specify offline-tolerant Synchronization between Cloud Control Plane, Edge Nodes, and authorized peers, including store-and-forward, conflict resolution, replay, and versioning interaction.

## Goals

- Full local orchestration without continuous connectivity.
- Deterministic conflict resolution.
- Eventual consistency without corrupting audit history.
- Transport-agnostic sync semantics.

## Non-Goals

- Choosing network protocols, VPNs, or physical sneakernet media
- Global real-time consensus (e.g. requiring Paxos across sites for every transition)
- Field Device drivers (Plugins)

## Requirements

1. Edge Nodes SHALL run Core engines locally and progress Deployments offline.
2. Synchronization Engine SHALL support store-and-forward of Events (and required CDO revisions).
3. Sync SHALL be eventually consistent and replayable.
4. Conflict Resolution SHALL be deterministic given the same inputs.
5. Sync SHALL negotiate versions (0010); incompatible peers SHALL fail closed with explicit error.
6. Air-gapped operation SHALL remain fully functional for local authority.

## Constraints

- Synchronization Engine MUST NOT know Kafka/HTTP/USB/etc.; transports are adapters.
- Sync MUST NOT rewrite Past States or delete audit Events.
- Cloud Control Plane is optional; it is not the source of truth while disconnected Edges progress.

## Nodes and Roles

| Role | Description |
|---|---|
| Edge Node | Site runtime with local Core; primary offline authority for its Deployments |
| Cloud Control Plane | Optional aggregator/coordinator when reachable |
| Sync Peer | Any authorized node exchanging SyncBatches |

## Sync Unit

```
SyncBatch
├── batch_id
├── sender_node_id
├── protocol_version
├── event_range / event set
├── cdo_revisions[] (referenced)
├── vector/summary clock
└── integrity (hash/signature)
```

## Store-and-Forward

1. Local Append to Event Engine succeeds independently of peer reachability.
2. Outbound queue retains unsynced Events until acknowledged by peer policy.
3. Inbound batches validate integrity, version, authorization, then merge via Conflict Resolution.

## Conflict Resolution (Normative Principles)

When two histories diverge:

1. Per-subject streams are merged using Event identity uniqueness + per-subject sequence rules.
2. If two Events share identity → treat as identical (idempotent).
3. If concurrent Events differ on the same subject without total order:
   - Apply deterministic total order key: `(subject_id, occurred_at, actor_id, event_id)` as tie-break set (exact tuple finalized in Phase 3 IDL).
4. State is re-derived after merge via Replay; if a previously accepted local transition becomes invalid under merged history, emit a compensating observation Event and mark divergence for operator workflow—**never silently drop history**.
5. CDO revision conflicts resolve by revision number + content hash; divergent content at same revision number is a hard fault.

**Working assumption:** prefer preserve-all-events + deterministic order over last-writer-wins deleting facts.

## Replay

- Nodes MUST be able to rebuild Current State from Event history after sync merge.
- SyncBatchCommitted marks an accepted merge boundary for observability.

## Edge ↔ Field Devices

- Field Devices connect through Plugins (OPC-UA, MQTT, SCADA, etc.).
- Synchronization Engine does not speak device protocols.

## Interfaces (Abstract)

| Interface | Purpose |
|---|---|
| ExportBatch(since) | Produce SyncBatch |
| ImportBatch(batch) | Validate + merge |
| SyncStatus(peer) | Cursor/health |
| QuarantineBatch(batch, reason) | Fail closed on integrity/version errors |

## Examples

### Intermittent link

Edge advances 40 Transitions offline. On connect, ExportBatch sends Events; Control Plane ImportBatch merges; both Replay to identical subject States for shared Deployments.

### Divergent Evidence order

Two Edges accept different Evidence order for same Asset while partitioned. Merge sorts deterministically; State Engine Replay yields one Current State; operators inspect TransitionRejected/compensation Events if plan constraints break.

## Open Questions

1. Deployment affinity: can two Edges concurrently advance the same Asset by design?  
   **Working assumption:** v1 assigns primary write affinity per Deployment to one Edge; others are read/forward unless explicitly authorized multi-writer mode (future).
2. Sneakernet batch format identical to online SyncBatch?  
   **Working assumption:** yes—same SyncBatch abstraction.

## Future Extensions

- Multi-writer CRDTs for selected projections (not for audit Events)
- Hierarchical site hubs

## Related RFCs

0004 CDO · 0005 State Engine · 0006 Event Model · 0010 Versioning · 0012 Security
