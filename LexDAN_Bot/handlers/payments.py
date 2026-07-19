"""Мягкий paywall: выбор тарифа (оплата подключим отдельно)."""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.lesson_keyboards import tariffs_inline_kb
from services.growth import subscription_blurb, ensure_growth
from services.database import load_users, get_user, save_users
from services.pricing import chat_price, discount_blurb, full_price
from config import SUPPORT_USERNAME

router = Router()


@router.callback_query(F.data == "tariff:open")
async def tariff_open(c: CallbackQuery):
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    ensure_growth(user)
    save_users(users)
    await c.answer()
    await c.message.answer(
        subscription_blurb(user) + "\n\nВыбери тариф:",
        reply_markup=tariffs_inline_kb(user),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "tariff:chat")
async def tariff_chat(c: CallbackQuery):
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    ensure_growth(user)
    price, pct = chat_price(user)
    contact = f"@{SUPPORT_USERNAME}" if SUPPORT_USERNAME else "поддержку"
    disc = f" (скидка {pct}%)" if pct else ""
    await c.answer()
    await c.message.answer(
        f"💬 <b>Только общение — {price}₽/мес</b>{disc}\n\n"
        "Безлимит чата (текст + голос).\n"
        f"{discount_blurb(user)}"
        f"Оплату подключим совсем скоро. Пока напиши {contact} "
        f"и пришли свой ID <code>{c.from_user.id}</code> — активируем вручную.",
        parse_mode="HTML",
    )


@router.callback_query(F.data == "tariff:full")
async def tariff_full(c: CallbackQuery):
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    ensure_growth(user)
    price, pct = full_price(user)
    contact = f"@{SUPPORT_USERNAME}" if SUPPORT_USERNAME else "поддержку"
    disc = f" (скидка {pct}%)" if pct else ""
    await c.answer()
    await c.message.answer(
        f"🚀 <b>Безлимит ко всему — {price}₽/мес</b>{disc}\n\n"
        "Уроки без дневных лимитов + безлимит общения.\n"
        f"{discount_blurb(user)}"
        f"Оплату подключим совсем скоро. Пока напиши {contact} "
        f"и пришли свой ID <code>{c.from_user.id}</code> — активируем вручную.",
        parse_mode="HTML",
    )