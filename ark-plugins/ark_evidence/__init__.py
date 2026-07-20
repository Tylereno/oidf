"""ark-evidence package."""

DESCRIPTOR = {
    "plugin_id": "ark-evidence",
    "plugin_version": "0.1.0",
    "capabilities": ["evidence.validate"],
    "publishes": ["EvidenceValidated", "EvidenceRejected"],
    "subscribes": ["EvidenceSubmitted"],
    "config_keys": ["allowed_evidence_types"],
}
