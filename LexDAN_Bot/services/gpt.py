"""
Проверка уровня + более строгая работа тьютора в чате.
"""

import json
import logging
import re
import requests
from config import OPENROUTER_API_KEY

SYSTEM_PROMPT = """
You are LexDAN — a strict but friendly English tutor for Russian-speaking students.

The student writes or speaks English. You MUST carefully find grammar, vocabulary,
word order, articles, prepositions, and unnatural phrasing mistakes.

ALWAYS answer in this exact JSON format (no markdown, no extra text):
{
  "mistakes_ru": "кратко по-русски что не так",
  "better_en": "правильный/естественный вариант на английском",
  "reply_en": "короткий ответ 1-2 предложения на английском + один follow-up вопрос"
}

STRICT RULES:
- If there is ANY mistake (even small: a/an, tense, preposition, word choice, word order) you MUST fill mistakes_ru and better_en.
- Only leave mistakes_ru and better_en empty when the student's English is truly correct and natural.
- Do NOT say there are no mistakes if the text is broken, incomplete, or non-native in a clear way.
- Russian speakers often make these errors — catch them: articles (a/the), Present Simple vs Continuous, much/many, in/on/at, he go/he goes, I am agree, etc.
- reply_en MUST be English only, short, warm.
- mistakes_ru MUST be Russian.
"""


def ask_tutor(user_text: str, user_name: str = "Student") -> dict:
    fallback = {
        "mistakes_ru": "Не удалось разобрать сообщение.",
        "better_en": "",
        "reply_en": "Sorry, I couldn't process that. Can you try again?",
    }

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
                        "content": SYSTEM_PROMPT + f"\nStudent's name: {user_name}.",
                    },
                    {
                        "role": "user",
                        "content": (
                            "Check this student message carefully for EVERY mistake, "
                            "then continue the conversation:\n\n"
                            f"{user_text}"
                        ),
                    },
                ],
                "max_tokens": 400,
                "temperature": 0.2,
            },
            timeout=25,
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"].strip()
        return _parse_tutor_json(raw) or fallback
    except Exception as e:
        logging.error(f"GPT error: {e}")
        return fallback


def judge_translation(source_en: str, reference_ru: str, user_ru: str) -> dict:
    """
    Оценка письменного перевода EN→RU.
    returned: passed, score (0-100), cefr_estimate, feedback_ru
    """
    fallback = {
        "passed": False,
        "score": 40,
        "cefr_estimate": "A2",
        "feedback_ru": "Не удалось проверить перевод. Попробуй ещё раз.",
    }
    prompt = {
        "role": "system",
        "content": (
            "You assess English→Russian translation for a placement test. "
            "Compare student translation to meaning of the English source and the Russian reference. "
            "Be fairly strict: score>=78 means PASS (very close meaning and decent wording). "
            "Also estimate student's CEFR: A0,A1,A2,B1,B2,C1,C2. "
            "Return ONLY JSON: "
            '{"passed":bool,"score":0-100,"cefr_estimate":"B1","feedback_ru":"краткий отзыв по-русски"}'
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"EN source:\n{source_en}\n\n"
            f"RU reference:\n{reference_ru}\n\n"
            f"Student RU translation:\n{user_ru}"
        ),
    }
    return _ask_json([prompt, user], fallback)


def judge_vocab(en_word: str, acceptable_ru: list[str], user_ru: str) -> dict:
    fallback = {"correct": False, "feedback_ru": "Неверно."}
    prompt = {
        "role": "system",
        "content": (
            "Check if the student's Russian translation of an English word is acceptable. "
            "Synonyms and minor morphology are OK. "
            "Return ONLY JSON: "
            '{"correct":bool,"feedback_ru":"кратко по-русски"}'
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"English word: {en_word}\n"
            f"Acceptable Russian: {', '.join(acceptable_ru)}\n"
            f"Student answer: {user_ru}"
        ),
    }
    return _ask_json([prompt, user], fallback)


def judge_listening(expected_en: str, user_text: str) -> dict:
    fallback = {"correct": False, "score": 30, "feedback_ru": "Не похоже на оригинал."}
    prompt = {
        "role": "system",
        "content": (
            "The student listened to an English sentence and typed what they heard. "
            "Ignore small spelling mistakes if words are recognizable. "
            "score>=75 means correct enough. "
            "Return ONLY JSON: "
            '{"correct":bool,"score":0-100,"feedback_ru":"кратко по-русски"}'
        ),
    }
    user = {
        "role": "user",
        "content": f"Expected:\n{expected_en}\n\nStudent wrote:\n{user_text}",
    }
    return _ask_json([prompt, user], fallback)


def judge_writing(topic: str, user_text: str, current_level: str) -> dict:
    fallback = {
        "cefr_estimate": current_level,
        "feedback_ru": "Спасибо! Текст принят.",
    }
    prompt = {
        "role": "system",
        "content": (
            "Assess an English placement writing sample. "
            "Topic was given. Student may write up to ~10 sentences. "
            "Estimate CEFR A0-C2 from grammar, vocabulary, coherence. "
            "Return ONLY JSON: "
            '{"cefr_estimate":"B1","feedback_ru":"краткий отзыв по-русски"}'
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"Current approx level: {current_level}\n"
            f"Topic: {topic}\n\n"
            f"Student text:\n{user_text}"
        ),
    }
    return _ask_json([prompt, user], fallback)


def format_tutor_message(result: dict, heard_text: str | None = None) -> str:
    parts = []

    if heard_text:
        parts.append(f"🗣️ Ты сказал(а): {heard_text}")

    mistakes = result.get("mistakes_ru") or ""
    better = result.get("better_en") or ""

    if mistakes or better:
        parts.append("✏️ Исправление:")
        if mistakes:
            parts.append(f"• {mistakes}")
        if better:
            parts.append(f"• Лучше сказать: {better}")
    else:
        parts.append("✅ Ошибок нет — отлично!")

    parts.append(f"\n🇬🇧 {result['reply_en']}")
    return "\n".join(parts)


def _ask_json(messages: list, fallback: dict) -> dict:
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": 350,
                "temperature": 0.1,
            },
            timeout=30,
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"].strip()
        data = _extract_json(raw)
        if not data:
            return fallback
        merged = dict(fallback)
        merged.update(data)
        return merged
    except Exception as e:
        logging.error(f"GPT json error: {e}")
        return fallback


def _extract_json(raw: str) -> dict | None:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None


def _parse_tutor_json(raw: str) -> dict | None:
    data = _extract_json(raw)
    if not data:
        return None
    reply = (data.get("reply_en") or "").strip()
    if not reply:
        return None
    return {
        "mistakes_ru": (data.get("mistakes_ru") or "").strip(),
        "better_en": (data.get("better_en") or "").strip(),
        "reply_en": reply,
    }
