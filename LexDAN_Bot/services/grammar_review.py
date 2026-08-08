"""
Ежедневное повторение Grammar: выбор темы, 5 типов заданий, строгая проверка.
"""

from __future__ import annotations

import random
from typing import Any

from data.grammar_curriculum import get_topic, is_ack_topic
from data.grammar_review_banks import get_review_bank
from services.lesson_state import ensure_progress, progress_key
from services.rico_tutor import answers_equivalent, check_write_answer

BTN_GRAMMAR_REVIEW_YES = "🔁 Повторить материал"
BTN_GRAMMAR_REVIEW_NO = "⏭ Отказаться"
BTN_VOCAB_REVIEW_YES = "🔁 Повторить"
BTN_VOCAB_REVIEW_NO = "⏭ Не сейчас"
BTN_START_GRAMMAR_TOPIC = "📚 Пройти тему Grammar"
BTN_START_VOCAB_TOPIC = "📚 Пройти тему Vocabulary"

REVIEW_TYPES = ("mcq", "word_form", "order_words", "translate_en", "write_sentence")


def _shuffle_mcq_options(item: dict) -> dict:
    """Правильный ответ не должен всегда быть на 1-й кнопке."""
    opts = list(item.get("options") or [])
    ans = (item.get("answer") or "").strip()
    if len(opts) < 2 or not ans:
        return item
    order = list(range(len(opts)))
    random.shuffle(order)
    # стараемся не оставлять correct на позиции 0
    for _ in range(6):
        if opts[order[0]] != ans or len(order) < 2:
            break
        random.shuffle(order)
    item["options"] = [opts[i] for i in order]
    return item


def _sanitize_tip(tip: str) -> str:
    """Убрать спойлеры вида «… → There are» из подсказок."""
    t = (tip or "").strip()
    if not t:
        return ""
    if "→" in t or "->" in t:
        # оставляем только безопасную часть до стрелки, если она общая
        left = t.split("→", 1)[0].split("->", 1)[0].strip(" .")
        if left.lower() in {
            "subject",
            "subject → verb → object (и обстоятельства)",
        } or left.startswith("Subject"):
            return "Порядок: подлежащее → глагол → остальное."
        if "вопрос" in left.lower() or "неисчисляем" in left.lower():
            return "Смотри: вопрос это или утверждение, и число (ед./мн.)."
        return ""
    # если tip явно содержит правильный ответ-фразу длиннее 3 слов — режем
    return t


def completed_practice_topics(user: dict) -> list[tuple[str, str, str]]:
    """[(level, topic_id, title), ...] только темы с заданиями."""
    ensure_progress(user)
    out: list[tuple[str, str, str]] = []
    for key in list(user["grammar_progress"].get("completed_topics") or []):
        if ":" not in str(key):
            continue
        level, tid = str(key).split(":", 1)
        topic = get_topic(level, tid)
        if not topic or is_ack_topic(topic):
            continue
        if not get_review_bank(tid):
            continue
        out.append((level, tid, topic.get("title") or tid))
    return out


def pick_review_set(topic_id: str) -> list[dict]:
    """Ровно 5 заданий разных типов из резерва темы."""
    bank = get_review_bank(topic_id)
    by_type: dict[str, list[dict]] = {t: [] for t in REVIEW_TYPES}
    for item in bank:
        st = (item.get("subtype") or "").strip()
        if st in by_type:
            by_type[st].append(dict(item))
    chosen: list[dict] = []
    for st in REVIEW_TYPES:
        pool = by_type.get(st) or []
        if not pool:
            continue
        item = dict(random.choice(pool))
        item["subtype"] = st
        item["kind"] = "mcq" if st == "mcq" else "write"
        # не светим спойлер-подсказки
        tip = _sanitize_tip(str(item.get("tip") or ""))
        if tip:
            item["tip"] = tip
        else:
            item.pop("tip", None)
        if st == "mcq":
            item = _shuffle_mcq_options(item)
        chosen.append(item)
    random.shuffle(chosen)
    return chosen


def ensure_grammar_review(user: dict) -> dict:
    if "grammar_review" not in user or not isinstance(user.get("grammar_review"), dict):
        user["grammar_review"] = {}
    return user["grammar_review"]


def start_review_session(user: dict, level: str, topic_id: str, title: str) -> dict:
    queue = pick_review_set(topic_id)
    gr = {
        "active": True,
        "level": level,
        "topic_id": topic_id,
        "title": title,
        "queue": queue,
        "index": 0,
        "correct": 0,
        "total": len(queue),
    }
    user["grammar_review"] = gr
    return gr


def current_review_item(user: dict) -> dict | None:
    gr = ensure_grammar_review(user)
    if not gr.get("active"):
        return None
    q = gr.get("queue") or []
    i = int(gr.get("index") or 0)
    if i < 0 or i >= len(q):
        return None
    return q[i]


def advance_review(user: dict, *, correct: bool) -> dict:
    gr = ensure_grammar_review(user)
    if correct:
        gr["correct"] = int(gr.get("correct") or 0) + 1
    gr["index"] = int(gr.get("index") or 0) + 1
    if int(gr["index"]) >= len(gr.get("queue") or []):
        gr["active"] = False
        gr["finished"] = True
        # снимок для логики офферов: не долбить ту же тему завтра
        from datetime import datetime, timedelta, timezone

        msk = timezone(timedelta(hours=3))
        user["grammar_review_last_topic_id"] = gr.get("topic_id")
        user["grammar_review_last_date"] = datetime.now(msk).date().isoformat()
        user["grammar_review_topics_count_at_review"] = len(
            completed_practice_topics(user)
        )
    return gr


def clear_review(user: dict) -> None:
    user["grammar_review"] = {"active": False}
    # Не оставлять hub=grammar_review — иначе ответы/выбор уровня перехватываются
    lesson = user.get("lesson")
    if isinstance(lesson, dict) and lesson.get("hub") == "grammar_review":
        lesson["hub"] = None


def format_review_prompt(item: dict, *, n: int, total: int, title: str) -> str:
    st = item.get("subtype") or ""
    head = f"🦜 <b>Повторение · {title}</b>\nЗадание {n}/{total}\n\n"
    instr = (item.get("instruction_ru") or "").strip()
    # tip никогда не показываем в условии — там часто спойлер ответа
    if st == "mcq":
        sent = (item.get("sentence_en") or "").strip()
        ru = (item.get("sentence_ru") or "").strip()
        body = instr
        if sent:
            body += f"\n\n<code>{sent}</code>"
        if ru:
            body += f"\n<i>{ru}</i>"
        return head + body
    if st == "word_form":
        sent = (item.get("sentence_en") or "").strip()
        ru = (item.get("sentence_ru") or "").strip()
        body = instr + (f"\n\n<code>{sent}</code>" if sent else "")
        if ru:
            body += f"\n<i>{ru}</i>"
        return head + body
    if st == "order_words":
        words = list(item.get("words") or [])
        random.shuffle(words)
        mixed = " / ".join(str(w) for w in words)
        return head + f"{instr}\n\n<code>{mixed}</code>"
    if st == "translate_en":
        ru = (item.get("sentence_ru") or "").strip()
        return head + f"{instr}\n\n<b>{ru}</b>"
    if st == "write_sentence":
        cue = (item.get("sentence_ru") or item.get("prompt_ru") or "").strip()
        return head + f"{instr}\n\n<b>{cue}</b>"
    return head + instr


def check_review_answer(user: dict, text: str) -> dict[str, Any]:
    item = current_review_item(user)
    if not item:
        return {"ok": False, "feedback": "Сессия повторения уже закончилась."}
    gr = ensure_grammar_review(user)
    level = gr.get("level") or "A1"
    title = gr.get("title") or ""
    st = item.get("subtype") or ""
    answer = (item.get("answer") or "").strip()
    accept = list(item.get("accept") or [])
    raw = (text or "").strip()

    if st == "mcq":
        options = list(item.get("options") or [])
        if raw in options and answers_equivalent(answer, raw):
            return {"ok": True, "feedback": "Верно! Супер ✨"}
        if raw == answer:
            return {"ok": True, "feedback": "Верно! Супер ✨"}
        # exact option match by normalize
        for opt in options:
            if answers_equivalent(answer, opt) and answers_equivalent(opt, raw):
                return {"ok": True, "feedback": "Верно! Супер ✨"}
        return {"ok": False, "feedback": f"Не то. Правильно: <b>{answer}</b>"}

    if st == "order_words":
        if answers_equivalent(answer, raw, accept):
            return {"ok": True, "feedback": "Порядок верный! 🧩"}
        return {"ok": False, "feedback": f"Правильный порядок: <b>{answer}</b>"}

    if st == "word_form":
        if answers_equivalent(answer, raw, accept):
            return {"ok": True, "feedback": "Форма верная!"}
        return {"ok": False, "feedback": f"Нужна форма: <b>{answer}</b>"}

    # translate_en / write_sentence — строгая проверка
    subtype = "translate_en" if st in {"translate_en", "write_sentence"} else st
    result = check_write_answer(
        level,
        title,
        item.get("instruction_ru") or "",
        answer,
        raw,
        subtype=subtype,
        accept=accept,
    )
    ok = bool(result.get("correct"))
    fb = result.get("feedback_ru") or ("Верно!" if ok else f"Пока неверно. Пример: <b>{answer}</b>")
    if not ok and answer and answer.lower() not in (fb or "").lower():
        fb = f"{fb}\nПример: <b>{answer}</b>"
    return {"ok": ok, "feedback": fb}
