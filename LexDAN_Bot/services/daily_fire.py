"""
🔥 Огонь дня — слово / фраза / голос / факт.
Каждую кнопку можно открыть 1 раз в сутки (МСК), контент кэшируется на день.
"""

from __future__ import annotations

import html
import random
import re
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
    # история без повторов живёт отдельно и не сбрасывается в 00:00
    seen = user.get("daily_fire_seen")
    if not isinstance(seen, dict):
        seen = {}
    for k in KINDS:
        if not isinstance(seen.get(k), list):
            seen[k] = []
    user["daily_fire_seen"] = seen

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


def _norm_key(s: str) -> str:
    t = (s or "").strip().lower()
    t = t.replace("’", "'").replace("`", "'")
    t = re.sub(r"[^\w\s'-]", " ", t, flags=re.UNICODE)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:160]


def fingerprint_for(kind: str, payload: dict) -> str:
    if kind in {"word", "phrase"}:
        return _norm_key(payload.get("item") or "")
    return _norm_key(payload.get("en") or "")


def seen_keys(user: dict, kind: str) -> set[str]:
    ensure_daily_fire(user)
    return {str(x) for x in (user.get("daily_fire_seen") or {}).get(kind) or [] if x}


def remember_seen(user: dict, kind: str, payload: dict) -> None:
    ensure_daily_fire(user)
    fp = fingerprint_for(kind, payload)
    if not fp:
        return
    store = user.setdefault("daily_fire_seen", {})
    arr = list(store.get(kind) or [])
    if fp not in arr:
        arr.append(fp)
    # длинная память, но без бесконечного роста
    store[kind] = arr[-400:]


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
        "(потом можно переслушать то же самое).\n"
        "Каждый новый день — <b>новый</b> контент: слова, фразы, голоса и факты не повторяются 🔄",
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
            "Не из классического Оксфорда, а из словаря тонких ощущений. "
            "Одной точной эмоцией описывает город вечером."
        ),
        "origin_ru": "The Dictionary of Obscure Sorrows (John Koenig).",
        "sentence_en": "Standing on the subway, I felt a sudden wave of sonder.",
        "sentence_ru": "Стоя в метро, я внезапно поймал волну sonder.",
    },
    {
        "item": "ephemeral",
        "translation_ru": "мимолётный, недолговечный",
        "explain_ru": (
            "Про красоту, которая не просит остаться навсегда: закат, пенка на кофе, "
            "удачная шутка в чате. Звучит умно и очень по-английски."
        ),
        "origin_ru": "От греч. ephēmeros — «для одного дня».",
        "sentence_en": "Street art is often ephemeral — here today, painted over tomorrow.",
        "sentence_ru": "Уличное искусство часто ephemeral — сегодня есть, завтра закрасили.",
    },
    {
        "item": "hiraeth",
        "translation_ru": "тоска по дому, которого уже нет / по месту, куда нельзя вернуться",
        "explain_ru": (
            "Глубже обычного homesickness: тоска по чувству, а не только по адресу. "
            "Заимствование из валлийского — англичане его полюбили."
        ),
        "origin_ru": "Валлийское слово, вошедшее в англоязычный обиход.",
        "sentence_en": "Scrolling old photos gave me a quiet hiraeth for that summer.",
        "sentence_ru": "Лента старых фото навеяла тихий hiraeth по тому лету.",
    },
    {
        "item": "flabbergasted",
        "translation_ru": "ошарашенный; в полном шоке (разговорно)",
        "explain_ru": (
            "Когда «wow» уже мало. Звучит смешно и театрально — идеально для реакций, "
            "а не для официальных писем."
        ),
        "origin_ru": "Английский XVIII века, точное происхождение спорное — тем милее.",
        "sentence_en": "I was flabbergasted when the tiny café had the best pasta in town.",
        "sentence_ru": "Я был flabbergasted, что в крошечном кафе — лучшая паста в городе.",
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
        "origin_ru": "Классический английский идиом.",
        "sentence_en": "Losing that job was a blessing in disguise — I built something better.",
        "sentence_ru": "Потеря той работы оказалась a blessing in disguise — я сделал лучше.",
    },
    {
        "item": "to read the room",
        "translation_ru": "считать атмосферу; понимать, что уместно сейчас",
        "explain_ru": (
            "Современный навык: не шутить на похоронах настроения. "
            "Часто про созвоны, тусовки и чаты."
        ),
        "origin_ru": "Разговорный американский оборот.",
        "sentence_en": "He started a loud joke, then finally read the room and went quiet.",
        "sentence_ru": "Он начал громкую шутку, потом read the room и замолчал.",
    },
    {
        "item": "to move the goalposts",
        "translation_ru": "менять правила по ходу; сдвигать «финиш»",
        "explain_ru": (
            "Когда критерии успеха внезапно «переехали». Полезно в разговорах "
            "про работу, отношения и бесконечные правки ТЗ."
        ),
        "origin_ru": "Спортивная метафора → перенос в жизнь и бизнес.",
        "sentence_en": "Every week they move the goalposts, so the project never feels done.",
        "sentence_ru": "Каждую неделю они move the goalposts — проект будто бесконечный.",
    },
    {
        "item": "spill the tea",
        "translation_ru": "рассказать сплетни / сочную правду (сленг)",
        "explain_ru": (
            "Не про чайник. «Tea» = gossip. Дружеский, мемный регистр — "
            "не для собеседования, зато для сторис и чатов."
        ),
        "origin_ru": "Афроамериканский сленг → интернет-культура.",
        "sentence_en": "Okay, spill the tea — what really happened at the party?",
        "sentence_ru": "Ну же, spill the tea — что там было на вечеринке?",
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
    {
        "en": (
            "Try this softener: 'I might be wrong, but…' It keeps your point "
            "and lowers the temperature of any debate."
        ),
        "ru": (
            "Попробуй смягчение: I might be wrong, but… Ты сохраняешь мысль "
            "и снижаешь температуру любого спора."
        ),
    },
    {
        "en": (
            "A lovely adjective: 'overwhelmed' — not just busy, but flooded. "
            "Name the feeling and English suddenly feels more honest."
        ),
        "ru": (
            "Классное слово overwhelmed — не просто «занят», а «захлёстнуло». "
            "Назови чувство — и английский сразу честнее."
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
    {
        "en": (
            "English loves silent letters: the 'k' in knife, the 'b' in doubt, "
            "the 'gh' in night — fossils of older pronunciations."
        ),
        "ru": (
            "Английский любит немые буквы: k в knife, b в doubt, "
            "gh в night — окаменелости старого произношения."
        ),
    },
    {
        "en": (
            "The word 'okay' may come from a 19th-century joke abbreviation: "
            "O.K. for 'oll korrect' — a playful misspelling of 'all correct'."
        ),
        "ru": (
            "Слово okay, возможно, из шуточной аббревиатуры XIX века: "
            "O.K. = oll korrect — игривая ошибка вместо all correct."
        ),
    },
]


def _fallback_pool(kind: str) -> list[dict]:
    if kind == "word":
        return list(_FALLBACK_WORDS)
    if kind == "phrase":
        return list(_FALLBACK_PHRASES)
    if kind == "voice":
        return list(_FALLBACK_VOICES)
    return list(_FALLBACK_FACTS)


def _fallback(kind: str, avoid: set[str] | None = None) -> dict:
    avoid = avoid or set()
    pool = _fallback_pool(kind)
    fresh = [x for x in pool if fingerprint_for(kind, x) not in avoid]
    choice = random.choice(fresh or pool)
    return dict(choice)


def _generate_gpt(kind: str, level: str, *, avoid: set[str] | None = None) -> dict | None:
    from services.gpt import _ask_json

    lvl = (level or "B1").upper()
    avoid = avoid or set()
    avoid_line = ""
    if avoid:
        sample = ", ".join(sorted(avoid)[:40])
        avoid_line = (
            f" Do NOT reuse any of these already-seen items/phrases/topics: {sample}."
        )
    ban = (
        "Ban banal textbook stuff: hello, apple, cat, I go to school, "
        "How are you, weather is nice, my name is..."
    )
    if kind == "word":
        fb = _fallback("word", avoid)
        data = _ask_json(
            [
                {
                    "role": "system",
                    "content": (
                        "You curate a delightful Word of the Day for English learners. "
                        f"{ban} Pick a vivid, uncommon-but-useful word (CEFR ~{lvl}+). "
                        f"Every day must feel NEW.{avoid_line} "
                        "Return ONLY JSON with keys: item, translation_ru, explain_ru, "
                        "origin_ru, sentence_en, sentence_ru. "
                        "explain_ru: warm tutor voice (Rico), 2-4 sentences in Russian. "
                        "sentence_en: one memorable natural sentence using the word."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Level hint: {lvl}. Make it witty and memorable. Fresh word only.",
                },
            ],
            fb,
            temperature=0.9,
            max_tokens=500,
        )
        if not (data.get("item") and data.get("sentence_en")):
            return None
        return data

    if kind == "phrase":
        fb = _fallback("phrase", avoid)
        data = _ask_json(
            [
                {
                    "role": "system",
                    "content": (
                        "You curate Phrase of the Day (idiom / colloquial chunk). "
                        f"{ban} CEFR ~{lvl}. Fresh only — no repeats.{avoid_line} "
                        "Return ONLY JSON: item, translation_ru, "
                        "explain_ru, origin_ru, sentence_en, sentence_ru. "
                        "Warm Russian tutor tone for explain_ru."
                    ),
                },
                {"role": "user", "content": f"Level: {lvl}. Fresh, useful in real talk."},
            ],
            fb,
            temperature=0.9,
            max_tokens=500,
        )
        if not (data.get("item") and data.get("sentence_en")):
            return None
        return data

    if kind == "voice":
        fb = _fallback("voice", avoid)
        data = _ask_json(
            [
                {
                    "role": "system",
                    "content": (
                        "Write a short spoken English monologue for TTS (2-4 sentences), "
                        "fun linguistic/life insight — not a lecture. "
                        f"{ban} Brand-new angle every time.{avoid_line} "
                        "Return ONLY JSON: en, ru (Russian translation of en)."
                    ),
                },
                {"role": "user", "content": f"Audience CEFR ~{lvl}. Sound like a clever friend."},
            ],
            fb,
            temperature=0.95,
            max_tokens=350,
        )
        if not data.get("en"):
            return None
        return data

    fb = _fallback("fact", avoid)
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Share one surprising English-language or culture fact in English "
                    f"(2-3 sentences). {ban} Must be new, not previously used.{avoid_line} "
                    "Return ONLY JSON: en, ru."
                ),
            },
            {"role": "user", "content": f"Level ~{lvl}. Prefer weird-but-true language facts."},
        ],
        fb,
        temperature=0.9,
        max_tokens=350,
    )
    if not data.get("en"):
        return None
    return data


def _normalize_payload(kind: str, data: dict) -> dict:
    if kind in {"word", "phrase"}:
        return {
            "item": str(data.get("item") or "").strip(),
            "translation_ru": str(data.get("translation_ru") or "").strip(),
            "explain_ru": str(data.get("explain_ru") or "").strip(),
            "origin_ru": str(data.get("origin_ru") or "").strip(),
            "sentence_en": str(data.get("sentence_en") or "").strip(),
            "sentence_ru": str(data.get("sentence_ru") or "").strip(),
        }
    return {
        "en": str(data.get("en") or "").strip(),
        "ru": str(data.get("ru") or "").strip(),
    }


def get_or_create_content(user: dict, kind: str) -> dict:
    """Вернуть кэш дня или сгенерировать новый без повторов из истории."""
    cached = get_cached(user, kind)
    if cached:
        return cached
    level = user.get("level") or "B1"
    avoid = seen_keys(user, kind)
    payload = None
    for _ in range(3):
        try:
            data = _generate_gpt(kind, level, avoid=avoid) or _fallback(kind, avoid)
        except Exception:
            data = _fallback(kind, avoid)
        cand = _normalize_payload(kind, data)
        fp = fingerprint_for(kind, cand)
        if fp and fp not in avoid:
            payload = cand
            break
        avoid = set(avoid) | ({fp} if fp else set())
    if payload is None:
        payload = _normalize_payload(kind, _fallback(kind, avoid))
    set_cached(user, kind, payload)
    remember_seen(user, kind, payload)
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
