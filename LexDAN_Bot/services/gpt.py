"""
Общение (живые правки по грамматике) + судьи для теста уровня.
"""

import json
import logging
import random
import re
import requests
from config import OPENROUTER_API_KEY

SYSTEM_PROMPT = """
You are LexDAN / Rico — a warm English tutor in Telegram for Russian-speaking students.
You check structure carefully and rewrite toward NATURAL native English, keeping the student's meaning.

Return ONLY JSON (no markdown).

Schema:
{
  "has_error": true/false,
  "better_en": "native natural English with the SAME meaning",
  "errors_ru": "конкретно что не так в структуре/грамматике/словах (по-русски), или пусто",
  "tips_ru": "почему носитель сказал бы так; 1-3 полезных слова/фразы которые стоит добавить или заменить (по-русски)",
  "reply_en": "short chatty English reply + ONE fresh question"
}

CORRECTION RULES (strict):
1) Analyze word order, tenses, articles, prepositions, agreement, awkward phrasing, missing words.
2) better_en = how a native speaker would naturally say the SAME idea.
   - Keep the student's meaning/facts. Do NOT invent a new story.
   - If the message is long, heavy, or textbook-like → simplify to natural spoken English.
   - Fix logic only when the sentence is nonsense; otherwise preserve intent.
3) has_error=true ONLY for real word/grammar/structure problems (not style-only nitpicking).
4) If the sentence is already natural and correct → has_error=false, better_en="", errors_ru="", tips_ru="".
5) NEVER check or mention punctuation or capitalization (., ,, ?, !, ;, quotes, Caps).
   You may silently put normal punctuation in better_en, but errors_ru/tips_ru must NOT talk about it.
6) Never praise mistakes. No "Молодец/Nice/Great" about wrong English.
7) errors_ru MUST be factually true vs the student's words:
   - Before saying a word is missing, CHECK the student message (ignore case).
   - Example: student wrote "... and Translate" → do NOT say translate is missing.
   - Example: "can explain" without you → say: нужно «you»: can you explain.
8) tips_ru: only useful words/phrases that are NEW vs what the student already wrote.

CHAT RULES (reply_en) — ALWAYS keep the chat moving:
1) EVERY reply_en MUST: (a) react to the student's LAST message, (b) ask ONE follow-up
   question that develops THE SAME idea/topic (football → club/player/match; food → dish/place…).
2) Never end with empty closers: "Got it", "Let's keep chatting", "Okay", "Alright",
   "Interesting" alone, or any reply WITHOUT a question mark.
3) Stay on the student's topic. Do NOT jump to a random new topic while theirs is alive.
4) Suggest a NEW concrete topic ONLY on pure small talk / "idk what to talk about" /
   one-word dead-end with nothing left to ask.
5) Never reuse the exact same question from recent replies; rephrase, keep the topic.
6) 1–3 short spoken A2–B1 sentences + one question. Not a textbook.
7) Light praise ("Nice!") is OK only if a real follow-up question comes right after.
"""

_FALLBACK_REPLIES = [
    "Hey! What made you smile today?",
    "Nice chatting! Do you like cooking or ordering food more?",
    "Cool. What's one song you can't stop listening to?",
    "Okay! Are you more of a morning person or a night owl?",
    "What do you usually do after work or school?",
    "Interesting! Coffee or tea — what's your go-to?",
    "Tell me about your favorite place in your city — why do you like it?",
    "Hey! If you had a free Saturday, how would you spend it?",
    "Do you prefer movies at home or going out with friends?",
    "What's something small you want to learn this week?",
]

_TOPIC_CONTINUE_REPLIES = [
    "Interesting! What else can you tell me about that?",
    "Cool — what do you like most about it?",
    "Nice detail. What happened next?",
    "Why is that important to you?",
    "How often do you do that?",
    "Who do you usually share that with?",
    "What made you start liking that?",
    "Would you recommend it to a friend — why?",
]

_DEAD_REPLY_RE = re.compile(
    r"^\s*(got it|okay|ok|alright|interesting|cool|nice|sure|thanks)[\s.!,—-]*"
    r"(let'?s keep chatting)?\s*$",
    re.I,
)

_SMALLTALK_RE = re.compile(
    r"^\s*(hi|hey|hello|hola|yo|sup|hiya|"
    r"how are you( doing)?|how'?s it going|what'?s up|"
    r"good morning|good evening|good night|"
    r"i don'?t know|idk|nothing|no idea|"
    r"ok|okay|yes|no|yeah|yep|nope|hmm|hm)\s*[.!?]*\s*$",
    re.I,
)


def ask_tutor(
    user_text: str,
    user_name: str = "Student",
    recent_replies: list[str] | None = None,
    recent_turns: list[dict] | None = None,
) -> dict:
    fallback = {
        "has_error": False,
        "better_en": "",
        "errors_ru": "",
        "tips_ru": "",
        "rule_ru": "",
        "reply_en": _fallback_reply_for(user_text, recent_replies or []),
    }

    recent = [r for r in (recent_replies or []) if r][-8:]
    turns = [t for t in (recent_turns or []) if t.get("text")][-10:]

    recent_block = ""
    if recent:
        recent_block = (
            "\n\nDo NOT repeat these questions word-for-word "
            "(rephrase OK, but KEEP the same topic if one is active):\n- "
            + "\n- ".join(recent)
        )

    dialogue_block = ""
    if turns:
        lines = []
        for t in turns:
            who = "Student" if t.get("role") == "user" else "Tutor"
            lines.append(f"{who}: {t.get('text')}")
        dialogue_block = (
            "\n\nRecent dialogue (continue the student's topic unless it is dead):\n"
            + "\n".join(lines)
        )

    topic_hint = (
        "Student has NO clear topic yet → answer briefly and suggest ONE concrete topic + a question."
        if _looks_like_no_topic(user_text) and not _active_topic_in_turns(turns)
        else (
            "Student has a topic → react to THEIR last message and ask ONE follow-up "
            "that develops the SAME topic (never 'Got it / let's keep chatting')."
        )
    )

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            SYSTEM_PROMPT
                            + f"\nStudent's name: {user_name}. Use the name lightly sometimes."
                            + recent_block
                            + dialogue_block
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "1) Check grammar/structure/words. Ignore punctuation and capitalization.\n"
                            "2) If real issues: rewrite as a native (same meaning).\n"
                            "3) errors_ru/tips_ru in Russian: ONLY real changes "
                            "(do not claim a word is missing if the student already used it).\n"
                            f"4) reply_en: {topic_hint}\n\n"
                            f"Student message: {user_text}"
                        ),
                    },
                ],
                "max_tokens": 520,
                "temperature": 0.4,
            },
            timeout=30,
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"].strip()
        parsed = _parse_tutor_json(raw) or dict(fallback)
        parsed = _sanitize_correction(user_text, parsed)
        parsed = _ensure_diverse_reply(parsed, recent, user_text=user_text, turns=turns)
        return parsed
    except Exception as e:
        logging.error(f"GPT error: {e}")
        return fallback


def _looks_like_no_topic(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return True
    if _SMALLTALK_RE.match(t):
        return True
    # очень короткое «пустое» сообщение без существительных темы
    tokens = _normalize_tokens(t)
    return len(tokens) <= 2 and tokens[0] in {
        "hi", "hey", "hello", "ok", "okay", "yes", "no", "yeah", "idk", "thanks", "thank",
    }


def _active_topic_in_turns(turns: list[dict]) -> bool:
    """Есть ли в недавнем диалоге содержательные реплики ученика (не small talk)."""
    for t in reversed(turns or []):
        if t.get("role") != "user":
            continue
        if not _looks_like_no_topic(t.get("text") or ""):
            return True
    return False


def _fallback_reply_for(
    user_text: str,
    recent: list[str],
    turns: list[dict] | None = None,
) -> str:
    # small talk / нет темы → предложить тему
    if _looks_like_no_topic(user_text) and not _active_topic_in_turns(turns or []):
        pool = [
            x
            for x in _FALLBACK_REPLIES
            if all(_token_overlap_ratio(x, r) < 0.5 for r in recent)
        ]
        return random.choice(pool or _FALLBACK_REPLIES)
    # есть тема — развить, не обрывать
    pool = [
        x
        for x in _TOPIC_CONTINUE_REPLIES
        if all(_token_overlap_ratio(x, r) < 0.55 for r in recent)
    ]
    return random.choice(pool or _TOPIC_CONTINUE_REPLIES)


def _is_dead_reply(reply: str) -> bool:
    r = (reply or "").strip()
    if not r:
        return True
    if "?" not in r:
        return True
    if _DEAD_REPLY_RE.match(r):
        return True
    low = r.lower()
    if "keep chatting" in low or "let's keep chat" in low:
        return True
    return False


def _strip_leading_praise(reply: str) -> str:
    """Убрать пустой восторг в начале, оставить вопрос/суть."""
    r = (reply or "").strip()
    r = re.sub(
        r"^(nice|great|awesome|well done|good job|cool|amazing|perfect)"
        r"(\s+choice)?[!.,]*\s*",
        "",
        r,
        flags=re.I,
    )
    return r.strip() or (reply or "").strip()


def _normalize_tokens(text: str) -> list[str]:
    text = (text or "").lower()
    text = re.sub(r"[^a-zа-яё0-9\s']", " ", text)
    return [t for t in text.split() if t]


def _token_overlap_ratio(a: str, b: str) -> float:
    sa, sb = set(_normalize_tokens(a)), set(_normalize_tokens(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / max(len(sa | sb), 1)


def _same_ignoring_noise(user_text: str, better_en: str) -> bool:
    return _normalize_tokens(user_text) == _normalize_tokens(better_en)


def _keeps_meaning(user_text: str, better_en: str) -> bool:
    """Разрешаем «как носитель» (можно короче/естественнее), но не смену темы."""
    u = _normalize_tokens(user_text)
    b = _normalize_tokens(better_en)
    if not u or not b:
        return False
    if len(u) <= 2:
        return len(b) <= 8 and (
            u[0][:2] == b[0][:2] or _token_overlap_ratio(user_text, better_en) >= 0.3
        )
    # достаточно общих смысловых слов ИЛИ высокая доля overlap
    overlap = len(set(u) & set(b))
    if overlap >= max(1, min(3, len(set(u)) // 2)):
        return True
    return _token_overlap_ratio(user_text, better_en) >= 0.28


def _token_diff(user_text: str, better_en: str) -> tuple[list[str], list[str]]:
    """Слова, которые добавили / убрали (без учёта пунктуации и регистра)."""
    from collections import Counter

    cu = Counter(_normalize_tokens(user_text))
    cb = Counter(_normalize_tokens(better_en))
    added = list((cb - cu).elements())
    removed = list((cu - cb).elements())
    return added, removed


def _auto_errors_ru(user_text: str, better_en: str) -> str:
    """Честное объяснение по реальной разнице слов — без выдумок модели."""
    added, removed = _token_diff(user_text, better_en)
    if not added and not removed:
        return ""

    bits = []
    # типичный случай: can explain → can you explain
    u = _normalize_tokens(user_text)
    if "you" in added and "can" in u and "explain" in u:
        bits.append('После «can» нужно «you»: can you explain (не «can explain»).')
        added = [w for w in added if w != "you"]

    if removed and added:
        bits.append(
            "Замени: "
            + ", ".join(f"«{w}»" for w in removed[:4])
            + " → "
            + ", ".join(f"«{w}»" for w in added[:4])
            + "."
        )
    elif removed:
        bits.append("Убери лишнее: " + ", ".join(f"«{w}»" for w in removed[:5]) + ".")
    elif added:
        bits.append("Добавь: " + ", ".join(f"«{w}»" for w in added[:5]) + ".")

    return " ".join(bits)


def _mentions_already_present_word(text: str, user_text: str, better_en: str) -> bool:
    """True, если объяснение врёт: говорит про слово, которое ученик уже написал и оно осталось."""
    if not text:
        return False
    added, removed = _token_diff(user_text, better_en)
    user_set = set(_normalize_tokens(user_text))
    low = text.lower()
    # «отсутствует / пропущено / добавь … X» при том что X уже был у ученика и не в removed
    claim_missing = any(
        m in low
        for m in (
            "отсутств",
            "пропущ",
            "добав",
            "нужно добавить",
            "нет глагол",
            "нет слов",
        )
    )
    if not claim_missing:
        return False
    for w in user_set:
        if len(w) < 3:
            continue
        if w in low and w not in removed and w not in added:
            # слово уже было у ученика и не менялось — нельзя говорить что его нет
            return True
    return False


def _strip_punctuation_talk(text: str) -> str:
    if not text:
        return ""
    low = text.lower()
    bad = (
        "пунктуац",
        "запят",
        "точк",
        "восклиц",
        "вопросительн",
        "заглавн",
        "регистр",
        "capital",
        "punctuation",
        "comma",
        "period",
        "question mark",
    )
    if any(b in low for b in bad):
        return ""
    return text


def _sanitize_correction(user_text: str, result: dict) -> dict:
    """Оставляем native-правку, если смысл сохранён; иначе чистим."""
    better = _clean_field(result.get("better_en") or "")
    errors = _strip_punctuation_talk(_clean_field(result.get("errors_ru") or ""))
    tips = _strip_punctuation_talk(
        _clean_field(result.get("tips_ru") or result.get("rule_ru") or "")
    )
    has_error = bool(result.get("has_error"))

    # только пунктуация/регистр — не ошибка
    if better and _same_ignoring_noise(user_text, better):
        better = ""
        errors = ""
        tips = ""
        has_error = False

    if better and not _keeps_meaning(user_text, better):
        logging.info(f"Dropped off-topic rewrite: '{user_text}' -> '{better}'")
        better = ""
        has_error = False
        errors = ""
        tips = ""

    if better:
        has_error = True
        auto = _auto_errors_ru(user_text, better)
        # если модель соврала про уже написанное слово — берём авто-объяснение
        if (
            not errors
            or _mentions_already_present_word(errors, user_text, better)
            or _mentions_already_present_word(tips, user_text, better)
        ):
            errors = auto or errors
            if _mentions_already_present_word(tips, user_text, better):
                tips = ""
        elif auto and len(auto) < len(errors) + 40:
            # короткое честное описание предпочтительнее длинной путаницы
            errors = auto
    elif has_error and not better and not errors and not tips:
        has_error = False

    result["has_error"] = has_error
    result["better_en"] = better
    result["errors_ru"] = errors
    result["tips_ru"] = tips
    result["rule_ru"] = tips  # совместимость
    return result


def _ensure_diverse_reply(
    result: dict,
    recent: list[str],
    user_text: str = "",
    turns: list[dict] | None = None,
) -> dict:
    """Не повторять тот же вопрос; тему ученика не ломать случайным fallback."""
    reply = _clean_field(result.get("reply_en") or "")
    banned_bits = (
        "tell me something about your day",
        "what was the best part",
        "best part of your day",
    )
    low = reply.lower()
    recent_low = [(r or "").lower() for r in recent]
    repeated = False

    for b in banned_bits:
        if b in low and any(b in r for r in recent_low):
            repeated = True
            break

    for r in recent:
        if reply and _token_overlap_ratio(reply, r) >= 0.72:
            repeated = True
            break

    if not reply or repeated or _is_dead_reply(reply):
        # при активной теме не подсовываем случайную «песню» и не обрываем чат
        reply = _fallback_reply_for(user_text, recent, turns=turns)
    result["reply_en"] = reply
    return result


def judge_translation(source_en: str, reference_ru: str, user_ru: str) -> dict:
    fallback = {"score": 20, "cefr_estimate": "A1"}
    prompt = {
        "role": "system",
        "content": (
            "Strict placement-test judge for English→Russian translation. "
            "Score 0-100. Be STRICT: demand close meaning and decent Russian. "
            "Typos ok if meaning is clear; invented meaning = low score. "
            "Also estimate CEFR A0-C2. "
            'Return ONLY JSON: {"score":0-100,"cefr_estimate":"A2"}'
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"EN:\n{source_en}\n\nRU reference:\n{reference_ru}\n\n"
            f"Student:\n{user_ru}"
        ),
    }
    return _ask_json([prompt, user], fallback, temperature=0.0)


def judge_vocab(en_word: str, acceptable_ru: list[str], user_ru: str) -> dict:
    fallback = {"correct": False}
    prompt = {
        "role": "system",
        "content": (
            "Strict vocab check. correct=true only if meaning clearly matches. "
            "Close synonyms OK; vague/wrong = false. "
            'Return ONLY JSON: {"correct":bool}'
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"EN: {en_word}\nAcceptable RU: {', '.join(acceptable_ru)}\n"
            f"Student: {user_ru}"
        ),
    }
    return _ask_json([prompt, user], fallback, temperature=0.0)


def judge_listening(expected_en: str, user_text: str) -> dict:
    fallback = {"correct": False, "score": 20}
    prompt = {
        "role": "system",
        "content": (
            "Strict listening dictation check. "
            "Small spelling mistakes OK if words are clear. "
            "Missing key words / wrong meaning = incorrect. "
            "score>=85 required for correct=true. "
            'Return ONLY JSON: {"correct":bool,"score":0-100}'
        ),
    }
    user = {
        "role": "user",
        "content": f"Expected:\n{expected_en}\n\nStudent:\n{user_text}",
    }
    return _ask_json([prompt, user], fallback, temperature=0.0)


def judge_writing(topic: str, user_text: str, current_level: str) -> dict:
    fallback = {"cefr_estimate": current_level}
    prompt = {
        "role": "system",
        "content": (
            "Strict CEFR writing placement judge A0-C2. "
            "Be conservative: if between two levels, choose the LOWER one. "
            'Return ONLY JSON: {"cefr_estimate":"B1"}'
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"Approx prior level: {current_level}\nTopic: {topic}\n\n"
            f"Student text:\n{user_text}"
        ),
    }
    return _ask_json([prompt, user], fallback, temperature=0.0)


_BAD_PLACEHOLDERS = (
    "пустая строка",
    "грамматическая/лексическая",
    "дружелюбное объяснение",
    "естественный вариант",
    "живой ответ",
    "лёгкий follow-up",
    "short friendly",
    "correct natural",
    "warm 1-2",
)


def _clean_field(text: str) -> str:
    t = (text or "").strip()
    low = t.lower()
    if low in {"нет", "no", "none", "n/a", "na", "-", "—", "пусто", "empty", "null"}:
        return ""
    for bad in _BAD_PLACEHOLDERS:
        if bad.lower() in low:
            return ""
    return t


def format_tutor_message(result: dict, heard_text: str | None = None) -> str:
    """Красивое HTML-сообщение для Telegram."""
    parts = []

    if heard_text:
        parts.append(f"🗣 <b>Услышал:</b> <i>{_esc(heard_text)}</i>")
        parts.append("")

    better = _clean_field(result.get("better_en") or "")
    errors = _clean_field(result.get("errors_ru") or "")
    tips = _clean_field(result.get("tips_ru") or result.get("rule_ru") or "")

    if better or errors or tips:
        parts.append("✏️ <b>Как сказал бы носитель</b>")
        if better:
            parts.append(f"<b>{_esc(better)}</b>")
        if errors:
            parts.append("")
            parts.append(f"<b>Что поправить:</b>\n{_esc(errors)}")
        if tips:
            parts.append("")
            parts.append(f"💡 <b>Полезно запомнить:</b>\n{_esc(tips)}")
        parts.append("")
        parts.append("Суть твоей мысли сохранили — просто сделали естественнее. Продолжаем!")
    else:
        parts.append("✅ <b>Звучит естественно — молодец!</b> 🎉")

    reply = _clean_field(result.get("reply_en") or "")
    # Раньше «Nice!» в живом ответе затирало ВЕСЬ reply на «Got it…» — больше не трогаем так.
    if better or errors:
        reply = _strip_leading_praise(reply)
    if _is_dead_reply(reply):
        reply = random.choice(_TOPIC_CONTINUE_REPLIES)
    result["reply_en"] = reply

    parts.append("")
    parts.append("────────")
    parts.append("")
    parts.append(f"💬 {_esc(reply)}")

    return "\n".join(parts)


def _esc(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _ask_json(
    messages: list,
    fallback: dict,
    temperature: float = 0.1,
    max_tokens: int = 350,
) -> dict:
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=35,
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"].strip()
        data = _extract_json(raw)
        if not data:
            return fallback
        merged = dict(fallback)
        merged.update(data)
        return merged
    except Exception as e:
        logging.error(f"GPT json error: {e}")
        return fallback


def _extract_json(raw: str) -> dict | None:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None


def _parse_tutor_json(raw: str) -> dict | None:
    data = _extract_json(raw)
    if not data:
        return None

    reply = (data.get("reply_en") or "").strip()
    if not reply or _clean_field(reply) == "":
        if not reply or any(b.lower() in reply.lower() for b in _BAD_PLACEHOLDERS):
            return None

    better = _clean_field(data.get("better_en") or "")
    errors = _clean_field(data.get("errors_ru") or data.get("mistakes_ru") or "")
    tips = _clean_field(
        data.get("tips_ru") or data.get("rule_ru") or ""
    )

    has_error = data.get("has_error")
    if isinstance(has_error, str):
        has_error = has_error.strip().lower() in {"1", "true", "yes"}
    elif has_error is None:
        has_error = bool(better or errors or tips)
    else:
        has_error = bool(has_error)

    if has_error and not better and not errors and not tips:
        has_error = False

    return {
        "has_error": has_error,
        "better_en": better,
        "errors_ru": errors,
        "tips_ru": tips,
        "rule_ru": tips,
        "reply_en": reply,
    }
