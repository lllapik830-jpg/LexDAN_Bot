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
    save_users,
    set_mode,
    MODE_MENU,
    MODE_CHAT,
    MODE_LESSONS,
    MODE_PROFILE,
)
from services.assessment import ensure_user_fields
from services.lesson_state import count_completed_tasks
from services.growth import (
    bind_referral_code,
    ensure_growth,
    note_lesson_activity,
    profile_growth_lines,
    is_premium,
)
from config import BOT_USERNAME

router = Router()


@router.message(F.text == "🗣️ Общаться")
async def open_chat(m: Message):
    set_mode(str(m.from_user.id), MODE_CHAT)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    note_lesson_activity(user)
    save_users(users)
    await m.reply(
        "🔥 <b>Погнали общаться!</b> 🙂\n\n"
        "Пиши текстом или кидай голосовое на английском.\n"
        "Ошибёшься — поправлю <i>только грамматику/слова</i> и коротко объясню почему.\n"
        "Всё ок — скажу «молодец» и продолжим диалог ✨\n\n"
        "Цель дня: можно закрыть, если поболтаешь несколько сообщений.\n\n"
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
    ensure_growth(user)
    note_lesson_activity(user)
    save_users(users)
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
    from services.vocabulary_state import sync_vocab_counters
    from handlers.lesson_keyboards import paywall_inline_kb
    from services.growth import PRICE_CHAT_MONTH, PRICE_FULL_MONTH

    ensure_growth(user)
    bind_referral_code(user_id, user)
    sync_vocab_counters(user)
    save_users(users)

    name = user.get("name") or m.from_user.first_name or "Не указано"
    tasks_done = count_completed_tasks(user)
    words = user.get("words_learned", 0)
    phrases = user.get("phrases_learned", 0)
    growth = profile_growth_lines(user, BOT_USERNAME)
    sub = "триал/полный" if is_premium(user) else "бесплатно"

    await m.reply(
        "📊 <b>Твой профиль</b>\n\n"
        f"📛 Имя: {name}\n"
        f"✅ Пройдено заданий: {tasks_done}\n"
        f"📈 Уровень: {user.get('level', 'A1')}\n"
        f"📝 Слов выучено: {words}\n"
        f"💬 Фраз выучено: {phrases}\n"
        f"💎 Подписка: {sub}\n\n"
        f"{growth}\n\n"
        f"💳 Тарифы: общение <b>{PRICE_CHAT_MONTH}₽/мес</b> · "
        f"всё <b>{PRICE_FULL_MONTH}₽/мес</b>\n\n"
        "Если тебе понравилось — нажми «Выбрать тариф» и оплати доступ.",
        reply_markup=profile_menu(user),
        parse_mode="HTML",
    )
    await m.reply("👇", reply_markup=paywall_inline_kb())


@router.message(F.text == "🆘 Поддержка")
async def open_support(m: Message):
    from config import SUPPORT_USERNAME

    set_mode(str(m.from_user.id), MODE_MENU)
    if SUPPORT_USERNAME:
        contact = f"@{SUPPORT_USERNAME}"
        tip = f"🆘 По вопросам пиши: {contact}"
    else:
        tip = (
            "🆘 Поддержка скоро будет с личным контактом.\n"
            "Пока добавь в Render переменную <code>SUPPORT_USERNAME</code>."
        )
    await m.reply(tip, reply_markup=main_menu(), parse_mode="HTML")


@router.message(ModeFilter(MODE_MENU), StepFilter("ready"), F.text)
async def menu_foolproof(m: Message):
    from handlers.keyboards import BTN_START_TODAY
    from aiogram.dispatcher.event.bases import SkipHandler

    if (m.text or "") == BTN_START_TODAY:
        raise SkipHandler
    await m.reply(
        "🙂 Пожалуйста, выбери действие кнопкой ниже.",
        reply_markup=main_menu(),
    )
