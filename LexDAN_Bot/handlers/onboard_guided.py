"""
Имитация направляемого онбординга: /imit_start · /imit_finish.
Слайды to be, CTA после Огня дня, «Уточнить».
"""

import asyncio

from aiogram import Router, F
from aiogram.filters import Command, BaseFilter
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from handlers.filters import ModeFilter
from handlers.keyboards import main_menu
from services.database import (
    MODE_MENU,
    MODE_LESSONS,
    load_users,
    get_user,
    save_users,
    set_mode,
    users_for,
    fetch_user,
)
from services.growth import ensure_growth
from services.onboard_guided import (
    BTN_ONBOARD_START_TASKS,
    DF_DONE_HTML,
    DF_TOUR_HTML,
    ONBOARD_TOPIC_ID,
    ONBOARD_TOPIC_LEVEL,
    ONBOARD_TOPIC_TITLE,
    PATH_DONE_HTML,
    SLIDES,
    TASKS_OVERVIEW_HTML,
    clarify_rico,
    complete_guided_path,
    ensure_onboard,
    finish_imit_onboard,
    is_guided_onboard,
    onboard_stage,
    plain_for_tts,
    start_imit_onboard,
)
from services.lesson_state import open_topic
from services.elevenlabs import send_rico_voice

router = Router()


class OnboardClarifyFilter(BaseFilter):
    """Только когда ждём вопрос после «Уточнить»."""

    async def __call__(self, message: Message) -> bool:
        if not message.from_user or not message.text or message.text.startswith("/"):
            return False
        user = await asyncio.to_thread(
            fetch_user, str(message.from_user.id)
        )
        if not is_guided_onboard(user):
            return False
        if onboard_stage(user) != "slides":
            return False
        return bool(ensure_onboard(user).get("awaiting_clarify"))


def _slide_kb(*, last: bool = False) -> InlineKeyboardMarkup:
    if last:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📝 Перейти к заданиям",
                        callback_data="og:tasks",
                    )
                ]
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➡️ Далее",
                    callback_data="og:next",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❓ Уточнить",
                    callback_data="og:ask",
                )
            ],
        ]
    )


def grammar_cta_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Начать",
                    callback_data="og:start_be",
                )
            ]
        ]
    )


def tasks_start_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_ONBOARD_START_TASKS)]],
        resize_keyboard=True,
    )


async def send_df_tour_intro(m: Message, user: dict) -> None:
    ob = ensure_onboard(user)
    if not ob.get("active") or ob.get("df_intro_sent"):
        return
    if onboard_stage(user) != "daily_fire":
        return
    ob["df_intro_sent"] = True
    await m.answer(DF_TOUR_HTML, parse_mode="HTML")


async def maybe_send_df_done_cta(m: Message, user: dict, users: dict, uid: str) -> bool:
    """После просмотра всех 4 разделов Огня дня — CTA на грамматику."""
    if not is_guided_onboard(user):
        return False
    ob = ensure_onboard(user)
    if ob.get("df_done_sent") or onboard_stage(user) != "daily_fire":
        return False
    from services.daily_fire import opened_count, mark_ritual_celebrated

    if opened_count(user) < 4:
        return False

    mark_ritual_celebrated(user)
    ob["df_done_sent"] = True
    ob["stage"] = "grammar_cta"
    save_users(users, only=uid)
    await m.answer(DF_DONE_HTML, reply_markup=grammar_cta_kb(), parse_mode="HTML")
    return True


async def send_slide(m: Message, user: dict, *, edit: bool = False) -> None:
    ob = ensure_onboard(user)
    idx = int(ob.get("slide") or 0)
    idx = max(0, min(idx, len(SLIDES) - 1))
    ob["slide"] = idx
    last = idx >= len(SLIDES) - 1
    text = SLIDES[idx]
    kb = _slide_kb(last=last)
    if edit and getattr(m, "edit_text", None):
        try:
            await m.edit_text(text, reply_markup=kb, parse_mode="HTML")
            return
        except Exception:
            pass
    await m.answer(text, reply_markup=kb, parse_mode="HTML")


async def begin_to_be_slides(m: Message, uid: str) -> None:
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    if not is_guided_onboard(user):
        await m.answer("Сейчас имитация выключена. Включи: /imit_start")
        return

    set_mode(uid, MODE_LESSONS)
    from services.lesson_state import set_grammar_list

    set_grammar_list(uid, ONBOARD_TOPIC_LEVEL)
    open_topic(uid, ONBOARD_TOPIC_ID, ONBOARD_TOPIC_TITLE)
    from services.lesson_state import update_lesson, ensure_lesson

    def _hub_slides(u):
        ensure_lesson(u)
        u["lesson"]["hub"] = "onboard_slides"

    update_lesson(uid, _hub_slides)

    users = load_users()
    user = get_user(users, uid)
    ob = ensure_onboard(user)
    ob["stage"] = "slides"
    ob["slide"] = 0
    ob["awaiting_clarify"] = False
    save_users(users, only=uid)

    await m.answer(
        f"📚 Тема: <b>{ONBOARD_TOPIC_TITLE}</b>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )
    await send_slide(m, user)


@router.message(Command("imit_start"))
async def imit_start_cmd(m: Message):
    """Полный онбординг с нуля (как новый пользователь)."""
    from handlers.start import HELLO_NEW, _hello_cta_kb
    from services.lesson_state import clear_lesson

    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    start_imit_onboard(user)
    save_users(users, only=uid)
    clear_lesson(uid)
    set_mode(uid, MODE_MENU)
    await m.answer(
        "🧪 <b>Имитация полного онбординга</b>\n"
        "Привет → имя → тест → подарок → Огонь дня → to be → 8 заданий.\n"
        "Выход в любой момент: /imit_finish",
        parse_mode="HTML",
    )
    await m.answer(HELLO_NEW, reply_markup=_hello_cta_kb(), parse_mode="HTML")


@router.message(Command("imit_finish"))
async def imit_finish_cmd(m: Message):
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    finish_imit_onboard(user)
    save_users(users, only=uid)
    set_mode(uid, MODE_MENU)
    await m.answer(
        "✅ Имитация выключена. Профиль возвращён, обычный режим.",
        reply_markup=main_menu(user, user_id=uid),
    )


@router.callback_query(F.data == "og:start_be")
async def cb_start_be(c: CallbackQuery):
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    if not is_guided_onboard(user):
        await c.message.answer("Имитация выключена. /imit_start")
        return
    try:
        await c.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await begin_to_be_slides(c.message, uid)


@router.callback_query(F.data == "og:next")
async def cb_slide_next(c: CallbackQuery):
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    if not is_guided_onboard(user) or onboard_stage(user) != "slides":
        await c.answer("Сейчас это недоступно", show_alert=True)
        return
    ob = ensure_onboard(user)
    ob["awaiting_clarify"] = False
    ob["slide"] = int(ob.get("slide") or 0) + 1
    if ob["slide"] >= len(SLIDES):
        ob["slide"] = len(SLIDES) - 1
    save_users(users, only=uid)
    await send_slide(c.message, user, edit=True)


@router.callback_query(F.data == "og:ask")
async def cb_slide_ask(c: CallbackQuery):
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    if not is_guided_onboard(user) or onboard_stage(user) != "slides":
        return
    ob = ensure_onboard(user)
    ob["awaiting_clarify"] = True
    save_users(users, only=uid)
    await c.message.answer(
        "🦜 Спрашивай <b>только про эту тему</b> (to be) — напиши вопрос текстом 👇",
        parse_mode="HTML",
    )


@router.callback_query(F.data == "og:tasks")
async def cb_go_tasks(c: CallbackQuery):
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    if not is_guided_onboard(user):
        return
    ob = ensure_onboard(user)
    ob["stage"] = "tasks_menu"
    ob["awaiting_clarify"] = False
    save_users(users, only=uid)
    try:
        await c.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await c.message.answer(
        TASKS_OVERVIEW_HTML,
        reply_markup=tasks_start_kb(),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_ONBOARD_START_TASKS)
async def onboard_start_tasks(m: Message):
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    if not is_guided_onboard(user) or onboard_stage(user) != "tasks_menu":
        return
    ob = ensure_onboard(user)
    ob["stage"] = "tasks"
    save_users(users, only=uid)

    from handlers.lessons_grammar import _launch_exercise

    await _launch_exercise(
        m,
        uid,
        ONBOARD_TOPIC_LEVEL,
        ONBOARD_TOPIC_ID,
        ONBOARD_TOPIC_TITLE,
        1,
    )


@router.message(OnboardClarifyFilter(), F.text)
async def onboard_clarify_text(m: Message):
    """Вопрос после «Уточнить» на слайдах."""
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)

    from services.moderation import guard_user_text, ensure_moderation

    ensure_moderation(user)
    if not await guard_user_text(m, user, m.text or ""):
        return

    ob = ensure_onboard(user)
    ob["awaiting_clarify"] = False
    save_users(users, only=uid)

    name = (user.get("name") or "друг").strip()
    from services.tg_out import status

    async with status(m, "🦜 Рико думает…"):
        answer = clarify_rico(m.text or "", user_name=name)

    await m.answer(answer, parse_mode="HTML")
    await send_rico_voice(
        m,
        plain_for_tts(answer),
        user=user,
        title="Rico · уточнение",
    )
    await send_slide(m, user)


async def finish_guided_after_topic(m: Message, uid: str) -> None:
    users = load_users()
    user = get_user(users, uid)
    complete_guided_path(user)
    save_users(users, only=uid)
    set_mode(uid, MODE_MENU)
    await m.answer(
        PATH_DONE_HTML,
        reply_markup=main_menu(user, user_id=uid),
        parse_mode="HTML",
    )
