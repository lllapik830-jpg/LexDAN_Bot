"""
Middleware: антифлуд на все апдейты с from_user (сообщения и кнопки).
"""

from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

log = logging.getLogger(__name__)


def _actor_id(update: Update) -> str | None:
    if update.message and update.message.from_user:
        return str(update.message.from_user.id)
    if update.callback_query and update.callback_query.from_user:
        return str(update.callback_query.from_user.id)
    if update.edited_message and update.edited_message.from_user:
        return str(update.edited_message.from_user.id)
    return None


class RateLimitMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Update):
            return await handler(event, data)

        uid = _actor_id(event)
        if not uid:
            return await handler(event, data)

        from services.database import fetch_user, save_users
        from services.rate_limit import check_and_touch

        user = fetch_user(uid)
        result = check_and_touch(uid, user)
        if result.get("persist"):
            try:
                save_users({uid: user}, only=uid)
            except Exception as e:
                log.warning("rate_limit save fail uid=%s: %s", uid, e)

        if result.get("allow"):
            return await handler(event, data)

        notify = result.get("notify")
        if notify:
            bot = data.get("bot")
            try:
                if event.callback_query:
                    await event.callback_query.answer(
                        "Слишком быстро — подожди немного",
                        show_alert=False,
                    )
                    if bot:
                        await bot.send_message(int(uid), notify, parse_mode="HTML")
                elif event.message and bot:
                    await bot.send_message(int(uid), notify, parse_mode="HTML")
                elif bot:
                    await bot.send_message(int(uid), notify, parse_mode="HTML")
            except Exception as e:
                log.warning("rate_limit notify fail uid=%s: %s", uid, e)
        return None
