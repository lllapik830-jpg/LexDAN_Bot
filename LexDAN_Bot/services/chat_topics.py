"""
Темы диалога по тарифу: free 10 / chat 50 / full 150.
"""

from __future__ import annotations

import random
import re

from data.chat_topics import CHAT_TOPICS
from services.rewards import user_plan

_GREETING_RE = re.compile(
    r"(привет|здравств|добр(ое|ый|ой|ая)\s+(утро|день|вечер)|"
    r"\b(hi|hey|hello|hola|yo|sup|hiya)\b|"
    r"how are you|how'?s it going|what'?s up|"
    r"как дела|как ты|как жизнь|good morning|good evening)",
    re.I,
)

_DONT_KNOW_RE = re.compile(
    r"^\s*(i don'?t know|idk|no idea|nothing|not sure|"
    r"не знаю|без понятия|хз|"
    r"don'?t know what|no clue)\s*[.!?]*\s*$",
    re.I,
)

PLAN_TOPIC_LIMITS = {
    "free": 10,
    "chat": 50,
    "full": 150,
}

PLAN_TOPIC_LABELS = {
    "free": "10 тем",
    "chat": "50 тем",
    "full": "150 тем",
}


def topics_for_plan(plan: str) -> list[dict]:
    n = PLAN_TOPIC_LIMITS.get(plan, 10)
    return list(CHAT_TOPICS[:n])


def topics_for_user(user: dict) -> list[dict]:
    return topics_for_plan(user_plan(user))


def topic_count_for_user(user: dict) -> int:
    return PLAN_TOPIC_LIMITS.get(user_plan(user), 10)


def pick_topic(user: dict, *, avoid_ids: set[str] | None = None) -> dict:
    pool = topics_for_user(user)
    avoid = avoid_ids or set()
    choices = [t for t in pool if t["id"] not in avoid] or pool
    return dict(random.choice(choices))


def ensure_active_topic(user: dict, *, force_new: bool = False) -> dict:
    """Активная тема сессии чата (из библиотеки тарифа)."""
    pool_ids = {t["id"] for t in topics_for_user(user)}
    cur = user.get("chat_active_topic")
    if (
        not force_new
        and isinstance(cur, dict)
        and cur.get("id") in pool_ids
        and cur.get("seed")
    ):
        return cur
    topic = pick_topic(user)
    user["chat_active_topic"] = topic
    return topic


def sample_for_prompt(user: dict, *, n: int = 12) -> list[dict]:
    """Подвыборка библиотеки для промпта (активная + случайные)."""
    pool = topics_for_user(user)
    active = ensure_active_topic(user)
    rest = [t for t in pool if t["id"] != active.get("id")]
    random.shuffle(rest)
    out = [active] + rest[: max(0, n - 1)]
    return out


def library_prompt_block(user: dict, *, engaged: bool = False) -> str:
    """
    engaged=True — только активная тема (обычный ход диалога, меньше токенов).
    engaged=False — активная + короткая выборка библиотеки (старт / смена темы).
    """
    active = ensure_active_topic(user)
    if engaged:
        return (
            f"\n\nACTIVE topic: {active['title_en']} ({active.get('title_ru', '')}). "
            f"Seed: {active['seed']}. Stay on this topic until the student changes it."
        )

    samples = sample_for_prompt(user, n=5)
    lines = [
        f"- {t['title_en']} ({t['title_ru']}): {t['seed']}"
        for t in samples
    ]
    return (
        f"\n\nTOPIC LIBRARY for this student (plan={user_plan(user)}, "
        f"{topic_count_for_user(user)} topics total). "
        "When the student has no clear topic / only small talk / says they don't know what to talk about, "
        "suggest ONE topic from this library (prefer the ACTIVE one unless they reject it) "
        "and ask its seed question (you may rephrase lightly).\n"
        f"ACTIVE topic now: {active['title_en']} — seed: {active['seed']}\n"
        "Sample from their library:\n" + "\n".join(lines)
    )


def is_dont_know(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return False
    if _DONT_KNOW_RE.match(t):
        return True
    low = t.lower()
    if len(t.split()) > 10:
        return False
    hints = (
        "не знаю",
        "не знаю о чем",
        "не знаю о чём",
        "не знаю что",
        "без понятия",
        "idk",
        "don't know",
        "do not know",
        "no idea",
        "nothing to",
        "not sure what",
    )
    return any(h in low for h in hints)


def is_greeting(text: str) -> bool:
    return bool(_GREETING_RE.search((text or "").strip()))


def topic_offered_in_recent(recent_replies: list[str], user: dict) -> bool:
    active = user.get("chat_active_topic") or {}
    title = (active.get("title_en") or "").lower()
    for r in reversed(recent_replies or []):
        rl = (r or "").lower()
        if title and title in rl:
            return True
        if "could talk about" in rl or "chat about" in rl or "could chat about" in rl:
            return True
    return False


_CHANGE_TOPIC_RE = re.compile(
    r"(?i)("
    r"another topic|new topic|other topic|change topic|different topic|"
    r"другую тему|другая тема|смени тему|новую тему|другую тему|"
    r"давай о другом|поговорим о другом|сменим тему"
    r")"
)


def wants_topic_change(text: str) -> bool:
    return bool(_CHANGE_TOPIC_RE.search((text or "").strip()))


def resolve_chat_reply_mode(
    user_text: str,
    user: dict,
    turns: list[dict],
    recent_replies: list[str],
) -> str:
    """
    suggest — поприветствовать и предложить тему из библиотеки;
    dive — сразу задать seed-вопрос по активной теме;
    gpt — обычный диалог с моделью.
    """
    from services.gpt import _active_topic_in_turns, _looks_like_no_topic

    # Явная просьба сменить тему — новый pick снаружи; здесь просто gpt/suggest
    if wants_topic_change(user_text):
        return "suggest"

    # Уже в теме (предложили / нырнули / есть диалог) — не прыгаем на другую
    if (
        user.get("chat_topic_dived")
        or user.get("chat_topic_offered")
        or _active_topic_in_turns(turns)
    ):
        if is_dont_know(user_text) and not user.get("chat_topic_dived"):
            return "dive"
        return "gpt"

    if is_dont_know(user_text):
        return "dive"

    offered = bool(user.get("chat_topic_offered")) or topic_offered_in_recent(
        recent_replies, user
    )
    if offered and (_looks_like_no_topic(user_text) or is_dont_know(user_text)):
        return "dive"

    if _looks_like_no_topic(user_text) or is_greeting(user_text):
        return "suggest"

    return "gpt"


def build_suggest_topic_reply(name: str, topic: dict, user_text: str = "") -> str:
    """Приветствие + мягкое предложение темы (без seed-вопроса)."""
    title = topic.get("title_en") or "something interesting"
    who = ""
    if name and name.strip().lower() not in ("student", ""):
        who = f", {name.strip()}"

    if is_greeting(user_text):
        opener = f"Hi{who}! I'm doing great, thanks for asking!"
    else:
        opener = f"Hi{who}!"

    return (
        f"{opener} What would you like to talk about? "
        f"Maybe we could chat about {title}?"
    )


def build_dive_topic_reply(topic: dict) -> str:
    """Сразу задаём стартовый вопрос по активной теме."""
    seed = (topic.get("seed") or "Tell me more about that.").strip()
    if seed and seed[0].islower():
        seed = seed[0].upper() + seed[1:]
    return f"Alright! {seed}"


def chat_intro_topics_blurb(user: dict) -> str:
    plan = user_plan(user)
    n = topic_count_for_user(user)
    active = ensure_active_topic(user)
    examples = topics_for_user(user)[:3]
    ex = ", ".join(f"«{t['title_ru']}»" for t in examples)

    if plan == "free":
        upgrade = (
            "На <b>399₽</b> — библиотека из <b>50</b> тем, на <b>799₽</b> — из <b>150</b>."
        )
    elif plan == "chat":
        upgrade = "На полном <b>799₽</b> открывается библиотека из <b>150</b> тем."
    else:
        upgrade = "У тебя максимальная библиотека тем для живого диалога."

    return (
        f"🗂 <b>Библиотека тем для разговора:</b> у тебя <b>{n}</b> "
        f"({PLAN_TOPIC_LABELS.get(plan, n)}).\n"
        f"Примеры: {ex}.\n"
        f"Сейчас могу начать с: <b>{active['title_ru']}</b> — "
        f"<i>{active['seed']}</i>\n"
        "Пиши свою тему — или просто hi / idk, и я предложу из библиотеки.\n"
        f"{upgrade}"
    )
