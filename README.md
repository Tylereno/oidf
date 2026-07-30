# OIDF (Open Integration Data Format)

The Open Integration Data Format (OIDF) provides a canonical schema and Domain-Specific Language (DSL) designed to unify and normalize fragmented data from disparate project management platforms (e.g., Jira, Asana, GitHub Issues, Trello) and real-time operational telemetry into a single, deterministic data model.

## Core Domains

- **Containers**: Organizational hierarchy (Projects, Epics, Sprints).
- **Actors**: Governance and identity (Users, Teams, Roles).
- **Lifecycle**: Workflow state transitions and performance metrics.
- **Graph**: Network topology (Dependencies, Blocks, Links).
- **Dynamic**: Extensible metadata (Tags, Custom fields).
- **Telemetry**: Operational logs and system health.

## Getting Started

### Installation

```bash
pip install -e .
```

### Registry Usage

```python
from oidf.registry import OIDFRegistry

registry = OIDFRegistry()
canonical_key = registry.get_canonical("jira", "status")
print(canonical_key)  # Output: workflow.status.current
```

### Translation

```python
from oidf.translator import OIDFTranslator

translator = OIDFTranslator()
# Maps native source data to canonical OIDF format
normalized_data = translator.translate("jira", {"status": "in-progress"})
```

## Governance

This project follows an RFC-driven governance model. See the `rfc/` directory for proposed changes.

## License

Apache-2.0
