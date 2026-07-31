"""
🔥 Огонь дня — слово / фраза / голос / факт.
Каждую кнопку можно открыть 1 раз в сутки (МСК), контент кэшируется на день.
"""

from __future__ import annotations

import html
import random
from datetime import datetime, timedelta, timezone

MSK = timezone(timedelta(hours=3))

BTN_DAILY_FIRE = "🔥 Огонь дня"
BTN_DF_WORD = "📖 Слово дня"
BTN_DF_PHRASE = "💬 Фраза дня"
BTN_DF_VOICE = "🎙 Голос дня"
BTN_DF_FACT = "💡 Факт дня"
BTN_DF_BACK = "⬅️ К огню дня"

KINDS = ("word", "phrase", "voice", "fact")

KIND_BTN = {
    "word": BTN_DF_WORD,
    "phrase": BTN_DF_PHRASE,
    "voice": BTN_DF_VOICE,
    "fact": BTN_DF_FACT,
}

BTN_TO_KIND = {v: k for k, v in KIND_BTN.items()}


def _today() -> str:
    return datetime.now(MSK).date().isoformat()


def _esc(s: str) -> str:
    return html.escape((s or "").strip(), quote=False)


def spoiler(text: str) -> str:
    """Telegram blur: тап открывает перевод."""
    return f"<tg-spoiler>{_esc(text)}</tg-spoiler>"


def ensure_daily_fire(user: dict) -> dict:
    raw = user.get("daily_fire")
    if not isinstance(raw, dict):
        raw = {}
    if raw.get("date") != _today():
        raw = {
            "date": _today(),
            "opened": {k: False for k in KINDS},
            "cache": {},
        }
    else:
        raw.setdefault("opened", {})
        raw.setdefault("cache", {})
        for k in KINDS:
            raw["opened"].setdefault(k, False)
    user["daily_fire"] = raw
    return raw


def is_opened(user: dict, kind: str) -> bool:
    df = ensure_daily_fire(user)
    return bool((df.get("opened") or {}).get(kind))


def opened_count(user: dict) -> int:
    df = ensure_daily_fire(user)
    return sum(1 for k in KINDS if (df.get("opened") or {}).get(k))


def mark_opened(user: dict, kind: str) -> None:
    df = ensure_daily_fire(user)
    df.setdefault("opened", {})[kind] = True


def get_cached(user: dict, kind: str) -> dict | None:
    df = ensure_daily_fire(user)
    item = (df.get("cache") or {}).get(kind)
    return item if isinstance(item, dict) else None


def set_cached(user: dict, kind: str, payload: dict) -> None:
    df = ensure_daily_fire(user)
    df.setdefault("cache", {})[kind] = payload


def hub_intro(user: dict) -> str:
    ensure_daily_fire(user)
    n = opened_count(user)
    lines = [
        "🔥 <b>Огонь дня</b>\n",
        "Маленький ритуал на сегодня: четыре искры от Рико — "
        "не банальщина из учебника, а штуки, от которых язык оживает ✨\n",
        f"Открыто сегодня: <b>{n}</b>/4 · обновление в <b>00:00 МСК</b>\n",
        "📖 <b>Слово дня</b> — редкое/сочное слово, блюр-перевод, история и озвучка",
        "💬 <b>Фраза дня</b> — живой оборот с объяснением и голосом",
        "🎙 <b>Голос дня</b> — короткое голосовое + текст и перевод под блюром",
        "💡 <b>Факт дня</b> — неожиданный факт + голос Рико + блюр-перевод\n",
        "Каждую кнопку можно открыть <b>один раз за день</b> "
        "(потом можно переслушать то же самое).",
    ]
    return "\n".join(lines)


# ── Fallbacks (интересные, не «apple/hello») ──────────────────────────

_FALLBACK_WORDS = [
    {
        "item": "serendipity",
        "translation_ru": "счастливая случайность; находка, которую не искал",
        "explain_ru": (
            "Когда жизнь подкидывает удачу без плана. Слово родилось из персидской сказки "
            "про принцев Серендипа, которые находили то, что не искали."
        ),
        "origin_ru": "Из англ. Serendip (старое название Шри-Ланки) + суффикс -ity.",
        "sentence_en": "I found this café by pure serendipity — wrong turn, perfect coffee.",
        "sentence_ru": "Я нашёл это кафе чистой serendipity — не туда свернул, а кофе идеальный.",
    },
    {
        "item": "petrichor",
        "translation_ru": "запах земли после дождя",
        "explain_ru": (
            "Тот самый «пахнет дождём» запах мокрой почвы. Научное словечко, "
            "но звучит как из поэзии — идеально для разговоров про погоду без скуки."
        ),
        "origin_ru": "От греч. petra (камень) + ichor (кровь богов) — придумано в 1960-х химиками.",
        "sentence_en": "The petrichor after the storm made the whole city smell brand new.",
        "sentence_ru": "Petrichor после грозы заставил весь город пахнуть как новый.",
    },
    {
        "item": "sonder",
        "translation_ru": "осознание, что у каждого прохожего — своя огромная жизнь",
        "explain_ru": (
            "Не официальный словарь Оксфорда, а слово из современного словаря ощущений. "
            "Полезно, когда хочешь описать город вечером одной точной эмоцией."
        ),
        "origin_ru": "Популярно через The Dictionary of Obscure Sorrows (John Koenig).",
        "sentence_en": "Standing on the subway, I felt a sudden wave of sonder.",
        "sentence_ru": "Стоя в метро, я внезапно поймал волну sonder.",
    },
]

_FALLBACK_PHRASES = [
    {
        "item": "to bite the bullet",
        "translation_ru": "собраться и сделать неприятное, потому что надо",
        "explain_ru": (
            "Буквально «закусить пулю» — раньше так терпели боль без наркоза. "
            "Сейчас: перестать тянуть и просто сделать."
        ),
        "origin_ru": "Военная/медицинская метафора XIX века.",
        "sentence_en": "I finally bit the bullet and called to cancel the subscription.",
        "sentence_ru": "Я наконец bit the bullet и позвонил отменить подписку.",
    },
    {
        "item": "a blessing in disguise",
        "translation_ru": "скрытое благо; плохое, из которого вышло хорошее",
        "explain_ru": (
            "Когда событие сначала бесит, а потом оказывается подарком. "
            "Мягкий способ сказать: «ок, вселенная сыграла странно, но в плюс»."
        ),
        "origin_ru": "Классический английский идиом, часто в разговорах про карьеру и переезды.",
        "sentence_en": "Losing that job was a blessing in disguise — I built something better.",
        "sentence_ru": "Потеря той работы оказалась a blessing in disguise — я сделал лучше.",
    },
]

_FALLBACK_VOICES = [
    {
        "en": (
            "Here's a tiny life hack with words: instead of saying 'I'm busy', "
            "try 'I'm protecting my focus today'. Same boundary — way more adult."
        ),
        "ru": (
            "Маленький лайфхак со словами: вместо «я занят» попробуй "
            "«сегодня я берегу фокус». Та же граница — звучит взрослее."
        ),
    },
    {
        "en": (
            "English has a delicious verb: to 'ghost' someone — vanish from a chat "
            "without explanation. Don't do it to friends. Do notice it in shows."
        ),
        "ru": (
            "В английском есть вкусный глагол to ghost — исчезнуть из переписки "
            "без объяснений. Друзьям так не делай. А в сериалах замечай."
        ),
    },
]

_FALLBACK_FACTS = [
    {
        "en": (
            "The shortest complete sentence in English is often taught as 'I am' — "
            "but in casual speech, 'Go.' or 'Done.' can carry a whole mood."
        ),
        "ru": (
            "Самое короткое «полное» предложение часто учат как I am — "
            "но в живой речи Go. или Done. могут нести целое настроение."
        ),
    },
    {
        "en": (
            "Shakespeare invented or popularized hundreds of words we still use — "
            "including 'lonely', 'swagger', and 'eyeball'."
        ),
        "ru": (
            "Шекспир придумал или закрепил сотни слов, которые мы всё ещё используем — "
            "включая lonely, swagger и eyeball."
        ),
    },
]


def _fallback(kind: str) -> dict:
    if kind == "word":
        return dict(random.choice(_FALLBACK_WORDS))
    if kind == "phrase":
        return dict(random.choice(_FALLBACK_PHRASES))
    if kind == "voice":
        return dict(random.choice(_FALLBACK_VOICES))
    return dict(random.choice(_FALLBACK_FACTS))


def _generate_gpt(kind: str, level: str) -> dict | None:
    from services.gpt import _ask_json

    lvl = (level or "B1").upper()
    ban = (
        "Ban banal textbook stuff: hello, apple, cat, I go to school, "
        "How are you, weather is nice, my name is..."
    )
    if kind == "word":
        fb = _fallback("word")
        data = _ask_json(
            [
                {
                    "role": "system",
                    "content": (
                        "You curate a delightful Word of the Day for English learners. "
                        f"{ban} Pick a vivid, uncommon-but-useful word (CEFR ~{lvl}+). "
                        "Return ONLY JSON with keys: item, translation_ru, explain_ru, "
                        "origin_ru, sentence_en, sentence_ru. "
                        "explain_ru: warm tutor voice (Rico), 2-4 sentences in Russian. "
                        "sentence_en: one memorable natural sentence using the word."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Level hint: {lvl}. Make it witty and memorable.",
                },
            ],
            fb,
            temperature=0.85,
            max_tokens=500,
        )
        if not (data.get("item") and data.get("sentence_en")):
            return None
        return data

    if kind == "phrase":
        fb = _fallback("phrase")
        data = _ask_json(
            [
                {
                    "role": "system",
                    "content": (
                        "You curate Phrase of the Day (idiom / colloquial chunk). "
                        f"{ban} CEFR ~{lvl}. Return ONLY JSON: item, translation_ru, "
                        "explain_ru, origin_ru, sentence_en, sentence_ru. "
                        "Warm Russian tutor tone for explain_ru."
                    ),
                },
                {"role": "user", "content": f"Level: {lvl}. Fresh, useful in real talk."},
            ],
            fb,
            temperature=0.85,
            max_tokens=500,
        )
        if not (data.get("item") and data.get("sentence_en")):
            return None
        return data

    if kind == "voice":
        fb = _fallback("voice")
        data = _ask_json(
            [
                {
                    "role": "system",
                    "content": (
                        "Write a short spoken English monologue for TTS (2-4 sentences), "
                        "fun linguistic/life insight — not a lecture. "
                        f"{ban} Return ONLY JSON: en, ru (Russian translation of en)."
                    ),
                },
                {"role": "user", "content": f"Audience CEFR ~{lvl}. Sound like a clever friend."},
            ],
            fb,
            temperature=0.9,
            max_tokens=350,
        )
        if not data.get("en"):
            return None
        return data

    fb = _fallback("fact")
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Share one surprising English-language or culture fact in English "
                    "(2-3 sentences). "
                    f"{ban} Return ONLY JSON: en, ru."
                ),
            },
            {"role": "user", "content": f"Level ~{lvl}. Prefer weird-but-true language facts."},
        ],
        fb,
        temperature=0.85,
        max_tokens=350,
    )
    if not data.get("en"):
        return None
    return data


def get_or_create_content(user: dict, kind: str) -> dict:
    """Вернуть кэш дня или сгенерировать новый."""
    cached = get_cached(user, kind)
    if cached:
        return cached
    level = user.get("level") or "B1"
    try:
        data = _generate_gpt(kind, level) or _fallback(kind)
    except Exception:
        data = _fallback(kind)
    # нормализация ключей
    if kind in {"word", "phrase"}:
        payload = {
            "item": str(data.get("item") or "").strip(),
            "translation_ru": str(data.get("translation_ru") or "").strip(),
            "explain_ru": str(data.get("explain_ru") or "").strip(),
            "origin_ru": str(data.get("origin_ru") or "").strip(),
            "sentence_en": str(data.get("sentence_en") or "").strip(),
            "sentence_ru": str(data.get("sentence_ru") or "").strip(),
        }
    else:
        payload = {
            "en": str(data.get("en") or "").strip(),
            "ru": str(data.get("ru") or "").strip(),
        }
    set_cached(user, kind, payload)
    return payload


def format_word_or_phrase(kind: str, data: dict, *, first_open: bool) -> str:
    title = "Слово дня" if kind == "word" else "Фраза дня"
    item = _esc(data.get("item") or "")
    tr = spoiler(data.get("translation_ru") or "—")
    explain = _esc(data.get("explain_ru") or "")
    origin = _esc(data.get("origin_ru") or "")
    sent = _esc(data.get("sentence_en") or "")
    sent_ru = spoiler(data.get("sentence_ru") or "—")
    head = "✨ Открываем впервые сегодня!" if first_open else "♻️ Уже открывали сегодня — вот снова:"
    parts = [
        f"🦜 <b>{title}</b>\n",
        head,
        f"\n<b>{item}</b>",
        f"🇷🇺 {tr}",
        f"\n{explain}",
    ]
    if origin:
        parts.append(f"\n🕰 <i>{origin}</i>")
    parts.append(f"\n💬 Пример:\n<i>{sent}</i>")
    parts.append(f"🇷🇺 {sent_ru}")
    parts.append("\n🎙 Сейчас произнесу пример вслух…")
    return "\n".join(parts)


def format_voice(data: dict, *, first_open: bool) -> str:
    en = _esc(data.get("en") or "")
    ru = spoiler(data.get("ru") or "—")
    head = "✨ Голос дня — впервые сегодня!" if first_open else "♻️ Голос дня (повтор):"
    return (
        f"🦜 <b>Голос дня</b>\n\n{head}\n\n"
        f"<i>{en}</i>\n\n"
        f"🇷🇺 Перевод (тапни блюр): {ru}"
    )


def format_fact(data: dict, *, first_open: bool) -> str:
    en = _esc(data.get("en") or "")
    ru = spoiler(data.get("ru") or "—")
    head = "✨ Факт дня — впервые сегодня!" if first_open else "♻️ Факт дня (повтор):"
    return (
        f"🦜 <b>Факт дня</b>\n\n{head}\n\n"
        f"{en}\n\n"
        f"🇷🇺 Перевод (тапни блюр): {ru}\n\n"
        "🎙 Сейчас озвучу факт…"
    )


def tts_text_for(kind: str, data: dict) -> str:
    if kind in {"word", "phrase"}:
        return (data.get("sentence_en") or data.get("item") or "").strip()
    return (data.get("en") or "").strip()


__all__ = [
    "BTN_DAILY_FIRE",
    "BTN_DF_WORD",
    "BTN_DF_PHRASE",
    "BTN_DF_VOICE",
    "BTN_DF_FACT",
    "BTN_DF_BACK",
    "KINDS",
    "BTN_TO_KIND",
    "ensure_daily_fire",
    "is_opened",
    "opened_count",
    "mark_opened",
    "hub_intro",
    "get_or_create_content",
    "format_word_or_phrase",
    "format_voice",
    "format_fact",
    "tts_text_for",
    "spoiler",
]
