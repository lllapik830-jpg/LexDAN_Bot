from aiogram import Router, types
from handlers.keyboards import back_to_menu

router = Router()

# --- ОБРАБОТЧИК ГОЛОСОВЫХ СООБЩЕНИЙ (ЗАГЛУШКА) ---
@router.message(lambda m: m.voice is not None)
async def voice_handler(m: types.Message):
    await m.reply(
        "🎧 Голосовые сообщения пока в разработке.\n"
        "Скоро я научусь их распознавать и отвечать голосом! 🚀",
        reply_markup=back_to_menu()
    )