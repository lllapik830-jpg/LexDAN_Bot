"""🔥 Огонь дня — хаб в главном меню."""

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from handlers.filters import ModeFilter
from handlers.keyboards import main_menu
from services.database import (
    MODE_DAILY_FIRE,
    MODE_MENU,
    users_for,
    get_user,
    save_users,
    set_mode,
)
from services.growth import ensure_growth, note_lesson_activity
from services.daily_fire import (
    BTN_DAILY_FIRE,
    BTN_DF_WORD,
    BTN_DF_PHRASE,
    BTN_DF_VOICE,
    BTN_DF_FACT,
    BTN_DF_BACK,
    BTN_TO_KIND,
    ensure_daily_fire,
    is_opened,
    mark_opened,
    hub_intro,
    get_or_create_content,
    format_word_or_phrase,
    format_voice,
    format_fact,
    tts_text_for,
)
from services.elevenlabs import send_voice_reply
from services.voices import RICO_VOICE_ID

router = Router()

BTN_BACK_MENU = "🔙 Вернуться в меню"


def daily_fire_kb(user: dict) -> ReplyKeyboardMarkup:
    ensure_daily_fire(user)

    def mark(btn: str, kind: str) -> str:
        return f"✅ {btn}" if is_opened(user, kind) else btn

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=mark(BTN_DF_WORD, "word")), KeyboardButton(text=mark(BTN_DF_PHRASE, "phrase"))],
            [KeyboardButton(text=mark(BTN_DF_VOICE, "voice")), KeyboardButton(text=mark(BTN_DF_FACT, "fact"))],
            [KeyboardButton(text=BTN_BACK_MENU)],
        ],
        resize_keyboard=True,
    )


def _kind_from_text(text: str) -> str | None:
    t = (text or "").strip()
    if t.startswith("✅ "):
        t = t[2:].strip()
    return BTN_TO_KIND.get(t)


def _uid(m: Message) -> str:
    return str(m.from_user.id)


@router.message(F.text == BTN_DAILY_FIRE)
async def open_daily_fire(m: Message):
    uid = _uid(m)
    set_mode(uid, MODE_DAILY_FIRE)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    note_lesson_activity(user)
    ensure_daily_fire(user)
    save_users(users, only=uid)
    await m.answer(hub_intro(user), reply_markup=daily_fire_kb(user), parse_mode="HTML")


@router.message(ModeFilter(MODE_DAILY_FIRE), F.text == BTN_DF_BACK)
async def back_to_fire_hub(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    await m.answer(hub_intro(user), reply_markup=daily_fire_kb(user), parse_mode="HTML")


@router.message(ModeFilter(MODE_DAILY_FIRE), F.text == BTN_BACK_MENU)
async def leave_daily_fire(m: Message):
    uid = _uid(m)
    set_mode(uid, MODE_MENU)
    users = users_for(uid)
    user = get_user(users, uid)
    await m.answer("Главное меню:", reply_markup=main_menu(user))


@router.message(ModeFilter(MODE_DAILY_FIRE))
async def daily_fire_item(m: Message):
    if not m.text or m.text.startswith("/"):
        return
    kind = _kind_from_text(m.text)
    if not kind:
        uid = _uid(m)
        users = users_for(uid)
        user = get_user(users, uid)
        await m.answer(
            "Выбери одну из четырёх кнопок огня дня 👇",
            reply_markup=daily_fire_kb(user),
        )
        return

    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    note_lesson_activity(user)
    first_open = not is_opened(user, kind)

    await m.answer("🦜 Рико колдует контент… секунду ✨", parse_mode="HTML")

    data = get_or_create_content(user, kind)
    if first_open:
        mark_opened(user, kind)
    save_users(users, only=uid)

    if kind in {"word", "phrase"}:
        text = format_word_or_phrase(kind, data, first_open=first_open)
    elif kind == "voice":
        text = format_voice(data, first_open=first_open)
    else:
        text = format_fact(data, first_open=first_open)

    # Голос дня: сначала голосовое, потом текст с блюром
    tts = tts_text_for(kind, data)
    if kind == "voice" and tts:
        await send_voice_reply(m, tts, title="Огонь дня", voice_id=RICO_VOICE_ID)
        await m.answer(text, reply_markup=daily_fire_kb(user), parse_mode="HTML")
        return

    await m.answer(text, reply_markup=daily_fire_kb(user), parse_mode="HTML")
    if tts:
        await send_voice_reply(m, tts, title="Огонь дня", voice_id=RICO_VOICE_ID)
        if kind == "fact":
            # факт: текст уже есть, голос дублирует; перевод под блюром в том же сообщении
            pass
