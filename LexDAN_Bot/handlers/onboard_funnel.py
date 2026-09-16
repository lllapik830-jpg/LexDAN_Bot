"""Inline-кнопки пост-онбординга: Общаться → Listening."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from handlers.keyboards import chat_menu, main_menu
from services.database import (
    MODE_CHAT,
    MODE_LESSONS,
    MODE_MENU,
    get_user,
    load_users,
    save_users,
    set_mode,
    users_for,
)
from services.funnel_track import ensure_funnel, record_event
from services.onboard_funnel import (
    CHAT_CTA_HTML,
    LISTEN_CTA_HTML,
    chat_cta_kb,
    listen_cta_kb,
    mark_chat_cta_sent,
    mark_listen_cta_sent,
    should_offer_listen,
)
from services.tg_out import say

router = Router()


async def send_chat_cta(m: Message, uid: str) -> None:
    users = load_users()
    user = get_user(users, uid)
    f = ensure_funnel(user)
    if f.get("chat_cta_sent"):
        save_users(users, only=uid)
        return
    mark_chat_cta_sent(user)
    save_users(users, only=uid)
    await m.answer(CHAT_CTA_HTML, reply_markup=chat_cta_kb(), parse_mode="HTML")


async def maybe_send_listen_cta(m: Message, uid: str, *, force_leave: bool = False) -> bool:
    users = load_users()
    user = get_user(users, uid)
    if not should_offer_listen(user, force_leave=force_leave):
        return False
    mark_listen_cta_sent(user)
    save_users(users, only=uid)
    await m.answer(LISTEN_CTA_HTML, reply_markup=listen_cta_kb(), parse_mode="HTML")
    return True


async def on_chat_message_counted(m: Message, uid: str, user: dict, users: dict) -> None:
    """Вызвать после успешного note_chat_message (+ save)."""
    from services.onboard_funnel import bump_chat_after_cta

    if bump_chat_after_cta(user):
        save_users(users, only=uid)
        await maybe_send_listen_cta(m, uid)


async def enter_chat_from_funnel(m: Message, uid: str) -> None:
    """Открыть Общаться так же, как кнопка меню (с темой от Рико)."""
    from services.chat_guard import try_open_chat
    from services.growth import ensure_growth, note_lesson_activity
    from services.moderation import ensure_moderation, is_banned, ban_remaining_text
    from services.chat_topics import ensure_active_topic, build_dive_topic_reply
    from services.database import set_last_bot_reply

    if not try_open_chat(uid):
        # уже в чате — просто подсказка
        await m.answer("Чат уже открыт — напиши сообщение Рико 🙂🦜", reply_markup=chat_menu())
        return

    set_mode(uid, MODE_CHAT)
    users = users_for(uid)
    user = get_user(users, uid)
    user["picking_chat_voice"] = False
    ensure_growth(user)
    note_lesson_activity(user)
    ensure_moderation(user)
    if is_banned(user):
        save_users(users, only=uid)
        await m.answer(ban_remaining_text(user), parse_mode="HTML")
        return

    f = ensure_funnel(user)
    f["chat_opened_after_cta"] = True
    record_event(user, "chat_opened_funnel")

    user["chat_recent_turns"] = []
    user["chat_recent_replies"] = []
    user["chat_topic_offered"] = True
    user["chat_topic_dived"] = True

    active = ensure_active_topic(user, force_new=True)
    opener_en = build_dive_topic_reply(active)
    user["chat_own_topic"] = False
    user["chat_recent_replies"] = [opener_en]
    user["last_bot_reply"] = opener_en
    save_users(users, only=uid)
    set_last_bot_reply(uid, opener_en)

    def _esc(t: str) -> str:
        return (
            (t or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    intro = (
        "🔥 <b>Погнали общаться!</b> 🙂✨\n\n"
        "💬 Пиши текстом или кидай голосовое на английском 🎙️\n\n"
        "🎯 Предлагаю тему для общения:\n"
        f"🦜 <i>{_esc(opener_en)}</i>\n\n"
        "💡 Либо можешь сам начать с того, что интересно!"
    )
    await say(
        m,
        intro,
        replace=False,
        delete_tap=False,
        section_emoji="🗣️",
        reply_markup=chat_menu(),
        parse_mode="HTML",
    )

    import asyncio
    from services.elevenlabs import send_voice_reply
    from services.voices import resolve_chat_voice_id

    async def _voice():
        try:
            await send_voice_reply(
                m,
                opener_en,
                title="Rico · topic",
                voice_id=resolve_chat_voice_id(user),
            )
        except Exception:
            pass

    asyncio.create_task(_voice())


async def enter_listening_from_funnel(m: Message, uid: str) -> None:
    from services.growth import ensure_growth
    from services.free_lesson_limits import SECTION_LISTENING, check_section_access
    from handlers.lesson_keyboards import lesson_limit_inline_kb, level_sections_kb
    from handlers.lessons_listening import open_listening_for_level
    from services.lesson_state import ensure_lesson, set_level_hub

    set_mode(uid, MODE_LESSONS)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    ensure_lesson(user)
    level = (user.get("level") or "A1").strip() or "A1"
    set_level_hub(uid, level)
    users = load_users()
    user = get_user(users, uid)

    f = ensure_funnel(user)
    f["listen_opened_after_cta"] = True
    record_event(user, "listen_opened_funnel")
    save_users(users, only=uid)

    ok, limit_msg = check_section_access(user, SECTION_LISTENING)
    if not ok:
        await m.answer(limit_msg, parse_mode="HTML")
        await m.answer("👇", reply_markup=lesson_limit_inline_kb())
        await m.answer(
            f"🎓 Уровень {level} — выбери раздел:",
            reply_markup=level_sections_kb(user_id=uid),
        )
        return

    await open_listening_for_level(m, user, level)


@router.callback_query(F.data == "ofu:chat")
async def cb_ofu_chat(c: CallbackQuery):
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    try:
        await c.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await enter_chat_from_funnel(c.message, uid)


@router.callback_query(F.data == "ofu:listen")
async def cb_ofu_listen(c: CallbackQuery):
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    try:
        await c.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await enter_listening_from_funnel(c.message, uid)
