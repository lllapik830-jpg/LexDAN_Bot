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
                            "После КАЖДОГО английского примера сразу ниже дай перевод "
                            "курсивом в HTML: <i>…</i>. "
                            "Формат ответа — HTML для Telegram (можно <b> и <i>). "
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
      answer: str,
      tip: str,
      help_count: 0
    }
    """
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

    beginner = level in {"A0", "A1"}
    fallback_options = ["am", "is", "are", "be"]
    fallback = {
        "kind": "mcq",
        "prompt": (
            f"({level} · {topic_title})\n"
            "Выбери правильную форму:\n"
            "I ____ a student.\n"
            "<i>Я ____ студент.</i>"
        ),
        "prompt_ru": "Выбери правильную форму глагола to be.\nЯ ____ студент.",
        "options": fallback_options,
        "answer": "am",
        "tip": "После I обычно am.",
    }
    if kind == "write":
        write_prompts = {
            5: "Перепиши предложение по теме урока (смотри задание ниже).",
            7: "Переведи на английский, используй тему урока:\nЯ живу в городе.",
            8: "Напиши 1–2 коротких предложения по теме урока (можно очень простые).",
        }
        fallback = {
            "kind": "write",
            "prompt": f"({level} · {topic_title})\n{write_prompts.get(exercise_num, write_prompts[8])}",
            "prompt_ru": write_prompts.get(exercise_num, write_prompts[8]),
            "options": None,
            "answer": "I live in a city.",
            "tip": "Пиши коротко и по теме.",
        }

    a0_hint = ""
    if beginner:
        a0_hint = (
            " IMPORTANT FOR A0/A1: Write task instructions as a short friendly story in Russian "
            "(Rico tutor voice). Keep English ONLY for the target sentence and answer options. "
            "Under each English sentence add Russian gloss in HTML <i>...</i>. "
            "Include prompt_ru: full Russian explanation of what to do AND translation of English parts. "
            "Use very simple vocabulary."
        )

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
                    f"{a0_hint} "
                    "Return ONLY JSON. "
                    'For MCQ: {"kind":"mcq","prompt":"...","prompt_ru":"полный перевод задания и англ. предложения на русском",'
                    '"options":["a","b","c","d"],"answer":"exact option text","tip":"short Russian tip"} '
                    'For WRITE: {"kind":"write","prompt":"...","prompt_ru":"что нужно сделать + перевод фраз на русском",'
                    '"options":null,"answer":"model answer","tip":"short Russian tip"}'
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

    prompt = (data.get("prompt") or fallback["prompt"]).strip()
    prompt_ru = (data.get("prompt_ru") or fallback.get("prompt_ru") or "").strip()
    tip = (data.get("tip") or fallback["tip"]).strip()
    answer = (data.get("answer") or fallback["answer"]).strip()
    options = data.get("options")

    if kind == "mcq":
        if not isinstance(options, list) or len(options) < 4:
            options = list(fallback_options)
        options = [str(x) for x in options[:4]]
        if answer not in options:
            lower_map = {o.lower(): o for o in options}
            if answer.lower() in lower_map:
                answer = lower_map[answer.lower()]
            else:
                answer = options[0]
        if not prompt_ru:
            prompt_ru = translate_exercise_prompt(prompt) or "Перевод временно недоступен."
        return {
            "kind": "mcq",
            "prompt": prompt,
            "prompt_ru": prompt_ru,
            "options": options,
            "answer": answer,
            "tip": tip,
            "help_count": 0,
        }

    if not prompt_ru:
        prompt_ru = translate_exercise_prompt(prompt) or "Перевод временно недоступен."
    return {
        "kind": "write",
        "prompt": prompt,
        "prompt_ru": prompt_ru,
        "options": None,
        "answer": answer,
        "tip": tip,
        "help_count": 0,
    }


def translate_exercise_prompt(prompt: str) -> str | None:
    """Переводит английскую часть задания для кнопки «Перевести»."""
    if not prompt:
        return None
    from services.translation import translate_to_russian

    clean = prompt.replace("<i>", "").replace("</i>", "").strip()
    # Убираем служебные префиксы уровня
    if "\n" in clean:
        lines = [ln for ln in clean.split("\n") if ln.strip() and not ln.strip().startswith("(")]
        clean = "\n".join(lines) if lines else clean
    ru = translate_to_russian(clean)
    if not ru:
        return None
    return ru


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
                    "For A0/A1 accept very simple answers if grammar target is ok. "
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
    reveal: bool = False,
    answer: str = "",
) -> str:
    opt_txt = ", ".join(options) if options else "(письменный ответ)"
    if reveal:
        fallback = (
            f"🦜 Правильный ответ: <b>{answer}</b>.\n"
            "Запомни правило и иди к следующему заданию!"
        )
    else:
        fallback = "🦜 Подсказка: вспомни правило темы и отбрось лишнее. Ты справишься!"

    try:
        if reveal:
            system = (
                "Ты Рико 🦜. Объяви правильный ответ и коротко объясни НА РУССКОМ, "
                "почему он верный, с мини-примером. English example + <i>русский перевод</i>. "
                f"Правильный ответ: {answer}. HTML ok."
            )
        else:
            system = (
                "Ты Рико 🦜. Дай ПОДСКАЗКУ НА РУССКОМ по заданию. "
                "НЕ называй правильный вариант и НЕ цитируй ответ дословно. "
                "Наведи на правило. Коротко. HTML: можно <i>."
            )
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system},
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


def rico_explain_wrong_final(
    level: str,
    topic_title: str,
    prompt: str,
    answer: str,
) -> str:
    fallback = (
        f"🦜 Неправильно. Правильный ответ: <b>{answer}</b>.\n"
        "Разбери пример и иди дальше 💪"
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
                            "Ты Рико 🦜. Ученик ошибся в последний раз. "
                            "Скажи, что неправильно, назови правильный ответ и коротко объясни "
                            "на русском + английский пример с <i>переводом</i>. HTML ok."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Уровень {level}, тема {topic_title}.\n"
                            f"Задание: {prompt}\nПравильный ответ: {answer}"
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
        logging.error(f"Rico final explain error: {e}")
        return fallback
