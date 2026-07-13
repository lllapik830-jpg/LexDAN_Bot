"""
Точка входа — «кнопка питания» бота.

Порядок роутеров важен:
1) start — команда /start и имя
2) voice — голосовые в режиме chat
3) chat — текст в режиме chat
4) lessons / profile — свои разделы
5) menu — кнопки главного меню и защита от дурака
"""

import asyncio
import logging
import os
import threading

from aiogram import Bot, Dispatcher
from flask import Flask

from config import BOT_TOKEN
from handlers import start, common, voice, chat, lessons, profile, menu

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_routers(
    start.router,      # /start и имя
    common.router,     # «Вернуться в меню» из любого раздела
    voice.router,      # голосовые только в chat
    chat.router,       # текст только в chat
    lessons.router,    # заглушка уроков
    profile.router,    # профиль
    menu.router,       # кнопки главного меню
)

# Веб-сервер нужен Render'у, чтобы сервис считался «живым»
app = Flask(__name__)


@app.route("/")
def home():
    return "LexDAN is running!"


def keep_alive():
    # Render сам даёт порт в переменной PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


async def main():
    print("🤖 LexDAN is running!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    asyncio.run(main())
