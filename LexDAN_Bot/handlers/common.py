"""
Общие кнопки из любого раздела.
"""

from aiogram import Router, F
from aiogram.types import Message

from handlers.keyboards import main_menu
from services.database import set_mode, MODE_MENU
from services.assessment import clear_assessment_phase
from services.lesson_state import clear_lesson
from services.tg_out import say

router = Router()


@router.message(F.text == "🔙 Вернуться в меню")
async def back_to_main(m: Message):
    from services.database import load_users, get_user, save_users
    from services.growth import ensure_growth
    from handlers.trial_notify import flush_trial_ended

    user_id = str(m.from_user.id)
    clear_assessment_phase(user_id)
    clear_lesson(user_id)
    try:
        from services.listening_state import clear_session as clear_listening

        clear_listening(user_id)
    except Exception:
        pass
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    await flush_trial_ended(m, user, users, user_id)
    # сбросить зависший ввод промокода, чтобы секреты/меню не ломались
    if (user.get("step") or "") in {"awaiting_promo_profile", "awaiting_promo", "awaiting_name_change"}:
        user["step"] = "ready"
    save_users(users, only=user_id)
    set_mode(user_id, MODE_MENU)
    await say(
        m,
        "🏠 Главное меню. Выбери кнопку ниже.",
        replace=True,
        delete_tap=True,
        reply_markup=main_menu(user),
    )
