"""Секретные задания Рико — вход из главного меню."""

from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from handlers.filters import ModeFilter
from handlers.keyboards import main_menu
from services.database import (
    MODE_SECRET,
    MODE_MENU,
    load_users,
    get_user,
    save_users,
    set_mode,
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
    clear_active,
    complete_mission,
    format_card,
    evaluate_voice_attempt,
)
from services.elevenlabs import send_voice_reply
from services.stt import recognize_english

router = Router()


def _hub_kb(user: dict) -> ReplyKeyboardMarkup:
    rows = []
    inbox = inbox_missions(user)
    active = get_active(user)
    if active:
        if active.get("type") == MISSION_WEEK:
            rows.append([KeyboardButton(text="➡️ Далее")])
        else:
            rows.append([KeyboardButton(text=BTN_SECRET_SKIP)])
        rows.append([KeyboardButton(text="🚪 Выйти из секрета")])
    else:
        if MISSION_WEEK in inbox:
            rows.append([KeyboardButton(text=BTN_SECRET_WEEK)])
        if MISSION_VOICE in inbox:
            rows.append([KeyboardButton(text=BTN_SECRET_VOICE)])
        rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _menu_for(user: dict) -> ReplyKeyboardMarkup:
    return main_menu(user)


@router.message(F.text == BTN_SECRET)
async def open_secret_hub(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    ensure_missions(user)
    if not has_secret_entry(user):
        await m.reply(
            "🔐 Пока секретов нет.\n"
            "Они открываются за серию дней — смотри <b>🔥 Серия дней</b> в профиле.",
            reply_markup=_menu_for(user),
            parse_mode="HTML",
        )
        return

    set_mode(str(m.from_user.id), MODE_SECRET)
    save_users(users)
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
    await m.reply("\n".join(lines), reply_markup=_hub_kb(user), parse_mode="HTML")


async def _resume_active(m: Message, user: dict):
    active = get_active(user) or {}
    if active.get("type") == MISSION_WEEK:
        await _send_week_card(m, user)
    elif active.get("type") == MISSION_VOICE:
        await _send_voice_prompt(m, user)


@router.message(ModeFilter(MODE_SECRET), F.text == BTN_SECRET_WEEK)
async def start_week(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.reply("🦜 Рико готовит разбор…")
    active = start_mission(user, MISSION_WEEK)
    save_users(users)
    if not active:
        await m.reply("Это задание уже недоступно.", reply_markup=_hub_kb(user))
        return
    await _send_week_card(m, user)


@router.message(ModeFilter(MODE_SECRET), F.text == BTN_SECRET_VOICE)
async def start_voice(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.reply("🦜 Рико готовит фразы…")
    active = start_mission(user, MISSION_VOICE)
    save_users(users)
    if not active:
        await m.reply("Это задание уже недоступно.", reply_markup=_hub_kb(user))
        return
    await _send_voice_prompt(m, user)


async def _send_week_card(m: Message, user: dict):
    active = get_active(user) or {}
    cards = active.get("cards") or []
    step = int(active.get("step") or 0)
    if step >= len(cards):
        users = load_users()
        user = get_user(users, str(m.from_user.id))
        msg = complete_mission(user)
        save_users(users)
        set_mode(str(m.from_user.id), MODE_MENU)
        await m.reply(msg, reply_markup=_menu_for(user), parse_mode="HTML")
        return
    card = cards[step]
    await m.reply(
        format_card(step + 1, len(cards), card),
        reply_markup=_hub_kb(user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_SECRET), F.text == "➡️ Далее")
async def week_next(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    active = get_active(user)
    if not active or active.get("type") != MISSION_WEEK:
        await m.reply("Выбери задание ниже.", reply_markup=_hub_kb(user))
        return
    active["step"] = int(active.get("step") or 0) + 1
    ensure_missions(user)["active"] = active
    save_users(users)
    await _send_week_card(m, user)


async def _send_voice_prompt(m: Message, user: dict):
    active = get_active(user) or {}
    phrases = active.get("phrases") or []
    step = int(active.get("step") or 0)
    if step >= len(phrases):
        users = load_users()
        user = get_user(users, str(m.from_user.id))
        msg = complete_mission(user)
        save_users(users)
        set_mode(str(m.from_user.id), MODE_MENU)
        await m.reply(msg, reply_markup=_menu_for(user), parse_mode="HTML")
        return
    phrase = phrases[step]
    await m.reply(
        f"🗣 <b>Фраза {step + 1}/{len(phrases)}</b>\n\n"
        f"<b>{phrase}</b>\n\n"
        "Скажи её <b>голосом</b> (или напиши текстом). "
        "Можно «Пропустить фразу».",
        reply_markup=_hub_kb(user),
        parse_mode="HTML",
    )
    await send_voice_reply(m, phrase, title="Rico phrase")


@router.message(ModeFilter(MODE_SECRET), F.text == BTN_SECRET_SKIP)
async def voice_skip(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    active = get_active(user)
    if not active or active.get("type") != MISSION_VOICE:
        return
    active["step"] = int(active.get("step") or 0) + 1
    ensure_missions(user)["active"] = active
    save_users(users)
    await _send_voice_prompt(m, user)


@router.message(ModeFilter(MODE_SECRET), F.text == "🚪 Выйти из секрета")
async def exit_secret(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    # не сбрасываем inbox — можно продолжить; active сохраняем
    set_mode(str(m.from_user.id), MODE_MENU)
    save_users(users)
    await m.reply(
        "Ок! Секрет ждёт в меню — кнопка <b>🔐 Секрет Рико</b>.",
        reply_markup=_menu_for(user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_SECRET), F.voice)
async def voice_secret(m: Message, bot: Bot):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    active = get_active(user)
    if not active or active.get("type") != MISSION_VOICE:
        await m.reply("Сейчас голосовое здесь не нужно.", reply_markup=_hub_kb(user))
        return

    phrases = active.get("phrases") or []
    step = int(active.get("step") or 0)
    if step >= len(phrases):
        return
    target = phrases[step]

    await m.reply("🎧 Слушаю…", reply_markup=_hub_kb(user))
    try:
        file = await bot.get_file(m.voice.file_id)
        buf = await bot.download_file(file.file_path)
        heard = recognize_english(buf.read()) or ""
    except Exception:
        heard = ""

    if not heard:
        await m.reply(
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
    save_users(users)

    tip = result.get("tip_ru") or ""
    better = result.get("better") or target
    await m.reply(
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
        "➡️ Далее",
        "🚪 Выйти из секрета",
        "🔙 Вернуться в меню",
    }:
        return

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    active = get_active(user)
    if not active:
        await m.reply("Выбери задание кнопкой.", reply_markup=_hub_kb(user))
        return

    if active.get("type") == MISSION_VOICE:
        phrases = active.get("phrases") or []
        step = int(active.get("step") or 0)
        if step >= len(phrases):
            return
        target = phrases[step]
        result = evaluate_voice_attempt(target, text)
        notes = list(active.get("notes") or [])
        notes.append({"target": target, "heard": text, **result})
        active["notes"] = notes
        active["step"] = step + 1
        ensure_missions(user)["active"] = active
        save_users(users)
        tip = result.get("tip_ru") or ""
        better = result.get("better") or target
        await m.reply(
            f"Ты написал: <i>{text}</i>\n"
            f"Цель: <b>{target}</b>\n"
            f"Естественнее: <b>{better}</b>\n"
            f"{('💡 ' + tip) if tip else ''}",
            reply_markup=_hub_kb(user),
            parse_mode="HTML",
        )
        await _send_voice_prompt(m, user)
        return

    await m.reply("Жми «Далее» для следующей карточки.", reply_markup=_hub_kb(user))
