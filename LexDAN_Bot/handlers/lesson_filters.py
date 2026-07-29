"""
Фильтры для состояния уроков.
"""

import asyncio

from aiogram.filters import BaseFilter
from aiogram.types import Message

from services.database import fetch_user
from services.lesson_state import ensure_lesson, assessment_busy


class LessonHubFilter(BaseFilter):
    def __init__(self, *hubs: str):
        self.hubs = set(hubs)

    async def __call__(self, message: Message) -> bool:
        user = await asyncio.to_thread(fetch_user, str(message.from_user.id))
        if assessment_busy(user):
            return False
        ensure_lesson(user)
        hub = (user.get("lesson") or {}).get("hub")
        return hub in self.hubs
