"""
Главное меню.
"""

from aiogram import Router, F
from aiogram.types import Message

from handlers.filters import ModeFilter, StepFilter
from handlers.keyboards import main_menu, chat_menu, profile_menu, assess_translate_kb, assess_simple_kb
from handlers.lessons import send_lessons_home
from services.database import (
    load_users,
    get_user,
    set_mode,
    MODE_MENU,
    MODE_CHAT,
    MODE_LESSONS,
    MODE_PROFILE,
)
from services.assessment import ensure_user_fields
from services.lesson_state import count_completed_tasks

router = Router()


@router.message(F.text == "🗣️ Общаться")
async def open_chat(m: Message):
    set_mode(str(m.from_user.id), MODE_CHAT)
    await m.reply(
        "🔥 <b>Погнали общаться!</b> 🙂\n\n"
        "Пиши текстом или кидай голосовое на английском.\n"
        "Ошибёшься — поправлю <i>только грамматику/слова</i> и коротко объясню почему.\n"
        "Всё ок — скажу «молодец» и продолжим диалог ✨\n\n"
        "⚠️ Будь внимателен: голосовые иногда приходят с небольшой задержкой.\n\n"
        "🌍 <b>Перевести</b> — переведу мой последний ответ\n"
        "🔙 <b>В меню</b> — выход",
        reply_markup=chat_menu(),
        parse_mode="HTML",
    )


@router.message(F.text == "📚 Уроки")
async def open_lessons(m: Message):
    user_id = str(m.from_user.id)
    set_mode(user_id, MODE_LESSONS)

    users = load_users()
    user = get_user(users, user_id)
    ensure_user_fields(user)
    phase = user["assessment"].get("phase")

    if phase == "translate":
        a = user["assessment"]
        show_skip = a.get("translate_level") == "A0" and a.get("a0_second_shown")
        await m.reply(
            "Продолжаем тест — задание 1/4: перевод.\n\n"
            f"🇬🇧 Текст:\n{a['translate_source_en']}",
            reply_markup=assess_translate_kb(show_skip=show_skip),
        )
        return

    if phase in {"vocab", "listen", "write"}:
        names = {
            "vocab": "словарь",
            "listen": "аудирование",
            "write": "письмо",
        }
        await m.reply(
            f"Продолжаем тест — {names.get(phase, 'задание')}. Пришли ответ текстом.",
            reply_markup=assess_simple_kb(),
        )
        return

    await send_lessons_home(m)


@router.message(F.text == "📊 Профиль")
async def open_profile(m: Message):
    set_mode(str(m.from_user.id), MODE_PROFILE)
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)

    name = user.get("name") or m.from_user.first_name or "Не указано"
    tasks_done = count_completed_tasks(user)
    words = user.get("words_learned", 0)
    phrases = user.get("phrases_learned", 0)

    await m.reply(
        "📊 Твой профиль:\n\n"
        f"📛 Имя: {name}\n"
        f"✅ Пройдено заданий: {tasks_done}\n"
        f"📈 Уровень: {user.get('level', 'A1')}\n"
        f"📝 Слов выучено: {words}\n"
        f"💬 Фраз выучено: {phrases}\n"
        f"💎 Подписка: бесплатно",
        reply_markup=profile_menu(),
    )


@router.message(F.text == "🆘 Поддержка")
async def open_support(m: Message):
    set_mode(str(m.from_user.id), MODE_MENU)
    await m.reply(
        "🆘 По вопросам пиши: @твой_ник",
        reply_markup=main_menu(),
    )


@router.message(ModeFilter(MODE_MENU), StepFilter("ready"), F.text)
async def menu_foolproof(m: Message):
    await m.reply(
        "🙂 Пожалуйста, выбери действие кнопкой ниже.",
        reply_markup=main_menu(),
    )
