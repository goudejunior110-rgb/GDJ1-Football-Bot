import os, re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

def extract_matches(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return [l for l in lines if '–' in l or '-' in l or 'vs' in l.lower()]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ GDJ1 V2.2 GRATUIT EN LIGNE !\nEnvoie tes matchs:\nCrystal Palace – Man City\nBayern – Stuttgart")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    matches = extract_matches(text)
    if not matches:
        await update.message.reply_text("Format: Equipe A – Equipe B")
        return
    
    await update.message.reply_text(f"🔎 Analyse GDJ1 lancée pour {len(matches)} matchs...\n\n" + "\n".join(matches))

    # ICI TA MÉTHODE GDJ1 SERA EXECUTEE
    resultat = "🔥 ANALYSE GDJ1\n\n"
    for m in matches:
        resultat += f"\n📍 MATCH: {m}\n🏆 Résultat probable: 1X ou DNB Domicile à analyser\n🎯 Score: 1-1 / 2-1\n📊 Confiance: 7/10\n---\n"
    
    resultat += "\n✅ COMBINÉ PRINCIPAL Cote 12\n✅ SAFE Cote 4.5\n\nBot V2.2 Opérationnel ! Maintenant on va brancher la recherche approfondie."
    
    await update.message.reply_text(resultat)

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
