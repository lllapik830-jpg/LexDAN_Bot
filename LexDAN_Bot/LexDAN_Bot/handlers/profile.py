"""Раздел «Профиль» — статистика и подписка (пока всё бесплатно)."""

from aiogram import Router, F
from aiogram.types import Message

from handlers.filters import ModeFilter
from handlers.keyboards import profile_menu
from services.database import MODE_PROFILE

router = Router()


@router.message(ModeFilter(MODE_PROFILE), F.text == "💎 Подписка")
async def subscription_info(m: Message):
    await m.reply(
        "💎 Подписка\n\n"
        "Сейчас бот полностью бесплатный — можно общаться текстом и голосом без лимитов.\n\n"
        "Позже появятся тарифы. Следи за обновлениями!",
        reply_markup=profile_menu(),
    )


@router.message(ModeFilter(MODE_PROFILE))
async def profile_foolproof(m: Message):
    await m.reply(
        "🙂 В профиле доступны кнопки ниже.",
        reply_markup=profile_menu(),
    )
