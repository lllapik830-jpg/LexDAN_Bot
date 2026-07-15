"""Раздел «Профиль» — статистика, подписка, рефералка, стрик-сейф."""

from aiogram import Router, F
from aiogram.types import Message

from handlers.filters import ModeFilter
from handlers.keyboards import profile_menu
from services.database import MODE_PROFILE, load_users, get_user, save_users
from services.growth import (
    BTN_RESTORE_STREAK,
    bind_referral_code,
    ensure_growth,
    invite_link,
    restore_streak,
    subscription_blurb,
)
from config import BOT_USERNAME

router = Router()


@router.message(ModeFilter(MODE_PROFILE), F.text == "💎 Подписка")
async def subscription_info(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    save_users(users)
    await m.reply(subscription_blurb(user), reply_markup=profile_menu(user), parse_mode="HTML")


@router.message(ModeFilter(MODE_PROFILE), F.text == "🎁 Пригласить друга")
async def invite_friend(m: Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    code = bind_referral_code(user_id, user)
    save_users(users)
    link = invite_link(BOT_USERNAME, code)
    await m.reply(
        "🎁 <b>Приведи друга</b>\n\n"
        "Отправь ссылку другу. Когда он запустит бота и напишет имя — "
        "вы оба получите <b>+3 дня</b> полного доступа.\n\n"
        f"🔗 <code>{link}</code>\n\n"
        "Можно кинуть в чат/сторис: "
        "«Учу английский 15 мин/день с Рико 🦜»",
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
    await m.reply(text, reply_markup=profile_menu(user), parse_mode="HTML")


@router.message(ModeFilter(MODE_PROFILE))
async def profile_foolproof(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    save_users(users)
    await m.reply(
        "🙂 В профиле доступны кнопки ниже.",
        reply_markup=profile_menu(user),
    )
