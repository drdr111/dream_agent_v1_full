
import openai
import os
from dotenv import load_dotenv

load_dotenv("config/.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

assistant = openai.beta.assistants.create(
    name="Dream Agent v1.0",
    instructions="""
Ты — Dream Agent, ядро команды Dream Team.  
У тебя есть роли: Эйнштейн (стратегия), Алина (дизайн), Илон (интеграции), Никита (бэкенд), Рой (DevOps), Марк (ML).  
На основе вопроса пользователя определи, кто из команды должен ответить.  
Формируй рассуждение и отвечай от имени участника (например, Эйнштейн: ...).  
Ты работаешь с внешними API, можешь вызывать действия и давать инструкции.
""",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

print("Assistant ID:", assistant.id)
