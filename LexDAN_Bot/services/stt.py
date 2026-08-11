"""
Распознавание речи (голос → текст).

Цепочка:
1) Telegram OGG → WAV 16 kHz mono (ffmpeg + нормализация)
2) OpenRouter Whisper / GPT-4o Mini Transcribe (основной, точнее)
3) Fallback: Google Web Speech en-US (бесплатно)

На Render нужен ffmpeg (Aptfile).
"""

from __future__ import annotations

import base64
import logging
import os
import shutil
import subprocess
import tempfile

import requests
import speech_recognition as sr

from config import OPENROUTER_API_KEY

# Быстрый и точный для коротких голосовых; переопределяется env
STT_MODEL = (os.getenv("OPENROUTER_STT_MODEL") or "openai/gpt-4o-mini-transcribe").strip()
# Запасной Whisper, если mini-transcribe недоступен у провайдера
STT_FALLBACK_MODEL = (
    os.getenv("OPENROUTER_STT_FALLBACK_MODEL") or "openai/whisper-1"
).strip()

_EN_PROMPT = (
    "Transcribe clear English speech from an English learner. "
    "Keep original words, grammar mistakes and pronunciation attempts as heard. "
    "Do not translate. Do not add punctuation that changes meaning. "
    "Output only the spoken English text."
)


def recognize_english(audio_bytes: bytes, *, hint: str | None = None) -> str | None:
    """
    Распознать английскую речь из Telegram voice (OGG/Opus).
    hint — опциональная ожидаемая фраза (speak-practice), помогает модели.
    """
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
        if not _ogg_to_wav(ogg_path, wav_path):
            return None

        with open(wav_path, "rb") as f:
            wav_bytes = f.read()

        text = _recognize_openrouter(wav_bytes, hint=hint)
        if text:
            return text

        text = _recognize_google(wav_path)
        return text

    except Exception as e:
        logging.error(f"STT error: {e}")
        return None
    finally:
        for path in (ogg_path, wav_path):
            if path and os.path.exists(path):
                try:
                    os.unlink(path)
                except OSError:
                    pass


def _ogg_to_wav(ogg_path: str, wav_path: str) -> bool:
    """
    Конвертация + лёгкая чистка:
    - highpass убирает гул
    - loudnorm поднимает тихие голосовые Telegram
    - 16 kHz mono — стандарт для STT
    """
    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            ogg_path,
            "-af",
            "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar",
            "16000",
            "-ac",
            "1",
            wav_path,
        ],
        capture_output=True,
        text=True,
        timeout=40,
    )
    if result.returncode != 0:
        # без фильтров — лучше хоть что-то
        logging.warning("ffmpeg loudnorm failed, plain convert: %s", (result.stderr or "")[:300])
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
            logging.error("ffmpeg error: %s", (result.stderr or "")[:500])
            return False
    return True


def _clean_transcript(text: str | None) -> str | None:
    if not text:
        return None
    t = " ".join(str(text).replace("\n", " ").split()).strip()
    # типичный мусор Whisper на тишине
    if t.lower() in {"", ".", "..", "...", "thank you.", "thanks for watching.", "you"}:
        return None
    return t or None


def _recognize_openrouter(wav_bytes: bytes, *, hint: str | None = None) -> str | None:
    if not OPENROUTER_API_KEY or not wav_bytes:
        return None

    prompt = _EN_PROMPT
    if hint:
        hint_s = " ".join(str(hint).split())[:180]
        prompt = f"{_EN_PROMPT} Expected phrase (may be approximate): {hint_s}"

    b64 = base64.b64encode(wav_bytes).decode("ascii")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/LexDAN_bot",
        "X-Title": "LexDAN",
    }

    for model in (STT_MODEL, STT_FALLBACK_MODEL):
        if not model:
            continue
        payload = {
            "model": model,
            "language": "en",
            "temperature": 0,
            "prompt": prompt,
            "input_audio": {"data": b64, "format": "wav"},
        }
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/audio/transcriptions",
                headers=headers,
                json=payload,
                timeout=45,
            )
            if r.status_code >= 400:
                # некоторые модели не принимают prompt — повторяем без него
                body = (r.text or "")[:400]
                logging.warning("OpenRouter STT %s HTTP %s: %s", model, r.status_code, body)
                if "prompt" in body.lower() or r.status_code == 400:
                    payload.pop("prompt", None)
                    r = requests.post(
                        "https://openrouter.ai/api/v1/audio/transcriptions",
                        headers=headers,
                        json=payload,
                        timeout=45,
                    )
            if r.status_code >= 400:
                logging.warning(
                    "OpenRouter STT fail model=%s: %s", model, (r.text or "")[:300]
                )
                continue
            data = r.json() if r.content else {}
            text = _clean_transcript((data.get("text") if isinstance(data, dict) else None) or "")
            if text:
                logging.info("STT ok via OpenRouter model=%s chars=%s", model, len(text))
                return text
        except Exception as e:
            logging.warning("OpenRouter STT error model=%s: %s", model, e)
    return None


def _recognize_google(wav_path: str) -> str | None:
    """Fallback: бесплатный Google Web Speech, en-US + лучший вариант из alternatives."""
    try:
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = True
        with sr.AudioFile(wav_path) as source:
            try:
                recognizer.adjust_for_ambient_noise(source, duration=0.25)
            except Exception:
                pass
            audio = recognizer.record(source)

        # show_all → выбрать самый уверенный / длинный разумный вариант
        try:
            raw = recognizer.recognize_google(audio, language="en-US", show_all=True)
        except sr.UnknownValueError:
            logging.info("STT Google: speech not understood")
            return None

        text = _pick_google_best(raw)
        if text:
            logging.info("STT ok via Google chars=%s", len(text))
        return text
    except sr.UnknownValueError:
        logging.info("STT Google: speech not understood")
        return None
    except Exception as e:
        logging.warning("STT Google error: %s", e)
        return None


def _pick_google_best(raw) -> str | None:
    if isinstance(raw, str):
        return _clean_transcript(raw)
    if not isinstance(raw, dict):
        return None
    alts = raw.get("alternative") or []
    if not alts:
        return _clean_transcript(raw.get("transcript"))
    best = None
    best_score = -1.0
    for alt in alts:
        if not isinstance(alt, dict):
            continue
        t = _clean_transcript(alt.get("transcript"))
        if not t:
            continue
        conf = alt.get("confidence")
        try:
            score = float(conf) if conf is not None else 0.5
        except (TypeError, ValueError):
            score = 0.5
        # слегка предпочитаем более длинные фразы при равной уверенности
        score += min(len(t), 80) / 400.0
        if score > best_score:
            best_score = score
            best = t
    return best
