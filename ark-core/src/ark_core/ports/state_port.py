"""State Engine port — RFC 0005, ADR-0001/0003/0008/0012/0013."""

from __future__ import annotations

from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class StateEnginePort(Protocol):
    """Evidence-gated deterministic transitions.

    Implementations MUST:
    - accept external intent only via TransitionRequested Events (ADR-0001)
    - serialize evaluation per subject (ADR-0013 single-flight)
    - count only EvidenceValidated within freshness window (ADR-0012)
    - emit StateAdvanced or TransitionRejected with revision pins (ADR-0008)
    - support Replay rebuilding Current State projections (ADR-0009)
    - remain compatible with TS-0001–TS-0020
    """

    def ingest_event(self, event: dict[str, Any]) -> dict[str, Any]:
        """Project evidence / handle TransitionRequested; may append result Events."""
        ...

    def current_state(self, subject_id: str) -> Optional[str]:
        """Derived Current State projection (non-authoritative)."""
        ...

    def replay(self) -> dict[str, str]:
        """Rebuild subject → state map from Event history."""
        ...

    def register_machine(self, machine_definition: dict[str, Any]) -> None:
        """Load MachineDefinition; MUST reject cyclic dependencies (ADR-0013)."""
        ...

    def preview_transition(self, request_payload: dict[str, Any], actor_id: str) -> dict[str, Any]:
        """Dry-run; MUST NOT append Events."""
        ...
