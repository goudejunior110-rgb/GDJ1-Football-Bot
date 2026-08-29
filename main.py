import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Flask - c'est ça qui garde Render LIVE gratuit
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "GDJ1 V2.7 LIVE - Bot Telegram OK!"

@flask_app.route('/health')
def health():
    return "OK"

# Bot Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ GDJ1 V2.7 EN LIGNE !\nEnvoie: Crystal Palace - Man City")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"🔎 Analyse GDJ1 pour: {text}\n(Version gratuite - logique de base active)")

def run_bot():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("ERREUR: TELEGRAM_TOKEN manquant")
        return
    print(f"BOT START avec token {token[:10]}...")
    try:
        app = ApplicationBuilder().token(token.strip()).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
        app.run_polling()
    except Exception as e:
        print(f"Erreur bot: {e}")

if __name__ == "__main__":
    # Bot dans un thread
    threading.Thread(target=run_bot, daemon=True).start()
    # Flask en principal - Render voit le port et reste LIVE
    port = int(os.environ.get("PORT", 10000))
    print(f"Flask démarre sur port {port}")
    flask_app.run(host='0.0.0.0', port=port)
