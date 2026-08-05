"""
Вступительный placement-тест курса «до B2» (~30+ мин).

Порядок: Grammar(40) → Vocab(50) → Reading(30) → Listening(25) → Writing → Speaking-интервью(до 20 ответов).
Строгий скоринг, адаптив по ошибкам, слабые места по темам.
"""

from __future__ import annotations

import math
import re
from typing import Any

from data.course_placement_bank import (
    GRAMMAR,
    LEVEL_ORDER,
    LISTENING_ITEMS,
    READING_PASSAGES,
    SPEAKING_INTERVIEW,
    TOPIC_LABELS_RU,
    VOCAB,
    WRITING_PROMPTS,
    grammar_by_id,
    vocab_by_id,
)

BTN_COURSES = "🎓 Курсы"
BTN_COURSE_START_TEST = "▶️ Пройти вступительный тест"
BTN_COURSE_CONTINUE = "▶️ Продолжить тест"
BTN_COURSE_RESULTS = "📋 Мой результат теста"
BTN_COURSE_BUY = "💳 Купить курс"
BTN_COURSE_ABOUT = "ℹ️ Как устроен курс"
BTN_SKIP_SPEAKING = "⏭ Пропустить вопрос"
BTN_COURSE_FINISH_NOW = "📋 Завершить и показать результат"


def courses_allowed(user_id: str | int | None) -> bool:
    if user_id is None:
        return False
    from config import MANAGER_ID

    try:
        return int(user_id) == int(MANAGER_ID)
    except (TypeError, ValueError):
        return False


INTRO_HTML = (
    "🎓 <b>Курс LexDAN · путь до B2</b>\n\n"
    "Персональная программа от твоего уровня до уверенного B2.\n\n"
    "Сначала — <b>полный вступительный тест</b> (~30–40 мин):\n"
    "· грамматика — 40 заданий (от лёгких к сложным)\n"
    "· словарь — 50 слов (EN↔RU)\n"
    "· чтение — 30 вопросов по разным текстам\n"
    "· аудирование — 25 аудио + вопросы на понимание\n"
    "· письмо — 8 предложений на тему\n"
    "· говорение — собеседование (до 20 ответов)\n\n"
    "Можно поставить паузу. По результату — уровень, слабые темы, срок и цена."
)

PRICE_BY_LEVEL = {
    "A0": 14900,
    "A1": 12900,
    "A2": 10900,
    "B1": 9900,
    "B2": 0,
}

HOURS_TO_B2 = {"A0": 550, "A1": 450, "A2": 320, "B1": 200, "B2": 0}
START_TOPIC = {
    "A0": "A0.T1",
    "A1": "A1.T1",
    "A2": "A2.T1",
    "B1": "B1.T1",
    "B2": "DONE",
}

SPEAKING_TARGET = 20
LEVEL_WEIGHT = {"A0": 1.0, "A1": 1.2, "A2": 1.5, "B1": 1.9, "B2": 2.4}

# пороги итогового weighted score → CEFR (строже)
SCORE_TO_LEVEL = (
    (0.22, "A0"),
    (0.38, "A1"),
    (0.55, "A2"),
    (0.72, "B1"),
    (1.01, "B2"),
)


def _norm(s: str) -> str:
    t = (s or "").strip().lower().replace("ё", "е")
    t = t.replace("’", "'").replace("`", "'").replace("'", "")
    t = re.sub(r"[.!?,;:\"«»()\[\]{}]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def answers_match(model: str, user: str, accept: list[str] | None = None) -> bool:
    u = _norm(user)
    if not u:
        return False
    cands = {_norm(model)}
    for a in accept or []:
        cands.add(_norm(a))
    if u in cands:
        return True
    # can't/cannot
    alts = {u.replace("cannot", "cant").replace("can not", "cant"), u.replace("cant", "cannot")}
    return bool(alts & cands)


def _blank_state() -> dict:
    return {
        "phase": None,
        "version": 2,
        "grammar_queue": [],
        "grammar_i": 0,
        "vocab_queue": [],
        "vocab_i": 0,
        "reading_flat": [],
        "reading_i": 0,
        "listening_queue": [],
        "listening_i": 0,
        "writing_level": "A2",
        "speaking_queue": [],
        "speaking_i": 0,
        "speaking_answers": 0,
        "speaking_skipped_n": 0,
        "adapt_max_level": "B2",
        "recent_results": [],
        "skill_scores": {
            "grammar": [0, 0],
            "vocab": [0, 0],
            "reading": [0, 0],
            "listening": [0, 0],
            "writing": [0, 0],
            "speaking": [0, 0],
        },
        "topic_scores": {},
        "weighted": {"grammar": 0.0, "vocab": 0.0, "reading": 0.0, "listening": 0.0},
        "weight_max": {"grammar": 0.0, "vocab": 0.0, "reading": 0.0, "listening": 0.0},
        "writing_score": 0.0,
        "speaking_score": 0.0,
        "speaking_transcripts": [],
        "entry_level": None,
        "weak_skills": [],
        "strong_skills": [],
        "weak_topics": [],
        "strong_topics": [],
        "skill_details": {},
        "months_45": None,
        "months_60": None,
        "price": None,
        "start_topic_id": None,
        "finished": False,
        "overall_score": None,
    }


def ensure_course(user: dict) -> dict:
    if "course" not in user or not isinstance(user.get("course"), dict):
        user["course"] = {"placement": _blank_state(), "purchased": False, "active": False}
    user["course"].setdefault("purchased", False)
    user["course"].setdefault("active", False)
    if "placement" not in user["course"] or not isinstance(user["course"]["placement"], dict):
        user["course"]["placement"] = _blank_state()
    else:
        blank = _blank_state()
        for k, v in blank.items():
            user["course"]["placement"].setdefault(k, v)
    return user


def placement(user: dict) -> dict:
    ensure_course(user)
    return user["course"]["placement"]


def _level_idx(lvl: str) -> int:
    return LEVEL_ORDER.index(lvl) if lvl in LEVEL_ORDER else 2


def _build_adaptive_grammar_queue(max_level: str) -> list[str]:
    cap = _level_idx(max_level)
    ids = []
    for g in GRAMMAR:
        if _level_idx(g.get("level") or "A0") <= cap:
            ids.append(g["id"])
    return ids


def _build_vocab_queue(max_level: str) -> list[str]:
    cap = _level_idx(max_level)
    ids = []
    for v in VOCAB:
        if _level_idx(v.get("level") or "A0") <= cap:
            ids.append(v["id"])
    # если адаптив срезал слишком много — всё равно минимум 30
    if len(ids) < 30:
        ids = [v["id"] for v in VOCAB]
    return ids


def _passage_by_id(pid: str) -> dict | None:
    for pass_ in READING_PASSAGES:
        if pass_.get("id") == pid:
            return pass_
    return None


def _build_reading_flat(max_level: str) -> list[dict]:
    """Только ссылки на пассаж/вопрос — без копий текста (иначе JSON раздувается и может теряться)."""
    cap = _level_idx(max_level)
    flat: list[dict] = []
    for pass_ in READING_PASSAGES:
        pl = _level_idx(pass_.get("level") or "A0")
        if pl > cap + 1 and not (cap >= 2):
            continue
        for qi, q in enumerate(pass_.get("questions") or []):
            flat.append(
                {
                    "passage_id": pass_["id"],
                    "q_index": qi,
                    "passage_level": pass_.get("level"),
                    "passage_topic": pass_.get("topic"),
                }
            )
    if len(flat) < 15:
        flat = []
        for pass_ in READING_PASSAGES:
            for qi, q in enumerate(pass_.get("questions") or []):
                flat.append(
                    {
                        "passage_id": pass_["id"],
                        "q_index": qi,
                        "passage_level": pass_.get("level"),
                        "passage_topic": pass_.get("topic"),
                    }
                )
    return flat


def hydrate_reading_item(ref: dict) -> dict | None:
    """Восстановить текст пассажа и вопрос из банка по ссылке."""
    if not ref:
        return None
    # уже старый формат с полным текстом
    if ref.get("q") and ref.get("passage_text") is not None:
        return ref
    pass_ = _passage_by_id(str(ref.get("passage_id") or ""))
    if not pass_:
        return None
    qs = pass_.get("questions") or []
    qi = int(ref.get("q_index") or 0)
    if qi < 0 or qi >= len(qs):
        return None
    return {
        "passage_id": pass_["id"],
        "q_index": qi,
        "passage_level": pass_.get("level"),
        "passage_topic": pass_.get("topic"),
        "passage_title": pass_.get("title") or "",
        "passage_text": pass_.get("text") or "",
        "q": qs[qi],
    }


def _build_listening_queue(max_level: str) -> list[str]:
    cap = _level_idx(max_level)
    ids = []
    for it in LISTENING_ITEMS:
        if _level_idx(it.get("level") or "A0") <= cap + 1:
            ids.append(it["id"])
    if len(ids) < 12:
        ids = [it["id"] for it in LISTENING_ITEMS]
    return ids


def repair_placement_queues(p: dict) -> None:
    """Если очередь секции потерялась — восстановить из банка, не сбрасывая прогресс."""
    phase = p.get("phase")
    adapt = p.get("adapt_max_level") or "B2"
    if phase == "grammar":
        if not p.get("grammar_queue"):
            p["grammar_queue"] = _build_adaptive_grammar_queue("B2")
    elif phase == "vocab":
        if not p.get("vocab_queue"):
            p["vocab_queue"] = _build_vocab_queue(adapt)
            if int(p.get("vocab_i") or 0) > len(p["vocab_queue"]):
                p["vocab_i"] = 0
    elif phase == "reading":
        if not p.get("reading_flat"):
            p["reading_flat"] = _build_reading_flat(adapt)
            if int(p.get("reading_i") or 0) > len(p["reading_flat"]):
                p["reading_i"] = 0
    elif phase == "listening":
        if not p.get("listening_queue"):
            p["listening_queue"] = _build_listening_queue(adapt)
            if int(p.get("listening_i") or 0) > len(p["listening_queue"]):
                p["listening_i"] = 0
    elif phase == "speaking":
        if not p.get("speaking_queue"):
            p["speaking_queue"] = [s["id"] for s in SPEAKING_INTERVIEW]


def start_placement(user: dict) -> dict:
    ensure_course(user)
    p = _blank_state()
    p["phase"] = "grammar"
    p["adapt_max_level"] = "B2"
    p["grammar_queue"] = _build_adaptive_grammar_queue("B2")
    p["grammar_i"] = 0
    user["course"]["placement"] = p
    return p


def _bump(p: dict, skill: str, ok: bool, *, topic: str | None = None, level: str | None = None) -> None:
    sc = p["skill_scores"].setdefault(skill, [0, 0])
    sc[1] += 1
    if ok:
        sc[0] += 1
    if topic:
        ts = p["topic_scores"].setdefault(topic, [0, 0])
        ts[1] += 1
        if ok:
            ts[0] += 1
    if level and skill in ("grammar", "vocab", "reading", "listening"):
        w = float(LEVEL_WEIGHT.get(level) or 1.0)
        p["weight_max"][skill] = float(p["weight_max"].get(skill) or 0) + w
        if ok:
            p["weighted"][skill] = float(p["weighted"].get(skill) or 0) + w


def _note_recent(p: dict, ok: bool) -> None:
    recent = list(p.get("recent_results") or [])
    recent.append(1 if ok else 0)
    p["recent_results"] = recent[-12:]


def _maybe_adapt(p: dict) -> None:
    """Если в начале много ошибок — понижаем потолок сложности."""
    recent = p.get("recent_results") or []
    if len(recent) < 6:
        return
    ratio = sum(recent) / len(recent)
    cur = p.get("adapt_max_level") or "B2"
    if ratio < 0.35 and _level_idx(cur) > 1:
        p["adapt_max_level"] = LEVEL_ORDER[max(1, _level_idx(cur) - 1)]
    elif ratio < 0.5 and _level_idx(cur) > 2:
        p["adapt_max_level"] = LEVEL_ORDER[_level_idx(cur) - 1]
    elif ratio > 0.85 and _level_idx(cur) < 4:
        p["adapt_max_level"] = LEVEL_ORDER[min(4, _level_idx(cur) + 1)]


def current_grammar(p: dict) -> dict | None:
    """Все 40 grammar по порядку (легкие→сложные). Адаптив влияет на следующие секции."""
    q = p.get("grammar_queue") or []
    i = int(p.get("grammar_i") or 0)
    if i < 0 or i >= len(q):
        return None
    return grammar_by_id(q[i])


def answer_grammar_mcq(p: dict, choice_idx: int) -> bool:
    item = current_grammar(p)
    if not item:
        return False
    ok = int(choice_idx) == int(item.get("correct") or -1)
    _bump(p, "grammar", ok, topic=item.get("topic"), level=item.get("level"))
    _note_recent(p, ok)
    p["grammar_i"] = int(p.get("grammar_i") or 0) + 1
    _maybe_adapt(p)
    return ok


def answer_grammar_text(p: dict, text: str) -> bool:
    item = current_grammar(p)
    if not item:
        return False
    ok = answers_match(item.get("answer") or "", text, list(item.get("accept") or []))
    _bump(p, "grammar", ok, topic=item.get("topic"), level=item.get("level"))
    _note_recent(p, ok)
    p["grammar_i"] = int(p.get("grammar_i") or 0) + 1
    _maybe_adapt(p)
    return ok


def grammar_done(p: dict) -> bool:
    return int(p.get("grammar_i") or 0) >= len(p.get("grammar_queue") or [])


def begin_vocab(p: dict) -> None:
    p["phase"] = "vocab"
    p["vocab_queue"] = _build_vocab_queue(p.get("adapt_max_level") or "B2")
    p["vocab_i"] = 0


def current_vocab(p: dict) -> dict | None:
    q = p.get("vocab_queue") or []
    i = int(p.get("vocab_i") or 0)
    if i < 0 or i >= len(q):
        return None
    return vocab_by_id(q[i])


def answer_vocab(p: dict, choice_idx: int) -> bool:
    item = current_vocab(p)
    if not item:
        return False
    ok = int(choice_idx) == int(item.get("correct") or -1)
    _bump(p, "vocab", ok, topic=item.get("topic"), level=item.get("level"))
    _note_recent(p, ok)
    p["vocab_i"] = int(p.get("vocab_i") or 0) + 1
    _maybe_adapt(p)
    return ok


def vocab_done(p: dict) -> bool:
    q = p.get("vocab_queue") or []
    if not q:
        return False
    return int(p.get("vocab_i") or 0) >= len(q)


def begin_reading(p: dict) -> None:
    p["phase"] = "reading"
    p["reading_flat"] = _build_reading_flat(p.get("adapt_max_level") or "B2")
    p["reading_i"] = 0
    p["reading_last_passage"] = None


def current_reading(p: dict) -> dict | None:
    flat = p.get("reading_flat") or []
    i = int(p.get("reading_i") or 0)
    if i < 0 or i >= len(flat):
        return None
    return hydrate_reading_item(flat[i])


def answer_reading(p: dict, choice_idx: int) -> bool:
    cur = current_reading(p)
    if not cur:
        return False
    q = cur["q"]
    ok = int(choice_idx) == int(q.get("correct") or -1)
    _bump(
        p,
        "reading",
        ok,
        topic=cur.get("passage_topic"),
        level=cur.get("passage_level"),
    )
    p["reading_i"] = int(p.get("reading_i") or 0) + 1
    return ok


def reading_done(p: dict) -> bool:
    flat = p.get("reading_flat") or []
    if not flat:
        return False
    return int(p.get("reading_i") or 0) >= len(flat)


def begin_listening(p: dict) -> None:
    p["phase"] = "listening"
    p["listening_queue"] = _build_listening_queue(p.get("adapt_max_level") or "B2")
    p["listening_i"] = 0


def _listening_by_id(lid: str) -> dict | None:
    for it in LISTENING_ITEMS:
        if it["id"] == lid:
            return it
    return None


def current_listening(p: dict) -> dict | None:
    q = p.get("listening_queue") or []
    i = int(p.get("listening_i") or 0)
    if i < 0 or i >= len(q):
        return None
    return _listening_by_id(q[i])


def answer_listening(p: dict, choice_idx: int) -> bool:
    item = current_listening(p)
    if not item:
        return False
    q = item.get("question") or {}
    ok = int(choice_idx) == int(q.get("correct") or -1)
    _bump(p, "listening", ok, topic=item.get("topic"), level=item.get("level"))
    p["listening_i"] = int(p.get("listening_i") or 0) + 1
    return ok


def listening_done(p: dict) -> bool:
    q = p.get("listening_queue") or []
    if not q:
        return False
    return int(p.get("listening_i") or 0) >= len(q)


def _provisional_level(p: dict) -> str:
    scores = []
    for skill in ("grammar", "vocab", "reading", "listening"):
        got = float(p["weighted"].get(skill) or 0)
        mx = float(p["weight_max"].get(skill) or 0)
        if mx > 0:
            scores.append(got / mx)
    if not scores:
        return "A1"
    avg = sum(scores) / len(scores)
    for thr, lvl in SCORE_TO_LEVEL:
        if avg < thr:
            return lvl
    return "B2"


def begin_writing(p: dict) -> None:
    lvl = _provisional_level(p)
    if lvl not in WRITING_PROMPTS:
        lvl = "A2"
    # при слабом результате не даём B2-промпт
    if _level_idx(lvl) > _level_idx(p.get("adapt_max_level") or "B2"):
        lvl = p.get("adapt_max_level") or "A2"
    p["writing_level"] = lvl
    p["phase"] = "writing"


def score_writing(p: dict, text: str) -> float:
    meta = WRITING_PROMPTS.get(p.get("writing_level") or "A2") or WRITING_PROMPTS["A2"]
    t = (text or "").strip()
    chars = len(t)
    sentences = [x for x in re.split(r"[.!?]+", t) if x.strip()]
    n_sent = len(sentences)
    latin = len(re.findall(r"[A-Za-z]", t))
    cyr = len(re.findall(r"[А-Яа-яЁё]", t))
    latin_ratio = latin / max(1, chars)
    words = re.findall(r"[A-Za-z']+", t)
    unique = len({w.lower() for w in words})

    score = 0.0
    need_s = int(meta.get("min_sentences") or 8)
    need_c = int(meta.get("min_chars") or 120)
    if n_sent >= need_s:
        score += 0.35
    elif n_sent >= max(3, need_s - 3):
        score += 0.18
    if chars >= need_c:
        score += 0.25
    elif chars >= need_c * 0.6:
        score += 0.12
    if latin_ratio >= 0.75 and cyr < latin:
        score += 0.2
    elif latin_ratio >= 0.5:
        score += 0.08
    if unique >= 18:
        score += 0.2
    elif unique >= 10:
        score += 0.1

    # анти-бред: слишком мало разных слов
    if unique < 6 or len(words) < 12:
        score = min(score, 0.25)

    p["writing_score"] = round(min(1.0, score), 2)
    ok = score >= 0.55
    p["skill_scores"]["writing"] = [1 if ok else 0, 1]
    return p["writing_score"]


def begin_speaking(p: dict) -> None:
    p["phase"] = "speaking"
    p["speaking_queue"] = [s["id"] for s in SPEAKING_INTERVIEW]
    p["speaking_i"] = 0
    p["speaking_answers"] = 0
    p["speaking_skipped_n"] = 0
    p["speaking_transcripts"] = []


def _speaking_by_id(sid: str) -> dict | None:
    for s in SPEAKING_INTERVIEW:
        if s["id"] == sid:
            return s
    return None


def current_speaking(p: dict) -> dict | None:
    """Текущий вопрос интервью. Без фильтра по adapt — иначе тест молча зависает."""
    if int(p.get("speaking_answers") or 0) >= SPEAKING_TARGET:
        return None
    q = p.get("speaking_queue") or []
    if not q:
        q = [s["id"] for s in SPEAKING_INTERVIEW]
        p["speaking_queue"] = q
    i = int(p.get("speaking_i") or 0)
    if i < 0:
        i = 0
        p["speaking_i"] = 0
    while i < len(q):
        item = _speaking_by_id(q[i])
        if not item:
            i += 1
            p["speaking_i"] = i
            continue
        p["speaking_current_id"] = item["id"]
        return item
    return None


def advance_speaking_pointer(p: dict) -> None:
    p["speaking_i"] = int(p.get("speaking_i") or 0) + 1


def score_speaking_utterance(p: dict, transcript: str | None) -> bool:
    t = (transcript or "").strip()
    words = re.findall(r"[A-Za-z]+", t)
    ok = len(words) >= 4
    if len(words) >= 8:
        ok = True
    sc = p["skill_scores"].setdefault("speaking", [0, 0])
    sc[1] += 1
    if ok:
        sc[0] += 1
    p["speaking_answers"] = int(p.get("speaking_answers") or 0) + 1
    advance_speaking_pointer(p)
    if t:
        # без HTML-тегов — иначе parse_mode может уронить ответ
        safe = t[:240].replace("<", " ").replace(">", " ")
        p.setdefault("speaking_transcripts", []).append(safe)
    tot = max(1, sc[1])
    avg_len = sum(len(re.findall(r"[A-Za-z]+", x)) for x in (p.get("speaking_transcripts") or [])) / max(
        1, len(p.get("speaking_transcripts") or [])
    )
    p["speaking_score"] = round(min(1.0, (sc[0] / tot) * 0.75 + min(0.25, avg_len / 40)), 2)
    return ok


def skip_speaking_item(p: dict) -> None:
    sc = p["skill_scores"].setdefault("speaking", [0, 0])
    sc[1] += 1
    p["speaking_answers"] = int(p.get("speaking_answers") or 0) + 1
    p["speaking_skipped_n"] = int(p.get("speaking_skipped_n") or 0) + 1
    advance_speaking_pointer(p)
    tot = max(1, sc[1])
    p["speaking_score"] = round(sc[0] / tot * 0.7, 2)


def speaking_done(p: dict) -> bool:
    if int(p.get("speaking_answers") or 0) >= SPEAKING_TARGET:
        return True
    q = p.get("speaking_queue") or []
    if not q:
        return int(p.get("speaking_answers") or 0) > 0
    # не вызываем current_speaking — он мутирует индекс
    return int(p.get("speaking_i") or 0) >= len(q)


def can_finalize_early(p: dict) -> bool:
    """Можно завершить с текущим прогрессом (не теряя ответы)."""
    if p.get("finished"):
        return True
    phase = p.get("phase")
    if phase in ("speaking", "analyzing"):
        return int(p.get("speaking_answers") or 0) >= 8
    return False


def _skill_ratio(p: dict, skill: str) -> float | None:
    ok, tot = p["skill_scores"].get(skill) or [0, 0]
    if not tot:
        return None
    return ok / tot


def _weighted_ratio(p: dict, skill: str) -> float | None:
    mx = float((p.get("weight_max") or {}).get(skill) or 0)
    if mx <= 0:
        return _skill_ratio(p, skill)
    return float((p.get("weighted") or {}).get(skill) or 0) / mx


def _skill_attempts(p: dict, skill: str) -> tuple[int, int]:
    ok, tot = p["skill_scores"].get(skill) or [0, 0]
    try:
        return int(ok or 0), int(tot or 0)
    except (TypeError, ValueError):
        return 0, 0


def _detail_num(detail: dict, skill: str, default: float = 0.0) -> float:
    """Безопасно читать skill_details: None (не пройдено) → default."""
    v = detail.get(skill)
    if v is None:
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def finalize_placement(p: dict) -> dict:
    parts = []
    weights = {
        "grammar": 0.25,
        "vocab": 0.15,
        "reading": 0.2,
        "listening": 0.2,
        "writing": 0.1,
        "speaking": 0.1,
    }
    detail = {}
    attempts = {}
    for skill, w in weights.items():
        ok_n, tot_n = _skill_attempts(p, skill)
        attempts[skill] = [ok_n, tot_n]
        if skill == "writing":
            # если письмо не писали — не считаем как 0 в среднем «сдано»
            if tot_n <= 0 and not p.get("writing_score"):
                r = None
            else:
                r = float(p.get("writing_score") or 0)
        elif skill == "speaking":
            if tot_n <= 0 and not p.get("speaking_score"):
                r = None
            else:
                r = float(p.get("speaking_score") or 0)
        else:
            # главный источник правды — skill_scores (ok/tot)
            r = _skill_ratio(p, skill)
            if r is None:
                r = _weighted_ratio(p, skill)
        detail[skill] = None if r is None else round(float(r), 3)
        # в overall учитываем только реально пройденные секции
        if r is not None:
            parts.append(float(r) * w)

    wsum = sum(weights[s] for s, r in detail.items() if r is not None) or 1.0
    overall = (sum(parts) / wsum) if parts else 0.0
    p["overall_score"] = round(overall, 3)
    p["skill_details"] = detail
    p["skill_attempts"] = attempts

    entry = "A0"
    for thr, lvl in SCORE_TO_LEVEL:
        if overall < thr:
            entry = lvl
            break
    else:
        entry = "B2"

    # жёсткие потолки
    skipped = int(p.get("speaking_skipped_n") or 0)
    speak_n = int(p.get("speaking_answers") or 0)
    if speak_n < SPEAKING_TARGET * 0.5 or skipped >= 10:
        entry = LEVEL_ORDER[min(_level_idx(entry), _level_idx("A2"))]
    elif skipped >= 5 or _detail_num(detail, "speaking") < 0.35:
        entry = LEVEL_ORDER[min(_level_idx(entry), _level_idx("B1"))]

    # B2 только если всё достаточно ровно и speaking не провален
    if entry == "B2":
        if _detail_num(detail, "speaking") < 0.55:
            entry = "B1"
        # None (не пройдено) тоже блокирует B2
        if min(
            _detail_num(detail, "grammar"),
            _detail_num(detail, "reading"),
            _detail_num(detail, "listening"),
        ) < 0.5:
            entry = "B1"
        if skipped >= 3:
            entry = "B1"

    # если grammar/vocab совсем слабые — не выше A1/A2
    g = detail.get("grammar")
    v = detail.get("vocab")
    if g is not None and v is not None and g < 0.3 and v < 0.35:
        entry = LEVEL_ORDER[min(_level_idx(entry), _level_idx("A1"))]
    elif g is not None and g < 0.45:
        entry = LEVEL_ORDER[min(_level_idx(entry), _level_idx("A2"))]

    p["entry_level"] = entry

    # skills weak/strong — игнорируем не пройденные (None)
    taken = [(s, r) for s, r in detail.items() if r is not None]
    skill_ru_order = sorted(taken, key=lambda x: x[1])
    weak = [s for s, r in skill_ru_order if r < 0.55][:3]
    if not weak and skill_ru_order:
        weak = [skill_ru_order[0][0]]
    strong = [s for s, r in sorted(taken, key=lambda x: -x[1]) if r >= 0.7][:3]
    p["weak_skills"] = weak
    p["strong_skills"] = strong

    # topics: нужен tot >= 3, формат label: ok/tot (pct%)
    topic_ratios = []
    for topic, pair in (p.get("topic_scores") or {}).items():
        try:
            ok, tot = int(pair[0]), int(pair[1])
        except Exception:
            continue
        if tot >= 3:
            topic_ratios.append((topic, ok / tot, ok, tot))
    topic_ratios.sort(key=lambda x: x[1])
    weak_topics = []
    for topic, r, ok, tot in topic_ratios:
        if r < 0.55:
            label = TOPIC_LABELS_RU.get(topic) or topic
            weak_topics.append(f"{label}: {ok}/{tot} ({int(r*100)}%)")
        if len(weak_topics) >= 6:
            break
    strong_topics = []
    for topic, r, ok, tot in sorted(topic_ratios, key=lambda x: -x[1]):
        if r >= 0.75:
            label = TOPIC_LABELS_RU.get(topic) or topic
            strong_topics.append(f"{label}: {ok}/{tot} ({int(r*100)}%)")
        if len(strong_topics) >= 4:
            break
    p["weak_topics"] = weak_topics
    p["strong_topics"] = strong_topics

    h = float(HOURS_TO_B2.get(entry) or 0)
    weak_mult = 1.0 + 0.05 * len(weak_topics) + 0.06 * len(weak)

    def _months(mins_per_day: float) -> int:
        if h <= 0:
            return 0
        # ~22 дня занятий в месяц
        hours_per_month = (mins_per_day / 60.0) * 22.0
        m = math.ceil((h * weak_mult) / max(0.1, hours_per_month))
        return int(max(3, min(36, m)))

    p["months_45"] = _months(45)
    p["months_60"] = _months(60)
    # 60 мин/день всегда не дольше, чем 45
    if p["months_60"] > p["months_45"]:
        p["months_60"] = p["months_45"]
    p["price"] = int(PRICE_BY_LEVEL.get(entry) or 12900)
    p["start_topic_id"] = START_TOPIC.get(entry) or "A2.T1"
    p["phase"] = "done"
    p["finished"] = True
    return p


def results_html(p: dict) -> str:
    entry = p.get("entry_level") or "?"
    detail = p.get("skill_details") or {}
    skill_ru = {
        "grammar": "грамматика",
        "vocab": "лексика",
        "reading": "чтение",
        "listening": "аудирование",
        "writing": "письмо",
        "speaking": "говорение",
    }
    attempts = p.get("skill_attempts") or {}
    lines = []
    for k in ("grammar", "vocab", "reading", "listening", "writing", "speaking"):
        if k not in detail:
            continue
        r = detail[k]
        ok_n, tot_n = 0, 0
        if k in attempts:
            try:
                ok_n, tot_n = int(attempts[k][0]), int(attempts[k][1])
            except Exception:
                ok_n, tot_n = 0, 0
        if r is None or (tot_n <= 0 and k not in ("writing", "speaking")):
            lines.append(f"· {skill_ru[k]}: <b>не пройдено</b> <i>({ok_n}/{tot_n})</i>")
        else:
            pct = int(round(float(r) * 100))
            if tot_n > 0:
                lines.append(f"· {skill_ru[k]}: <b>{pct}%</b> <i>({ok_n}/{tot_n})</i>")
            else:
                lines.append(f"· {skill_ru[k]}: <b>{pct}%</b>")
    skills_block = "\n".join(lines) or "—"

    weak_topics = p.get("weak_topics") or []
    strong_topics = p.get("strong_topics") or []
    weak_s = ", ".join(skill_ru.get(x, x) for x in (p.get("weak_skills") or [])) or "—"
    strong_s = ", ".join(skill_ru.get(x, x) for x in (p.get("strong_skills") or [])) or "—"
    wt = "\n".join(f"· {x}" for x in weak_topics) or "· пока без явных провалов по темам"
    st = "\n".join(f"· {x}" for x in strong_topics) or "· уточним в курсе"
    overall = p.get("overall_score")
    overall_s = f"{int(round(float(overall)*100))}%" if overall is not None else "—"
    price = int(p.get("price") or 0)
    m45 = p.get("months_45")
    m60 = p.get("months_60")

    head = (
        "📋 <b>Результат вступительного теста</b>\n\n"
        f"Итоговый уровень входа: <b>{entry}</b>\n"
        f"Общий балл: <b>{overall_s}</b>\n\n"
        f"<b>Навыки</b>\n{skills_block}\n\n"
        f"Сильные стороны: <b>{strong_s}</b>\n"
        f"Слабые навыки: <b>{weak_s}</b>\n\n"
        f"<b>Слабые темы</b>\n{wt}\n\n"
        f"<b>Сильные темы</b>\n{st}\n\n"
    )

    if entry == "B2" and price <= 0:
        return head + (
            "Курс «путь до B2» как основной пакет не обязателен — "
            "можно качать навыки в уроках и общении с Рико."
        )

    return (
        head
        + f"Старт программы: тема <code>{p.get('start_topic_id')}</code>\n\n"
        f"⏱ До B2 ориентировочно:\n"
        f"· ~45 мин/день → <b>~{m45} мес</b>\n"
        f"· ~60 мин/день → <b>~{m60} мес</b>\n\n"
        f"💳 Курс с твоего уровня: <b>{price}₽</b>\n"
        "<i>полный путь до B2 под твои слабые места</i>"
    )


def progress_label(p: dict) -> str:
    names = {
        "grammar": "Грамматика",
        "vocab": "Словарь",
        "reading": "Чтение",
        "listening": "Аудирование",
        "writing": "Письмо",
        "speaking": "Собеседование",
        "analyzing": "Анализ",
        "done": "Готово",
    }
    return names.get(p.get("phase") or "", p.get("phase") or "")


def grammar_progress(p: dict) -> tuple[int, int]:
    return int(p.get("grammar_i") or 0) + 1, len(p.get("grammar_queue") or [])


def vocab_progress(p: dict) -> tuple[int, int]:
    return int(p.get("vocab_i") or 0) + 1, len(p.get("vocab_queue") or [])


def reading_progress(p: dict) -> tuple[int, int]:
    return int(p.get("reading_i") or 0) + 1, len(p.get("reading_flat") or [])


def listening_progress(p: dict) -> tuple[int, int]:
    return int(p.get("listening_i") or 0) + 1, len(p.get("listening_queue") or [])


PROCESSING_STEPS = [
    "🦜 Рико обрабатывает лексику…",
    "🦜 Рико обрабатывает грамматику…",
    "🦜 Рико обрабатывает чтение…",
    "🦜 Рико обрабатывает аудирование…",
    "🦜 Рико обрабатывает письмо…",
    "🦜 Рико обрабатывает говорение…",
    "🦜 Рико собирает слабые темы…",
    "🦜 Почти готово — считаю итоговый уровень…",
]