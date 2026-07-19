"""
Раздел «Общаться».
Кнопка «Перевести» ловится по слову Перевести (на случай разного эмодзи).
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.filters import ModeFilter
from handlers.keyboards import chat_menu
from services.database import (
    load_users,
    get_user,
    save_users,
    MODE_CHAT,
)
from services.translation import translate_to_russian
from services.tutor_reply import reply_as_tutor
from services.voices import (
    BTN_CHAT_VOICE,
    CHAT_VOICES,
    VOICE_PREVIEW_PHRASE,
    set_chat_voice,
    voice_by_key,
    voices_help_text,
)

router = Router()


def _voices_inline_kb() -> InlineKeyboardMarkup:
    """У каждого голоса: прослушать (всем) + выбрать (по тарифу)."""
    rows = []
    for v in CHAT_VOICES:
        need = "399" if v["min_plan"] == "chat" else "799"
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"🎧 {v['label']}",
                    callback_data=f"vlisten:{v['key']}",
                ),
                InlineKeyboardButton(
                    text=f"✅ Выбрать ({need})",
                    callback_data=f"vset:{v['key']}",
                ),
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)


@router.message(ModeFilter(MODE_CHAT), F.text == BTN_CHAT_VOICE)
async def chat_voice_picker(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.reply(
        voices_help_text(user),
        reply_markup=chat_menu(),
        parse_mode="HTML",
    )
    await m.reply(
        f"Фраза для прослушивания:\n<i>«{VOICE_PREVIEW_PHRASE}»</i>",
        reply_markup=_voices_inline_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("vlisten:"))
async def chat_voice_listen(c: CallbackQuery):
    """Превью голоса — не считает в лимит чата."""
    key = (c.data or "").split(":", 1)[-1].strip()
    v = voice_by_key(key)
    if not v:
        await c.answer("Голос не найден", show_alert=True)
        return
    await c.answer(f"Озвучиваю: {v['label']}")
    from services.elevenlabs import send_voice_reply

    await c.message.answer(f"🎧 <b>{v['label']}</b>", parse_mode="HTML")
    await send_voice_reply(
        c.message,
        VOICE_PREVIEW_PHRASE,
        title=v["label"],
        voice_id=v["voice_id"],
    )


@router.callback_query(F.data.startswith("vset:"))
async def chat_voice_pick(c: CallbackQuery):
    key = (c.data or "").split(":", 1)[-1].strip()
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    ok, msg = set_chat_voice(user, key)
    if ok:
        save_users(users, only=str(c.from_user.id))
    await c.answer("Готово" if ok else "Нужен тариф", show_alert=not ok)
    await c.message.answer(msg, reply_markup=chat_menu(), parse_mode="HTML")
    if not ok:
        from handlers.lesson_keyboards import tariffs_inline_kb

        await c.message.answer("Тарифы:", reply_markup=tariffs_inline_kb(user))


@router.callback_query(F.data.startswith("voice:"))
async def chat_voice_pick_legacy(c: CallbackQuery):
    """Старые кнопки voice:key → выбор голоса."""
    key = (c.data or "").split(":", 1)[-1].strip()
    users = load_users()
    user = get_user(users, str(c.from_user.id))
    ok, msg = set_chat_voice(user, key)
    if ok:
        save_users(users, only=str(c.from_user.id))
    await c.answer("Готово" if ok else "Нужен тариф", show_alert=not ok)
    await c.message.answer(msg, reply_markup=chat_menu(), parse_mode="HTML")


@router.message(ModeFilter(MODE_CHAT), F.text.func(lambda t: bool(t) and "Перевести" in t))
async def translate_last(m: Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    last = user.get("last_bot_reply")

    if not last:
        await m.reply(
            "❌ Пока нет текста для перевода. Сначала напиши или пришли голосовое.",
            reply_markup=chat_menu(),
        )
        return

    await m.reply("🌐 Перевожу…")
    translation = translate_to_russian(last)
    if translation:
        await m.reply(
            f"🌐 <b>Перевод:</b>\n{_esc_html(translation)}",
            reply_markup=chat_menu(),
            parse_mode="HTML",
        )
    else:
        await m.reply("Не получилось перевести 🙈 Попробуй ещё раз.", reply_markup=chat_menu())


def _esc_html(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


@router.message(
    ModeFilter(MODE_CHAT),
    F.text,
    ~F.text.func(
        lambda t: bool(t)
        and (
            "Перевести" in t
            or "Вернуться в меню" in t
            or t == "🚀 Начать сегодня"
            or t == BTN_CHAT_VOICE
        )
    ),
)
async def chat_text(m: Message):
    text = (m.text or "").strip()
    if not text or text.startswith("/"):
        return

    from services.growth import note_chat_message, ensure_growth
    from aiogram.dispatcher.event.bases import SkipHandler
    from handlers.keyboards import BTN_START_TODAY

    if text == BTN_START_TODAY:
        raise SkipHandler

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    ok, tip = note_chat_message(user)
    save_users(users, only=str(m.from_user.id))
    if not ok:
        from handlers.lesson_keyboards import chat_limit_inline_kb

        await m.reply(
            tip or "Мы здорово поболтали!",
            reply_markup=chat_menu(),
            parse_mode="HTML",
        )
        await m.reply("👇", reply_markup=chat_limit_inline_kb())
        return

    await m.reply("✨ …")
    await reply_as_tutor(m, user_text=text)


@router.message(ModeFilter(MODE_CHAT))
async def chat_wrong_content(m: Message):
    if m.voice:
        return
    await m.reply(
        "🙂 В этом разделе пришли текст или голосовое на английском.",
        reply_markup=chat_menu(),
    )
