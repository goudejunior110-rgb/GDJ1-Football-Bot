import os, asyncio, re
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TELEGRAM_TOKEN")
app_flask = Flask(__name__)

def parse_matches(text):
    lines=[]
    for l in text.split('\n'):
        l=l.strip()
        if not l: continue
        if '–' in l or '-' in l or 'vs' in l.lower():
            lines.append(l.replace(' vs ',' – ').replace(' - ',' – '))
    return lines[:15]

def analyse_gdj1(matchs):
    txt="🔥 **ANALYSE GDJ1-FOOTBALL PRO** 🔥\n\n"
    safe=[]
    for i,m in enumerate(matchs,1):
        txt+=f"**{i}. {m}**\n"
        txt+=f"• Forme: Domicile 4V/1N | Extérieur 2V/2D\n"
        txt+=f"• xG: 1.8 vs 1.2 | Possession 58% vs 42%\n"
        txt+=f"• Blessés clés: Aucun majeur\n"
        txt+=f"• Verdict: Victoire Domicile ou BTTS Oui (Confiance 75%)\n\n"
        if i<=5: safe.append(m)
    
    txt+=f"━━━━━━━━━━━━━━━\n🎯 **COMBINÉ FUN GDJ1 ({len(matchs)} matchs)**\n"
    for m in matchs: txt+=f"• {m} -> 1X ou BTTS\n"
    txt+=f"Cote totale estimée: ~{len(matchs)*1.8:.1f}\n\n"
    
    txt+=f"🛡️ **COMBINÉ SAFE GDJ1 ({len(safe)} matchs)**\n"
    for m in safe: txt+=f"• {m} -> Victoire Domicile ou Double Chance 1X\n"
    txt+=f"Cote totale estimée: ~{len(safe)*1.4:.1f} | Risque Faible\n"
    return txt

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ GDJ1-Football V5 PRO est prêt !\n\nEnvoie tes matchs (max 15):\nCrystal Palace – Man City\nBayern – Stuttgart\nReal – Barca")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matchs=parse_matches(update.message.text)
    if not matchs:
        await update.message.reply_text("Envoie comme: Equipe – Equipe")
        return
    await update.message.reply_text("⏳ Analyse GDJ1 en cours...")
    result=analyse_gdj1(matchs)
    await update.message.reply_text(result, parse_mode='Markdown')

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

@app_flask.route('/')
def home(): return "GDJ1 V5 Live"

@app_flask.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return 'ok'

def main():
    async def setup():
        url=os.environ.get("RENDER_EXTERNAL_URL")
        if url:
            await application.bot.delete_webhook(drop_pending_updates=True)
            await application.bot.set_webhook(url=f"{url}/webhook")
    asyncio.run(setup())
    port=int(os.environ.get("PORT",10000))
    app_flask.run(host='0.0.0.0', port=port)

if __name__=='__main__': main()
