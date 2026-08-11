"""
Напоминания о боте для free / «Общение» (399): 2 раза в день — 12:00 и 18:00 МСК.
Напоминания о заданиях (Grammar/Vocabulary) — только у полного тарифа (см. daily_reviews).
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from services.database import load_users, save_users, get_user
from services.growth import ensure_growth
from services.rewards import user_plan

MSK = timezone(timedelta(hours=3))

# Слоты мягкого пинга «загляни в бота» (МСК), только не-премиум
BOT_PING_HOURS = (12, 18)


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


def _bot_ping_text(user: dict, hour: int) -> str:
    name = user.get("name") or "друг"
    if hour == 12:
        return (
            f"🦜 <b>Привет, {name}!</b>\n\n"
            "Полдень — хорошее время заглянуть к Рико на пару минут английского.\n"
            "Жми кнопку ниже, когда будет удобно 💚"
        )
    return (
        f"🦜 <b>{name}, вечерний привет!</b>\n\n"
        "Рико на связи. Можно коротко поговорить или заглянуть в уроки — "
        "как хочешь сегодня ✨"
    )


def users_due_for_bot_ping(hour: int | None = None) -> list[tuple[str, dict, int]]:
    """
    Кому слать мягкий пинг о боте.
    Returns [(user_id, user, slot_hour), ...]
    """
    now = _now_msk()
    slot = int(hour if hour is not None else now.hour)
    if slot not in BOT_PING_HOURS:
        return []

    today = _today()
    users = load_users()
    due: list[tuple[str, dict, int]] = []
    for uid, raw in users.items():
        if not isinstance(raw, dict):
            continue
        if str(uid).startswith("__"):
            continue
        if raw.get("imitating_registration"):
            continue
        user = get_user(users, str(uid))
        ensure_growth(user)
        if user.get("tg_blocked"):
            continue
        if not user.get("name") or user.get("step") != "ready":
            continue
        # Полный тариф получает задания через daily_reviews — не дублируем
        if user_plan(user) == "full":
            continue
        slots = user.get("bot_ping_slots")
        if not isinstance(slots, dict):
            slots = {}
        day_done = slots.get(today) or []
        if not isinstance(day_done, list):
            day_done = []
        if str(slot) in {str(x) for x in day_done}:
            continue
        due.append((str(uid), user, slot))
    return due


# Совместимость со старым именем (раньше — inactivity reminder)
def users_due_for_reminder() -> list[tuple[str, dict]]:
    return [(uid, u) for uid, u, _ in users_due_for_bot_ping()]


async def send_due_reminders(bot) -> int:
    """Пинги 12:00 и 18:00 МСК для free / 399."""
    now = _now_msk()
    if now.hour not in BOT_PING_HOURS:
        return 0

    users = load_users()
    due = users_due_for_bot_ping(now.hour)
    sent = 0
    dirty = False
    today = _today()

    for uid, _, slot in due:
        user = get_user(users, uid)
        ensure_growth(user)
        text = _bot_ping_text(user, slot)
        try:
            await bot.send_message(
                int(uid),
                text,
                reply_markup=reminder_keyboard(),
                parse_mode="HTML",
            )
            slots = user.get("bot_ping_slots")
            if not isinstance(slots, dict):
                slots = {}
            day_done = list(slots.get(today) or [])
            if str(slot) not in {str(x) for x in day_done}:
                day_done.append(str(slot))
            # не раздувать историю — только сегодня + вчера
            keep = {today, (_now_msk().date() - timedelta(days=1)).isoformat()}
            slots = {d: v for d, v in slots.items() if d in keep}
            slots[today] = day_done
            user["bot_ping_slots"] = slots
            user["reminder_sent_date"] = today  # legacy-флаг
            user.pop("tg_blocked", None)
            sent += 1
            dirty = True
        except Exception as e:
            err = str(e).lower()
            logging.warning(f"Bot ping fail {uid}: {e}")
            if "blocked" in err or "deactivated" in err or "forbidden" in err:
                user["tg_blocked"] = True
                dirty = True
    if dirty:
        save_users(users)
    return sent
