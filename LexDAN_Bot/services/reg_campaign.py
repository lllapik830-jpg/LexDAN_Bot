"""Акция при регистрации: 3 дня полного доступа (=799) + тексты для welcome."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

MSK = timezone(timedelta(hours=3))

# Акция для новых регистраций: полный доступ на 3 дня.
REG_FULL_TRIAL_DAYS = 3
# None = бессрочно для всех новых; иначе дата окончания (МСК).
REG_FULL_TRIAL_END: datetime | None = None

# Разовый грант + DM (список от менеджера, авг 2026).
BATCH_3D_USER_IDS: list[str] = [
    "5153509214",  # Настя
    "8587548079",  # Amiri
    "2129005517",  # Dasha
    "505311211",  # Алекс
    "7994178868",  # Светлана
    "1708621212",  # Анна
    "6177018223",  # Покиза
    "548452736",  # Любовь
    "6275142565",  # Ayau
    "1034188102",  # Женя
    "5609411474",  # Петр
    "6302495155",  # Айдана
    "938681037",  # Алина
]
BATCH_3D_DM_FLAG = "reg_3d_batch_dm_v1"

BATCH_3D_DM_HTML = (
    "🦜 <b>Отличная новость!</b>\n\n"
    "Вам предоставлен <b>безлимит на 3 дня</b> — полный доступ "
    "как на тарифе <b>799₽</b>.\n"
    "Пользуйтесь всеми функциями: уроки без лимита, Listening, "
    "голоса и общение 💚\n\n"
    "Через 3 дня доступ вернётся к бесплатному режиму. "
    "В последний день напомню, если захотите продолжить на выгодных условиях."
)


def now_msk() -> datetime:
    return datetime.now(MSK)


def is_reg_full_trial_active(at: datetime | None = None) -> bool:
    if REG_FULL_TRIAL_END is None:
        return True
    t = at or now_msk()
    return t < REG_FULL_TRIAL_END


def grant_reg_full_trial(
    user: dict, *, days: int | None = None, force: bool = False
) -> bool:
    """
    Выдать N дней полного доступа (=799).
    force=True — выдать снова (для ручного батча), даже если флаг уже стоял.
    """
    from services.growth import ensure_growth, start_trial

    ensure_growth(user)
    # не трогаем тех, кто реально оплатил подписку
    if user.get("yookassa_last_payment_id") or (
        user.get("sub_plan") in ("chat", "full")
        and user.get("yookassa_payment_method_id")
    ):
        return False
    if user.get("reg_full_trial_granted") and not force:
        return False

    n = int(days if days is not None else REG_FULL_TRIAL_DAYS)
    start_trial(user, days=n)
    user["reg_full_trial_granted"] = True
    user["in_promo_trial"] = True
    user["trial_end_notified"] = False
    user["promo_listening"] = True
    user["reg_full_trial_days"] = n
    return True


def grant_reg_full_trial_if_active(user: dict) -> bool:
    """Выдать 3 дня полного доступа один раз при регистрации (если акция жива)."""
    if not is_reg_full_trial_active():
        return False
    return grant_reg_full_trial(user, force=False)


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


async def deliver_batch_3d_trials(bot) -> dict:
    """
    Разовый грант 3 дней + DM списку пользователей.
    Идемпотентно: повторно не шлёт, если уже отмечен BATCH_3D_DM_FLAG.
    """
    from services.database import get_user, save_users, users_for
    from services.growth import ensure_growth

    sent = 0
    granted = 0
    skipped = 0
    fail = 0
    for uid in BATCH_3D_USER_IDS:
        try:
            users = users_for(uid)
            user = get_user(users, uid)
            ensure_growth(user)
            if user.get(BATCH_3D_DM_FLAG):
                skipped += 1
                continue
            if grant_reg_full_trial(user, days=REG_FULL_TRIAL_DAYS, force=True):
                granted += 1
            try:
                await bot.send_message(
                    int(uid), BATCH_3D_DM_HTML, parse_mode="HTML"
                )
                sent += 1
            except Exception:
                fail += 1
            user[BATCH_3D_DM_FLAG] = True
            save_users(users, only=uid)
        except Exception:
            fail += 1
    return {
        "granted": granted,
        "sent": sent,
        "skipped": skipped,
        "fail": fail,
        "total": len(BATCH_3D_USER_IDS),
    }