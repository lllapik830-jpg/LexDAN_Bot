"""
Рост и запуск: streak, дневная цель, триал, мягкие лимиты, рефералка.
Grammar / Vocabulary не ломаем — только обёртка вокруг привычки и монетизации.
"""

from __future__ import annotations

import hashlib
import time
from datetime import datetime, timedelta, timezone

from services.database import get_user

TRIAL_DAYS = 7
REF_BONUS_DAYS = 3
FREE_CHAT_PER_DAY = 12
DAILY_WORDS_GOAL = 1
DAILY_CHAT_GOAL = 3

MSK = timezone(timedelta(hours=3))


def _today() -> str:
    return datetime.now(MSK).date().isoformat()


def _now_ts() -> float:
    return time.time()


def ensure_growth(user: dict) -> dict:
    user.setdefault("streak", 0)
    user.setdefault("streak_last_date", "")
    user.setdefault("daily", {})
    user.setdefault("referred_by", None)
    user.setdefault("invite_count", 0)
    user.setdefault("trial_started_at", 0)
    user.setdefault("premium_until", user.get("premium_until") or 0)
    user.setdefault("growth_onboarded", False)
    user.setdefault("referral_bonus_granted", False)
    user.setdefault("streak_rewards_claimed", [])
    if not isinstance(user.get("daily"), dict):
        user["daily"] = {}
    daily = user["daily"]
    if daily.get("date") != _today():
        user["daily"] = {
            "date": _today(),
            "chat_count": 0,
            "words_today": 0,
            "phrases_today": 0,
            "goal_done": False,
        }
    return user


def bind_referral_code(user_id: str, user: dict) -> str:
    ensure_growth(user)
    if user.get("referral_code"):
        return user["referral_code"]
    user["referral_code"] = hashlib.sha256(str(user_id).encode()).hexdigest()[:8]
    return user["referral_code"]


def is_premium(user: dict) -> bool:
    ensure_growth(user)
    if user.get("dev_unlock"):
        return True
    return float(user.get("premium_until") or 0) > _now_ts()


def premium_days_left(user: dict) -> int:
    """Сколько полных суток осталось (по реальному времени timestamp)."""
    ensure_growth(user)
    until = float(user.get("premium_until") or 0)
    if until <= _now_ts():
        return 0
    return max(1, int((until - _now_ts()) / 86400) + 1)


def premium_time_label(user: dict) -> str:
    """Человекочитаемый остаток: '3 дн. 5 ч.' или 'бесплатно'."""
    ensure_growth(user)
    until = float(user.get("premium_until") or 0)
    left = until - _now_ts()
    if user.get("dev_unlock"):
        return "DEV ∞"
    if left <= 0:
        return "бесплатно (лимит чата)"
    days = int(left // 86400)
    hours = int((left % 86400) // 3600)
    if days <= 0:
        return f"≈{max(1, hours)} ч."
    if hours == 0:
        return f"≈{days} дн."
    return f"≈{days} дн. {hours} ч."


def start_trial(user: dict, days: int = TRIAL_DAYS) -> None:
    ensure_growth(user)
    now = _now_ts()
    until = float(user.get("premium_until") or 0)
    target = now + days * 86400
    if until < target:
        user["premium_until"] = target
    if not user.get("trial_started_at"):
        user["trial_started_at"] = now


def extend_premium(user: dict, days: int) -> None:
    ensure_growth(user)
    now = _now_ts()
    base = max(float(user.get("premium_until") or 0), now)
    user["premium_until"] = base + days * 86400


STREAK_REWARDS = {
    3: 1,   # +1 день доступа
    7: 2,
    10: 3,
    20: 5,
    30: 7,
    50: 10,
    100: 14,
}


def touch_streak(user: dict) -> dict:
    ensure_growth(user)
    user.setdefault("streak_rewards_claimed", [])
    today = _today()
    last = user.get("streak_last_date") or ""
    info = {
        "streak": int(user.get("streak") or 0),
        "streak_up": False,
        "new_day": False,
        "reward_days": 0,
        "reward_streak": 0,
        "reward_msg": "",
    }
    if last == today:
        return info
    yesterday = (datetime.now(MSK).date() - timedelta(days=1)).isoformat()
    if last == yesterday:
        user["streak"] = int(user.get("streak") or 0) + 1
        info["streak_up"] = True
    else:
        user["streak"] = 1
        info["new_day"] = True
    user["streak_last_date"] = today
    info["streak"] = user["streak"]

    claimed = list(user.get("streak_rewards_claimed") or [])
    st = int(user["streak"])
    if st in STREAK_REWARDS and st not in claimed:
        days = STREAK_REWARDS[st]
        claimed.append(st)
        user["streak_rewards_claimed"] = claimed
        extend_premium(user, days)
        info["reward_days"] = days
        info["reward_streak"] = st
        info["reward_msg"] = (
            f"🏆 Бонус за серию <b>{st}</b> дн.! +<b>{days}</b> дн. полного доступа 🦜"
        )
    return info


def note_chat_message(user: dict) -> tuple[bool, str | None]:
    ensure_growth(user)
    touch_streak(user)
    daily = user["daily"]
    daily["chat_count"] = int(daily.get("chat_count") or 0) + 1
    _maybe_complete_goal(user)

    if is_premium(user):
        return True, None

    used = int(daily.get("chat_count") or 0)
    if used > FREE_CHAT_PER_DAY:
        return False, (
            f"🦜 <b>Лимит на сегодня</b>\n\n"
            f"На бесплатном тарифе — <b>{FREE_CHAT_PER_DAY}</b> сообщений в чате в день.\n"
            "Завтра лимит обновится.\n\n"
            "💎 Полный доступ без лимита — в профиле → <b>Подписка</b>.\n"
            f"После теста уровня даём <b>{TRIAL_DAYS} дней</b> без лимитов."
        )
    left = FREE_CHAT_PER_DAY - used
    tip = None
    if left in (3, 1):
        tip = f"🦜 Осталось сообщений в чате сегодня: <b>{left}</b>."
    return True, tip


def note_word_learned(user: dict) -> str:
    ensure_growth(user)
    streak_info = touch_streak(user)
    daily = user["daily"]
    daily["words_today"] = int(daily.get("words_today") or 0) + 1
    goal_just = _maybe_complete_goal(user)
    return format_session_wrap(
        user, kind="word", streak_info=streak_info, goal_just_done=goal_just
    )


def note_phrase_learned(user: dict) -> str:
    ensure_growth(user)
    streak_info = touch_streak(user)
    daily = user["daily"]
    daily["phrases_today"] = int(daily.get("phrases_today") or 0) + 1
    goal_just = _maybe_complete_goal(user)
    return format_session_wrap(
        user, kind="phrase", streak_info=streak_info, goal_just_done=goal_just
    )


def note_lesson_activity(user: dict) -> None:
    ensure_growth(user)
    touch_streak(user)
    _maybe_complete_goal(user)


def _maybe_complete_goal(user: dict) -> bool:
    daily = user["daily"]
    if daily.get("goal_done"):
        return False
    words_ok = int(daily.get("words_today") or 0) >= DAILY_WORDS_GOAL
    chat_ok = int(daily.get("chat_count") or 0) >= DAILY_CHAT_GOAL
    phrases_ok = int(daily.get("phrases_today") or 0) >= 1
    if words_ok or chat_ok or phrases_ok:
        daily["goal_done"] = True
        return True
    return False


def format_session_wrap(
    user: dict, *, kind: str, streak_info: dict, goal_just_done: bool
) -> str:
    ensure_growth(user)
    daily = user["daily"]
    streak = int(streak_info.get("streak") or user.get("streak") or 0)
    words_t = int(daily.get("words_today") or 0)
    phrases_t = int(daily.get("phrases_today") or 0)
    if kind == "word":
        head = f"✅ Сегодня: +1 слово (за день: {words_t})"
    else:
        head = f"✅ Сегодня: +1 фраза (за день: {phrases_t})"
    lines = ["────────", head, f"🔥 Серия: <b>{streak}</b> дн."]
    if daily.get("goal_done"):
        lines.append("🎯 Цель дня выполнена — Рико гордится 🦜")
    else:
        lines.append(f"🎯 Цель дня: слово/фраза или {DAILY_CHAT_GOAL} сообщ. в чате")
    if goal_just_done:
        lines.append("🎉 Красава, дневная норма закрыта!")
    if streak_info.get("reward_msg"):
        lines.append(streak_info["reward_msg"])
    lines.append("📅 Завтра продолжим — 15 минут с Рико.")
    return "\n".join(lines)


def apply_referral_on_start(new_user: dict, ref_code: str, all_users: dict) -> str | None:
    ensure_growth(new_user)
    if new_user.get("referred_by") or new_user.get("name"):
        return None
    ref_code = (ref_code or "").strip().lower()
    if not ref_code:
        return None
    for uid, u in all_users.items():
        if not isinstance(u, dict):
            continue
        ensure_growth(u)
        if (u.get("referral_code") or "").lower() == ref_code:
            new_user["referred_by"] = str(uid)
            return str(uid)
    return None


def grant_referral_bonuses(new_user_id: str, users: dict) -> None:
    user = get_user(users, new_user_id)
    ensure_growth(user)
    ref = user.get("referred_by")
    if not ref or user.get("referral_bonus_granted"):
        return
    user["referral_bonus_granted"] = True
    extend_premium(user, REF_BONUS_DAYS)
    if str(ref) in users:
        inviter = get_user(users, str(ref))
        ensure_growth(inviter)
        extend_premium(inviter, REF_BONUS_DAYS)
        inviter["invite_count"] = int(inviter.get("invite_count") or 0) + 1


def invite_link(bot_username: str, code: str) -> str:
    uname = (bot_username or "").lstrip("@")
    if not uname:
        return f"код: {code} (добавь BOT_USERNAME в env)"
    return f"https://t.me/{uname}?start=ref_{code}"


def subscription_blurb(user: dict) -> str:
    ensure_growth(user)
    if is_premium(user):
        status = f"✅ Активен ещё ≈ <b>{premium_days_left(user)}</b> дн."
    else:
        status = "🆓 Бесплатный тариф (лимит чата)"
    return (
        "💎 <b>Подписка LexDAN</b>\n\n"
        f"Сейчас: {status}\n\n"
        "<b>Бесплатно</b>\n"
        f"• чат до {FREE_CHAT_PER_DAY} сообщ./день\n"
        "• тест уровня\n"
        "• Vocabulary + Grammar\n\n"
        "<b>Полный доступ (оплата скоро)</b>\n"
        "• без лимита чата\n"
        "• ориентир: <b>399₽/мес</b>\n\n"
        f"🎁 После теста — <b>{TRIAL_DAYS} дней</b> полного доступа.\n"
        f"Приведи друга — оба +<b>{REF_BONUS_DAYS}</b> дня.\n\n"
        "Кнопка оплаты появится здесь позже."
    )


def profile_growth_lines(user: dict, bot_username: str = "") -> str:
    ensure_growth(user)
    code = user.get("referral_code") or "—"
    link = invite_link(bot_username, code) if code != "—" else "—"
    daily = user["daily"]
    goal = "✅ выполнена" if daily.get("goal_done") else "⏳ выучи слово/фразу или 3 сообщ. в чате"
    prem = premium_time_label(user)
    next_bonus = ""
    claimed = set(user.get("streak_rewards_claimed") or [])
    for st in sorted(STREAK_REWARDS):
        if st not in claimed and st > int(user.get("streak") or 0):
            next_bonus = f"\n🎁 След. бонус серии: <b>{st}</b> дн. → +{STREAK_REWARDS[st]} дн. доступа"
            break
    return (
        f"🔥 Серия дней: <b>{int(user.get('streak') or 0)}</b>{next_bonus}\n"
        f"🎯 Цель дня: {goal}\n"
        f"💎 Доступ: {prem}\n"
        f"   (счётчик реален: время идёт само, дни убавляются)\n"
        f"🎁 Друзей приглашено: {int(user.get('invite_count') or 0)}\n"
        f"🔗 Ссылка для друга (приглашение в бота):\n<code>{link}</code>"
    )
