"""
«База данных» пользователей.

Сейчас это обычный файл users.json рядом с проектом.
Плюс: просто понять новичку.
Минус на Render: после большого перезапуска файла может не быть —
позже можно перейти на бесплатную облачную БД (объясню в конце).

Что храним на каждого пользователя:
- name — имя
- step — этап регистрации (start / awaiting_name / ready)
- mode — где сейчас человек: menu / chat / lessons / profile
- last_bot_reply — последнее английское сообщение бота (для «Перевести»)
- level, lessons_done, words_learned — для профиля (уроки потом)
"""

import json
import os
from config import USER_DATA_FILE

# Какие режимы бывают (как комнаты в квартире)
MODE_MENU = "menu"
MODE_CHAT = "chat"
MODE_LESSONS = "lessons"
MODE_PROFILE = "profile"


def load_users() -> dict:
    if not os.path.exists(USER_DATA_FILE):
        return {}
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(data: dict) -> None:
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_user(users: dict, user_id: str) -> dict:
    """Достать пользователя. Если его ещё нет — создать карточку."""
    if user_id not in users:
        users[user_id] = {
            "name": None,
            "step": "start",
            "mode": MODE_MENU,
            "level": "A1",
            "lessons_done": 0,
            "words_learned": 0,
            "phrases_learned": 0,
            "last_bot_reply": None,
            "premium_until": 0,
            "assessment_done": False,
            "dev_unlock": False,
            "assessment": {},
            "grammar_progress": {
                "completed_exercises": {},
                "completed_topics": [],
            },
            "vocabulary_progress": {"words": [], "phrases": []},
            "streak": 0,
            "streak_last_date": "",
            "daily": {},
            "referral_code": "",
            "referred_by": None,
            "invite_count": 0,
            "trial_started_at": 0,
            "growth_onboarded": False,
            "referral_bonus_granted": False,
            "streak_safes": 0,
            "streak_safe_milestones_claimed": [],
            "streak_pending_restore": 0,
            "streak_burned": False,
            "streak_burn_date": "",
            "last_active_at": "",
            "reminder_sent_date": "",
            "chat_until": 0,
        }
    # На всякий случай дописываем новые поля старым пользователям
    defaults = {
        "mode": MODE_MENU,
        "last_bot_reply": None,
        "level": "A1",
        "lessons_done": 0,
        "words_learned": 0,
        "phrases_learned": 0,
        "premium_until": 0,
        "assessment_done": False,
        "dev_unlock": False,
        "assessment": {},
        "grammar_progress": {
            "completed_exercises": {},
            "completed_topics": [],
        },
        "vocabulary_progress": {"words": [], "phrases": []},
        "streak": 0,
        "streak_last_date": "",
        "daily": {},
        "referral_code": "",
        "referred_by": None,
        "invite_count": 0,
        "trial_started_at": 0,
        "growth_onboarded": False,
        "referral_bonus_granted": False,
        "streak_safes": 0,
        "streak_safe_milestones_claimed": [],
        "streak_pending_restore": 0,
        "streak_burned": False,
        "streak_burn_date": "",
        "last_active_at": "",
        "reminder_sent_date": "",
        "chat_until": 0,
    }
    for key, value in defaults.items():
        users[user_id].setdefault(key, value)
    return users[user_id]


def set_mode(user_id: str, mode: str) -> dict:
    """Переключить «комнату» пользователя и сразу сохранить."""
    users = load_users()
    user = get_user(users, user_id)
    user["mode"] = mode
    save_users(users)
    return user


def set_last_bot_reply(user_id: str, text: str) -> None:
    """Запомнить последний английский ответ бота (кнопка «Перевести»)."""
    users = load_users()
    user = get_user(users, user_id)
    user["last_bot_reply"] = text
    save_users(users)


def get_mode(user_id: str) -> str:
    users = load_users()
    user = get_user(users, user_id)
    return user.get("mode", MODE_MENU)
