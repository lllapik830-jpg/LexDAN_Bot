"""Состояние раздела «Живая речь» (пока только MANAGER_ID)."""

from __future__ import annotations

import re

from data.street_talk import PACKS, get_pack
from services.database import get_user, save_users


def street_talk_allowed(user_id: str | int | None) -> bool:
    if user_id is None:
        return False
    from config import MANAGER_ID

    try:
        return int(str(user_id).strip()) == int(MANAGER_ID)
    except (TypeError, ValueError):
        return False


def ensure_street(user: dict) -> dict:
    if "street_talk" not in user or not isinstance(user.get("street_talk"), dict):
        user["street_talk"] = {"progress": {}, "session": None}
    sm = user["street_talk"]
    if not isinstance(sm.get("progress"), dict):
        sm["progress"] = {}
    return sm


def is_pack_done(user: dict, pack_id: str) -> bool:
    sm = ensure_street(user)
    return bool(sm["progress"].get(str(pack_id)))


def _save(user_id: str, mutator) -> dict:
    from services.database import users_for

    users = users_for(user_id)
    user = get_user(users, user_id)
    ensure_street(user)
    mutator(user)
    save_users(users, only=str(user_id))
    return user


def get_session(user: dict) -> dict | None:
    sm = ensure_street(user)
    s = sm.get("session")
    return s if isinstance(s, dict) else None


def set_session(user_id: str, session: dict | None) -> dict:
    def mut(u):
        ensure_street(u)["session"] = session

    return _save(user_id, mut)


def update_session(user_id: str, **fields) -> dict:
    def mut(u):
        sm = ensure_street(u)
        s = sm.get("session")
        if not isinstance(s, dict):
            s = {}
        s.update(fields)
        sm["session"] = s

    return _save(user_id, mut)


def clear_session(user_id: str) -> dict:
    def mut(u):
        sm = ensure_street(u)
        sm["session"] = None
        lesson = u.get("lesson")
        if isinstance(lesson, dict) and str(lesson.get("hub") or "").startswith("street"):
            lesson["hub"] = "street_list"

    return _save(user_id, mut)


def mark_pack_done(user_id: str, pack_id: str) -> dict:
    def mut(u):
        sm = ensure_street(u)
        sm["progress"][str(pack_id)] = True
        sm["session"] = None

    return _save(user_id, mut)


def set_street_list(user_id: str, level: str) -> dict:
    def mut(u):
        from services.lesson_state import ensure_lesson

        ensure_lesson(u)
        ensure_street(u)
        u["lesson"]["hub"] = "street_list"
        u["lesson"]["level"] = level
        u["lesson"]["section"] = "Street"
        u["street_talk"]["session"] = None

    return _save(user_id, mut)


def set_street_hub(user_id: str, hub: str) -> dict:
    def mut(u):
        from services.lesson_state import ensure_lesson

        ensure_lesson(u)
        u["lesson"]["hub"] = hub

    return _save(user_id, mut)


def start_pack_card(user_id: str, pack_id: str) -> dict:
    def mut(u):
        from services.lesson_state import ensure_lesson

        ensure_lesson(u)
        ensure_street(u)
        u["lesson"]["hub"] = "street_card"
        u["street_talk"]["session"] = {
            "pack_id": pack_id,
            "task_i": 0,
            "attempts": 0,
        }

    return _save(user_id, mut)


def start_tasks(user_id: str) -> dict:
    def mut(u):
        from services.lesson_state import ensure_lesson

        ensure_lesson(u)
        sm = ensure_street(u)
        s = dict(sm.get("session") or {})
        s["task_i"] = 0
        s["attempts"] = 0
        sm["session"] = s
        u["lesson"]["hub"] = "street_task"

    return _save(user_id, mut)


def bump_attempt(user_id: str) -> int:
    def mut(u):
        s = dict(ensure_street(u).get("session") or {})
        s["attempts"] = int(s.get("attempts") or 0) + 1
        u["street_talk"]["session"] = s

    u = _save(user_id, mut)
    return int((get_session(u) or {}).get("attempts") or 0)


def reset_attempts(user_id: str) -> dict:
    return update_session(user_id, attempts=0)


def advance_task(user_id: str) -> dict | None:
    """Следующее задание или None, если пак закончен."""

    def mut(u):
        sm = ensure_street(u)
        s = dict(sm.get("session") or {})
        nxt = int(s.get("task_i") or 0) + 1
        s["task_i"] = nxt
        s["attempts"] = 0
        sm["session"] = s

    u = _save(user_id, mut)
    s = get_session(u) or {}
    pack = get_pack(str(s.get("pack_id") or ""))
    tasks = (pack or {}).get("tasks") or []
    if int(s.get("task_i") or 0) >= len(tasks):
        pack_id = str(s.get("pack_id") or "")
        if pack_id:
            mark_pack_done(user_id, pack_id)
        return None
    return s


def current_task(user: dict) -> dict | None:
    s = get_session(user) or {}
    pack = get_pack(str(s.get("pack_id") or ""))
    if not pack:
        return None
    tasks = pack.get("tasks") or []
    i = int(s.get("task_i") or 0)
    if i < 0 or i >= len(tasks):
        return None
    return tasks[i]


def current_pack(user: dict) -> dict | None:
    s = get_session(user) or {}
    return get_pack(str(s.get("pack_id") or ""))


def _norm(text: str) -> str:
    t = (text or "").strip().lower().replace("ё", "е")
    t = t.replace("’", "'").replace("`", "'").replace("‘", "'")
    t = t.replace("'", "")
    t = re.sub(r"[.!?,;:\"«»()\[\]{}]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def check_write(task: dict, user_text: str) -> bool:
    u = _norm(user_text)
    if not u:
        return False
    cands = {_norm(task.get("answer") or "")}
    for a in task.get("accept") or []:
        cands.add(_norm(a))
    cands.discard("")
    return u in cands


def check_mcq(task: dict, user_text: str) -> bool:
    got = (user_text or "").strip()
    ans = (task.get("answer") or "").strip()
    if got == ans:
        return True
    return _norm(got) == _norm(ans)


def check_speak(task: dict, heard: str) -> bool:
    if check_write(task, heard):
        return True
    from services.rico_tutor import answers_equivalent

    phrase = (task.get("phrase") or task.get("answer") or "").strip()
    accept = list(task.get("accept") or [])
    if phrase:
        return answers_equivalent(phrase, heard, accept)
    return False


def packs_for_list() -> list[dict]:
    return list(PACKS)
