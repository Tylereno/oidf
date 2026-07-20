"""Worker entrypoint — JSON-lines plugin protocol."""

from __future__ import annotations

import json
import sys

from keel_telemetry.logic import DEFAULT_RULES, telemetry_to_evidence


def main() -> None:
    rules = DEFAULT_RULES
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        op = msg.get("op")
        if op == "start":
            sys.stdout.write(json.dumps({"status": "ok"}) + "\n")
            sys.stdout.flush()
        elif op == "stop":
            sys.stdout.write(json.dumps({"status": "ok"}) + "\n")
            sys.stdout.flush()
            return
        elif op == "event":
            try:
                pubs = telemetry_to_evidence(msg["event"], rules)
                sys.stdout.write(json.dumps({"status": "ok", "publish": pubs}) + "\n")
                sys.stdout.flush()
            except Exception as exc:  # noqa: BLE001
                sys.stdout.write(json.dumps({"status": "error", "reason": str(exc)}) + "\n")
                sys.stdout.flush()
        else:
            sys.stdout.write(json.dumps({"status": "error", "reason": "unknown_op"}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
