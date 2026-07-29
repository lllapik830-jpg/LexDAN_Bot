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


def _clip(text: str, n: int = 70) -> str:
    t = " ".join(str(text or "").split())
    if len(t) <= n:
        return t
    cut = t[: n - 1].rsplit(" ", 1)[0]
    return (cut or t[: n - 1]).rstrip(".,;:") + "…"


def _shuffle_mcq(correct: str, wrong: list[str], explain_ru: str, options_ru: list[str] | None = None) -> dict:
    opts = [correct] + [w for w in wrong if w and w != correct][:3]
    while len(opts) < 4:
        opts.append(f"Not mentioned ({len(opts)})")
    opts = opts[:4]
    order = list(range(4))
    random.shuffle(order)
    shuffled = [opts[i] for i in order]
    correct_i = shuffled.index(correct)
    if options_ru and len(options_ru) >= 4:
        ru_map = {opts[i]: options_ru[i] for i in range(4)}
        shuffled_ru = [ru_map.get(x, x) for x in shuffled]
    else:
        shuffled_ru = list(shuffled)
    return {
        "question": "",  # заполняет вызывающий
        "options": shuffled,
        "options_ru": shuffled_ru,
        "correct": correct_i,
        "explain_wrong_ru": explain_ru,
    }


def _derive_tasks_from_turns(turns: list[dict], n0: str, n1: str, topic: dict) -> tuple[list, list, list]:
    """
    Вопросы строго из ЭТОГО диалога и с ЭТИМИ именами.
    Task1 / Task2 / Task3 не дублируют одни и те же факты.
    Не зависят от имени ElevenLabs-голоса.
    """
    title = topic.get("title_en") or topic.get("title_ru") or "the topic"
    title_ru = topic.get("title_ru") or title
    lines = [
        {"speaker": str(t.get("speaker") or n0), "text": str(t.get("text") or "").strip()}
        for t in turns
        if isinstance(t, dict) and str(t.get("text") or "").strip()
    ]
    # имена только из диалога (n0/n1) — не голоса TTS
    for i, t in enumerate(lines):
        if t["speaker"] not in {n0, n1}:
            t["speaker"] = n0 if i % 2 == 0 else n1
    while len(lines) < 4:
        lines.append({"speaker": n0 if len(lines) % 2 == 0 else n1, "text": f"Let's continue with {title}."})

    meat = [t for t in lines if len(t["text"].split()) >= 4] or lines
    # три разные реплики для task1
    early = meat[0]
    mid = meat[max(1, len(meat) // 2)]
    if mid is early and len(meat) > 1:
        mid = meat[1]
    late = meat[-1]
    if late is early or late is mid:
        late = meat[-1] if meat[-1] is not early else (meat[-2] if len(meat) > 1 else late)

    fake_lines = [
        "I need a new passport at desk three.",
        "Let's finish the math homework now.",
        "The football match starts at midnight.",
        "Please book a flight to the Moon.",
        "My password is one two three four.",
        "We should paint the kitchen green tomorrow.",
    ]
    dialogue_blob = " ".join(t["text"].lower() for t in lines)

    def _fakes(n: int) -> list[str]:
        out = []
        for f in fake_lines:
            if f.lower() not in dialogue_blob and f not in out:
                out.append(f)
            if len(out) >= n:
                break
        while len(out) < n:
            out.append(f"They only talk about space travel #{len(out)}.")
        return out

    # сторонние имена — только если не совпадают с героями диалога
    who_distract = [x for x in ("Alex", "Sam", "Teacher", "Driver", "Officer", "Pilot", "Chef") if x not in {n0, n1}]

    # --- task1 MCQ: кто сказал / какая реплика / кто ближе к концу ---
    q1 = _shuffle_mcq(
        early["speaker"],
        [x for x in (n0, n1, *who_distract) if x != early["speaker"]][:3],
        f"Эту фразу говорит {early['speaker']}.",
        None,
    )
    q1["question"] = f'Who says: "{_clip(early["text"], 64)}"?'
    q1["options_ru"] = list(q1["options"])

    real_mid = _clip(mid["text"], 56)
    distract = [_clip(f, 56) for f in _fakes(3)]
    q2 = _shuffle_mcq(
        real_mid,
        distract,
        f"В диалоге звучит: «{real_mid}».",
        None,
    )
    q2["question"] = f'Which line is from the dialogue about «{title}»?'
    q2["options_ru"] = list(q2["options"])

    q3 = _shuffle_mcq(
        late["speaker"],
        [x for x in (n0, n1, *who_distract) if x != late["speaker"]][:3],
        f"Ближе к концу говорит {late['speaker']}.",
        None,
    )
    q3["question"] = f'Near the end, who says: "{_clip(late["text"], 64)}"?'
    q3["options_ru"] = list(q3["options"])

    task1 = [q1, q2, q3]

    # --- task2 True/False: другие факты, не копия early из task1 ---
    tf_line = None
    for t in meat:
        if t is not early and t is not late and t["text"] != early["text"]:
            tf_line = t
            break
    if tf_line is None:
        tf_line = mid if mid is not early else (late if late is not early else meat[min(1, len(meat) - 1)])

    is_passport = any(k in _topic_blob(topic) for k in ("passport", "immigration", "миграц"))
    wrong_topic = (
        f"{n0} and {n1} only discuss football scores."
        if is_passport
        else f"{n0} and {n1} only discuss a passport desk."
    )
    # ложное утверждение про чужую реплику
    other = n1 if tf_line["speaker"] == n0 else n0
    task2 = [
        {
            "statement": f'{tf_line["speaker"]} says: "{_clip(tf_line["text"], 50)}"',
            "is_true": True,
            "explain_ru": f"Да, именно {tf_line['speaker']} говорит это в диалоге.",
        },
        {
            "statement": f'{other} says: "{_clip(tf_line["text"], 50)}"',
            "is_true": False,
            "explain_ru": f"Нет, эту реплику говорит {tf_line['speaker']}, не {other}.",
        },
        {
            "statement": wrong_topic,
            "is_true": False,
            "explain_ru": f"Нет, разговор про «{title_ru}».",
        },
    ]

    # --- task3 chronology: подряд идущие реплики обоих говорящих ---
    events = [f"{t['speaker']}: {_clip(t['text'], 40)}" for t in lines[:4]]
    while len(events) < 4:
        t = lines[len(events) % len(lines)]
        events.append(f"{t['speaker']}: {_clip(t['text'], 40)}")

    return task1, task2, events[:4]


def _fallback_dialogue_turns(topic: dict, n0: str, n1: str) -> list[tuple[str, str]]:
    """Уникальный запасной диалог под тему (имена = n0/n1)."""
    title = topic.get("title_en") or topic.get("title_ru") or "this topic"
    setting = topic.get("setting") or title
    tid = str(topic.get("id") or "")

    # явные id — самые частые жалобы
    by_id = {
        "hello": [
            (n0, "Hi! What's your name?"),
            (n1, f"Hello! My name is {n1}. Nice to meet you."),
            (n0, f"Nice to meet you, {n1}. I'm {n0}."),
            (n1, "Are you a new student here?"),
            (n0, "Yes. This is my first day."),
            (n1, "Welcome! Do you like the school?"),
            (n0, "Yes, I like it. It's friendly."),
            (n1, "Great. See you in class!"),
        ],
        "cafe_simple": [
            (n0, "Good morning! What can I get you?"),
            (n1, "A latte and a croissant, please."),
            (n0, "For here or to go?"),
            (n1, "To go, please."),
            (n0, "Anything else? We have muffins."),
            (n1, "No, that's all. How much is it?"),
            (n0, "Four pounds fifty."),
            (n1, "Here you are. Thanks!"),
        ],
        "food_words": [
            (n0, "Hi! What would you like to eat?"),
            (n1, "An apple and a sandwich, please."),
            (n0, "Tea or water with that?"),
            (n1, "Water, please. How much is it?"),
            (n0, "Five pounds altogether."),
            (n1, "Can I also get bread?"),
            (n0, "Sure. Here you are."),
            (n1, "Thank you! It looks good."),
        ],
        "police": [
            (n0, "Good afternoon. How can I help you?"),
            (n1, "I lost my wallet this morning."),
            (n0, "Where did you lose it?"),
            (n1, "Near the bus stop on Green Street."),
            (n0, "What colour is the wallet?"),
            (n1, "It's black, with my ID card inside."),
            (n0, "Please fill in this form."),
            (n1, "Okay. Thank you, officer."),
        ],
        "numbers": [
            (n0, "Excuse me. What is your phone number?"),
            (n1, "It's zero seven seven zero zero one two."),
            (n0, "And how old are you?"),
            (n1, "I am twenty years old."),
            (n0, "Okay. I will write it down."),
            (n1, "Do you need my name too?"),
            (n0, f"Yes, please. Your name is {n1}, right?"),
            (n1, "Yes, that's right. Thank you."),
        ],
        "family": [
            (n0, "Who is in your family?"),
            (n1, "My mum, my dad, and my sister."),
            (n0, "How old is your sister?"),
            (n1, "She is ten."),
            (n0, "Does your dad work?"),
            (n1, "Yes, he works in a shop."),
            (n0, "And your mum?"),
            (n1, "My mum is a teacher."),
        ],
        "school": [
            (n0, "What class do you have now?"),
            (n1, "English, then a break."),
            (n0, "Do you have homework today?"),
            (n1, "Yes, ten new words."),
            (n0, "Want to study together after school?"),
            (n1, "Good idea. At the library?"),
            (n0, "Yes. See you at four."),
            (n1, "Okay, see you!"),
        ],
        "bus": [
            (n0, "One ticket to the centre, please."),
            (n1, "That's two pounds. Next stop is Market Street."),
            (n0, "Where do I get off for the museum?"),
            (n1, "Get off at Park Stop."),
            (n0, "How many stops is that?"),
            (n1, "Three stops from here."),
            (n0, "Thank you, driver."),
            (n1, "You're welcome. Hold the rail."),
        ],
        "doctor": [
            (n0, "What seems to be the problem?"),
            (n1, "I have a sore throat and a fever."),
            (n0, "How long have you felt like this?"),
            (n1, "Since yesterday morning."),
            (n0, "I'll give you medicine and rest advice."),
            (n1, "Should I stay home from work?"),
            (n0, "Yes, rest for two days."),
            (n1, "Thank you, doctor."),
        ],
        "hotel": [
            (n0, "Good evening. Do you have a reservation?"),
            (n1, "Yes, a room for two nights."),
            (n0, "Breakfast is from seven to ten."),
            (n1, "Is the Wi-Fi free?"),
            (n0, "Yes. Your room is 214."),
            (n1, "Where is the lift?"),
            (n0, "On the left, past reception."),
            (n1, "Perfect, thank you."),
        ],
        "job_interview": [
            (n0, "Tell me about your experience."),
            (n1, "I worked in sales for three years."),
            (n0, "Can you start next Monday?"),
            (n1, "Yes, that works for me."),
            (n0, "The hours are nine to five."),
            (n1, "Do you offer remote days?"),
            (n0, "One remote day per week."),
            (n1, "Great. I'm interested in the role."),
        ],
    }
    if tid in by_id:
        return by_id[tid]

    # Не шарим шаблоны между темами по ключевым словам (из‑за этого путались имена/сюжеты).
    # Для остальных id — уникальный диалог из title/setting.
    roles = str(topic.get("roles") or "two people")
    detail = setting if setting != title else roles
    return [
        (n0, f"Hello! Let's focus on {title} today."),
        (n1, f"Sure. I came because of {detail}."),
        (n0, f"What do you need most regarding {title}?"),
        (n1, f"Clear steps and a simple plan for {detail}."),
        (n0, "Alright. I can explain it step by step."),
        (n1, "Can we start with the first step now?"),
        (n0, f"Yes. First we clarify {detail}."),
        (n1, f"Great. Thanks for helping with {title}!"),
    ]


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
                    "FORBIDDEN: invent a different situation (e.g. passport desk) "
                    "unless the topic itself is about that.\n"
                    f"turns: exactly 8 {{speaker,text}}. speaker = one of the two names. {pace}\n"
                    "task1/task2/task3_events: include them, but they will be rebuilt from the dialogue.\n"
                    f"CEFR level: {level}."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level:{level}\nTopic EN:{title_en}\nTopic RU:{title_ru}\n"
                    f"Roles:{roles}\nSetting:{setting}\n"
                    f"Write ONLY about this topic. Seed:{random.random()}"
                ),
            },
        ],
        fallback,
        temperature=0.45,
        max_tokens=1600,
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
    if not (isinstance(turns, list) and len(turns) >= 6):
        return fallback
    sp0 = speakers[0] if isinstance(speakers[0], dict) else {"name": "Ben", "gender": "male"}
    sp1 = speakers[1] if isinstance(speakers[1], dict) else {"name": "Mia", "gender": "female"}
    n0 = str(sp0.get("name") or "Ben").strip() or "Ben"
    n1 = str(sp1.get("name") or "Mia").strip() or "Mia"
    if n0.lower() == n1.lower():
        n1 = "Mia" if n0.lower() != "mia" else "Emma"
    clean_turns = []
    for t in turns[:8]:
        if not isinstance(t, dict):
            continue
        sp = str(t.get("speaker") or n0).strip()
        if sp not in {n0, n1}:
            # частый баг GPT: имя голоса / чужое имя
            low = sp.lower()
            if low in {n0.lower(), n1.lower()}:
                sp = n0 if low == n0.lower() else n1
            else:
                sp = n0 if len(clean_turns) % 2 == 0 else n1
        text = str(t.get("text") or "").strip()
        if text:
            clean_turns.append({"speaker": sp, "text": text})
    while len(clean_turns) < 8:
        clean_turns.append(
            {"speaker": n0 if len(clean_turns) % 2 == 0 else n1, "text": "Okay, I understand."}
        )
    clean_turns = clean_turns[:8]

    # Задания здесь временные — generate_listening_pack пересоберёт из turns
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
