"""Раздел Listening — диалог + 3 задания (пока только MANAGER_ID)."""

from __future__ import annotations

import random

from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import MANAGER_ID
from handlers.filters import ModeFilter
from handlers.lesson_filters import LessonHubFilter
from handlers.lesson_keyboards import level_sections_kb
from data.listening_topics import topics_for_level, topic_by_button_label, get_topic
from services.database import MODE_LESSONS, load_users, get_user, save_users
from services.lesson_state import assessment_busy, ensure_lesson, set_level_hub
from services.listening_state import (
    ensure_listening,
    is_topic_done,
    set_listening_list,
    set_listening_hub,
    get_session,
    set_session,
    update_session,
    clear_session,
    mark_topic_done,
)
from services.listening_gen import generate_listening_pack
from services.elevenlabs import send_voice_reply
from services.growth import ensure_growth

router = Router()

BTN_READY = "✅ Готов"
BTN_LISTENED = "✅ Прослушал(а)"
BTN_TRUE = "✅ Верно"
BTN_FALSE = "❌ Неверно"
BTN_EXIT = "🚪 Выйти из Listening"
BTN_RETRY_ORDER = "🔄 Начать сначала"
BTN_BACK_TOPICS = "⬅️ К темам Listening"
BTN_BACK_SECTIONS = "⬅️ К разделам"
BTN_LISTENING = "🎧 Listening"


def listening_allowed(user_id: str | int) -> bool:
    try:
        return int(user_id) == int(MANAGER_ID)
    except (TypeError, ValueError):
        return False


def listening_topics_kb(level: str, user: dict) -> ReplyKeyboardMarkup:
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


def _exit_row() -> list[KeyboardButton]:
    return [KeyboardButton(text=BTN_EXIT)]


def intro_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_READY)], _exit_row()],
        resize_keyboard=True,
    )


def listened_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_LISTENED)], _exit_row()],
        resize_keyboard=True,
    )


def mcq_kb(options: list[str]) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=o)] for o in options]
    rows.append(_exit_row())
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def tf_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_TRUE), KeyboardButton(text=BTN_FALSE)], _exit_row()],
        resize_keyboard=True,
    )


def order_kb(events: list[str], *, show_retry: bool = False) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=e)] for e in events]
    if show_retry:
        rows.append([KeyboardButton(text=BTN_RETRY_ORDER)])
    rows.append(_exit_row())
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def translate_q_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌍 Перевести вопрос", callback_data="listen:tr_q")]
        ]
    )


async def open_listening_for_level(m: Message, user: dict, level: str) -> None:
    uid = str(m.from_user.id)
    if not listening_allowed(uid):
        await m.answer(
            "🎧 Listening скоро откроется для всех. Пока раздел на проверке 🦜",
            reply_markup=level_sections_kb(user_id=uid),
        )
        return
    set_listening_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    await m.answer(
        f"🎧 <b>Listening · {level}</b>\n\n"
        "Выбери тему — короткий диалог + 3 задания на понимание.\n"
        "Если выйдешь посреди темы, прогресс темы сбросится.",
        reply_markup=listening_topics_kb(level, user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_LISTENING)
async def open_listening_section(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    if (user.get("lesson") or {}).get("hub") != "level_hub":
        return
    level = (user.get("lesson") or {}).get("level") or user.get("level") or "A1"
    await open_listening_for_level(m, user, level)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_list"), F.text == BTN_BACK_SECTIONS)
async def listening_back_sections(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    level = (user.get("lesson") or {}).get("level") or user.get("level") or "A1"
    clear_session(str(m.from_user.id))
    set_level_hub(str(m.from_user.id), level)
    await m.answer(
        f"🎓 Уровень {level} — выбери раздел:",
        reply_markup=level_sections_kb(user_id=m.from_user.id),
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_list"), F.text)
async def listening_pick_topic(m: Message):
    text = (m.text or "").strip()
    if text in {BTN_BACK_SECTIONS, "🔙 Вернуться в меню", BTN_EXIT}:
        return
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if not listening_allowed(m.from_user.id):
        return
    level = (user.get("lesson") or {}).get("level") or "A1"
    topic = topic_by_button_label(level, text)
    if not topic:
        await m.answer("Выбери тему кнопкой ниже.", reply_markup=listening_topics_kb(level, user))
        return

    await m.answer(
        f"🦜 <b>Рико:</b> Сейчас ты услышишь короткий диалог между друзьями "
        f"на тему «{topic['title_ru']}».\n\n"
        "Нажми <b>Готов</b>, когда будешь готов(а).\n"
        "Прослушай голосовые по порядку и выполни 3 задания.\n\n"
        "⚠️ Если выйдешь — прогресс темы сбросится, при следующем входе будет новый диалог.",
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
    set_listening_hub(str(m.from_user.id), "listening_play")


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_play", "listening_task1", "listening_task2", "listening_task3"), F.text == BTN_EXIT)
async def listening_exit(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    level = (get_session(user) or {}).get("level") or (user.get("lesson") or {}).get("level") or "A1"
    clear_session(str(m.from_user.id))
    set_listening_list(str(m.from_user.id), level)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.answer(
        "Ок, вышли. Прогресс этой попытки сброшен — тема не засчитана.\n"
        "Можешь выбрать тему снова (будет новая генерация).",
        reply_markup=listening_topics_kb(level, user),
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_play"), F.text == BTN_READY)
async def listening_ready(m: Message):
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
        "setting": "everyday dialogue",
    }

    from services.tg_out import status

    async with status(m, "🦜 Рико готовит диалог…"):
        pack = generate_listening_pack(level, topic)

    events = list(pack["task3_events"])
    shuffled = list(events)
    random.shuffle(shuffled)
    # если случайно совпало — ещё раз
    if shuffled == events:
        random.shuffle(shuffled)

    update_session(
        uid,
        content=pack,
        phase="playing",
        task1_i=0,
        task2_i=0,
        task3_picked=[],
        task3_shuffled=shuffled,
        task3_correct=events,
        last_question="",
    )
    set_listening_hub(uid, "listening_play")

    await m.answer(
        "🎧 Слушай диалог по порядку. Каждая реплика — отдельное голосовое.",
        reply_markup=listened_kb(),
    )
    voice_map = pack.get("voice_map") or {}
    for turn in pack["turns"]:
        speaker = turn["speaker"]
        text = turn["text"]
        vinfo = voice_map.get(speaker) or {}
        voice_id = vinfo.get("voice_id")
        await m.answer(f"<b>{speaker}:</b>", parse_mode="HTML")
        await send_voice_reply(m, text, title=f"{speaker}", voice_id=voice_id)

    await m.answer(
        "Когда прослушаешь всё — жми <b>Прослушал(а)</b> 👇",
        reply_markup=listened_kb(),
        parse_mode="HTML",
    )
    update_session(uid, phase="await_listened")


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_play"), F.text == BTN_LISTENED)
async def listening_listened(m: Message):
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user)
    if not sess or sess.get("phase") != "await_listened":
        return
    await _start_task1(m, uid)


async def _start_task1(m: Message, uid: str) -> None:
    update_session(uid, phase="task1", task1_i=0)
    set_listening_hub(uid, "listening_task1")
    await m.answer(
        "📝 <b>Задание 1 · Понимание</b>\n\n"
        "Сейчас 3 вопроса по диалогу на английском.\n"
        "Выбери ответ кнопкой. Можно перевести сам вопрос.",
        parse_mode="HTML",
    )
    await _send_task1_question(m, uid)


async def _send_task1_question(m: Message, uid: str) -> None:
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    content = sess.get("content") or {}
    qs = content.get("task1") or []
    i = int(sess.get("task1_i") or 0)
    if i >= len(qs):
        await _start_task2(m, uid)
        return
    q = qs[i]
    question = q["question"]
    update_session(uid, last_question=question)
    await m.answer(
        f"<b>Вопрос {i + 1}/3</b>\n\n{question}",
        reply_markup=mcq_kb(q["options"]),
        parse_mode="HTML",
    )
    await m.answer("👇", reply_markup=translate_q_kb())


@router.callback_query(F.data == "listen:tr_q")
async def listening_translate_question(c: CallbackQuery):
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    sess = get_session(user) or {}
    q = (sess.get("last_question") or "").strip()
    if not q:
        await c.answer("Сейчас нечего переводить", show_alert=True)
        return
    from services.translation import translate_to_russian

    await c.answer()
    ru = translate_to_russian(q)
    if not ru:
        await c.message.answer("Не получилось перевести — попробуй ещё раз.")
        return
    await c.message.answer(f"🇷🇺 <b>Перевод вопроса:</b>\n{ru}", parse_mode="HTML")


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_task1"), F.text)
async def listening_task1_answer(m: Message):
    text = (m.text or "").strip()
    if text in {BTN_EXIT, BTN_READY, BTN_LISTENED}:
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    content = sess.get("content") or {}
    qs = content.get("task1") or []
    i = int(sess.get("task1_i") or 0)
    if i >= len(qs):
        return
    q = qs[i]
    opts = q.get("options") or []
    if text not in opts:
        await m.answer("Выбери один из вариантов кнопкой.", reply_markup=mcq_kb(opts))
        return
    correct_i = int(q.get("correct") or 0)
    correct_ans = opts[correct_i] if 0 <= correct_i < len(opts) else opts[0]
    if text == correct_ans:
        await m.answer("✅ Верно!")
    else:
        await m.answer(f"❌ Не совсем. Правильный ответ: <b>{correct_ans}</b>", parse_mode="HTML")
    update_session(uid, task1_i=i + 1)
    await _send_task1_question(m, uid)


async def _start_task2(m: Message, uid: str) -> None:
    update_session(uid, phase="task2", task2_i=0)
    set_listening_hub(uid, "listening_task2")
    await m.answer(
        "📝 <b>Задание 2 · Верно / Неверно</b>\n\n"
        "🦜 Рико: Проверим, насколько внимательно ты слушал(а)!\n"
        "Сейчас 3 утверждения — на каждое жми <b>Верно</b> или <b>Неверно</b>.",
        parse_mode="HTML",
        reply_markup=tf_kb(),
    )
    await _send_task2_item(m, uid)


async def _send_task2_item(m: Message, uid: str) -> None:
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    items = (sess.get("content") or {}).get("task2") or []
    i = int(sess.get("task2_i") or 0)
    if i >= len(items):
        await m.answer("🎉 Задание 2 выполнено! Идём к третьему…")
        await _start_task3(m, uid)
        return
    st = items[i]["statement"]
    await m.answer(
        f"<b>Утверждение {i + 1}/3</b>\n\n{st}",
        reply_markup=tf_kb(),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_task2"), F.text.in_({BTN_TRUE, BTN_FALSE}))
async def listening_task2_answer(m: Message):
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    items = (sess.get("content") or {}).get("task2") or []
    i = int(sess.get("task2_i") or 0)
    if i >= len(items):
        return
    item = items[i]
    user_says_true = m.text == BTN_TRUE
    is_true = bool(item.get("is_true"))
    explain = item.get("explain_ru") or ""
    if user_says_true == is_true:
        await m.answer(f"✅ Правильно!\n{explain}")
    else:
        await m.answer(f"❌ Не так.\n{explain}")
    update_session(uid, task2_i=i + 1)
    await _send_task2_item(m, uid)


async def _start_task3(m: Message, uid: str) -> None:
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    shuffled = list(sess.get("task3_shuffled") or sess.get("task3_correct") or [])
    update_session(uid, phase="task3", task3_picked=[])
    set_listening_hub(uid, "listening_task3")
    await m.answer(
        "📝 <b>Задание 3 · Восстанови порядок событий</b>\n\n"
        "🦜 Рико: Нажми 4 события в правильной хронологии — "
        "от первого к последнему.",
        reply_markup=order_kb(shuffled),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_task3"), F.text == BTN_RETRY_ORDER)
async def listening_task3_retry(m: Message):
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    correct = list(sess.get("task3_correct") or [])
    shuffled = list(correct)
    random.shuffle(shuffled)
    update_session(uid, task3_picked=[], task3_shuffled=shuffled)
    await m.answer(
        "🔄 Ок, начнём порядок заново. Жми события по очереди:",
        reply_markup=order_kb(shuffled),
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_task3"), F.text)
async def listening_task3_pick(m: Message):
    text = (m.text or "").strip()
    if text in {BTN_EXIT, BTN_RETRY_ORDER}:
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    shuffled = list(sess.get("task3_shuffled") or [])
    correct = list(sess.get("task3_correct") or [])
    picked = list(sess.get("task3_picked") or [])
    if text not in shuffled:
        await m.answer("Жми кнопки событий ниже.", reply_markup=order_kb(shuffled, show_retry=bool(picked)))
        return
    if text in picked:
        await m.answer("Это событие уже выбрано.")
        return
    picked.append(text)
    update_session(uid, task3_picked=picked)
    lines = [f"{n}. {e}" for n, e in enumerate(picked, start=1)]
    await m.answer("Твой порядок:\n" + "\n".join(lines), parse_mode="HTML")

    remaining = [e for e in shuffled if e not in picked]
    if remaining:
        await m.answer("Выбери следующее:", reply_markup=order_kb(remaining))
        return

    # проверка
    if picked == correct:
        level = sess.get("level") or "A1"
        topic_id = sess.get("topic_id") or ""
        title = sess.get("topic_title") or "тема"
        mark_topic_done(uid, level, topic_id)
        set_listening_list(uid, level)
        users = load_users()
        user = get_user(users, uid)
        await m.answer(
            "🏆 <b>Отличный результат!</b> Ты точно помнишь хронологию.\n\n"
            f"Тема «{title}» пройдена ✅ — можно выбрать следующую.",
            reply_markup=listening_topics_kb(level, user),
            parse_mode="HTML",
        )
        return

    await m.answer(
        "😕 Последовательность не совсем верная.\n"
        "Обрати внимание на начало диалога и моменты с заказом/действиями.\n"
        "Можешь нажать события заново или «Начать сначала».",
        reply_markup=order_kb(shuffled, show_retry=True),
    )
    update_session(uid, task3_picked=[])
