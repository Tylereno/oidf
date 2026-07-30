# Contributing to OIDF

Welcome to OIDF! We are building the canonical language for project management telemetry.

## Governance Model
- **RFC Process**: Major schema changes (new domains, breaking changes) require an RFC.
- **Backwards Compatibility**: OIDF keys must never be renamed; only deprecated.
- **Standardization**: All new elements must be justified by at least two supported platforms.

## How to Submit
1. Fork the repository.
2. Add your new mapping to `schemas/`.
3. Run the validation suite: `python3 -m pytest tests/`.
4. Open a PR.
