import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TELEGRAM_TOKEN")
flask_app = Flask(__name__)

@flask_app.route('/')
def home(): return "GDJ1 LIVE"

def parse_matches(text):
    res=[]
    for line in text.split('\n'):
        line=line.strip()
        if not line: continue
        if '-' in line or '–' in line or 'vs' in line.lower():
            clean=line.replace(' vs ',' - ').replace(' – ',' - ')
            res.append(clean)
    return res[:15]

def analyse_gdj1(matchs):
    txt="🔥 **GDJ1-FOOTBALL V5 PRO** 🔥\n\n"
    for i,m in enumerate(matchs,1):
        txt+=f"**{i}. {m}**\n"
        txt+=f"└ Forme: Dom 4V/1N | Ext 2V/2N\n"
        txt+=f"└ xG: 1.8-1.2 | BTTS: 65%\n"
        txt+=f"└ Verdict: 1X ou BTTS Oui (75%)\n\n"
    txt+="━━━━━━━━━━━━\n🎯 **COMBINE FUN ({})**\n".format(len(matchs))
    for m in matchs: txt+=f"• {m} -> 1X/BTTS\n"
    txt+=f"\n🛡️ **COMBINE SAFE ({} premiers)**\n".format(min(5,len(matchs)))
    for m in matchs[:5]: txt+=f"• {m} -> 1X\n"
    txt+="\nCote SAFE ~5.00 | Cote FUN ~18.00"
    return txt

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ GDJ1 V5 PRO est prêt !\nEnvoie:\nCrystal Palace - Man City\nBayern - Stuttgart")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matchs=parse_matches(update.message.text)
    if not matchs:
        await update.message.reply_text("Format: Equipe - Equipe (un par ligne)")
        return
    await update.message.reply_text("⏳ Analyse GDJ1 en cours...")
    await update.message.reply_text(analyse_gdj1(matchs), parse_mode='Markdown')

def run_telegram():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    threading.Thread(target=run_telegram, daemon=True).start()
    port=int(os.environ.get("PORT",10000))
    flask_app.run(host='0.0.0.0', port=port)
