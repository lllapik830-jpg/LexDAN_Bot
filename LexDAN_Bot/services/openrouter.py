"""
Общий клиент OpenRouter: keep-alive + быстрая модель для чата.
"""

from __future__ import annotations

import logging
import os

import requests
from config import OPENROUTER_API_KEY

# gpt-4o-mini: быстрее и обычно лучше 3.5 по правкам; переопределяется env
CHAT_MODEL = (os.getenv("OPENROUTER_CHAT_MODEL") or "openai/gpt-4o-mini").strip()
# Уроки/судьи — та же быстрая модель по умолчанию
DEFAULT_MODEL = (os.getenv("OPENROUTER_MODEL") or CHAT_MODEL).strip()

_session: requests.Session | None = None


def _get_session() -> requests.Session:
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update(
            {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://t.me/LexDAN_bot",
                "X-Title": "LexDAN",
            }
        )
    return _session


def chat_completion(
    messages: list[dict],
    *,
    model: str | None = None,
    temperature: float = 0.4,
    max_tokens: int = 280,
    timeout: float = 20,
) -> str:
    """
    Сырой content ответа ассистента.
    Raises requests/HTTP errors наружу — ловит вызывающий код.
    """
    payload = {
        "model": (model or DEFAULT_MODEL).strip() or CHAT_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    # Предпочитаем провайдеров с низкой задержкой, если OpenRouter поддержит
    payload["provider"] = {"sort": "latency"}

    r = _get_session().post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        timeout=timeout,
    )
    if r.status_code >= 400:
        # provider.sort поддерживается не всегда — повторяем без него
        body = (r.text or "")[:300]
        if r.status_code == 400 and "provider" in body.lower():
            payload.pop("provider", None)
            r = _get_session().post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                timeout=timeout,
            )
        if r.status_code >= 400:
            logging.error("OpenRouter HTTP %s: %s", r.status_code, (r.text or "")[:400])
            r.raise_for_status()
    data = r.json()
    return (data["choices"][0]["message"]["content"] or "").strip()
