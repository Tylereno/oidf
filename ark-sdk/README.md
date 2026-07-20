# ark-sdk

Developer-facing contracts for ARK Plugins and integrators.

## Status

Phase 5 stub. Normative schemas live in `ark-specs/idl/`. This package will grow typed helpers without becoming a Core dependency (RFC 0001).

## Rules

- SDK adapts to specs; Core does not depend on SDK.
- Plugins publish/subscribe Events; they do not call State Engine internals.
- Transition intent: publish `TransitionRequested` (ADR-0001).

## Schema index

See `../ark-specs/0015-INTERFACE-DEFINITIONS.md`.
