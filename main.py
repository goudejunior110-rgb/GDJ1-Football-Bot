import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Petit serveur web pour que Render ne coupe pas le bot
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
    await update.message.reply_text(
        "✅ **GDJ1 V2.1 est prêt !**\n\nEnvoie les matchs comme :\nCrystal Palace – Man City\nBayern – Stuttgart\n\nJe lance la méthode complète 🔥"
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matchs = parse_matches(update.message.text)
    if not matchs:
        await update.message.reply_text("Format : Equipe – Equipe")
        return
    await update.message.reply_text(f"🔎 J'ai reçu {len(matchs)} matchs. Analyse GDJ1 en cours...\n" + "\n".join(matchs))

def run_bot():
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot GDJ1 lancé...")
    app.run_polling()

# Lancement des 2 en même temps
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)
