"""
Хранение пользователей: PostgreSQL (Render) или файл users.json (локально / fallback).

Если задан DATABASE_URL — пишем в Postgres (данные переживают редеплой).
Иначе — как раньше, в users.json.

Важно: ModeFilter вызывается десятки раз на одно сообщение.
Поэтому читаем ОДНОГО юзера (fetch_user), держим keep-alive к PG и короткий кэш.
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from typing import Any

from config import USER_DATA_FILE

MODE_MENU = "menu"
MODE_CHAT = "chat"
MODE_LESSONS = "lessons"
MODE_PROFILE = "profile"
MODE_SECRET = "secret"
MODE_DAILY_FIRE = "daily_fire"
MODE_EXCLUSIVE = "exclusive"

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()

_pg_ready = False
_migrated_from_file = False

# Keep-alive соединение (новый connect на Render = сотни мс…секунды)
_conn = None
_conn_lock = threading.Lock()

# Кэш одного юзера: user_id -> (monotonic_ts, user_dict)
_user_cache: dict[str, tuple[float, dict]] = {}
_USER_CACHE_TTL = 2.0

# Кэш полной таблицы (админка / редкие места) — короткий, чтобы не долбить SELECT *
_all_cache: dict[str, Any] | None = None
_all_cache_at = 0.0
_ALL_CACHE_TTL = 1.5


def _use_postgres() -> bool:
    return bool(DATABASE_URL)


def _dsn() -> str:
    url = DATABASE_URL
    if "sslmode=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return url


def _get_conn():
    """Переиспользуем одно соединение — без TLS handshake на каждый клик."""
    global _conn
    import psycopg

    with _conn_lock:
        if _conn is not None and not _conn.closed:
            # Не делаем SELECT 1 на каждый клик — это сериализует все хендлеры.
            return _conn
        _conn = psycopg.connect(_dsn(), connect_timeout=5)
        return _conn


def _reset_conn() -> None:
    global _conn
    with _conn_lock:
        if _conn is not None:
            try:
                _conn.close()
            except Exception:
                pass
        _conn = None


def _ensure_pg() -> None:
    global _pg_ready, _migrated_from_file
    if _pg_ready:
        return
    with _conn_lock:
        # повторная проверка под локом
        if _pg_ready:
            return
    conn = _get_conn()
    with _conn_lock:
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

    conn = _get_conn()
    with _conn_lock:
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


def _invalidate_caches(user_ids: list[str] | None = None) -> None:
    global _all_cache, _all_cache_at
    _all_cache = None
    _all_cache_at = 0.0
    if user_ids is None:
        _user_cache.clear()
        return
    for uid in user_ids:
        _user_cache.pop(str(uid), None)


def _decode_row(data: Any) -> dict:
    if isinstance(data, dict):
        return data
    if isinstance(data, str):
        return json.loads(data)
    return dict(data) if data else {}


def fetch_user(user_id: str, *, use_cache: bool = True) -> dict:
    """
    Загрузить ОДНОГО пользователя (быстрый путь для кнопок/фильтров).
    Всегда возвращает карточку с дефолтами (как get_user).
    """
    uid = str(user_id)
    now = time.monotonic()
    if use_cache:
        hit = _user_cache.get(uid)
        if hit and (now - hit[0]) < _USER_CACHE_TTL:
            # get_user на копии в map — мутации идут в тот же dict (ок для кэша)
            return get_user({uid: hit[1]}, uid)

    raw: dict | None = None
    if _use_postgres():
        try:
            _ensure_pg()
            conn = _get_conn()
            with _conn_lock:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT data FROM users WHERE user_id = %s",
                        (uid,),
                    )
                    row = cur.fetchone()
            if row:
                raw = _decode_row(row[0])
        except Exception as e:
            logging.error(f"Postgres fetch_user failed: {e}")
            _reset_conn()
            file_data = _load_users_file()
            raw = file_data.get(uid) if isinstance(file_data.get(uid), dict) else None
    else:
        file_data = _load_users_file()
        raw = file_data.get(uid) if isinstance(file_data.get(uid), dict) else None

    bucket = {uid: dict(raw)} if raw else {}
    user = get_user(bucket, uid)
    _user_cache[uid] = (now, user)
    return user


def users_for(user_id: str) -> dict:
    """Мини-словарь {uid: user} — вместо load_users() в обычных хендлерах."""
    uid = str(user_id)
    return {uid: fetch_user(uid)}


def load_users() -> dict:
    """
    Вся таблица. Тяжело на Postgres — используй users_for()/fetch_user() в хендлерах.
    Оставлен для админки, рассылок, статистики.
    """
    global _all_cache, _all_cache_at

    if not _use_postgres():
        return _load_users_file()

    now = time.monotonic()
    if _all_cache is not None and (now - _all_cache_at) < _ALL_CACHE_TTL:
        return _all_cache

    try:
        _ensure_pg()
        users: dict[str, Any] = {}
        conn = _get_conn()
        with _conn_lock:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, data FROM users")
                rows = cur.fetchall()
        for user_id, data in rows:
            users[str(user_id)] = _decode_row(data)
        _all_cache = users
        _all_cache_at = now
        return users
    except Exception as e:
        logging.error(f"Postgres load_users failed, fallback to file: {e}")
        return _load_users_file()


def save_users(data: dict, only: str | list[str] | None = None) -> None:
    """
    Сохранить юзеров.
    only=user_id или [id,…] — писать только их (без гонок «перезаписал чужие данные»).
    only=None — все (админ/миграция).
    """
    if only is None:
        targets = [(str(uid), payload) for uid, payload in data.items() if isinstance(payload, dict)]
    else:
        ids = [only] if isinstance(only, str) else list(only)
        targets = []
        for uid in ids:
            payload = data.get(str(uid))
            if isinstance(payload, dict):
                targets.append((str(uid), payload))

    if not targets:
        return

    if not _use_postgres():
        file_data = _load_users_file()
        for uid, payload in targets:
            file_data[uid] = payload
        _save_users_file(file_data)
        _invalidate_caches([uid for uid, _ in targets])
        return
    try:
        _ensure_pg()
        conn = _get_conn()
        with _conn_lock:
            with conn.cursor() as cur:
                for uid, payload in targets:
                    cur.execute(
                        """
                        INSERT INTO users (user_id, data, updated_at)
                        VALUES (%s, %s::jsonb, now())
                        ON CONFLICT (user_id) DO UPDATE SET
                            data = EXCLUDED.data,
                            updated_at = now()
                        """,
                        (uid, json.dumps(payload, ensure_ascii=False)),
                    )
            conn.commit()
        # обновим кэш свежими данными
        now = time.monotonic()
        for uid, payload in targets:
            _user_cache[uid] = (now, payload)
        global _all_cache, _all_cache_at
        _all_cache = None
        _all_cache_at = 0.0
    except Exception as e:
        logging.error(f"Postgres save_users failed, fallback to file: {e}")
        _reset_conn()
        file_data = _load_users_file()
        for uid, payload in targets:
            file_data[uid] = payload
        _save_users_file(file_data)
        _invalidate_caches([uid for uid, _ in targets])


def delete_users(user_ids: list[str] | set[str]) -> int:
    """Удалить пользователей из Postgres / файла. Возвращает число удалённых."""
    ids = sorted({str(uid).strip() for uid in user_ids if str(uid).strip()})
    if not ids:
        return 0

    if not _use_postgres():
        file_data = _load_users_file()
        n = 0
        for uid in ids:
            if uid in file_data:
                del file_data[uid]
                n += 1
        if n:
            _save_users_file(file_data)
            _invalidate_caches(ids)
        return n

    try:
        _ensure_pg()
        conn = _get_conn()
        with _conn_lock:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM users WHERE user_id = ANY(%s)",
                    (ids,),
                )
                n = cur.rowcount or 0
            conn.commit()
        _invalidate_caches(ids)
        return int(n)
    except Exception as e:
        logging.error(f"Postgres delete_users failed, fallback to file: {e}")
        _reset_conn()
        file_data = _load_users_file()
        n = 0
        for uid in ids:
            if uid in file_data:
                del file_data[uid]
                n += 1
        if n:
            _save_users_file(file_data)
            _invalidate_caches(ids)
        return n


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
            "first_seen_at": 0,
            "chat_text_total": 0,
            "chat_voice_total": 0,
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
        "first_seen_at": 0,
        "chat_text_total": 0,
        "chat_voice_total": 0,
    }
    for key, value in defaults.items():
        users[user_id].setdefault(key, value)
    return users[user_id]


def set_mode(user_id: str, mode: str) -> dict:
    users = users_for(user_id)
    user = get_user(users, user_id)
    user["mode"] = mode
    labels = {
        MODE_MENU: "главное меню",
        MODE_CHAT: "общение",
        MODE_LESSONS: "уроки",
        MODE_PROFILE: "профиль",
        MODE_SECRET: "секрет Рико",
        MODE_DAILY_FIRE: "огонь дня",
        MODE_EXCLUSIVE: "эксклюзив Рико",
    }
    user["last_section"] = labels.get(mode, mode)
    from datetime import datetime, timedelta, timezone

    user["last_active_at"] = datetime.now(timezone(timedelta(hours=3))).isoformat()
    save_users(users, only=str(user_id))
    return user


def set_last_bot_reply(user_id: str, text: str) -> None:
    users = users_for(user_id)
    user = get_user(users, user_id)
    user["last_bot_reply"] = text
    save_users(users, only=str(user_id))


def get_mode(user_id: str) -> str:
    user = fetch_user(user_id)
    return user.get("mode", MODE_MENU)
