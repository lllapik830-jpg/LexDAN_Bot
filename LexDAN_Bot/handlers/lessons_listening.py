"""Раздел Listening — диалог + 3 задания."""

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

from handlers.filters import ModeFilter
from handlers.lesson_filters import LessonHubFilter
from handlers.lesson_keyboards import level_sections_kb
from data.listening_topics import topics_for_level, topic_by_button_label, get_topic
from services.database import MODE_LESSONS, load_users, get_user
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
    can_start_listening,
    consume_listening_slot,
)
from services.listening_gen import generate_listening_pack, build_order_summary, TURN_COUNT
from services.elevenlabs import send_voice_reply, send_rico_voice

router = Router()

# Голос Рико запрещён в репликах диалога Listening (только cast-голоса).
_RICO_VOICE_IDS = {
    "fBD19tfE58bkETeiwUoC",
    "XsmrVB66q3D4TaXVaWNF",
}
_CAST_FALLBACK_VOICE = "pNInz6obpgDQGcFmaJgB"  # Adam — не Рико


def _cast_voice_id(voice_id: str | None) -> str:
    """Voice ID персонажа диалога; никогда не Рико."""
    try:
        from services.voices import RICO_VOICE_ID, RICO_VOICE_ALT_ID

        banned = {RICO_VOICE_ID, RICO_VOICE_ALT_ID} | _RICO_VOICE_IDS
    except Exception:
        banned = set(_RICO_VOICE_IDS)
    vid = (voice_id or "").strip()
    if not vid or vid in banned:
        return _CAST_FALLBACK_VOICE
    return vid

BTN_READY = "✅ Готов"
BTN_LISTENED = "✅ Прослушал(а)"
BTN_TRUE = "✅ Верно"
BTN_FALSE = "❌ Неверно"
BTN_EXIT = "🚪 Выйти из Listening"
BTN_UNDO = "↩️ Отменить выбранное"
BTN_RESTART_PICK = "🔄 Начать выбирать заново"
BTN_BACK_TOPICS = "⬅️ К темам Listening"
BTN_BACK_SECTIONS = "⬅️ К разделам"
BTN_LISTENING = "🎧 Listening"


def _slow_for_level(level: str) -> bool:
    return str(level or "").upper() in {"A0", "A1"}


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


def listened_kb(n_turns: int) -> ReplyKeyboardMarkup:
    """Цифры 1..N — повтор реплики; затем «Прослушал»."""
    rows = []
    row = []
    for i in range(1, n_turns + 1):
        row.append(KeyboardButton(text=str(i)))
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text=BTN_LISTENED)])
    rows.append(_exit_row())
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def mcq_kb(options: list[str]) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=o)] for o in options]
    rows.append(_exit_row())
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def tf_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_TRUE), KeyboardButton(text=BTN_FALSE)], _exit_row()],
        resize_keyboard=True,
    )


def order_kb(remaining: list[str], *, picked: list[str] | None = None) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=e)] for e in remaining]
    if picked:
        rows.append([KeyboardButton(text=BTN_UNDO)])
        rows.append([KeyboardButton(text=BTN_RESTART_PICK)])
    rows.append(_exit_row())
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def translate_q_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌍 Перевести вопрос", callback_data="listen:tr_q")],
            [
                InlineKeyboardButton(
                    text="🇷🇺 Показать русский вариант",
                    callback_data="listen:ru_opts",
                )
            ],
        ]
    )


def translate_stmt_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌍 Перевести предложение",
                    callback_data="listen:tr_stmt",
                )
            ]
        ]
    )


def turn_replay_inline_kb(n: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌍 Перевести", callback_data=f"listen:tr_turn:{n}")]
        ]
    )


def _roles_phrase(topic: dict) -> str:
    roles = (topic.get("roles") or "").strip()
    if roles:
        return roles
    return "двух участников разговора"


async def open_listening_for_level(m: Message, user: dict, level: str) -> None:
    from services.growth import ensure_growth
    from services.rewards import user_plan

    uid = str(m.from_user.id)
    ensure_growth(user)
    set_listening_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    ensure_listening(user)
    plan = user_plan(user)
    if plan == "full":
        limit_note = "Безлимит ситуаций на твоём тарифе ✨"
    else:
        limit_note = "На free и 399₽ — <b>1 ситуация в день</b> · на 799₽ — безлимит."
    await m.answer(
        f"🎧 <b>Listening · {level}</b>\n\n"
        f"{limit_note}\n"
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
    level = (user.get("lesson") or {}).get("level") or "A1"
    topic = topic_by_button_label(level, text)
    if not topic:
        await m.answer("Выбери тему кнопкой ниже.", reply_markup=listening_topics_kb(level, user))
        return

    already_done = is_topic_done(user, level, topic["id"])
    if not already_done:
        ok, limit_msg = can_start_listening(user)
        if not ok:
            await m.answer(limit_msg, reply_markup=listening_topics_kb(level, user), parse_mode="HTML")
            return

    roles = _roles_phrase(topic)
    redo_note = (
        "\n\n♻️ Тема уже пройдена — это повтор без дневного лимита."
        if already_done
        else ""
    )
    await m.answer(
        f"🦜 <b>Рико:</b> Сейчас ты услышишь короткий диалог "
        f"(<i>{roles}</i>) на тему «{topic['title_ru']}».\n\n"
        "Нажми <b>Готов</b>, когда будешь готов(а).\n"
        "Прослушай голосовые по порядку и выполни 3 задания.\n"
        "Цифры под диалогом — повтор нужной реплики + перевод.\n\n"
        "⚠️ Если выйдешь — прогресс темы сбросится, при следующем входе будет новый диалог."
        f"{redo_note}",
        reply_markup=intro_kb(),
        parse_mode="HTML",
    )
    set_session(
        str(m.from_user.id),
        {
            "level": level,
            "topic_id": topic["id"],
            "topic_title": topic["title_ru"],
            "topic_roles": roles,
            "phase": "intro",
            "content": None,
            "slot_consumed": False,
        },
    )
    set_listening_hub(str(m.from_user.id), "listening_play")


@router.message(
    ModeFilter(MODE_LESSONS),
    LessonHubFilter("listening_play", "listening_task1", "listening_task2", "listening_task3"),
    F.text == BTN_EXIT,
)
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

    ok, limit_msg = can_start_listening(user)
    already_done = is_topic_done(user, sess.get("level") or "A1", sess.get("topic_id") or "")
    if not ok and not already_done:
        level = sess.get("level") or "A1"
        clear_session(uid)
        set_listening_list(uid, level)
        users = load_users()
        user = get_user(users, uid)
        await m.answer(limit_msg, reply_markup=listening_topics_kb(level, user), parse_mode="HTML")
        return

    level = sess["level"]
    topic = get_topic(level, sess["topic_id"]) or {
        "id": sess["topic_id"],
        "title_ru": sess.get("topic_title") or "Тема",
        "title_en": "Topic",
        "setting": "everyday dialogue",
        "roles": sess.get("topic_roles") or "two people",
    }

    from services.tg_out import status

    async with status(m, "🦜 Рико готовит диалог…"):
        pack = generate_listening_pack(level, topic)

    if not sess.get("slot_consumed") and not already_done:
        consume_listening_slot(uid)

    events = list(pack["task3_events"])
    shuffled = list(events)
    random.shuffle(shuffled)
    if shuffled == events:
        random.shuffle(shuffled)

    turns_n = pack.get("turns_numbered") or []
    update_session(
        uid,
        content=pack,
        phase="playing",
        task1_i=0,
        task2_i=0,
        task3_picked=[],
        task3_shuffled=shuffled,
        task3_correct=events,
        task3_fails=0,
        last_question="",
        last_statement="",
        slot_consumed=True,
    )
    set_listening_hub(uid, "listening_play")

    slow = _slow_for_level(level)
    # Список героев с акцентами (уникальные спикеры)
    cast_bits = []
    seen_sp = set()
    for t in turns_n:
        sp = t.get("speaker") or ""
        if not sp or sp in seen_sp:
            continue
        seen_sp.add(sp)
        acc = (t.get("accent") or "").strip()
        # accent может быть только в label — достанем из label если нет поля
        if not acc:
            lab = t.get("label") or ""
            if " · " in lab:
                mid = lab.split(" · ", 1)[1]
                acc = mid.rsplit(" ", 1)[0].strip()
        cast_bits.append(f"{sp}" + (f" · {acc}" if acc else ""))
    cast_line = ""
    if cast_bits:
        cast_line = "👥 <b>Кто говорит:</b> " + "; ".join(cast_bits) + "\n\n"
    await m.answer(
        cast_line
        + "🎧 Слушай диалог по порядку. Каждая реплика — отдельное голосовое.\n"
        "Ниже цифры — можно повторно открыть текст реплики и перевести.",
        reply_markup=listened_kb(len(turns_n) or len(pack.get("turns") or [])),
        parse_mode="HTML",
    )
    for t in turns_n:
        label = t.get("label") or f"{t['speaker']} {t['n']}"
        await m.answer(f"<b>{label}:</b>", parse_mode="HTML")
        # Без gTTS-fallback: иначе к 5–6 реплике голос персонажа прыгает на Google
        ok = await send_voice_reply(
            m,
            t["text"],
            title=label,
            voice_id=_cast_voice_id(t.get("voice_id")),
            slow=slow,
            allow_gtts_fallback=False,
        )
        if not ok:
            await m.answer(
                f"<i>(голос {t.get('speaker') or ''} временно недоступен — текст ниже)</i>\n"
                f"<code>{t.get('text') or ''}</code>",
                parse_mode="HTML",
            )

    await m.answer(
        "Когда прослушаешь всё — жми <b>Прослушал(а)</b>.\n"
        "Или нажми цифру, чтобы увидеть текст этой реплики.",
        reply_markup=listened_kb(len(turns_n) or TURN_COUNT),
        parse_mode="HTML",
    )
    update_session(uid, phase="await_listened")


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_play"), F.text == BTN_LISTENED)
async def listening_listened(m: Message):
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user)
    if not sess:
        return
    phase = sess.get("phase")
    if phase == "await_listened":
        await _start_task1(m, uid)
        return
    if phase == "await_listened_retry":
        # после первой ошибки порядка — снова задание 3
        await m.answer("Ок, ещё раз соберём порядок событий.")
        await _start_task3(m, uid)
        return


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_play"), F.text.regexp(r"^\d{1,2}$"))
async def listening_replay_turn(m: Message):
    """Повтор текста реплики по номеру + озвучка + кнопка перевести."""
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    if sess.get("phase") not in {"await_listened", "playing", "await_listened_retry"}:
        return
    try:
        n = int((m.text or "").strip())
    except ValueError:
        return
    turns = (sess.get("content") or {}).get("turns_numbered") or []
    turn = next((t for t in turns if int(t.get("n") or 0) == n), None)
    if not turn:
        await m.answer("Нет такой реплики. Выбери цифру из кнопок.")
        return
    label = turn.get("label") or f"{turn['speaker']} {n}"
    await m.answer(
        f"<b>{label}</b>\n\n{turn['text']}",
        reply_markup=turn_replay_inline_kb(n),
        parse_mode="HTML",
    )
    level = sess.get("level") or "A1"
    await send_voice_reply(
        m,
        turn["text"],
        title=label,
        voice_id=_cast_voice_id(turn.get("voice_id")),
        slow=_slow_for_level(level),
        allow_gtts_fallback=False,
    )


@router.callback_query(F.data.startswith("listen:tr_turn:"))
async def listening_translate_turn(c: CallbackQuery):
    try:
        n = int((c.data or "").split(":")[-1])
    except ValueError:
        await c.answer()
        return
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    sess = get_session(user) or {}
    turns = (sess.get("content") or {}).get("turns_numbered") or []
    turn = next((t for t in turns if int(t.get("n") or 0) == n), None)
    if not turn:
        await c.answer("Реплика не найдена", show_alert=True)
        return
    from services.translation import translate_to_russian

    await c.answer()
    ru = translate_to_russian(turn["text"])
    if not ru:
        await c.message.answer("Не получилось перевести — попробуй ещё раз.")
        return
    label = turn.get("label") or f"Реплика {n}"
    await c.message.answer(f"🇷🇺 <b>{label}:</b>\n{ru}", parse_mode="HTML")


async def _start_task1(m: Message, uid: str) -> None:
    update_session(uid, phase="task1", task1_i=0)
    set_listening_hub(uid, "listening_task1")
    await m.answer(
        "📝 <b>Задание 1 · Понимание</b>\n\n"
        "3 вопроса по диалогу. Выбери ответ кнопкой.\n"
        "Можно перевести вопрос или посмотреть русские варианты ответов "
        "(потом всё равно выбери ответ).",
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
    update_session(uid, last_question=question, last_options_ru=q.get("options_ru") or [])
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


@router.callback_query(F.data == "listen:ru_opts")
async def listening_show_ru_options(c: CallbackQuery):
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    sess = get_session(user) or {}
    opts_ru = sess.get("last_options_ru") or []
    if not opts_ru:
        # fallback из текущего вопроса
        content = sess.get("content") or {}
        qs = content.get("task1") or []
        i = int(sess.get("task1_i") or 0)
        if i < len(qs):
            opts_ru = qs[i].get("options_ru") or qs[i].get("options") or []
    if not opts_ru:
        await c.answer("Варианты недоступны", show_alert=True)
        return
    await c.answer()
    lines = [f"{n}. {o}" for n, o in enumerate(opts_ru, start=1)]
    await c.message.answer(
        "🇷🇺 <b>Варианты на русском:</b>\n" + "\n".join(lines) + "\n\n"
        "Теперь выбери ответ кнопкой на английском 👆",
        parse_mode="HTML",
    )


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
        explain = (q.get("explain_wrong_ru") or "").strip()
        msg = f"❌ Не совсем. Правильный ответ: <b>{correct_ans}</b>"
        if explain:
            msg += f"\n\n🦜 Рико: {explain}"
        await m.answer(msg, parse_mode="HTML")
    update_session(uid, task1_i=i + 1)
    await _send_task1_question(m, uid)


async def _start_task2(m: Message, uid: str) -> None:
    update_session(uid, phase="task2", task2_i=0)
    set_listening_hub(uid, "listening_task2")
    await m.answer(
        "📝 <b>Задание 2 · Верно / Неверно</b>\n\n"
        "🦜 Рико: Теперь другие детали диалога — не те же, что в первом задании!\n"
        "На каждое утверждение жми <b>Верно</b> или <b>Неверно</b>.",
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
    update_session(uid, last_statement=st)
    await m.answer(
        f"<b>Утверждение {i + 1}/3</b>\n\n{st}",
        reply_markup=tf_kb(),
        parse_mode="HTML",
    )
    await m.answer("👇", reply_markup=translate_stmt_kb())


@router.callback_query(F.data == "listen:tr_stmt")
async def listening_translate_statement(c: CallbackQuery):
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    sess = get_session(user) or {}
    st = (sess.get("last_statement") or "").strip()
    if not st:
        await c.answer("Сейчас нечего переводить", show_alert=True)
        return
    from services.translation import translate_to_russian

    await c.answer()
    ru = translate_to_russian(st)
    if not ru:
        await c.message.answer("Не получилось перевести — попробуй ещё раз.")
        return
    await c.message.answer(f"🇷🇺 <b>Перевод:</b>\n{ru}", parse_mode="HTML")


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
    explain = (item.get("explain_ru") or "").strip()
    if user_says_true == is_true:
        msg = "✅ Правильно!"
        if explain:
            msg += f"\n🦜 Рико: {explain}"
        await m.answer(msg)
    else:
        msg = "❌ Не так."
        if explain:
            msg += f"\n🦜 Рико: {explain}"
        await m.answer(msg)
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
        "🦜 Рико: Нажми 4 события в правильной хронологии — от первого к последнему.\n"
        "Ошибся — «Отменить выбранное» или «Начать выбирать заново».",
        reply_markup=order_kb(shuffled),
        parse_mode="HTML",
    )


def _remaining_events(shuffled: list[str], picked: list[str]) -> list[str]:
    """Убрать выбранные, сохраняя порядок кнопок; каждое событие один раз."""
    left = []
    used = list(picked)
    for e in shuffled:
        if e in used:
            used.remove(e)
            continue
        left.append(e)
    return left


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_task3"), F.text == BTN_UNDO)
async def listening_task3_undo(m: Message):
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    shuffled = list(sess.get("task3_shuffled") or [])
    picked = list(sess.get("task3_picked") or [])
    if not picked:
        await m.answer("Пока нечего отменять.", reply_markup=order_kb(shuffled))
        return
    picked.pop()
    update_session(uid, task3_picked=picked)
    remaining = _remaining_events(shuffled, picked)
    if picked:
        lines = [f"{n}. {e}" for n, e in enumerate(picked, start=1)]
        await m.answer(
            "↩️ Отменил последнее.\nТвой порядок:\n" + "\n".join(lines),
            reply_markup=order_kb(remaining, picked=picked),
        )
    else:
        await m.answer("↩️ Снова с нуля — выбирай первое событие:", reply_markup=order_kb(remaining))


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_task3"), F.text == BTN_RESTART_PICK)
async def listening_task3_restart(m: Message):
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    shuffled = list(sess.get("task3_shuffled") or [])
    update_session(uid, task3_picked=[])
    await m.answer(
        "🔄 Ок, выбираем события заново с первого:",
        reply_markup=order_kb(shuffled),
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("listening_task3"), F.text)
async def listening_task3_pick(m: Message):
    text = (m.text or "").strip()
    if text in {BTN_EXIT, BTN_UNDO, BTN_RESTART_PICK}:
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    sess = get_session(user) or {}
    shuffled = list(sess.get("task3_shuffled") or [])
    correct = list(sess.get("task3_correct") or [])
    picked = list(sess.get("task3_picked") or [])
    remaining = _remaining_events(shuffled, picked)
    if text not in remaining:
        await m.answer(
            "Жми кнопки событий ниже.",
            reply_markup=order_kb(remaining, picked=picked),
        )
        return

    picked.append(text)
    update_session(uid, task3_picked=picked)
    lines = [f"{n}. {e}" for n, e in enumerate(picked, start=1)]
    await m.answer("Твой порядок:\n" + "\n".join(lines))

    remaining = _remaining_events(shuffled, picked)
    if remaining:
        await m.answer(
            "Выбери следующее:",
            reply_markup=order_kb(remaining, picked=picked),
        )
        return

    # проверка полного порядка
    if picked == correct:
        await _finish_topic_ok(m, uid, sess)
        return

    fails = int(sess.get("task3_fails") or 0) + 1
    update_session(uid, task3_fails=fails, task3_picked=[])

    if fails == 1:
        await m.answer(
            "😕 Последовательность неверная.\n\n"
            "🦜 Рико: Прослушай ещё раз — нажми цифры реплик, "
            "потом «Прослушал(а)» и собери порядок заново.",
            reply_markup=listened_kb(len((sess.get("content") or {}).get("turns_numbered") or []) or TURN_COUNT),
        )
        update_session(uid, phase="await_listened_retry")
        set_listening_hub(uid, "listening_play")
        return

    # вторая ошибка — Рико показывает правильный порядок мини-текстом
    summary = build_order_summary(correct)
    level = sess.get("level") or "A1"
    slow = _slow_for_level(level)
    await m.answer(
        "🦜 Рико: Давай разберём правильный порядок.\n\n" + summary,
        parse_mode="HTML",
    )
    await send_rico_voice(m, summary, user=user, title="Rico order", slow=slow)
    from services.translation import translate_to_russian

    ru = translate_to_russian(summary) or ""
    if ru:
        await m.answer(f"🇷🇺 <b>Перевод:</b>\n{ru}", parse_mode="HTML")

    await _finish_topic_ok(m, uid, sess, after_help=True)


async def _finish_topic_ok(m: Message, uid: str, sess: dict, *, after_help: bool = False) -> None:
    level = sess.get("level") or "A1"
    topic_id = sess.get("topic_id") or ""
    title = sess.get("topic_title") or "тема"
    users = load_users()
    user = get_user(users, uid)

    already_done = is_topic_done(user, level, topic_id)
    mark_topic_done(uid, level, topic_id)
    set_listening_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    from services.collection import collection_allowed
    from services.event_magic import add_listening_points, remember_tg_username

    if (not already_done) and collection_allowed(uid):
        remember_tg_username(user, getattr(m.from_user, "username", None))
        add_listening_points(user)
        from services.database import save_users

        save_users(users, only=uid)
    if after_help:
        head = "Тема засчитана после разбора ✅"
    else:
        head = "🏆 <b>Отличный результат!</b> Ты точно помнишь хронологию."
    await m.answer(
        f"{head}\n\nТема «{title}» пройдена ✅ — можно выбрать следующую.",
        reply_markup=listening_topics_kb(level, user),
        parse_mode="HTML",
    )
