"""
Вступительный placement-тест курса «до B2».

Логика близка к Cambridge CEPT (~30 мин):
1) Language Knowledge (2 раунда MCQ, адаптивный второй раунд)
2) Reading
3) Listening (+ TTS)
4) Writing
5) Speaking (голос + STT)

Результат: CEFR A0–B2, weak/strong skills, старт темы, срок, цена.
"""

from __future__ import annotations

import re
from typing import Any

from data.course_placement_bank import (
    LEVEL_ORDER,
    LISTENING,
    LK_ROUND1_IDS,
    LK_ROUND2_HIGH_IDS,
    LK_ROUND2_LOW_IDS,
    READING,
    SPEAKING,
    WRITING,
    lk_by_id,
    nearest_listening_level,
    nearest_reading_level,
)

BTN_COURSES = "🎓 Курсы"


def courses_allowed(user_id: str | int | None) -> bool:
    """Пока раздел только для менеджера (превью до публичного запуска)."""
    if user_id is None:
        return False
    from config import MANAGER_ID

    try:
        return int(user_id) == int(MANAGER_ID)
    except (TypeError, ValueError):
        return False

BTN_COURSE_START_TEST = "▶️ Пройти вступительный тест"
BTN_COURSE_CONTINUE = "▶️ Продолжить тест"
BTN_COURSE_RESULTS = "📋 Мой результат теста"
BTN_COURSE_BUY = "💳 Купить курс"
BTN_COURSE_ABOUT = "ℹ️ Как устроен курс"
BTN_SKIP_SPEAKING = "⏭ Пропустить говорение"

INTRO_HTML = (
    "🎓 <b>Курс LexDAN · путь до B2</b>\n\n"
    "Персональная программа от твоего уровня до уверенного B2.\n"
    "Рико ведёт как репетитор: тема → практика → экзамен (≥80%), "
    "без прыжков вперёд.\n\n"
    "Сначала — <b>вступительный тест</b> (ориентир Cambridge Placement):\n"
    "· язык (грамматика + лексика)\n"
    "· чтение\n"
    "· аудирование\n"
    "· письмо\n"
    "· говорение\n\n"
    "⏱ Обычно <b>25–35 минут</b>. Можно сделать паузу и продолжить позже.\n"
    "По результату покажем уровень, слабые места, срок и цену."
)

PRICE_BY_LEVEL = {
    "A0": 14900,
    "A1": 12900,
    "A2": 10900,
    "B1": 9900,
    "B2": 0,  # курс «до B2» не нужен
}

HOURS_TO_B2 = {
    "A0": 550,
    "A1": 450,
    "A2": 320,
    "B1": 200,
    "B2": 0,
}

# Старт программы (id тем — логические; контент тем подключим позже)
START_TOPIC = {
    "A0": "A0.T1",
    "A1": "A1.T1",
    "A2": "A2.T1",
    "B1": "B1.T1",
    "B2": "DONE",
}

LEVEL_POINTS = {"A0": 1, "A1": 2, "A2": 3, "B1": 4, "B2": 5}


def _blank_state() -> dict:
    return {
        "phase": None,  # intro|lk1|lk2|reading|listening|writing|speaking|done
        "lk_ids": [],
        "lk_i": 0,
        "lk_correct": 0,
        "lk_answered": 0,
        "lk_by_skill": {"grammar": [0, 0], "vocab": [0, 0]},  # ok, total
        "skill_scores": {
            "grammar": [0, 0],
            "vocab": [0, 0],
            "reading": [0, 0],
            "listening": [0, 0],
            "writing": [0, 0],
            "speaking": [0, 0],
        },
        "provisional": "A2",
        "reading_level": "A2",
        "reading_i": 0,
        "listening_level": "A2",
        "listening_i": 0,
        "listening_script": "",
        "writing_level": "A2",
        "speaking_level": "A2",
        "speaking_i": 0,
        "entry_level": None,
        "weak_skills": [],
        "strong_skills": [],
        "months_45": None,
        "months_60": None,
        "price": None,
        "start_topic_id": None,
        "finished": False,
    }


def ensure_course(user: dict) -> dict:
    if "course" not in user or not isinstance(user.get("course"), dict):
        user["course"] = {
            "placement": _blank_state(),
            "purchased": False,
            "active": False,
        }
    user["course"].setdefault("purchased", False)
    user["course"].setdefault("active", False)
    if "placement" not in user["course"] or not isinstance(
        user["course"]["placement"], dict
    ):
        user["course"]["placement"] = _blank_state()
    else:
        blank = _blank_state()
        for k, v in blank.items():
            user["course"]["placement"].setdefault(k, v)
    return user


def placement(user: dict) -> dict:
    ensure_course(user)
    return user["course"]["placement"]


def start_placement(user: dict) -> dict:
    ensure_course(user)
    p = _blank_state()
    p["phase"] = "lk1"
    p["lk_ids"] = list(LK_ROUND1_IDS)
    p["lk_i"] = 0
    user["course"]["placement"] = p
    return p


def current_lk_item(p: dict) -> dict | None:
    ids = p.get("lk_ids") or []
    i = int(p.get("lk_i") or 0)
    if i < 0 or i >= len(ids):
        return None
    return lk_by_id(ids[i])


def _bump_skill(p: dict, skill: str, ok: bool) -> None:
    sc = p["skill_scores"].setdefault(skill, [0, 0])
    sc[1] += 1
    if ok:
        sc[0] += 1
    if skill in ("grammar", "vocab"):
        lv = p["lk_by_skill"].setdefault(skill, [0, 0])
        lv[1] += 1
        if ok:
            lv[0] += 1


def answer_lk(p: dict, choice_idx: int) -> tuple[bool, str]:
    item = current_lk_item(p)
    if not item:
        return False, "Нет текущего вопроса."
    ok = int(choice_idx) == int(item["correct"])
    _bump_skill(p, item.get("skill") or "grammar", ok)
    p["lk_answered"] = int(p.get("lk_answered") or 0) + 1
    if ok:
        p["lk_correct"] = int(p.get("lk_correct") or 0) + 1
    p["lk_i"] = int(p.get("lk_i") or 0) + 1
    return ok, "ok"


def lk_round_done(p: dict) -> bool:
    return int(p.get("lk_i") or 0) >= len(p.get("lk_ids") or [])


def after_lk1_choose_round2(p: dict) -> None:
    """Адаптивный второй раунд как в CEPT: ниже/выше по результатам 1-го."""
    total = max(1, int(p.get("lk_answered") or 1))
    ratio = int(p.get("lk_correct") or 0) / total
    if ratio < 0.45:
        p["lk_ids"] = list(LK_ROUND2_LOW_IDS)
        p["provisional"] = "A1"
    elif ratio < 0.7:
        p["lk_ids"] = list(LK_ROUND2_LOW_IDS[:3] + LK_ROUND2_HIGH_IDS[:3])
        p["provisional"] = "A2"
    else:
        p["lk_ids"] = list(LK_ROUND2_HIGH_IDS)
        p["provisional"] = "B1"
    p["lk_i"] = 0
    p["phase"] = "lk2"


def provisional_from_lk(p: dict) -> str:
    """Грубая оценка после всех LK (вес по уровню задания)."""
    # Используем уже накопленные ответы: пересчитаем по id нельзя — храним score proxy
    correct = int(p.get("lk_correct") or 0)
    answered = max(1, int(p.get("lk_answered") or 1))
    ratio = correct / answered
    if ratio < 0.25:
        lvl = "A0"
    elif ratio < 0.4:
        lvl = "A1"
    elif ratio < 0.58:
        lvl = "A2"
    elif ratio < 0.75:
        lvl = "B1"
    else:
        lvl = "B2"
    p["provisional"] = lvl
    return lvl


def begin_reading(p: dict) -> None:
    lvl = nearest_reading_level(provisional_from_lk(p))
    p["reading_level"] = lvl
    p["reading_i"] = 0
    p["phase"] = "reading"


def current_reading_q(p: dict) -> tuple[dict, dict] | None:
    block = READING.get(p.get("reading_level") or "A2") or READING["A2"]
    qs = block["questions"]
    i = int(p.get("reading_i") or 0)
    if i >= len(qs):
        return None
    return block, qs[i]


def answer_reading(p: dict, choice_idx: int) -> bool:
    cur = current_reading_q(p)
    if not cur:
        return False
    _block, q = cur
    ok = int(choice_idx) == int(q["correct"])
    _bump_skill(p, "reading", ok)
    p["reading_i"] = int(p.get("reading_i") or 0) + 1
    return ok


def reading_done(p: dict) -> bool:
    block = READING.get(p.get("reading_level") or "A2") or READING["A2"]
    return int(p.get("reading_i") or 0) >= len(block["questions"])


def begin_listening(p: dict) -> None:
    lvl = nearest_listening_level(p.get("provisional") or "A2")
    # подстроить по reading
    r_ok, r_tot = p["skill_scores"].get("reading") or [0, 0]
    if r_tot and (r_ok / r_tot) < 0.4:
        idx = max(0, LEVEL_ORDER.index(lvl) - 1)
        lvl = LEVEL_ORDER[idx]
    elif r_tot and (r_ok / r_tot) > 0.85:
        idx = min(len(LEVEL_ORDER) - 1, LEVEL_ORDER.index(lvl) + 1)
        lvl = LEVEL_ORDER[idx]
    block = LISTENING.get(lvl) or LISTENING["A2"]
    p["listening_level"] = lvl
    p["listening_script"] = block["script"]
    p["listening_i"] = 0
    p["phase"] = "listening"


def current_listening_q(p: dict) -> dict | None:
    block = LISTENING.get(p.get("listening_level") or "A2") or LISTENING["A2"]
    qs = block["questions"]
    i = int(p.get("listening_i") or 0)
    if i >= len(qs):
        return None
    return qs[i]


def answer_listening(p: dict, choice_idx: int) -> bool:
    q = current_listening_q(p)
    if not q:
        return False
    ok = int(choice_idx) == int(q["correct"])
    _bump_skill(p, "listening", ok)
    p["listening_i"] = int(p.get("listening_i") or 0) + 1
    return ok


def listening_done(p: dict) -> bool:
    block = LISTENING.get(p.get("listening_level") or "A2") or LISTENING["A2"]
    return int(p.get("listening_i") or 0) >= len(block["questions"])


def begin_writing(p: dict) -> None:
    lvl = p.get("provisional") or "A2"
    p["writing_level"] = lvl if lvl in WRITING else "A2"
    p["phase"] = "writing"


def score_writing(p: dict, text: str) -> float:
    """0..1 по длине/предложениям (без GPT)."""
    meta = WRITING.get(p.get("writing_level") or "A2") or WRITING["A2"]
    t = (text or "").strip()
    chars = len(t)
    sentences = max(1, len([x for x in re.split(r"[.!?]+", t) if x.strip()]))
    # латиница
    latin = len(re.findall(r"[A-Za-z]", t))
    latin_ratio = latin / max(1, chars)

    score = 0.0
    if chars >= int(meta["min_chars"]):
        score += 0.45
    elif chars >= int(meta["min_chars"]) * 0.6:
        score += 0.25
    if sentences >= int(meta["min_sentences"]):
        score += 0.35
    elif sentences >= max(1, int(meta["min_sentences"]) - 2):
        score += 0.2
    if latin_ratio >= 0.7:
        score += 0.2
    elif latin_ratio >= 0.45:
        score += 0.1

    ok = score >= 0.55
    # пишем как ok/total в долях: используем 1 attempt
    p["skill_scores"]["writing"] = [1 if ok else 0, 1]
    # сохраним сырой score для тонкой настройки уровня
    p["writing_score"] = round(score, 2)
    return score


def begin_speaking(p: dict) -> None:
    lvl = p.get("provisional") or "A2"
    p["speaking_level"] = lvl if lvl in SPEAKING else "A2"
    p["speaking_i"] = 0
    p["phase"] = "speaking"


def current_speaking(p: dict) -> dict | None:
    items = SPEAKING.get(p.get("speaking_level") or "A2") or SPEAKING["A2"]
    i = int(p.get("speaking_i") or 0)
    if i >= len(items):
        return None
    return items[i]


def score_speaking_utterance(p: dict, transcript: str | None) -> bool:
    """Простая проверка: есть распознанный английский текст."""
    t = (transcript or "").strip()
    words = re.findall(r"[A-Za-z]+", t)
    ok = len(words) >= 3 or (len(words) >= 1 and len(t) >= 8)
    sc = p["skill_scores"].setdefault("speaking", [0, 0])
    sc[1] += 1
    if ok:
        sc[0] += 1
    p["speaking_i"] = int(p.get("speaking_i") or 0) + 1
    return ok


def skip_speaking_item(p: dict) -> None:
    sc = p["skill_scores"].setdefault("speaking", [0, 0])
    sc[1] += 1
    p["speaking_i"] = int(p.get("speaking_i") or 0) + 1


def speaking_done(p: dict) -> bool:
    items = SPEAKING.get(p.get("speaking_level") or "A2") or SPEAKING["A2"]
    return int(p.get("speaking_i") or 0) >= len(items)


def _skill_ratio(p: dict, skill: str) -> float | None:
    ok, tot = p["skill_scores"].get(skill) or [0, 0]
    if not tot:
        return None
    return ok / tot


def finalize_placement(p: dict) -> dict:
    """Итоговый CEFR + слабые/сильные + оффер."""
    base = p.get("provisional") or "A2"
    idx = LEVEL_ORDER.index(base) if base in LEVEL_ORDER else 2

    # корректировки по skills
    adjustments = 0
    for skill, thr_low, thr_high, delta in (
        ("reading", 0.34, 0.85, 1),
        ("listening", 0.34, 0.85, 1),
        ("writing", 0.45, 0.85, 1),
        ("speaking", 0.4, 0.85, 1),
    ):
        r = _skill_ratio(p, skill)
        if r is None:
            continue
        if r < thr_low:
            adjustments -= 1
        elif r >= thr_high:
            adjustments += 0  # не раздуваем выше базы слишком легко

    # writing_score тонкая подстройка
    ws = float(p.get("writing_score") or 0)
    if ws and ws < 0.4:
        adjustments -= 1
    elif ws >= 0.85:
        adjustments += 1

    # LK overall
    lk_r = int(p.get("lk_correct") or 0) / max(1, int(p.get("lk_answered") or 1))
    if lk_r < 0.3:
        adjustments -= 1
    elif lk_r >= 0.85:
        adjustments += 1

    idx = max(0, min(len(LEVEL_ORDER) - 1, idx + max(-2, min(2, adjustments))))
    entry = LEVEL_ORDER[idx]
    p["entry_level"] = entry

    # weak / strong
    ratios: list[tuple[str, float]] = []
    for skill in ("grammar", "vocab", "reading", "listening", "writing", "speaking"):
        r = _skill_ratio(p, skill)
        if r is None:
            continue
        ratios.append((skill, r))
    ratios.sort(key=lambda x: x[1])
    weak = [s for s, r in ratios if r < 0.6][:2]
    if not weak and ratios:
        weak = [ratios[0][0]]
    strong = [s for s, r in sorted(ratios, key=lambda x: -x[1]) if r >= 0.75][:2]
    p["weak_skills"] = weak
    p["strong_skills"] = strong

    # срок
    h = float(HOURS_TO_B2.get(entry) or 0)
    weak_mult = 1.0
    for w in weak:
        weak_mult += {
            "grammar": 0.08,
            "vocab": 0.04,
            "reading": 0.04,
            "listening": 0.1,
            "writing": 0.06,
            "speaking": 0.1,
        }.get(w, 0.05)
    import math

    def _months(hours_per_month: float) -> int:
        if h <= 0:
            return 0
        m = math.ceil((h * weak_mult) / hours_per_month)
        return int(max(4, min(16, m)))

    p["months_45"] = _months(22)  # ~45 мин/день
    p["months_60"] = _months(30)  # ~60 мин/день
    p["price"] = int(PRICE_BY_LEVEL.get(entry) or 12900)
    p["start_topic_id"] = START_TOPIC.get(entry) or "A2.T1"
    p["phase"] = "done"
    p["finished"] = True
    return p


def results_html(p: dict) -> str:
    entry = p.get("entry_level") or "?"
    weak = p.get("weak_skills") or []
    strong = p.get("strong_skills") or []
    skill_ru = {
        "grammar": "грамматика",
        "vocab": "лексика",
        "reading": "чтение",
        "listening": "аудирование",
        "writing": "письмо",
        "speaking": "говорение",
    }
    weak_s = ", ".join(skill_ru.get(x, x) for x in weak) or "пока ровно"
    strong_s = ", ".join(skill_ru.get(x, x) for x in strong) or "ещё уточним в курсе"
    price = int(p.get("price") or 0)
    m45 = p.get("months_45")
    m60 = p.get("months_60")

    if entry == "B2" and price <= 0:
        return (
            "📋 <b>Результат вступительного теста</b>\n\n"
            f"Уровень: <b>B2</b> (уже около цели курса)\n"
            f"Сильные стороны: <b>{strong_s}</b>\n"
            f"Зоны роста: <b>{weak_s}</b>\n\n"
            "Курс «путь до B2» тебе как основной пакет не обязателен — "
            "можешь качать навыки в обычных уроках и общении с Рико."
        )

    return (
        "📋 <b>Результат вступительного теста</b>\n\n"
        f"Уровень входа: <b>{entry}</b>\n"
        f"Сильные стороны: <b>{strong_s}</b>\n"
        f"Слабые места: <b>{weak_s}</b>\n"
        f"Старт программы: тема <code>{p.get('start_topic_id')}</code>\n\n"
        f"⏱ До B2 ориентировочно:\n"
        f"· ~45 мин/день → <b>~{m45} мес</b>\n"
        f"· ~60 мин/день → <b>~{m60} мес</b>\n\n"
        f"💳 Курс с твоего уровня: <b>{price:,}₽</b>\n"
        "<i>(полный путь до B2, персональный план под слабые места)</i>\n\n"
        "Оплату курса подключим на следующем шаге — "
        "сейчас можно сохранить результат и вернуться."
    ).replace(",", " ")


def progress_label(p: dict) -> str:
    phase = p.get("phase") or ""
    names = {
        "lk1": "Язык · раунд 1",
        "lk2": "Язык · раунд 2",
        "reading": "Чтение",
        "listening": "Аудирование",
        "writing": "Письмо",
        "speaking": "Говорение",
        "done": "Готово",
    }
    return names.get(phase, phase)
