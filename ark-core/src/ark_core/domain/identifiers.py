"""Domain identifiers — no I/O."""

from typing import NewType

PrincipalId = NewType("PrincipalId", str)
EventId = NewType("EventId", str)
DeploymentId = NewType("DeploymentId", str)
AssetId = NewType("AssetId", str)
NodeId = NewType("NodeId", str)
