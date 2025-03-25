import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, Application, MessageHandler,
    ContextTypes, filters
)
from openai import OpenAI

# Load env vars
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

client = OpenAI(api_key=OPENAI_API_KEY)

# Create FastAPI and Telegram Application
app = FastAPI()
telegram_app: Application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Telegram handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    thread = client.beta.threads.create()
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_message)

    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    # Wait for completion
    while True:
        status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status
        if status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    last_response = messages.data[0].content[0].text.value
    await update.message.reply_text(last_response)

# Register handler
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# FastAPI webhook endpoint
@app.post("/")
async def webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, telegram_app.bot)

    # ✅ Make sure it's initialized
    if not telegram_app._initialized:
        await telegram_app.initialize()

    await telegram_app.process_update(update)
    return {"ok": True}

# FastAPI lifecycle hooks
@app.on_event("startup")
async def on_startup():
    await telegram_app.initialize()
    await telegram_app.start()

@app.on_event("shutdown")
async def on_shutdown():
    await telegram_app.stop()
    await telegram_app.shutdown()
