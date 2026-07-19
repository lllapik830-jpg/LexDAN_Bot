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

    hist = turns[:-1]
    # После сброса сессии подскажем модели прошлую тему (если юзер не сменил её сам)
    prev_topic = (user.get("chat_last_user_text") or "").strip()
    if not hist and prev_topic and prev_topic.lower() != user_text.strip().lower():
        hist = [
            {"role": "user", "text": prev_topic},
            {
                "role": "bot",
                "text": "Last time we talked about that — happy to continue if you want.",
            },
        ]

    result = ask_tutor(
        user_text,
        name,
        recent_replies=recent,
        recent_turns=hist,
    )
    text_out, reply_en = format_tutor_message(result, heard_text=heard_text)
    if not reply_en:
        reply_en = result.get("reply_en") or "Interesting! What else can you tell me about that?"

    recent = (recent + [reply_en])[-8:]
    turns = (turns + [{"role": "bot", "text": reply_en}])[-10:]
    user["chat_recent_replies"] = recent
    user["chat_recent_turns"] = turns
    user["chat_last_user_text"] = user_text.strip()[:500]
    save_users(users, only=user_id)
    set_last_bot_reply(user_id, reply_en)

    await message.reply(text_out, parse_mode="HTML")
    # Голос = тот же текст, что в 💬 Рико (не другой кусок ответа)
    from services.voices import resolve_chat_voice_id

    voice_id = resolve_chat_voice_id(user)
    await send_voice_reply(message, reply_en, title="LexDAN reply", voice_id=voice_id)
