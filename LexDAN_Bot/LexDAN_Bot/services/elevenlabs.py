"""
Голос через ElevenLabs:
- STT = речь → текст (распознать голосовое)
- TTS = текст → речь (бот отвечает голосом)

OGG от Telegram можно отправлять в STT как есть — ffmpeg не нужен.
"""

import logging
import requests
from config import ELEVENLABS_API_KEY

# Голос Adam. Позже можно сменить ID на другой голос в кабинете ElevenLabs.
VOICE_ID = "pNInz6obpgDQGcFmaJgB"


def elevenlabs_stt(audio_bytes: bytes, filename: str = "voice.ogg") -> str | None:
    """Распознать речь. Возвращает текст или None."""
    try:
        response = requests.post(
            "https://api.elevenlabs.io/v1/speech-to-text",
            headers={"xi-api-key": ELEVENLABS_API_KEY},
            data={
                "model_id": "scribe_v1",
                "language_code": "en",
            },
            files={"file": (filename, audio_bytes, "audio/ogg")},
            timeout=60,
        )
        if response.status_code != 200:
            logging.error(f"ElevenLabs STT error: {response.status_code} - {response.text}")
            return None

        data = response.json()
        # В ответе обычно поле "text"
        text = (data.get("text") or "").strip()
        return text or None
    except Exception as e:
        logging.error(f"ElevenLabs STT error: {e}")
        return None


def elevenlabs_tts(text: str) -> bytes | None:
    """Превратить английский текст в MP3. Возвращает байты или None."""
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
