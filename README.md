# ARK

Autonomous Resilient Kernel — offline-first deployment operating system for physical infrastructure.

## Top-Level Topology

```
ark/
├── ark-specs/          # RFCs, ADRs, IDL (source of truth)
├── ark-core/           # State engine & microkernel (production — Phase 6+)
├── ark-sdk/            # Plugin interfaces and developer SDK
├── ark-plugins/        # Official plugins
├── ark-reference/      # Phase 5 reference implementation + conformance tests
├── ark-docs/           # User and operator documentation
└── ark-examples/       # Example deployments and tutorials
```

## Quick start (reference)

```bash
pip install -e ark-reference
pytest ark-reference/tests -q
```

## Specs

- Charter: [`ark-specs/0000-CONSTITUTION.md`](./ark-specs/0000-CONSTITUTION.md)
- Topology: [`ark-specs/0001-REPOSITORY-TOPOLOGY.md`](./ark-specs/0001-REPOSITORY-TOPOLOGY.md)
- IDL: [`ark-specs/idl/`](./ark-specs/idl/)
