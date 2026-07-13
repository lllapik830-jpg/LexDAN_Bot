"""
Фильтры = «пропускалки».

Пример: ModeFilter("chat") пропускает сообщение только если
пользователь сейчас в разделе «Общаться».
Из-за этого голосовое в «Уроках» НЕ уйдёт в обработчик общения.
"""

from aiogram.filters import BaseFilter
from aiogram.types import Message
from services.database import load_users, get_user


class ModeFilter(BaseFilter):
    def __init__(self, mode: str):
        self.mode = mode

    async def __call__(self, message: Message) -> bool:
        user_id = str(message.from_user.id)
        users = load_users()
        user = get_user(users, user_id)
        return user.get("mode") == self.mode


class StepFilter(BaseFilter):
    def __init__(self, step: str):
        self.step = step

    async def __call__(self, message: Message) -> bool:
        user_id = str(message.from_user.id)
        users = load_users()
        user = get_user(users, user_id)
        return user.get("step") == self.step
