"""Генерация Reading-пакета: текст, пропуски, вопросы, план пересказа."""

from __future__ import annotations

import logging
import random
import re

log = logging.getLogger(__name__)


def _fallback_pack(level: str, topic: dict) -> dict:
    title = topic.get("title_en") or "Topic"
    # Кафе-пример как в ТЗ, на английском
    if "cafe" in (topic.get("id") or "") or "café" in title.lower() or "cafe" in title.lower():
        full = (
            "Michael and Anna met at a café at 2 p.m. "
            "Michael ordered a cup of coffee and a piece of chocolate cake. "
            "Anna ordered green tea and a fruit salad. "
            "They talked about their plans for the weekend. "
            "In the end they decided to go to the cinema first and then walk in the park. "
            "Michael paid for the order — 15 pounds. "
            "Anna preferred quiet weekends with books, but today she wanted something fun. "
            "Michael wanted to try a new film and then get some fresh air. "
            "The café was busy, but their table near the window was free. "
            "They left happy and already planned to meet again next Saturday."
        )
        gaps = (
            "Michael and Anna (1)___ at a café at 2 p.m. "
            "Michael ordered a cup of coffee and a (2)___ of chocolate cake. "
            "Anna ordered green tea and a (3)___ salad. "
            "They talked about their (4)___ for the weekend. "
            "In the end they decided to go to the cinema first and then (5)___ in the park. "
            "Michael paid for the order — 15 pounds. "
            "Anna preferred quiet weekends with books, but today she wanted something fun. "
            "Michael wanted to try a new film and then get some fresh air. "
            "The café was busy, but their table near the window was free. "
            "They left happy and already planned to meet again next Saturday."
        )
        answers = ["met", "piece", "fruit", "plans", "walk"]
        bank = ["met", "piece", "fruit", "plans", "walk", "red"]
        questions = [
            {
                "q": "How much did Michael's order cost?",
                "accept": ["15 pounds", "15", "fifteen pounds", "£15"],
                "hint_ru": "Найди в тексте сумму, которую заплатил Майкл.",
                "quote": "Michael paid for the order — 15 pounds.",
            },
            {
                "q": "What kind of weekends did Anna usually prefer?",
                "accept": ["quiet weekends with books", "quiet", "books", "reading"],
                "hint_ru": "Что Анна обычно предпочитала делать на выходных?",
                "quote": "Anna preferred quiet weekends with books…",
            },
            {
                "q": "What time did the friends meet?",
                "accept": ["2 p.m.", "2 pm", "2", "two", "at 2"],
                "hint_ru": "Во сколько друзья встретились?",
                "quote": "…met at a café at 2 p.m.",
            },
            {
                "q": "What did Michael want to do after the cinema?",
                "accept": ["walk in the park", "get fresh air", "park", "fresh air"],
                "hint_ru": "Что Майкл хотел сделать после кино?",
                "quote": "…then walk in the park / get some fresh air.",
            },
        ]
        plan = [
            "Where and when the friends met",
            "What they ordered",
            "What they discussed and decided",
            "Who paid and how much",
        ]
        facts = [
            "They met at a café at 2 p.m.",
            "Michael ordered coffee and chocolate cake; Anna ordered green tea and fruit salad.",
            "They discussed weekend plans and decided on cinema then park.",
            "Michael paid 15 pounds.",
        ]
    else:
        focus = topic.get("focus") or title
        full = (
            f"This short story is about {title}. "
            f"It includes simple facts related to {focus}. "
            "Tom woke up early and made a plan for the day. "
            "He met his friend Sara near the bus stop at ten. "
            "They bought two tickets and waited for a few minutes. "
            "On the way they talked about school and free time. "
            "Sara wanted to visit a museum, but Tom preferred a park. "
            "In the end they chose the park because the weather was sunny. "
            "They bought water and sat on a bench for half an hour. "
            "Tom paid three pounds for the drinks. "
            "Sara took photos and sent one to her family. "
            "They agreed to meet again next Friday."
        )
        gaps = (
            f"This short story is about {title}. "
            "Tom woke up early and made a (1)___ for the day. "
            "He met his friend Sara near the bus stop at (2)___. "
            "They bought two tickets and waited for a few minutes. "
            "On the way they talked about school and free time. "
            "Sara wanted to visit a museum, but Tom preferred a (3)___. "
            "In the end they chose the park because the weather was (4)___. "
            "They bought water and sat on a bench for half an hour. "
            "Tom paid three pounds for the drinks. "
            "Sara took photos and sent one to her family. "
            "They agreed to meet again next (5)___."
        )
        answers = ["plan", "ten", "park", "sunny", "Friday"]
        bank = ["plan", "ten", "park", "sunny", "Friday", "winter"]
        questions = [
            {
                "q": "What time did Tom meet Sara?",
                "accept": ["ten", "10", "at ten", "10 o'clock"],
                "hint_ru": "Во сколько Том встретил Сару?",
                "quote": "…near the bus stop at ten.",
            },
            {
                "q": "Why did they choose the park?",
                "accept": ["sunny", "weather was sunny", "because it was sunny"],
                "hint_ru": "Почему они выбрали парк?",
                "quote": "…because the weather was sunny.",
            },
            {
                "q": "How much did Tom pay for the drinks?",
                "accept": ["three pounds", "3 pounds", "3", "£3"],
                "hint_ru": "Сколько Том заплатил за напитки?",
                "quote": "Tom paid three pounds for the drinks.",
            },
            {
                "q": "When did they agree to meet again?",
                "accept": ["next Friday", "Friday"],
                "hint_ru": "Когда они договорились встретиться снова?",
                "quote": "They agreed to meet again next Friday.",
            },
        ]
        plan = [
            "When and where Tom met Sara",
            "What each person wanted to do",
            "What they chose and why",
            "What they did in the park and the payment",
        ]
        facts = [
            "Tom met Sara at the bus stop at ten.",
            "Sara wanted a museum; Tom preferred a park.",
            "They chose the park because it was sunny.",
            "They sat on a bench; Tom paid three pounds.",
        ]

    random.shuffle(bank)
    return {
        "full_text": full,
        "gapped_text": gaps,
        "answers": answers,
        "word_bank": bank,
        "questions": questions,
        "plan": plan,
        "facts": facts,
    }


def generate_reading_pack(level: str, topic: dict) -> dict:
    from services.gpt import _ask_json

    fallback = _fallback_pack(level, topic)
    title_en = topic.get("title_en") or "Topic"
    title_ru = topic.get("title_ru") or title_en
    focus = topic.get("focus") or title_en
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Create CEFR English READING practice JSON for Russian learners. ONLY JSON.\n"
                    "Keys: full_text, gapped_text, answers, word_bank, questions, plan, facts.\n"
                    f"TOPIC LOCK: must be about «{title_en}» / «{title_ru}». Focus: {focus}.\n"
                    "full_text: exactly 10 short English sentences as ONE string (spaces between).\n"
                    "gapped_text: SAME story with exactly 5 gaps marked (1)___ (2)___ … (5)___.\n"
                    "answers: exactly 5 English words/short phrases for gaps 1..5 in order.\n"
                    "word_bank: those 5 answers PLUS 1 distractor that fits none of the gaps; shuffled.\n"
                    "questions: exactly 4 objects {q, accept[2-5], hint_ru, quote}.\n"
                    "  q = comprehension (not copy-paste word hunt). accept = acceptable short answers.\n"
                    "  quote = short snippet from full_text that proves the answer.\n"
                    "plan: exactly 4 English plan points for a retelling.\n"
                    "facts: exactly 4 short English fact lines matching the plan (for checking).\n"
                    f"CEFR level: {level}. Vocabulary must match the level."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level:{level}\nTopic:{title_en}/{title_ru}\nFocus:{focus}\n"
                    f"Seed:{random.random()}"
                ),
            },
        ],
        fallback,
        temperature=0.5,
        max_tokens=1800,
    )
    pack = _normalize_pack(data, fallback)
    # перемешать банк слов
    bank = list(pack["word_bank"])
    random.shuffle(bank)
    pack["word_bank"] = bank
    return pack


def _normalize_pack(data: dict, fallback: dict) -> dict:
    if not isinstance(data, dict):
        return fallback
    full = str(data.get("full_text") or "").strip()
    gapped = str(data.get("gapped_text") or "").strip()
    answers = data.get("answers")
    bank = data.get("word_bank")
    questions = data.get("questions")
    plan = data.get("plan")
    facts = data.get("facts")
    if not full or not gapped:
        return fallback
    if not (isinstance(answers, list) and len(answers) >= 5):
        return fallback
    if not (isinstance(bank, list) and len(bank) >= 6):
        return fallback
    ans = [str(a).strip() for a in answers[:5]]
    wb = [str(w).strip() for w in bank[:6]]
    # убедиться, что все answers есть в банке
    for a in ans:
        if a and a not in wb:
            wb[0] = a
    qs = []
    src = questions if isinstance(questions, list) else []
    for i in range(4):
        raw = src[i] if i < len(src) and isinstance(src[i], dict) else fallback["questions"][i]
        accept = raw.get("accept") or fallback["questions"][i]["accept"]
        if not isinstance(accept, list):
            accept = [str(accept)]
        qs.append(
            {
                "q": str(raw.get("q") or fallback["questions"][i]["q"]).strip(),
                "accept": [str(x).strip() for x in accept if str(x).strip()][:6],
                "hint_ru": str(raw.get("hint_ru") or fallback["questions"][i]["hint_ru"]).strip(),
                "quote": str(raw.get("quote") or fallback["questions"][i]["quote"]).strip(),
            }
        )
    pl = [str(x).strip() for x in (plan or []) if str(x).strip()]
    if len(pl) < 4:
        pl = list(fallback["plan"])
    pl = pl[:4]
    fc = [str(x).strip() for x in (facts or []) if str(x).strip()]
    if len(fc) < 4:
        fc = list(fallback["facts"])
    fc = fc[:4]
    # проверка: 5 пропусков в тексте
    if len(re.findall(r"\(\d\)___", gapped)) < 5:
        return fallback
    return {
        "full_text": full,
        "gapped_text": gapped,
        "answers": ans,
        "word_bank": wb[:6],
        "questions": qs,
        "plan": pl,
        "facts": fc,
    }


def normalize_gap_token(s: str) -> str:
    t = (s or "").strip().lower()
    t = t.replace("ё", "е")
    t = re.sub(r"[^\w\s'-]", "", t, flags=re.UNICODE)
    return re.sub(r"\s+", " ", t).strip()


def parse_gap_answers(text: str, need: int = 5) -> list[str] | None:
    """Разобрать ответ: через запятую / точку с запятой / с новой строки."""
    raw = (text or "").strip()
    if not raw:
        return None
    if "," in raw or ";" in raw or "\n" in raw:
        parts = re.split(r"[,;\n]+", raw)
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) == need:
            return parts
        return None
    # одно слово — вернём список из одного (обработчик решит)
    return [raw]


def check_one_gap(user_word: str, expected: str) -> bool:
    u = normalize_gap_token(user_word)
    e = normalize_gap_token(expected)
    if not u or not e:
        return False
    if u == e:
        return True
    # мягко: без артиклей
    for art in ("a ", "an ", "the "):
        if u.startswith(art):
            u = u[len(art) :]
        if e.startswith(art):
            e = e[len(art) :]
    return u == e


def check_comprehension_answer(user_text: str, accept: list[str]) -> bool:
    u = normalize_gap_token(user_text)
    if not u:
        return False
    for a in accept:
        ea = normalize_gap_token(a)
        if not ea:
            continue
        if u == ea or ea in u or u in ea:
            return True
    return False


def judge_retelling(plan: list[str], facts: list[str], full_text: str, user_text: str) -> dict:
    """Проверка пересказа: ok + feedback_ru + missing_points."""
    from services.gpt import _ask_json

    fallback = {
        "ok": False,
        "feedback_ru": "Попробуй ещё раз — проверь все 4 пункта плана и факты из текста.",
        "missing": [1],
    }
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Judge an English reading retelling for a learner. ONLY JSON.\n"
                    'Return {"ok":bool,"feedback_ru":"short Russian feedback",'
                    '"missing":[plan point numbers 1-4 that are missing or wrong]}.\n'
                    "ok=true only if ALL 4 plan points are covered without factual errors vs facts/text.\n"
                    "Be fair: paraphrase is OK; inventing facts is not."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"PLAN:\n" + "\n".join(f"{i}. {p}" for i, p in enumerate(plan, 1))
                    + f"\n\nFACTS:\n" + "\n".join(f"- {f}" for f in facts)
                    + f"\n\nTEXT:\n{full_text}\n\nSTUDENT:\n{user_text}"
                ),
            },
        ],
        fallback,
        temperature=0.0,
        max_tokens=250,
    )
    if not isinstance(data, dict):
        return fallback
    missing = data.get("missing") or []
    if not isinstance(missing, list):
        missing = []
    clean_m = []
    for x in missing:
        try:
            n = int(x)
            if 1 <= n <= 4:
                clean_m.append(n)
        except (TypeError, ValueError):
            continue
    ok = bool(data.get("ok")) and not clean_m
    # эвристика без GPT: если текст слишком короткий
    if len((user_text or "").split()) < 12:
        ok = False
        if not clean_m:
            clean_m = [1, 2, 3, 4]
    return {
        "ok": ok,
        "feedback_ru": str(data.get("feedback_ru") or fallback["feedback_ru"]).strip(),
        "missing": clean_m,
    }
