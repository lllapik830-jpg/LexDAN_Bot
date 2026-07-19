"""
Состояние уроков (грамматика и дальше).
Прогресс (галочки) живёт отдельно от навигации — не сбрасывается в меню.
"""

from services.database import load_users, save_users, get_user

SECTIONS = [
    ("Grammar", "📘 Grammar"),
    ("Vocabulary", "📗 Vocabulary"),
    # Listening / Reading / Speaking / Writing — временно скрыты (скоро)
]

EXERCISE_TYPES = [
    (1, "Выбор правильного ответа"),
    (2, "Выбор правильного ответа"),
    (3, "Выбор правильного ответа"),
    (4, "Напиши форму слова"),
    (5, "Напиши форму слова"),
    (6, "Напиши форму слова"),
    (7, "Перевод: русский → английский"),
    (8, "Перевод: английский → русский"),
]

ALL_EXERCISE_NUMS = {n for n, _ in EXERCISE_TYPES}


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
        "grammar_test": None,
    }


def _blank_progress() -> dict:
    return {
        # "A0:present_simple" -> [1, 3, 5]
        "completed_exercises": {},
        # ["A0:alphabet", ...] — темы полностью пройдены
        "completed_topics": [],
        # {"A0": true, "A1": true} — тест по разделу Grammar сдан
        "grammar_test_passed": {},
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
        user["grammar_progress"].setdefault("grammar_test_passed", {})
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


def is_topic_exercises_done(user: dict, level: str, topic_id: str) -> bool:
    done = set(get_done_exercises(user, level, topic_id))
    return ALL_EXERCISE_NUMS.issubset(done)


def is_grammar_topic_done(user: dict, level: str, topic: dict) -> bool:
    from data.grammar_curriculum import is_ack_topic

    tid = topic["id"]
    if is_ack_topic(topic):
        return is_topic_completed(user, level, tid)
    return is_topic_exercises_done(user, level, tid)


def all_grammar_topics_done(user: dict, level: str) -> bool:
    from data.grammar_curriculum import get_topics

    topics = get_topics(level)
    if not topics:
        return False
    return all(is_grammar_topic_done(user, level, t) for t in topics)


def is_grammar_test_passed(user: dict, level: str) -> bool:
    ensure_progress(user)
    return bool((user["grammar_progress"].get("grammar_test_passed") or {}).get(level))


def mark_grammar_test_passed(user_id: str, level: str) -> dict:
    def mut(u):
        ensure_progress(u)
        passed = u["grammar_progress"].setdefault("grammar_test_passed", {})
        passed[level] = True

    return update_lesson(user_id, mut)


def start_grammar_test(user_id: str, test_state: dict) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["hub"] = "grammar_test"
        u["lesson"]["grammar_test"] = test_state
        u["lesson"]["exercise"] = None
        u["lesson"]["exercise_num"] = None

    return update_lesson(user_id, mut)


def update_grammar_test(user_id: str, test_state: dict) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["grammar_test"] = test_state

    return update_lesson(user_id, mut)


def clear_grammar_test(user_id: str) -> dict:
    def mut(u):
        ensure_lesson(u)
        u["lesson"]["hub"] = "grammar_list"
        u["lesson"]["grammar_test"] = None

    return update_lesson(user_id, mut)


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
    save_users(users, only=str(user_id))
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


def set_section_stub(user_id: str, section_key: str) -> dict:
    """Заготовка будущего раздела (listening/reading/speaking/writing)."""

    def mut(u):
        ensure_lesson(u)
        u["lesson"]["hub"] = f"stub_{section_key}"

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
        u["lesson"]["grammar_test"] = None

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


def count_completed_tasks(user: dict) -> int:
    """Сколько заданий/тем засчитано в Grammar (для профиля)."""
    ensure_progress(user)
    gp = user["grammar_progress"]
    total = len(gp.get("completed_topics") or [])
    for nums in (gp.get("completed_exercises") or {}).values():
        total += len(nums or [])
    return total


def assessment_busy(user: dict) -> bool:
    return bool((user.get("assessment") or {}).get("phase"))
