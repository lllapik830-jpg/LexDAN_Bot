"""
Middleware: логирует что за апдейт и сколько занял — чтобы ловить 10–20с зависания.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

log = logging.getLogger(__name__)


def _update_label(update: Update) -> str:
    if update.message:
        m = update.message
        text = (m.text or m.caption or "").strip().replace("\n", " ")
        if len(text) > 60:
            text = text[:57] + "…"
        kind = "voice" if m.voice else "text"
        uid = m.from_user.id if m.from_user else "?"
        return f"msg:{kind} uid={uid} «{text}»"
    if update.callback_query:
        cq = update.callback_query
        uid = cq.from_user.id if cq.from_user else "?"
        return f"cb uid={uid} data={cq.data!r}"
    return f"update:{update.event_type}"


class TimingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        label = _update_label(event) if isinstance(event, Update) else type(event).__name__
        t0 = time.perf_counter()
        try:
            return await handler(event, data)
        finally:
            ms = int((time.perf_counter() - t0) * 1000)
            if ms >= 3000:
                log.warning("SLOW update %sms | %s", ms, label)
            elif ms >= 1000:
                log.info("update %sms | %s", ms, label)
