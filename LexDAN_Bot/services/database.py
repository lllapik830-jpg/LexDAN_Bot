"""
Хранение пользователей: PostgreSQL (Render) или файл users.json (локально / fallback).

Если задан DATABASE_URL — пишем в Postgres (данные переживают редеплой).
Иначе — как раньше, в users.json.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from config import USER_DATA_FILE

MODE_MENU = "menu"
MODE_CHAT = "chat"
MODE_LESSONS = "lessons"
MODE_PROFILE = "profile"
MODE_SECRET = "secret"

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()

_pg_ready = False
_migrated_from_file = False


def _use_postgres() -> bool:
    return bool(DATABASE_URL)


def _connect():
    import psycopg

    url = DATABASE_URL
    # Render обычно требует SSL
    if "sslmode=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return psycopg.connect(url)


def _ensure_pg() -> None:
    global _pg_ready, _migrated_from_file
    if _pg_ready:
        return
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    data JSONB NOT NULL DEFAULT '{}'::jsonb,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )
        conn.commit()
    _pg_ready = True
    logging.info("Postgres users table ready")
    _maybe_migrate_json_once()


def _maybe_migrate_json_once() -> None:
    """Один раз перенести users.json в Postgres, если таблица пустая."""
    global _migrated_from_file
    if _migrated_from_file:
        return
    _migrated_from_file = True
    if not os.path.exists(USER_DATA_FILE):
        return
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            file_data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return
    if not isinstance(file_data, dict) or not file_data:
        return

    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users")
            (count,) = cur.fetchone()
            if count and int(count) > 0:
                return
            for uid, payload in file_data.items():
                if not isinstance(payload, dict):
                    continue
                cur.execute(
                    """
                    INSERT INTO users (user_id, data)
                    VALUES (%s, %s::jsonb)
                    ON CONFLICT (user_id) DO NOTHING
                    """,
                    (str(uid), json.dumps(payload, ensure_ascii=False)),
                )
        conn.commit()
    logging.info(f"Migrated {len(file_data)} users from {USER_DATA_FILE} → Postgres")


def load_users() -> dict:
    if not _use_postgres():
        return _load_users_file()
    try:
        _ensure_pg()
        users: dict[str, Any] = {}
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, data FROM users")
                for user_id, data in cur.fetchall():
                    if isinstance(data, dict):
                        users[str(user_id)] = data
                    else:
                        users[str(user_id)] = json.loads(data)
        return users
    except Exception as e:
        logging.error(f"Postgres load_users failed, fallback to file: {e}")
        return _load_users_file()


def save_users(data: dict) -> None:
    if not _use_postgres():
        _save_users_file(data)
        return
    try:
        _ensure_pg()
        with _connect() as conn:
            with conn.cursor() as cur:
                for uid, payload in data.items():
                    if not isinstance(payload, dict):
                        continue
                    cur.execute(
                        """
                        INSERT INTO users (user_id, data, updated_at)
                        VALUES (%s, %s::jsonb, now())
                        ON CONFLICT (user_id) DO UPDATE SET
                            data = EXCLUDED.data,
                            updated_at = now()
                        """,
                        (str(uid), json.dumps(payload, ensure_ascii=False)),
                    )
            conn.commit()
    except Exception as e:
        logging.error(f"Postgres save_users failed, fallback to file: {e}")
        _save_users_file(data)


def _load_users_file() -> dict:
    if not os.path.exists(USER_DATA_FILE):
        return {}
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_users_file(data: dict) -> None:
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
    users = load_users()
    user = get_user(users, user_id)
    user["mode"] = mode
    save_users(users)
    return user


def set_last_bot_reply(user_id: str, text: str) -> None:
    users = load_users()
    user = get_user(users, user_id)
    user["last_bot_reply"] = text
    save_users(users)


def get_mode(user_id: str) -> str:
    users = load_users()
    user = get_user(users, user_id)
    return user.get("mode", MODE_MENU)
