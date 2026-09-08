"""
УСТАРЕЛО: авто-рассылки заменены на services/notify_engine.py.
Файл оставлен пустым-совместимым, чтобы старые импорты не падали.
Кнопки/клавиатуры review живут в handlers/daily_reviews.py + services/grammar_review.py.
"""

from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from services.grammar_review import (
    BTN_GRAMMAR_REVIEW_NO,
    BTN_GRAMMAR_REVIEW_YES,
    BTN_START_GRAMMAR_TOPIC,
    BTN_START_VOCAB_TOPIC,
    BTN_VOCAB_REVIEW_NO,
    BTN_VOCAB_REVIEW_YES,
)


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


async def send_grammar_review_offers(bot) -> dict:
    return {"sent": 0, "disabled": True}


async def send_vocab_review_offers(bot) -> dict:
    return {"sent": 0, "disabled": True}
