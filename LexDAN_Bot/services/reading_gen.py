"""Генерация Reading-пакета: текст, пропуски, вопросы, план пересказа."""

from __future__ import annotations

import logging
import random
import re

log = logging.getLogger(__name__)

_GAP_RE = re.compile(r"\((\d)\)___")

# Слова, которые почти всегда дают неоднозначный пропуск без явной подсказки рядом
_AMBIGUOUS_GAP_HINTS = (
    r"years?\s+old",
    r"\bage\b",
    r"o'?clock",
    r"\bpounds?\b",
    r"\beuros?\b",
    r"\bdollars?\b",
    r"\bkilomet",
    r"\bmeters?\b",
)


def _norm_cmp(s: str) -> str:
    t = (s or "").lower().replace("ё", "е")
    t = re.sub(r"[^\w\s]", " ", t, flags=re.UNICODE)
    return re.sub(r"\s+", " ", t).strip()


def _fill_gaps(gapped: str, answers: list[str]) -> str:
    out = gapped
    for i, a in enumerate(answers, start=1):
        out = out.replace(f"({i})___", str(a).strip(), 1)
    return out


def _token_set(s: str) -> set[str]:
    return {w for w in _norm_cmp(s).split() if len(w) > 1}


def _gap_local_context(gapped: str, n: int, radius: int = 40) -> str:
    m = re.search(rf"\({n}\)___", gapped)
    if not m:
        return ""
    start = max(0, m.start() - radius)
    end = min(len(gapped), m.end() + radius)
    return gapped[start:end]


def _looks_ambiguous_gap(gapped: str, answers: list[str], bank: list[str]) -> str | None:
    """
    Вернуть причину, если пропуск угадывается только «наугад»
    (возраст/число/цена/профессия без опоры в видимом тексте).
    """
    bank_l = [str(w).strip().lower() for w in bank]
    numberish = {
        w
        for w in bank_l
        if w.isdigit()
        or w
        in {
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "fifteen",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen",
            "twenty",
            "thirty",
            "forty",
            "fifty",
            "sixty",
            "seventy",
            "eighty",
            "ninety",
        }
    }
    jobs = {
        "doctor",
        "teacher",
        "engineer",
        "nurse",
        "driver",
        "pilot",
        "cook",
        "chef",
        "waiter",
        "waitress",
        "manager",
        "student",
        "writer",
        "singer",
        "actor",
        "actress",
        "farmer",
        "lawyer",
        "police",
        "policeman",
        "firefighter",
        "builder",
        "dentist",
        "vet",
        "artist",
        "programmer",
        "secretary",
        "shopkeeper",
    }
    job_cues = {
        "doctor": ("hospital", "sick", "patient", "medicine", "ill"),
        "nurse": ("hospital", "sick", "patient", "medicine"),
        "teacher": ("school", "teach", "teaches", "lesson", "class", "student"),
        "engineer": ("bridge", "machine", "design", "factory", "build"),
        "driver": ("bus", "taxi", "car", "drive", "drives"),
        "cook": ("kitchen", "cook", "cooks", "restaurant", "food"),
        "chef": ("kitchen", "cook", "restaurant"),
        "farmer": ("farm", "field", "animals", "crop"),
        "dentist": ("teeth", "tooth", "clinic"),
        "vet": ("animal", "pet", "dog", "cat"),
        "pilot": ("plane", "airport", "fly", "flies"),
        "lawyer": ("court", "law", "case"),
        "builder": ("house", "build", "builds", "brick"),
        "programmer": ("code", "computer", "software"),
        "artist": ("paint", "drawing", "picture", "gallery"),
        "singer": ("song", "sing", "sings", "concert"),
        "actor": ("film", "stage", "theatre", "theater"),
        "actress": ("film", "stage", "theatre", "theater"),
        "waiter": ("restaurant", "menu", "serve"),
        "waitress": ("restaurant", "menu", "serve"),
    }

    years_old_gaps = 0
    for i in range(1, 6):
        ctx = _gap_local_context(gapped, i).lower()
        if re.search(r"years?\s+old", ctx) or re.search(r"\bage\b", ctx):
            years_old_gaps += 1

    # Несколько возрастных пропусков + несколько чисел в банке = почти всегда лотерея
    if years_old_gaps >= 2 and len(numberish) >= 2:
        # разрешаем только если КАЖдое число-ответ уже написано в видимом тексте вне пропусков
        rest = _GAP_RE.sub(" ", gapped)
        rest_tok = set(_norm_cmp(rest).split())
        for ans in answers:
            a = str(ans).strip().lower()
            if a in numberish and a not in rest_tok:
                return (
                    "several age gaps with numbers in the bank, but number "
                    f"«{ans}» is not written elsewhere in the gapped text"
                )

    for i, ans in enumerate(answers, start=1):
        ctx = _gap_local_context(gapped, i).lower()
        a = str(ans).strip().lower()
        if any(re.search(p, ctx) for p in _AMBIGUOUS_GAP_HINTS):
            if len(numberish) >= 2 and a in numberish:
                rest = _GAP_RE.sub(" ", gapped)
                rest_tok = set(_norm_cmp(rest).lower().split())
                if a not in rest_tok and a not in rest.lower():
                    return (
                        f"gap {i}: «{ans}» — число/возраст/цена без подсказки "
                        f"в остальном тексте (пример: sister is ___ years old)"
                    )

        # Профессии: при 2+ работах в банке у каждой должна быть уникальная подсказка в тексте
        jobs_in_bank = [w for w in bank_l if w in jobs]
        if a in jobs and len(jobs_in_bank) >= 2:
            rest = _GAP_RE.sub(" ", gapped).lower()
            cues = job_cues.get(a, ())
            if cues:
                if not any(c in rest for c in cues):
                    return (
                        f"gap {i}: job «{ans}» is not uniquely cued in the gapped text "
                        f"(need a clue like hospital/school/…)"
                    )
            else:
                rest_tok = set(_norm_cmp(rest).split())
                if a not in rest_tok:
                    return f"gap {i}: job «{ans}» has no unique clue among {jobs_in_bank}"
    return None


def _pack_structurally_ok(pack: dict) -> str | None:
    """None = ок, иначе причина брака."""
    full = str(pack.get("full_text") or "").strip()
    gapped = str(pack.get("gapped_text") or "").strip()
    answers = [str(a).strip() for a in (pack.get("answers") or [])[:5]]
    bank = [str(w).strip() for w in (pack.get("word_bank") or [])[:6]]
    if not full or not gapped:
        return "empty text"
    if len(answers) < 5:
        return "need 5 answers"
    if len(bank) < 6:
        return "need 6 word_bank"
    marks = _GAP_RE.findall(gapped)
    if len(marks) < 5 or [int(x) for x in marks[:5]] != [1, 2, 3, 4, 5]:
        return "gaps must be (1)___ … (5)___ in order"
    # answers ⊆ bank
    bank_l = {w.lower() for w in bank}
    for a in answers:
        if a.lower() not in bank_l:
            return f"answer «{a}» missing from word_bank"
    # ровно один лишний в банке
    if len({w.lower() for w in bank}) < 6:
        return "word_bank has duplicates"
    # заполненный gapped ≈ full_text
    filled = _fill_gaps(gapped, answers)
    full_tok = _token_set(full)
    fill_tok = _token_set(filled)
    if not full_tok or not fill_tok:
        return "empty tokens"
    overlap = len(full_tok & fill_tok) / max(1, len(full_tok | fill_tok))
    if overlap < 0.55:
        return f"filled gaps poorly match full_text (overlap={overlap:.2f})"
    # каждый ответ должен реально встречаться в full_text
    full_l = _norm_cmp(full)
    for a in answers:
        al = _norm_cmp(a)
        if al and al not in full_l and al not in full_l.split():
            # допускаем короткие формы
            if not any(al == t or al in t for t in full_l.split()):
                return f"answer «{a}» not found in full_text"
    amb = _looks_ambiguous_gap(gapped, answers, bank)
    if amb:
        return amb
    return None


def _fallback_cafe() -> dict:
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
            "model_en": "Michael's order cost 15 pounds.",
        },
        {
            "q": "What kind of weekends did Anna usually prefer?",
            "accept": ["quiet weekends with books", "quiet", "books", "reading"],
            "hint_ru": "Что Анна обычно предпочитала делать на выходных?",
            "quote": "Anna preferred quiet weekends with books…",
            "model_en": "Anna usually preferred quiet weekends with books.",
        },
        {
            "q": "What time did the friends meet?",
            "accept": ["2 p.m.", "2 pm", "2", "two", "at 2"],
            "hint_ru": "Во сколько друзья встретились?",
            "quote": "…met at a café at 2 p.m.",
            "model_en": "The friends met at 2 p.m.",
        },
        {
            "q": "What did Michael want to do after the cinema?",
            "accept": ["walk in the park", "get fresh air", "park", "fresh air"],
            "hint_ru": "Что Майкл хотел сделать после кино?",
            "quote": "…then walk in the park / get some fresh air.",
            "model_en": "Michael wanted to walk in the park after the cinema.",
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
    return _pack(full, gaps, answers, bank, questions, plan, facts)


def _fallback_family() -> dict:
    """
    Семья без «угадай возраст»: возраст дан целиком в тексте,
    пропуски — только то, что однозначно читается из подсказок.
    """
    full = (
        "My name is Lena. I live with my family in a small flat. "
        "I have one sister. Her name is Olga. "
        "Olga is ten years old and she likes school. "
        "My father is a doctor. Dad helps sick people at the hospital. "
        "My mother is a teacher. Mum works at our school and teaches English. "
        "At weekends we cook together in the kitchen. "
        "I love my family very much. "
        "Next Sunday we will visit grandma."
    )
    gaps = (
        "My name is Lena. I live with my family in a small flat. "
        "I have one sister. Her name is Olga. "
        "Olga is ten years old and she likes school. "
        "My sister's name is (1)___. "
        "My father is a (2)___. Dad helps sick people at the hospital. "
        "My mother is a teacher. Mum works at our school and teaches (3)___. "
        "At weekends we cook together in the (4)___. "
        "I love my family very much. "
        "Next Sunday we will visit (5)___."
    )
    # (1) Olga — уже «Her name is Olga»
    # (2) doctor — «helps sick people at the hospital»
    # (3) English — «teaches English»
    # (4) kitchen — «cook together in the kitchen»
    # (5) grandma — «visit grandma»
    answers = ["Olga", "doctor", "English", "kitchen", "grandma"]
    bank = ["Olga", "doctor", "English", "kitchen", "grandma", "twelve"]
    questions = [
        {
            "q": "How old is Olga?",
            "accept": ["ten", "10", "ten years old"],
            "hint_ru": "Сколько лет Ольге? Возраст уже написан в тексте целиком.",
            "quote": "Olga is ten years old…",
            "model_en": "Olga is ten years old.",
        },
        {
            "q": "What is Lena's father's job?",
            "accept": ["doctor", "a doctor"],
            "hint_ru": "Кем работает папа? Смотри, что он делает в больнице.",
            "quote": "My father is a doctor…",
            "model_en": "Lena's father is a doctor.",
        },
        {
            "q": "What does Mum teach?",
            "accept": ["English", "English language"],
            "hint_ru": "Что преподаёт мама?",
            "quote": "…teaches English.",
            "model_en": "Mum teaches English.",
        },
        {
            "q": "Where do they cook at weekends?",
            "accept": ["in the kitchen", "kitchen"],
            "hint_ru": "Где они готовят?",
            "quote": "…cook together in the kitchen.",
            "model_en": "They cook in the kitchen at weekends.",
        },
    ]
    plan = [
        "Who Lena lives with",
        "Facts about Olga (name and age from the text)",
        "Parents' jobs",
        "Weekend cooking and Sunday visit",
    ]
    facts = [
        "Lena lives with her family; she has a sister Olga.",
        "Olga is ten and likes school.",
        "Father is a doctor; mother is a teacher of English.",
        "They cook in the kitchen; next Sunday they visit grandma.",
    ]
    return _pack(full, gaps, answers, bank, questions, plan, facts)


def _fallback_generic(level: str, topic: dict) -> dict:
    """
    Тематический запасной текст для любой темы/уровня.
    Пропуски однозначны; план и факты только из текста.
    """
    title = (topic.get("title_en") or "this topic").strip()
    focus = (topic.get("focus") or title).strip()
    lvl = (level or "A1").upper()

    if lvl in {"A0", "A1"}:
        full = (
            f"Today Mia studies a short English text about {title}. "
            f"The text focuses on {focus}. "
            "She wakes up early and makes a plan for practice. "
            "At ten she meets her friend Ben near the library. "
            "Ben wants to watch a film, but Mia prefers reading. "
            "In the end they choose reading because it helps memory. "
            "They buy water and sit on a bench for half an hour. "
            "Mia pays three pounds for the drinks. "
            "Ben takes notes and sends one photo to his family. "
            "They agree to meet again next Monday and Mia puts the notes in her bag. "
            "Before leaving, Ben checks the time on his phone."
        )
        gaps = (
            f"Today Mia studies a short English text about {title}. "
            f"The text focuses on {focus}. "
            "She wakes up early and makes a (1)___ for practice. "
            "At ten she meets her friend Ben near the library. "
            "Ben wants to watch a film, but Mia prefers reading. "
            "In the end they choose reading because it helps (2)___. "
            "They buy water and sit on a bench for half an hour. "
            "Mia pays three pounds for the drinks. "
            "Ben takes notes and sends one photo to his family. "
            "They agree to meet again next (3)___ and Mia puts the notes in her (4)___. "
            "Before leaving, Ben checks the time on his (5)___."
        )
        answers = ["plan", "memory", "Monday", "bag", "phone"]
        bank = ["plan", "memory", "Monday", "bag", "phone", "winter"]
        questions = [
            {
                "q": "What is Mia's text about?",
                "accept": [title, title.lower(), focus.split(",")[0].strip()],
                "hint_ru": "О чём текст, который читает Миа?",
                "quote": f"…text about {title}.",
                "model_en": f"Mia's text is about {title}.",
            },
            {
                "q": "What time does Mia meet Ben?",
                "accept": ["ten", "10", "at ten"],
                "hint_ru": "Во сколько Миа встречает Бена?",
                "quote": "At ten she meets her friend Ben…",
                "model_en": "Mia meets Ben at ten.",
            },
            {
                "q": "Why do they choose reading?",
                "accept": ["helps memory", "memory", "because it helps memory"],
                "hint_ru": "Почему они выбирают чтение?",
                "quote": "…because it helps memory.",
                "model_en": "They choose reading because it helps memory.",
            },
            {
                "q": "When do they agree to meet again?",
                "accept": ["next Monday", "Monday"],
                "hint_ru": "Когда они договариваются встретиться снова?",
                "quote": "They agree to meet again next Monday…",
                "model_en": "They agree to meet again next Monday.",
            },
        ]
        plan = [
            f"What topic Mia studies ({title})",
            "Meeting Ben and different preferences",
            "Why they choose reading",
            "Payment, notes and next meeting",
        ]
        facts = [
            f"Mia studies a text about {title} (focus: {focus}).",
            "She meets Ben at ten near the library.",
            "They choose reading because it helps memory.",
            "Mia pays three pounds; they meet next Monday.",
        ]
        return _pack(full, gaps, answers, bank, questions, plan, facts)

    if lvl in {"A2", "B1"}:
        full = (
            f"Last week Dana prepared a short presentation about {title}. "
            f"She collected simple examples related to {focus}. "
            "She made a clear plan before she started writing. "
            "On Tuesday she met her classmate Omar in the city library. "
            "Omar wanted to visit a museum first, but Dana preferred the quiet library. "
            "Finally they stayed in the library because it was raining outside. "
            "They worked for two hours and shared one bottle of water. "
            "Dana paid four pounds for printing. "
            "Omar saved the notes on his laptop and emailed a copy to Dana. "
            "They agreed to practise again next Thursday and Dana put the printouts in her folder. "
            "Before leaving, Omar locked his laptop in his bag."
        )
        gaps = (
            f"Last week Dana prepared a short presentation about {title}. "
            f"She collected simple examples related to {focus}. "
            "She made a clear (1)___ before she started writing. "
            "On Tuesday she met her classmate Omar in the city library. "
            "Omar wanted to visit a museum first, but Dana preferred the quiet library. "
            "Finally they stayed in the library because it was (2)___ outside. "
            "They worked for two hours and shared one bottle of water. "
            "Dana paid four pounds for printing. "
            "Omar saved the notes on his laptop and emailed a copy to Dana. "
            "They agreed to practise again next (3)___ and Dana put the printouts in her (4)___. "
            "Before leaving, Omar locked his (5)___ in his bag."
        )
        answers = ["plan", "raining", "Thursday", "folder", "laptop"]
        bank = ["plan", "raining", "Thursday", "folder", "laptop", "sunny"]
        questions = [
            {
                "q": "What was Dana's presentation about?",
                "accept": [title, title.lower()],
                "hint_ru": "О чём была презентация Даны?",
                "quote": f"…presentation about {title}.",
                "model_en": f"Dana's presentation was about {title}.",
            },
            {
                "q": "Why did they stay in the library?",
                "accept": ["raining", "because it was raining", "rain"],
                "hint_ru": "Почему они остались в библиотеке?",
                "quote": "…because it was raining outside.",
                "model_en": "They stayed in the library because it was raining outside.",
            },
            {
                "q": "How much did Dana pay for printing?",
                "accept": ["four pounds", "4 pounds", "4", "£4"],
                "hint_ru": "Сколько Дана заплатила за печать?",
                "quote": "Dana paid four pounds for printing.",
                "model_en": "Dana paid four pounds for printing.",
            },
            {
                "q": "When did they agree to practise again?",
                "accept": ["next Thursday", "Thursday"],
                "hint_ru": "Когда они договорились потренироваться снова?",
                "quote": "They agreed to practise again next Thursday…",
                "model_en": "They agreed to practise again next Thursday.",
            },
        ]
        plan = [
            f"Dana's presentation topic ({title})",
            "Meeting Omar and the choice of place",
            "Why they stayed and how they worked",
            "Payment and next practice day",
        ]
        facts = [
            f"Dana prepared a presentation about {title}.",
            "They met on Tuesday; it was raining so they stayed in the library.",
            "Dana paid four pounds for printing.",
            "They practise again next Thursday.",
        ]
        return _pack(full, gaps, answers, bank, questions, plan, facts)

    # B2 / C1 / C2
    full = (
        f"For a seminar on {title}, Nora drafted a brief analysis linked to {focus}. "
        "She outlined a careful plan before drafting the first paragraph. "
        "On Wednesday she joined her colleague Victor at a quiet coworking space. "
        "Victor suggested a noisy café, but Nora insisted on the coworking space. "
        "They stayed there because the café was overcrowded and loud. "
        "After three focused hours they summarised the key arguments. "
        "Nora paid twelve pounds for day passes. "
        "Victor uploaded the shared document and sent Nora the link. "
        "They scheduled a follow-up next Friday and Nora filed the printouts in her portfolio. "
        "Before leaving, Victor switched off his tablet and packed it away."
    )
    gaps = (
        f"For a seminar on {title}, Nora drafted a brief analysis linked to {focus}. "
        "She outlined a careful (1)___ before drafting the first paragraph. "
        "On Wednesday she joined her colleague Victor at a quiet coworking space. "
        "Victor suggested a noisy café, but Nora insisted on the coworking space. "
        "They stayed there because the café was overcrowded and (2)___. "
        "After three focused hours they summarised the key arguments. "
        "Nora paid twelve pounds for day passes. "
        "Victor uploaded the shared document and sent Nora the link. "
        "They scheduled a follow-up next (3)___ and Nora filed the printouts in her (4)___. "
        "Before leaving, Victor switched off his (5)___ and packed it away."
    )
    answers = ["plan", "loud", "Friday", "portfolio", "tablet"]
    bank = ["plan", "loud", "Friday", "portfolio", "tablet", "silent"]
    questions = [
        {
            "q": "What seminar topic was Nora preparing?",
            "accept": [title, title.lower()],
            "hint_ru": "К какому семинару готовилась Нора?",
            "quote": f"For a seminar on {title}…",
            "model_en": f"Nora was preparing a seminar on {title}.",
        },
        {
            "q": "Why did they stay at the coworking space?",
            "accept": ["café was overcrowded and loud", "overcrowded", "loud", "noisy café"],
            "hint_ru": "Почему они остались в коворкинге?",
            "quote": "…the café was overcrowded and loud.",
            "model_en": "They stayed because the café was overcrowded and loud.",
        },
        {
            "q": "How much did Nora pay for day passes?",
            "accept": ["twelve pounds", "12 pounds", "12", "£12"],
            "hint_ru": "Сколько Нора заплатила за дневные пропуски?",
            "quote": "Nora paid twelve pounds for day passes.",
            "model_en": "Nora paid twelve pounds for day passes.",
        },
        {
            "q": "When is their follow-up?",
            "accept": ["next Friday", "Friday"],
            "hint_ru": "Когда у них следующая встреча?",
            "quote": "They scheduled a follow-up next Friday…",
            "model_en": "Their follow-up is next Friday.",
        },
    ]
    plan = [
        f"Seminar topic ({title}) and focus",
        "Where they worked and why",
        "How they collaborated",
        "Payment and follow-up",
    ]
    facts = [
        f"Nora prepared an analysis for a seminar on {title}.",
        "They chose coworking because the café was overcrowded and loud.",
        "Nora paid twelve pounds for day passes.",
        "Follow-up is next Friday.",
    ]
    return _pack(full, gaps, answers, bank, questions, plan, facts)


def _pack(
    full: str,
    gaps: str,
    answers: list[str],
    bank: list[str],
    questions: list[dict],
    plan: list[str],
    facts: list[str],
) -> dict:
    wb = list(bank)
    random.shuffle(wb)
    return {
        "full_text": full,
        "gapped_text": gaps,
        "answers": answers,
        "word_bank": wb,
        "questions": questions,
        "plan": plan,
        "facts": facts,
    }


def _fallback_food() -> dict:
    full = (
        "Anna likes simple food. "
        "For breakfast she eats bread and cheese. "
        "She drinks tea with lemon, not coffee. "
        "At lunch she takes an apple and a sandwich. "
        "In the evening her family cooks soup together. "
        "Anna does not like fish, but she loves fruit. "
        "On Sundays they buy fresh bread at the shop. "
        "Anna puts the bread in a basket on the table. "
        "Then they sit and eat slowly. "
        "After dinner Anna washes the cups."
    )
    gaps = (
        "Anna likes simple food. "
        "For breakfast she eats bread and cheese. "
        "She drinks (1)___ with lemon, not coffee. "
        "At lunch she takes an (2)___ and a sandwich. "
        "In the evening her family cooks (3)___ together. "
        "Anna does not like fish, but she loves fruit. "
        "On Sundays they buy fresh bread at the shop. "
        "Anna puts the bread in a (4)___ on the table. "
        "Then they sit and eat slowly. "
        "After dinner Anna washes the (5)___."
    )
    answers = ["tea", "apple", "soup", "basket", "cups"]
    bank = ["tea", "apple", "soup", "basket", "cups", "pizza"]
    questions = [
        {
            "q": "What does Anna drink with lemon?",
            "accept": ["tea", "tea with lemon"],
            "hint_ru": "Что Анна пьёт с лимоном?",
            "quote": "She drinks tea with lemon…",
            "model_en": "Anna drinks tea with lemon.",
        },
        {
            "q": "What fruit does she take at lunch?",
            "accept": ["apple", "an apple"],
            "hint_ru": "Какой фрукт она берёт в обед?",
            "quote": "…takes an apple and a sandwich.",
            "model_en": "She takes an apple at lunch.",
        },
        {
            "q": "What do they cook in the evening?",
            "accept": ["soup"],
            "hint_ru": "Что они готовят вечером?",
            "quote": "…cooks soup together.",
            "model_en": "They cook soup in the evening.",
        },
        {
            "q": "Where does Anna put the bread?",
            "accept": ["in a basket", "basket", "on the table"],
            "hint_ru": "Куда Анна кладёт хлеб?",
            "quote": "…in a basket on the table.",
            "model_en": "Anna puts the bread in a basket on the table.",
        },
    ]
    plan = ["Breakfast drinks and food", "Lunch", "Evening cooking", "Sunday shop and dinner"]
    facts = [
        "Anna drinks tea with lemon, not coffee.",
        "At lunch she takes an apple and a sandwich.",
        "In the evening they cook soup.",
        "On Sundays they buy bread; she puts it in a basket.",
    ]
    return _pack(full, gaps, answers, bank, questions, plan, facts)


def _fallback_home() -> dict:
    full = (
        "Leo lives in a small flat with two rooms. "
        "The kitchen is bright because of a big window. "
        "His bedroom has a bed, a desk and a blue chair. "
        "Near the door there is a green plant. "
        "In the evening Leo reads a book on the sofa. "
        "His sister draws pictures at the desk. "
        "Mum opens the window when it is hot. "
        "Dad fixes the door when it makes a noise. "
        "They keep shoes next to the door. "
        "Leo likes his home because it is quiet."
    )
    gaps = (
        "Leo lives in a small flat with two rooms. "
        "The kitchen is bright because of a big (1)___. "
        "His bedroom has a bed, a desk and a blue (2)___. "
        "Near the door there is a green plant. "
        "In the evening Leo reads a book on the (3)___. "
        "His sister draws pictures at the desk. "
        "Mum opens the window when it is hot. "
        "Dad fixes the (4)___ when it makes a noise. "
        "They keep shoes next to the door. "
        "Leo likes his home because it is (5)___."
    )
    answers = ["window", "chair", "sofa", "door", "quiet"]
    bank = ["window", "chair", "sofa", "door", "quiet", "noisy"]
    questions = [
        {
            "q": "Why is the kitchen bright?",
            "accept": ["big window", "window", "because of a big window"],
            "hint_ru": "Почему кухня светлая?",
            "quote": "…because of a big window.",
            "model_en": "The kitchen is bright because of a big window.",
        },
        {
            "q": "What colour is the chair?",
            "accept": ["blue", "blue chair"],
            "hint_ru": "Какого цвета стул?",
            "quote": "…a blue chair.",
            "model_en": "The chair is blue.",
        },
        {
            "q": "Where does Leo read in the evening?",
            "accept": ["on the sofa", "sofa"],
            "hint_ru": "Где Лео читает вечером?",
            "quote": "…reads a book on the sofa.",
            "model_en": "Leo reads a book on the sofa in the evening.",
        },
        {
            "q": "Why does Leo like his home?",
            "accept": ["quiet", "because it is quiet"],
            "hint_ru": "Почему Лео нравится дом?",
            "quote": "…because it is quiet.",
            "model_en": "Leo likes his home because it is quiet.",
        },
    ]
    plan = ["Flat and kitchen", "Bedroom things", "Evening at home", "Door, shoes, feeling"]
    facts = [
        "Kitchen is bright because of a big window.",
        "Bedroom has a bed, desk and blue chair.",
        "Leo reads on the sofa; sister draws at the desk.",
        "Dad fixes the door; Leo likes the quiet home.",
    ]
    return _pack(full, gaps, answers, bank, questions, plan, facts)


def _fallback_weather() -> dict:
    full = (
        "Yesterday the weather was rainy and cold. "
        "Mia wore a warm coat and took an umbrella. "
        "She walked to the bus stop slowly. "
        "Today the sky is blue and the sun is bright. "
        "Mia puts the umbrella back in the hall. "
        "She chooses a light jacket instead of the coat. "
        "Her brother wants to play football in the park. "
        "Mum says they can go if it stays sunny. "
        "In the evening it may become windy. "
        "Mia checks the weather on her phone again."
    )
    gaps = (
        "Yesterday the weather was rainy and cold. "
        "Mia wore a warm coat and took an (1)___. "
        "She walked to the bus stop slowly. "
        "Today the sky is blue and the sun is bright. "
        "Mia puts the umbrella back in the hall. "
        "She chooses a light (2)___ instead of the coat. "
        "Her brother wants to play football in the (3)___. "
        "Mum says they can go if it stays (4)___. "
        "In the evening it may become windy. "
        "Mia checks the weather on her (5)___ again."
    )
    # (1) umbrella — later «puts the umbrella back»
    answers = ["umbrella", "jacket", "park", "sunny", "phone"]
    bank = ["umbrella", "jacket", "park", "sunny", "phone", "snowy"]
    questions = [
        {
            "q": "What was the weather like yesterday?",
            "accept": ["rainy and cold", "rainy", "cold"],
            "hint_ru": "Какая была погода вчера?",
            "quote": "Yesterday the weather was rainy and cold.",
            "model_en": "Yesterday the weather was rainy and cold.",
        },
        {
            "q": "What does Mia choose today instead of the coat?",
            "accept": ["light jacket", "jacket"],
            "hint_ru": "Что она выбирает вместо пальто?",
            "quote": "…a light jacket instead of the coat.",
            "model_en": "Mia chooses a light jacket instead of the coat.",
        },
        {
            "q": "Where does her brother want to play football?",
            "accept": ["in the park", "park"],
            "hint_ru": "Где брат хочет играть в футбол?",
            "quote": "…in the park.",
            "model_en": "Her brother wants to play football in the park.",
        },
        {
            "q": "When may it become windy?",
            "accept": ["in the evening", "evening"],
            "hint_ru": "Когда может стать ветрено?",
            "quote": "In the evening it may become windy.",
            "model_en": "It may become windy in the evening.",
        },
    ]
    plan = ["Yesterday weather and clothes", "Today sky and jacket", "Park plans", "Evening wind and phone"]
    facts = [
        "Yesterday was rainy and cold; Mia took an umbrella.",
        "Today is sunny; she chooses a light jacket.",
        "Brother wants football in the park if it stays sunny.",
        "Evening may be windy; Mia checks her phone.",
    ]
    return _pack(full, gaps, answers, bank, questions, plan, facts)


def _fallback_pack(level: str, topic: dict) -> dict:
    tid = (topic.get("id") or "").lower()
    title = (topic.get("title_en") or "").lower()
    if "cafe" in tid or "café" in title or "cafe" in title:
        return _fallback_cafe()
    if "family" in tid or "family" in title:
        return _fallback_family()
    if tid in {"food"} or "food" in title:
        return _fallback_food()
    if tid in {"home"} or title.strip() == "home":
        return _fallback_home()
    if "weather" in tid or "weather" in title:
        return _fallback_weather()
    return _fallback_generic(level, topic)


def generate_reading_pack(level: str, topic: dict) -> dict:
    """
    Текст Reading — только из фиксированного банка (data/reading_packs.py).
    GPT здесь не вызывается (качество/стоимость). GPT остаётся в судьях заданий 2–3.
    """
    from data.reading_packs import get_reading_pack

    tid = topic.get("id") or ""
    pack = get_reading_pack(level, tid)
    if not pack:
        # страховка: тематический fallback из шаблонов
        pack = dict(_fallback_pack(level, topic))
    else:
        pack = dict(pack)
    bank = list(pack.get("word_bank") or [])
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
    wb = [str(w).strip() for w in bank]
    # answers обязаны быть в банке
    for a in ans:
        if a and a.lower() not in {x.lower() for x in wb}:
            wb.append(a)
    # ровно 6 уникальных (5 answers + 1 distractor)
    seen = set()
    uniq = []
    for w in wb:
        k = w.lower()
        if k in seen or not w:
            continue
        seen.add(k)
        uniq.append(w)
    # если distractor пропал — возьмём из fallback
    need = {a.lower() for a in ans}
    extras = [w for w in uniq if w.lower() not in need]
    core = []
    for a in ans:
        for w in uniq:
            if w.lower() == a.lower():
                core.append(w)
                break
        else:
            core.append(a)
    distractor = extras[0] if extras else str(fallback["word_bank"][-1])
    if distractor.lower() in need:
        distractor = "purple" if "purple" not in need else "winter"
    wb = core[:5] + [distractor]
    qs = []
    src = questions if isinstance(questions, list) else []
    for i in range(4):
        raw = src[i] if i < len(src) and isinstance(src[i], dict) else fallback["questions"][i]
        accept = raw.get("accept") or fallback["questions"][i]["accept"]
        if not isinstance(accept, list):
            accept = [str(accept)]
        fb_q = fallback["questions"][i]
        model_en = str(raw.get("model_en") or fb_q.get("model_en") or "").strip()
        quote = str(raw.get("quote") or fb_q.get("quote") or "").strip()
        if len(model_en.split()) < 3:
            qclean = quote.replace("…", "").strip(" .")
            if len(qclean.split()) >= 3:
                model_en = qclean if qclean.endswith(".") else qclean + "."
        if len(model_en.split()) < 3:
            acc0 = accept[0] if accept else ""
            model_en = str(acc0).strip()
            if model_en and not model_en.endswith("."):
                # слабый запасной вариант — GPT в проде даст полное предложение
                model_en = model_en[0].upper() + model_en[1:] + "."
        qs.append(
            {
                "q": str(raw.get("q") or fb_q["q"]).strip(),
                "accept": [str(x).strip() for x in accept if str(x).strip()][:6],
                "hint_ru": str(raw.get("hint_ru") or fb_q["hint_ru"]).strip(),
                "quote": quote,
                "model_en": model_en,
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
    if len(_GAP_RE.findall(gapped)) < 5:
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
    return [raw]


def check_one_gap(user_word: str, expected: str) -> bool:
    u = normalize_gap_token(user_word)
    e = normalize_gap_token(expected)
    if not u or not e:
        return False
    if u == e:
        return True
    for art in ("a ", "an ", "the "):
        if u.startswith(art):
            u = u[len(art) :]
        if e.startswith(art):
            e = e[len(art) :]
    return u == e


def check_comprehension_answer(user_text: str, accept: list[str]) -> bool:
    """
    Строгая проверка смысла по ключам accept.
    Короткий ключ вроде «tea» НЕ засчитывает «black tea», если в accept есть «green tea».
    """
    u = normalize_gap_token(user_text)
    if not u:
        return False
    accepts = [normalize_gap_token(a) for a in accept if normalize_gap_token(a)]
    if not accepts:
        return False

    # точное совпадение
    if u in accepts:
        return True

    # сначала длинные фразы — они специфичнее
    accepts_sorted = sorted(set(accepts), key=len, reverse=True)
    u_words = set(re.findall(r"[a-z0-9']+", u))

    for ea in accepts_sorted:
        ea_words = re.findall(r"[a-z0-9']+", ea)
        if not ea_words:
            continue
        # multi-word: все слова ключа должны быть в ответе как целые слова
        if len(ea_words) >= 2:
            if all(w in u_words for w in ea_words):
                # и фраза целиком (порядок) или все токены без конфликтующих уточнений
                if ea in u or all(w in u_words for w in ea_words):
                    # конфликт: у ответа есть другой модификатор того же head-noun
                    head = ea_words[-1]
                    mods_expected = set(ea_words[:-1])
                    # слова перед head в ответе
                    u_list = re.findall(r"[a-z0-9']+", u)
                    for i, w in enumerate(u_list):
                        if w == head and i > 0:
                            prev = u_list[i - 1]
                            # цвет/прилагательное перед head, которого нет в ключе
                            if prev not in mods_expected and prev not in {
                                "a", "an", "the", "some", "his", "her", "their", "my", "our",
                                "dan", "sara", "he", "she", "ordered", "chose", "chooses",
                                "bought", "wants", "wanted", "drinks", "drink",
                            }:
                                # чужой модификатор при том же существительном → не ок
                                if any(
                                    other != ea
                                    and head in other.split()
                                    and prev in other.split()
                                    for other in accepts_sorted
                                ):
                                    continue
                                # если есть более полный ключ с другим модом — отвергаем
                                rivals = [
                                    a
                                    for a in accepts_sorted
                                    if a != ea and head in re.findall(r"[a-z0-9']+", a)
                                ]
                                if rivals and prev not in mods_expected:
                                    # black vs green
                                    return False
                    return True
            continue

        # single-word key
        if ea not in u_words and ea not in u:
            continue
        # если есть более длинные ключи, где это слово — «голова», короткий ключ сам по себе слаб
        longer = [
            a
            for a in accepts_sorted
            if a != ea and ea in re.findall(r"[a-z0-9']+", a) and len(a) > len(ea)
        ]
        if longer:
            # засчитываем short только если один из длинных тоже матчится
            if any(
                all(w in u_words for w in re.findall(r"[a-z0-9']+", a))
                for a in longer
            ):
                return True
            # ответ содержит head, но не полный ключ (black tea vs green tea)
            return False
        # нет более длинных вариантов — одиночный ключ ок как целое слово
        if ea in u_words:
            return True
    return False


def looks_like_full_sentence(text: str) -> bool:
    """Грубая эвристика: не одно слово/фрагмент вроде «ten»."""
    words = [w for w in re.split(r"\s+", (text or "").strip()) if w]
    if len(words) >= 4:
        return True
    if len(words) <= 1:
        return False
    verbs = {
        "is",
        "are",
        "was",
        "were",
        "am",
        "be",
        "has",
        "have",
        "had",
        "do",
        "does",
        "did",
        "can",
        "will",
        "would",
        "like",
        "likes",
        "live",
        "lives",
        "go",
        "goes",
        "went",
        "met",
        "paid",
        "ordered",
        "chose",
        "wanted",
        "prefer",
        "preferred",
    }
    return any(re.sub(r"[^\w']", "", w).lower() in verbs for w in words)


def _default_review(level: str) -> dict:
    lvl = (level or "A1").upper()
    defaults = {
        "A0": ("I / You + to be", "A0"),
        "A1": ("Present Simple", "A1"),
        "A2": ("Past Simple", "A2"),
        "B1": ("Present Perfect", "B1"),
        "B2": ("Conditionals 2 & 3", "B2"),
        "C1": ("Inversion / emphasis", "C1"),
        "C2": ("Advanced discourse markers", "C2"),
    }
    title, lv = defaults.get(lvl, ("Present Simple", "A1"))
    return {"review_topic": title, "review_level": lv}


def hint_gap_fill(
    *,
    level: str,
    gapped: str,
    word_bank: list[str],
    answers: list[str],
    wrong_pairs: list[tuple[int, str]],
) -> str:
    """Подсказка без раскрытия правильных слов."""
    from services.gpt import _ask_json

    lines = [f"gap {i}: user wrote «{w}»" for i, w in wrong_pairs]
    fallback = {
        "hint_ru": (
            "🦜 Рико: Посмотри ещё раз на слова вокруг каждого пропуска — "
            "ответ уже спрятан в тексте (раньше или позже). "
            "Лишнее слово из банка никуда не подходит. Попробуй ещё раз!"
        )
    }
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "You are Rico, a warm English tutor. ONLY JSON.\n"
                    'Return {"hint_ru":"2-4 short Russian sentences"}.\n'
                    "Give helpful HINTS for wrong gap fills WITHOUT naming the correct answers "
                    "and WITHOUT listing the answer words.\n"
                    "Point to context clues / collocations / contrasts in the gapped text.\n"
                    "Do not reveal the solution. Friendly Rico voice."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level:{level}\nGAPPED:\n{gapped}\nBANK:{', '.join(word_bank)}\n"
                    f"WRONG:\n" + "\n".join(lines)
                ),
            },
        ],
        fallback,
        temperature=0.2,
        max_tokens=280,
    )
    if not isinstance(data, dict):
        return fallback["hint_ru"]
    return str(data.get("hint_ru") or fallback["hint_ru"]).strip()


def explain_gap_fill(
    *,
    level: str,
    gapped: str,
    answers: list[str],
    wrong_pairs: list[tuple[int, str]],
) -> dict:
    """После 2-й ошибки: объяснить + темы на повтор."""
    from services.gpt import _ask_json

    rev = _default_review(level)
    lines = [f"gap {i}: user «{w}» → correct «{answers[i - 1]}»" for i, w in wrong_pairs if 1 <= i <= len(answers)]
    fallback = {
        "explain_ru": (
            "🦜 Рико: Разберём ошибки. Смотри правильные слова ниже — "
            "они следуют из смысла текста и сочетаний слов."
        ),
        "review_topic": rev["review_topic"],
        "review_level": rev["review_level"],
    }
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "You are Rico. ONLY JSON.\n"
                    "Return {"
                    '"explain_ru":"Russian explanation of mistakes (2-5 sentences)",'
                    '"review_topic":"grammar topic title from curriculum",'
                    '"review_level":"CEFR level where that topic is taught (A0-C2)"'
                    "}.\n"
                    "Explain WHY the correct gap words fit. Be concrete.\n"
                    "Pick ONE main grammar/vocab theme to review based on the errors "
                    "(articles, Present Simple, Past Simple, collocations, prepositions…).\n"
                    "review_level should match where that theme usually lives "
                    f"(student level is {level}, but topic level may differ slightly)."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level:{level}\nGAPPED:\n{gapped}\n"
                    f"ERRORS:\n" + "\n".join(lines)
                ),
            },
        ],
        fallback,
        temperature=0.15,
        max_tokens=350,
    )
    if not isinstance(data, dict):
        return fallback
    return {
        "explain_ru": str(data.get("explain_ru") or fallback["explain_ru"]).strip(),
        "review_topic": str(data.get("review_topic") or fallback["review_topic"]).strip(),
        "review_level": str(data.get("review_level") or fallback["review_level"]).strip().upper(),
    }


def judge_comprehension_answer(
    *,
    level: str,
    question: str,
    accept: list[str],
    model_en: str,
    quote: str,
    full_text: str,
    user_text: str,
) -> dict:
    """
    Проверка ответа по тексту.

    Не шаблоним формулировку: «Her father is a doctor» ≡ «Lena's father is a doctor».
    Смотрим: (1) факт совпадает с текстом/вопросом, (2) грамматика.
    Регистр и пунктуацию игнорируем.
    """
    from services.gpt import _ask_json

    rev = _default_review(level)
    meaning_local = check_comprehension_answer(user_text, accept)
    is_sentence = looks_like_full_sentence(user_text)
    model = (model_en or "").strip() or (
        (accept[0] if accept else "See the text.") + "."
    )

    # Одно слово / обрывок при верном ключе — попросить предложение, без «ошибки»
    if meaning_local and not is_sentence:
        return {
            "fact_ok": True,
            "grammar_ok": True,
            "need_full_sentence": True,
            "feedback_ru": (
                "🦜 Рико: Факт верный! Напиши его, пожалуйста, "
                "полным предложением (не одно слово)."
            ),
            "better_en": model,
            "review_topic": rev["review_topic"],
            "review_level": rev["review_level"],
        }

    fallback = {
        "fact_ok": meaning_local,
        "grammar_ok": True if meaning_local else True,
        "need_full_sentence": False,
        "feedback_ru": (
            "🦜 Рико: Верно по смыслу!"
            if meaning_local
            else "🦜 Рико: По факту из текста не совсем так. Найди нужную информацию и ответь снова."
        ),
        "better_en": "" if meaning_local else model,
        "review_topic": rev["review_topic"],
        "review_level": rev["review_level"],
    }

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "You are Rico judging a reading comprehension answer. ONLY JSON.\n"
                    "Ignore case and punctuation forever — never mention them.\n"
                    "Do NOT require a template wording. Accept ANY paraphrase that answers "
                    "the QUESTION with a FACT that matches the TEXT "
                    "(e.g. «her father is a doctor» == «Lena's father is a doctor»).\n"
                    "Separate FACT from GRAMMAR:\n"
                    "- fact_ok=true if the student's meaning correctly answers the question "
                    "using information from the text (even if grammar is imperfect).\n"
                    "- fact_ok=false if they answer the wrong thing "
                    "(e.g. give a job when asked for age, invent facts, OR "
                    "change a critical detail: black tea vs green tea, wrong name/number/colour).\n"
                    "- grammar_ok=false only for real grammar/spelling/tense/word-form errors.\n"
                    "- need_full_sentence=true ONLY for tiny fragments like «doctor» / «ten» "
                    "with no subject+verb. If there is already a clause with a verb "
                    "(«her father is a doctor»), need_full_sentence MUST be false.\n"
                    "Return {"
                    '"fact_ok":bool,'
                    '"grammar_ok":bool,'
                    '"need_full_sentence":bool,'
                    '"feedback_ru":"short Russian Rico feedback",'
                    '"better_en":"corrected English if grammar_ok is false OR model answer if fact_ok is false; else empty",'
                    '"review_topic":"grammar topic if grammar issue, else empty",'
                    '"review_level":"CEFR level of that topic or empty"'
                    "}.\n"
                    f"Student CEFR level: {level}."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"TEXT:\n{full_text}\n\nQ: {question}\n"
                    f"KEY FACTS (accept any paraphrase covering these): {accept}\n"
                    f"QUOTE: {quote}\nEXAMPLE (not a required template): {model}\n"
                    f"STUDENT: {user_text}"
                ),
            },
        ],
        fallback,
        temperature=0.0,
        max_tokens=320,
    )
    if not isinstance(data, dict):
        data = fallback

    gpt_fact = data.get("fact_ok")
    # Строгий локальный матч важнее слабого substring прошлого.
    # - local False → fact_ok False (black tea ≠ green tea)
    # - local True + предложение → можно принять, даже если GPT ошибся
    # - local True + обрывок → факт ок, но просим полное предложение
    if not meaning_local:
        fact_ok = False
    elif not is_sentence:
        fact_ok = True
    else:
        fact_ok = True if gpt_fact is None else bool(gpt_fact)
        # сильный локальный матч перекрывает ложный GPT false
        if meaning_local:
            fact_ok = True

    grammar_ok = bool(data.get("grammar_ok", True))
    need_fs = bool(data.get("need_full_sentence"))
    if is_sentence:
        need_fs = False
    if meaning_local and not is_sentence:
        need_fs = True
        fact_ok = True

    better = str(data.get("better_en") or "").strip()
    if fact_ok and grammar_ok:
        better = ""
    elif fact_ok and not grammar_ok and not better:
        better = model
    elif not fact_ok and not better:
        better = model

    review_topic = str(data.get("review_topic") or "").strip()
    review_level = str(data.get("review_level") or "").strip().upper()
    if fact_ok and not grammar_ok and not review_topic:
        review_topic = rev["review_topic"]
        review_level = rev["review_level"]
    if fact_ok and grammar_ok:
        review_topic = ""
        review_level = ""

    feedback = str(data.get("feedback_ru") or fallback["feedback_ru"]).strip()
    if fact_ok and grammar_ok and is_sentence:
        feedback = "🦜 Рико: Верно!"
    elif not fact_ok:
        feedback = str(data.get("feedback_ru") or fallback["feedback_ru"]).strip()
        if not feedback or "Верно" in feedback:
            feedback = (
                "🦜 Рико: По факту из текста не совсем так. "
                "Перечитай вопрос и ответь точнее."
            )
    elif fact_ok and not grammar_ok:
        if not feedback or "полн" in feedback.lower():
            feedback = "🦜 Рико: Факт верный, чуть поправлю грамматику."

    return {
        "fact_ok": fact_ok,
        "grammar_ok": grammar_ok,
        "need_full_sentence": need_fs,
        "feedback_ru": feedback,
        "better_en": better,
        "review_topic": review_topic,
        "review_level": review_level,
        "ok": bool(fact_ok and grammar_ok and not need_fs),
        "meaning_ok": fact_ok,
    }


def _retell_copy_ratio(user_text: str, full_text: str) -> float:
    """Доля длинных n-грамм пересказа, совпадающих с исходником (0..1)."""
    src = normalize_gap_token(full_text)
    usr = normalize_gap_token(user_text)
    if not src or not usr:
        return 0.0
    src_words = re.findall(r"[a-z0-9']+", src)
    usr_words = re.findall(r"[a-z0-9']+", usr)
    if len(usr_words) < 8:
        return 0.0
    n = 5
    if len(usr_words) < n:
        return 0.0
    src_set = {
        " ".join(src_words[i : i + n]) for i in range(len(src_words) - n + 1)
    }
    if not src_set:
        return 0.0
    hits = 0
    total = 0
    for i in range(len(usr_words) - n + 1):
        total += 1
        if " ".join(usr_words[i : i + n]) in src_set:
            hits += 1
    return hits / total if total else 0.0


def _facts_coverage(user_text: str, facts: list[str]) -> float:
    """Грубая доля фактов, которые хоть как-то отражены в пересказе."""
    if not facts:
        return 1.0
    u = normalize_gap_token(user_text)
    u_words = set(re.findall(r"[a-z0-9']+", u))
    hit = 0
    for f in facts:
        fw = [w for w in re.findall(r"[a-z0-9']+", normalize_gap_token(f)) if len(w) > 3]
        if not fw:
            continue
        # хотя бы половина значимых слов факта
        ok = sum(1 for w in fw if w in u_words)
        if ok >= max(1, len(fw) // 2):
            hit += 1
    return hit / max(1, len(facts))


def judge_retelling(
    plan: list[str],
    facts: list[str],
    full_text: str,
    user_text: str,
    level: str = "A1",
) -> dict:
    """
    Пересказ своими словами: нельзя копировать текст.
    Нужны ключевые факты; passed может быть false.
    """
    from services.gpt import _ask_json

    rev = _default_review(level)
    copy_ratio = _retell_copy_ratio(user_text, full_text)
    coverage = _facts_coverage(user_text, facts)

    if copy_ratio >= 0.45:
        return {
            "passed": False,
            "feedback_ru": (
                "🦜 Рико: Это почти копия текста. Перескажи <b>своими словами</b>: "
                "главные факты своими предложениями, без копипаста."
            ),
            "better_en": "",
            "tips_ru": "Составь 3–5 предложений по плану: кто / что сделал / чем закончилось.",
            "review_topics": [],
            "copy_ratio": copy_ratio,
            "coverage": coverage,
        }

    if coverage < 0.35 and len(facts) >= 2:
        return {
            "passed": False,
            "feedback_ru": (
                "🦜 Рико: В пересказе мало фактов из текста. "
                "Добавь ключевые детали (кто, что, где) своими словами."
            ),
            "better_en": "",
            "tips_ru": "Ориентируйся на план и факты — но не копируй абзацы.",
            "review_topics": [],
            "copy_ratio": copy_ratio,
            "coverage": coverage,
        }

    fallback = {
        "passed": True,
        "feedback_ru": (
            "🦜 Рико: Спасибо за пересказ! Задание принято. "
            "Ниже — мягкие правки, если они нужны."
        ),
        "better_en": (user_text or "").strip(),
        "tips_ru": "",
        "review_topics": [],
    }
    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "You are Rico judging an English READING retelling. ONLY JSON.\n"
                    "Set passed=false if the student mostly copied the source OR "
                    "missed most key facts OR wrote almost nothing relevant.\n"
                    "Set passed=true if it is a real paraphrase covering the main facts "
                    "(wording can be imperfect).\n"
                    "The PLAN is a soft hint, not a rigid checklist.\n"
                    "Judge:\n"
                    "1) FACTS vs source TEXT (no invented facts).\n"
                    "2) GRAMMAR — ignore case/punctuation.\n"
                    "Return {"
                    '"passed":bool,'
                    '"feedback_ru":"warm Russian feedback",'
                    '"better_en":"improved English keeping student meaning; empty if fine",'
                    '"tips_ru":"optional tip; empty if not needed",'
                    '"review_topics":[{"topic":"Grammar theme","level":"A1"}]'
                    "}.\n"
                    f"Student CEFR level: {level}."
                ),
            },
            {
                "role": "user",
                "content": (
                    "PLAN (soft hint):\n"
                    + "\n".join(f"{i}. {p}" for i, p in enumerate(plan, 1))
                    + "\n\nKEY FACTS:\n"
                    + "\n".join(f"- {f}" for f in facts)
                    + f"\n\nSOURCE TEXT:\n{full_text}\n\nSTUDENT RETELLING:\n{user_text}"
                    + f"\n\nLOCAL_HINTS: copy_ratio={copy_ratio:.2f}, facts_coverage={coverage:.2f}"
                ),
            },
        ],
        fallback,
        temperature=0.2,
        max_tokens=500,
    )
    if not isinstance(data, dict):
        return fallback
    topics = data.get("review_topics") or []
    clean_topics = []
    if isinstance(topics, list):
        for t in topics[:3]:
            if isinstance(t, dict):
                topic = str(t.get("topic") or "").strip()
                lv = str(t.get("level") or level).strip().upper()
                if topic:
                    clean_topics.append({"topic": topic, "level": lv})
            elif isinstance(t, str) and t.strip():
                clean_topics.append({"topic": t.strip(), "level": (level or "A1").upper()})
    better = str(data.get("better_en") or "").strip()
    passed = bool(data.get("passed", True))
    # локальные стоп-условия сильнее GPT
    if copy_ratio >= 0.45:
        passed = False
    return {
        "passed": passed,
        "feedback_ru": str(data.get("feedback_ru") or fallback["feedback_ru"]).strip(),
        "better_en": better,
        "tips_ru": str(data.get("tips_ru") or "").strip(),
        "review_topics": clean_topics,
        "copy_ratio": copy_ratio,
        "coverage": coverage,
    }
