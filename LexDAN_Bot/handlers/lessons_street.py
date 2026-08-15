"""Живая речь — слайды + голос. Пока только MANAGER_ID."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from data.street_talk import (
    BTN_BACK_PACKS,
    BTN_BACK_SECTIONS,
    BTN_NEXT,
    BTN_PREV,
    BTN_REPLAY,
    BTN_SKIP_SPEAK,
    BTN_STREET,
    SECTION_INTRO_HTML,
    format_item_html,
    format_produce_html,
    pack_button_label,
    pack_by_button_label,
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
    go_next,
    go_prev,
    is_pack_done,
    packs_for_list,
    reset_attempts,
    set_street_list,
    start_pack,
    street_talk_allowed,
)

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
    BTN_REPLAY,
    *_SKIP_SPEAK,
    "🔙 Вернуться в меню",
}

_SLIDE_HUBS = ("street_slide", "street_card", "street_task")


def _packs_kb(user: dict) -> ReplyKeyboardMarkup:
    rows = []
    row: list[KeyboardButton] = []
    for p in packs_for_list():
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
            [KeyboardButton(text=BTN_REPLAY), KeyboardButton(text=BTN_NEXT)],
            [KeyboardButton(text=BTN_PREV), KeyboardButton(text=BTN_BACK_PACKS)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def _produce_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_SKIP_SPEAK)],
            [KeyboardButton(text=BTN_NEXT)],
            [KeyboardButton(text=BTN_PREV), KeyboardButton(text=BTN_BACK_PACKS)],
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


async def _present_slide(m: Message, user: dict) -> None:
    from services.elevenlabs import send_rico_voice

    pack = current_pack(user) or {}
    title = pack.get("title_ru") or "Живая речь"
    slide = current_slide(user)
    kind = slide.get("kind")
    if kind == "done":
        await _finish_pack(m, user, pack)
        return
    if kind == "intro":
        await m.answer(pack.get("intro_html") or "Поехали.", reply_markup=_intro_kb(), parse_mode="HTML")
        return
    if kind == "item":
        item = slide["item"]
        voice_en = (item.get("voice_en") or item.get("example") or "").strip()
        if voice_en:
            ok = await send_rico_voice(m, voice_en, user=user, title="Живая речь")
            if not ok:
                await m.answer(f"🔊 <i>{voice_en}</i>", parse_mode="HTML")
        html = format_item_html(title, slide["n"], slide["total"], item)
        await m.answer(html, reply_markup=_item_kb(), parse_mode="HTML")
        return
    if kind == "produce":
        html = format_produce_html(title, slide["n"], slide["total"], slide["task"])
        await m.answer(html, reply_markup=_produce_kb(), parse_mode="HTML")
        return
    await _goto_packs(m)


async def _finish_pack(m: Message, user: dict, pack: dict) -> None:
    uid = str(m.from_user.id)
    level = (user.get("lesson") or {}).get("level") or user.get("level") or "A1"
    set_street_list(uid, level)
    users = load_users()
    user = get_user(users, uid)
    text = pack.get("done_html") or f"🏁 {pack.get('title_ru') or 'Пак'} пройден."
    await m.answer(text, reply_markup=_packs_kb(user), parse_mode="HTML")


async def _advance(m: Message) -> None:
    uid = str(m.from_user.id)
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
        SECTION_INTRO_HTML,
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
        await m.answer("Выбери пак кнопкой ниже 🤙", reply_markup=_packs_kb(user))
        return
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
    await _advance(m)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.text == BTN_PREV)
async def street_prev(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    uid = str(m.from_user.id)
    where = go_prev(uid)
    if where == "intro_back":
        await _goto_packs(m)
        return
    users = load_users()
    user = get_user(users, uid)
    await _present_slide(m, user)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.text == BTN_REPLAY)
async def street_replay(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    slide = current_slide(user)
    if slide.get("kind") != "item":
        await m.answer("Тут нечего переслушивать — жми Далее.", reply_markup=_kb_for_slide(slide))
        return
    from services.elevenlabs import send_rico_voice

    item = slide["item"]
    voice_en = (item.get("voice_en") or item.get("example") or "").strip()
    if voice_en:
        await send_rico_voice(m, voice_en, user=user, title="Живая речь · повтор")
    await m.answer("Ещё раз. Повтори в микрофон 🎤", reply_markup=_item_kb())


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter(*_SLIDE_HUBS), F.text.in_(_SKIP_SPEAK))
async def street_skip_speak(m: Message):
    if not street_talk_allowed(m.from_user.id):
        return
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    slide = current_slide(user)
    if slide.get("kind") == "intro":
        await _advance(m)
        return
    await m.answer("Ок, пропускаем 🦜")
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
        await m.answer(f"✅ Услышал: <i>{heard}</i> — живьём 🔥", parse_mode="HTML")
        await _advance(m)
        return

    attempts = bump_attempt(uid)
    shown = heard or "…"
    kb = _kb_for_slide(slide)
    if attempts >= 2:
        await m.answer(
            f"Услышал: <i>{shown}</i>\n"
            "Идём дальше — ещё наговоримся на следующих слайдах 🦜",
            parse_mode="HTML",
        )
        await _advance(m)
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
