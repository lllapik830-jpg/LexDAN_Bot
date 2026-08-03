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
    """Кнопки с ценой оффера (HTML в кнопках нельзя)."""
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


def _is_paid_subscriber(user: dict) -> bool:
    """Реально платил через ЮKassa (не триал)."""
    if user.get("yookassa_last_payment_id"):
        return True
    if user.get("sub_plan") in ("chat", "full") and user.get(
        "yookassa_payment_method_id"
    ):
        return True
    return False


def is_trial_access_user(user: dict) -> bool:
    """
    Промокод / рег-триал / ручной грант премиума без оплаты.
    «premium дней ≈ 1» при 11ч — только отображение, на отбор не влияет.
    """
    ensure_growth(user)
    if _is_paid_subscriber(user):
        return False
    if user.get("in_promo_trial"):
        return True
    if user.get("promo_trial_code"):
        return True
    if user.get("reg_full_trial_granted"):
        return True
    # Премиум без следов оплаты = пробный доступ
    if is_premium(user):
        return True
    return False


def premium_seconds_left(user: dict) -> float:
    ensure_growth(user)
    return max(0.0, float(user.get("premium_until") or 0) - _now_ts())


def explain_eligibility(user: dict, *, ignore_sent: bool = False) -> tuple[bool, str]:
    """(ok, reason) — почему подходит / не подходит."""
    ensure_growth(user)
    left = premium_seconds_left(user)
    hours = left / 3600
    if _is_paid_subscriber(user):
        return False, "платный подписчик (ЮKassa), оффер только для триала"
    if not is_premium(user):
        return False, "премиум уже закончился"
    if user.get("tg_blocked"):
        return False, "пользователь заблокировал бота"
    if left <= 0:
        return False, "остаток ≤ 0"
    if left > MAX_LEFT_SEC:
        return (
            False,
            f"осталось ≈{hours:.1f} ч (>24 ч) — рано для оффера",
        )
    if not ignore_sent and user.get("trial_last_day_offer_sent") == _today_msk():
        return False, "уже отправляли сегодня"
    if not is_trial_access_user(user):
        return False, "не похож на триал-доступ"
    return True, f"ок, осталось ≈{hours:.1f} ч"


def eligible_for_last_day_offer(user: dict, *, ignore_sent: bool = False) -> bool:
    ok, _ = explain_eligibility(user, ignore_sent=ignore_sent)
    return ok


def apply_last_day_discount(user: dict) -> None:
    # Скидка живёт до конца дня ИЛИ до конца триала — что раньше
    until = end_of_today_msk_ts()
    prem = float(user.get("premium_until") or 0)
    if prem > _now_ts():
        until = min(until, prem)
    set_discount(
        user,
        OFFER_PERCENT,
        note=OFFER_NOTE,
        until_ts=until,
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


def scan_near_expiry(*, within_sec: float = MAX_LEFT_SEC) -> list[dict]:
    """Все с премиумом ≤ within_sec + причина eligibility."""
    from services.database import load_users, get_user
    from config import MANAGER_ID

    users = load_users()
    rows: list[dict] = []
    for uid, raw in (users or {}).items():
        if not isinstance(raw, dict) or str(uid).startswith("__"):
            continue
        if str(uid) == str(MANAGER_ID):
            continue
        user = get_user(users, str(uid))
        left = premium_seconds_left(user)
        if left <= 0 or left > within_sec:
            continue
        ok, reason = explain_eligibility(user)
        rows.append(
            {
                "uid": str(uid),
                "ok": ok,
                "reason": reason,
                "hours": left / 3600,
                "user": user,
            }
        )
    rows.sort(key=lambda r: r["hours"])
    return rows


def collect_last_day_offer_targets(*, force: bool = False) -> list[tuple[str, dict]]:
    out: list[tuple[str, dict]] = []
    for row in scan_near_expiry():
        ok, _ = explain_eligibility(row["user"], ignore_sent=force)
        if ok:
            out.append((row["uid"], row["user"]))
    return out


async def send_due_last_day_offers(bot, *, force: bool = False) -> dict:
    """Разослать оффер всем, у кого ≤24ч триала."""
    import asyncio

    from services.database import save_users

    near = scan_near_expiry()
    targets = collect_last_day_offer_targets(force=force)
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

    skipped = [
        f"{r['uid']} · {r['hours']:.1f}ч · {r['reason']}"
        for r in near
        if not r["ok"]
    ]
    return {
        "sent": sent,
        "fail": fail,
        "candidates": len(targets),
        "near": len(near),
        "skipped": skipped,
    }
