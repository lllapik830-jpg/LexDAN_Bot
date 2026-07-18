"""
Старт и регистрация имени + рефералка.
"""

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from handlers.filters import StepFilter
from handlers.keyboards import main_menu
from services.database import (
    load_users,
    save_users,
    get_user,
    MODE_MENU,
)
from services.growth import (
    apply_referral_on_start,
    bind_referral_code,
    ensure_growth,
    grant_referral_bonuses,
    REF_BONUS_DAYS,
)

router = Router()

HELLO_NEW = (
    "✨ <b>Привет!</b> Я <b>LexDan</b>, рядом попугай <b>Рико</b> 🦜\n\n"
    "Английский в Telegram: ~15 минут в день — общение, слова, грамматика.\n\n"
    "🥰 <b>Как тебя зовут?</b>"
)

WELCOME_AFTER_NAME = (
    "🎉 <b>Приятно познакомиться, {name}!</b>\n\n"
    "1) 📚 Уроки → тест уровня\n"
    "2) Каждый день ~15 минут: слова или грамматика\n"
    "3) 🗣️ Общаться — закрепить вживую\n\n"
    "После теста — <b>7 дней</b> полного доступа.\n"
    "👇 С чего начнём?"
)

WELCOME_AGAIN = (
    "🔥 Снова привет, {name}! Чем займёмся сегодня?"
)


@router.message(Command("start"))
async def start_cmd(m: Message, command: CommandObject = None):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    bind_referral_code(user_id, user)
    user["mode"] = MODE_MENU

    # /start ref_XXXX
    args = (command.args if command else None) or ""
    if args.startswith("ref_"):
        apply_referral_on_start(user, args[4:], users)

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


@router.message(Command("danil_test_messi"))
async def danil_test_messi(m: Message):
    """Секретная команда: разблокировать все уровни и разделы для проверки."""
    from handlers.keyboards import lessons_home_levels
    from services.database import MODE_LESSONS, set_mode
    from services.lesson_state import clear_lesson
    from services.growth import start_trial, extend_premium

    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)

    user["dev_unlock"] = True
    user["assessment_done"] = True
    user["level"] = "C2"
    user["step"] = "ready"
    user["assessment"] = {}
    user["mode"] = MODE_LESSONS
    start_trial(user, days=30)
    extend_premium(user, 30)
    save_users(users)
    clear_lesson(user_id)
    set_mode(user_id, MODE_LESSONS)

    users = load_users()
    user = get_user(users, user_id)
    await m.reply(
        "🔓 <b>DEV-режим включён</b>\n\n"
        "• тест уровня пропущен\n"
        "• уровень профиля: <b>C2</b>\n"
        "• открыты <b>все уровни A0–C2</b>\n"
        "• Grammar / Vocabulary и задания по всем уровням доступны\n\n"
        "Выбери уровень ниже и тестируй ⚽",
        reply_markup=lessons_home_levels(user=user, show_global_tasks=True),
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
        "🎁 Пригласить друга",
    }
    if not name or name.startswith("/") or len(name) > 40 or name in banned:
        await m.reply("🙂 Напиши просто своё имя текстом, например: <b>Даня</b>", parse_mode="HTML")
        return

    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    bind_referral_code(user_id, user)
    user["name"] = name
    user["step"] = "ready"
    user["mode"] = MODE_MENU
    grant_referral_bonuses(user_id, users)
    save_users(users)

    extra = ""
    if user.get("referred_by"):
        extra = f"\n\n🎁 Бонус за друга: +{REF_BONUS_DAYS} дня полного доступа!"

    await m.reply(
        WELCOME_AFTER_NAME.format(name=_esc(name)) + extra,
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
