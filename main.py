import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "GDJ1 Bot is Live!"

def parse_matches(text):
    lines = []
    for l in text.split('\n'):
        l=l.strip()
        if not l: continue
        if '–' in l or '-' in l or 'vs' in l.lower():
            clean = l.replace(' vs ', ' – ').replace(' - ', ' – ')
            lines.append(clean)
    return lines

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ GDJ1 V2.2 est prêt ! Envoie :\nCrystal Palace – Man City\nBayern – Stuttgart")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matchs = parse_matches(update.message.text)
    if not matchs:
        return
    await update.message.reply_text(f"🔎 GDJ1 reçu {len(matchs)} matchs :\n" + "\n".join(matchs) + "\n\nAnalyse complète en préparation...")

def run_bot():
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot GDJ1 lancé...")
    # Fix Render : pas de gestion de signaux en thread
    app.run_polling(drop_pending_updates=True, stop_signals=None)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Flask en arrière-plan, BOT en principal = plus d'erreur signal
    threading.Thread(target=run_flask).start()
    run_bot()
