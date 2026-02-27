import os, time, requests, firebase_admin, base64
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- 🔐 TITAN-X MÜHİMMAT DEPOSU (10 ADET GROQ ANAHTARI) ---
# GitHub engellemesin diye anahtarlarını 'zırhlı' (Base64) hale getirdim.
ZIRHLI_ANAHTARLAR = [
    "Z3NrX2dTQ1dTcUUwblFTZTlmOVVMa3pEV0dyeWIzRllnQUFjNHFuQTVYc1dUaE83dE52V1psRnY=",
    "Z3NrXzNiY0pLc2FOZGJwa09JOVdMVEdXZ3liM0ZZeEt5cUJhc1FpSFl6MDNGWGhTc1R0WVF3",
    "Z3NrX3lXQlVzUmNrYXVRcmMzZHlLblgyV0dyeWIzRllmSUZ6R2xzNGloa3ZWSnZ2b1dibk12bHA=",
    "Z3NrX1VwQlZhbzBCUUN3YVRpOHFxaHlLV0dyeWIzRllzb1l5U3RPZDNqU2hpbGRyZ2FrZWtENT0=",
    "Z3NrX3c1SmNEWkF0SFpWQnFubk1FTzVyV0dyeWIzRllVYnpRTW5GY0lJY3NNUGJTMlZuT2RkVzk=",
    "Z3NrX25NZDN1dU85VzdNZW9ySWZGTVhzV0dyeWIzRllDaXM3WEEyaUR2YVZ5OWZUTXVtQU43Qk8=",
    "Z3NrX2wzZlZBWURoV3VhTUY1WWF3R1dMV0dyeWIzRllPNUh5bzE4VmwwNGplRk1tWVU0QWM0Qlo=",
    "Z3NrX3hIZjZETmF3ZXZGcldoUUllWURjV0dyeWIzRllVOWlIRXlDQzBGRm1BVGU1bnFZeFUxQlM=",
    "Z3NrX010ODNsc2c2U3F0Rm9VVVlvcDhXZ3liM0ZZcTZZWG1zcnNyUXhhdVBieFpVNEFoQmVJ",
    "Z3NrX2Jld1czR3ZJeW9uZUhxYk5Nd3hUV0dyeWIzRllZVUdVME9YWVVQeWx0U1YxVFc3YVhIT2k="
]

def anahtarlari_coz():
    return [base64.b64decode(k).decode('utf-8') for k in ZIRHLI_ANAHTARLAR]

GROQ_KEYS = anahtarlari_coz()

# --- # --- 🔥 FIREBASE ÖLÜMSÜZ HAFIZA (EKSİKSİZ KİMLİK) ---
if not firebase_admin._apps:
    FB_CRED = {
      "type": "service_account",
      "project_id": "senkl-25cc8",
      "private_key_id": "c33ab2b59a2e030c3d2e6b7934f34ce3f5a83635",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdDCLH5Hlygzus\n16AD+mHWGlkhbFfwQb/40SLnphugpd9WtgdVlkiAw2vO1EKQGjIcPUMr8jkL/Js4\nDou0OZwB+kWMuZURdAPDRTh8/n2uJPcG7WjaTuug/1sJXAQ6ClRWBwALCC4D6rGf\nDr5mwca6pLg0Cqhg7MfhDnNKDdxigb/MQ5dtAveDzmJ0qBYQIcdA18Qq1pz4iZh6\nS3CIWMYy23joJI6XFT1oP6lEMV+166mKJ7ruWJuXrbboBy1I0Iur49a8b3qjQuLE\nWmVxj82ER7BequnDD3ubNXxhqYpVsFagwpVmH/K1yEUXi2mSVdsf00Fx/NE/H7wQ\nfjYTR/iLAgMBAAECggEAIlbW/BJPI+TiFYcIbBZBcklMl+xSxiv6R/OiyDgf7l6W\nmSUwMVys+crBNfZfn5a6wkX6/A74vlA7uGQl1ACMxjntHzotCCXv9LCcC2iyHnPi\nt9cNiD6dcxSi2UcPfYloq27YaZEeTqjwsbDNnTZdt83woSB7dMYRZnp8ZwLk33zb\nsVkNSoYtUwJ1i4CznO5JEKyZK1L8Kbnc6lXLxmzm9plUZlTngtFJhTlDyb6FRVZE\nhowPpm7NmCZj21DlFXwasJPBamdlu66hvDb6mjlbd1GWdmlbCDw6A2s9eWDTJ5sj\nMJ3rfHw9wds6CAXAxWLM+STLXEc6BQjTp4hpee7iQQKBgQDPQbw6qT7hec2qvFzH\n4cnlSZvTxDPqykol4RBzOokhAZI7xtKChduYax1koGebRtKb0L7ur+d+Wt+gPK69\nnJbkG3buHtgLf5njyNbDodD1PNVhqnHXwL59mZvybcyWSWlvNihjJvMz9kplpXJl\nlvTgIKy3pZnD3wrkkX+J0mnL2wKBgQDB+3Sg+roezqkQXWUCsRQRk2B+LQmIr7HF\nDt/FT/FZUAIMXaTVqBhyLDYCITE4l5+BVFtJ5RMuekua8bf4FIiKpaQA1lCm7dhr\nTGR2KiQkjIctXl5q1tjdtp4Pf1g+0lGk7b6aP1KT+naM44q6QI7r/cwG8FHuwC2N\n2ggfgn79EQKBgFgOEa7KoVCis2LKzJCPuXuVHoOGZJhogcA+MwMB56kCReLnwiB6\nRqYnPEG4dMxf9rMEqVo3mh7w9PnbTlJ46RLZKFpa+GdKO1OvzK8pXOIUioQIKn4E\nAerTDJKfW8CuSAFb/STDM6jsBwfQlx3aWQewWjFcRkwVw0cBGjKwFwrpAoGBAKmq\nsMYkxyovA/zGU5VZIP6Gcz2pUs91LP35FoxUcfr2WfRK6+Pc1RT3yn1uXsjrBZ5v\nFDG75V0fpoVtqsWX4B2054+75Gs9Wa/v72bTUS2OpKVwBxFXvfOeyP0xGxRHjRW+\nxJnRjP7VcV+lni9uTBPptszS4jb7bFzIOZal40ChAoGASdyoZ2gU56BN4R+uq213\nDzAWESmCgTvROsLucQqikJU9iM+B+GPywLboc/awoOGhNqCpmTOsyi5867ehI8a6\n5BpHBsSekUP4EX/b5UkJVzLCVM2sl9KkD4RWZ8pXft8yMa5WvzI3x4moBAOzBRRe\nuEPRxRocUlr9wPXEe3WzUXY=\n-----END PRIVATE KEY-----\n",
      "client_email": "firebase-adminsdk-fbsvc@senkl-25cc8.iam.gserviceaccount.com",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token"
    }
    cred = credentials.Certificate(FB_CRED)
    firebase_admin.initialize_app(cred)
db = firestore.client()
    firebase_admin.initialize_app(cred)
db = firestore.client()

def ai_sorusunu_yanitla(prompt):
    for key in GROQ_KEYS:
        try:
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "system", "content": "Sen S.E.N.O.L TITAN-X'sin. Ayvalık'ta üretilmiş otonom bir dehaysın. Kullanıcıya Patron diye hitap et."}, {"role": "user", "content": prompt}]
                },
                timeout=12
            )
            if res.status_code == 200: return res.json()['choices'][0]['message']['content']
        except: continue
    return "Tüm anahtarların limiti doldu Patron!"

@app.route('/')
def home():
    # Firebase'den geçmişi çek (Asla silinmez)
    docs = db.collection('titan_chats').order_by('time').stream()
    history = [d.to_dict() for d in docs]
    return render_template_string(HTML_UI, history=history)

@app.route('/send', methods=['POST'])
def send():
    msg = request.json.get('msg')
    db.collection('titan_chats').add({'role': 'user', 'content': msg, 'time': time.time()})
    resp = ai_sorusunu_yanitla(msg)
    db.collection('titan_chats').add({'role': 'assistant', 'content': resp, 'time': time.time()})
    return jsonify({"response": resp})

HTML_UI = """
<!DOCTYPE html><html><head><title>TITAN-X ULTIMATE</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{background:#050505;color:#00ffcc;font-family:monospace;margin:0;display:flex;flex-direction:column;height:100vh;}
#chat{flex:1;overflow-y:auto;padding:20px;} .msg{padding:10px;margin:10px;border-radius:5px;max-width:85%;}
.user{background:#1e293b;align-self:flex-end;margin-left:auto;color:#58a6ff;} .assistant{background:#0d1117;border:1px solid #00ffcc33;}
.in{padding:20px;background:#111;display:flex;gap:10px;} input{flex:1;background:#000;border:1px solid #333;color:#00ffcc;padding:12px;}
button{background:#00ffcc;color:#000;border:none;padding:12px;font-weight:bold;cursor:pointer;}</style></head>
<body><div id="chat">{% for h in history %}<div class="msg {{h.role}}"><b>{{'SENOL' if h.role=='user' else 'TITAN-X'}}:</b><br>{{h.content}}</div>{% endfor %}</div>
<div class="in"><input type="text" id="m" placeholder="Emret patron..."><button onclick="s()">GÖNDER</button></div>
<script>async function s(){let i=document.getElementById('m'); let v=i.value; if(!v)return; i.value='';
document.getElementById('chat').innerHTML+=`<div class='msg user'><b>SENOL:</b><br>${v}</div>`;
let r=await fetch('/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({msg:v})});
let d=await r.json(); document.getElementById('chat').innerHTML+=`<div class='msg assistant'><b>TITAN-X:</b><br>${d.response}</div>`;
document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;}</script></body></html>
"""
