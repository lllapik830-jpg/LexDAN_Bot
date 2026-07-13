"""
Общие кнопки, которые работают из любого раздела.
Сейчас это только «Вернуться в меню».
"""

from aiogram import Router, F
from aiogram.types import Message

from handlers.keyboards import main_menu
from services.database import set_mode, MODE_MENU

router = Router()


@router.message(F.text == "🔙 Вернуться в меню")
async def back_to_main(m: Message):
    set_mode(str(m.from_user.id), MODE_MENU)
    await m.reply("🏠 Главное меню. Выбери кнопку ниже.", reply_markup=main_menu())
