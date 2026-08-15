"""Состояние раздела «Живая речь» (пока только MANAGER_ID)."""

from __future__ import annotations

import re

from data.street_talk import get_pack, packs_for_level, slide_count
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


def start_pack(user_id: str, pack_id: str) -> dict:
    def mut(u):
        from services.lesson_state import ensure_lesson

        ensure_lesson(u)
        ensure_street(u)
        u["lesson"]["hub"] = "street_slide"
        u["street_talk"]["session"] = {
            "pack_id": pack_id,
            "slide_i": 0,
            "attempts": 0,
            "card_msg_id": None,
            "voice_msg_id": None,
            "heard_msg_id": None,
            "remind_msg_id": None,
        }

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


def current_pack(user: dict) -> dict | None:
    s = get_session(user) or {}
    return get_pack(str(s.get("pack_id") or ""))


def decode_slide(pack: dict | None, slide_i: int) -> dict:
    if not pack:
        return {"kind": "done"}
    items = pack.get("items") or []
    produce = pack.get("produce") or []
    i = int(slide_i or 0)
    if i <= 0:
        return {"kind": "intro"}
    if i <= len(items):
        return {
            "kind": "item",
            "item": items[i - 1],
            "n": i,
            "total": len(items),
        }
    p = i - 1 - len(items)
    if p < len(produce):
        return {
            "kind": "produce",
            "task": produce[p],
            "n": p + 1,
            "total": len(produce),
        }
    return {"kind": "done"}


def current_slide(user: dict) -> dict:
    pack = current_pack(user)
    s = get_session(user) or {}
    return decode_slide(pack, int(s.get("slide_i") or 0))


def go_next(user_id: str) -> dict | None:
    """Следующий слайд или None, если пак закончен."""

    def mut(u):
        s = dict(ensure_street(u).get("session") or {})
        s["slide_i"] = int(s.get("slide_i") or 0) + 1
        s["attempts"] = 0
        u["street_talk"]["session"] = s

    u = _save(user_id, mut)
    s = get_session(u) or {}
    pack = get_pack(str(s.get("pack_id") or ""))
    if not pack or int(s.get("slide_i") or 0) >= slide_count(pack):
        pack_id = str(s.get("pack_id") or "")
        if pack_id:
            mark_pack_done(user_id, pack_id)
        return None
    return s


def go_prev(user_id: str) -> str:
    """intro_back — уйти к списку; ok — остаться в слайдах."""
    from services.database import users_for

    users = users_for(user_id)
    user = get_user(users, user_id)
    ensure_street(user)
    s = dict((user.get("street_talk") or {}).get("session") or {})
    i = int(s.get("slide_i") or 0)
    if i <= 0:
        return "intro_back"
    s["slide_i"] = i - 1
    s["attempts"] = 0
    user["street_talk"]["session"] = s
    save_users(users, only=str(user_id))
    return "ok"


def _norm(text: str) -> str:
    t = (text or "").strip().lower().replace("ё", "е")
    t = t.replace("’", "'").replace("`", "'").replace("‘", "'")
    t = t.replace("'", "")
    t = re.sub(r"[.!?,;:\"«»()\[\]{}]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def check_item_speak(item: dict, heard: str) -> bool:
    if not (heard or "").strip():
        return False
    if check_write_like(item.get("accept") or [], heard):
        return True
    from services.rico_tutor import answers_equivalent

    example = (item.get("example") or item.get("voice_en") or "").strip()
    accept = list(item.get("accept") or [])
    if example and answers_equivalent(example, heard, accept):
        return True
    # мягко: в расшифровке есть сжатая или полная форма
    u = _norm(heard)
    for token in (item.get("form"), item.get("full")):
        n = _norm(token or "")
        if n and n in u:
            return True
    return False


def check_write_like(accept: list[str], heard: str) -> bool:
    u = _norm(heard)
    if not u:
        return False
    for a in accept:
        n = _norm(a)
        if n and (u == n or n in u or u in n):
            return True
    return False


def check_produce(task: dict, heard: str) -> bool:
    u = _norm(heard)
    if not u:
        return False
    words = u.split()
    if len(words) < int(task.get("min_words") or 3):
        return False
    for m in task.get("must") or []:
        n = _norm(m)
        if n and n in u:
            return True
    return False


def packs_for_list(level: str | None = None) -> list[dict]:
    return packs_for_level(level)
