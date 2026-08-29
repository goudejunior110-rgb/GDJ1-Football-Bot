
import os, threading
from flask import Flask
from telegram.ext import Application, CommandHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot Live!"

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

async def start(update, context):
    await update.message.reply_text("⚽ GDJ1 est EN LIGNE!")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__": main()
