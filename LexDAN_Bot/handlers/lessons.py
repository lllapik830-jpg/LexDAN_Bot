from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from services.database import load_users, save_users, get_user
from handlers.keyboards import back_to_lessons_menu, lessons_menu
from data.lessons_data import LESSONS

router = Router()

# --- КОМАНДА /lesson ---
@router.message(Command("lesson"))
async def lesson_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    # Проверяем подписку (если нужно — раскомментировать)
    # if not is_premium(user_id):
    #     await m.reply("📚 *Уроки доступны только в Премиум-подписке!*", parse_mode="Markdown")
    #     return

    await m.reply("📚 *Выберите урок:*", parse_mode="Markdown", reply_markup=lessons_menu())

# --- ОБРАБОТЧИК ВЫБОРА УРОКА ---
@router.callback_query(lambda c: c.data.startswith("lesson_"))
async def show_lesson(callback: CallbackQuery):
    lesson_id = callback.data.split("_")[1]
    lesson = LESSONS.get(lesson_id)

    if not lesson:
        await callback.message.reply("❌ Урок не найден.")
        await callback.answer()
        return

    # Удаляем сообщение с кнопками
    await callback.message.delete()

    # Отправляем урок (части)
    for part in lesson["parts"]:
        await callback.message.reply(part, parse_mode="Markdown")

    # Кнопка "Вернуться"
    await callback.message.reply(
        "⬅️ *Вернуться к урокам*",
        parse_mode="Markdown",
        reply_markup=back_to_lessons_menu()
    )
    await callback.answer()

# --- ОБРАБОТЧИК "ВЕРНУТЬСЯ К УРОКАМ" ---
@router.callback_query(lambda c: c.data == "back_to_lessons")
async def back_to_lessons(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.reply("📚 *Выберите урок:*", parse_mode="Markdown", reply_markup=lessons_menu())
    await callback.answer()