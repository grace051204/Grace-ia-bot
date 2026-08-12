import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Les clés seront ajoutées plus tard dans Render.
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bonjour ! Je suis Grace IA 🤖\n\n"
        "Pose-moi ta question et je ferai de mon mieux pour t'aider."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=(
                "Tu es Grace IA, un assistant intelligent, "
                "amical, clair et utile. Réponds en français sauf "
                "si l'utilisateur demande une autre langue."
            ),
            input=message
        )

        answer = response.output_text

        await update.message.reply_text(answer)

    except Exception:
        await update.message.reply_text(
            "Désolé, une erreur s'est produite. Réessaie dans quelques instants."
        )


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("Grace IA est démarré !")
    app.run_polling()


if __name__ == "__main__":
    main()
