from aiogram import Router, types
from services.database import load_users, save_users, get_user
from handlers.keyboards import main_menu, back_to_menu, profile_menu
from services.gpt import ask_gpt
from services.translation import translate_to_language
from services.elevenlabs import elevenlabs_tts
from aiogram.types import FSInputFile
import speech_recognition as sr
from pydub import AudioSegment
import io
import tempfile
import os
import logging
import time

router = Router()

# --- ХРАНИЛИЩЕ СОСТОЯНИЙ И ПЕРЕВОДОВ ---
user_states = {}  # user_id: "chat" / "profile" / "lessons" / "menu"
user_translations = {}

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

    # --- ШАГ 2: Обработка кнопок (кроме "Вернуться") ---
    current_state = user_states.get(user_id, "menu")
    
    if m.text == "🔙 Вернуться в меню":
        user_states[user_id] = "menu"
        await m.reply(
            "🏠 Ты в главном меню. Выбери, что хочешь делать.",
            reply_markup=main_menu()
        )
        return

    # --- ШАГ 3: РЕЖИМ ОБЩЕНИЯ (ОБРАБАТЫВАЕТСЯ ПЕРВЫМ) ---
    if current_state == "chat":
        # --- ТЕКСТОВЫЕ СООБЩЕНИЯ ---
        if m.text and not m.text.startswith('/'):
            answer_en = ask_gpt(m.text, user.get("name", "Student"))
            answer_ru = translate_to_language(answer_en, "Russian")
            if answer_ru:
                user_translations[user_id] = {"translation": answer_ru}
            
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
            
            if answer_ru:
                await m.reply(f"🌐 {answer_ru}")
            return

        # --- ГОЛОСОВЫЕ СООБЩЕНИЯ (в режиме чата) ---
        if m.voice:
            await m.reply("🎧 Обрабатываю голосовое...")
            try:
                file = await bot.get_file(m.voice.file_id)
                voice_data = await bot.download_file(file.file_path)

                audio = AudioSegment.from_file(io.BytesIO(voice_data.read()), format="ogg")
                wav_bytes = io.BytesIO()
                audio.export(wav_bytes, format="wav")
                wav_bytes.seek(0)

                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_bytes) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="en-US")

                if text:
                    answer_en = ask_gpt(text, user.get("name", "Student"))
                    answer_ru = translate_to_language(answer_en, "Russian")
                    if answer_ru:
                        user_translations[user_id] = {"translation": answer_ru}

                    await m.reply(f"🗣️ Ты сказал: {text}\n\n🇬🇧 {answer_en}")
                    
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
                    
                    if answer_ru:
                        await m.reply(f"🌐 {answer_ru}")
                else:
                    await m.reply("Не удалось распознать речь. Попробуй ещё раз.")
            except sr.UnknownValueError:
                await m.reply("Не понял речь. Попробуй сказать чётче.")
            except Exception as e:
                logging.error(f"Voice error: {e}")
                await m.reply("Ошибка обработки голосового. Попробуй текстом.")
            return

        return

    # --- ШАГ 4: Обработка кнопок (только если в меню) ---
    if m.text == "🗣️ Общаться":
        user_states[user_id] = "chat"
        await m.reply(
            "🗣️ Отправь мне голосовое или текстовое сообщение на английском, "
            "я отвечу и переведу, если нужно.\n\n"
            "🔙 Чтобы вернуться — нажми кнопку ниже.",
            reply_markup=back_to_menu()
        )
        return

    if m.text == "📚 Уроки":
        user_states[user_id] = "lessons"
        await m.reply(
            "📚 Раздел «Уроки» сейчас в разработке.\n"
            "Скоро здесь появятся интерактивные занятия!\n"
            "Следи за обновлениями 🚀",
            reply_markup=back_to_menu()
        )
        return

    if m.text == "📊 Профиль":
        user_states[user_id] = "profile"
        name = user.get("name", "Не указано")
        lessons_done = user.get("lessons_done", 0)
        words_learned = user.get("words_learned", 0)
        level = user.get("level", "A1")
        
        premium_until = user.get("premium_until", 0)
        if time.time() < premium_until:
            subscription = "Золото"
        else:
            subscription = "Серебро"

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
        await m.reply(
            "🆘 По всем вопросам работы бота, подписке и прочему — пиши сюда: @твой_ник"
        )
        return

    if m.text == "💎 Подписка":
        await m.reply(
            "💎 *Тарифы:*\n\n"
            "🆓 *Серебро* — бесплатно (20 голосовых/день)\n"
            "🥇 *Золото* — 399 ₽ (безлимит голосовые + текст)\n"
            "💎 *Бриллиант* — 799 ₽ (всё из Золота + уроки)\n\n"
            "Чтобы купить, напиши в поддержку: @твой_ник",
            parse_mode="Markdown",
            reply_markup=profile_menu()
        )
        return

    # --- ШАГ 5: Если пользователь пишет текст без кнопки ---
    if m.text and not m.text.startswith('/'):
        await m.reply(
            "Пожалуйста, выбери действие с помощью кнопок ниже.\n"
            "Если хочешь пообщаться — нажми «🗣️ Общаться».\n"
            "Если хочешь учиться — нажми «📚 Уроки».\n"
            "Если хочешь посмотреть свой прогресс — открой «📊 Профиль».\n"
            "Если возникли вопросы — жми «🆘 Поддержка».",
            reply_markup=main_menu()
        )
        return

    # --- ШАГ 6: Голосовые (если не в чате) ---
    if m.voice:
        await m.reply(
            "🎤 Чтобы отправить голосовое, нажми сначала кнопку «🗣️ Общаться».\n"
            "Там я смогу распознать твою речь и ответить."
        )
        return