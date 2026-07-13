"""
Распознавание речи (голос → текст).

ElevenLabs STT у тебя в ключе выключен, поэтому используем:
OGG (Telegram) → WAV (через ffmpeg) → Google Speech Recognition (бесплатно).
На Render нужен ffmpeg (файл Aptfile в корне репозитория).
"""

import logging
import os
import shutil
import subprocess
import tempfile

import speech_recognition as sr


def recognize_english(audio_bytes: bytes) -> str | None:
    if not audio_bytes:
        return None

    if not shutil.which("ffmpeg"):
        logging.error("ffmpeg not found. Install ffmpeg (Aptfile on Render).")
        return None

    ogg_path = None
    wav_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as ogg:
            ogg.write(audio_bytes)
            ogg_path = ogg.name

        wav_path = ogg_path + ".wav"
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                ogg_path,
                "-ar",
                "16000",
                "-ac",
                "1",
                wav_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            logging.error(f"ffmpeg error: {result.stderr}")
            return None

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language="en-US")
        return (text or "").strip() or None

    except sr.UnknownValueError:
        logging.info("STT: speech not understood")
        return None
    except Exception as e:
        logging.error(f"STT error: {e}")
        return None
    finally:
        for path in (ogg_path, wav_path):
            if path and os.path.exists(path):
                os.unlink(path)
