"""
Рико: тексты Vocabulary, карточки слов/фраз, проверка предложений.
"""

import logging
import random
import re

from services.gpt import _ask_json


def highlight_target_terms(text: str, terms: list[str]) -> str:
    """
    Выделить целевые слова/фразы жирным <b>…</b> в тексте.
    Снимает старые <i>/<b>, затем оборачивает термины (длинные первыми).
    """
    out = re.sub(r"</?(?:b|i|strong|em)>", "", text or "", flags=re.IGNORECASE)
    cleaned: list[str] = []
    seen: set[str] = set()
    for t in terms or []:
        s = (t or "").strip()
        if not s:
            continue
        key = s.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(s)
    cleaned.sort(key=len, reverse=True)
    for term in cleaned:
        if " " in term or "-" in term:
            pat = re.compile(re.escape(term), re.IGNORECASE)
        else:
            pat = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)

        def _repl(m: re.Match, _term=term) -> str:
            return f"<b>{m.group(0)}</b>"

        out = pat.sub(_repl, out)
    # убрать случайное двойное выделение
    out = re.sub(r"<b>\s*<b>(.*?)</b>\s*</b>", r"<b>\1</b>", out, flags=re.IGNORECASE | re.DOTALL)
    return out


def generate_vocab_text(
    level: str,
    topic_title: str,
    words: list[dict],
    *,
    kind: str = "words",
) -> dict:
    """
    kind=words: 6-7 предложений, целевые слова жирным
    kind=phrases: до 5 предложений, 2 фразы жирным
    """
    if kind == "phrases":
        labels = [p["en"] for p in words[:2]]
        count = 2
        fallback_en = (
            f"My family is very important to me. We often say <b>{labels[0] if labels else 'family first'}</b> "
            f"when we talk. Last weekend we had dinner together. "
            f"My grandmother told us <b>{labels[1] if len(labels) > 1 else 'home sweet home'}</b> "
            f"and everyone smiled."
        )
        fallback_ru = (
            "Моя семья очень важна для меня. Мы часто говорим выделенную фразу, когда разговариваем. "
            "В прошлые выходные мы ужинали вместе. Бабушка сказала вторую фразу — и все улыбнулись."
        )
    else:
        labels = [w["en"] for w in words[:5]]
        count = min(5, len(labels))
        fallback_en = (
            f"Today I want to tell you about {topic_title.lower()}. "
            f"I see my <b>{labels[0] if labels else 'friend'}</b> every day. "
            f"We like to <b>{labels[1] if len(labels) > 1 else 'talk'}</b> together. "
            f"Sometimes we visit a <b>{labels[2] if len(labels) > 2 else 'place'}</b> nearby. "
            f"It makes me feel <b>{labels[3] if len(labels) > 3 else 'happy'}</b>. "
            f"I hope you enjoy these new words!"
        )
        fallback_ru = (
            f"Сегодня расскажу про тему «{topic_title}». "
            "Я каждый день вижу выделенных людей и места. "
            "Нам нравится проводить время вместе. "
            "Иногда мы ходим в интересные места рядом. "
            "Это делает меня счастливым. Надеюсь, тебе понравятся новые слова!"
        )

    word_list = "\n".join(f"- {w['en']} ({w['ru']})" for w in words[:count])
    system = (
        "Create a short English story for a vocabulary lesson. "
        "Return ONLY JSON: "
        '{"text_en":"...","text_ru":"...","highlighted":["word1",...]} '
        f"Level {level}, topic {topic_title}. "
    )
    if kind == "phrases":
        system += (
            "Max 5 sentences. Wrap EXACTLY 2 given phrases in <b>...</b> in the English text. "
            "highlighted = list of 2 English phrases without tags."
        )
    else:
        system += (
            "6-7 sentences. Wrap EVERY given target word in <b>...</b> in the English text "
            "(bold HTML, not italic). "
            "highlighted = list of English words used (without tags)."
        )

    data = _ask_json(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Use these items:\n{word_list}\nSeed {random.random()}"},
        ],
        {
            "text_en": fallback_en,
            "text_ru": fallback_ru,
            "highlighted": labels[:count],
        },
        temperature=0.75,
        max_tokens=500,
    )
    highlighted = data.get("highlighted") or labels[:count]
    if not isinstance(highlighted, list):
        highlighted = labels[:count]
    highlighted = [str(x) for x in highlighted[:count]] or labels[:count]
    # гарантируем жирное выделение целевых слов из батча
    text_en = highlight_target_terms((data.get("text_en") or fallback_en).strip(), labels[:count])
    return {
        "text_en": text_en,
        "text_ru": (data.get("text_ru") or fallback_ru).strip(),
        "highlighted": highlighted,
    }


def _diverse_word_examples(en: str, ru: str) -> tuple[str, str, str, str]:
    """Локальные разнообразные примеры (не один шаблон на все слова)."""
    w = (en or "word").strip()
    r = (ru or "").strip() or w
    templates = [
        (
            f"I can't imagine my day without this {w}.",
            f"Не представляю свой день без этого: «{r}».",
            f"Could you explain what {w} means in this context?",
            f"Можешь объяснить, что значит «{r}» в этом контексте?",
        ),
        (
            f"She mentioned {w} twice during the meeting.",
            f"Она дважды упомянула «{r}» на встрече.",
            f"That's a useful {w} to remember.",
            f"Это полезное слово «{r}», его стоит запомнить.",
        ),
        (
            f"We talked about {w} all evening.",
            f"Мы весь вечер говорили про «{r}».",
            f"I finally understood {w} after a few examples.",
            f"Я наконец понял(а) «{r}» после нескольких примеров.",
        ),
        (
            f"Is {w} formal or casual English?",
            f"«{r}» — это формальный или разговорный английский?",
            f"He used {w} in a really natural way.",
            f"Он использовал «{r}» очень естественно.",
        ),
        (
            f"Don't forget to practise {w} out loud.",
            f"Не забудь потренировать «{r}» вслух.",
            f"I heard {w} in a podcast yesterday.",
            f"Вчера услышал(а) «{r}» в подкасте.",
        ),
        (
            f"My friend always says {w} when she's excited.",
            f"Моя подруга всегда говорит «{r}», когда радуется.",
            f"Using {w} correctly takes a bit of practice.",
            f"Правильно использовать «{r}» — дело практики.",
        ),
        (
            f"There's a big difference between {w} and similar words.",
            f"Между «{r}» и похожими словами большая разница.",
            f"Can you make a sentence with {w}?",
            f"Можешь составить предложение со словом «{r}»?",
        ),
        (
            f"I looked up {w} and it clicked immediately.",
            f"Я посмотрел(а) «{r}» — и сразу щёлкнуло.",
            f"Please write {w} in your notebook.",
            f"Запиши «{r}» в тетрадь.",
        ),
    ]
    # стабильный выбор по слову — разные слова → разные шаблоны
    idx = sum(ord(c) for c in w.lower()) % len(templates)
    return templates[idx]


def _format_word_card(word: dict, data: dict) -> str:
    en = word["en"]
    ru = word["ru"]
    emoji = word.get("emoji") or "📘"
    meaning = (data.get("meaning_ru") or f"Это значит «{ru}».").strip()
    assoc = (data.get("association_ru") or "").strip()
    e1d, e1rd, e2d, e2rd = _diverse_word_examples(en, ru)
    e1 = (data.get("example1_en") or e1d).strip()
    e1r = (data.get("example1_ru") or e1rd).strip()
    e2 = (data.get("example2_en") or e2d).strip()
    e2r = (data.get("example2_ru") or e2rd).strip()
    # если GPT/старый фолбэк выдал один и тот же банальный шаблон — подменим
    bland = (
        f"today i learned {en}".lower() in e1.lower()
        or f"today i learned {en}".lower() in e2.lower()
        or e1.lower().startswith("i know the word")
        or e2.lower().startswith("i know the word")
        or e1.lower() == e2.lower()
    )
    if bland:
        e1, e1r, e2, e2r = e1d, e1rd, e2d, e2rd

    lines = [
        f"🦜 {emoji} <b>{en}</b> — <i>{ru}</i>",
        "",
        f"<b>Что значит:</b> {meaning}",
    ]
    if assoc:
        lines.append(f"<b>Запомни:</b> {assoc}")
    lines += [
        "",
        "<b>Примеры:</b>",
        f"1. {e1}",
        f"<i>{e1r}</i>",
        f"2. {e2}",
        f"<i>{e2r}</i>",
        "",
        "✍️ Напиши <b>одно предложение</b> с этим словом на английском.",
    ]
    return "\n".join(lines)


def rico_word_card(level: str, topic_title: str, word: dict) -> str:
    en = word["en"]
    ru = word["ru"]
    emoji = word.get("emoji") or "📘"
    e1, e1r, e2, e2r = _diverse_word_examples(en, ru)
    fallback = {
        "meaning_ru": f"Слово «{en}» значит «{ru}».",
        "association_ru": f"Представь картинку с эмодзи {emoji} — и сразу вспоминается «{ru}».",
        "example1_en": e1,
        "example1_ru": e1r,
        "example2_en": e2,
        "example2_ru": e2r,
    }
    try:
        data = _ask_json(
            [
                {
                    "role": "system",
                    "content": (
                        "Ты Рико 🦜 — дружелюбный репетитор английского для русскоязычных. "
                        "Объясни слово ТОЛЬКО по-русски (кроме самих английских примеров). "
                        "Верни JSON:\n"
                        "{"
                        '"meaning_ru":"краткое понятное объяснение на русском",'
                        '"association_ru":"короткая ассоциация/мнемоника на русском",'
                        '"example1_en":"живое предложение со словом (не шаблон)",'
                        '"example1_ru":"перевод примера 1 на русский",'
                        '"example2_en":"ДРУГОЕ живое предложение со словом",'
                        '"example2_ru":"перевод примера 2 на русский"'
                        "}\n"
                        "FORBIDDEN templates: 'Today I learned …', 'I know the word …', "
                        "'This is my …', 'I use … every day' as the only pattern. "
                        "Make two DIFFERENT natural sentences. "
                        f"Эмодзи для ассоциации: {emoji}. Уровень CEFR: {level}."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Тема: {topic_title}. Слово: {en} = {ru}. Seed {random.random()}",
                },
            ],
            fallback,
            temperature=0.75,
            max_tokens=380,
        )
        return _format_word_card(word, data if isinstance(data, dict) else fallback)
    except Exception as e:
        logging.error(f"rico_word_card: {e}")
        return _format_word_card(word, fallback)


def _diverse_phrase_examples(en: str, ru: str) -> tuple[str, str, str, str]:
    p = (en or "phrase").strip()
    r = (ru or "").strip() or p
    templates = [
        (
            f"In that situation I'd probably say, \"{p}\".",
            f"В такой ситуации я, скорее всего, скажу: «{r}».",
            f"Native speakers use \"{p}\" all the time in chats.",
            f"Носители постоянно пишут «{r}» в переписке.",
        ),
        (
            f"She replied with \"{p}\" and smiled.",
            f"Она ответила «{r}» и улыбнулась.",
            f"If someone helps you, \"{p}\" sounds natural.",
            f"Если тебе помогли, «{r}» звучит естественно.",
        ),
        (
            f"I overheard someone say \"{p}\" on the bus.",
            f"В автобусе услышал(а), как кто-то сказал «{r}».",
            f"Try dropping \"{p}\" into your next conversation.",
            f"Попробуй вставить «{r}» в следующий разговор.",
        ),
        (
            f"\"{p}\" fits better than a long formal sentence here.",
            f"Здесь «{r}» уместнее, чем длинная формальная фраза.",
            f"He always opens with \"{p}\" when he calls.",
            f"Он всегда начинает звонок с «{r}».",
        ),
        (
            f"Don't translate it word for word — just say \"{p}\".",
            f"Не переводи дословно — просто скажи «{r}».",
            f"I finally started using \"{p}\" without thinking.",
            f"Я наконец начал(а) говорить «{r}» не задумываясь.",
        ),
    ]
    idx = sum(ord(c) for c in p.lower()) % len(templates)
    return templates[idx]


def _format_phrase_card(phrase: dict, data: dict) -> str:
    en = phrase["en"]
    ru = phrase["ru"]
    emoji = phrase.get("emoji") or "💬"
    meaning = (data.get("meaning_ru") or f"Это значит «{ru}».").strip()
    when = (data.get("when_ru") or "").strip()
    assoc = (data.get("association_ru") or "").strip()
    e1d, e1rd, e2d, e2rd = _diverse_phrase_examples(en, ru)
    e1 = (data.get("example1_en") or e1d).strip()
    e1r = (data.get("example1_ru") or e1rd).strip()
    e2 = (data.get("example2_en") or e2d).strip()
    e2r = (data.get("example2_ru") or e2rd).strip()
    bland = (
        f"i say '{en}'".lower() in e1.lower()
        or f"everyone knows '{en}'".lower() in e2.lower()
        or e1.lower() == e2.lower()
    )
    if bland:
        e1, e1r, e2, e2r = e1d, e1rd, e2d, e2rd

    lines = [
        f"🦜 {emoji} <b>{en}</b>",
        f"<i>{ru}</i>",
        "",
        f"<b>Что значит:</b> {meaning}",
    ]
    if when:
        lines.append(f"<b>Когда говорят:</b> {when}")
    if assoc:
        lines.append(f"<b>Запомни:</b> {assoc}")
    lines += [
        "",
        "<b>Примеры:</b>",
        f"1. {e1}",
        f"<i>{e1r}</i>",
        f"2. {e2}",
        f"<i>{e2r}</i>",
        "",
        "✍️ Напиши предложение с этой фразой на английском.",
    ]
    return "\n".join(lines)


def rico_phrase_card(level: str, topic_title: str, phrase: dict) -> str:
    en = phrase["en"]
    ru = phrase["ru"]
    emoji = phrase.get("emoji") or "💬"
    e1, e1r, e2, e2r = _diverse_phrase_examples(en, ru)
    fallback = {
        "meaning_ru": f"Фраза «{en}» значит «{ru}».",
        "when_ru": "Говорят в повседневных ситуациях по смыслу фразы.",
        "association_ru": f"Эмодзи {emoji} поможет вспомнить «{ru}».",
        "example1_en": e1,
        "example1_ru": e1r,
        "example2_en": e2,
        "example2_ru": e2r,
    }
    try:
        data = _ask_json(
            [
                {
                    "role": "system",
                    "content": (
                        "Ты Рико 🦜. Объясни устойчивую фразу ТОЛЬКО по-русски "
                        "(примеры предложений — на английском + перевод). JSON:\n"
                        "{"
                        '"meaning_ru":"...",'
                        '"when_ru":"когда говорят",'
                        '"association_ru":"...",'
                        '"example1_en":"живое предложение с фразой",'
                        '"example1_ru":"...",'
                        '"example2_en":"другое живое предложение",'
                        '"example2_ru":"..."'
                        "}\n"
                        "FORBIDDEN: 'I say … to friends', 'Everyone knows …' as templates. "
                        "Two DIFFERENT natural examples. "
                        f"Эмодзи: {emoji}. Уровень: {level}."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Тема: {topic_title}. Фраза: {en} = {ru}. Seed {random.random()}",
                },
            ],
            fallback,
            temperature=0.75,
            max_tokens=380,
        )
        return _format_phrase_card(phrase, data if isinstance(data, dict) else fallback)
    except Exception as e:
        logging.error(f"rico_phrase_card: {e}")
        return _format_phrase_card(phrase, fallback)


def check_vocab_sentence(
    level: str,
    target_en: str,
    user_sentence: str,
    *,
    is_phrase: bool = False,
) -> dict:
    kind = "phrase" if is_phrase else "word"
    target = (target_en or "").strip()
    sentence = (user_sentence or "").strip()

    def _coerce_correct(val) -> bool:
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return bool(val)
        if isinstance(val, str):
            return val.strip().lower() in {"1", "true", "yes", "да", "ok", "верно"}
        return False

    import re

    tokens = re.findall(r"[a-zA-Z']+", sentence)
    # Одно слово / просто цель — это не предложение
    if len(tokens) < 3:
        return {
            "correct": False,
            "feedback_ru": (
                "Это не предложение. Напиши полное предложение на английском "
                f"(минимум 3 слова) с {kind} «{target}»."
            ),
            "better_en": "",
            "errors_ru": "Слишком коротко — нужна целая фраза.",
        }

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    f"You are Rico 🦜, a careful English tutor. Check the student's sentence.\n"
                    f"The sentence MUST use the target {kind} naturally and make LOGICAL sense.\n"
                    "Find grammar mistakes AND nonsense/logic problems "
                    "(wrong meaning, impossible situation, word salad).\n"
                    "Return ONLY JSON:\n"
                    "{"
                    '"correct":true/false,'
                    '"feedback_ru":"по-русски: что не так или краткая похвала",'
                    '"errors_ru":"по-русски коротко перечисли ошибки (или пусто если всё ок)",'
                    '"better_en":"исправленное естественное предложение С целевым словом/фразой"'
                    "}\n"
                    "correct=true ONLY if: target is used, grammar is basically ok for the level, "
                    "and the sentence is meaningful. "
                    "If student only stuffed the target with broken English → correct=false.\n"
                    "If wrong: always fill better_en with a natural corrected sentence."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Level {level}. Target {kind}: «{target}»\n"
                    f"Student sentence: {sentence}"
                ),
            },
        ],
        {
            "correct": False,
            "feedback_ru": f"Исправь предложение и обязательно используй «{target}».",
            "errors_ru": "",
            "better_en": "",
        },
        temperature=0.1,
        max_tokens=320,
    )
    if not isinstance(data, dict):
        data = {
            "correct": False,
            "feedback_ru": "Попробуй ещё раз.",
            "errors_ru": "",
            "better_en": "",
        }

    ok = _coerce_correct(data.get("correct"))
    # Не засчитываем автоматически только из-за наличия слова — ошибки должны ловиться
    data["correct"] = ok
    data["feedback_ru"] = str(data.get("feedback_ru") or "").strip()
    data["errors_ru"] = str(data.get("errors_ru") or "").strip()
    data["better_en"] = "" if ok else str(data.get("better_en") or "").strip()
    return data


def rico_dont_remember(item: dict, *, is_phrase: bool = False) -> str:
    en = item["en"]
    ru = item["ru"]
    emoji = item.get("emoji") or "💡"
    kind = "фраза" if is_phrase else "слово"
    if is_phrase:
        ex_en = f"People often say '{en}'."
        ex_ru = f"Люди часто говорят: «{ru}»."
    else:
        base = en[3:].strip() if en.lower().startswith("to ") else en
        ex_en = f"I learned the word {en} today."
        ex_ru = f"Сегодня я выучил(а) слово «{ru}»."
    return (
        f"🦜 {emoji} Не страшно! <b>{en}</b> — <i>{ru}</i>\n\n"
        f"Запомни: {kind} «{en}» = {ru}.\n"
        f"Пример: <b>{ex_en}</b>\n"
        f"<i>{ex_ru}</i>\n\n"
        "Дальше следующее задание 👇"
    )
