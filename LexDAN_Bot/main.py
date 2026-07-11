import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(m: Message):
    await m.reply("🤖 *Hello! I'm LexDAN, your AI English tutor.*\n\n📝 *What is your name?*", parse_mode="Markdown")

@dp.message()
async def all_messages(m: Message):
    if m.text and not m.text.startswith('/'):
        await m.reply("📩 I received your message. I will respond soon!")

async def main():
    print("🤖 LexDAN is running (aiogram 3 with VPN)!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())