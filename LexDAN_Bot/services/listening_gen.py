"""Генерация диалога Listening + заданий через GPT."""

from __future__ import annotations

import logging
import random

log = logging.getLogger(__name__)

# Классический Adam (чат/дефолт бота) — без импорта voices→config
_DEFAULT_ADAM_ID = "pNInz6obpgDQGcFmaJgB"
# Голоса Listening: новые + уже используемые в боте.
# tags — подбор под ситуацию; prefer_levels — бонус на CEFR.
_LISTENING_VOICES: list[dict] = [
    # ── новые ───────────────────────────────────────────────────────
    {
        "key": "jessa",
        "name": "Jessa",
        "gender": "female",
        "voice_id": "yj30vwTGJxSHezdAGsv9",
        "tags": {"friend", "casual", "chat"},
    },
    {
        "key": "adam_friendly",
        "name": "Adam",
        "gender": "male",
        "voice_id": "IRHApOXLvnW57QJPQH2P",
        "tags": {"friend", "casual", "chat"},
    },
    {
        "key": "alex",
        "name": "Alex",
        "gender": "male",
        "voice_id": "GzE4TcXfh9rYCU9gVgPp",
        "tags": {"friend", "service", "sales", "waiter", "consultant"},
    },
    {
        "key": "ad",
        "name": "Ad",
        "gender": "male",
        "voice_id": "ZzBnwUd5N5vZp018EN64",
        "tags": {"radio", "ads", "broadcast", "announcer"},
    },
    {
        "key": "allison",
        "name": "Allison",
        "gender": "female",
        "voice_id": "1wGbFxmAM3Fgw63G1zZJ",
        "tags": {"friend", "casual", "beginner", "calm"},
        "prefer_levels": {"A0", "A1"},
    },
    {
        "key": "yuri",
        "name": "Yuri",
        "gender": "male",
        "voice_id": "UalXHhfqFg6JugnheN0j",
        "tags": {"podcast", "host", "interview", "clear"},
    },
    # ── уже были в боте ─────────────────────────────────────────────
    {
        "key": "adam",
        "name": "Adam",
        "gender": "male",
        "voice_id": _DEFAULT_ADAM_ID,
        "tags": {"friend", "casual", "chat", "teacher"},
    },
    {
        "key": "scotty",
        "name": "Scotty",
        "gender": "male",
        "voice_id": "NfUrCNRReUL9RXS9upG1",
        "tags": {"friend", "casual", "chat"},
    },
    {
        "key": "joe",
        "name": "Joe",
        "gender": "male",
        "voice_id": "av1BMOR1GPgThz9p4fLo",
        "tags": {"friend", "service", "consultant"},
    },
    {
        "key": "ed",
        "name": "Ed",
        "gender": "male",
        "voice_id": "dHd5gvgSOzSfduK4CvEg",
        "tags": {"friend", "casual", "work"},
    },
    {
        "key": "lucas",
        "name": "Lucas",
        "gender": "male",
        "voice_id": "wSqOdjeNqDrHcoK0zorF",
        "tags": {"formal", "work", "interview", "manager"},
    },
    {
        "key": "jimbo",
        "name": "Jimbo",
        "gender": "male",
        "voice_id": "YLbQE9U7P1K6rBNJWNSv",
        "tags": {"friend", "casual", "travel"},
    },
    {
        "key": "emmaline",
        "name": "Emmaline",
        "gender": "female",
        "voice_id": "nDJIICjR9zfJExIFeSCN",
        "tags": {"friend", "casual", "chat", "teacher"},
    },
    {
        "key": "aria",
        "name": "Aria",
        "gender": "female",
        "voice_id": "TC0Zp7WVFzhA8zpTlRqV",
        "tags": {"formal", "work", "service", "consultant"},
    },
    {
        "key": "ruby",
        "name": "Ruby",
        "gender": "female",
        "voice_id": "b8gbDO0ybjX1VA89pBdX",
        "tags": {"friend", "casual", "travel"},
    },
]


def _situation_tags(level: str, topic: dict, roles: str, setting: str) -> set[str]:
    blob = f"{roles} {setting} {topic.get('title_en') or ''} {topic.get('id') or ''}".lower()
    tags: set[str] = set()
    if any(k in blob for k in ("podcast", "host", "radio show", "interview host")):
        tags |= {"podcast", "host"}
    if any(k in blob for k in ("radio", "broadcast", "announc", "advert", "ads", "promo")):
        tags |= {"radio", "ads", "broadcast", "announcer"}
    if any(
        k in blob
        for k in (
            "waiter",
            "barista",
            "bartender",
            "cashier",
            "seller",
            "shop",
            "sales",
            "clerk",
            "receptionist",
            "consultant",
            "agent",
            "support",
            "librarian",
            "trainer",
            "stylist",
            "nurse",
            "doctor",
            "officer",
            "driver",
            "staff",
        )
    ):
        tags |= {"service", "sales", "waiter", "consultant"}
    if any(k in blob for k in ("friend", "classmate", "flatmate", "neighbour", "date", "colleague")):
        tags |= {"friend", "casual", "chat"}
    if any(k in blob for k in ("manager", "interview", "lawyer", "ceo", "professor", "hr", "board")):
        tags |= {"formal", "work", "interview", "manager"}
    if any(k in blob for k in ("travel", "airport", "hotel", "taxi", "station", "tourist")):
        tags |= {"travel", "service"}
    if str(level).upper() in {"A0", "A1"}:
        tags |= {"beginner", "calm"}
    if not tags:
        tags |= {"friend", "casual", "chat"}
    return tags


def _score_voice(v: dict, gender: str, sit_tags: set[str], level: str) -> float:
    if v.get("gender") != gender:
        return -1.0
    vtags = set(v.get("tags") or [])
    score = 1.0 + len(vtags & sit_tags) * 3.0
    prefer = set(v.get("prefer_levels") or [])
    if prefer:
        if str(level).upper() in prefer:
            score += 12.0
        else:
            score -= 4.0
    # жёсткие роли
    key = v.get("key")
    if "podcast" in sit_tags and key == "yuri":
        score += 15.0
    if sit_tags & {"radio", "ads", "broadcast", "announcer"} and key == "ad":
        score += 15.0
    if sit_tags & {"service", "sales", "waiter", "consultant"} and key in {"alex", "emmaline"}:
        score += 6.0
    if sit_tags & {"friend", "casual", "chat"} and key in {"jessa", "adam_friendly"}:
        score += 4.0
    if str(level).upper() in {"A0", "A1"} and key == "allison":
        score += 10.0
    # лёгкий шум, чтобы чередовать
    score += random.random() * 2
    return score


def _pick_voices(
    gender_a: str,
    gender_b: str,
    *,
    level: str,
    topic: dict,
    roles: str,
    setting: str,
) -> tuple[dict, dict]:
    sit = _situation_tags(level, topic, roles, setting)
    pool = list(_LISTENING_VOICES)

    def choose(gender: str, exclude_keys: set[str]) -> dict:
        scored = []
        for v in pool:
            if v["key"] in exclude_keys:
                continue
            # не два «Adam» с разными id в одном диалоге — по имени тоже
            s = _score_voice(v, gender, sit, level)
            if s < 0:
                continue
            scored.append((s, v))
        if not scored:
            fallback = [v for v in pool if v.get("gender") == gender and v["key"] not in exclude_keys]
            if not fallback:
                fallback = [v for v in pool if v.get("gender") == gender] or pool
            return random.choice(fallback)
        scored.sort(key=lambda x: x[0], reverse=True)
        # топ-3 с весом — чередование, не всегда один и тот же
        top = scored[:3]
        weights = [max(0.1, t[0]) for t in top]
        return random.choices([t[1] for t in top], weights=weights, k=1)[0]

    va = choose(gender_a, set())
    used = {va["key"]}
    # если оба голоса с одним display-name — исключить второй с тем же name
    vb = choose(gender_b, used)
    if vb["name"] == va["name"] and gender_a == gender_b:
        vb = choose(gender_b, used | {v["key"] for v in pool if v["name"] == va["name"]})
    elif vb["name"] == va["name"]:
        alt = choose(gender_b, used | {vb["key"]})
        if alt["name"] != va["name"] or alt["key"] != vb["key"]:
            vb = alt
    return va, vb


def _pace_hint(level: str) -> str:
    if level in {"A0", "A1"}:
        return (
            "Speak SLOWLY and clearly: short sentences (5–10 words), "
            "simple vocab, repeat key facts, no idioms."
        )
    if level in {"A2", "B1"}:
        return "Natural everyday pace, clear speech, common phrasal verbs ok."
    return "Fluent natural speech, richer vocabulary matching CEFR level."


def _topic_blob(topic: dict) -> str:
    return " ".join(
        str(topic.get(k) or "")
        for k in ("id", "title_en", "title_ru", "roles", "setting")
    ).lower()


def _topic_must_words(topic: dict) -> list[str]:
    """Ключевые слова, хотя бы часть которых должна встретиться в диалоге."""
    blob = _topic_blob(topic)
    bags = {
        "food": ["food", "eat", "menu", "coffee", "tea", "apple", "bread", "water", "order", "hungry", "breakfast", "lunch", "dinner", "snack", "drink"],
        "cafe": ["coffee", "tea", "latte", "cake", "table", "order", "menu", "barista"],
        "school": ["school", "class", "homework", "lesson", "teacher", "break"],
        "shop": ["price", "size", "bag", "buy", "pay", "shop", "store"],
        "bus": ["bus", "ticket", "stop", "get off", "driver"],
        "doctor": ["doctor", "pain", "medicine", "symptom", "clinic", "nurse", "appointment"],
        "hotel": ["hotel", "room", "check-in", "breakfast", "key", "reservation"],
        "police": ["police", "wallet", "lost", "report", "officer"],
        "bar": ["drink", "bar", "beer", "wine", "card", "cash"],
        "taxi": ["taxi", "address", "traffic", "fare", "driver"],
        "family": ["mum", "mom", "dad", "brother", "sister", "family"],
        "weather": ["sunny", "rainy", "cold", "hot", "weather"],
        "work": ["work", "office", "meeting", "deadline", "boss"],
        "airport": ["flight", "gate", "boarding", "airport", "passport", "luggage"],
        "passport": ["passport", "document", "visa", "border"],
        "podcast": ["podcast", "episode", "listen", "show", "host"],
        "pet": ["cat", "dog", "pet"],
        "color": ["red", "blue", "green", "color", "colour"],
        "number": ["number", "phone", "age"],
        "home": ["kitchen", "room", "door", "window", "home"],
        "gym": ["gym", "train", "exercise", "membership"],
        "bank": ["bank", "account", "card", "pin"],
        "interview": ["job", "experience", "interview", "hire"],
    }
    found: list[str] = []
    for keys, words in [
        (("food", "еда", "cafe", "restaurant", "бар", "bar", "snack"), bags["food"] + bags["cafe"] + bags["bar"]),
        (("school", "класс", "homework"), bags["school"]),
        (("shop", "store", "магазин", "shopping"), bags["shop"]),
        (("bus", "автобус"), bags["bus"]),
        (("doctor", "clinic", "hospital", "врач", "поликлиник"), bags["doctor"]),
        (("hotel", "отел"), bags["hotel"]),
        (("police", "полиц"), bags["police"]),
        (("taxi", "такси"), bags["taxi"]),
        (("family", "семь"), bags["family"]),
        (("weather", "погод"), bags["weather"]),
        (("work", "job", "office", "workplace"), bags["work"]),
        (("airport", "flight", "boarding"), bags["airport"]),
        (("passport", "immigration", "миграц"), bags["passport"]),
        (("podcast", "подкаст"), bags["podcast"]),
        (("pet", "питом"), bags["pet"]),
        (("color", "colour", "цвет"), bags["color"]),
        (("number", "phone", "телефон", "числ"), bags["number"]),
        (("home", "дом", "kitchen"), bags["home"]),
        (("gym", "спортзал"), bags["gym"]),
        (("bank", "банк"), bags["bank"]),
        (("interview", "собеседован"), bags["interview"]),
    ]:
        if any(k in blob for k in keys):
            found.extend(words)
    # слова из setting/title
    for raw in (topic.get("setting"), topic.get("title_en")):
        for w in str(raw or "").replace(",", " ").split():
            w = w.strip().lower()
            if len(w) >= 4 and w.isalpha():
                found.append(w)
    # уникальные
    out = []
    seen = set()
    for w in found:
        if w not in seen:
            seen.add(w)
            out.append(w)
    return out[:24]


def _dialogue_text(pack: dict) -> str:
    turns = pack.get("turns") or []
    return " ".join(str(t.get("text") or "") for t in turns if isinstance(t, dict)).lower()


def _pack_matches_topic(pack: dict, topic: dict) -> bool:
    text = _dialogue_text(pack)
    if not text.strip():
        return False
    must = _topic_must_words(topic)
    if not must:
        return True
    hits = sum(1 for w in must if w in text)
    need = 2 if len(must) >= 4 else 1
    if hits >= need:
        return True
    # жёсткий запрет: паспортный офисный фоллбек на не-паспортной теме
    blob = _topic_blob(topic)
    is_passport_topic = any(k in blob for k in ("passport", "immigration", "миграц", "border"))
    if not is_passport_topic and ("passport" in text or "desk three" in text):
        return False
    return False


_MALE_NAMES = ("Ben", "Tom", "Jake", "Omar", "Leo", "Chris", "Noah", "Ryan")
_FEMALE_NAMES = ("Mia", "Emma", "Sara", "Lily", "Nora", "Anna", "Zoe", "Helen")


def _stable_pair_names(topic: dict) -> tuple[tuple[str, str], tuple[str, str]]:
    """Стабильные имена героев по topic id (не имена ElevenLabs-голосов)."""
    import hashlib

    raw = str(topic.get("id") or topic.get("title_en") or "x").encode("utf-8")
    seed = int(hashlib.md5(raw).hexdigest()[:8], 16)
    n0 = _MALE_NAMES[seed % len(_MALE_NAMES)]
    n1 = _FEMALE_NAMES[(seed // 7) % len(_FEMALE_NAMES)]
    roles = str(topic.get("roles") or "")
    role_a = roles.split(" and ")[0].strip() if " and " in roles else "speaker A"
    blob = roles.lower()
    if any(k in role_a.lower() for k in ("nurse", "mum", "mom", "sister", "waitress", "hostess")):
        return (n1, "female"), (n0, "male")
    if "mother" in blob or "woman" in role_a.lower():
        return (n1, "female"), (n0, "male")
    return (n0, "male"), (n1, "female")


TURN_COUNT = 12

# Пулы правдоподобных отвлекающих ответов (тот же тип, не «футбол vs кафе»)
_PRICE_POOL = [
    "two pounds",
    "three pounds",
    "four pounds",
    "four pounds fifty",
    "five pounds",
    "five pounds fifty",
    "six pounds",
    "six pounds fifty",
    "eight pounds",
    "ten pounds",
    "twelve pounds",
    "fifteen pounds",
    "eighteen pounds",
    "twenty pounds",
    "twenty-eight pounds",
]
_COLOR_POOL = ["red", "blue", "green", "black", "white", "yellow", "brown", "grey", "pink", "orange"]
_TIME_POOL = [
    "at nine",
    "at ten",
    "at ten thirty",
    "at eleven",
    "at two",
    "at three",
    "at four",
    "at five",
    "at five thirty",
    "at six",
    "at seven",
    "at eight",
]
_NUM_POOL = [
    "two",
    "three",
    "four",
    "five",
    "seven",
    "eight",
    "nine",
    "ten",
    "twelve",
    "fourteen",
    "fifteen",
    "seventeen",
    "twenty",
    "twenty-two",
    "thirty",
    "forty",
    "fifty",
]


def _clip(text: str, n: int = 70) -> str:
    t = " ".join(str(text or "").split())
    if len(t) <= n:
        return t
    cut = t[: n - 1].rsplit(" ", 1)[0]
    return (cut or t[: n - 1]).rstrip(".,;:") + "…"


def _shuffle_mcq(correct: str, wrong: list[str], explain_ru: str, options_ru: list[str] | None = None) -> dict:
    opts = [correct] + [w for w in wrong if w and w.lower() != correct.lower()][:3]
    # уникальные
    seen = set()
    uniq = []
    for o in opts:
        k = o.lower()
        if k not in seen:
            seen.add(k)
            uniq.append(o)
    opts = uniq
    while len(opts) < 4:
        opts.append(f"not said ({len(opts)})")
    opts = opts[:4]
    order = list(range(4))
    random.shuffle(order)
    shuffled = [opts[i] for i in order]
    correct_i = next(
        (i for i, x in enumerate(shuffled) if x.lower() == correct.lower()),
        0,
    )
    if options_ru and len(options_ru) >= 4:
        ru_map = {opts[i]: options_ru[i] for i in range(min(4, len(options_ru)))}
        shuffled_ru = [ru_map.get(x, x) for x in shuffled]
    else:
        shuffled_ru = list(shuffled)
    return {
        "question": "",
        "options": shuffled,
        "options_ru": shuffled_ru,
        "correct": correct_i,
        "explain_wrong_ru": explain_ru,
    }


def _alt_from_pool(correct: str, pool: list[str], n: int = 3) -> list[str]:
    c = (correct or "").strip().lower()
    cands = [p for p in pool if p.lower() != c]
    random.shuffle(cands)
    out = cands[:n]
    while len(out) < n:
        out.append(f"not mentioned")
    return out[:n]


def _extract_detail_facts(lines: list[dict], n0: str, n1: str) -> list[dict]:
    """
    Конкретные факты из реплик: цена, цвет, время, номер, количество, место.
    Каждый факт → MCQ и/или true/false без «зеркальных» говорящих.
    """
    import re

    facts: list[dict] = []
    used_keys: set[str] = set()

    def add(fact: dict) -> None:
        key = f"{fact.get('kind')}|{str(fact.get('correct') or '').lower()}"
        if key in used_keys:
            return
        used_keys.add(key)
        facts.append(fact)

    price_re = re.compile(
        r"\b((?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
        r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
        r"twenty-\w+|thirty|forty|fifty|sixty|eighty|\d+)"
        r"(?:\s+point\s+\w+)?(?:\s+pounds?(?:\s+\w+)?)?(?:\s+fifty|\s+twenty)?|"
        r"\d+\s*pounds?(?:\s+\d+)?|£\s*\d+(?:\.\d+)?)\b",
        re.I,
    )
    color_re = re.compile(
        r"\b(red|blue|green|black|white|yellow|brown|grey|gray|pink|orange|silver|teal)\b",
        re.I,
    )
    time_re = re.compile(
        r"\b(?:at|until|by|from|after|before)\s+"
        r"((?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
        r"\d{1,2})(?:\s*(?:thirty|fifteen|forty|o'clock|\d{2}))?"
        r"(?:\s*(?:a\.?m\.?|p\.?m\.?))?)",
        re.I,
    )
    room_re = re.compile(
        r"\b(?:room|gate|desk|platform|floor|row|seat|bed|table|order(?:\s+number)?|bus(?:\s+number)?|"
        r"extension|carriage)\s+"
        r"([A-Z]?\s*\d+[A-Z]?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
        r"fourteen|fifteen|seventeen|twenty|twenty-\w+)\b",
        re.I,
    )
    age_re = re.compile(
        r"\b(?:I am|I'm|she is|he is|is)\s+"
        r"(ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
        r"twenty|twenty-\w+|thirty|forty|forty-\w+|\d+)\s*(?:years?\s*old)?\b",
        re.I,
    )
    qty_re = re.compile(
        r"\b((?:two|three|four|five|six|seven|eight|nine|ten|twelve|fourteen|fifteen|"
        r"seventeen|twenty|thirty|forty|fifty|\d+)\s+"
        r"(?:stops?|nights?|days?|weeks?|minutes?|hours?|words?|pounds?|people|visitors|"
        r"tablets?|films?|kilometres?|rows?|units?|pages?|sources?))\b",
        re.I,
    )
    place_re = re.compile(
        r"\b((?:Green|King|Hill|Park|Oak|Market|Station|River|Hill)\s+"
        r"(?:Street|Road|Avenue|Stop|Lane|Square|Park)|"
        r"second floor|third floor|by the window|near the fountain)\b",
        re.I,
    )

    for i, t in enumerate(lines):
        text = t["text"]
        sp = t["speaker"]

        for m in price_re.finditer(text):
            val = " ".join(m.group(1).split())
            if len(val) < 3:
                continue
            add(
                {
                    "kind": "price",
                    "correct": val,
                    "wrongs": _alt_from_pool(val, _PRICE_POOL),
                    "question": f"How much is mentioned here: «{_clip(text, 48)}»?",
                    "explain_ru": f"В диалоге звучит: {val}.",
                    "true_stmt": f"Someone mentions the amount: {val}.",
                    "false_stmt": f"Someone mentions the amount: {_alt_from_pool(val, _PRICE_POOL, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        for m in color_re.finditer(text):
            val = m.group(1).lower()
            after = text[m.end() : m.end() + 14].lower()
            # «Green Street» — это место, не цвет предмета
            if any(
                after.lstrip().startswith(x)
                for x in ("street", "road", "avenue", "lane", "park", "square", "stop")
            ):
                continue
            add(
                {
                    "kind": "color",
                    "correct": val,
                    "wrongs": _alt_from_pool(val, _COLOR_POOL),
                    "question": f"What colour is mentioned in: «{_clip(text, 52)}»?",
                    "explain_ru": f"В этой реплике цвет — {val}.",
                    "true_stmt": f"The colour {val} is mentioned in the dialogue.",
                    "false_stmt": f"The colour {_alt_from_pool(val, _COLOR_POOL, 1)[0]} is mentioned instead of {val}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        for m in time_re.finditer(text):
            val = "at " + " ".join(m.group(1).split()).lower()
            val = val.replace("at at ", "at ")
            add(
                {
                    "kind": "time",
                    "correct": val,
                    "wrongs": _alt_from_pool(val, _TIME_POOL),
                    "question": f"What time is mentioned in: «{_clip(text, 52)}»?",
                    "explain_ru": f"В диалоге время — {val}.",
                    "true_stmt": f"A time mentioned in the dialogue is {val}.",
                    "false_stmt": f"A time mentioned in the dialogue is {_alt_from_pool(val, _TIME_POOL, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        for m in room_re.finditer(text):
            label = m.group(0)
            num = " ".join(m.group(1).split())
            add(
                {
                    "kind": "number",
                    "correct": num,
                    "wrongs": _alt_from_pool(num, _NUM_POOL),
                    "question": f"Which number is in: «{_clip(label, 40)}»?",
                    "explain_ru": f"В диалоге: {label}.",
                    "true_stmt": f"The dialogue mentions: {label}.",
                    "false_stmt": f"The dialogue mentions: {label.split()[0]} {_alt_from_pool(num, _NUM_POOL, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        for m in age_re.finditer(text):
            val = m.group(1).lower()
            add(
                {
                    "kind": "age",
                    "correct": val,
                    "wrongs": _alt_from_pool(val, _NUM_POOL),
                    "question": f"What age/number is in: «{_clip(text, 52)}»?",
                    "explain_ru": f"Звучит число/возраст: {val}.",
                    "true_stmt": f"The age or number {val} is said in the dialogue.",
                    "false_stmt": f"The age or number {_alt_from_pool(val, _NUM_POOL, 1)[0]} is said instead.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        for m in qty_re.finditer(text):
            val = " ".join(m.group(1).split()).lower()
            wrongs = []
            for alt_n in _alt_from_pool(val.split()[0], _NUM_POOL, 3):
                rest = " ".join(val.split()[1:])
                wrongs.append(f"{alt_n} {rest}".strip())
            add(
                {
                    "kind": "qty",
                    "correct": val,
                    "wrongs": wrongs,
                    "question": f"What quantity is mentioned: «{_clip(text, 52)}»?",
                    "explain_ru": f"В диалоге количество — {val}.",
                    "true_stmt": f"The dialogue mentions {val}.",
                    "false_stmt": f"The dialogue mentions {wrongs[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        for m in place_re.finditer(text):
            val = " ".join(m.group(1).split())
            other_places = [
                "Green Street",
                "King Street",
                "Hill Street",
                "Park Road",
                "Oak Avenue",
                "Market Square",
                "by the window",
                "second floor",
            ]
            add(
                {
                    "kind": "place",
                    "correct": val,
                    "wrongs": _alt_from_pool(val, other_places),
                    "question": f"Which place is mentioned in: «{_clip(text, 52)}»?",
                    "explain_ru": f"Место в диалоге — {val}.",
                    "true_stmt": f"They mention {val}.",
                    "false_stmt": f"They mention {_alt_from_pool(val, other_places, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

    # факт «кто что заказал / сказал предмет» — короткие именные реплики
    item_re = re.compile(
        r"\b(a|an|the|one|large|small)?\s*"
        r"(latte|cappuccino|croissant|muffin|sandwich|apple|tea|water|bag|ticket|"
        r"wallet|umbrella|room|book|coffee|pizza|salad|lager)\b",
        re.I,
    )
    for i, t in enumerate(lines):
        m = item_re.search(t["text"])
        if not m:
            continue
        item = m.group(2).lower()
        others = [x for x in ("latte", "croissant", "sandwich", "tea", "ticket", "wallet", "umbrella", "salad") if x != item]
        random.shuffle(others)
        add(
            {
                "kind": "item",
                "correct": item,
                "wrongs": others[:3],
                "question": f"What item is mentioned by {t['speaker']} in: «{_clip(t['text'], 48)}»?",
                "explain_ru": f"{t['speaker']} говорит про {item}.",
                "true_stmt": f"{t['speaker']} mentions a {item}.",
                "false_stmt": f"{t['speaker']} mentions a {others[0]}.",
                "line_i": i,
                "speaker": t["speaker"],
            }
        )

    # разнообразие типов
    facts.sort(key=lambda f: (f.get("kind") or "", f.get("line_i") or 0))
    # перемешать внутри, сохранив покрытие kinds
    by_kind: dict[str, list] = {}
    for f in facts:
        by_kind.setdefault(f["kind"], []).append(f)
    ordered = []
    kinds = list(by_kind.keys())
    random.shuffle(kinds)
    while any(by_kind.values()):
        for k in kinds:
            if by_kind.get(k):
                ordered.append(by_kind[k].pop(0))
    return ordered


def _derive_tasks_from_turns(turns: list[dict], n0: str, n1: str, topic: dict) -> tuple[list, list, list]:
    """
    Task1: 1× кто сказал + 2× точечных MCQ по деталям диалога.
    Task2: 3× True/False по разным фактам (не зеркало «A сказал / B сказал то же»).
    Task3: 4 события по ходу 12 реплик.
    """
    title = topic.get("title_en") or topic.get("title_ru") or "the topic"
    lines = [
        {"speaker": str(t.get("speaker") or n0), "text": str(t.get("text") or "").strip()}
        for t in turns
        if isinstance(t, dict) and str(t.get("text") or "").strip()
    ]
    for i, t in enumerate(lines):
        if t["speaker"] not in {n0, n1}:
            t["speaker"] = n0 if i % 2 == 0 else n1
    while len(lines) < 4:
        lines.append({"speaker": n0 if len(lines) % 2 == 0 else n1, "text": f"Let's continue with {title}."})

    meat = [t for t in lines if len(t["text"].split()) >= 4] or lines
    early = meat[0]
    late = meat[-1] if meat[-1] is not early else meat[min(1, len(meat) - 1)]

    who_distract = [x for x in (n0, n1, "Alex", "Sam", "Teacher", "Driver") if x != early["speaker"]]
    # только имена из диалога + 1–2 лишних, без угадывания по теме
    who_wrong = []
    for x in who_distract:
        if x not in who_wrong:
            who_wrong.append(x)
        if len(who_wrong) >= 3:
            break

    q1 = _shuffle_mcq(
        early["speaker"],
        who_wrong,
        f"Эту фразу говорит {early['speaker']}.",
        None,
    )
    q1["question"] = f'Who says: "{_clip(early["text"], 64)}"?'
    q1["options_ru"] = list(q1["options"])

    facts = _extract_detail_facts(lines, n0, n1)
    # не строить detail-вопрос на той же реплике, что q1 who-says (по возможности)
    detail_facts = [f for f in facts if f.get("line_i") != 0] or facts

    def mcq_from_fact(f: dict) -> dict:
        q = _shuffle_mcq(
            str(f["correct"]),
            list(f.get("wrongs") or []),
            str(f.get("explain_ru") or "Слушай внимательнее эту деталь."),
            None,
        )
        q["question"] = str(f["question"])
        q["options_ru"] = list(q["options"])
        return q

    if len(detail_facts) >= 2:
        q2 = mcq_from_fact(detail_facts[0])
        q3 = mcq_from_fact(detail_facts[1])
    elif len(detail_facts) == 1:
        q2 = mcq_from_fact(detail_facts[0])
        q3 = _shuffle_mcq(
            late["speaker"],
            [x for x in (n0, n1, "Alex", "Sam") if x != late["speaker"]][:3],
            f"Ближе к концу говорит {late['speaker']}.",
            None,
        )
        q3["question"] = f'Near the end, who says: "{_clip(late["text"], 64)}"?'
        q3["options_ru"] = list(q3["options"])
    else:
        # запас: две разные цитаты «что прозвучало» с правдоподобными искажениями из других реплик
        mid = meat[len(meat) // 2]
        real = _clip(mid["text"], 56)
        other_bits = [_clip(x["text"], 56) for x in meat if x is not mid][:3]
        while len(other_bits) < 3:
            other_bits.append(_clip(early["text"], 56) + " (later)")
        # лёгкие правки чисел в wrong — не уводим в другую тему
        q2 = _shuffle_mcq(real, other_bits, f"В диалоге звучит: «{real}».", None)
        q2["question"] = f"Which line did you hear in the dialogue?"
        q2["options_ru"] = list(q2["options"])
        q3 = _shuffle_mcq(
            late["speaker"],
            [x for x in (n0, n1, "Alex", "Sam") if x != late["speaker"]][:3],
            f"Ближе к концу говорит {late['speaker']}.",
            None,
        )
        q3["question"] = f'Near the end, who says: "{_clip(late["text"], 64)}"?'
        q3["options_ru"] = list(q3["options"])

    task1 = [q1, q2, q3]

    # Task2: три независимых утверждения
    tf_facts = [f for f in detail_facts[2:]] or list(detail_facts)
    if len(tf_facts) < 3:
        # добрать из оставшихся / синтетика по репликам
        for t in meat[1:]:
            if len(tf_facts) >= 6:
                break
            tf_facts.append(
                {
                    "true_stmt": f'{t["speaker"]} talks about this: "{_clip(t["text"], 42)}"',
                    "false_stmt": f'{t["speaker"]} says they need a passport at desk three.',
                    "explain_ru": f"Сверь с репликой {t['speaker']}.",
                    "kind": "line",
                }
            )

    task2 = []
    # паттерн: True, False, True/False — разные факты, без speaker-mirror
    plan = [
        (tf_facts[0], True),
        (tf_facts[1 % len(tf_facts)], False),
        (tf_facts[2 % len(tf_facts)], True if len(tf_facts) > 2 else False),
    ]
    # если 2-й и 0-й один и тот же объект — сдвинуть
    if plan[1][0] is plan[0][0] and len(tf_facts) > 1:
        plan[1] = (tf_facts[1], False)
    if plan[2][0] is plan[0][0] or plan[2][0] is plan[1][0]:
        for f in tf_facts:
            if f is not plan[0][0] and f is not plan[1][0]:
                plan[2] = (f, False)
                break

    for fact, want_true in plan:
        if want_true:
            stmt = fact.get("true_stmt") or fact.get("false_stmt")
            is_true = True
            explain = fact.get("explain_ru") or "Это правда по диалогу."
        else:
            stmt = fact.get("false_stmt") or (
                "They only discuss a football match at midnight."
            )
            # не использовать football если это правда в тексте
            blob = " ".join(x["text"].lower() for x in lines)
            if "football" in (stmt or "").lower() and "football" in blob:
                stmt = f"They say the price is {_PRICE_POOL[0]} (wrong amount)."
            is_true = False
            explain = fact.get("explain_ru") or "Этого в диалоге не было / цифра другая."
        task2.append(
            {
                "statement": stmt,
                "is_true": is_true,
                "explain_ru": explain,
            }
        )

    # Task3: события из разных частей 12-репликового диалога
    idxs = [0, 3, 6, 9]
    events = []
    for j in idxs:
        t = lines[j] if j < len(lines) else lines[j % len(lines)]
        events.append(f"{t['speaker']}: {_clip(t['text'], 42)}")

    return task1, task2, events[:4]


def _fallback_dialogue_turns(topic: dict, n0: str, n1: str) -> list[tuple[str, str]]:
    """Уникальный запасной диалог 12 реплик под тему."""
    from data.listening_fallbacks import get_fallback_turns

    return get_fallback_turns(topic, n0, n1)


def _fallback_pack(level: str, topic: dict) -> dict:
    """Запасной диалог строго по теме; задания строятся из реплик отдельно."""
    roles = topic.get("roles") or "two people"
    role_a = roles.split(" and ")[0].strip() if " and " in roles else "speaker A"
    role_b = roles.split(" and ")[-1].strip() if " and " in roles else "speaker B"
    (n0, g0), (n1, g1) = _stable_pair_names(topic)
    pairs = _fallback_dialogue_turns(topic, n0, n1)
    turns = [{"speaker": a, "text": b} for a, b in pairs]
    t1, t2, events = _derive_tasks_from_turns(turns, n0, n1, topic)
    return {
        "speakers": [
            {"name": n0, "gender": g0, "role": role_a},
            {"name": n1, "gender": g1, "role": role_b},
        ],
        "turns": turns,
        "task1": t1,
        "task2": t2,
        "task3_events": events,
    }


def generate_listening_pack(level: str, topic: dict) -> dict:
    from services.gpt import _ask_json

    fallback = _fallback_pack(level, topic)
    setting = topic.get("setting") or topic.get("title_en") or "everyday situation"
    roles = topic.get("roles") or "two people in a realistic situation"
    title_en = topic.get("title_en") or "Topic"
    title_ru = topic.get("title_ru") or title_en
    pace = _pace_hint(level)
    must = ", ".join(_topic_must_words(topic)[:12]) or setting
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Create CEFR listening practice JSON for Russian learners. ONLY JSON.\n"
                    "Keys: speakers, turns, task1, task2, task3_events.\n"
                    "speakers: exactly 2 {name, gender:male|female, role}. "
                    "Use short natural first names (NOT Alex/Sam every time). "
                    "Names in turns MUST match speakers[].name exactly.\n"
                    f"CRITICAL TOPIC LOCK: The WHOLE dialogue MUST be about «{title_en}» / «{title_ru}».\n"
                    f"Setting: {setting}. Roles: {roles}.\n"
                    f"Use these topic words naturally: {must}.\n"
                    f"turns: exactly {TURN_COUNT} {{speaker,text}}. speaker = one of the two names. {pace}\n"
                    "CRITICAL DETAIL DENSITY: Plant at least 6 concrete listen-for details "
                    "(prices with pounds, clock times, colours, room/gate/order numbers, ages, "
                    "quantities, street names). Say numbers mostly in WORDS for beginners.\n"
                    "FORBIDDEN: invent a different situation (e.g. passport desk) "
                    "unless the topic itself is about that.\n"
                    "task1/task2/task3_events: include stubs; they will be rebuilt from the dialogue.\n"
                    f"CEFR level: {level}."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level:{level}\nTopic EN:{title_en}\nTopic RU:{title_ru}\n"
                    f"Roles:{roles}\nSetting:{setting}\n"
                    f"Write ONLY about this topic with rich concrete details. "
                    f"Exactly {TURN_COUNT} turns. Seed:{random.random()}"
                ),
            },
        ],
        fallback,
        temperature=0.45,
        max_tokens=2500,
    )
    pack = _normalize_pack(data, fallback)
    if not _pack_matches_topic(pack, topic):
        log.warning(
            "Listening pack off-topic for %s/%s — using topic fallback",
            topic.get("id"),
            title_en,
        )
        pack = _normalize_pack(fallback, fallback)

    # Вопросы ВСЕГДА из финального диалога + имена героев (не голосов TTS)
    sp = pack["speakers"]
    n0 = sp[0]["name"]
    n1 = sp[1]["name"]
    t1, t2, ev = _derive_tasks_from_turns(pack["turns"], n0, n1, topic)
    pack["task1"] = t1
    pack["task2"] = t2
    pack["task3_events"] = ev

    g0 = (sp[0].get("gender") or "male").lower()
    g1 = (sp[1].get("gender") or "female").lower()
    if g0 not in {"male", "female"}:
        g0 = "male"
    if g1 not in {"male", "female"}:
        g1 = "female"
    v0, v1 = _pick_voices(g0, g1, level=level, topic=topic, roles=roles, setting=setting)
    voice_map = {n0: v0, n1: v1}
    pack["voice_map"] = {
        name: {"key": v["key"], "voice_id": v["voice_id"], "voice_name": v["name"]}
        for name, v in voice_map.items()
    }
    numbered = []
    for i, t in enumerate(pack["turns"], start=1):
        vinfo = pack["voice_map"].get(t["speaker"]) or {}
        speaker = t["speaker"]
        numbered.append(
            {
                "n": i,
                "speaker": speaker,
                "text": t["text"],
                # Подпись = имя героя диалога (как в вопросах), НЕ имя голоса ElevenLabs
                "label": f"{speaker} {i}",
                "voice_id": vinfo.get("voice_id"),
            }
        )
    pack["turns_numbered"] = numbered
    return pack


def build_order_summary(events: list[str]) -> str:
    """Мини-текст с связками из правильного порядка событий."""
    if not events:
        return ""
    connectors = ["First,", "Then,", "After that,", "Finally,"]
    parts = []
    for i, ev in enumerate(events):
        e = ev.strip().rstrip(".")
        if e and e[0].islower():
            e = e[0].upper() + e[1:]
        conn = connectors[i] if i < len(connectors) else "Next,"
        parts.append(f"{conn} {e}.")
    return " ".join(parts)


def _normalize_pack(data: dict, fallback: dict) -> dict:
    if not isinstance(data, dict):
        return fallback
    speakers = data.get("speakers")
    turns = data.get("turns")
    if not (isinstance(speakers, list) and len(speakers) >= 2):
        return fallback
    if not (isinstance(turns, list) and len(turns) >= 8):
        return fallback
    sp0 = speakers[0] if isinstance(speakers[0], dict) else {"name": "Ben", "gender": "male"}
    sp1 = speakers[1] if isinstance(speakers[1], dict) else {"name": "Mia", "gender": "female"}
    n0 = str(sp0.get("name") or "Ben").strip() or "Ben"
    n1 = str(sp1.get("name") or "Mia").strip() or "Mia"
    if n0.lower() == n1.lower():
        n1 = "Mia" if n0.lower() != "mia" else "Emma"
    clean_turns = []
    for t in turns[:TURN_COUNT]:
        if not isinstance(t, dict):
            continue
        sp = str(t.get("speaker") or n0).strip()
        if sp not in {n0, n1}:
            low = sp.lower()
            if low in {n0.lower(), n1.lower()}:
                sp = n0 if low == n0.lower() else n1
            else:
                sp = n0 if len(clean_turns) % 2 == 0 else n1
        text = str(t.get("text") or "").strip()
        if text:
            clean_turns.append({"speaker": sp, "text": text})
    # если GPT дал меньше 12 — добираем из fallback, не короткими «Okay»
    if len(clean_turns) < TURN_COUNT:
        fb_turns = fallback.get("turns") or []
        for t in fb_turns:
            if len(clean_turns) >= TURN_COUNT:
                break
            if not isinstance(t, dict):
                continue
            text = str(t.get("text") or "").strip()
            if not text:
                continue
            sp = str(t.get("speaker") or n0).strip()
            if sp not in {n0, n1}:
                sp = n0 if len(clean_turns) % 2 == 0 else n1
            clean_turns.append({"speaker": sp, "text": text})
    while len(clean_turns) < TURN_COUNT:
        clean_turns.append(
            {"speaker": n0 if len(clean_turns) % 2 == 0 else n1, "text": "Okay, I understand."}
        )
    clean_turns = clean_turns[:TURN_COUNT]

    t1, t2, ev = _derive_tasks_from_turns(clean_turns, n0, n1, {"title_en": "Topic", "title_ru": "Тема"})
    fb1 = fallback.get("task1") or t1
    fb2 = fallback.get("task2") or t2
    fbev = fallback.get("task3_events") or ev

    return {
        "speakers": [
            {"name": n0, "gender": str(sp0.get("gender") or "male"), "role": str(sp0.get("role") or "")},
            {"name": n1, "gender": str(sp1.get("gender") or "female"), "role": str(sp1.get("role") or "")},
        ],
        "turns": clean_turns,
        "task1": fb1,
        "task2": fb2,
        "task3_events": list(fbev)[:4] if fbev else ev,
    }
