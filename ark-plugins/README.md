# ark-plugins

Official Plugins home.

## Status

Topology reserved. No official Plugins shipped in Phase 5.

## Rules

- Event in / Event out
- Isolated failure domains
- Capability registry descriptors MUST validate against `idl/plugin/capability_descriptor.json`

## Example descriptor (non-implemented)

```json
{
  "plugin_id": "ark-evidence",
  "plugin_version": "0.0.0",
  "capabilities": ["evidence.validate"],
  "publishes": ["EvidenceValidated", "EvidenceRejected"],
  "subscribes": ["EvidenceSubmitted"],
  "config_keys": ["ruleset_revision"]
}
```
