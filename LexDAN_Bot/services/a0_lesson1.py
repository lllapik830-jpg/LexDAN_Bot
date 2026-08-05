# -*- coding: utf-8 -*-
"""A0.T1 Lesson 1 — playable pilot (v2 after timing feedback)."""

from __future__ import annotations

import random
import re
import time
from difflib import SequenceMatcher


def ensure_a0_pilot(user: dict) -> dict:
    p = user.get("a0_pilot")
    if not isinstance(p, dict):
        p = {}
        user["a0_pilot"] = p
    return p


def start_lesson1(user: dict) -> dict:
    p = {
        "lesson": "A0.T1.L1",
        "step": "ask_name",
        "started_at": time.time(),
        "name": "",
        "practice_i": 0,
        "listen_i": 0,
        "check_i": 0,
        "check_ok": 0,
        "check_tot": 0,
        "speak_round": 0,
        "last_audio": "",
        "mcq_opts": [],
        "mcq_correct": -1,
        "note": "",
        "explain_topic": "",
        "finished": False,
    }
    user["a0_pilot"] = p
    return p


def shuffle_mcq(options: list[str], correct: int) -> tuple[list[str], int]:
    """Никогда не оставлять correct стабильно на кнопке 1."""
    order = list(range(len(options)))
    random.shuffle(order)
    # если после shuffle correct снова на 0 и есть выбор — перетасовать ещё
    for _ in range(8):
        if order[0] != correct or len(order) < 2:
            break
        random.shuffle(order)
    disp = [options[i] for i in order]
    new_correct = order.index(correct)
    return disp, new_correct


PRACTICE = [
    {
        "q": "Hi, ___ Maya. Что вставить?",
        "options": ["I'm", "I", "Am I", "You"],
        "correct": 0,
    },
    {
        "q": "I am и I'm — это…",
        "options": [
            "один смысл, I'm короче",
            "разный смысл",
            "I'm только для вопросов",
            "I am нельзя в речи",
        ],
        "correct": 0,
    },
    {
        "q": "Про собеседника выбери норму:",
        "options": ["You're Alex.", "I'm Alex.", "Are Alex.", "Is you Alex."],
        "correct": 0,
    },
    {
        "q": "Как спросить «ты Дэн?»",
        "options": ["Are you Dan?", "You are Dan?", "Am you Dan?", "Is you Dan?"],
        "correct": 0,
    },
    {
        "q": "Короткий ответ «нет, я не …»",
        "options": ["No, I'm not.", "No, I amn't.", "No, I not.", "No, I'm no."],
        "correct": 0,
    },
    {
        "q": "Nice to meet you — это…",
        "options": [
            "приятно познакомиться",
            "как дела",
            "до завтра",
            "меня зовут",
        ],
        "correct": 0,
    },
]

LISTENINGS = [
    {
        "audio": "Hi, I'm Tom.",
        "q": "Как зовут человека на записи?",
        "options": ["Tom", "Tim", "Sam", "Bob"],
        "correct": 0,
    },
    {
        "audio": "Hello, I'm Sara. Nice to meet you.",
        "q": "Что было после имени?",
        "options": [
            "Nice to meet you",
            "How are you",
            "See you",
            "Good morning",
        ],
        "correct": 0,
    },
    {
        "audio": "Are you Alex?",
        "q": "Это вопрос или утверждение?",
        "options": ["Вопрос", "Утверждение", "Прощание", "Число"],
        "correct": 0,
    },
    {
        "audio": "Hi. I'm not Paul. I'm Mark.",
        "q": "Как его на самом деле зовут?",
        "options": ["Mark", "Paul", "Alex", "Tom"],
        "correct": 0,
    },
]

MINI_CHECK = [
    {
        "q": "Короткая форма от I am:",
        "options": ["I'm", "I'd", "I've", "I'll"],
        "correct": 0,
    },
    {
        "q": "Hi, ___ {name}.",
        "options": ["I'm", "You're", "Am", "Are"],
        "correct": 0,
        "use_name": True,
    },
    {
        "q": "Правильный вопрос:",
        "options": ["Are you Maya?", "You are Maya?", "Is you Maya?", "Am you Maya?"],
        "correct": 0,
    },
    {
        "q": "Короткий ответ «да, это я»:",
        "options": ["Yes, I am.", "Yes, I'm.", "Yes, I.", "Yes, am I."],
        "correct": 0,
    },
    {
        "q": "You're — это…",
        "options": ["you are", "you am", "your", "you is"],
        "correct": 0,
    },
    {
        "q": "Nice to meet you значит…",
        "options": [
            "приятно познакомиться",
            "до свидания",
            "как дела",
            "сколько лет",
        ],
        "correct": 0,
    },
]


def practice_item(p: dict) -> dict | None:
    i = int(p.get("practice_i") or 0)
    if i < 0 or i >= len(PRACTICE):
        return None
    return PRACTICE[i]


def listen_item(p: dict) -> dict | None:
    i = int(p.get("listen_i") or 0)
    if i < 0 or i >= len(LISTENINGS):
        return None
    return LISTENINGS[i]


def check_item(p: dict) -> dict | None:
    i = int(p.get("check_i") or 0)
    if i < 0 or i >= len(MINI_CHECK):
        return None
    item = dict(MINI_CHECK[i])
    if item.pop("use_name", False):
        name = p.get("name") or "Alex"
        item["q"] = item["q"].format(name=name)
    return item


def elapsed_min(p: dict) -> float:
    t0 = float(p.get("started_at") or time.time())
    return max(0.0, (time.time() - t0) / 60.0)


def _norm_tokens(text: str) -> list[str]:
    t = (text or "").lower().replace("'", " ")
    return re.findall(r"[a-zа-яё]+", t, flags=re.IGNORECASE)


def name_match(text: str | None, name: str) -> bool:
    """Имя должно быть узнаваемо; 'Dan' ≠ 'Danil'."""
    n = re.sub(r"[^a-z]", "", (name or "").lower())
    if len(n) < 2:
        return True
    raw = (text or "").lower()
    if n in raw:
        return True
    best = 0.0
    for w in _norm_tokens(raw):
        w = re.sub(r"[^a-z]", "", w.lower())
        if not w:
            continue
        best = max(best, SequenceMatcher(None, w, n).ratio())
    # строго: почти полное имя
    return best >= 0.86


def speaking_ok(text: str | None, name: str, *, need_nice: bool = False) -> tuple[bool, str]:
    """
    Возвращает (ok, подсказка_если_нет).
    Требует I'm/I am + узнаваемое имя (+ nice… по флагу).
    """
    t = (text or "").strip()
    if len(t) < 2:
        return False, "Слишком тихо/пусто. Ещё раз ближе к микрофону."
    low = t.lower()
    has_im = bool(re.search(r"\bi\s*am\b|\bi'?m\b|\bim\b", low))
    if not has_im:
        return False, "Нужно I'm или I am — без этого не засчитаю."
    if not name_match(t, name):
        return False, f"Имя почти не слышно. Скажи чётче: I'm {name}."
    if need_nice:
        if "nice" not in low and "meet" not in low:
            return False, "Добавь в конце: Nice to meet you."
    return True, ""


def rico_explain_reply(question: str, topic: str, name: str) -> str:
    """Живой ответ Рико в стиле хорошего репетитора/лингуст-тона."""
    try:
        from services.openrouter import chat_completion

        sys = (
            "Ты Рико — живой репетитор английского в Telegram для новичка A0.\n"
            "Пиши ПО-РУССКИ, как умный друг-преподаватель: тепло, с лёгким юмором, без канцелярита.\n"
            "Формат ОБЯЗАТЕЛЕН:\n"
            "— короткие абзацы (1–2 предложения);\n"
            "— между смысловыми кусками отделяй строкой со смайлом (типа 😊 или 🔑 или 🎧);\n"
            "— в конце спроси, понял ли ученик / что ещё уточнить.\n"
            "Не лей воду. Не копируй учебники дословно. Тема сейчас только: "
            "I am/I'm, you are/you're, Hi/Hello, Nice to meet you.\n"
            "Если дурь/оффтоп — доброжелательно, но твёрдо верни к теме.\n"
            "Объём: примерно 5–8 коротких предложений максимум."
        )
        return (
            chat_completion(
                [
                    {"role": "system", "content": sys},
                    {
                        "role": "user",
                        "content": f"Ученика зовут {name}. Тема блока: {topic}. Вопрос/реплика: {question}",
                    },
                ],
                temperature=0.65,
                max_tokens=320,
                timeout=20,
            )
            or ""
        ).strip()
    except Exception:
        return (
            f"Ок, {name}, давай совсем по-простому 😊\n\n"
            "I am и I'm — это одно и то же.\n\n"
            "🔑\n"
            "I'm просто короче — так говорят в жизни чаще.\n\n"
            "Понял? Напиши своими словами или задай ещё вопрос ✍️"
        )


def rico_react(kind: str, name: str = "") -> str:
    """Короткие человечные реакции вместо сухого ✅."""
    n = name or "друг"
    table = {
        "ok": [
            f"Есть, {n} 🔥",
            "В точку 👏",
            "Да! Чувствуется 😊",
            "Красиво, идём дальше 💪",
        ],
        "soft_no": [
            "Почти — но давай точнее 🧐",
            "Близко! Смотри правильный вариант 👇",
            "Не сердись, так и учат — вот как надо 🙂",
        ],
    }
    import random

    return random.choice(table.get(kind) or table["ok"])

