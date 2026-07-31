"""Акция при регистрации: 3 дня полного доступа (=799) + тексты для welcome."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

MSK = timezone(timedelta(hours=3))

# Акция для новых регистраций (реклама). Конец: 04.08.2026 00:00 МСК.
REG_FULL_TRIAL_DAYS = 3
REG_FULL_TRIAL_END = datetime(2026, 8, 4, 0, 0, 0, tzinfo=MSK)


def now_msk() -> datetime:
    return datetime.now(MSK)


def is_reg_full_trial_active(at: datetime | None = None) -> bool:
    t = at or now_msk()
    return t < REG_FULL_TRIAL_END


def grant_reg_full_trial_if_active(user: dict) -> bool:
    """
    Выдать 3 дня полного доступа (= тариф 799) один раз при регистрации.
    True — выдали сейчас.
    """
    if not is_reg_full_trial_active():
        return False
    if user.get("reg_full_trial_granted"):
        return False
    from services.growth import ensure_growth, start_trial

    ensure_growth(user)
    start_trial(user, days=REG_FULL_TRIAL_DAYS)
    user["reg_full_trial_granted"] = True
    user["in_promo_trial"] = True
    user["reg_full_trial_days"] = REG_FULL_TRIAL_DAYS
    return True


def reg_full_trial_welcome_html() -> str:
    if not is_reg_full_trial_active():
        return ""
    return (
        "\n\n🎁 <b>Подарок при регистрации</b>\n"
        f"Тебе открыт <b>полный доступ</b> как на тарифе <b>799₽</b> "
        f"на <b>{REG_FULL_TRIAL_DAYS} дня</b>: уроки без лимита, Listening, "
        "все голоса и общение.\n"
        "Успей попробовать всё 🚀"
    )


def reg_event_welcome_html() -> str:
    """Пока идёт ивент «Магические элементы» — блок во вступительном тексте."""
    try:
        from services.event_magic import is_event_active, EVENT_TITLE, EVENT_END
    except Exception:
        return ""
    if not is_event_active():
        return ""
    end_label = EVENT_END.strftime("%d.%m")
    return (
        f"\n\n✨ <b>Сейчас идёт ивент «{EVENT_TITLE}»!</b>\n"
        "Открывай магические карточки за задания, копи баллы и "
        "выигрывай ценные призы.\n"
        f"⏰ До <b>{end_label} 00:00</b> (МСК).\n"
        "📋 Правила и призы — в канале: https://t.me/LexDan_Rico\n"
        "Успей открывать карточки, пока ивент жив 🎴🏆"
    )
