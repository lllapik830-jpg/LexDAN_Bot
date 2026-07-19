"""
Цены со скидкой + розыгрыши (билеты из streak / рефералки).
"""

from __future__ import annotations

import random
import time
from datetime import datetime, timedelta, timezone

from services.growth import PRICE_CHAT_MONTH, PRICE_FULL_MONTH, ensure_growth

MSK = timezone(timedelta(hours=3))

LOTTERY_30_PRIZE = "6 месяцев полного доступа (799)"
LOTTERY_100_PRIZE = "15 000₽"
LOTTERY_REF_PRIZE = "бонусный месяц полного доступа"


def _today() -> str:
    return datetime.now(MSK).date().isoformat()


def _now_ts() -> float:
    return time.time()


def discount_percent(user: dict) -> int:
    ensure_growth(user)
    return max(0, min(90, int(user.get("discount_percent") or 0)))


def price_with_discount(base: int, user: dict) -> tuple[int, int]:
    """Возвращает (итоговая цена, процент скидки)."""
    pct = discount_percent(user)
    if pct <= 0:
        return base, 0
    return max(1, int(round(base * (100 - pct) / 100))), pct


def chat_price(user: dict) -> tuple[int, int]:
    return price_with_discount(PRICE_CHAT_MONTH, user)


def full_price(user: dict) -> tuple[int, int]:
    return price_with_discount(PRICE_FULL_MONTH, user)


def discount_blurb(user: dict) -> str:
    pct = discount_percent(user)
    if pct <= 0:
        return ""
    chat, _ = chat_price(user)
    full, _ = full_price(user)
    note = user.get("discount_note") or "награда"
    return (
        f"\n🏷 <b>Твоя скидка {pct}%</b> ({note})\n"
        f"• Общение: <s>{PRICE_CHAT_MONTH}₽</s> → <b>{chat}₽</b>\n"
        f"• Всё: <s>{PRICE_FULL_MONTH}₽</s> → <b>{full}₽</b>\n"
        "Скажи про скидку поддержке при оплате — активируем по этой цене.\n"
    )


def set_discount(user: dict, percent: int, note: str = "admin") -> None:
    ensure_growth(user)
    user["discount_percent"] = max(0, min(90, int(percent)))
    user["discount_note"] = note
    user["discount_set_at"] = _today()


def clear_discount(user: dict) -> None:
    user["discount_percent"] = 0
    user["discount_note"] = ""


def consume_discount(user: dict) -> int:
    """Списать скидку после оплаты. Возвращает какой % был."""
    pct = discount_percent(user)
    if pct:
        clear_discount(user)
        user["discount_last_used_at"] = _today()
        user["discount_last_used_percent"] = pct
    return pct


# ─── лотереи ───────────────────────────────────────────────


def lottery_status_lines(user: dict) -> str:
    ensure_growth(user)
    bits = []
    if user.get("lottery_30"):
        bits.append(
            f"🎟 Розыгрыш «30 дней» (полугодовая подписка) — в игре"
            f" с {user.get('lottery_30_entered_at') or '—'}"
        )
    if user.get("lottery_100"):
        bits.append(
            f"🎟 Розыгрыш «100 дней» (15 000₽) — в игре"
            f" с {user.get('lottery_100_entered_at') or '—'}"
        )
    tickets = int(user.get("referral_lottery_tickets") or 0)
    if tickets:
        bits.append(f"🎟 Реф-билеты: <b>{tickets}</b>")
    if not bits:
        return ""
    return "\n" + "\n".join(bits) + "\n"


def list_lottery_30(users: dict) -> list[tuple[str, dict]]:
    out = []
    for uid, u in users.items():
        if isinstance(u, dict) and u.get("lottery_30"):
            out.append((str(uid), u))
    return out


def list_lottery_100(users: dict) -> list[tuple[str, dict]]:
    out = []
    for uid, u in users.items():
        if isinstance(u, dict) and u.get("lottery_100"):
            out.append((str(uid), u))
    return out


def list_referral_ticket_pool(users: dict) -> list[tuple[str, dict]]:
    """Каждый билет = отдельный слот (uid может повторяться)."""
    pool: list[tuple[str, dict]] = []
    for uid, u in users.items():
        if not isinstance(u, dict):
            continue
        n = int(u.get("referral_lottery_tickets") or 0)
        for _ in range(max(0, n)):
            pool.append((str(uid), u))
    return pool


def draw_lottery_30(users: dict) -> tuple[str, dict] | None:
    entrants = list_lottery_30(users)
    if not entrants:
        return None
    uid, user = random.choice(entrants)
    user["lottery_30"] = False
    user["lottery_30_won_at"] = _today()
    from services.growth import extend_premium

    extend_premium(user, 180)  # ~6 месяцев
    return uid, user


def draw_lottery_100(users: dict) -> tuple[str, dict] | None:
    entrants = list_lottery_100(users)
    if not entrants:
        return None
    uid, user = random.choice(entrants)
    user["lottery_100"] = False
    user["lottery_100_won_at"] = _today()
    user["lottery_100_prize_pending"] = True  # деньги вручную
    return uid, user


def draw_referral_lottery(users: dict) -> tuple[str, dict] | None:
    pool = list_referral_ticket_pool(users)
    if not pool:
        return None
    uid, user = random.choice(pool)
    # списать один билет у победителя
    left = max(0, int(user.get("referral_lottery_tickets") or 0) - 1)
    user["referral_lottery_tickets"] = left
    user["referral_lottery_won_at"] = _today()
    from services.growth import extend_premium

    extend_premium(user, 30)
    return uid, user
