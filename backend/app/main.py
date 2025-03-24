from fastapi import FastAPI
from app.routes import chat, memory, tools

app = FastAPI(title='Dream Agent v1.0')

app.include_router(chat.router, prefix='/chat')
app.include_router(memory.router, prefix='/memory')
app.include_router(tools.router, prefix='/tools')
