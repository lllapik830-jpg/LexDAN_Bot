"""
Собрать фиксированные Reading-пакеты для всех тем/уровней.
Запуск: python scripts/build_reading_packs.py
"""

from __future__ import annotations

import hashlib
import pprint
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data.reading_topics import READING_TOPICS  # noqa: E402
from services.reading_gen import (  # noqa: E402
    _fallback_cafe,
    _fallback_family,
    _fallback_food,
    _fallback_home,
    _fallback_weather,
    _pack,
    _pack_structurally_ok,
)

_GAP_RE = re.compile(r"\((\d)\)___")


def _seed(level: str, topic_id: str) -> int:
    h = hashlib.md5(f"{level}:{topic_id}".encode()).hexdigest()
    return int(h[:8], 16)


def _names(seed: int) -> tuple[str, str]:
    a = ["Mia", "Leo", "Anna", "Tom", "Sara", "Ben", "Lena", "Omar", "Nora", "Dana", "Victor", "Kate"]
    b = ["Alex", "Sam", "Rita", "Nick", "Eva", "Max", "Olga", "Ivan", "Nina", "Paul", "Helen", "Chris"]
    return a[seed % len(a)], b[(seed // 7) % len(b)]


def _day(seed: int) -> str:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[seed % 7]


def _build_unique(level: str, topic: dict) -> dict:
    """Уникальный текст на тему: пропуски однозначны, возраст не gap-ится."""
    tid = topic["id"]
    title = topic.get("title_en") or "Topic"
    focus = topic.get("focus") or title
    seed = _seed(level, tid)
    rng = random.Random(seed)
    n0, n1 = _names(seed)
    day = _day(seed)
    place = rng.choice(["library", "café", "park", "school", "office", "museum"])
    alt_place = "museum" if place != "museum" else "cinema"
    reason = rng.choice(["sunny", "quiet", "warm", "free"])
    distractor = rng.choice(["purple", "winter", "zebra", "silent", "heavy"])
    pay = rng.choice(["three", "four", "five", "six"])
    bag = rng.choice(["bag", "backpack", "folder"])

    if level.upper() in {"A0", "A1"}:
        full = (
            f"{n0} reads a short text about {title}. "
            f"The text focuses on {focus}. "
            f"{n0} makes a plan before practice. "
            f"At ten {n0} meets {n1} near the {place}. "
            f"{n1} wants to visit a {alt_place}, but {n0} prefers the {place}. "
            f"In the end they choose the {place} because it is {reason}. "
            f"They buy water and sit for half an hour. "
            f"{n0} pays {pay} pounds for the drinks. "
            f"{n1} takes notes and sends one photo to family. "
            f"They agree to meet again next {day} and {n0} puts the notes in a {bag}. "
            f"Before leaving, {n1} checks the time on a phone."
        )
        gaps = (
            f"{n0} reads a short text about {title}. "
            f"The text focuses on {focus}. "
            f"{n0} makes a (1)___ before practice. "
            f"At ten {n0} meets {n1} near the {place}. "
            f"{n1} wants to visit a {alt_place}, but {n0} prefers the {place}. "
            f"In the end they choose the {place} because it is (2)___. "
            f"They buy water and sit for half an hour. "
            f"{n0} pays {pay} pounds for the drinks. "
            f"{n1} takes notes and sends one photo to family. "
            f"They agree to meet again next (3)___ and {n0} puts the notes in a (4)___. "
            f"Before leaving, {n1} checks the time on a (5)___."
        )
        answers = ["plan", reason, day, bag, "phone"]
        bank = answers + [distractor if distractor not in answers else "zebra"]
        questions = [
            {
                "q": f"What is {n0}'s text about?",
                "accept": [title, title.lower()],
                "hint_ru": "О чём текст в начале?",
                "quote": f"…text about {title}.",
                "model_en": f"The text is about {title}.",
            },
            {
                "q": f"What time does {n0} meet {n1}?",
                "accept": ["ten", "10", "at ten"],
                "hint_ru": "Во сколько они встречаются?",
                "quote": f"At ten {n0} meets {n1}…",
                "model_en": f"{n0} meets {n1} at ten.",
            },
            {
                "q": f"Why do they choose the {place}?",
                "accept": [reason, f"it is {reason}", f"because it is {reason}"],
                "hint_ru": "Почему они выбирают это место?",
                "quote": f"…because it is {reason}.",
                "model_en": f"They choose the {place} because it is {reason}.",
            },
            {
                "q": "When do they agree to meet again?",
                "accept": [f"next {day}", day],
                "hint_ru": "Когда следующая встреча?",
                "quote": f"…meet again next {day}…",
                "model_en": f"They agree to meet again next {day}.",
            },
        ]
        plan = [
            f"Topic of the text ({title})",
            f"Meeting near the {place}",
            "Why they stay there",
            "Payment and next day",
        ]
        facts = [
            f"{n0} reads about {title} ({focus}).",
            f"They meet at ten near the {place}.",
            f"They choose it because it is {reason}.",
            f"{n0} pays {pay} pounds; next meeting is {day}.",
        ]
        return _pack(full, gaps, answers, bank, questions, plan, facts)

    if level.upper() in {"A2", "B1"}:
        next_day = _day(seed + 3)
        full = (
            f"Last week {n0} prepared a short presentation about {title}. "
            f"Examples were related to {focus}. "
            f"{n0} made a clear plan before writing. "
            f"On Tuesday {n0} met {n1} in the city {place}. "
            f"{n1} wanted a {alt_place} first, but {n0} preferred the quiet {place}. "
            f"They stayed because it was raining outside. "
            f"They worked for two hours and shared water. "
            f"{n0} paid {pay} pounds for printing. "
            f"{n1} saved the notes on a laptop. "
            f"They agreed to practise again next {next_day} and {n0} put the printouts in a {bag}. "
            f"Before leaving, {n1} locked the laptop in a bag."
        )
        gaps = (
            f"Last week {n0} prepared a short presentation about {title}. "
            f"Examples were related to {focus}. "
            f"{n0} made a clear (1)___ before writing. "
            f"On Tuesday {n0} met {n1} in the city {place}. "
            f"{n1} wanted a {alt_place} first, but {n0} preferred the quiet {place}. "
            f"They stayed because it was (2)___ outside. "
            f"They worked for two hours and shared water. "
            f"{n0} paid {pay} pounds for printing. "
            f"{n1} saved the notes on a laptop. "
            f"They agreed to practise again next (3)___ and {n0} put the printouts in a (4)___. "
            f"Before leaving, {n1} locked the (5)___ in a bag."
        )
        answers = ["plan", "raining", next_day, bag, "laptop"]
        bank = answers + [distractor if distractor not in answers else "sunny"]
        questions = [
            {
                "q": f"What was {n0}'s presentation about?",
                "accept": [title, title.lower()],
                "hint_ru": "О чём презентация?",
                "quote": f"…presentation about {title}.",
                "model_en": f"The presentation was about {title}.",
            },
            {
                "q": "Why did they stay?",
                "accept": ["raining", "because it was raining", "rain"],
                "hint_ru": "Почему они остались?",
                "quote": "…because it was raining outside.",
                "model_en": "They stayed because it was raining outside.",
            },
            {
                "q": f"How much did {n0} pay for printing?",
                "accept": [f"{pay} pounds", pay],
                "hint_ru": "Сколько заплатили за печать?",
                "quote": f"{n0} paid {pay} pounds for printing.",
                "model_en": f"{n0} paid {pay} pounds for printing.",
            },
            {
                "q": "When will they practise again?",
                "accept": [f"next {next_day}", next_day],
                "hint_ru": "Когда следующая практика?",
                "quote": f"…practise again next {next_day}…",
                "model_en": f"They will practise again next {next_day}.",
            },
        ]
        plan = [
            f"Presentation topic ({title})",
            f"Meeting at the {place}",
            "Why they stayed",
            "Payment and next practice",
        ]
        facts = [
            f"{n0} presented about {title}.",
            "It was raining, so they stayed.",
            f"{n0} paid {pay} pounds for printing.",
            f"Next practice is {next_day}.",
        ]
        return _pack(full, gaps, answers, bank, questions, plan, facts)

    # B2+
    next_day = _day(seed + 5)
    full = (
        f"For a seminar on {title}, {n0} drafted a brief analysis linked to {focus}. "
        f"{n0} outlined a careful plan before drafting. "
        f"On Wednesday {n0} joined {n1} at a quiet coworking space. "
        f"{n1} suggested a noisy café, but {n0} insisted on the coworking space. "
        f"They stayed because the café was overcrowded and loud. "
        f"After three focused hours they summarised the key arguments. "
        f"{n0} paid twelve pounds for day passes. "
        f"{n1} uploaded the shared document. "
        f"They scheduled a follow-up next {next_day} and {n0} filed printouts in a portfolio. "
        f"Before leaving, {n1} switched off a tablet."
    )
    gaps = (
        f"For a seminar on {title}, {n0} drafted a brief analysis linked to {focus}. "
        f"{n0} outlined a careful (1)___ before drafting. "
        f"On Wednesday {n0} joined {n1} at a quiet coworking space. "
        f"{n1} suggested a noisy café, but {n0} insisted on the coworking space. "
        f"They stayed because the café was overcrowded and (2)___. "
        f"After three focused hours they summarised the key arguments. "
        f"{n0} paid twelve pounds for day passes. "
        f"{n1} uploaded the shared document. "
        f"They scheduled a follow-up next (3)___ and {n0} filed printouts in a (4)___. "
        f"Before leaving, {n1} switched off a (5)___."
    )
    answers = ["plan", "loud", next_day, "portfolio", "tablet"]
    bank = answers + [distractor if distractor not in answers else "silent"]
    questions = [
        {
            "q": "What seminar topic was being prepared?",
            "accept": [title, title.lower()],
            "hint_ru": "Тема семинара?",
            "quote": f"For a seminar on {title}…",
            "model_en": f"The seminar was on {title}.",
        },
        {
            "q": "Why did they stay at the coworking space?",
            "accept": ["loud", "overcrowded", "café was overcrowded and loud"],
            "hint_ru": "Почему коворкинг?",
            "quote": "…overcrowded and loud.",
            "model_en": "They stayed because the café was overcrowded and loud.",
        },
        {
            "q": f"How much did {n0} pay?",
            "accept": ["twelve pounds", "12 pounds", "12"],
            "hint_ru": "Сколько заплатили?",
            "quote": f"{n0} paid twelve pounds…",
            "model_en": f"{n0} paid twelve pounds for day passes.",
        },
        {
            "q": "When is the follow-up?",
            "accept": [f"next {next_day}", next_day],
            "hint_ru": "Когда follow-up?",
            "quote": f"…follow-up next {next_day}…",
            "model_en": f"The follow-up is next {next_day}.",
        },
    ]
    plan = [
        f"Seminar topic ({title})",
        "Workplace choice",
        "Work session",
        "Payment and follow-up",
    ]
    facts = [
        f"Seminar on {title}; focus {focus}.",
        "Café was loud; they used coworking.",
        f"{n0} paid twelve pounds.",
        f"Follow-up next {next_day}.",
    ]
    return _pack(full, gaps, answers, bank, questions, plan, facts)


def _pick(level: str, topic: dict) -> dict:
    tid = (topic.get("id") or "").lower()
    title = (topic.get("title_en") or "").lower()
    if "cafe" in tid or "café" in title or "cafe" in title:
        return _fallback_cafe()
    if "family" in tid or "family" in title:
        return _fallback_family()
    if tid == "food" or title.strip() == "food":
        return _fallback_food()
    if tid == "home" or title.strip() == "home":
        return _fallback_home()
    if "weather" in tid or "weather" in title:
        return _fallback_weather()
    return _build_unique(level, topic)


def _freeze(pack: dict) -> dict:
    """Стабильный порядок word_bank (answers + distractor), без shuffle."""
    answers = list(pack["answers"])
    bank = list(pack["word_bank"])
    need = {a.lower() for a in answers}
    extra = next((w for w in bank if w.lower() not in need), "purple")
    return {
        "full_text": pack["full_text"],
        "gapped_text": pack["gapped_text"],
        "answers": answers,
        "word_bank": answers + [extra],
        "questions": pack["questions"],
        "plan": pack["plan"],
        "facts": pack["facts"],
    }


def main() -> None:
    packs: dict[str, dict[str, dict]] = {}
    bad = []
    for level, topics in READING_TOPICS.items():
        packs[level] = {}
        for t in topics:
            p = _freeze(_pick(level, t))
            reason = _pack_structurally_ok(p)
            if reason:
                bad.append((level, t["id"], reason))
            packs[level][t["id"]] = p

    out = ROOT / "data" / "reading_packs.py"
    header = '''"""Фиксированные Reading-пакеты: все уровни и темы.

Сгенерировано scripts/build_reading_packs.py — править вручную можно,
но проще пересобрать скриптом после правок шаблонов.
В рантайме GPT для текстов не вызывается.
"""

from __future__ import annotations

READING_PACKS: dict[str, dict[str, dict]] = '''
    body = pprint.pformat(packs, width=100, sort_dicts=False)
    footer = '''


def get_reading_pack(level: str, topic_id: str) -> dict | None:
    lvl = (level or "A1").upper()
    tid = (topic_id or "").strip()
    block = READING_PACKS.get(lvl) or {}
    pack = block.get(tid)
    if not pack:
        return None
    # копия + shuffle банка на вызывающей стороне
    return {
        "full_text": pack["full_text"],
        "gapped_text": pack["gapped_text"],
        "answers": list(pack["answers"]),
        "word_bank": list(pack["word_bank"]),
        "questions": [dict(q) for q in pack["questions"]],
        "plan": list(pack["plan"]),
        "facts": list(pack["facts"]),
    }
'''
    out.write_text(header + body + footer, encoding="utf-8")
    print(f"wrote {out} topics={sum(len(v) for v in packs.values())} bad={bad}")


if __name__ == "__main__":
    main()
