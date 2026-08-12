import os
from flask import Flask, request
from openai import OpenAI
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=30
    )


@app.route("/", methods=["GET"])
def home():
    return "Grace IA est en ligne 🤖"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return "OK"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(
            chat_id,
            "👋 Bonjour ! Je suis Grace IA 🤖\n\n"
            "Pose-moi ta question."
        )
        return "OK"

    if not text:
        return "OK"

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=(
                "Tu es Grace IA, un assistant intelligent, "
                "amical, clair et utile. "
                "Réponds en français sauf si l'utilisateur "
                "demande une autre langue."
            ),
            input=text
        )

        answer = response.output_text

        send_message(chat_id, answer)

        except Exception as e:
    print("ERREUR OPENAI :", repr(e))
    send_message(
        chat_id,
        f"⚠️ Erreur technique : {str(e)[:1000]}"
    )
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
