"""
Раздел «Общаться» — только текст (голос в voice.py).
Работает ТОЛЬКО когда mode == chat.
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


@router.message(ModeFilter(MODE_CHAT), F.text == "🌍 Перевести")
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

    translation = translate_to_russian(last)
    if translation:
        await m.reply(f"🌐 {translation}", reply_markup=chat_menu())
    else:
        await m.reply("❌ Не удалось перевести. Попробуй ещё раз.", reply_markup=chat_menu())


@router.message(
    ModeFilter(MODE_CHAT),
    F.text,
    ~F.text.in_({"🌍 Перевести", "🔙 Вернуться в меню"}),
)
async def chat_text(m: Message):
    text = (m.text or "").strip()
    if not text or text.startswith("/"):
        return

    await m.reply("💭 Думаю…")
    await reply_as_tutor(m, user_text=text)


@router.message(ModeFilter(MODE_CHAT))
async def chat_wrong_content(m: Message):
    """Стикеры, фото и т.п. в разделе общения."""
    if m.voice:
        return  # голос обработает voice.py
    await m.reply(
        "🙂 В этом разделе пришли текст или голосовое на английском.",
        reply_markup=chat_menu(),
    )
