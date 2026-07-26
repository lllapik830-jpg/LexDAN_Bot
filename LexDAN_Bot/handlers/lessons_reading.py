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
    check_comprehension_answer,
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
        "1️⃣ Заполни пропуски\n"
        "2️⃣ Найди соответствие (вопросы по тексту)\n"
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
        task1_filled=[None, None, None, None, None],  # правильные слова по пропускам
        task1_next=0,  # следующий ожидаемый пропуск при поштучном вводе
        task2_i=0,
    )
    set_reading_hub(uid, "reading_task1")
    await _send_task1(m, uid)


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
        "Напиши <b>5 слов через запятую</b> по порядку пропусков "
        "или по одному слову (сначала 1-й пропуск, потом 2-й…).\n\n"
        f"{gapped}\n\n"
        f"<b>Слова:</b> {bank}\n\n"
        f"<b>Сейчас заполнено:</b>\n" + "\n".join(status_lines),
        reply_markup=_exit_kb(),
        parse_mode="HTML",
    )


def _apply_gap_list(uid: str, words: list[str], answers: list[str], filled: list) -> tuple[list, list[str]]:
    """Применить список слов к пропускам. Returns (new_filled, error_messages)."""
    errs = []
    new_filled = list(filled)
    for i, w in enumerate(words[:5]):
        if check_one_gap(w, answers[i]):
            new_filled[i] = answers[i]
        else:
            # не затираем уже правильный ответ неверным
            if new_filled[i] != answers[i]:
                new_filled[i] = None
            errs.append(
                f"В {i + 1}-м пропуске «{w}» не подходит по смыслу. "
                f"Правильное слово другое — попробуй ещё раз для этого пропуска."
            )
    return new_filled, errs


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
        filled, errs = _apply_gap_list(uid, parsed, answers, filled)
        update_session(uid, task1_filled=filled)
        if errs:
            await m.answer("❌ " + "\n".join(errs))
            await _send_task1(m, uid)
            return
    else:
        # одно слово — в следующий незаполненный / указанный пропуск
        # если пользователь пишет только одно — кладём в первый пустой
        target = next((i for i, w in enumerate(filled) if w is None), None)
        if target is None:
            await m.answer("Все пропуски уже заполнены верно!")
            await _start_task2(m, uid)
            return
        # если next_i указывает на пустой — используем его
        if 0 <= next_i < 5 and filled[next_i] is None:
            target = next_i
        word = text.strip()
        if check_one_gap(word, answers[target]):
            filled[target] = answers[target]
            update_session(uid, task1_filled=filled, task1_next=target + 1)
            await m.answer(f"✅ Пропуск {target + 1} верно: <b>{answers[target]}</b>", parse_mode="HTML")
        else:
            await m.answer(
                f"❌ В {target + 1}-м пропуске вместо подходящего слова ты написал(а) «{word}» — "
                "это не подходит по смыслу. Попробуй ещё раз."
            )
            update_session(uid, task1_next=target)
            await _send_task1(m, uid)
            return

    if all(filled[i] == answers[i] for i in range(5)):
        await m.answer(
            "🏆 Отличный результат! Все слова подобраны верно.\n"
            "Переходим ко второму заданию…"
        )
        await _start_task2(m, uid)
        return

    # ещё есть пустые
    empty = [str(i + 1) for i, w in enumerate(filled) if w is None]
    await m.answer(
        "✅ Часть пропусков верна. Осталось заполнить: " + ", ".join(empty) + ".\n"
        "Можно написать одно слово или все оставшиеся через запятую заново целиком (5 слов)."
    )
    update_session(uid, task1_filled=filled)
    await _send_task1(m, uid)


async def _start_task2(m: Message, uid: str) -> None:
    update_session(uid, phase="task2", task2_i=0)
    set_reading_hub(uid, "reading_task2")
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    pack = sess.get("content") or {}
    full = pack.get("full_text") or ""
    await m.answer(
        "📝 <b>Задание 2 · Найди соответствие</b>\n\n"
        "🦜 Рико: Теперь проверю, как ты находишь ключевую информацию.\n"
        "Я задам <b>4 вопроса</b> — найди ответ в тексте и напиши в чат.\n\n"
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
        f"<b>Вопрос {i + 1}/4</b>\n\n{q.get('q')}",
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
    qs = (sess.get("content") or {}).get("questions") or []
    i = int(sess.get("task2_i") or 0)
    if i >= len(qs):
        return
    q = qs[i]
    if check_comprehension_answer(text, q.get("accept") or []):
        quote = q.get("quote") or ""
        msg = "✅ Верно!"
        if quote:
            msg += f"\nВ тексте: «{quote}»"
        await m.answer(msg)
        update_session(uid, task2_i=i + 1)
        await _send_task2_q(m, uid)
        return
    hint = q.get("hint_ru") or "Найди нужное предложение в тексте и напиши ответ ещё раз."
    await m.answer(f"❌ Не совсем. {hint}")


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
        "📝 <b>Задание 3 · Пересказ по плану</b>\n\n"
        "🦜 Рико: Напиши краткий пересказ текста по плану. "
        "Свои слова — ок, факты не меняй.\n\n"
        f"<b>Текст (на всякий случай):</b>\n{full}\n\n"
        f"<b>План:</b>\n{lines}",
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
            "Напиши чуть подробнее — пересказ по всем пунктам плана (несколько предложений)."
        )
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    pack = sess.get("content") or {}

    from services.tg_out import status

    async with status(m, "🦜 Рико проверяет пересказ…"):
        verdict = judge_retelling(
            pack.get("plan") or [],
            pack.get("facts") or [],
            pack.get("full_text") or "",
            text,
        )

    if verdict.get("ok"):
        await m.answer(
            "✅ Отлично! Ты правильно пересказал(а) текст и указал(а) все ключевые моменты."
        )
        await _finish_topic(m, uid, sess)
        return

    missing = verdict.get("missing") or []
    plan = pack.get("plan") or []
    miss_txt = ""
    if missing:
        bits = []
        for n in missing:
            if 1 <= n <= len(plan):
                bits.append(f"{n}) {plan[n - 1]}")
        if bits:
            miss_txt = "\nПроверь пункты:\n• " + "\n• ".join(bits)
    fb = verdict.get("feedback_ru") or "Дополни пересказ по плану."
    await m.answer(f"❌ {fb}{miss_txt}\n\nМожешь прислать исправленный пересказ.")


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
