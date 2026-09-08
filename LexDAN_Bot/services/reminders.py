"""
УСТАРЕЛО: мягкие пинги 12/18 заменены на services/notify_engine.py.
"""

from __future__ import annotations


async def send_due_reminders(bot) -> int:
    return 0


def users_due_for_bot_ping(hour: int | None = None):
    return []


def users_due_for_reminder():
    return []
