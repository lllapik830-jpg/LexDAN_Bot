import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, chat, profile, lessons, subscription, voice

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ПОДКЛЮЧАЕМ ВСЕ ОБРАБОТЧИКИ ---
dp.include_routers(
    start.router,
    chat.router,
    profile.router,
    lessons.router,
    subscription.router,
    voice.router
)

async def main():
    print("🤖 LexDAN is running!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())