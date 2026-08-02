"""Эксклюзивные задания Рико — /test_winners и прохождение паков 1/2/3."""

from __future__ import annotations

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import MANAGER_ID
from handlers.filters import ModeFilter
from handlers.keyboards import main_menu
from services.database import (
    MODE_EXCLUSIVE,
    MODE_MENU,
    users_for,
    get_user,
    save_users,
    set_mode,
)
from services.growth import ensure_growth, is_premium
from services.exclusive_rico import (
    BTN_EX_PLACE_1,
    BTN_EX_PLACE_2,
    BTN_EX_PLACE_3,
    BTN_EX_NEXT,
    BTN_EX_HINT,
    BTN_EX_SKIP,
    BTN_EX_EXIT,
    PLACE_BUTTONS,
    get_pack,
    start_pack,
    get_active,
    clear_active,
    current_task,
    advance,
    format_task_card,
    mcq_options,
    check_answer,
)
from services.elevenlabs import send_voice_reply
from services.voices import RICO_VOICE_ID
from services.stt import recognize_english

router = Router()


def _uid(m: Message) -> str:
    return str(m.from_user.id)


def _can_test(m: Message, user: dict) -> bool:
    """Менеджер или активный триал/премиум — для обкатки."""
    if m.from_user and m.from_user.id == MANAGER_ID:
        return True
    if user.get("in_promo_trial") or user.get("reg_full_trial_granted"):
        return True
    return bool(is_premium(user))


def _hub_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_EX_PLACE_1)],
            [KeyboardButton(text=BTN_EX_PLACE_2)],
            [KeyboardButton(text=BTN_EX_PLACE_3)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def _play_kb(task: dict | None) -> ReplyKeyboardMarkup:
    rows: list[list[KeyboardButton]] = []
    if task and (task.get("kind") or "") == "mcq":
        for opt in mcq_options(task):
            rows.append([KeyboardButton(text=opt)])
    rows.append([KeyboardButton(text=BTN_EX_HINT), KeyboardButton(text=BTN_EX_SKIP)])
    rows.append([KeyboardButton(text=BTN_EX_EXIT)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


async def _send_task(m: Message, user: dict) -> None:
    task = current_task(user)
    if not task:
        clear_active(user)
        await m.answer(
            "🦜 Пак пройден или пуст. Выбери место снова или выйди в меню.",
            reply_markup=_hub_kb(),
            parse_mode="HTML",
        )
        return
    await m.answer(format_task_card(user, task), reply_markup=_play_kb(task), parse_mode="HTML")
    if (task.get("kind") or "") == "voice":
        line = (task.get("voice_text") or "").strip()
        if line:
            await send_voice_reply(m, line, title="Эксклюзив Рико", voice_id=RICO_VOICE_ID)


@router.message(Command("test_winners"))
async def cmd_test_winners(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    if not _can_test(m, user):
        return  # молча, как админ-команды
    clear_active(user)
    set_mode(uid, MODE_EXCLUSIVE)
    users = users_for(uid)
    user = get_user(users, uid)
    save_users(users, only=uid)
    await m.answer(
        "🧪 <b>Тест призов ивента</b>\n\n"
        "Выбери место — загрузится эксклюзивный пак Рико:\n"
        "🥇 <b>1</b> — Легенда · квест + голос + перефраз + ошибки профи (20)\n"
        "🥈 <b>2</b> — Мастер · сленг/идиомы + карты слов (8)\n"
        "🥉 <b>3</b> — Охотник · охота на ошибки + загадки (8)\n\n"
        "Контент разный у каждого места. Это тестовый режим (прогресс пака локальный).",
        reply_markup=_hub_kb(),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text.in_(set(PLACE_BUTTONS)))
async def pick_place(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    place = PLACE_BUTTONS.get((m.text or "").strip())
    if not place:
        return
    pack = get_pack(place)
    if not pack:
        await m.answer("Пак не найден 😅", reply_markup=_hub_kb())
        return
    start_pack(user, place, test_mode=True)
    save_users(users, only=uid)
    await m.answer(pack.get("intro_html") or pack.get("title") or "Старт!", parse_mode="HTML")
    users = users_for(uid)
    user = get_user(users, uid)
    await _send_task(m, user)


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_EXIT)
@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == "🔙 Вернуться в меню")
async def exit_exclusive(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    clear_active(user)
    set_mode(uid, MODE_MENU)
    users = users_for(uid)
    user = get_user(users, uid)
    save_users(users, only=uid)
    await m.answer("Главное меню:", reply_markup=main_menu(user))


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_HINT)
async def exclusive_hint(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    task = current_task(user)
    if not task:
        await m.answer("Сначала выбери место 👇", reply_markup=_hub_kb())
        return
    hint = (task.get("hint_ru") or "Думай про смысл и конструкцию — ответ за тебя не скажу 💛").strip()
    await m.answer(f"💡 {hint}", reply_markup=_play_kb(task), parse_mode="HTML")


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_SKIP)
async def exclusive_skip(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    if not get_active(user):
        await m.answer("Сначала выбери место 👇", reply_markup=_hub_kb())
        return
    more = advance(user)
    save_users(users, only=uid)
    if not more:
        await m.answer(
            "🏁 Пак пройден (с пропусками). Можно выбрать другое место или выйти.",
            reply_markup=_hub_kb(),
            parse_mode="HTML",
        )
        return
    await m.answer("⏭ Ок, дальше — не зависаем 🚀", parse_mode="HTML")
    users = users_for(uid)
    user = get_user(users, uid)
    await _send_task(m, user)


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_NEXT)
async def exclusive_next_alias(m: Message):
    await exclusive_skip(m)


@router.message(ModeFilter(MODE_EXCLUSIVE), F.voice)
async def exclusive_voice(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    task = current_task(user)
    if not task:
        return
    if (task.get("kind") or "") != "voice":
        await m.answer("Здесь пока текстом 🙂", reply_markup=_play_kb(task))
        return
    try:
        heard = await recognize_english(m.bot, m.voice)
    except Exception:
        heard = ""
    if not (heard or "").strip():
        await m.answer(
            "Не разобрал голос 😅 Попробуй ещё раз или напиши текстом.",
            reply_markup=_play_kb(task),
        )
        return
    await _grade_and_advance(m, uid, user, users, task, heard)


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text)
async def exclusive_answer(m: Message):
    text = (m.text or "").strip()
    if not text or text.startswith("/"):
        return
    if text in {
        BTN_EX_PLACE_1,
        BTN_EX_PLACE_2,
        BTN_EX_PLACE_3,
        BTN_EX_HINT,
        BTN_EX_SKIP,
        BTN_EX_NEXT,
        BTN_EX_EXIT,
        "🔙 Вернуться в меню",
    }:
        return

    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    task = current_task(user)
    if not task:
        await m.answer("Выбери место кнопкой 👇", reply_markup=_hub_kb())
        return
    await _grade_and_advance(m, uid, user, users, task, text)


async def _grade_and_advance(
    m: Message, uid: str, user: dict, users: dict, task: dict, answer: str
) -> None:
    result = check_answer(task, answer)
    if not result.get("correct"):
        save_users(users, only=uid)
        await m.answer(
            "😅 " + (result.get("explain_ru") or "Почти! Попробуй ещё раз — тебе по плечу 💪"),
            reply_markup=_play_kb(task),
            parse_mode="HTML",
        )
        return

    more = advance(user)
    save_users(users, only=uid)
    cheers = [
        "✅ Есть! Красава 🦜",
        "✅ В яблочко 🎯",
        "✅ Супер, так держать ✨",
    ]
    import random

    await m.answer(random.choice(cheers), parse_mode="HTML")
    if not more:
        await m.answer(
            "🏆 <b>Пак закрыт!</b> Рико гордится.\n"
            "Можно прогнать другое место или вернуться в меню.",
            reply_markup=_hub_kb(),
            parse_mode="HTML",
        )
        return
    users = users_for(uid)
    user = get_user(users, uid)
    await _send_task(m, user)
