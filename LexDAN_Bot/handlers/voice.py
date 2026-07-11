from aiogram import Router, types
from aiogram.types import FSInputFile
from services.gpt import ask_gpt
from services.translation import translate_to_language
from services.elevenlabs import elevenlabs_tts
from services.database import load_users, save_users, get_user
from handlers.keyboards import main_menu, translate_keyboard
import speech_recognition as sr
from pydub import AudioSegment
import io
import tempfile
import os
import logging
from datetime import date

router = Router()

# --- ОБРАБОТКА ГОЛОСОВЫХ СООБЩЕНИЙ ---
@router.message(lambda m: m.voice is not None)
async def voice_handler(m: types.Message):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    save_users(users)

    # --- ЛИМИТ 20 ГОЛОСОВЫХ В ДЕНЬ ---
    if not is_premium(user_id):
        today = date.today().isoformat()
        if user.get("voice_date") != today:
            user["voice_date"] = today
            user["voice_count"] = 0
            save_users(users)
        if user.get("voice_count", 0) >= 20:
            from handlers.keyboards import subscription_keyboard
            await m.reply(
                "🎤 *Ты исчерпал лимит на сегодня.*\n\n"
                "Купи безлимит за 399 ₽ и продолжай заниматься!",
                parse_mode="Markdown",
                reply_markup=subscription_keyboard()
            )
            return

    await m.reply("🎧 Processing voice...")

    try:
        # 1. Скачиваем голосовое
        file = await bot.get_file(m.voice.file_id)
        voice_data = await bot.download_file(file.file_path)

        # 2. Конвертируем OGG → WAV
        audio = AudioSegment.from_file(io.BytesIO(voice_data.read()), format="ogg")
        wav_bytes = io.BytesIO()
        audio.export(wav_bytes, format="wav")
        wav_bytes.seek(0)

        # 3. Распознаём через Google Speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_bytes) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="en-US")

        if text:
            # --- Увеличиваем счётчик ---
            if not is_premium(user_id):
                user["voice_count"] = user.get("voice_count", 0) + 1
                save_users(users)

            # --- Отвечаем через GPT ---
            answer_en = ask_gpt(text, user["name"])
            translation = translate_to_language(answer_en, user["language"])

            await m.reply(
                f"🗣️ You said: {text}\n\n🇬🇧 {answer_en}",
                reply_markup=translate_keyboard(user["language"])
            )

            # --- Озвучиваем ответ ---
            audio_bytes = elevenlabs_tts(answer_en)
            if audio_bytes:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(audio_bytes)
                    path = f.name
                await m.reply_voice(FSInputFile(path))
                os.unlink(path)
        else:
            await m.reply("Could not understand audio.", reply_markup=main_menu())

    except sr.UnknownValueError:
        await m.reply("Could not understand audio. Please speak clearly.", reply_markup=main_menu())
    except sr.RequestError as e:
        logging.error(f"Google Speech error: {e}")
        await m.reply("Speech recognition service error. Please try again.", reply_markup=main_menu())
    except Exception as e:
        logging.error(f"Voice error: {e}")
        await m.reply("Error processing voice.", reply_markup=main_menu())

# --- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ПРОВЕРКИ ПРЕМИУМ ---
def is_premium(user_id):
    users = load_users()
    user = users.get(user_id, {})
    premium_until = user.get("premium_until", 0)
    import time
    return time.time() < premium_until