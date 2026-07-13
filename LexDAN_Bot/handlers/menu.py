"""
Главное меню: переход в разделы + защита от «напишу что угодно».
"""

from aiogram import Router, F
from aiogram.types import Message

from handlers.filters import ModeFilter, StepFilter
from handlers.keyboards import main_menu, chat_menu, back_to_menu, profile_menu
from services.database import (
    load_users,
    get_user,
    set_mode,
    MODE_MENU,
    MODE_CHAT,
    MODE_LESSONS,
    MODE_PROFILE,
)

router = Router()


@router.message(ModeFilter(MODE_MENU), F.text == "🗣️ Общаться")
async def open_chat(m: Message):
    set_mode(str(m.from_user.id), MODE_CHAT)
    await m.reply(
        "🗣️ Режим общения.\n\n"
        "Пиши или присылай голосовое на английском.\n"
        "Я исправлю ошибки, отвечу текстом и голосом.\n\n"
        "🌍 Перевести — перевод моего последнего английского ответа.\n"
        "🔙 Вернуться в меню — выход из раздела.",
        reply_markup=chat_menu(),
    )


@router.message(ModeFilter(MODE_MENU), F.text == "📚 Уроки")
async def open_lessons(m: Message):
    set_mode(str(m.from_user.id), MODE_LESSONS)
    await m.reply(
        "📚 Раздел «Уроки» пока в разработке.\n"
        "Скоро здесь будут уровни A0–C2: грамматика, чтение, аудирование и словарь.\n\n"
        "Пока нажми «Вернуться в меню».",
        reply_markup=back_to_menu(),
    )


@router.message(ModeFilter(MODE_MENU), F.text == "📊 Профиль")
async def open_profile(m: Message):
    set_mode(str(m.from_user.id), MODE_PROFILE)
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)

    await m.reply(
        "📊 *Твой профиль:*\n\n"
        f"📛 Имя: {user.get('name') or 'Не указано'}\n"
        f"📚 Пройдено уроков: {user.get('lessons_done', 0)}\n"
        f"📈 Уровень: {user.get('level', 'A1')}\n"
        f"📝 Слов выучено: {user.get('words_learned', 0)}\n"
        f"💎 Подписка: бесплатно (все функции открыты)",
        parse_mode="Markdown",
        reply_markup=profile_menu(),
    )


@router.message(ModeFilter(MODE_MENU), F.text == "🆘 Поддержка")
async def open_support(m: Message):
    # остаёмся в меню — поддержка это просто сообщение
    await m.reply(
        "🆘 По вопросам пиши: @твой_ник\n"
        "(замени этот ник на свой в файле handlers/menu.py)",
        reply_markup=main_menu(),
    )


@router.message(ModeFilter(MODE_MENU), StepFilter("ready"), F.text)
async def menu_foolproof(m: Message):
    """Если человек в главном меню пишет ерунду — мягко направляем на кнопки."""
    await m.reply(
        "🙂 Пожалуйста, выбери действие кнопкой ниже.",
        reply_markup=main_menu(),
    )
