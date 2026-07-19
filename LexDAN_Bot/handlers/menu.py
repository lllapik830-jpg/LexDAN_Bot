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
from services.tg_out import say

router = Router()


@router.message(F.text == "🗣️ Общаться")
async def open_chat(m: Message):
    set_mode(str(m.from_user.id), MODE_CHAT)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    note_lesson_activity(user)
    # новая сессия — историю сбрасываем, но помним последнюю тему
    last_topic = (user.get("chat_last_user_text") or "").strip()
    user["chat_recent_turns"] = []
    user["chat_recent_replies"] = []
    save_users(users, only=str(m.from_user.id))

    intro = (
        "🔥 <b>Погнали общаться!</b> 🙂\n\n"
        "Пиши текстом или кидай голосовое на английском.\n"
        "Ошибёшься — поправлю <i>только грамматику/слова</i> и коротко объясню почему.\n"
        "Всё ок — скажу «молодец» и продолжим диалог ✨\n\n"
        "🎙 Можно <b>выбрать голос озвучки</b> (и бесплатно прослушать все) — "
        "кнопка ниже.\n\n"
        "Цель дня: можно закрыть, если поболтаешь несколько сообщений.\n\n"
        "🌍 <b>Перевести</b> — переведу мой последний ответ\n"
        "🎙 <b>Голос озвучки</b> — послушать и выбрать голос\n"
        "🔙 <b>В меню</b> — выход"
    )
    if last_topic:
        snippet = last_topic if len(last_topic) <= 120 else last_topic[:117] + "…"
        intro = (
            "🔥 <b>Снова на связи!</b>\n\n"
            f"В прошлый раз ты писал(а):\n<i>«{_esc(snippet)}»</i>\n\n"
            "Продолжим про это — или кидай новую тему 🙂\n\n"
            "🎙 Голос озвучки можно сменить в любой момент (прослушивание бесплатно).\n\n"
            "🌍 <b>Перевести</b> — мой последний ответ\n"
            "🎙 <b>Голос озвучки</b> — послушать и выбрать\n"
            "🔙 <b>В меню</b> — выход"
        )
    await say(m, intro, replace=True, delete_tap=True, reply_markup=chat_menu(), parse_mode="HTML")


def _esc(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
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

    from services.tg_out import purge, try_delete_user_tap

    await try_delete_user_tap(m)
    await purge(m.bot, user_id, chat_id=m.chat.id)

    if phase == "translate":
        a = user["assessment"]
        show_skip = a.get("translate_level") == "A0" and a.get("a0_second_shown")
        await say(
            m,
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
        await say(
            m,
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

    await say(
        m,
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
        replace=True,
        delete_tap=True,
        reply_markup=profile_menu(user),
        parse_mode="HTML",
    )
    await say(m, "👇", reply_markup=paywall_inline_kb())


@router.message(F.text == "🆘 Поддержка")
async def open_support(m: Message):
    from config import SUPPORT_USERNAME

    set_mode(str(m.from_user.id), MODE_MENU)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    if SUPPORT_USERNAME:
        contact = f"@{SUPPORT_USERNAME}"
        tip = f"🆘 По вопросам пиши: {contact}"
    else:
        tip = (
            "🆘 Поддержка скоро будет с личным контактом.\n"
            "Пока добавь в Render переменную <code>SUPPORT_USERNAME</code>."
        )
    await say(m, tip, replace=True, delete_tap=True, reply_markup=main_menu(user), parse_mode="HTML")


@router.message(ModeFilter(MODE_MENU), StepFilter("ready"), F.text)
async def menu_foolproof(m: Message):
    from handlers.keyboards import BTN_START_TODAY
    from aiogram.dispatcher.event.bases import SkipHandler

    if (m.text or "") == BTN_START_TODAY:
        raise SkipHandler
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await say(
        m,
        "🙂 Пожалуйста, выбери действие кнопкой ниже.",
        reply_markup=main_menu(user),
    )
