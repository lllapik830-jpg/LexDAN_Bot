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

# --- КНОПКА "ВЕРНУТЬСЯ В МЕНЮ" (используется в разделах) ---
def back_to_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Вернуться в меню")]],
        resize_keyboard=True
    )

# --- КНОПКИ В ПРОФИЛЕ (Подписка + Вернуться) ---
def profile_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💎 Подписка")],
            [KeyboardButton(text="🔙 Вернуться в меню")]
        ],
        resize_keyboard=True
    )

# --- КНОПКИ В РАЗДЕЛЕ "ОБЩАТЬСЯ" (пока нет перевода, только "Вернуться") ---
def chat_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Вернуться в меню")]],
        resize_keyboard=True
    )