import requests
import logging
from config import OPENROUTER_API_KEY

def ask_gpt(prompt, user_name="Student"):
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
                    {
                        "role": "system",
                        "content": f"You are a strict but friendly English tutor. Your student's name is {user_name}. Respond ONLY in English. Keep responses SHORT (1-2 sentences). Always ask a follow-up question to practice speaking."
                    },
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 150
            },
            timeout=15
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"GPT error: {e}")
        return "Sorry, I couldn't process that."
