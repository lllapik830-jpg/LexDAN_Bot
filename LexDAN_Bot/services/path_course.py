"""Состояние и раннер ежедневного курса (path)."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from data.path_course import (
    COURSE_ID,
    COURSE_TITLE,
    ERROR_TMPL,
    EXAM_STUB_HTML,
    IDEAL,
    LESSON_COUNT,
    PRAISE_DONE,
    PRAISE_SCORE_UP,
    RANK_CHANGE,
    RETURN_AFTER_SKIP,
    STUB_HTML,
    WAIT_TOMORROW,
    get_lesson,
    rank_for_score,
)

MSK = timezone(timedelta(hours=3))


def _today() -> str:
    return datetime.now(MSK).date().isoformat()


def _date(s: str):
    return datetime.strptime(s, "%Y-%m-%d").date()


def ensure_path(user: dict) -> dict:
    p = user.get("path")
    if not isinstance(p, dict):
        p = {}
        user["path"] = p
    p.setdefault("course", COURSE_ID)
    p.setdefault("lesson", 1)
    p.setdefault("score", 1.0)
    p.setdefault("rank", rank_for_score(1.0)[1])
    p.setdefault("last_done", "")
    p.setdefault("enrolled_on", "")
    p.setdefault("welcomed", False)
    p.setdefault("skip_streak", 0)
    p.setdefault("skip_checked_on", "")
    if not isinstance(p.get("session"), dict):
        p["session"] = None
    return p


def _norm(text: str) -> str:
    t = (text or "").strip().lower().replace("ё", "е")
    t = t.replace("’", "'").replace("`", "'").replace("‘", "'")
    t = t.replace("'", "")
    t = re.sub(r"[.!?,;:\"«»()\[\]{}]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def check_answer(kind: str, text: str) -> bool:
    u = _norm(text)
    if not u:
        return False
    if kind == "name":
        if "my name is" in u:
            rest = u.split("my name is", 1)[-1].strip()
            return len(rest) >= 1
        if re.search(r"\b(i am|im|i m)\b", u) and len(u.split()) >= 2:
            return True
        return bool(re.fullmatch(r"[a-zа-я]{2,20}", u))
    if kind == "bee":
        compact = u.replace(" ", "").replace("/", "")
        return compact in {"би", "bee", "bi", "be", "b", "bi:", "би:"}
    if kind == "cab":
        return u == "cab" or u.replace(" ", "") == "cab"
    if kind == "goodbye":
        return any(
            x in u
            for x in ("goodbye", "good bye", "bye", "see you", "see ya")
        )
    return False


def current_lesson(user: dict) -> dict | None:
    p = ensure_path(user)
    return get_lesson(int(p.get("lesson") or 1))


def done_today(user: dict) -> bool:
    p = ensure_path(user)
    return str(p.get("last_done") or "") == _today()


def note_open(user: dict) -> int:
    """Посчитать пропуски один раз за календарный день. Возвращает skip_streak к показу."""
    p = ensure_path(user)
    today = _today()
    if not p.get("enrolled_on"):
        p["enrolled_on"] = today
    if p.get("skip_checked_on") == today:
        return int(p.get("skip_streak") or 0) if p.get("_show_skip") else 0
    p["skip_checked_on"] = today
    p["_show_skip"] = False
    if p.get("last_done") == today:
        p["skip_streak"] = 0
        return 0
    if p.get("last_done"):
        first_av = _date(p["last_done"]) + timedelta(days=1)
    else:
        first_av = _date(str(p.get("enrolled_on") or today))
    yest = _date(today) - timedelta(days=1)
    if first_av > yest:
        p["skip_streak"] = 0
        return 0
    missed = (yest - first_av).days + 1
    p["skip_streak"] = max(0, int(missed))
    if p["skip_streak"] >= 1:
        p["_show_skip"] = True
        return p["skip_streak"]
    return 0


def consume_skip_flag(user: dict) -> int:
    p = ensure_path(user)
    if p.get("_show_skip"):
        p["_show_skip"] = False
        return int(p.get("skip_streak") or 0)
    return 0


def start_session(user: dict) -> dict:
    p = ensure_path(user)
    n = int(p.get("lesson") or 1)
    lesson = get_lesson(n) or {}
    p["session"] = {
        "lesson_n": n,
        "step_i": 0,
        "sub_i": 0,
        "attempts": 0,
        "correct": 0,
        "total": 0,
        "had_skip": int(p.get("skip_streak") or 0),
        "score_from": float(p.get("score") or 1.0),
    }
    return lesson


def clear_session(user: dict) -> None:
    ensure_path(user)["session"] = None


def _step(user: dict) -> dict | None:
    p = ensure_path(user)
    s = p.get("session") or {}
    lesson = get_lesson(int(s.get("lesson_n") or p.get("lesson") or 1))
    if not lesson:
        return None
    steps = lesson.get("steps") or []
    i = int(s.get("step_i") or 0)
    if i < 0 or i >= len(steps):
        return None
    return steps[i]


def _advance(user: dict) -> None:
    p = ensure_path(user)
    s = dict(p.get("session") or {})
    s["step_i"] = int(s.get("step_i") or 0) + 1
    s["sub_i"] = 0
    s["attempts"] = 0
    p["session"] = s


def _finish_lesson(user: dict) -> dict:
    """Закрыть урок на сегодня, маленький delta по качеству ответов."""
    p = ensure_path(user)
    s = p.get("session") or {}
    score_from = float(s.get("score_from") or p.get("score") or 1.0)
    total = max(1, int(s.get("total") or 0))
    correct = int(s.get("correct") or 0)
    ratio = correct / total if int(s.get("total") or 0) else 1.0
    delta = round(0.02 + 0.03 * ratio, 2)
    score_to = round(score_from + delta, 2)
    old_rank = p.get("rank") or rank_for_score(score_from)[1]
    new_rank = rank_for_score(score_to)[1]
    p["score"] = score_to
    p["rank"] = new_rank
    p["last_done"] = _today()
    p["skip_streak"] = 0
    n = int(p.get("lesson") or 1)
    nxt = get_lesson(n + 1) or {}
    # Не прыгаем в заглушку: живой следующий урок появится — тогда сдвинем номер.
    if nxt.get("steps") and n < LESSON_COUNT:
        p["lesson"] = n + 1
    perfect = int(s.get("total") or 0) > 0 and correct == int(s.get("total") or 0)
    had_skip = int(s.get("had_skip") or 0)
    p["session"] = None
    return {
        "score_from": score_from,
        "score_to": score_to,
        "old_rank": old_rank,
        "new_rank": new_rank,
        "rank_changed": old_rank != new_rank,
        "perfect": perfect,
        "score_up": score_to > score_from + 1e-9,
        "had_skip": had_skip,
    }


def hub_html(user: dict) -> str:
    p = ensure_path(user)
    lesson = current_lesson(user) or {}
    n = int(p.get("lesson") or 1)
    score = float(p.get("score") or 1.0)
    rank = p.get("rank") or rank_for_score(score)[1]
    tag = "экзамен · " if lesson.get("exam") else ""
    lines = [
        f"🎓 <b>{COURSE_TITLE}</b>",
        f"Урок <b>{n}</b> / {LESSON_COUNT} · {tag}{lesson.get('title') or '—'}",
        f"Уровень Рико: <b>{score:.2f}</b>",
        f"Ранг: {rank}",
    ]
    if done_today(user):
        lines.append("\nСегодняшний урок уже пройден.")
    return "\n".join(lines)


def present(user: dict) -> dict:
    """Что показать сейчас (без ввода)."""
    p = ensure_path(user)
    lesson = current_lesson(user) or {}
    steps = lesson.get("steps")
    if not steps:
        if lesson.get("exam"):
            html = EXAM_STUB_HTML.format(
                title=lesson.get("title") or "Экзамен",
                target=f"{float(lesson.get('target') or 0):.1f}",
            )
        else:
            html = STUB_HTML.format(
                n=lesson.get("n") or p.get("lesson") or 1,
                title=lesson.get("title") or "",
            )
        return {"html": html, "kb": "hub", "options": None, "finished": False, "stub": True}

    s = p.get("session")
    if not isinstance(s, dict):
        return {"html": hub_html(user), "kb": "hub", "options": None, "finished": False}

    step = _step(user)
    if not step:
        fin = _finish_lesson(user)
        return _outro_payload(user, None, fin)

    kind = step.get("kind")
    sub = int((p.get("session") or {}).get("sub_i") or 0)

    if kind == "intro":
        return {"html": step["html"], "kb": "next", "options": None}
    if kind == "lex":
        return {"html": step["html"], "kb": "next", "options": None}
    if kind == "mcq":
        return {"html": step["html"], "kb": "mcq", "options": list(step.get("options") or [])}
    if kind == "prompt":
        return {"html": step["html"], "kb": "text", "options": None}
    if kind == "dialogue":
        turns = step.get("turns") or []
        if sub >= len(turns):
            _advance(user)
            return present(user)
        turn = turns[sub]
        head = step.get("html") or ""
        if sub == 0 and head:
            html = f"{head}\n\nЯ: {turn['rico']}"
        else:
            html = f"🦜 <b>Рико:</b> {turn['rico']}"
        return {"html": html, "kb": "text", "options": None}
    if kind == "quiz":
        items = step.get("items") or []
        if sub >= len(items):
            _advance(user)
            return present(user)
        item = items[sub]
        head = step.get("html") if sub == 0 else ""
        q = item.get("html") or ""
        html = f"{head}\n\n{sub + 1}. {q}".strip() if head else f"{sub + 1}. {q}"
        return {"html": html, "kb": "mcq", "options": list(item.get("options") or [])}
    if kind == "outro":
        fin = _finish_lesson(user)
        return _outro_payload(user, step, fin)
    _advance(user)
    return present(user)


def _outro_payload(user: dict, step: dict | None, fin: dict) -> dict:
    p = ensure_path(user)
    tmpl = (step or {}).get("html") or (
        "🦜 <b>Рико:</b> Урок закрыт.\n"
        "Твой прогресс: <b>{score_from}</b> → <b>{score_to}</b>\n"
        "{rank_line}"
    )
    rank_line = f"{fin['new_rank']}"
    html = tmpl.format(
        score_from=f"{fin['score_from']:.2f}",
        score_to=f"{fin['score_to']:.2f}",
        rank_line=f"Ранг: {rank_line}",
    )
    extras: list[str] = []
    if fin.get("perfect"):
        extras.append(IDEAL)
    extras.append(PRAISE_DONE)
    if fin.get("score_up"):
        extras.append(PRAISE_SCORE_UP)
    if fin.get("rank_changed"):
        extras.append(RANK_CHANGE.format(rank=fin["new_rank"]))
    if int(fin.get("had_skip") or 0) >= 1:
        extras.append(RETURN_AFTER_SKIP)
    return {
        "html": html,
        "kb": "hub",
        "options": None,
        "finished": True,
        "extras": extras,
        "hub": hub_html(user),
    }


def handle_next(user: dict) -> dict:
    step = _step(user)
    if not step:
        return present(user)
    if step.get("kind") in {"intro", "lex"}:
        _advance(user)
        return present(user)
    return present(user)


def handle_answer(user: dict, text: str) -> dict:
    p = ensure_path(user)
    s = p.get("session")
    if not isinstance(s, dict):
        return present(user)
    step = _step(user)
    if not step:
        return present(user)
    kind = step.get("kind")
    raw = (text or "").strip()

    if kind == "mcq":
        return _handle_mcq(user, step, raw, item=None)
    if kind == "quiz":
        items = step.get("items") or []
        sub = int(s.get("sub_i") or 0)
        if sub >= len(items):
            _advance(user)
            return present(user)
        return _handle_mcq(user, step, raw, item=items[sub])
    if kind == "prompt":
        return _handle_prompt(user, step, raw)
    if kind == "dialogue":
        return _handle_dialogue(user, step, raw)
    if kind in {"intro", "lex"}:
        return handle_next(user)
    return present(user)


def _match_mcq(text: str, options: list[str], correct: int) -> bool | None:
    """True/False если распознали выбор; None = не вариант."""
    u = _norm(text)
    if not u:
        return None
    if u[0].isdigit():
        try:
            idx = int(u.split(".", 1)[0].split()[0]) - 1
            if 0 <= idx < len(options):
                return idx == int(correct)
        except ValueError:
            pass
    for i, opt in enumerate(options):
        if u == _norm(opt) or u == _norm(f"{i + 1}. {opt}"):
            return i == int(correct)
    return None


def _handle_mcq(user: dict, step: dict, text: str, item: dict | None) -> dict:
    p = ensure_path(user)
    s = dict(p["session"])
    src = item or step
    options = list(src.get("options") or [])
    correct = int(src.get("correct") or 0)
    matched = _match_mcq(text, options, correct)
    if matched is None:
        return {
            "html": "Выбери вариант кнопкой ниже.",
            "kb": "mcq",
            "options": options,
        }
    first = int(s.get("attempts") or 0) == 0
    if first:
        s["total"] = int(s.get("total") or 0) + 1
    if matched:
        if first:
            s["correct"] = int(s.get("correct") or 0) + 1
        s["attempts"] = 0
        p["session"] = s
        if item is not None:
            s["sub_i"] = int(s.get("sub_i") or 0) + 1
            p["session"] = s
            items = step.get("items") or []
            if int(s["sub_i"]) >= len(items):
                _advance(user)
        else:
            _advance(user)
        nxt = present(user)
        nxt["flash"] = "Верно."
        return nxt
    s["attempts"] = int(s.get("attempts") or 0) + 1
    p["session"] = s
    explain = src.get("explain") or "посмотри варианты ещё раз"
    return {
        "html": ERROR_TMPL.format(explain=explain),
        "kb": "mcq",
        "options": options,
        "retry": True,
    }


def _handle_prompt(user: dict, step: dict, text: str) -> dict:
    p = ensure_path(user)
    s = dict(p["session"])
    ok = check_answer(str(step.get("check") or ""), text)
    first = int(s.get("attempts") or 0) == 0
    if first:
        s["total"] = int(s.get("total") or 0) + 1
        s["attempts"] = 1
    if ok:
        if first:
            s["correct"] = int(s.get("correct") or 0) + 1
        p["session"] = s
        _advance(user)
        nxt = present(user)
        nxt["flash"] = "Есть."
        return nxt
    p["session"] = s
    return {
        "html": ERROR_TMPL.format(explain=step.get("explain") or "попробуй ещё раз"),
        "kb": "text",
        "retry": True,
    }


def _handle_dialogue(user: dict, step: dict, text: str) -> dict:
    p = ensure_path(user)
    s = dict(p["session"])
    turns = step.get("turns") or []
    sub = int(s.get("sub_i") or 0)
    if sub >= len(turns):
        _advance(user)
        return present(user)
    turn = turns[sub]
    ok = check_answer(str(turn.get("check") or ""), text)
    first = int(s.get("attempts") or 0) == 0
    if first:
        s["total"] = int(s.get("total") or 0) + 1
        s["attempts"] = 1
    if ok:
        if first:
            s["correct"] = int(s.get("correct") or 0) + 1
        s["sub_i"] = sub + 1
        s["attempts"] = 0
        p["session"] = s
        if s["sub_i"] >= len(turns):
            _advance(user)
        nxt = present(user)
        nxt["flash"] = "Живой ответ."
        return nxt
    p["session"] = s
    return {
        "html": ERROR_TMPL.format(explain=turn.get("explain") or "ответь по образцу"),
        "kb": "text",
        "retry": True,
    }


def reset_path(user: dict) -> dict:
    """Сброс прогресса курса (тест урока 1)."""
    user["path"] = {}
    return ensure_path(user)


def start_or_resume(user: dict) -> dict:
    """Начать/продолжить сегодняшний урок. stub=True если контента нет."""
    p = ensure_path(user)
    if done_today(user):
        return {"html": WAIT_TOMORROW, "kb": "hub", "blocked": True}
    sess = p.get("session")
    if isinstance(sess, dict) and int(sess.get("lesson_n") or 0) == int(p.get("lesson") or 1):
        return present(user)
    lesson = start_session(user)
    if not (lesson.get("steps") or []):
        clear_session(user)
        return present(user)
    return present(user)
