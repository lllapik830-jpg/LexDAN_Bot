"""
Рико: тексты Vocabulary, карточки слов/фраз, проверка предложений.
"""

import logging
import random

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


def _format_word_card(word: dict, data: dict) -> str:
    en = word["en"]
    ru = word["ru"]
    emoji = word.get("emoji") or "📘"
    meaning = (data.get("meaning_ru") or f"Это значит «{ru}».").strip()
    assoc = (data.get("association_ru") or "").strip()
    e1 = (data.get("example1_en") or f"I use {en} every day.").strip()
    e1r = (data.get("example1_ru") or f"Я использую «{ru}» каждый день.").strip()
    e2 = (data.get("example2_en") or f"This is my {en}.").strip()
    e2r = (data.get("example2_ru") or f"Это мой/моя {ru}.").strip()

    lines = [
        f"🦜 {emoji} <b>{en}</b> — <i>{ru}</i>",
        "",
        f"<b>Что значит:</b> {meaning}",
    ]
    if assoc:
        lines.append(f"<b>Запомни:</b> {assoc}")
    lines += [
        "",
        "<b>Примеры:</b>",
        f"1. {e1}",
        f"<i>{e1r}</i>",
        f"2. {e2}",
        f"<i>{e2r}</i>",
        "",
        "✍️ Напиши <b>одно предложение</b> с этим словом на английском.",
    ]
    return "\n".join(lines)


def rico_word_card(level: str, topic_title: str, word: dict) -> str:
    en = word["en"]
    ru = word["ru"]
    emoji = word.get("emoji") or "📘"
    fallback = {
        "meaning_ru": f"Слово «{en}» значит «{ru}».",
        "association_ru": f"Представь картинку с эмодзи {emoji} — и сразу вспоминается «{ru}».",
        "example1_en": f"I know the word {en}.",
        "example1_ru": f"Я знаю слово «{ru}».",
        "example2_en": f"Today I learned {en}.",
        "example2_ru": f"Сегодня я выучил(а) «{ru}».",
    }
    try:
        data = _ask_json(
            [
                {
                    "role": "system",
                    "content": (
                        "Ты Рико 🦜 — дружелюбный репетитор английского для русскоязычных. "
                        "Объясни слово ТОЛЬКО по-русски (кроме самих английских примеров). "
                        "Верни JSON:\n"
                        "{"
                        '"meaning_ru":"краткое понятное объяснение на русском",'
                        '"association_ru":"короткая ассоциация/мнемоника на русском",'
                        '"example1_en":"простое предложение на английском со словом",'
                        '"example1_ru":"перевод примера 1 на русский",'
                        '"example2_en":"другое простое предложение на английском",'
                        '"example2_ru":"перевод примера 2 на русский"'
                        "}\n"
                        f"Эмодзи для ассоциации: {emoji}. Уровень CEFR: {level}."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Тема: {topic_title}. Слово: {en} = {ru}",
                },
            ],
            fallback,
            temperature=0.55,
            max_tokens=380,
        )
        return _format_word_card(word, data if isinstance(data, dict) else fallback)
    except Exception as e:
        logging.error(f"rico_word_card: {e}")
        return _format_word_card(word, fallback)


def _format_phrase_card(phrase: dict, data: dict) -> str:
    en = phrase["en"]
    ru = phrase["ru"]
    emoji = phrase.get("emoji") or "💬"
    meaning = (data.get("meaning_ru") or f"Это значит «{ru}».").strip()
    when = (data.get("when_ru") or "").strip()
    assoc = (data.get("association_ru") or "").strip()
    e1 = (data.get("example1_en") or f"I often say '{en}'.").strip()
    e1r = (data.get("example1_ru") or f"Я часто говорю: «{ru}».").strip()
    e2 = (data.get("example2_en") or f"People use '{en}' a lot.").strip()
    e2r = (data.get("example2_ru") or f"Люди часто используют «{ru}».").strip()

    lines = [
        f"🦜 {emoji} <b>{en}</b>",
        f"<i>{ru}</i>",
        "",
        f"<b>Что значит:</b> {meaning}",
    ]
    if when:
        lines.append(f"<b>Когда говорят:</b> {when}")
    if assoc:
        lines.append(f"<b>Запомни:</b> {assoc}")
    lines += [
        "",
        "<b>Примеры:</b>",
        f"1. {e1}",
        f"<i>{e1r}</i>",
        f"2. {e2}",
        f"<i>{e2r}</i>",
        "",
        "✍️ Напиши предложение с этой фразой на английском.",
    ]
    return "\n".join(lines)


def rico_phrase_card(level: str, topic_title: str, phrase: dict) -> str:
    en = phrase["en"]
    ru = phrase["ru"]
    emoji = phrase.get("emoji") or "💬"
    fallback = {
        "meaning_ru": f"Фраза «{en}» значит «{ru}».",
        "when_ru": "Говорят в повседневных ситуациях по смыслу фразы.",
        "association_ru": f"Эмодзи {emoji} поможет вспомнить «{ru}».",
        "example1_en": f"I say '{en}' to friends.",
        "example1_ru": f"Я говорю друзьям: «{ru}».",
        "example2_en": f"Everyone knows '{en}'.",
        "example2_ru": f"Все знают выражение «{ru}».",
    }
    try:
        data = _ask_json(
            [
                {
                    "role": "system",
                    "content": (
                        "Ты Рико 🦜. Объясни устойчивую фразу ТОЛЬКО по-русски "
                        "(примеры предложений — на английском + перевод). JSON:\n"
                        "{"
                        '"meaning_ru":"...",'
                        '"when_ru":"когда говорят",'
                        '"association_ru":"...",'
                        '"example1_en":"...",'
                        '"example1_ru":"...",'
                        '"example2_en":"...",'
                        '"example2_ru":"..."'
                        "}\n"
                        f"Эмодзи: {emoji}. Уровень: {level}."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Тема: {topic_title}. Фраза: {en} = {ru}",
                },
            ],
            fallback,
            temperature=0.55,
            max_tokens=380,
        )
        return _format_phrase_card(phrase, data if isinstance(data, dict) else fallback)
    except Exception as e:
        logging.error(f"rico_phrase_card: {e}")
        return _format_phrase_card(phrase, fallback)


def check_vocab_sentence(
    level: str,
    target_en: str,
    user_sentence: str,
    *,
    is_phrase: bool = False,
) -> dict:
    kind = "phrase" if is_phrase else "word"
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    f"You check a Russian student's English sentence that must use the target {kind}. "
                    "Be friendly like a tutor. "
                    "Accept minor grammar issues if the target is used correctly and meaning is clear. "
                    "Return ONLY JSON: "
                    '{"correct":true/false,"feedback_ru":"краткий отзыв по-русски",'
                    '"better_en":"исправленный вариант или пустая строка"}\n'
                    "If correct: correct=true, feedback_ru хвалит кратко, better_en=\"\". "
                    "If wrong: correct=false, feedback_ru объясняет проблему по-русски, "
                    "better_en = natural corrected English sentence WITH the target."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {level}. Target {kind}: {target_en}\n"
                    f"Student sentence: {user_sentence}"
                ),
            },
        ],
        {
            "correct": False,
            "feedback_ru": "Попробуй ещё раз — используй целевое слово/фразу в предложении.",
            "better_en": "",
        },
        temperature=0.0,
    )
    if not isinstance(data, dict):
        return {
            "correct": False,
            "feedback_ru": "Попробуй ещё раз.",
            "better_en": "",
        }
    data["correct"] = bool(data.get("correct"))
    data["feedback_ru"] = str(data.get("feedback_ru") or "").strip()
    data["better_en"] = str(data.get("better_en") or "").strip()
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
