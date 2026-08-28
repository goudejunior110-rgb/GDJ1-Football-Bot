import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ GDJ-Football-Bot est en ligne !\nEnvoie ta liste de matchs.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    propre = text.replace(" vs ", " – ").replace(" - ", " – ").replace(" VS ", " – ")
    await update.message.reply_text(propre)

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("Ajoute TELEGRAM_TOKEN")
        return
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Bot lancé...")
    app.run_polling()

if __name__ == "__main__":
    main()
