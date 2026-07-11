import requests
import logging
from config import OPENROUTER_API_KEY

def translate_to_language(text, target_lang):
    if not text:
        return None
    if not target_lang or target_lang.lower() == "english":
        return None

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": f"Translate the following English text to NATURAL {target_lang}. Keep the meaning, but make it sound like a friendly tutor explaining to a student. Only output the {target_lang} translation, nothing else."},
                    {"role": "user", "content": text}
                ],
                "max_tokens": 800
            },
            timeout=20
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"Translation error: {e}")
        return None