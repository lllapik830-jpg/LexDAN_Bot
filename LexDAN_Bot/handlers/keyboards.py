"""
Кнопки бота.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.assessment_data import LEVELS, is_level_accessible

BTN_ALL_LEVELS_TASKS = "📋 Задания по всем уровням"


def is_dev_unlocked(user: dict | None) -> bool:
    return bool(user and user.get("dev_unlock"))


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
            [KeyboardButton(text="🎁 Пригласить друга")],
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


def lessons_home_levels(
    user_level: str | None = None,
    *,
    show_global_tasks: bool = False,
    user: dict | None = None,
) -> ReplyKeyboardMarkup:
    if is_dev_unlocked(user):
        visible = list(LEVELS)
    elif user_level:
        visible = [lv for lv in LEVELS if is_level_accessible(user_level, lv)]
    else:
        visible = list(LEVELS)
    rows = []
    row = []
    for lv in visible:
        row.append(KeyboardButton(text=lv))
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    if show_global_tasks:
        rows.append([KeyboardButton(text=BTN_ALL_LEVELS_TASKS)])
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
