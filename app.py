import os, requests, base64, traceback
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- 🔐 TITAN-X ZIRHLI CEPHANELİK ---
ENCRYPTED_KEYS = [
    "Z3NrX2dTQ1dTcUUwblFTZTlmOVVMa3pEV0dyeWIzRllnQUFjNHFuQTVYc1dUaE83dE52V1psRnY=",
    "Z3NrXzNiY0pLc2FOZGJwa09JOVdMVEdXZ3liM0ZZeEt5cUJhc1FpSFl6MDNGWGhTc1R0WVF3",
    "Z3NrX3lXQlVzUmNrYXVRcmMzZHlLblgyV0dyeWIzRllfSUZ6R2xzNGloa3ZWSnZ2b1dibk12bHA=",
    "Z3NrX1VwQlZhbzBCUUN3YVRpOHFxaHlLV0dyeWIzRllzb1l5U3RPZDNqU2hpbGRyZ2FrZWtENT0=",
    "Z3NrX3c1SmNEWkF0SFpWQnFubk1FTzVyV0dyeWIzRllVYnpRTW5GY0lJY3NNUGJTMlZuT2RkVzk=",
    "Z3NrX25NZDN1dU85VzdNZW9ySWZGTVhzV0dyeWIzRllDaXM3WEEyaUR2YVZ5OWZUTXVtQU43Qk8=",
    "Z3NrX2wzZlZBWURoV3VhTUY1WWF3R1dMV0dyeWIzRllPNUh5bzE4VmwwNGplRk1tWVU0QWM0Qlo=",
    "Z3NrX3hIZjZETmF3ZXZGcldoUUllWURjV0dyeWIzRllVOWlIRXlDQzBGRm1BVGU1bnFZeFUxQlM=",
    "Z3NrX010ODNsc2c2U3F0Rm9VVVlvcDhXZ3liM0ZZcTZZWG1zcnNyUXhhdVBieFpVNEFoQmVJ",
    "Z3NrX2Jld1czR3ZJeW9uZUhxYk5Nd3hUV0dyeWIzRllZVUdVME9YWVVQeWx0U1YxVFc3YVhIT2k="
]
GROQ_KEYS = [base64.b64decode(k).decode('utf-8') for k in ENCRYPTED_KEYS]

# --- 🔥 FIREBASE ANTI-CRASH KALKANI ---
db = None
sistem_mesaji = "TÜM SİSTEMLER AKTİF VE KUSURSUZ."

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    if not firebase_admin._apps:
        cred_json = {
          "type": "service_account",
          "project_id": "senkl-25cc8",
          "private_key_id": "4ef6b0fa9c3e4eb09fc482a65b503fcc0172311d",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDdsfIK0ZVH7pb2\nggAKCjQxqZuPURPkEPoLzh2fXpnvrsvHkN0e4r/hPqOx66F3xhaxsNwECRVz4h7o\n6RLQMbvfrLFTRBP6MmemNO2wfmvPaNsDCFnr+8T1ALQ4K58ExCEqORQADrMGSaQe\n4Rj5KFZ7elRX23BaXopJwgHi/81RzpT5oSuMpsRZUVvNcy0fa4baPGmPaA63JmLZ\nyxrQ+6/nxE1o/Q1AOuXPNwbxXYPXLQJZFyEE35t9QZoeDUgIhogKKuGmTNA1ONVe\no6oaUkXDAEMUGreizqn8sDKYo2Q8FHf6k1ThFLYar+4NBlqK/UYtqTUiLhuA3W01\nuImaHzKJAgMBAAECggEAEOL9DNXqCRCjbyN33Uvprd69eq0yVqz0XvHUT89k6lzm\nKM1gCno7I20iCutn4Te1gtN17tjCSZFvyU33oOQo62C8IRuOagBs5LwjXs5CaAoU\npKZ+Mvt6hS8Iiz7HXhWScSTn4Rk9ib0SQ0fiHxhzffRTeF2+sSOCZRviCOhzO0fc\nszTjCiMT2dULQzlZbFOmNOvuPBAebEekhuLEKb5PE+YKaeEZJRltr9TQD9pbxHOr\nPyMf22rM9TX9B2sIg8JpwdbI68EId43oMycxU/8WACOIJqQCKjnFZnoTaPQjIinv\nEBK14sF7GZb60XLX43yzOtJpS2VLyuQ3z6XjwitGAQKBgQD978z+lQly+XtSPzAc\nu37bzokd/phCRtwnap8cmoM1uA/Pwn8eJHewv3zFsGxWfEbFtEk7JYFhQ7Plhz7R\nV/DaVqTe2Mg9ZTxn0B4KCgGdRU+uRmH975A7sL3PSfcgdmsq/fpFVhicaToCR5Ml\nxNxFV7tYIFNu4ic1SkCPJ/Ae5wKBgQDffxStBG3U0JxXFJbto0ENEVWYSLDm4TWt\nj55MVyoTglB5jUlEH7uuBcDTENFm2huV743zE1WXwz+kT9Q17mIdEqzYAYUtcvD0\nEQPBIYZMoh++8td0DBFSYvKzj+1JMUyFFsNr+wRqWzM7v9OMPoJMwfKTRgdvEmdP\nhDOzd/olDwKBgQDs2Wkjn1ED60yqBwPSGNOXI0njLx9G2h7nqNwlarytMzOUPb4h\nGDSHJ+Ox4/74n8vHBYQ0ZaQKW4KEuKPP0K12iNAYhqwmD7HKxmPuSyz8SrSqQT2P\nA45NDmnL2RpmLe2BWQjA+S/VW5ReofHOjZJCHzU/Wk9Xohqd6tbSb5bYywKBgQCF\nfllyMqgLqoMHfHPeA1oynPz8VcbcUP6H6bXKsXGfb4Hz6JEvkKjAfA09xNjezz4U\n455s50qDuIrF8Sy2/ek6plH5P4c1q2cC0Trl28lk8p11p4VLen3KMPH4kOpRgpHL\nGNqnH6r2f/ztHloUda3MfTgQAY8lJ9/vXe6nru0JvwKBgG2h2MK62LAw05Rs8vq7\n4J9Y5CbQQXfv52pJzDWZLsGp78mpiGCY+uS1sICDOtUkBPotFiU2UX10d4wL5HGP\nmgfDEouf5KGyT6oftzsOPGJf/n0so8vhKgdu46bjaNolvtSx58cFH1Emxi41aPdD\nvIeWRWHyVvq9rZkZtsjor6+9\n-----END PRIVATE KEY-----\n",
          "client_email": "firebase-adminsdk-fbsvc@senkl-25cc8.iam.gserviceaccount.com",
          "client_id": "115314493289391907128",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40senkl-25cc8.iam.gserviceaccount.com",
          "universe_domain": "googleapis.com"
        }
        cred = credentials.Certificate(cred_json)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    db = None
    sistem_mesaji = f"FIREBASE BAĞLANTI HATASI: {str(e)}"

# --- 🧠 ZEKÂ MOTORU ---
def zeka_motoru(prompt):
    for key in GROQ_KEYS:
        try:
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Sen S.E.N.O.L TITAN-X'sin. Şenol'un otonom şirket asistanısın."}, {"role": "user", "content": prompt}]},
                timeout=12
            )
            if res.status_code == 200: return res.json()['choices'][0]['message']['content']
        except: continue
    return "⚠️ API limitleri doldu!"

@app.route('/')
def ana_sayfa():
    # Vercel dosya bulamama hatasını kökten çözdük, arayüz burada gömülü.
    return render_template_string(ARAYUZ_KODU, durum=sistem_mesaji)

@app.route('/api/sor', methods=['POST'])
def sor():
    mesaj = request.json.get('msg')
    cevap = zeka_motoru(mesaj)
    return jsonify({"cevap": cevap})

# --- 🎨 ARAYÜZ (HTML/CSS) ---
ARAYUZ_KODU = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITAN-X OMEGA MERKEZİ</title>
    <style>
        body { background-color: #070a13; color: #00ffcc; font-family: monospace; margin: 0; padding: 0; height: 100vh; display: flex; flex-direction: column; }
        .header { background: #03050a; padding: 15px; border-bottom: 2px solid #00ffcc; text-align: center; }
        .header h1 { margin: 0; font-size: 20px; text-shadow: 0 0 10px #00ffcc; }
        .status { font-size: 11px; color: {% if 'HATA' in durum %}#ff0000{% else %}#0f0{% endif %}; margin-top: 5px; }
        #chat { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 15px; }
        .msg { padding: 12px; border-radius: 8px; max-width: 85%; font-size: 14px; word-wrap: break-word; }
        .user { align-self: flex-end; background: #141f33; border: 1px solid #2a3d5e; color: #8bb4f7; }
        .ai { align-self: flex-start; background: #061513; border: 1px solid #00ffcc; color: #e0ffff; }
        .isim { font-weight: bold; font-size: 11px; margin-bottom: 5px; display: block; }
        .user .isim { color: #58a6ff; }
        .ai .isim { color: #00ffcc; }
        .panel { background: #03050a; padding: 15px; display: flex; gap: 10px; border-top: 1px solid #1a2333; }
        input { flex: 1; background: #0b111c; border: 1px solid #00ffcc; color: #00ffcc; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 14px; outline: none; }
        button { background: #00ffcc; color: #000; border: none; padding: 0 20px; border-radius: 6px; font-weight: bold; font-family: monospace; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <h1>TITAN-X OMEGA</h1>
        <div class="status">{{ durum }}</div>
    </div>
    <div id="chat">
        <div class="msg ai"><span class="isim">SİSTEM</span>Kalkanlar devrede. Emirlerinizi bekliyorum Patron.</div>
    </div>
    <div class="panel">
        <input type="text" id="komut" placeholder="Emret..." onkeypress="if(event.key === 'Enter') gonder()">
        <button onclick="gonder()">GÖNDER</button>
    </div>

    <script>
        async function gonder() {
            let input = document.getElementById('komut');
            let metin = input.value.trim();
            if (!metin) return;
            input.value = '';

            let chat = document.getElementById('chat');
            chat.innerHTML += `<div class="msg user"><span class="isim">CEO ŞENOL</span>${metin}</div>`;
            chat.scrollTop = chat.scrollHeight;

            let id = "b_" + Date.now();
            chat.innerHTML += `<div class="msg ai" id="${id}"><span class="isim">TITAN-X</span>İşleniyor...</div>`;
            chat.scrollTop = chat.scrollHeight;

            try {
                let istek = await fetch('/api/sor', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ msg: metin })
                });
                let yanit = await istek.json();
                
                document.getElementById(id).remove();
                chat.innerHTML += `<div class="msg ai"><span class="isim">TITAN-X</span>${yanit.cevap}</div>`;
            } catch (e) {
                document.getElementById(id).remove();
                chat.innerHTML += `<div class="msg ai" style="border-color: red; color: red;"><span class="isim">HATA</span>Sistem yanıt vermiyor.</div>`;
            }
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run()
        
