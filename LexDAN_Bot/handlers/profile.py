"""Раздел «Профиль» — статистика, подписка, рефералка, стрик."""

from aiogram import Router, F
from aiogram.types import Message

from handlers.filters import ModeFilter
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

router = Router()


@router.message(ModeFilter(MODE_PROFILE), F.text == "💎 Подписка")
async def subscription_info(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    save_users(users)
    from handlers.lesson_keyboards import tariffs_inline_kb
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    await m.answer(subscription_blurb(user), reply_markup=profile_menu(user), parse_mode="HTML")
    rows = tariffs_inline_kb(user).inline_keyboard
    if user.get("sub_auto") and user.get("yookassa_payment_method_id"):
        rows = list(rows) + [
            [InlineKeyboardButton(text="⏹ Отменить автопродление", callback_data="tariff:cancel_auto")]
        ]
    await m.answer(
        "Выбери тариф:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
    )


@router.message(ModeFilter(MODE_PROFILE), F.text == BTN_STREAK)
async def streak_rewards_info(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    save_users(users)
    await m.answer(
        format_streak_rewards_message(user),
        reply_markup=profile_menu(user),
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
        reply_markup=profile_menu(user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_PROFILE), F.text == BTN_RESTORE_STREAK)
async def restore_streak_btn(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    ok, text = restore_streak(user)
    save_users(users)
    await m.answer(text, reply_markup=profile_menu(user), parse_mode="HTML")


@router.message(ModeFilter(MODE_PROFILE))
async def profile_foolproof(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    save_users(users)
    await m.answer(
        "🙂 В профиле: Подписка, Серия дней, Пригласить друга.",
        reply_markup=profile_menu(user),
    )
