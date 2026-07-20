from __future__ import annotations

from pathlib import Path

from ark_core.adapters.ed25519_signing import Ed25519SigningAdapter
from ark_core.adapters.file_event_store import FileEventStore
from ark_core.app.event_service import EventService
from ark_core.app.kernel import CoreKernel
from ark_core.adapters.memory import SystemClock


def test_file_event_store_roundtrip(tmp_path: Path):
    path = tmp_path / "events.jsonl"
    store = FileEventStore(path)
    clock = SystemClock()
    svc = EventService(clock, store=store)
    ev = {
        "id": "evt-persist-1",
        "type": "TelemetryReceived",
        "spec_version": "1.0.0",
        "occurred_at": "2026-07-20T00:00:00Z",
        "recorded_at": "2026-07-20T00:00:00Z",
        "actor_id": "P1",
        "payload": {"ok": True},
    }
    svc.append(ev)
    # reload from disk
    store2 = FileEventStore(path)
    svc2 = EventService(clock, store=store2)
    assert svc2.get("evt-persist-1") is not None
    assert svc2.get("evt-persist-1")["payload"]["ok"] is True


def test_ed25519_sign_verify_on_append():
    signing = Ed25519SigningAdapter()
    signing.generate("P1")
    k = CoreKernel(signing=signing, require_signatures=True)
    ev = {
        "id": "evt-signed-1",
        "type": "TelemetryReceived",
        "spec_version": "1.0.0",
        "occurred_at": "2026-07-20T00:00:00Z",
        "actor_id": "P1",
        "payload": {"n": 1},
    }
    stored = k.events.append(ev)
    assert "signature" in stored
    assert "payload_hash" in stored
    assert signing.verify("P1", stored["payload_hash"], stored["signature"])
