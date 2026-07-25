"""Состояние и прогресс раздела Listening."""

from __future__ import annotations

from services.database import load_users, get_user, save_users


def ensure_listening(user: dict) -> dict:
    if "listening" not in user or not isinstance(user.get("listening"), dict):
        user["listening"] = {"progress": {}, "session": None}
    sm = user["listening"]
    if not isinstance(sm.get("progress"), dict):
        sm["progress"] = {}
    return sm


def progress_key(level: str, topic_id: str) -> str:
    return f"{level}:{topic_id}"


def is_topic_done(user: dict, level: str, topic_id: str) -> bool:
    sm = ensure_listening(user)
    return bool(sm["progress"].get(progress_key(level, topic_id)))


def _save(user_id: str, mutator) -> dict:
    users = load_users()
    user = get_user(users, user_id)
    ensure_listening(user)
    mutator(user)
    save_users(users, only=str(user_id))
    return user


def mark_topic_done(user_id: str, level: str, topic_id: str) -> dict:
    def mut(u):
        sm = ensure_listening(u)
        sm["progress"][progress_key(level, topic_id)] = True
        sm["session"] = None

    return _save(user_id, mut)


def clear_session(user_id: str) -> dict:
    def mut(u):
        sm = ensure_listening(u)
        sm["session"] = None
        lesson = u.get("lesson")
        if isinstance(lesson, dict) and str(lesson.get("hub") or "").startswith("listening"):
            lesson["hub"] = "listening_list"

    return _save(user_id, mut)


def get_session(user: dict) -> dict | None:
    sm = ensure_listening(user)
    s = sm.get("session")
    return s if isinstance(s, dict) else None


def set_session(user_id: str, session: dict | None) -> dict:
    def mut(u):
        ensure_listening(u)["session"] = session

    return _save(user_id, mut)


def update_session(user_id: str, **fields) -> dict:
    def mut(u):
        sm = ensure_listening(u)
        s = sm.get("session")
        if not isinstance(s, dict):
            s = {}
        s.update(fields)
        sm["session"] = s

    return _save(user_id, mut)


def set_listening_list(user_id: str, level: str) -> dict:
    def mut(u):
        from services.lesson_state import ensure_lesson

        ensure_lesson(u)
        ensure_listening(u)
        u["lesson"]["hub"] = "listening_list"
        u["lesson"]["level"] = level
        u["lesson"]["section"] = "Listening"

    return _save(user_id, mut)


def set_listening_hub(user_id: str, hub: str) -> dict:
    def mut(u):
        from services.lesson_state import ensure_lesson

        ensure_lesson(u)
        u["lesson"]["hub"] = hub

    return _save(user_id, mut)
