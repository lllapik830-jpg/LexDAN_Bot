"""
Кнопки бота.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.assessment_data import LEVELS, is_level_accessible_for_user

BTN_ALL_LEVELS_TASKS = "📋 Задания по всем уровням"
BTN_START_TODAY = "🚀 Начать сегодня"


def is_dev_unlocked(user: dict | None) -> bool:
    return bool(user and user.get("dev_unlock"))


def main_menu(user: dict | None = None, *, user_id: str | int | None = None) -> ReplyKeyboardMarkup:
    from services.secret_missions import BTN_SECRET, has_secret_entry
    from services.daily_fire import BTN_DAILY_FIRE
    from services.course_placement import BTN_COURSES, courses_allowed

    rows = [
        [KeyboardButton(text="🗣️ Общаться"), KeyboardButton(text="📚 Уроки")],
    ]
    uid = user_id
    if uid is None and isinstance(user, dict):
        uid = (
            user.get("tg_id")
            or user.get("telegram_id")
            or user.get("id")
        )
    # Курсы — только менеджеру; у остальных кнопки нет вообще
    if courses_allowed(uid):
        rows.append([KeyboardButton(text=BTN_COURSES)])
    rows.append([KeyboardButton(text=BTN_DAILY_FIRE)])
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


def profile_menu(
    user: dict | None = None, *, user_id: str | int | None = None
) -> ReplyKeyboardMarkup:
    from services.growth import BTN_RESTORE_STREAK, can_restore_streak
    from services.rewards import BTN_STREAK, BTN_REFERRAL
    from services.promo import BTN_ENTER_PROMO
    from services.collection import BTN_COLLECTION, collection_allowed
    from services.event_magic import BTN_HALL_OF_FAME, BTN_LEADERBOARD, is_event_active
    from services.event_prize_delivery import prize_task_button_for

    rows = [
        [KeyboardButton(text="💎 Подписка")],
    ]
    if collection_allowed(user_id):
        # Кнопка ивента только пока ивент активен
        if is_event_active():
            rows.append([KeyboardButton(text=BTN_COLLECTION)])
        # Гонка и зал славы — всегда (после финала показывают итоги)
        rows.append(
            [KeyboardButton(text=BTN_LEADERBOARD), KeyboardButton(text=BTN_HALL_OF_FAME)]
        )
    task_btn = prize_task_button_for(user)
    if task_btn:
        rows.append([KeyboardButton(text=task_btn)])
    rows.append([KeyboardButton(text="✏️ Изменить имя"), KeyboardButton(text=BTN_ENTER_PROMO)])
    rows.append([KeyboardButton(text="🗺 Навигация")])
    rows.append([KeyboardButton(text=BTN_STREAK), KeyboardButton(text=BTN_REFERRAL)])
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
            and not is_dev_unlocked(user)
            and not is_level_accessible_for_user(user, lv)
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
    # Второй голос Рико — приз 1–2 места
    try:
        from services.voices import BTN_RICO_VOICE, rico_alt_voice_unlocked

        if user is not None and rico_alt_voice_unlocked(user):
            rows.append([KeyboardButton(text=BTN_RICO_VOICE)])
    except Exception:
        pass
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def assess_translate_kb(show_skip: bool = True, *, no_menu: bool = False) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text="⬇️ Дай текст проще")]]
    if show_skip:
        rows.append([KeyboardButton(text="⏭️ Пропустить задание")])
    if not no_menu:
        rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def assess_simple_kb(*, no_menu: bool = False) -> ReplyKeyboardMarkup:
    if no_menu:
        return ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Вернуться в меню")]],
        resize_keyboard=True,
    )


def assess_dont_know_kb(*, no_menu: bool = False) -> ReplyKeyboardMarkup:
    """Словарь / аудирование."""
    rows = [[KeyboardButton(text="🙈 Не знаю")]]
    if not no_menu:
        rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def assess_write_kb(
    *, no_menu: bool = False, show_skip: bool = False
) -> ReplyKeyboardMarkup:
    """Письмо: замена темы; на последнем тексте — пропуск."""
    rows: list[list[KeyboardButton]] = []
    if show_skip:
        rows.append([KeyboardButton(text="⏭️ Пропустить задание")])
    else:
        rows.append([KeyboardButton(text="🔄 Заменить текст")])
    if not no_menu:
        rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)
