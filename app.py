from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return "🤖 Mon chatbot WhatsApp est en marche !"

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.form.get('Body', '').strip()
    sender = request.form.get('From')
    print(f"💬 Message reçu de {sender}: {incoming_msg}")

    response_msg = "Merci pour ton message ! Je suis un bot automatisé. 🚀"

    resp = make_response(f"""
<Response>
    <Message>{response_msg}</Message>
</Response>
""")
    resp.mimetype = "text/xml"
    return resp

if __name__ == '__main__':
    app.run(port=5000)