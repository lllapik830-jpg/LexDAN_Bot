from aiogram import Router, types
from aiogram.filters import Command
from handlers.keyboards import lessons_menu

router = Router()

@router.message(Command("lesson"))
async def lesson_cmd(m: types.Message):
    await m.reply("📚 *Выберите урок:*", parse_mode="Markdown", reply_markup=lessons_menu())
