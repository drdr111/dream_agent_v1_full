
# 🤖 Dream Agent Telegram Bot

Бот на базе OpenAI Assistant API, развёрнутый на [Railway](https://railway.app). Отвечает на сообщения пользователей с использованием собственного ассистента OpenAI GPT-4.

---

## 📦 Возможности

- Интеграция с Telegram через webhook  
- Использование OpenAI Assistants API (GPT-4, функции, инструменты)
- Деплой в 1 клик на Railway  
- Асинхронная архитектура на FastAPI

---

## 🛠️ Стек

- Python 3.12+
- FastAPI
- python-telegram-bot v20.5
- OpenAI SDK
- Railway

---

## 🔐 Переменные окружения (.env)

Создайте файл `.env` в корне проекта и добавьте:

```env
OPENAI_API_KEY=sk-...
ASSISTANT_ID=asst_...
TELEGRAM_BOT_TOKEN=7658570175:...
```

---

## 🚀 Локальный запуск

```bash
pip install -r requirements.txt
python telegram_bot.py
```

---

## 🐳 Деплой на Railway

1. Клонируйте репозиторий:

```bash
git clone https://github.com/drdr111/dream_agent_v1_full.git
```

2. Убедитесь, что в репозитории есть:

- `Dockerfile`
- `Procfile`
- `requirements.txt`
- `telegram_bot.py`

3. Зайдите на Railway → New Project → Deploy from GitHub

4. В разделе `Variables` добавьте переменные окружения из `.env`

5. Railway автоматически поднимет сервер и выдаст `https://your-app.up.railway.app`

---

## 🔗 Установка Webhook для Telegram

```bash
curl -X POST https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook ^
     -d "url=https://your-app.up.railway.app/"
```

Проверьте:

```bash
curl -X POST https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getWebhookInfo
```

---

## 📁 Структура проекта

```
dream_agent_v1_full/
│
├── telegram_bot.py        # основной код Telegram-бота + FastAPI
├── requirements.txt       # зависимости
├── Dockerfile             # docker-сборка для Railway
├── Procfile               # команда запуска
├── .env                   # переменные окружения (не коммить!)
└── README.md              # эта документация
```

---

## 🧠 Ассистент OpenAI

Создайте ассистента в [OpenAI Playground](https://platform.openai.com/assistants) и скопируйте его `asst_...` ID в `.env`.

---

## 🐞 Возможные ошибки

- 404 OpenAI: `No assistant found` → проверьте `ASSISTANT_ID`
- 502 Webhook: неправильный ответ → не запущен бот на Railway
- Ошибка `Method Not Allowed`: вы открыли URL в браузере (GET), а Telegram использует POST

---

## ✅ Автор

Darkhan | [@drdr111](https://github.com/drdr111)
