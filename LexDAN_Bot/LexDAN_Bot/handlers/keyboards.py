"""
Кнопки бота.

Простыми словами:
здесь только РИСУЕМ кнопки. Логика «что делать при нажатии» — в других файлах.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu() -> ReplyKeyboardMarkup:
    """Главное меню — 4 большие кнопки."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗣️ Общаться"), KeyboardButton(text="📚 Уроки")],
            [KeyboardButton(text="📊 Профиль"), KeyboardButton(text="🆘 Поддержка")],
        ],
        resize_keyboard=True,
    )


def chat_menu() -> ReplyKeyboardMarkup:
    """Кнопки внутри раздела «Общаться»."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 Перевести")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def back_to_menu() -> ReplyKeyboardMarkup:
    """Одна кнопка «назад» (уроки, заглушки и т.п.)."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Вернуться в меню")]],
        resize_keyboard=True,
    )


def profile_menu() -> ReplyKeyboardMarkup:
    """Кнопки внутри профиля."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💎 Подписка")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )
