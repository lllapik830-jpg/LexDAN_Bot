"""
Озвучка: ElevenLabs (основной) + gTTS (запасной, если EL недоступен с облака).
Telegram voice = OGG/Opus через ffmpeg.
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import tempfile
from io import BytesIO

import requests
from config import ELEVENLABS_API_KEY

# Adam — стандартный голос; можно переопределить в env
VOICE_ID = (os.getenv("ELEVENLABS_VOICE_ID") or "pNInz6obpgDQGcFmaJgB").strip()
# Несколько моделей: если одна недоступна на тарифе — пробуем другую
_MODELS = [
    (os.getenv("ELEVENLABS_MODEL") or "").strip() or None,
    "eleven_turbo_v2_5",
    "eleven_multilingual_v2",
    "eleven_monolingual_v1",
]


def _clean_models() -> list[str]:
    seen = set()
    out = []
    for m in _MODELS:
        if not m or m in seen:
            continue
        seen.add(m)
        out.append(m)
    return out


def elevenlabs_tts(text: str, voice_id: str | None = None) -> bytes | None:
    """Текст → MP3 через ElevenLabs. None = не удалось."""
    audio, _err = elevenlabs_tts_detail(text, voice_id=voice_id)
    return audio


def elevenlabs_tts_detail(text: str, voice_id: str | None = None) -> tuple[bytes | None, str]:
    text = (text or "").strip()
    if not text:
        return None, "empty text"
    if not ELEVENLABS_API_KEY:
        return None, "no ELEVENLABS_API_KEY"

    vid = (voice_id or VOICE_ID or "").strip() or VOICE_ID

    # Лимит символов на запрос
    if len(text) > 900:
        text = text[:900].rsplit(" ", 1)[0] + "…"

    last_err = "unknown"
    for model_id in _clean_models():
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
            response = requests.post(
                url,
                headers={
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Content-Type": "application/json",
                    "Accept": "audio/mpeg",
                },
                json={
                    "text": text,
                    "model_id": model_id,
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75,
                    },
                },
                timeout=35,
            )
            if response.status_code == 200 and response.content:
                return response.content, ""

            body = (response.text or "")[:400]
            last_err = f"HTTP {response.status_code} model={model_id} voice={vid}: {body}"
            logging.error(f"ElevenLabs TTS: {last_err}")

            # Бесплатный тариф часто режет облачные IP (Render) — нет смысла крутить модели
            if response.status_code in (401, 402, 403) and (
                "unusual_activity" in body
                or "Free Tier" in body
                or "payment_required" in body
                or "quota" in body.lower()
            ):
                break
        except Exception as e:
            last_err = str(e)
            logging.error(f"ElevenLabs TTS exception: {e}")
    return None, last_err


def gtts_tts(text: str) -> bytes | None:
    """Запасная озвучка Google TTS (работает с Render)."""
    text = (text or "").strip()
    if not text:
        return None
    if len(text) > 900:
        text = text[:900].rsplit(" ", 1)[0] + "…"
    try:
        from gtts import gTTS

        buf = BytesIO()
        gTTS(text=text, lang="en", slow=False).write_to_fp(buf)
        data = buf.getvalue()
        return data or None
    except Exception as e:
        logging.error(f"gTTS error: {e}")
        return None


def synthesize_speech(text: str, voice_id: str | None = None) -> tuple[bytes | None, str]:
    """
    Сначала ElevenLabs, при ошибке — gTTS.
    Возвращает (mp3_bytes, source) где source = 'elevenlabs' | 'gtts' | ''.
    """
    audio, err = elevenlabs_tts_detail(text, voice_id=voice_id)
    if audio:
        return audio, "elevenlabs"
    logging.warning(f"ElevenLabs unavailable ({err}), falling back to gTTS")
    audio = gtts_tts(text)
    if audio:
        return audio, "gtts"
    return None, ""


def mp3_to_ogg_opus(mp3_bytes: bytes) -> bytes | None:
    """Telegram voice лучше принимать как OGG/Opus."""
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


async def send_voice_reply(
    message,
    text: str,
    *,
    title: str = "LexDAN",
    voice_id: str | None = None,
) -> bool:
    """Сгенерировать и отправить голосовое. True если ушло."""
    from aiogram.types import FSInputFile

    mp3_bytes, source = synthesize_speech(text, voice_id=voice_id)
    if not mp3_bytes:
        logging.error("All TTS backends failed")
        await message.answer("⚠️ Текст готов, но голос сейчас не отправился. Попробуй ещё раз чуть позже.")
        return False

    ogg_bytes = mp3_to_ogg_opus(mp3_bytes)
    path = None
    try:
        if ogg_bytes:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
                f.write(ogg_bytes)
                path = f.name
            await message.reply_voice(FSInputFile(path))
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(mp3_bytes)
                path = f.name
            await message.reply_audio(FSInputFile(path), title=title)
        logging.info(f"Voice sent via {source} voice_id={voice_id or 'default'}")
        return True
    except Exception as e:
        logging.error(f"Send voice error: {e}")
        await message.answer("⚠️ Не удалось отправить голосовое сообщение.")
        return False
    finally:
        if path and os.path.exists(path):
            os.unlink(path)
