# -*- coding: utf-8 -*-
"""Эмодзи для тем Grammar — по смыслу темы."""

from __future__ import annotations


_ID_EMOJI: dict[str, str] = {
    "alphabet": "🔤",
    "numbers": "🔢",
    "pronouns_be": "🪞",
    "this_that": "👆",
    "articles_a_an": "🅰️",
    "plural": "👥",
    "have_got": "📦",
    "there_is": "📍",
    "can_ability": "💪",
    "imperatives": "👉",
    "present_simple": "⏰",
    "present_continuous": "🎬",
    "past_simple": "📅",
    "going_to": "🚀",
    "comparatives": "📊",
    "modals": "🔐",
    "time_dates": "🕑",
    "present_perfect": "✅",
    "past_perfect": "⏪",
    "conditionals": "🎲",
    "passive": "🔄",
    "relative": "🔗",
    "gerund": "🏃",
    "reported": "💬",
}

_KW: list[tuple[tuple[str, ...], str]] = [
    (("alphabet", "letter", "алфавит"), "🔤"),
    (("number", "digit", "цифр"), "🔢"),
    (("pronoun", "to be", "i am", "you are"), "🪞"),
    (("this", "that", "these", "those"), "👆"),
    (("article", "a/an", "the "), "🅰️"),
    (("plural", "множеств"), "👥"),
    (("have got", "have/has"), "📦"),
    (("there is", "there are"), "📍"),
    (("can ", "ability", "модальн"), "💪"),
    (("imperative", "приказ"), "👉"),
    (("present simple", "present_simple"), "⏰"),
    (("continuous", "сейчас"), "🎬"),
    (("past simple", "past_simple", "вчера"), "📅"),
    (("going to", "will ", "future"), "🚀"),
    (("compar", "суперлатив", "than"), "📊"),
    (("perfect",), "✅"),
    (("conditional", "if ", "условн"), "🎲"),
    (("passive", "пассив"), "🔄"),
    (("relative", "who ", "which"), "🔗"),
    (("gerund", "infinitive", "-ing"), "🏃"),
    (("reported", "косвенн"), "💬"),
    (("modal", "must", "should", "might"), "🔐"),
    (("time", "date", "clock"), "🕑"),
    (("question", "вопрос"), "❓"),
    (("negat", "отрицан"), "🚫"),
    (("preposition", "предлог"), "📌"),
    (("adj", "прилагат"), "🎨"),
    (("adv", "нареч"), "🌀"),
    (("noun", "существ"), "📦"),
    (("verb", "глагол"), "⚡"),
]


def topic_emoji(topic: dict | None) -> str:
    if not topic:
        return "📘"
    tid = str(topic.get("id") or "").lower()
    if tid in _ID_EMOJI:
        return _ID_EMOJI[tid]
    for key, emo in _ID_EMOJI.items():
        if key in tid:
            return emo
    blob = f"{tid} {topic.get('title') or ''}".lower()
    for keys, emo in _KW:
        if any(k in blob for k in keys):
            return emo
    return "📘"
