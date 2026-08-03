"""Отправка призовых поздравлений Рико (текст + голос + перевод)."""

from __future__ import annotations

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from data.event_congrats import get_congrats
from services.elevenlabs import send_voice_reply
from services.voices import resolve_rico_voice_id

BTN_CONGRATS_TRANSLATE = "🌍 Перевести поздравление"
BTN_CONGRATS_BACK = "🔙 К выбору мест"


def congrats_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_CONGRATS_TRANSLATE)],
            [KeyboardButton(text=BTN_CONGRATS_BACK)],
        ],
        resize_keyboard=True,
    )


async def send_place_congrats(m: Message, user: dict, place: int) -> bool:
    """Отправить EN-текст + голосовое. True если контент найден."""
    data = get_congrats(place)
    if not data:
        return False
    en = (data.get("en") or "").strip()
    title = data.get("title_ru") or f"Место {place}"
    # сохранить для кнопки перевода
    ep = user.get("event_prizes")
    if not isinstance(ep, dict):
        ep = {}
    ep["last_congrats_place"] = int(place)
    ep["last_congrats_en"] = en
    ep["last_congrats_ru"] = (data.get("ru") or "").strip()
    user["event_prizes"] = ep
    user["last_bot_reply"] = en

    await m.answer(
        f"🦜 <b>Рико · {title}</b>\n\n🇬🇧 {en}",
        reply_markup=congrats_kb(),
        parse_mode="HTML",
    )
    await send_voice_reply(
        m,
        en,
        title=f"Rico · {title}",
        voice_id=resolve_rico_voice_id(user),
    )
    return True


def congrats_translate_html(user: dict) -> str | None:
    ep = user.get("event_prizes")
    if not isinstance(ep, dict):
        return None
    ru = (ep.get("last_congrats_ru") or "").strip()
    if not ru:
        return None
    title_place = int(ep.get("last_congrats_place") or 0)
    data = get_congrats(title_place) or {}
    title = data.get("title_ru") or "Поздравление"
    return f"🌐 <b>Перевод · {title}</b>\n\n{ru}"
