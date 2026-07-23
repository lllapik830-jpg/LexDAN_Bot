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
FREE_CHAT_PER_DAY = 10
FREE_GRAMMAR_EXERCISES_PER_DAY = 8  # суммарно по всем уровням/темам
FREE_VOCAB_ITEMS_PER_DAY = 3  # слова + фразы, общий счётчик
DAILY_WORDS_GOAL = 1
DAILY_CHAT_GOAL = 3

# Тарифы (мягкий paywall — оплата подключим отдельно)
PRICE_CHAT_MONTH = 399  # безлимит только «Общение»
PRICE_FULL_MONTH = 799  # безлимит ко всему

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
    user.setdefault("last_active_at", "")
    user.setdefault("reminder_sent_date", "")
    user.setdefault("first_seen_at", user.get("first_seen_at") or _now_ts())
    user.setdefault("chat_text_total", int(user.get("chat_text_total") or 0))
    user.setdefault("chat_voice_total", int(user.get("chat_voice_total") or 0))
    if not isinstance(user.get("daily"), dict):
        user["daily"] = {}
    daily = user["daily"]
    if daily.get("date") != _today():
        user["daily"] = {
            "date": _today(),
            "chat_count": 0,
            "chat_messages_today": 0,
            "chat_text_today": 0,
            "chat_voice_today": 0,
            "lessons_completed_today": 0,
            "grammar_exercises_today": 0,
            "vocab_texts_today": 0,
            "vocab_items_today": 0,
            "words_today": 0,
            "phrases_today": 0,
            "grammar_cap": FREE_GRAMMAR_EXERCISES_PER_DAY,
            "vocab_cap": FREE_VOCAB_ITEMS_PER_DAY,
            "goal_done": False,
            "hit_chat_limit": False,
            "hit_grammar_limit": False,
            "hit_vocab_limit": False,
        }
    else:
        daily.setdefault("chat_messages_today", int(daily.get("chat_count") or 0))
        daily.setdefault("lessons_completed_today", 0)
        daily.setdefault("grammar_exercises_today", 0)
        daily.setdefault("vocab_texts_today", 0)
        daily.setdefault("vocab_items_today", 0)
        daily.setdefault("words_today", 0)
        daily.setdefault("phrases_today", 0)
        daily.setdefault("grammar_cap", FREE_GRAMMAR_EXERCISES_PER_DAY)
        daily.setdefault("vocab_cap", FREE_VOCAB_ITEMS_PER_DAY)
        daily.setdefault("chat_count", int(daily.get("chat_messages_today") or 0))
        items = int(daily.get("vocab_items_today") or 0)
        wp = int(daily.get("words_today") or 0) + int(daily.get("phrases_today") or 0)
        if wp > items:
            daily["vocab_items_today"] = wp
    user.setdefault("streak_rewards_claimed", [])
    user.setdefault("referral_qualified", 0)
    user.setdefault("lessons_until", 0)
    user.setdefault("discount_percent", 0)
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
    """Полный доступ (триал / подписка «ко всему» / DEV)."""
    ensure_growth(user)
    if user.get("dev_unlock"):
        return True
    return float(user.get("premium_until") or 0) > _now_ts()


def is_paid(user: dict) -> bool:
    """Платный/триальный полный доступ — оба суточных лимита игнорируются."""
    return is_premium(user)


def has_chat_pass(user: dict) -> bool:
    """Безлимит только на «Общение» (отдельный тариф) или полный доступ."""
    ensure_growth(user)
    if is_paid(user):
        return True
    return float(user.get("chat_until") or 0) > _now_ts()


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
        if has_chat_pass(user):
            return "безлимит общения"
        return "бесплатно"
    days = int(left // 86400)
    hours = int((left % 86400) // 3600)
    if days <= 0:
        return f"≈{max(1, hours)} ч."
    if hours == 0:
        return f"≈{days} дн."
    return f"≈{days} дн. {hours} ч."


def start_trial(user: dict, days: int = TRIAL_DAYS) -> None:
    """Выдать полный доступ на N дней (сейчас — только DEV / ручные акции)."""
    ensure_growth(user)
    now = _now_ts()
    until = float(user.get("premium_until") or 0)
    target = now + days * 86400
    if until < target:
        user["premium_until"] = target
    if not user.get("trial_started_at"):
        user["trial_started_at"] = now
        if int(user.get("streak_safes") or 0) < 1:
            user["streak_safes"] = 1


def extend_premium(user: dict, days: int) -> None:
    ensure_growth(user)
    now = _now_ts()
    base = max(float(user.get("premium_until") or 0), now)
    user["premium_until"] = base + days * 86400


STREAK_SAFE_MILESTONES = {
    7: 1,  # один сейф на 7-й день; остальное — в rewards.py
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

    # Награды лестницы (бустеры / скидки / розыгрыши)
    try:
        from services.rewards import claim_streak_rewards

        reward_msgs = claim_streak_rewards(user)
        if reward_msgs:
            extra = "\n".join(reward_msgs)
            info["reward_msg"] = (
                (info["reward_msg"] + "\n" + extra) if info.get("reward_msg") else extra
            )
    except Exception:
        pass
    return info


def touch_activity(user: dict) -> None:
    """Отметить, что пользователь сейчас активен (для напоминаний)."""
    ensure_growth(user)
    user["last_active_at"] = datetime.now(MSK).isoformat()


def note_chat_message(user: dict, *, kind: str = "text") -> tuple[bool, str | None]:
    """
    Учёт сообщений в «Общаться» (текст + голос в одном дневном лимите).
    kind: "text" | "voice" — раздельные счётчики для админки.
    Бесплатно: ровно FREE_CHAT_PER_DAY сообщений в сутки, на следующем — блок.
    """
    ensure_growth(user)
    touch_activity(user)
    touch_streak(user)
    daily = user["daily"]
    kind = "voice" if kind == "voice" else "text"

    user.setdefault("chat_text_total", 0)
    user.setdefault("chat_voice_total", 0)
    daily.setdefault("chat_text_today", 0)
    daily.setdefault("chat_voice_today", 0)

    # Синхронизация старого поля chat_count ↔ chat_messages_today
    used = int(daily.get("chat_messages_today") or 0)
    legacy = int(daily.get("chat_count") or 0)
    if legacy > used:
        used = legacy
        daily["chat_messages_today"] = used

    def _bump_kind() -> None:
        if kind == "voice":
            daily["chat_voice_today"] = int(daily.get("chat_voice_today") or 0) + 1
            user["chat_voice_total"] = int(user.get("chat_voice_total") or 0) + 1
        else:
            daily["chat_text_today"] = int(daily.get("chat_text_today") or 0) + 1
            user["chat_text_total"] = int(user.get("chat_text_total") or 0) + 1

    if has_chat_pass(user):
        daily["chat_messages_today"] = used + 1
        daily["chat_count"] = daily["chat_messages_today"]
        _bump_kind()
        _maybe_complete_goal(user)
        return True, None

    if used >= FREE_CHAT_PER_DAY:
        daily["hit_chat_limit"] = True
        user["hit_chat_limit_ever"] = True
        return False, (
            "🦜 <b>Мы здорово поболтали!</b>\n\n"
            "На сегодня хватит — мозгу и языку полезно отдохнуть.\n"
            f"(Лимит бесплатного чата: <b>{FREE_CHAT_PER_DAY}</b> сообщ. текст+голос.)\n"
            "Завтра снова можно продолжить, а полный безлимит — по кнопке ниже 👇"
        )

    daily["chat_messages_today"] = used + 1
    daily["chat_count"] = daily["chat_messages_today"]
    _bump_kind()
    if daily["chat_messages_today"] >= FREE_CHAT_PER_DAY:
        daily["hit_chat_limit"] = True
        user["hit_chat_limit_ever"] = True
    _maybe_complete_goal(user)
    return True, None


def _brain_rest_msg(*, what: str, limit: int, price: int = PRICE_FULL_MONTH) -> str:
    return (
        "🦜 <b>Мозгу нужно немного отдохнуть</b>\n\n"
        f"Ты уже хорошо позанимался: на бесплатном тарифе — "
        f"<b>{limit} {what}</b> в день.\n\n"
        "Новой информации сейчас достаточно — дай мозгу её обработать. "
        "Возвращайся через сутки и продолжим 💚\n\n"
        f"С подпиской за <b>{price}₽/мес</b> — безлимит уроков, "
        "можно заниматься сколько хочешь."
    )


def can_start_new_lesson(user: dict) -> tuple[bool, str | None]:
    """Совместимость: лимит Grammar = упражнения в сутки, не «темы»."""
    return can_do_grammar_exercise(user)


def can_do_grammar_exercise(user: dict) -> tuple[bool, str | None]:
    """Бесплатно — дневной лимит Grammar (с учётом бустов streak/реф)."""
    ensure_growth(user)
    from services.rewards import grammar_daily_cap, has_lessons_pass

    if has_lessons_pass(user):
        return True, None
    cap = grammar_daily_cap(user)
    done = int(user["daily"].get("grammar_exercises_today") or 0)
    if done >= cap:
        user["daily"]["hit_grammar_limit"] = True
        return False, _brain_rest_msg(what="заданий Grammar", limit=cap)
    return True, None


def note_grammar_exercise_done(user: dict) -> dict:
    """Учёт упражнения + серия дней / активность (как у Vocabulary и чата)."""
    ensure_growth(user)
    touch_activity(user)
    streak_info = touch_streak(user)
    daily = user["daily"]
    daily["grammar_exercises_today"] = int(daily.get("grammar_exercises_today") or 0) + 1
    from services.rewards import grammar_daily_cap, has_lessons_pass

    if (
        not has_lessons_pass(user)
        and int(daily["grammar_exercises_today"]) >= grammar_daily_cap(user)
    ):
        daily["hit_grammar_limit"] = True
    _maybe_complete_goal(user)
    return streak_info


def vocab_items_used_today(user: dict) -> int:
    ensure_growth(user)
    daily = user["daily"]
    items = int(daily.get("vocab_items_today") or 0)
    wp = int(daily.get("words_today") or 0) + int(daily.get("phrases_today") or 0)
    return max(items, wp)


def vocab_items_remaining(user: dict) -> int:
    from services.rewards import has_lessons_pass, vocab_daily_cap

    if has_lessons_pass(user):
        return 999
    return max(0, vocab_daily_cap(user) - vocab_items_used_today(user))


def can_learn_vocab_item(user: dict) -> tuple[bool, str | None]:
    """Бесплатно — дневной лимит слов/фраз (с бустами)."""
    ensure_growth(user)
    from services.rewards import has_lessons_pass, vocab_daily_cap

    if has_lessons_pass(user):
        return True, None
    cap = vocab_daily_cap(user)
    if vocab_items_used_today(user) >= cap:
        user["daily"]["hit_vocab_limit"] = True
        return False, _brain_rest_msg(what="слов или фраз Vocabulary", limit=cap)
    return True, None


def can_start_vocab_text(user: dict) -> tuple[bool, str | None]:
    """Старт текста: нужен хотя бы 1 свободный слот в дневном лимите."""
    return can_learn_vocab_item(user)


def note_vocab_text_started(user: dict) -> None:
    """Больше не списываем «текст» — лимит по изученным словам/фразам."""
    ensure_growth(user)


def note_lesson_completed(user: dict) -> None:
    """Тема Grammar закрыта — для статистики; дневной лимит идёт по упражнениям."""
    ensure_growth(user)
    if is_paid(user):
        return
    daily = user["daily"]
    daily["lessons_completed_today"] = int(daily.get("lessons_completed_today") or 0) + 1


def note_word_learned(user: dict) -> str:
    ensure_growth(user)
    touch_activity(user)
    streak_info = touch_streak(user)
    daily = user["daily"]
    daily["words_today"] = int(daily.get("words_today") or 0) + 1
    from services.rewards import has_lessons_pass, vocab_daily_cap

    if not has_lessons_pass(user):
        daily["vocab_items_today"] = vocab_items_used_today(user)
    goal_just = _maybe_complete_goal(user)
    wrap = format_session_wrap(
        user, kind="word", streak_info=streak_info, goal_just_done=goal_just
    )
    if not has_lessons_pass(user) and vocab_items_used_today(user) >= vocab_daily_cap(user):
        wrap = (wrap + "\n\n" if wrap else "") + _brain_rest_msg(
            what="слов или фраз Vocabulary",
            limit=vocab_daily_cap(user),
        )
    return wrap


def note_phrase_learned(user: dict) -> str:
    ensure_growth(user)
    touch_activity(user)
    streak_info = touch_streak(user)
    daily = user["daily"]
    daily["phrases_today"] = int(daily.get("phrases_today") or 0) + 1
    from services.rewards import has_lessons_pass, vocab_daily_cap

    if not has_lessons_pass(user):
        daily["vocab_items_today"] = vocab_items_used_today(user)
    goal_just = _maybe_complete_goal(user)
    wrap = format_session_wrap(
        user, kind="phrase", streak_info=streak_info, goal_just_done=goal_just
    )
    if not has_lessons_pass(user) and vocab_items_used_today(user) >= vocab_daily_cap(user):
        wrap = (wrap + "\n\n" if wrap else "") + _brain_rest_msg(
            what="слов или фраз Vocabulary",
            limit=vocab_daily_cap(user),
        )
    return wrap


def note_lesson_activity(user: dict) -> None:
    ensure_growth(user)
    touch_activity(user)
    touch_streak(user)
    _maybe_complete_goal(user)


def _maybe_complete_goal(user: dict) -> bool:
    daily = user["daily"]
    if daily.get("goal_done"):
        return False
    words_ok = int(daily.get("words_today") or 0) >= DAILY_WORDS_GOAL
    chat_ok = int(daily.get("chat_count") or 0) >= DAILY_CHAT_GOAL
    phrases_ok = int(daily.get("phrases_today") or 0) >= 1
    grammar_ok = int(daily.get("grammar_exercises_today") or 0) >= 1
    if words_ok or chat_ok or phrases_ok or grammar_ok:
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
    """При регистрации по ссылке: считаем старт + welcome-буст другу (без +3 дней премиума)."""
    user = get_user(users, new_user_id)
    ensure_growth(user)
    ref = user.get("referred_by")
    if not ref or user.get("referral_bonus_granted"):
        return
    user["referral_bonus_granted"] = True
    from services.rewards import grant_invitee_welcome_boost

    grant_invitee_welcome_boost(user)
    if str(ref) in users:
        inviter = get_user(users, str(ref))
        ensure_growth(inviter)
        inviter["invite_count"] = int(inviter.get("invite_count") or 0) + 1


def invite_link(bot_username: str, code: str) -> str:
    uname = (bot_username or "").lstrip("@")
    if not uname:
        return ""
    return f"https://t.me/{uname}?start=ref_{code}"


def subscription_blurb(user: dict) -> str:
    ensure_growth(user)
    from services.pricing import discount_blurb, lottery_status_lines

    if is_premium(user):
        status = f"✅ Полный доступ ещё ≈ <b>{premium_days_left(user)}</b> дн."
    elif has_chat_pass(user):
        status = "✅ Безлимит «Общение» активен"
    else:
        status = "🆓 Бесплатный тариф"

    auto_line = ""
    if user.get("sub_auto") and user.get("yookassa_payment_method_id"):
        auto_line = "\n🔁 Автопродление: <b>вкл</b>"

    return (
        "💎 <b>Тарифы LexDAN</b>\n\n"
        f"Сейчас: {status}{auto_line}\n"
        f"{discount_blurb(user)}"
        f"{lottery_status_lines(user)}\n"
        "<b>Бесплатно</b>\n"
        f"• Vocabulary — до {FREE_VOCAB_ITEMS_PER_DAY} слов/фраз в день\n"
        f"• Grammar — до {FREE_GRAMMAR_EXERCISES_PER_DAY} заданий в день (все уровни)\n"
        f"• общение — до {FREE_CHAT_PER_DAY} сообщ./день\n"
        "• тест уровня\n\n"
        f"<b>💬 Только общение</b> — <b>{PRICE_CHAT_MONTH}₽/мес</b>\n"
        "• безлимит чата (текст + голос)\n\n"
        f"<b>🚀 Безлимит ко всему</b> — <b>{PRICE_FULL_MONTH}₽/мес</b>\n"
        "• уроки без лимита\n"
        "• безлимит общения\n\n"
        "🔥 Серия дней и 🎁 друзья дают бустеры — смотри в профиле."
    )


def profile_growth_lines(user: dict, bot_username: str = "") -> str:
    ensure_growth(user)
    code = user.get("referral_code") or "—"
    link = invite_link(bot_username, code) if code != "—" else ""
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
    if link:
        ref_line = f"Твоя ссылка для друга:\n<code>{link}</code>"
    else:
        ref_line = "Твоя ссылка для друга: скоро появится"
    return (
        f"{streak_line}\n"
        f"🛡️ Стрик-сейфы: <b>{safes}</b>{next_safe}{restore_hint}\n"
        f"🎯 Цель дня: {goal}\n"
        f"💎 Доступ: {prem}\n"
        f"🎁 Друзей приглашено: {int(user.get('invite_count') or 0)} "
        f"(засчитано: {int(user.get('referral_qualified') or 0)})\n"
        f"{ref_line}"
    )
