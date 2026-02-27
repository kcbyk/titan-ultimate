import os, requests, base64, firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, send_from_directory

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

# --- 🔥 FIREBASE ÖLÜMSÜZ HAFIZASI ---
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

@app.route('/')
def ana_sayfa():
    # Ayrı mimari: Doğrudan index.html dosyasını okuyup gönderir.
    return send_from_directory('.', 'index.html')

@app.route('/api/sor', methods=['POST'])
def sor():
    mesaj = request.json.get('msg')
    cevap = "Sistem aktif."
    for key in GROQ_KEYS:
        try:
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Sen S.E.N.O.L TITAN-X'sin. Şenol'un CEO asistanısın ve yazılım dehasısın."}, {"role": "user", "content": mesaj}]},
                timeout=12
            )
            if res.status_code == 200: 
                cevap = res.json()['choices'][0]['message']['content']
                break
        except: continue
    return jsonify({"cevap": cevap})

# --- KOYEB SUNUCU ATEŞLEMESİ ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
                
