# -*- coding: utf-8 -*-
"""Собрать data/vocab_example_bank.py: 2 адекватных EN/RU примера на каждое слово/фразу.

Запуск: python scripts/gen_vocab_example_bank.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))

from data.vocabulary_phrases import PHRASES  # noqa: E402
from data.vocabulary_words import WORDS  # noqa: E402

OUT = ROOT / "data" / "vocab_example_bank.py"

# Ручные оверрайды для слов, где шаблоны ломаются
WORD_OVERRIDES: dict[str, tuple[tuple[str, str], tuple[str, str]]] = {
    "abroad": (
        ("She wants to study abroad next year.", "Она хочет учиться за границей в следующем году."),
        ("Have you ever lived abroad?", "Ты когда-нибудь жил(а) за границей?"),
    ),
    "again": (
        ("Can you say that again, please?", "Можешь сказать это ещё раз, пожалуйста?"),
        ("I'll call you again tomorrow.", "Я позвоню тебе снова завтра."),
    ),
    "back": (
        ("I'll be back in ten minutes.", "Я вернусь через десять минут."),
        ("My back hurts after the long walk.", "У меня болит спина после долгой прогулки."),
    ),
    "fine": (
        ("I'm fine, thank you.", "Я в порядке, спасибо."),
        ("Everything will be fine.", "Всё будет хорошо."),
    ),
    "well": (
        ("I don't feel well today.", "Сегодня я плохо себя чувствую."),
        ("She speaks English very well.", "Она очень хорошо говорит по-английски."),
    ),
    "OK": (
        ("OK, let's start.", "Окей, давай начнём."),
        ("Is everything OK?", "Всё в порядке?"),
    ),
    "ok": (
        ("OK, let's start.", "Окей, давай начнём."),
        ("Is everything OK?", "Всё в порядке?"),
    ),
    "love": (
        ("I love my family.", "Я люблю свою семью."),
        ("They love this song.", "Им нравится эта песня."),
    ),
    "home": (
        ("I'm going home now.", "Я сейчас иду домой."),
        ("Home is where I feel safe.", "Дом — это место, где я чувствую себя в безопасности."),
    ),
    "later": (
        ("See you later!", "Увидимся позже!"),
        ("I'll do it later.", "Я сделаю это позже."),
    ),
    "name": (
        ("What's your name?", "Как тебя зовут?"),
        ("My name is Anna.", "Меня зовут Анна."),
    ),
    "help": (
        ("Can you help me, please?", "Можешь помочь мне, пожалуйста?"),
        ("I need help with this task.", "Мне нужна помощь с этим заданием."),
    ),
    "meet": (
        ("Nice to meet you!", "Приятно познакомиться!"),
        ("Let's meet at the café.", "Давай встретимся в кафе."),
    ),
    "see you": (
        ("See you tomorrow at school!", "Увидимся завтра в школе!"),
        ("OK, see you later.", "Окей, увидимся позже."),
    ),
    "how are you": (
        ("Hi! How are you today?", "Привет! Как дела сегодня?"),
        ("How are you after the trip?", "Как ты после поездки?"),
    ),
    "nice to meet you": (
        ("Nice to meet you! I'm Rico.", "Приятно познакомиться! Я Рико."),
        ("She smiled and said, \"Nice to meet you.\"", "Она улыбнулась и сказала: «Приятно познакомиться.»"),
    ),
    "excuse me": (
        ("Excuse me, where is the station?", "Извините, где станция?"),
        ("Excuse me, can I pass?", "Извините, можно пройти?"),
    ),
    "thank you": (
        ("Thank you for your help!", "Спасибо за помощь!"),
        ("Thank you so much!", "Большое спасибо!"),
    ),
    "a walk": (
        ("Let's go for a walk after dinner.", "Давай прогуляемся после ужина."),
        ("I need a walk to clear my head.", "Мне нужна прогулка, чтобы проветрить голову."),
    ),
    "big number": (
        ("One million is a big number.", "Миллион — это большое число."),
        ("Don't worry about the big number on the bill.", "Не переживай из-за большой суммы в счёте."),
    ),
    "free time": (
        ("I read books in my free time.", "В свободное время я читаю книги."),
        ("What do you do in your free time?", "Что ты делаешь в свободное время?"),
    ),
}

PHRASE_OVERRIDES: dict[str, tuple[tuple[str, str], tuple[str, str]]] = {
    "on time": (
        ("The train arrived on time.", "Поезд прибыл вовремя."),
        ("Please be on time for the meeting.", "Пожалуйста, приходи вовремя на встречу."),
    ),
    "you're welcome": (
        ("\"Thank you!\" — \"You're welcome.\"", "«Спасибо!» — «Пожалуйста.»"),
        ("You're welcome — happy to help.", "Пожалуйста — рад(а) помочь."),
    ),
    "see you later": (
        ("OK, see you later!", "Окей, увидимся позже!"),
        ("She waved and said, \"See you later.\"", "Она помахала и сказала: «Увидимся позже.»"),
    ),
    "take care": (
        ("Take care on your way home.", "Береги себя по дороге домой."),
        ("Bye! Take care!", "Пока! Береги себя!"),
    ),
    "out of order": (
        ("Sorry, the lift is out of order.", "Извините, лифт не работает."),
        ("This machine is out of order again.", "Этот аппарат снова не работает."),
    ),
    "out of stock": (
        ("Sorry, this size is out of stock.", "Извините, этого размера нет в наличии."),
        ("The book is out of stock online.", "Книги нет в наличии в онлайн-магазине."),
    ),
    "split the bill": (
        ("Shall we split the bill?", "Давай разделим счёт?"),
        ("We usually split the bill after dinner.", "Мы обычно делим счёт после ужина."),
    ),
    "work out": (
        ("I work out three times a week.", "Я тренируюсь три раза в неделю."),
        ("Do you work out in the morning?", "Ты тренируешься по утрам?"),
    ),
    "run out of": (
        ("We've run out of milk.", "У нас закончилось молоко."),
        ("Don't run out of patience.", "Не теряй терпение."),
    ),
}


def _article(word: str) -> str:
    w = (word or "").strip()
    if not w:
        return "a "
    return "an " if w[0].lower() in "aeiou" else "a "


_ADJECTIVES = {
    "good", "bad", "big", "small", "old", "young", "happy", "sad", "nice", "fine",
    "cold", "hot", "warm", "cool", "busy", "tired", "hungry", "thirsty", "angry",
    "bored", "boring", "interesting", "fun", "funny", "easy", "hard", "difficult",
    "cheap", "expensive", "affordable", "clean", "dirty", "fast", "slow", "strong",
    "weak", "tall", "short", "long", "new", "ready", "late", "early", "free",
    "important", "useful", "beautiful", "ugly", "quiet", "loud", "soft",
    "bitter", "sweet", "salty", "spicy", "fresh", "healthy", "sick", "ill",
    "allergic", "nervous", "calm", "kind", "friendly", "polite", "rude", "honest",
    "close", "open", "full", "empty", "safe", "dangerous", "famous", "popular",
    "modern", "traditional", "local", "foreign", "private", "public",
}

_FEEL_ADJ = {
    "happy", "sad", "fine", "good", "bad", "tired", "hungry", "thirsty", "angry",
    "bored", "nervous", "calm", "sick", "ill", "cold", "hot", "warm", "cool",
    "busy", "ready", "free", "strong", "weak",
}

_PRICE_ADJ = {"cheap", "expensive", "affordable"}

_GREET = {
    "hello", "hi", "goodbye", "bye", "please", "thank you", "thanks", "sorry",
    "yes", "no", "welcome", "ok", "okay", "excuse me", "see you", "how are you",
    "nice to meet you", "good morning", "good afternoon", "good evening",
    "good night", "cheers",
}


def _kind(en: str) -> tuple[str, str]:
    w = (en or "").strip()
    low = w.lower()
    if low in _GREET or low.startswith(
        ("good ", "nice to ", "how are ", "excuse ", "see you", "thank ")
    ):
        return w, "greet"
    if low.startswith("to ") and len(w) > 3:
        base = w[3:].strip()
        if base:
            return base, "verb"
    if " " in w:
        return w, "multi"
    if low in _ADJECTIVES or any(
        low.endswith(s) for s in ("ful", "less", "ous", "ive", "able", "ible", "ish")
    ):
        return w, "adj"
    return w, "noun"


def _word_pair(en: str, ru: str) -> tuple[tuple[str, str], tuple[str, str]]:
    key = en.strip().lower()
    if key in WORD_OVERRIDES:
        return WORD_OVERRIDES[key]
    if en.strip() in WORD_OVERRIDES:
        return WORD_OVERRIDES[en.strip()]

    form, kind = _kind(en)
    r = (ru or "").strip() or form
    a = _article(form)

    if kind == "greet":
        shown = en.strip()
        shown_cap = shown[:1].upper() + shown[1:] if shown else shown
        return (
            (f'She smiled and said, "{shown_cap}."', f"Она улыбнулась и сказала: «{r}.»"),
            (f'He waved and answered, "{shown_cap}!"', f"Он помахал и ответил: «{r}!»"),
        )
    if kind == "verb":
        return (
            (f"I {form} every morning before work.", f"Я каждое утро {r} перед работой."),
            (f"Do you want to {form} with me tomorrow?", f"Хочешь {r} со мной завтра?"),
        )
    if kind == "adj":
        low = form.lower()
        if low in _PRICE_ADJ:
            return (
                (f"This phone is {form}.", f"Этот телефон {r}."),
                (f"We need something more {form}.", f"Нам нужно что-то более {r}."),
            )
        if low in _FEEL_ADJ:
            return (
                (f"Today I feel really {form}.", f"Сегодня я чувствую себя очень {r}."),
                (f"She looks {form} this morning.", f"Сегодня утром она выглядит {r}."),
            )
        return (
            (f"This place looks {form}.", f"Это место выглядит {r}."),
            (f"It was a {form} day.", f"Это был {r} день."),
        )
    if kind == "multi":
        # короткие устойчивые словосочетания — как целую фразу в речи
        return (
            (f"People often say \"{form}\" in daily life.", f"В повседневной жизни часто говорят «{r}»."),
            (f"I learned the phrase \"{form}\" yesterday.", f"Вчера я выучил(а) выражение «{r}»."),
        )
    # noun — избегаем «I saw an abroad»
    # неисчисляемые / абстрактные по эвристике
    massish = {
        "milk", "water", "coffee", "tea", "bread", "cheese", "money", "cash",
        "music", "news", "advice", "fun", "love", "help", "work", "homework",
        "traffic", "weather", "information", "furniture", "luggage", "blood",
        "hair", "rice", "pasta", "butter", "sugar", "salt", "pepper", "juice",
        "soup", "salad", "meat", "fish", "chicken", "fruit", "food", "time",
        "space", "energy", "health", "luck", "progress", "research", "evidence",
        "equipment", "software", "homework", "knowledge", "education",
    }
    if form.lower() in massish:
        return (
            (f"I need more {form}.", f"Мне нужно больше: {r}."),
            (f"There isn't enough {form} here.", f"Здесь недостаточно ({r})."),
        )
    return (
        (f"There is {a}{form} on the table.", f"На столе есть {r}."),
        (f"I bought {a}{form} yesterday.", f"Я вчера купил(а) {r}."),
    )


def _phrase_pair(en: str, ru: str) -> tuple[tuple[str, str], tuple[str, str]]:
    key = en.strip().lower()
    if key in PHRASE_OVERRIDES:
        return PHRASE_OVERRIDES[key]
    p = en.strip()
    r = (ru or "").strip() or p
    # Императив / вопрос / утверждение
    if p.endswith("?"):
        return (
            (f'He asked, "{p}"', f"Он спросил: «{r}»"),
            (f'At the door she asked me, "{p}"', f"У двери она спросила меня: «{r}»"),
        )
    if re.match(
        r"^(open|close|turn|sit|take|pay|see|pass|pick|set|try|split|stay|work|shop|rent)\b",
        p,
        re.I,
    ):
        return (
            (f"Remember to {p.lower()}.", f"Не забудь: {r}."),
            (f"She told me to {p.lower()}.", f"Она сказала мне {r}."),
        )
    # идиомы / словосочетания — встроить в предложение
    return (
        (f"In this situation people often say: \"{p}\".", f"В такой ситуации часто говорят: «{r}»."),
        (f"I heard someone say \"{p}\" on the phone.", f"Я слышал(а), как кто-то сказал «{r}» по телефону."),
    )


# Улучшенные топик-специфичные паттерны для существительных/глаголов
TOPIC_NOUN = {
    "family": (
        lambda w, a, r: (f"My {w} lives near me.", f"Мой/моя {r} живёт рядом со мной."),
        lambda w, a, r: (f"I called my {w} yesterday.", f"Я вчера позвонил(а) своему {r}."),
    ),
    "food": (
        lambda w, a, r: (f"I like {a}{w} for breakfast.", f"Мне нравится {r} на завтрак."),
        lambda w, a, r: (f"Would you like {a}{w}?", f"Хочешь {r}?"),
    ),
    "home": (
        lambda w, a, r: (f"Our {w} is upstairs.", f"Наш(а) {r} наверху."),
        lambda w, a, r: (f"Please clean the {w}.", f"Пожалуйста, убери {r}."),
    ),
    "colors": (
        lambda w, a, r: (f"I like the color {w}.", f"Мне нравится цвет «{r}»."),
        lambda w, a, r: (f"Her bag is {w}.", f"Её сумка {r}."),
    ),
    "travel": (
        lambda w, a, r: (f"We saw {a}{w} at the airport.", f"Мы увидели {r} в аэропорту."),
        lambda w, a, r: (f"Is there {a}{w} nearby?", f"Рядом есть {r}?"),
    ),
    "health": (
        lambda w, a, r: (f"The doctor talked about {w}.", f"Врач говорил(а) про {r}."),
        lambda w, a, r: (f"I had {a}{w} last week.", f"На прошлой неделе у меня был(а) {r}."),
    ),
    "work": (
        lambda w, a, r: (f"My {w} starts at nine.", f"Мой/моя {r} начинается в девять."),
        lambda w, a, r: (f"She met her {w} at the office.", f"Она встретила своего {r} в офисе."),
    ),
    "shopping": (
        lambda w, a, r: (f"I paid the {w} by card.", f"Я оплатил(а) {r} картой."),
        lambda w, a, r: (f"Where is the {w}?", f"Где {r}?"),
    ),
}


def _word_pair_with_topic(en: str, ru: str, topic_id: str) -> tuple[tuple[str, str], tuple[str, str]]:
    key = en.strip().lower()
    if key in WORD_OVERRIDES or en.strip() in WORD_OVERRIDES:
        return _word_pair(en, ru)
    form, kind = _kind(en)
    if kind != "noun":
        return _word_pair(en, ru)
    # match topic family
    for tip, makers in TOPIC_NOUN.items():
        if tip in (topic_id or "").lower():
            a = _article(form)
            r = (ru or "").strip() or form
            return makers[0](form, a, r), makers[1](form, a, r)
    return _word_pair(en, ru)


def _phrase_pair_better(en: str, ru: str) -> tuple[tuple[str, str], tuple[str, str]]:
    key = en.strip().lower()
    if key in PHRASE_OVERRIDES:
        return PHRASE_OVERRIDES[key]
    p = en.strip()
    r = (ru or "").strip() or p
    low = p.lower()

    # устойчивые шаблоны по типу фразы
    if " " in p and not p.endswith("?"):
        # попытаться встроить как обстоятельство / дополнение
        if low.startswith(("on ", "in ", "at ", "by ", "for ", "with ", "out of ", "once ")):
            return (
                (f"We usually meet {low}.", f"Мы обычно встречаемся ({r})."),
                (f"Is it OK if we do it {low}?", f"Нормально, если сделаем это ({r})?"),
            )
        if low.startswith(("take ", "make ", "get ", "have ", "pay ", "pass ", "pick ", "set ", "work ", "stay ", "split ", "turn ", "open ", "sit ", "see ", "rent ", "try ", "shop ", "run ")):
            return (
                (f"Don't forget to {low}.", f"Не забудь {r}."),
                (f"She decided to {low}.", f"Она решила {r}."),
            )
        if low.startswith(("too ", "the ", "this ", "we ", "she ", "he ", "i ", "you ")):
            return (
                (f"{p[0].upper()}{p[1:] if len(p)>1 else ''}.", f"{r[0].upper()}{r[1:] if len(r)>1 else ''}." if r else r),
                (f"My friend said: \"{p}.\"", f"Мой друг сказал: «{r}.»"),
            )
    return _phrase_pair(en, ru)


def _py_str(s: str) -> str:
    return repr(s)


def main() -> None:
    words: dict[str, tuple[tuple[str, str], tuple[str, str]]] = {}
    phrases: dict[str, tuple[tuple[str, str], tuple[str, str]]] = {}

    for _lv, topics in WORDS.items():
        for tid, items in topics.items():
            for it in items:
                en = (it.get("en") or "").strip()
                ru = (it.get("ru") or "").strip()
                if not en:
                    continue
                key = en.lower()
                if key not in words:
                    words[key] = _word_pair_with_topic(en, ru, tid)

    for _lv, topics in PHRASES.items():
        for _tid, items in topics.items():
            for it in items:
                en = (it.get("en") or "").strip()
                ru = (it.get("ru") or "").strip()
                if not en:
                    continue
                key = en.lower()
                if key not in phrases:
                    phrases[key] = _phrase_pair_better(en, ru)

    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Готовые EN/RU примеры для Vocabulary и повторения (2 на слово/фразу).',
        "",
        "Сгенерировано: python scripts/gen_vocab_example_bank.py",
        'Карточки и «не помню» берут оба примера из этой базы."""',
        "",
        "from __future__ import annotations",
        "",
        "# key = lower(en) -> ((ex1_en, ex1_ru), (ex2_en, ex2_ru))",
        "WORD_EXAMPLES: dict[str, tuple[tuple[str, str], tuple[str, str]]] = {",
    ]
    for k in sorted(words):
        (e1, r1), (e2, r2) = words[k]
        lines.append(
            f"    {_py_str(k)}: (("
            f"{_py_str(e1)}, {_py_str(r1)}), ("
            f"{_py_str(e2)}, {_py_str(r2)})),"
        )
    lines.append("}")
    lines.append("")
    lines.append("PHRASE_EXAMPLES: dict[str, tuple[tuple[str, str], tuple[str, str]]] = {")
    for k in sorted(phrases):
        (e1, r1), (e2, r2) = phrases[k]
        lines.append(
            f"    {_py_str(k)}: (("
            f"{_py_str(e1)}, {_py_str(r1)}), ("
            f"{_py_str(e2)}, {_py_str(r2)})),"
        )
    lines.append("}")
    lines.append(
        """

def lookup_word_examples(en: str, ru: str = "") -> tuple[tuple[str, str], tuple[str, str]] | None:
    key = (en or "").strip().lower()
    if key in WORD_EXAMPLES:
        return WORD_EXAMPLES[key]
    return None


def lookup_phrase_examples(en: str, ru: str = "") -> tuple[tuple[str, str], tuple[str, str]] | None:
    key = (en or "").strip().lower()
    if key in PHRASE_EXAMPLES:
        return PHRASE_EXAMPLES[key]
    return None


def lookup_word_example(en: str, ru: str = "") -> tuple[str, str] | None:
    \"\"\"Первый пример (для совместимости / повторения).\"\"\"
    both = lookup_word_examples(en, ru)
    return both[0] if both else None


def lookup_phrase_example(en: str, ru: str = "") -> tuple[str, str] | None:
    both = lookup_phrase_examples(en, ru)
    return both[0] if both else None
"""
    )
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} words={len(words)} phrases={len(phrases)}")


if __name__ == "__main__":
    main()
