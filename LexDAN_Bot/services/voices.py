"""
Каталог голосов ElevenLabs для чата и Рико (уроки).

Политика голоса Рико (RICO_VOICE_ID):
  ИСПОЛЬЗОВАТЬ: Grammar / Vocabulary / Reading-озвучка / Daily Fire /
  A0 / order-summary Listening / эксклюзив Рико /
  поздравления ивента / курсы (монологи).
  НЕ ИСПОЛЬЗОВАТЬ: раздел «Общаться» (чат), реплики персонажей
  в диалогах Listening и Живой речи, и аудирование во вступительном
  тесте уровня (там 3 разных голоса из CHAT_VOICES).
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
# free → только Adam (дефолт ElevenLabs), остальные можно послушать
# Безлимит (full) → все голоса
CHAT_VOICES: list[dict] = [
    # Все голоса каталога — только с «Безлимитом»
    {
        "key": "scotty",
        "name": "Scotty",
        "accent": "British",
        "flag": "🇬🇧",
        "voice_id": "NfUrCNRReUL9RXS9upG1",
        "min_plan": "full",
    },
    {
        "key": "emmaline",
        "name": "Emmaline",
        "accent": "British",
        "flag": "🇬🇧",
        "voice_id": "nDJIICjR9zfJExIFeSCN",
        "min_plan": "full",
    },
    {
        "key": "joe",
        "name": "Joe",
        "accent": "British",
        "flag": "🇬🇧",
        "voice_id": "av1BMOR1GPgThz9p4fLo",
        "min_plan": "full",
    },
    {
        "key": "ed",
        "name": "Ed",
        "accent": "American",
        "flag": "🇺🇸",
        "voice_id": "dHd5gvgSOzSfduK4CvEg",
        "min_plan": "full",
    },
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
        return (
            False,
            "🎙 Этот голос доступен только с безлимитом. "
            "Оформи подписку, чтобы использовать все голоса.",
        )
    user["chat_voice_key"] = key
    return True, f"🎙 Ок! Теперь озвучка: <b>{voice_label(v)}</b>"


def voices_help_text(user: dict) -> str:
    """Короткий хаб выбора голоса (для всех)."""
    plan = user_plan(user)
    cur = current_voice_label(user)
    for suffix in (" (бесплатный)", " (по умолчанию)"):
        if cur.endswith(suffix):
            cur = cur[: -len(suffix)]
    plan_title = {
        "free": "бесплатный",
        "chat": "безлимит общения (старый)",
        "full": "Безлимит",
    }.get(plan, plan)

    full_n = len(CHAT_VOICES)
    avail = available_chat_voices(user)

    lines = [
        f"Сейчас выбран: <b>{cur}</b>\n",
        f"Твой тариф: <b>{plan_title}</b>\n",
        "🎧 Прослушать можно бесплатно (не тратит лимит чата).\n"
        "✅ Выбрать — Adam на free · все голоса с безлимитом.\n",
        "━━━━━━━━━━━━━━\n",
        "🆓 Бесплатно: <b>Adam · American 🇺🇸</b>\n"
        f"🚀 Безлимит: <b>{full_n}</b> голосов на выбор\n",
        "━━━━━━━━━━━━━━",
    ]
    if avail:
        lines.append("\nНиже — голоса, доступные тебе: 🎧 прослушать · ✅ выбрать")
    else:
        lines.append(
            "\nНа бесплатном для ответов — <b>Adam</b>. "
            "Чтобы выбирать другие голоса — нужен безлимит 👇"
        )
    return "\n".join(lines)


def rico_alt_voice_unlocked(user: dict | None) -> bool:
    """Второй голос Рико — только победителю ивента (не менеджеру)."""
    if not user:
        return False
    if user.get("rico_alt_voice_unlocked"):
        return True
    ep = user.get("event_prizes")
    if isinstance(ep, dict) and ep.get("exclusive_voice"):
        return True
    place = int(ep.get("place") or 0) if isinstance(ep, dict) else 0
    return place == 1


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
