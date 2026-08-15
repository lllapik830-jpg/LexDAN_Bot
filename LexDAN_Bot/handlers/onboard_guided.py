"""
Направляемый онбординг: привет → тест → Огонь дня → to be.
/imit_start · /imit_finish — прогон для админа.
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
    ONBOARD_TOPIC_ID,
    ONBOARD_TOPIC_LEVEL,
    ONBOARD_TOPIC_TITLE,
    PATH_DONE_HTML,
    PATH_NAV_HTML,
    SLIDES,
    TASKS_OVERVIEW_HTML,
    clarify_rico,
    complete_guided_path,
    ensure_onboard,
    path_channel_html,
    finish_imit_onboard,
    is_guided_onboard,
    onboard_stage,
    start_imit_onboard,
)
from services.lesson_state import open_topic

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


def _slide_kb(idx: int) -> InlineKeyboardMarkup:
    last = idx >= len(SLIDES) - 1
    rows: list[list[InlineKeyboardButton]] = []
    nav: list[InlineKeyboardButton] = []
    if idx > 0:
        nav.append(
            InlineKeyboardButton(text="⬅️ Назад", callback_data="og:prev")
        )
    if not last:
        nav.append(
            InlineKeyboardButton(text="➡️ Далее", callback_data="og:next")
        )
    if nav:
        rows.append(nav)
    rows.append(
        [InlineKeyboardButton(text="❓ Уточнить", callback_data="og:ask")]
    )
    if last:
        rows.append(
            [
                InlineKeyboardButton(
                    text="📝 Перейти к заданиям",
                    callback_data="og:tasks",
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)


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


def _got_it_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Понял",
                    callback_data="og:got_it",
                )
            ]
        ]
    )


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
    # Убрать кнопки разделов Огня дня
    await m.answer("✨", reply_markup=ReplyKeyboardRemove())
    await m.answer(DF_DONE_HTML, reply_markup=grammar_cta_kb(), parse_mode="HTML")
    return True


async def _render_slide(bot, user: dict, *, chat_id: int | None = None) -> None:
    """Одно сообщение со слайдом — только edit, без новых текстов объяснения."""
    ob = ensure_onboard(user)
    idx = int(ob.get("slide") or 0)
    idx = max(0, min(idx, len(SLIDES) - 1))
    ob["slide"] = idx
    text = SLIDES[idx]
    kb = _slide_kb(idx)
    msg_id = ob.get("slide_msg_id")
    cid = chat_id or ob.get("slide_chat_id")
    if msg_id and cid:
        try:
            await bot.edit_message_text(
                text,
                chat_id=int(cid),
                message_id=int(msg_id),
                reply_markup=kb,
                parse_mode="HTML",
            )
            return
        except Exception:
            pass


async def begin_to_be_slides(m: Message, uid: str) -> None:
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    if not is_guided_onboard(user):
        await m.answer("Сценарий знакомства сейчас не активен.")
        return

    set_mode(uid, MODE_LESSONS)
    from services.lesson_state import set_grammar_list, update_lesson, ensure_lesson

    set_grammar_list(uid, ONBOARD_TOPIC_LEVEL)
    open_topic(uid, ONBOARD_TOPIC_ID, ONBOARD_TOPIC_TITLE)

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
    ob["clarify_ids"] = []
    ob["slide_msg_id"] = None
    ob["slide_chat_id"] = None
    save_users(users, only=uid)

    await m.answer("📚", reply_markup=ReplyKeyboardRemove())
    sent = await m.answer(
        SLIDES[0],
        reply_markup=_slide_kb(0),
        parse_mode="HTML",
    )
    users = load_users()
    user = get_user(users, uid)
    ob = ensure_onboard(user)
    ob["slide_msg_id"] = sent.message_id
    ob["slide_chat_id"] = sent.chat.id
    save_users(users, only=uid)


@router.message(Command("imit_start"))
async def imit_start_cmd(m: Message):
    """Полный онбординг с нуля (как новый пользователь). Только MANAGER."""
    from config import MANAGER_ID
    from handlers.start import HELLO_NEW, HELLO_RICO_VOICE_EN, _hello_cta_kb
    from services.lesson_state import clear_lesson
    from services.elevenlabs import send_rico_voice

    if not m.from_user or m.from_user.id != MANAGER_ID:
        return

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
        "Выход: /imit_finish",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML",
    )
    await m.answer(HELLO_NEW, reply_markup=_hello_cta_kb(), parse_mode="HTML")
    # Ждём голос: create_task мог молча не отправиться
    await send_rico_voice(m, HELLO_RICO_VOICE_EN, user=user, title="Rico · hello")


@router.message(Command("imit_finish"))
async def imit_finish_cmd(m: Message):
    from config import MANAGER_ID

    if not m.from_user or m.from_user.id != MANAGER_ID:
        return
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
        await c.message.answer("Сценарий знакомства сейчас не активен.")
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
    # Передумал уточнять — убрать «спрашивай только про тему»
    if ob.get("awaiting_clarify") or ob.get("clarify_ids"):
        for mid in list(ob.get("clarify_ids") or []):
            try:
                await c.bot.delete_message(c.message.chat.id, int(mid))
            except Exception:
                pass
        ob["clarify_ids"] = []
        ob["awaiting_clarify"] = False
    ob["slide"] = min(int(ob.get("slide") or 0) + 1, len(SLIDES) - 1)
    ob["slide_msg_id"] = c.message.message_id
    ob["slide_chat_id"] = c.message.chat.id
    save_users(users, only=uid)
    await _render_slide(c.bot, user, chat_id=c.message.chat.id)


@router.callback_query(F.data == "og:prev")
async def cb_slide_prev(c: CallbackQuery):
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    if not is_guided_onboard(user) or onboard_stage(user) != "slides":
        return
    ob = ensure_onboard(user)
    if ob.get("awaiting_clarify") or ob.get("clarify_ids"):
        for mid in list(ob.get("clarify_ids") or []):
            try:
                await c.bot.delete_message(c.message.chat.id, int(mid))
            except Exception:
                pass
        ob["clarify_ids"] = []
        ob["awaiting_clarify"] = False
    ob["slide"] = max(int(ob.get("slide") or 0) - 1, 0)
    ob["slide_msg_id"] = c.message.message_id
    ob["slide_chat_id"] = c.message.chat.id
    save_users(users, only=uid)
    await _render_slide(c.bot, user, chat_id=c.message.chat.id)


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
    # слайд остаётся тем же сообщением
    ob["slide_msg_id"] = c.message.message_id
    ob["slide_chat_id"] = c.message.chat.id
    save_users(users, only=uid)
    ask = await c.message.answer(
        "🦜 Спрашивай <b>только про эту тему</b> (to be) — напиши вопрос текстом 👇",
        parse_mode="HTML",
    )
    users = load_users()
    user = get_user(users, uid)
    ob = ensure_onboard(user)
    ids = list(ob.get("clarify_ids") or [])
    ids.append(ask.message_id)
    ob["clarify_ids"] = ids
    save_users(users, only=uid)


@router.callback_query(F.data == "og:got_it")
async def cb_got_it(c: CallbackQuery):
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ob = ensure_onboard(user)
    ids = list(ob.get("clarify_ids") or [])
    # удалить и само сообщение с «Понял»
    ids.append(c.message.message_id)
    chat_id = c.message.chat.id
    for mid in ids:
        try:
            await c.bot.delete_message(chat_id, int(mid))
        except Exception:
            pass
    ob["clarify_ids"] = []
    ob["awaiting_clarify"] = False
    save_users(users, only=uid)


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
    if ob.get("clarify_ids"):
        await c.answer("Сначала закрой уточнение кнопкой «Понял»", show_alert=True)
        return
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
    ids = list(ob.get("clarify_ids") or [])
    ids.append(m.message_id)  # вопрос пользователя тоже уберём по «Понял»
    ob["clarify_ids"] = ids
    save_users(users, only=uid)

    name = (user.get("name") or "друг").strip()
    from services.tg_out import status

    async with status(m, "🦜 Рико думает…"):
        answer = clarify_rico(m.text or "", user_name=name)

    ans = await m.answer(answer, parse_mode="HTML")
    got = await m.answer(
        "Если ясно — жми 👇",
        reply_markup=_got_it_kb(),
    )
    users = users_for(uid)
    user = get_user(users, uid)
    ob = ensure_onboard(user)
    ids = list(ob.get("clarify_ids") or [])
    ids.extend([ans.message_id, got.message_id])
    ob["clarify_ids"] = ids
    save_users(users, only=uid)


async def finish_guided_after_topic(m: Message, uid: str) -> None:
    users = load_users()
    user = get_user(users, uid)
    complete_guided_path(user)
    save_users(users, only=uid)
    set_mode(uid, MODE_MENU)
    await m.answer(PATH_DONE_HTML, parse_mode="HTML")
    await m.answer(path_channel_html(), parse_mode="HTML")
    await m.answer(
        PATH_NAV_HTML,
        reply_markup=main_menu(user, user_id=uid),
        parse_mode="HTML",
    )
