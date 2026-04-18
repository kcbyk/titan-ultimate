import json
import os
from typing import List, Optional

import firebase_admin
import requests
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, render_template, request

DEFAULT_SYSTEM_PROMPT = (
    "Sen TITAN asistansin. Cevaplarini net, kisa ve aksiyon odakli ver."
)
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("GROQ_TIMEOUT_SECONDS", "20"))
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "3000"))

app = Flask(__name__, template_folder="templates")
db: Optional[object] = None


def _read_csv_env(env_name: str) -> List[str]:
    raw_value = os.getenv(env_name, "")
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def load_groq_keys() -> List[str]:
    keys: List[str] = []
    keys.extend(_read_csv_env("GROQ_API_KEYS"))

    single_key = os.getenv("GROQ_API_KEY", "").strip()
    if single_key:
        keys.append(single_key)

    # Preserve order while removing duplicates.
    unique_keys: List[str] = []
    seen = set()
    for key in keys:
        if key not in seen:
            unique_keys.append(key)
            seen.add(key)
    return unique_keys


def load_participants() -> List[str]:
    users = _read_csv_env("ROOM_CONNECTED_USERS")
    if not users:
        return ["SEN", "TITAN"]

    unique_users: List[str] = []
    seen = set()
    for user in users:
        if user not in seen:
            unique_users.append(user)
            seen.add(user)
    return unique_users


def init_firestore_client() -> Optional[object]:
    service_account = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
    if not service_account:
        return None

    try:
        cred_data = json.loads(service_account)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(credentials.Certificate(cred_data))
        return firestore.client()
    except Exception as exc:  # pylint: disable=broad-except
        app.logger.warning("Firestore disabled: %s", exc)
        return None


GROQ_KEYS = load_groq_keys()
ROOM_PARTICIPANTS = load_participants()
db = init_firestore_client()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "keysLoaded": len(GROQ_KEYS),
            "firebaseEnabled": db is not None,
            "model": DEFAULT_MODEL,
            "participants": ROOM_PARTICIPANTS,
        }
    )


@app.post("/api/sor")
def sor():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("msg", "")).strip()

    if not message:
        return jsonify({"error": "Mesaj bos olamaz."}), 400

    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify(
            {
                "error": (
                    f"Mesaj cok uzun. En fazla {MAX_MESSAGE_LENGTH} karakter "
                    "gonderebilirsin."
                )
            }
        ), 400

    if not GROQ_KEYS:
        return jsonify({"error": "Sunucu eksik ayar: GROQ_API_KEY veya GROQ_API_KEYS."}), 503

    last_error = "Bilinmeyen hata."

    for key in GROQ_KEYS:
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": DEFAULT_MODEL,
                    "messages": [
                        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                        {"role": "user", "content": message},
                    ],
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            last_error = f"Ag hatasi: {exc}"
            continue

        if response.status_code != 200:
            detail = response.text.replace("\n", " ").strip()
            last_error = f"HTTP {response.status_code}: {detail[:160]}"
            continue

        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            last_error = f"Gecersiz cevap formati: {exc}"
            continue

        if content:
            return jsonify({"cevap": content})
        last_error = "Model bos cevap verdi."

    return jsonify({"error": "AI su anda cevap uretemiyor.", "detail": last_error}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
