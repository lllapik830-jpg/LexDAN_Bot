from aiogram import Router, types
from aiogram.types import CallbackQuery
from services.database import load_users
from handlers.keyboards import back_to_lessons_menu, lessons_menu
from data.lessons_data import LESSONS

router = Router()
user_translations = {}

@router.callback_query()
async def handle_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    users = load_users()
    user_data = users.get(user_id, {})
    lang = user_data.get("language", "Russian")

    # --- КНОПКА ПЕРЕВОДА ---
    if callback.data == "translate":
        translation = user_translations.get(user_id, {}).get("translation")
        if translation:
            await callback.message.reply(f"🌐 {translation}")
        else:
            await callback.message.reply("❌ Перевод не найден.")
        await callback.answer()
        return

    # --- КНОПКИ УРОКОВ ---
    if callback.data.startswith("lesson_"):
        lesson_id = callback.data.split("_")[1]
        lesson = LESSONS.get(lesson_id)
        if lesson:
            await callback.message.delete()
            for part in lesson["parts"]:
                await callback.message.reply(part, parse_mode="Markdown")
            await callback.message.reply("⬅️ *Вернуться к урокам*", parse_mode="Markdown", reply_markup=back_to_lessons_menu())
        else:
            await callback.message.reply("❌ Урок не найден.")
        await callback.answer()
        return

    if callback.data == "back_to_lessons":
        await callback.message.delete()
        await callback.message.reply("📚 *Выберите урок:*", parse_mode="Markdown", reply_markup=lessons_menu())
        await callback.answer()
        return

    # --- КНОПКИ ПОДПИСКИ ---
    if callback.data in ["buy_base", "buy_premium"]:
        price = "399 ₽" if callback.data == "buy_base" else "799 ₽"
        await callback.message.reply(
            f"💎 *Вы выбрали подписку за {price}*\n\n"
            f"Переведите {price} на карту:\n`1234 5678 9012 3456`\n\n"
            f"После перевода пришлите сюда скриншот или напишите «Оплатил».",
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    await callback.message.reply("⚠️ Неизвестная команда.")
    await callback.answer()
