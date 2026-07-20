# 00 — Preamble: Why OIDF Exists

**Status:** Accepted doctrine  
**Audience:** Owners, EPCs, OT/IT architects, regulators evaluating the format  
**Baseline:** `KEEL-SPEC-BASELINE-2026.07.20`

---

Critical infrastructure is being built with nineteenth-century proof habits and twenty-first-century cloud assumptions.

Schedules live in one system. Drawings live in another. Telemetry lives in a third. When an Authority Having Jurisdiction asks *what state is this asset in, and who proved it*, the industry answers with PDFs, checkboxes, and verbal assurances. That is not a process failure. It is a **format failure**.

**OIDF — the Open Infrastructure Deployment Format — exists to make deployment truth portable, attributable, and enforceable offline.**

OIDF is not a product dashboard. It is not a project-management suite. It is the contract layer: state machines, evidence types, SAT event logs, and handoff ledgers that any compliant runtime may enforce. The first such runtime is Keel. The format outlives any single implementation.

Three non-negotiables shape every document in this folder:

1. **Offline-first sovereignty.** Sites that matter will lose the uplink. Truth must advance at the edge, then sync — never wait on a SaaS round-trip to become real.
2. **Attributable evidence.** State advances only when typed Evidence exists. Machine-sourced Evidence is preferred; human inspection is labeled and never sufficient alone on the lighthouse happy path.
3. **Portable handoff.** An as-built that cannot be replayed is theater. The ledger is the artifact.

What follows is the thesis, the wedge, and the stance. Normative schemas live in [`../../core_schemas/`](../../core_schemas/). Deep RFCs live in [`../normative/`](../normative/).
