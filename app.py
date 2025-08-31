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

import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "openai/gpt-oss-120b:free",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ],
    
  })
)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)