"""
Админ-команды (только MANAGER_ID). Молча игнорируются у всех остальных.
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
    "🛠 <b>Админ LexDAN</b>\n"
    f"<i>Только id <code>{MANAGER_ID}</code></i>\n\n"
    "/admin — список пользователей + сводка общения\n"
    "/users — живые (зарегистрированы, не блокировали бота)\n"
    "/purge_blocked — проверить Telegram и удалить блоки из БД\n"
    "/user <code>id</code> — полная карточка\n"
    "/top — топ по использованию (чат/grammar/vocab/listening)\n"
    "/others — без активности в разделах\n"
    "/starts — кто нажал /start сегодня\n"
    "/paid — у кого активный тариф\n"
    "/grant_chat <code>id</code> [дней]\n"
    "/grant_full <code>id</code> [дней]\n"
    "/grant_secret <code>id</code> [week|voice|both]\n"
    "/broadcast_fix — рассылка: фикс-апдейт + картинка\n"
    "/broadcast_features — Listening / сейфы 30·70 / отмена списаний\n"
    "/revoke <code>id</code>\n"
    "/unlock_levels — открыть себе все уровни A0–C2\n"
    "/event — статус ивента + баллы по Grammar/Vocab/Listening\n"
    "/event_force on|off — форс-активация (тест)\n"
    "/event_announce [force] — рассылка «ивент начался»\n"
    "/event_finalize — подвести итоги и выдать призы\n"
    "/event_deliver [force] — рассылка призов топ-10 в личку\n"
    "/test_winners — тест эксклюзивных паков 1/2/3 места\n"
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
    from services.admin_stats import report_admin_home, chunk_html

    text = report_admin_home()
    for part in chunk_html(text):
        await m.answer(part, parse_mode="HTML")


@router.message(Command("users"))
async def admin_users_alive(m: Message):
    """Список зарегистрированных, кто не блокировал бота."""
    if not _is_admin(m):
        return
    from services.admin_stats import chunk_html
    from services.blocked_users import format_alive_list

    for part in chunk_html(format_alive_list()):
        await m.answer(part, parse_mode="HTML")


@router.message(Command("purge_blocked"))
async def admin_purge_blocked(m: Message):
    """Проверить Telegram и удалить из БД тех, кто заблокировал бота."""
    if not _is_admin(m):
        return
    from services.blocked_users import list_flagged_blocked, list_alive_registered, scan_and_purge_blocked

    flagged = len(list_flagged_blocked())
    to_check = len(list_alive_registered())
    status = await m.answer(
        f"🧹 Чищу базу…\n"
        f"Уже помечены блок: <b>{flagged}</b>\n"
        f"Проверяю в Telegram: <b>{to_check}</b> (это может занять минуту)",
        parse_mode="HTML",
    )
    result = await scan_and_purge_blocked(m.bot)
    removed = len(result["removed_flagged"]) + len(result["removed_scanned"])
    text = (
        "✅ Готово.\n\n"
        f"Удалено по старому флагу: <b>{len(result['removed_flagged'])}</b>\n"
        f"Удалено после проверки Telegram: <b>{len(result['removed_scanned'])}</b>\n"
        f"Всего удалено: <b>{removed}</b>\n"
        f"Живых зарегистрированных осталось: <b>{result['alive_left']}</b>\n\n"
        "Список: /users"
    )
    if result["removed_scanned"]:
        ids = ", ".join(f"<code>{x}</code>" for x in result["removed_scanned"][:30])
        text += f"\n\nНовые блоки: {ids}"
        if len(result["removed_scanned"]) > 30:
            text += f" …+{len(result['removed_scanned']) - 30}"
    try:
        await status.edit_text(text, parse_mode="HTML")
    except Exception:
        await m.answer(text, parse_mode="HTML")


@router.message(Command("unlock_levels"))
async def admin_unlock_levels(m: Message):
    """Открыть все CEFR-уровни только админу (себе)."""
    if not _is_admin(m):
        return
    uid = str(m.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    user["assessment_done"] = True
    user["grammar_unlock_ceiling"] = "C2"
    if not (user.get("level") or "").strip():
        user["level"] = "A1"
    save_users(users, only=uid)
    await m.answer(
        "🔓 Тебе открыты <b>все уровни A0–C2</b>.\n"
        "Входной тест помечен как пройденный.\n"
        "Тариф не менялся — только доступ к уровням.",
        parse_mode="HTML",
    )


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


@router.message(Command("top"))
async def admin_top(m: Message):
    if not _is_admin(m):
        return
    from services.admin_stats import report_top

    await _send_report(m, report_top())


@router.message(Command("others"))
async def admin_others(m: Message):
    if not _is_admin(m):
        return
    from services.admin_stats import report_others

    await _send_report(m, report_others())


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


@router.message(Command("grant_secret"))
async def admin_grant_secret(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    parts = (command.args or "").strip().split()
    if not parts:
        await m.answer("Формат: /grant_secret <user_id> [week|voice|both]")
        return
    uid = parts[0].lstrip("@")
    kind = (parts[1] if len(parts) > 1 else "both").lower()
    from services.secret_missions import unlock_mission, MISSION_WEEK, MISSION_VOICE, has_secret_entry

    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    opened = []
    if kind in {"week", "both", "all"}:
        unlock_mission(user, MISSION_WEEK)
        opened.append("Разбор недели")
    if kind in {"voice", "both", "all"}:
        unlock_mission(user, MISSION_VOICE)
        opened.append("Голос дня")
    if not opened:
        await m.answer("kind: week | voice | both")
        return
    save_users(users, only=uid)
    await m.answer(
        f"✅ Секрет → <code>{uid}</code>: {', '.join(opened)} "
        f"(inbox={has_secret_entry(user)})",
        parse_mode="HTML",
    )
    try:
        from handlers.keyboards import main_menu

        await m.bot.send_message(
            int(uid),
            "🔐 Рико открыл секретное задание! Жми <b>🔐 Секрет Рико</b> в меню.",
            reply_markup=main_menu(user),
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
    from services.admin_stats import format_user_card, chunk_html

    for part in chunk_html(format_user_card(uid, user)):
        await m.answer(part, parse_mode="HTML")
    save_users(users, only=uid)


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


@router.message(Command("event"))
async def admin_event_status(m: Message):
    if not _is_admin(m):
        return
    from services.event_magic import format_event_admin_chunks

    for chunk in format_event_admin_chunks():
        await m.answer(chunk, parse_mode="HTML")


@router.message(Command("event_force"))
async def admin_event_force(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    from services.event_magic import set_force_active, status_text

    arg = (command.args or "").strip().lower()
    if arg not in {"on", "off", "1", "0"}:
        await m.answer("Формат: /event_force on|off")
        return
    on = arg in {"on", "1"}
    set_force_active(on)
    await m.answer(
        f"{'✅ force_active включён' if on else '⏹ force_active выключен'}\n\n{status_text()}",
        parse_mode="HTML",
    )


@router.message(Command("broadcast_fix"))
async def admin_broadcast_fix(m: Message):
    if not _is_admin(m):
        return
    from services.broadcast import broadcast_fix_update, fix_update_image_path

    if not fix_update_image_path():
        await m.answer("❌ Картинка lexdan_fix_update.png не найдена на сервере.")
        return
    await m.answer("📣 Рассылаю обновление с картинкой…")
    result = await broadcast_fix_update(m.bot)
    if not result.get("ok"):
        await m.answer(f"❌ Не вышло: {result.get('error')}")
        return
    await m.answer(
        f"✅ Готово.\n"
        f"Отправлено: <b>{result.get('sent', 0)}</b>\n"
        f"Ошибок: <b>{result.get('fail', 0)}</b>\n"
        f"Помечено blocked: <b>{result.get('blocked', 0)}</b>",
        parse_mode="HTML",
    )


@router.message(Command("broadcast_features"))
async def admin_broadcast_features(m: Message):
    if not _is_admin(m):
        return
    from services.broadcast import broadcast_features_update, features_update_image_path

    if not features_update_image_path():
        await m.answer("❌ Картинка для рассылки не найдена на сервере.")
        return
    await m.answer("📣 Рассылаю новости (Listening / сейфы / подписка)…")
    result = await broadcast_features_update(m.bot)
    if not result.get("ok"):
        await m.answer(f"❌ Не вышло: {result.get('error')}")
        return
    await m.answer(
        f"✅ Готово.\n"
        f"Отправлено: <b>{result.get('sent', 0)}</b>\n"
        f"Ошибок: <b>{result.get('fail', 0)}</b>\n"
        f"Помечено blocked: <b>{result.get('blocked', 0)}</b>",
        parse_mode="HTML",
    )


@router.message(Command("event_announce"))
async def admin_event_announce(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    from services.event_magic import broadcast_event_start

    force = (command.args or "").strip().lower() in {"force", "1", "redo"}
    await m.answer("📣 Рассылаю анонс ивента…")
    result = await broadcast_event_start(m.bot, force=force)
    if result.get("already"):
        await m.answer(
            "Анонс уже был отправлен. Повторить: /event_announce force"
        )
        return
    await m.answer(
        f"✅ Готово.\nОтправлено: {result.get('sent', 0)}\n"
        f"Ошибок: {result.get('fail', 0)}"
    )


@router.message(Command("event_finalize"))
async def admin_event_finalize(m: Message, command: CommandObject):
    if not _is_admin(m):
        return
    from services.event_magic import finalize_event, format_points
    from services.event_prize_delivery import deliver_all_prizes

    force = (command.args or "").strip().lower() in {"force", "redo", "1"}
    result = finalize_event(force=force)
    if result.get("already"):
        await m.answer(
            "Итоги уже были подведены. Чтобы пересчитать: /event_finalize force\n"
            "Рассылка призов: /event_deliver [force]"
        )
        return
    top = result.get("top") or []
    lines = ["✅ Итоги ивента зафиксированы.\n", "Топ:"]
    if not top:
        lines.append("пусто (никто не набрал баллов)")
    for r in top:
        un = (r.get("username") or "").strip()
        who = f"@{un}" if un else (r.get("name") or r.get("user_id"))
        lines.append(
            f"{r.get('place')}. {who} — {format_points(float(r.get('points') or 0))}"
        )
    await m.answer("\n".join(lines))
    delivery = await deliver_all_prizes(m.bot, top)
    await m.answer(
        f"📬 Рассылка призов: отправлено {delivery.get('sent', 0)}, "
        f"ошибок {delivery.get('fail', 0)}"
    )


@router.message(Command("event_deliver"))
async def admin_event_deliver(m: Message, command: CommandObject):
    """Повторно разослать призы топ-10 (после финала)."""
    if not _is_admin(m):
        return
    from services.event_magic import load_event_state, save_event_state
    from services.event_prize_delivery import deliver_all_prizes

    force = (command.args or "").strip().lower() in {"force", "redo", "1"}
    st = load_event_state()
    if not st.get("finalized"):
        await m.answer("Сначала подведи итоги: /event_finalize")
        return
    if force:
        st["force_deliver"] = True
        st["prizes_delivered"] = False
        save_event_state(st)
    delivery = await deliver_all_prizes(m.bot)
    if delivery.get("already"):
        await m.answer("Рассылка уже была. Повторить: /event_deliver force")
        return
    await m.answer(
        f"📬 Готово. Отправлено: {delivery.get('sent', 0)}, ошибок: {delivery.get('fail', 0)}"
    )
