# Titan Ultimate (Flask + Groq)

Responsive chat UI with Flask backend. Optimized for mobile and desktop, deploy-ready for Vercel.

## Local Run

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Open `http://127.0.0.1:5000`.

## Environment Variables

- `GROQ_API_KEY` (required if `GROQ_API_KEYS` is empty)
- `GROQ_API_KEYS` (optional comma-separated fallback keys)
- `GROQ_MODEL` (default: `llama3-8b-8192`)
- `GROQ_TIMEOUT_SECONDS` (default: `20`)
- `MAX_MESSAGE_LENGTH` (default: `3000`)
- `ROOM_CONNECTED_USERS` (optional comma-separated online list for room panel)
- `FIREBASE_SERVICE_ACCOUNT_JSON` (optional JSON string)

## Vercel Deploy

1. Import repository into Vercel.
2. Set environment variables from `.env.example` in Project Settings.
3. Deploy.

`app.py` exports `app = Flask(__name__)`, so Vercel can detect the Flask entrypoint directly.
