"""
Клавиатуры Vocabulary.
"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data.vocabulary_curriculum import get_vocab_topics
from services.vocabulary_state import (
    topic_combined_progress,
    topic_words_progress,
    topic_phrases_progress,
    is_word_learned,
    is_phrase_learned,
)
from data.vocabulary_words import words_total, has_vocabulary_level
from data.vocabulary_phrases import phrases_total

BTN_VOCABULARY = "📗 Vocabulary"
BTN_LEARN_PHRASES = "📌 Учить фразы"
BTN_ALL_LEVELS = "📋 Задания по всем уровням"
BTN_REPEAT_WORDS = "🔁 Повторить изученные слова"
BTN_REPEAT_PHRASES = "🔁 Повторить изученные фразы"
BTN_DONT_REMEMBER = "🤔 Не помню"
BTN_BACK_DRILL = "⬅️ Вернуться назад"


def vocab_topics_kb(level: str, user: dict) -> ReplyKeyboardMarkup:
    topics = get_vocab_topics(level)
    rows = []
    row = []
    for i, t in enumerate(topics, start=1):
        row.append(KeyboardButton(text=str(i)))
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text="⬅️ К разделам")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def vocab_topic_kb(level: str, topic_id: str, user: dict, batch_words: list[str]) -> ReplyKeyboardMarkup:
    rows = []
    for en in batch_words:
        mark = "✅ " if is_word_learned(user, level, topic_id, en) else ""
        rows.append([KeyboardButton(text=f"{mark}{en}")])
    rows.append([KeyboardButton(text=BTN_LEARN_PHRASES)])
    rows.append([KeyboardButton(text="⬅️ К темам")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def vocab_phrase_topic_kb(level: str, topic_id: str, user: dict, batch: list[str]) -> ReplyKeyboardMarkup:
    rows = []
    for en in batch:
        short = en if len(en) <= 40 else en[:37] + "..."
        mark = "✅ " if is_phrase_learned(user, level, topic_id, en) else ""
        rows.append([KeyboardButton(text=f"{mark}{short}")])
    rows.append([KeyboardButton(text="⬅️ К теме (слова)")])
    rows.append([KeyboardButton(text="⬅️ К темам")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def vocab_practice_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ К словам")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def global_drill_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_REPEAT_WORDS)],
            [KeyboardButton(text=BTN_REPEAT_PHRASES)],
            [KeyboardButton(text="⬅️ К уровням")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def drill_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_DONT_REMEMBER)],
            [KeyboardButton(text=BTN_BACK_DRILL)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def topic_progress_line(user: dict, level: str, topic_id: str) -> str:
    wt = words_total(level, topic_id)
    pt = phrases_total(level, topic_id)
    wl, _, _ = topic_words_progress(user, level, topic_id, wt)
    pl, _, _ = topic_phrases_progress(user, level, topic_id, pt)
    return f"Слов: {wl}/{wt} · Фраз: {pl}/{pt}"
