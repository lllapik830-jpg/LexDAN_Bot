"""
Клавиатуры для уроков (грамматика).
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.grammar_curriculum import get_topics
from services.lesson_state import EXERCISE_TYPES, all_grammar_topics_done, is_grammar_test_passed

BTN_GRAMMAR_TEST = "🎯 Тест по Grammar"


def level_sections_kb() -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(text="📘 Grammar"), KeyboardButton(text="📗 Vocabulary")],
        [KeyboardButton(text="🎧 Listening"), KeyboardButton(text="📖 Reading")],
        [KeyboardButton(text="🗣 Speaking"), KeyboardButton(text="✍️ Writing")],
        [KeyboardButton(text="⬅️ К уровням")],
        [KeyboardButton(text="🔙 Вернуться в меню")],
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


def exercises_menu_kb() -> ReplyKeyboardMarkup:
    rows = []
    row = []
    for num, _title in EXERCISE_TYPES:
        row.append(KeyboardButton(text=f"Задание {num}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text="⬅️ К теме")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def exercise_mcq_kb(options: list[str]) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=opt)] for opt in options]
    rows.append([KeyboardButton(text="🌍 Перевести")])
    rows.append([KeyboardButton(text="🦜 Помощь Рико")])
    rows.append([KeyboardButton(text="⬅️ К выбору заданий"), KeyboardButton(text="⬅️ К теме")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def exercise_write_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 Перевести")],
            [KeyboardButton(text="🦜 Помощь Рико")],
            [KeyboardButton(text="⬅️ К выбору заданий"), KeyboardButton(text="⬅️ К теме")],
        ],
        resize_keyboard=True,
    )
