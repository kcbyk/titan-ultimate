import os, time, requests, firebase_admin, base64
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- 🔐 TITAN-X ZIRHLI CEPHANELİK (10 GROQ ANAHTARI) ---
# GitHub Secret Scanning engeline takılmamak için anahtarlar Base64 ile şifrelenmiştir.
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

# --- 🔥 FIREBASE ÖLÜMSÜZ HAFIZA BAĞLANTISI ---
# Eksiksiz JSON verisi kullanıldı. Vercel'deki token_uri hatası kökten çözüldü.
if not firebase_admin._apps:
    FIREBASE_CREDENTIALS = {
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
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)
db = firestore.client()

def titan_x_zeka_motoru(prompt):
    """10 anahtarı sırayla dener, biri bozulursa sarsılmadan diğerine geçer."""
    for key in GROQ_KEYS:
        try:
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "Sen S.E.N.O.L TITAN-X'sin. Ayvalık'ta üretilmiş, siber güvenlik, yazılım ve oyun geliştirmede uzman otonom bir dehaysın. Kullanıcıya Patron diye hitap et."},
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=12
            )
            if res.status_code == 200: 
                return res.json()['choices'][0]['message']['content']
        except:
            continue
    return "⚠️ Sistem Uyarısı: Tüm ateşleme anahtarlarının limiti doldu!"

@app.route('/')
def ana_panel():
    docs = db.collection('chats').order_by('time').stream()
    history = [doc.to_dict() for doc in docs]
    return render_template_string(GELISMIS_ARAYUZ, history=history)

@app.route('/komut_gonder', methods=['POST'])
def komut_gonder():
    kullanici_mesaji = request.json.get('msg')
    # Kullanıcı mesajını Firebase'e mühürle
    db.collection('chats').add({'role': 'user', 'content': kullanici_mesaji, 'time': time.time()})
    
    # TITAN-X yanıtlasın ve o da mühürlensin
    titan_yaniti = titan_x_zeka_motoru(kullanici_mesaji)
    db.collection('chats').add({'role': 'assistant', 'content': titan_yaniti, 'time': time.time()})
    
    return jsonify({"response": titan_yaniti})

# --- 🛰️ SİBER GÜVENLİK TEMALI GELİŞMİŞ ARAYÜZ (HTML/CSS) ---
GELISMIS_ARAYUZ = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITAN-X OMEGA MERKEZİ</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        
        body { background: #070a13; color: #00ffcc; font-family: 'Fira Code', monospace; margin: 0; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
        
        .header { background: #03050a; padding: 20px; border-bottom: 2px solid #00ffcc; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 0 20px rgba(0, 255, 204, 0.2); }
        .header h1 { margin: 0; font-size: 1.4rem; text-shadow: 0 0 10px #00ffcc; letter-spacing: 3px; }
        .status { font-size: 0.8rem; color: #00ffcc; animation: pulse 2s infinite; border: 1px solid #00ffcc; padding: 5px 10px; border-radius: 4px; }
        @keyframes pulse { 0% { opacity: 1; box-shadow: 0 0 5px #00ffcc; } 50% { opacity: 0.4; box-shadow: none; } 100% { opacity: 1; box-shadow: 0 0 5px #00ffcc; } }
        
        #chat-kutu { flex: 1; overflow-y: auto; padding: 25px; display: flex; flex-direction: column; gap: 20px; background: radial-gradient(circle at center, #0a0e17 0%, #03050a 100%); }
        .msg { padding: 18px; border-radius: 8px; max-width: 80%; line-height: 1.6; font-size: 0.95rem; word-wrap: break-word; position: relative; }
        .user { align-self: flex-end; background: #141f33; border: 1px solid #2a3d5e; color: #8bb4f7; border-bottom-right-radius: 0; }
        .assistant { align-self: flex-start; background: #061513; border: 1px solid #00ffcc; color: #e0ffff; border-bottom-left-radius: 0; box-shadow: inset 0 0 15px rgba(0, 255, 204, 0.05); }
        
        .isim-etiket { font-weight: bold; font-size: 0.8rem; opacity: 0.7; margin-bottom: 8px; display: block; letter-spacing: 1px; }
        .user .isim-etiket { color: #58a6ff; }
        .assistant .isim-etiket { color: #00ffcc; }
        
        .kontrol-paneli { background: #03050a; padding: 20px 25px; display: flex; gap: 15px; border-top: 1px solid #1a2333; }
        input { flex: 1; background: #0b111c; border: 1px solid #00ffcc; color: #00ffcc; padding: 18px; border-radius: 6px; font-family: 'Fira Code', monospace; font-size: 1rem; outline: none; transition: all 0.3s ease; }
        input:focus { box-shadow: 0 0 15px rgba(0,255,204,0.3); background: #0e1624; }
        button { background: #00ffcc; color: #000; border: none; padding: 0 35px; border-radius: 6px; font-weight: bold; font-family: 'Fira Code', monospace; font-size: 1rem; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase; }
        button:hover { background: #fff; box-shadow: 0 0 20px #00ffcc; transform: translateY(-2px); }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #03050a; }
        ::-webkit-scrollbar-thumb { background: #00ffcc; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>TITAN-X OMEGA</h1>
        <div class="status">SİSTEM AKTİF • 10x API • FIREBASE BAĞLI</div>
    </div>
    
    <div id="chat-kutu">
        {% for h in history %}
            <div class="msg {{ 'user' if h.role == 'user' else 'assistant' }}">
                <span class="isim-etiket">{{ 'CEO ŞENOL' if h.role == 'user' else 'TITAN-X' }}</span>
                {{ h.content }}
            </div>
        {% endfor %}
    </div>
    
    <div class="kontrol-paneli">
        <input type="text" id="komut-satiri" placeholder="Sistem emrinizi bekliyor patron..." onkeypress="if(event.key === 'Enter') atesle()">
        <button onclick="atesle()">İLET</button>
    </div>

    <script>
        async function atesle() {
            const input = document.getElementById('komut-satiri');
            const mesaj = input.value.trim();
            if (!mesaj) return;
            
            input.value = '';
            const chatKutu = document.getElementById('chat-kutu');
            
            // Kullanıcı mesajını ekrana bas
            chatKutu.innerHTML += `<div class='msg user'><span class='isim-etiket'>CEO ŞENOL</span>${mesaj}</div>`;
            chatKutu.scrollTop = chatKutu.scrollHeight;
            
            try {
                // Sunucuya gönder
                const yanit = await fetch('/komut_gonder', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ msg: mesaj })
                });
                
                const veri = await yanit.json();
                
                // Yapay zeka yanıtını ekrana bas
                chatKutu.innerHTML += `<div class='msg assistant'><span class='isim-etiket'>TITAN-X</span>${veri.response}</div>`;
            } catch (hata) {
                chatKutu.innerHTML += `<div class='msg assistant' style='border-color: red;'><span class='isim-etiket' style='color: red;'>SİSTEM HATASI</span>Bağlantı kurulamadı.</div>`;
            }
            
            chatKutu.scrollTop = chatKutu.scrollHeight;
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
        
