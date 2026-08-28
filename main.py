import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut ! Je suis GDJ1 Football Bot ⚽️ Envoie moi un match, ex: Real contre Barca")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Tu as dit: {text}\nMon IA pronostic arrive bientôt...")

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
