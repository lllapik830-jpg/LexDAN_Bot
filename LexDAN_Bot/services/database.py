import json
from datetime import date
from config import USER_DATA_FILE

def load_users():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(users, user_id):
    if user_id not in users:
        users[user_id] = {
            "name": None,
            "language": None,
            "step": "name",
            "level": "A1",
            "voice_count": 0,
            "voice_date": date.today().isoformat(),
            "premium_until": 0,
            "lessons_done": 0,
            "words_learned": 0
        }
    return users[user_id]