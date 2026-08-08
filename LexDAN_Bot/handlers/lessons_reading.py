"""Раздел Reading — 3 задания (пока только MANAGER_ID)."""

from __future__ import annotations

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import MANAGER_ID
from handlers.filters import ModeFilter
from handlers.lesson_filters import LessonHubFilter
from handlers.lesson_keyboards import level_sections_kb
from data.reading_topics import topics_for_level, topic_by_button_label, get_topic
from services.database import MODE_LESSONS, load_users, get_user
from services.lesson_state import assessment_busy, ensure_lesson, set_level_hub
from services.reading_state import (
    ensure_reading,
    is_topic_done,
    set_reading_list,
    set_reading_hub,
    get_session,
    set_session,
    update_session,
    clear_session,
    mark_topic_done,
)
from services.reading_gen import (
    generate_reading_pack,
    parse_gap_answers,
    check_one_gap,
    normalize_gap_token,
    hint_gap_fill,
    explain_gap_fill,
    judge_comprehension_answer,
    judge_retelling,
)

router = Router()

BTN_READING = "📖 Reading"
BTN_EXIT = "🚪 Выйти из Reading"
BTN_BACK_SECTIONS = "⬅️ К разделам"
BTN_READY = "✅ Начать задание 1"


def reading_allowed(user_id: str | int) -> bool:
    try:
        return int(user_id) == int(MANAGER_ID)
    except (TypeError, ValueError):
        return False


def reading_topics_kb(level: str, user: dict) -> ReplyKeyboardMarkup:
    rows = []
    row = []
    for i, t in enumerate(topics_for_level(level), start=1):
        done = is_topic_done(user, level, t["id"])
        label = f"{i}. {t['title_ru']}" + (" ✅" if done else "")
        row.append(KeyboardButton(text=label))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text=BTN_BACK_SECTIONS)])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _exit_kb(*extra_rows: list[KeyboardButton]) -> ReplyKeyboardMarkup:
    rows = list(extra_rows)
    rows.append([KeyboardButton(text=BTN_EXIT)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def intro_kb() -> ReplyKeyboardMarkup:
    return _exit_kb([KeyboardButton(text=BTN_READY)])


async def open_reading_for_level(m: Message, user: dict, level: str) -> None:
    uid = str(m.from_user.id)
    if not reading_allowed(uid):
        await m.answer(
            "📖 Reading скоро откроется. Пока раздел на проверке 🦜",
            reply_markup=level_sections_kb(user=user, user_id=uid),
        )
        return
    set_reading_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    ensure_reading(user)
    await m.answer(
        f"📖 <b>Reading · {level}</b>\n\n"
        "Выбери тему — короткий текст + 3 задания.\n"
        "Чтобы закрыть тему галочкой, нужно пройти все 3 задания подряд.\n"
        "Если выйдешь раньше — прогресс темы сбросится, текст будет новый.",
        reply_markup=reading_topics_kb(level, user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_READING)
async def open_reading_section(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    if (user.get("lesson") or {}).get("hub") != "level_hub":
        return
    level = (user.get("lesson") or {}).get("level") or user.get("level") or "A1"
    await open_reading_for_level(m, user, level)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("reading_list"), F.text == BTN_BACK_SECTIONS)
async def reading_back_sections(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    level = (user.get("lesson") or {}).get("level") or user.get("level") or "A1"
    clear_session(str(m.from_user.id))
    set_level_hub(str(m.from_user.id), level)
    await m.answer(
        f"🎓 Уровень {level} — выбери раздел:",
        reply_markup=level_sections_kb(user_id=m.from_user.id),
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("reading_list"), F.text)
async def reading_pick_topic(m: Message):
    text = (m.text or "").strip()
    if text in {BTN_BACK_SECTIONS, "🔙 Вернуться в меню", BTN_EXIT}:
        return
    if not reading_allowed(m.from_user.id):
        return
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    level = (user.get("lesson") or {}).get("level") or "A1"
    topic = topic_by_button_label(level, text)
    if not topic:
        await m.answer("Выбери тему кнопкой ниже.", reply_markup=reading_topics_kb(level, user))
        return

    await m.answer(
        f"🦜 <b>Рико:</b> Тема «{topic['title_ru']}».\n\n"
        "Будет текст на английском и 3 задания:\n"
        "1️⃣ Заполни пропуски (2 попытки)\n"
        "2️⃣ Ответы на вопросы полными предложениями\n"
        "3️⃣ Пересказ по плану\n\n"
        "Нажми <b>Начать задание 1</b>.\n"
        "⚠️ Выход сбросит прогресс этой попытки.",
        reply_markup=intro_kb(),
        parse_mode="HTML",
    )
    set_session(
        str(m.from_user.id),
        {
            "level": level,
            "topic_id": topic["id"],
            "topic_title": topic["title_ru"],
            "phase": "intro",
            "content": None,
        },
    )
    set_reading_hub(str(m.from_user.id), "reading_play")


@router.message(
    ModeFilter(MODE_LESSONS),
    LessonHubFilter("reading_play", "reading_task1", "reading_task2", "reading_task3"),
    F.text == BTN_EXIT,
)
async def reading_exit(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    level = (get_session(user) or {}).get("level") or (user.get("lesson") or {}).get("level") or "A1"
    clear_session(str(m.from_user.id))
    set_reading_list(str(m.from_user.id), level)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.answer(
        "Ок, вышли. Прогресс этой попытки сброшен — тема не засчитана.\n"
        "Можешь выбрать тему снова (будет новая генерация).",
        reply_markup=reading_topics_kb(level, user),
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("reading_play"), F.text == BTN_READY)
async def reading_ready(m: Message):
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user)
    if not sess or sess.get("phase") != "intro":
        return
    level = sess["level"]
    topic = get_topic(level, sess["topic_id"]) or {
        "id": sess["topic_id"],
        "title_ru": sess.get("topic_title") or "Тема",
        "title_en": "Topic",
        "focus": "everyday reading",
    }

    from services.tg_out import status

    async with status(m, "🦜 Рико готовит текст…"):
        pack = generate_reading_pack(level, topic)

    update_session(
        uid,
        content=pack,
        phase="task1",
        task1_filled=[None, None, None, None, None],
        task1_next=0,
        task1_fails=0,
        task2_i=0,
        task2_tries=0,
    )
    set_reading_hub(uid, "reading_task1")
    await _send_task1(m, uid)


def _format_review_line(topic: str, level: str) -> str:
    return f"📚 Повтори в Grammar: <b>{topic}</b> (уровень <b>{level}</b>)"


async def _send_task1(m: Message, uid: str) -> None:
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    pack = sess.get("content") or {}
    filled = list(sess.get("task1_filled") or [None] * 5)
    bank = ", ".join(pack.get("word_bank") or [])
    gapped = pack.get("gapped_text") or ""

    status_lines = []
    for i, w in enumerate(filled, start=1):
        status_lines.append(f"{i}. {w if w else '…'}")

    await m.answer(
        "📝 <b>Задание 1 · Заполни пропуски по смыслу</b>\n\n"
        "В тексте 5 пропусков. Ниже 6 слов — одно лишнее.\n"
        "Каждый пропуск однозначно читается из <b>остального текста</b>.\n"
        "Напиши <b>5 слов через запятую</b> по порядку "
        "или по одному слову.\n"
        "У тебя <b>2 попытки</b> на комбинацию: после первой ошибки Рико подскажет "
        "(без ответа), после второй — разберёт и перейдёте дальше.\n\n"
        f"{gapped}\n\n"
        f"<b>Слова:</b> {bank}\n\n"
        f"<b>Сейчас заполнено:</b>\n" + "\n".join(status_lines),
        reply_markup=_exit_kb(),
        parse_mode="HTML",
    )


def _apply_gap_list(words: list[str], answers: list[str], filled: list) -> tuple[list, list[tuple[int, str]]]:
    """Returns (new_filled, wrong_pairs as 1-based index + user word)."""
    wrong: list[tuple[int, str]] = []
    new_filled = list(filled)
    for i, w in enumerate(words[:5]):
        if check_one_gap(w, answers[i]):
            new_filled[i] = answers[i]
        else:
            if new_filled[i] != answers[i]:
                new_filled[i] = None
            wrong.append((i + 1, w))
    return new_filled, wrong


async def _task1_fail_flow(
    m: Message,
    uid: str,
    *,
    level: str,
    pack: dict,
    answers: list[str],
    filled: list,
    wrong: list[tuple[int, str]],
) -> None:
    fails = int((get_session(get_user(load_users(), uid)) or {}).get("task1_fails") or 0)
    gapped = pack.get("gapped_text") or ""
    bank = list(pack.get("word_bank") or [])

    if fails <= 0:
        update_session(uid, task1_filled=filled, task1_fails=1)
        from services.tg_out import status

        async with status(m, "🦜 Рико смотрит пропуски…"):
            hint = hint_gap_fill(
                level=level,
                gapped=gapped,
                word_bank=bank,
                answers=answers,
                wrong_pairs=wrong,
            )
        await m.answer(
            f"{hint}\n\n"
            "🔁 Это была первая попытка — ответ не раскрываю. "
            "Собери комбинацию ещё раз.",
            parse_mode="HTML",
        )
        await _send_task1(m, uid)
        return

    from services.tg_out import status

    async with status(m, "🦜 Рико разбирает ошибки…"):
        expl = explain_gap_fill(
            level=level,
            gapped=gapped,
            answers=answers,
            wrong_pairs=wrong,
        )
    correct = ", ".join(answers)
    review = _format_review_line(
        expl.get("review_topic") or "Present Simple",
        expl.get("review_level") or level,
    )
    await m.answer(
        f"{expl.get('explain_ru')}\n\n"
        f"✅ Правильная комбинация: <b>{correct}</b>\n"
        f"{review}\n\n"
        "Идём ко второму заданию.",
        parse_mode="HTML",
    )
    update_session(uid, task1_filled=list(answers), task1_fails=2)
    await _start_task2(m, uid)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("reading_task1"), F.text)
async def reading_task1_answer(m: Message):
    text = (m.text or "").strip()
    if text in {BTN_EXIT, BTN_READY, BTN_BACK_SECTIONS}:
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    pack = sess.get("content") or {}
    level = sess.get("level") or "A1"
    answers = list(pack.get("answers") or [])
    if len(answers) < 5:
        await m.answer("Что-то пошло не так с текстом. Выйди и зайди в тему снова.")
        return
    filled = list(sess.get("task1_filled") or [None] * 5)
    next_i = int(sess.get("task1_next") or 0)

    parsed = parse_gap_answers(text, need=5)
    if "," in text or ";" in text or "\n" in text:
        if parsed is None:
            await m.answer(
                "Нужно ровно <b>5 слов</b> через запятую (по пропускам 1–5), "
                "или одно слово для следующего пропуска.",
                parse_mode="HTML",
            )
            return

    if parsed is not None and len(parsed) == 5:
        filled, wrong = _apply_gap_list(parsed, answers, filled)
        if wrong:
            await _task1_fail_flow(
                m, uid, level=level, pack=pack, answers=answers, filled=filled, wrong=wrong
            )
            return
        update_session(uid, task1_filled=filled)
    else:
        target = next((i for i, w in enumerate(filled) if w is None), None)
        if target is None:
            await m.answer("Все пропуски уже заполнены верно!")
            await _start_task2(m, uid)
            return
        if 0 <= next_i < 5 and filled[next_i] is None:
            target = next_i
        word = text.strip()
        if check_one_gap(word, answers[target]):
            filled[target] = answers[target]
            update_session(uid, task1_filled=filled, task1_next=target + 1)
            await m.answer(f"✅ Пропуск {target + 1} верно: <b>{answers[target]}</b>", parse_mode="HTML")
        else:
            await _task1_fail_flow(
                m,
                uid,
                level=level,
                pack=pack,
                answers=answers,
                filled=filled,
                wrong=[(target + 1, word)],
            )
            return

    if all(filled[i] == answers[i] for i in range(5)):
        await m.answer(
            "🏆 Отличный результат! Все слова подобраны верно.\n"
            "Переходим ко второму заданию…"
        )
        await _start_task2(m, uid)
        return

    empty = [str(i + 1) for i, w in enumerate(filled) if w is None]
    await m.answer(
        "✅ Часть пропусков верна. Осталось: " + ", ".join(empty) + ".\n"
        "Можно одно слово или снова 5 через запятую."
    )
    update_session(uid, task1_filled=filled)
    await _send_task1(m, uid)


async def _start_task2(m: Message, uid: str) -> None:
    update_session(uid, phase="task2", task2_i=0, task2_tries=0)
    set_reading_hub(uid, "reading_task2")
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    pack = sess.get("content") or {}
    full = pack.get("full_text") or ""
    await m.answer(
        "📝 <b>Задание 2 · Вопросы по тексту</b>\n\n"
        "🦜 Рико: 4 вопроса по тексту. Отвечай на английском своими словами — "
        "шаблон не нужен (и <i>Her father is a doctor</i>, и <i>Lena's father is a doctor</i> — ок).\n"
        "Смотрю только факты и грамматику (времена, формы слов). "
        "Регистр и запятые не трогаю.\n"
        "Если перепутал факт — помогу и дам ещё попытку. "
        "Если факт верный, а грамматика хромает — поправлю и идём дальше.\n\n"
        f"<b>Текст:</b>\n{full}",
        reply_markup=_exit_kb(),
        parse_mode="HTML",
    )
    await _send_task2_q(m, uid)


async def _send_task2_q(m: Message, uid: str) -> None:
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    qs = (sess.get("content") or {}).get("questions") or []
    i = int(sess.get("task2_i") or 0)
    if i >= len(qs):
        await _start_task3(m, uid)
        return
    q = qs[i]
    await m.answer(
        f"<b>Вопрос {i + 1}/4</b>\n\n{q.get('q')}\n\n"
        "<i>Ответь предложением своими словами — без шаблона.</i>",
        reply_markup=_exit_kb(),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("reading_task2"), F.text)
async def reading_task2_answer(m: Message):
    text = (m.text or "").strip()
    if text in {BTN_EXIT, BTN_READY}:
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    pack = sess.get("content") or {}
    level = sess.get("level") or "A1"
    qs = pack.get("questions") or []
    i = int(sess.get("task2_i") or 0)
    tries = int(sess.get("task2_tries") or 0)
    if i >= len(qs):
        return
    q = qs[i]

    from services.tg_out import status

    async with status(m, "🦜 Рико читает ответ…"):
        verdict = judge_comprehension_answer(
            level=level,
            question=str(q.get("q") or ""),
            accept=list(q.get("accept") or []),
            model_en=str(q.get("model_en") or ""),
            quote=str(q.get("quote") or ""),
            full_text=str(pack.get("full_text") or ""),
            user_text=text,
        )

    fact_ok = bool(verdict.get("fact_ok") or verdict.get("meaning_ok"))
    grammar_ok = bool(verdict.get("grammar_ok", True))
    need_fs = bool(verdict.get("need_full_sentence"))
    better = (verdict.get("better_en") or q.get("model_en") or "").strip()
    feedback = (verdict.get("feedback_ru") or "").strip()

    # Обрывок вроде «doctor» — попросить предложение, попытку не сжигаем
    if need_fs and fact_ok:
        await m.answer(
            f"{feedback or '🦜 Рико: Факт верный — напиши полным предложением.'}",
            parse_mode="HTML",
        )
        return

    # Факт + грамматика ок
    if fact_ok and grammar_ok:
        quote = q.get("quote") or ""
        msg = "✅ Верно!"
        if quote:
            msg += f"\nВ тексте: «{quote}»"
        await m.answer(msg)
        update_session(uid, task2_i=i + 1, task2_tries=0)
        await _send_task2_q(m, uid)
        return

    # Факт верный, грамматика нет — правим и идём дальше (без второй попытки)
    if fact_ok and not grammar_ok:
        parts = [feedback or "🦜 Рико: Факт верный, чуть поправлю грамматику."]
        if better:
            parts.append(f"✏️ Лучше так: <i>{better}</i>")
        topic = (verdict.get("review_topic") or "").strip()
        if topic:
            parts.append(
                _format_review_line(topic, verdict.get("review_level") or level)
            )
        parts.append("Идём дальше ✅")
        await m.answer("\n".join(parts), parse_mode="HTML")
        update_session(uid, task2_i=i + 1, task2_tries=0)
        await _send_task2_q(m, uid)
        return

    # Факт неверный
    hint = q.get("hint_ru") or "Найди нужный факт в тексте."
    if tries <= 0:
        await m.answer(
            f"{feedback or '🦜 Рико: По факту из текста не так.'}\n\n"
            f"💡 Подсказка: {hint}\n"
            "Перепиши ответ — своими словами, но с верным фактом."
        )
        update_session(uid, task2_tries=1)
        return

    review = ""
    topic = (verdict.get("review_topic") or "").strip()
    if topic:
        review = "\n" + _format_review_line(topic, verdict.get("review_level") or level)
    await m.answer(
        f"{feedback or '🦜 Рико: Факт всё ещё не сходится с текстом.'}\n\n"
        f"✅ По смыслу текста подходит, например: <b>{better}</b>"
        f"{review}\n\n"
        "Идём к следующему вопросу.",
        parse_mode="HTML",
    )
    update_session(uid, task2_i=i + 1, task2_tries=0)
    await _send_task2_q(m, uid)


async def _start_task3(m: Message, uid: str) -> None:
    update_session(uid, phase="task3")
    set_reading_hub(uid, "reading_task3")
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    pack = sess.get("content") or {}
    plan = pack.get("plan") or []
    full = pack.get("full_text") or ""
    lines = "\n".join(f"{n}. {p}" for n, p in enumerate(plan, start=1))
    await m.answer(
        "📝 <b>Задание 3 · Пересказ</b>\n\n"
        "🦜 Рико: Напиши пересказ своими словами. "
        "План ниже — только подсказка, не шаблон: можно другой порядок и не все пункты.\n"
        "Главное — не противоречить тексту и не выдумывать то, чего в нём нет.\n"
        "Проверю факты и грамматику, сразу дам правки и засчитаю задание.\n\n"
        f"<b>Текст:</b>\n{full}\n\n"
        f"<b>План (подсказка):</b>\n{lines}",
        reply_markup=_exit_kb(),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("reading_task3"), F.text)
async def reading_task3_answer(m: Message):
    text = (m.text or "").strip()
    if text in {BTN_EXIT, BTN_READY}:
        return
    if len(text.split()) < 8:
        await m.answer(
            "🦜 Рико: Напиши чуть подробнее — несколько предложений своими словами."
        )
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    pack = sess.get("content") or {}
    level = sess.get("level") or "A1"

    from services.tg_out import status

    async with status(m, "🦜 Рико проверяет пересказ…"):
        verdict = judge_retelling(
            pack.get("plan") or [],
            pack.get("facts") or [],
            pack.get("full_text") or "",
            text,
            level=level,
        )

    parts = [
        "✅ <b>Задание 3 пройдено!</b>",
        str(verdict.get("feedback_ru") or "").strip(),
    ]
    tips = str(verdict.get("tips_ru") or "").strip()
    if tips:
        parts.append(f"💡 {tips}")
    better = str(verdict.get("better_en") or "").strip()
    if better and normalize_gap_token(better) != normalize_gap_token(text):
        parts.append(f"✏️ Более естественно:\n<i>{better}</i>")
    reviews = verdict.get("review_topics") or []
    if reviews:
        lines = []
        for r in reviews:
            if isinstance(r, dict):
                lines.append(
                    _format_review_line(
                        str(r.get("topic") or "Grammar"),
                        str(r.get("level") or level),
                    )
                )
        if lines:
            parts.append("Что полезно повторить:\n" + "\n".join(lines))
    await m.answer("\n\n".join(p for p in parts if p), parse_mode="HTML")
    await _finish_topic(m, uid, sess)


async def _finish_topic(m: Message, uid: str, sess: dict) -> None:
    level = sess.get("level") or "A1"
    topic_id = sess.get("topic_id") or ""
    title = sess.get("topic_title") or "тема"
    mark_topic_done(uid, level, topic_id)
    set_reading_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    await m.answer(
        f"🏆 Тема «{title}» пройдена ✅ — все 3 задания сделаны!\n"
        "Можешь выбрать следующую.",
        reply_markup=reading_topics_kb(level, user),
        parse_mode="HTML",
    )
