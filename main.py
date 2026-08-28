import os
from flask import Flask
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Mini serveur web pour que Render ne coupe pas le bot
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "GDJ1 Football Bot is Live!"

def run_flask():
    app_flask.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask, daemon=True).start()

# Commandes Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut ! Je suis GDJ1 Football Bot ⚽🔥")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Tu as dit: {text}")

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("ERREUR: TELEGRAM_TOKEN manquant")
        return

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
