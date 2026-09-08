"""Разовые рассылки всем пользователям."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

log = logging.getLogger(__name__)

FIX_UPDATE_CAPTION = (
    "🦜 <b>LexDAN обновился</b>\n\n"
    "Вышло обновление с исправлением ошибок — уроки стали работать стабильнее и удобнее.\n\n"
    "Заходите в канал, чтобы быть в курсе всех обновлений:\n"
    "👉 https://t.me/LexDan_Rico"
)

FEATURES_UPDATE_CAPTION = (
    "🦜 <b>Рико с новостями</b>\n\n"
    "🎧 <b>Listening</b> доступен полностью — это уже не ранний доступ.\n\n"
    "🛡️ Стрик-сейфы: <b>30</b>, <b>70</b>, <b>100</b>, <b>150</b> "
    "и дальше каждые <b>30</b> дней. Пропуск закрывается сейфом автоматически.\n\n"
    "💎 Если у вас активная подписка — в профиле → «Подписка» "
    "появилась кнопка <b>«Отменить списания»</b>: "
    "можно спокойно отключить автопродление, текущий период доработает до конца.\n\n"
    "Канал обновлений:\n"
    "👉 https://t.me/LexDan_Rico"
)

_STREET_CHANNEL_KEY = "street_talk_open_all_20260817_ch"
_STREET_DM_KEY = "street_talk_open_all_20260817"


STREET_TALK_CHANNEL_CAPTION = (
    "🦜 <b>Рико:</b> Вы просили — мы сделали.\n\n"
    "🤙 <b>Живая речь</b> открыта для всех!\n\n"
    "Новый режим в уроках: как говорят живые люди, "
    "а не диктор из учебника. Склейки, короткие ответы, настоящие диалоги "
    "с акцентами — wanna, gonna, I’m down, spill the tea и всё такое.\n\n"
    "📍 Где найти:\n"
    "<b>Уроки → свой уровень A1–C2 → 🤙 Живая речь</b>\n\n"
    "🆓 Бесплатный и тариф «Общение» — <b>1 пак в день</b> "
    "(одна кнопка: теория или диалог).\n"
    "🚀 Полный доступ (799) — безлимит.\n\n"
    "Заходите быстрее попробовать, пока вайб свежий 🧃\n"
    "👉 https://t.me/LexDAN_bot"
)

STREET_TALK_DM_CAPTION = (
    "🦜 <b>Рико:</b> Вы просили — мы сделали.\n\n"
    "🤙 <b>Живая речь</b> открыта для всех!\n\n"
    "Новый режим в уроках: как говорят живые люди, а не диктор из учебника. "
    "Склейки, короткие ответы, диалоги с акцентами — wanna, gonna, I’m down и всё такое.\n\n"
    "📍 <b>Уроки → свой уровень A1–C2 → 🤙 Живая речь</b>\n\n"
    "🆓 Бесплатный и тариф «Общение» — <b>1 пак в день</b> "
    "(теория или диалог).\n"
    "🚀 Полный доступ (799) — безлимит.\n\n"
    "Заходи быстрее попробовать 🧃"
)


def street_talk_image_path() -> str | None:
    here = Path(__file__).resolve().parent.parent
    candidates = [
        here / "assets" / "posts" / "street_talk_rico.png",
        here / "assets" / "street_talk_rico.png",
    ]
    for p in candidates:
        if p.is_file():
            return str(p)
    return None


async def post_street_talk_to_channel(bot) -> dict:
    """Пост в канал @LexDan_Rico (не рассылка в личку)."""
    from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup

    from config import CHANNEL_USERNAME

    channel = f"@{CHANNEL_USERNAME.lstrip('@')}"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🤙 Открыть бота", url="https://t.me/LexDAN_bot")]
        ]
    )
    photo = street_talk_image_path()
    try:
        if photo:
            await bot.send_photo(
                chat_id=channel,
                photo=FSInputFile(photo),
                caption=STREET_TALK_CHANNEL_CAPTION,
                parse_mode="HTML",
                reply_markup=kb,
            )
        else:
            await bot.send_message(
                chat_id=channel,
                text=STREET_TALK_CHANNEL_CAPTION,
                parse_mode="HTML",
                reply_markup=kb,
                disable_web_page_preview=True,
            )
        logging.info("Street talk posted to channel %s", channel)
        return {"ok": True, "channel": channel}
    except Exception as e:
        logging.error("Street talk channel post failed: %s", e)
        return {"ok": False, "error": str(e)}


async def post_street_talk_to_channel_once(bot, *, force: bool = False) -> dict:
    from services.database import load_users, save_users

    users = load_users()
    meta = users.get("__broadcasts__")
    if not isinstance(meta, dict):
        meta = {}
    if meta.get(_STREET_CHANNEL_KEY) and not force:
        return {"ok": False, "already": True}
    result = await post_street_talk_to_channel(bot)
    if result.get("ok"):
        users = load_users()
        meta = users.get("__broadcasts__")
        if not isinstance(meta, dict):
            meta = {}
            users["__broadcasts__"] = meta
        meta[_STREET_CHANNEL_KEY] = True
        users["__broadcasts__"] = meta
        save_users(users, only=["__broadcasts__"])
    return result


async def broadcast_street_talk(bot) -> dict:
    """Рассылка абсолютно всем: Живая речь открыта (фото или текст)."""
    photo_path = street_talk_image_path()
    kwargs = {
        "caption": STREET_TALK_DM_CAPTION,
        "log_name": "broadcast_street",
        "include_blocked": True,
    }
    if photo_path:
        return await _broadcast_photo(bot, photo_path=photo_path, **kwargs)
    return await _broadcast_text(bot, **kwargs)


async def broadcast_street_talk_once(bot, *, force: bool = False) -> dict:
    from services.database import load_users, save_users

    users = load_users()
    meta = users.get("__broadcasts__")
    if not isinstance(meta, dict):
        meta = {}
    if meta.get(_STREET_DM_KEY) and not force:
        return {"ok": False, "already": True, "sent": 0, "fail": 0}
    result = await broadcast_street_talk(bot)
    if result.get("ok"):
        users = load_users()
        meta = users.get("__broadcasts__")
        if not isinstance(meta, dict):
            meta = {}
            users["__broadcasts__"] = meta
        meta[_STREET_DM_KEY] = True
        users["__broadcasts__"] = meta
        save_users(users, only=["__broadcasts__"])
    return result


def fix_update_image_path() -> str | None:
    here = Path(__file__).resolve().parent.parent
    candidates = [
        here / "assets" / "lexdan_fix_update.png",
        here / "assets" / "posts" / "post-lexdan-fix-update.png",
    ]
    for p in candidates:
        if p.is_file():
            return str(p)
    return None


def features_update_image_path() -> str | None:
    here = Path(__file__).resolve().parent.parent
    candidates = [
        here / "assets" / "lexdan_fix_update.png",
        here / "assets" / "posts" / "post-lexdan-rico-hello.png",
        here / "assets" / "rico_sad_cancel.png",
    ]
    for p in candidates:
        if p.is_file():
            return str(p)
    return None


async def _broadcast_text(
    bot,
    *,
    caption: str,
    log_name: str,
    extra_buttons: list | None = None,
    include_blocked: bool = False,
) -> dict:
    return await _broadcast_send(
        bot,
        caption=caption,
        log_name=log_name,
        extra_buttons=extra_buttons,
        include_blocked=include_blocked,
        photo_path=None,
    )


async def _broadcast_photo(
    bot,
    *,
    photo_path: str,
    caption: str,
    log_name: str,
    extra_buttons: list | None = None,
    include_blocked: bool = False,
) -> dict:
    return await _broadcast_send(
        bot,
        caption=caption,
        log_name=log_name,
        extra_buttons=extra_buttons,
        include_blocked=include_blocked,
        photo_path=photo_path,
    )


async def _broadcast_send(
    bot,
    *,
    caption: str,
    log_name: str,
    extra_buttons: list | None = None,
    include_blocked: bool = False,
    photo_path: str | None = None,
) -> dict:
    from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup

    from services.database import load_users, save_users

    users = load_users()
    rows = [
        [
            InlineKeyboardButton(
                text="📣 Канал обновлений",
                url="https://t.me/LexDan_Rico",
            )
        ]
    ]
    if extra_buttons:
        rows = list(extra_buttons) + rows
    kb = InlineKeyboardMarkup(inline_keyboard=rows)

    sent = 0
    fail = 0
    blocked_ids: list[str] = []
    unblocked_ids: list[str] = []

    for uid, payload in users.items():
        if not isinstance(payload, dict) or str(uid).startswith("__"):
            continue
        if payload.get("imitating_registration"):
            continue
        if payload.get("tg_blocked") and not include_blocked:
            continue
        try:
            chat_id = int(uid)
        except (TypeError, ValueError):
            fail += 1
            continue
        try:
            if photo_path:
                await bot.send_photo(
                    chat_id,
                    photo=FSInputFile(photo_path),
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=kb,
                )
            else:
                await bot.send_message(
                    chat_id,
                    caption,
                    parse_mode="HTML",
                    reply_markup=kb,
                    disable_web_page_preview=True,
                )
            sent += 1
            if payload.get("tg_blocked"):
                payload["tg_blocked"] = False
                unblocked_ids.append(str(uid))
        except Exception as e:
            fail += 1
            err = str(e).lower()
            if "blocked" in err or "deactivated" in err or "forbidden" in err:
                payload["tg_blocked"] = True
                blocked_ids.append(str(uid))
            log.warning("%s fail uid=%s: %s", log_name, uid, e)
        await asyncio.sleep(0.05)

    touch_ids = list(dict.fromkeys(blocked_ids + unblocked_ids))
    if touch_ids:
        save_users(users, only=touch_ids)

    log.info("%s sent=%s fail=%s blocked=%s", log_name, sent, fail, len(blocked_ids))
    return {"ok": True, "sent": sent, "fail": fail, "blocked": len(blocked_ids)}


async def broadcast_fix_update(bot) -> dict:
    """Фото + текст про фикс всем user_id из БД (кроме служебных ключей)."""
    photo_path = fix_update_image_path()
    if not photo_path:
        return {"ok": False, "error": "image_missing", "sent": 0, "fail": 0}
    return await _broadcast_photo(
        bot,
        photo_path=photo_path,
        caption=FIX_UPDATE_CAPTION,
        log_name="broadcast_fix",
    )


async def broadcast_features_update(bot) -> dict:
    """Listening / сейфы 30+70 / отмена списаний."""
    photo_path = features_update_image_path()
    if not photo_path:
        return {"ok": False, "error": "image_missing", "sent": 0, "fail": 0}
    return await _broadcast_photo(
        bot,
        photo_path=photo_path,
        caption=FEATURES_UPDATE_CAPTION,
        log_name="broadcast_features",
    )
