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
from handlers import start, common, voice, chat, lessons, lessons_grammar, lessons_vocabulary, lessons_sections, profile, menu, payments, secret_missions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_routers(
    start.router,
    common.router,
    secret_missions.router,  # кнопка секрета до catch-all меню
    menu.router,
    payments.router,
    voice.router,
    lessons_vocabulary.router,
    lessons_grammar.router,
    lessons_sections.router,
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
    db = "Postgres" if os.getenv("DATABASE_URL") else "users.json (file)"
    print(f"🤖 LexDAN is running! Storage: {db}")
    logging.info(f"User storage backend: {db}")
    asyncio.create_task(_reminder_loop())
    await dp.start_polling(bot)


async def _reminder_loop():
    """Раз в час проверяем, кому напомнить про занятие."""
    from services.reminders import send_due_reminders

    await asyncio.sleep(45)  # дать боту подняться
    while True:
        try:
            n = await send_due_reminders(bot)
            if n:
                logging.info(f"Reminders sent: {n}")
        except Exception as e:
            logging.error(f"Reminder loop error: {e}")
        await asyncio.sleep(3600)


if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    asyncio.run(main())
