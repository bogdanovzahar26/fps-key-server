from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# База ключей (можно потом расширить)
KEYS = {
    "ULT1-AAAA-1111": {"plan": 1, "used": False},
    "ULT2-BBBB-2222": {"plan": 2, "used": False},
    "ULT3-CCCC-3333": {"plan": 3, "used": False}
}

@app.route("/")
def home():
    return "FPS Key Server работает"

@app.route("/check", methods=["POST"])
def check_key():
    data = request.get_json()
    key = data.get("key")

    if key not in KEYS:
        return jsonify({"ok": False, "msg": "Неверный ключ"})

    if KEYS[key]["used"]:
        return jsonify({"ok": False, "msg": "Ключ уже использован"})

    KEYS[key]["used"] = True
    return jsonify({"ok": True, "plan": KEYS[key]["plan"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
