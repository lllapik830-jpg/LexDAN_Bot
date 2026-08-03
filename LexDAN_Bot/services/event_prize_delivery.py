"""
Рассылка призов после финала ивента (сообщения + голос + картинки).
"""

from __future__ import annotations

import logging
from pathlib import Path

from aiogram import Bot
from aiogram.types import FSInputFile

from data.event_congrats import get_congrats
from services.event_magic import (
    EVENT_TITLE,
    TITLE_PLACE_1,
    TITLE_PLACE_2,
    TITLE_PLACE_3,
    TITLE_PLACE_4_10,
    load_event_state,
    save_event_state,
)
from services.voices import RICO_VOICE_ID

log = logging.getLogger(__name__)

_ASSETS = Path(__file__).resolve().parent.parent / "assets"
HALL_ART = _ASSETS / "legends_lexdan_hall.png"
THANKS_STICKER_IMG = _ASSETS / "stickers" / "sticker_thanks_champion.png"
PACK3_DIR = _ASSETS / "stickers" / "pack3"

BTN_LEGEND_TASK = "🏆 Задание для легенды"
BTN_MASTER_TASK = "🥈 Задание для мастера"
BTN_HUNTER_TASK = "🥉 Задание для охотника"

PLACE_TASK_BUTTON = {
    1: BTN_LEGEND_TASK,
    2: BTN_MASTER_TASK,
    3: BTN_HUNTER_TASK,
}


def prize_task_button_for(user: dict | None) -> str | None:
    if not user:
        return None
    ep = user.get("event_prizes")
    if not isinstance(ep, dict):
        return None
    place = int(ep.get("place") or 0)
    return PLACE_TASK_BUTTON.get(place)


async def _send_text(bot: Bot, chat_id: int, text: str) -> None:
    await bot.send_message(chat_id, text, parse_mode="HTML")


async def _send_photo(bot: Bot, chat_id: int, path: Path, caption: str = "") -> None:
    if not path.exists():
        log.warning("Missing asset: %s", path)
        return
    await bot.send_photo(
        chat_id,
        FSInputFile(str(path)),
        caption=caption or None,
        parse_mode="HTML" if caption else None,
    )


async def _send_congrats_voice(bot: Bot, chat_id: int, place: int) -> None:
    """Текст + голос классическим Rico (не alt) + перевод."""
    import asyncio
    import os
    import tempfile

    from services.elevenlabs import synthesize_speech, mp3_to_ogg_opus

    data = get_congrats(place)
    if not data:
        return
    en = (data.get("en") or "").strip()
    title = data.get("title_ru") or f"Место {place}"
    ru = (data.get("ru") or "").strip()
    await bot.send_message(
        chat_id,
        f"🦜 <b>Рико · {title}</b>\n\n🇬🇧 {en}",
        parse_mode="HTML",
    )
    mp3, _src = await asyncio.to_thread(synthesize_speech, en, RICO_VOICE_ID)
    if mp3:
        ogg = await asyncio.to_thread(mp3_to_ogg_opus, mp3)
        path = None
        try:
            if ogg:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
                    f.write(ogg)
                    path = f.name
                await bot.send_voice(chat_id, FSInputFile(path))
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(mp3)
                    path = f.name
                await bot.send_audio(chat_id, FSInputFile(path), title=f"Rico · {title}")
        finally:
            if path and os.path.exists(path):
                os.unlink(path)
    if ru:
        await bot.send_message(
            chat_id,
            f"🌐 <b>Перевод</b>\n\n{ru}",
            parse_mode="HTML",
        )


async def deliver_place_1(bot: Bot, chat_id: int, *, username: str = "") -> None:
    who = f"@{username.lstrip('@')}" if username else "чемпион"
    await _send_photo(
        bot,
        chat_id,
        HALL_ART,
        caption=(
            f"🏛️ <b>Зал славы LexDan</b>\n"
            f"Твоё имя — <b>{who}</b> — навечно среди легенд."
        ),
    )
    await _send_congrats_voice(bot, chat_id, 1)
    await _send_text(
        bot,
        chat_id,
        "🎙 Тебе открыт <b>новый голос Рико</b>!\n"
        "Выбрать его можно в разделе <b>📚 Уроки</b> → кнопка <b>🦜 Голос Рико</b> "
        "(переключение classic ↔ legend).",
    )
    await _send_text(
        bot,
        chat_id,
        "📜 Эксклюзивная история ждёт тебя:\n"
        f"Зайди в <b>📊 Профиль</b> и нажми <b>{BTN_LEGEND_TASK}</b>.",
    )
    await _send_text(
        bot,
        chat_id,
        f"🎖 Тебе присвоен титул <b>{TITLE_PLACE_1}</b>.\n"
        "Он отображается табличкой рядом с ником в профиле.",
    )


async def deliver_place_2(bot: Bot, chat_id: int) -> None:
    await _send_congrats_voice(bot, chat_id, 2)
    await _send_text(
        bot,
        chat_id,
        "🎙 Тебе открыт <b>новый голос Рико</b>!\n"
        "Выбрать: <b>📚 Уроки</b> → <b>🦜 Голос Рико</b>.",
    )
    await _send_text(
        bot,
        chat_id,
        "✨ Задания мастера:\n"
        f"<b>📊 Профиль</b> → <b>{BTN_MASTER_TASK}</b>.",
    )
    await _send_text(
        bot,
        chat_id,
        f"🎖 Титул <b>{TITLE_PLACE_2}</b> закреплён табличкой рядом с ником в профиле.",
    )


async def deliver_place_3(bot: Bot, chat_id: int) -> None:
    await _send_congrats_voice(bot, chat_id, 3)
    await _send_text(
        bot,
        chat_id,
        "🎯 Задания охотника:\n"
        f"<b>📊 Профиль</b> → <b>{BTN_HUNTER_TASK}</b>.",
    )
    await _send_text(
        bot,
        chat_id,
        f"🎖 Титул <b>{TITLE_PLACE_3}</b> закреплён табличкой рядом с ником в профиле.",
    )
    # Стикерпак: если есть file_id в стейте — шлём стикеры; иначе картинки-заготовки
    state = load_event_state()
    file_ids = list(state.get("place3_sticker_file_ids") or [])
    if file_ids:
        await _send_text(bot, chat_id, "🎟 Твой стикерпак охотника:")
        for fid in file_ids:
            try:
                await bot.send_sticker(chat_id, sticker=fid)
            except Exception as e:
                log.warning("sticker send fail: %s", e)
    elif PACK3_DIR.exists():
        await _send_text(
            bot,
            chat_id,
            "🎟 Стикеры охотника (пока как картинки — после пака в @Stickers "
            "подключим настоящие стикеры):",
        )
        for p in sorted(PACK3_DIR.glob("pack3_sticker_*.png")):
            await _send_photo(bot, chat_id, p)


async def deliver_place_4_10(bot: Bot, chat_id: int) -> None:
    await _send_photo(
        bot,
        chat_id,
        THANKS_STICKER_IMG,
        caption="🎟 Спасибо за участие, чемпион LexDan!",
    )
    await _send_text(
        bot,
        chat_id,
        f"🏁 Ивент «{EVENT_TITLE}» завершён.\n\n"
        f"🎖 Тебе присвоен титул <b>{TITLE_PLACE_4_10}</b> — "
        "он отображается табличкой рядом с ником в профиле.\n"
        "Гонка лидеров сохранила итоги — до следующего ивента можно смотреть топ.",
    )


async def deliver_all_prizes(bot: Bot, top: list[dict] | None = None) -> dict:
    """
    Разослать призы топ-10. Идемпотентно через state['prizes_delivered'].
    """
    state = load_event_state()
    if state.get("prizes_delivered") and not state.get("force_deliver"):
        return {"ok": True, "already": True, "sent": 0, "fail": 0}

    if top is None:
        top = list(state.get("frozen_top") or [])

    sent = 0
    fail = 0
    for r in top:
        uid = str(r.get("user_id") or "")
        place = int(r.get("place") or 0)
        if not uid or place < 1:
            continue
        try:
            chat_id = int(uid)
        except ValueError:
            fail += 1
            continue
        un = (r.get("username") or "").strip()
        try:
            if place == 1:
                await deliver_place_1(bot, chat_id, username=un)
            elif place == 2:
                await deliver_place_2(bot, chat_id)
            elif place == 3:
                await deliver_place_3(bot, chat_id)
            else:
                await deliver_place_4_10(bot, chat_id)
            sent += 1
        except Exception as e:
            log.error("Prize deliver fail uid=%s place=%s: %s", uid, place, e)
            fail += 1

    state["prizes_delivered"] = True
    state["force_deliver"] = False
    save_event_state(state)
    return {"ok": True, "already": False, "sent": sent, "fail": fail}
