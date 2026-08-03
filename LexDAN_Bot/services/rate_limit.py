"""
Антифлуд: максимум N апдейтов (текст/кнопки/голос) в минуту на пользователя.

При превышении — кулдаун 2 минуты + предупреждение.
3 срабатывания за час → временный бан.
Админ (MANAGER_ID) не ограничивается.
"""

from __future__ import annotations

import logging
import time
from typing import Any

log = logging.getLogger(__name__)

MAX_PER_MINUTE = 20
WINDOW_SEC = 60.0
COOLDOWN_SEC = 120.0  # 2 минуты
STRIKES_FOR_BAN = 3
STRIKE_WINDOW_SEC = 3600.0  # 1 час
FLOOD_BAN_SEC = 2 * 3600.0  # бан на 2 часа

# Скользящее окно в памяти процесса (быстро); кулдаун/страйки/бан — в user в БД
_msg_times: dict[str, list[float]] = {}
_last_warn_at: dict[str, float] = {}


WARN_HTML = (
    "🦜 <b>Воу-воу, притормози-ка</b>\n\n"
    "Ты слишком быстро работаешь… или пытаешься сломать сервер? 😏\n"
    "Подожди <b>2 минуты</b> — и сможешь продолжить.\n\n"
    f"Если повторишь такое <b>{STRIKES_FOR_BAN} раза за час</b> — "
    "улетишь в бан.\n"
    "Обычный пользователь так много в минуту не пишет )))"
)

FLOOD_BAN_HTML = (
    "🚫 <b>Бан за флуд / попытку положить бота</b>\n\n"
    "Слишком много сообщений слишком часто.\n"
    "Обычный ученик так не пишет — а вот скрипты любят.\n\n"
    "Блокировка на <b>2 часа</b>. Потом можно снова учиться 💚"
)


def _now() -> float:
    return time.time()


def ensure_rate_fields(user: dict) -> dict:
    user.setdefault("rate_cooldown_until", 0.0)
    user.setdefault("rate_strikes", [])
    user.setdefault("ban_reason", "")
    return user


def _prune_strikes(user: dict, now: float) -> list[float]:
    ensure_rate_fields(user)
    raw = user.get("rate_strikes") or []
    if not isinstance(raw, list):
        raw = []
    kept = [float(t) for t in raw if now - float(t) <= STRIKE_WINDOW_SEC]
    user["rate_strikes"] = kept
    return kept


def flood_ban_remaining_text(user: dict) -> str:
    from datetime import datetime, timedelta, timezone

    MSK = timezone(timedelta(hours=3))
    until = float(user.get("banned_until") or 0)
    left = max(0, int(until - _now()))
    hours = left // 3600
    mins = (left % 3600) // 60
    when = datetime.fromtimestamp(until, MSK).strftime("%d.%m %H:%M")
    return (
        f"🚫 Аккаунт временно заблокирован до <b>{when}</b> (МСК).\n"
        f"Осталось примерно {hours} ч {mins} мин.\n\n"
        "Причина: флуд / слишком частые сообщения (защита от DDoS)."
    )


def check_and_touch(user_id: str, user: dict) -> dict[str, Any]:
    """
    Учесть один апдейт от пользователя.

    Returns dict:
      allow: bool
      notify: str | None  — HTML сообщение пользователю (если нужно)
      persist: bool — нужно сохранить user в БД
    """
    from config import MANAGER_ID
    from services.moderation import is_banned

    uid = str(user_id)
    if uid == str(MANAGER_ID):
        return {"allow": True, "notify": None, "persist": False}

    ensure_rate_fields(user)
    now = _now()

    # Уже в бане (маты или флуд)
    if is_banned(user):
        reason = (user.get("ban_reason") or "").strip()
        if reason == "flood":
            notify = flood_ban_remaining_text(user)
        else:
            from services.moderation import ban_remaining_text

            notify = ban_remaining_text(user)
        last = float(_last_warn_at.get(uid) or 0)
        if now - last >= 30:
            _last_warn_at[uid] = now
            return {"allow": False, "notify": notify, "persist": False}
        return {"allow": False, "notify": None, "persist": False}

    cooldown_until = float(user.get("rate_cooldown_until") or 0)
    if cooldown_until > now:
        # В кулдауне — молча режем; раз в 30с можно напомнить
        last = float(_last_warn_at.get(uid) or 0)
        left = max(1, int(cooldown_until - now))
        if now - last >= 30:
            _last_warn_at[uid] = now
            return {
                "allow": False,
                "notify": (
                    f"🦜 Ещё подожди <b>{left} сек</b> — "
                    "потом снова можно писать."
                ),
                "persist": False,
            }
        return {"allow": False, "notify": None, "persist": False}

    # Кулдаун истёк — подчистим поле
    persist = False
    if cooldown_until and cooldown_until <= now:
        user["rate_cooldown_until"] = 0.0
        persist = True

    times = _msg_times.setdefault(uid, [])
    times[:] = [t for t in times if now - t < WINDOW_SEC]
    times.append(now)

    if len(times) <= MAX_PER_MINUTE:
        return {"allow": True, "notify": None, "persist": persist}

    # Превышение лимита → кулдаун + страйк
    times.clear()
    user["rate_cooldown_until"] = now + COOLDOWN_SEC
    strikes = _prune_strikes(user, now)
    strikes.append(now)
    user["rate_strikes"] = strikes
    _last_warn_at[uid] = now
    persist = True

    if len(strikes) >= STRIKES_FOR_BAN:
        user["banned_until"] = now + FLOOD_BAN_SEC
        user["ban_reason"] = "flood"
        user["rate_cooldown_until"] = 0.0
        user["rate_strikes"] = []
        _msg_times.pop(uid, None)
        log.warning("Flood ban uid=%s for %ss", uid, int(FLOOD_BAN_SEC))
        return {"allow": False, "notify": FLOOD_BAN_HTML, "persist": True}

    left_strikes = STRIKES_FOR_BAN - len(strikes)
    warn = (
        WARN_HTML
        + f"\n\n⚠️ Срабатывание <b>{len(strikes)}/{STRIKES_FOR_BAN}</b> за час"
        + (f" · ещё {left_strikes} — и бан." if left_strikes > 0 else ".")
    )
    log.info("Rate limit hit uid=%s strike=%s", uid, len(strikes))
    return {"allow": False, "notify": warn, "persist": True}


def clear_rate_state(user: dict, user_id: str | None = None) -> None:
    """Сброс кулдауна/страйков (для /unban)."""
    ensure_rate_fields(user)
    user["rate_cooldown_until"] = 0.0
    user["rate_strikes"] = []
    if (user.get("ban_reason") or "") == "flood":
        user["banned_until"] = 0.0
        user["ban_reason"] = ""
    if user_id is not None:
        _msg_times.pop(str(user_id), None)
        _last_warn_at.pop(str(user_id), None)
