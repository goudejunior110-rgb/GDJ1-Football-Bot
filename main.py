import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Flask - garde Render LIVE
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "GDJ1 V2.8 LIVE"

# Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ GDJ1 V2.8 EN LIGNE !\nEnvoie: Crystal Palace - Man City")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔎 Reçu: {update.message.text}\nJe lance l'analyse...")

async def bot_main():
    token = os.getenv("TELEGRAM_TOKEN")
    print(f"BOT START token {token[:10] if token else 'MANQUANT'}...", flush=True)
    app = ApplicationBuilder().token(token.strip()).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("BOT POLLING OK", flush=True)
    await app.run_polling(drop_pending_updates=True)

def run_bot_thread():
    asyncio.run(bot_main())

if __name__ == "__main__":
    threading.Thread(target=run_bot_thread, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    print(f"FLASK sur {port}", flush=True)
    flask_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
