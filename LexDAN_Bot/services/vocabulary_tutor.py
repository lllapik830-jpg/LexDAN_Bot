"""
Рико: тексты Vocabulary, карточки слов/фраз, проверка предложений.
"""

import logging
import random

import requests

from config import OPENROUTER_API_KEY
from services.gpt import _ask_json


def generate_vocab_text(
    level: str,
    topic_title: str,
    words: list[dict],
    *,
    kind: str = "words",
) -> dict:
    """
    kind=words: 6-7 предложений, 4-5 слов курсивом
    kind=phrases: до 5 предложений, 2 фразы курсивом
    """
    if kind == "phrases":
        labels = [p["en"] for p in words[:2]]
        count = 2
        fallback_en = (
            f"My family is very important to me. We often say <i>{labels[0] if labels else 'family first'}</i> "
            f"when we talk. Last weekend we had dinner together. "
            f"My grandmother told us <i>{labels[1] if len(labels) > 1 else 'home sweet home'}</i> "
            f"and everyone smiled."
        )
        fallback_ru = (
            "Моя семья очень важна для меня. Мы часто говорим выделенную фразу, когда разговариваем. "
            "В прошлые выходные мы ужинали вместе. Бабушка сказала вторую фразу — и все улыбнулись."
        )
    else:
        labels = [w["en"] for w in words[:5]]
        count = min(5, len(labels))
        hi = ", ".join(labels[:count])
        fallback_en = (
            f"Today I want to tell you about {topic_title.lower()}. "
            f"I see my <i>{labels[0] if labels else 'friend'}</i> every day. "
            f"We like to <i>{labels[1] if len(labels) > 1 else 'talk'}</i> together. "
            f"Sometimes we visit a <i>{labels[2] if len(labels) > 2 else 'place'}</i> nearby. "
            f"It makes me feel <i>{labels[3] if len(labels) > 3 else 'happy'}</i>. "
            f"I hope you enjoy these new words!"
        )
        fallback_ru = (
            f"Сегодня расскажу про тему «{topic_title}». "
            "Я каждый день вижу выделенных людей и места. "
            "Нам нравится проводить время вместе. "
            "Иногда мы ходим в интересные места рядом. "
            "Это делает меня счастливым. Надеюсь, тебе понравятся новые слова!"
        )

    word_list = "\n".join(f"- {w['en']} ({w['ru']})" for w in words[:count])
    system = (
        "Create a short English story for a vocabulary lesson. "
        "Return ONLY JSON: "
        '{"text_en":"...","text_ru":"...","highlighted":["word1",...]} '
        f"Level {level}, topic {topic_title}. "
    )
    if kind == "phrases":
        system += (
            "Max 5 sentences. Wrap EXACTLY 2 given phrases in <i>...</i> in BOTH languages. "
            "highlighted = list of 2 English phrases without tags."
        )
    else:
        system += (
            "6-7 sentences. Wrap EXACTLY 4-5 given words in <i>...</i> in English text. "
            "Same words wrapped in <i> in Russian translation. "
            "highlighted = list of English words/phrases used (without tags)."
        )

    data = _ask_json(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Use these items:\n{word_list}\nSeed {random.random()}"},
        ],
        {
            "text_en": fallback_en,
            "text_ru": fallback_ru,
            "highlighted": labels[:count],
        },
        temperature=0.75,
        max_tokens=500,
    )
    highlighted = data.get("highlighted") or labels[:count]
    if not isinstance(highlighted, list):
        highlighted = labels[:count]
    return {
        "text_en": (data.get("text_en") or fallback_en).strip(),
        "text_ru": (data.get("text_ru") or fallback_ru).strip(),
        "highlighted": [str(x) for x in highlighted[:count]],
    }


def rico_word_card(level: str, topic_title: str, word: dict) -> str:
    en = word["en"]
    ru = word["ru"]
    emoji = word.get("emoji") or "📘"
    fallback = (
        f"🦜 {emoji} <b>{en}</b> — <i>{ru}</i>\n\n"
        f"Пример: I know <b>{en}</b>.\n<i>Я знаю: {ru}.</i>\n\n"
        "✍️ Напиши <b>одно предложение</b> с этим словом на английском."
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
                            "Ты Рико 🦜. Объясни слово ученику: перевод, 2 примера EN+<i>RU</i>, "
                            f"ассоциация для запоминания, эмодзи {emoji}. "
                            "В конце: «✍️ Напиши одно предложение с этим словом на английском.» HTML ok."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Level {level}, topic {topic_title}, word {en} = {ru}",
                    },
                ],
                "max_tokens": 380,
                "temperature": 0.5,
            },
            timeout=28,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        if not text.startswith("🦜"):
            text = f"🦜 {emoji} {text}"
        return text
    except Exception as e:
        logging.error(f"rico_word_card: {e}")
        return fallback


def rico_phrase_card(level: str, topic_title: str, phrase: dict) -> str:
    en = phrase["en"]
    ru = phrase["ru"]
    emoji = phrase.get("emoji") or "💬"
    fallback = (
        f"🦜 {emoji} <b>{en}</b>\n<i>{ru}</i>\n\n"
        "✍️ Напиши предложение с этой фразой на английском."
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
                            "Ты Рико 🦜. Объясни устойчивую фразу: перевод, когда говорят, "
                            "2 примера EN+<i>RU</i>, ассоциация, эмодзи. "
                            "В конце попроси написать предложение с фразой. HTML."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Level {level}, topic {topic_title}, phrase {en} = {ru}",
                    },
                ],
                "max_tokens": 380,
                "temperature": 0.5,
            },
            timeout=28,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        if not text.startswith("🦜"):
            text = f"🦜 {emoji} {text}"
        return text
    except Exception as e:
        logging.error(f"rico_phrase_card: {e}")
        return fallback


def check_vocab_sentence(
    level: str,
    target_en: str,
    user_sentence: str,
    *,
    is_phrase: bool = False,
) -> dict:
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Check if student used the target word/phrase correctly in English. "
                    "Minor grammar ok if word/phrase used right. "
                    'JSON: {"correct":bool,"feedback_ru":"..."}'
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {level}. Target: {target_en}. Phrase={is_phrase}.\n"
                    f"Student: {user_sentence}"
                ),
            },
        ],
        {"correct": False, "feedback_ru": "Попробуй ещё раз — используй слово/фразу в предложении."},
        temperature=0.0,
    )
    return data


def rico_dont_remember(item: dict, *, is_phrase: bool = False) -> str:
    en = item["en"]
    ru = item["ru"]
    emoji = item.get("emoji") or "💡"
    kind = "фраза" if is_phrase else "слово"
    return (
        f"🦜 {emoji} Не страшно! <b>{en}</b> — <i>{ru}</i>\n\n"
        f"Запомни: {kind} «{en}» = {ru}.\n"
        f"Пример: <b>I use {en} every day.</b>\n"
        f"<i>Я использую «{ru}» каждый день.</i>\n\n"
        "Продолжаем — переведи следующее задание 💪"
    )
