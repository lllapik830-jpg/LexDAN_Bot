"""Пост-онбординг воронка: CTA в Общаться → потом Listening (inline)."""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services.funnel_track import ensure_funnel, record_event

# Сколько сообщений в чате после CTA, прежде чем предложить Listening
CHAT_MSGS_BEFORE_LISTEN = 3

CHAT_CTA_HTML = (
    "🗣️ Заходи в раздел <b>Общаться</b> и попробуй поболтать с Рико — "
    "он сразу предложит тебе тему!"
)

LISTEN_CTA_HTML = (
    "🦜 А ты знал, что язык на <b>общении</b> учится примерно на "
    "<b>90%</b> быстрее?\n\n"
    "Давай заглянем в <b>Listening</b> — там ты сам выберешь тему 🎧"
)


def chat_cta_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗣️ Общаться",
                    callback_data="ofu:chat",
                )
            ]
        ]
    )


def listen_cta_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎧 Listening",
                    callback_data="ofu:listen",
                )
            ]
        ]
    )


def mark_chat_cta_sent(user: dict) -> None:
    f = ensure_funnel(user)
    f["chat_cta_sent"] = True
    record_event(user, "chat_cta_sent")


def mark_listen_cta_sent(user: dict) -> None:
    f = ensure_funnel(user)
    f["listen_cta_sent"] = True
    record_event(user, "listen_cta_sent")


def should_offer_listen(user: dict, *, force_leave: bool = False) -> bool:
    """После CTA в чат: N сообщений или выход из Общаться."""
    f = ensure_funnel(user)
    if not f.get("chat_cta_sent"):
        return False
    if f.get("listen_cta_sent"):
        return False
    if force_leave and f.get("chat_opened_after_cta"):
        return True
    return int(f.get("chat_msgs_after_cta") or 0) >= CHAT_MSGS_BEFORE_LISTEN


def bump_chat_after_cta(user: dict) -> bool:
    """+1 к сообщениям после chat CTA. True если пора слать Listening CTA."""
    f = ensure_funnel(user)
    if not f.get("chat_cta_sent") or f.get("listen_cta_sent"):
        return False
    f["chat_msgs_after_cta"] = int(f.get("chat_msgs_after_cta") or 0) + 1
    return should_offer_listen(user)
