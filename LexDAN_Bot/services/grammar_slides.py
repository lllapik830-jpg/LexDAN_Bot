"""
Состояние слайдов теории Grammar (прототип).
Превью UX — только MANAGER (ui_preview), пока владелец не скажет «заливай».
"""

from __future__ import annotations

from data.grammar_slides import get_grammar_slides, has_grammar_slides
from services.lesson_state import ensure_lesson, update_lesson
from services.ui_preview import ui_preview_only


def grammar_slides_enabled(user: dict, level: str, topic_id: str) -> bool:
    """Слайды вместо одного rico_intro — пока только превью + темы с банком."""
    if not has_grammar_slides(level, topic_id):
        return False
    return ui_preview_only(user=user)


def open_grammar_slides(user_id: str, topic_id: str, title: str) -> dict:
    """Открыть тему в режиме слайдов (hub = grammar_slides)."""

    def mut(u):
        ensure_lesson(u)
        les = u["lesson"]
        les["hub"] = "grammar_slides"
        les["topic_id"] = topic_id
        les["topic_title"] = title
        les["exercise"] = None
        les["exercise_num"] = None
        les["grammar_slide"] = 0
        les["slide_msg_id"] = None
        les["slide_chat_id"] = None
        les["awaiting_clarify"] = False
        les["clarify_ids"] = []

    return update_lesson(user_id, mut)


def set_grammar_slide_index(user_id: str, idx: int) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["grammar_slide"] = max(0, int(idx))

    return update_lesson(user_id, mut)


def save_grammar_slide_message(user_id: str, chat_id: int, message_id: int) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["slide_chat_id"] = int(chat_id)
        u["lesson"]["slide_msg_id"] = int(message_id)

    return update_lesson(user_id, mut)


def set_grammar_clarify(user_id: str, awaiting: bool) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["awaiting_clarify"] = bool(awaiting)
        if not awaiting:
            u["lesson"]["clarify_ids"] = []

    return update_lesson(user_id, mut)


def remember_clarify_msg(user_id: str, message_id: int) -> dict:
    def mut(u):
        ensure_lesson(u)
        ids = list(u["lesson"].get("clarify_ids") or [])
        ids.append(int(message_id))
        u["lesson"]["clarify_ids"] = ids[-12:]

    return update_lesson(user_id, mut)


__all__ = [
    "grammar_slides_enabled",
    "get_grammar_slides",
    "has_grammar_slides",
    "open_grammar_slides",
    "set_grammar_slide_index",
    "save_grammar_slide_message",
    "set_grammar_clarify",
    "remember_clarify_msg",
]
