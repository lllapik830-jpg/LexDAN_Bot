"""
Общение (живые правки по грамматике) + судьи для теста уровня.
"""

import json
import logging
import random
import re
import requests
from config import OPENROUTER_API_KEY

SYSTEM_PROMPT = """
You are LexDAN / Rico — a warm English tutor in Telegram for Russian-speaking students.
You check structure carefully and rewrite toward NATURAL native English, keeping the student's meaning.

Return ONLY JSON (no markdown).

Schema:
{
  "has_error": true/false,
  "better_en": "native natural English with the SAME meaning",
  "errors_ru": "конкретно что не так в структуре/грамматике/словах (по-русски), или пусто",
  "tips_ru": "почему носитель сказал бы так; 1-3 полезных слова/фразы которые стоит добавить или заменить (по-русски)",
  "reply_en": "short chatty English reply + ONE fresh question"
}

CORRECTION RULES (strict):
1) Analyze word order, tenses, articles, prepositions, agreement, awkward phrasing.
2) better_en = how a native speaker would naturally say the SAME idea.
   - Keep the student's meaning/facts. Do NOT invent a new story.
   - If the message is long, heavy, or textbook-like → simplify to natural spoken English.
   - Fix logic only when the sentence is nonsense; otherwise preserve intent.
3) has_error=true if there are real mistakes OR the phrasing is clearly unnatural for a native.
4) If the sentence is already natural and correct → has_error=false, better_en="", errors_ru="", tips_ru="".
5) Ignore ONLY capitalization and ending punctuation as "errors", but you MAY still polish wording in better_en if unnatural.
6) Never praise mistakes. No "Молодец/Nice/Great" about wrong English.
7) tips_ru should teach: name concrete words/phrases to use next time.

CHAT RULES (reply_en):
1) React to THEIR topic, then ask ONE new open question.
2) NEVER reuse openers/questions from "recent replies" — change topic and wording every turn.
3) Never repeat: "Tell me something about your day", "what was the best part", "How was your day".
4) Rotate topics each turn: food, hobbies, city, work/study, weekend, sports, music, travel, friends, weather, plans, books, games.
5) 1–3 short sentences + one question. Spoken A2–B1 English.
6) Never sound like a textbook or an AI.
"""

_FALLBACK_REPLIES = [
    "Hey! What made you smile today?",
    "Nice chatting! Do you like cooking or ordering food more?",
    "Cool. What's one song you can't stop listening to?",
    "Okay! Are you more of a morning person or a night owl?",
    "Got it. What do you usually do after work or school?",
    "Interesting! Coffee or tea — what's your go-to?",
    "Alright. Tell me about your favorite place in your city.",
    "Hey! If you had a free Saturday, how would you spend it?",
    "Nice. Do you prefer movies at home or going out with friends?",
    "Okay! What's something small you want to learn this week?",
]


def ask_tutor(
    user_text: str,
    user_name: str = "Student",
    recent_replies: list[str] | None = None,
) -> dict:
    fallback = {
        "has_error": False,
        "better_en": "",
        "errors_ru": "",
        "tips_ru": "",
        "rule_ru": "",
        "reply_en": random.choice(_FALLBACK_REPLIES),
    }

    recent = [r for r in (recent_replies or []) if r][-8:]
    recent_block = ""
    if recent:
        recent_block = (
            "\n\nFORBIDDEN to reuse (recent reply_en). Invent a DIFFERENT question:\n- "
            + "\n- ".join(recent)
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
                            SYSTEM_PROMPT
                            + f"\nStudent's name: {user_name}. Use the name lightly sometimes."
                            + recent_block
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "1) Strictly check the student's English structure.\n"
                            "2) If anything is wrong OR unnatural, rewrite as a native would "
                            "(same meaning; simplify if too long/complex).\n"
                            "3) Explain mistakes and useful phrases in Russian fields.\n"
                            "4) Then reply_en with a fresh non-repeating question.\n\n"
                            f"Student message: {user_text}"
                        ),
                    },
                ],
                "max_tokens": 520,
                "temperature": 0.55,
            },
            timeout=30,
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"].strip()
        parsed = _parse_tutor_json(raw) or dict(fallback)
        parsed = _sanitize_correction(user_text, parsed)
        parsed = _ensure_diverse_reply(parsed, recent)
        return parsed
    except Exception as e:
        logging.error(f"GPT error: {e}")
        return fallback


def _normalize_tokens(text: str) -> list[str]:
    text = (text or "").lower()
    text = re.sub(r"[^a-zа-яё0-9\s']", " ", text)
    return [t for t in text.split() if t]


def _token_overlap_ratio(a: str, b: str) -> float:
    sa, sb = set(_normalize_tokens(a)), set(_normalize_tokens(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / max(len(sa | sb), 1)


def _same_ignoring_noise(user_text: str, better_en: str) -> bool:
    return _normalize_tokens(user_text) == _normalize_tokens(better_en)


def _keeps_meaning(user_text: str, better_en: str) -> bool:
    """Разрешаем «как носитель» (можно короче/естественнее), но не смену темы."""
    u = _normalize_tokens(user_text)
    b = _normalize_tokens(better_en)
    if not u or not b:
        return False
    if len(u) <= 2:
        return len(b) <= 8 and (
            u[0][:2] == b[0][:2] or _token_overlap_ratio(user_text, better_en) >= 0.3
        )
    # достаточно общих смысловых слов ИЛИ высокая доля overlap
    overlap = len(set(u) & set(b))
    if overlap >= max(1, min(3, len(set(u)) // 2)):
        return True
    return _token_overlap_ratio(user_text, better_en) >= 0.28


def _sanitize_correction(user_text: str, result: dict) -> dict:
    """Оставляем native-правку, если смысл сохранён; иначе чистим."""
    better = _clean_field(result.get("better_en") or "")
    errors = _clean_field(result.get("errors_ru") or "")
    tips = _clean_field(result.get("tips_ru") or result.get("rule_ru") or "")
    has_error = bool(result.get("has_error"))

    if better and _same_ignoring_noise(user_text, better):
        better = ""

    if better and not _keeps_meaning(user_text, better):
        logging.info(f"Dropped off-topic rewrite: '{user_text}' -> '{better}'")
        better = ""
        has_error = False
        errors = ""
        tips = ""

    # Если есть улучшение — показываем блок правки
    if better:
        has_error = True
    elif has_error and not better and not errors and not tips:
        has_error = False

    result["has_error"] = has_error
    result["better_en"] = better
    result["errors_ru"] = errors
    result["tips_ru"] = tips
    result["rule_ru"] = tips  # совместимость
    return result


def _ensure_diverse_reply(result: dict, recent: list[str]) -> dict:
    reply = _clean_field(result.get("reply_en") or "")
    banned_bits = (
        "tell me something about your day",
        "what was the best part",
        "best part of your day",
        "how was your day",
        "what did you do today",
    )
    low = reply.lower()
    recent_low = [(r or "").lower() for r in recent]
    repeated = False

    # один и тот же «шаблонный» вопрос уже был недавно
    for b in banned_bits:
        if b in low and any(b in r for r in recent_low):
            repeated = True
            break

    # почти тот же текст ответа, что уже отправляли
    for r in recent:
        if reply and _token_overlap_ratio(reply, r) >= 0.55:
            repeated = True
            break

    if not reply or repeated:
        pool = [
            x
            for x in _FALLBACK_REPLIES
            if all(_token_overlap_ratio(x, r) < 0.5 for r in recent)
            and not any(b in x.lower() and any(b in rl for rl in recent_low) for b in banned_bits)
        ]
        reply = random.choice(pool or _FALLBACK_REPLIES)
    result["reply_en"] = reply
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
    errors = _clean_field(result.get("errors_ru") or "")
    tips = _clean_field(result.get("tips_ru") or result.get("rule_ru") or "")

    if has_error and not better and not errors and not tips:
        has_error = False

    if better or errors or tips:
        parts.append("✏️ <b>Как сказал бы носитель</b>")
        if better:
            parts.append(f"<b>{_esc(better)}</b>")
        if errors:
            parts.append("")
            parts.append(f"<b>Что поправить:</b>\n{_esc(errors)}")
        if tips:
            parts.append("")
            parts.append(f"💡 <b>Полезно запомнить:</b>\n{_esc(tips)}")
        parts.append("")
        parts.append("Суть твоей мысли сохранили — просто сделали естественнее. Продолжаем!")
    else:
        parts.append("✅ <b>Звучит естественно — молодец!</b> 🎉")

    reply = _clean_field(result.get("reply_en") or "")
    if better or errors:
        low = reply.lower()
        for bad in ("молодец", "nice!", "great!", "awesome", "well done", "nice choice"):
            if bad in low:
                reply = "Got it — let's keep chatting."
                break

    parts.append("")
    parts.append("────────")
    parts.append("")
    parts.append(f"💬 {_esc(reply)}")

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
        if not reply or any(b.lower() in reply.lower() for b in _BAD_PLACEHOLDERS):
            return None

    better = _clean_field(data.get("better_en") or "")
    errors = _clean_field(data.get("errors_ru") or data.get("mistakes_ru") or "")
    tips = _clean_field(
        data.get("tips_ru") or data.get("rule_ru") or ""
    )

    has_error = data.get("has_error")
    if isinstance(has_error, str):
        has_error = has_error.strip().lower() in {"1", "true", "yes"}
    elif has_error is None:
        has_error = bool(better or errors or tips)
    else:
        has_error = bool(has_error)

    if has_error and not better and not errors and not tips:
        has_error = False

    return {
        "has_error": has_error,
        "better_en": better,
        "errors_ru": errors,
        "tips_ru": tips,
        "rule_ru": tips,
        "reply_en": reply,
    }
