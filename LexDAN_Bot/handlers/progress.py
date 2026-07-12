from aiogram import Router, types
from aiogram.filters import Command
from services.database import load_users, get_user
from handlers.keyboards import main_menu

router = Router()

@router.message(Command("progress"))
async def progress_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)

    if is_premium(user_id):
        await m.reply(
            f"📊 *Your progress:*\n\n"
            f"✅ Premium active\n"
            f"📚 Lessons done: {user.get('lessons_done', 0)}\n"
            f"📝 Words learned: {user.get('words_learned', 0)}",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    else:
        await m.reply(
            "📊 *Free plan.*\n\n"
            "🎤 20 free voice messages/day.\n"
            "💎 Buy subscription to remove limits.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

def is_premium(user_id):
    users = load_users()
    user = users.get(user_id, {})
    premium_until = user.get("premium_until", 0)
    import time
    return time.time() < premium_until
