"""
Раздел «Уроки» — пока заглушка.

Логика уже правильная: сюда попадают сообщения ТОЛЬКО если mode == lessons.
Голосовое из общения здесь не обрабатывается.
"""

from aiogram import Router
from aiogram.types import Message

from handlers.filters import ModeFilter
from handlers.keyboards import back_to_menu
from services.database import MODE_LESSONS

router = Router()


@router.message(ModeFilter(MODE_LESSONS))
async def lessons_stub(m: Message):
    await m.reply(
        "📚 Уроки ещё не готовы.\n"
        "Нажми «🔙 Вернуться в меню».",
        reply_markup=back_to_menu(),
    )
