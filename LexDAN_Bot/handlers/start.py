"""
Старт и регистрация имени + рефералка + правила.
Онбординг (часть 1): привет → CTA → имя → подтверждение → Погнали → тест → подарок + Огонь дня.
"""

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

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
)
from services.moderation import (
    BTN_ACCEPT_RULES,
    BTN_NAME_SURE,
    RULES_HTML,
    ensure_moderation,
    guard_user_text,
    is_banned,
    ban_remaining_text,
)

router = Router()

HELLO_NEW = (
    "👋 <b>Привет!</b> Я <b>LexDan</b>, а рядом всегда мой попугай <b>Рико</b> 🦜✨\n\n"
    "Здесь мы превращаем английский из «😱 страшно сказать» в «💬 легко болтать».\n\n"
    "💚 <b>Наш рецепт простой:</b> 15 минут в день — болтовня, слова, грамматика. "
    "Без стресса, в твоём темпе.\n\n"
    "🎯 Давай проверим твой уровень? Это 3–4 минуты."
)

HELLO_RICO_VOICE_EN = (
    "Hey! I'm LexDan, and this is my parrot Rico. "
    "We'll turn your English from scary to easy. Let's go!"
)

ASK_NAME_RICO = (
    "🦜 <b>Рико:</b> «Отлично! Прежде чем начать, давай познакомимся поближе.\n"
    "Как тебя зовут?»"
)

NAME_CONFIRM = (
    "Приятно познакомиться, <b>{name}</b>! 💚\n\n"
    "🦜 <b>Рико:</b> «Хочу убедиться, что правильно расслышал. "
    "Мне нужно только твоё имя, а не фразы вроде «Hello, I'm Ann».»\n\n"
    "Если всё верно — жми кнопку 👇"
)

PRE_TEST_HTML = (
    "Супер! Тогда начинаем 🎯\n\n"
    "📝 Сейчас будет небольшой тест. Отвечай как умеешь — здесь нет ошибок, "
    "это просто проверка твоего уровня, чтобы качественнее подобрать тебе задания!\n"
    "После прохождения тебя будет ждать подарок 🎁"
)

WELCOME_AGAIN = (
    "Снова привет, {name}! 🦜 Чем займёмся сегодня?"
)

# Карта главного меню (может пригодиться позже)
NAV_MAP_HTML = (
    "🗺 <b>Карта бота — куда жать</b>\n\n"
    "🗣️ <b>Общаться</b> — живой чат с Рико на английском "
    "(текст и голос). Внутри: перевод реплики и выбор голоса озвучки.\n\n"
    "📚 <b>Уроки</b> — основной путь обучения. Сначала уровни A0–C2, "
    "внутри каждого:\n"
    "· 📘 <b>Grammar</b> — темы и задания + помощь Рико\n"
    "· 📗 <b>Vocabulary</b> — слова и фразы с практикой\n"
    "· 🎧 <b>Listening</b> — диалоги и задания на слух\n"
    "· 📖 <b>Reading</b> — тексты и понимание\n\n"
    "🔥 <b>Огонь дня</b> — короткий микс на сегодня "
    "(слово / фраза / голос / факт).\n\n"
    "📊 <b>Профиль</b> — имя, подписка, стрик, рефералка, промокод.\n\n"
    "Готов? Выбирай кнопку в меню и вперёд 🚀"
)

BTN_ONBOARD_CHECK_LEVEL = "🎯 Проверить уровень"
BTN_NAME_YES = "✅ Да, это моё имя"
BTN_NAME_REDO = "✍️ Написать заново"
BTN_ONBOARD_GO = "✅ Погнали!"
BTN_ONBOARD_DAILY_FIRE = "🔥 Огонь дня"


def _rules_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_ACCEPT_RULES)]],
        resize_keyboard=True,
    )


def _hello_cta_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BTN_ONBOARD_CHECK_LEVEL,
                    callback_data="onboard:check_level",
                )
            ]
        ]
    )


def _name_confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BTN_NAME_YES,
                    callback_data="name_confirm:yes",
                )
            ],
            [
                InlineKeyboardButton(
                    text=BTN_NAME_REDO,
                    callback_data="name_confirm:redo",
                )
            ],
        ]
    )


def _pre_test_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BTN_ONBOARD_GO,
                    callback_data="onboard:go_test",
                )
            ]
        ]
    )


def _post_test_fire_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BTN_ONBOARD_DAILY_FIRE,
                    callback_data="onboard:daily_fire",
                )
            ]
        ]
    )


def _esc(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _banned_name_tokens() -> set[str]:
    return {
        "🗣️ Общаться",
        "📚 Уроки",
        "📊 Профиль",
        "🆘 Поддержка",
        "🌍 Перевести",
        "🔙 Вернуться в меню",
        "💎 Подписка",
        "🎁 Пригласить друга",
        BTN_ACCEPT_RULES,
        BTN_NAME_SURE,
        BTN_NAME_YES,
        BTN_NAME_REDO,
        BTN_ONBOARD_CHECK_LEVEL,
        BTN_ONBOARD_GO,
        "✏️ Изменить имя",
        "🎟 Промокод",
    }


async def _ask_name_after_cta(m: Message, user_id: str) -> None:
    users = load_users()
    user = get_user(users, user_id)
    user["step"] = "awaiting_name"
    save_users(users, only=user_id)
    await m.answer(ASK_NAME_RICO, parse_mode="HTML")


async def _send_pre_test(m: Message, user_id: str, name: str) -> None:
    """После подтверждения имени — экран перед тестом (подарок обещаем, выдадим после теста)."""
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    ensure_moderation(user)
    bind_referral_code(user_id, user)
    user["name"] = name
    user["pending_name"] = ""
    user["rules_accepted"] = True  # часть 1: без отдельного экрана правил
    user["mode"] = MODE_MENU
    user["step"] = "awaiting_onboard_go"
    from services.onboard_guided import ensure_onboard, ensure_live_onboard, is_onboard_locked

    ensure_live_onboard(user)
    if is_onboard_locked(user):
        ensure_onboard(user)["stage"] = "pre_test"
    grant_referral_bonuses(user_id, users)
    save_users(users, only=user_id)

    await m.answer(PRE_TEST_HTML, reply_markup=_pre_test_kb(), parse_mode="HTML")
    from aiogram.types import ReplyKeyboardRemove

    if is_onboard_locked(user):
        # Убрать reply-меню без лишнего текста
        rm = await m.answer(".", reply_markup=ReplyKeyboardRemove())
        try:
            await m.bot.delete_message(m.chat.id, rm.message_id)
        except Exception:
            pass
    else:
        await m.answer("👇", reply_markup=main_menu(user, user_id=user_id))


# ─── legacy helpers (промо/правила — оставляем для тех, кто уже в середине старого флоу) ───


async def _finish_registration(m: Message, user_id: str, name: str) -> None:
    """Старый путь: имя → промо. Новый онбординг идёт через _send_pre_test."""
    await _send_pre_test(m, user_id, name)


async def _ask_rules_after_promo(m: Message, user_id: str, *, promo_msg: str = "") -> None:
    users = load_users()
    user = get_user(users, user_id)
    user["step"] = "awaiting_rules"
    user["pending_promo_msg"] = promo_msg or ""
    save_users(users, only=user_id)
    await m.answer(
        "Отлично! Теперь коротко про правила — это важно 👇",
        reply_markup=_rules_kb(),
    )
    await m.answer(RULES_HTML, reply_markup=_rules_kb(), parse_mode="HTML")


async def _send_welcome_after_promo(m: Message, user_id: str, *, promo_msg: str = "") -> None:
    """Старый welcome после правил → теперь тоже ведём на pre-test."""
    users = load_users()
    user = get_user(users, user_id)
    name = (user.get("name") or "друг").strip()
    user["rules_accepted"] = True
    user.pop("pending_promo_msg", None)
    save_users(users, only=user_id)
    if promo_msg:
        await m.answer(promo_msg, parse_mode="HTML")
    await _send_pre_test(m, user_id, name)


@router.message(Command("start"))
async def start_cmd(m: Message, command: CommandObject = None):
    import time

    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    ensure_moderation(user)
    bind_referral_code(user_id, user)
    user["mode"] = MODE_MENU
    user["last_start_at"] = time.time()

    args = (command.args if command else None) or ""
    if args.startswith("ref_"):
        apply_referral_on_start(user, args[4:], users)

    if is_banned(user):
        save_users(users, only=user_id)
        await m.answer(ban_remaining_text(user), parse_mode="HTML")
        return

    # Новый пользователь: привет + CTA (имя спросим после кнопки)
    if not user.get("name"):
        from services.onboard_guided import ensure_live_onboard

        ensure_live_onboard(user)
        user["step"] = "awaiting_onboard_cta"
        save_users(users, only=user_id)
        await m.answer(HELLO_NEW, reply_markup=_hello_cta_kb(), parse_mode="HTML")
        from services.elevenlabs import send_rico_voice

        await send_rico_voice(
            m, HELLO_RICO_VOICE_EN, user=user, title="Rico · hello"
        )
        return

    if user.get("step") == "awaiting_onboard_cta":
        from services.onboard_guided import ensure_live_onboard

        ensure_live_onboard(user)
        save_users(users, only=user_id)
        await m.answer(HELLO_NEW, reply_markup=_hello_cta_kb(), parse_mode="HTML")
        from services.elevenlabs import send_rico_voice

        await send_rico_voice(
            m, HELLO_RICO_VOICE_EN, user=user, title="Rico · hello"
        )
        return

    if user.get("step") == "awaiting_onboard_go":
        save_users(users, only=user_id)
        await m.answer(PRE_TEST_HTML, reply_markup=_pre_test_kb(), parse_mode="HTML")
        return

    if user.get("step") == "awaiting_promo":
        from services.promo import BTN_SKIP_PROMO

        save_users(users, only=user_id)
        await m.answer(
            "Если есть промокод — введи его. Или нажми «Пропустить».",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=BTN_SKIP_PROMO)]],
                resize_keyboard=True,
            ),
        )
        return

    if not user.get("rules_accepted"):
        user["step"] = "awaiting_rules"
        save_users(users, only=user_id)
        await m.answer(RULES_HTML, reply_markup=_rules_kb(), parse_mode="HTML")
        return

    user["step"] = "ready"
    save_users(users, only=user_id)
    await m.answer(
        WELCOME_AGAIN.format(name=user["name"]),
        reply_markup=main_menu(user, user_id=user_id),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "onboard:check_level")
async def onboard_check_level(c: CallbackQuery):
    """Первая кнопка после /start → знакомство (имя)."""
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    ensure_moderation(user)

    if user.get("name") and user.get("assessment_done"):
        from handlers.lessons import send_lessons_home
        from services.database import MODE_LESSONS, set_mode

        set_mode(uid, MODE_LESSONS)
        await c.message.answer("Тест уже пройден — открываю уроки 👇")
        await send_lessons_home(c.message)
        return

    if user.get("name") and user.get("step") == "awaiting_onboard_go":
        await c.message.answer(PRE_TEST_HTML, reply_markup=_pre_test_kb(), parse_mode="HTML")
        return

    if user.get("name"):
        # Имя есть, теста нет — сразу к pre-test
        await _send_pre_test(c.message, uid, user["name"])
        return

    try:
        await c.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await _ask_name_after_cta(c.message, uid)


@router.callback_query(F.data == "onboard:go_test")
async def onboard_go_test(c: CallbackQuery):
    """Кнопка «Погнали!» → вступительный тест."""
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    ensure_moderation(user)

    if not user.get("name"):
        await c.message.answer("Сначала напиши, как тебя зовут 🙂")
        await _ask_name_after_cta(c.message, uid)
        return

    if user.get("assessment_done") or user.get("dev_unlock"):
        from handlers.lessons import send_lessons_home
        from services.database import MODE_LESSONS, set_mode

        set_mode(uid, MODE_LESSONS)
        await c.message.answer("Тест уровня уже пройден — открываю уроки 👇")
        await send_lessons_home(c.message)
        return

    user["step"] = "ready"
    user["rules_accepted"] = True
    from services.onboard_guided import ensure_live_onboard

    ensure_live_onboard(user)
    save_users(users, only=uid)

    try:
        await c.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    from handlers.lessons import start_level_test_flow
    from services.database import MODE_LESSONS, set_mode

    set_mode(uid, MODE_LESSONS)
    await start_level_test_flow(c.message, skip_intro=True, user_id=uid)


@router.callback_query(F.data == "onboard:daily_fire")
async def onboard_daily_fire(c: CallbackQuery):
    """После теста — переход в Огонь дня."""
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    from services.database import MODE_DAILY_FIRE, set_mode, users_for
    from services.daily_fire import ensure_daily_fire, hub_intro
    from handlers.daily_fire import daily_fire_kb
    from services.growth import note_lesson_activity

    set_mode(uid, MODE_DAILY_FIRE)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    note_lesson_activity(user)
    ensure_daily_fire(user)
    save_users(users, only=uid)
    try:
        await c.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await c.message.answer(
        hub_intro(user),
        reply_markup=daily_fire_kb(user),
        parse_mode="HTML",
    )
    from services.onboard_guided import ensure_onboard, is_guided_onboard, onboard_stage

    if is_guided_onboard(user) and onboard_stage(user) == "daily_fire":
        users = users_for(uid)
        user = get_user(users, uid)
        ensure_onboard(user)["df_intro_sent"] = True
        save_users(users, only=uid)


@router.callback_query(F.data == "onboard:level_test")
async def onboard_level_test_legacy(c: CallbackQuery):
    """Старая кнопка — направляем в новый флоу."""
    await onboard_check_level(c)


@router.message(Command("danil_test_messi"))
async def danil_test_messi(m: Message):
    """Секретная команда: разблокировать все уровни и разделы для проверки (только MANAGER)."""
    from config import MANAGER_ID
    from handlers.keyboards import lessons_home_levels
    from services.database import MODE_LESSONS, set_mode
    from services.lesson_state import clear_lesson
    from services.growth import start_trial, extend_premium

    if not m.from_user or m.from_user.id != MANAGER_ID:
        return

    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    ensure_moderation(user)

    user["dev_unlock"] = True
    user["assessment_done"] = True
    user["rules_accepted"] = True
    user["level"] = "C2"
    user["grammar_unlock_ceiling"] = "C2"
    user["step"] = "ready"
    user["assessment"] = {}
    user["mode"] = MODE_LESSONS
    start_trial(user, days=30)
    extend_premium(user, 30)
    save_users(users, only=user_id)
    clear_lesson(user_id)
    set_mode(user_id, MODE_LESSONS)

    users = load_users()
    user = get_user(users, user_id)
    await m.answer(
        "🔓 <b>DEV-режим включён</b>\n\n"
        "• тест уровня пропущен\n"
        "• уровень профиля: <b>C2</b>\n"
        "• открыты <b>все уровни A0–C2</b>\n"
        "• Grammar / Vocabulary и задания по всем уровням доступны\n\n"
        "Выбери уровень ниже и тестируй ⚽",
        reply_markup=lessons_home_levels(user=user, show_global_tasks=True),
        parse_mode="HTML",
    )


@router.message(StepFilter("awaiting_rules"), F.text == BTN_ACCEPT_RULES)
async def accept_rules(m: Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_moderation(user)
    user["rules_accepted"] = True
    promo_msg = (user.get("pending_promo_msg") or "").strip()
    user.pop("pending_promo_msg", None)

    if user.get("name"):
        save_users(users, only=user_id)
        await _send_welcome_after_promo(m, user_id, promo_msg=promo_msg)
        return

    user["step"] = "awaiting_name"
    save_users(users, only=user_id)
    await m.answer(ASK_NAME_RICO, parse_mode="HTML")


@router.message(StepFilter("awaiting_rules"))
async def rules_nudge(m: Message):
    await m.answer(
        "Сначала прими правила — кнопка <b>✅ Принимаю правила</b> ниже.",
        reply_markup=_rules_kb(),
        parse_mode="HTML",
    )


@router.message(StepFilter("awaiting_onboard_cta"))
async def onboard_cta_nudge(m: Message):
    await m.answer(
        "Жми кнопку <b>🎯 Проверить уровень</b> под приветствием — "
        "сначала познакомимся, потом тест 🙂",
        reply_markup=_hello_cta_kb(),
        parse_mode="HTML",
    )


@router.message(StepFilter("awaiting_onboard_go"))
async def onboard_go_nudge(m: Message):
    await m.answer(
        "Жми <b>✅ Погнали!</b> под сообщением про тест 👇",
        reply_markup=_pre_test_kb(),
        parse_mode="HTML",
    )


@router.message(StepFilter("awaiting_name"), F.text)
async def save_name_draft(m: Message):
    name = (m.text or "").strip()
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_moderation(user)

    if not await guard_user_text(m, user, name):
        return

    if (
        not name
        or name.startswith("/")
        or len(name) > 40
        or name in _banned_name_tokens()
    ):
        await m.answer(
            "🙂 Напиши просто своё имя текстом, например: <b>Даня</b>",
            parse_mode="HTML",
        )
        return

    user["pending_name"] = name
    user["step"] = "awaiting_name_confirm"
    save_users(users, only=user_id)
    await m.answer(
        NAME_CONFIRM.format(name=_esc(name)),
        reply_markup=_name_confirm_kb(),
        parse_mode="HTML",
    )


@router.message(StepFilter("awaiting_name"))
async def name_not_text(m: Message):
    await m.answer("🙂 Напиши своё имя обычным текстом, например: Даня")


@router.message(StepFilter("awaiting_name_confirm"), F.text)
async def rename_during_confirm(m: Message):
    """Если ошибся — можно сразу написать имя ещё раз."""
    name = (m.text or "").strip()
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_moderation(user)

    if name == BTN_ACCEPT_RULES:
        return
    if not await guard_user_text(m, user, name):
        return
    if (
        not name
        or name.startswith("/")
        or len(name) > 40
        or name in _banned_name_tokens()
    ):
        await m.answer(
            "🙂 Напиши только имя, например: <b>Анна</b>",
            parse_mode="HTML",
        )
        return

    user["pending_name"] = name
    save_users(users, only=user_id)
    await m.answer(
        NAME_CONFIRM.format(name=_esc(name)),
        reply_markup=_name_confirm_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "name_confirm:redo")
async def name_confirm_redo(c: CallbackQuery):
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    user["pending_name"] = ""
    user["step"] = "awaiting_name"
    save_users(users, only=uid)
    try:
        await c.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await c.message.answer(ASK_NAME_RICO, parse_mode="HTML")


@router.callback_query(F.data == "name_confirm:yes")
async def name_confirm_yes(c: CallbackQuery):
    user_id = str(c.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    name = (user.get("pending_name") or "").strip()
    if not name:
        await c.answer("Сначала напиши имя текстом", show_alert=True)
        return
    await c.answer()
    if c.message:
        try:
            await c.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
        await _send_pre_test(c.message, user_id, name)
    else:
        await c.bot.send_message(int(user_id), "Напиши /start ещё раз.")


@router.message(StepFilter("awaiting_promo"), F.text)
async def promo_after_registration(m: Message):
    from services.promo import BTN_SKIP_PROMO, apply_promo

    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    ensure_moderation(user)
    text = (m.text or "").strip()

    if text == BTN_SKIP_PROMO:
        save_users(users, only=user_id)
        await _ask_rules_after_promo(m, user_id)
        return

    if text.startswith("/"):
        await m.answer("Введи промокод или нажми «Пропустить».")
        return

    if not await guard_user_text(m, user, text):
        return

    ok, msg = apply_promo(user, text)
    save_users(users, only=user_id)
    if not ok:
        await m.answer(msg, parse_mode="HTML")
        return
    await _ask_rules_after_promo(m, user_id, promo_msg=msg)


@router.message(StepFilter("awaiting_promo"))
async def promo_nudge(m: Message):
    from services.promo import BTN_SKIP_PROMO
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    await m.answer(
        "Введи промокод текстом или нажми «Пропустить».",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=BTN_SKIP_PROMO)]],
            resize_keyboard=True,
        ),
    )


@router.message(StepFilter("awaiting_name_change"), F.text)
async def save_name_change(m: Message):
    from handlers.keyboards import profile_menu
    from services.rewards import user_plan
    import time

    name = (m.text or "").strip()
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_moderation(user)

    if name in ("🔙 Вернуться в меню", "📊 Профиль"):
        user["step"] = "ready"
        save_users(users, only=user_id)
        await m.answer("Ок, имя не меняем.", reply_markup=profile_menu(user, user_id=m.from_user.id))
        return

    if not await guard_user_text(m, user, name):
        return

    if not name or name.startswith("/") or len(name) > 40 or name in _banned_name_tokens():
        await m.answer("🙂 Напиши только новое имя, например: <b>Анна</b>", parse_mode="HTML")
        return

    plan = user_plan(user)
    now = time.time()
    last = float(user.get("name_changed_at") or 0)
    if plan != "full" and last and (now - last) < 30 * 86400:
        left = int((30 * 86400 - (now - last)) / 86400) + 1
        user["step"] = "ready"
        save_users(users, only=user_id)
        await m.answer(
            f"Имя на твоём тарифе можно менять раз в 30 дней.\n"
            f"Подожди ещё примерно <b>{left}</b> дн. "
            f"На тарифе 799₽ — безлимит смены имени.",
            reply_markup=profile_menu(user, user_id=m.from_user.id),
            parse_mode="HTML",
        )
        return

    user["name"] = name
    user["name_changed_at"] = now
    user["step"] = "ready"
    save_users(users, only=user_id)
    await m.answer(
        f"✅ Готово! Теперь ты <b>{_esc(name)}</b>.",
        reply_markup=profile_menu(user, user_id=m.from_user.id),
        parse_mode="HTML",
    )
