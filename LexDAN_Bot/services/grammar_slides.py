"""
Состояние и выдача слайдов теории Grammar (как в онбординге).
Для всех пользователей и всех тем раздела.
"""

from __future__ import annotations

from data.grammar_slides import get_manual_slides, intro_to_slides
from services.lesson_state import ensure_lesson, update_lesson


def get_grammar_slides(level: str, topic_id: str) -> list[str] | None:
    """Ручной банк или авто-разбивка rico_intro темы."""
    manual = get_manual_slides(level, topic_id)
    if manual:
        return manual

    from data.grammar_curriculum import get_topic, is_ack_topic

    topic = get_topic(level, topic_id)
    if not topic:
        return None
    intro = (topic.get("rico_intro") or "").strip()
    if not intro:
        return None
    return intro_to_slides(intro, ack=is_ack_topic(topic))


def has_grammar_slides(level: str, topic_id: str) -> bool:
    return get_grammar_slides(level, topic_id) is not None


def grammar_slides_enabled(user: dict, level: str, topic_id: str) -> bool:
    """Слайды вместо одного длинного rico_intro — для всех."""
    return has_grammar_slides(level, topic_id)


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
