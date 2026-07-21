"""Оплата тарифов через ЮKassa + автопродление."""

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.lesson_keyboards import tariffs_inline_kb
from services.growth import subscription_blurb, ensure_growth
from services.database import load_users, get_user, save_users
from services.pricing import chat_price, discount_blurb, full_price
from services.yookassa_pay import (
    PLAN_CHAT,
    PLAN_FULL,
    confirmation_url,
    create_payment,
    disable_autorenew,
    plan_amount_for_user,
    plan_title,
    yookassa_configured,
)
from config import SUPPORT_USERNAME

router = Router()


def _pay_kb(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить", url=url)],
            [InlineKeyboardButton(text="⬅️ Другой тариф", callback_data="tariff:open")],
        ]
    )


async def _start_checkout(c: CallbackQuery, plan: str) -> None:
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    ensure_growth(user)

    if not yookassa_configured():
        contact = f"@{SUPPORT_USERNAME}" if SUPPORT_USERNAME else "поддержку"
        await c.answer()
        await c.message.answer(
            "Оплата пока настраивается. Напиши "
            f"{contact} и пришли ID <code>{c.from_user.id}</code> — "
            "активируем вручную.",
            parse_mode="HTML",
        )
        return

    price = plan_amount_for_user(user, plan)
    pct = 0
    if plan == PLAN_CHAT:
        _, pct = chat_price(user)
    else:
        _, pct = full_price(user)

    title = plan_title(plan)
    disc = f" (скидка {pct}%)" if pct else ""
    try:
        payment = create_payment(
            user_id=str(c.from_user.id),
            plan=plan,
            amount_rub=price,
            description=f"LexDAN: {title} на 30 дней",
            save_method=True,
        )
    except Exception:
        await c.answer("Не удалось создать платёж", show_alert=True)
        contact = f"@{SUPPORT_USERNAME}" if SUPPORT_USERNAME else "поддержку"
        await c.message.answer(
            f"Ошибка оплаты. Напиши {contact} или попробуй позже."
        )
        return

    url = confirmation_url(payment)
    if not url:
        await c.answer("Нет ссылки на оплату", show_alert=True)
        return

    user["yookassa_last_checkout_id"] = payment.get("id")
    save_users(users, only=str(c.from_user.id))

    await c.answer()
    await c.message.answer(
        f"💳 <b>{title} — {price}₽/мес</b>{disc}\n\n"
        f"{discount_blurb(user)}"
        "После оплаты подписка включится автоматически "
        "(обычно сразу, иногда до пары минут).\n"
        "Карта сохранится для <b>автопродления</b> — отменить можно кнопкой "
        "в профиле / подписке.\n\n"
        "Нажми «Оплатить» 👇",
        reply_markup=_pay_kb(url),
        parse_mode="HTML",
    )


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
    await _start_checkout(c, PLAN_CHAT)


@router.callback_query(F.data == "tariff:full")
async def tariff_full(c: CallbackQuery):
    await _start_checkout(c, PLAN_FULL)


@router.callback_query(F.data == "tariff:cancel_auto")
async def tariff_cancel_auto(c: CallbackQuery):
    ok = disable_autorenew(str(c.from_user.id))
    await c.answer("Автопродление выключено" if ok else "Уже выключено")
    if ok:
        await c.message.answer(
            "Автопродление отключено. Текущая подписка действует до конца оплаченного периода."
        )
