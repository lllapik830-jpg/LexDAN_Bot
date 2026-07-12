from aiogram import Router, types
from aiogram.filters import Command
from handlers.keyboards import profile_menu, back_to_menu

router = Router()

# --- ОБРАБОТЧИК КНОПКИ "ПОДПИСКА" (В ПРОФИЛЕ) ---
@router.message(lambda m: m.text == "💎 Подписка")
async def subscription_handler(m: types.Message):
    await m.reply(
        "💎 *Тарифы:*\n\n"
        "🆓 *Серебро* — бесплатно (20 голосовых/день)\n"
        "🥇 *Золото* — 399 ₽ (безлимит голосовые + текст)\n"
        "💎 *Бриллиант* — 799 ₽ (всё из Золота + уроки)\n\n"
        "Чтобы купить подписку, напиши в поддержку: @твой_ник",
        parse_mode="Markdown",
        reply_markup=profile_menu()  # Оставляем те же кнопки (Подписка + Назад)
    )

# --- ОБРАБОТЧИК КОМАНДЫ /upgrade (если пользователь введёт вручную) ---
@router.message(Command("upgrade"))
async def upgrade_cmd(m: types.Message):
    await m.reply(
        "💎 *Тарифы:*\n\n"
        "🆓 *Серебро* — бесплатно (20 голосовых/день)\n"
        "🥇 *Золото* — 399 ₽ (безлимит голосовые + текст)\n"
        "💎 *Бриллиант* — 799 ₽ (всё из Золота + уроки)\n\n"
        "Чтобы купить подписку, напиши в поддержку: @твой_ник",
        parse_mode="Markdown"
    )