# -*- coding: utf-8 -*-
"""A0.T1 Lesson 1 — playable pilot for timing/quality check."""

from __future__ import annotations

import time
from typing import Any


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
        "listen_show": False,
        "speak_model": "Hi, I'm Alex. Nice to meet you.",
        "note": "",
        "fail_rounds": 0,
        "finished": False,
    }
    user["a0_pilot"] = p
    return p


PRACTICE = [
    {
        "q": "Выбери правильный вариант:\nHi, ___ Maya.",
        "options": ["I'm", "I", "Am I", "You"],
        "correct": 0,
    },
    {
        "q": "Смысл один и тот же?",
        "options": ["I am = I'm", "I am ≠ I'm", "I'm = you are", "I = I'm"],
        "correct": 0,
    },
    {
        "q": "Про собеседника:",
        "options": ["You're Alex.", "I'm Alex.", "Are Alex.", "Is you Alex."],
        "correct": 0,
    },
    {
        "q": "Вопрос:",
        "options": ["Are you Dan?", "You are Dan?", "Am you Dan?", "Is you Dan?"],
        "correct": 0,
    },
]

LISTENINGS = [
    {
        "audio": "Hi, I'm Tom.",
        "q": "Как зовут человека?",
        "options": ["Tom", "Tim", "Sam", "Bob"],
        "correct": 0,
    },
    {
        "audio": "Hello, I'm Sara. Nice to meet you.",
        "q": "Что она сказала после имени?",
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
        "q": "Это вопрос?",
        "options": ["Да", "Нет", "Это имя", "Это прощание"],
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
        "q": "Короткий ответ «да»:",
        "options": ["Yes, I am.", "Yes, I'm.", "Yes, I.", "Yes, am I."],
        "correct": 0,
    },
    {
        "q": "Слышишь (представь): “Nice to meet you.” Это…",
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


def speaking_ok(text: str | None, name: str) -> bool:
    t = (text or "").lower()
    if len(t.strip()) < 2:
        return False
    words = set(w.strip(".,!?") for w in t.replace("'", " ").split())
    # мягко: есть hi/hello и i + am/im или имя
    greet = "hi" in words or "hello" in words or "i'm" in t.lower() or "i am" in t.lower()
    has_i = "i" in words or "i'm" in t.lower() or "im" in words
    return greet or has_i or (name and name.lower() in t.lower())
