"""
Правила пользования + фильтр матов / запрещённого контента.
10 нарушений (маты) → бан на 2 суток.
"""

from __future__ import annotations

import re
import time
from datetime import datetime, timedelta, timezone

MSK = timezone(timedelta(hours=3))

BAN_DAYS = 2
SWEAR_STRIKES_LIMIT = 10

RULES_HTML = (
    "📜 <b>Правила пользования LexDAN</b>\n\n"
    "Пользуясь ботом, ты соглашаешься с правилами Telegram и нашими условиями:\n\n"
    "1) <b>Без матов и оскорблений</b> — в чате, уроках и голосовых.\n"
    "2) <b>Без порнографии, насилия, спама и всего запрещённого</b> "
    "правилами Telegram и законом.\n"
    "3) Уважай Рико и других учеников — учимся спокойно и по делу.\n\n"
    "🦜 За мат Рико предупредит. "
    f"<b>{SWEAR_STRIKES_LIMIT} нарушений</b> с матами = "
    f"<b>блокировка на {BAN_DAYS} суток</b>.\n\n"
    "Нажми кнопку ниже, если принимаешь правила 👇"
)

BTN_ACCEPT_RULES = "✅ Принимаю правила"
BTN_NAME_SURE = "Уверен(а)"

# Грубый список RU/EN (словоцеликом / очевидные формы)
_SWEAR_RE = re.compile(
    r"(?i)(?<![а-яa-z])"
    r"("
    r"бля(?:т|д|ть|дина)?|блять|бляд|"
    r"сука|сучк|"
    r"хуй|хуя|хуе|хуё|хуи|"
    r"пизд|пезд|"
    r"еб(?:а|у|ё|е|л|ну)|ёб|"
    r"мудак|мудил|"
    r"гандон|гондон|"
    r"залуп|"
    r"fuck|fucking|fucked|shit|bitch|asshole|dick|cunt|bastard|"
    r"porn|porno|xxx|nsfw"
    r")"
    r"(?![а-яa-z])"
)

_NSFW_HINT_RE = re.compile(
    r"(?i)\b("
    r"порно|порнух|секс\s*чат|только\s*fans|onlyfans|"
    r"nude|nudes|hentai|эротик"
    r")\b"
)


def _now_ts() -> float:
    return time.time()


def ensure_moderation(user: dict) -> dict:
    user.setdefault("rules_accepted", False)
    user.setdefault("swear_strikes", 0)
    user.setdefault("banned_until", 0.0)
    user.setdefault("ban_reason", "")
    user.setdefault("pending_name", "")
    user.setdefault("name_changed_at", 0.0)
    try:
        from services.rate_limit import ensure_rate_fields

        ensure_rate_fields(user)
    except Exception:
        pass
    return user


def is_banned(user: dict) -> bool:
    ensure_moderation(user)
    until = float(user.get("banned_until") or 0)
    if until <= _now_ts():
        if until:
            user["banned_until"] = 0
            user["ban_reason"] = ""
        return False
    return True


def ban_remaining_text(user: dict) -> str:
    if (user.get("ban_reason") or "").strip() == "flood":
        from services.rate_limit import flood_ban_remaining_text

        return flood_ban_remaining_text(user)
    until = float(user.get("banned_until") or 0)
    left = max(0, int(until - _now_ts()))
    hours = left // 3600
    mins = (left % 3600) // 60
    when = datetime.fromtimestamp(until, MSK).strftime("%d.%m %H:%M")
    return (
        f"🚫 Аккаунт временно заблокирован до <b>{when}</b> (МСК).\n"
        f"Осталось примерно {hours} ч {mins} мин.\n\n"
        f"Причина: {SWEAR_STRIKES_LIMIT}+ нарушений правил (маты / запрещённый контент)."
    )


def contains_forbidden(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return False
    if _SWEAR_RE.search(t):
        return True
    if _NSFW_HINT_RE.search(t):
        return True
    return False


def note_swear_violation(user: dict) -> tuple[bool, str]:
    """
    Учесть нарушение. Returns (banned_now, message_to_user).
    """
    ensure_moderation(user)
    user["swear_strikes"] = int(user.get("swear_strikes") or 0) + 1
    strikes = int(user["swear_strikes"])
    left = max(0, SWEAR_STRIKES_LIMIT - strikes)

    if strikes >= SWEAR_STRIKES_LIMIT:
        user["banned_until"] = _now_ts() + BAN_DAYS * 86400
        user["ban_reason"] = "swear"
        user["swear_strikes"] = 0
        return True, (
            "🦜 <b>Стоп.</b> Слишком много нарушений правил.\n\n"
            f"Блокировка на <b>{BAN_DAYS} суток</b>.\n"
            "Без матов и запрещённого контента — так учиться спокойнее."
        )

    return False, (
        "🦜 Эй, так нельзя.\n\n"
        "В LexDAN <b>запрещены маты, порнография и всё, что запрещено Telegram</b>.\n"
        f"Предупреждение <b>{strikes}/{SWEAR_STRIKES_LIMIT}</b>. "
        f"Ещё {left} — и будет бан на {BAN_DAYS} суток.\n"
        "Давай без этого, ок? 💚"
    )


async def guard_user_text(m, user: dict, text: str) -> bool:
    """
    True = можно продолжать обработку.
    False = уже ответили (бан / предупреждение).
    """
    from services.database import save_users

    ensure_moderation(user)
    if is_banned(user):
        await m.answer(ban_remaining_text(user), parse_mode="HTML")
        return False
    if not contains_forbidden(text):
        return True

    _, msg = note_swear_violation(user)
    save_users({str(m.from_user.id): user}, only=str(m.from_user.id))
    await m.answer(msg, parse_mode="HTML")
    return False
