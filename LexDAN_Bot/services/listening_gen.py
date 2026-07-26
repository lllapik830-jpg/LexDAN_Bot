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
        "key": "kristen",
        "name": "Kristen",
        "gender": "female",
        "voice_id": "OIadkU6YLviNhuekXGly",
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
    if sit_tags & {"service", "sales", "waiter", "consultant"} and key in {"alex", "kristen"}:
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


def _fallback_pack(level: str, topic: dict) -> dict:
    roles = topic.get("roles") or "two people"
    return {
        "speakers": [
            {"name": "David", "gender": "male", "role": roles.split(" and ")[0] if " and " in roles else "person A"},
            {"name": "Emily", "gender": "female", "role": roles.split(" and ")[-1] if " and " in roles else "person B"},
        ],
        "turns": [
            {"speaker": "David", "text": "Good afternoon. How can I help you today?"},
            {"speaker": "Emily", "text": "Hi. I need some help with this, please."},
            {"speaker": "David", "text": "Of course. Can you tell me what happened?"},
            {"speaker": "Emily", "text": "Sure. It started this morning around nine."},
            {"speaker": "David", "text": "Alright. Do you have your document with you?"},
            {"speaker": "Emily", "text": "Yes, here it is. I also brought my passport."},
            {"speaker": "David", "text": "Perfect. Please wait five minutes at desk three."},
            {"speaker": "Emily", "text": "Thank you. I'll wait there."},
        ],
        "task1": [
            {
                "question": "What time did Emily's problem start?",
                "options": ["At seven", "At eight", "At nine", "At ten"],
                "correct": 2,
                "explain_wrong_ru": "Эмили сказала, что всё началось около девяти утра.",
                "options_ru": ["В семь", "В восемь", "В девять", "В десять"],
            },
            {
                "question": "What extra document did Emily bring?",
                "options": ["A ticket", "A passport", "A map", "A photo"],
                "correct": 1,
                "explain_wrong_ru": "Эмили сказала, что принесла ещё паспорт.",
                "options_ru": ["Билет", "Паспорт", "Карту", "Фото"],
            },
            {
                "question": "Where should Emily wait?",
                "options": ["Desk one", "Desk two", "Desk three", "Outside"],
                "correct": 2,
                "explain_wrong_ru": "Дэвид попросил подождать у стойки номер три.",
                "options_ru": ["Стойка 1", "Стойка 2", "Стойка 3", "Снаружи"],
            },
        ],
        "task2": [
            {
                "statement": "Emily asked for help in the evening.",
                "is_true": False,
                "explain_ru": "Разговор днём (Good afternoon), а проблема началась утром.",
            },
            {
                "statement": "David asked Emily to wait five minutes.",
                "is_true": True,
                "explain_ru": "Дэвид сказал подождать пять минут у стойки три.",
            },
            {
                "statement": "Emily forgot her passport.",
                "is_true": False,
                "explain_ru": "Эмили как раз сказала, что паспорт с собой.",
            },
        ],
        "task3_events": [
            "David offers to help",
            "Emily explains the morning problem",
            "Emily shows her passport",
            "David asks her to wait at desk three",
        ],
    }


def generate_listening_pack(level: str, topic: dict) -> dict:
    from services.gpt import _ask_json

    fallback = _fallback_pack(level, topic)
    setting = topic.get("setting") or topic.get("title_en") or "everyday situation"
    roles = topic.get("roles") or "two people in a realistic situation"
    pace = _pace_hint(level)
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Create CEFR listening practice JSON for Russian learners. ONLY JSON.\n"
                    "Keys: speakers, turns, task1, task2, task3_events.\n"
                    "speakers: exactly 2 {name, gender:male|female, role}. Names fit the roles "
                    "(e.g. officer/citizen, bartender/guest, doctor/patient) — NOT always friends.\n"
                    f"turns: exactly 8 {{speaker,text}}. {pace} Setting: {setting}. Roles: {roles}.\n"
                    "task1: 3 MCQs {question, options[4], correct(0-3), explain_wrong_ru, options_ru[4]}.\n"
                    "  Questions = listening comprehension (facts from dialogue). NOT grammar.\n"
                    "  options_ru = Russian translations of the 4 options in the same order.\n"
                    "  explain_wrong_ru = short Russian explanation if student picks wrong.\n"
                    "task2: 3 TRUE/FALSE {statement, is_true, explain_ru}.\n"
                    "  CRITICAL: task2 must test DIFFERENT facts than task1 — no paraphrases of the same 3 questions.\n"
                    "  Mix true and false. Statements about details NOT asked in task1.\n"
                    "task3_events: 4 short English event phrases in correct chronology.\n"
                    f"CEFR level: {level}."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level:{level}\nTopic:{topic.get('title_en')} / {topic.get('title_ru')}\n"
                    f"Roles:{roles}\nSetting:{setting}\nSeed:{random.random()}"
                ),
            },
        ],
        fallback,
        temperature=0.6,
        max_tokens=1600,
    )
    pack = _normalize_pack(data, fallback)
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
    # пронумерованные реплики — подпись = имя голоса + номер (Jessa 1, Alex 3)
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
