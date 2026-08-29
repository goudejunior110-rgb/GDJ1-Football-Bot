import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Petit serveur web pour Render
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "GDJ1 Bot V2.3 is Live!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# Bot Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ GDJ1 V2.3 EN LIGNE !\nEnvoie tes matchs:\nCrystal Palace - Man City\nBayern - Stuttgart")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"🔎 Analyse GDJ1 pour:\n{text}\n\n📍 Analyse approfondie en cours...\n✅ Combiné 12 + SAFE 4.5 bientot!")

def run_bot():
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    run_bot()
