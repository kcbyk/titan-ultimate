import os, requests, base64
from flask import Flask, request, jsonify

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
    try:
        # Arayüzü artık başka bir dosyadan (index.html) çekiyoruz
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Arayüz dosyası (index.html) bulunamadı! Hata: {str(e)}"

@app.route('/api/sor', methods=['POST'])
def sor():
    mesaj = request.json.get('msg')
    cevap = zeka_motoru(mesaj)
    return jsonify({"cevap": cevap})

if __name__ == "__main__":
    app.run()
    
