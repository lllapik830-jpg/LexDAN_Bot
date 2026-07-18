"""Мягкий paywall: выбор тарифа (оплата подключим отдельно)."""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.lesson_keyboards import tariffs_inline_kb
from services.growth import PRICE_CHAT_MONTH, PRICE_FULL_MONTH, subscription_blurb, ensure_growth
from services.database import load_users, get_user
from config import SUPPORT_USERNAME

router = Router()


@router.callback_query(F.data == "tariff:open")
async def tariff_open(c: CallbackQuery):
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    ensure_growth(user)
    await c.answer()
    await c.message.answer(
        subscription_blurb(user) + "\n\nВыбери тариф:",
        reply_markup=tariffs_inline_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "tariff:chat")
async def tariff_chat(c: CallbackQuery):
    contact = f"@{SUPPORT_USERNAME}" if SUPPORT_USERNAME else "поддержку"
    await c.answer()
    await c.message.answer(
        f"💬 <b>Только общение — {PRICE_CHAT_MONTH}₽/мес</b>\n\n"
        "Безлимит чата (текст + голос).\n"
        f"Оплату подключим совсем скоро. Пока напиши {contact} — активируем вручную.",
        parse_mode="HTML",
    )


@router.callback_query(F.data == "tariff:full")
async def tariff_full(c: CallbackQuery):
    contact = f"@{SUPPORT_USERNAME}" if SUPPORT_USERNAME else "поддержку"
    await c.answer()
    await c.message.answer(
        f"🚀 <b>Безлимит ко всему — {PRICE_FULL_MONTH}₽/мес</b>\n\n"
        "Уроки без дневных лимитов + безлимит общения.\n"
        f"Оплату подключим совсем скоро. Пока напиши {contact} — активируем вручную.",
        parse_mode="HTML",
    )
