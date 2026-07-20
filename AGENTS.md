# AGENTS.md

## Cursor Cloud specific instructions

### What this repository is

`oidf` is currently a **specification / documentation-only repository** — the `ark-specs` charter for the ARK ("Autonomous Resilient Kernel") platform. As of now it contains only:

- `README.md` — placeholder.
- `ark-specs/0000-CONSTITUTION.md` — the master architectural charter (the source of truth).

There is **no application code, build system, package manifest, lockfile, dependency, database, or service** in this repo. Per the constitution, the project is intentionally at "Phase 0" and implementation is deferred to later phases.

### Build / lint / test / run

There is nothing to build, lint, test, or run — no dev server, no entry point, no test suite. Do not fabricate one. The "product" at this stage is the specification document itself, which is reviewed by reading `ark-specs/0000-CONSTITUTION.md`.

The VM startup/update script is intentionally a no-op because there are no dependencies to install. If and when real code (e.g. `ark-core`, an `ark-sdk`, package manifests, or a `Dockerfile`) is added in later phases, update the SetupVmEnvironment update script and this section accordingly.

### Working conventions (from the constitution)

The constitution mandates a strict, phase-gated process: execute exactly ONE phase at a time and stop for approval before the next. Architectural changes require an ADR, and implementation work must reference an approved RFC. Keep `ark-specs` free of application code — code belongs in separate repos (`ark-core`, `ark-sdk`, `ark-plugins`, etc.) when those phases begin.
