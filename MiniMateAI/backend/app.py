import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Güncellenmiş Gemini 1.5 Pro URL
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not gemini_api_key:
        return jsonify({"error": "Gemini API anahtarı eksik"}), 500

    headers = {
        "Content-Type": "application/json"
    }

    # API anahtarını URL'ye ekle
    api_url = f"{GEMINI_API_URL}?key={gemini_api_key}"
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": user_message
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # HTTP hataları için istisna oluştur
        
        result = response.json()
        
        try:
            generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": generated_text})
        except (KeyError, IndexError) as e:
            print(f"Yanıt işleme hatası: {e}")
            print(f"API yanıtı: {result}")
            return jsonify({"error": "Yanıt formatı beklendiği gibi değil"}), 500
            
    except requests.exceptions.RequestException as e:
        print(f"API isteği hatası: {e}")
        error_message = str(e)
        if response and hasattr(response, 'text'):
            error_message = response.text
        return jsonify({"error": f"API isteği başarısız: {error_message}"}), 500

if __name__ == "__main__":
    app.run(debug=True)