from aiogram import Router, types
from services.gpt import ask_gpt
from services.translation import translate_to_language
from services.database import load_users, save_users, get_user
from handlers.keyboards import main_menu, translate_keyboard

router = Router()

@router.message()
async def chat_handler(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    # --- ШАГ 1: ЗАПРОС ИМЕНИ ---
    if user.get("name") is None:
        user["name"] = m.text.strip()
        # --- УСТАНАВЛИВАЕМ ЯЗЫК ПО УМОЛЧАНИЮ (РУССКИЙ) ---
        user["language"] = "Russian"
        user["step"] = "ready"
        save_users(users)

        welcome_en = (
            f"🌟 *Welcome, {user['name']}!*\n\n"
            "🎯 *Your AI English tutor is ready to help you:*\n\n"
            "💬 *Chat in English* — practice anytime, get instant feedback.\n"
            "🎤 *Voice messages* — speak, listen, and improve your pronunciation.\n"
            "📚 *Structured lessons* — learn with proven methods, not random topics.\n"
            "✨ *Grammar check & correction* — I'll fix your mistakes and explain them.\n\n"
            "🔥 *Why LexDAN?*\n"
            "• No need to pay a tutor — I'm here 24/7.\n"
            "• Learn at your own pace with real materials.\n"
            "• Level up from A1 to C1 with clear progress.\n\n"
            "💎 You get *20 free voice messages* every day.\n"
            "Unlock unlimited learning with /upgrade.\n\n"
            "👇 *Choose what to do using the buttons below.*"
        )
        
        # --- СОХРАНЯЕМ ПЕРЕВОД ДЛЯ КНОПКИ ---
        translation_ru = translate_to_language(welcome_en, user["language"])
        if translation_ru:
            user_translations[user_id] = {"translation": translation_ru}
            
        await m.reply(
            welcome_en,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        # --- ОТДЕЛЬНОЕ СООБЩЕНИЕ С КНОПКОЙ ПЕРЕВОДА ---
        await m.reply(
            "📖 *Нажми кнопку ниже, чтобы прочитать это сообщение на русском.*",
            parse_mode="Markdown",
            reply_markup=translate_keyboard(user["language"])
        )
        return

    # --- ОСТАЛЬНАЯ ЛОГИКА (для зарегистрированных пользователей) ---
    if m.text and not m.text.startswith("/"):
        answer_en = ask_gpt(m.text, user["name"])
        # --- СОХРАНЯЕМ ПЕРЕВОД ОТВЕТА ---
        answer_ru = translate_to_language(answer_en, user["language"])
        if answer_ru:
            user_translations[user_id] = {"translation": answer_ru}
            
        await m.reply(
            answer_en,
            reply_markup=translate_keyboard(user["language"])
        )
