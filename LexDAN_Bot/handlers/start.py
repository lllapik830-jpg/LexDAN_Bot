from aiogram import Router, types
from aiogram.filters import Command
from datetime import date
from services.database import load_users, save_users, get_user
from handlers.keyboards import main_menu

router = Router()

@router.message(Command("start"))
async def start_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    if user.get("name") is None:
        user["step"] = "name"
        await m.reply("🤖 *Hello! I'm LexDAN, your AI English tutor.*\n\n📝 *What is your name?*", parse_mode="Markdown")
        return

    if user.get("language") is None:
        user["step"] = "language"
        await m.reply("🌐 *What is your native language?*\nType your language (e.g., Russian)", parse_mode="Markdown")
        return

    await m.reply(
        f"👋 Welcome back, *{user['name']}*!\n🌐 Language: *{user['language']}*\n\nChoose an option:",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@router.message(Command("reset"))
async def reset_cmd(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)

    if user_id in users:
        name = user.get("name", "Student")
        language = user.get("language", "Russian")
        premium_until = user.get("premium_until", 0)

        users[user_id] = {
            "name": name,
            "language": language,
            "level": "A1",
            "step": "ready",
            "premium_until": premium_until,
            "lessons_done": 0,
            "words_learned": 0,
            "voice_count": 0,
            "voice_date": date.today().isoformat()
        }
        save_users(users)

        await m.reply(
            f"🔄 *Data reset.*\n"
            f"Registration data saved ✅\n"
            f"Name: {name}\n"
            f"Language: {language}\n\n"
            "Progress reset. Subscription active.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    else:
        await m.reply("❌ No data to reset.")
