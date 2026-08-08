"""
Кнопки офферов ежедневного повторения Grammar / Vocabulary.
"""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from handlers.filters import ModeFilter
from handlers.keyboards import main_menu
from handlers.lesson_filters import LessonHubFilter
from handlers.vocabulary_keyboards import global_drill_menu_kb
from services.database import (
    MODE_LESSONS,
    MODE_MENU,
    get_user,
    save_users,
    set_mode,
    users_for,
)
from services.daily_reviews import grammar_offer_kb, vocab_offer_kb
from services.grammar_review import (
    BTN_GRAMMAR_REVIEW_NO,
    BTN_GRAMMAR_REVIEW_YES,
    BTN_START_GRAMMAR_TOPIC,
    BTN_START_VOCAB_TOPIC,
    BTN_VOCAB_REVIEW_NO,
    BTN_VOCAB_REVIEW_YES,
    advance_review,
    check_review_answer,
    clear_review,
    current_review_item,
    ensure_grammar_review,
    format_review_prompt,
    start_review_session,
)
from services.growth import ensure_growth
from services.vocabulary_state import set_vocab_hub

log = logging.getLogger(__name__)
router = Router()


def _review_mcq_kb(options: list[str]) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=o)] for o in options]
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _review_write_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Вернуться в меню")]],
        resize_keyboard=True,
    )


async def _send_current_review(m: Message, user: dict) -> None:
    item = current_review_item(user)
    gr = ensure_grammar_review(user)
    if not item:
        ok = int(gr.get("correct") or 0)
        total = int(gr.get("total") or 0)
        clear_review(user)
        await m.answer(
            f"🦜 Красава! Повторение закончено: <b>{ok}/{total}</b>.\n"
            "Так материал лучше остаётся в голове. Увидимся на следующем круге 💚",
            parse_mode="HTML",
            reply_markup=main_menu(user),
        )
        set_mode(str(m.from_user.id), MODE_MENU)
        return
    n = int(gr.get("index") or 0) + 1
    total = int(gr.get("total") or len(gr.get("queue") or []))
    text = format_review_prompt(
        item, n=n, total=total, title=gr.get("title") or ""
    )
    if item.get("subtype") == "mcq":
        await m.answer(
            text,
            parse_mode="HTML",
            reply_markup=_review_mcq_kb(list(item.get("options") or [])),
        )
    else:
        await m.answer(text, parse_mode="HTML", reply_markup=_review_write_kb())


@router.message(F.text == BTN_START_GRAMMAR_TOPIC)
async def grammar_start_topic(m: Message):
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    set_mode(uid, MODE_LESSONS)
    save_users(users, only=uid)
    from handlers.lessons_grammar import open_grammar

    await m.answer(
        "🦜 Отлично — идём в Grammar. Выбери тему и пройди её с заданиями 💚"
    )
    await open_grammar(m)


@router.message(F.text == BTN_START_VOCAB_TOPIC)
async def vocab_start_topic(m: Message):
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    set_mode(uid, MODE_LESSONS)
    from datetime import datetime, timedelta, timezone

    from services.daily_reviews import _vocab_learned_count

    msk = timezone(timedelta(hours=3))
    user["vocab_review_last_date"] = datetime.now(msk).date().isoformat()
    user["vocab_review_learned_at_review"] = _vocab_learned_count(user)
    save_users(users, only=uid)
    from handlers.lessons_vocabulary import start_today

    await m.answer("🦜 Супер — открываю Vocabulary, пойдём учить слова 📚")
    await start_today(m)


@router.message(F.text == BTN_GRAMMAR_REVIEW_YES)
async def grammar_review_yes(m: Message):
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    offer = user.get("grammar_review_offer_topic") or {}
    level = offer.get("level")
    tid = offer.get("topic_id")
    title = offer.get("title") or tid
    if not level or not tid:
        from services.grammar_review import completed_practice_topics
        import random

        topics = completed_practice_topics(user)
        if not topics:
            await m.answer(
                "🦜 Пока нет пройденных тем Grammar с заданиями — "
                "сначала пройди хотя бы одну тему в Уроках.",
                reply_markup=main_menu(user),
            )
            return
        level, tid, title = random.choice(topics)
    start_review_session(user, level, tid, title)
    save_users(users, only=uid)
    set_mode(uid, MODE_LESSONS)
    set_vocab_hub(uid, "grammar_review")
    users = users_for(uid)
    user = get_user(users, uid)
    if not (user.get("grammar_review") or {}).get("active"):
        start_review_session(user, level, tid, title)
        save_users(users, only=uid)
    await m.answer(
        f"🦜 Отлично! Повторяем тему <b>{title}</b>.\n"
        "Пять разных заданий — я рядом, пиши спокойно ✨",
        parse_mode="HTML",
    )
    await _send_current_review(m, user)


@router.message(F.text == BTN_GRAMMAR_REVIEW_NO)
async def grammar_review_no(m: Message):
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    clear_review(user)
    save_users(users, only=uid)
    set_mode(uid, MODE_MENU)
    await m.answer(
        "🦜 Ок, без давления. Но правда: короткое повторение сильно помогает памяти. "
        "Когда будешь готов(а) — загляни в Grammar 💚",
        reply_markup=main_menu(user),
    )


@router.message(F.text == BTN_VOCAB_REVIEW_YES)
async def vocab_review_yes(m: Message):
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    from datetime import datetime, timedelta, timezone

    from services.daily_reviews import _vocab_learned_count

    msk = timezone(timedelta(hours=3))
    learned = _vocab_learned_count(user)
    if learned <= 0:
        await m.answer(
            "🦜 Пока нет изученных слов — сначала пройди тему Vocabulary.",
            reply_markup=main_menu(user),
        )
        set_mode(uid, MODE_MENU)
        save_users(users, only=uid)
        return
    user["vocab_review_last_date"] = datetime.now(msk).date().isoformat()
    user["vocab_review_learned_at_review"] = learned
    set_mode(uid, MODE_LESSONS)
    set_vocab_hub(uid, "global_drill_menu")
    save_users(users, only=uid)
    await m.answer(
        "🦜 Супер! Открываю задания по изученным словам и фразам ✨",
        reply_markup=global_drill_menu_kb(),
        parse_mode="HTML",
    )


@router.message(F.text == BTN_VOCAB_REVIEW_NO)
async def vocab_review_no(m: Message):
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    set_mode(uid, MODE_MENU)
    await m.answer(
        "🦜 Хорошо. Если передумаешь — «Уроки» → «Задания по всем уровням».",
        reply_markup=main_menu(user),
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("grammar_review"), F.text)
async def grammar_review_answer(m: Message):
    text = (m.text or "").strip()
    if text in {
        BTN_GRAMMAR_REVIEW_YES,
        BTN_GRAMMAR_REVIEW_NO,
        BTN_VOCAB_REVIEW_YES,
        BTN_VOCAB_REVIEW_NO,
        BTN_START_GRAMMAR_TOPIC,
        BTN_START_VOCAB_TOPIC,
        "🔙 Вернуться в меню",
    }:
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    gr = ensure_grammar_review(user)
    if not gr.get("active"):
        await m.answer("Сессия повторения не активна.", reply_markup=main_menu(user))
        set_mode(uid, MODE_MENU)
        return
    result = check_review_answer(user, text)
    await m.answer(
        ("✅ " if result["ok"] else "❌ ") + (result.get("feedback") or ""),
        parse_mode="HTML",
    )
    advance_review(user, correct=bool(result["ok"]))
    save_users(users, only=uid)
    await _send_current_review(m, user)
