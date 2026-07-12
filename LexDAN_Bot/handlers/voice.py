from aiogram import Router, types, Bot
from aiogram.types import FSInputFile
from services.gpt import ask_gpt
from services.elevenlabs import elevenlabs_tts
import speech_recognition as sr
import tempfile
import os
import logging

router = Router()
user_last_message = {}

@router.message(lambda m: m.voice is not None)
async def voice_handler(m: types.Message, bot: Bot):
    user_id = str(m.from_user.id)
    logging.info(f"🎤 VOICE RECEIVED from {user_id}")
    
    await m.reply("🎧 Обрабатываю голосовое...")
    
    try:
        file = await bot.get_file(m.voice.file_id)
        voice_data = await bot.download_file(file.file_path)
        logging.info("✅ VOICE DOWNLOADED")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_ogg:
            tmp_ogg.write(voice_data.read())
            ogg_path = tmp_ogg.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(ogg_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="en-US")
        
        os.unlink(ogg_path)
        logging.info(f"📝 RECOGNIZED: {text}")

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
            await m.reply("Не удалось распознать речь.")
            
    except Exception as e:
        logging.error(f"❌ Voice error: {e}")
        await m.reply(f"Ошибка: {str(e)}")