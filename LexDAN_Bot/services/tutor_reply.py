"""
Общий конвейер ответа:
текст ученика → ИИ → сообщение → голосовое (OGG).
"""

import logging
import os
import tempfile

from aiogram.types import FSInputFile, Message

from services.database import load_users, get_user, set_last_bot_reply
from services.elevenlabs import elevenlabs_tts, mp3_to_ogg_opus
from services.gpt import ask_tutor, format_tutor_message


async def reply_as_tutor(
    message: Message,
    user_text: str,
    heard_text: str | None = None,
) -> None:
    user_id = str(message.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    name = user.get("name") or message.from_user.first_name or "Student"

    result = ask_tutor(user_text, name)
    set_last_bot_reply(user_id, result["reply_en"])

    text_out = format_tutor_message(result, heard_text=heard_text)
    await message.reply(text_out, parse_mode="HTML")

    mp3_bytes = elevenlabs_tts(result["reply_en"])
    if not mp3_bytes:
        await message.reply("⚠️ Текст готов, но голос сейчас не отправился.")
        return

    ogg_bytes = mp3_to_ogg_opus(mp3_bytes)
    path = None
    try:
        if ogg_bytes:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
                f.write(ogg_bytes)
                path = f.name
            await message.reply_voice(FSInputFile(path))
        else:
            # запасной вариант: обычное аудио-вложение (MP3)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(mp3_bytes)
                path = f.name
            await message.reply_audio(FSInputFile(path), title="LexDAN reply")
    except Exception as e:
        logging.error(f"Send voice error: {e}")
        await message.reply("⚠️ Не удалось отправить голосовое сообщение.")
    finally:
        if path and os.path.exists(path):
            os.unlink(path)
