"""Раздел «Живая речь» — пока только MANAGER_ID, один пак."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from data.street_talk import (
    BTN_BACK_PACKS,
    BTN_BACK_SECTIONS,
    BTN_REPLAY,
    BTN_SKIP_SPEAK,
    BTN_STREET,
    BTN_TASKS,
    SECTION_INTRO_HTML,
    pack_button_label,
    pack_by_button_label,
)
from handlers.filters import ModeFilter
from handlers.lesson_filters import LessonHubFilter
from handlers.lesson_keyboards import level_sections_kb
from services.database import MODE_LESSONS, get_user, load_users
from services.lesson_state import assessment_busy, ensure_lesson, set_level_hub
from services.street_talk import (
    advance_task,
    bump_attempt,
    check_mcq,
    check_speak,
    check_write,
    clear_session,
    current_pack,
    current_task,
    ensure_street,
    is_pack_done,
    packs_for_list,
    reset_attempts,
    set_street_list,
    start_pack_card,
    start_tasks,
    street_talk_allowed,
)

router = Router()

_NAV = {
    BTN_STREET,
    BTN_TASKS,
    BTN_BACK_PACKS,
    BTN_BACK_SECTIONS,
    BTN_REPLAY,
    BTN_SKIP_SPEAK,
    "⏭ Пропустить произношение",
    "⏭️ Пропустить произношение",
    "Пропустить произношение",
    "🔙 Вернуться в меню",
}


def _packs_kb(user: dict) -> ReplyKeyboardMarkup:
    rows = []
    for p in packs_for_list():
        rows.append(
            [KeyboardButton(text=pack_button_label(p, done=is_pack_done(user, p["id"])))]
        )
    rows.append([KeyboardButton(text=BTN_BACK_SECTIONS)])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _card_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_TASKS)],
            [KeyboardButton(text=BTN_BACK_PACKS)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def _task_kb(task: dict) -> ReplyKeyboardMarkup:
    rows: list[list[KeyboardButton]] = []
    if task.get("kind") in {"mcq", "listen_mcq"}:
        for opt in task.get("options") or []:
            rows.append([KeyboardButton(text=opt)])
    if task.get("kind") == "listen_mcq":
        rows.append([KeyboardButton(text=BTN_REPLAY)])
    if task.get("kind") == "speak":
        rows.append([KeyboardButton(text=BTN_SKIP_SPEAK)])
    rows.append([KeyboardButton(text=BTN_BACK_PACKS)])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


async def _goto_sections(m: Message) -> None:
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    level = (user.get("lesson") or {}).get("level") or user.get("level") or "A1"
    clear_session(uid)
    set_level_hub(uid, level)
    await m.answer(
        f"🎓 Уровень {level} — выбери раздел:",
        reply_markup=level_sections_kb(user_id=m.from_user.id),
    )


async def _goto_packs(m: Message) -> None:
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    level = (user.get("lesson") or {}).get("level") or user.get("level") or "A1"
    clear_session(uid)
    set_street_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    await m.answer(
        SECTION_INTRO_HTML,
        reply_markup=_packs_kb(user),
        parse_mode="HTML",
    )


async def _send_task(m: Message, user: dict, task: dict) -> None:
    from services.elevenlabs import send_rico_voice

    kb = _task_kb(task)
    voice_en = (task.get("voice_en") or "").strip()
    if task.get("kind") in {"listen_mcq", "speak"} and voice_en:
        ok = await send_rico_voice(m, voice_en, user=user, title="Живая речь")
        if not ok and task.get("kind") == "listen_mcq":
            await m.answer(
                "Голос не отправился — вот фраза:\n"
                f"<tg-spoiler>{voice_en}</tg-spoiler>",
                parse_mode="HTML",
            )
    if task.get("kind") == "speak":
        phrase = (task.get("phrase") or voice_en).strip()
        if phrase and phrase != voice_en:
            await send_rico_voice(m, phrase, user=user, title="Живая речь · образец")
    await m.answer(task["prompt_html"], reply_markup=kb, parse_mode="HTML")


async def open_street_for_level(m: Message, user: dict, level: str) -> None:
    uid = str(m.from_user.id)
    if not street_talk_allowed(uid):
        return
    ensure_street(user)
    set_street_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    await m.answer(
        SECTION_INTRO_HTML,
        reply_markup=_packs_kb(user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_STREET)
async def open_street_section(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    if (user.get("lesson") or {}).get("hub") != "level_hub":
        return
    level = (user.get("lesson") or {}).get("level") or user.get("level") or "A1"
    await open_street_for_level(m, user, level)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("street_list"), F.text == BTN_BACK_SECTIONS)
async def street_back_sections(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    await _goto_sections(m)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("street_list"), F.text)
async def street_pick_pack(m: Message):
    text = (m.text or "").strip()
    if text in _NAV:
        return
    if not street_talk_allowed(m.from_user.id):
        return
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    pack = pack_by_button_label(text)
    if not pack:
        await m.answer("Выбери пак кнопкой ниже.", reply_markup=_packs_kb(user))
        return
    start_pack_card(str(m.from_user.id), pack["id"])
    await m.answer(pack["card_html"], reply_markup=_card_kb(), parse_mode="HTML")


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("street_card", "street_task"), F.text == BTN_BACK_PACKS)
async def street_back_packs(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    await _goto_packs(m)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("street_card", "street_task"), F.text == BTN_BACK_SECTIONS)
async def street_task_back_sections(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    await _goto_sections(m)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("street_card"), F.text == BTN_TASKS)
async def street_start_tasks(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    uid = str(m.from_user.id)
    start_tasks(uid)
    users = load_users()
    user = get_user(users, uid)
    task = current_task(user)
    if not task:
        await _goto_packs(m)
        return
    await _send_task(m, user, task)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("street_task"), F.text == BTN_REPLAY)
async def street_replay(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    task = current_task(user)
    if not task or task.get("kind") != "listen_mcq":
        return
    from services.elevenlabs import send_rico_voice

    voice_en = (task.get("voice_en") or "").strip()
    if voice_en:
        await send_rico_voice(m, voice_en, user=user, title="Живая речь · повтор")
    await m.answer("Ещё раз. Выбери ответ кнопкой.", reply_markup=_task_kb(task))


@router.message(
    ModeFilter(MODE_LESSONS),
    LessonHubFilter("street_task"),
    F.text.in_(
        {
            BTN_SKIP_SPEAK,
            "⏭ Пропустить произношение",
            "⏭️ Пропустить произношение",
            "Пропустить произношение",
        }
    ),
)
async def street_skip_speak(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    task = current_task(user)
    if not task or task.get("kind") != "speak":
        return
    await m.answer("Ок, пропускаем произношение 🦜")
    await _after_correct(m, user)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("street_task"), F.voice)
async def street_voice_answer(m: Message):
    if not street_talk_allowed(m.from_user.id):
        raise SkipHandler
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    task = current_task(user)
    if not task:
        raise SkipHandler
    if task.get("kind") != "speak":
        await m.answer(
            "Тут нужен ответ кнопкой, не голосом.",
            reply_markup=_task_kb(task),
        )
        return

    from services.stt import recognize_english

    phrase = (task.get("phrase") or "").strip()
    uid = str(m.from_user.id)
    try:
        file = await m.bot.get_file(m.voice.file_id)
        voice_buffer = await m.bot.download_file(file.file_path)
        heard = (recognize_english(voice_buffer.read(), hint=phrase) or "").strip()
    except Exception:
        heard = ""

    if heard and check_speak(task, heard):
        await m.answer(f"✅ Услышал: <i>{heard}</i>", parse_mode="HTML")
        await _after_correct(m, user)
        return

    attempts = bump_attempt(uid)
    shown = heard or "…"
    if attempts >= 2:
        await m.answer(
            f"Услышал: <i>{shown}</i>\n"
            f"Ориентир: <b>{phrase}</b>\n"
            "Идём дальше — ещё наговоримся в следующих паках 🦜",
            parse_mode="HTML",
        )
        await _after_correct(m, user)
        return
    await m.answer(
        f"Услышал: <i>{shown}</i>\n"
        f"Попробуй ещё раз:\n<b>{phrase}</b>",
        parse_mode="HTML",
        reply_markup=_task_kb(task),
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("street_task"), F.text)
async def street_task_answer(m: Message):
    text = (m.text or "").strip()
    if text in _NAV:
        return
    if not street_talk_allowed(m.from_user.id):
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    task = current_task(user)
    if not task:
        await _goto_packs(m)
        return

    kind = task.get("kind")
    if kind == "speak":
        await m.answer(
            "Пришли голосовое — или жми «Пропустить произношение».",
            reply_markup=_task_kb(task),
        )
        return

    if kind in {"mcq", "listen_mcq"}:
        ok = check_mcq(task, text)
        if text not in (task.get("options") or []) and not ok:
            await m.answer("Выбери вариант кнопкой.", reply_markup=_task_kb(task))
            return
        if ok:
            await _after_correct(m, user)
            return
        await _after_wrong(m, user, task)
        return

    if kind == "write":
        if check_write(task, text):
            await _after_correct(m, user)
            return
        await _after_wrong(m, user, task)
        return

    await m.answer("Выбери действие кнопкой.", reply_markup=_task_kb(task))


async def _after_wrong(m: Message, user: dict, task: dict) -> None:
    uid = str(m.from_user.id)
    attempts = bump_attempt(uid)
    if attempts >= 2:
        ans = (task.get("answer") or "").strip()
        await m.answer(
            f"Не в этот раз. Правильно: <b>{ans}</b>",
            parse_mode="HTML",
        )
        await _after_correct(m, user, celebrate=False)
        return
    await m.answer("Ещё попытка — подумай и ответь снова.", reply_markup=_task_kb(task))


async def _after_correct(m: Message, user: dict, *, celebrate: bool = True) -> None:
    uid = str(m.from_user.id)
    task = current_task(user)
    pack = current_pack(user) or {}
    title = pack.get("title_ru") or "пак"
    if celebrate and task and task.get("ok_html"):
        await m.answer(task["ok_html"], parse_mode="HTML")
    reset_attempts(uid)
    nxt = advance_task(uid)
    users = load_users()
    user = get_user(users, uid)
    if nxt is None:
        set_street_list(uid, (user.get("lesson") or {}).get("level") or user.get("level") or "A1")
        users = load_users()
        user = get_user(users, uid)
        await m.answer(
            f"🏁 Пак «{title}» пройден.\n\n"
            "🦜 <b>Рико:</b> Теперь wanna и don'tcha не будут звучать как шум — "
            "ты слышишь, что за ними стоит.\n\n"
            "Остальные паки (чаты, сериалы) — после того как утвердим тон.",
            reply_markup=_packs_kb(user),
            parse_mode="HTML",
        )
        return
    task = current_task(user)
    if not task:
        await _goto_packs(m)
        return
    await _send_task(m, user, task)
