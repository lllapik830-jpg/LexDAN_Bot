from aiogram import Router, types
from handlers.keyboards import back_to_menu

router = Router()

@router.message(lambda m: m.text == "📚 Уроки")
async def lessons_placeholder(m: types.Message):
    await m.reply(
        "📚 Раздел «Уроки» сейчас в разработке.\n"
        "Скоро здесь появятся интерактивные занятия!\n"
        "Следи за обновлениями 🚀",
        reply_markup=back_to_menu()
    )