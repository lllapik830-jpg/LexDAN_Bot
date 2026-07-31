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


async def _broadcast_photo(
    bot,
    *,
    photo_path: str,
    caption: str,
    log_name: str,
) -> dict:
    from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup

    from services.database import load_users, save_users

    users = load_users()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📣 Канал обновлений",
                    url="https://t.me/LexDan_Rico",
                )
            ]
        ]
    )

    sent = 0
    fail = 0
    blocked_ids: list[str] = []

    for uid, payload in users.items():
        if not isinstance(payload, dict) or str(uid).startswith("__"):
            continue
        if payload.get("tg_blocked"):
            continue
        try:
            chat_id = int(uid)
        except (TypeError, ValueError):
            fail += 1
            continue
        try:
            await bot.send_photo(
                chat_id,
                photo=FSInputFile(photo_path),
                caption=caption,
                parse_mode="HTML",
                reply_markup=kb,
            )
            sent += 1
        except Exception as e:
            fail += 1
            err = str(e).lower()
            if "blocked" in err or "deactivated" in err or "forbidden" in err:
                payload["tg_blocked"] = True
                blocked_ids.append(str(uid))
            log.warning("%s fail uid=%s: %s", log_name, uid, e)
        await asyncio.sleep(0.05)

    if blocked_ids:
        save_users(users, only=blocked_ids)

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
