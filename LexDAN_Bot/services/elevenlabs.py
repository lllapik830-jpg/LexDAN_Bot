"""
ElevenLabs: только озвучка текста (TTS).
Распознавание голоса — в services/stt.py (Google).
"""

import logging
import os
import shutil
import subprocess
import tempfile

import requests
from config import ELEVENLABS_API_KEY

VOICE_ID = "pNInz6obpgDQGcFmaJgB"


def elevenlabs_tts(text: str) -> bytes | None:
    """Текст → MP3 байты."""
    if not text:
        return None
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        response = requests.post(
            url,
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
            json={
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                },
            },
            timeout=30,
        )
        if response.status_code == 200:
            return response.content
        logging.error(f"ElevenLabs TTS error: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        logging.error(f"ElevenLabs TTS error: {e}")
        return None


def mp3_to_ogg_opus(mp3_bytes: bytes) -> bytes | None:
    """
    Telegram принимает voice только как OGG/Opus.
    MP3 как reply_voice часто просто не уходит.
    """
    if not mp3_bytes:
        return None
    if not shutil.which("ffmpeg"):
        logging.error("ffmpeg not found — cannot convert TTS to ogg")
        return None

    mp3_path = None
    ogg_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(mp3_bytes)
            mp3_path = f.name
        ogg_path = mp3_path + ".ogg"

        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                mp3_path,
                "-c:a",
                "libopus",
                "-b:a",
                "48k",
                ogg_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            logging.error(f"ffmpeg TTS convert error: {result.stderr}")
            return None

        with open(ogg_path, "rb") as f:
            return f.read()
    except Exception as e:
        logging.error(f"mp3_to_ogg error: {e}")
        return None
    finally:
        for path in (mp3_path, ogg_path):
            if path and os.path.exists(path):
                os.unlink(path)
