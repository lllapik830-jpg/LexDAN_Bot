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
    "Приятно познакомиться, {name}! Я LexDan — твой репетитор по английскому.\n\n"
    "Можем просто болтать на английском (текст и голос) — "
    "я мягко поправлю грамматику и подскажу, как звучит естественнее.\n"
    "Есть уроки по уровням и профиль с прогрессом.\n\n"
    "Кнопки внизу:\n"
    "🗣️ Общаться — живой диалог\n"
    "📚 Уроки — тест уровня и занятия\n"
    "📊 Профиль — твоя статистика\n"
    "🆘 Поддержка — если что-то не так\n\n"
    "С чего начнём?"
)

WELCOME_AGAIN = (
    "Снова привет, {name}! Рад тебя видеть 🙂\n\n"
    "Выбирай, чем займёмся:"
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
            "Привет! Я LexDan — твой репетитор по английскому.\n"
            "Будем болтать, разбирать ошибки и подтягивать язык без занудства.\n\n"
            "Как тебя зовут?"
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
