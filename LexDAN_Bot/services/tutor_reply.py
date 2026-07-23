"""
Общий конвейер ответа:
текст ученика → ИИ → сообщение → голосовое (OGG).
"""

from aiogram.types import Message

from services.database import load_users, get_user, save_users, set_last_bot_reply
from services.elevenlabs import send_voice_reply
from services.gpt import ask_tutor, format_tutor_message
from services.chat_topics import (
    build_dive_topic_reply,
    build_suggest_topic_reply,
    ensure_active_topic,
    library_prompt_block,
    pick_topic,
    resolve_chat_reply_mode,
)


async def reply_as_tutor(
    message: Message,
    user_text: str,
    heard_text: str | None = None,
    *,
    users: dict | None = None,
    user: dict | None = None,
) -> None:
    user_id = str(message.from_user.id)
    if users is None or user is None:
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

    ensure_active_topic(user)

    # если юзер явно просит другую тему — крутим библиотеку
    low = (user_text or "").strip().lower()
    if any(
        p in low
        for p in (
            "another topic",
            "new topic",
            "other topic",
            "change topic",
            "другую тему",
            "другая тема",
            "смени тему",
            "новую тему",
        )
    ):
        old_id = (user.get("chat_active_topic") or {}).get("id")
        user["chat_active_topic"] = pick_topic(user, avoid_ids={old_id} if old_id else set())
        user["chat_topic_offered"] = False
        user["chat_topic_dived"] = False

    active = ensure_active_topic(user)
    mode = resolve_chat_reply_mode(user_text, user, hist, recent)
    topic_block = library_prompt_block(user)

    if mode == "suggest":
        reply_en = build_suggest_topic_reply(name, active, user_text)
        result = {
            "has_error": False,
            "better_en": "",
            "errors_ru": "",
            "tips_ru": "",
            "rule_ru": "",
            "reply_en": reply_en,
        }
        user["chat_topic_offered"] = True
    elif mode == "dive":
        reply_en = build_dive_topic_reply(active)
        result = {
            "has_error": False,
            "better_en": "",
            "errors_ru": "",
            "tips_ru": "",
            "rule_ru": "",
            "reply_en": reply_en,
        }
        user["chat_topic_offered"] = True
        user["chat_topic_dived"] = True
    else:
        topic_engaged = bool(user.get("chat_topic_dived") or user.get("chat_topic_offered"))
        result = ask_tutor(
            user_text,
            name,
            recent_replies=recent,
            recent_turns=hist,
            topic_library_block=topic_block,
            active_topic=active,
            topic_engaged=topic_engaged,
        )
    text_out, reply_en = format_tutor_message(result, heard_text=heard_text)
    if not reply_en:
        active = ensure_active_topic(user)
        reply_en = (
            result.get("reply_en")
            or f"Sure! Let's talk about {active.get('title_en')}. {active.get('seed')}"
        )

    recent = (recent + [reply_en])[-8:]
    turns = (turns + [{"role": "bot", "text": reply_en}])[-10:]
    user["chat_recent_replies"] = recent
    user["chat_recent_turns"] = turns
    user["chat_last_user_text"] = user_text.strip()[:500]
    save_users(users, only=user_id)
    set_last_bot_reply(user_id, reply_en)

    await message.answer(text_out, parse_mode="HTML")
    from services.voices import resolve_chat_voice_id

    voice_id = resolve_chat_voice_id(user)
    await send_voice_reply(message, reply_en, title="LexDAN reply", voice_id=voice_id)
