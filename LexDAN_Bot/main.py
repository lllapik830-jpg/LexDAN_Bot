"""
Точка входа бота.
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
    start.router,
    common.router,
    menu.router,       # кнопки меню раньше разделов — чтобы всегда ловились
    voice.router,
    chat.router,
    lessons.router,
    profile.router,
)

app = Flask(__name__)


@app.route("/")
def home():
    return "LexDAN is running!"


def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


async def main():
    # Сбрасываем старые апдейты и webhook — меньше двойных ответов
    await bot.delete_webhook(drop_pending_updates=True)
    print("🤖 LexDAN is running!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    asyncio.run(main())
