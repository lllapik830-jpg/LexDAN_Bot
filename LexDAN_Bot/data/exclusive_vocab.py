"""
Слова и фразы из призовых паков 2/3 места — попадают в «Повторить изученные…».
Ключи: EX:rico_prize:<en.lower()>
"""

from __future__ import annotations

EX_LEVEL = "EX"
EX_TOPIC = "rico_prize"


def _w(en: str, ru: str, emoji: str = "✨") -> dict:
    return {"en": en, "ru": ru, "emoji": emoji}


def _p(en: str, ru: str, emoji: str = "💬") -> dict:
    return {"en": en, "ru": ru, "emoji": emoji}


# Слова (в основном 2 место · карты слов)
EXCLUSIVE_WORDS: dict[str, dict] = {
    "serendipity": _w("serendipity", "счастливая случайность / неожиданная находка", "🍀"),
    "petrichor": _w("petrichor", "запах земли после дождя", "🌧"),
    "ephemeral": _w("ephemeral", "мимолётный, недолговечный", "⏳"),
    "flabbergasted": _w("flabbergasted", "ошарашенный, поражённый", "😮"),
}

# Фразы / идиомы / полезные конструкции (2 и 3 место)
EXCLUSIVE_PHRASES: dict[str, dict] = {
    "spill the tea": _p("spill the tea", "рассказать сочные подробности / сплетни", "🫖"),
    "read the room": _p("read the room", "считать атмосферу, понимать что уместно", "👀"),
    "move the goalposts": _p("move the goalposts", "менять правила/критерии по ходу", "🥅"),
    "a blessing in disguise": _p("a blessing in disguise", "скрытое благо", "🎁"),
    "I have been waiting since 6 o'clock": _p(
        "I have been waiting since 6 o'clock",
        "Я жду с шести часов (Present Perfect Continuous)",
        "⏰",
    ),
    "I agree": _p("I agree", "Я согласен (не I am agree)", "✅"),
    "Don't forget to buy milk": _p(
        "Don't forget to buy milk",
        "Не забудь купить молоко (forget + to)",
        "🥛",
    ),
    "If I see her, I will tell her": _p(
        "If I see her, I will tell her",
        "Если увижу её, скажу ей (1-я условная)",
        "1️⃣",
    ),
    "If I had more free time, I would travel": _p(
        "If I had more free time, I would travel",
        "Если бы было больше свободного времени, я бы путешествовал (2-я условная)",
        "2️⃣",
    ),
    "I've been learning English for two years": _p(
        "I've been learning English for two years",
        "Я учу английский уже два года (Present Perfect Continuous)",
        "📚",
    ),
}


def get_exclusive_word(en: str) -> dict | None:
    return EXCLUSIVE_WORDS.get((en or "").strip().lower())


def get_exclusive_phrase(en: str) -> dict | None:
    key = (en or "").strip().lower()
    hit = EXCLUSIVE_PHRASES.get(key)
    if hit:
        return hit
    # мягкий поиск по нормализованному ключу
    for k, v in EXCLUSIVE_PHRASES.items():
        if k.lower() == key:
            return v
    return None


def resolve_exclusive_entry(kind: str, en: str) -> dict | None:
    if kind == "word":
        return get_exclusive_word(en)
    return get_exclusive_phrase(en)
