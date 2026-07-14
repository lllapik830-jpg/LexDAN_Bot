"""
Раздел Grammar внутри уровня.
"""

from aiogram import Router, F
from aiogram.types import Message

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
)
from services.database import MODE_LESSONS, load_users, get_user
from services.lesson_state import (
    ensure_lesson,
    assessment_busy,
    set_level_hub,
    set_grammar_list,
    open_topic,
    open_exercises_menu,
    start_exercise,
    mark_exercise_done,
    clear_active_exercise,
    clear_lesson,
    EXERCISE_TYPES,
)
from services.rico_tutor import (
    rico_topic_chat_text,
    generate_grammar_exercise,
    check_write_answer,
    rico_help_for_exercise,
)

router = Router()

BTN_GRAMMAR = "📘 Grammar"
SECTION_STUBS = {
    "📗 Vocabulary",
    "🎧 Listening",
    "📖 Reading",
    "🗣 Speaking",
    "✍️ Writing",
}


def _as_bool(v) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.lower() in {"1", "true", "yes", "да"}
    return bool(v)


async def open_level_hub(m: Message, level: str):
    set_level_hub(str(m.from_user.id), level)
    await m.reply(
        f"🎓 <b>Уровень {level}</b>\n\n"
        "Выбери раздел. Сейчас полностью готов <b>Grammar</b> — остальные скоро!\n"
        "🦜 Рико уже настроен помогать в грамматике.",
        reply_markup=level_sections_kb(),
        parse_mode="HTML",
    )


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

    await m.reply(
        format_topics_list(level),
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
        await m.reply("Нет такой темы. Выбери номер из списка.", reply_markup=grammar_topics_kb(level))
        return

    open_topic(str(m.from_user.id), topic["id"], topic["title"])
    await m.reply(
        topic["rico_intro"]
        + "\n\n💬 Пиши вопросы по теме прямо сюда — или жми <b>📝 Задания</b>.",
        reply_markup=topic_chat_kb(),
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

    open_exercises_menu(str(m.from_user.id))
    topic_id = user["lesson"]["topic_id"]
    done = (user["lesson"].get("completed_exercises") or {}).get(topic_id) or []
    lines = ["📝 <b>Задания по теме</b>\n", "Сложность растёт от 1 к 8:\n"]
    for num, title in EXERCISE_TYPES:
        mark = "✅" if num in done else "▫️"
        lines.append(f"{mark} <b>Задание {num}</b> — {title}")
    lines.append(
        "\n🦜 В заданиях помощь доступна всегда.\n"
        "После практики откроется тест (позже) — там только 2 подсказки."
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
    await m.reply(
        format_topics_list(level),
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
    await m.reply(intro, reply_markup=topic_chat_kb(), parse_mode="HTML")


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


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("exercises"), F.text.regexp(r"^Задание\s+[1-8]$"))
async def start_assignment(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    num = int(m.text.split()[-1])
    level = user["lesson"].get("level") or "A1"
    title = user["lesson"].get("topic_title") or "Grammar"

    await m.reply("🦜 Рико готовит задание…")
    ex = generate_grammar_exercise(level, title, num)
    start_exercise(str(m.from_user.id), num, ex)

    if ex["kind"] == "mcq":
        text = f"<b>Задание {num}/8</b>\n\n{ex['prompt']}\n\nВыбери ответ кнопкой:"
        await m.reply(text, reply_markup=exercise_mcq_kb(ex["options"]), parse_mode="HTML")
    else:
        text = (
            f"<b>Задание {num}/8</b>\n\n{ex['prompt']}\n\n"
            "Напиши ответ текстом. Можно попросить помощь Рико."
        )
        await m.reply(text, reply_markup=exercise_write_kb(), parse_mode="HTML")


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("exercise"), F.text == "🦜 Помощь Рико")
async def exercise_help(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ex = user["lesson"].get("exercise") or {}
    level = user["lesson"].get("level") or "A1"
    title = user["lesson"].get("topic_title") or "Grammar"
    tip = rico_help_for_exercise(level, title, ex.get("prompt", ""), ex.get("options"))
    kb = (
        exercise_mcq_kb(ex["options"])
        if ex.get("kind") == "mcq" and ex.get("options")
        else exercise_write_kb()
    )
    await m.reply(tip, reply_markup=kb)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("exercise"))
async def exercise_answer(m: Message):
    if not m.text or m.text.startswith("/"):
        return
    # buttons handled elsewhere
    if m.text in {
        "🦜 Помощь Рико",
        "⬅️ К выбору заданий",
        "🔙 Вернуться в меню",
        "📝 Задания",
        "⬅️ К теме",
        "⬅️ К темам",
    }:
        return

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    lesson = user["lesson"]
    ex = lesson.get("exercise") or {}
    num = lesson.get("exercise_num")
    topic_id = lesson.get("topic_id")
    level = lesson.get("level") or "A1"
    title = lesson.get("topic_title") or "Grammar"

    if ex.get("kind") == "mcq":
        options = ex.get("options") or []
        if m.text not in options:
            await m.reply("Выбери один из вариантов кнопок ниже.", reply_markup=exercise_mcq_kb(options))
            return
        correct = m.text.strip() == (ex.get("answer") or "").strip()
        if correct:
            mark_exercise_done(str(m.from_user.id), topic_id, num)
            clear_active_exercise(str(m.from_user.id))
            await m.reply("✅ Верно! Красава 🦜", reply_markup=exercises_menu_kb())
        else:
            await m.reply(
                f"❌ Не совсем.\n💡 {ex.get('tip') or 'Вспомни правило темы.'}",
                reply_markup=exercise_mcq_kb(options),
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
        mark_exercise_done(str(m.from_user.id), topic_id, num)
        clear_active_exercise(str(m.from_user.id))
        fb = result.get("feedback_ru") or "Отлично!"
        await m.reply(f"✅ {fb}", reply_markup=exercises_menu_kb())
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
    name = user.get("name") or m.from_user.first_name or "друг"
    await m.reply("🦜 …")
    answer = rico_topic_chat_text(level, title, text, name)
    await m.reply(answer, reply_markup=topic_chat_kb())
