"""
Фильтры = «пропускалки».

fetch_user в to_thread: иначе sync Postgres под локом стопорит ВСЕ апдейты
(пока один юзер ждёт TTS/GPT — у другого «висит» даже кнопка A2).
"""

import asyncio

from aiogram.filters import BaseFilter
from aiogram.types import Message
from services.database import fetch_user


class ModeFilter(BaseFilter):
    def __init__(self, mode: str):
        self.mode = mode

    async def __call__(self, message: Message) -> bool:
        user = await asyncio.to_thread(fetch_user, str(message.from_user.id))
        return user.get("mode") == self.mode


class StepFilter(BaseFilter):
    def __init__(self, step: str):
        self.step = step

    async def __call__(self, message: Message) -> bool:
        user = await asyncio.to_thread(fetch_user, str(message.from_user.id))
        return user.get("step") == self.step
