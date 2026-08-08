"""
Каталог голосов ElevenLabs для чата и Рико (уроки).
"""

from __future__ import annotations

import os

from services.rewards import user_plan

# Дефолт для бесплатного тарифа (Adam)
def _env_voice(name: str, fallback: str) -> str:
    v = (os.getenv(name) or "").strip()
    return v if v else fallback


DEFAULT_VOICE_ID = _env_voice("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")

# Голос Рико — для уроков / огня дня / Рико-реплик (всегда)
RICO_VOICE_ID = _env_voice("RICO_VOICE_ID", "fBD19tfE58bkETeiwUoC")
RICO_VOICE_NAME = "Rico 🦜"
# Призовой второй голос Рико (1–2 место ивента)
RICO_VOICE_ALT_ID = _env_voice("RICO_VOICE_ALT_ID", "XsmrVB66q3D4TaXVaWNF")
RICO_VOICE_ALT_NAME = "Rico · Legend 👑"

BTN_RICO_VOICE = "🦜 Голос Рико"

RICO_VOICE_CHOICES = (
    {"key": "classic", "name": RICO_VOICE_NAME, "voice_id": RICO_VOICE_ID},
    {"key": "legend", "name": RICO_VOICE_ALT_NAME, "voice_id": RICO_VOICE_ALT_ID},
)


# Чат:
# free → только Adam (дефолт)
# 399 (chat) → British/American ниже
# 799 (full) → все голоса
CHAT_VOICES: list[dict] = [
    # ── 399₽ (Общение) ──────────────────────────────────────────────
    {
        "key": "scotty",
        "name": "Scotty",
        "accent": "British",
        "flag": "🇬🇧",
        "voice_id": "NfUrCNRReUL9RXS9upG1",
        "min_plan": "chat",
    },
    {
        "key": "emmaline",
        "name": "Emmaline",
        "accent": "British",
        "flag": "🇬🇧",
        "voice_id": "nDJIICjR9zfJExIFeSCN",
        "min_plan": "chat",
    },
    {
        "key": "joe",
        "name": "Joe",
        "accent": "British",
        "flag": "🇬🇧",
        "voice_id": "av1BMOR1GPgThz9p4fLo",
        "min_plan": "chat",
    },
    {
        "key": "ed",
        "name": "Ed",
        "accent": "American",
        "flag": "🇺🇸",
        "voice_id": "dHd5gvgSOzSfduK4CvEg",
        "min_plan": "chat",
    },
    # ── 799₽ (полный) ───────────────────────────────────────────────
    {
        "key": "lucas",
        "name": "Lucas",
        "accent": "American",
        "flag": "🇺🇸",
        "voice_id": "wSqOdjeNqDrHcoK0zorF",
        "min_plan": "full",
    },
    {
        "key": "aria",
        "name": "Aria",
        "accent": "American",
        "flag": "🇺🇸",
        "voice_id": "TC0Zp7WVFzhA8zpTlRqV",
        "min_plan": "full",
    },
    {
        "key": "jimbo",
        "name": "Jimbo",
        "accent": "Australian",
        "flag": "🇦🇺",
        "voice_id": "YLbQE9U7P1K6rBNJWNSv",
        "min_plan": "full",
    },
    {
        "key": "ruby",
        "name": "Ruby",
        "accent": "Australian",
        "flag": "🇦🇺",
        "voice_id": "b8gbDO0ybjX1VA89pBdX",
        "min_plan": "full",
    },
]

BTN_CHAT_VOICE = "🎙 Голос озвучки"

# Одна фраза для превью всех голосов (не считается в лимит чата)
VOICE_PREVIEW_PHRASE = "Hello! I'm your tutor. Let's talk together."

_PLAN_RANK = {"free": 0, "chat": 1, "full": 2}


def voice_label(v: dict) -> str:
    return f"{v['name']} · {v['accent']} {v.get('flag') or ''}".strip()


# обратная совместимость для кода, который читал v["label"]
for _v in CHAT_VOICES:
    _v["label"] = voice_label(_v)


def _plan_ok(user_plan_name: str, min_plan: str) -> bool:
    return _PLAN_RANK.get(user_plan_name, 0) >= _PLAN_RANK.get(min_plan, 99)


def voice_by_key(key: str) -> dict | None:
    for v in CHAT_VOICES:
        if v["key"] == key:
            return v
    return None


def voices_for_min_plan(min_plan: str) -> list[dict]:
    return [v for v in CHAT_VOICES if v["min_plan"] == min_plan]


def available_chat_voices(user: dict) -> list[dict]:
    plan = user_plan(user)
    return [v for v in CHAT_VOICES if _plan_ok(plan, v["min_plan"])]


def locked_chat_voices(user: dict) -> list[dict]:
    plan = user_plan(user)
    return [v for v in CHAT_VOICES if not _plan_ok(plan, v["min_plan"])]


def resolve_chat_voice_id(user: dict) -> str:
    """Какой Voice ID использовать для озвучки ответа в чате."""
    plan = user_plan(user)
    if plan == "free":
        return DEFAULT_VOICE_ID

    key = (user.get("chat_voice_key") or "").strip()
    v = voice_by_key(key) if key else None
    if v and _plan_ok(plan, v["min_plan"]):
        return v["voice_id"]
    avail = available_chat_voices(user)
    if avail:
        return avail[0]["voice_id"]
    return DEFAULT_VOICE_ID


def current_voice_label(user: dict) -> str:
    plan = user_plan(user)
    if plan == "free":
        return "Adam · American 🇺🇸 (бесплатный)"

    key = (user.get("chat_voice_key") or "").strip()
    v = voice_by_key(key) if key else None
    if v and _plan_ok(plan, v["min_plan"]):
        return voice_label(v)
    avail = available_chat_voices(user)
    if avail:
        return f"{voice_label(avail[0])} (по умолчанию)"
    return "Стандартный голос"


def set_chat_voice(user: dict, key: str) -> tuple[bool, str]:
    """Выбрать голос. (ok, message_html)."""
    v = voice_by_key(key)
    if not v:
        return False, "Такого голоса нет."
    if not _plan_ok(user_plan(user), v["min_plan"]):
        need = "399₽ (Общение)" if v["min_plan"] == "chat" else "799₽ (полный доступ)"
        return False, f"🔒 Голос <b>{voice_label(v)}</b> доступен на тарифе <b>{need}</b>."
    user["chat_voice_key"] = key
    return True, f"🎙 Ок! Теперь озвучка: <b>{voice_label(v)}</b>"


def voices_help_text(user: dict) -> str:
    plan = user_plan(user)
    cur = current_voice_label(user)
    plan_title = {
        "free": "бесплатный",
        "chat": "399₽ · Общение",
        "full": "799₽ · полный доступ",
    }.get(plan, plan)

    lines = [
        "🎙 <b>Голоса озвучки в «Общаться»</b>\n",
        f"Сейчас выбран: <b>{cur}</b>\n",
        f"Твой тариф: <b>{plan_title}</b>\n",
        "🎧 Прослушать можно любой голос бесплатно (не тратит лимит чата).\n"
        "✅ Выбрать для ответов — только голоса твоего тарифа.\n",
        "━━━━━━━━━━━━━━\n",
        "<b>🆓 Бесплатно</b>\n"
        "• Adam · American 🇺🇸\n",
        "<b>💬 399₽ · Общение</b> (+ всё с бесплатного)\n",
    ]
    for v in voices_for_min_plan("chat"):
        lines.append(f"• {voice_label(v)}")
    lines.append("")
    lines.append("<b>🚀 799₽ · полный доступ</b> (+ всё с 399)\n")
    for v in voices_for_min_plan("full"):
        lines.append(f"• {voice_label(v)}")

    lines.append("\n━━━━━━━━━━━━━━")
    avail = available_chat_voices(user)
    if avail:
        lines.append("\n<b>Тебе можно выбрать сейчас:</b>")
        for v in avail:
            mark = "✅" if user.get("chat_voice_key") == v["key"] else "▫️"
            lines.append(f"{mark} {voice_label(v)}")
    else:
        lines.append(
            "\nНа бесплатном для ответов — <b>Adam</b>. "
            "Послушай премиум ниже и возьми подписку, чтобы выбрать их 👇"
        )

    lines.append("\nКнопки ниже: 🎧 прослушать · ✅ выбрать")
    return "\n".join(lines)


def rico_alt_voice_unlocked(user: dict | None) -> bool:
    """Второй голос Рико — приз 1–2 места (или явный флаг / менеджер)."""
    if not user:
        return False
    if user.get("rico_alt_voice_unlocked") or user.get("dev_unlock"):
        return True
    try:
        from config import MANAGER_ID

        uid = user.get("telegram_id") or user.get("id")
        if uid is not None and int(uid) == int(MANAGER_ID):
            return True
    except Exception:
        pass
    ep = user.get("event_prizes")
    if isinstance(ep, dict) and ep.get("exclusive_voice"):
        return True
    place = int(ep.get("place") or 0) if isinstance(ep, dict) else 0
    return place in {1, 2}


def resolve_rico_voice_id(user: dict | None = None) -> str:
    """Какой Voice ID Рико использовать в уроках/озвучке. Никогда не пустой."""
    if user and rico_alt_voice_unlocked(user) and (user.get("rico_voice_key") or "") == "legend":
        vid = (RICO_VOICE_ALT_ID or "").strip() or RICO_VOICE_ID
    else:
        vid = (RICO_VOICE_ID or "").strip()
    return vid or "fBD19tfE58bkETeiwUoC"


def current_rico_voice_label(user: dict | None = None) -> str:
    if user and (user.get("rico_voice_key") or "") == "legend" and rico_alt_voice_unlocked(user):
        return RICO_VOICE_ALT_NAME
    return RICO_VOICE_NAME


def toggle_rico_voice(user: dict) -> tuple[bool, str]:
    """
    Переключить classic ↔ legend.
    Returns (ok, html_message).
    """
    if not rico_alt_voice_unlocked(user):
        return (
            False,
            "🔒 Второй голос Рико — приз для <b>1 и 2 места</b> ивента. "
            "Пока доступен классический Rico 🦜",
        )
    cur = (user.get("rico_voice_key") or "classic").strip()
    nxt = "legend" if cur != "legend" else "classic"
    user["rico_voice_key"] = nxt
    label = RICO_VOICE_ALT_NAME if nxt == "legend" else RICO_VOICE_NAME
    return True, f"🦜 Голос Рико: <b>{label}</b>"


def rico_voice_help_html(user: dict) -> str:
    unlocked = rico_alt_voice_unlocked(user)
    cur = current_rico_voice_label(user)
    lines = [
        "🦜 <b>Голос Рико в уроках</b>\n",
        f"Сейчас: <b>{cur}</b>\n",
    ]
    if unlocked:
        lines.append(
            "Тебе открыт второй голос-приз.\n"
            "Нажми кнопку ещё раз — переключится classic ↔ legend.\n"
            "Ниже — короткое превью выбранного голоса 🎧"
        )
    else:
        lines.append(
            "Пока только классический Rico.\n"
            "Второй голос откроется победителям <b>1 и 2 места</b> ивента 👑"
        )
    return "\n".join(lines)
