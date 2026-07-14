"""
Состояние уроков (грамматика и дальше).
Прогресс (галочки) живёт отдельно от навигации — не сбрасывается в меню.
"""

from services.database import load_users, save_users, get_user

SECTIONS = [
    ("Grammar", "📘 Grammar"),
    ("Vocabulary", "📗 Vocabulary"),
    ("Listening", "🎧 Listening"),
    ("Reading", "📖 Reading"),
    ("Speaking", "🗣 Speaking"),
    ("Writing", "✍️ Writing"),
]

EXERCISE_TYPES = [
    (1, "Форма слова (выбор)"),
    (2, "Правильное предложение"),
    (3, "Пропуск в предложении"),
    (4, "Найди ошибку"),
    (5, "Преобразуй предложение"),
    (6, "Собери порядок слов"),
    (7, "Перевод на английский"),
    (8, "Напиши свои примеры"),
]


def _blank_lesson() -> dict:
    """Только навигация по экранам. Прогресс — в grammar_progress."""
    return {
        "hub": None,  # level_hub | grammar_list | topic | exercises | exercise
        "level": None,
        "section": None,
        "topic_id": None,
        "topic_title": None,
        "exercise_num": None,
        "exercise": None,
    }


def _blank_progress() -> dict:
    return {
        # "A0:present_simple" -> [1, 3, 5]
        "completed_exercises": {},
        # ["A0:alphabet", ...] — темы «только ознакомился»
        "completed_topics": [],
    }


def ensure_progress(user: dict) -> dict:
    if "grammar_progress" not in user or not isinstance(user["grammar_progress"], dict):
        user["grammar_progress"] = _blank_progress()
    else:
        blank = _blank_progress()
        for k, v in blank.items():
            user["grammar_progress"].setdefault(k, v if not isinstance(v, dict) else {})
        user["grammar_progress"].setdefault("completed_exercises", {})
        user["grammar_progress"].setdefault("completed_topics", [])
    # Миграция со старого хранения внутри lesson
    old = (user.get("lesson") or {}).get("completed_exercises")
    if isinstance(old, dict) and old:
        level = (user.get("lesson") or {}).get("level") or user.get("level") or "A1"
        dest = user["grammar_progress"]["completed_exercises"]
        for topic_id, nums in old.items():
            key = progress_key(level, topic_id) if ":" not in str(topic_id) else str(topic_id)
            merged = set(dest.get(key) or [])
            for n in nums or []:
                try:
                    merged.add(int(n))
                except (TypeError, ValueError):
                    pass
            dest[key] = sorted(merged)
        user["lesson"]["completed_exercises"] = {}
    return user["grammar_progress"]


def progress_key(level: str, topic_id: str) -> str:
    return f"{level}:{topic_id}"


def get_done_exercises(user: dict, level: str, topic_id: str) -> list[int]:
    ensure_progress(user)
    key = progress_key(level, topic_id)
    return list(user["grammar_progress"]["completed_exercises"].get(key) or [])


def is_topic_completed(user: dict, level: str, topic_id: str) -> bool:
    ensure_progress(user)
    return progress_key(level, topic_id) in (user["grammar_progress"].get("completed_topics") or [])


def ensure_lesson(user: dict) -> dict:
    if "lesson" not in user or not isinstance(user["lesson"], dict):
        user["lesson"] = _blank_lesson()
    else:
        blank = _blank_lesson()
        for k, v in blank.items():
            user["lesson"].setdefault(k, v)
    ensure_progress(user)
    return user


def update_lesson(user_id: str, mutator) -> dict:
    users = load_users()
    user = get_user(users, user_id)
    ensure_lesson(user)
    mutator(user)
    save_users(users)
    return user


def clear_lesson(user_id: str) -> None:
    """Сброс только навигации; прогресс (галочки) остаётся."""

    def mut(u):
        ensure_progress(u)
        u["lesson"] = _blank_lesson()

    update_lesson(user_id, mut)


def set_level_hub(user_id: str, level: str) -> dict:
    def mut(u):
        ensure_progress(u)
        u["lesson"] = _blank_lesson()
        u["lesson"]["hub"] = "level_hub"
        u["lesson"]["level"] = level

    return update_lesson(user_id, mut)


def set_grammar_list(user_id: str, level: str | None = None) -> dict:
    def mut(u):
        ensure_lesson(u)
        if level:
            u["lesson"]["level"] = level
        u["lesson"]["hub"] = "grammar_list"
        u["lesson"]["section"] = "Grammar"
        u["lesson"]["topic_id"] = None
        u["lesson"]["topic_title"] = None
        u["lesson"]["exercise"] = None
        u["lesson"]["exercise_num"] = None

    return update_lesson(user_id, mut)


def open_topic(user_id: str, topic_id: str, title: str) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["hub"] = "topic"
        u["lesson"]["topic_id"] = topic_id
        u["lesson"]["topic_title"] = title
        u["lesson"]["exercise"] = None
        u["lesson"]["exercise_num"] = None

    return update_lesson(user_id, mut)


def open_exercises_menu(user_id: str) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["hub"] = "exercises"
        u["lesson"]["exercise"] = None
        u["lesson"]["exercise_num"] = None

    return update_lesson(user_id, mut)


def start_exercise(user_id: str, num: int, exercise: dict) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["hub"] = "exercise"
        u["lesson"]["exercise_num"] = num
        u["lesson"]["exercise"] = exercise

    return update_lesson(user_id, mut)


def update_active_exercise(user_id: str, exercise: dict) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["exercise"] = exercise

    return update_lesson(user_id, mut)


def mark_exercise_done(user_id: str, level: str, topic_id: str, num: int) -> dict:
    def mut(u):
        ensure_progress(u)
        key = progress_key(level, topic_id)
        done = u["grammar_progress"].setdefault("completed_exercises", {})
        arr = list(done.get(key) or [])
        if num not in arr:
            arr.append(num)
        done[key] = sorted(arr)

    return update_lesson(user_id, mut)


def mark_topic_done(user_id: str, level: str, topic_id: str) -> dict:
    def mut(u):
        ensure_progress(u)
        key = progress_key(level, topic_id)
        topics = list(u["grammar_progress"].get("completed_topics") or [])
        if key not in topics:
            topics.append(key)
        u["grammar_progress"]["completed_topics"] = topics

    return update_lesson(user_id, mut)


def clear_active_exercise(user_id: str) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["hub"] = "exercises"
        u["lesson"]["exercise"] = None
        u["lesson"]["exercise_num"] = None

    return update_lesson(user_id, mut)


def assessment_busy(user: dict) -> bool:
    return bool((user.get("assessment") or {}).get("phase"))
