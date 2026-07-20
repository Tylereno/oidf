# 0002 — Ubiquitous Language Glossary

**Status:** Locked (Phase 2 amendments via ADR-0006)  
**Phase:** 0.5  
**Depends on:** 0000-CONSTITUTION, 0001-REPOSITORY-TOPOLOGY  
**Authority:** Locked. All subsequent RFCs MUST use these definitions. Contradictions require an ADR amending this glossary.

## Purpose

Lock the meaning of ARK’s core terms before architecture specifications are written.

This document is a dictionary, not a feature RFC. It defines vocabulary. It does not define APIs, schemas, storage, or protocols.

## Goals

- One meaning per term.
- Remove ambiguity between physical-world language and platform language.
- Provide the shared language for Level 2+ specifications.

## Non-Goals

- State catalogs or transition tables
- Evidence type registries
- Plugin catalogs
- IDL field definitions
- Synonyms for marketing or UI copy

## How to Read

- **MUST / MUST NOT** bind future specifications.
- **Assumption** marks a definition required for clarity that the Constitution implies but does not spell out.
- **Rejected meaning** records a common interpretation that ARK explicitly does not use.

---

## Core Terms (Locked Targets)

### Deployment

**Definition:**  
A Deployment is the root managed unit of work in ARK: the orchestration of bringing a defined set of Assets from planned condition to commissioned (or otherwise terminal) condition under evidence-driven state progression.

**MUST:**
- Be representable as a state machine.
- Own a lifecycle distinct from any single Asset.
- Be historically reproducible from events.

**MUST NOT:**
- Mean a software release, CI/CD pipeline, or cloud resource provisioning job.
- Mean a project-management “project,” schedule, or work breakdown structure.

**Rejected meanings:** Procore project; Primavera project; git deployment; Kubernetes Deployment object.

**Assumption:** A Deployment is the primary aggregate that the Canonical Deployment Object describes. Exact CDO fields are deferred.

### Asset

**Definition:**  
An Asset is a distinct managed entity within a Deployment whose condition is tracked by exactly one current State at any time.

**Includes (examples, not a closed set):** microreactor, substation, battery system, feeder segment, data-hall, crane, generator, or other infrastructure element under orchestration.

**MUST:**
- Exist in one—and only one—State at a time.
- Belong to exactly one Deployment at any time (ADR-0006). Transfer is a modeled transition sequence, not shared mutable ownership.
- Advance only through deterministic, evidence-validated transitions.

**MUST NOT:**
- Mean a digital file, document, or media object (those may be Evidence or artifacts).
- Mean a financial asset or accounting entity.

**Assumption:** Assets may form hierarchies (parent/child) without violating single-state-per-asset. Hierarchical state machines are permitted later; vocabulary does not require them yet.

### Evidence

**Definition:**  
Evidence is an immutable, attributable record that asserts a fact relevant to a State transition.

**MUST:**
- Be submitted before a dependent transition may proceed.
- Be validatable against rules associated with the intended transition.
- Be retained for audit and replay.

**MUST NOT:**
- Be a mere UI button click, approval emoji, or undocumented verbal claim.
- By itself equal a State transition (Evidence enables; the State Engine transitions).

**Related terms:** EvidenceSubmitted, EvidenceValidated (event names are illustrative until the Event Model RFC).

**Assumption:** Evidence has a type, payload, provenance (who/what produced it), and timestamp. Schema deferred.

### State

**Definition:**  
A State is a named, discrete condition in a deterministic finite state machine for a specific Deployment or Asset.

**MUST:**
- Be mutually exclusive with all other States of the same machine instance.
- Change only through a State Transition.
- Be derivable by replaying events (current State is derived; past States are immutable history).

**MUST NOT:**
- Mean a vague status string without machine semantics.
- Mean infrastructure “desired state” in the Terraform/Kubernetes sense unless an RFC later maps that concept explicitly.

**Distinctions:**
- **Past State:** immutable historical condition.
- **Current State:** derived projection of the event history.
- **Future State:** planned condition; not yet actualized; not treated as current.

### Plugin

**Definition:**  
A Plugin is an isolated capability that extends ARK by integrating an external system or providing a non-core function exclusively through published contracts and Events.

**MUST:**
- Subscribe to and/or publish Events.
- Be able to fail independently of ARK Core.
- Live outside ARK Core (typically under `ark-plugins` or an equivalent external plugin).

**MUST NOT:**
- Modify ARK Core.
- Bypass the Event model to command another capability’s internals.
- Directly mutate another capability’s datastore.

**Rejected meanings:** dynamically loaded Core module that shares Core’s process authority without isolation; “plugin” as a UI widget only.

---

## Platform Terms

### ARK (Autonomous Resilient Kernel)

**Definition:**  
The platform: an offline-first deployment operating system for physical infrastructure, centered on deterministic state machines, event sourcing, evidence-driven transitions, and digital twins.

### ARK Core

**Definition:**  
The microkernel. It contains only: State Engine, Event Engine, Plugin Runtime, Synchronization Engine, Identity Interfaces, Versioning, and Configuration.

**MUST NOT** know transport protocols, persistence engines, cloud vendors, enterprise products, messaging implementations, database implementations, serialization formats, or authentication providers.

### Capability

**Definition:**  
A Capability is a bounded unit of platform function that owns its data and reacts to Events. Core engines and Plugins are both capabilities in the data-ownership sense; only Plugins are externalized integrations.

**MUST:** Own its persistence.  
**MUST NOT:** Directly modify another capability’s database.

### Canonical Deployment Object (CDO)

**Definition:**  
The technology-agnostic specification of a Deployment’s authoritative structured representation—Assets, planned structure, and related orchestration data—independent of any storage or transport implementation.

**Assumption:** CDO is defined by IDL in later phases. This glossary only names the concept.

### Digital Twin

**Definition:**  
The living, event-derived representation of a Deployment and its Assets as known to ARK—current State, history, and planned Future State—used for orchestration, not as a replacement for CAD, GIS, or simulation engines.

### Orchestration

**Definition:**  
Coordination of progression across Deployments and Assets by validating Evidence, applying State Transitions, and exchanging Events with Plugins and external systems.

**MUST NOT:** Mean performing engineering calculations, PLC control, SCADA replacement, or ERP functions.

---

## Execution Terms

### State Machine

**Definition:**  
A deterministic finite state machine governing allowable States and State Transitions for a Deployment or Asset.

### State Transition

**Definition:**  
An atomic, deterministic change from one State to exactly one successor State, permitted only when required Evidence and Dependencies are satisfied.

**MUST:** Validate evidence; validate dependencies; generate Events; persist history; reject invalid attempts; support replay; support rollback where applicable.

### Dependency (Transition Dependency)

**Definition:**  
A declared prerequisite—typically Evidence sufficiency and/or peer Asset/Deployment State conditions—that must hold before a State Transition is legal.

### Event

**Definition:**  
An immutable, timestamped fact record that something occurred in the system. Services and Plugins communicate by publishing and reacting to Events; they do not directly control one another.

**MUST:** Carry a timestamp and be ordered for reproducibility.  
**Assumption:** Events are the sole cross-capability control channel.

### Event Sourcing (ARK sense)

**Definition:**  
The practice of treating Events as the append-only source of truth from which Current State is derived and history is replayed.

### Replay

**Definition:**  
Reprocessing recorded Events to reconstruct historical or Current State without changing Past States.

### Rollback

**Definition:**  
A controlled, auditable transition path that returns a machine to a prior allowable State when the State Machine permits it—not silent history rewriting.

**MUST NOT:** Mean deleting Events or mutating Past States.

### Invalid Transition

**Definition:**  
Any attempted State Transition that fails Evidence, Dependency, or machine-rule validation and MUST be rejected without changing Current State.

---

## Topology & Runtime Terms

### Cloud Control Plane

**Definition:**  
The optional connected coordination plane for ARK. Presence is not required for local correctness.

### Edge Node

**Definition:**  
An ARK runtime location at or near the physical site that can operate Connected, Intermittently Connected, or Fully Air-Gapped.

### Field Device

**Definition:**  
A device or system at the physical edge that produces telemetry, Evidence, or actuation signals consumed via Plugins—not part of ARK Core.

### Synchronization

**Definition:**  
Exchange of Events and derived projections between Cloud Control Plane, Edge Nodes, and authorized peers under store-and-forward, conflict resolution, versioning, replay, and eventual consistency rules.

### Store-and-Forward

**Definition:**  
The requirement that Events and Evidence accepted while disconnected are retained and propagated when connectivity returns, without loss of local progression authority.

### Conflict Resolution

**Definition:**  
Deterministic rules for reconciling concurrent Event histories after partitioned operation. Exact algorithm deferred; the term denotes the requirement that reconciliation be defined and replayable.

### Offline-First

**Definition:**  
Design posture where full orchestration capability exists without continuous connectivity. Cloud is optional.

### Connected / Intermittently Connected / Fully Air-Gapped

**Definitions:**
- **Connected:** reliable ongoing sync possible.
- **Intermittently Connected:** sync windows are partial or unreliable; local progress continues.
- **Fully Air-Gapped:** no external network path; local operation remains complete.

### Plugin Runtime

**Definition:**  
The Core engine that loads, isolates, and mediates Plugins according to approved contracts—without embedding Plugin business logic in Core.

### State Engine

**Definition:**  
The Core engine that evaluates Transition rules, Evidence, and Dependencies, and applies or rejects State Transitions.

### Event Engine

**Definition:**  
The Core engine responsible for accepting, ordering, persisting, and dispatching Events inside Core’s abstract event model (not a specific broker product).

### Synchronization Engine

**Definition:**  
The Core engine responsible for offline-tolerant Synchronization semantics, independent of concrete transport.

### Identity Interface

**Definition:**  
A Core-facing abstract contract for principal identity and attribution. Concrete authentication providers are Plugins or replaceable implementations outside Core knowledge.

### Versioning

**Definition:**  
First-class tracking of specification, schema, and artifact versions so replay and Synchronization remain correct across time.

### Configuration

**Definition:**  
Declarative, data-borne settings that change behavior without enlarging Core. Prefer configuration over Core code.

### Interface

**Definition:**  
A stable, technology-agnostic contract. Interfaces are forever; implementations are replaceable.

### Implementation

**Definition:**  
A replaceable realization of an Interface. Never the source of architectural truth.

---

## Security & Governance Terms

### Zero Trust

**Definition:**  
No network location or continuous session implies authority. Every action is authenticated and authorized in context, including offline contexts via previously established credentials and signed artifacts as specified later.

### Signed Event

**Definition:**  
An Event whose integrity and attribution are cryptographically verifiable per future Security RFCs.

### Audit Log

**Definition:**  
The immutable, ordered record of Events and State Transitions sufficient to explain every decision historically.

### Authorization

**Definition:**  
Rule-based permission to submit Evidence, invoke transitions, or administer capabilities. Role-based authorization is required; detailed model deferred.

### RFC

**Definition:**  
A normative specification artifact in `ark-specs` governing architecture or interfaces.

### ADR (Architecture Decision Record)

**Definition:**  
A record of a significant architectural decision, including context, decision, alternatives, tradeoffs, consequences, status, and related RFCs.

### Specification Drift

**Definition:**  
Divergence between approved specs and implementations or between RFCs. Treated as a failure mode requiring governance, not improvisation.

---

## Explicit Non-ARK Terms (Rejected as Platform Meanings)

| Term in industry | ARK stance |
|---|---|
| Project (PM software) | Not a Deployment |
| Workflow button / human click | Not Evidence |
| Desired state (IaC) | Not State unless mapped by a future RFC |
| Microservice calling another’s DB | Forbidden; violates Capability ownership |
| Core “integration module” for SAP/etc. | Forbidden; must be a Plugin |

---

## Open Questions

1. **Evidence authority:** Who may declare Evidence types—Core config, a dedicated evidence Plugin, or Deployment-level config?  
   **Deferred** to Evidence/Plugin RFCs. Vocabulary only requires that Evidence be typed, attributable, and immutable.

2. **Deployment vs CDO identity:** Is the Deployment ID identical to the CDO ID?  
   **Locked working assumption (unchanged):** yes, one identifier names both the aggregate and its canonical object.

## Future Extensions

- Domain vocabulary packs (nuclear, grid, data center) as additive glossaries that MUST NOT redefine core terms.
- Event name registry (separate RFC).
- State name registries per Asset class (separate RFCs).

## Architectural Scorecard (Phase 0.5)

| Quality | Score | Notes |
|---|---|---|
| Modularity | 9 | Terms map cleanly to Core vs Plugin vs Deployment |
| Coupling | 9 | Definitions avoid technology coupling |
| Cohesion | 9 | Single meaning per term |
| Replaceability | 9 | Interface/Implementation split preserved |
| Testability | 8 | Terms support deterministic replay language |
| Offline capability | 9 | Offline terms first-class |
| Security | 8 | Zero Trust / Signed Event named without over-specifying |
| Observability | 8 | Audit/Event language supports later observability |
| Extensibility | 9 | Domain packs allowed without redefining core |
| Documentation | 9 | Glossary is the documentation backbone |
| Cognitive Load | 8 | Breadth is intentional; core five terms remain primary |

No score below 8. Glossary is ready to lock pending review.
