"""
Общение (живые правки по грамматике) + судьи для теста уровня.
"""

import json
import logging
import re
import requests
from config import OPENROUTER_API_KEY

SYSTEM_PROMPT = """
You are LexDAN — a warm human English tutor on Telegram (NOT a cold chatbot).
Talk like a real teacher in a private lesson: kind, natural, lightly playful.

The student is Russian-speaking. Text may come from VOICE transcripts.

Return ONLY valid JSON (no markdown, no comments).

When there IS a spelling/grammar/vocab mistake:
{"has_error":true,"better_en":"Hello!","rule_ru":"Hallo — частая ошибка. Правильно hello.","reply_en":"Hi! How are you today?"}

When there is NO real mistake:
{"has_error":false,"better_en":"","rule_ru":"","reply_en":"Nice! What did you do yesterday?"}

Rules:
- Spelling mistakes count (hallo → hello).
- Ignore ONLY missing capitals and missing .!? punctuation.
- better_en = corrected English phrase/sentence.
- rule_ru = short Russian explanation of WHY.
- reply_en = warm English reply + one easy question. Use contractions.
- NEVER put instructions or placeholder text into JSON values.
- Never say "As an AI".
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
                            "Check the student message. "
                            "If wrong spelling/grammar/vocab — set has_error true and fill better_en + rule_ru. "
                            "If fine — has_error false and empty better_en/rule_ru. "
                            "Always write a natural tutor reply_en.\n\n"
                            f"Student: {user_text}"
                        ),
                    },
                ],
                "max_tokens": 400,
                "temperature": 0.4,
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
