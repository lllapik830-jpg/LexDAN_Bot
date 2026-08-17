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
BTN_RICO_CHAT = "🦜 Общение с Рико"
BTN_EXTRA = "📝 Доп. задания"
BTN_EXTRA_NEXT = "➡️ Далее"  # legacy alias
BTN_EXTRA_SKIP = "⏭ Пропустить"
BTN_EXTRA_HINT = "💡 Подсказка"
BTN_EXTRA_DO = "✅ Делать задания"
BTN_EXTRA_MISTAKES = "🔧 Отработать ошибки"
BTN_TRANSLATE = "🌍 Перевести"
BTN_RICO_HELP = "🦜 Помощь Рико"


def level_sections_kb(user: dict | None = None, *, user_id: str | int | None = None) -> ReplyKeyboardMarkup:
    """Grammar + Vocabulary + Listening + Reading (+ Живая речь на A1–C2)."""
    uid = user_id
    if uid is None and isinstance(user, dict):
        uid = user.get("tg_id") or user.get("telegram_id") or user.get("id")
    rows = [
        [KeyboardButton(text="📘 Grammar"), KeyboardButton(text="📗 Vocabulary")],
        [KeyboardButton(text="🎧 Listening"), KeyboardButton(text="📖 Reading")],
    ]
    from data.street_talk import BTN_STREET, street_talk_open
    from services.database import get_user, load_users

    level = ""
    if isinstance(user, dict):
        level = (user.get("lesson") or {}).get("level") or user.get("level") or ""
    if not level and uid is not None:
        try:
            u = get_user(load_users(), str(uid))
            level = (u.get("lesson") or {}).get("level") or u.get("level") or ""
        except Exception:
            level = ""
    if street_talk_open(level):
        rows.append([KeyboardButton(text=BTN_STREET)])
    rows.append(
        [KeyboardButton(text="⬅️ К уровням"), KeyboardButton(text="🔙 Вернуться в меню")]
    )
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
    lvl = (level or "").upper()
    if lvl in {"A1", "A2", "B1", "B2", "C1", "C2"}:
        rows.append([KeyboardButton(text=BTN_EXTRA), KeyboardButton(text=BTN_RICO_CHAT)])
    else:
        rows.append([KeyboardButton(text=BTN_RICO_CHAT)])
    if user and all_grammar_topics_done(user, level) and not is_grammar_test_passed(user, level):
        rows.append([KeyboardButton(text=BTN_GRAMMAR_TEST)])
    rows.append([KeyboardButton(text="⬅️ К разделам")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def grammar_extra_menu_kb(*, mistakes: int = 0) -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(text=BTN_EXTRA_DO)],
        [KeyboardButton(text=BTN_EXTRA_MISTAKES + (f" ({mistakes})" if mistakes else ""))],
        [KeyboardButton(text="⬅️ К темам")],
        [KeyboardButton(text="🔙 Вернуться в меню")],
    ]
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def grammar_extra_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_EXTRA_HINT), KeyboardButton(text=BTN_EXTRA_SKIP)],
            [KeyboardButton(text="⬅️ К темам")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def grammar_rico_chat_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_TRANSLATE)],
            [KeyboardButton(text="⬅️ К темам")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


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
    from services.sept_promo import (
        PROMO_CHAT_RUB,
        PROMO_FULL_RUB,
        is_sept_promo_active,
    )

    promo = is_sept_promo_active()
    if user:
        chat_p, chat_d = chat_price(user)
        full_p, full_d = full_price(user)
        if promo:
            chat_label = f"💬 Общение — {chat_p}₽ (было {PRICE_CHAT_MONTH})"
            full_label = f"🚀 Полный — {full_p}₽ (было {PRICE_FULL_MONTH})"
        elif chat_d or full_d:
            chat_label = (
                f"💬 Общение — {chat_p}₽ (было {PRICE_CHAT_MONTH})"
                if chat_d
                else f"💬 Только общение — {PRICE_CHAT_MONTH}₽/мес"
            )
            full_label = (
                f"🚀 Полный — {full_p}₽ (было {PRICE_FULL_MONTH})"
                if full_d
                else f"🚀 Безлимит ко всему — {PRICE_FULL_MONTH}₽/мес"
            )
        else:
            chat_label = f"💬 Только общение — {PRICE_CHAT_MONTH}₽/мес"
            full_label = f"🚀 Безлимит ко всему — {PRICE_FULL_MONTH}₽/мес"
    elif promo:
        chat_label = f"💬 Общение — {PROMO_CHAT_RUB}₽ (было {PRICE_CHAT_MONTH})"
        full_label = f"🚀 Полный — {PROMO_FULL_RUB}₽ (было {PRICE_FULL_MONTH})"
    else:
        chat_label = f"💬 Только общение — {PRICE_CHAT_MONTH}₽/мес"
        full_label = f"🚀 Безлимит ко всему — {PRICE_FULL_MONTH}₽/мес"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=chat_label, callback_data="tariff:chat")],
            [InlineKeyboardButton(text=full_label, callback_data="tariff:full")],
        ]
    )


def upgrade_inline_kb(user: dict | None = None) -> InlineKeyboardMarkup:
    """Кнопка апгрейда 399 → 799 для тарифа «Общение»."""
    from services.pricing import upgrade_price

    price, disc = upgrade_price(user) if user else (399, 0)
    label = (
        f"🚀 Апгрейд до полного — {price}₽ (−{disc}%)"
        if disc
        else f"🚀 Апгрейд до полного — {price}₽"
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data="tariff:upgrade")],
        ]
    )
