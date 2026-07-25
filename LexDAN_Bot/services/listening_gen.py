"""Генерация диалога Listening + заданий через GPT."""

from __future__ import annotations

import logging
import random

from services.voices import CHAT_VOICES, DEFAULT_VOICE_ID

log = logging.getLogger(__name__)

# Мужские / женские голоса из нашей библиотеки
_MALE = [
    {"key": "adam", "name": "Adam", "voice_id": DEFAULT_VOICE_ID},
    {"key": "scotty", "name": "Scotty", "voice_id": "NfUrCNRReUL9RXS9upG1"},
    {"key": "joe", "name": "Joe", "voice_id": "av1BMOR1GPgThz9p4fLo"},
    {"key": "ed", "name": "Ed", "voice_id": "dHd5gvgSOzSfduK4CvEg"},
    {"key": "lucas", "name": "Lucas", "voice_id": "wSqOdjeNqDrHcoK0zorF"},
    {"key": "jimbo", "name": "Jimbo", "voice_id": "YLbQE9U7P1K6rBNJWNSv"},
]
_FEMALE = [
    {"key": "emmaline", "name": "Emmaline", "voice_id": "nDJIICjR9zfJExIFeSCN"},
    {"key": "aria", "name": "Aria", "voice_id": "TC0Zp7WVFzhA8zpTlRqV"},
    {"key": "ruby", "name": "Ruby", "voice_id": "b8gbDOK0ybjX1VA89pBdX"},
]

# Fix ruby voice id - from voices.py it's b8gbDO0ybjX1VA89pBdX
_FEMALE[2]["voice_id"] = "b8gbDO0ybjX1VA89pBdX"


def _pick_voices(gender_a: str, gender_b: str) -> tuple[dict, dict]:
    pool_a = list(_MALE if gender_a == "male" else _FEMALE)
    pool_b = list(_MALE if gender_b == "male" else _FEMALE)
    va = random.choice(pool_a)
    vb = random.choice([v for v in pool_b if v["key"] != va["key"]] or pool_b)
    return va, vb


def _fallback_pack(level: str, topic: dict) -> dict:
    """Запасной контент, если GPT недоступен (кафе A2-ish)."""
    title = topic.get("title_en") or "Café"
    return {
        "speakers": [
            {"name": "Michael", "gender": "male"},
            {"name": "Anna", "gender": "female"},
        ],
        "turns": [
            {"speaker": "Michael", "text": f"Hi Anna! Shall we sit by the window? This {title.lower()} looks nice."},
            {"speaker": "Anna", "text": "Sure! I'm starving. Let's check the menu."},
            {"speaker": "Michael", "text": "I'll have a cappuccino and a cheese sandwich."},
            {"speaker": "Anna", "text": "Nice. I want a green salad and a glass of water."},
            {"speaker": "Michael", "text": "The waiter is coming. Do you want dessert later?"},
            {"speaker": "Anna", "text": "Maybe ice cream. After that we can walk in the park."},
            {"speaker": "Michael", "text": "Perfect. I'll pay the bill this time."},
            {"speaker": "Anna", "text": "Thanks! Next time it's on me. See you at seven tonight?"},
        ],
        "task1": [
            {
                "question": "What does Michael order to drink?",
                "options": ["Tea", "Cappuccino", "Orange juice", "Cola"],
                "correct": 1,
            },
            {
                "question": "What does Anna want to eat?",
                "options": ["Pizza", "A burger", "A green salad", "Soup"],
                "correct": 2,
            },
            {
                "question": "What time do they plan to meet later?",
                "options": ["At five", "At six", "At seven", "At eight"],
                "correct": 2,
            },
        ],
        "task2": [
            {
                "statement": "Michael ordered tea.",
                "is_true": False,
                "explain_ru": "Майкл заказал капучино, а не чай.",
            },
            {
                "statement": "Anna ordered a green salad.",
                "is_true": True,
                "explain_ru": "Да, Анна заказала зелёный салат.",
            },
            {
                "statement": "Michael will pay the bill.",
                "is_true": True,
                "explain_ru": "Майкл сказал, что оплатит счёт.",
            },
        ],
        "task3_events": [
            "Friends sit by the window",
            "Michael orders a cappuccino",
            "Anna orders a salad",
            "Michael offers to pay the bill",
        ],
    }


def generate_listening_pack(level: str, topic: dict) -> dict:
    """
    Полный пакет: 8 реплик, 3 MCQ, 3 T/F, 4 события по порядку.
    """
    from services.gpt import _ask_json

    fallback = _fallback_pack(level, topic)
    setting = topic.get("setting") or topic.get("title_en") or "everyday situation"
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "You create CEFR-appropriate English listening practice for Russian learners. "
                    "Return ONLY JSON with keys: speakers, turns, task1, task2, task3_events.\n"
                    "speakers: exactly 2 objects {name, gender} gender=male|female, English first names.\n"
                    "turns: exactly 8 objects {speaker, text} — natural spoken dialogue, short lines, "
                    f"CEFR {level}, setting: {setting}. Alternate speakers roughly.\n"
                    "task1: exactly 3 comprehension MCQs {question, options[4], correct(0-3)}. "
                    "Questions test LISTENING understanding (who/what/where/when), NOT grammar. "
                    "Options grammatically fine; only one matches the dialogue.\n"
                    "task2: exactly 3 true/false {statement, is_true, explain_ru}. "
                    "explain_ru short Russian reason.\n"
                    "task3_events: exactly 4 short English event phrases in CORRECT chronological order "
                    "from the dialogue.\n"
                    "No spoilers in speaker names beyond the dialogue facts."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level: {level}\n"
                    f"Topic: {topic.get('title_en')} ({topic.get('title_ru')})\n"
                    f"Setting: {setting}\n"
                    f"Seed: {random.random()}"
                ),
            },
        ],
        fallback,
        temperature=0.55,
        max_tokens=1400,
    )
    pack = _normalize_pack(data, fallback)
    # назначить голоса
    sp = pack["speakers"]
    g0 = (sp[0].get("gender") or "male").lower()
    g1 = (sp[1].get("gender") or "female").lower()
    if g0 not in {"male", "female"}:
        g0 = "male"
    if g1 not in {"male", "female"}:
        g1 = "female"
    v0, v1 = _pick_voices(g0, g1)
    voice_map = {sp[0]["name"]: v0, sp[1]["name"]: v1}
    pack["voice_map"] = {
        name: {"key": v["key"], "voice_id": v["voice_id"], "voice_name": v["name"]}
        for name, v in voice_map.items()
    }
    return pack


def _normalize_pack(data: dict, fallback: dict) -> dict:
    if not isinstance(data, dict):
        return fallback
    speakers = data.get("speakers")
    turns = data.get("turns")
    task1 = data.get("task1")
    task2 = data.get("task2")
    events = data.get("task3_events")
    if not (isinstance(speakers, list) and len(speakers) >= 2):
        return fallback
    if not (isinstance(turns, list) and len(turns) >= 6):
        return fallback
    # trim / pad
    sp0 = speakers[0] if isinstance(speakers[0], dict) else {"name": "Michael", "gender": "male"}
    sp1 = speakers[1] if isinstance(speakers[1], dict) else {"name": "Anna", "gender": "female"}
    n0 = str(sp0.get("name") or "Michael").strip() or "Michael"
    n1 = str(sp1.get("name") or "Anna").strip() or "Anna"
    clean_turns = []
    for t in turns[:8]:
        if not isinstance(t, dict):
            continue
        sp = str(t.get("speaker") or n0).strip()
        if sp not in {n0, n1}:
            sp = n0 if len(clean_turns) % 2 == 0 else n1
        text = str(t.get("text") or "").strip()
        if text:
            clean_turns.append({"speaker": sp, "text": text})
    while len(clean_turns) < 8:
        clean_turns.append(
            {"speaker": n0 if len(clean_turns) % 2 == 0 else n1, "text": "Okay, sounds good."}
        )
    clean_turns = clean_turns[:8]

    def _mcq(items, fb):
        out = []
        src = items if isinstance(items, list) else []
        for i in range(3):
            raw = src[i] if i < len(src) and isinstance(src[i], dict) else fb[i]
            opts = list(raw.get("options") or fb[i]["options"])[:4]
            while len(opts) < 4:
                opts.append(f"Option {len(opts)+1}")
            try:
                correct = int(raw.get("correct", fb[i]["correct"]))
            except (TypeError, ValueError):
                correct = fb[i]["correct"]
            correct = max(0, min(3, correct))
            out.append(
                {
                    "question": str(raw.get("question") or fb[i]["question"]).strip(),
                    "options": [str(o).strip() for o in opts],
                    "correct": correct,
                }
            )
        return out

    def _tf(items, fb):
        out = []
        src = items if isinstance(items, list) else []
        for i in range(3):
            raw = src[i] if i < len(src) and isinstance(src[i], dict) else fb[i]
            out.append(
                {
                    "statement": str(raw.get("statement") or fb[i]["statement"]).strip(),
                    "is_true": bool(raw.get("is_true", fb[i]["is_true"])),
                    "explain_ru": str(raw.get("explain_ru") or fb[i]["explain_ru"]).strip(),
                }
            )
        return out

    ev = [str(x).strip() for x in (events or []) if str(x).strip()]
    if len(ev) < 4:
        ev = list(fallback["task3_events"])
    ev = ev[:4]

    return {
        "speakers": [
            {"name": n0, "gender": str(sp0.get("gender") or "male")},
            {"name": n1, "gender": str(sp1.get("gender") or "female")},
        ],
        "turns": clean_turns,
        "task1": _mcq(task1, fallback["task1"]),
        "task2": _tf(task2, fallback["task2"]),
        "task3_events": ev,
    }
