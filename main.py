
import os
import asyncio
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

PROMPT_GDJ1 = """
Tu es l'IA GDJ1 - Expert Prédiction Football.
MÉTHODE OBLIGATOIRE à suivre pour chaque match reçu:

1. Recherche approfondie: Forme, Domicile/Exterieur, Buts marqués/encaissés, xG/xGA, H2H, Blessures, Compos probables, Série, Moyenne buts, Tirs, Corners si fiable, Tendances Over/Under, BTTS, Cotes, Prédictions autres sites. Ne dépends jamais d'une seule source.

2. Pour chaque match produis:
MATCH: Equipe A 🆚 Equipe B
🏆 Résultat probable:
🎯 Score exact principal:
🔄 Scores alternatifs:
⏱️ Mi-temps:
⚽ Over 1,5: / Over 2,5: / Under 3,5:
🤝 BTTS:
🎯 Premier but:
📊 Confiance: X/10
🧠 Scénario:

3. Sélectionne meilleurs marchés (Double chance, DNB, Over/Under, BTTS, Team to score, etc). Ne force jamais.

4. Construis COMBINÉ PRINCIPAL cote 10-15
5. Construis COMBINÉ SAFE cote 3-5 totalement indépendant
6. Pas de "100% sûr", pas de "garanti"
7. Termine par MEILLEURS CHOIX, COMBINE 10-15, SAFE 3-5, SCORES A SURVEILLER, MATCHS A EVITER

Format final très visuel avec emojis comme dans le cahier des charges GDJ1.
"""

def extract_matches(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    matches = []
    for l in lines:
        if '–' in l or '-' in l or 'vs' in l.lower():
            clean = l.replace(' vs ', ' – ').replace(' - ', ' – ').replace('vs', '–')
            matches.append(clean)
    return matches

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ GDJ1 Football Bot V2 EN LIGNE!\n\nEnvoie-moi tes matchs du jour comme ça:\nCrystal Palace – Man City\nBayern – Stuttgart\n\nJe lance Recherche → Analyse → Combiné 10-15 → SAFE 3-5 🔥")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    matches = extract_matches(text)

    if not matches:
        await update.message.reply_text("Envoie-moi les matchs au format: Equipe A – Equipe B")
        return

    await update.message.reply_text(f"🔎 GDJ1 analyse {len(matches)} match(s) en cours...\nRecherche approfondie lancée...\n\n{chr(10).join(matches)}\n\n⏳ Patiente 30-60 sec...")

    if not openai_client:
        await update.message.reply_text("❌ Il manque la clé OPENAI_API_KEY sur Render. Ajoute-la dans Environment.")
        return

    try:
        full_prompt = f"{PROMPT_GDJ1}\n\nMATCHS DU JOUR A ANALYSER:\n" + "\n".join(matches)

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.7,
            max_tokens=4000
        )
        result = response.choices[0].message.content
        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"Erreur analyse: {e}")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("GDJ1 V2 Lancé...")
    app.run_polling()

if __name__ == "__main__":
    main()
