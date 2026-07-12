from aiogram import Router, types
from services.database import load_users, save_users, get_user
from handlers.keyboards import main_menu, back_to_menu, profile_menu
from services.gpt import ask_gpt
from services.translation import translate_to_language
from services.elevenlabs import elevenlabs_tts
from aiogram.types import FSInputFile
from handlers.voice import user_last_message  # <-- импорт из voice.py
import tempfile
import os
import logging
import time

router = Router()

user_states = {}  # user_id: "chat" / "profile" / "lessons" / "menu"

@router.message()
async def chat_handler(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    # --- ШАГ 1: Пользователь пишет имя ---
    if user.get("step") == "awaiting_name":
        user["name"] = m.text.strip()
        user["step"] = "ready"
        save_users(users)

        welcome_text = (
            f"🎉 Привет, {user['name']}! Рад познакомиться!\n\n"
            "🧠 Вот что я умею:\n"
            "• 💬 Общаться на английском — я исправлю ошибки и подскажу, как сказать лучше.\n"
            "• 🎤 Распознавать голосовые сообщения и отвечать на них голосом.\n"
            "• 📚 Проводить короткие интерактивные уроки (5-7 минут) по твоему уровню.\n"
            "• 📊 Отслеживать твой прогресс — ты видишь, сколько слов выучил и уроков прошёл.\n\n"
            "🎯 Твоя цель: заниматься 15–20 минут в день.\n"
            "⏳ Через месяц ты заметишь результат.\n\n"
            "👇 Что означают кнопки:\n"
            "🗣️ Общаться — простое общение на английском с переводом и голосовыми сообщениями.\n"
            "📚 Уроки — изучай английский с помощью коротких интерактивных занятий.\n"
            "📊 Профиль — твой прогресс, уровень и статистика.\n"
            "🆘 Поддержка — если есть вопросы, жми на кнопку.\n\n"
            "👇 Выбери, с чего начнёшь:"
        )
        await m.reply(welcome_text, reply_markup=main_menu())
        return

    # --- ШАГ 2: Обработка кнопок ---
    current_state = user_states.get(user_id, "menu")
    
    if m.text == "🌍 Перевести":
        last_text = user_last_message.get(user_id)
        if last_text:
            translation = translate_to_language(last_text, "Russian")
            if translation:
                await m.reply(f"🌐 {translation}")
            else:
                await m.reply("❌ Не удалось перевести.")
        else:
            await m.reply("❌ Нет текста для перевода.")
        return

    if m.text == "🔙 Вернуться в меню":
        user_states[user_id] = "menu"
        await m.reply("🏠 Главное меню.", reply_markup=main_menu())
        return

    # --- ШАГ 3: РЕЖИМ ОБЩЕНИЯ (только текст) ---
    if current_state == "chat":
        if m.text and not m.text.startswith('/'):
            answer_en = ask_gpt(m.text, user.get("name", "Student"))
            user_last_message[user_id] = answer_en
            
            await m.reply(f"🇬🇧 {answer_en}")
            
            audio_bytes = elevenlabs_tts(answer_en)
            if audio_bytes:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                        f.write(audio_bytes)
                        path = f.name
                    await m.reply_voice(FSInputFile(path))
                    os.unlink(path)
                except Exception as e:
                    logging.error(f"TTS error: {e}")
            return

    # --- ШАГ 4: Обработка кнопок ---
    if m.text == "🗣️ Общаться":
        user_states[user_id] = "chat"
        await m.reply(
            "🗣️ Отправь мне голосовое или текстовое сообщение на английском.\n\n"
            "🔙 Вернуться в меню — кнопка ниже.\n"
            "🌍 Перевести последнее сообщение — тоже кнопка ниже.",
            reply_markup=back_to_menu()
        )
        return

    if m.text == "📚 Уроки":
        user_states[user_id] = "lessons"
        await m.reply("📚 Уроки в разработке.", reply_markup=back_to_menu())
        return

    if m.text == "📊 Профиль":
        user_states[user_id] = "profile"
        name = user.get("name", "Не указано")
        lessons_done = user.get("lessons_done", 0)
        words_learned = user.get("words_learned", 0)
        level = user.get("level", "A1")
        
        premium_until = user.get("premium_until", 0)
        subscription = "Золото" if time.time() < premium_until else "Серебро"

        profile_text = (
            f"📊 *Твой профиль:*\n\n"
            f"📛 Имя: {name}\n"
            f"📚 Пройдено уроков: {lessons_done}\n"
            f"📈 Уровень: {level}\n"
            f"📝 Слов выучено: {words_learned}\n"
            f"💎 Подписка: {subscription}"
        )
        await m.reply(profile_text, parse_mode="Markdown", reply_markup=profile_menu())
        return

    if m.text == "🆘 Поддержка":
        await m.reply("🆘 По всем вопросам пиши: @твой_ник")
        return

    if m.text == "💎 Подписка":
        await m.reply(
            "💎 *Тарифы:*\n\n"
            "🆓 *Серебро* — бесплатно (20 голосовых/день)\n"
            "🥇 *Золото* — 399 ₽ (безлимит)\n"
            "💎 *Бриллиант* — 799 ₽ (всё + уроки)\n\n"
            "Для покупки пиши в поддержку: @твой_ник",
            parse_mode="Markdown",
            reply_markup=profile_menu()
        )
        return

    # --- ШАГ 5: Текст без кнопки ---
    if m.text and not m.text.startswith('/'):
        await m.reply(
            "Пожалуйста, выбери действие с помощью кнопок ниже.",
            reply_markup=main_menu()
        )
        return