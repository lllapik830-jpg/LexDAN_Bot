"""
Каталог голосов ElevenLabs для чата и Рико (уроки).
"""

from __future__ import annotations

import os

from services.rewards import user_plan

# Дефолт для бесплатного тарифа (Adam)
DEFAULT_VOICE_ID = (os.getenv("ELEVENLABS_VOICE_ID") or "pNInz6obpgDQGcFmaJgB").strip()

# Голос Рико — для уроков (всегда)
RICO_VOICE_ID = (os.getenv("RICO_VOICE_ID") or "fBD19tfE58bkETeiwUoC").strip()
RICO_VOICE_NAME = "Rico 🦜"

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
