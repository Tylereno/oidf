# 05 — AHJ FAQ

**Not legal advice.**

---

### What is an OIDF ledger?

A structured, append-oriented record of commissioning state and SAT outcomes: who/what asserted a fact, when, and which Evidence unlocked a transition. Schema: `core_schemas/handoff_ledger.json`.

### Why should we accept it?

Because it is **replayable**. Unlike a PDF packet alone, a compliant ledger shows the sequence of states and the Evidence that authorized each advance.

### Does OIDF replace NEC / NFPA / utility rules?

**No.** Architecture packs list safety-gate checklists that map to code *concerns*. OIDF records whether those gates passed. Code and tariff authority remain with the AHJ and utility.

### What if the site was offline?

Expected. Ask for the **export** covering the inspection window. Do not require a live cloud session as the record of truth.

### Is this cryptocurrency / blockchain?

**No.** High-assurance profiles may use Ed25519 signatures on events for integrity and attribution (ADR-0017). That is ordinary public-key signing for offline verification — not a token, chain, or speculative asset.

### Can human inspection alone commission the asset?

On the lighthouse paths: **no.** `InspectionPass` is explicitly human and optional dual-control. Happy-path transitions require machine Evidence types from the catalog.

### Who implements OIDF?

Any compliant runtime. EnoTech’s reference runtime is **Keel** (separate repository). This repository defines the format only.

### What if the ledger says pass but I see a hazard?

Fail the inspection. OIDF does not override your eyes, instruments, or adopted code. The ledger is evidence of what the *commissioning system* recorded — not a veto of your authority.

### How do I know the Evidence types mean what the contractor claims?

Demand the **evidence catalog** version pinned for the project (e.g. `bess-commissioning` / `solar-inverter-commissioning`) and the machine definition. Types are named and described there. Spot-check against field instruments.
