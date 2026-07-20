# Product naming (locked)

**Status:** Accepted  
**Date:** 2026-07-20  
**Applies to:** this repository (`Tylereno/oidf`) and all agents working the EnoTech multi-repo environment

## One-sentence map

**OIDF** is the format. **Keel** is the runtime that implements it. **VITO** is a different product (sovereign edge node) and lives in `ark-node`, not here.

## Canonical names

| Name | Layer | Meaning | Home |
|---|---|---|---|
| **OIDF** | Format / contracts | Schemas, CDO, events, machine definitions, evidence types — how deployment truth is represented and exchanged | `oidf` repo → `ark-specs/`, IDL |
| **Keel** | Runtime / product | Microkernel that enforces OIDF: state engine, evidence gates, sync, plugins | `oidf` repo → `ark-core/`, SDK, plugins, examples |
| **VITO** | Edge platform | Sovereign DDIL node (power governor, crew/agents, dashboard). Formerly an older project once called “ARK” | `ark-node` → `vito-update/` |
| **EnoTech** | Company | Bids, web, capability statements | `enotech-web`, `enotech-site` |
| **Sun-Wave** | Hardware venture | Expedition / off-grid power systems | Separate (not this repo) |
| **Sentinel** | Situational awareness | Mission monitoring — not a World Monitor clone | `Sentinel` |

## Deprecated

| Term | Rule |
|---|---|
| **ARK** / “Autonomous Resilient Kernel” | **Do not use** for new writing. Historical alias only. In this repo it meant the runtime now called **Keel** (and sometimes blurred with the format now called **OIDF**). |
| Calling this repo “VITO” | **Wrong.** VITO ≠ Keel ≠ OIDF. |
| Calling VITO “ARK” | **Wrong** on site/docs; that rename already happened for the edge product. |

## Directory names (`ark-*`)

Paths such as `ark-specs/`, `ark-core/`, Python packages `ark_core` remain **temporarily** for mechanical stability. Treat them as legacy path prefixes meaning “OIDF/Keel tree,” not as the product brand. A future rename PR may migrate paths; agents must not invent a second product called ARK because folders still say `ark-`.

## How to speak in PRs and agent prompts

- “Update the **OIDF** IDL for Evidence type X”
- “Fix **Keel** State Engine rejection path”
- “VITO dashboard change belongs in **ark-node**, not oidf”
- Never: “ARK commission demo” → say “**Keel** commissioning demo (OIDF-compliant)”

## Related

- Spec index: [`ark-specs/README.md`](./ark-specs/README.md)
- Naming RFC: [`ark-specs/0022-PRODUCT-NAMING.md`](./ark-specs/0022-PRODUCT-NAMING.md)
- Stack siblings (multi-repo env): `ark-node`, `enotech-web`, `enotech-site`, `Sentinel`, `Tylereno.github.io`
