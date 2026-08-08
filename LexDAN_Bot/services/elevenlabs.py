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
# Сначала быстрые модели (качество для коротких реплик чата ок), потом fallback
_MODELS = [
    (os.getenv("ELEVENLABS_MODEL") or "").strip() or None,
    "eleven_flash_v2_5",
    "eleven_turbo_v2_5",
    "eleven_multilingual_v2",
]

_el_session: requests.Session | None = None


def _el_http() -> requests.Session:
    global _el_session
    if _el_session is None:
        _el_session = requests.Session()
        _el_session.headers.update(
            {
                "xi-api-key": ELEVENLABS_API_KEY or "",
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            }
        )
    return _el_session


def _clean_models() -> list[str]:
    seen = set()
    out = []
    for m in _MODELS:
        if not m or m in seen:
            continue
        seen.add(m)
        out.append(m)
    return out


def elevenlabs_tts(text: str, voice_id: str | None = None, *, slow: bool = False) -> bytes | None:
    """Текст → MP3 через ElevenLabs. None = не удалось."""
    audio, _err = elevenlabs_tts_detail(text, voice_id=voice_id, slow=slow)
    return audio


def elevenlabs_tts_detail(
    text: str, voice_id: str | None = None, *, slow: bool = False
) -> tuple[bytes | None, str]:
    text = (text or "").strip()
    if not text:
        return None, "empty text"
    if not ELEVENLABS_API_KEY:
        return None, "no ELEVENLABS_API_KEY"

    vid = (voice_id or VOICE_ID or "").strip() or VOICE_ID

    # Лимит символов на запрос
    if len(text) > 900:
        text = text[:900].rsplit(" ", 1)[0] + "…"

    voice_settings = {
        "stability": 0.7 if slow else 0.5,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": True,
    }
    # speed поддерживается новыми моделями (0.7–1.2); старые могут игнорить
    if slow:
        voice_settings["speed"] = 0.82

    last_err = "unknown"
    sess = _el_http()
    # Короткий timeout: на Render EL часто тупит → лучше быстро уйти в gTTS,
    # чем держать апдейт 20+ секунд (из логов: Duration 23163 ms).
    for model_id in _clean_models()[:2]:
        try:
            url = (
                f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
                f"?optimize_streaming_latency=4&output_format=mp3_22050_32"
            )
            response = sess.post(
                url,
                json={
                    "text": text,
                    "model_id": model_id,
                    "voice_settings": voice_settings,
                },
                timeout=6,
            )
            if response.status_code == 200 and response.content:
                return response.content, ""

            body = (response.text or "")[:400]
            last_err = f"HTTP {response.status_code} model={model_id} voice={vid}: {body}"
            logging.error(f"ElevenLabs TTS: {last_err}")

            if response.status_code in (401, 402, 403) and (
                "unusual_activity" in body
                or "Free Tier" in body
                or "payment_required" in body
                or "quota" in body.lower()
            ):
                break
            if response.status_code in (400, 422):
                continue
        except requests.Timeout as e:
            last_err = f"timeout model={model_id}: {e}"
            logging.warning(f"ElevenLabs TTS timeout, fallback soon: {last_err}")
            break  # не крутим следующую модель ещё 6с — сразу gTTS
        except Exception as e:
            last_err = str(e)
            logging.error(f"ElevenLabs TTS exception: {e}")
            break
    return None, last_err


def gtts_tts(text: str, *, slow: bool = False) -> bytes | None:
    """Запасная озвучка Google TTS (работает с Render)."""
    text = (text or "").strip()
    if not text:
        return None
    if len(text) > 900:
        text = text[:900].rsplit(" ", 1)[0] + "…"
    try:
        from gtts import gTTS

        buf = BytesIO()
        gTTS(text=text, lang="en", slow=slow).write_to_fp(buf)
        data = buf.getvalue()
        return data or None
    except Exception as e:
        logging.error(f"gTTS error: {e}")
        return None


def synthesize_speech(
    text: str, voice_id: str | None = None, *, slow: bool = False,
    allow_gtts_fallback: bool = True,
) -> tuple[bytes | None, str]:
    """
    Сначала ElevenLabs, при ошибке — gTTS (если allow_gtts_fallback).
    Для listening-диалогов: allow_gtts_fallback=False, чтобы голос персонажа
    не прыгал на google mid-cast.
    """
    audio, err = elevenlabs_tts_detail(text, voice_id=voice_id, slow=slow)
    if audio:
        return audio, "elevenlabs"
    # один повтор для sticky-voice (часто timeout на Render)
    if voice_id:
        audio, err2 = elevenlabs_tts_detail(text, voice_id=voice_id, slow=slow)
        if audio:
            return audio, "elevenlabs"
        err = err2 or err
    logging.warning(f"ElevenLabs unavailable ({err}), falling back to gTTS={allow_gtts_fallback}")
    if not allow_gtts_fallback:
        return None, ""
    audio = gtts_tts(text, slow=slow)
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

    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                "pipe:0",
                "-c:a",
                "libopus",
                "-b:a",
                "32k",
                "-f",
                "ogg",
                "pipe:1",
            ],
            input=mp3_bytes,
            capture_output=True,
            timeout=20,
        )
        if result.returncode != 0 or not result.stdout:
            err = (result.stderr or b"")[:400]
            logging.error(f"ffmpeg TTS convert error: {err}")
            return None
        return result.stdout
    except Exception as e:
        logging.error(f"mp3_to_ogg error: {e}")
        return None


async def send_voice_from_mp3(
    message,
    mp3_bytes: bytes | None,
    *,
    source: str = "",
    title: str = "LexDAN",
) -> bool:
    """Отправить уже сгенерированный MP3 как voice/audio."""
    import asyncio

    from aiogram.types import FSInputFile

    if not mp3_bytes:
        logging.error("All TTS backends failed")
        await message.answer(
            "⚠️ Текст готов, но голос сейчас не отправился. Попробуй ещё раз чуть позже."
        )
        return False

    ogg_bytes = await asyncio.to_thread(mp3_to_ogg_opus, mp3_bytes)
    path = None
    try:
        if ogg_bytes:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
                f.write(ogg_bytes)
                path = f.name
            await message.answer_voice(FSInputFile(path))
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(mp3_bytes)
                path = f.name
            await message.answer_audio(FSInputFile(path), title=title)
        logging.info(f"Voice sent via {source or 'unknown'}")
        return True
    except Exception as e:
        logging.error(f"Send voice error: {e}")
        await message.answer("⚠️ Не удалось отправить голосовое сообщение.")
        return False
    finally:
        if path and os.path.exists(path):
            os.unlink(path)


async def send_voice_reply(
    message,
    text: str,
    *,
    title: str = "LexDAN",
    voice_id: str | None = None,
    slow: bool = False,
    allow_gtts_fallback: bool = True,
) -> bool:
    """Сгенерировать и отправить голосовое. True если ушло."""
    import asyncio

    vid = (voice_id or "").strip() or None
    mp3_bytes, source = await asyncio.to_thread(
        synthesize_speech,
        text,
        vid,
        slow=slow,
        allow_gtts_fallback=allow_gtts_fallback,
    )
    return await send_voice_from_mp3(
        message, mp3_bytes, source=source, title=title
    )


async def send_rico_voice(
    message,
    text: str,
    *,
    user: dict | None = None,
    title: str = "Rico",
    slow: bool = False,
) -> bool:
    """
    Озвучка голосом Рико (уроки, огонь дня, реплики Рико).
    Не использовать для чата и персонажей Listening.
    """
    from services.voices import resolve_rico_voice_id

    return await send_voice_reply(
        message,
        text,
        title=title,
        voice_id=resolve_rico_voice_id(user),
        slow=slow,
        allow_gtts_fallback=True,
    )

