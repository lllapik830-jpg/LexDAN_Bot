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
    # (topic_id_hint, human title)
    "A1": {
        "fix_sentence": ("present_simple", "Present Simple"),
        "default": ("present_simple", "Present Simple"),
    },
    "A2": {
        "order_words": ("word_order", "Порядок слов / Word order"),
        "default": ("past_simple", "Past Simple"),
    },
    "B1": {
        "paraphrase": ("conditionals_0_1", "Условные / перефраз"),
        "default": ("present_perfect", "Present Perfect"),
    },
    "B2": {
        "continue_sentence": ("conditionals_mixed", "Сложные конструкции / Conditionals"),
        "default": ("passives", "Passive Voice"),
    },
    "C1": {
        "continue_sentence": ("inversion", "Продвинутый синтаксис"),
        "default": ("nominalisation", "Сложные структуры"),
    },
    "C2": {
        "continue_sentence": ("discourse", "Дискурс и нюансы"),
        "default": ("style_register", "Стиль и регистр"),
    },
}


def _normalize_text(s: str) -> str:
    t = (s or "").strip().lower().replace("ё", "е")
    t = t.replace("’", "'").replace("`", "'")
    t = re.sub(r"[.!?,;:\"«»()\[\]{}]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _answer_aliases(text: str) -> set[str]:
    n = _normalize_text(text)
    out = {n}
    if not n:
        return out
    out.add(n.replace("cannot", "can't").replace("can not", "can't"))
    out.add(n.replace("can't", "cannot"))
    out.add(n.replace("there's", "there is"))
    out.add(n.replace("there is", "there's"))
    out.add(n.replace("i am", "i'm"))
    out.add(n.replace("i'm", "i am"))
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
            "Как друг, который понял мысль и пересказал по-своему."
        ),
        "B2": (
            "Я кидаю начало фразы — ты <b>дописываешь конец</b> логично и красиво ✍️ "
            "Тут важны смысл и грамматика уровня B2, не зубрёжка."
        ),
        "C1": (
            "Продолжай мысль на уровне C1: нюансы, связность, взрослый английский 🎓 "
            "Пиши так, будто объясняешь идею умному другу."
        ),
        "C2": (
            "C2 — это почти родной вайб 🔥 Допиши фразу тонко, стильно, по делу. "
            "Я рядом, если что-то поедет."
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
        "Пиши ответ текстом. Точки и заглавные буквы не придираюсь — "
        "смотрю на <b>смысл и грамматику</b> 👀"
    )


def review_topic_for(level: str, ex: dict) -> tuple[str, str]:
    """(topic_title, tip_ru) для отсылки при ошибке."""
    lvl = str(level or "").upper()
    subtype = ex.get("subtype") or subtype_for_level(lvl)
    mapping = _REVIEW_BY_LEVEL.get(lvl) or _REVIEW_BY_LEVEL["A1"]
    topic_id, title = mapping.get(subtype) or mapping.get("default") or ("", "Grammar")

    # уточнение для A1 fix по содержимому ошибки
    blob = f"{ex.get('prompt_en') or ''} {ex.get('answer') or ''}".lower()
    if lvl == "A1" and subtype == "fix_sentence":
        if any(x in blob for x in (" was ", " were ", " went ", " yesterday", " last ")):
            topic_id, title = "past_simple", "Past Simple"
        elif any(x in blob for x in (" a ", " an ", "the ")):
            topic_id, title = "articles_a_an", "Articles (a/an/the)"
        elif any(x in blob for x in ("don't", "doesn't", "did", "can ", "must ")):
            topic_id, title = "present_simple", "Present Simple / вспомогательные"
        elif any(x in blob for x in ("is ", "are ", "am ")):
            topic_id, title = "to_be", "To be (am/is/are)"

    # подтянуть реальное название темы из curriculum, если есть
    try:
        from data.grammar_curriculum import get_topics

        for t in get_topics(lvl) or []:
            tid = str(t.get("id") or "")
            if topic_id and (tid == topic_id or topic_id in tid or tid in topic_id):
                title = t.get("title") or title
                break
            # fuzzy by keywords in title
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
        "paraphrase": "Сохрани смысл, но поменяй слова/конструкцию — не копируй исходник.",
        "continue_sentence": "Продолжение должно логично цепляться к началу и быть грамматичным.",
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
    review_title, _ = review_topic_for(level, {"subtype": subtype, "prompt_en": prompt_en, "answer": item.get("answer")})
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
        "prompt": _format_prompt(level, instruction, prompt_en, subtype, item_id=int(item.get("id") or index + 1)),
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
        return answers_equivalent(gold, user_answer, accept)

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
        return (
            "Смысл рядом, но перефраз пока не попал в цель. "
            f"Можно так: <b>{example}</b>."
        )
    return (
        "Продолжение должно цепляться к началу и звучать естественно. "
        f"Например: <b>{example}</b>."
    )


def check_extra_answer(level: str, ex: dict, user_answer: str) -> dict:
    """
    {"correct": bool, "example": str, "explain_ru": str, "review_topic": str, "review_tip": str}
    """
    example = (ex.get("example") or ex.get("answer") or "").strip()
    subtype = ex.get("subtype") or subtype_for_level(level)
    review_topic, review_tip = review_topic_for(level, ex)

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
            return {
                "correct": True,
                "example": example,
                "explain_ru": "",
                "review_topic": review_topic,
                "review_tip": review_tip,
            }
        return {
            "correct": False,
            "example": (gpt.get("example") or example).strip() or example,
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

    if subtype == "fix_sentence":
        hint = (
            "Student must FIX the grammar error. Accept any correct grammatical rewrite "
            "with the same meaning. Ignore punctuation/capitalization. "
            "Reject if the original error remains."
        )
        task = f"Broken: {stem}\nModel: {gold}"
    elif subtype == "paraphrase":
        hint = (
            "Student must PARAPHRASE with same meaning. Accept natural rewording. "
            "Ignore punctuation/capitalization."
        )
        task = f"Original: {stem}\nExample: {gold}\nAlso ok: {accept}"
    else:
        hint = (
            "Student must CONTINUE the stem logically. Accept any sensible completion. "
            "Reject unfinished/off-topic/clearly ungrammatical. Ignore punctuation."
        )
        task = f"Stem: {stem}\nSample: {example}"

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Grade English grammar practice for Russian learners. Be LENIENT. "
                    f"{hint} "
                    "If incorrect, explain briefly in warm friendly Russian (2-4 short sentences), "
                    "like a tutor-friend named Rico — no scolding. "
                    'Return ONLY JSON: {"correct":bool,"example":"short correct sample",'
                    '"explain_ru":"friendly Russian explanation","review_topic":"grammar topic name"}'
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {level}. Subtype {subtype}. Suggested review topic: {review_topic}.\n"
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
        temperature=0.2,
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
        lines.append(
            f"📚 Повтори тему в Grammar: <b>{review_topic}</b>"
        )
        if review_tip:
            lines.append(f"<i>{review_tip}</i>")
    lines.append("")
    lines.append("👉 Сейчас следующее — не зависаем, учимся на ходу 🚀")
    return "\n".join(lines)


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
    "review_topic_for",
    "get_extra_bank",
]
