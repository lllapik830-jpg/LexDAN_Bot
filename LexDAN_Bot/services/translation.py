"""Перевод: EN→RU для кнопки «Перевести»; RU→EN для «скажи по-английски»."""

from __future__ import annotations

import logging
import re

import requests
from config import OPENROUTER_API_KEY

_SAY_EN_RE = re.compile(
    r"(?is)^\s*(?:"
    r"скажи\s+(?:это\s+)?по[- ]?английски|"
    r"скажи\s+на\s+английском|"
    r"переведи\s+на\s+английский|"
    r"как\s+(?:будет|сказать)\s+по[- ]?английски|"
    r"say\s+(?:this\s+)?in\s+english|"
    r"translate\s+(?:(?:this|to)\s+)?(?:into\s+)?english|"
    r"in\s+english(?:\s+please)?"
    r")\s*[,:\-–—]?\s*(.+?)\s*$"
)


def extract_say_english_payload(text: str) -> str | None:
    """
    Если пользователь просит сказать фразу по-английски и даёт русский текст —
    вернуть русскую фразу. Иначе None.
    """
    raw = (text or "").strip()
    if not raw:
        return None
    m = _SAY_EN_RE.match(raw)
    if not m:
        return None
    payload = (m.group(1) or "").strip()
    if not payload or len(payload) < 2:
        return None
    return payload


def translate_to_russian(text: str) -> str | None:
    if not text:
        return None

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
                            "Translate the English text to natural Russian. "
                            "Output ONLY the Russian translation, nothing else."
                        ),
                    },
                    {"role": "user", "content": text},
                ],
                "max_tokens": 400,
                "temperature": 0.2,
            },
            timeout=20,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(f"Translation error: {e}")
        return None


def translate_to_english(text: str) -> str | None:
    """Русский (или смешанный) → естественный английский. Только перевод."""
    if not text:
        return None

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
                            "Translate the user's phrase into natural spoken English. "
                            "Keep the same meaning and tone. "
                            "If the text is already English, return it lightly polished. "
                            "Output ONLY the English sentence(s), nothing else — "
                            "no quotes, no Russian, no explanations."
                        ),
                    },
                    {"role": "user", "content": text},
                ],
                "max_tokens": 400,
                "temperature": 0.2,
            },
            timeout=20,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip().strip("\"'")
    except Exception as e:
        logging.error(f"EN translation error: {e}")
        return None
