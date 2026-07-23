"""
Админ-команды (только MANAGER_ID).

/admin — справка
/grant_chat <id> [дней=30]
/grant_full <id> [дней=30]
/revoke <id>
/user <id>
/paid
/set_discount <id> <процент>
/clear_discount <id>
/lottery30 | /lottery30_draw
/lottery100 | /lottery100_draw
/lottery_ref | /lottery_ref_draw
"""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import MANAGER_ID, SUPPORT_USERNAME
from services.database import load_users, get_user, save_users
from services.growth import (
    ensure_growth,
    extend_premium,
    is_premium,
    premium_days_left,
)
from services.pricing import (
    LOTTERY_100_PRIZE,
    LOTTERY_30_PRIZE,
    LOTTERY_REF_PRIZE,
    chat_price,
    clear_discount,
    clear_lottery_100_prize,
    consume_discount,
    discount_percent,
    draw_lottery_100,
    draw_lottery_30,
    draw_referral_lottery,
    full_price,
    list_lottery_100,
    list_lottery_30,
    list_referral_ticket_pool,
    lottery_status_lines,
    pending_lottery_100_prizes,
    set_discount,
)
from services.rewards import extend_chat_pass, user_plan

router = Router()

HELP = (
    "🛠 <b>Админ LexDAN</b>\n\n"
    "<b>Воронка / реклама</b>\n"
    "/funnel — сводка\n"
    "/starts — кто нажал Start (id)\n"
    "/chat_stats — текст/голос в «Общаться» + лимит\n"
    "/assessed — кто прошёл входной тест\n"
    "/limits — кто упёрся в лимиты сегодня\n"
    "/progress — задания Grammar и слова Vocabulary\n\n"
    "<b>Тарифы</b>\n"
    "/grant_chat <code>id</code> [дней] — общение\n"
    "/grant_full <code>id</code> [дней] — полный доступ\n"
    "  (если у юзера скидка — спишется автоматически)\n"
    "/revoke <code>id</code> — снять chat + full\n"
    "/user <code>id</code> — карточка\n"
    "/paid — кто с активным тарифом\n\n"
    "<b>Скидки</b>\n"
    "/set_discount <code>id</code> <code>%</code>\n"
    "/clear_discount <code>id</code>\n\n"
    "<b>Розыгрыши</b>\n"
    "/lottery30 — участники (серия 30 на 799)\n"
    "/lottery30_draw — выбрать победителя (+180 дн. full)\n"
    "/lottery100 — участники (серия 100)\n"
    "/lottery100_draw — победитель (приз деньгами вручную)\n"
    "/lottery_ref — пул реф-билетов\n"
    "/lottery_ref_draw — победитель (+30 дн. full)\n"
    "/prize_pending — кому ещё не выплатили 15 000₽\n"
    "/prize_paid <code>id</code> — отметить выплату\n"
)


def _is_admin(m: Message) -> bool:
    return bool(m.from_user and m.from_user.id == MANAGER_ID)


def _parse_uid_days(args: str | None, default_days: int = 30) -> tuple[str | None, int]:
    parts = (args or "").strip().split()
    if not parts:
        return None, default_days
    uid = parts[0].lstrip("@")
    days = default_days
    if len(parts) >= 2:
        try:
            days = max(1, int(parts[1]))
        except ValueError:
            days = default_days
    return uid, days


@router.message(Command("admin"))
async def admin_help(m: Message):
    if not _is_admin(m):
        return
    await m.answer(HELP, parse_mode="HTML")


async def _send_report(m: Message, text: str) -> None:
    from services.admin_stats import chunk_html

    for part in chunk_html(text):
        await m.answer(part, parse_mode="HTML")


@router.message(Command("funnel"))
async def admin_funnel(m: Message):
    if not _is_admin(m):
        return
    from services.admin_stats import report_funnel

    await _send_report(m, report_funnel())


@router.message(Command("starts"))
async def admin_starts(m: Message):
    if not _is_admin(m):
        return
    from services.admin_stats import report_starts

    await _send_report(m, report_starts())


@router.message(Command("chat_stats"))
async def admin_chat_stats(m: Message):
    if not _is_admin(m):
        return
    from services.admin_stats import report_chat_stats

    await _send_report(m, report_chat_stats())


@router.message(Command("assessed"))
async def admin_assessed(m: Message):
    if not _is_admin(m):
        return
    from services.admin_stats import report_assessed

    await _send_report(m, report_assessed())


@router.message(Command("limits"))
async def admin_limits(m: Message):
    if not _is_admin(m):
        return
    from services.admin_stats import report_limits

    await _send_report(m, report_limits())


@router.message(Command("progress"))
async def admin_progress(m: Message):
    if not _is_admin(m):
        return
    from services.admin_stats import report_progress

    await _send_report(m, report_progress())


@router.message(Command("grant_chat"))
async def admin_grant_chat(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    uid, days = _parse_uid_days(command.args)
    if not uid:
        await m.answer("Формат: /grant_chat <user_id> [дней]")
        return
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    pct = consume_discount(user)
    extend_chat_pass(user, days)
    save_users(users, only=uid)
    disc = f" (скидка {pct}% списана)" if pct else ""
    await m.answer(f"✅ Chat на {days} дн. → <code>{uid}</code>{disc}", parse_mode="HTML")
    try:
        await m.bot.send_message(
            int(uid),
            f"🦜 Рико: тебе активировали безлимит «Общение» на <b>{days}</b> дн. Приятного общения!",
            parse_mode="HTML",
        )
    except Exception:
        pass


@router.message(Command("grant_full"))
async def admin_grant_full(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    uid, days = _parse_uid_days(command.args)
    if not uid:
        await m.answer("Формат: /grant_full <user_id> [дней]")
        return
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    pct = consume_discount(user)
    extend_premium(user, days)
    save_users(users, only=uid)
    disc = f" (скидка {pct}% списана)" if pct else ""
    await m.answer(f"✅ Full на {days} дн. → <code>{uid}</code>{disc}", parse_mode="HTML")
    try:
        await m.bot.send_message(
            int(uid),
            f"🦜 Рико: полный доступ на <b>{days}</b> дн. активирован! Уроки и чат без лимитов 🚀",
            parse_mode="HTML",
        )
    except Exception:
        pass


@router.message(Command("revoke"))
async def admin_revoke(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    uid = (command.args or "").strip().split()
    if not uid:
        await m.answer("Формат: /revoke <user_id>")
        return
    uid = uid[0]
    users = load_users()
    user = get_user(users, uid)
    user["premium_until"] = 0
    user["chat_until"] = 0
    user["lessons_until"] = 0
    user["dev_unlock"] = False
    save_users(users, only=uid)
    await m.answer(f"⛔ Доступ снят у <code>{uid}</code>", parse_mode="HTML")


@router.message(Command("user"))
async def admin_user(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    uid = (command.args or "").strip().split()
    if not uid:
        await m.answer("Формат: /user <user_id>")
        return
    uid = uid[0]
    users = load_users()
    if uid not in users:
        await m.answer("Пользователь не найден в базе.")
        return
    user = get_user(users, uid)
    ensure_growth(user)
    plan = user_plan(user)
    chat_p, chat_d = chat_price(user)
    full_p, full_d = full_price(user)
    lot = lottery_status_lines(user)
    from services.admin_stats import user_card_extra

    await m.answer(
        f"👤 <code>{uid}</code> · {user.get('name') or '—'}\n"
        f"Тариф: <b>{plan}</b>\n"
        f"Level: {user.get('level') or '—'} · streak: {int(user.get('streak') or 0)}\n"
        f"premium_until days≈ {premium_days_left(user) if is_premium(user) else 0}\n"
        f"chat_until: {user.get('chat_until') or 0}\n"
        f"Скидка: {discount_percent(user)}%"
        f" → chat {chat_p}₽ / full {full_p}₽\n"
        f"Реф. засчитано: {int(user.get('referral_qualified') or 0)}\n"
        f"{lot}\n"
        f"{user_card_extra(user)}",
        parse_mode="HTML",
    )


@router.message(Command("paid"))
async def admin_paid(m: Message):
    if not _is_admin(m):
        return
    users = load_users()
    lines = ["💳 <b>Активные тарифы</b>\n"]
    n = 0
    for uid, raw in users.items():
        if not isinstance(raw, dict):
            continue
        user = get_user(users, str(uid))
        plan = user_plan(user)
        if plan == "free":
            continue
        n += 1
        extra = ""
        if plan == "full":
            extra = f" (~{premium_days_left(user)} дн.)"
        lines.append(
            f"• <code>{uid}</code> {user.get('name') or ''} — <b>{plan}</b>{extra}"
        )
    if n == 0:
        lines.append("Пока никого.")
    await m.answer("\n".join(lines[:80]), parse_mode="HTML")


@router.message(Command("set_discount"))
async def admin_set_discount(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    parts = (command.args or "").strip().split()
    if len(parts) < 2:
        await m.answer("Формат: /set_discount <user_id> <процент>")
        return
    uid, pct_s = parts[0], parts[1]
    try:
        pct = int(pct_s)
    except ValueError:
        await m.answer("Процент — число, например 50")
        return
    users = load_users()
    user = get_user(users, uid)
    set_discount(user, pct, note="admin")
    save_users(users, only=uid)
    chat_p, _ = chat_price(user)
    full_p, _ = full_price(user)
    await m.answer(
        f"🏷 Скидка {pct}% для <code>{uid}</code>\n"
        f"Цены: chat {chat_p}₽ · full {full_p}₽",
        parse_mode="HTML",
    )


@router.message(Command("clear_discount"))
async def admin_clear_discount(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    uid = (command.args or "").strip().split()
    if not uid:
        await m.answer("Формат: /clear_discount <user_id>")
        return
    uid = uid[0]
    users = load_users()
    user = get_user(users, uid)
    clear_discount(user)
    save_users(users, only=uid)
    await m.answer(f"Скидка снята у <code>{uid}</code>", parse_mode="HTML")


def _fmt_entrants(rows: list[tuple[str, dict]], title: str) -> str:
    if not rows:
        return f"{title}\nПока никого."
    lines = [title, f"Участников: <b>{len(rows)}</b>\n"]
    for uid, u in rows[:60]:
        lines.append(f"• <code>{uid}</code> {u.get('name') or ''} · streak {int(u.get('streak') or 0)}")
    if len(rows) > 60:
        lines.append(f"… и ещё {len(rows) - 60}")
    return "\n".join(lines)


@router.message(Command("lottery30"))
async def admin_lottery30(m: Message):
    if not _is_admin(m):
        return
    users = load_users()
    rows = list_lottery_30(users)
    await m.answer(
        _fmt_entrants(rows, f"🎟 <b>Розыгрыш 30 дней</b>\nПриз: {LOTTERY_30_PRIZE}"),
        parse_mode="HTML",
    )


@router.message(Command("lottery30_draw"))
async def admin_lottery30_draw(m: Message):
    if not _is_admin(m):
        return
    users = load_users()
    won = draw_lottery_30(users)
    if not won:
        await m.answer("Некого разыгрывать — список пуст.")
        return
    uid, user = won
    save_users(users, only=uid)
    await m.answer(
        f"🏆 Победитель lottery30: <code>{uid}</code> {user.get('name') or ''}\n"
        f"Приз: {LOTTERY_30_PRIZE} (+180 дн. full)",
        parse_mode="HTML",
    )
    try:
        await m.bot.send_message(
            int(uid),
            f"🏆 Поздравляем! Ты выиграл розыгрыш за серию 30 дней: "
            f"<b>{LOTTERY_30_PRIZE}</b>. Доступ уже начислен 🦜",
            parse_mode="HTML",
        )
    except Exception:
        pass


@router.message(Command("lottery100"))
async def admin_lottery100(m: Message):
    if not _is_admin(m):
        return
    users = load_users()
    rows = list_lottery_100(users)
    await m.answer(
        _fmt_entrants(rows, f"🎟 <b>Розыгрыш 100 дней</b>\nПриз: {LOTTERY_100_PRIZE}"),
        parse_mode="HTML",
    )


@router.message(Command("lottery100_draw"))
async def admin_lottery100_draw(m: Message):
    if not _is_admin(m):
        return
    users = load_users()
    won = draw_lottery_100(users)
    if not won:
        await m.answer("Некого разыгрывать — список пуст.")
        return
    uid, user = won
    save_users(users, only=uid)
    contact = f"@{SUPPORT_USERNAME}" if SUPPORT_USERNAME else "поддержку"
    await m.answer(
        f"🏆 Победитель lottery100: <code>{uid}</code> {user.get('name') or ''}\n"
        f"Приз: {LOTTERY_100_PRIZE} — выплати вручную / отметь.\n"
        f"Флаг lottery_100_prize_pending=True",
        parse_mode="HTML",
    )
    try:
        await m.bot.send_message(
            int(uid),
            f"🏆 Поздравляем! Ты выиграл розыгрыш за серию 100 дней: "
            f"<b>{LOTTERY_100_PRIZE}</b>.\n"
            f"Напиши {contact} — оформим приз 🦜",
            parse_mode="HTML",
        )
    except Exception:
        pass


@router.message(Command("lottery_ref"))
async def admin_lottery_ref(m: Message):
    if not _is_admin(m):
        return
    users = load_users()
    pool = list_referral_ticket_pool(users)
    # уникальные с числом билетов
    counts: dict[str, int] = {}
    names: dict[str, str] = {}
    for uid, u in pool:
        counts[uid] = counts.get(uid, 0) + 1
        names[uid] = u.get("name") or ""
    if not counts:
        await m.answer("Реф-билетов пока нет.")
        return
    lines = [
        f"🎟 <b>Реф-розыгрыш</b>\nПриз: {LOTTERY_REF_PRIZE}\n"
        f"Билетов в урне: <b>{len(pool)}</b>\n"
    ]
    for uid, n in sorted(counts.items(), key=lambda x: -x[1])[:60]:
        lines.append(f"• <code>{uid}</code> {names[uid]} — {n} билет(ов)")
    await m.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command("lottery_ref_draw"))
async def admin_lottery_ref_draw(m: Message):
    if not _is_admin(m):
        return
    users = load_users()
    won = draw_referral_lottery(users)
    if not won:
        await m.answer("Некого разыгрывать — билетов нет.")
        return
    uid, user = won
    save_users(users, only=uid)
    await m.answer(
        f"🏆 Победитель реф-розыгрыша: <code>{uid}</code> {user.get('name') or ''}\n"
        f"Приз: {LOTTERY_REF_PRIZE} (+30 дн. full). Билетов осталось: "
        f"{int(user.get('referral_lottery_tickets') or 0)}",
        parse_mode="HTML",
    )
    try:
        await m.bot.send_message(
            int(uid),
            f"🏆 Поздравляем! Реф-розыгрыш: тебе начислен "
            f"<b>{LOTTERY_REF_PRIZE}</b> 🦜",
            parse_mode="HTML",
        )
    except Exception:
        pass


@router.message(Command("prize_pending"))
async def admin_prize_pending(m: Message):
    if not _is_admin(m):
        return
    users = load_users()
    rows = pending_lottery_100_prizes(users)
    if not rows:
        await m.answer("Нет ожидающих выплат 15 000₽.")
        return
    lines = ["💰 <b>Ждут выплату (lottery 100)</b>\n"]
    for uid, u in rows:
        lines.append(f"• <code>{uid}</code> {u.get('name') or ''} · won {u.get('lottery_100_won_at') or '—'}")
    lines.append("\nПосле перевода: /prize_paid <id>")
    await m.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command("prize_paid"))
async def admin_prize_paid(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    uid = (command.args or "").strip().split()
    if not uid:
        await m.answer("Формат: /prize_paid <user_id>")
        return
    uid = uid[0]
    users = load_users()
    user = get_user(users, uid)
    if not clear_lottery_100_prize(user):
        await m.answer("У этого юзера нет pending-приза (или уже отмечен).")
        return
    save_users(users, only=uid)
    await m.answer(f"✅ Приз отмечен выплаченным для <code>{uid}</code>", parse_mode="HTML")
    try:
        await m.bot.send_message(
            int(uid),
            "💰 Рико: приз за серию 100 дней отмечен как выплаченный. Поздравляем ещё раз! 🦜",
        )
    except Exception:
        pass
