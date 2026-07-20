# Architectural Failure Modes Register

**Status:** Accepted (Red Team Pass — Phase 5→6)  
**Baseline:** `ARK-SPEC-BASELINE-2026.07.20`  
**Role:** Red Team Lead  
**Related:** Constitution Failure Modes; ADRs 0012–0016  

## Method

Attack the frozen Phase 0–5 specs as a hostile implementer and field adversary. Prefer architectural kills over implementation bugs.

Likelihood: Low / Medium / High  
Severity: Low / Medium / High / Critical  

---

## Register

| Failure Name | Likelihood | Severity | Failure Mechanism | Architectural Mitigation |
|---|---|---|---|---|
| Forged Evidence Injection | Medium | Critical | Attacker publishes `EvidenceValidated` without going through a trusted validator path, or spoofs actor_id on unsigned Events | **ADR-0012**: Evidence validation chain mandatory; only principals with `evidence.validate` may emit `EvidenceValidated`; Signed Events required for high-assurance profiles; State Engine MUST ignore unvalidated Evidence |
| Stale Evidence Replay | High | High | Old valid Evidence reused after permit/process expiry to re-open gates | **ADR-0012**: Evidence carries `valid_from`/`valid_until`; Transition evaluation rejects expired Evidence; machine may require fresh Evidence types |
| Transition Request Race | High | High | Concurrent `TransitionRequested` on same subject yields double-advance or nondeterministic rejects under parallel evaluators | **ADR-0013**: Per-subject single-flight serialization in State Engine; idempotency_key + compare-and-append on subject sequence |
| Evidence Gate Deadlock | Medium | High | Circular `AssetStateIn` dependencies (A waits B, B waits A) freeze progress with perpetual `DependencyUnsatisfied` | **ADR-0013**: MachineDefinition publish-time cycle detection; reject cyclic dependency graphs; operator-visible `MachineInvalid` config fault |
| Split-Brain Multi-Writer | Medium | Critical | Affinity misconfig or partition allows two Edges to advance same Deployment; merge produces compensations that look like commission then rollback | **ADR-0014**: Fencing token / affinity epoch in SyncBatch; non-primary writes to StateAdvanced quarantined unless epoch matches; Controllers must not treat compensation as silent success |
| Clock Drift Undermines Order | High | High | Skewed `occurred_at` reorders merge winners across nodes | **ADR-0014**: Conflict primary key prefers Event Engine `sequence` + event `id` within subject stream after sync assign; `occurred_at` is audit/domain only, not sole conflict authority (strengthen 0006/0008) |
| Revision Pin Bypass | Medium | High | Caller omits pins or evaluates against moving “latest” without recording | Already **ADR-0008**; Phase 6 port MUST require pins on result Events; IDL already requires pins on StateAdvanced/TransitionRejected — enforce in Core Port |
| Sync Key / Node Identity Compromise | Medium | Critical | Stolen node key signs malicious SyncBatches; offline Edges accept poison history | **ADR-0015**: Node key rotation + revocation list cached offline; SyncBatch verify fail-closed; quarantine + alarm Event; dual-control for root trust updates |
| Plugin Host Crash Propagation | Medium | Critical | In-process Plugin brings down Core Event append path | **ADR-0016**: Production Plugin Runtime isolation floor = separate failure domain (process/sandbox); host supervision with restart budget; Core append path MUST NOT run Plugin code on calling thread without isolation boundary |
| Plugin Memory Exhaustion | High | High | Runaway Plugin allocates until OOM kills node | **ADR-0016**: Runtime resource quotas (memory/CPU/fds) as Configuration; breach → quarantine Plugin, emit `PluginError`, Core continues |
| Plugin Privilege Escalation | Medium | Critical | Plugin publishes `StateAdvanced` or `EvidenceValidated` outside allowlist | **ADR-0016**: Publish allowlist per CapabilityDescriptor; Event Engine rejects unauthorized types from Plugin identity; never grant Plugins direct StateEngine internal ports |
| Authorization Policy Staleness Offline | Medium | High | Cached grants continue after revocation while air-gapped | **0012/0009**: Grants carry `expires_at`; deny-by-default; short TTL for high-privilege actions; renewal Evidence required |
| Specification Drift in Adapters | High | High | Phase 6 adapters reintroduce vendor types into Core modules | Baseline immutability + CI boundary lint: `ark-core` may not import adapter packages; adapters depend inward only |
| Projection Treated as Authority | Medium | High | Operators/API mutate cached Current State | **ADR-0009**: Read APIs mark projections non-authoritative; writes only via Events |
| Bootstrap Evidence Vacuum Abuse | Low | Medium | Empty-evidence create machine used to skip all gates | **ADR-0010**: Create machines are explicit Configuration under change control; Authorize still required; audit `DeploymentCreated` |

---

## Critical Findings Requiring Contract Amendments

1. **ADR-0012 — Evidence Trust Chain & Freshness** (Critical/High)
2. **ADR-0013 — Subject Single-Flight & Dependency Acyclicity** (High)
3. **ADR-0014 — Sync Fencing & Ordering Authority** (Critical/High)
4. **ADR-0015 — Node Trust Rotation & Revocation** (Critical)
5. **ADR-0016 — Plugin Isolation Floor & Publish Allowlists** (Critical/High)

These ADRs are Accepted as baseline amendments for Phase 6 entry.

## Residual Risks (Accepted for Phase 6 start)

| Risk | Why deferred |
|---|---|
| Crypto algorithm suite | Needs dedicated ADR before Signed Events impl |
| Physical supply-chain Evidence forgery | Process/Plugin domain; Core verifies signatures/types only |
| Multi-org federation trust | Out of v1 scope |

## Red Team Verdict

The Phase 0–5 architecture survives as a microkernel **if and only if** ADRs 0012–0016 are enforced in Phase 6 ports before any adapter lands. Without them, Evidence forgery, split-brain commission, and in-process Plugin collapse are credible field failures.

**Proceed to Phase 6 port scaffolding: YES (conditional on 0012–0016).**
