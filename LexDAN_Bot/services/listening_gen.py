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


def _fallback_pack(level: str, topic: dict) -> dict:
    """Запасной диалог строго по теме (не универсальный «паспорт»)."""
    roles = topic.get("roles") or "two people"
    title = topic.get("title_en") or topic.get("title_ru") or "Topic"
    setting = topic.get("setting") or title
    blob = _topic_blob(topic)
    role_a = roles.split(" and ")[0].strip() if " and " in roles else "Alex"
    role_b = roles.split(" and ")[-1].strip() if " and " in roles else "Sam"

    # шаблоны по категориям
    if any(k in blob for k in ("food", "еда", "cafe", "coffee", "restaurant", "snack", "apple", "bread")):
        turns = [
            ("Alex", "Hi! What would you like to eat today?"),
            ("Sam", "I'd like an apple and a sandwich, please."),
            ("Alex", "Sure. Do you want tea or water with that?"),
            ("Sam", "Water, please. How much is it?"),
            ("Alex", "It's five pounds altogether."),
            ("Sam", "Okay. Can I also get a small cake?"),
            ("Alex", "Of course. Here you are."),
            ("Sam", "Thank you! This looks delicious."),
        ]
        t1 = [
            {"question": "What does Sam order first?", "options": ["Soup", "An apple and a sandwich", "Only tea", "Pizza"], "correct": 1, "explain_wrong_ru": "Сэм заказал яблоко и сэндвич.", "options_ru": ["Суп", "Яблоко и сэндвич", "Только чай", "Пиццу"]},
            {"question": "What drink does Sam choose?", "options": ["Tea", "Coffee", "Water", "Juice"], "correct": 2, "explain_wrong_ru": "Сэм попросил воду.", "options_ru": ["Чай", "Кофе", "Воду", "Сок"]},
            {"question": "How much is the food?", "options": ["Two pounds", "Five pounds", "Ten pounds", "Free"], "correct": 1, "explain_wrong_ru": "Алекс сказал: пять фунтов.", "options_ru": ["2 фунта", "5 фунтов", "10 фунтов", "Бесплатно"]},
        ]
        t2 = [
            {"statement": "Sam orders pizza.", "is_true": False, "explain_ru": "Сэм заказал яблоко, сэндвич и потом торт — не пиццу."},
            {"statement": "Alex offers tea or water.", "is_true": True, "explain_ru": "Алекс спросил: чай или вода."},
            {"statement": "Sam also asks for a small cake.", "is_true": True, "explain_ru": "В конце Сэм попросил ещё маленький торт."},
        ]
        events = ["Alex greets the guest", "Sam orders apple and sandwich", "Sam chooses water", "Sam asks for a cake"]
    elif any(k in blob for k in ("cafe", "barista", "кофе")):
        turns = [
            ("Alex", "Good morning! What can I get you?"),
            ("Sam", "A latte and a croissant, please."),
            ("Alex", "Sure. For here or to go?"),
            ("Sam", "To go, please."),
            ("Alex", "Anything else? We have muffins too."),
            ("Sam", "No, that's all. How much is it?"),
            ("Alex", "Four pounds fifty."),
            ("Sam", "Here you are. Thanks!"),
        ]
        t1 = [
            {"question": "What drink does Sam order?", "options": ["Tea", "Latte", "Water", "Juice"], "correct": 1, "explain_wrong_ru": "Сэм заказал латте.", "options_ru": ["Чай", "Латте", "Воду", "Сок"]},
            {"question": "Is the order for here or to go?", "options": ["For here", "To go", "Both", "Not said"], "correct": 1, "explain_wrong_ru": "Сэм сказал «to go».", "options_ru": ["Здесь", "С собой", "И то и то", "Не сказано"]},
            {"question": "How much does it cost?", "options": ["£2", "£4.50", "£10", "Free"], "correct": 1, "explain_wrong_ru": "Цена — four pounds fifty.", "options_ru": ["2£", "4.50£", "10£", "Бесплатно"]},
        ]
        t2 = [
            {"statement": "Sam wants a muffin.", "is_true": False, "explain_ru": "Сэм отказался от маффинов."},
            {"statement": "Alex offers muffins.", "is_true": True, "explain_ru": "Бариста предложил маффины."},
            {"statement": "Sam orders a croissant.", "is_true": True, "explain_ru": "Да, латте и круассан."},
        ]
        events = ["Alex greets customer", "Sam orders latte and croissant", "Sam chooses to go", "Sam pays"]
    elif any(k in blob for k in ("police", "полиц", "wallet")):
        turns = [
            ("Alex", "Good afternoon. How can I help you?"),
            ("Sam", "I lost my wallet this morning."),
            ("Alex", "Where did you lose it?"),
            ("Sam", "Near the bus stop on Green Street."),
            ("Alex", "What colour is the wallet?"),
            ("Sam", "It's black, with my ID card inside."),
            ("Alex", "Alright. Please fill in this form."),
            ("Sam", "Okay. Thank you, officer."),
        ]
        t1 = [
            {"question": "What did Sam lose?", "options": ["Phone", "Keys", "Wallet", "Bag"], "correct": 2, "explain_wrong_ru": "Сэм потерял кошелёк.", "options_ru": ["Телефон", "Ключи", "Кошелёк", "Сумку"]},
            {"question": "Where was it lost?", "options": ["In a shop", "Near a bus stop", "At home", "At school"], "correct": 1, "explain_wrong_ru": "Около автобусной остановки.", "options_ru": ["В магазине", "У остановки", "Дома", "В школе"]},
            {"question": "What colour is the wallet?", "options": ["Red", "Blue", "Black", "Brown"], "correct": 2, "explain_wrong_ru": "Кошелёк чёрный.", "options_ru": ["Красный", "Синий", "Чёрный", "Коричневый"]},
        ]
        t2 = [
            {"statement": "Sam lost a phone.", "is_true": False, "explain_ru": "Потерян кошелёк, не телефон."},
            {"statement": "There is an ID card in the wallet.", "is_true": True, "explain_ru": "Сэм сказал, что внутри ID."},
            {"statement": "The officer asks Sam to fill a form.", "is_true": True, "explain_ru": "Офицер попросил заполнить форму."},
        ]
        events = ["Officer offers help", "Sam reports lost wallet", "Sam describes colour", "Sam fills the form"]
    else:
        # универсальный шаблон из setting — без паспорта
        turns = [
            ("Alex", f"Hello! Let's talk about {title}."),
            ("Sam", f"Sure. I'm here about {setting}."),
            ("Alex", "Okay. What do you need today?"),
            ("Sam", "I need a little help, please."),
            ("Alex", "No problem. Can you tell me more?"),
            ("Sam", "Yes. It is important for me."),
            ("Alex", "Alright. We can do it step by step."),
            ("Sam", "Great, thank you so much!"),
        ]
        t1 = [
            {"question": f"What is the dialogue mainly about?", "options": [title, "Sports only", "A passport office", "Math homework"], "correct": 0, "explain_wrong_ru": f"Тема разговора — {title}.", "options_ru": [str(topic.get("title_ru") or title), "Только спорт", "Паспортный стол", "Домашка по математике"]},
            {"question": "Does Sam ask for help?", "options": ["Yes", "No", "Maybe later", "Not clear"], "correct": 0, "explain_wrong_ru": "Сэм просит помощи.", "options_ru": ["Да", "Нет", "Позже", "Неясно"]},
            {"question": "How does Alex want to proceed?", "options": ["Step by step", "Never", "Tomorrow only", "By email only"], "correct": 0, "explain_wrong_ru": "Алекс предлагает шаг за шагом.", "options_ru": ["Шаг за шагом", "Никогда", "Только завтра", "Только по почте"]},
        ]
        t2 = [
            {"statement": "The speakers talk about a passport desk.", "is_true": False, "explain_ru": f"Диалог про «{title}», не про паспортный стол."},
            {"statement": "Alex offers to help.", "is_true": True, "explain_ru": "Алекс готов помочь."},
            {"statement": "Sam says thank you at the end.", "is_true": True, "explain_ru": "В конце Сэм благодарит."},
        ]
        events = ["Alex greets Sam", "Sam explains the need", "Alex offers step-by-step help", "Sam thanks Alex"]

    return {
        "speakers": [
            {"name": "Alex", "gender": "male", "role": role_a},
            {"name": "Sam", "gender": "female", "role": role_b},
        ],
        "turns": [{"speaker": a, "text": b} for a, b in turns],
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
                    "speakers: exactly 2 {name, gender:male|female, role}. Names fit the roles.\n"
                    f"CRITICAL TOPIC LOCK: The WHOLE dialogue MUST be about «{title_en}» / «{title_ru}».\n"
                    f"Setting: {setting}. Roles: {roles}.\n"
                    f"Use these topic words naturally: {must}.\n"
                    "FORBIDDEN: invent a different situation (e.g. passport desk, documents, immigration) "
                    "unless the topic itself is about that.\n"
                    f"turns: exactly 8 {{speaker,text}}. {pace}\n"
                    "task1: 3 MCQs {question, options[4], correct(0-3), explain_wrong_ru, options_ru[4]} "
                    "ONLY about facts from THIS dialogue.\n"
                    "task2: 3 TRUE/FALSE {statement, is_true, explain_ru} about DIFFERENT facts than task1.\n"
                    "task3_events: 4 short English event phrases in correct chronology from THIS dialogue.\n"
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

    sp = pack["speakers"]
    g0 = (sp[0].get("gender") or "male").lower()
    g1 = (sp[1].get("gender") or "female").lower()
    if g0 not in {"male", "female"}:
        g0 = "male"
    if g1 not in {"male", "female"}:
        g1 = "female"
    v0, v1 = _pick_voices(g0, g1, level=level, topic=topic, roles=roles, setting=setting)
    voice_map = {sp[0]["name"]: v0, sp[1]["name"]: v1}
    pack["voice_map"] = {
        name: {"key": v["key"], "voice_id": v["voice_id"], "voice_name": v["name"]}
        for name, v in voice_map.items()
    }
    numbered = []
    for i, t in enumerate(pack["turns"], start=1):
        vinfo = pack["voice_map"].get(t["speaker"]) or {}
        voice_name = vinfo.get("voice_name") or t["speaker"]
        numbered.append(
            {
                "n": i,
                "speaker": t["speaker"],
                "text": t["text"],
                "label": f"{voice_name} {i}",
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
    task1 = data.get("task1")
    task2 = data.get("task2")
    events = data.get("task3_events")
    if not (isinstance(speakers, list) and len(speakers) >= 2):
        return fallback
    if not (isinstance(turns, list) and len(turns) >= 6):
        return fallback
    sp0 = speakers[0] if isinstance(speakers[0], dict) else {"name": "David", "gender": "male"}
    sp1 = speakers[1] if isinstance(speakers[1], dict) else {"name": "Emily", "gender": "female"}
    n0 = str(sp0.get("name") or "David").strip() or "David"
    n1 = str(sp1.get("name") or "Emily").strip() or "Emily"
    clean_turns = []
    for t in turns[:8]:
        if not isinstance(t, dict):
            continue
        sp = str(t.get("speaker") or n0).strip()
        if sp not in {n0, n1}:
            sp = n0 if len(clean_turns) % 2 == 0 else n1
        text = str(t.get("text") or "").strip()
        if text:
            clean_turns.append({"speaker": sp, "text": text})
    while len(clean_turns) < 8:
        clean_turns.append(
            {"speaker": n0 if len(clean_turns) % 2 == 0 else n1, "text": "Okay, I understand."}
        )
    clean_turns = clean_turns[:8]

    def _mcq(items, fb):
        out = []
        src = items if isinstance(items, list) else []
        for i in range(3):
            raw = src[i] if i < len(src) and isinstance(src[i], dict) else fb[i]
            opts = list(raw.get("options") or fb[i]["options"])[:4]
            while len(opts) < 4:
                opts.append(f"Option {len(opts)+1}")
            opts_ru = list(raw.get("options_ru") or fb[i].get("options_ru") or opts)[:4]
            while len(opts_ru) < 4:
                opts_ru.append(opts[len(opts_ru)])
            try:
                correct = int(raw.get("correct", fb[i]["correct"]))
            except (TypeError, ValueError):
                correct = fb[i]["correct"]
            correct = max(0, min(3, correct))
            out.append(
                {
                    "question": str(raw.get("question") or fb[i]["question"]).strip(),
                    "options": [str(o).strip() for o in opts],
                    "options_ru": [str(o).strip() for o in opts_ru],
                    "correct": correct,
                    "explain_wrong_ru": str(
                        raw.get("explain_wrong_ru") or fb[i].get("explain_wrong_ru") or ""
                    ).strip(),
                }
            )
        return out

    def _tf(items, fb):
        out = []
        src = items if isinstance(items, list) else []
        for i in range(3):
            raw = src[i] if i < len(src) and isinstance(src[i], dict) else fb[i]
            out.append(
                {
                    "statement": str(raw.get("statement") or fb[i]["statement"]).strip(),
                    "is_true": bool(raw.get("is_true", fb[i]["is_true"])),
                    "explain_ru": str(raw.get("explain_ru") or fb[i]["explain_ru"]).strip(),
                }
            )
        return out

    ev = [str(x).strip() for x in (events or []) if str(x).strip()]
    if len(ev) < 4:
        ev = list(fallback["task3_events"])
    ev = ev[:4]

    return {
        "speakers": [
            {"name": n0, "gender": str(sp0.get("gender") or "male"), "role": str(sp0.get("role") or "")},
            {"name": n1, "gender": str(sp1.get("gender") or "female"), "role": str(sp1.get("role") or "")},
        ],
        "turns": clean_turns,
        "task1": _mcq(task1, fallback["task1"]),
        "task2": _tf(task2, fallback["task2"]),
        "task3_events": ev,
    }
