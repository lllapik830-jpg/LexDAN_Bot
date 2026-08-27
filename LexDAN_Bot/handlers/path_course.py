"""Новый путь: ежедневный курс A0→A1. Кнопка 🎓 Курсы, пока MANAGER."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from data.path_course import (
    ABOUT_HTML,
    BTN_ABOUT,
    BTN_CONTINUE,
    BTN_GO,
    BTN_NEXT,
    BTN_PATH,
    BTN_PAUSE,
    BTN_REPLAY,
    BTN_START_LESSON,
    WELCOME_HTML,
    skip_html,
)
from handlers.filters import ModeFilter
from services.course_placement import courses_allowed
from services.database import (
    MODE_PATH,
    get_user,
    save_users,
    set_mode,
    users_for,
)
from services.path_course import (
    consume_skip_flag,
    done_today,
    ensure_path,
    handle_answer,
    handle_next,
    hub_html,
    note_open,
    reset_path,
    start_or_resume,
)

router = Router()

_NAV = {
    BTN_PATH,
    BTN_GO,
    BTN_START_LESSON,
    BTN_CONTINUE,
    BTN_NEXT,
    BTN_PAUSE,
    BTN_ABOUT,
    BTN_REPLAY,
    "🔙 Вернуться в меню",
}


def _deny(m: Message) -> bool:
    return not courses_allowed(m.from_user.id if m.from_user else None)


def _hub_kb(user: dict) -> ReplyKeyboardMarkup:
    p = ensure_path(user)
    rows: list[list[KeyboardButton]] = []
    if done_today(user):
        pass
    elif isinstance(p.get("session"), dict):
        rows.append([KeyboardButton(text=BTN_CONTINUE)])
    elif not p.get("welcomed"):
        rows.append([KeyboardButton(text=BTN_GO)])
    else:
        rows.append([KeyboardButton(text=BTN_START_LESSON)])
    rows.append([KeyboardButton(text=BTN_REPLAY)])
    rows.append([KeyboardButton(text=BTN_ABOUT)])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _next_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_NEXT)],
            [KeyboardButton(text=BTN_PAUSE)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def _text_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_PAUSE)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def _mcq_kb(options: list[str]) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=opt)] for opt in options]
    rows.append([KeyboardButton(text=BTN_PAUSE)])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _kb_for(payload: dict, user: dict) -> ReplyKeyboardMarkup:
    kind = payload.get("kb")
    if kind == "next":
        return _next_kb()
    if kind == "mcq":
        return _mcq_kb(list(payload.get("options") or []))
    if kind == "text":
        return _text_kb()
    return _hub_kb(user)


async def _send_payload(m: Message, user: dict, payload: dict) -> None:
    for extra in payload.get("extras") or []:
        await m.answer(extra, parse_mode="HTML")
    flash = payload.get("flash")
    html = payload.get("html") or ""
    if flash:
        html = f"{flash}\n\n{html}" if html else flash
    await m.answer(html, parse_mode="HTML", reply_markup=_kb_for(payload, user))
    if payload.get("finished") and payload.get("hub"):
        await m.answer(payload["hub"], parse_mode="HTML", reply_markup=_hub_kb(user))


async def _open_hub(m: Message) -> None:
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_path(user)
    set_mode(uid, MODE_PATH)
    skip_n = note_open(user)
    show_skip = consume_skip_flag(user)
    first = not user["path"].get("welcomed")
    if first:
        user["path"]["welcomed"] = True
    save_users(users, only=uid)
    if first:
        await m.answer(WELCOME_HTML, parse_mode="HTML")
    if show_skip:
        await m.answer(skip_html(skip_n), parse_mode="HTML")
    await m.answer(hub_html(user), parse_mode="HTML", reply_markup=_hub_kb(user))


@router.message(Command("path_reset"))
async def path_reset_cmd(m: Message):
    if _deny(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    reset_path(user)
    set_mode(uid, MODE_PATH)
    save_users(users, only=uid)
    await m.answer("Курс сброшен. Снова урок 1 с нуля.", parse_mode="HTML")
    await _open_hub(m)


@router.message(ModeFilter(MODE_PATH), F.text == BTN_REPLAY)
async def path_replay(m: Message):
    if _deny(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    reset_path(user)
    set_mode(uid, MODE_PATH)
    save_users(users, only=uid)
    payload = start_or_resume(user)
    save_users(users, only=uid)
    await m.answer("Курс сброшен. Снова урок 1.", parse_mode="HTML")
    await _send_payload(m, user, payload)


@router.message(F.text == BTN_PATH)
async def open_path(m: Message):
    if _deny(m):
        raise SkipHandler
    await _open_hub(m)


@router.message(ModeFilter(MODE_PATH), F.text == BTN_ABOUT)
async def path_about(m: Message):
    if _deny(m):
        return
    uid = str(m.from_user.id)
    user = get_user(users_for(uid), uid)
    await m.answer(ABOUT_HTML, parse_mode="HTML", reply_markup=_hub_kb(user))


@router.message(ModeFilter(MODE_PATH), F.text == BTN_PAUSE)
async def path_pause(m: Message):
    if _deny(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_path(user)
    save_users(users, only=uid)
    await m.answer(
        "Пауза. Прогресс урока сохранён — можно продолжить сегодня.",
        reply_markup=_hub_kb(user),
    )


@router.message(ModeFilter(MODE_PATH), F.text.in_({BTN_GO, BTN_START_LESSON, BTN_CONTINUE}))
async def path_start(m: Message):
    if _deny(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_path(user)
    payload = start_or_resume(user)
    save_users(users, only=uid)
    await _send_payload(m, user, payload)


@router.message(ModeFilter(MODE_PATH), F.text == BTN_NEXT)
async def path_next(m: Message):
    if _deny(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_path(user)
    if not isinstance((user.get("path") or {}).get("session"), dict):
        await m.answer(hub_html(user), parse_mode="HTML", reply_markup=_hub_kb(user))
        return
    payload = handle_next(user)
    save_users(users, only=uid)
    await _send_payload(m, user, payload)


@router.message(ModeFilter(MODE_PATH), F.text)
async def path_text(m: Message):
    if _deny(m):
        return
    text = (m.text or "").strip()
    if text in _NAV:
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_path(user)
    if not isinstance((user.get("path") or {}).get("session"), dict):
        await m.answer("Жми кнопку ниже — урок или пауза.", reply_markup=_hub_kb(user))
        return
    payload = handle_answer(user, text)
    save_users(users, only=uid)
    await _send_payload(m, user, payload)
