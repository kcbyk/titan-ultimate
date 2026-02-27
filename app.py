import os, time, requests, base64
from flask import Flask, request, jsonify, render_template_string

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

# --- 🧠 GEÇİCİ RAM HAFIZASI (Firebase Devre Dışı) ---
# Sohbetler şimdilik sunucu hafızasında tutulacak. Sunucu yeniden başlarsa silinir.
gecici_hafiza = []

def titan_x_zeka_motoru(prompt):
    for key in GROQ_KEYS:
        try:
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Sen S.E.N.O.L TITAN-X'sin. Siber güvenlik ve yazılım uzmanısın. Kullanıcıya Patron diye hitap et."}, {"role": "user", "content": prompt}]},
                timeout=12
            )
            if res.status_code == 200: return res.json()['choices'][0]['message']['content']
        except: continue
    return "⚠️ Sistem Uyarısı: API limitleri doldu!"

@app.route('/')
def ana_panel():
    try:
        return render_template_string(GELISMIS_ARAYUZ, history=gecici_hafiza, status="TEST MODU (FIREBASE KAPALI)")
    except Exception as e:
        return f"<div style='background:black; color:red; padding:20px; font-family:monospace; font-size:18px;'><h1>ARAYÜZ HATASI!</h1><p>{str(e)}</p></div>"

@app.route('/komut_gonder', methods=['POST'])
def komut_gonder():
    kullanici_mesaji = request.json.get('msg')
    
    # Kullanıcı mesajını RAM'e ekle
    gecici_hafiza.append({'role': 'user', 'content': kullanici_mesaji})
    
    # TITAN-X yanıtlasın ve RAM'e eklensin
    titan_yaniti = titan_x_zeka_motoru(kullanici_mesaji)
    gecici_hafiza.append({'role': 'assistant', 'content': titan_yaniti})
    
    return jsonify({"response": titan_yaniti})

# --- MÜKEMMEL ARAYÜZ (GÜVENLİ CSS) ---
GELISMIS_ARAYUZ = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TITAN-X OMEGA MERKEZİ</title>
    <style>
        body { background-color: #070a13; color: #00ffcc; font-family: monospace; margin: 0; padding: 0; height: 100vh; display: flex; flex-direction: column; }
        .header { background: #03050a; padding: 15px; border-bottom: 2px solid #00ffcc; text-align: center; }
        .header h1 { margin: 0; font-size: 20px; text-shadow: 0 0 10px #00ffcc; }
        .status { font-size: 12px; color: #ffeb3b; margin-top: 5px; animation: blink 1.5s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        #chat-kutu { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 15px; }
        .msg { padding: 12px; border-radius: 8px; max-width: 85%; font-size: 14px; word-wrap: break-word; }
        .user { align-self: flex-end; background: #141f33; border: 1px solid #2a3d5e; color: #8bb4f7; }
        .assistant { align-self: flex-start; background: #061513; border: 1px solid #00ffcc; color: #e0ffff; }
        .isim-etiket { font-weight: bold; font-size: 11px; margin-bottom: 5px; display: block; }
        .user .isim-etiket { color: #58a6ff; }
        .assistant .isim-etiket { color: #00ffcc; }
        .kontrol-paneli { background: #03050a; padding: 15px; display: flex; gap: 10px; border-top: 1px solid #1a2333; }
        input { flex: 1; background: #0b111c; border: 1px solid #00ffcc; color: #00ffcc; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 14px; }
        button { background: #00ffcc; color: #000; border: none; padding: 0 20px; border-radius: 6px; font-weight: bold; font-family: monospace; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <h1>TITAN-X OMEGA</h1>
        <div class="status">SİSTEM DURUMU: {{ status }}</div>
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
        <input type="text" id="komut-satiri" placeholder="Emret Patron...">
        <button onclick="atesle()">İLET</button>
    </div>

    <script>
        async function atesle() {
            const input = document.getElementById('komut-satiri');
            const mesaj = input.value.trim();
            if (!mesaj) return;
            
            input.value = '';
            const chatKutu = document.getElementById('chat-kutu');
            chatKutu.innerHTML += `<div class='msg user'><span class='isim-etiket'>CEO ŞENOL</span>${mesaj}</div>`;
            chatKutu.scrollTop = chatKutu.scrollHeight;
            
            try {
                const yanit = await fetch('/komut_gonder', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ msg: mesaj })
                });
                const veri = await yanit.json();
                chatKutu.innerHTML += `<div class='msg assistant'><span class='isim-etiket'>TITAN-X</span>${veri.response}</div>`;
            } catch (hata) {
                chatKutu.innerHTML += `<div class='msg assistant' style='border-color: red;'>BAĞLANTI HATASI</div>`;
            }
            chatKutu.scrollTop = chatKutu.scrollHeight;
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run()
            
