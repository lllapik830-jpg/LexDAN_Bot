"""Секретные задания Рико — вход из главного меню."""

import asyncio

from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from handlers.filters import ModeFilter
from handlers.keyboards import main_menu
from services.database import (
    MODE_SECRET,
    MODE_MENU,
    users_for,
    get_user,
    save_users,
)
from services.growth import ensure_growth
from services.secret_missions import (
    BTN_SECRET,
    BTN_SECRET_WEEK,
    BTN_SECRET_VOICE,
    BTN_SECRET_SKIP,
    BTN_SECRET_DONE,
    MISSION_WEEK,
    MISSION_VOICE,
    MISSION_META,
    ensure_missions,
    has_secret_entry,
    inbox_missions,
    start_mission,
    get_active,
    complete_mission,
    format_card,
    evaluate_voice_attempt,
    mission_intro,
    phrase_text,
)
from services.elevenlabs import send_voice_reply
from services.stt import recognize_english

router = Router()

BTN_BACK_MENU = "🔙 Вернуться в меню"
BTN_EXIT_SECRET = "🚪 Выйти из секрета"
BTN_NEXT = "➡️ Далее"


def _hub_kb(user: dict) -> ReplyKeyboardMarkup:
    rows = []
    inbox = inbox_missions(user)
    active = get_active(user)
    if active:
        if active.get("type") == MISSION_WEEK:
            rows.append([KeyboardButton(text=BTN_NEXT)])
        else:
            rows.append([KeyboardButton(text=BTN_SECRET_SKIP)])
        rows.append([KeyboardButton(text=BTN_EXIT_SECRET)])
    else:
        if MISSION_WEEK in inbox:
            rows.append([KeyboardButton(text=BTN_SECRET_WEEK)])
        if MISSION_VOICE in inbox:
            rows.append([KeyboardButton(text=BTN_SECRET_VOICE)])
        rows.append([KeyboardButton(text=BTN_BACK_MENU)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _menu_for(user: dict) -> ReplyKeyboardMarkup:
    return main_menu(user)


def _uid(m: Message) -> str:
    return str(m.from_user.id)


def _load_user(uid: str):
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    ensure_missions(user)
    return users, user


def _enter_secret_mode(users: dict, user: dict, uid: str) -> None:
    """Выставить MODE_SECRET и сохранить один раз (без гонки set_mode + stale save)."""
    user["mode"] = MODE_SECRET
    save_users(users, only=uid)


def _leave_to_menu(users: dict, user: dict, uid: str) -> None:
    user["mode"] = MODE_MENU
    save_users(users, only=uid)


@router.message(F.text == BTN_SECRET)
async def open_secret_hub(m: Message):
    uid = _uid(m)
    users, user = _load_user(uid)
    # если застряли на вводе промокода — сбросить, иначе секреты «ломаются»
    if (user.get("step") or "") in {"awaiting_promo_profile", "awaiting_promo"}:
        user["step"] = "ready"
        save_users(users, only=uid)

    if not has_secret_entry(user):
        await m.answer(
            "🔐 Пока секретов нет.\n"
            "Они открываются за серию дней — смотри <b>🔥 Серия дней</b> в профиле.",
            reply_markup=_menu_for(user),
            parse_mode="HTML",
        )
        return

    _enter_secret_mode(users, user, uid)
    active = get_active(user)
    if active:
        await _resume_active(m, user)
        return

    lines = [
        "🔐 <b>Секрет Рико</b>\n",
        "Эксклюзив за серию дней. Выбери задание:\n",
    ]
    for mid in inbox_missions(user):
        meta = MISSION_META[mid]
        lines.append(
            f"{meta['title']}\n"
            f"<i>{meta['blurb']}</i>\n"
            f"⏱ {meta['mins']}\n"
        )
    await m.answer("\n".join(lines), reply_markup=_hub_kb(user), parse_mode="HTML")


async def _resume_active(m: Message, user: dict):
    active = get_active(user) or {}
    if active.get("type") == MISSION_WEEK:
        await _send_week_card(m, user)
    elif active.get("type") == MISSION_VOICE:
        await _send_voice_prompt(m, user)


@router.message(ModeFilter(MODE_SECRET), F.text == BTN_SECRET_WEEK)
async def start_week(m: Message):
    uid = _uid(m)
    users, user = _load_user(uid)
    from services.tg_out import status

    async with status(m, "🦜 Рико готовит разбор…"):
        active = await asyncio.to_thread(start_mission, user, MISSION_WEEK)
        save_users(users, only=uid)
    if not active:
        await m.answer("Это задание уже недоступно.", reply_markup=_hub_kb(user))
        return
    intro = mission_intro(MISSION_WEEK)
    if intro:
        await m.answer(intro, parse_mode="HTML")
    await _send_week_card(m, user)


@router.message(ModeFilter(MODE_SECRET), F.text == BTN_SECRET_VOICE)
async def start_voice(m: Message):
    uid = _uid(m)
    users, user = _load_user(uid)
    from services.tg_out import status

    async with status(m, "🦜 Рико готовит фразы…"):
        active = await asyncio.to_thread(start_mission, user, MISSION_VOICE)
        save_users(users, only=uid)
    if not active:
        await m.answer("Это задание уже недоступно.", reply_markup=_hub_kb(user))
        return
    intro = mission_intro(MISSION_VOICE)
    if intro:
        await m.answer(intro, parse_mode="HTML")
    await _send_voice_prompt(m, user)


async def _finish_and_menu(m: Message, uid: str) -> None:
    users, user = _load_user(uid)
    msg = complete_mission(user)
    _leave_to_menu(users, user, uid)
    await m.answer(msg, reply_markup=_menu_for(user), parse_mode="HTML")


async def _send_week_card(m: Message, user: dict):
    uid = _uid(m)
    active = get_active(user) or {}
    cards = active.get("cards") or []
    step = int(active.get("step") or 0)
    if step >= len(cards):
        await _finish_and_menu(m, uid)
        return
    card = cards[step]
    await m.answer(
        format_card(step + 1, len(cards), card),
        reply_markup=_hub_kb(user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_SECRET), F.text == BTN_NEXT)
async def week_next(m: Message):
    uid = _uid(m)
    users, user = _load_user(uid)
    active = get_active(user)
    if not active or active.get("type") != MISSION_WEEK:
        await m.answer("Выбери задание ниже.", reply_markup=_hub_kb(user))
        return
    active["step"] = int(active.get("step") or 0) + 1
    ensure_missions(user)["active"] = active
    save_users(users, only=uid)
    await _send_week_card(m, user)


async def _send_voice_prompt(m: Message, user: dict):
    uid = _uid(m)
    active = get_active(user) or {}
    phrases = active.get("phrases") or []
    step = int(active.get("step") or 0)
    if step >= len(phrases):
        await _finish_and_menu(m, uid)
        return
    item = phrases[step]
    phrase = phrase_text(item)
    voice_label = ""
    voice_id = None
    if isinstance(item, dict):
        voice_label = (item.get("voice_label") or "").strip()
        voice_id = (item.get("voice_id") or "").strip() or None
    accent_line = f"🎙 Акцент: <b>{voice_label}</b>\n\n" if voice_label else ""
    await m.answer(
        f"🗣 <b>Фраза {step + 1}/{len(phrases)}</b>\n\n"
        f"{accent_line}"
        f"<b>{phrase}</b>\n\n"
        "Скажи её <b>голосом</b> (или напиши текстом). "
        "Можно «Пропустить фразу».",
        reply_markup=_hub_kb(user),
        parse_mode="HTML",
    )
    await send_voice_reply(
        m, phrase, title="Voice day", voice_id=voice_id
    )


@router.message(ModeFilter(MODE_SECRET), F.text == BTN_SECRET_SKIP)
async def voice_skip(m: Message):
    uid = _uid(m)
    users, user = _load_user(uid)
    active = get_active(user)
    if not active or active.get("type") != MISSION_VOICE:
        return
    active["step"] = int(active.get("step") or 0) + 1
    ensure_missions(user)["active"] = active
    save_users(users, only=uid)
    await _send_voice_prompt(m, user)


@router.message(ModeFilter(MODE_SECRET), F.text.in_({BTN_EXIT_SECRET, BTN_BACK_MENU}))
async def exit_secret(m: Message):
    uid = _uid(m)
    users, user = _load_user(uid)
    # не сбрасываем inbox — можно продолжить; active сохраняем
    _leave_to_menu(users, user, uid)
    await m.answer(
        "Ок! Секрет ждёт в меню — кнопка <b>🔐 Секрет Рико</b>.",
        reply_markup=_menu_for(user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_SECRET), F.voice)
async def voice_secret(m: Message, bot: Bot):
    uid = _uid(m)
    users, user = _load_user(uid)
    active = get_active(user)
    if not active or active.get("type") != MISSION_VOICE:
        await m.answer("Сейчас голосовое здесь не нужно.", reply_markup=_hub_kb(user))
        return

    phrases = active.get("phrases") or []
    step = int(active.get("step") or 0)
    if step >= len(phrases):
        return
    target = phrase_text(phrases[step])

    await m.answer("🎧 Слушаю…", reply_markup=_hub_kb(user))
    try:
        file = await bot.get_file(m.voice.file_id)
        buf = await bot.download_file(file.file_path)
        heard = recognize_english(buf.read(), hint=target) or ""
    except Exception:
        heard = ""

    if not heard:
        await m.answer(
            "Не разобрал речь — попробуй ещё раз или напиши текстом.",
            reply_markup=_hub_kb(user),
        )
        return

    result = evaluate_voice_attempt(target, heard)
    notes = list(active.get("notes") or [])
    notes.append({"target": target, "heard": heard, **result})
    active["notes"] = notes
    active["step"] = step + 1
    ensure_missions(user)["active"] = active
    save_users(users, only=uid)

    tip = result.get("tip_ru") or ""
    better = result.get("better") or target
    await m.answer(
        f"Услышал: <i>{heard}</i>\n"
        f"Цель: <b>{target}</b>\n"
        f"Естественнее: <b>{better}</b>\n"
        f"{('💡 ' + tip) if tip else ''}",
        reply_markup=_hub_kb(user),
        parse_mode="HTML",
    )
    await _send_voice_prompt(m, user)


@router.message(ModeFilter(MODE_SECRET), F.text)
async def secret_text(m: Message):
    text = (m.text or "").strip()
    if text in {
        BTN_SECRET,
        BTN_SECRET_WEEK,
        BTN_SECRET_VOICE,
        BTN_SECRET_SKIP,
        BTN_SECRET_DONE,
        BTN_NEXT,
        BTN_EXIT_SECRET,
        BTN_BACK_MENU,
    }:
        return

    uid = _uid(m)
    users, user = _load_user(uid)
    active = get_active(user)
    if not active:
        await m.answer("Выбери задание кнопкой.", reply_markup=_hub_kb(user))
        return

    if active.get("type") == MISSION_VOICE:
        phrases = active.get("phrases") or []
        step = int(active.get("step") or 0)
        if step >= len(phrases):
            return
        target = phrase_text(phrases[step])
        result = evaluate_voice_attempt(target, text)
        notes = list(active.get("notes") or [])
        notes.append({"target": target, "heard": text, **result})
        active["notes"] = notes
        active["step"] = step + 1
        ensure_missions(user)["active"] = active
        save_users(users, only=uid)
        tip = result.get("tip_ru") or ""
        better = result.get("better") or target
        await m.answer(
            f"Ты написал: <i>{text}</i>\n"
            f"Цель: <b>{target}</b>\n"
            f"Естественнее: <b>{better}</b>\n"
            f"{('💡 ' + tip) if tip else ''}",
            reply_markup=_hub_kb(user),
            parse_mode="HTML",
        )
        await _send_voice_prompt(m, user)
        return

    await m.answer("Жми «Далее» для следующей карточки.", reply_markup=_hub_kb(user))
