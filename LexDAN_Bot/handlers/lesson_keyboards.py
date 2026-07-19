"""
Клавиатуры для уроков (грамматика).
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from data.grammar_curriculum import get_topics
from services.lesson_state import EXERCISE_TYPES, all_grammar_topics_done, is_grammar_test_passed

BTN_GRAMMAR_TEST = "🎯 Тест по Grammar"
BTN_TRANSLATE = "🌍 Перевести"
BTN_RICO_HELP = "🦜 Помощь Рико"


def level_sections_kb() -> ReplyKeyboardMarkup:
    """Grammar + Vocabulary. L/R/S/W временно скрыты."""
    rows = [
        [KeyboardButton(text="📘 Grammar"), KeyboardButton(text="📗 Vocabulary")],
        [KeyboardButton(text="⬅️ К уровням"), KeyboardButton(text="🔙 Вернуться в меню")],
    ]
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def grammar_topics_kb(level: str, user: dict | None = None) -> ReplyKeyboardMarkup:
    topics = get_topics(level)
    rows = []
    row = []
    for i, _ in enumerate(topics, start=1):
        row.append(KeyboardButton(text=str(i)))
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    if user and all_grammar_topics_done(user, level) and not is_grammar_test_passed(user, level):
        rows.append([KeyboardButton(text=BTN_GRAMMAR_TEST)])
    rows.append([KeyboardButton(text="⬅️ К разделам")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def topic_chat_kb(*, ack: bool = False) -> ReplyKeyboardMarkup:
    rows = []
    if ack:
        rows.append([KeyboardButton(text="✅ Ознакомился")])
    else:
        rows.append([KeyboardButton(text="📝 Задания")])
    rows.append([KeyboardButton(text="⬅️ К темам")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def grammar_test_kb(*, mcq_options: list[str] | None = None) -> ReplyKeyboardMarkup:
    rows = []
    if mcq_options:
        rows.extend([[KeyboardButton(text=opt)] for opt in mcq_options])
    rows.append([KeyboardButton(text="⬅️ К темам")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def exercises_menu_kb(done: list[int] | None = None) -> ReplyKeyboardMarkup:
    done_set = set(done or [])
    rows = []
    row = []
    for num, _title in EXERCISE_TYPES:
        label = f"Задание {num} ✅" if num in done_set else f"Задание {num}"
        row.append(KeyboardButton(text=label))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text="⬅️ К теме")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def exercise_help_inline_kb() -> InlineKeyboardMarkup:
    """Перевод и помощь — над полем ввода, не перекрываются клавиатурой."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=BTN_TRANSLATE, callback_data="ex:translate"),
                InlineKeyboardButton(text=BTN_RICO_HELP, callback_data="ex:help"),
            ]
        ]
    )


def exercise_mcq_kb(options: list[str]) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=opt)] for opt in options]
    rows.append([KeyboardButton(text="⬅️ К выбору заданий"), KeyboardButton(text="⬅️ К теме")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def exercise_write_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ К выбору заданий"), KeyboardButton(text="⬅️ К теме")],
        ],
        resize_keyboard=True,
    )


def paywall_inline_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Выбрать тариф", callback_data="tariff:open")],
        ]
    )


def lesson_limit_inline_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Купить доступ", callback_data="tariff:open")],
        ]
    )


def chat_limit_inline_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Активировать полный доступ",
                    callback_data="tariff:open",
                )
            ],
        ]
    )


def tariffs_inline_kb(user: dict | None = None) -> InlineKeyboardMarkup:
    from services.growth import PRICE_CHAT_MONTH, PRICE_FULL_MONTH
    from services.pricing import chat_price, full_price

    if user:
        chat_p, chat_d = chat_price(user)
        full_p, full_d = full_price(user)
        chat_label = (
            f"💬 Общение — {chat_p}₽/мес (−{chat_d}%)"
            if chat_d
            else f"💬 Только общение — {PRICE_CHAT_MONTH}₽/мес"
        )
        full_label = (
            f"🚀 Всё — {full_p}₽/мес (−{full_d}%)"
            if full_d
            else f"🚀 Безлимит ко всему — {PRICE_FULL_MONTH}₽/мес"
        )
    else:
        chat_label = f"💬 Только общение — {PRICE_CHAT_MONTH}₽/мес"
        full_label = f"🚀 Безлимит ко всему — {PRICE_FULL_MONTH}₽/мес"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=chat_label, callback_data="tariff:chat")],
            [InlineKeyboardButton(text=full_label, callback_data="tariff:full")],
        ]
    )
