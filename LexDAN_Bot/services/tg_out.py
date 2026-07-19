"""
Исходящие сообщения без цитирования + автоочистка служебных.

- say() / answer без reply_to (не «отвечает» на кнопку пользователя)
- track ephemeral → purge при смене экрана (меню / профиль / раздел)
- status() → «генерирую…» с последующим delete
"""

from __future__ import annotations

from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Any

from aiogram.types import Message

# user_id -> list[(chat_id, message_id)]
_EPHEMERAL: dict[str, list[tuple[int, int]]] = defaultdict(list)
_MAX_TRACK = 40


def _uid(m: Message) -> str:
    return str(m.from_user.id) if m.from_user else str(m.chat.id)


def track(user_id: str, chat_id: int, message_id: int) -> None:
    lst = _EPHEMERAL[user_id]
    lst.append((chat_id, message_id))
    if len(lst) > _MAX_TRACK:
        del lst[:-_MAX_TRACK]


async def try_delete(bot, chat_id: int, message_id: int) -> None:
    try:
        await bot.delete_message(chat_id, message_id)
    except Exception:
        pass


async def try_delete_user_tap(m: Message) -> None:
    """В личке бот может удалить нажатие кнопки пользователя — меньше мусора."""
    try:
        await m.delete()
    except Exception:
        pass


async def purge(bot, user_id: str, *, chat_id: int | None = None) -> None:
    items = list(_EPHEMERAL.pop(user_id, []))
    for cid, mid in items:
        if chat_id is not None and cid != chat_id:
            continue
        await try_delete(bot, cid, mid)


async def say(
    m: Message,
    text: str,
    *,
    ephemeral: bool = True,
    replace: bool = False,
    delete_tap: bool = False,
    **kwargs: Any,
) -> Message:
    """
    Отправить сообщение без цитирования пользовательского.
    replace=True — сначала удалить предыдущие ephemeral этого юзера.
    """
    if delete_tap:
        await try_delete_user_tap(m)
    if replace:
        await purge(m.bot, _uid(m), chat_id=m.chat.id)
    sent = await m.answer(text, **kwargs)
    if ephemeral and sent:
        track(_uid(m), m.chat.id, sent.message_id)
    return sent


@asynccontextmanager
async def status(m: Message, text: str = "🦜 …"):
    """Показать статус («готовлю задание»), удалить после блока."""
    msg = await m.answer(text)
    try:
        yield msg
    finally:
        if msg:
            await try_delete(m.bot, m.chat.id, msg.message_id)
