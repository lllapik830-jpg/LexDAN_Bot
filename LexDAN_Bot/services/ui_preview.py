"""
Превью правок оформления: покажет только MANAGER_ID.
Когда ок — пользователь говорит «заливай», убираем флаг / включаем всем.
"""

from __future__ import annotations


def ui_preview_only(user_id: str | int | None = None, user: dict | None = None) -> bool:
    """True — этот человек видит новые тексты/UI до общего релиза."""
    from config import MANAGER_ID

    uid = user_id
    if uid is None and isinstance(user, dict):
        uid = user.get("tg_id") or user.get("telegram_id") or user.get("id")
    if uid is None:
        return False
    try:
        return int(str(uid).strip()) == int(MANAGER_ID)
    except Exception:
        return False
