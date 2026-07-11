from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from services.database import load_users, save_users, get_user
from handlers.keyboards import subscription_keyboard
import time
from config import MANAGER_ID

router = Router()

# --- КОМАНДА /upgrade ---
@router.message(Command("upgrade"))
async def upgrade_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    await m.reply(
        "💎 *Выберите подписку:*\n\n"
        "🔹 Безлимит (399 ₽) — голосовые без ограничений + исправление ошибок\n"
        "🔹 Премиум (799 ₽) — всё из безлимита + уроки по уровням\n\n"
        "Нажмите кнопку ниже:",
        parse_mode="Markdown",
        reply_markup=subscription_keyboard()
    )

# --- КОМАНДА /buy (инструкция по оплате) ---
@router.message(Command("buy"))
async def buy_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    await m.reply(
        f"💎 *Как купить подписку:*\n\n"
        f"1️⃣ Переведите нужную сумму на карту:\n"
        f"`1234 5678 9012 3456`\n\n"
        f"2️⃣ После перевода напишите «Оплатил» и пришлите скриншот.\n"
        f"3️⃣ Мы проверим и активируем подписку в течение 5–10 минут.\n\n"
        f"✅ Подписка действует 30 дней.",
        parse_mode="Markdown"
    )

# --- КОМАНДА /activate (только для менеджера) ---
@router.message(Command("activate"))
async def activate_cmd(m: types.Message):
    if m.from_user.id != MANAGER_ID:
        await m.reply("❌ У вас нет прав для этой команды.")
        return

    parts = m.text.split()
    if len(parts) < 2:
        await m.reply("❌ Укажите ID пользователя: /activate 123456789")
        return

    target_user_id = parts[1]
    users = load_users()
    if target_user_id not in users:
        await m.reply(f"❌ Пользователь с ID {target_user_id} не найден.")
        return

    users[target_user_id]["premium_until"] = int(time.time()) + 30 * 24 * 60 * 60
    save_users(users)
    await m.reply(f"✅ Подписка активирована для пользователя {target_user_id}!")

    try:
        await m.bot.send_message(
            target_user_id,
            f"🎉 *Подписка Premium активирована!*\n\n"
            f"✅ Доступ открыт на 30 дней.\n"
            f"Наслаждайтесь всеми функциями бота! 🚀",
            parse_mode="Markdown"
        )
    except Exception as e:
        await m.reply(f"⚠️ Не удалось отправить уведомление пользователю: {e}")

# --- ОБРАБОТЧИК КНОПОК ПОДПИСКИ (выбор тарифа) ---
@router.callback_query(lambda c: c.data in ["buy_base", "buy_premium"])
async def subscription_buttons(callback: CallbackQuery):
    price = "399 ₽" if callback.data == "buy_base" else "799 ₽"
    await callback.message.reply(
        f"💎 *Вы выбрали подписку за {price}*\n\n"
        f"Переведите {price} на карту:\n"
        f"`1234 5678 9012 3456`\n\n"
        f"После перевода пришлите сюда скриншот или напишите «Оплатил».",
        parse_mode="Markdown"
    )
    await callback.answer()