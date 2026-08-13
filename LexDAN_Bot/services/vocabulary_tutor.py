"""
Рико: тексты Vocabulary, карточки слов/фраз, проверка предложений.
"""

import logging
import random
import re

from services.gpt import _ask_json


def highlight_target_terms(text: str, terms: list[str]) -> str:
    """
    Выделить целевые слова/фразы жирным <b>…</b> в тексте.
    Снимает старые <i>/<b>, затем оборачивает термины (длинные первыми).
    """
    out = re.sub(r"</?(?:b|i|strong|em)>", "", text or "", flags=re.IGNORECASE)
    cleaned: list[str] = []
    seen: set[str] = set()
    for t in terms or []:
        s = (t or "").strip()
        if not s:
            continue
        key = s.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(s)
    cleaned.sort(key=len, reverse=True)
    for term in cleaned:
        if " " in term or "-" in term:
            pat = re.compile(re.escape(term), re.IGNORECASE)
        else:
            pat = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)

        def _repl(m: re.Match, _term=term) -> str:
            return f"<b>{m.group(0)}</b>"

        out = pat.sub(_repl, out)
    # убрать случайное двойное выделение
    out = re.sub(r"<b>\s*<b>(.*?)</b>\s*</b>", r"<b>\1</b>", out, flags=re.IGNORECASE | re.DOTALL)
    return out


def generate_vocab_text(
    level: str,
    topic_title: str,
    words: list[dict],
    *,
    kind: str = "words",
) -> dict:
    """
    kind=words: 6-7 предложений, целевые слова жирным
    kind=phrases: до 5 предложений, 2 фразы жирным
    """
    if kind == "phrases":
        labels = [p["en"] for p in words[:2]]
        count = 2
        fallback_en = (
            f"My family is very important to me. We often say <b>{labels[0] if labels else 'family first'}</b> "
            f"when we talk. Last weekend we had dinner together. "
            f"My grandmother told us <b>{labels[1] if len(labels) > 1 else 'home sweet home'}</b> "
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
            f"I see my <b>{labels[0] if labels else 'friend'}</b> every day. "
            f"We like to <b>{labels[1] if len(labels) > 1 else 'talk'}</b> together. "
            f"Sometimes we visit a <b>{labels[2] if len(labels) > 2 else 'place'}</b> nearby. "
            f"It makes me feel <b>{labels[3] if len(labels) > 3 else 'happy'}</b>. "
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
            "Max 5 sentences. Wrap EXACTLY 2 given phrases in <b>...</b> in the English text. "
            "highlighted = list of 2 English phrases without tags."
        )
    else:
        system += (
            "6-7 sentences. Wrap EVERY given target word in <b>...</b> in the English text "
            "(bold HTML, not italic). "
            "highlighted = list of English words used (without tags)."
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
    highlighted = [str(x) for x in highlighted[:count]] or labels[:count]
    # гарантируем жирное выделение целевых слов из батча
    text_en = highlight_target_terms((data.get("text_en") or fallback_en).strip(), labels[:count])
    return {
        "text_en": text_en,
        "text_ru": (data.get("text_ru") or fallback_ru).strip(),
        "highlighted": highlighted,
    }


_COMMON_ADJECTIVES = frozenset(
    {
        "happy", "sad", "angry", "tired", "hungry", "thirsty", "cold", "hot",
        "warm", "cool", "big", "small", "large", "little", "long", "short",
        "tall", "new", "old", "young", "good", "bad", "nice", "kind", "funny",
        "beautiful", "ugly", "easy", "hard", "difficult", "important", "busy",
        "free", "ready", "late", "early", "fast", "slow", "strong", "weak",
        "rich", "poor", "clean", "dirty", "quiet", "loud", "bright", "dark",
        "soft", "hard", "sweet", "salty", "fresh", "empty", "full", "open",
        "closed", "afraid", "scared", "bored", "excited", "nervous", "calm",
        "friendly", "polite", "rude", "lucky", "useful", "useless", "interesting",
        "boring", "expensive", "cheap", "safe", "dangerous", "healthy", "sick",
        "ill", "right", "wrong", "true", "false", "possible", "necessary",
    }
)


def _article(word: str) -> str:
    w = (word or "").strip()
    if not w:
        return "a "
    return "an " if w[0].lower() in "aeiou" else "a "


def _word_example_kind(en: str) -> tuple[str, str]:
    """Return (form_to_use_in_sentence, kind) where kind is verb|multi|adj|noun."""
    w = (en or "word").strip()
    low = w.lower()
    if low.startswith("to ") and len(w) > 3:
        base = w[3:].strip()
        if base:
            return base, "verb"
    if " " in w:
        return w, "multi"
    if low in _COMMON_ADJECTIVES or (
        len(low) > 4
        and any(low.endswith(s) for s in ("ful", "less", "ous", "ive", "able", "ible", "ish"))
    ):
        return w, "adj"
    return w, "noun"


def _diverse_word_examples(en: str, ru: str) -> tuple[str, str, str, str]:
    """Локальные примеры: слово USE в реальной ситуации (не мета про изучение)."""
    raw = (en or "word").strip()
    w, kind = _word_example_kind(raw)
    r = (ru or "").strip() or raw
    a = _article(w)

    if kind == "verb":
        templates = [
            (
                f"I {w} in the park every morning.",
                f"Я каждое утро занимаюсь этим ({r}) в парке.",
                f"Do you want to {w} with me after work?",
                f"Хочешь {r} со мной после работы?",
            ),
            (
                f"She can {w} really well.",
                f"Она умеет отлично {r}.",
                f"Let's {w} together this weekend.",
                f"Давай {r} вместе в эти выходные.",
            ),
            (
                f"I need to {w} before it gets dark.",
                f"Мне нужно {r}, пока не стало темно.",
                f"He likes to {w} when he has free time.",
                f"Ему нравится {r}, когда есть свободное время.",
            ),
            (
                f"Please {w} carefully.",
                f"Пожалуйста, {r} осторожно.",
                f"We usually {w} after dinner.",
                f"Мы обычно делаем это ({r}) после ужина.",
            ),
            (
                f"I forgot to {w} yesterday.",
                f"Я вчера забыл(а) {r}.",
                f"They {w} every day at school.",
                f"Они каждый день делают это ({r}) в школе.",
            ),
            (
                f"Can you {w} a little slower?",
                f"Можешь {r} чуть медленнее?",
                f"My brother wants to {w} too.",
                f"Мой брат тоже хочет {r}.",
            ),
        ]
    elif kind == "multi":
        templates = [
            (
                f"\"{w},\" she said with a smile.",
                f"«{r},» — сказала она с улыбкой.",
                f"He waved and answered, \"{w}.\"",
                f"Он помахал и ответил: «{r}.»",
            ),
            (
                f"He replied, \"{w}!\" and waved goodbye.",
                f"Он ответил: «{r}!» — и помахал на прощание.",
                f"At the door I smiled and said \"{w}.\"",
                f"У двери я улыбнулся(ась) и сказал(а) «{r}.»",
            ),
            (
                f"When someone helps you, just say \"{w}\".",
                f"Когда тебе помогают, просто скажи «{r}».",
                f"I heard her whisper \"{w}\" on the phone.",
                f"Я слышал(а), как она прошептала «{r}» по телефону.",
            ),
            (
                f"\"{w}\" — that was the first thing he said.",
                f"«{r}» — это было первое, что он сказал.",
                f"We both said \"{w}\" at the same time.",
                f"Мы оба сказали «{r}» одновременно.",
            ),
            (
                f"At the door she smiled and said \"{w}\".",
                f"У двери она улыбнулась и сказала «{r}».",
                f"After the meeting everyone said \"{w}.\"",
                f"После встречи все сказали «{r}.»",
            ),
        ]
    elif kind == "adj":
        templates = [
            (
                f"She looks {w} today.",
                f"Она сегодня выглядит {r}.",
                f"I feel {w} after a long walk.",
                f"Я чувствую себя {r} после долгой прогулки.",
            ),
            (
                f"Why do you look so {w}?",
                f"Почему ты выглядишь таким {r}?",
                f"The weather was {w} all weekend.",
                f"Погода весь уикенд была {r}.",
            ),
            (
                f"Everyone felt {w} after the good news.",
                f"Все почувствовали себя {r} после хороших новостей.",
                f"This room looks very {w}.",
                f"Эта комната выглядит очень {r}.",
            ),
            (
                f"I'm a bit {w} right now.",
                f"Я сейчас немного {r}.",
                f"He always stays {w}, even under pressure.",
                f"Он всегда остаётся {r}, даже под давлением.",
            ),
            (
                f"That was a really {w} day.",
                f"Это был очень {r} день.",
                f"You sound {w} — is everything okay?",
                f"Ты звучишь {r} — всё в порядке?",
            ),
            (
                f"The cake smells {w}.",
                f"Торт пахнет {r}.",
                f"She became {w} when she saw the gift.",
                f"Она стала {r}, когда увидела подарок.",
            ),
        ]
    else:  # noun
        people = {
            "brother", "sister", "mother", "father", "mum", "dad", "friend",
            "teacher", "doctor", "nurse", "child", "baby", "boy", "girl",
            "man", "woman", "uncle", "aunt", "cousin", "neighbour", "neighbor",
            "classmate", "partner", "boss", "student",
            "dependant", "dependent", "guardian", "orphan", "breadwinner",
            "host", "guest", "colleague", "coworker", "client", "customer",
            "patient", "passenger", "stranger", "roommate", "flatmate",
            "landlord", "tenant", "relative", "spouse", "husband", "wife",
            "son", "daughter", "parent", "parents", "kid", "kids", "adult",
            "teenager", "chef", "waiter", "waitress", "pilot", "driver",
            "engineer", "lawyer", "manager", "tourist", "visitor", "owner",
            "member", "leader", "family",
        }
        abstracts = {
            "kinship", "upbringing", "inheritance", "custody", "freedom",
            "happiness", "sadness", "anger", "love", "fear", "hope", "advice",
            "knowledge", "patience", "courage", "honesty", "loyalty", "respect",
            "trust", "privacy", "responsibility", "independence", "poverty",
            "wealth", "success", "failure", "education", "career", "marriage",
            "friendship", "relationship", "habit", "tradition", "culture",
            "society", "justice", "opportunity",
        }
        low = w.lower()
        if low in people:
            templates = [
                (
                    f"My {w} called me after school.",
                    f"Мой {r} позвонил(а) мне после школы.",
                    f"I went to the park with my {w}.",
                    f"Я пошёл(шла) в парк со своим {r}.",
                ),
                (
                    f"Her {w} is very kind.",
                    f"Её {r} очень добрый.",
                    f"I met his {w} at the party.",
                    f"Я встретил(а) его {r} на вечеринке.",
                ),
                (
                    f"My {w} lives near the station.",
                    f"Мой {r} живёт рядом со станцией.",
                    f"Can your {w} help us tomorrow?",
                    f"Твой {r} может помочь нам завтра?",
                ),
                (
                    f"I talked to my {w} yesterday.",
                    f"Я вчера говорил(а) со своим {r}.",
                    f"She visits her {w} every Sunday.",
                    f"Она навещает своего {r} каждое воскресенье.",
                ),
                (
                    f"He still lives as {a}{w} of his parents.",
                    f"Он всё ещё живёт как {r} своих родителей.",
                    f"Being {a}{w} is hard when you want freedom.",
                    f"Быть {r} трудно, когда хочешь свободы.",
                ),
            ]
        elif low in abstracts or any(
            low.endswith(s)
            for s in ("ness", "ment", "tion", "sion", "ship", "hood", "dom", "ance", "ence")
        ):
            templates = [
                (
                    f"{w.capitalize()} is important in every family.",
                    f"{r.capitalize()} важно в каждой семье.",
                    f"We talked about {w} for a long time.",
                    f"Мы долго говорили про {r}.",
                ),
                (
                    f"He learned the value of {w} the hard way.",
                    f"Он на горьком опыте понял ценность ({r}).",
                    f"Without {w}, life feels empty.",
                    f"Без {r} жизнь кажется пустой.",
                ),
                (
                    f"Her story is about {w} and growing up.",
                    f"Её история — про {r} и взросление.",
                    f"I need more {w} in my daily life.",
                    f"Мне нужно больше {r} в повседневной жизни.",
                ),
                (
                    f"They discussed {w} in class today.",
                    f"Сегодня на уроке они обсуждали {r}.",
                    f"True {w} takes time and honesty.",
                    f"Настоящий/настоящая {r} требует времени и честности.",
                ),
            ]
        else:
            templates = [
                (
                    f"I need {a}{w} for the trip.",
                    f"Мне нужен {r} для поездки.",
                    f"I left my {w} on the bus.",
                    f"Я оставил(а) свой {r} в автобусе.",
                ),
                (
                    f"Do you have {a}{w} I can borrow?",
                    f"Есть у тебя {r}, который можно одолжить?",
                    f"I bought {a}{w} yesterday.",
                    f"Я вчера купил(а) {r}.",
                ),
                (
                    f"Where did you put the {w}?",
                    f"Куда ты положил(а) {r}?",
                    f"This {w} belongs to my friend.",
                    f"Этот {r} принадлежит моему другу.",
                ),
                (
                    f"There's {a}{w} on the table.",
                    f"На столе лежит {r}.",
                    f"Can you pass me the {w}, please?",
                    f"Передай мне, пожалуйста, {r}.",
                ),
                (
                    f"She gave me her {w} for a moment.",
                    f"Она на минуту дала мне свой {r}.",
                    f"Is this your {w}?",
                    f"Это твой {r}?",
                ),
                (
                    f"I saw your {w} near the door.",
                    f"Я видел(а) твой {r} у двери.",
                    f"Don't forget the {w} tomorrow.",
                    f"Не забудь {r} завтра.",
                ),
                (
                    f"We need {a}{w} before we leave.",
                    f"Нам нужен {r}, прежде чем уйдём.",
                    f"He always takes his {w} with him.",
                    f"Он всегда берёт с собой свой {r}.",
                ),
                (
                    f"I found {a}{w} under the chair.",
                    f"Я нашёл(нашла) {r} под стулом.",
                    f"Put the {w} back on the shelf.",
                    f"Положи {r} обратно на полку.",
                ),
            ]

    idx = sum(ord(c) for c in raw.lower()) % len(templates)
    return templates[idx]


def _example_is_bland(text: str, target: str) -> bool:
    """True if example talks ABOUT the word instead of using it naturally."""
    t = (text or "").lower()
    w = (target or "").strip().lower()
    if not t:
        return True
    checks = [
        "today i learned",
        "i know the word",
        "i learned the word",
        "make a sentence with",
        "can't imagine my day without",
        "cannot imagine my day without",
        "people often say",
        "native speakers use",
        "i'd probably say",
        "i would probably say",
    ]
    if any(c in t for c in checks):
        return True
    if w:
        meta_bits = [
            f"practise {w} out loud",
            f"practice {w} out loud",
            f"what {w} means",
            f"looked up {w}",
            f"look up {w}",
            f"using {w} correctly",
            f"mentioned {w} twice",
            f"talked about {w}",
            f"talk about {w}",
        ]
        if any(m in t for m in meta_bits):
            return True
    return False


def _example_is_nonsensical(text: str, target: str) -> bool:
    """Предметные шаблоны для людей/абстракций (dependant on the table и т.п.)."""
    t = (text or "").lower()
    w = (target or "").strip().lower()
    if not t or not w or w not in t:
        return False
    people_ish = {
        "dependant", "dependent", "guardian", "orphan", "breadwinner",
        "colleague", "coworker", "client", "customer", "patient", "passenger",
        "stranger", "roommate", "landlord", "tenant", "relative", "spouse",
        "husband", "wife", "son", "daughter", "parent", "teacher", "doctor",
        "friend", "brother", "sister", "mother", "father", "boss", "student",
    }
    abstract_ish = w.endswith(
        ("ness", "ment", "tion", "sion", "ship", "hood", "dom", "ance", "ence")
    ) or w in {
        "kinship", "upbringing", "inheritance", "custody", "freedom", "advice",
        "knowledge", "patience", "courage", "honesty", "loyalty", "respect",
        "trust", "privacy", "responsibility", "independence",
    }
    object_patterns = (
        "on the table",
        "on the bus",
        "under the chair",
        "on the shelf",
        "pass me the",
        "left my ",
        "borrow",
        "bought a ",
        "bought an ",
        "put the ",
        "belongs to my friend",
    )
    if (w in people_ish or abstract_ish) and any(p in t for p in object_patterns):
        return True
    return False


def _format_word_card(word: dict, data: dict) -> str:
    en = word["en"]
    ru = word["ru"]
    emoji = word.get("emoji") or "📘"
    meaning = (data.get("meaning_ru") or f"Это значит «{ru}».").strip()
    assoc = (data.get("association_ru") or "").strip()
    e1d, e1rd, e2d, e2rd = _diverse_word_examples(en, ru)
    e1 = (data.get("example1_en") or e1d).strip()
    e1r = (data.get("example1_ru") or e1rd).strip()
    e2 = (data.get("example2_en") or e2d).strip()
    e2r = (data.get("example2_ru") or e2rd).strip()
    # если GPT/старый фолбэк выдал мета-шаблон или бессмыслицу для роли/абстракции — подменим
    bland = (
        _example_is_bland(e1, en)
        or _example_is_bland(e2, en)
        or e1.lower() == e2.lower()
        or _example_is_nonsensical(e1, en)
        or _example_is_nonsensical(e2, en)
    )
    if bland:
        e1, e1r, e2, e2r = e1d, e1rd, e2d, e2rd

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
    e1, e1r, e2, e2r = _diverse_word_examples(en, ru)
    fallback = {
        "meaning_ru": f"Слово «{en}» значит «{ru}».",
        "association_ru": f"Представь картинку с эмодзи {emoji} — и сразу вспоминается «{ru}».",
        "example1_en": e1,
        "example1_ru": e1r,
        "example2_en": e2,
        "example2_ru": e2r,
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
                        '"example1_en":"живое предложение со словом (не шаблон)",'
                        '"example1_ru":"перевод примера 1 на русский",'
                        '"example2_en":"ДРУГОЕ живое предложение со словом",'
                        '"example2_ru":"перевод примера 2 на русский"'
                        "}\n"
                        "FORBIDDEN templates: 'Today I learned …', 'I know the word …', "
                        "'I can't imagine my day without …', 'Could you explain what … means', "
                        "'Don't forget to practise …', 'I looked up …', 'make a sentence with …', "
                        "'using … correctly', 'mentioned … twice', 'talked about …', "
                        "'This is my …', 'I use … every day' as the only pattern. "
                        "Examples must USE the word as vocabulary in a real-life situation, "
                        "not talk about learning the word. "
                        "CRITICAL: if the word means a PERSON/ROLE (dependant, teacher, guardian…) "
                        "or an ABSTRACT idea (freedom, kinship…), do NOT treat it like an object "
                        "(never 'on the table', 'on the bus', 'pass me the …'). "
                        "Make two DIFFERENT natural sentences that contain the word. "
                        f"Эмодзи для ассоциации: {emoji}. Уровень CEFR: {level}."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Тема: {topic_title}. Слово: {en} = {ru}. Seed {random.random()}",
                },
            ],
            fallback,
            temperature=0.75,
            max_tokens=380,
        )
        return _format_word_card(word, data if isinstance(data, dict) else fallback)
    except Exception as e:
        logging.error(f"rico_word_card: {e}")
        return _format_word_card(word, fallback)


def _diverse_phrase_examples(en: str, ru: str) -> tuple[str, str, str, str]:
    """Фраза в живом диалоге/контексте — не мета «People often say…»."""
    p = (en or "phrase").strip()
    r = (ru or "").strip() or p
    templates = [
        (
            f"\"{p},\" she said and waved.",
            f"«{r},» — сказала она и помахала.",
            f"He smiled and answered, \"{p}.\"",
            f"Он улыбнулся и ответил: «{r}.»",
        ),
        (
            f"Before leaving, my friend called out, \"{p}!\"",
            f"Перед уходом подруга крикнула: «{r}!»",
            f"At the door I just said \"{p}\" and left.",
            f"У двери я просто сказал(а) «{r}» и ушёл/ушла.",
        ),
        (
            f"When the call ended, she whispered \"{p}.\"",
            f"Когда звонок закончился, она прошептала «{r}.»",
            f"I texted him \"{p}\" and put my phone away.",
            f"Я написал(а) ему «{r}» и убрал(а) телефон.",
        ),
        (
            f"\"{p}\" — that's what I told my brother.",
            f"«{r}» — вот что я сказал(а) брату.",
            f"Everyone in the room answered together: \"{p}!\"",
            f"Все в комнате хором ответили: «{r}!»",
        ),
        (
            f"She opened the chat with \"{p}\" this morning.",
            f"Сегодня утром она начала переписку с «{r}».",
            f"After lunch he stood up and said \"{p}.\"",
            f"После обеда он встал и сказал «{r}.»",
        ),
        (
            f"I heard someone shout \"{p}\" from across the street.",
            f"Я услышал(а), как кто-то крикнул «{r}» с другой стороны улицы.",
            f"\"{p},\" my mum said as she hugged me.",
            f"«{r},» — сказала мама, обнимая меня.",
        ),
    ]
    idx = sum(ord(c) for c in p.lower()) % len(templates)
    return templates[idx]


def _format_phrase_card(phrase: dict, data: dict) -> str:
    en = phrase["en"]
    ru = phrase["ru"]
    emoji = phrase.get("emoji") or "💬"
    meaning = (data.get("meaning_ru") or f"Это значит «{ru}».").strip()
    when = (data.get("when_ru") or "").strip()
    assoc = (data.get("association_ru") or "").strip()
    e1d, e1rd, e2d, e2rd = _diverse_phrase_examples(en, ru)
    e1 = (data.get("example1_en") or e1d).strip()
    e1r = (data.get("example1_ru") or e1rd).strip()
    e2 = (data.get("example2_en") or e2d).strip()
    e2r = (data.get("example2_ru") or e2rd).strip()
    bland = (
        _example_is_bland(e1, en)
        or _example_is_bland(e2, en)
        or f"i say '{en}'".lower() in e1.lower()
        or f"everyone knows '{en}'".lower() in e2.lower()
        or e1.lower() == e2.lower()
    )
    if bland:
        e1, e1r, e2, e2r = e1d, e1rd, e2d, e2rd

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
    e1, e1r, e2, e2r = _diverse_phrase_examples(en, ru)
    fallback = {
        "meaning_ru": f"Фраза «{en}» значит «{ru}».",
        "when_ru": "Говорят в повседневных ситуациях по смыслу фразы.",
        "association_ru": f"Эмодзи {emoji} поможет вспомнить «{ru}».",
        "example1_en": e1,
        "example1_ru": e1r,
        "example2_en": e2,
        "example2_ru": e2r,
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
                        '"example1_en":"живое предложение с фразой",'
                        '"example1_ru":"...",'
                        '"example2_en":"другое живое предложение",'
                        '"example2_ru":"..."'
                        "}\n"
                        "FORBIDDEN: 'I say … to friends', 'Everyone knows …', "
                        "'People often say …', 'Native speakers use …', "
                        "'I'd probably say …', 'Try dropping … into your conversation'. "
                        "Examples must USE the phrase in a real-life dialogue or situation, "
                        "not talk about learning or explaining the phrase. "
                        "Two DIFFERENT natural examples that contain the phrase. "
                        f"Эмодзи: {emoji}. Уровень: {level}."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Тема: {topic_title}. Фраза: {en} = {ru}. Seed {random.random()}",
                },
            ],
            fallback,
            temperature=0.75,
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
    target = (target_en or "").strip()
    sentence = (user_sentence or "").strip()

    def _coerce_correct(val) -> bool:
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return bool(val)
        if isinstance(val, str):
            return val.strip().lower() in {"1", "true", "yes", "да", "ok", "верно"}
        return False

    import re

    tokens = re.findall(r"[a-zA-Z']+", sentence)
    # Одно слово / просто цель — это не предложение
    if len(tokens) < 3:
        return {
            "correct": False,
            "feedback_ru": (
                "Это не предложение. Напиши полное предложение на английском "
                f"(минимум 3 слова) с {kind} «{target}»."
            ),
            "better_en": "",
            "errors_ru": "Слишком коротко — нужна целая фраза.",
        }

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    f"You are Rico 🦜, a careful English tutor. Check the student's sentence.\n"
                    f"The sentence MUST use the target {kind} naturally and make LOGICAL sense.\n"
                    "Find grammar mistakes AND nonsense/logic problems "
                    "(wrong meaning, impossible situation, word salad).\n"
                    "Return ONLY JSON:\n"
                    "{"
                    '"correct":true/false,'
                    '"feedback_ru":"по-русски: что не так или краткая похвала",'
                    '"errors_ru":"по-русски коротко перечисли ошибки (или пусто если всё ок)",'
                    '"better_en":"исправленное естественное предложение С целевым словом/фразой"'
                    "}\n"
                    "correct=true ONLY if: target is used, grammar is basically ok for the level, "
                    "and the sentence is meaningful. "
                    "If student only stuffed the target with broken English → correct=false.\n"
                    "If wrong: always fill better_en with a natural corrected sentence."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {level}. Target {kind}: «{target}»\n"
                    f"Student sentence: {sentence}"
                ),
            },
        ],
        {
            "correct": False,
            "feedback_ru": f"Исправь предложение и обязательно используй «{target}».",
            "errors_ru": "",
            "better_en": "",
        },
        temperature=0.1,
        max_tokens=320,
    )
    if not isinstance(data, dict):
        data = {
            "correct": False,
            "feedback_ru": "Попробуй ещё раз.",
            "errors_ru": "",
            "better_en": "",
        }

    ok = _coerce_correct(data.get("correct"))
    # Не засчитываем автоматически только из-за наличия слова — ошибки должны ловиться
    data["correct"] = ok
    data["feedback_ru"] = str(data.get("feedback_ru") or "").strip()
    data["errors_ru"] = str(data.get("errors_ru") or "").strip()
    data["better_en"] = "" if ok else str(data.get("better_en") or "").strip()
    return data


def rico_dont_remember(item: dict, *, is_phrase: bool = False) -> str:
    en = item["en"]
    ru = item["ru"]
    emoji = item.get("emoji") or "💡"
    kind = "фраза" if is_phrase else "слово"
    if is_phrase:
        ex_en, ex_ru, _, _ = _diverse_phrase_examples(en, ru)
    else:
        ex_en, ex_ru, _, _ = _diverse_word_examples(en, ru)
    return (
        f"🦜 {emoji} Не страшно! <b>{en}</b> — <i>{ru}</i>\n\n"
        f"Запомни: {kind} «{en}» = {ru}.\n"
        f"Пример: <b>{ex_en}</b>\n"
        f"<i>{ex_ru}</i>\n\n"
        "Дальше следующее задание 👇"
    )
