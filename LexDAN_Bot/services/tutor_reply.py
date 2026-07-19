"""
Общий конвейер ответа:
текст ученика → ИИ → сообщение → голосовое (OGG).
"""

from aiogram.types import Message

from services.database import load_users, get_user, save_users, set_last_bot_reply
from services.elevenlabs import send_voice_reply
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

    recent = list(user.get("chat_recent_replies") or [])
    if user.get("last_bot_reply"):
        if not recent or recent[-1] != user["last_bot_reply"]:
            recent = (recent + [user["last_bot_reply"]])[-8:]

    turns = list(user.get("chat_recent_turns") or [])
    turns = (turns + [{"role": "user", "text": user_text}])[-10:]

    result = ask_tutor(
        user_text,
        name,
        recent_replies=recent,
        recent_turns=turns[:-1],  # история до текущего сообщения
    )
    text_out = format_tutor_message(result, heard_text=heard_text)
    reply_en = result.get("reply_en") or ""

    recent = (recent + [reply_en])[-8:]
    turns = (turns + [{"role": "bot", "text": reply_en}])[-10:]
    user["chat_recent_replies"] = recent
    user["chat_recent_turns"] = turns
    save_users(users)
    set_last_bot_reply(user_id, reply_en)

    await message.reply(text_out, parse_mode="HTML")

    await send_voice_reply(message, reply_en, title="LexDAN reply")
