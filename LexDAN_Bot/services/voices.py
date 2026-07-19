"""
Каталог голосов ElevenLabs для чата и Рико (уроки).
"""

from __future__ import annotations

import os

from services.rewards import user_plan

# Дефолт, если у free нет премиум-голоса
DEFAULT_VOICE_ID = (os.getenv("ELEVENLABS_VOICE_ID") or "pNInz6obpgDQGcFmaJgB").strip()

# Голос Рико — для уроков (всегда)
RICO_VOICE_ID = (os.getenv("RICO_VOICE_ID") or "fBD19tfE58bkETeiwUoC").strip()
RICO_VOICE_NAME = "Rico 🦜"

# Чат: 399 → scotty+emmaline; 799 → все четыре
CHAT_VOICES: list[dict] = [
    {
        "key": "scotty",
        "label": "Scotty · British 🇬🇧",
        "voice_id": "NfUrCNRReUL9RXS9upG1",
        "min_plan": "chat",  # 399+
    },
    {
        "key": "emmaline",
        "label": "Emmaline · British 🇬🇧",
        "voice_id": "nDJIICjR9zfJExIFeSCN",
        "min_plan": "chat",
    },
    {
        "key": "lucas",
        "label": "Lucas · American 🇺🇸",
        "voice_id": "wSqOdjeNqDrHcoK0zorF",
        "min_plan": "full",  # 799
    },
    {
        "key": "aria",
        "label": "Aria · American 🇺🇸",
        "voice_id": "TC0Zp7WVFzhA8zpTlRqV",
        "min_plan": "full",
    },
]

BTN_CHAT_VOICE = "🎙 Голос озвучки"

# Одна фраза для превью всех голосов (не считается в лимит чата)
VOICE_PREVIEW_PHRASE = "Hello! I'm your tutor. Let's talk together."

_PLAN_RANK = {"free": 0, "chat": 1, "full": 2}


def _plan_ok(user_plan_name: str, min_plan: str) -> bool:
    return _PLAN_RANK.get(user_plan_name, 0) >= _PLAN_RANK.get(min_plan, 99)


def voice_by_key(key: str) -> dict | None:
    for v in CHAT_VOICES:
        if v["key"] == key:
            return v
    return None


def available_chat_voices(user: dict) -> list[dict]:
    plan = user_plan(user)
    return [v for v in CHAT_VOICES if _plan_ok(plan, v["min_plan"])]


def locked_chat_voices(user: dict) -> list[dict]:
    plan = user_plan(user)
    return [v for v in CHAT_VOICES if not _plan_ok(plan, v["min_plan"])]


def resolve_chat_voice_id(user: dict) -> str:
    """Какой Voice ID использовать для озвучки ответа в чате."""
    plan = user_plan(user)
    # Бесплатники — только исходный дефолт (Adam / ELEVENLABS_VOICE_ID)
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
        return "Стандартный (Adam) · бесплатный"

    key = (user.get("chat_voice_key") or "").strip()
    v = voice_by_key(key) if key else None
    if v and _plan_ok(plan, v["min_plan"]):
        return v["label"]
    avail = available_chat_voices(user)
    if avail:
        return f"{avail[0]['label']} (по умолчанию)"
    return "Стандартный голос"


def set_chat_voice(user: dict, key: str) -> tuple[bool, str]:
    """Выбрать голос. (ok, message_html)."""
    v = voice_by_key(key)
    if not v:
        return False, "Такого голоса нет."
    if not _plan_ok(user_plan(user), v["min_plan"]):
        need = "399₽ (Общение)" if v["min_plan"] == "chat" else "799₽ (полный доступ)"
        return False, f"🔒 Голос <b>{v['label']}</b> доступен на тарифе <b>{need}</b>."
    user["chat_voice_key"] = key
    return True, f"🎙 Ок! Теперь озвучка: <b>{v['label']}</b>"


def voices_help_text(user: dict) -> str:
    plan = user_plan(user)
    cur = current_voice_label(user)
    lines = [
        "🎙 <b>Голоса озвучки</b>\n",
        f"Сейчас выбран: <b>{cur}</b>\n",
        f"Твой тариф: <b>{plan}</b>\n",
        "<b>Тарифы и голоса</b>\n"
        "• <b>399₽</b> (Общение) — Scotty, Emmaline (British)\n"
        "• <b>799₽</b> (всё) — все четыре: Scotty, Emmaline, Lucas, Aria\n",
        "🎧 <b>Прослушать</b> можно любой голос бесплатно — это не тратит лимит чата.\n"
        "✅ <b>Выбрать</b> для озвучки ответов — только голоса твоего тарифа.\n",
    ]
    avail = available_chat_voices(user)
    if avail:
        lines.append("<b>Тебе можно выбрать:</b>")
        for v in avail:
            mark = "✅" if user.get("chat_voice_key") == v["key"] else "▫️"
            lines.append(f"{mark} {v['label']}")
    else:
        lines.append(
            "На бесплатном тарифе для ответов — <b>стандартный голос Adam</b> "
            "(как было изначально).\n"
            "Послушай премиум ниже и возьми подписку, чтобы включить их 👇"
        )

    lines.append("\nКнопки: 🎧 прослушать · ✅ выбрать")
    return "\n".join(lines)
