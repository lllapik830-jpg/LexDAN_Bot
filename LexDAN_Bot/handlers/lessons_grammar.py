"""
Раздел Grammar внутри уровня.
"""

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup
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
)
from handlers.keyboards import lessons_home_levels, lessons_home_first
from data.assessment_data import LEVELS
from data.grammar_curriculum import (
    format_topics_list,
    get_topic_by_index,
    get_topic,
    is_ack_topic,
    get_grammar_section_intro,
)
from data.level_intros import get_level_welcome
from services.database import MODE_LESSONS, load_users, get_user
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
    is_topic_completed,
    EXERCISE_TYPES,
)
from services.rico_tutor import (
    rico_topic_chat_text,
    generate_grammar_exercise,
    check_write_answer,
    rico_help_for_exercise,
    rico_explain_wrong_final,
    translate_exercise_prompt,
)

router = Router()

BTN_GRAMMAR = "📘 Grammar"
BTN_ACK = "✅ Ознакомился"
BTN_TRANSLATE = "🌍 Перевести"
SECTION_STUBS = {
    "📗 Vocabulary",
    "🎧 Listening",
    "📖 Reading",
    "🗣 Speaking",
    "✍️ Writing",
}

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
    prefix = f"{level}:"
    out = set()
    for key in user["grammar_progress"].get("completed_topics") or []:
        if str(key).startswith(prefix):
            out.add(str(key)[len(prefix) :])
    return out


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
        return grammar_topics_kb(level)
    if hub == "topic":
        return _topic_kb_for(level, lesson.get("topic_id") or "")
    if hub == "exercises":
        return exercises_menu_kb()
    if hub == "exercise":
        ex = lesson.get("exercise") or {}
        if ex.get("kind") == "mcq" and ex.get("options"):
            return exercise_mcq_kb(ex["options"])
        return exercise_write_kb()
    if user.get("assessment_done"):
        return lessons_home_levels()
    return lessons_home_first()


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
        reply_markup=grammar_topics_kb(level),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text.in_(SECTION_STUBS))
async def section_stub(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    if (user.get("lesson") or {}).get("hub") != "level_hub":
        return
    await m.reply(
        f"{m.text}\n\n🦜 Раздел ещё в мастерской у Рико. Скоро откроем!\n"
        "Пока залетай в <b>Grammar</b> — там уже полно мяса ✨",
        reply_markup=level_sections_kb(),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К уровням")
async def back_to_levels(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    clear_lesson(str(m.from_user.id))
    kb = lessons_home_levels() if user.get("assessment_done") else lessons_home_first()
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
    level = user["lesson"].get("level") or "A1"
    idx = int(m.text)
    topic = get_topic_by_index(level, idx)
    if not topic:
        await m.reply(
            "Нет такой темы. Выбери номер из списка.",
            reply_markup=grammar_topics_kb(level),
        )
        return

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
    set_grammar_list(str(m.from_user.id), level)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.reply(
        f"✅ Тема «{topic['title']}» засчитана!\n\n"
        + format_topics_list(level, _completed_topic_ids(user, level)),
        reply_markup=grammar_topics_kb(level),
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
        "\n🦜 Неверный ответ → кнопка пропадает.\n"
        "При двух оставшихся вариантах ошибка = ответ + объяснение (зачёт).\n"
        "Помощь: 1-я = подсказка, 2-я = ответ (и зачёт).\n"
        "Можно проходить задания снова."
    )
    await m.reply("\n".join(lines), reply_markup=exercises_menu_kb(), parse_mode="HTML")


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К темам")
async def back_to_topics(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    level = (user.get("lesson") or {}).get("level") or "A1"
    set_grammar_list(str(m.from_user.id), level)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.reply(
        format_topics_list(level, _completed_topic_ids(user, level)),
        reply_markup=grammar_topics_kb(level),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К теме")
async def back_to_topic(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    topic_id = user["lesson"].get("topic_id")
    title = user["lesson"].get("topic_title") or "тема"
    if not topic_id:
        await back_to_topics(m)
        return
    open_topic(str(m.from_user.id), topic_id, title)
    level = user["lesson"].get("level") or "A1"
    topic = get_topic(level, topic_id)
    intro = topic["rico_intro"] if topic else f"🦜 Тема: {title}"
    await m.reply(
        intro,
        reply_markup=_topic_kb_for(level, topic_id),
        parse_mode="HTML",
    )


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
    await m.reply(
        "Задание пропущено (не засчитано). Выбери другое:",
        reply_markup=exercises_menu_kb(),
    )


async def _finish_exercise_ok(m: Message, user_id: str, level: str, topic_id: str, num: int, text: str):
    mark_exercise_done(user_id, level, topic_id, num)
    clear_active_exercise(user_id)
    users = load_users()
    user = get_user(users, user_id)
    done = get_done_exercises(user, level, topic_id)
    lines = [text, "", "📝 Прогресс:"]
    for n, title in EXERCISE_TYPES:
        mark = "✅" if n in done else "▫️"
        lines.append(f"{mark} Задание {n} — {title}")
    await m.reply("\n".join(lines), reply_markup=exercises_menu_kb(), parse_mode="HTML")


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("exercises"), F.text.regexp(r"^Задание\s+[1-8]$"))
async def start_assignment(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    num = int(m.text.split()[-1])
    level = user["lesson"].get("level") or "A1"
    title = user["lesson"].get("topic_title") or "Grammar"
    topic_id = user["lesson"].get("topic_id")
    topic = get_topic(level, topic_id) if topic_id else None
    if is_ack_topic(topic):
        await m.reply("У этой темы нет заданий.", reply_markup=topic_chat_kb(ack=True))
        return

    await m.reply("🦜 Рико готовит задание…")
    ex = generate_grammar_exercise(level, title, num)
    start_exercise(str(m.from_user.id), num, ex)

    if ex["kind"] == "mcq":
        text = (
            f"<b>Задание {num}/8</b>\n\n{ex['prompt']}\n\n"
            "Выбери ответ кнопкой. Не понимаешь фразу — жми <b>🌍 Перевести</b>."
        )
        await m.reply(text, reply_markup=exercise_mcq_kb(ex["options"]), parse_mode="HTML")
    else:
        text = (
            f"<b>Задание {num}/8</b>\n\n{ex['prompt']}\n\n"
            "Напиши ответ текстом. Не понятно — <b>🌍 Перевести</b> или помощь Рико."
        )
        await m.reply(text, reply_markup=exercise_write_kb(), parse_mode="HTML")


def _exercise_kb(ex: dict) -> ReplyKeyboardMarkup:
    if ex.get("kind") == "mcq" and ex.get("options"):
        return exercise_mcq_kb(ex["options"])
    return exercise_write_kb()


async def _show_exercise_translation(m: Message, user: dict):
    ex = dict((user.get("lesson") or {}).get("exercise") or {})
    ru = ex.get("prompt_ru") or translate_exercise_prompt(ex.get("prompt") or "")
    if not ru:
        await m.reply(
            "🦜 Не получилось перевести. Попробуй ещё раз или спроси помощь.",
            reply_markup=_exercise_kb(ex),
        )
        return
    await m.reply(
        f"🌍 <b>Перевод задания:</b>\n\n{ru}",
        reply_markup=_exercise_kb(ex),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("exercise"), F.text == BTN_TRANSLATE)
async def exercise_translate(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await _show_exercise_translation(m, user)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("exercise"), F.text == "🦜 Помощь Рико")
async def exercise_help(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
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
            str(m.from_user.id),
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
    update_active_exercise(str(m.from_user.id), ex)
    await m.reply(tip, reply_markup=_exercise_kb(ex), parse_mode="HTML")


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
        return

    # write
    result = check_write_answer(
        level,
        title,
        ex.get("prompt") or "",
        ex.get("answer") or "",
        m.text,
    )
    if _as_bool(result.get("correct")):
        fb = result.get("feedback_ru") or "Отлично!"
        await _finish_exercise_ok(m, uid, level, topic_id, num, f"✅ {fb}")
    else:
        fb = result.get("feedback_ru") or "Попробуй ещё раз."
        await m.reply(f"❌ {fb}", reply_markup=exercise_write_kb())


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
