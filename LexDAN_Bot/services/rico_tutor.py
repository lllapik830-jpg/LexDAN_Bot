"""
Рико-тьютор: свободный чат по теме + генерация/проверка заданий + помощь.
"""

import logging
import random

import requests
from config import OPENROUTER_API_KEY
from services.gpt import _ask_json


def rico_topic_chat_text(level: str, topic_title: str, question: str, user_name: str = "друг") -> str:
    fallback = (
        "🦜 Хм, давай так: напиши свой пример по теме — разберём вместе! "
        "Я на связи."
    )
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Ты попугай Рико 🦜 — дружелюбный репетитор. "
                            "Отвечай по-русски, с английскими примерами. "
                            "Коротко, ясно, по-человечески. Не используй JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Уровень: {level}. Тема грамматики: {topic_title}. "
                            f"Ученика зовут {user_name}.\nВопрос: {question}"
                        ),
                    },
                ],
                "max_tokens": 450,
                "temperature": 0.55,
            },
            timeout=30,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        if not text.startswith("🦜"):
            text = f"🦜 {text}"
        return text
    except Exception as e:
        logging.error(f"Rico chat error: {e}")
        return fallback


def generate_grammar_exercise(
    level: str,
    topic_title: str,
    exercise_num: int,
) -> dict:
    """
    Возвращает:
    {
      kind: mcq|write,
      prompt: str,
      options: [4 strings] | null,
      answer: str,  # exact option text or expected answer
      tip: str
    }
    """
    # 1–4, 6 — выбор кнопкой; 5, 7, 8 — сам пишет
    kind = "mcq" if exercise_num in {1, 2, 3, 4, 6} else "write"
    labels = {
        1: "Choose the correct word form for the blank. One sentence with ____ .",
        2: "Choose the grammatically correct sentence.",
        3: "Fill the blank: choose the best option.",
        4: "Which sentence has NO grammar mistake?",
        5: "Rewrite the sentence using the target grammar. Student will type the answer.",
        6: "Choose the option with the correct word order.",
        7: "Translate the Russian sentence into English using the topic grammar.",
        8: "Write 2 short English sentences using the topic grammar.",
    }

    fallback_options = ["am", "is", "are", "be"]
    fallback = {
        "kind": "mcq",
        "prompt": f"({level} · {topic_title})\nI ____ a student.",
        "options": fallback_options,
        "answer": "am",
        "tip": "После I обычно am.",
    }
    if kind == "write":
        write_prompts = {
            5: "Перепиши предложение, используя грамматику темы (смотри инструкцию внутри prompt из JSON).",
            7: "Переведи на английский, используй тему урока:\nЯ живу в городе.",
            8: "Напиши 2 коротких предложения по теме урока.",
        }
        fallback = {
            "kind": "write",
            "prompt": f"({level} · {topic_title})\n{write_prompts.get(exercise_num, write_prompts[8])}",
            "options": None,
            "answer": "I live in a city.",
            "tip": "Пиши коротко и по теме.",
        }

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Create ONE English grammar exercise for Telegram. "
                    f"CEFR level: {level}. Topic: {topic_title}. "
                    f"Task style #{exercise_num}: {labels.get(exercise_num, '')} "
                    f'Output kind MUST be "{kind}". '
                    "Difficulty must match the level (not too easy/hard). "
                    "Return ONLY JSON. "
                    'For MCQ: {"kind":"mcq","prompt":"...with ____ ...","options":["a","b","c","d"],'
                    '"answer":"exact option text","tip":"short Russian tip"} '
                    'For WRITE: {"kind":"write","prompt":"...","options":null,'
                    '"answer":"model answer","tip":"short Russian tip"}'
                ),
            },
            {
                "role": "user",
                "content": f"Make exercise {exercise_num}/8. Seed {random.random()}",
            },
        ],
        fallback,
        temperature=0.7,
        max_tokens=350,
    )

    kind_out = kind
    prompt = (data.get("prompt") or fallback["prompt"]).strip()
    tip = (data.get("tip") or fallback["tip"]).strip()
    answer = (data.get("answer") or fallback["answer"]).strip()
    options = data.get("options")

    if kind_out == "mcq":
        if not isinstance(options, list) or len(options) < 4:
            options = list(fallback_options)
        options = [str(x) for x in options[:4]]
        if answer not in options:
            answer = options[0]
        return {
            "kind": "mcq",
            "prompt": prompt,
            "options": options,
            "answer": answer,
            "tip": tip,
        }

    return {
        "kind": "write",
        "prompt": prompt,
        "options": None,
        "answer": answer,
        "tip": tip,
    }


def check_write_answer(
    level: str,
    topic_title: str,
    prompt: str,
    model_answer: str,
    user_answer: str,
) -> dict:
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Check student's English answer for a grammar exercise. "
                    "Be fair: meaning + target grammar matter more than style. "
                    'Return ONLY JSON: {"correct":bool,"feedback_ru":"short friendly Russian"}'
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {level}. Topic {topic_title}.\n"
                    f"Task: {prompt}\nModel: {model_answer}\nStudent: {user_answer}"
                ),
            },
        ],
        {"correct": False, "feedback_ru": "Попробуй ещё раз, чуть точнее по теме."},
        temperature=0.0,
    )
    return data


def rico_help_for_exercise(
    level: str,
    topic_title: str,
    prompt: str,
    options: list[str] | None,
) -> str:
    opt_txt = ", ".join(options) if options else "(письменный ответ)"
    fallback = "🦜 Подсказка: вспомни правило темы и отбрось лишнее. Ты справишься!"
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Ты Рико 🦜. Дай подсказку НА РУССКОМ по конкретному заданию, "
                            "с мини-примером. НЕ называй прямой правильный вариант-букву, "
                            "если это выбор из кнопок — наведи на правило. Коротко."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Уровень {level}, тема {topic_title}.\n"
                            f"Задание: {prompt}\nВарианты: {opt_txt}"
                        ),
                    },
                ],
                "max_tokens": 280,
                "temperature": 0.4,
            },
            timeout=25,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        if not text.startswith("🦜"):
            text = f"🦜 {text}"
        return text
    except Exception as e:
        logging.error(f"Rico help error: {e}")
        return fallback
