# app.py
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Dream Agent v1.0 is running"}

# Запуск локально
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)

from fastapi import FastAPI, Request
import openai
from dotenv import load_dotenv
import os

load_dotenv("config/.env")
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")

    thread = openai.beta.threads.create()
    openai.beta.threads.messages.create(thread_id=thread.id, role="user", content=message)
    run = openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)

    while run.status not in ["completed", "failed"]:
        run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    return {"reply": messages.data[0].content[0].text.value}
