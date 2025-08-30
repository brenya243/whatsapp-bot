from flask import Flask, request, make_response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "🤖 Mon chatbot WhatsApp est en marche !"

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.form.get('Body', '').strip()
    sender = request.form.get('From')
    print(f"💬 Message reçu de {sender}: {incoming_msg}")

    # Appel à Deepseek pour générer une réponse
    response_ai = get_ai_response(incoming_msg)
    
    # Réponse par défaut si l'IA échoue
    if not response_ai:
        response_ai = "Désolé, je n'arrive pas à répondre pour l'instant. 🤖"

    # Envoie la réponse via Twilio
    resp = make_response(f"""
<Response>
    <Message>{response_ai}</Message>
</Response>
""")
    resp.mimetype = "text/xml"
    return resp

def get_ai_response(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",  # ← Mets ta clé OpenRouter
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-chat",  # Modèle Deepseek sur OpenRouter
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }
    try:
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 200:
            return r.json()['choices'][0]['message']['content']
        else:
            print(f"Erreur OpenRouter: {r.status_code}, {r.text}")
            return None
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return None

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)