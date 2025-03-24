import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    Application,
)
from fastapi import FastAPI, Request
from openai import OpenAI

# Загрузка переменных окружения
load_dotenv("config/.env")

# Ключи
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Инициализация клиентов
client = OpenAI(api_key=OPENAI_API_KEY)
telegram_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app = FastAPI()

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Создание сессии Assistant
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    )

    while True:
        status = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        ).status
        if status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    last_response = messages.data[0].content[0].text.value
    await update.message.reply_text(last_response)

# Хендлер сообщений
telegram_app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

# Webhook endpoint для FastAPI
@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

