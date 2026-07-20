from keel_reference.core.authorize import AuthorizePort
from keel_reference.core.events import EventEngine
from keel_reference.core.state import StateEngine
from keel_reference.core.sync import SyncEngine


def build_kernel(
    grants: list | None = None,
    node_id: str = "edge-a",
) -> tuple[EventEngine, AuthorizePort, StateEngine, SyncEngine]:
    events = EventEngine()
    auth = AuthorizePort(grants=grants or [])
    state = StateEngine(events=events, authorize=auth)
    sync = SyncEngine(events=events, local_node_id=node_id)
    return events, auth, state, sync
