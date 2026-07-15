"""
Голосовые — только в режиме chat.
STT: Google (через ffmpeg), не ElevenLabs.
"""

import logging

from aiogram import Router, Bot, F
from aiogram.types import Message

from handlers.filters import ModeFilter
from handlers.keyboards import chat_menu
from services.database import MODE_CHAT
from services.stt import recognize_english
from services.tutor_reply import reply_as_tutor

router = Router()


@router.message(ModeFilter(MODE_CHAT), F.voice)
async def voice_in_chat(m: Message, bot: Bot):
    from services.database import load_users, get_user, save_users
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

    await m.reply("🎧 Слушаю…", reply_markup=chat_menu())

    try:
        file = await bot.get_file(m.voice.file_id)
        voice_buffer = await bot.download_file(file.file_path)
        audio_bytes = voice_buffer.read()

        text = recognize_english(audio_bytes)
        if not text:
            await m.reply(
                "❌ Не удалось распознать речь.\n"
                "Говори по-английски чуть громче и чётче, потом попробуй снова.",
                reply_markup=chat_menu(),
            )
            return

        logging.info(f"STT ok: {text}")
        await reply_as_tutor(m, user_text=text, heard_text=text)

    except Exception as e:
        logging.error(f"Voice error: {e}")
        await m.reply("❌ Ошибка обработки голоса. Попробуй снова.", reply_markup=chat_menu())
