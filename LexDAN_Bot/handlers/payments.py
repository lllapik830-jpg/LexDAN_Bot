"""Оплата тарифов через ЮKassa + автопродление."""

from __future__ import annotations

import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.lesson_keyboards import tariffs_inline_kb
from services.growth import subscription_blurb, ensure_growth
from services.database import load_users, get_user, save_users
from services.pricing import chat_price, discount_blurb, full_price
from services.yookassa_pay import (
    PLAN_CHAT,
    PLAN_FULL,
    PLAN_UPGRADE,
    confirmation_url,
    create_payment,
    disable_autorenew,
    plan_amount_for_user,
    plan_title,
    yookassa_configured,
)
from config import SUPPORT_USERNAME

router = Router()
log = logging.getLogger(__name__)


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

    if plan == PLAN_UPGRADE:
        from services.rewards import user_plan

        if user_plan(user) != "chat":
            await c.answer(
                "Апгрейд доступен на тарифе «Общение» (399₽).",
                show_alert=True,
            )
            return

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
    elif plan == PLAN_UPGRADE:
        from services.pricing import upgrade_price

        _, pct = upgrade_price(user)
    else:
        _, pct = full_price(user)

    title = plan_title(plan)
    disc = f" (скидка {pct}%)" if pct else ""
    from services.sept_promo import is_sept_promo_active

    promo_any = is_sept_promo_active()
    if plan == PLAN_UPGRADE:
        if promo_any:
            description = "LexDAN: апгрейд до полного доступа до 30.09"
            pay_blurb = (
                f"💳 <b>Апгрейд — {price}₽</b>{disc}\n\n"
                "Доплата с тарифа «Общение» до полного доступа "
                "по акции — до <b>30.09</b> включительно:\n"
                "• безлимит уроков\n"
                "• все голоса и 150 тем\n"
                "• премиальные награды серии\n\n"
                "В чеке ЮKassa будет комментарий <b>«апгрейд»</b>.\n\n"
                "Нажми «Оплатить» 👇"
            )
        else:
            description = "LexDAN: апгрейд до полного доступа на 30 дней"
            pay_blurb = (
                f"💳 <b>Апгрейд — {price}₽</b>{disc}\n\n"
                "Доплата с тарифа «Общение» до полного доступа на 30 дней:\n"
                "• безлимит уроков\n"
                "• все голоса и 150 тем\n"
                "• премиальные награды серии\n\n"
                "В чеке ЮKassa будет комментарий <b>«апгрейд»</b>, не «общение».\n\n"
                "Нажми «Оплатить» 👇"
            )
    elif promo_any:
        description = f"LexDAN: {title} до 30.09 (акция)"
        pay_blurb = (
            f"💳 <b>{title} — {price}₽</b>{disc}\n"
            "🦜 Акция к 1 сентября: доступ до <b>30.09</b> включительно\n\n"
            f"{discount_blurb(user)}"
            "После оплаты подписка включится автоматически "
            "(обычно сразу, иногда до пары минут).\n"
            "Карта сохранится для <b>автопродления</b> после акции "
            "(по обычной цене) — отменить можно в профиле.\n\n"
            "Нажми «Оплатить» 👇"
        )
    else:
        description = f"LexDAN: {title} на 30 дней"
        pay_blurb = (
            f"💳 <b>{title} — {price}₽/мес</b>{disc}\n\n"
            f"{discount_blurb(user)}"
            "После оплаты подписка включится автоматически "
            "(обычно сразу, иногда до пары минут).\n"
            "Карта сохранится для <b>автопродления</b> — отменить списания можно кнопкой "
            "в профиле / подписке.\n\n"
            "Нажми «Оплатить» 👇"
        )

    try:
        payment = create_payment(
            user_id=str(c.from_user.id),
            plan=plan,
            amount_rub=price,
            description=description,
            save_method=True,
        )
    except Exception as e:
        log.exception("Checkout failed")
        detail = str(e).strip() or "unknown"
        if len(detail) > 180:
            detail = detail[:177] + "…"
        await c.answer("Не удалось создать платёж", show_alert=True)
        contact = f"@{SUPPORT_USERNAME}" if SUPPORT_USERNAME else "поддержку"
        await c.message.answer(
            "❌ <b>Ошибка оплаты</b>\n"
            f"<code>{detail}</code>\n\n"
            "Проверь shopId/секретный ключ в Render Environment "
            f"или напиши {contact}.",
            parse_mode="HTML",
        )
        return

    url = confirmation_url(payment)
    if not url:
        await c.answer("Нет ссылки на оплату", show_alert=True)
        return

    user["yookassa_last_checkout_id"] = payment.get("id")
    save_users(users, only=str(c.from_user.id))

    await c.answer()
    kb = _pay_kb(url)
    if plan == PLAN_UPGRADE:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить апгрейд", url=url)],
            ]
        )
    await c.message.answer(
        pay_blurb,
        reply_markup=kb,
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


@router.callback_query(F.data == "tariff:upgrade")
async def tariff_upgrade(c: CallbackQuery):
    await _start_checkout(c, PLAN_UPGRADE)


@router.callback_query(F.data == "tariff:cancel_auto")
async def tariff_cancel_auto(c: CallbackQuery):
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    ensure_growth(user)
    if not (user.get("sub_auto") and user.get("yookassa_payment_method_id")):
        await c.answer("Автосписания уже выключены", show_alert=True)
        return
    await c.answer()
    await c.message.answer(
        "🦜 <b>Отмена автосписаний</b>\n\n"
        "Если вы отмените списания, следующая подписка "
        "<b>не будет активирована автоматически</b>.\n\n"
        "После окончания текущей подписки вы автоматически перейдёте "
        "на <b>бесплатный тариф</b> с дневными лимитами и "
        "<b>ограниченными призами</b> за серию дней.\n\n"
        "Текущий оплаченный период продолжит действовать до конца срока.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⏹ Отменить подписку",
                        callback_data="tariff:cancel_ask",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Оставить как есть",
                        callback_data="tariff:cancel_abort",
                    )
                ],
            ]
        ),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "tariff:cancel_abort")
async def tariff_cancel_abort(c: CallbackQuery):
    await c.answer("Ок, подписка без изменений")
    try:
        await c.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass


def _sad_rico_path() -> str | None:
    from pathlib import Path

    here = Path(__file__).resolve().parent.parent
    for name in ("rico_sad_cancel.png", "stickers/sticker_06_sad.png"):
        p = here / "assets" / name
        if p.is_file():
            return str(p)
    return None


@router.callback_query(F.data == "tariff:cancel_ask")
async def tariff_cancel_ask(c: CallbackQuery):
    from aiogram.types import FSInputFile

    users = load_users()
    user = get_user(users, str(c.from_user.id))
    ensure_growth(user)
    if not (user.get("sub_auto") and user.get("yookassa_payment_method_id")):
        await c.answer("Автосписания уже выключены", show_alert=True)
        return
    await c.answer()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Уверен",
                    callback_data="tariff:cancel_confirm",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Не отменять",
                    callback_data="tariff:cancel_abort",
                )
            ],
        ]
    )
    photo = _sad_rico_path()
    caption = (
        "🦜 <b>Рико:</b> Вы уверены?\n\n"
        "Отменить это действие потом <b>нельзя</b> будет — "
        "автосписания выключатся.\n\n"
        "Текущая подписка до конца оплаченного периода останется."
    )
    if photo:
        await c.message.answer_photo(
            photo=FSInputFile(photo),
            caption=caption,
            reply_markup=kb,
            parse_mode="HTML",
        )
    else:
        await c.message.answer(caption, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "tariff:cancel_confirm")
async def tariff_cancel_confirm(c: CallbackQuery):
    ok = disable_autorenew(str(c.from_user.id))
    await c.answer("Автосписания выключены" if ok else "Уже выключено")
    try:
        await c.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    if ok:
        await c.message.answer(
            "✅ Автосписания отключены.\n\n"
            "Текущая подписка действует до конца оплаченного периода. "
            "Дальше — бесплатный тариф с лимитами."
        )
