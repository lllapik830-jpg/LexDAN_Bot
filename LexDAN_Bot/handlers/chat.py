"""
Раздел «Общаться».
Кнопка «Перевести» ловится по слову Перевести (на случай разного эмодзи).
"""

from aiogram import Router, F
from aiogram.types import Message

from handlers.filters import ModeFilter
from handlers.keyboards import chat_menu
from services.database import (
    load_users,
    get_user,
    MODE_CHAT,
)
from services.translation import translate_to_russian
from services.tutor_reply import reply_as_tutor

router = Router()


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
    ~F.text.func(lambda t: bool(t) and ("Перевести" in t or "Вернуться в меню" in t)),
)
async def chat_text(m: Message):
    text = (m.text or "").strip()
    if not text or text.startswith("/"):
        return

    from services.database import save_users
    from services.growth import note_chat_message, ensure_growth

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    ok, tip = note_chat_message(user)
    save_users(users)
    if not ok:
        await m.reply(tip or "Лимит на сегодня.", reply_markup=chat_menu(), parse_mode="HTML")
        return
    if tip:
        await m.reply(tip, parse_mode="HTML")

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
