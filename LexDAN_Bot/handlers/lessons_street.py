"""Живая речь — слайды без засорения чата. Только MANAGER_ID."""

from __future__ import annotations

import asyncio
import random

from aiogram import F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from data.street_talk import (
    BTN_BACK_PACKS,
    BTN_BACK_SECTIONS,
    BTN_NEXT,
    BTN_PREV,
    BTN_REMIND,
    BTN_SKIP_SPEAK,
    BTN_STREET,
    format_item_html,
    format_produce_html,
    format_remind_html,
    pack_button_label,
    pack_by_button_label,
    section_intro_html,
)
from handlers.filters import ModeFilter
from handlers.lesson_filters import LessonHubFilter
from handlers.lesson_keyboards import level_sections_kb
from services.database import MODE_LESSONS, get_user, load_users
from services.lesson_state import assessment_busy, ensure_lesson, set_level_hub
from services.street_talk import (
    bump_attempt,
    check_item_speak,
    check_produce,
    clear_session,
    current_pack,
    current_slide,
    ensure_street,
    get_session,
    go_next,
    go_prev,
    is_pack_done,
    packs_for_list,
    reset_attempts,
    set_street_list,
    start_pack,
    street_talk_allowed,
    update_session,
)
from services.tg_out import try_delete, try_delete_user_tap

router = Router()

_SKIP_SPEAK = {
    BTN_SKIP_SPEAK,
    "⏭ Пропустить произношение",
    "⏭️ Пропустить произношение",
    "Пропустить произношение",
}

_NAV = {
    BTN_STREET,
    "💬 Живая речь",
    BTN_NEXT,
    BTN_PREV,
    BTN_BACK_PACKS,
    BTN_BACK_SECTIONS,
    BTN_REMIND,
    *_SKIP_SPEAK,
    "🔙 Вернуться в меню",
}

_SLIDE_HUBS = ("street_slide", "street_card", "street_task")

_PRAISE = (
    "живьём 🔥",
    "звучит native 🤙",
    "вот это вайб ✨",
    "чисто 😎",
    "как в сериале 🎬",
    "топ 🧃",
    "есть контакт ✌️",
    "без учебника 💪",
    "вау, рот работает 🦜",
    "держишь вайб 🧃",
)


def _lesson_level(user: dict) -> str:
    return (user.get("lesson") or {}).get("level") or user.get("level") or "A1"


def _packs_kb(user: dict) -> ReplyKeyboardMarkup:
    level = _lesson_level(user)
    rows = []
    row: list[KeyboardButton] = []
    for p in packs_for_list(level):
        row.append(KeyboardButton(text=pack_button_label(p, done=is_pack_done(user, p["id"]))))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text=BTN_BACK_SECTIONS)])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _intro_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_NEXT)],
            [KeyboardButton(text=BTN_BACK_PACKS)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def _item_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_SKIP_SPEAK)],
            [KeyboardButton(text=BTN_PREV), KeyboardButton(text=BTN_NEXT)],
            [KeyboardButton(text=BTN_BACK_PACKS)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def _produce_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_REMIND)],
            [KeyboardButton(text=BTN_SKIP_SPEAK)],
            [KeyboardButton(text=BTN_PREV), KeyboardButton(text=BTN_NEXT)],
            [KeyboardButton(text=BTN_BACK_PACKS)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def _kb_for_slide(slide: dict) -> ReplyKeyboardMarkup:
    kind = slide.get("kind")
    if kind == "intro":
        return _intro_kb()
    if kind == "produce":
        return _produce_kb()
    return _item_kb()


async def _del(m: Message, mid) -> None:
    if not mid:
        return
    try:
        await try_delete(m.bot, m.chat.id, int(mid))
    except Exception:
        pass


async def _wipe_slide_msgs(m: Message, uid: str, *, keep_card: bool = False) -> None:
    s = get_session(get_user(load_users(), uid)) or {}
    await _del(m, s.get("voice_msg_id"))
    await _del(m, s.get("heard_msg_id"))
    await _del(m, s.get("remind_msg_id"))
    if not keep_card:
        await _del(m, s.get("card_msg_id"))
        update_session(
            uid,
            voice_msg_id=None,
            heard_msg_id=None,
            remind_msg_id=None,
            card_msg_id=None,
        )
    else:
        update_session(uid, voice_msg_id=None, heard_msg_id=None, remind_msg_id=None)


async def _goto_sections(m: Message) -> None:
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    level = _lesson_level(user)
    await _wipe_slide_msgs(m, uid)
    await try_delete_user_tap(m)
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
    level = _lesson_level(user)
    await _wipe_slide_msgs(m, uid)
    await try_delete_user_tap(m)
    clear_session(uid)
    set_street_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    await m.answer(
        section_intro_html(level),
        reply_markup=_packs_kb(user),
        parse_mode="HTML",
    )


async def _present_slide(m: Message, user: dict) -> None:
    from services.elevenlabs import send_rico_voice

    uid = str(m.from_user.id)
    pack = current_pack(user) or {}
    title = pack.get("title_ru") or "Живая речь"
    slide = current_slide(user)
    kind = slide.get("kind")
    if kind == "done":
        await _finish_pack(m, user, pack)
        return

    await _wipe_slide_msgs(m, uid)

    html = ""
    kb = _kb_for_slide(slide)
    voice_en = ""
    if kind == "intro":
        html = pack.get("intro_html") or "Поехали."
    elif kind == "item":
        item = slide["item"]
        html = format_item_html(title, slide["n"], slide["total"], item)
        voice_en = (item.get("voice_en") or item.get("example") or "").strip()
    elif kind == "produce":
        html = format_produce_html(title, slide["n"], slide["total"], slide["task"])
    else:
        await _goto_packs(m)
        return

    card = await m.answer(html, reply_markup=kb, parse_mode="HTML")
    voice_id = None
    if voice_en:
        sent = await send_rico_voice(m, voice_en, user=user, title="Живая речь")
        if sent is not False and sent is not None and getattr(sent, "message_id", None):
            voice_id = sent.message_id
        elif not sent:
            fallback = await m.answer(f"🔊 <i>{voice_en}</i>", parse_mode="HTML")
            voice_id = fallback.message_id if fallback else None
    update_session(
        uid,
        card_msg_id=card.message_id if card else None,
        voice_msg_id=voice_id,
        heard_msg_id=None,
        remind_msg_id=None,
    )


async def _finish_pack(m: Message, user: dict, pack: dict) -> None:
    uid = str(m.from_user.id)
    level = _lesson_level(user)
    await _wipe_slide_msgs(m, uid)
    set_street_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    text = pack.get("done_html") or f"🏁 {pack.get('title_ru') or 'Пак'} пройден."
    await m.answer(text, reply_markup=_packs_kb(user), parse_mode="HTML")


async def _advance(m: Message, *, flash: Message | None = None) -> None:
    uid = str(m.from_user.id)
    if flash:
        await asyncio.sleep(3)
        await _del(m, flash.message_id)
        update_session(uid, heard_msg_id=None)
    users = load_users()
    user = get_user(users, uid)
    pack = current_pack(user) or {}
    reset_attempts(uid)
    nxt = go_next(uid)
    users = load_users()
    user = get_user(users, uid)
    if nxt is None:
        await _finish_pack(m, user, pack)
        return
    await _present_slide(m, user)


async def open_street_for_level(m: Message, user: dict, level: str) -> None:
    uid = str(m.from_user.id)
    if not street_talk_allowed(uid):
        return
    ensure_street(user)
    set_street_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    await m.answer(
        section_intro_html(level),
        reply_markup=_packs_kb(user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text.in_({BTN_STREET, "💬 Живая речь"}))
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
    level = _lesson_level(user)
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
    pack = pack_by_button_label(text, level=_lesson_level(user))
    if not pack:
        await m.answer("Выбери пак кнопкой ниже 🤙", reply_markup=_packs_kb(user))
        return
    await try_delete_user_tap(m)
    start_pack(str(m.from_user.id), pack["id"])
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await _present_slide(m, user)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.text == BTN_BACK_PACKS)
async def street_back_packs(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    await _goto_packs(m)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.text == BTN_BACK_SECTIONS)
async def street_slide_back_sections(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    await _goto_sections(m)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.text == BTN_NEXT)
async def street_next(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    await try_delete_user_tap(m)
    await _advance(m)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.text == BTN_PREV)
async def street_prev(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    uid = str(m.from_user.id)
    await try_delete_user_tap(m)
    where = go_prev(uid)
    if where == "intro_back":
        await _goto_packs(m)
        return
    users = load_users()
    user = get_user(users, uid)
    await _present_slide(m, user)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.text == BTN_REMIND)
async def street_remind(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    slide = current_slide(user)
    if slide.get("kind") != "produce":
        await m.answer("Напоминалка — на заданиях со своей фразой.", reply_markup=_kb_for_slide(slide))
        return
    s = get_session(user) or {}
    await _del(m, s.get("remind_msg_id"))
    await try_delete_user_tap(m)
    sent = await m.answer(format_remind_html(slide["task"]), parse_mode="HTML")
    update_session(uid, remind_msg_id=sent.message_id if sent else None)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.text.in_(_SKIP_SPEAK))
async def street_skip_speak(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    await try_delete_user_tap(m)
    await _advance(m)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.voice)
async def street_voice_answer(m: Message):
    if not street_talk_allowed(m.from_user.id):
        raise SkipHandler
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    slide = current_slide(user)
    kind = slide.get("kind")
    if kind == "intro":
        await m.answer("Сначала жми Далее — там будет что повторять.", reply_markup=_intro_kb())
        return
    if kind not in {"item", "produce"}:
        raise SkipHandler

    from services.stt import recognize_english

    uid = str(m.from_user.id)
    hint = ""
    if kind == "item":
        hint = (slide["item"].get("example") or slide["item"].get("form") or "").strip()
    else:
        must = slide["task"].get("must") or []
        hint = str(must[0]) if must else ""
    try:
        file = await m.bot.get_file(m.voice.file_id)
        voice_buffer = await m.bot.download_file(file.file_path)
        heard = (recognize_english(voice_buffer.read(), hint=hint) or "").strip()
    except Exception:
        heard = ""

    ok = False
    if heard:
        if kind == "item":
            ok = check_item_speak(slide["item"], heard)
        else:
            ok = check_produce(slide["task"], heard)

    if ok:
        praise = random.choice(_PRAISE)
        flash = await m.answer(
            f"✅ Услышал: <i>{heard}</i> — {praise}",
            parse_mode="HTML",
        )
        update_session(uid, heard_msg_id=flash.message_id if flash else None)
        try:
            await m.delete()
        except Exception:
            pass
        await _advance(m, flash=flash)
        return

    attempts = bump_attempt(uid)
    shown = heard or "…"
    kb = _kb_for_slide(slide)
    if attempts >= 2:
        flash = await m.answer(
            f"Услышал: <i>{shown}</i>\nИдём дальше 🦜",
            parse_mode="HTML",
        )
        update_session(uid, heard_msg_id=flash.message_id if flash else None)
        await _advance(m, flash=flash)
        return
    tip = "Попробуй ещё раз повторить пример." if kind == "item" else "Скажи ещё раз — и вставь конструкцию в фразу."
    await m.answer(
        f"Услышал: <i>{shown}</i>\n{tip}",
        parse_mode="HTML",
        reply_markup=kb,
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.text)
async def street_slide_text(m: Message):
    text = (m.text or "").strip()
    if text in _NAV:
        return
    if not street_talk_allowed(m.from_user.id):
        return
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    slide = current_slide(user)
    await m.answer(
        "Тут голос, не набор 🎤\nПришли голосовое — или Далее / Пропустить.",
        reply_markup=_kb_for_slide(slide),
    )
