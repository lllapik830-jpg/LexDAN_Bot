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
    user.setdefault("streak_safes", 0)
    user.setdefault("streak_safe_milestones_claimed", [])
    user.setdefault("streak_pending_restore", 0)
    user.setdefault("streak_burned", False)
    user.setdefault("streak_burn_date", "")
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
    # Окно восстановления — только в день возврата
    if (
        user.get("streak_burned")
        and user.get("streak_burn_date")
        and user.get("streak_burn_date") != _today()
    ):
        user["streak_burned"] = False
        user["streak_pending_restore"] = 0
        user["streak_burn_date"] = ""
    detect_streak_break(user)
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
        # Стартовый сейф «на дорожку» (один раз с триалом)
        if int(user.get("streak_safes") or 0) < 1:
            user["streak_safes"] = 1


def extend_premium(user: dict, days: int) -> None:
    ensure_growth(user)
    now = _now_ts()
    base = max(float(user.get("premium_until") or 0), now)
    user["premium_until"] = base + days * 86400


STREAK_SAFE_MILESTONES = {
    7: 1,
    14: 1,
    30: 1,
    50: 1,
    100: 1,
}

BTN_RESTORE_STREAK = "🛡️ Восстановить серию"


def detect_streak_break(user: dict) -> bool:
    """Пропуск дня → серия сгорает; значение можно вернуть сейфом."""
    today = _today()
    last = user.get("streak_last_date") or ""
    streak = int(user.get("streak") or 0)
    if streak <= 0 or not last:
        return False
    yesterday = (datetime.now(MSK).date() - timedelta(days=1)).isoformat()
    if last in {today, yesterday}:
        return False
    if user.get("streak_burned") and int(user.get("streak_pending_restore") or 0) > 0:
        return False
    user["streak_pending_restore"] = streak
    user["streak_burned"] = True
    user["streak_burn_date"] = _today()
    user["streak"] = 0
    return True


def can_restore_streak(user: dict) -> bool:
    ensure_growth(user)
    return (
        bool(user.get("streak_burned"))
        and int(user.get("streak_pending_restore") or 0) > 0
        and int(user.get("streak_safes") or 0) > 0
    )


def restore_streak(user: dict) -> tuple[bool, str]:
    ensure_growth(user)
    if not can_restore_streak(user):
        if int(user.get("streak_pending_restore") or 0) <= 0:
            return False, "🦜 Сейчас нечего восстанавливать — серия не сгорала."
        if int(user.get("streak_safes") or 0) <= 0:
            return False, (
                "🦜 Сейфов нет 😢\n"
                "Их дают за серию: 7 / 14 / 30 / 50 / 100 дней подряд."
            )
        return False, "🦜 Восстановить серию сейчас нельзя."

    restored = int(user["streak_pending_restore"])
    user["streak_safes"] = int(user["streak_safes"]) - 1
    user["streak"] = restored
    user["streak_last_date"] = _today()
    user["streak_pending_restore"] = 0
    user["streak_burned"] = False
    user["streak_burn_date"] = ""
    left = int(user["streak_safes"])
    return True, (
        f"🛡️ <b>Серия восстановлена!</b>\n\n"
        f"Снова <b>{restored}</b> дн. подряд 🔥\n"
        f"Сейфов осталось: <b>{left}</b>"
    )


def grant_safe(user: dict, n: int = 1) -> None:
    ensure_growth(user)
    user["streak_safes"] = int(user.get("streak_safes") or 0) + max(0, n)


def touch_streak(user: dict) -> dict:
    ensure_growth(user)
    today = _today()
    last = user.get("streak_last_date") or ""
    info = {
        "streak": int(user.get("streak") or 0),
        "streak_up": False,
        "new_day": False,
        "reward_msg": "",
        "burned": False,
        "pending_restore": int(user.get("streak_pending_restore") or 0),
    }

    if last == today:
        info["streak"] = int(user.get("streak") or 0)
        return info

    yesterday = (datetime.now(MSK).date() - timedelta(days=1)).isoformat()

    # Сгоревшая серия: начинаем с 1, кнопка restore ещё доступна
    if user.get("streak_burned") and int(user.get("streak_pending_restore") or 0) > 0:
        user["streak"] = 1
        user["streak_last_date"] = today
        info["new_day"] = True
        info["burned"] = True
        info["streak"] = 1
        info["pending_restore"] = int(user.get("streak_pending_restore") or 0)
        if can_restore_streak(user):
            info["reward_msg"] = (
                f"⚠️ Серия сгорела (было {info['pending_restore']} дн.).\n"
                f"В профиле жми <b>{BTN_RESTORE_STREAK}</b> — сейфов: "
                f"{int(user.get('streak_safes') or 0)}"
            )
        else:
            info["reward_msg"] = (
                f"⚠️ Серия сгорела (было {info['pending_restore']} дн.). "
                "Сейфов нет — копи новую 💪"
            )
        return info

    if last == yesterday:
        user["streak"] = int(user.get("streak") or 0) + 1
        info["streak_up"] = True
        user["streak_burned"] = False
        user["streak_pending_restore"] = 0
    else:
        user["streak"] = 1
        info["new_day"] = True

    user["streak_last_date"] = today
    info["streak"] = int(user["streak"])

    claimed = list(user.get("streak_safe_milestones_claimed") or [])
    st = int(user["streak"])
    if st in STREAK_SAFE_MILESTONES and st not in claimed:
        n = STREAK_SAFE_MILESTONES[st]
        claimed.append(st)
        user["streak_safe_milestones_claimed"] = claimed
        grant_safe(user, n)
        info["reward_msg"] = (
            f"🛡️ Бонус серии <b>{st}</b> дн.! +<b>{n}</b> стрик-сейф "
            f"(всего: {int(user['streak_safes'])})"
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
    safes = int(user.get("streak_safes") or 0)
    pending = int(user.get("streak_pending_restore") or 0)
    streak_line = f"🔥 Серия дней: <b>{int(user.get('streak') or 0)}</b>"
    if pending > 0 and user.get("streak_burned"):
        streak_line += f" (сгорела с {pending} — можно восстановить)"
    next_safe = ""
    claimed = set(user.get("streak_safe_milestones_claimed") or [])
    for st in sorted(STREAK_SAFE_MILESTONES):
        if st not in claimed and st > int(user.get("streak") or 0):
            next_safe = f"\n🎁 След. сейф за серию: <b>{st}</b> дн."
            break
    restore_hint = ""
    if can_restore_streak(user):
        restore_hint = f"\n👉 Жми кнопку <b>{BTN_RESTORE_STREAK}</b> ниже"
    return (
        f"{streak_line}\n"
        f"🛡️ Стрик-сейфы: <b>{safes}</b>{next_safe}{restore_hint}\n"
        f"🎯 Цель дня: {goal}\n"
        f"💎 Доступ: {prem}\n"
        f"   (время доступа реальное — дни убавляются сами)\n"
        f"🎁 Друзей приглашено: {int(user.get('invite_count') or 0)}\n"
        f"🔗 Ссылка для друга:\n<code>{link}</code>"
    )
