"""Состояние и прогресс раздела Reading."""

from __future__ import annotations

from datetime import date

from services.database import get_user, save_users


def ensure_reading(user: dict) -> dict:
    if "reading" not in user or not isinstance(user.get("reading"), dict):
        user["reading"] = {
            "progress": {},
            "session": None,
            "daily_date": "",
            "daily_used": 0,
        }
    sm = user["reading"]
    if not isinstance(sm.get("progress"), dict):
        sm["progress"] = {}
    if "daily_date" not in sm:
        sm["daily_date"] = ""
    if "daily_used" not in sm:
        sm["daily_used"] = 0
    return sm


def progress_key(level: str, topic_id: str) -> str:
    return f"{level}:{topic_id}"


def is_topic_done(user: dict, level: str, topic_id: str) -> bool:
    sm = ensure_reading(user)
    return bool(sm["progress"].get(progress_key(level, topic_id)))


def count_reading_topics_done(user: dict) -> int:
    sm = ensure_reading(user)
    return sum(1 for v in (sm.get("progress") or {}).values() if v)


def _today() -> str:
    return date.today().isoformat()


def reading_daily_cap(user: dict) -> int | None:
    """None = безлимит (799 / триал). Иначе дневной лимит тем."""
    from services.growth import FREE_READING_PER_DAY
    from services.rewards import user_plan

    if user_plan(user) == "full":
        return None
    return FREE_READING_PER_DAY  # free + 399


def reading_used_today(user: dict) -> int:
    sm = ensure_reading(user)
    if sm.get("daily_date") != _today():
        return 0
    return int(sm.get("daily_used") or 0)


def can_start_reading(user: dict) -> tuple[bool, str]:
    from services.growth import FREE_READING_PER_DAY

    cap = reading_daily_cap(user)
    if cap is None:
        return True, ""
    used = reading_used_today(user)
    if used >= cap:
        return (
            False,
            f"📖 На твоём тарифе — <b>{FREE_READING_PER_DAY} тема Reading в день</b>.\n"
            "Лимит на сегодня уже использован. Завтра снова можно, "
            "или открой полный доступ (799₽) без дневного лимита.",
        )
    return True, ""


def consume_reading_slot(user_id: str) -> dict:
    """Списать одну тему за сегодня (при старте задания 1)."""

    def mut(u):
        sm = ensure_reading(u)
        today = _today()
        if sm.get("daily_date") != today:
            sm["daily_date"] = today
            sm["daily_used"] = 0
        sm["daily_used"] = int(sm.get("daily_used") or 0) + 1

    return _save(user_id, mut)


def _save(user_id: str, mutator) -> dict:
    from services.database import users_for, get_user, save_users

    users = users_for(user_id)
    user = get_user(users, user_id)
    ensure_reading(user)
    mutator(user)
    save_users(users, only=str(user_id))
    return user


def mark_topic_done(user_id: str, level: str, topic_id: str) -> dict:
    def mut(u):
        sm = ensure_reading(u)
        sm["progress"][progress_key(level, topic_id)] = True
        sm["session"] = None

    return _save(user_id, mut)


def clear_session(user_id: str) -> dict:
    def mut(u):
        sm = ensure_reading(u)
        sm["session"] = None
        lesson = u.get("lesson")
        if isinstance(lesson, dict) and str(lesson.get("hub") or "").startswith("reading"):
            lesson["hub"] = "reading_list"

    return _save(user_id, mut)


def get_session(user: dict) -> dict | None:
    sm = ensure_reading(user)
    s = sm.get("session")
    return s if isinstance(s, dict) else None


def set_session(user_id: str, session: dict | None) -> dict:
    def mut(u):
        ensure_reading(u)["session"] = session

    return _save(user_id, mut)


def update_session(user_id: str, **fields) -> dict:
    def mut(u):
        sm = ensure_reading(u)
        s = sm.get("session")
        if not isinstance(s, dict):
            s = {}
        s.update(fields)
        sm["session"] = s

    return _save(user_id, mut)


def set_reading_list(user_id: str, level: str) -> dict:
    def mut(u):
        from services.lesson_state import ensure_lesson

        ensure_lesson(u)
        ensure_reading(u)
        u["lesson"]["hub"] = "reading_list"
        u["lesson"]["level"] = level
        u["lesson"]["section"] = "Reading"

    return _save(user_id, mut)


def set_reading_hub(user_id: str, hub: str) -> dict:
    def mut(u):
        from services.lesson_state import ensure_lesson

        ensure_lesson(u)
        u["lesson"]["hub"] = hub

    return _save(user_id, mut)
