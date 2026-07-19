"""
Темы диалога по тарифу: free 10 / chat 50 / full 150.
"""

from __future__ import annotations

import random

from data.chat_topics import CHAT_TOPICS
from services.rewards import user_plan

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


def library_prompt_block(user: dict) -> str:
    samples = sample_for_prompt(user, n=12)
    active = ensure_active_topic(user)
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
