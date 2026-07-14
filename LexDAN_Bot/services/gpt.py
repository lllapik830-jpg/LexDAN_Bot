"""
Общение (живые правки по грамматике) + судьи для теста уровня.
"""

import json
import logging
import re
import requests
from config import OPENROUTER_API_KEY

SYSTEM_PROMPT = """
You are LexDAN — a warm human English tutor on Telegram.
Student is Russian-speaking. Messages may be from voice transcripts.

Return ONLY JSON (no markdown).

Schema:
{"has_error":bool,"better_en":"","rule_ru":"","reply_en":""}

CRITICAL — how corrections work:
1) better_en is a MINIMAL fix of the student's OWN words.
2) Keep the SAME meaning. Do NOT rewrite into a new sentence/idea.
3) Do NOT replace a greeting with a different greeting (hello ≠ Hi how are you).
4) Do NOT invent content the student did not say.
5) Ignore capitalization and missing punctuation completely.
6) If the student message is already correct (example: "hello") → has_error=false, better_en="", rule_ru="".
7) Spelling typos still count (hallo → hello). Grammar counts (I likes → I like).

Examples:
Student: "hello"
→ {"has_error":false,"better_en":"","rule_ru":"","reply_en":"Hey! How are you today?"}

Student: "hallo"
→ {"has_error":true,"better_en":"hello","rule_ru":"Это опечатка: правильно hello (привет).","reply_en":"Hey! Nice to meet you — how are you?"}

Student: "i likes cow"
→ {"has_error":true,"better_en":"I like cow","rule_ru":"После I глагол без -s: I like (не likes).","reply_en":"Cool! Do you like milk too?"}

Student: "I go to school yesterday"
→ {"has_error":true,"better_en":"I went to school yesterday","rule_ru":"Yesterday = прошедшее время: went, не go.","reply_en":"Nice! What did you do there?"}

BAD (never do this):
Student: "hello" → better_en "Hi! How are you today?"  ❌
Student: "i likes cow" → better_en "I love playing chess" ❌

reply_en = separate warm tutor reply about what they said + one easy question.
Never say "As an AI".
"""


def ask_tutor(user_text: str, user_name: str = "Student") -> dict:
    fallback = {
        "has_error": False,
        "better_en": "",
        "rule_ru": "",
        "reply_en": "Hey! I didn't catch that — can you say it again?",
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
                        "content": (
                            SYSTEM_PROMPT
                            + f"\nStudent's name: {user_name}. Use the name naturally sometimes."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Minimal-correct the student message if needed. "
                            "Preserve meaning. Separate chat reply in reply_en.\n\n"
                            f"Student message: {user_text}"
                        ),
                    },
                ],
                "max_tokens": 350,
                "temperature": 0.25,
            },
            timeout=25,
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"].strip()
        parsed = _parse_tutor_json(raw) or fallback
        return _sanitize_correction(user_text, parsed)
    except Exception as e:
        logging.error(f"GPT error: {e}")
        return fallback


def _normalize_tokens(text: str) -> list[str]:
    text = (text or "").lower()
    text = re.sub(r"[^a-zа-яё0-9\s']", " ", text)
    return [t for t in text.split() if t]


def _is_minimal_correction(user_text: str, better_en: str) -> bool:
    """Проверка: правка близка к исходной фразе, а не новый смысл."""
    u = _normalize_tokens(user_text)
    b = _normalize_tokens(better_en)
    if not u or not b:
        return False

    # короткие реплики (hello/hallo): правка тоже короткая
    if len(u) <= 2:
        if len(b) > 4:
            return False
        return (u[0][:2] == b[0][:2]) or (
            abs(len(u[0]) - len(b[0])) <= 2 and u[0][0] == b[0][0]
        )

    # для фраз: много общих слов И похожая длина
    overlap = len(set(u) & set(b))
    if overlap >= max(1, len(set(u)) - 2):
        return True
    if overlap / max(len(set(u)), 1) >= 0.5 and abs(len(u) - len(b)) <= 3:
        return True
    return False


def _same_ignoring_noise(user_text: str, better_en: str) -> bool:
    """Одинаковый смысл без учёта регистра/пунктуации."""
    return _normalize_tokens(user_text) == _normalize_tokens(better_en)


def _sanitize_correction(user_text: str, result: dict) -> dict:
    """Если модель переписала смысл — считаем, что ошибки нет."""
    if not result.get("has_error"):
        result["better_en"] = ""
        result["rule_ru"] = ""
        return result

    better = (result.get("better_en") or "").strip()
    if not better:
        result["has_error"] = False
        result["rule_ru"] = ""
        return result

    # "hello" → "Hello" не ошибка
    if _same_ignoring_noise(user_text, better):
        result["has_error"] = False
        result["better_en"] = ""
        result["rule_ru"] = ""
        return result

    if not _is_minimal_correction(user_text, better):
        logging.info(
            f"Dropped non-minimal correction: '{user_text}' -> '{better}'"
        )
        result["has_error"] = False
        result["better_en"] = ""
        result["rule_ru"] = ""
    return result


def judge_translation(source_en: str, reference_ru: str, user_ru: str) -> dict:
    fallback = {"score": 20, "cefr_estimate": "A1"}
    prompt = {
        "role": "system",
        "content": (
            "Strict placement-test judge for English→Russian translation. "
            "Score 0-100. Be STRICT: demand close meaning and decent Russian. "
            "Typos ok if meaning is clear; invented meaning = low score. "
            "Also estimate CEFR A0-C2. "
            'Return ONLY JSON: {"score":0-100,"cefr_estimate":"A2"}'
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"EN:\n{source_en}\n\nRU reference:\n{reference_ru}\n\n"
            f"Student:\n{user_ru}"
        ),
    }
    return _ask_json([prompt, user], fallback, temperature=0.0)


def judge_vocab(en_word: str, acceptable_ru: list[str], user_ru: str) -> dict:
    fallback = {"correct": False}
    prompt = {
        "role": "system",
        "content": (
            "Strict vocab check. correct=true only if meaning clearly matches. "
            "Close synonyms OK; vague/wrong = false. "
            'Return ONLY JSON: {"correct":bool}'
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"EN: {en_word}\nAcceptable RU: {', '.join(acceptable_ru)}\n"
            f"Student: {user_ru}"
        ),
    }
    return _ask_json([prompt, user], fallback, temperature=0.0)


def judge_listening(expected_en: str, user_text: str) -> dict:
    fallback = {"correct": False, "score": 20}
    prompt = {
        "role": "system",
        "content": (
            "Strict listening dictation check. "
            "Small spelling mistakes OK if words are clear. "
            "Missing key words / wrong meaning = incorrect. "
            "score>=85 required for correct=true. "
            'Return ONLY JSON: {"correct":bool,"score":0-100}'
        ),
    }
    user = {
        "role": "user",
        "content": f"Expected:\n{expected_en}\n\nStudent:\n{user_text}",
    }
    return _ask_json([prompt, user], fallback, temperature=0.0)


def judge_writing(topic: str, user_text: str, current_level: str) -> dict:
    fallback = {"cefr_estimate": current_level}
    prompt = {
        "role": "system",
        "content": (
            "Strict CEFR writing placement judge A0-C2. "
            "Be conservative: if between two levels, choose the LOWER one. "
            'Return ONLY JSON: {"cefr_estimate":"B1"}'
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"Approx prior level: {current_level}\nTopic: {topic}\n\n"
            f"Student text:\n{user_text}"
        ),
    }
    return _ask_json([prompt, user], fallback, temperature=0.0)


def format_tutor_message(result: dict, heard_text: str | None = None) -> str:
    """Красивое HTML-сообщение для Telegram."""
    parts = []

    if heard_text:
        parts.append(f"🗣 <b>Услышал:</b> <i>{_esc(heard_text)}</i>")
        parts.append("")

    has_error = bool(result.get("has_error"))
    better = _clean_field(result.get("better_en") or "")
    rule = _clean_field(result.get("rule_ru") or "")

    if has_error and not better and not rule:
        has_error = False

    if has_error:
        parts.append("✏️ <b>Не совсем так</b>")
        if better:
            parts.append(f"Правильно будет: <b>{_esc(better)}</b>")
        if rule:
            parts.append("")
            parts.append(f"💡 <b>Почему:</b>\n{_esc(rule)}")
    else:
        parts.append("✅ <b>Ошибки отсутствуют — молодец!</b> 🎉")

    parts.append("")
    parts.append("────────")
    parts.append("")
    parts.append(f"💬 {_esc(result.get('reply_en') or '')}")

    return "\n".join(parts)


_BAD_PLACEHOLDERS = (
    "пустая строка",
    "грамматическая/лексическая",
    "дружелюбное объяснение",
    "естественный вариант",
    "живой ответ",
    "лёгкий follow-up",
    "short friendly",
    "correct natural",
    "warm 1-2",
)


def _clean_field(text: str) -> str:
    t = (text or "").strip()
    low = t.lower()
    for bad in _BAD_PLACEHOLDERS:
        if bad.lower() in low:
            return ""
    return t


def _esc(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _ask_json(
    messages: list,
    fallback: dict,
    temperature: float = 0.1,
    max_tokens: int = 350,
) -> dict:
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
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=35,
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
    if not reply or _clean_field(reply) == "":
        # если reply сам похож на плейсхолдер — отбрасываем
        if not reply or any(b.lower() in reply.lower() for b in _BAD_PLACEHOLDERS):
            return None

    better = _clean_field(data.get("better_en") or "")
    rule = _clean_field(data.get("rule_ru") or "")

    has_error = data.get("has_error")
    if isinstance(has_error, str):
        has_error = has_error.strip().lower() in {"1", "true", "yes"}
    elif has_error is None:
        has_error = bool(better or rule)
    else:
        has_error = bool(has_error)

    if has_error and not better and not rule:
        has_error = False

    return {
        "has_error": has_error,
        "better_en": better,
        "rule_ru": rule,
        "reply_en": reply,
    }
