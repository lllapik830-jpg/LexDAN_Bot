from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- ГЛАВНОЕ МЕНЮ (4 кнопки) ---
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗣️ Общаться"), KeyboardButton(text="📚 Уроки")],
            [KeyboardButton(text="📊 Профиль"), KeyboardButton(text="🆘 Поддержка")]
        ],
        resize_keyboard=True
    )

# --- КНОПКИ В РЕЖИМЕ "ОБЩАТЬСЯ" (Перевести + Вернуться) ---
def back_to_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 Перевести")],
            [KeyboardButton(text="🔙 Вернуться в меню")]
        ],
        resize_keyboard=True
    )

# --- КНОПКИ В ПРОФИЛЕ ---
def profile_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💎 Подписка")],
            [KeyboardButton(text="🔙 Вернуться в меню")]
        ],
        resize_keyboard=True
    )