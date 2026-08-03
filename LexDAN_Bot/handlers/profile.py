"""Раздел «Профиль» — статистика, подписка, рефералка, стрик."""

from aiogram import Router, F
from aiogram.types import Message

from handlers.filters import ModeFilter, StepFilter
from handlers.keyboards import profile_menu
from services.database import MODE_PROFILE, load_users, get_user, save_users
from services.growth import (
    BTN_RESTORE_STREAK,
    bind_referral_code,
    ensure_growth,
    restore_streak,
    subscription_blurb,
)
from services.rewards import (
    BTN_STREAK,
    BTN_REFERRAL,
    format_streak_rewards_message,
    format_referral_rewards_message,
)
from config import BOT_USERNAME
from services.promo import BTN_ENTER_PROMO

router = Router()


@router.message(ModeFilter(MODE_PROFILE), F.text == "✏️ Изменить имя")
async def change_name_start(m: Message):
    import time

    from services.rewards import user_plan
    from services.moderation import ensure_moderation

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    ensure_moderation(user)
    plan = user_plan(user)
    now = time.time()
    last = float(user.get("name_changed_at") or 0)
    if plan != "full" and last and (now - last) < 30 * 86400:
        left = int((30 * 86400 - (now - last)) / 86400) + 1
        await m.answer(
            f"На бесплатном и тарифе «Общение» имя можно менять <b>раз в 30 дней</b>.\n"
            f"Подожди ещё примерно <b>{left}</b> дн.\n"
            f"На тарифе <b>799₽</b> — безлимитная смена имени.",
            reply_markup=profile_menu(user, user_id=m.from_user.id),
            parse_mode="HTML",
        )
        return

    user["step"] = "awaiting_name_change"
    save_users(users, only=str(m.from_user.id))
    note = (
        "Безлимит смены имени на тарифе 799₽."
        if plan == "full"
        else "На твоём тарифе — не чаще раза в 30 дней."
    )
    await m.answer(
        f"✏️ Напиши новое имя (<b>только имя</b>, не фразу).\n{note}\n"
        "Или «🔙 Вернуться в меню», чтобы отменить.",
        parse_mode="HTML",
        reply_markup=profile_menu(user, user_id=m.from_user.id),
    )


@router.message(ModeFilter(MODE_PROFILE), F.text == "💎 Подписка")
async def subscription_info(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    from handlers.trial_notify import flush_trial_ended

    await flush_trial_ended(m, user, users, str(m.from_user.id))
    save_users(users, only=str(m.from_user.id))
    from handlers.lesson_keyboards import tariffs_inline_kb, upgrade_inline_kb
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from services.rewards import user_plan

    await m.answer(subscription_blurb(user), reply_markup=profile_menu(user, user_id=m.from_user.id), parse_mode="HTML")
    plan = user_plan(user)
    if plan == "free":
        rows = tariffs_inline_kb(user).inline_keyboard
        await m.answer(
            "Выбери тариф:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        )
    elif plan == "chat":
        await m.answer(
            "Хочешь уроки без лимита, все голоса и 150 тем?\n"
            "Апгрейд до полного доступа — доплата <b>399₽</b> (или со скидкой).",
            reply_markup=upgrade_inline_kb(user),
            parse_mode="HTML",
        )
        if user.get("sub_auto") and user.get("yookassa_payment_method_id"):
            await m.answer(
                "Управление подпиской:",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="⏹ Отключить автопродление",
                                callback_data="tariff:cancel_auto",
                            )
                        ]
                    ]
                ),
            )
    elif user.get("sub_auto") and user.get("yookassa_payment_method_id"):
        await m.answer(
            "Управление подпиской:",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="⏹ Отключить автопродление",
                            callback_data="tariff:cancel_auto",
                        )
                    ]
                ]
            ),
        )


@router.message(ModeFilter(MODE_PROFILE), F.text == BTN_ENTER_PROMO)
async def profile_promo_start(m: Message):
    from services.promo import BTN_SKIP_PROMO
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    user["step"] = "awaiting_promo_profile"
    save_users(users, only=str(m.from_user.id))
    await m.answer(
        "🎟 Введи промокод текстом.\n"
        "Или нажми «Пропустить», чтобы вернуться в профиль.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=BTN_SKIP_PROMO)],
                [KeyboardButton(text="🔙 Вернуться в меню")],
            ],
            resize_keyboard=True,
        ),
    )


@router.message(StepFilter("awaiting_promo_profile"), F.text)
async def profile_promo_enter(m: Message):
    from services.promo import BTN_SKIP_PROMO, apply_promo
    from handlers.keyboards import profile_menu
    from services.database import MODE_PROFILE, MODE_MENU, set_mode
    from services.secret_missions import BTN_SECRET
    from services.collection import BTN_COLLECTION
    from services.event_magic import BTN_HALL_OF_FAME, BTN_LEADERBOARD
    from services.event_prize_delivery import BTN_LEGEND_TASK, BTN_MASTER_TASK, BTN_HUNTER_TASK
    from services.rewards import BTN_STREAK, BTN_REFERRAL
    from aiogram.dispatcher.event.bases import SkipHandler

    text = (m.text or "").strip()
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)

    # Меню / секреты / разделы — не считать промокодом
    menu_like = {
        BTN_SKIP_PROMO,
        "🔙 Вернуться в меню",
        "📊 Профиль",
        "🗣️ Общаться",
        "📚 Уроки",
        "🆘 Поддержка",
        BTN_SECRET,
        "💎 Подписка",
        BTN_STREAK,
        BTN_REFERRAL,
        BTN_ENTER_PROMO,
        BTN_COLLECTION,
        BTN_LEADERBOARD,
        BTN_HALL_OF_FAME,
        BTN_LEGEND_TASK,
        BTN_MASTER_TASK,
        BTN_HUNTER_TASK,
        "✏️ Изменить имя",
        "⬅️ В профиль",
    }
    if text in menu_like or text.startswith("🔐"):
        user["step"] = "ready"
        save_users(users, only=user_id)
        if text == BTN_SECRET:
            set_mode(user_id, MODE_MENU)
            raise SkipHandler
        if text == "🔙 Вернуться в меню":
            set_mode(user_id, MODE_MENU)
            raise SkipHandler
        set_mode(user_id, MODE_PROFILE)
        if text in (BTN_SKIP_PROMO, "📊 Профиль"):
            await m.answer("Ок, без промокода.", reply_markup=profile_menu(user, user_id=m.from_user.id))
            return
        raise SkipHandler

    if text.startswith("/"):
        await m.answer("Введи промокод текстом или нажми «Пропустить».")
        return

    from services.moderation import ensure_moderation, guard_user_text

    ensure_moderation(user)
    if not await guard_user_text(m, user, text):
        return

    ok, msg = apply_promo(user, text)
    user["step"] = "ready"
    save_users(users, only=user_id)
    set_mode(user_id, MODE_PROFILE)
    await m.answer(msg, reply_markup=profile_menu(user, user_id=m.from_user.id), parse_mode="HTML")


@router.message(ModeFilter(MODE_PROFILE), F.text == BTN_STREAK)
async def streak_rewards_info(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    save_users(users)
    await m.answer(
        format_streak_rewards_message(user),
        reply_markup=profile_menu(user, user_id=m.from_user.id),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_PROFILE), F.text == BTN_REFERRAL)
async def invite_friend(m: Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    bind_referral_code(user_id, user)
    save_users(users)
    await m.answer(
        format_referral_rewards_message(user, BOT_USERNAME),
        reply_markup=profile_menu(user, user_id=m.from_user.id),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_PROFILE), F.text == BTN_RESTORE_STREAK)
async def restore_streak_btn(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    ok, text = restore_streak(user)
    save_users(users)
    await m.answer(text, reply_markup=profile_menu(user, user_id=m.from_user.id), parse_mode="HTML")


@router.message(ModeFilter(MODE_PROFILE))
async def profile_foolproof(m: Message):
    from services.collection import BTN_COLLECTION
    from services.event_magic import BTN_HALL_OF_FAME, BTN_LEADERBOARD, is_event_active
    from services.event_prize_delivery import BTN_LEGEND_TASK, BTN_MASTER_TASK, BTN_HUNTER_TASK
    from aiogram.dispatcher.event.bases import SkipHandler

    text = (m.text or "").strip()
    # альбом / гонка / зал / призовые задания / цифры — другим хендлерам
    if text in (
        BTN_COLLECTION,
        BTN_LEADERBOARD,
        BTN_HALL_OF_FAME,
        BTN_LEGEND_TASK,
        BTN_MASTER_TASK,
        BTN_HUNTER_TASK,
        "⬅️ В профиль",
    ) or text.isdigit():
        raise SkipHandler

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    save_users(users, only=str(m.from_user.id))
    bits = ["Подписка", "Гонка лидеров", "Зал славы"]
    if is_event_active():
        bits.insert(1, "Магические элементы")
    await m.answer(
        "🙂 В профиле: " + ", ".join(bits) + ", "
        "Изменить имя, Промокод, Серия дней, Пригласить друга.",
        reply_markup=profile_menu(user, user_id=m.from_user.id),
    )
