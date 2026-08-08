"""
Награды за streak и рефералку — каталоги по тарифам + выдача бустов.
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone

from services.growth import (
    FREE_GRAMMAR_EXERCISES_PER_DAY,
    FREE_LESSON_POINTS_PER_DAY,
    FREE_VOCAB_ITEMS_PER_DAY,
    PRICE_CHAT_MONTH,
    PRICE_FULL_MONTH,
    ensure_growth,
    extend_premium,
    is_premium,
)

MSK = timezone(timedelta(hours=3))

BTN_STREAK = "🔥 Серия дней"
BTN_REFERRAL = "🎁 Пригласить друга"

# Сколько grammar-заданий должен сделать друг, чтобы засчитаться (3 темы × 8)
REF_QUALIFY_EXERCISES = 24


def _now_ts() -> float:
    return time.time()


def _today() -> str:
    return datetime.now(MSK).date().isoformat()


def user_plan(user: dict) -> str:
    """free | chat (399) | full (799 / триал / DEV)."""
    ensure_growth(user)
    if is_premium(user):
        return "full"
    if float(user.get("chat_until") or 0) > _now_ts():
        return "chat"
    return "free"


def plan_label(plan: str) -> str:
    return {
        "free": "начальная",
        "chat": "продвинутая",
        "full": "премиальная",
    }.get(plan, plan)


def has_lessons_pass(user: dict) -> bool:
    ensure_growth(user)
    if is_premium(user):
        return True
    return float(user.get("lessons_until") or 0) > _now_ts()


def extend_chat_pass(user: dict, days: float = 1) -> None:
    ensure_growth(user)
    now = _now_ts()
    base = max(float(user.get("chat_until") or 0), now)
    user["chat_until"] = base + days * 86400


def extend_lessons_pass(user: dict, days: float = 1) -> None:
    ensure_growth(user)
    now = _now_ts()
    base = max(float(user.get("lessons_until") or 0), now)
    user["lessons_until"] = base + days * 86400


def grammar_daily_cap(user: dict) -> int:
    """Дневной потолок баллов уроков (совместимое имя для бустов/админки)."""
    ensure_growth(user)
    if has_lessons_pass(user):
        return 10_000
    daily = user["daily"]
    return int(
        daily.get("lesson_points_cap")
        or daily.get("grammar_cap")
        or FREE_LESSON_POINTS_PER_DAY
    )


def vocab_daily_cap(user: dict) -> int:
    """Дневной потолок слов/фраз Vocabulary (отдельный от Grammar)."""
    ensure_growth(user)
    if has_lessons_pass(user):
        return 10_000
    daily = user["daily"]
    return int(daily.get("vocab_cap") or FREE_VOCAB_ITEMS_PER_DAY)


def set_grammar_cap_today(user: dict, cap: int) -> None:
    ensure_growth(user)
    cur = int(
        user["daily"].get("lesson_points_cap")
        or user["daily"].get("grammar_cap")
        or FREE_LESSON_POINTS_PER_DAY
    )
    boosted = max(cur, int(cap))
    user["daily"]["lesson_points_cap"] = boosted
    user["daily"]["grammar_cap"] = boosted


def set_vocab_cap_today(user: dict, cap: int) -> None:
    ensure_growth(user)
    cur = int(user["daily"].get("vocab_cap") or FREE_VOCAB_ITEMS_PER_DAY)
    user["daily"]["vocab_cap"] = max(cur, int(cap))


STREAK_MILESTONES = (7, 14, 30, 50, 100)


def streak_reward_text(plan: str, days: int) -> str:
    table = {
        "free": {
            7: "Бустер уроков: сегодня до <b>24</b> баллов вместо 10",
            14: "🔐 Секрет Рико: <b>Разбор твоей недели</b> (кнопка в главном меню)",
            30: "Безлимит «Общение» на <b>сутки</b>",
            50: "Скидка <b>50%</b> на любой тариф на 1 месяц",
            100: f"Месяц тарифа «Общение» ({PRICE_CHAT_MONTH}₽) — бесплатно",
        },
        "chat": {
            7: "Бустер уроков: сегодня до <b>24</b> баллов вместо 10",
            14: "🔐 Секрет Рико: <b>Разбор твоей недели</b> (кнопка в главном меню)",
            30: "Безлимит <b>уроков</b> на сутки",
            50: "Скидка <b>50%</b> на любой тариф на 1 месяц",
            100: "Бесплатно <b>10 дней</b> полного доступа к урокам",
        },
        "full": {
            7: "🔐 Секреты Рико: <b>Разбор недели</b> + <b>Голос дня</b> (акценты)",
            14: "🗣 ещё один <b>Голос дня</b> + билет в реф-розыгрыш",
            30: "Билет в розыгрыш полугодовой подписки (среди 30-дневных на 799)",
            50: "Ещё один <b>Голос дня</b> с разными акцентами",
            100: "Билет в розыгрыш <b>15 000₽</b> (среди 100-дневных на 799)",
        },
    }
    return table.get(plan, table["free"]).get(days, "—")


def format_streak_rewards_message(user: dict) -> str:
    ensure_growth(user)
    plan = user_plan(user)
    streak = int(user.get("streak") or 0)
    claimed = set(user.get("streak_rewards_claimed") or [])
    lines = [
        "🔥 <b>Серия дней — награды</b>\n",
        f"Сейчас: серия <b>{streak}</b> дн. · тариф: <b>{plan_label(plan)}</b>\n",
        "Занимайся каждый день — награды по ступеням:\n",
    ]
    for d in STREAK_MILESTONES:
        key = f"{plan}:{d}"
        got = key in claimed or d in claimed
        if got:
            mark, status = "✅", " — получено"
        elif streak >= d:
            mark, status = "👉", " — начислено"
        else:
            mark, status = "▫️", f" — ещё {d - streak} дн."
        lines.append(f"{mark} <b>{d} дн.</b>{status}\n{streak_reward_text(plan, d)}\n")
    lines.append(
        "🛡️ Стрик-сейфы: <b>30</b>, <b>70</b>, <b>100</b>, <b>150</b> "
        "и дальше каждые <b>30</b> дней серии.\n"
        "Пропуск дня в 00:00 МСК: если есть сейф — списывается сам и серия живёт; "
        "если нет — серия обнуляется (в тот же день ещё можно восстановить кнопкой)."
    )
    if plan in {"free", "chat"}:
        lines.append(
            "\n💎 С <b>премиальной</b> подпиской (799₽) призы ценнее: "
            "эксклюзивный контент Рико и розыгрыши."
        )
    return "\n".join(lines)


def claim_streak_rewards(user: dict) -> list[str]:
    ensure_growth(user)
    plan = user_plan(user)
    streak = int(user.get("streak") or 0)
    claimed = list(user.get("streak_rewards_claimed") or [])
    msgs: list[str] = []
    for d in STREAK_MILESTONES:
        key = f"{plan}:{d}"
        # совместимость со старым форматом [7, 14, ...]
        if streak < d or key in claimed or d in claimed:
            continue
        msg = _grant_streak_reward(user, plan, d)
        claimed.append(key)
        if msg:
            msgs.append(msg)
    user["streak_rewards_claimed"] = claimed
    return msgs


def _grant_streak_reward(user: dict, plan: str, days: int) -> str:
    if plan == "free":
        if days == 7:
            set_grammar_cap_today(user, 24)
            return "🔥 7 дней! Бустер: сегодня Grammar до <b>24</b> заданий."
        if days == 14:
            from services.secret_missions import unlock_mission, MISSION_WEEK

            unlock_mission(user, MISSION_WEEK)
            return (
                "🔥 14 дней! Открыт секрет Рико: <b>Разбор твоей недели</b> 📝\n"
                "В меню появится <b>🔐 Секрет Рико</b> — 5 карточек правок "
                "«как сказал бы носитель»."
            )
        if days == 30:
            extend_chat_pass(user, 1)
            return "🔥 30 дней! Безлимит «Общение» на <b>сутки</b>."
        if days == 50:
            user["discount_percent"] = max(int(user.get("discount_percent") or 0), 50)
            user["discount_note"] = "streak_50"
            return "🔥 50 дней! Скидка <b>50%</b> на любой тариф (при оплате)."
        if days == 100:
            extend_chat_pass(user, 30)
            return f"🔥 100 дней! Месяц тарифа «Общение» ({PRICE_CHAT_MONTH}₽)."
        return ""

    if plan == "chat":
        if days == 7:
            set_grammar_cap_today(user, 24)
            return "🔥 7 дней! Бустер: сегодня до <b>24</b> баллов на уроки."
        if days == 14:
            from services.secret_missions import unlock_mission, MISSION_WEEK

            unlock_mission(user, MISSION_WEEK)
            return (
                "🔥 14 дней на «Общение»! Секрет Рико: <b>Разбор твоей недели</b> 📝\n"
                "Кнопка <b>🔐 Секрет Рико</b> в меню — разберём типичные ошибки "
                "и твои фразы из чата."
            )
        if days == 30:
            extend_lessons_pass(user, 1)
            return "🔥 30 дней! Безлимит <b>уроков</b> на сутки."
        if days == 50:
            user["discount_percent"] = max(int(user.get("discount_percent") or 0), 50)
            user["discount_note"] = "streak_50_chat"
            return "🔥 50 дней! Скидка <b>50%</b> на любой тариф."
        if days == 100:
            extend_lessons_pass(user, 10)
            return "🔥 100 дней! <b>10 дней</b> доступа к урокам."
        return ""

    # full (799 / триал)
    if days == 7:
        from services.secret_missions import unlock_mission, MISSION_WEEK, MISSION_VOICE

        unlock_mission(user, MISSION_WEEK)
        unlock_mission(user, MISSION_VOICE)
        return (
            "🔥 7 дней на 799! Два секрета Рико:\n"
            "📝 <b>Разбор недели</b> и 🗣 <b>Голос дня</b> "
            "(4 фразы разными акцентами из наших голосов).\n"
            "Кнопка <b>🔐 Секрет Рико</b> — в главном меню!"
        )
    if days == 14:
        from services.secret_missions import unlock_mission, MISSION_VOICE

        unlock_mission(user, MISSION_VOICE)
        user["referral_lottery_tickets"] = int(user.get("referral_lottery_tickets") or 0) + 1
        return (
            "🔥 14 дней на 799!\n"
            "🗣 ещё один <b>Голос дня</b> · "
            "🎟 <b>+1</b> билет в реф-розыгрыш.\n"
            "Секрет — в меню <b>🔐 Секрет Рико</b>."
        )
    if days == 30:
        user["lottery_30"] = True
        user["lottery_30_entered_at"] = _today()
        return (
            "🔥 30 дней! 🎟 Билет в розыгрыш <b>полугодовой</b> подписки 799 "
            "засчитан. Смотри статус в профиле → Подписка."
        )
    if days == 50:
        from services.secret_missions import unlock_mission, MISSION_VOICE

        user["exclusive_rico_tasks"] = True
        unlock_mission(user, MISSION_VOICE)
        return (
            "🔥 50 дней! Ещё один <b>Голос дня</b> — 4 фразы разными акцентами "
            "(Adam, British, American, AU).\n"
            "Кнопка <b>🔐 Секрет Рико</b> в меню."
        )
    if days == 100:
        user["lottery_100"] = True
        user["lottery_100_entered_at"] = _today()
        return (
            "🔥 100 дней! 🎟 Ты в розыгрыше <b>15 000₽</b>. "
            "Билет активен — статус в профиле → Подписка."
        )
    return ""


def extend_sections_unlock(user: dict, days: int = 7) -> None:
    ensure_growth(user)
    now = _now_ts()
    base = max(float(user.get("sections_unlock_until") or 0), now)
    user["sections_unlock_until"] = base + days * 86400


def has_sections_unlock(user: dict) -> bool:
    ensure_growth(user)
    return float(user.get("sections_unlock_until") or 0) > _now_ts()


def count_grammar_exercises_done(user: dict) -> int:
    gp = user.get("grammar_progress") or {}
    total = 0
    for nums in (gp.get("completed_exercises") or {}).values():
        total += len(nums or [])
    return total


def format_referral_rewards_message(user: dict, bot_username: str = "") -> str:
    from services.growth import invite_link

    ensure_growth(user)
    plan = user_plan(user)
    code = user.get("referral_code") or ""
    link = invite_link(bot_username, code) if code else ""
    qualified = int(user.get("referral_qualified") or 0)
    started = int(user.get("invite_count") or 0)

    lines = [
        "🎁 <b>Приведи друга</b>\n",
        f"Твой тариф: <b>{plan_label(plan)}</b>\n",
        f"Приглашено (старт): <b>{started}</b> · засчитано (3 темы): <b>{qualified}</b>\n",
    ]
    if link:
        lines.append(f"Ссылка:\n<code>{link}</code>\n")
    else:
        lines.append("Ссылка появится после настройки BOT_USERNAME.\n")

    lines.append(
        "<b>Условие засчёта друга</b>\n"
        f"Друг выполняет <b>{REF_QUALIFY_EXERCISES} заданий</b> Grammar "
        "(≈3 темы × 8). На бесплатном это минимум ~3 дня.\n"
    )

    if plan == "free":
        lines.append(
            "<b>Тебе (бесплатный тариф)</b>\n"
            "1️⃣ → Grammar <b>16</b>/сутки\n"
            "2️⃣ → Grammar <b>32</b>/сутки\n"
            "3️⃣ → Grammar <b>48</b>/сутки + <b>10</b> слов Vocabulary\n"
        )
    elif plan == "chat":
        lines.append(
            "<b>Тебе (тариф Общение)</b>\n"
            "Каждый засчитанный друг → <b>+3 дня</b> общения "
            "+ бустер Grammar (16 → 32 → 48).\n"
        )
    else:
        lines.append(
            "<b>Тебе (тариф 799)</b>\n"
            "Каждый засчитанный друг → <b>+3 дня</b> полного доступа "
            "+ билет в реф-розыгрыш.\n"
        )

    lines.append(
        "<b>Что получает друг</b>\n"
        "• В день старта по ссылке — Grammar до <b>12</b> заданий\n"
        "• Когда закроет 3 темы — реферальный прогресс засчитан + буст дня\n"
    )
    return "\n".join(lines)


def grant_invitee_welcome_boost(user: dict) -> None:
    ensure_growth(user)
    if user.get("invitee_welcome_boost_done"):
        return
    user["invitee_welcome_boost_done"] = True
    set_grammar_cap_today(user, 12)


def on_invitee_qualified(inviter: dict, invitee: dict) -> tuple[str, str]:
    """Возвращает (сообщение пригласившему, сообщение другу)."""
    ensure_growth(inviter)
    ensure_growth(invitee)

    if invitee.get("referral_qualified_done"):
        return "", ""
    invitee["referral_qualified_done"] = True

    q = int(inviter.get("referral_qualified") or 0) + 1
    inviter["referral_qualified"] = q
    plan = user_plan(inviter)
    msgs: list[str] = []

    if q == 1:
        set_grammar_cap_today(inviter, 16)
        msgs.append("Grammar сегодня до <b>16</b>")
    elif q == 2:
        set_grammar_cap_today(inviter, 32)
        msgs.append("Grammar сегодня до <b>32</b>")
    else:
        set_grammar_cap_today(inviter, 48)
        set_vocab_cap_today(inviter, FREE_VOCAB_ITEMS_PER_DAY + 10)
        msgs.append("Grammar сегодня до <b>48</b> + Vocabulary <b>+10</b>")

    if plan == "chat":
        extend_chat_pass(inviter, 3)
        msgs.append("+3 дня общения")
    elif plan == "full":
        extend_premium(inviter, 3)
        inviter["referral_lottery_tickets"] = int(inviter.get("referral_lottery_tickets") or 0) + 1
        msgs.append("+3 дня полного доступа и билет в реф-розыгрыш")

    to_inviter = (
        f"🎁 Друг закрыл 3 темы Grammar! Засчитан друг №<b>{q}</b>.\n"
        + " · ".join(msgs)
    )
    to_invitee = (
        "🎉 Ты закрыл 3 темы Grammar — реферальный прогресс засчитан!\n"
        "Рико гордится тобой 🦜 · сейфы копятся за длинную серию дней."
    )
    return to_inviter, to_invitee


def maybe_qualify_referral(invitee: dict, users: dict) -> tuple[str | None, str | None]:
    """(сообщение инвайтеру, сообщение другу) или (None, None)."""
    ensure_growth(invitee)
    if invitee.get("referral_qualified_done"):
        return None, None
    if count_grammar_exercises_done(invitee) < REF_QUALIFY_EXERCISES:
        return None, None
    ref = invitee.get("referred_by")
    if not ref or str(ref) not in users:
        invitee["referral_qualified_done"] = True
        return None, (
            "🎉 Ты закрыл 3 темы Grammar — Рико гордится тобой 🦜"
        )
    inviter = users[str(ref)]
    if not isinstance(inviter, dict):
        return None, None
    to_inv, to_friend = on_invitee_qualified(inviter, invitee)
    return to_inv or None, to_friend or None
