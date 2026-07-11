import requests
import logging
from config import ELEVENLABS_API_KEY

def elevenlabs_tts(text):
    try:
        url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(url, headers=headers, json=data, timeout=20)
        if response.status_code == 200:
            return response.content
        else:
            logging.error(f"ElevenLabs error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"ElevenLabs error: {e}")
        return None