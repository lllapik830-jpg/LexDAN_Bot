import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import BOT_TOKEN
from handlers import start, chat, voice, lessons, subscription, progress, callback  # <-- callback добавлен
from flask import Flask
import threading

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ПОДКЛЮЧАЕМ ВСЕ ОБРАБОТЧИКИ ---
dp.include_routers(
    start.router,
    chat.router,
    voice.router,
    lessons.router,
    subscription.router,
    progress.router,
    callback.router,  # <-- callback добавлен в список
)

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 LexDAN is running!"

def keep_alive():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=keep_alive, daemon=True).start()

async def main():
    print("🤖 LexDAN is running on Render!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
