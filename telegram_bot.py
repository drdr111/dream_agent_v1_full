import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# Загрузка переменных окружения
load_dotenv("config/.env")

openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Настройка OpenAI
client = OpenAI(api_key=openai_api_key)

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    while True:
        status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if status.status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    last_response = messages.data[0].content[0].text.value

    await update.message.reply_text(last_response)

# Основной запуск
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8443))

    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{os.environ['RAILWAY_PUBLIC_DOMAIN']}/"
    )
