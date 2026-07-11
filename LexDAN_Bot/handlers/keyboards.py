from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- ГЛАВНОЕ МЕНЮ (всегда внизу) ---
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗣️ Общаться"), KeyboardButton(text="📚 Уроки")],
            [KeyboardButton(text="💎 Подписка"), KeyboardButton(text="📊 Прогресс")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="🔄 Сброс")]
        ],
        resize_keyboard=True
    )

# --- КНОПКА ПЕРЕВОДА (под сообщением) ---
def translate_keyboard(lang="Russian"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📖 Перевести на {lang}", callback_data="translate")]
    ])

# --- КНОПКИ ПОДПИСКИ ---
def subscription_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 Безлимит (399 ₽)", callback_data="buy_base"),
            InlineKeyboardButton(text="👑 Премиум (799 ₽)", callback_data="buy_premium")
        ]
    ])

# --- МЕНЮ УРОКОВ ---
def lessons_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1. Введение", callback_data="lesson_1")]
    ])

# --- КНОПКА "ВЕРНУТЬСЯ К УРОКАМ" ---
def back_to_lessons_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Вернуться к урокам", callback_data="back_to_lessons")]
    ])