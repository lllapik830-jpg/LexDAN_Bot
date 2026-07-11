from aiogram import Router, types
from services.gpt import ask_gpt
from services.translation import translate_to_language
from services.elevenlabs import elevenlabs_tts
from services.database import load_users, save_users, get_user
from handlers.keyboards import main_menu, translate_keyboard
import tempfile
import os
import logging

router = Router()

# --- ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ ---
@router.message()
async def chat_handler(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    # --- РЕГИСТРАЦИЯ: ИМЯ ---
    if user.get("step") == "name":
        user["name"] = m.text.strip()
        user["step"] = "language"
        save_users(users)
        await m.reply("🌐 *What is your native language?*\nType your language (e.g., Russian)", parse_mode="Markdown")
        return

    # --- РЕГИСТРАЦИЯ: ЯЗЫК ---
    if user.get("step") == "language":
        user["language"] = m.text.strip()
        user["step"] = "ready"
        save_users(users)

        welcome_en = (
            f"🌟 *Welcome, {user['name']}!*\n\n"
            f"🌐 Your native language: *{user['language']}*\n\n"
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
        await m.reply(welcome_en, parse_mode="Markdown", reply_markup=main_menu())
        return

    # --- ОБЫЧНОЕ ОБЩЕНИЕ ---
    if m.text and not m.text.startswith("/"):
        await m.reply("💬 Thinking...")
        answer_en = ask_gpt(m.text, user["name"])
        await m.reply(answer_en, reply_markup=translate_keyboard(user["language"]))

        # --- ОЗВУЧКА ОТВЕТА ---
        audio_bytes = elevenlabs_tts(answer_en)
        if audio_bytes:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(audio_bytes)
                    path = f.name
                await m.reply_voice(types.FSInputFile(path))
                os.unlink(path)
            except Exception as e:
                logging.error(f"TTS error: {e}")