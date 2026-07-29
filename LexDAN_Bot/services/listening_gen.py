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


def _close_price_alts(correct: str, n: int = 3) -> list[str]:
    """Близкие суммы — все выглядят правдоподобно."""
    c = (correct or "").strip().lower()
    if c in [p.lower() for p in _PRICE_POOL]:
        idx = next(i for i, p in enumerate(_PRICE_POOL) if p.lower() == c)
        near = []
        for d in (1, -1, 2, -2, 3, -3):
            j = idx + d
            if 0 <= j < len(_PRICE_POOL):
                near.append(_PRICE_POOL[j])
        return _alt_from_pool(correct, near + _PRICE_POOL, n)
    return _alt_from_pool(correct, _PRICE_POOL, n)


def _noun_near(text: str, pos: int, window: int = 40) -> str | None:
    """Существительное рядом с ценой для вопроса How much is the X?"""
    import re

    chunk = text[max(0, pos - window) : pos + window].lower()
    nouns = (
        "ticket|latte|cappuccino|croissant|muffin|sandwich|apple|tea|coffee|bag|"
        "wallet|umbrella|room|book|salad|lager|cheesecake|brownie|cone|stamp|"
        "membership|fine|trip|journey|bill|total|order|drink|meal|fare"
    )
    m = re.search(rf"\b(the|a|an|your|my)?\s*({nouns})\b", chunk)
    if m:
        return m.group(2)
    m2 = re.search(rf"\b({nouns})\b", chunk)
    return m2.group(1) if m2 else None


def _extract_detail_facts(lines: list[dict], n0: str, n1: str) -> list[dict]:
    """
    Факты с простыми вопросами БЕЗ цитаты реплики и БЕЗ ответа в формулировке.
    Пример: How much is the ticket? / Which platform? / What colour is the wallet?
    """
    import re

    facts: list[dict] = []
    used_q: set[str] = set()

    def add(fact: dict) -> None:
        q = (fact.get("question") or "").strip()
        ans = str(fact.get("correct") or "").strip().lower()
        if not q or not ans:
            return
        if ans and ans in q.lower():
            return
        key = q.lower()
        if key in used_q:
            return
        used_q.add(key)
        facts.append(fact)

    price_val = (
        r"(?:twenty-\w+|thirty(?:-\w+)?|forty(?:-\w+)?|fifty(?:-\w+)?|sixty|eighty|"
        r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
        r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
        r"\d+(?:\.\d+)?)"
        r"(?:\s+hundred(?:\s+\w+)?)?"
        r"(?:\s+pounds?(?:\s+(?:fifty|twenty|eighty))?|\s+pound|\s+euros?|\s+dollars?)?"
    )
    price_with_item = re.compile(
        rf"\b(?:the|a|an)?\s*(ticket|latte|cappuccino|croissant|muffin|sandwich|apple|"
        rf"bag|wallet|umbrella|cheesecake|brownie|salad|lager|coffee|tea|fare|bill|stamp|"
        rf"membership|room|fine)\s+(?:is|are|costs?)\s+({price_val})\b",
        re.I,
    )
    price_thats = re.compile(
        rf"\b(?:that's|its|it's|total(?:\s+is)?)\s+({price_val})\b",
        re.I,
    )
    price_altogether = re.compile(rf"\b({price_val})\s+altogether\b", re.I)
    price_about = re.compile(rf"\b(?:about|around|roughly)\s+({price_val})\b", re.I)

    labeled_num = re.compile(
        r"\b(platform|gate|desk|room|floor|row|seat|bed|table|carriage|order(?:\s+number)?|"
        r"bus(?:\s+number)?|extension)\s+"
        r"(\d{2,3}|[A-Z]\s*\d+[A-Z]?|"
        r"two hundred(?:\s+\w+)?|one hundred(?:\s+\w+)?|"
        r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
        r"fourteen|fifteen|seventeen|twenty|twenty-\w+|B\s*\d+)\b",
        re.I,
    )
    color_noun = re.compile(
        r"\b(red|blue|green|black|white|yellow|brown|grey|gray|pink|orange|silver)\s+"
        r"(wallet|bag|umbrella|door|T-shirt|t-shirt|ball|chairs?|sign|vest|lamp|cone)\b",
        re.I,
    )
    noun_color = re.compile(
        r"\b(wallet|bag|umbrella|door|T-shirt|t-shirt|ball|chairs?|sign|vest|lamp)\s+"
        r"(?:is|are|'s)\s+(red|blue|green|black|white|yellow|brown|grey|gray|pink|orange)\b",
        re.I,
    )
    time_leave = re.compile(
        r"\b(?:leave[s]?|depart(?:s|ure)?|start(?:s)?|meet(?:s)?|arrive[s]?|open(?:s)?|"
        r"close[s]?|finish(?:es)?|film starts?|class|lesson|appointment|boarding)\b"
        r".{0,40}?\b(?:at|until|by|from|after|before)\s+"
        r"((?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d{1,2})"
        r"(?:\s*(?:thirty|fifteen|forty|o'clock|\d{2}))?(?:\s*(?:a\.?m\.?|p\.?m\.?))?)",
        re.I,
    )
    time_simple = re.compile(
        r"\b(?:at|until|by)\s+"
        r"((?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d{1,2})"
        r"(?:\s*(?:thirty|fifteen|forty|o'clock|\d{2}))?(?:\s*(?:a\.?m\.?|p\.?m\.?))?)",
        re.I,
    )
    stops_re = re.compile(
        r"\b(two|three|four|five|six|seven|eight|nine|ten|\d+)\s+stops?\b",
        re.I,
    )
    nights_re = re.compile(
        r"\b(two|three|four|five|six|seven|\d+)\s+nights?\b",
        re.I,
    )
    age_re = re.compile(
        r"\b(?:sister|brother|dad|mum|mom|she|he|I)\s+(?:is|am|'m)\s+"
        r"(ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
        r"twenty|twenty-\w+|thirty|forty|forty-\w+|\d+)(?:\s+years?\s+old)?\b",
        re.I,
    )
    age_re2 = re.compile(
        r"\b(?:I am|I'm|she is|he is)\s+"
        r"(ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
        r"twenty|twenty-\w+|thirty|forty|forty-\w+|\d+)(?:\s+years?\s+old)?\b",
        re.I,
    )
    place_re = re.compile(
        r"\b(?:get off at|meet (?:at|on|near)|live(?:s)? (?:at|on)|café on|cafe on|on)\s+"
        r"((?:Green|King|Hill|Park|Oak|Market|Station|River)\s+(?:Street|Road|Avenue|Stop|Lane|Square)|"
        r"Park Stop|the (?:library|cinema|station|café|cafe|window))\b",
        re.I,
    )
    item_order = re.compile(
        r"\b(?:want|like|get|have|order(?:ed)?|I'll have|A )\b.{0,24}\b"
        r"(a|an|the|one|large|small)?\s*"
        r"(latte|cappuccino|croissant|muffin|sandwich|apple|salad|lager|coffee|tea|brownie)\b",
        re.I,
    )

    label_q = {
        "platform": "Which platform?",
        "gate": "Which gate?",
        "desk": "Which desk?",
        "room": "What is the room number?",
        "floor": "Which floor?",
        "row": "Which row?",
        "seat": "Which seat?",
        "bed": "Which bed?",
        "table": "Which table?",
        "carriage": "Which carriage?",
        "order": "What is the order number?",
        "order number": "What is the order number?",
        "bus": "What is the bus number?",
        "bus number": "What is the bus number?",
        "extension": "What is the extension number?",
    }

    def _money_ok(val: str, text: str) -> bool:
        v = val.lower()
        if "pound" in v or "euro" in v or "dollar" in v or "£" in v:
            return True
        return bool(re.search(r"pound|euro|dollar|£|\$", text, re.I))

    for i, t in enumerate(lines):
        text = t["text"]
        prev = lines[i - 1]["text"] if i > 0 else ""
        ctx = f"{prev} {text}"
        sp = t["speaker"]

        for m in price_with_item.finditer(text):
            item, val = m.group(1).lower(), " ".join(m.group(2).split())
            if not _money_ok(val, text):
                continue
            add(
                {
                    "kind": "price",
                    "correct": val,
                    "wrongs": _close_price_alts(val),
                    "question": f"How much is the {item}?",
                    "explain_ru": f"В диалоге {item} стоит {val}.",
                    "true_stmt": f"The {item} costs {val}.",
                    "false_stmt": f"The {item} costs {_close_price_alts(val, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        for pat in (price_thats, price_altogether, price_about):
            for m in pat.finditer(text):
                val = " ".join(m.group(1).split())
                if not _money_ok(val, text):
                    continue
                noun = _noun_near(ctx, len(prev) + 1 + m.start()) or _noun_near(text, m.start())
                if noun:
                    q = f"How much is the {noun}?"
                    true_s = f"The {noun} costs {val}."
                    false_s = f"The {noun} costs {_close_price_alts(val, 1)[0]}."
                else:
                    q = "How much do they pay?"
                    true_s = f"They pay {val}."
                    false_s = f"They pay {_close_price_alts(val, 1)[0]}."
                add(
                    {
                        "kind": "price",
                        "correct": val,
                        "wrongs": _close_price_alts(val),
                        "question": q,
                        "explain_ru": f"Сумма в диалоге — {val}.",
                        "true_stmt": true_s,
                        "false_stmt": false_s,
                        "line_i": i,
                        "speaker": sp,
                    }
                )

        for m in labeled_num.finditer(text):
            label = " ".join(m.group(1).lower().split())
            num = " ".join(m.group(2).split())
            q = label_q.get(label) or f"What is the {label}?"
            wrongs = _alt_from_pool(num, _NUM_POOL + ["B twelve", "C", "A seventeen", "twenty-one"])
            add(
                {
                    "kind": "number",
                    "correct": num,
                    "wrongs": wrongs,
                    "question": q,
                    "explain_ru": f"В диалоге: {label} {num}.",
                    "true_stmt": f"The {label} is {num}.",
                    "false_stmt": f"The {label} is {_alt_from_pool(num, _NUM_POOL, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        for m in color_noun.finditer(text):
            color, noun = m.group(1).lower(), m.group(2).lower().rstrip("s")
            add(
                {
                    "kind": "color",
                    "correct": color,
                    "wrongs": _alt_from_pool(color, _COLOR_POOL),
                    "question": f"What colour is the {noun}?",
                    "explain_ru": f"{noun.capitalize()} — {color}.",
                    "true_stmt": f"The {noun} is {color}.",
                    "false_stmt": f"The {noun} is {_alt_from_pool(color, _COLOR_POOL, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )
        for m in noun_color.finditer(text):
            noun, color = m.group(1).lower().rstrip("s"), m.group(2).lower()
            add(
                {
                    "kind": "color",
                    "correct": color,
                    "wrongs": _alt_from_pool(color, _COLOR_POOL),
                    "question": f"What colour is the {noun}?",
                    "explain_ru": f"{noun.capitalize()} — {color}.",
                    "true_stmt": f"The {noun} is {color}.",
                    "false_stmt": f"The {noun} is {_alt_from_pool(color, _COLOR_POOL, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        tmatch = time_leave.search(text)
        if tmatch:
            raw_t = " ".join(tmatch.group(1).split()).lower()
            val = raw_t if raw_t.startswith("at") else f"at {raw_t}"
            low = text.lower()
            if "until" in low:
                q = "Until what time?"
                val = val.replace("at ", "until ", 1) if not val.startswith("until") else val
            elif any(k in low for k in ("leave", "depart", "train", "bus", "flight")):
                q = "What time does it leave?"
            elif any(k in low for k in ("meet", "see you", "appointment")):
                q = "What time do they meet?"
            elif any(k in low for k in ("start", "film", "class", "lesson", "boarding")):
                q = "What time does it start?"
            elif "open" in low and "until" not in low:
                q = "What time does it open?"
            elif "close" in low:
                q = "What time does it close?"
            elif "breakfast" in ctx.lower():
                q = "When is breakfast?"
            else:
                q = "What time do they agree on?"
            # нормализуем wrongs под until/at
            time_pool = _TIME_POOL
            if val.startswith("until"):
                time_pool = [x.replace("at ", "until ") for x in _TIME_POOL]
            add(
                {
                    "kind": "time",
                    "correct": val,
                    "wrongs": _alt_from_pool(val, time_pool),
                    "question": q,
                    "explain_ru": f"В диалоге время — {val}.",
                    "true_stmt": f"The time is {val}.",
                    "false_stmt": f"The time is {_alt_from_pool(val, time_pool, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )
        else:
            m = time_simple.search(text)
            if m:
                raw_t = " ".join(m.group(1).split()).lower()
                val = f"at {raw_t}"
                add(
                    {
                        "kind": "time",
                        "correct": val,
                        "wrongs": _alt_from_pool(val, _TIME_POOL),
                        "question": "What time do they agree on?",
                        "explain_ru": f"В диалоге время — {val}.",
                        "true_stmt": f"They agree on {val}.",
                        "false_stmt": f"They agree on {_alt_from_pool(val, _TIME_POOL, 1)[0]}.",
                        "line_i": i,
                        "speaker": sp,
                    }
                )

        m = stops_re.search(text)
        if m:
            n = m.group(1).lower()
            wrongs = [f"{x} stops" for x in _alt_from_pool(n, _NUM_POOL, 3)]
            add(
                {
                    "kind": "qty",
                    "correct": f"{n} stops",
                    "wrongs": wrongs,
                    "question": "How many stops is it?",
                    "explain_ru": f"Нужно {n} остановок.",
                    "true_stmt": f"It is {n} stops.",
                    "false_stmt": f"It is {wrongs[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )
        m = nights_re.search(text)
        if m:
            n = m.group(1).lower()
            wrongs = [f"{x} nights" for x in _alt_from_pool(n, _NUM_POOL, 3)]
            add(
                {
                    "kind": "qty",
                    "correct": f"{n} nights",
                    "wrongs": wrongs,
                    "question": "How many nights is the stay?",
                    "explain_ru": f"Бронь на {n} nights.",
                    "true_stmt": f"The stay is {n} nights.",
                    "false_stmt": f"The stay is {wrongs[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        for are in (age_re, age_re2):
            m = are.search(text)
            if not m:
                continue
            val = m.group(1).lower()
            low = f"{prev} {text}".lower()
            if "sister" in low:
                q = "How old is the sister?"
            elif "brother" in low:
                q = "How old is the brother?"
            elif "dad" in low or "father" in low:
                q = "How old is the dad?"
            elif "mum" in low or "mom" in low:
                q = "How old is the mum?"
            elif "i am" in text.lower() or "i'm" in text.lower():
                q = f"How old is {sp}?"
            else:
                q = "How old are they talking about?"
            add(
                {
                    "kind": "age",
                    "correct": val,
                    "wrongs": _alt_from_pool(val, _NUM_POOL),
                    "question": q,
                    "explain_ru": f"Возраст — {val}.",
                    "true_stmt": f"The age is {val}.",
                    "false_stmt": f"The age is {_alt_from_pool(val, _NUM_POOL, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )
            break

        m = place_re.search(text)
        if m:
            val = " ".join(m.group(1).split())
            places = [
                "Green Street",
                "King Street",
                "Hill Street",
                "Park Road",
                "Oak Avenue",
                "Park Stop",
                "Market Square",
                "the library",
                "the cinema",
                "the station",
            ]
            low = text.lower()
            if "get off" in low:
                q = "Where do they get off?"
            elif "meet" in low:
                q = "Where do they meet?"
            elif "live" in low:
                q = "Where do they live?"
            else:
                q = "Which place do they talk about?"
            add(
                {
                    "kind": "place",
                    "correct": val,
                    "wrongs": _alt_from_pool(val, places),
                    "question": q,
                    "explain_ru": f"Место — {val}.",
                    "true_stmt": f"They talk about {val}.",
                    "false_stmt": f"They talk about {_alt_from_pool(val, places, 1)[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

        m = item_order.search(text)
        if m:
            item = m.group(2).lower()
            others = [
                x
                for x in ("latte", "croissant", "sandwich", "tea", "coffee", "salad", "muffin", "brownie")
                if x != item
            ]
            random.shuffle(others)
            add(
                {
                    "kind": "item",
                    "correct": item,
                    "wrongs": others[:3],
                    "question": "What does the customer order?",
                    "explain_ru": f"Заказ — {item}.",
                    "true_stmt": f"The customer orders a {item}.",
                    "false_stmt": f"The customer orders a {others[0]}.",
                    "line_i": i,
                    "speaker": sp,
                }
            )

    by_kind: dict[str, list] = {}
    for f in facts:
        by_kind.setdefault(f["kind"], []).append(f)
    ordered: list[dict] = []
    kinds = list(by_kind.keys())
    random.shuffle(kinds)
    while any(by_kind.values()):
        for k in kinds:
            if by_kind.get(k):
                ordered.append(by_kind[k].pop(0))
    return ordered


def _derive_tasks_from_turns(turns: list[dict], n0: str, n1: str, topic: dict) -> tuple[list, list, list]:
    """
    Task1: 3 простых MCQ по деталям (цена / платформа / цвет…) — без «кто сказал».
    Task2: 3× True/False по другим фактам.
    Task3: 4 события из 12 реплик.
    """
    import re

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

    facts = _extract_detail_facts(lines, n0, n1)

    def mcq_from_fact(f: dict) -> dict:
        q = _shuffle_mcq(
            str(f["correct"]),
            list(f.get("wrongs") or []),
            str(f.get("explain_ru") or "Слушай эту деталь ещё раз."),
            None,
        )
        q["question"] = str(f["question"])
        q["options_ru"] = list(q["options"])
        return q

    if len(facts) < 3:
        for t in lines:
            if len(facts) >= 6:
                break
            m = re.search(
                r"\b((?:two|three|four|five|six|seven|eight|nine|ten|twelve|fourteen|fifteen|"
                r"seventeen|twenty|twenty-\w+|thirty|forty|fifty|\d+)\s+pounds?(?:\s+\w+)?)\b",
                t["text"],
                re.I,
            )
            if not m:
                continue
            val = " ".join(m.group(1).split())
            noun = _noun_near(t["text"], m.start()) or "ticket"
            cand = {
                "kind": "price",
                "correct": val,
                "wrongs": _close_price_alts(val),
                "question": f"How much is the {noun}?",
                "explain_ru": f"Сумма — {val}.",
                "true_stmt": f"The {noun} costs {val}.",
                "false_stmt": f"The {noun} costs {_close_price_alts(val, 1)[0]}.",
                "line_i": 0,
                "speaker": t["speaker"],
            }
            if cand["question"].lower() not in {f["question"].lower() for f in facts}:
                if val.lower() not in cand["question"].lower():
                    facts.append(cand)

    picked: list[dict] = []
    seen_kinds: set[str] = set()
    for f in facts:
        k = f.get("kind") or ""
        if k in seen_kinds and len([p for p in picked if (p.get("kind") == k)]) >= 1 and len(picked) < 2:
            continue
        if any(p["question"] == f["question"] for p in picked):
            continue
        picked.append(f)
        seen_kinds.add(k)
        if len(picked) >= 3:
            break
    for f in facts:
        if len(picked) >= 3:
            break
        if not any(p["question"] == f["question"] for p in picked):
            picked.append(f)

    while len(picked) < 3:
        picked.append(
            {
                "kind": "time",
                "correct": "at ten",
                "wrongs": ["at nine", "at eleven", "at twelve"],
                "question": "What time do they agree on?",
                "explain_ru": "Слушай время в диалоге.",
                "true_stmt": "They agree on at ten.",
                "false_stmt": "They agree on at midnight.",
            }
        )

    task1 = [mcq_from_fact(f) for f in picked[:3]]

    used_q = {f["question"] for f in picked[:3]}
    tf_facts = [f for f in facts if f.get("question") not in used_q] or list(facts)
    while len(tf_facts) < 3:
        tf_facts.append(
            {
                "true_stmt": f"The dialogue is about «{title}».",
                "false_stmt": "They only discuss a football match.",
                "explain_ru": f"Тема — «{title}».",
            }
        )

    plan = [
        (tf_facts[0], True),
        (tf_facts[1 % len(tf_facts)], False),
        (tf_facts[2 % len(tf_facts)], True),
    ]
    if plan[1][0] is plan[0][0] and len(tf_facts) > 1:
        plan[1] = (tf_facts[1], False)
    if plan[2][0] is plan[0][0] or plan[2][0] is plan[1][0]:
        for f in tf_facts:
            if f is not plan[0][0] and f is not plan[1][0]:
                plan[2] = (f, False)
                break

    task2 = []
    for fact, want_true in plan:
        if want_true:
            stmt = fact.get("true_stmt") or "This detail is in the dialogue."
            is_true = True
            explain = fact.get("explain_ru") or "Это правда по диалогу."
        else:
            stmt = fact.get("false_stmt") or "They only discuss a football match."
            is_true = False
            explain = fact.get("explain_ru") or "Этого в диалоге не было / цифра другая."
        task2.append({"statement": stmt, "is_true": is_true, "explain_ru": explain})

    events = []
    for j in (0, 3, 6, 9):
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
