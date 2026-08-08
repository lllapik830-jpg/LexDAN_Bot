"""
Напоминания: «ты не заходил» — не чаще 1 раза в сутки, тихие часы по Москве.
Ведут к урокам/заданиям, не к «огню дня».
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from services.database import load_users, save_users, get_user
from services.growth import ensure_growth

MSK = timezone(timedelta(hours=3))


def _now_msk() -> datetime:
    return datetime.now(MSK)


def _today() -> str:
    return _now_msk().date().isoformat()


def reminder_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Уроки")],
            [KeyboardButton(text="🗣️ Общаться"), KeyboardButton(text="📊 Профиль")],
        ],
        resize_keyboard=True,
    )


def users_due_for_reminder() -> list[tuple[str, dict]]:
    """Вернуть [(user_id, user), ...] кому пора напомнить."""
    users = load_users()
    now = _now_msk()
    hour = now.hour
    # Тихие часы 23:00–09:00 МСК
    if hour >= 23 or hour < 9:
        return []

    today = _today()
    due = []
    for uid, raw in users.items():
        if not isinstance(raw, dict):
            continue
        user = get_user(users, str(uid))
        ensure_growth(user)
        if user.get("tg_blocked"):
            continue
        if not user.get("name") or user.get("step") != "ready":
            continue
        if user.get("reminder_sent_date") == today:
            continue
        last = user.get("last_active_at") or ""
        if not last:
            continue
        try:
            last_d = datetime.fromisoformat(last)
            if last_d.tzinfo is None:
                last_d = last_d.replace(tzinfo=MSK)
        except ValueError:
            continue
        if now - last_d < timedelta(hours=20):
            continue
        due.append((str(uid), user))
    return due


async def send_due_reminders(bot) -> int:
    users = load_users()
    due = users_due_for_reminder()
    sent = 0
    dirty = False
    today = _today()
    for uid, _ in due:
        user = get_user(users, uid)
        ensure_growth(user)
        name = user.get("name") or "друг"
        streak = int(user.get("streak") or 0)
        text = (
            f"🦜 <b>Эй, {name}!</b>\n\n"
            "Рико соскучился. Давай 15 минут английского сегодня?\n"
        )
        if streak > 0:
            text += (
                f"Твоя серия сейчас <b>{streak}</b> дн. — "
                f"не прерывай её, зайди в задания 💪\n\n"
            )
        else:
            text += "\n"
        text += "Жми <b>📚 Уроки</b> — Grammar / Vocabulary / Listening."
        try:
            await bot.send_message(
                int(uid),
                text,
                reply_markup=reminder_keyboard(),
                parse_mode="HTML",
            )
            user["reminder_sent_date"] = today
            user.pop("tg_blocked", None)
            sent += 1
            dirty = True
        except Exception as e:
            err = str(e).lower()
            logging.warning(f"Reminder fail {uid}: {e}")
            if "blocked" in err or "deactivated" in err or "forbidden" in err:
                user["tg_blocked"] = True
                dirty = True
    if dirty:
        save_users(users)
    return sent
