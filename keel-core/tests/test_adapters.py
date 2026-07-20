from __future__ import annotations

from pathlib import Path

from keel_core.adapters.ed25519_signing import Ed25519SigningAdapter
from keel_core.adapters.file_event_store import FileEventStore
from keel_core.app.event_service import EventService
from keel_core.app.kernel import CoreKernel
from keel_core.adapters.memory import SystemClock


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


def test_file_event_store_survives_reopen_after_many_appends(tmp_path: Path):
    path = tmp_path / "events.jsonl"
    store = FileEventStore(path)
    for i in range(5):
        store.append_persisted(
            {
                "id": f"evt-{i}",
                "type": "TelemetryReceived",
                "payload": {"n": i},
            }
        )
    reloaded = FileEventStore(path)
    assert len(reloaded.load_all()) == 5
    assert reloaded.get("evt-4")["payload"]["n"] == 4


def test_file_event_store_skips_truncated_trailing_line(tmp_path: Path):
    """Simulate crash mid-write: good lines remain; truncated tail is ignored."""
    path = tmp_path / "events.jsonl"
    store = FileEventStore(path)
    store.append_persisted({"id": "evt-good-1", "type": "TelemetryReceived", "payload": {}})
    store.append_persisted({"id": "evt-good-2", "type": "TelemetryReceived", "payload": {}})

    # Append a truncated JSON line as if the process died mid-write.
    with path.open("a", encoding="utf-8") as f:
        f.write('{"id":"evt-partial","type":"TelemetryReceived","paylo')

    reloaded = FileEventStore(path)
    ids = {e["id"] for e in reloaded.load_all()}
    assert ids == {"evt-good-1", "evt-good-2"}
    assert reloaded.get("evt-partial") is None


def test_file_event_store_idempotent_duplicate_append(tmp_path: Path):
    path = tmp_path / "events.jsonl"
    store = FileEventStore(path)
    ev = {"id": "evt-dup", "type": "TelemetryReceived", "payload": {"x": 1}}
    store.append_persisted(ev)
    store.append_persisted(ev)
    assert len(store.load_all()) == 1
    reloaded = FileEventStore(path)
    assert len(reloaded.load_all()) == 1


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
