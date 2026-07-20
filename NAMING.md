# Product naming (locked)

**Status:** Accepted  
**Date:** 2026-07-20  
**Applies to:** this repository (`Tylereno/oidf`) and all agents working the EnoTech multi-repo environment

## One-sentence map

**OIDF** is the format. **Keel** is the runtime that implements it. **VITO** is a different product (sovereign edge node) and lives in `ark-node`, not here.

## Canonical names

| Name | Layer | Meaning | Home |
|---|---|---|---|
| **OIDF** | Format / contracts | Schemas, CDO, events, machine definitions, evidence types — how deployment truth is represented and exchanged | `oidf` → `keel-specs/`, IDL |
| **Keel** | Runtime / product | Microkernel that enforces OIDF: state engine, evidence gates, sync, plugins | `oidf` → `keel-core/`, SDK, plugins, examples |
| **VITO** | Edge platform | Sovereign DDIL node (power governor, crew/agents, dashboard). Formerly an older edge project once branded “ARK” | GitHub repo `ark-node` → `vito-update/` |
| **EnoTech** | Company | Bids, web, capability statements | `enotech-web`, `enotech-site` |
| **Sun-Wave** | Hardware venture | Expedition / off-grid power systems | Separate (not this repo) |
| **Sentinel** | Situational awareness | Mission monitoring — not a World Monitor clone | `Sentinel` |

## Deprecated

| Term | Rule |
|---|---|
| **ARK** / “Autonomous Resilient Kernel” | **Do not use** for new writing in this repo. Historical brand only. Replaced by **Keel** (runtime) + **OIDF** (format). |
| Calling this repo “VITO” | **Wrong.** VITO ≠ Keel ≠ OIDF. |
| Calling VITO “ARK” or “Keel” | **Wrong.** VITO is only the edge product in `ark-node`. |

## Directory / package names

Top-level paths and Python packages use the **keel-** / **keel_** prefix:

`keel-specs`, `keel-core`, `keel-sdk`, `keel-plugins`, `keel-reference`, `keel-docs`, `keel-examples`, packages `keel_core`, `keel_sdk`, `keel_reference`, `keel_evidence`, `keel_telemetry`.

The external GitHub repository name **`ark-node`** (VITO) is unchanged — that is a different repo.

## How to speak in PRs and agent prompts

- “Update the **OIDF** IDL for Evidence type X”
- “Fix **Keel** State Engine rejection path”
- “VITO dashboard change belongs in **ark-node**, not oidf”
- Never introduce the brand **ARK** in new prose

## Related

- Spec index: [`keel-specs/README.md`](./keel-specs/README.md)
- Naming RFC: [`keel-specs/0022-PRODUCT-NAMING.md`](./keel-specs/0022-PRODUCT-NAMING.md)
- Stack siblings: `ark-node`, `enotech-web`, `enotech-site`, `Sentinel`, `Tylereno.github.io`
