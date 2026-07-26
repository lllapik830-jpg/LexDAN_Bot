"""Состояние и прогресс раздела Listening."""

from __future__ import annotations

from datetime import date

from services.database import load_users, get_user, save_users


def ensure_listening(user: dict) -> dict:
    if "listening" not in user or not isinstance(user.get("listening"), dict):
        user["listening"] = {"progress": {}, "session": None, "daily_date": "", "daily_used": 0}
    sm = user["listening"]
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
    sm = ensure_listening(user)
    return bool(sm["progress"].get(progress_key(level, topic_id)))


def _today() -> str:
    return date.today().isoformat()


def listening_daily_cap(user: dict) -> int | None:
    """None = безлимит (799 / триал). Иначе дневной лимит ситуаций."""
    from services.rewards import user_plan

    if user_plan(user) == "full":
        return None
    return 1  # free + 399

def listening_used_today(user: dict) -> int:
    sm = ensure_listening(user)
    if sm.get("daily_date") != _today():
        return 0
    return int(sm.get("daily_used") or 0)


def can_start_listening(user: dict) -> tuple[bool, str]:
    """Можно ли начать новую ситуацию сегодня."""
    cap = listening_daily_cap(user)
    if cap is None:
        return True, ""
    used = listening_used_today(user)
    if used >= cap:
        return (
            False,
            "🎧 На твоём тарифе — <b>1 ситуация Listening в день</b>.\n"
            "Лимит на сегодня уже использован. Завтра снова можно, "
            "или открой полный доступ (799₽) без дневного лимита.",
        )
    return True, ""


def consume_listening_slot(user_id: str) -> dict:
    """Списать одну ситуацию за сегодня (при старте диалога)."""

    def mut(u):
        sm = ensure_listening(u)
        today = _today()
        if sm.get("daily_date") != today:
            sm["daily_date"] = today
            sm["daily_used"] = 0
        sm["daily_used"] = int(sm.get("daily_used") or 0) + 1

    return _save(user_id, mut)


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
