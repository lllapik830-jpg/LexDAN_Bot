"""
Общие кнопки из любого раздела.
"""

from aiogram import Router, F
from aiogram.types import Message

from handlers.keyboards import main_menu
from services.database import set_mode, MODE_MENU
from services.assessment import clear_assessment_phase
from services.lesson_state import clear_lesson

router = Router()


@router.message(F.text == "🔙 Вернуться в меню")
async def back_to_main(m: Message):
    from services.database import load_users, get_user
    from services.growth import ensure_growth

    user_id = str(m.from_user.id)
    clear_assessment_phase(user_id)
    clear_lesson(user_id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    set_mode(user_id, MODE_MENU)
    await m.reply(
        "🏠 Главное меню. Выбери кнопку ниже.",
        reply_markup=main_menu(user),
    )
