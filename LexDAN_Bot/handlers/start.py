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

HELLO_NEW = (
    "✨ <b>Привет!</b> Рад тебя видеть 👋\n\n"
    "Я — <b>LexDan</b>, твой личный репетитор по английскому 🎓🇬🇧\n\n"
    "Здесь можно:\n"
    "💬 болтать со мной на английском (текст и голос)\n"
    "✏️ разбирать ошибки по-человечески, без занудства\n"
    "📚 проходить уроки по уровню\n"
    "📈 смотреть свой прогресс\n\n"
    "Атмосфера лёгкая — как на занятии с живым преподом, только всегда на связи 🚀\n\n"
    "🥰 <b>Давай познакомимся!</b>\n"
    "Как тебя зовут?"
)

WELCOME_AFTER_NAME = (
    "🎉 <b>Вау, приятно познакомиться, {name}!</b>\n\n"
    "Я LexDan — буду рядом, пока ты качаешь английский 💪🇬🇧\n\n"
    "Вот что умею прямо сейчас:\n\n"
    "🗣️ <b>Общаться</b>\n"
    "Пиши или кидай голосовые — отвечу текстом и голосом.\n"
    "Если ошибёшься, мягко поправлю <i>только грамматику/слова</i> и коротко объясню почему.\n"
    "Если всё ок — просто похвалю и продолжим болтать ✨\n\n"
    "📚 <b>Уроки</b>\n"
    "Сначала короткие тест на уровень, потом занятия от A0 до C2.\n\n"
    "📊 <b>Профиль</b>\n"
    "Твой уровень, прогресс и статистика в одном месте.\n\n"
    "🆘 <b>Поддержка</b>\n"
    "Если что-то сломалось или есть идея — пиши туда.\n\n"
    "👇 Жми кнопку внизу и начнём!\n"
    "С чего хочешь стартовать сегодня? 🚀"
)

WELCOME_AGAIN = (
    "🔥 <b>Снова привет, {name}!</b>\n\n"
    "Рад, что ты вернулся 🙂\n"
    "Готов продолжать? Выбирай, чем займёмся:"
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
        await m.reply(HELLO_NEW, parse_mode="HTML")
        return

    user["step"] = "ready"
    save_users(users)
    await m.reply(
        WELCOME_AGAIN.format(name=user["name"]),
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


@router.message(StepFilter("awaiting_name"), F.text)
async def save_name(m: Message):
    name = (m.text or "").strip()

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
        await m.reply("🙂 Напиши просто своё имя текстом, например: <b>Даня</b>", parse_mode="HTML")
        return

    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    user["name"] = name
    user["step"] = "ready"
    user["mode"] = MODE_MENU
    save_users(users)

    await m.reply(
        WELCOME_AFTER_NAME.format(name=_esc(name)),
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


@router.message(StepFilter("awaiting_name"))
async def name_not_text(m: Message):
    await m.reply("🙂 Напиши своё имя обычным текстом, например: Даня")


def _esc(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
