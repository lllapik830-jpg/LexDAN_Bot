"""Уведомление о конце пробного периода (промо ENGRICO77 и т.п.)."""

from __future__ import annotations

from aiogram.types import Message

from services.database import save_users
from services.promo import pop_trial_ended_notice


async def flush_trial_ended(m: Message, user: dict, users: dict, user_id: str) -> bool:
    """
    Если пробный период только что истёк — отправить сообщение Рико + кнопки тарифов.
    True если отправили.
    """
    msg = pop_trial_ended_notice(user)
    if not msg:
        return False
    save_users(users, only=user_id)
    from handlers.lesson_keyboards import tariffs_inline_kb

    await m.answer(msg, reply_markup=tariffs_inline_kb(user), parse_mode="HTML")
    return True
