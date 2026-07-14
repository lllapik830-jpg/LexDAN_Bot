"""
Состояние уроков (грамматика и дальше).
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
    return {
        "hub": None,  # level_hub | grammar_list | topic | exercises | exercise
        "level": None,
        "section": None,
        "topic_id": None,
        "topic_title": None,
        "exercise_num": None,
        "exercise": None,  # {type, prompt, options, answer, explanation}
        "completed_exercises": {},  # topic_id -> [1,2,...]
    }


def ensure_lesson(user: dict) -> dict:
    if "lesson" not in user or not isinstance(user["lesson"], dict):
        user["lesson"] = _blank_lesson()
    else:
        blank = _blank_lesson()
        for k, v in blank.items():
            user["lesson"].setdefault(k, v)
        user["lesson"].setdefault("completed_exercises", {})
    return user


def update_lesson(user_id: str, mutator) -> dict:
    users = load_users()
    user = get_user(users, user_id)
    ensure_lesson(user)
    mutator(user)
    save_users(users)
    return user


def clear_lesson(user_id: str) -> None:
    def mut(u):
        u["lesson"] = _blank_lesson()

    update_lesson(user_id, mut)


def set_level_hub(user_id: str, level: str) -> dict:
    def mut(u):
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


def mark_exercise_done(user_id: str, topic_id: str, num: int) -> dict:
    def mut(u):
        ensure_lesson(u)
        done = u["lesson"].setdefault("completed_exercises", {})
        arr = list(done.get(topic_id) or [])
        if num not in arr:
            arr.append(num)
        done[topic_id] = sorted(arr)

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
