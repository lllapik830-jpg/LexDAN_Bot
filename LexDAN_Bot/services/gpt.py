"""
Общение (строгие правки с объяснением правил) + судьи для теста уровня.
"""

import json
import logging
import re
import requests
from config import OPENROUTER_API_KEY

SYSTEM_PROMPT = """
You are LexDAN — a strict but friendly English tutor for Russian-speaking students.

ALWAYS answer in this exact JSON format (no markdown, no extra text):
{
  "mistakes_ru": "конкретно что неправильно в тексте ученика",
  "rule_ru": "короткое объяснение ПОЧЕМУ (правило грамматики/лексики простыми словами, 1-2 предложения)",
  "better_en": "естественный правильный вариант на английском",
  "reply_en": "короткий ответ 1-2 предложения на английском + один follow-up вопрос"
}

STRICT RULES:
- If there is ANY mistake, fill mistakes_ru, rule_ru and better_en.
- rule_ru MUST mention the grammar/vocab rule (tenses, articles, prepositions, agreement, word order, collocation...).
- Only leave mistakes_ru/rule_ru/better_en empty when English is truly correct and natural.
- Catch typical Russian-speaker errors: articles, he go/goes, Present Simple vs Continuous, in/on/at, much/many, I am agree, etc.
- reply_en: English only, short, warm.
- mistakes_ru and rule_ru: Russian only.
"""


def ask_tutor(user_text: str, user_name: str = "Student") -> dict:
    fallback = {
        "mistakes_ru": "Не удалось разобрать сообщение.",
        "rule_ru": "",
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
                            "Find mistakes, explain the rule simply in Russian, "
                            "give a better English version, then continue chatting:\n\n"
                            f"{user_text}"
                        ),
                    },
                ],
                "max_tokens": 450,
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
    parts = []

    if heard_text:
        parts.append(f"🗣️ Ты сказал(а): {heard_text}")

    mistakes = result.get("mistakes_ru") or ""
    rule = result.get("rule_ru") or ""
    better = result.get("better_en") or ""

    if mistakes or better or rule:
        parts.append("✏️ Исправление:")
        if mistakes:
            parts.append(f"• Ошибка: {mistakes}")
        if rule:
            parts.append(f"• Почему: {rule}")
        if better:
            parts.append(f"• Лучше сказать: {better}")
    else:
        parts.append("✅ Ошибок нет — отлично!")

    parts.append(f"\n🇬🇧 {result['reply_en']}")
    return "\n".join(parts)


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
    if not reply:
        return None
    return {
        "mistakes_ru": (data.get("mistakes_ru") or "").strip(),
        "rule_ru": (data.get("rule_ru") or "").strip(),
        "better_en": (data.get("better_en") or "").strip(),
        "reply_en": reply,
    }
