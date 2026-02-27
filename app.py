import requests, base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 🔐 TITAN-X ZIRHLI CEPHANELİK (10 GROQ ANAHTARI) ---
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

def titan_x_zeka_motoru(prompt):
    for key in GROQ_KEYS:
        try:
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Sen S.E.N.O.L TITAN-X'sin. Siber güvenlik ve yazılım dehasısın. Kullanıcıya Patron diye hitap et."}, {"role": "user", "content": prompt}]},
                timeout=12
            )
            if res.status_code == 200: return res.json()['choices'][0]['message']['content']
        except: continue
    return "⚠️ Sistem Uyarısı: API limitleri doldu!"

@app.route('/')
def ana_panel():
    # Güvenli, çökmez saf HTML arayüzü
    return BASIT_AMA_GUCLU_ARAYUZ

@app.route('/komut_gonder', methods=['POST'])
def komut_gonder():
    kullanici_mesaji = request.json.get('msg')
    titan_yaniti = titan_x_zeka_motoru(kullanici_mesaji)
    return jsonify({"response": titan_yaniti})

# --- KURŞUN GEÇİRMEZ ARAYÜZ (Mobil Uyumlu) ---
BASIT_AMA_GUCLU_ARAYUZ = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITAN-X KONTROL PANELİ</title>
    <style>
        body { background-color: #050505; color: #00ffcc; font-family: monospace; padding: 15px; margin: 0; }
        .kutu { border: 2px solid #00ffcc; padding: 10px; margin-bottom: 20px; text-align: center; box-shadow: 0 0 10px #00ffcc; }
        #chat { height: 60vh; overflow-y: scroll; border: 1px solid #333; padding: 15px; margin-bottom: 15px; background: #0a0a0a; border-radius: 5px; }
        .msg { margin-bottom: 15px; padding: 10px; border-radius: 5px; line-height: 1.4; word-wrap: break-word; }
        .user { background: #1a2639; color: #66b3ff; border-left: 4px solid #66b3ff; }
        .titan { background: #0d1a18; color: #00ffcc; border-left: 4px solid #00ffcc; }
        .isim { font-weight: bold; font-size: 12px; margin-bottom: 5px; display: block; opacity: 0.8; }
        .input-alan { display: flex; gap: 10px; }
        input { flex: 1; padding: 15px; background: #000; border: 1px solid #00ffcc; color: #00ffcc; outline: none; border-radius: 5px; font-family: monospace; font-size: 16px; }
        button { padding: 15px 20px; background: #00ffcc; color: #000; font-weight: bold; border: none; cursor: pointer; border-radius: 5px; font-family: monospace; font-size: 16px; }
        button:active { background: #fff; }
    </style>
</head>
<body>

    <div class="kutu">
        <h2>🚀 TITAN-X OMEGA AKTİF</h2>
        <p style="font-size: 12px; color: #aaa;">Eğer bu paneli görüyorsan, teşhisin %100 doğruydu Patron!</p>
    </div>

    <div id="chat">
        <div class="msg titan"><span class="isim">SİSTEM MESAJI</span>Emirlerini bekliyorum...</div>
    </div>

    <div class="input-alan">
        <input type="text" id="komut" placeholder="Emrini yaz...">
        <button onclick="atesle()">GÖNDER</button>
    </div>

    <script>
        async function atesle() {
            let input = document.getElementById('komut');
            let mesaj = input.value.trim();
            if (!mesaj) return;
            
            input.value = '';
            let chat = document.getElementById('chat');
            
            chat.innerHTML += `<div class="msg user"><span class="isim">CEO ŞENOL</span>${mesaj}</div>`;
            chat.scrollTop = chat.scrollHeight;
            
            chat.innerHTML += `<div class="msg titan" id="yukleniyor"><span class="isim">TITAN-X</span>İşleniyor...</div>`;
            chat.scrollTop = chat.scrollHeight;

            try {
                let yanit = await fetch('/komut_gonder', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ msg: mesaj })
                });
                let veri = await yanit.json();
                
                document.getElementById('yukleniyor').remove();
                chat.innerHTML += `<div class="msg titan"><span class="isim">TITAN-X</span>${veri.response}</div>`;
            } catch (hata) {
                document.getElementById('yukleniyor').remove();
                chat.innerHTML += `<div class="msg titan" style="border-left: 4px solid red; color: red;"><span class="isim">HATA</span>Sistem bağlantısı koptu.</div>`;
            }
            chat.scrollTop = chat.scrollHeight;
        }
    </script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run()
    
