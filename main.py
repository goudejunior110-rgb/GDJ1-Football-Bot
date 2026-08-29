
import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "GDJ1 Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

async def start(update, context):
    await update.message.reply_text("⚽ Salut ! GDJ1 Football Bot est en ligne !")

def main():
    # Lance le serveur web pour Render
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Lance le bot Telegram
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
