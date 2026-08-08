# -*- coding: utf-8 -*-
"""
Ежедневные офферы заданий (только полный тариф 799):
Grammar 12:00 МСК, Vocabulary 16:00 МСК.
Пустой прогресс / уже повторил без новых тем → предложить пройти тему, не «огонь».
"""

from __future__ import annotations

import logging
import random
from datetime import datetime, timedelta, timezone

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from services.database import load_users, save_users, get_user
from services.growth import ensure_growth
from services.grammar_review import (
    BTN_GRAMMAR_REVIEW_NO,
    BTN_GRAMMAR_REVIEW_YES,
    BTN_START_GRAMMAR_TOPIC,
    BTN_VOCAB_REVIEW_NO,
    BTN_VOCAB_REVIEW_YES,
    BTN_START_VOCAB_TOPIC,
    completed_practice_topics,
)

MSK = timezone(timedelta(hours=3))
log = logging.getLogger(__name__)


def _now_msk() -> datetime:
    return datetime.now(MSK)


def _today() -> str:
    return _now_msk().date().isoformat()


def _yesterday() -> str:
    return (_now_msk().date() - timedelta(days=1)).isoformat()


def grammar_offer_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_GRAMMAR_REVIEW_YES)],
            [KeyboardButton(text=BTN_GRAMMAR_REVIEW_NO)],
        ],
        resize_keyboard=True,
    )


def grammar_start_topic_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_START_GRAMMAR_TOPIC)],
            [KeyboardButton(text=BTN_GRAMMAR_REVIEW_NO)],
        ],
        resize_keyboard=True,
    )


def vocab_offer_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_VOCAB_REVIEW_YES)],
            [KeyboardButton(text=BTN_VOCAB_REVIEW_NO)],
        ],
        resize_keyboard=True,
    )


def vocab_start_topic_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_START_VOCAB_TOPIC)],
            [KeyboardButton(text=BTN_VOCAB_REVIEW_NO)],
        ],
        resize_keyboard=True,
    )


def _eligible_user(user: dict) -> bool:
    """Напоминания о заданиях / повторении — только полный доступ (799)."""
    from services.rewards import user_plan

    ensure_growth(user)
    if user.get("tg_blocked"):
        return False
    if not user.get("name") or user.get("step") != "ready":
        return False
    if user_plan(user) != "full":
        return False
    return True


def _vocab_learned_count(user: dict) -> int:
    try:
        from services.vocabulary_state import (
            get_all_learned_phrase_entries,
            get_all_learned_word_entries,
        )

        return len(get_all_learned_word_entries(user)) + len(
            get_all_learned_phrase_entries(user)
        )
    except Exception:
        return int(user.get("words_learned") or 0)


def _grammar_needs_new_topic(user: dict, topics: list) -> bool:
    """Уже повторял, новых пройденных тем нет → лучше предложить пройти тему."""
    if not topics:
        return True
    last_id = user.get("grammar_review_last_topic_id")
    last_date = user.get("grammar_review_last_date") or ""
    snap = int(user.get("grammar_review_topics_count_at_review") or 0)
    # повторил вчера/сегодня и число пройденных тем не выросло
    if last_id and last_date in {_today(), _yesterday()} and len(topics) <= max(1, snap):
        # единственная тема = та, что уже повторяли
        if len(topics) == 1 and topics[0][1] == last_id:
            return True
        if len(topics) <= snap:
            return True
    return False


def _vocab_needs_new_learning(user: dict, learned: int) -> bool:
    if learned <= 0:
        return True
    last_date = user.get("vocab_review_last_date") or ""
    snap = int(user.get("vocab_review_learned_at_review") or 0)
    if last_date in {_today(), _yesterday()} and learned <= max(0, snap):
        return True
    return False


async def send_grammar_review_offers(bot, *, force_hour: bool = True) -> dict:
    """В 12:00–12:59 МСК — повторение grammar ИЛИ старт темы."""
    now = _now_msk()
    if force_hour and now.hour != 12:
        return {"sent": 0, "skipped_hour": True}
    today = _today()
    users = load_users()
    sent = 0
    dirty_ids: list[str] = []
    for uid, raw in list(users.items()):
        if not isinstance(raw, dict):
            continue
        user = get_user(users, str(uid))
        if not _eligible_user(user):
            continue
        if user.get("grammar_review_offer_date") == today:
            continue
        topics = completed_practice_topics(user)
        name = user.get("name") or "друг"

        if not topics or _grammar_needs_new_topic(user, topics):
            text = (
                f"🦜 <b>Эй, {name}!</b>\n\n"
                "Пока рано долбить повторение — сначала нужна пройденная тема "
                "с заданиями.\n\n"
                "📚 Давай откроем <b>Grammar</b> и пройдём тему? "
                "Это база, без неё повторять нечего 💚"
            )
            user["grammar_review_offer_date"] = today
            user["grammar_review_offer_kind"] = "start_topic"
            user.pop("grammar_review_offer_topic", None)
            kb = grammar_start_topic_kb()
        else:
            last_id = user.get("grammar_review_last_topic_id")
            pool = [t for t in topics if t[1] != last_id] or topics
            level, tid, title = random.choice(pool)
            text = (
                f"🦜 <b>Эй, {name}!</b>\n\n"
                f"Давай закрепим материал по теме <b>{title}</b>?\n"
                "Короткое повторение (5 заданий) лучше держит тему в памяти, "
                "чем бежать только вперёд 💚\n\n"
                "Жми «Повторить материал» — без стресса, я рядом."
            )
            user["grammar_review_offer_date"] = today
            user["grammar_review_offer_kind"] = "review"
            user["grammar_review_offer_topic"] = {
                "level": level,
                "topic_id": tid,
                "title": title,
            }
            kb = grammar_offer_kb()

        try:
            await bot.send_message(
                int(uid),
                text,
                parse_mode="HTML",
                reply_markup=kb,
            )
            user.pop("tg_blocked", None)
            sent += 1
            dirty_ids.append(str(uid))
        except Exception as e:
            err = str(e).lower()
            log.warning("grammar review offer fail %s: %s", uid, e)
            if "blocked" in err or "deactivated" in err or "forbidden" in err:
                user["tg_blocked"] = True
                dirty_ids.append(str(uid))
    if dirty_ids:
        save_users(users, only=dirty_ids)
    return {"sent": sent}


async def send_vocab_review_offers(bot, *, force_hour: bool = True) -> dict:
    """В 16:00–16:59 МСК — повтор слов ИЛИ старт изучения."""
    now = _now_msk()
    if force_hour and now.hour != 16:
        return {"sent": 0, "skipped_hour": True}
    today = _today()
    users = load_users()
    sent = 0
    dirty_ids: list[str] = []
    for uid, raw in list(users.items()):
        if not isinstance(raw, dict):
            continue
        user = get_user(users, str(uid))
        if not _eligible_user(user):
            continue
        if user.get("vocab_review_offer_date") == today:
            continue
        name = user.get("name") or "друг"
        learned = _vocab_learned_count(user)

        if _vocab_needs_new_learning(user, learned):
            text = (
                f"🦜 <b>{name}, давай к словам!</b>\n\n"
                "Пока нечего освежать в памяти — сначала нужно выучить "
                "хотя бы несколько слов или фраз.\n\n"
                "📚 Откроем Vocabulary и пройдём тему? "
                "Потом повторение будет иметь смысл 😊"
            )
            user["vocab_review_offer_kind"] = "start_topic"
            kb = vocab_start_topic_kb()
        else:
            text = (
                f"🦜 <b>{name}, время освежить слова!</b>\n\n"
                "Короткая сессия по уже изученным словам и фразам "
                "очень помогает памяти — без давления 😊\n\n"
                "Жми «Повторить» — открою задания по изученному."
            )
            user["vocab_review_offer_kind"] = "review"
            kb = vocab_offer_kb()

        user["vocab_review_offer_date"] = today
        try:
            await bot.send_message(
                int(uid),
                text,
                parse_mode="HTML",
                reply_markup=kb,
            )
            user.pop("tg_blocked", None)
            sent += 1
            dirty_ids.append(str(uid))
        except Exception as e:
            err = str(e).lower()
            log.warning("vocab review offer fail %s: %s", uid, e)
            if "blocked" in err or "deactivated" in err or "forbidden" in err:
                user["tg_blocked"] = True
                dirty_ids.append(str(uid))
    if dirty_ids:
        save_users(users, only=dirty_ids)
    return {"sent": sent}
