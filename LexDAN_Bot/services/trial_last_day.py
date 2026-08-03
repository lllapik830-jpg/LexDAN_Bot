"""
Оффер последнего дня триала: −15% до конца дня (МСК).
399 → 340, 799 → 680.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta, timezone

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services.growth import (
    PRICE_CHAT_MONTH,
    PRICE_FULL_MONTH,
    ensure_growth,
    is_premium,
)
from services.pricing import set_discount

log = logging.getLogger(__name__)

MSK = timezone(timedelta(hours=3))

OFFER_PERCENT = 15
# Явные цены под 15% (округление как в ТЗ)
PRICE_CHAT_OFFER = 340
PRICE_FULL_OFFER = 680
OFFER_NOTE = "last_day_trial"
MAX_LEFT_SEC = 24 * 3600


def _now_ts() -> float:
    return time.time()


def _today_msk() -> str:
    return datetime.now(MSK).date().isoformat()


def end_of_today_msk_ts() -> float:
    now = datetime.now(MSK)
    end = datetime(
        now.year, now.month, now.day, 23, 59, 59, tzinfo=MSK
    )
    return end.timestamp()


def trial_offer_html() -> str:
    return (
        "🦜 <b>Эй, друг!</b>\n\n"
        "Сегодня — <b>последний день</b> твоего бесплатного премиального доступа.\n"
        "С завтрашнего дня ты возвращаешься на бесплатный тариф… "
        "но можешь оформить подписку и дальше пользоваться ботом на полную 💚\n\n"
        "🎁 <b>Специально для тебя — только сегодня:</b>\n"
        "если до конца дня оформишь подписку на месяц — скидка <b>15%</b>:\n\n"
        "🚀 Полная библиотека знаний:\n"
        f"<s>{PRICE_FULL_MONTH}₽</s> → <b>{PRICE_FULL_OFFER}₽</b> / мес\n\n"
        "💬 Безлимитное общение:\n"
        f"<s>{PRICE_CHAT_MONTH}₽</s> → <b>{PRICE_CHAT_OFFER}₽</b> / мес\n\n"
        "Успей воспользоваться скидкой <b>сегодня</b> — "
        "другого такого шанса не будет ⏳"
    )


def trial_offer_kb() -> InlineKeyboardMarkup:
    """Кнопки с перечёркнутой старой ценой в тексте (HTML в кнопках нельзя)."""
    chat_btn = (
        f"💬 Общение — {PRICE_CHAT_OFFER}₽  "
        f"(было {PRICE_CHAT_MONTH})"
    )
    full_btn = (
        f"🚀 Полный — {PRICE_FULL_OFFER}₽  "
        f"(было {PRICE_FULL_MONTH})"
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=chat_btn, callback_data="tariff:chat")],
            [InlineKeyboardButton(text=full_btn, callback_data="tariff:full")],
        ]
    )


def is_trial_access_user(user: dict) -> bool:
    """Промокод / 3-дневный рег-триал (не оплативший подписку)."""
    ensure_growth(user)
    if user.get("sub_plan") in ("chat", "full", "upgrade"):
        return False
    if user.get("in_promo_trial"):
        return True
    if user.get("promo_trial_code") and is_premium(user):
        return True
    if user.get("reg_full_trial_granted") and is_premium(user):
        return True
    return False


def premium_seconds_left(user: dict) -> float:
    ensure_growth(user)
    return max(0.0, float(user.get("premium_until") or 0) - _now_ts())


def eligible_for_last_day_offer(user: dict, *, ignore_sent: bool = False) -> bool:
    if not is_trial_access_user(user):
        return False
    if not is_premium(user):
        return False
    if user.get("tg_blocked"):
        return False
    left = premium_seconds_left(user)
    if left <= 0 or left > MAX_LEFT_SEC:
        return False
    if not ignore_sent and user.get("trial_last_day_offer_sent") == _today_msk():
        return False
    return True


def apply_last_day_discount(user: dict) -> None:
    set_discount(
        user,
        OFFER_PERCENT,
        note=OFFER_NOTE,
        until_ts=end_of_today_msk_ts(),
    )
    user["trial_last_day_offer_sent"] = _today_msk()


async def send_last_day_offer(bot, chat_id: int, user: dict) -> None:
    apply_last_day_discount(user)
    await bot.send_message(
        chat_id,
        trial_offer_html(),
        reply_markup=trial_offer_kb(),
        parse_mode="HTML",
    )


def collect_last_day_offer_targets() -> list[tuple[str, dict]]:
    from services.database import load_users, get_user
    from config import MANAGER_ID

    users = load_users()
    out: list[tuple[str, dict]] = []
    for uid, raw in (users or {}).items():
        if not isinstance(raw, dict) or str(uid).startswith("__"):
            continue
        if str(uid) == str(MANAGER_ID):
            continue
        user = get_user(users, str(uid))
        if eligible_for_last_day_offer(user):
            out.append((str(uid), user))
    return out


async def send_due_last_day_offers(bot) -> dict:
    """Разослать оффер всем, у кого ≤24ч триала и ещё не слали сегодня."""
    import asyncio

    from services.database import save_users

    targets = collect_last_day_offer_targets()
    sent = 0
    fail = 0
    for uid, user in targets:
        try:
            await send_last_day_offer(bot, int(uid), user)
            save_users({uid: user}, only=uid)
            sent += 1
        except Exception as e:
            log.warning("last-day offer fail uid=%s: %s", uid, e)
            fail += 1
        await asyncio.sleep(0.05)
    return {"sent": sent, "fail": fail, "candidates": len(targets)}
