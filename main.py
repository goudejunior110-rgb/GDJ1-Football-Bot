import os, threading, asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "GDJ1 Bot Live - Anti-Conflict OK"

def parse_matches(text):
    lines=[]
    for l in text.split('\n'):
        l=l.strip()
        if not l: continue
        if '–' in l or '-' in l or 'vs' in l.lower():
            lines.append(l.replace(' vs ',' – ').replace(' - ',' – '))
    return lines

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ GDJ1 V2.3 est ENFIN prêt !\nEnvoie tes matchs:\nCrystal Palace – Man City")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m=parse_matches(update.message.text)
    if m:
        await update.message.reply_text(f"🔥 {len(m)} matchs reçus:\n"+"\n".join(m)+"\n\nAnalyse GDJ1 complète arrive...")

async def run_bot_async():
    token=os.environ.get("TELEGRAM_TOKEN")
    app=ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    
    # FIX CONFLIT : on supprime l'ancien webhook/getUpdates avant de démarrer
    await app.bot.delete_webhook(drop_pending_updates=True)
    print("Webhook supprimé, lancement polling...")
    await app.run_polling(drop_pending_updates=True, stop_signals=None, allowed_updates=Update.ALL_TYPES)

def run_bot():
    asyncio.run(run_bot_async())

def run_flask():
    port=int(os.environ.get("PORT",10000))
    app_web.run(host='0.0.0.0', port=port)

if __name__=="__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
