"""Кнопки уведомлений (inline)."""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.keyboards import main_menu, profile_menu
from services.database import (
    MODE_DAILY_FIRE,
    MODE_LESSONS,
    MODE_MENU,
    MODE_PROFILE,
    get_user,
    load_users,
    save_users,
    set_mode,
)
from services.growth import ensure_growth
from services.notify_copy import EXCLUSIVE_PACKS
from services.notify_state import ensure_notify

log = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "ntf:menu")
async def ntf_menu(c: CallbackQuery):
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    set_mode(uid, MODE_MENU)
    save_users(users, only=uid)
    await c.answer()
    from services.tg_out import section_banner

    await section_banner(c.message, "🏠")
    await c.message.answer(
        "🏠 Главное меню. Выбери кнопку ниже.",
        reply_markup=main_menu(user, user_id=uid),
    )


@router.callback_query(F.data == "ntf:fire")
async def ntf_fire(c: CallbackQuery):
    from handlers.daily_fire import daily_fire_kb
    from services.daily_fire import ensure_daily_fire, hub_intro
    from services.growth import note_lesson_activity

    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    set_mode(uid, MODE_DAILY_FIRE)
    ensure_daily_fire(user)
    note_lesson_activity(user)
    save_users(users, only=uid)
    await c.answer()
    from services.tg_out import section_banner

    await section_banner(c.message, "🔥")
    await c.message.answer(
        hub_intro(user),
        parse_mode="HTML",
        reply_markup=daily_fire_kb(user),
    )


@router.callback_query(F.data == "ntf:tariff")
async def ntf_tariff(c: CallbackQuery):
    from handlers.lesson_keyboards import tariffs_inline_kb
    from services.growth import subscription_blurb

    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    save_users(users, only=uid)
    await c.answer()
    await c.message.answer(
        subscription_blurb(user) + "\n\nВыбери тариф:",
        reply_markup=tariffs_inline_kb(user),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "ntf:profile")
async def ntf_profile(c: CallbackQuery):
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    set_mode(uid, MODE_PROFILE)
    save_users(users, only=uid)
    await c.answer()
    from services.tg_out import section_banner

    await section_banner(c.message, "📊")
    await c.message.answer(
        "📊 Профиль",
        reply_markup=profile_menu(user, user_id=uid),
    )


@router.callback_query(F.data == "ntf:week")
async def ntf_week(c: CallbackQuery):
    from services.notify_week import format_top10_html

    await c.answer()
    await c.message.answer(format_top10_html(), parse_mode="HTML")


@router.callback_query(F.data == "ntf:excl")
async def ntf_excl(c: CallbackQuery):
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    ntf = ensure_notify(user)
    pid = str(ntf.get("pending_excl") or "")
    pack = next((p for p in EXCLUSIVE_PACKS if p.get("id") == pid), None)
    if not pack:
        pack = EXCLUSIVE_PACKS[0] if EXCLUSIVE_PACKS else None
    await c.answer()
    if not pack:
        await c.message.answer("Пока пусто — загляни позже 💚")
        return
    await c.message.answer(pack.get("body") or pack.get("title") or "Бонус", parse_mode="HTML")
    voice = (pack.get("voice") or "").strip()
    if voice:
        from services.elevenlabs import send_rico_voice

        await send_rico_voice(c.message, voice, user=user, title="Exclusive")
    save_users(users, only=uid)


@router.callback_query(F.data == "ntf:cont")
async def ntf_cont(c: CallbackQuery):
    """Умный next step: незакрытая тема Grammar → иначе Огонь дня."""
    from data.grammar_curriculum import get_topic, get_topics, is_ack_topic
    from handlers.lesson_keyboards import topic_chat_kb
    from services.lesson_state import ensure_progress, open_topic, progress_key, set_grammar_list

    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    ensure_progress(user)
    await c.answer()

    level = (user.get("level") or "A1").strip() or "A1"
    done = set(user["grammar_progress"].get("completed_topics") or [])
    chosen = None
    for t in get_topics(level) or []:
        tid = t.get("id") or ""
        if not tid or progress_key(level, tid) in done:
            continue
        chosen = t
        break

    if chosen:
        tid = chosen.get("id")
        title = chosen.get("title") or tid
        set_mode(uid, MODE_LESSONS)
        set_grammar_list(uid, level)
        open_topic(uid, tid, title)
        users = load_users()
        user = get_user(users, uid)
        topic = get_topic(level, tid) or chosen
        intro = (topic.get("rico_intro") or f"Тема: {title}").strip()
        await c.message.answer(
            intro,
            parse_mode="HTML",
            reply_markup=topic_chat_kb(ack=is_ack_topic(topic)),
        )
        save_users(users, only=uid)
        return

    # fallback — огонь дня
    await ntf_fire(c)


@router.callback_query(F.data == "ntf:plan")
async def ntf_plan(c: CallbackQuery):
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    ntf = ensure_notify(user)
    payload = ntf.get("pending_plan") if isinstance(ntf.get("pending_plan"), dict) else {}
    action = str(payload.get("action") or "fire")
    await c.answer()
    if action == "grammar":
        from data.grammar_curriculum import get_topic, is_ack_topic
        from handlers.lesson_keyboards import topic_chat_kb
        from services.lesson_state import open_topic, set_grammar_list

        level = str(payload.get("level") or user.get("level") or "A1")
        tid = str(payload.get("topic_id") or "")
        title = str(payload.get("title") or tid)
        if tid:
            set_mode(uid, MODE_LESSONS)
            set_grammar_list(uid, level)
            open_topic(uid, tid, title)
            users = load_users()
            user = get_user(users, uid)
            topic = get_topic(level, tid) or {"title": title, "rico_intro": title}
            await c.message.answer(
                (topic.get("rico_intro") or title),
                parse_mode="HTML",
                reply_markup=topic_chat_kb(ack=is_ack_topic(topic)),
            )
            save_users(users, only=uid)
            return
    await ntf_fire(c)


@router.callback_query(F.data.startswith("ntf:review:"))
async def ntf_review(c: CallbackQuery):
    """Запуск grammar review по теме из уведомления."""
    from handlers.daily_reviews import _send_current_review
    from services.grammar_review import start_review_session
    from services.database import MODE_LESSONS, set_mode
    from services.lesson_state import set_grammar_list, update_lesson

    parts = (c.data or "").split(":")
    # ntf:review:LEVEL:TOPIC_ID
    if len(parts) < 4:
        await c.answer("Тема не найдена", show_alert=True)
        return
    level, tid = parts[2], parts[3]
    uid = str(c.from_user.id)
    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    from data.grammar_curriculum import get_topic

    topic = get_topic(level, tid)
    title = (topic or {}).get("title") or tid
    ok = start_review_session(user, level=level, topic_id=tid, title=title)
    if not ok or not int(ok.get("total") or 0):
        await c.answer("Пока нет заданий для этой темы", show_alert=True)
        return
    set_mode(uid, MODE_LESSONS)
    set_grammar_list(uid, level)

    def mut(u):
        from services.lesson_state import ensure_lesson

        ensure_lesson(u)
        u["lesson"]["hub"] = "grammar_review"

    update_lesson(uid, mut)
    users = load_users()
    user = get_user(users, uid)
    save_users(users, only=uid)
    await c.answer()
    await _send_current_review(c.message, user)
