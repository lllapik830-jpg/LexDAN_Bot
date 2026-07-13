"""
Общий «конвейер ответа» для текста и голоса.

Цепочка одинаковая:
сообщение ученика → ИИ (исправления + ответ) → текст в чат → голос (только английский ответ)
"""

import logging
import os
import tempfile

from aiogram.types import FSInputFile, Message

from services.database import load_users, get_user, set_last_bot_reply
from services.elevenlabs import elevenlabs_tts
from services.gpt import ask_tutor, format_tutor_message


async def reply_as_tutor(
    message: Message,
    user_text: str,
    heard_text: str | None = None,
) -> None:
    user_id = str(message.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    name = user.get("name") or "Student"

    result = ask_tutor(user_text, name)
    set_last_bot_reply(user_id, result["reply_en"])

    text_out = format_tutor_message(result, heard_text=heard_text)
    await message.reply(text_out)

    # Голосом озвучиваем ТОЛЬКО английский reply (не русские пояснения)
    audio_bytes = elevenlabs_tts(result["reply_en"])
    if not audio_bytes:
        return

    path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(audio_bytes)
            path = f.name
        await message.reply_voice(FSInputFile(path))
    except Exception as e:
        logging.error(f"Send voice error: {e}")
    finally:
        if path and os.path.exists(path):
            os.unlink(path)
