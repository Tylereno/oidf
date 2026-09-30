# Product naming (locked)

**Status:** Accepted  
**Date:** 2026-07-20  
**Applies to:** this repository (`Tylereno/oidf`) and agents in the EnoTech multi-repo environment

## One-sentence map

**OIDF** is the format. **Keel** is the runtime that implements it (separate repo). **VITO** is a different product (sovereign edge node) and lives in `ark-node`.

## Canonical names

| Name | Layer | Meaning | Home |
|---|---|---|---|
| **OIDF** | Format / contracts | Schemas, CDO, events, machines, evidence types, SAT ledgers — how deployment truth is represented and exchanged | **`Tylereno/oidf`** → `docs/`, `core_schemas/`, `architectures/` |
| **Keel** | Runtime / product | Microkernel that enforces OIDF: state engine, evidence gates, sync, plugins | **`Tylereno/keel`** → `keel-core/`, SDK, plugins, examples |
| **VITO** | Edge platform | Sovereign DDIL node (power governor, crew/agents, dashboard) | GitHub `ark-node` → `vito-update/` |
| **Sunwave** | Hardware division | Expedition / off-grid power, MRP platforms | GitHub `sunwave` |
| **EnoTech** | Company | Umbrella company for the products above | `enotech-site` → enotech.systems |
| **Sentinel** | Situational awareness | Mission monitoring — open feeds only | `Sentinel` |

## Deprecated

| Term | Rule |
|---|---|
| **ARK** | Do not use in new prose. Historical brand only. |
| Calling this repo “Keel” or “VITO” | **Wrong.** This repo is **OIDF only**. |
| “Keel lives in oidf” | **Obsolete.** Keel is `Tylereno/keel`. |

## Path notes

- Former folder `keel-specs/` is now `docs/normative/` (RFCs/ADRs) + `core_schemas/idl/` + `core_schemas/evidence-catalog/`.
- Python packages `keel_*` live in **`Tylereno/keel`**, not here.

## How to speak in PRs

- “Update the **OIDF** IDL for Evidence type X”
- “Fix **Keel** State Engine rejection path” → PR against **`keel`**, not this repo
- “VITO dashboard change belongs in **ark-node**”
