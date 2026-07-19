"""
Рико-тьютор: свободный чат по теме + генерация/проверка заданий + помощь.
"""

import logging
import random
import re

import requests
from config import OPENROUTER_API_KEY
from services.gpt import _ask_json

WORD_LOOKUP_PATTERNS = (
    r"как\s+перевод",
    r"как\s+будет",
    r"что\s+значит",
    r"перевод\s+слова",
    r"переведи\s+слово",
    r"what\s+does\s+.+\s+mean",
    r"how\s+do\s+you\s+say",
    r"how\s+to\s+translate",
)


def exercise_subtype(exercise_num: int) -> str:
    if exercise_num <= 3:
        return "mcq"
    if exercise_num <= 6:
        return "word_form"
    if exercise_num == 7:
        return "translate_en"
    return "translate_ru"


def is_word_lookup_question(text: str) -> bool:
    t = (text or "").strip().lower()
    if not t:
        return False
    return any(re.search(p, t) for p in WORD_LOOKUP_PATTERNS)


def rico_word_lookup(level: str, topic_title: str, question: str, exercise: dict) -> str:
    """Подсказка по слову во время переводного задания — задание не завершается."""
    fallback = "🦜 Напиши слово, которое непонятно — переведу!"
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Ты Рико 🦜. Ученик в переводном задании спрашивает про слово. "
                            "Дай короткий перевод/объяснение слова на русском. "
                            "Если спрашивают EN→RU или RU→EN — покажи оба варианта. "
                            "В конце одной строкой: «Задание продолжается — напиши перевод предложения». "
                            "HTML: <b> для слова. Без JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Уровень {level}, тема {topic_title}.\n"
                            f"Задание: {exercise.get('prompt') or ''}\n"
                            f"Вопрос ученика: {question}"
                        ),
                    },
                ],
                "max_tokens": 220,
                "temperature": 0.3,
            },
            timeout=25,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        if not text.startswith("🦜"):
            text = f"🦜 {text}"
        return text
    except Exception as e:
        logging.error(f"Rico word lookup error: {e}")
        return fallback


def rico_topic_chat_text(level: str, topic_title: str, question: str, user_name: str = "друг") -> str:
    fallback = (
        "🦜 Хм, давай так: напиши свой пример по теме — разберём вместе! "
        "Я на связи."
    )
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Ты попугай Рико 🦜 — дружелюбный репетитор. "
                            "Отвечай по-русски, с английскими примерами. "
                            "После КАЖДОГО английского примера сразу ниже дай перевод "
                            "курсивом в HTML: <i>…</i>. "
                            "Формат ответа — HTML для Telegram (можно <b> и <i>). "
                            "Коротко, ясно, по-человечески. Не используй JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Уровень: {level}. Тема грамматики: {topic_title}. "
                            f"Ученика зовут {user_name}.\nВопрос: {question}"
                        ),
                    },
                ],
                "max_tokens": 450,
                "temperature": 0.55,
            },
            timeout=30,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        if not text.startswith("🦜"):
            text = f"🦜 {text}"
        return text
    except Exception as e:
        logging.error(f"Rico chat error: {e}")
        return fallback


def generate_grammar_exercise(
    level: str,
    topic_title: str,
    exercise_num: int,
    topic_id: str | None = None,
) -> dict:
    """
    1–3: MCQ (кнопки)
    4–6: написать форму слова (базовая форма в скобках у пропуска)
    7: RU → EN перевод
    8: EN → RU перевод

    Если есть проверенный банк темы — берём его (GPT часто путает времена / a,b,c,d).
    """
    from data.grammar_exercise_fallbacks import (
        FALLBACKS,
        focus_for,
        get_topic_fallback,
        looks_on_topic,
    )

    subtype = exercise_subtype(exercise_num)
    kind = "mcq" if subtype == "mcq" else "write"
    focus = focus_for(topic_id, topic_title)

    topic_fb = get_topic_fallback(topic_id, exercise_num)
    bank = FALLBACKS.get(topic_id or "", [])

    # Предпочитаем curated bank — качество важнее «рандома» GPT
    if topic_fb and bank and len(bank) >= 8:
        return _finalize_exercise(dict(topic_fb), subtype, kind, topic_fb)

    mcq_labels = {
        1: "Choose the correct option for the blank. One sentence with ____ .",
        2: "Choose the grammatically correct sentence (4 full sentences as options).",
        3: "Fill the blank: choose the best option among 4 choices.",
    }
    word_form_labels = {
        4: "Student types ONLY the correct word/form. Show blank with base form in parentheses.",
        5: "Same word-form task, slightly harder, STILL on the same grammar topic.",
        6: "Same word-form task, hardest of three, STILL on the same grammar topic.",
    }

    if topic_fb:
        fallback = topic_fb
        fallback_options = list(fallback.get("options") or ["is", "are", "am", "be"])
    else:
        fallback_options = ["is", "are", "am", "be"]
        fallback = {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери правильный ответ по теме.",
            "sentence_en": f"Choose the form for «{topic_title}».",
            "sentence_ru": f"Задание по теме «{topic_title}».",
            "options": fallback_options,
            "answer": "is",
            "tip": f"Вспомни правило темы «{topic_title}».",
        }
        if subtype == "word_form":
            fallback = {
                "kind": "write",
                "subtype": "word_form",
                "instruction_ru": "Напиши правильную форму (одно слово).",
                "sentence_en": f"Practice «{topic_title}»: fill ____ (be).",
                "sentence_ru": f"Тренируем тему «{topic_title}».",
                "base_form": "be",
                "options": None,
                "answer": "is",
                "tip": f"Тема: {topic_title}.",
            }
        elif subtype == "translate_en":
            fallback = {
                "kind": "write",
                "subtype": "translate_en",
                "instruction_ru": f"Переведи на английский (тема «{topic_title}»):",
                "sentence_en": "",
                "sentence_ru": f"Пример по теме «{topic_title}».",
                "options": None,
                "answer": f"Example about {topic_title}.",
                "tip": f"Используй грамматику темы «{topic_title}».",
            }
        elif subtype == "translate_ru":
            fallback = {
                "kind": "write",
                "subtype": "translate_ru",
                "instruction_ru": "Переведи на русский:",
                "sentence_en": f"This sentence practices {topic_title}.",
                "sentence_ru": f"Это предложение тренирует тему «{topic_title}».",
                "options": None,
                "answer": f"Это предложение тренирует тему «{topic_title}».",
                "tip": "Переводи смысл.",
            }

    if subtype == "mcq":
        task_desc = mcq_labels[exercise_num]
        json_hint = (
            'For MCQ: {"kind":"mcq","subtype":"mcq","instruction_ru":"...","sentence_en":"... ____ ...",'
            '"sentence_ru":"перевод правильного предложения",'
            '"options":["goes","go","going","went"],'
            '"answer":"goes","tip":"..."} '
            "CRITICAL: options must be REAL words/phrases (never a/b/c/d). "
            "answer MUST be exactly one of options. "
            "For Present Simple NEVER mark Continuous (is/are + -ing) as correct."
        )
    elif subtype == "word_form":
        task_desc = word_form_labels[exercise_num]
        json_hint = (
            'For WORD FORM: {"kind":"write","subtype":"word_form","instruction_ru":"Напиши форму",'
            '"sentence_en":"... ____ (base) ...","base_form":"base",'
            '"sentence_ru":"...","answer":"only-the-form","tip":"..."} '
            "sentence_en MUST contain ____ and (base_form). answer = ONLY the form."
        )
    elif subtype == "translate_en":
        task_desc = "Russian → English. English answer MUST use the topic grammar."
        json_hint = (
            'For TRANSLATE EN: {"kind":"write","subtype":"translate_en",'
            '"instruction_ru":"Переведи на английский:","sentence_ru":"...",'
            '"sentence_en":"","answer":"correct English with TOPIC grammar","tip":"..."}'
        )
    else:
        task_desc = "English → Russian. English sentence MUST use the topic grammar."
        json_hint = (
            'For TRANSLATE RU: {"kind":"write","subtype":"translate_ru",'
            '"instruction_ru":"Переведи на русский:","sentence_en":"English with TOPIC grammar",'
            '"sentence_ru":"...","answer":"Russian translation","tip":"..."}'
        )

    level_hint = (
        " instruction_ru = short Russian instruction. "
        "sentence_ru = meaning of the correct English sentence for the Translate button. "
    )
    if level in {"A0", "A1", "A2"}:
        level_hint += " Very simple vocabulary for A0-A2."

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Create ONE English grammar exercise for Telegram. "
                    f"CEFR: {level}. Topic title: {topic_title}. Topic id: {topic_id or 'n/a'}. "
                    f"CRITICAL FOCUS: {focus} "
                    f"Task #{exercise_num}/8: {task_desc} "
                    f'Output kind MUST be "{kind}". {level_hint} '
                    "If you make an off-topic exercise (wrong tense/construction), it is INVALID. "
                    "Return ONLY JSON. " + json_hint
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Make ON-TOPIC exercise {exercise_num}/8 for «{topic_title}». "
                    f"Seed {random.random()}"
                ),
            },
        ],
        fallback,
        temperature=0.25,
        max_tokens=450,
    )

    trial_en = (data.get("sentence_en") or "") + " " + (data.get("answer") or "")
    if topic_id and not looks_on_topic(
        topic_id, trial_en, data.get("options"), str(data.get("answer") or "")
    ):
        logging.warning(f"Off-topic exercise for {topic_id}, using fallback #{exercise_num}")
        data = dict(fallback)

    sen_low = (data.get("sentence_en") or "").lower()
    if (
        "choose the form for" in sen_low
        or "practice «" in sen_low
        or "practices " + (topic_title or "").lower() in sen_low
        or sen_low.strip() in {"", "____"}
    ):
        logging.warning(f"Meta/empty exercise for {topic_id}, using fallback #{exercise_num}")
        data = dict(fallback)

    if kind == "mcq":
        opts = data.get("options")
        ans = str(data.get("answer") or "").strip()
        if not _mcq_options_ok(opts, ans):
            logging.warning(f"Bad MCQ options/answer for {topic_id}, using fallback #{exercise_num}")
            data = dict(fallback)

    return _finalize_exercise(data, subtype, kind, fallback)


def _mcq_options_ok(options, answer: str) -> bool:
    if not isinstance(options, list) or len(options) < 4:
        return False
    opts = [str(x).strip() for x in options[:4]]
    if len(set(o.lower() for o in opts)) < 4:
        return False
    # GPT часто пишет a/b/c/d — брак
    letters = {"a", "b", "c", "d"}
    if all(o.lower().rstrip(".") in letters for o in opts):
        return False
    if answer not in opts:
        lower_map = {o.lower(): o for o in opts}
        if answer.lower() not in lower_map:
            return False
    return True


def _finalize_exercise(data: dict, subtype: str, kind: str, fallback: dict) -> dict:
    instruction_ru = (data.get("instruction_ru") or fallback.get("instruction_ru") or "").strip()
    if instruction_ru.lower() in {"выбери правильный ответ по теме.", "выбери правильный ответ по теме"}:
        instruction_ru = (fallback.get("instruction_ru") or instruction_ru).strip()
    sentence_en = (data.get("sentence_en") or fallback.get("sentence_en") or "").strip()
    if "choose the form for" in sentence_en.lower():
        data = dict(fallback)
        instruction_ru = (data.get("instruction_ru") or "").strip()
        sentence_en = (data.get("sentence_en") or "").strip()
    sentence_ru = (data.get("sentence_ru") or fallback.get("sentence_ru") or "").strip()
    tip = (data.get("tip") or fallback.get("tip") or "").strip()
    answer = (data.get("answer") or fallback.get("answer") or "").strip()
    base_form = (data.get("base_form") or fallback.get("base_form") or "").strip()
    options = data.get("options")
    ex_subtype = (data.get("subtype") or fallback.get("subtype") or subtype).strip()
    if subtype == "word_form" and base_form and "____" in sentence_en and f"({base_form})" not in sentence_en:
        sentence_en = sentence_en.replace("____", f"____ ({base_form})", 1)
    prompt = _build_exercise_display(instruction_ru, sentence_en, sentence_ru, ex_subtype)

    if kind == "mcq":
        if not isinstance(options, list) or len(options) < 4:
            options = list(fallback.get("options") or ["is", "are", "am", "be"])
            answer = str(fallback.get("answer") or options[0])
            sentence_en = (fallback.get("sentence_en") or sentence_en).strip()
            instruction_ru = (fallback.get("instruction_ru") or instruction_ru).strip()
            tip = (fallback.get("tip") or tip).strip()
            prompt = _build_exercise_display(instruction_ru, sentence_en, sentence_ru, "mcq")
        options = [str(x) for x in options[:4]]
        if answer not in options:
            lower_map = {o.lower(): o for o in options}
            if answer.lower() in lower_map:
                answer = lower_map[answer.lower()]
            else:
                # Никогда не помечаем options[0] «наугад» — берём весь fallback
                options = list(fallback.get("options") or options)
                answer = str(fallback.get("answer") or options[0])
                sentence_en = (fallback.get("sentence_en") or sentence_en).strip()
                instruction_ru = (fallback.get("instruction_ru") or instruction_ru).strip()
                tip = (fallback.get("tip") or tip).strip()
                prompt = _build_exercise_display(instruction_ru, sentence_en, sentence_ru, "mcq")
        if not sentence_ru:
            sentence_ru = translate_exercise_sentence(sentence_en, answer) or ""
        return {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": instruction_ru,
            "sentence_en": sentence_en,
            "sentence_ru": sentence_ru,
            "prompt": prompt,
            "options": options,
            "answer": answer,
            "tip": tip,
            "help_count": 0,
        }

    if not sentence_ru and ex_subtype == "translate_ru":
        sentence_ru = answer
    if not sentence_ru:
        sentence_ru = translate_exercise_sentence(sentence_en, answer, model_answer=answer) or ""

    return {
        "kind": "write",
        "subtype": ex_subtype,
        "instruction_ru": instruction_ru,
        "sentence_en": sentence_en,
        "sentence_ru": sentence_ru,
        "base_form": base_form,
        "prompt": prompt,
        "options": None,
        "answer": answer,
        "tip": tip,
        "help_count": 0,
    }


def _build_exercise_display(
    instruction_ru: str,
    sentence_en: str,
    sentence_ru: str = "",
    subtype: str = "mcq",
) -> str:
    parts = []
    if instruction_ru:
        parts.append(instruction_ru)
    if subtype == "translate_en" and sentence_ru:
        parts.append(sentence_ru)
    elif subtype == "translate_ru" and sentence_en:
        parts.append(sentence_en)
    elif sentence_en:
        parts.append(sentence_en)
    if subtype == "word_form":
        parts.append("✍️ Напиши в чат <b>только форму слова</b>.")
    elif subtype in {"translate_en", "translate_ru"}:
        parts.append(
            "💬 Можешь спросить: «как переводится слово …» — подскажу, задание продолжится."
        )
    return "\n\n".join(parts)


def _fill_blank(sentence_en: str, answer: str) -> str:
    for blank in ("____", "___", "__"):
        if blank in sentence_en:
            return sentence_en.replace(blank, answer, 1)
    return sentence_en


def translate_exercise_sentence(
    sentence_en: str,
    answer: str,
    model_answer: str = "",
) -> str | None:
    """Перевод смысла английского предложения для кнопки «Перевести»."""
    from services.translation import translate_to_russian

    if model_answer and not sentence_en:
        return translate_to_russian(model_answer)
    if not sentence_en:
        return None
    if answer and " " in answer.strip() and "____" not in sentence_en:
        return translate_to_russian(answer)
    filled = _fill_blank(sentence_en, answer)
    return translate_to_russian(filled)


def get_exercise_sentence_translation(exercise: dict) -> str | None:
    ru = (exercise.get("sentence_ru") or "").strip()
    if ru:
        return ru
    return translate_exercise_sentence(
        exercise.get("sentence_en") or "",
        exercise.get("answer") or "",
        model_answer=exercise.get("answer") or "",
    )


def translate_exercise_prompt(prompt: str) -> str | None:
    """Переводит английскую часть задания для кнопки «Перевести»."""
    if not prompt:
        return None
    from services.translation import translate_to_russian

    clean = prompt.replace("<i>", "").replace("</i>", "").strip()
    # Убираем служебные префиксы уровня
    if "\n" in clean:
        lines = [ln for ln in clean.split("\n") if ln.strip() and not ln.strip().startswith("(")]
        clean = "\n".join(lines) if lines else clean
    ru = translate_to_russian(clean)
    if not ru:
        return None
    return ru


def _normalize_text(s: str) -> str:
    return " ".join((s or "").strip().lower().split())


def check_word_form_answer(model_answer: str, user_answer: str) -> bool:
    return _normalize_text(model_answer) == _normalize_text(user_answer)


def check_write_answer(
    level: str,
    topic_title: str,
    prompt: str,
    model_answer: str,
    user_answer: str,
    subtype: str = "write",
) -> dict:
    if subtype == "word_form" and check_word_form_answer(model_answer, user_answer):
        return {"correct": True, "feedback_ru": "Верно!"}

    task_hint = ""
    if subtype == "translate_en":
        task_hint = "Student must translate Russian to English using topic grammar."
    elif subtype == "translate_ru":
        task_hint = "Student must translate English to Russian. Accept close natural Russian."

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "Check student's answer for a grammar exercise. "
                    "Be fair: meaning + target grammar matter more than punctuation. "
                    "For word_form accept only if the word form matches (ignore case). "
                    "For A0/A1 accept very simple answers if grammar target is ok. "
                    f"{task_hint} "
                    'Return ONLY JSON: {"correct":bool,"feedback_ru":"short friendly Russian"}'
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {level}. Topic {topic_title}. Subtype {subtype}.\n"
                    f"Task: {prompt}\nModel: {model_answer}\nStudent: {user_answer}"
                ),
            },
        ],
        {"correct": False, "feedback_ru": "Попробуй ещё раз, чуть точнее по теме."},
        temperature=0.0,
    )
    return data


def generate_grammar_test(level: str, topic_titles: list[str], topic_ids: list[str] | None = None) -> list[dict]:
    """
    10 вопросов из curated-банков тем уровня (без GPT).
    Разнообразие: не больше 2 заданий с одной темы.
    """
    import random

    from data.grammar_curriculum import get_topics
    from data.grammar_exercise_fallbacks import FALLBACKS

    topics = get_topics(level) or []
    if topic_ids and topic_titles and len(topic_ids) == len(topic_titles):
        # сохранить порядок/названия с хендлера
        by_id = {t["id"]: t for t in topics}
        topics = []
        for tid, title in zip(topic_ids, topic_titles):
            base = by_id.get(tid) or {"id": tid, "title": title}
            topics.append({"id": tid, "title": title or base.get("title") or tid})

    pool: list[dict] = []
    for t in topics:
        tid = t["id"]
        title = t.get("title") or tid
        bank = FALLBACKS.get(tid) or []
        for raw in bank:
            item = dict(raw)
            subtype = (item.get("subtype") or ("mcq" if item.get("kind") == "mcq" else "word_form")).strip()
            kind = "mcq" if subtype == "mcq" else "write"
            try:
                ex = _finalize_exercise(item, subtype, kind, item)
            except Exception:
                continue
            ex["topic_id"] = tid
            ex["topic_title"] = title
            pool.append(ex)

    if not pool:
        # крайний случай — старое поведение по одной теме
        titles = topic_titles or ["Grammar"]
        ids = topic_ids or [None] * len(titles)
        questions = []
        for i in range(10):
            title = titles[i % len(titles)]
            tid = ids[i % len(ids)] if ids else None
            num = (i % 3) + 1 if i < 6 else (7 if i % 2 == 0 else 8)
            ex = generate_grammar_exercise(level, title, num, topic_id=tid)
            ex["topic_id"] = tid
            ex["topic_title"] = title
            ex["q_num"] = i + 1
            questions.append(ex)
        return questions

    random.shuffle(pool)
    selected: list[dict] = []
    per_topic: dict[str, int] = {}
    for ex in pool:
        tid = ex.get("topic_id") or "_"
        if per_topic.get(tid, 0) >= 2:
            continue
        selected.append(ex)
        per_topic[tid] = per_topic.get(tid, 0) + 1
        if len(selected) >= 10:
            break

    if len(selected) < 10:
        for ex in pool:
            if ex in selected:
                continue
            selected.append(ex)
            if len(selected) >= 10:
                break

    # если тем мало — можно повторить с другим индексом
    while len(selected) < 10 and pool:
        selected.append(dict(random.choice(pool)))

    out = selected[:10]
    for i, q in enumerate(out):
        q["q_num"] = i + 1
    return out


def format_grammar_test_review(mistakes: list[dict], *, score: int, total: int, passed: bool) -> str:
    """Итог теста + разбор ошибок по разделам."""
    if passed:
        head = (
            f"🏆 <b>Тест сдан!</b> Результат: {score}/{total}.\n"
            "Grammar уровня закрыт — ты красава! 🦜"
        )
    else:
        head = f"🦜 Результат: {score}/{total} — нужно минимум 8."

    if not mistakes:
        if passed:
            return head
        return head + "\nПочти идеально, попробуй ещё раз!"

    lines = [head, "", "<b>Где ошибки:</b>"]
    weak: list[str] = []
    for m in mistakes:
        n = m.get("q_num") or "?"
        topic = m.get("topic_title") or "тема"
        correct = m.get("correct") or "—"
        your = m.get("your") or "—"
        lines.append(
            f"• Вопрос {n} · <b>{topic}</b>\n"
            f"  твой: <i>{your}</i> → верно: <b>{correct}</b>"
        )
        if topic not in weak:
            weak.append(topic)
    lines.append("")
    lines.append("<b>Стоит подтянуть:</b> " + ", ".join(f"«{t}»" for t in weak))
    if not passed:
        lines.append("Повтори эти разделы в Grammar и пройди тест снова.")
    else:
        lines.append("Можно ещё раз глянуть эти темы для закрепления 💪")
    return "\n".join(lines)


def rico_help_for_exercise(
    level: str,
    topic_title: str,
    prompt: str,
    options: list[str] | None,
    reveal: bool = False,
    answer: str = "",
) -> str:
    opt_txt = ", ".join(options) if options else "(письменный ответ)"
    if reveal:
        fallback = (
            f"🦜 Правильный ответ: <b>{answer}</b>.\n"
            "Запомни правило и иди к следующему заданию!"
        )
    else:
        fallback = "🦜 Подсказка: вспомни правило темы и отбрось лишнее. Ты справишься!"

    try:
        if reveal:
            system = (
                "Ты Рико 🦜 — живой тёплый репетитор в Telegram, говоришь как друг, не как учебник. "
                "Объяви правильный ответ и коротко объясни НА РУССКОМ, почему он верный. "
                "Живой тон, можно лёгкую шутку. English example + <i>русский перевод</i>. "
                f"Правильный ответ: {answer}. HTML ok. Без канцелярита."
            )
        else:
            system = (
                "Ты Рико 🦜 — живой тёплый репетитор. Дай ПОДСКАЗКУ НА РУССКОМ по заданию. "
                "Говори разговорно, как будто сидишь рядом: «смотри…», «попробуй подумать…». "
                "НЕ называй правильный вариант и НЕ цитируй ответ дословно. "
                "Наведи на правило через мини-пример из жизни. Коротко. HTML: можно <i>."
            )
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system},
                    {
                        "role": "user",
                        "content": (
                            f"Уровень {level}, тема {topic_title}.\n"
                            f"Задание: {prompt}\nВарианты: {opt_txt}"
                        ),
                    },
                ],
                "max_tokens": 280,
                "temperature": 0.4,
            },
            timeout=25,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        if not text.startswith("🦜"):
            text = f"🦜 {text}"
        return text
    except Exception as e:
        logging.error(f"Rico help error: {e}")
        return fallback


def rico_explain_wrong_final(
    level: str,
    topic_title: str,
    prompt: str,
    answer: str,
) -> str:
    fallback = (
        f"🦜 Неправильно. Правильный ответ: <b>{answer}</b>.\n"
        "Разбери пример и иди дальше 💪"
    )
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Ты Рико 🦜. Ученик ошибся в последний раз. "
                            "Скажи, что неправильно, назови правильный ответ и коротко объясни "
                            "на русском + английский пример с <i>переводом</i>. HTML ok."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Уровень {level}, тема {topic_title}.\n"
                            f"Задание: {prompt}\nПравильный ответ: {answer}"
                        ),
                    },
                ],
                "max_tokens": 280,
                "temperature": 0.4,
            },
            timeout=25,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        if not text.startswith("🦜"):
            text = f"🦜 {text}"
        return text
    except Exception as e:
        logging.error(f"Rico final explain error: {e}")
        return fallback
