from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, request


APP_VERSION = "1.0.0"
ADMIN_PASSWORD = "Kalambur01"
STORAGE_PATH = Path("keys.json")

app = Flask(__name__)
_storage_lock = Lock()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_keys() -> dict[str, dict]:
    if not STORAGE_PATH.exists():
        return {}

    with STORAGE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        return {}

    return data


def _save_keys(keys: dict[str, dict]) -> None:
    with STORAGE_PATH.open("w", encoding="utf-8") as f:
        json.dump(keys, f, ensure_ascii=False, indent=2)


@app.get("/")
def root():
    return jsonify(
        {
            "ok": True,
            "service": "fps-key-server",
            "version": APP_VERSION,
            "pulse": "/pulse",
            "time": _utc_now_iso(),
        }
    )


@app.get("/pulse")
def pulse():
    """Health-check endpoint similar to a service pulse/heartbeat."""
    return jsonify(
        {
            "ok": True,
            "status": "alive",
            "service": "fps-key-server",
            "version": APP_VERSION,
            "time": _utc_now_iso(),
        }
    )


@app.post("/add_key")
def add_key():
    payload = request.get_json(silent=True) or {}

    if payload.get("password") != ADMIN_PASSWORD:
        return jsonify({"ok": False, "error": "invalid_password"}), 403

    key = str(payload.get("key", "")).strip().upper()
    plan = payload.get("plan")

    if not key:
        return jsonify({"ok": False, "error": "missing_key"}), 400

    if plan not in (1, 2, 3):
        return jsonify({"ok": False, "error": "invalid_plan"}), 400

    with _storage_lock:
        keys = _load_keys()
        keys[key] = {
            "plan": plan,
            "used": False,
            "created_at": _utc_now_iso(),
            "used_at": None,
        }
        _save_keys(keys)

    return jsonify({"ok": True, "key": key, "plan": plan})


@app.post("/use_key")
def use_key():
    payload = request.get_json(silent=True) or {}
    key = str(payload.get("key", "")).strip().upper()

    if not key:
        return jsonify({"ok": False, "error": "missing_key"}), 400

    with _storage_lock:
        keys = _load_keys()
        record = keys.get(key)

        if record is None:
            return jsonify({"ok": False, "error": "key_not_found"}), 404

        if record.get("used"):
            return jsonify({"ok": False, "error": "key_already_used"}), 409

        record["used"] = True
        record["used_at"] = _utc_now_iso()
        _save_keys(keys)

    return jsonify({"ok": True, "plan": record.get("plan")})


@app.get("/key/<string:key>")
def key_status(key: str):
    with _storage_lock:
        keys = _load_keys()
        record = keys.get(key.upper())

    if record is None:
        return jsonify({"ok": False, "error": "key_not_found"}), 404

    return jsonify({"ok": True, "key": key.upper(), "data": record})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
