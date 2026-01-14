import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from google import genai

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam! 🤖 Men Gemini AI bot ✅ Sorag ýaz!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        r = client.models.generate_content(
            model=genai.GenerativeModel("models/gemini-pro"),
            contents=text
        )
        await update.message.reply_text(r.text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ýalňyşlyk: {e}")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ Bot Render-da işe başlady...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

