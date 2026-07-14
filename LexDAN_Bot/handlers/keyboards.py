"""
Кнопки бота.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.assessment_data import LEVELS


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗣️ Общаться"), KeyboardButton(text="📚 Уроки")],
            [KeyboardButton(text="📊 Профиль"), KeyboardButton(text="🆘 Поддержка")],
        ],
        resize_keyboard=True,
    )


def chat_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 Перевести")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def back_to_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Вернуться в меню")]],
        resize_keyboard=True,
    )


def profile_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💎 Подписка")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def lessons_home_first() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎯 Проверить уровень")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def lessons_home_levels() -> ReplyKeyboardMarkup:
    rows = []
    row = []
    for i, lv in enumerate(LEVELS):
        row.append(KeyboardButton(text=lv))
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def assess_translate_kb(show_skip: bool = False) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text="⬇️ Дай текст проще")]]
    if show_skip:
        rows.append([KeyboardButton(text="⏭️ Пропустить задание")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def assess_simple_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Вернуться в меню")]],
        resize_keyboard=True,
    )


def assess_dont_know_kb() -> ReplyKeyboardMarkup:
    """Словарь / аудирование."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🙈 Не знаю")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def assess_write_kb() -> ReplyKeyboardMarkup:
    """Письмо: замена темы."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔄 Заменить текст")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )
