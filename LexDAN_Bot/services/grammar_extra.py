"""
Доп. задания Grammar (A1–C2): выдача карточек и мягкая проверка ответов.
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


def next_extra_index(level: str, done_ids: list[int] | None = None) -> int:
    """Следующий индекс 0..99: сначала непройденные, иначе случайный."""
    bank = get_extra_bank(level)
    n = len(bank) or 100
    done = {int(x) for x in (done_ids or [])}
    remaining = [i for i in range(n) if (i + 1) not in done]
    if remaining:
        return random.choice(remaining)
    return random.randrange(n)


def prepare_extra_exercise(level: str, index: int) -> dict:
    """Готовая карточка для показа (words перемешаны для A2)."""
    item = get_extra_item(level, index)
    if not item:
        raise ValueError(f"no extra bank for {level}")
    subtype = item.get("subtype") or subtype_for_level(level)
    words = list(item.get("words") or [])
    display_words = list(words)
    if subtype == "order_words" and display_words:
        random.shuffle(display_words)
        # не оставляем исходный порядок
        if display_words == words and len(words) > 1:
            display_words = words[1:] + words[:1]

    prompt_en = (item.get("prompt_en") or "").strip()
    if subtype == "order_words":
        prompt_en = " / ".join(display_words)

    instruction = item.get("instruction_ru") or title_for_level(level)
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
        "prompt": _format_prompt(level, instruction, prompt_en, subtype),
    }
    return card


def _format_prompt(level: str, instruction: str, prompt_en: str, subtype: str) -> str:
    title = title_for_level(level)
    if subtype == "order_words":
        body = f"<b>{instruction}</b>\n\n<code>{prompt_en}</code>"
    elif subtype == "continue_sentence":
        body = f"<b>{instruction}</b>\n\n<i>{prompt_en}</i>"
    else:
        body = f"<b>{instruction}</b>\n\n{prompt_en}"
    return f"📝 <b>Доп. задания · {level}</b>\n{title}\n\n{body}"


def _strip_stem_prefix(user: str, stem: str) -> str:
    """Если пользователь повторил начало фразы — сравниваем хвост."""
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
    # допускаем пропущенный вспомогательный артикль в начале/конце
    if answers_equivalent(gold, user_answer):
        return True
    if words:
        # все ключевые слова из набора должны быть, порядок = gold
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
        # хвост совпал с примером / accept
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
        # очень короткий бессмысленный ответ
        if len(tail.split()) < 2 and len(_tokens(user_answer)) < 3:
            return False
        return False

    if subtype == "fix_sentence":
        # если пользователь просто скопировал ошибочное предложение — нет
        bad = ex.get("prompt_en") or ""
        if answers_equivalent(bad, user_answer):
            return False
        return answers_equivalent(gold, user_answer, accept)

    if subtype == "paraphrase":
        return answers_equivalent(gold, user_answer, accept)

    return False


def check_extra_answer(level: str, ex: dict, user_answer: str) -> dict:
    """
    Мягкая проверка. Ответ:
      {"correct": True}  → показать «✅ Верно!»
      {"correct": False, "example": "..."} → «❌ Не совсем. Правильно будет: …»
    """
    example = (ex.get("example") or ex.get("answer") or "").strip()
    subtype = ex.get("subtype") or subtype_for_level(level)

    if _local_extra_ok(ex, user_answer):
        return {"correct": True, "example": example}

    # GPT для paraphrase / continue / сложных fix
    if subtype in {"paraphrase", "continue_sentence", "fix_sentence"}:
        gpt = _gpt_soft_check(level, ex, user_answer)
        if gpt.get("correct"):
            return {"correct": True, "example": example}
        return {"correct": False, "example": (gpt.get("example") or example).strip() or example}

    return {"correct": False, "example": example}


def _gpt_soft_check(level: str, ex: dict, user_answer: str) -> dict:
    from services.gpt import _ask_json

    subtype = ex.get("subtype") or ""
    stem = ex.get("prompt_en") or ""
    gold = ex.get("answer") or ""
    example = ex.get("example") or gold
    accept = ", ".join(ex.get("accept") or [])

    if subtype == "fix_sentence":
        hint = (
            "Student must FIX the grammar error. Accept any correct grammatical rewrite "
            "with the same meaning. Ignore punctuation, capitalization, extra/missing "
            "periods and minor wording. Reject if the original error remains or meaning changed."
        )
        task = f"Broken sentence: {stem}\nExpected idea: {gold}"
    elif subtype == "paraphrase":
        hint = (
            "Student must PARAPHRASE. Accept any natural rewording with the same meaning. "
            "Do NOT require the model answer verbatim. Ignore punctuation and capitalization."
        )
        task = f"Original: {stem}\nExample paraphrase: {gold}\nAlso ok: {accept}"
    else:
        hint = (
            "Student must CONTINUE the unfinished sentence logically and grammatically. "
            "Accept ANY sensible completion at this CEFR level. Do not demand the sample ending. "
            "Reject only if unfinished, off-topic, or clearly ungrammatical for the level. "
            "Ignore punctuation and capitalization."
        )
        task = f"Stem: {stem}\nSample ending: {example}\nFull sample: {gold}"

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "You grade English grammar practice answers for Russian learners. "
                    "Be LENIENT and meaning-focused. Never reject for spaces, commas, "
                    "periods, or capital letters. "
                    f"{hint} "
                    'Return ONLY JSON: {"correct":bool,"example":"short sample answer"} '
                    "If correct=false, example must be a short correct version (not a lecture)."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {level}. Subtype {subtype}.\n{task}\nStudent: {user_answer}"
                ),
            },
        ],
        {"correct": False, "example": example},
        temperature=0.0,
    )
    if not isinstance(data, dict):
        return {"correct": False, "example": example}
    ex_out = str(data.get("example") or example).strip() or example
    # safety: if local-ish match to example after GPT said no
    if not data.get("correct") and answers_equivalent(gold, user_answer, ex.get("accept")):
        return {"correct": True, "example": ex_out}
    return {"correct": bool(data.get("correct")), "example": ex_out}


def format_ok() -> str:
    return "✅ Верно!"


def format_bad(example: str) -> str:
    ex = (example or "").strip()
    # короткий пример — обрезаем слишком длинное
    if len(ex) > 120:
        ex = ex[:117].rstrip() + "…"
    return f"❌ Не совсем. Правильно будет: {ex}"


__all__ = [
    "has_extra_for_level",
    "subtype_for_level",
    "title_for_level",
    "next_extra_index",
    "prepare_extra_exercise",
    "check_extra_answer",
    "format_ok",
    "format_bad",
    "get_extra_bank",
]
