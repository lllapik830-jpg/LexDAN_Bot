from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from services.database import load_users, get_user
from handlers.keyboards import lessons_menu, back_to_lessons_menu
from data.lessons_data import LESSONS

router = Router()

@router.message(Command("lesson"))
async def lesson_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)

    await m.reply("📚 *Choose a lesson:*", parse_mode="Markdown", reply_markup=lessons_menu())

@router.callback_query(lambda c: c.data.startswith("lesson_"))
async def show_lesson(callback: CallbackQuery):
    lesson_id = callback.data.split("_")[1]
    lesson = LESSONS.get(lesson_id)

    if not lesson:
        await callback.message.reply("❌ Lesson not found.")
        await callback.answer()
        return

    await callback.message.delete()
    for part in lesson["parts"]:
        await callback.message.reply(part, parse_mode="Markdown")
    await callback.message.reply(
        "⬅️ *Back to lessons*",
        parse_mode="Markdown",
        reply_markup=back_to_lessons_menu()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "back_to_lessons")
async def back_to_lessons(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.reply("📚 *Choose a lesson:*", parse_mode="Markdown", reply_markup=lessons_menu())
    await callback.answer()
