"""
Секретные задания Рико (награды за серию дней).
"""

from __future__ import annotations

import logging
import random

from services.growth import ensure_growth, grant_safe
from services.rewards import set_grammar_cap_today

MISSION_WEEK = "week_review"
MISSION_VOICE = "voice_day"

MISSION_META = {
    MISSION_WEEK: {
        "title": "📝 Разбор твоей недели",
        "blurb": (
            "Рико разберёт типичные ошибки твоего уровня (и твои фразы из чата, если они есть) "
            "и даст 5 правок «как сказал бы носитель»."
        ),
        "mins": "7–10 мин",
        "intro": (
            "🦜 <b>Рико:</b> Ого, секрет открыт! Давай разберём неделю.\n\n"
            "Я покажу 5 ситуаций: как часто говорят ученики → как звучит естественнее → "
            "короткий совет на русском. Читай, запоминай, жми «Далее».\n\n"
            "Готов? Поехали 👇"
        ),
    },
    MISSION_VOICE: {
        "title": "🗣 Голос дня",
        "blurb": (
            "4 живые фразы под твой уровень — каждая озвучена разным акцентом "
            "(наши голоса: Adam, British, American, Australian). "
            "Скажи голосом или текстом — Рико подскажет, как естественнее."
        ),
        "mins": "5–8 мин",
        "intro": (
            "🦜 <b>Рико:</b> Голос — это мышца. Сейчас 4 короткие фразы.\n\n"
            "Каждую озвучу <b>другим акцентом</b> из нашей коллекции — "
            "слушай → повтори в микрофон (или напиши).\n"
            "Я скажу, что услышал и как можно естественнее.\n\n"
            "Можно «Пропустить фразу». Погнали 🗣"
        ),
    },
}

BTN_SECRET = "🔐 Секрет Рико"
BTN_SECRET_WEEK = "📝 Разбор недели"
BTN_SECRET_VOICE = "🗣 Голос дня"
BTN_SECRET_SKIP = "⏭ Пропустить фразу"
BTN_SECRET_DONE = "✅ Готово"


def ensure_missions(user: dict) -> dict:
    ensure_growth(user)
    if "secret_missions" not in user or not isinstance(user["secret_missions"], dict):
        user["secret_missions"] = {"inbox": [], "active": None, "done": []}
    sm = user["secret_missions"]
    sm.setdefault("inbox", [])
    sm.setdefault("active", None)
    sm.setdefault("done", [])
    return sm


def unlock_mission(user: dict, mission_id: str) -> bool:
    """Добавить миссию в inbox (можно несколько одинаковых за разные streak-ступени)."""
    sm = ensure_missions(user)
    if mission_id not in MISSION_META:
        return False
    sm["inbox"].append(mission_id)
    user["pending_secret_rico"] = True
    return True


def has_secret_entry(user: dict) -> bool:
    sm = ensure_missions(user)
    return bool(sm["inbox"]) or bool(sm.get("active"))


def inbox_missions(user: dict) -> list[str]:
    """Уникальные id в порядке появления (для кнопок хаба)."""
    seen: list[str] = []
    for mid in ensure_missions(user).get("inbox") or []:
        if mid not in seen:
            seen.append(mid)
    return seen


def get_active(user: dict) -> dict | None:
    return ensure_missions(user).get("active")


def clear_active(user: dict) -> None:
    sm = ensure_missions(user)
    sm["active"] = None
    user["pending_secret_rico"] = bool(sm["inbox"])


def start_mission(user: dict, mission_id: str) -> dict | None:
    sm = ensure_missions(user)
    inbox = list(sm.get("inbox") or [])
    if mission_id not in inbox:
        return None
    inbox.remove(mission_id)  # только один экземпляр
    sm["inbox"] = inbox
    if mission_id == MISSION_WEEK:
        cards = build_week_review(user)
        if not cards:
            cards = _fallback_week_cards(user.get("level") or "A1")
        sm["active"] = {
            "type": MISSION_WEEK,
            "step": 0,
            "cards": cards,
            "intro_sent": False,
        }
    elif mission_id == MISSION_VOICE:
        phrases = build_voice_phrases(user)
        if not phrases or len(phrases) < 4:
            phrases = _fallback_voice_phrases(user.get("level") or "A1")
        items = attach_accent_tour(phrases[:4], user)
        sm["active"] = {
            "type": MISSION_VOICE,
            "step": 0,
            "phrases": items,
            "notes": [],
            "intro_sent": False,
        }
    else:
        return None
    user["pending_secret_rico"] = True
    return sm["active"]


def complete_mission(user: dict) -> str:
    """Завершить активную миссию, выдать награду."""
    sm = ensure_missions(user)
    active = sm.get("active") or {}
    mtype = active.get("type") or ""
    sm["done"] = list(sm.get("done") or []) + [mtype]
    sm["active"] = None
    user["pending_secret_rico"] = bool(sm["inbox"])

    set_grammar_cap_today(user, 24)
    grant_safe(user, 1)
    title = MISSION_META.get(mtype, {}).get("title", "Секрет")
    return (
        f"🏆 <b>Секрет выполнен:</b> {title}\n\n"
        "Награда:\n"
        "• сегодня до <b>24</b> баллов на уроки (Grammar + Vocab)\n"
        "• <b>+1</b> стрик-сейф 🛡️\n\n"
        "Рико гордится тобой. Завтра — снова ~15 минут 💪"
    )


def mission_intro(mission_id: str) -> str:
    return (MISSION_META.get(mission_id) or {}).get("intro") or ""


def build_week_review(user: dict) -> list[dict]:
    """5 карточек правок на основе недавнего чата / уровня."""
    level = user.get("level") or "A1"
    turns = user.get("chat_recent_turns") or []
    user_lines = [
        t.get("text") or ""
        for t in turns
        if t.get("role") == "user" and (t.get("text") or "").strip()
    ][-8:]
    sample = "\n".join(f"- {x}" for x in user_lines) if user_lines else "(мало сообщений в чате)"

    from services.gpt import _ask_json

    fallback = _fallback_week_cards(level)
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "You are Rico, warm English tutor for Russian students. "
                    "Return ONLY JSON: {\"cards\":[{\"wrong\":\"...\",\"better\":\"...\","
                    "\"tip_ru\":\"...\"}]} with exactly 5 cards. "
                    "Prefer mistakes from the student's lines; if few lines, use typical "
                    f"CEFR {level} mistakes for Russian speakers. "
                    "wrong/better in English, tip_ru in Russian, concrete and short."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"CEFR level: {level}\nRecent student English:\n{sample}\n"
                    "Make 5 personal native-style corrections."
                ),
            },
        ],
        {"cards": fallback},
        temperature=0.4,
        max_tokens=700,
    )
    cards = data.get("cards") if isinstance(data, dict) else None
    if not isinstance(cards, list) or len(cards) < 3:
        return fallback
    out = []
    for c in cards[:5]:
        if not isinstance(c, dict):
            continue
        wrong = str(c.get("wrong") or "").strip()
        better = str(c.get("better") or "").strip()
        tip = str(c.get("tip_ru") or "").strip()
        if better:
            out.append({"wrong": wrong or "—", "better": better, "tip_ru": tip})
    while len(out) < 5:
        out.append(fallback[len(out) % len(fallback)])
    return out[:5]


def _fallback_week_cards(level: str) -> list[dict]:
    by_level = {
        "A0": [
            {
                "wrong": "I is student",
                "better": "I am a student",
                "tip_ru": "I → am. Перед профессией часто нужен a/an.",
            },
            {
                "wrong": "She have a cat",
                "better": "She has a cat",
                "tip_ru": "he/she/it → has, не have.",
            },
            {
                "wrong": "I go school",
                "better": "I go to school",
                "tip_ru": "go to school — предлог to обязателен.",
            },
            {
                "wrong": "My name Dan",
                "better": "My name is Dan",
                "tip_ru": "Нужна связка is: My name is…",
            },
            {
                "wrong": "I like very much pizza",
                "better": "I like pizza very much",
                "tip_ru": "very much обычно в конце, не перед существительным.",
            },
        ],
        "A1": [
            {
                "wrong": "I go to school yesterday",
                "better": "I went to school yesterday",
                "tip_ru": "Вчера → Past Simple: go → went.",
            },
            {
                "wrong": "She don't like coffee",
                "better": "She doesn't like coffee",
                "tip_ru": "he/she/it → doesn't, не don't.",
            },
            {
                "wrong": "I am agree with you",
                "better": "I agree with you",
                "tip_ru": "agree — без am (это не continuous).",
            },
            {
                "wrong": "How you say this?",
                "better": "How do you say this?",
                "tip_ru": "В вопросе нужен Do/Does: How do you…?",
            },
            {
                "wrong": "I very like it",
                "better": "I really like it / I like it a lot",
                "tip_ru": "Не very like — really или a lot.",
            },
        ],
        "A2": [
            {
                "wrong": "I have seen him yesterday",
                "better": "I saw him yesterday",
                "tip_ru": "С yesterday — Past Simple, не Present Perfect.",
            },
            {
                "wrong": "If I will see her, I tell you",
                "better": "If I see her, I'll tell you",
                "tip_ru": "В if-условии обычно Present, will — в результате.",
            },
            {
                "wrong": "I interested in music",
                "better": "I'm interested in music",
                "tip_ru": "interested нуждается в be: I'm interested.",
            },
            {
                "wrong": "He suggested me to go",
                "better": "He suggested that I go / He suggested going",
                "tip_ru": "suggest не берёт me to — другая конструкция.",
            },
            {
                "wrong": "Despite of the rain…",
                "better": "Despite the rain… / In spite of the rain…",
                "tip_ru": "despite без of; in spite of — с of.",
            },
        ],
    }
    if level in {"A0"}:
        return by_level["A0"]
    if level in {"A1"}:
        return by_level["A1"]
    if level in {"A2"}:
        return by_level["A2"]
    # B1+
    return [
        {
            "wrong": "I look forward to meet you",
            "better": "I look forward to meeting you",
            "tip_ru": "После look forward to — глагол на -ing.",
        },
        {
            "wrong": "She explained me the rule",
            "better": "She explained the rule to me",
            "tip_ru": "explain something to someone — не explain me.",
        },
        {
            "wrong": "I used to living here",
            "better": "I used to live here",
            "tip_ru": "used to + V1 (не -ing).",
        },
        {
            "wrong": "It's depend on you",
            "better": "It depends on you",
            "tip_ru": "depend — обычный глагол: it depends.",
        },
        {
            "wrong": "I wish I can speak better",
            "better": "I wish I could speak better",
            "tip_ru": "После wish о настоящем — Past: could, not can.",
        },
    ]


def _fallback_voice_phrases(level: str) -> list[str]:
    pools = {
        "A0": [
            "Hello! How are you today?",
            "My name is Alex.",
            "I like coffee and tea.",
            "See you tomorrow!",
        ],
        "A1": [
            "What did you do yesterday?",
            "I'm learning English every day.",
            "Can you help me, please?",
            "That sounds great — let's try!",
        ],
        "A2": [
            "I've been busy this week.",
            "Could you say that again, please?",
            "I'm trying to sound more natural.",
            "Let's grab a coffee later.",
        ],
        "B1": [
            "I've been meaning to practice speaking more.",
            "That makes sense — I hadn't thought of it that way.",
            "Could you walk me through it one more time?",
            "I'm getting more comfortable with small talk.",
        ],
    }
    if level in pools:
        return list(pools[level])
    if level in {"B2", "C1", "C2"}:
        return list(pools["B1"])
    return list(pools["A1"])


def build_voice_phrases(user: dict) -> list[str]:
    level = user.get("level") or "A1"
    from services.gpt import _ask_json

    fallback = _fallback_voice_phrases(level)
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Return ONLY JSON {\"phrases\":[\"...\",\"...\",\"...\",\"...\"]} "
                    "— 4 short spoken English lines for pronunciation practice, "
                    f"CEFR {level}, natural conversation, not textbook drills."
                ),
            },
            {"role": "user", "content": f"CEFR: {level}. Seed {random.random()}"},
        ],
        {"phrases": fallback},
        temperature=0.5,
        max_tokens=200,
    )
    phrases = data.get("phrases") if isinstance(data, dict) else None
    if not isinstance(phrases, list) or len(phrases) < 4:
        return fallback
    clean = [str(p).strip() for p in phrases[:4] if str(p).strip()]
    return clean if len(clean) >= 4 else fallback


def attach_accent_tour(phrases: list[str], user: dict | None = None) -> list[dict]:
    """
    Привязать к фразам разные голоса из каталога LexDAN (для «Голос дня»).
    Слушать акценты можно все; для практики не зависит от тарифа.
    """
    from services.voices import CHAT_VOICES, DEFAULT_VOICE_ID

    tour = [
        {
            "key": "adam",
            "name": "Adam",
            "accent": "American",
            "flag": "🇺🇸",
            "voice_id": DEFAULT_VOICE_ID,
        },
    ] + list(CHAT_VOICES)
    # 4 фразы: Adam → Scotty → Emmaline → Joe (или дальше по кругу)
    out: list[dict] = []
    for i, text in enumerate(list(phrases)[:4]):
        v = tour[i % len(tour)]
        label = f"{v['name']} · {v.get('accent') or ''} {v.get('flag') or ''}".strip()
        out.append(
            {
                "text": str(text).strip(),
                "voice_id": v["voice_id"],
                "voice_label": label,
                "voice_key": v["key"],
            }
        )
    return out


def phrase_text(item) -> str:
    if isinstance(item, dict):
        return str(item.get("text") or "").strip()
    return str(item or "").strip()


def evaluate_voice_attempt(target: str, heard: str) -> dict:
    from services.gpt import _ask_json

    fallback = {
        "ok": True,
        "better": target,
        "tip_ru": "Хорошая попытка! Повтори ещё раз чуть медленнее.",
    }
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Pronunciation/speaking coach. Student tried to say TARGET. "
                    "Return ONLY JSON "
                    '{"ok":bool,"better":"natural version","tip_ru":"short Russian tip"} '
                    "ok=true if meaning is clear even with mistakes."
                ),
            },
            {
                "role": "user",
                "content": f"TARGET: {target}\nSTUDENT SAID: {heard}",
            },
        ],
        fallback,
        temperature=0.2,
        max_tokens=220,
    )
    if not isinstance(data, dict):
        return fallback
    return {
        "ok": bool(data.get("ok", True)),
        "better": str(data.get("better") or target).strip(),
        "tip_ru": str(data.get("tip_ru") or "").strip(),
    }


def format_card(i: int, total: int, card: dict) -> str:
    wrong = card.get("wrong") or "—"
    better = card.get("better") or "—"
    tip = card.get("tip_ru") or ""
    tip_block = f"💡 {tip}\n\n" if tip else ""
    return (
        f"📝 <b>Разбор недели · карточка {i}/{total}</b>\n\n"
        f"❌ Часто так:\n<i>{wrong}</i>\n\n"
        f"✅ Как носитель:\n<b>{better}</b>\n\n"
        f"{tip_block}"
        "Запомни пару и жми «Далее» 💚"
    )
