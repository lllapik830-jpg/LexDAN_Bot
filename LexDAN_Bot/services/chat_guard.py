"""
Защита раздела «Общаться» от спама:
- один ответ бота за раз на пользователя;
- отмена предыдущего TTS при новом ответе;
- debounce повторных нажатий «Общаться».
"""

from __future__ import annotations

import asyncio
import time

# uid → занят ответом до timestamp
_chat_busy_until: dict[str, float] = {}
_last_busy_notify: dict[str, float] = {}
_last_open_at: dict[str, float] = {}
_last_open_notify: dict[str, float] = {}
_voice_tasks: dict[str, asyncio.Task] = {}

CHAT_BUSY_TTL = 60.0
OPEN_DEBOUNCE_SEC = 4.0
NOTIFY_EVERY_SEC = 2.5


def try_begin_chat_reply(uid: str) -> bool:
    """True — можно начинать ответ; False — уже отвечаем."""
    now = time.time()
    until = float(_chat_busy_until.get(uid) or 0)
    if until > now:
        return False
    _chat_busy_until[uid] = now + CHAT_BUSY_TTL
    return True


def end_chat_reply(uid: str) -> None:
    _chat_busy_until.pop(str(uid), None)


def should_notify_busy(uid: str) -> bool:
    now = time.time()
    last = float(_last_busy_notify.get(uid) or 0)
    if now - last < NOTIFY_EVERY_SEC:
        return False
    _last_busy_notify[uid] = now
    return True


def try_open_chat(uid: str) -> bool:
    """False — слишком часто жмут «Общаться» (не плодим голоса)."""
    now = time.time()
    last = float(_last_open_at.get(uid) or 0)
    if now - last < OPEN_DEBOUNCE_SEC:
        return False
    _last_open_at[uid] = now
    return True


def should_notify_open_spam(uid: str) -> bool:
    now = time.time()
    last = float(_last_open_notify.get(uid) or 0)
    if now - last < NOTIFY_EVERY_SEC:
        return False
    _last_open_notify[uid] = now
    return True


def replace_voice_task(uid: str, task: asyncio.Task) -> None:
    """Новый TTS отменяет предыдущий незавершённый для этого юзера."""
    key = str(uid)
    old = _voice_tasks.pop(key, None)
    if old is not None and not old.done():
        old.cancel()
    _voice_tasks[key] = task

    def _clear(done: asyncio.Task, u: str = key) -> None:
        if _voice_tasks.get(u) is done:
            _voice_tasks.pop(u, None)

    task.add_done_callback(_clear)
