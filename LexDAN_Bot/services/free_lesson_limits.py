"""
Лимиты бесплатного тарифа по разделам уроков.

Free: один раздел в день (grammar / vocabulary / listening / reading).
После прохождения 1 темы в выбранном разделе остальные разделы
блокируются до 00:00 МСК. Платный «Безлимит» — без ограничений.
"""

from __future__ import annotations

from services.growth import ensure_growth

# Ключи разделов (уроки; Живая речь — отдельно, только с безлимитом)
SECTION_GRAMMAR = "grammar"
SECTION_VOCABULARY = "vocabulary"
SECTION_LISTENING = "listening"
SECTION_READING = "reading"

SECTION_LABELS = {
    SECTION_GRAMMAR: "Grammar",
    SECTION_VOCABULARY: "Vocabulary",
    SECTION_LISTENING: "Listening",
    SECTION_READING: "Reading",
}

# Сообщение при попытке зайти в другой раздел после темы
MSG_SECTION_LOCKED = (
    "🔥 На сегодня лимит исчерпан. Ты уже прошёл тему в другом разделе. "
    "Оформи безлимит, чтобы заниматься без ограничений."
)


def _has_unlimited_lessons(user: dict) -> bool:
    from services.rewards import has_lessons_pass

    return has_lessons_pass(user)


def free_lesson_section(user: dict) -> str | None:
    """Какой раздел уже «зачтён» сегодня (после прохождения темы)."""
    ensure_growth(user)
    sec = (user["daily"].get("free_lesson_section") or "").strip()
    return sec or None


def free_lesson_topic_done(user: dict) -> bool:
    ensure_growth(user)
    return bool(user["daily"].get("free_lesson_topic_done"))


def check_section_access(user: dict, section: str) -> tuple[bool, str | None]:
    """
    Можно ли бесплатнику зайти / продолжить раздел.
    Возвращает (ok, html_ошибка_или_None).
    """
    if _has_unlimited_lessons(user):
        return True, None
    ensure_growth(user)
    if not free_lesson_topic_done(user):
        return True, None
    chosen = free_lesson_section(user)
    if chosen and chosen == section:
        # Тот же раздел — можно продолжать
        return True, None
    return False, MSG_SECTION_LOCKED


def note_free_lesson_topic_done(user: dict, section: str) -> None:
    """
    Засчитать прохождение темы в разделе (1 раз в сутки на free).
    Фиксирует выбранный раздел и блокирует остальные до завтра.
    """
    if _has_unlimited_lessons(user):
        return
    if section not in SECTION_LABELS:
        return
    ensure_growth(user)
    daily = user["daily"]
    if daily.get("free_lesson_topic_done"):
        # Уже засчитано — не переключаем раздел
        return
    daily["free_lesson_section"] = section
    daily["free_lesson_topic_done"] = True
