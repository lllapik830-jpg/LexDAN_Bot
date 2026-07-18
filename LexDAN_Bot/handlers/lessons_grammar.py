"""
Раздел Grammar внутри уровня.
"""

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, CallbackQuery
from aiogram.dispatcher.event.bases import SkipHandler

from handlers.filters import ModeFilter
from handlers.lesson_filters import LessonHubFilter
from handlers.lesson_keyboards import (
    level_sections_kb,
    grammar_topics_kb,
    topic_chat_kb,
    exercises_menu_kb,
    exercise_mcq_kb,
    exercise_write_kb,
    exercise_help_inline_kb,
    grammar_test_kb,
    BTN_GRAMMAR_TEST,
    lesson_limit_inline_kb,
)
from handlers.keyboards import lessons_home_levels, lessons_home_first
from data.assessment_data import LEVELS
from data.grammar_curriculum import (
    format_topics_list,
    get_topic_by_index,
    get_topic,
    get_topics,
    is_ack_topic,
    get_grammar_section_intro,
)
from data.level_intros import get_level_welcome
from services.database import MODE_LESSONS, load_users, get_user, save_users
from services.lesson_state import (
    ensure_lesson,
    ensure_progress,
    assessment_busy,
    set_level_hub,
    set_grammar_list,
    open_topic,
    open_exercises_menu,
    start_exercise,
    update_active_exercise,
    mark_exercise_done,
    mark_topic_done,
    clear_active_exercise,
    clear_lesson,
    get_done_exercises,
    is_topic_exercises_done,
    is_grammar_topic_done,
    all_grammar_topics_done,
    is_grammar_test_passed,
    mark_grammar_test_passed,
    start_grammar_test,
    update_grammar_test,
    clear_grammar_test,
    EXERCISE_TYPES,
)
from services.rico_tutor import (
    rico_topic_chat_text,
    generate_grammar_exercise,
    generate_grammar_test,
    check_write_answer,
    rico_help_for_exercise,
    rico_explain_wrong_final,
    get_exercise_sentence_translation,
    is_word_lookup_question,
    rico_word_lookup,
)
from services.growth import (
    can_do_grammar_exercise,
    note_grammar_exercise_done,
    note_lesson_completed,
    ensure_growth,
)

router = Router()

BTN_GRAMMAR = "📘 Grammar"
BTN_ACK = "✅ Ознакомился"
BTN_TRANSLATE = "🌍 Перевести"


VOICE_ONLY_TEXT = (
    "🦜 Здесь пока только <b>текстом</b>!\n"
    "Разговорная практика — в разделе <b>Speaking</b>.\n"
    "Напиши сообщение или нажми кнопку ✍️"
)


def _as_bool(v) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.lower() in {"1", "true", "yes", "да"}
    return bool(v)


def _completed_topic_ids(user: dict, level: str) -> set[str]:
    ensure_progress(user)
    return {t["id"] for t in get_topics(level) if is_grammar_topic_done(user, level, t)}


def _topic_kb_for(level: str, topic_id: str) -> ReplyKeyboardMarkup:
    topic = get_topic(level, topic_id)
    return topic_chat_kb(ack=is_ack_topic(topic))


def _kb_for_user(user: dict) -> ReplyKeyboardMarkup:
    ensure_lesson(user)
    lesson = user.get("lesson") or {}
    hub = lesson.get("hub")
    level = lesson.get("level") or user.get("level") or "A1"

    if hub == "level_hub":
        return level_sections_kb()
    if hub == "grammar_list":
        return grammar_topics_kb(level, user)
    if hub == "topic":
        return _topic_kb_for(level, lesson.get("topic_id") or "")
    if hub == "exercises":
        done = get_done_exercises(user, level, lesson.get("topic_id") or "")
        return exercises_menu_kb(done)
    if hub == "exercise":
        ex = lesson.get("exercise") or {}
        if ex.get("kind") == "mcq" and ex.get("options"):
            return exercise_mcq_kb(ex["options"])
        return exercise_write_kb()
    if hub == "grammar_test":
        test = lesson.get("grammar_test") or {}
        q = _current_test_question(test)
        opts = q.get("options") if q and q.get("kind") == "mcq" else None
        return grammar_test_kb(mcq_options=opts)
    if user.get("assessment_done") or user.get("dev_unlock"):
        return lessons_home_levels(user.get("level"), user=user)
    return lessons_home_first()


def _current_test_question(test: dict) -> dict | None:
    qs = test.get("questions") or []
    idx = int(test.get("index") or 0)
    if 0 <= idx < len(qs):
        return qs[idx]
    return None


async def _show_grammar_test_question(m: Message, user: dict):
    test = (user.get("lesson") or {}).get("grammar_test") or {}
    q = _current_test_question(test)
    if not q:
        return
    idx = int(test.get("index") or 0) + 1
    total = len(test.get("questions") or [])
    body = q.get("prompt") or ""
    header = f"🎯 <b>Тест Grammar · вопрос {idx}/{total}</b>\n\n{body}"
    if q.get("kind") == "mcq":
        await m.reply(header + "\n\nВыбери ответ кнопкой.", reply_markup=grammar_test_kb(mcq_options=q["options"]), parse_mode="HTML")
    else:
        await m.reply(header + "\n\nНапиши ответ текстом.", reply_markup=grammar_test_kb(), parse_mode="HTML")


async def open_level_hub(m: Message, level: str):
    set_level_hub(str(m.from_user.id), level)
    await m.reply(
        get_level_welcome(level),
        reply_markup=level_sections_kb(),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.voice)
async def voice_in_lessons_grammar(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        raise SkipHandler
    ensure_lesson(user)
    if not (user.get("lesson") or {}).get("hub"):
        raise SkipHandler
    await m.reply(VOICE_ONLY_TEXT, reply_markup=_kb_for_user(user), parse_mode="HTML")


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_GRAMMAR)
async def open_grammar(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    level = (user.get("lesson") or {}).get("level") or user.get("level") or "A1"
    if level not in LEVELS:
        level = "A1"
    set_grammar_list(str(m.from_user.id), level)

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.reply(get_grammar_section_intro(level), parse_mode="HTML")
    await m.reply(
        format_topics_list(level, _completed_topic_ids(user, level)),
        reply_markup=grammar_topics_kb(level, user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("grammar_list"), F.text == BTN_GRAMMAR_TEST)
async def start_grammar_section_test(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    level = user["lesson"].get("level") or "A1"
    if not all_grammar_topics_done(user, level):
        await m.reply(
            "🦜 Сначала пройди все темы Grammar с ✅",
            reply_markup=grammar_topics_kb(level, user),
        )
        return
    if is_grammar_test_passed(user, level):
        await m.reply(
            "🦜 Ты уже сдал этот тест! Молодец 🏆",
            reply_markup=grammar_topics_kb(level, user),
        )
        return

    await m.reply("🦜 Готовлю итоговый тест по Grammar…")
    topics = get_topics(level)
    titles = [t["title"] for t in topics]
    ids = [t["id"] for t in topics]
    questions = generate_grammar_test(level, titles, topic_ids=ids)
    start_grammar_test(str(m.from_user.id), {"questions": questions, "index": 0, "score": 0})
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.reply(
        "🎯 <b>Итоговый тест по Grammar</b>\n\n"
        "8 вопросов по всем темам уровня. Нужно ≥6 правильных.\n"
        "Поехали!",
        parse_mode="HTML",
    )
    await _show_grammar_test_question(m, user)


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К уровням")
async def back_to_levels(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    clear_lesson(str(m.from_user.id))
    kb = (
        lessons_home_levels(user.get("level"), user=user)
        if (user.get("assessment_done") or user.get("dev_unlock"))
        else lessons_home_first()
    )
    await m.reply("Выбери уровень:", reply_markup=kb)


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К разделам")
async def back_to_sections(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    level = user["lesson"].get("level") or user.get("level") or "A1"
    set_level_hub(str(m.from_user.id), level)
    await m.reply(
        f"🎓 Уровень {level} — выбери раздел:",
        reply_markup=level_sections_kb(),
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("grammar_list"), F.text.regexp(r"^\d+$"))
async def choose_topic_number(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    level = user["lesson"].get("level") or "A1"
    idx = int(m.text)
    topic = get_topic_by_index(level, idx)
    if not topic:
        await m.reply(
            "Нет такой темы. Выбери номер из списка.",
            reply_markup=grammar_topics_kb(level, user),
        )
        return

    # Лимит — на старте задания, не на просмотре темы
    open_topic(str(m.from_user.id), topic["id"], topic["title"])
    ack = is_ack_topic(topic)
    await m.reply(
        topic["rico_intro"],
        reply_markup=topic_chat_kb(ack=ack),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_ACK)
async def acknowledge_topic(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    if user["lesson"].get("hub") != "topic":
        return
    level = user["lesson"].get("level") or "A1"
    topic_id = user["lesson"].get("topic_id")
    topic = get_topic(level, topic_id) if topic_id else None
    if not is_ack_topic(topic):
        await m.reply(
            "🦜 Для этой темы жми «Задания».",
            reply_markup=_topic_kb_for(level, topic_id or ""),
        )
        return

    mark_topic_done(str(m.from_user.id), level, topic_id)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    note_lesson_completed(user)
    save_users(users)
    set_grammar_list(str(m.from_user.id), level)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    extra = ""
    if all_grammar_topics_done(user, level) and not is_grammar_test_passed(user, level):
        extra = "\n\n🔓 Все темы пройдены — открой <b>🎯 Тест по Grammar</b>!"
    await m.reply(
        f"✅ Тема «{topic['title']}» засчитана!{extra}\n\n"
        + format_topics_list(level, _completed_topic_ids(user, level)),
        reply_markup=grammar_topics_kb(level, user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == "📝 Задания")
async def open_assignments(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    if user["lesson"].get("hub") not in {"topic", "exercises", "exercise"}:
        return
    if not user["lesson"].get("topic_id"):
        return

    level = user["lesson"].get("level") or "A1"
    topic_id = user["lesson"]["topic_id"]
    topic = get_topic(level, topic_id)
    if is_ack_topic(topic):
        await m.reply(
            "🦜 У этой темы заданий нет — просто жми «Ознакомился».",
            reply_markup=topic_chat_kb(ack=True),
        )
        return

    open_exercises_menu(str(m.from_user.id))
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    done = get_done_exercises(user, level, topic_id)
    lines = ["📝 <b>Задания по теме</b>\n", "Сложность растёт от 1 к 8:\n"]
    for num, title in EXERCISE_TYPES:
        mark = "✅" if num in done else "▫️"
        lines.append(f"{mark} <b>Задание {num}</b> — {title}")
    lines.append(
        "\n🦜 <b>8 заданий на тему:</b>\n"
        "1–3 — выбор кнопкой · 4–6 — напиши форму слова · "
        "7 — RU→EN · 8 — EN→RU\n"
        "В переводах можно спросить «как переводится слово …».\n"
        "Все 8 заданий → тема с ✅. Все темы → откроется тест по Grammar."
    )
    await m.reply("\n".join(lines), reply_markup=exercises_menu_kb(done), parse_mode="HTML")


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К темам")
async def back_to_topics(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    hub = (user.get("lesson") or {}).get("hub") or ""
    # Vocabulary ловит эту же кнопку своим хендлером раньше; если сюда дошли — не для vocab.
    if hub.startswith("vocab") or hub in {"global_drill_menu", "vocab_drill"}:
        raise SkipHandler
    level = (user.get("lesson") or {}).get("level") or "A1"
    if hub == "grammar_test":
        clear_grammar_test(str(m.from_user.id))
    else:
        set_grammar_list(str(m.from_user.id), level)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.reply(
        format_topics_list(level, _completed_topic_ids(user, level)),
        reply_markup=grammar_topics_kb(level, user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К теме")
async def back_to_topic(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    hub = user["lesson"].get("hub")
    if hub not in {"topic", "exercises", "exercise"}:
        return
    topic_id = user["lesson"].get("topic_id")
    title = user["lesson"].get("topic_title") or "тема"
    if not topic_id:
        await back_to_topics(m)
        return
    if hub == "exercise":
        clear_active_exercise(str(m.from_user.id))
    elif hub == "exercises":
        pass
    open_topic(str(m.from_user.id), topic_id, title)
    level = user["lesson"].get("level") or "A1"
    topic = get_topic(level, topic_id)
    intro = topic["rico_intro"] if topic else f"🦜 Тема: {title}"
    await m.reply(intro, reply_markup=_topic_kb_for(level, topic_id), parse_mode="HTML")


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К выбору заданий")
async def abandon_exercise(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    if user["lesson"].get("hub") != "exercise":
        return
    clear_active_exercise(str(m.from_user.id))
    level = user["lesson"].get("level") or "A1"
    topic_id = user["lesson"].get("topic_id") or ""
    done = get_done_exercises(user, level, topic_id)
    await m.reply(
        "Задание пропущено (не засчитано). Выбери другое:",
        reply_markup=exercises_menu_kb(done),
    )


async def _finish_exercise_ok(m: Message, user_id: str, level: str, topic_id: str, num: int, text: str):
    mark_exercise_done(user_id, level, topic_id, num)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    note_grammar_exercise_done(user)

    # Рефералка: друг закрыл 24 задания → награда пригласившему
    from services.rewards import maybe_qualify_referral

    to_inviter, to_friend = maybe_qualify_referral(user, users)
    save_users(users)
    if to_friend:
        await m.reply(to_friend, parse_mode="HTML")
    if to_inviter:
        ref = user.get("referred_by")
        if ref and str(ref) != user_id:
            try:
                await m.bot.send_message(int(ref), to_inviter, parse_mode="HTML")
            except Exception:
                pass

    topic_title = (user.get("lesson") or {}).get("topic_title") or "тема"
    extra = ""
    topic_just_done = False
    if is_topic_exercises_done(user, level, topic_id):
        mark_topic_done(user_id, level, topic_id)
        users = load_users()
        user = get_user(users, user_id)
        ensure_growth(user)
        note_lesson_completed(user)
        save_users(users)
        topic_just_done = True
        extra = f"\n\n🎉 <b>Тема «{topic_title}» полностью пройдена!</b> ✅"
        users = load_users()
        user = get_user(users, user_id)
        if all_grammar_topics_done(user, level) and not is_grammar_test_passed(user, level):
            extra += "\n\n🔓 Все темы пройдены — открой <b>🎯 Тест по Grammar</b> в списке тем!"

    done = get_done_exercises(user, level, topic_id)
    next_num = None
    for n, _title in EXERCISE_TYPES:
        if n not in done:
            next_num = n
            break

    if topic_just_done or next_num is None:
        clear_active_exercise(user_id)
        lines = [text + extra, "", "📝 Прогресс:"]
        for n, title in EXERCISE_TYPES:
            mark = "✅" if n in done else "▫️"
            lines.append(f"{mark} Задание {n} — {title}")
        await m.reply("\n".join(lines), reply_markup=exercises_menu_kb(done), parse_mode="HTML")
        return

    # Автопереход к следующему заданию без возврата в список
    await m.reply(text + extra, parse_mode="HTML")
    await _launch_exercise(m, user_id, level, topic_id, topic_title, next_num)


async def _launch_exercise(
    m: Message,
    user_id: str,
    level: str,
    topic_id: str,
    topic_title: str,
    num: int,
):
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    ok, tip = can_do_grammar_exercise(user)
    if not ok:
        done = get_done_exercises(user, level, topic_id)
        await m.reply(tip or "", reply_markup=lesson_limit_inline_kb(), parse_mode="HTML")
        await m.reply(
            "📝 Прогресс по теме сохранён — завтра продолжим с галочками:",
            reply_markup=exercises_menu_kb(done),
        )
        open_exercises_menu(user_id)
        return

    await m.reply("🦜 Рико готовит задание…")
    ex = generate_grammar_exercise(level, topic_title, num, topic_id=topic_id)
    start_exercise(user_id, num, ex)
    await _send_exercise_card(m, num, ex)


async def _send_exercise_card(m: Message, num: int, ex: dict):
    inline = exercise_help_inline_kb()
    if ex["kind"] == "mcq":
        body = ex.get("prompt") or ""
        text = (
            f"<b>Задание {num}/8</b>\n\n{body}\n\n"
            "Выбери ответ кнопкой. Не понимаешь фразу — жми <b>🌍 Перевести</b> под сообщением."
        )
        await m.reply(text, reply_markup=exercise_mcq_kb(ex["options"]), parse_mode="HTML")
        await m.reply("👇 Подсказки к заданию:", reply_markup=inline)
    else:
        body = ex.get("prompt") or ""
        text = f"<b>Задание {num}/8</b>\n\n{body}"
        if ex.get("subtype") in {"translate_en", "translate_ru"}:
            text += "\n\nНе понятно слово — спроси: «как переводится …»"
        else:
            text += "\n\nНе понятно — жми кнопки под этим сообщением."
        await m.reply(text, reply_markup=exercise_write_kb(), parse_mode="HTML")
        await m.reply("👇 Подсказки к заданию:", reply_markup=inline)


@router.message(
    ModeFilter(MODE_LESSONS),
    LessonHubFilter("exercises"),
    F.text.regexp(r"^Задание\s+[1-8](?:\s*✅)?$"),
)
async def start_assignment(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    import re as _re

    m_num = _re.search(r"[1-8]", m.text or "")
    num = int(m_num.group(0)) if m_num else 1
    level = user["lesson"].get("level") or "A1"
    title = user["lesson"].get("topic_title") or "Grammar"
    topic_id = user["lesson"].get("topic_id")
    topic = get_topic(level, topic_id) if topic_id else None
    if is_ack_topic(topic):
        await m.reply("У этой темы нет заданий.", reply_markup=topic_chat_kb(ack=True))
        return

    await _launch_exercise(m, str(m.from_user.id), level, topic_id, title, num)


def _exercise_kb(ex: dict) -> ReplyKeyboardMarkup:
    if ex.get("kind") == "mcq" and ex.get("options"):
        return exercise_mcq_kb(ex["options"])
    return exercise_write_kb()


async def _show_exercise_translation(m: Message, user: dict):
    ex = dict((user.get("lesson") or {}).get("exercise") or {})
    ru = get_exercise_sentence_translation(ex)
    if not ru:
        await m.reply(
            "🦜 Не получилось перевести. Попробуй ещё раз или спроси помощь.",
            reply_markup=_exercise_kb(ex),
        )
        return
    await m.reply(
        f"🌍 <b>Перевод:</b>\n<i>{ru}</i>",
        reply_markup=_exercise_kb(ex),
        parse_mode="HTML",
    )
    await m.reply("👇 Подсказки:", reply_markup=exercise_help_inline_kb())


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("exercise"), F.text == BTN_TRANSLATE)
async def exercise_translate(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await _show_exercise_translation(m, user)


async def _do_exercise_help(m: Message, user: dict, uid: str):
    lesson = user["lesson"]
    ex = dict(lesson.get("exercise") or {})
    level = lesson.get("level") or "A1"
    title = lesson.get("topic_title") or "Grammar"
    topic_id = lesson.get("topic_id")
    num = lesson.get("exercise_num")
    help_count = int(ex.get("help_count") or 0)

    if help_count >= 1:
        tip = rico_help_for_exercise(
            level,
            title,
            ex.get("prompt", ""),
            ex.get("options"),
            reveal=True,
            answer=ex.get("answer") or "",
        )
        await _finish_exercise_ok(
            m,
            uid,
            level,
            topic_id,
            num,
            tip + "\n\n✅ Задание засчитано (по подсказке с ответом).",
        )
        return

    tip = rico_help_for_exercise(
        level,
        title,
        ex.get("prompt", ""),
        ex.get("options"),
        reveal=False,
    )
    ex["help_count"] = help_count + 1
    update_active_exercise(uid, ex)
    await m.reply(tip, reply_markup=_exercise_kb(ex), parse_mode="HTML")
    await m.reply("👇 Подсказки:", reply_markup=exercise_help_inline_kb())


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("exercise"), F.text == "🦜 Помощь Рико")
async def exercise_help(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await _do_exercise_help(m, user, str(m.from_user.id))


@router.callback_query(F.data == "ex:translate")
async def cb_exercise_translate(c: CallbackQuery):
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    if (user.get("lesson") or {}).get("hub") != "exercise":
        await c.answer("Сейчас нет активного задания", show_alert=True)
        return
    await c.answer()
    await _show_exercise_translation(c.message, user)


@router.callback_query(F.data == "ex:help")
async def cb_exercise_help(c: CallbackQuery):
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    if (user.get("lesson") or {}).get("hub") != "exercise":
        await c.answer("Сейчас нет активного задания", show_alert=True)
        return
    await c.answer()
    await _do_exercise_help(c.message, user, str(c.from_user.id))


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("exercise"))
async def exercise_answer(m: Message):
    if not m.text or m.text.startswith("/"):
        return
    if m.text in {
        "🦜 Помощь Рико",
        BTN_TRANSLATE,
        "⬅️ К выбору заданий",
        "🔙 Вернуться в меню",
        "📝 Задания",
        "⬅️ К теме",
        "⬅️ К темам",
        BTN_ACK,
    }:
        return

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    lesson = user["lesson"]
    ex = dict(lesson.get("exercise") or {})
    num = lesson.get("exercise_num")
    topic_id = lesson.get("topic_id")
    level = lesson.get("level") or "A1"
    title = lesson.get("topic_title") or "Grammar"
    uid = str(m.from_user.id)

    if ex.get("kind") == "mcq":
        options = list(ex.get("options") or [])
        if m.text not in options:
            await m.reply(
                "Выбери один из вариантов кнопок ниже.",
                reply_markup=_exercise_kb(ex),
            )
            return

        answer = (ex.get("answer") or "").strip()
        correct = m.text.strip() == answer

        if correct:
            await _finish_exercise_ok(
                m, uid, level, topic_id, num, "✅ Верно! Красава 🦜"
            )
            return

        # wrong — remove chosen option
        remaining = [o for o in options if o != m.text]
        # Если до ошибки оставалось ровно 2 варианта — раскрываем ответ
        if len(options) == 2:
            explain = rico_explain_wrong_final(
                level, title, ex.get("prompt") or "", answer
            )
            await _finish_exercise_ok(
                m,
                uid,
                level,
                topic_id,
                num,
                explain + "\n\n✅ Задание засчитано (после финальной ошибки).",
            )
            return

        ex["options"] = remaining
        update_active_exercise(uid, ex)
        await m.reply(
            "🦜 Неправильно, попробуй ещё раз!",
            reply_markup=_exercise_kb(ex),
        )
        await m.reply("👇 Подсказки:", reply_markup=exercise_help_inline_kb())
        return

    # write
    subtype = ex.get("subtype") or "write"
    if subtype in {"translate_en", "translate_ru"} and is_word_lookup_question(m.text):
        tip = rico_word_lookup(level, title, m.text, ex)
        await m.reply(tip, reply_markup=exercise_write_kb(), parse_mode="HTML")
        await m.reply("👇 Подсказки:", reply_markup=exercise_help_inline_kb())
        return

    result = check_write_answer(
        level,
        title,
        ex.get("prompt") or "",
        ex.get("answer") or "",
        m.text,
        subtype=subtype,
    )
    if _as_bool(result.get("correct")):
        fb = result.get("feedback_ru") or "Отлично!"
        # Не хвалим «Nice choice!» за ошибочный ввод — только за реально верный
        await _finish_exercise_ok(m, uid, level, topic_id, num, f"✅ {fb}")
    else:
        better = (result.get("better_en") or result.get("answer") or "").strip()
        fb = result.get("feedback_ru") or ""
        if better or fb:
            msg = "Мы исправили ошибку. Продолжаем!"
            if better:
                msg += f"\nПравильнее: <b>{better}</b>"
            if fb and "nice" not in fb.lower() and "молодец" not in fb.lower():
                msg += f"\n{fb}"
            await m.reply(f"❌ {msg}", reply_markup=exercise_write_kb(), parse_mode="HTML")
        else:
            await m.reply(
                "❌ Мы исправили ошибку. Продолжаем! Попробуй ещё раз.",
                reply_markup=exercise_write_kb(),
            )
        await m.reply("👇 Подсказки:", reply_markup=exercise_help_inline_kb())


async def _advance_grammar_test(m: Message, user: dict, correct: bool):
    uid = str(m.from_user.id)
    level = user["lesson"].get("level") or "A1"
    test = dict(user["lesson"].get("grammar_test") or {})
    if correct:
        test["score"] = int(test.get("score") or 0) + 1
    test["index"] = int(test.get("index") or 0) + 1
    questions = test.get("questions") or []
    if test["index"] >= len(questions):
        score = int(test.get("score") or 0)
        passed = score >= 6
        clear_grammar_test(uid)
        users = load_users()
        user = get_user(users, uid)
        if passed:
            mark_grammar_test_passed(uid, level)
            text = (
                f"🏆 <b>Тест сдан!</b> Результат: {score}/8.\n"
                "Grammar уровня закрыт — ты красава! 🦜"
            )
        else:
            text = (
                f"🦜 Результат: {score}/8 — нужно минимум 6.\n"
                "Повтори слабые темы и попробуй снова!"
            )
        await m.reply(
            text,
            reply_markup=grammar_topics_kb(level, user),
            parse_mode="HTML",
        )
        return
    update_grammar_test(uid, test)
    users = load_users()
    user = get_user(users, uid)
    await _show_grammar_test_question(m, user)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("grammar_test"))
async def grammar_test_answer(m: Message):
    if not m.text or m.text.startswith("/"):
        return
    if m.text in {"⬅️ К темам", "🔙 Вернуться в меню"}:
        return

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    test = dict(user["lesson"].get("grammar_test") or {})
    q = _current_test_question(test)
    if not q:
        await back_to_topics(m)
        return

    level = user["lesson"].get("level") or "A1"
    title = "Grammar test"

    if q.get("kind") == "mcq":
        options = list(q.get("options") or [])
        if m.text not in options:
            await m.reply("Выбери вариант кнопкой.", reply_markup=grammar_test_kb(mcq_options=options))
            return
        correct = m.text.strip() == (q.get("answer") or "").strip()
        if correct:
            await m.reply("✅ Верно!")
        else:
            await m.reply(f"❌ Неверно. Правильно: <b>{q.get('answer')}</b>", parse_mode="HTML")
        await _advance_grammar_test(m, user, correct)
        return

    subtype = q.get("subtype") or "write"
    if subtype in {"translate_en", "translate_ru"} and is_word_lookup_question(m.text):
        tip = rico_word_lookup(level, title, m.text, q)
        await m.reply(tip, reply_markup=grammar_test_kb(), parse_mode="HTML")
        return

    result = check_write_answer(
        level,
        title,
        q.get("prompt") or "",
        q.get("answer") or "",
        m.text,
        subtype=subtype,
    )
    correct = _as_bool(result.get("correct"))
    if correct:
        await m.reply(f"✅ {result.get('feedback_ru') or 'Верно!'}")
    else:
        fb = result.get("feedback_ru") or "Неверно."
        await m.reply(f"❌ {fb}\nПравильно: <i>{q.get('answer')}</i>", parse_mode="HTML")
    await _advance_grammar_test(m, user, correct)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("topic"), F.text)
async def topic_free_chat(m: Message):
    text = (m.text or "").strip()
    if not text or text.startswith("/"):
        return
    if text in {
        "📝 Задания",
        BTN_ACK,
        "⬅️ К темам",
        "🔙 Вернуться в меню",
        "⬅️ К теме",
        "⬅️ К разделам",
        "⬅️ К уровням",
    }:
        return

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    level = user["lesson"].get("level") or "A1"
    title = user["lesson"].get("topic_title") or "Grammar"
    topic_id = user["lesson"].get("topic_id") or ""
    name = user.get("name") or m.from_user.first_name or "друг"
    await m.reply("🦜 …")
    answer = rico_topic_chat_text(level, title, text, name)
    await m.reply(
        answer,
        reply_markup=_topic_kb_for(level, topic_id),
        parse_mode="HTML",
    )
