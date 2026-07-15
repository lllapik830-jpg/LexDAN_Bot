"""Перевод последнего ответа бота на русский."""

import logging
import requests
from config import OPENROUTER_API_KEY


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
