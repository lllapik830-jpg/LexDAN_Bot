"""
Ежедневные офферы повторения: Grammar 12:00 МСК, Vocabulary 16:00 МСК.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from services.database import load_users, save_users, get_user
from services.growth import ensure_growth
from services.grammar_review import (
    BTN_GRAMMAR_REVIEW_NO,
    BTN_GRAMMAR_REVIEW_YES,
    BTN_VOCAB_REVIEW_NO,
    BTN_VOCAB_REVIEW_YES,
    completed_practice_topics,
)

MSK = timezone(timedelta(hours=3))
log = logging.getLogger(__name__)


def _now_msk() -> datetime:
    return datetime.now(MSK)


def _today() -> str:
    return _now_msk().date().isoformat()


def grammar_offer_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_GRAMMAR_REVIEW_YES)],
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


def _eligible_user(user: dict) -> bool:
    ensure_growth(user)
    if user.get("tg_blocked"):
        return False
    if not user.get("name") or user.get("step") != "ready":
        return False
    return True


async def send_grammar_review_offers(bot, *, force_hour: bool = True) -> dict:
    """В 12:00–12:59 МСК — оффер закрепить grammar."""
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
        if not topics:
            # всё равно отметим день? нет — пусть получит, когда появятся темы
            continue
        import random

        level, tid, title = random.choice(topics)
        name = user.get("name") or "друг"
        text = (
            f"🦜 <b>Эй, {name}!</b>\n\n"
            f"Давай закрепим материал? Вчера/недавно ты проходил(а) тему "
            f"<b>{title}</b> — для памяти лучше повторить пройденное, "
            f"чем бежать только вперёд 💚\n\n"
            "Я рядом как репетитор: коротко, по делу и без стресса. "
            "Жми «Повторить материал» — дам 5 свежих заданий по этой теме "
            "(не те же, что в уроке)."
        )
        # сохраним выбранную тему на сегодня
        user["grammar_review_offer_date"] = today
        user["grammar_review_offer_topic"] = {
            "level": level,
            "topic_id": tid,
            "title": title,
        }
        try:
            await bot.send_message(
                int(uid),
                text,
                parse_mode="HTML",
                reply_markup=grammar_offer_kb(),
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
    """В 16:00–16:59 МСК — оффер повторить слова/фразы (всем ready)."""
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
        text = (
            f"🦜 <b>{name}, время освежить слова!</b>\n\n"
            "Заглянем в изученные слова и фразы? Короткая сессия повторения "
            "очень помогает памяти — я рядом, без давления 😊\n\n"
            "Жми «Повторить» — открою раздел заданий по всем уровням."
        )
        user["vocab_review_offer_date"] = today
        try:
            await bot.send_message(
                int(uid),
                text,
                parse_mode="HTML",
                reply_markup=vocab_offer_kb(),
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
