"""
Генерация уникальных заданий теста уровня через ИИ.
При ошибке API — короткие запасные варианты.
"""

import logging
import random

from data.assessment_data import LEVELS, get_translation, pick_topic
from services.gpt import _ask_json


def generate_translation(level: str, seed: str = "") -> dict:
    """
    EN текст 4–5 предложений + эталонный RU перевод под CEFR level.
    """
    fallback = get_translation(level, random.randint(0, 1))
    tip = {
        "C2": "advanced abstract vocabulary, complex clauses",
        "C1": "advanced but clear, some idioms",
        "B2": "upper-intermediate, natural everyday/academic mix",
        "B1": "intermediate, common topics, simple linking words",
        "A2": "elementary, short simple sentences",
        "A1": "beginner, very basic words",
        "A0": "absolute beginner, ultra-simple words and phrases",
    }.get(level, "intermediate")

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Create a UNIQUE English placement-test passage and its Russian translation. "
                    "Exactly 4 or 5 short sentences. No dialogue labels. "
                    f"CEFR target: {level} ({tip}). "
                    "Make content different every time (different topic). "
                    "Return ONLY JSON: "
                    '{"en":"...","ru":"..."}'
                ),
            },
            {
                "role": "user",
                "content": f"Generate for level {level}. Variation seed: {seed or random.random()}",
            },
        ],
        {"en": fallback["en"], "ru": fallback["ru"]},
        temperature=0.95,
        max_tokens=450,
    )
    en = (data.get("en") or "").strip()
    ru = (data.get("ru") or "").strip()
    if not en or not ru:
        return fallback
    return {"en": en, "ru": ru}


def generate_vocab(level: str, used: list[str] | None = None) -> dict:
    """
    Одно английское слово строго своего CEFR + русские ответы.
    Словари сложнее: B1 ≠ weather/school.
    """
    used = used or []
    hard_hint = {
        "C2": "rare academic/abstract verbs or nouns (nuance-level)",
        "C1": "advanced verbs/nouns like scrutinize, mitigate, coherent",
        "B2": "upper-intermediate: inevitably, thorough, reluctant, outcome",
        "B1": "true B1: experience, prefer, available, suggest, improve — NOT baby words like weather, school, family",
        "A2": "A2: busy, hungry, invite, travel — not cat/house",
        "A1": "A1 basic nouns/verbs: book, milk, name, house",
        "A0": "A0: hello, big, red, dog, I, you",
    }.get(level, "intermediate")

    fallback_map = {
        "C2": {"en": "unprecedented", "ru": ["беспрецедентный"]},
        "C1": {"en": "consequence", "ru": ["последствие"]},
        "B2": {"en": "reluctant", "ru": ["неохотный", "нежелающий"]},
        "B1": {"en": "available", "ru": ["доступный"]},
        "A2": {"en": "hungry", "ru": ["голодный"]},
        "A1": {"en": "book", "ru": ["книга"]},
        "A0": {"en": "hello", "ru": ["привет", "здравствуйте"]},
    }
    fallback = fallback_map.get(level, fallback_map["A1"])

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Generate ONE English word for a CEFR vocabulary placement item. "
                    f"Level {level}: {hard_hint}. "
                    "Do NOT reuse words from the avoid list. "
                    "Avoid childish/easy words if level is B1+. "
                    "Return ONLY JSON: "
                    '{"en":"word","ru":["перевод1","перевод2"]}'
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level: {level}\n"
                    f"Avoid: {', '.join(used) if used else 'none'}\n"
                    f"Seed: {random.random()}"
                ),
            },
        ],
        fallback,
        temperature=0.9,
        max_tokens=120,
    )
    en = (data.get("en") or "").strip()
    ru = data.get("ru") or []
    if isinstance(ru, str):
        ru = [ru]
    ru = [str(x).strip() for x in ru if str(x).strip()]
    if not en or not ru:
        return fallback
    return {"en": en, "ru": ru}


def generate_listen(level: str, used: list[str] | None = None) -> str:
    used = used or []
    fallback = {
        "C2": "Although funding seemed secure, several members still questioned the long-term plan.",
        "C1": "Many professionals improve faster when they review mistakes after each meeting.",
        "B2": "I would join the course next month if the schedule fits my work.",
        "B1": "My cousin works near the station and finishes late on Fridays.",
        "A2": "She takes the bus to work and comes home at six.",
        "A1": "This is my bag and that is my book.",
        "A0": "I am fine. Good morning.",
    }.get(level, "I like learning English every day.")

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Create ONE unique English listening sentence for a placement test. "
                    f"CEFR {level}. Length: speakable in under 10 seconds. "
                    "No quotes. Avoid reused sentences. "
                    'Return ONLY JSON: {"text":"..."}'
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {level}. Avoid: {'; '.join(used) if used else 'none'}. "
                    f"Seed {random.random()}"
                ),
            },
        ],
        {"text": fallback},
        temperature=0.95,
        max_tokens=100,
    )
    text = (data.get("text") or "").strip()
    return text or fallback


def generate_write_topic(level: str) -> str:
    fallback = pick_topic(level)
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Create ONE unique English writing prompt for a placement test. "
                    f"CEFR {level}. One clear sentence in English. "
                    'Return ONLY JSON: {"topic":"..."}'
                ),
            },
            {
                "role": "user",
                "content": f"Level {level}. Seed {random.random()}",
            },
        ],
        {"topic": fallback},
        temperature=0.95,
        max_tokens=80,
    )
    topic = (data.get("topic") or "").strip()
    return topic or fallback


def estimate_level_from_translation(text_level: str, score: int) -> str:
    """Строгая оценка после перевода (внутри, пользователю не показываем)."""
    from data.assessment_data import level_index, LEVELS

    i = level_index(text_level)
    if score >= 90:
        est = i
    elif score >= 75:
        est = max(0, i - 1)
    elif score >= 55:
        est = max(0, i - 2)
    elif score >= 35:
        est = max(0, i - 3)
    elif score >= 15:
        est = max(0, i - 4)
    else:
        est = 0
    return LEVELS[est]
