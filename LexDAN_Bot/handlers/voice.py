from aiogram import Router, types
from aiogram.types import FSInputFile
from services.gpt import ask_gpt
from services.translation import translate_to_language
from services.elevenlabs import elevenlabs_tts
from handlers.keyboards import back_to_menu
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import io
import logging

router = Router()

# --- ГЛОБАЛЬНЫЙ СЛОВАРЬ ДЛЯ ПОСЛЕДНИХ СООБЩЕНИЙ ---
user_last_message = {}

@router.message(lambda m: m.voice is not None)
async def voice_handler(m: types.Message):
    user_id = str(m.from_user.id)
    await m.reply("🎧 Обрабатываю голосовое...")
    
    try:
        file = await bot.get_file(m.voice.file_id)
        voice_data = await bot.download_file(file.file_path)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_ogg:
            tmp_ogg.write(voice_data.read())
            ogg_path = tmp_ogg.name

        audio = AudioSegment.from_ogg(ogg_path)
        wav_bytes = io.BytesIO()
        audio.export(wav_bytes, format="wav")
        wav_bytes.seek(0)
        os.unlink(ogg_path)

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_bytes) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="en-US")

        if text:
            answer_en = ask_gpt(text, "Student")
            user_last_message[user_id] = answer_en
            
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
        else:
            await m.reply("Не удалось распознать речь. Попробуй ещё раз.")
            
    except Exception as e:
        logging.error(f"Voice error: {e}")
        await m.reply(f"Ошибка: {str(e)}")