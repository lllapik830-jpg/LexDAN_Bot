import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import BOT_TOKEN
from handlers import start, chat, voice, lessons, subscription, progress

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем все обработчики
dp.include_routers(
    start.router,
    chat.router,
    voice.router,
    lessons.router,
    subscription.router,
    progress.router
)

async def main():
    print("🤖 LexDAN is running on Render!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
