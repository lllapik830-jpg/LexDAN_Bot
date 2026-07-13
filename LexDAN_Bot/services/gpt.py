"""
Общение с ИИ (через OpenRouter → модель ChatGPT).

Бот:
1) смотрит ошибки ученика
2) пишет как сказать естественнее
3) отвечает коротко по-английски и задаёт вопрос дальше
"""

import json
import logging
import re
import requests
from config import OPENROUTER_API_KEY

SYSTEM_PROMPT = """
You are LexDAN — a friendly English tutor for Telegram.

The student may write or speak English (sometimes with mistakes).

ALWAYS answer in this exact JSON format (no markdown, no extra text):
{
  "mistakes_ru": "кратко по-русски что не так, или пустая строка если ошибок нет",
  "better_en": "как сказать естественнее как носитель, или пустая строка если всё ок",
  "reply_en": "короткий ответ 1-2 предложения на английском + один follow-up вопрос"
}

Rules:
- reply_en MUST be English only, short, warm, tutoring style
- mistakes_ru MUST be Russian (simple words) or ""
- If the message is already good: mistakes_ru="", better_en=""
- Do not invent mistakes
"""


def ask_tutor(user_text: str, user_name: str = "Student") -> dict:
    """
    Возвращает словарь:
    {
      "mistakes_ru": "...",
      "better_en": "...",
      "reply_en": "..."
    }
    """
    fallback = {
        "mistakes_ru": "",
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
                        "content": SYSTEM_PROMPT
                        + f"\nStudent's name: {user_name}.",
                    },
                    {"role": "user", "content": user_text},
                ],
                "max_tokens": 350,
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


def _parse_tutor_json(raw: str) -> dict | None:
    """Достаём JSON даже если модель обернула его в ```json ... ```."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # запасной путь: искать {...} внутри текста
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            return None
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None

    reply = (data.get("reply_en") or "").strip()
    if not reply:
        return None

    return {
        "mistakes_ru": (data.get("mistakes_ru") or "").strip(),
        "better_en": (data.get("better_en") or "").strip(),
        "reply_en": reply,
    }


def format_tutor_message(result: dict, heard_text: str | None = None) -> str:
    """Собирает красивый текст для Telegram."""
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
