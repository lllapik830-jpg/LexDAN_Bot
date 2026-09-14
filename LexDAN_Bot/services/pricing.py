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
    until = float(user.get("discount_until") or 0)
    if until and until <= _now_ts():
        # Срок скидки вышел — сбрасываем
        user["discount_percent"] = 0
        user["discount_note"] = ""
        user["discount_until"] = 0
        return 0
    return max(0, min(90, int(user.get("discount_percent") or 0)))


def price_with_discount(base: int, user: dict) -> tuple[int, int]:
    """Возвращает (итоговая цена, процент скидки)."""
    pct = discount_percent(user)
    if pct <= 0:
        return base, 0
    return max(1, int(round(base * (100 - pct) / 100))), pct


def chat_price(user: dict) -> tuple[int, int]:
    return price_with_discount(int(PRICE_CHAT_MONTH), user)


def full_price(user: dict) -> tuple[int, int]:
    from services.promo import lifetime_full_price_rub

    # Персональная вечная цена важнее каталога
    locked = lifetime_full_price_rub(user)
    if locked is not None:
        return int(locked), 0
    return price_with_discount(int(PRICE_FULL_MONTH), user)


def upgrade_price(user: dict) -> tuple[int, int]:
    """Доплата с тарифа «Общение» до полного (= цена «общения» + скидка)."""
    return price_with_discount(int(PRICE_CHAT_MONTH), user)


def catalog_price_lines_html() -> str:
    """Блок цены для экрана подписки — один тариф «Безлимит»."""
    return (
        f"<b>🚀 Безлимит</b> — <b>{PRICE_FULL_MONTH}₽/мес</b>\n"
        "• все разделы уроков без ограничений\n"
        "• Огонь дня: все 4 искры\n"
        "• общение с Рико безлимит\n"
        "• Живая речь\n"
        "• все голоса озвучки\n"
        "• рейтинг недели, стрик-награды, ранний доступ\n\n"
    )


def discount_blurb(user: dict) -> str:
    from services.promo import has_lifetime_full_price, lifetime_full_price_rub

    if has_lifetime_full_price(user):
        rub = lifetime_full_price_rub(user) or 399
        return (
            f"\n🏷 <b>Персональная цена навсегда:</b> безлимит "
            f"<b>{rub}₽/мес</b>\n"
        )

    pct = discount_percent(user)
    if pct <= 0:
        return ""

    full, _ = full_price(user)
    note = user.get("discount_note") or "награда"
    return (
        f"\n🏷 <b>Твоя скидка {pct}%</b> ({note})\n"
        f"• Безлимит: <s>{PRICE_FULL_MONTH}₽</s> → <b>{full}₽</b>\n"
        "Скидка учтётся при оплате через бота.\n"
    )


def set_discount(
    user: dict,
    percent: int,
    note: str = "admin",
    *,
    until_ts: float | None = None,
) -> None:
    ensure_growth(user)
    user["discount_percent"] = max(0, min(90, int(percent)))
    user["discount_note"] = note
    user["discount_set_at"] = _today()
    if until_ts is not None:
        user["discount_until"] = float(until_ts)
    elif "discount_until" not in user:
        user["discount_until"] = 0.0


def clear_discount(user: dict) -> None:
    user["discount_percent"] = 0
    user["discount_note"] = ""
    user["discount_until"] = 0.0


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
        if str(uid).startswith("__") or not isinstance(u, dict):
            continue
        if u.get("imitating_registration"):
            continue
        if u.get("lottery_30"):
            out.append((str(uid), u))
    return out


def list_lottery_100(users: dict) -> list[tuple[str, dict]]:
    out = []
    for uid, u in users.items():
        if str(uid).startswith("__") or not isinstance(u, dict):
            continue
        if u.get("imitating_registration"):
            continue
        if u.get("lottery_100"):
            out.append((str(uid), u))
    return out


def list_referral_ticket_pool(users: dict) -> list[tuple[str, dict]]:
    """Каждый билет = отдельный слот (uid может повторяться)."""
    pool: list[tuple[str, dict]] = []
    for uid, u in users.items():
        if str(uid).startswith("__") or not isinstance(u, dict):
            continue
        if u.get("imitating_registration"):
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


def clear_lottery_100_prize(user: dict) -> bool:
    """Отметить, что денежный приз 100-дневной лотереи выплачен."""
    if not user.get("lottery_100_prize_pending"):
        return False
    user["lottery_100_prize_pending"] = False
    user["lottery_100_prize_paid_at"] = _today()
    return True


def pending_lottery_100_prizes(users: dict) -> list[tuple[str, dict]]:
    out = []
    for uid, u in users.items():
        if str(uid).startswith("__") or not isinstance(u, dict):
            continue
        if u.get("imitating_registration"):
            continue
        if u.get("lottery_100_prize_pending"):
            out.append((str(uid), u))
    return out
