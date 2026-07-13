"""
Старт и регистрация имени.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from handlers.filters import StepFilter
from handlers.keyboards import main_menu
from services.database import (
    load_users,
    save_users,
    get_user,
    MODE_MENU,
)

router = Router()

WELCOME_AFTER_NAME = (
    "🎉 Привет, {name}! Рад познакомиться!\n\n"
    "🧠 Вот что я умею:\n"
    "• 💬 Общаться на английском — исправлю ошибки и подскажу, как сказать лучше.\n"
    "• 🎤 Распознавать голосовые и отвечать голосом.\n"
    "• 📚 Уроки по уровням (скоро).\n"
    "• 📊 Показывать прогресс в профиле.\n\n"
    "👇 Кнопки:\n"
    "🗣️ Общаться — текст и голосовые.\n"
    "📚 Уроки — занятия по уровням (в разработке).\n"
    "📊 Профиль — твоя статистика.\n"
    "🆘 Поддержка — если нужна помощь.\n\n"
    "👇 Выбери, с чего начнёшь:"
)

WELCOME_AGAIN = (
    "🎉 Привет, {name}! Рад снова тебя видеть!\n\n"
    "👇 Выбери действие кнопками ниже:"
)


@router.message(Command("start"))
async def start_cmd(m: Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    user["mode"] = MODE_MENU
    save_users(users)

    if not user.get("name"):
        user["step"] = "awaiting_name"
        save_users(users)
        await m.reply(
            "👋 Привет! Я — LD (LexDan), твой личный ИИ-репетитор.\n"
            "🚀 Помогу выучить английский быстрее и проще.\n"
            "😊 Давай познакомимся! Как тебя зовут?"
        )
        return

    user["step"] = "ready"
    save_users(users)
    await m.reply(
        WELCOME_AGAIN.format(name=user["name"]),
        reply_markup=main_menu(),
    )


@router.message(StepFilter("awaiting_name"), F.text)
async def save_name(m: Message):
    """Сюда попадает ТОЛЬКО когда бот ждёт имя."""
    name = (m.text or "").strip()

    # защита от дурака: имя не должно быть командой/кнопкой
    banned = {
        "🗣️ Общаться",
        "📚 Уроки",
        "📊 Профиль",
        "🆘 Поддержка",
        "🌍 Перевести",
        "🔙 Вернуться в меню",
        "💎 Подписка",
    }
    if not name or name.startswith("/") or len(name) > 40 or name in banned:
        await m.reply("🙂 Напиши просто своё имя текстом, например: Даня")
        return

    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    user["name"] = name
    user["step"] = "ready"
    user["mode"] = MODE_MENU
    save_users(users)

    await m.reply(
        WELCOME_AFTER_NAME.format(name=name),
        reply_markup=main_menu(),
    )


@router.message(StepFilter("awaiting_name"))
async def name_not_text(m: Message):
    """Если вместо имени прислали голосовое/стикер — просим текст."""
    await m.reply("🙂 Напиши своё имя обычным текстом, например: Даня")
