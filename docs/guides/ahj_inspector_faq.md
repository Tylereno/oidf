# AHJ inspector FAQ

**Audience:** Authority Having Jurisdiction (AHJ) inspectors and owner reps evaluating OIDF ledgers.  
**Not legal advice.** Lab-oriented framing.

## What is an OIDF ledger?

A structured, append-oriented record of commissioning state and SAT outcomes — who/what asserted a fact, when, and which evidence type validated a transition. See `core_schemas/handoff_ledger.json`.

## Why should we accept it?

Because it is **replayable**. Unlike a PDF packet, a compliant ledger can show the sequence of states and the evidence that authorized each advance.

## Does OIDF replace NEC / NFPA compliance?

No. Architecture packs list **safety gate checklists** that map to code concerns; OIDF records whether those gates passed. Code authority remains with the AHJ.

## What if the site was offline?

OIDF assumes edge-local progress with later sync. Inspectors should ask for the **export** covering the inspection window, not a live cloud dashboard.

## Who implements this?

**Keel** (or another OIDF-compliant runtime). This repository only defines the format.
