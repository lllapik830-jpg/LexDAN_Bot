from aiogram import Router, types
from aiogram.filters import Command
from services.database import load_users, get_user
from handlers.keyboards import main_menu

router = Router()

# --- КОМАНДА /progress ---
@router.message(Command("progress"))
async def progress_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)

    # Проверяем подписку
    premium = is_premium(user_id)

    if premium:
        lessons_done = user.get("lessons_done", 0)
        words_learned = user.get("words_learned", 0)
        await m.reply(
            f"📊 *Твой прогресс:*\n\n"
            f"✅ Премиум активен\n"
            f"📚 Уроков пройдено: {lessons_done}\n"
            f"📝 Слов выучено: {words_learned}",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    else:
        await m.reply(
            "📊 *Ты на бесплатном тарифе.*\n\n"
            "🎤 Осталось голосовых на сегодня: 20\n"
            "💎 Купи подписку, чтобы снять лимиты.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

# --- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ (временная, пока нет общей) ---
def is_premium(user_id):
    users = load_users()
    user = users.get(user_id, {})
    premium_until = user.get("premium_until", 0)
    import time
    return time.time() < premium_until