"""
Секретные задания Рико (награды за серию дней).
"""

from __future__ import annotations

import logging
import random

from services.growth import ensure_growth, grant_safe
from services.rewards import set_grammar_cap_today

MISSION_WEEK = "week_review"
MISSION_VOICE = "voice_day"

MISSION_META = {
    MISSION_WEEK: {
        "title": "📝 Разбор твоей недели",
        "blurb": "Рико разберёт твои живые ошибки и даст 5 персональных правок «как носитель».",
        "mins": "7–10 мин",
    },
    MISSION_VOICE: {
        "title": "🗣 Голос дня",
        "blurb": "4 фразы — говори голосом (или текстом). Рико скажет, как звучать естественнее.",
        "mins": "5–8 мин",
    },
}

BTN_SECRET = "🔐 Секрет Рико"
BTN_SECRET_WEEK = "📝 Разбор недели"
BTN_SECRET_VOICE = "🗣 Голос дня"
BTN_SECRET_SKIP = "⏭ Пропустить фразу"
BTN_SECRET_DONE = "✅ Готово"


def ensure_missions(user: dict) -> dict:
    ensure_growth(user)
    if "secret_missions" not in user or not isinstance(user["secret_missions"], dict):
        user["secret_missions"] = {"inbox": [], "active": None, "done": []}
    sm = user["secret_missions"]
    sm.setdefault("inbox", [])
    sm.setdefault("active", None)
    sm.setdefault("done", [])
    return sm


def unlock_mission(user: dict, mission_id: str) -> bool:
    """Добавить миссию в inbox. True если реально добавили."""
    sm = ensure_missions(user)
    if mission_id not in MISSION_META:
        return False
    if mission_id in sm["inbox"]:
        return False
    # можно пройти снова через N дней — пока один раз на тип, пока не в done
    # если уже done — всё равно даём повторный unlock за новый streak-milestone
    sm["inbox"].append(mission_id)
    user["pending_secret_rico"] = True
    return True


def has_secret_entry(user: dict) -> bool:
    sm = ensure_missions(user)
    return bool(sm["inbox"]) or bool(sm.get("active"))


def inbox_missions(user: dict) -> list[str]:
    return list(ensure_missions(user).get("inbox") or [])


def get_active(user: dict) -> dict | None:
    return ensure_missions(user).get("active")


def clear_active(user: dict) -> None:
    sm = ensure_missions(user)
    sm["active"] = None
    user["pending_secret_rico"] = bool(sm["inbox"])


def start_mission(user: dict, mission_id: str) -> dict | None:
    sm = ensure_missions(user)
    if mission_id not in sm["inbox"]:
        return None
    sm["inbox"] = [x for x in sm["inbox"] if x != mission_id]
    if mission_id == MISSION_WEEK:
        cards = build_week_review(user)
        sm["active"] = {
            "type": MISSION_WEEK,
            "step": 0,
            "cards": cards,
        }
    elif mission_id == MISSION_VOICE:
        phrases = build_voice_phrases(user)
        sm["active"] = {
            "type": MISSION_VOICE,
            "step": 0,
            "phrases": phrases,
            "notes": [],
        }
    else:
        return None
    user["pending_secret_rico"] = True
    return sm["active"]


def complete_mission(user: dict) -> str:
    """Завершить активную миссию, выдать награду."""
    sm = ensure_missions(user)
    active = sm.get("active") or {}
    mtype = active.get("type") or ""
    sm["done"] = list(sm.get("done") or []) + [mtype]
    sm["active"] = None
    user["pending_secret_rico"] = bool(sm["inbox"])

    # награда: бустер grammar + сейф
    set_grammar_cap_today(user, 24)
    grant_safe(user, 1)
    title = MISSION_META.get(mtype, {}).get("title", "Секрет")
    return (
        f"🏆 <b>Секрет выполнен:</b> {title}\n\n"
        "Награда:\n"
        "• Grammar сегодня до <b>24</b> заданий\n"
        "• <b>+1</b> стрик-сейф 🛡️\n\n"
        "Рико гордится тобой. Завтра — снова ~15 минут 💪"
    )


def build_week_review(user: dict) -> list[dict]:
    """5 карточек правок на основе недавнего чата / уровня."""
    level = user.get("level") or "A1"
    turns = user.get("chat_recent_turns") or []
    user_lines = [
        t.get("text") or ""
        for t in turns
        if t.get("role") == "user" and (t.get("text") or "").strip()
    ][-8:]
    sample = "\n".join(f"- {x}" for x in user_lines) if user_lines else "(мало сообщений)"

    from services.gpt import _ask_json

    fallback = _fallback_week_cards(level)
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "You are Rico, English tutor for Russian students. "
                    "Return ONLY JSON: {\"cards\":[{\"wrong\":\"...\",\"better\":\"...\","
                    "\"tip_ru\":\"...\"}]} with exactly 5 cards. "
                    "Based on student lines (or typical CEFR mistakes if empty). "
                    "wrong/better in English, tip_ru in Russian, short."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"CEFR level: {level}\nRecent student English:\n{sample}\n"
                    "Make 5 personal native-style corrections."
                ),
            },
        ],
        {"cards": fallback},
        temperature=0.4,
        max_tokens=700,
    )
    cards = data.get("cards") if isinstance(data, dict) else None
    if not isinstance(cards, list) or len(cards) < 3:
        return fallback
    out = []
    for c in cards[:5]:
        if not isinstance(c, dict):
            continue
        wrong = str(c.get("wrong") or "").strip()
        better = str(c.get("better") or "").strip()
        tip = str(c.get("tip_ru") or "").strip()
        if better:
            out.append({"wrong": wrong, "better": better, "tip_ru": tip})
    return out or fallback


def _fallback_week_cards(level: str) -> list[dict]:
    base = [
        {
            "wrong": "I go to school yesterday",
            "better": "I went to school yesterday",
            "tip_ru": "Вчера → Past Simple: go → went.",
        },
        {
            "wrong": "She don't like coffee",
            "better": "She doesn't like coffee",
            "tip_ru": "he/she/it → doesn't, не don't.",
        },
        {
            "wrong": "I am agree with you",
            "better": "I agree with you",
            "tip_ru": "agree — без am (это не continuous).",
        },
        {
            "wrong": "How you say this?",
            "better": "How do you say this?",
            "tip_ru": "Вопрос: Do/Does + подлежащее.",
        },
        {
            "wrong": "I very like it",
            "better": "I like it a lot / I really like it",
            "tip_ru": "Не very like — really / a lot.",
        },
    ]
    if level in {"A0", "A1"}:
        return base
    return base  # достаточно универсально


def build_voice_phrases(user: dict) -> list[str]:
    level = user.get("level") or "A1"
    from services.gpt import _ask_json

    pools = {
        "A0": [
            "Hello! How are you today?",
            "My name is Alex.",
            "I like coffee.",
            "See you tomorrow!",
        ],
        "A1": [
            "What did you do yesterday?",
            "I'm learning English every day.",
            "Can you help me, please?",
            "That sounds great!",
        ],
        "A2": [
            "I've been busy this week.",
            "Could you say that again?",
            "I'm trying to sound more natural.",
            "Let's grab a coffee later.",
        ],
    }
    fallback = pools.get(level, pools["A2"] if level >= "B1" else pools["A1"])
    if level in {"B1", "B2", "C1", "C2"}:
        fallback = [
            "I've been meaning to practice speaking more.",
            "That makes sense — I hadn't thought of it that way.",
            "Could you walk me through it one more time?",
            "I'm getting more comfortable with small talk.",
        ]

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Return ONLY JSON {\"phrases\":[\"...\",\"...\",\"...\",\"...\"]} "
                    "— 4 short spoken English lines for pronunciation practice, CEFR-appropriate."
                ),
            },
            {"role": "user", "content": f"CEFR: {level}. Seed {random.random()}"},
        ],
        {"phrases": fallback},
        temperature=0.5,
        max_tokens=200,
    )
    phrases = data.get("phrases") if isinstance(data, dict) else None
    if not isinstance(phrases, list) or len(phrases) < 4:
        return fallback
    return [str(p).strip() for p in phrases[:4] if str(p).strip()]


def evaluate_voice_attempt(target: str, heard: str) -> dict:
    from services.gpt import _ask_json

    fallback = {
        "ok": True,
        "better": target,
        "tip_ru": "Хорошая попытка! Повтори ещё раз чуть медленнее.",
    }
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Pronunciation/speaking coach. Student tried to say TARGET. "
                    "Return ONLY JSON "
                    '{"ok":bool,"better":"natural version","tip_ru":"short Russian tip"} '
                    "ok=true if meaning is clear even with mistakes."
                ),
            },
            {
                "role": "user",
                "content": f"TARGET: {target}\nSTUDENT SAID: {heard}",
            },
        ],
        fallback,
        temperature=0.2,
        max_tokens=220,
    )
    if not isinstance(data, dict):
        return fallback
    return {
        "ok": bool(data.get("ok", True)),
        "better": str(data.get("better") or target).strip(),
        "tip_ru": str(data.get("tip_ru") or "").strip(),
    }


def format_card(i: int, total: int, card: dict) -> str:
    wrong = card.get("wrong") or "—"
    better = card.get("better") or "—"
    tip = card.get("tip_ru") or ""
    return (
        f"📝 <b>Разбор {i}/{total}</b>\n\n"
        f"Часто так: <i>{wrong}</i>\n"
        f"Как носитель: <b>{better}</b>\n"
        f"{('💡 ' + tip) if tip else ''}\n\n"
        "Жми «Далее», когда запомнил."
    )
