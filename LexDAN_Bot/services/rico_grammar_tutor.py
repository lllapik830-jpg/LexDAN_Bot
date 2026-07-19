"""
Рико как репетитор Grammar: диалог строго по темам уровня.
"""

from __future__ import annotations

import logging
import re

import requests

from config import OPENROUTER_API_KEY
from data.grammar_curriculum import get_topics


def _topics_block(level: str) -> str:
    topics = get_topics(level) or []
    if not topics:
        return f"Level {level}: general elementary grammar."
    lines = [f"- {t.get('title')}" for t in topics]
    return f"Level {level} Grammar topics (ONLY these):\n" + "\n".join(lines)


def ask_rico_grammar(
    level: str,
    user_text: str,
    *,
    user_name: str = "Student",
    recent_turns: list[dict] | None = None,
) -> str:
    """
    Дружелюбный репетитор: английский ответ + вопрос, только темы Grammar уровня.
    """
    topics_block = _topics_block(level)
    hist = ""
    turns = [t for t in (recent_turns or []) if t.get("text")][-8:]
    if turns:
        lines = []
        for t in turns:
            who = "Student" if t.get("role") == "user" else "Rico"
            lines.append(f"{who}: {t.get('text')}")
        hist = "\nRecent dialogue:\n" + "\n".join(lines)

    system = (
        "You are Rico 🦜 — a warm, friendly English grammar tutor (not a generic chatbot). "
        "You teach Russian-speaking students. "
        "Speak as a patient tutor: clear, encouraging, concrete examples. "
        "STRICT SCOPE: discuss ONLY the Grammar topics listed for this CEFR level. "
        "If the student asks about something outside these topics, gently redirect to a listed topic "
        "and offer to explain that grammar instead. "
        "Reply in simple spoken English (A2–B1 phrasing even on higher levels when teaching). "
        "1–4 short sentences + ONE clear follow-up question. "
        "You may briefly use a Russian gloss in parentheses for a hard term, but the reply is mostly English. "
        "Do NOT return JSON. Plain text only. No markdown headings."
        f"\n\n{topics_block}"
        f"\nStudent name: {user_name}."
        f"{hist}"
    )
    fallback = (
        f"Hey {user_name}! Let's practise grammar for {level}. "
        "Which topic from the list do you want me to explain first?"
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
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_text},
                ],
                "max_tokens": 420,
                "temperature": 0.55,
            },
            timeout=35,
        )
        response.raise_for_status()
        text = (response.json()["choices"][0]["message"]["content"] or "").strip()
        text = re.sub(r"^```(?:\w+)?\s*|\s*```$", "", text).strip()
        return text or fallback
    except Exception as e:
        logging.error(f"ask_rico_grammar: {e}")
        return fallback


def format_rico_grammar_message(reply_en: str) -> str:
    body = (reply_en or "").strip()
    body = (
        body.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f"🦜 <b>Рико:</b>\n{body}"
