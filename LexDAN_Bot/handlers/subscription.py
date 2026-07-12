from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from services.database import load_users, save_users, get_user
from handlers.keyboards import subscription_keyboard
import time
from config import MANAGER_ID

router = Router()

@router.message(Command("upgrade"))
async def upgrade_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    await m.reply(
        "💎 *Choose your plan:*\n\n"
        "🔹 Unlimited (399 ₽) — unlimited voice + error correction\n"
        "🔹 Premium (799 ₽) — everything + lessons\n\n"
        "Click button below:",
        parse_mode="Markdown",
        reply_markup=subscription_keyboard()
    )

@router.message(Command("buy"))
async def buy_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    await m.reply(
        f"💎 *How to buy:*\n\n"
        f"1️⃣ Send money to card:\n"
        f"`1234 5678 9012 3456`\n\n"
        f"2️⃣ After payment, send screenshot with 'Paid'.\n"
        f"3️⃣ We'll activate within 5-10 minutes.\n\n"
        f"✅ Subscription valid for 30 days.",
        parse_mode="Markdown"
    )

@router.message(Command("activate"))
async def activate_cmd(m: types.Message):
    if m.from_user.id != MANAGER_ID:
        await m.reply("❌ You don't have permission.")
        return

    parts = m.text.split()
    if len(parts) < 2:
        await m.reply("❌ Usage: /activate 123456789")
        return

    target_user_id = parts[1]
    users = load_users()
    if target_user_id not in users:
        await m.reply(f"❌ User {target_user_id} not found.")
        return

    users[target_user_id]["premium_until"] = int(time.time()) + 30 * 24 * 60 * 60
    save_users(users)
    await m.reply(f"✅ Subscription activated for {target_user_id}!")

@router.callback_query(lambda c: c.data in ["buy_base", "buy_premium"])
async def subscription_buttons(callback: CallbackQuery):
    price = "399 ₽" if callback.data == "buy_base" else "799 ₽"
    await callback.message.reply(
        f"💎 *You chose {price}*\n\n"
        f"Send {price} to card:\n"
        f"`1234 5678 9012 3456`\n\n"
        f"Send screenshot with 'Paid'.",
        parse_mode="Markdown"
    )
    await callback.answer()
