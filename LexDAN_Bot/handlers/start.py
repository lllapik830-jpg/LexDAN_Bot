"""
Старт и регистрация имени + рефералка + правила.
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
    "Мы здесь, чтобы превратить твой английский из "
    "«😱 страшно сказать» в «💬 легко болтать».\n\n"
    "🍳 <b>Наш рецепт простой:</b>\n"
    "⏱ <b>15 минут в день</b> в Telegram — болтовня, слова, грамматика.\n"
    "😌 Без стресса, в твоём темпе, с Рико рядом.\n\n"
    "🤝 Сначала познакомимся — <b>как тебя зовут?</b>"
)

# Английская озвучка первого приветствия (дублирует смысл HELLO_NEW)
HELLO_NEW_EN = (
    "Hi! I'm LexDan, and my parrot Rico is always with me. "
    "We're here to turn your English from 'scary to speak' into 'easy to chat'. "
    "Our recipe is simple: fifteen minutes a day in Telegram — chatting, words, grammar. "
    "No stress, at your pace. First, let's get to know each other — what's your name?"
)

ASK_NAME = "🥰 Как мне тебя называть? Напиши <b>только имя</b>, например: <b>Анна</b>"

NAME_CONFIRM = (
    "Это точно твоё имя — <b>{name}</b>?\n\n"
    "Нужно написать <b>только имя</b>, а не фразу вроде «Hello, I'm Ann».\n"
    "Если ошибся — просто напиши имя ещё раз.\n"
    "Если всё верно — нажми кнопку ниже 👇"
)

WELCOME_AFTER_NAME = (
    "🎉 <b>Приятно познакомиться, {name}!</b> 🦜💛\n\n"
    "Я тут придумал для тебя план:\n\n"
    "1️⃣ Сначала <b>проверим уровень</b> — короткий тест, чтобы понять, с чего начать.\n"
    "2️⃣ Потом по чуть-чуть, минут по <b>15 в день</b>: слова, грамматика и разговоры.\n"
    "3️⃣ Серия дней и друзья дают бустеры и секреты Рико — смотри в <b>Профиле</b> 🔥\n\n"
    "📣 Канал <b>@LexDan_Rico</b> — обновления, конкурсы и промокоды:\n"
    "https://t.me/LexDan_Rico\n\n"
    "🎯 <b>Рико советует:</b> начни со вступительного теста уровня — "
    "так занятия сразу попадут в твою зону комфорта.\n"
    "Жми кнопку ниже 👇"
)

WELCOME_AGAIN = (
    "Снова привет, {name}! 🦜 Чем займёмся сегодня?"
)

# Карта главного меню (после теста уровня)
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
    "(грамматика / слова / аудирование), чтобы не пропускать серию.\n\n"
    "📊 <b>Профиль</b> — имя, подписка, стрик, рефералка, промокод; "
    "там же коллекция и лидеры ивента (когда активен).\n\n"
    "🆘 <b>Поддержка</b> — если что-то сломалось или нужна помощь.\n\n"
    "🔐 <b>Секрет Рико</b> — появляется как награда "
    "(серия / ивент) — особые миссии.\n\n"
    "Готов? Выбирай кнопку в меню и вперёд 🚀"
)

BTN_ONBOARD_LEVEL_TEST = "🎯 Пройти вступительный тест"


def _rules_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_ACCEPT_RULES)]],
        resize_keyboard=True,
    )


def _name_sure_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BTN_NAME_SURE, callback_data="name_confirm:yes")]
        ]
    )


def _onboard_assess_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BTN_ONBOARD_LEVEL_TEST,
                    callback_data="onboard:level_test",
                )
            ]
        ]
    )


async def _send_hello_new(m: Message, *, user: dict | None = None) -> None:
    """Текст приветствия + голос Рико на английском."""
    await m.answer(HELLO_NEW, parse_mode="HTML")
    try:
        from services.elevenlabs import send_rico_voice

        await send_rico_voice(
            m, HELLO_NEW_EN, user=user, title="Rico · hello"
        )
    except Exception:
        pass


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
        "✏️ Изменить имя",
        "🎟 Промокод",
    }


async def _finish_registration(m: Message, user_id: str, name: str) -> None:
    from services.promo import BTN_SKIP_PROMO
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    ensure_moderation(user)
    bind_referral_code(user_id, user)
    user["name"] = name
    user["pending_name"] = ""
    # правила — после промокода
    user["rules_accepted"] = False
    user["mode"] = MODE_MENU
    user["step"] = "awaiting_promo"
    grant_referral_bonuses(user_id, users)
    save_users(users, only=user_id)

    await m.answer(
        f"Приятно познакомиться, {_esc(name)}! 🦜\n\n"
        "Если есть <b>промокод</b> — введи его сейчас.\n"
        "Нет кода — нажми «Пропустить».",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=BTN_SKIP_PROMO)]],
            resize_keyboard=True,
        ),
        parse_mode="HTML",
    )


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
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    user["step"] = "ready"
    user["mode"] = MODE_MENU
    user["rules_accepted"] = True
    user.pop("pending_promo_msg", None)

    from services.reg_campaign import (
        grant_reg_full_trial_if_active,
        reg_full_trial_welcome_html,
        reg_event_welcome_html,
    )

    grant_reg_full_trial_if_active(user)
    save_users(users, only=user_id)

    extra = ""
    if user.get("referred_by"):
        extra = (
            "\n\n🎁 Ты пришёл по ссылке друга — сегодня больше баллов на уроки!"
        )
    if promo_msg:
        extra = "\n\n" + promo_msg + extra
    extra += reg_full_trial_welcome_html()
    extra += reg_event_welcome_html()

    name = user.get("name") or "друг"
    await m.answer(
        WELCOME_AFTER_NAME.format(name=_esc(name)) + extra,
        reply_markup=_onboard_assess_kb(),
        parse_mode="HTML",
    )
    await m.answer(
        "👇 Главное меню всегда снизу — а тест можно начать кнопкой выше.",
        reply_markup=main_menu(user, user_id=user_id),
    )


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

    # Имя → промо → правила → welcome
    if not user.get("name"):
        user["step"] = "awaiting_name"
        save_users(users, only=user_id)
        await _send_hello_new(m, user=user)
        await m.answer(ASK_NAME, parse_mode="HTML")
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


@router.callback_query(F.data == "onboard:level_test")
async def onboard_level_test(c: CallbackQuery):
    """Кнопка «Пройти вступительный тест» после регистрации."""
    await c.answer()
    if not c.from_user or not c.message:
        return
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    ensure_moderation(user)

    if not user.get("name") or not user.get("rules_accepted"):
        await c.message.answer(
            "Сначала закончи регистрацию — имя и правила 🙂",
            parse_mode="HTML",
        )
        return

    if user.get("assessment_done") or user.get("dev_unlock"):
        from handlers.lessons import send_lessons_home
        from services.database import MODE_LESSONS, set_mode

        set_mode(uid, MODE_LESSONS)
        await c.message.answer(
            "Тест уровня уже пройден — открываю уроки 👇",
            parse_mode="HTML",
        )
        await send_lessons_home(c.message)
        return

    from handlers.lessons import start_level_test_flow
    from services.database import MODE_LESSONS, set_mode

    set_mode(uid, MODE_LESSONS)
    await start_level_test_flow(c.message)


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
    await m.answer(ASK_NAME, parse_mode="HTML")


@router.message(StepFilter("awaiting_rules"))
async def rules_nudge(m: Message):
    await m.answer(
        "Сначала прими правила — кнопка <b>✅ Принимаю правила</b> ниже.",
        reply_markup=_rules_kb(),
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

    # Фразы вроде Hello, I'm Ann — мягко подскажем, но всё равно спросим подтверждение
    user["pending_name"] = name
    user["step"] = "awaiting_name_confirm"
    save_users(users, only=user_id)
    await m.answer(
        NAME_CONFIRM.format(name=_esc(name)),
        reply_markup=_name_sure_kb(),
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
        reply_markup=_name_sure_kb(),
        parse_mode="HTML",
    )


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
        await _finish_registration(c.message, user_id, name)
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
