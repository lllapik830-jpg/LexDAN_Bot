"""
Кнопки бота.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.assessment_data import LEVELS, is_level_accessible

BTN_ALL_LEVELS_TASKS = "📋 Задания по всем уровням"
BTN_START_TODAY = "🚀 Начать сегодня"


def is_dev_unlocked(user: dict | None) -> bool:
    return bool(user and user.get("dev_unlock"))


def main_menu(user: dict | None = None) -> ReplyKeyboardMarkup:
    from services.secret_missions import BTN_SECRET, has_secret_entry

    rows = [
        [KeyboardButton(text="🗣️ Общаться"), KeyboardButton(text="📚 Уроки")],
    ]
    if user is not None and has_secret_entry(user):
        rows.append([KeyboardButton(text=BTN_SECRET)])
    rows.append(
        [KeyboardButton(text="📊 Профиль"), KeyboardButton(text="🆘 Поддержка")]
    )
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def chat_menu() -> ReplyKeyboardMarkup:
    from services.voices import BTN_CHAT_VOICE

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 Перевести"), KeyboardButton(text=BTN_CHAT_VOICE)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def back_to_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Вернуться в меню")]],
        resize_keyboard=True,
    )


def profile_menu(user: dict | None = None) -> ReplyKeyboardMarkup:
    from services.growth import BTN_RESTORE_STREAK, can_restore_streak
    from services.rewards import BTN_STREAK, BTN_REFERRAL

    rows = [
        [KeyboardButton(text="💎 Подписка")],
        [KeyboardButton(text=BTN_STREAK), KeyboardButton(text=BTN_REFERRAL)],
    ]
    if user is not None and can_restore_streak(user):
        rows.append([KeyboardButton(text=BTN_RESTORE_STREAK)])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


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
    show_start_today: bool = False,
) -> ReplyKeyboardMarkup:
    """Всегда показываем A0–C2; доступность проверяется при клике."""
    visible = list(LEVELS)
    rows = []
    if show_start_today:
        rows.append([KeyboardButton(text=BTN_START_TODAY)])
    row = []
    for lv in visible:
        # 🔒 на кнопке, если уровень выше доступного (кроме DEV)
        label = lv
        if (
            user
            and user_level
            and not is_dev_unlocked(user)
            and not is_level_accessible(user_level, lv)
        ):
            label = f"{lv} 🔒"
        row.append(KeyboardButton(text=label))
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    if show_global_tasks:
        rows.append([KeyboardButton(text=BTN_ALL_LEVELS_TASKS)])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def assess_translate_kb(show_skip: bool = True) -> ReplyKeyboardMarkup:
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
