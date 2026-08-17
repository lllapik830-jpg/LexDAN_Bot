"""
Акция к 1 сентября 2026:
  покупка до 31.08 включительно → цены 549 / 279,
  доступ до 30.09 включительно.
После окна акции — снова 799 / 399 и обычные +30 дней.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

MSK = timezone(timedelta(hours=3))

# Каталог (обычные цены) — не меняем константы growth.PRICE_*
PROMO_CHAT_RUB = 279
PROMO_FULL_RUB = 549

# Покупка по акции: до конца 31.08.2026 МСК
_PROMO_BUY_UNTIL = datetime(2026, 8, 31, 23, 59, 59, tzinfo=MSK)
# Доступ включительно 30.09 → истекает в 00:00 01.10 МСК
_PROMO_ACCESS_UNTIL = datetime(2026, 10, 1, 0, 0, 0, tzinfo=MSK)

PROMO_META_KEY = "sept2026"


def is_sept_promo_active(now: datetime | None = None) -> bool:
    now = now or datetime.now(MSK)
    if now.tzinfo is None:
        now = now.replace(tzinfo=MSK)
    return now <= _PROMO_BUY_UNTIL


def sept_promo_access_until_ts() -> float:
    return _PROMO_ACCESS_UNTIL.timestamp()


def catalog_chat_rub() -> int:
    from services.growth import PRICE_CHAT_MONTH

    return PROMO_CHAT_RUB if is_sept_promo_active() else int(PRICE_CHAT_MONTH)


def catalog_full_rub() -> int:
    from services.growth import PRICE_FULL_MONTH

    return PROMO_FULL_RUB if is_sept_promo_active() else int(PRICE_FULL_MONTH)


def promo_price_lines_html() -> str:
    """Блок цен для экрана подписки (HTML)."""
    from services.growth import PRICE_CHAT_MONTH, PRICE_FULL_MONTH

    if not is_sept_promo_active():
        return (
            f"<b>💬 Только общение</b> — <b>{PRICE_CHAT_MONTH}₽/мес</b>\n"
            "• безлимит чата (текст + голос)\n"
            "• апгрейд до полного — доплата в профиле\n\n"
            f"<b>🚀 Безлимит ко всему</b> — <b>{PRICE_FULL_MONTH}₽/мес</b>\n"
            "• уроки без лимита (включая Живую речь)\n"
            "• безлимит общения\n\n"
        )
    return (
        "🦜 <b>Акция к 1 сентября</b> — до <b>31.08</b>\n"
        f"📅 Оформи сейчас → доступ до <b>30.09</b> включительно\n\n"
        f"<b>💬 Только общение</b> — <s>{PRICE_CHAT_MONTH}₽</s> → <b>{PROMO_CHAT_RUB}₽</b>\n"
        "• безлимит чата (текст + голос)\n"
        "• апгрейд до полного — доплата в профиле\n\n"
        f"<b>🚀 Безлимит ко всему</b> — <s>{PRICE_FULL_MONTH}₽</s> → <b>{PROMO_FULL_RUB}₽</b>\n"
        "• уроки без лимита (включая Живую речь)\n"
        "• безлимит общения\n\n"
        f"После 31.08 цены вернутся к {PRICE_CHAT_MONTH}₽ и {PRICE_FULL_MONTH}₽.\n\n"
    )
