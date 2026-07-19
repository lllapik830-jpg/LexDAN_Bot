"""
Итоговый тест Vocabulary по уровню (5 заданий, без генерации «на лету»).
"""

from __future__ import annotations

import random
import re

from data.vocab_final_texts import pick_final_text
from data.vocabulary_words import iter_level_words, level_words_total
from services.vocabulary_state import ensure_vocab_progress


def level_words_learned(user: dict, level: str) -> int:
    ensure_vocab_progress(user)
    prefix = f"{level}:"
    return sum(1 for k in user["vocabulary_progress"]["words"] if k.startswith(prefix))


def is_level_vocab_words_complete(user: dict, level: str) -> bool:
    total = level_words_total(level)
    if total <= 0:
        return False
    return level_words_learned(user, level) >= total


def is_vocab_final_passed(user: dict, level: str) -> bool:
    ensure_vocab_progress(user)
    passed = user["vocabulary_progress"].setdefault("final_test_passed", {})
    return bool(passed.get(level))


def mark_vocab_final_passed(user_id: str, level: str) -> dict:
    from services.lesson_state import update_lesson

    def mut(u):
        ensure_vocab_progress(u)
        passed = u["vocabulary_progress"].setdefault("final_test_passed", {})
        passed[level] = True

    return update_lesson(user_id, mut)


def _norm_ru(s: str) -> str:
    s = (s or "").strip().lower().replace("ё", "е")
    s = re.sub(r"[^\w\s\-]", " ", s, flags=re.UNICODE)
    return " ".join(s.split())


def _ru_variants(ru: str) -> list[str]:
    """Разбить эталон на варианты: «привет / здравствуй», «хорошо, окей»."""
    raw = (ru or "").strip().lower().replace("ё", "е")
    parts = re.split(r"[/;|]+|,", raw)
    out = []
    for p in parts:
        n = _norm_ru(p)
        if n:
            out.append(n)
    if not out and raw:
        out.append(_norm_ru(raw))
    return out


def check_word_translation(expected_ru: str, user_answer: str) -> bool:
    ans = _norm_ru(user_answer)
    if not ans:
        return False
    for var in _ru_variants(expected_ru):
        if ans == var:
            return True
        # короткие слова — только точное; длиннее — допускаем вхождение
        if len(var) >= 4 and (var in ans or ans in var):
            return True
        # overlap токенов для мультисловных
        ta, tb = set(ans.split()), set(var.split())
        if ta and tb and len(ta & tb) >= max(1, (len(tb) + 1) // 2):
            return True
    return False


def check_text_translation(expected_ru: str, user_answer: str) -> bool:
    """Детерминированная проверка: перекрытие токенов с эталоном."""
    ans = _norm_ru(user_answer)
    ref = _norm_ru(expected_ru)
    if not ans or not ref:
        return False
    if ans == ref:
        return True
    sa, sb = set(ans.split()), set(ref.split())
    if not sa or not sb:
        return False
    overlap = len(sa & sb) / max(len(sa | sb), 1)
    # мягкий порог: смысл близко к эталону
    return overlap >= 0.28 and len(sa & sb) >= 4


def _word_forms(en: str) -> set[str]:
    """Простые формы для поиска в тексте пользователя."""
    base = (en or "").strip().lower()
    base = re.sub(r"^to\s+", "", base)
    forms = {base}
    if " " not in base:
        if base.endswith("y") and len(base) > 2:
            forms.add(base[:-1] + "ies")
        if not base.endswith("s"):
            forms.add(base + "s")
            forms.add(base + "es")
        if base.endswith("e"):
            forms.add(base + "d")
            forms.add(base + "ing")
        else:
            forms.add(base + "ed")
            forms.add(base + "ing")
    return {f for f in forms if f}


def count_level_words_in_text(text: str, level_words: list[dict]) -> list[str]:
    """Вернуть список уникальных EN-слов уровня, найденных в тексте пользователя."""
    raw = (text or "").lower()
    tokens = set(re.findall(r"[a-z']+", raw))
    found: list[str] = []
    seen: set[str] = set()
    # сначала длинные фразы (nice to meet you), потом одиночные
    sorted_words = sorted(level_words, key=lambda w: len(w.get("en") or ""), reverse=True)
    for w in sorted_words:
        en = (w.get("en") or "").strip()
        if not en:
            continue
        key = en.lower()
        if key in seen:
            continue
        phrase = re.sub(r"^to\s+", "", key)
        if " " in phrase:
            if phrase in raw:
                found.append(en)
                seen.add(key)
            continue
        forms = _word_forms(en)
        if forms & tokens:
            found.append(en)
            seen.add(key)
    return found


def build_vocab_final_test(level: str) -> dict:
    """
    5 заданий:
    1–3: перевод слов EN→RU (из всей библиотеки уровня)
    4: перевод короткого текста EN→RU (заранее)
    5: написать до 5 предложений, используя ≥5 слов уровня
    """
    pool = list(iter_level_words(level))
    if len(pool) < 5:
        raise ValueError(f"Not enough words for level {level}")

    word_pick = random.sample(pool, min(3, len(pool)))
    text = pick_final_text(level)
    # подсказка для задания 5 — любые 8 слов уровня (пользователь может взять и другие)
    hint_words = random.sample(pool, min(8, len(pool)))

    tasks: list[dict] = []
    for i, w in enumerate(word_pick, start=1):
        tasks.append(
            {
                "type": "word_tr",
                "n": i,
                "en": w["en"],
                "ru": w["ru"],
                "emoji": w.get("emoji") or "",
            }
        )
    tasks.append(
        {
            "type": "text_tr",
            "n": 4,
            "en": text["en"],
            "ru": text["ru"],
        }
    )
    tasks.append(
        {
            "type": "write_words",
            "n": 5,
            "need": 5,
            "hint_ens": [w["en"] for w in hint_words],
            "pool_ens": [w["en"] for w in pool],
        }
    )
    return {
        "level": level,
        "index": 0,
        "score": 0,
        "tasks": tasks,
    }


def format_task_prompt(task: dict, *, total: int = 5) -> str:
    n = int(task.get("n") or 0)
    t = task.get("type")
    if t == "word_tr":
        emoji = task.get("emoji") or "📝"
        return (
            f"🎯 <b>Итоговый тест Vocabulary</b> · задание {n}/{total}\n\n"
            f"{emoji} Переведи на русский (напиши ответ):\n"
            f"<b>{task['en']}</b>"
        )
    if t == "text_tr":
        return (
            f"🎯 <b>Итоговый тест Vocabulary</b> · задание {n}/{total}\n\n"
            f"📜 Переведи весь текст на русский:\n\n"
            f"<i>{task['en']}</i>"
        )
    # write_words
    hints = ", ".join(task.get("hint_ens") or [])
    need = int(task.get("need") or 5)
    return (
        f"🎯 <b>Итоговый тест Vocabulary</b> · задание {n}/{total}\n\n"
        f"✍️ Напиши текст до 5 предложений на английском.\n"
        f"Нужно использовать <b>не меньше {need} разных слов</b> из уровня "
        f"(можно любые из библиотеки уровня, не только из подсказки).\n\n"
        f"Подсказка (примеры слов): <code>{hints}</code>"
    )


def format_vocab_final_review(mistakes: list[dict], *, score: int, total: int, passed: bool) -> str:
    head = (
        f"🏆 <b>Тест сдан!</b> Результат: {score}/{total}.\n"
        f"Vocabulary уровня закрыт — ты красава! 🦜"
        if passed
        else f"🦜 Результат: {score}/{total} — нужно минимум 4.\nПовтори слова и попробуй снова!"
    )
    if not mistakes:
        return head

    lines = [head, "", "<b>Где ошибки:</b>"]
    tips: list[str] = []
    for m in mistakes:
        n = m.get("n") or "?"
        kind = m.get("type") or ""
        if kind == "word_tr":
            lines.append(
                f"• Задание {n} · слово <b>{m.get('en')}</b>\n"
                f"  твой: <i>{m.get('your') or '—'}</i> → верно: <b>{m.get('correct') or '—'}</b>"
            )
            tips.append(f"слово «{m.get('en')}»")
        elif kind == "text_tr":
            lines.append(
                f"• Задание {n} · перевод текста\n"
                f"  твой был далековат. Ориентир:\n"
                f"  <i>{(m.get('correct') or '—')[:220]}</i>"
            )
            tips.append("перевод связного текста")
        elif kind == "write_words":
            found = int(m.get("found") or 0)
            need = int(m.get("need") or 5)
            lines.append(
                f"• Задание {n} · свой текст\n"
                f"  нашлось слов уровня: <b>{found}</b> из {need}."
            )
            tips.append("активное использование слов в предложениях")
        else:
            lines.append(f"• Задание {n}")
    uniq = []
    for t in tips:
        if t not in uniq:
            uniq.append(t)
    lines.append("")
    lines.append("<b>Стоит подтянуть:</b> " + ", ".join(uniq))
    return "\n".join(lines)
