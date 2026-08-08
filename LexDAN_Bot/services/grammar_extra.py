"""
Доп. задания Grammar (A1–C2): карточки, мягкая проверка, душевный фидбек Рико.
"""

from __future__ import annotations

import random
import re

from data.grammar_extra_banks import (
    LEVEL_SUBTYPE,
    LEVEL_TITLE_RU,
    get_extra_bank,
    get_extra_item,
    has_extra_for_level,
)

# К какой теме Grammar отсылать при ошибке (по уровню + типу)
_REVIEW_BY_LEVEL: dict[str, dict[str, tuple[str, str]]] = {
    "A1": {
        "fix_sentence": ("present_simple", "Present Simple"),
        "default": ("present_simple", "Present Simple"),
    },
    "A2": {
        "order_words": ("word_order", "Порядок слов / Word order"),
        "default": ("past_simple", "Past Simple"),
    },
    "B1": {
        "paraphrase": ("present_perfect", "Present Perfect / перефраз"),
        "default": ("present_perfect", "Present Perfect"),
    },
    "B2": {
        "continue_sentence": ("conditionals_2_3", "Conditionals 2 & 3"),
        "default": ("passives", "Passive Voice"),
    },
    "C1": {
        "continue_sentence": ("mixed_conditionals", "Mixed conditionals"),
        "default": ("nominalisation", "Сложные структуры"),
    },
    "C2": {
        "continue_sentence": ("discourse", "Дискурс и нюансы"),
        "default": ("style_register", "Стиль и регистр"),
    },
}


def _normalize_text(s: str) -> str:
    """Нижний регистр, без пунктуации; апострофы снимаем — havent == haven't."""
    t = (s or "").strip().lower().replace("ё", "е")
    t = t.replace("’", "'").replace("`", "'").replace("ʻ", "'")
    t = t.replace("'", "")  # don't / dont / don't → dont
    t = re.sub(r"[.!?,;:\"«»()\[\]{}]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _answer_aliases(text: str) -> set[str]:
    n = _normalize_text(text)
    out = {n}
    if not n:
        return out
    out.add(n.replace("cannot", "cant").replace("can not", "cant"))
    out.add(n.replace("cant", "cannot"))
    out.add(n.replace("theres", "there is"))
    out.add(n.replace("there is", "theres"))
    out.add(n.replace("i am", "im"))
    out.add(n.replace("im", "i am"))
    out.add(n.replace("it is", "its"))
    out.add(n.replace("its", "it is"))
    return {x for x in out if x}


def answers_equivalent(model_answer: str, user_answer: str, accept: list[str] | None = None) -> bool:
    user_forms = _answer_aliases(user_answer)
    candidates: set[str] = set()
    for a in [model_answer, *(accept or [])]:
        candidates |= _answer_aliases(a)
    return bool(user_forms & candidates)


def subtype_for_level(level: str) -> str:
    return LEVEL_SUBTYPE.get(str(level or "").upper(), "fix_sentence")


def title_for_level(level: str) -> str:
    return LEVEL_TITLE_RU.get(str(level or "").upper(), "Доп. задания")


def rico_mode_intro(level: str, *, done: int = 0, mistakes: int = 0) -> str:
    """Тёплое вступление Рико перед выбором режима."""
    lvl = str(level or "").upper()
    title = title_for_level(lvl)
    tips = {
        "A1": (
            "Здесь мы ловим <b>маленькие, но вредные ошибки</b> в предложении "
            "и чиним их вместе. Не страшно ошибаться — так мозг запоминает лучше 🧠✨"
        ),
        "A2": (
            "Слова в куче — как пазл 🧩 Собери из них <b>живое правильное предложение</b>. "
            "Порядок слов в английском — суперсила!"
        ),
        "B1": (
            "Перефраз — это когда одно и то же говоришь <b>другими словами</b> 💬 "
            "Смысл и время (present/past) оставляем теми же, меняем формулировку."
        ),
        "B2": (
            "Я кидаю начало фразы — ты <b>дописываешь конец</b> логично и грамматично ✍️ "
            "На B2 смотрю и смысл, и конструкции (особенно conditionals)."
        ),
        "C1": (
            "Продолжай мысль на уровне C1: нюансы, связность, взрослый английский 🎓 "
            "Пиши так, будто объясняешь идею умному другу — грамматика тоже на чеку."
        ),
        "C2": (
            "C2 — это почти родной вайб 🔥 Допиши фразу тонко, стильно, по делу. "
            "Я рядом и подскажу, если грамматика поедет."
        ),
    }
    tip = tips.get(lvl, tips["A1"])
    return (
        f"🦜 <b>Рико · Доп. задания · {lvl}</b>\n"
        f"<b>{title}</b>\n\n"
        f"Привет! Давай потренируемся как друзья-репетиторы 💛\n\n"
        f"{tip}\n\n"
        f"📊 Пройдено: <b>{done}</b>/100\n"
        f"🔧 В ошибках на повтор: <b>{mistakes}</b>\n\n"
        "Выбери режим:\n"
        "✅ <b>Делать задания</b> — продолжим с того места, где остановились\n"
        "🔧 <b>Отработать ошибки</b> — только то, где споткнулись\n\n"
        "Пиши ответ текстом. Апострофы, точки и заглавные — не придираюсь; "
        "смотрю на <b>смысл и грамматику уровня</b> 👀\n"
        "На free доп. задания идут в общий дневной лимит Grammar "
        "(обычные + доп. вместе).\n"
        "Можно жать <b>⏭ Пропустить</b> — задание уйдёт в «Отработать ошибки».\n"
        "Застрял(а)? Жми <b>💡 Подсказка</b> — подтолкну правилом/словом, "
        "но ответ за тебя не напишу 💛"
    )


def review_topic_for(level: str, ex: dict) -> tuple[str, str]:
    """(topic_title, tip_ru) для отсылки при ошибке."""
    lvl = str(level or "").upper()
    subtype = ex.get("subtype") or subtype_for_level(lvl)
    mapping = _REVIEW_BY_LEVEL.get(lvl) or _REVIEW_BY_LEVEL["A1"]
    topic_id, title = mapping.get(subtype) or mapping.get("default") or ("", "Grammar")

    blob = f"{ex.get('prompt_en') or ''} {ex.get('answer') or ''}".lower()
    if lvl == "A1" and subtype == "fix_sentence":
        if any(x in blob for x in (" was ", " were ", " went ", " yesterday", " last ")):
            topic_id, title = "past_simple", "Past Simple"
        elif any(x in blob for x in (" a ", " an ", "the ")):
            topic_id, title = "articles_a_an", "Articles (a/an/the)"
        elif any(x in blob for x in ("don't", "doesn't", "did", "can ", "must ", "dont", "doesnt")):
            topic_id, title = "present_simple", "Present Simple / вспомогательные"
        elif any(x in blob for x in ("is ", "are ", "am ")):
            topic_id, title = "to_be", "To be (am/is/are)"

    if subtype == "continue_sentence" or ("if " in blob):
        if re.search(r"\bif .{0,60}\bhad (been|done|known|gone|seen|left|taken|made)\b", blob):
            topic_id, title = "conditionals_2_3", "Conditionals 2 & 3"
        elif re.search(r"\bif (i|he|she|we|they|you) had\b", blob) or "if i were" in blob:
            topic_id, title = "conditionals_2_3", "Conditionals 2 & 3"
        elif re.search(r"\bif .{0,40}\b(will|can)\b", blob) or re.search(
            r"\bif .{0,30}\b(go|comes?|rains?|finishes?)\b", blob
        ):
            topic_id, title = "conditionals_0_1", "Conditionals 0 & 1"

    if subtype == "paraphrase":
        if any(x in blob for x in ("have ", "has ", "haven't", "hasn't", "already", "yet", "ever", "never")):
            topic_id, title = "present_perfect", "Present Perfect"
        elif any(x in blob for x in (" will ", "going to", "tomorrow")):
            topic_id, title = "future", "Future forms"
        elif any(x in blob for x in (" was ", " were ", " yesterday", " last ", " ago")):
            topic_id, title = "past_simple", "Past Simple"
        else:
            topic_id, title = "present_simple", "Present Simple"

    try:
        from data.grammar_curriculum import get_topics

        for t in get_topics(lvl) or []:
            tid = str(t.get("id") or "")
            if topic_id and (tid == topic_id or topic_id in tid or tid in topic_id):
                title = t.get("title") or title
                break
            low = (t.get("title") or "").lower()
            key = title.split("/")[0].strip().lower()
            if key and key[:8] in low:
                title = t.get("title") or title
                break
    except Exception:
        pass

    tips = {
        "fix_sentence": "Сравни свою версию с образцом и посмотри, какая форма «поехала».",
        "order_words": "В английском почти всегда Subject → Verb → Object. Собери по этой схеме.",
        "paraphrase": "Сохрани смысл и время глагола, поменяй слова/конструкцию — не копируй исходник.",
        "continue_sentence": "Продолжение должно логично цепляться к началу и быть грамматичным для этого уровня.",
    }
    tip = tips.get(subtype, "Загляни в тему Grammar и пробегись глазами по правилам ещё раз.")
    return title, tip


def next_practice_index(level: str, done_ids: list[int] | None, cursor: int) -> int | None:
    """
    Следующий индекс 0..99 по порядку с места остановки.
    None — всё пройдено.
    """
    bank = get_extra_bank(level)
    n = len(bank) or 100
    done = {int(x) for x in (done_ids or [])}
    if len(done) >= n:
        return None
    start = max(0, int(cursor or 0)) % n
    for i in range(n):
        idx = (start + i) % n
        if (idx + 1) not in done:
            return idx
    return None


def prepare_extra_exercise(level: str, index: int) -> dict:
    item = get_extra_item(level, index)
    if not item:
        raise ValueError(f"no extra bank for {level}")
    subtype = item.get("subtype") or subtype_for_level(level)
    words = list(item.get("words") or [])
    display_words = list(words)
    if subtype == "order_words" and display_words:
        random.shuffle(display_words)
        if display_words == words and len(words) > 1:
            display_words = words[1:] + words[:1]

    prompt_en = (item.get("prompt_en") or "").strip()
    if subtype == "order_words":
        prompt_en = " / ".join(display_words)

    instruction = item.get("instruction_ru") or title_for_level(level)
    review_title, _ = review_topic_for(
        level, {"subtype": subtype, "prompt_en": prompt_en, "answer": item.get("answer")}
    )
    card = {
        "kind": "write",
        "subtype": subtype,
        "id": int(item.get("id") or (index + 1)),
        "index": int(index),
        "instruction_ru": instruction,
        "prompt_en": prompt_en,
        "words": words,
        "display_words": display_words,
        "answer": item.get("answer") or "",
        "accept": list(item.get("accept") or []),
        "example": item.get("example") or item.get("answer") or "",
        "review_topic": review_title,
        "prompt": _format_prompt(
            level, instruction, prompt_en, subtype, item_id=int(item.get("id") or index + 1)
        ),
    }
    return card


def _format_prompt(level: str, instruction: str, prompt_en: str, subtype: str, *, item_id: int) -> str:
    title = title_for_level(level)
    cheer = random.choice(
        [
            "Давай, я в тебя верю 💪",
            "Поехали, это по плечу ✨",
            "Спокойно, пиши как чувствуешь 🫶",
            "Рико рядом — ошибаться можно 🦜",
        ]
    )
    if subtype == "order_words":
        body = f"<b>{instruction}</b>\n\n<code>{prompt_en}</code>"
    elif subtype == "continue_sentence":
        body = f"<b>{instruction}</b>\n\n<i>{prompt_en}</i>"
    else:
        body = f"<b>{instruction}</b>\n\n{prompt_en}"
    return (
        f"🦜 <b>Доп · {level}</b> · №{item_id}/100\n"
        f"<i>{title}</i>\n\n"
        f"{body}\n\n"
        f"{cheer}"
    )


def _strip_stem_prefix(user: str, stem: str) -> str:
    u = _normalize_text(user)
    s = _normalize_text(stem)
    if s and u.startswith(s):
        return u[len(s) :].strip(" ,.-")
    return u


def _tokens(s: str) -> list[str]:
    return [t for t in _normalize_text(s).split() if t]


def _order_match(user_answer: str, gold: str, words: list[str] | None = None) -> bool:
    u = _tokens(user_answer)
    g = _tokens(gold)
    if u == g:
        return True
    if answers_equivalent(gold, user_answer):
        return True
    if words:
        needed = _tokens(" ".join(words))
        if sorted(u) == sorted(needed) and u == g:
            return True
    return False


_PAST_HINTS = re.compile(
    r"\b(was|were|been|went|did|had|made|took|saw|came|left|bought|thought|said|"
    r"\w+ed)\b"
)
_PRESENT_HINTS = re.compile(
    r"\b(am|is|are|do|does|have|has|go|goes|work|works|train|trains|"
    r"exercise|exercises|live|lives|want|wants|need|needs|like|likes)\b"
)
_FUTURE_HINTS = re.compile(r"\b(will|wont|going to|gonna)\b")


def _time_frame(text: str) -> str:
    t = _normalize_text(text)
    if _FUTURE_HINTS.search(t):
        return "future"
    # past before present if clear past markers (avoid "have" as past)
    if re.search(r"\b(yesterday|ago|last (night|week|month|year)|in 20\d\d)\b", t):
        return "past"
    if _PAST_HINTS.search(t) and not re.search(r"\b(have|has|had) (been|\w+ed|\w+en)\b", t):
        # "had" alone in "if i had" is subjunctive present-unreal — treat as present_unreal
        if re.search(r"\bif .{0,40}\bhad\b", t) and not re.search(
            r"\bhad (been|done|known|gone|seen|left|taken|made)\b", t
        ):
            return "present_unreal"
        if re.search(r"\b(was|were|went|did|yesterday|ago|\w+ed)\b", t):
            return "past"
    if _PRESENT_HINTS.search(t) or re.search(r"\b\w+s\b", t):
        return "present"
    return "unknown"


def _paraphrase_tense_ok(original: str, user: str) -> bool:
    """False если пользователь явно сменил время относительно исходника."""
    o = _time_frame(original)
    u = _time_frame(user)
    if o in {"unknown", "present_unreal"} or u in {"unknown", "present_unreal"}:
        return True
    return o == u


def _conditional_mismatch_explain(stem: str, user_answer: str) -> str | None:
    """
    Явный промах по типу conditional → текст объяснения.
    Иначе None (пусть дальше разберёт GPT / локальные эталоны).
    """
    s = _normalize_text(stem)
    u = _normalize_text(user_answer)
    full = u if (s and u.startswith(s)) else (f"{s} {u}".strip())

    # 2nd conditional / present unreal: If I had more… / If I were…
    type2 = bool(
        re.search(r"\bif (i|he|she|we|they|you) had\b", s)
        or re.search(r"\bif .{0,40}\bwere\b", s)
    ) and not bool(re.search(r"\bhad (been|done|known|gone|seen|left|taken|made|heard)\b", s))

    if type2 and re.search(r"\bwould(ve| have)\b", full):
        return (
            "Здесь <b>вторая условная</b> (гипотеза про сейчас/будущее): "
            "<i>If + Past Simple, … would + V1</i>.\n"
            "Ты использовал(а) <i>would have + V3</i> — это про <b>прошлое</b> "
            "(3-я условная / mixed). Смысл стема — «сейчас нет…», не «тогда не было…».\n"
            "Нужно: <b>would + глагол</b> (would train / would travel…), не would have trained."
        )

    # 3rd: If I had known / If she had gone…
    type3 = bool(re.search(r"\bif .{0,50}\bhad (been|done|known|gone|seen|left|taken|made|heard)\b", s))
    if type3 and re.search(r"\bwould\b", full) and not re.search(r"\bwould(ve| have)\b", full):
        return (
            "Стем про <b>прошлое</b> (3-я условная): "
            "<i>If + Past Perfect, … would have + V3</i>.\n"
            "Обычное <i>would + V1</i> здесь не подходит — нужен результат в прошлом."
        )

    # 1st: If it rains / If you go…
    type1 = bool(
        re.search(r"\bif .{0,40}\b(rains?|comes?|goes?|finishes?|need|want)\b", s)
        or re.search(r"\bif you (are|have|need|want|go|come)\b", s)
    )
    if type1 and re.search(r"\bwould\b", full):
        return (
            "Похоже на <b>1-ю условную</b> (реальная ситуация): "
            "<i>If + Present, … will/can/might + V1</i>.\n"
            "<i>Would</i> тут обычно лишний — это уже гипотеза 2-го типа."
        )
    return None


def _local_extra_ok(ex: dict, user_answer: str) -> bool:
    subtype = ex.get("subtype") or ""
    gold = ex.get("answer") or ""
    accept = list(ex.get("accept") or [])
    example = ex.get("example") or ""
    if answers_equivalent(gold, user_answer, accept + ([example] if example else [])):
        return True

    if subtype == "order_words":
        return _order_match(user_answer, gold, ex.get("words"))

    if subtype == "continue_sentence":
        if _conditional_mismatch_explain(ex.get("prompt_en") or "", user_answer):
            return False
        stem = ex.get("prompt_en") or ""
        tail = _strip_stem_prefix(user_answer, stem)
        cands = [example, gold] + accept
        for c in cands:
            c_norm = _normalize_text(c)
            stem_n = _normalize_text(stem)
            if stem_n and c_norm.startswith(stem_n):
                c_norm = c_norm[len(stem_n) :].strip(" ,.-")
            if tail and c_norm and (tail == c_norm or answers_equivalent(c_norm, tail)):
                return True
            if answers_equivalent(c, user_answer):
                return True
        if len(tail.split()) < 2 and len(_tokens(user_answer)) < 3:
            return False
        return False

    if subtype == "fix_sentence":
        bad = ex.get("prompt_en") or ""
        if answers_equivalent(bad, user_answer):
            return False
        return answers_equivalent(gold, user_answer, accept)

    if subtype == "paraphrase":
        # совпало с эталоном — ок; иначе не считаем локально верным без GPT
        if answers_equivalent(gold, user_answer, accept):
            if not _paraphrase_tense_ok(ex.get("prompt_en") or "", user_answer):
                return False
            return True
        return False

    return False


def _local_explain(level: str, ex: dict, user_answer: str) -> str:
    subtype = ex.get("subtype") or ""
    example = (ex.get("example") or ex.get("answer") or "").strip()
    bad = (ex.get("prompt_en") or "").strip()
    if subtype == "fix_sentence":
        return (
            f"В исходнике была грамматическая осечка: <i>{bad}</i>\n"
            f"Нужно поправить форму/согласование. Верный ориентир: <b>{example}</b>."
        )
    if subtype == "order_words":
        return (
            "Слова те же, но порядок «поехал». "
            f"Собери так: <b>{example}</b>."
        )
    if subtype == "paraphrase":
        if not _paraphrase_tense_ok(bad, user_answer):
            return (
                "Смысл рядом, но <b>время глагола</b> сменилось — при перефразе "
                "оставляем то же время, что в исходнике.\n"
                f"Ориентир: <b>{example}</b>."
            )
        return (
            "Смысл рядом, но перефраз пока не попал в цель. "
            f"Можно так: <b>{example}</b>."
        )
    mismatch = _conditional_mismatch_explain(bad, user_answer)
    if mismatch:
        return mismatch + f"\n\nОриентир: <b>{example}</b>."
    return (
        "Продолжение должно цепляться к началу и звучать естественно на этом уровне. "
        f"Например: <b>{example}</b>."
    )


def check_extra_answer(level: str, ex: dict, user_answer: str) -> dict:
    """
    {"correct": bool, "example": str, "explain_ru": str, "review_topic": str, "review_tip": str}
    """
    example = (ex.get("example") or ex.get("answer") or "").strip()
    subtype = ex.get("subtype") or subtype_for_level(level)
    review_topic, review_tip = review_topic_for(level, ex)

    # явный промах по conditional — сразу объясняем, без «милости» GPT
    if subtype == "continue_sentence":
        mismatch = _conditional_mismatch_explain(ex.get("prompt_en") or "", user_answer)
        if mismatch:
            return {
                "correct": False,
                "example": example,
                "explain_ru": mismatch,
                "review_topic": review_topic,
                "review_tip": review_tip,
            }

    if subtype == "paraphrase" and not _paraphrase_tense_ok(ex.get("prompt_en") or "", user_answer):
        # если всё же совпало с accept (маловероятно) — уже отсечёт _local; здесь стоп до GPT
        if not answers_equivalent(
            ex.get("answer") or "",
            user_answer,
            list(ex.get("accept") or []),
        ):
            return {
                "correct": False,
                "example": example,
                "explain_ru": _local_explain(level, ex, user_answer),
                "review_topic": review_topic,
                "review_tip": review_tip,
            }

    if _local_extra_ok(ex, user_answer):
        return {
            "correct": True,
            "example": example,
            "explain_ru": "",
            "review_topic": review_topic,
            "review_tip": review_tip,
        }

    if subtype in {"paraphrase", "continue_sentence", "fix_sentence"}:
        gpt = _gpt_soft_check(level, ex, user_answer)
        if gpt.get("correct"):
            # страховка: GPT не должен принять смену времени / wrong conditional
            if subtype == "paraphrase" and not _paraphrase_tense_ok(
                ex.get("prompt_en") or "", user_answer
            ):
                return {
                    "correct": False,
                    "example": example,
                    "explain_ru": _local_explain(level, ex, user_answer),
                    "review_topic": review_topic,
                    "review_tip": review_tip,
                }
            if subtype == "continue_sentence" and _conditional_mismatch_explain(
                ex.get("prompt_en") or "", user_answer
            ):
                return {
                    "correct": False,
                    "example": example,
                    "explain_ru": _conditional_mismatch_explain(
                        ex.get("prompt_en") or "", user_answer
                    )
                    or "",
                    "review_topic": review_topic,
                    "review_tip": review_tip,
                }
            return {
                "correct": True,
                "example": example,
                "explain_ru": "",
                "review_topic": review_topic,
                "review_tip": review_tip,
            }
        safe_example = (gpt.get("example") or example).strip() or example
        # пример от GPT не должен менять время исходника при paraphrase
        if subtype == "paraphrase" and not _paraphrase_tense_ok(ex.get("prompt_en") or "", safe_example):
            safe_example = example
        return {
            "correct": False,
            "example": safe_example,
            "explain_ru": (gpt.get("explain_ru") or _local_explain(level, ex, user_answer)).strip(),
            "review_topic": (gpt.get("review_topic") or review_topic).strip() or review_topic,
            "review_tip": review_tip,
        }

    return {
        "correct": False,
        "example": example,
        "explain_ru": _local_explain(level, ex, user_answer),
        "review_topic": review_topic,
        "review_tip": review_tip,
    }


def _gpt_soft_check(level: str, ex: dict, user_answer: str) -> dict:
    from services.gpt import _ask_json

    subtype = ex.get("subtype") or ""
    stem = ex.get("prompt_en") or ""
    gold = ex.get("answer") or ""
    example = ex.get("example") or gold
    accept = ", ".join(ex.get("accept") or [])
    review_topic, _ = review_topic_for(level, ex)
    lvl = str(level or "").upper()

    if subtype == "fix_sentence":
        hint = (
            "Student must FIX the grammar error. Accept any correct grammatical rewrite "
            "with the SAME meaning and SAME tense. Ignore punctuation/capitalization/"
            "missing apostrophes (havent=haven't). Reject if the original error remains."
        )
        task = f"Broken: {stem}\nModel: {gold}"
    elif subtype == "paraphrase":
        hint = (
            "Student must PARAPHRASE. Accept natural rewording with the SAME meaning "
            "AND the SAME tense/aspect/time frame as the original "
            "(present stays present: 'I work out' → 'I train/exercise at the gym' is OK; "
            "'I trained' is WRONG because tense changed). "
            "Do NOT suggest answers that change tense. "
            "Ignore punctuation/capitalization/missing apostrophes. "
            "Accept synonyms even if not in the example list, when meaning+tense match."
        )
        task = f"Original: {stem}\nExample: {gold}\nAlso ok: {accept}"
    else:
        hint = (
            f"Student must CONTINUE the stem. Grade grammar at CEFR {lvl} fairly but clearly: "
            "mark WRONG for real grammar mistakes (wrong conditional type, wrong tense, "
            "broken agreement). Accept varied vocabulary if grammar+logic fit the stem. "
            "Conditionals: match the type implied by the stem "
            "(If I had more free time, … → 2nd conditional: would + V1; "
            "NOT would have + V3). "
            "Ignore punctuation/capitalization/missing apostrophes. "
            "If wrong, explain the grammar point in warm Russian (2-4 sentences) "
            "and set review_topic to the relevant grammar theme."
        )
        task = f"Stem: {stem}\nSample: {example}"

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    f"You are Rico, a warm English tutor grading CEFR {lvl} practice. "
                    f"{hint} "
                    "If incorrect, explain briefly in friendly Russian (2-4 short sentences), "
                    "no scolding. Your example field MUST keep the same tense as the original/stem. "
                    'Return ONLY JSON: {"correct":bool,"example":"short correct sample",'
                    '"explain_ru":"friendly Russian explanation","review_topic":"grammar topic name"}'
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {lvl}. Subtype {subtype}. Suggested review topic: {review_topic}.\n"
                    f"{task}\nStudent: {user_answer}"
                ),
            },
        ],
        {
            "correct": False,
            "example": example,
            "explain_ru": _local_explain(level, ex, user_answer),
            "review_topic": review_topic,
        },
        temperature=0.15,
    )
    if not isinstance(data, dict):
        return {
            "correct": False,
            "example": example,
            "explain_ru": _local_explain(level, ex, user_answer),
            "review_topic": review_topic,
        }
    if not data.get("correct") and answers_equivalent(gold, user_answer, ex.get("accept")):
        return {"correct": True, "example": example, "explain_ru": "", "review_topic": review_topic}
    return {
        "correct": bool(data.get("correct")),
        "example": str(data.get("example") or example).strip() or example,
        "explain_ru": str(data.get("explain_ru") or "").strip(),
        "review_topic": str(data.get("review_topic") or review_topic).strip() or review_topic,
    }


_OK_LINES = [
    "✅ Верно! Красава, Рико гордится 🦜💛",
    "✅ Есть! Прям в яблочко 🎯",
    "✅ Супер! Так держать, дружище ✨",
    "✅ Йес! Чувствуется прогресс 🔥",
    "✅ Отлично! Мозг явно в теме 🧠💚",
]


def format_ok() -> str:
    return random.choice(_OK_LINES)


def format_bad(
    *,
    example: str,
    explain_ru: str = "",
    review_topic: str = "",
    review_tip: str = "",
) -> str:
    ex = (example or "").strip()
    if len(ex) > 140:
        ex = ex[:137].rstrip() + "…"
    lines = [
        "😅 <b>Почти!</b> Сейчас разберём без стресса.",
    ]
    if explain_ru:
        lines.append("")
        lines.append(explain_ru)
    lines.append("")
    lines.append(f"💡 Ориентир: <b>{ex}</b>")
    if review_topic:
        lines.append("")
        lines.append(f"📚 Повтори тему в Grammar: <b>{review_topic}</b>")
        if review_tip:
            lines.append(f"<i>{review_tip}</i>")
    lines.append("")
    lines.append("👉 Сейчас следующее — не зависаем, учимся на ходу 🚀")
    return "\n".join(lines)


def format_skip() -> str:
    return (
        "⏭ Ок, пропускаем — я положил(а) это в <b>Отработать ошибки</b>, "
        "вернёшься позже 🔧💛\n"
        "Дальше следующее…"
    )


def rico_extra_hint(level: str, ex: dict) -> str:
    """
    Дружелюбная подсказка без готового ответа:
    правило, конструкция, направление мысли.
    """
    from services.gpt import _ask_json

    subtype = ex.get("subtype") or subtype_for_level(level)
    stem = (ex.get("prompt_en") or "").strip()
    instruction = (ex.get("instruction_ru") or "").strip()
    review_topic, _ = review_topic_for(level, ex)
    lvl = str(level or "").upper()

    subtype_hint = {
        "fix_sentence": "Help notice WHAT is broken (tense/article/agreement) without rewriting the sentence.",
        "order_words": "Hint at English word order pattern (S-V-O / time place) without assembling the full sentence.",
        "paraphrase": "Suggest synonym direction or structure to keep SAME tense/meaning — no full paraphrase.",
        "continue_sentence": "Hint which grammar construction fits the stem (e.g. 2nd conditional would+V1) — do NOT finish the sentence.",
    }.get(subtype, "Give a gentle grammar nudge without the answer.")

    fallback = (
        f"🦜 Эй, ты справишься — это тебе по плечу 💪\n\n"
        f"Подсказка: подумай про тему <b>{review_topic}</b>. "
        "Не гонись за идеалом с первого раза — наметь конструкцию, а слова подставь сам(а). "
        "Я в тебя верю ✨"
    )

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "You are Rico, a warm parrot English tutor for Russian learners. "
                    "Give a SHORT hint (3-5 sentences in Russian, friendly, emoji ok). "
                    "NEVER write the full correct answer or a ready-made sentence the student can copy. "
                    "You MAY name a rule, construction, tense, or suggest 1-2 word OPTIONS "
                    "(not the whole solution). Encourage: 'тебе это по плечу', 'ты сможешь'. "
                    f"{subtype_hint} "
                    'Return ONLY JSON: {"hint_ru":"..."}'
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {lvl}. Subtype {subtype}. Topic hint: {review_topic}.\n"
                    f"Instruction: {instruction}\n"
                    f"Prompt: {stem}\n"
                    "Do NOT reveal the model answer."
                ),
            },
        ],
        {"hint_ru": fallback},
        temperature=0.45,
        max_tokens=280,
    )
    hint = str((data or {}).get("hint_ru") or "").strip() or fallback
    # страховка: если GPT всё же выдал слишком похожее на ответ — fallback
    gold = _normalize_text(ex.get("answer") or "")
    if gold and len(gold) > 8 and gold in _normalize_text(hint):
        hint = fallback
    if not hint.startswith("🦜"):
        hint = "🦜 " + hint
    return hint


__all__ = [
    "has_extra_for_level",
    "subtype_for_level",
    "title_for_level",
    "rico_mode_intro",
    "next_practice_index",
    "prepare_extra_exercise",
    "check_extra_answer",
    "format_ok",
    "format_bad",
    "format_skip",
    "rico_extra_hint",
    "review_topic_for",
    "get_extra_bank",
]
