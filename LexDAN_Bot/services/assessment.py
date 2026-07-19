"""
Состояние входного теста (генерация заданий уникальна для пользователя).
"""

import uuid

from data.assessment_data import LEVELS, lower_level, raise_level, level_index
from services.database import load_users, save_users, get_user
from services.assessment_gen import (
    generate_translation,
    generate_vocab,
    generate_listen,
    generate_write_topic,
)


def _blank_assessment() -> dict:
    return {
        "phase": None,
        "cefr": "B2",
        "translate_level": "B2",
        "translate_variant": 0,
        "translate_source_en": "",
        "translate_reference_ru": "",
        "translate_estimate": "B2",
        "a0_second_shown": False,
        "vocab_i": 0,
        "vocab_level": "B2",
        "vocab_en": "",
        "vocab_ru": [],
        "vocab_used": [],
        "listen_i": 0,
        "listen_level": "B2",
        "listen_text": "",
        "listen_used": [],
        "write_topic": "",
        "write_level": "B2",
        "write_replacements_left": 3,
        "write_failed": False,
    }


def ensure_user_fields(user: dict) -> dict:
    user.setdefault("assessment_done", False)
    if "assessment" not in user or not isinstance(user["assessment"], dict):
        user["assessment"] = _blank_assessment()
    else:
        blank = _blank_assessment()
        for k, v in blank.items():
            user["assessment"].setdefault(k, v)
    return user


def update_user(user_id: str, mutator) -> dict:
    users = load_users()
    user = get_user(users, user_id)
    ensure_user_fields(user)
    mutator(user)
    save_users(users)
    return user


def start_assessment(user_id: str) -> dict:
    item = generate_translation("B2", seed=f"{user_id}-{uuid.uuid4()}")

    def mut(user):
        user["assessment"] = _blank_assessment()
        a = user["assessment"]
        a["phase"] = "translate"
        a["cefr"] = "B2"
        a["translate_level"] = "B2"
        a["translate_variant"] = 0
        a["translate_source_en"] = item["en"]
        a["translate_reference_ru"] = item["ru"]
        a["a0_second_shown"] = False

    return update_user(user_id, mut)


def set_translation_item(user_id: str, level: str, variant: int) -> dict:
    item = generate_translation(level, seed=f"{user_id}-{level}-{variant}-{uuid.uuid4()}")

    def mut(user):
        a = user["assessment"]
        a["translate_level"] = level
        a["translate_variant"] = variant
        a["translate_source_en"] = item["en"]
        a["translate_reference_ru"] = item["ru"]
        if level == "A0" and variant == 1:
            a["a0_second_shown"] = True

    return update_user(user_id, mut)


def set_translate_estimate(user_id: str, level: str) -> dict:
    def mut(user):
        user["assessment"]["translate_estimate"] = level
        user["assessment"]["cefr"] = level

    return update_user(user_id, mut)


def begin_vocab(user_id: str, level: str) -> dict:
    word = generate_vocab(level, [])

    def mut(user):
        a = user["assessment"]
        a["phase"] = "vocab"
        a["cefr"] = level
        a["vocab_level"] = level
        a["vocab_i"] = 0
        a["vocab_en"] = word["en"]
        a["vocab_ru"] = word["ru"]
        a["vocab_used"] = [word["en"]]

    return update_user(user_id, mut)


def next_vocab(user_id: str, level: str) -> dict:
    users = load_users()
    user = get_user(users, user_id)
    ensure_user_fields(user)
    used = list(user["assessment"].get("vocab_used") or [])
    word = generate_vocab(level, used)

    def mut(u):
        a = u["assessment"]
        a["vocab_level"] = level
        a["cefr"] = level
        a["vocab_i"] = int(a.get("vocab_i", 0)) + 1
        a["vocab_en"] = word["en"]
        a["vocab_ru"] = word["ru"]
        used2 = list(a.get("vocab_used") or [])
        used2.append(word["en"])
        a["vocab_used"] = used2

    return update_user(user_id, mut)


def begin_listen(user_id: str, level: str) -> dict:
    text = generate_listen(level, [])

    def mut(user):
        a = user["assessment"]
        a["phase"] = "listen"
        a["listen_level"] = level
        a["cefr"] = level
        a["listen_i"] = 0
        a["listen_text"] = text
        a["listen_used"] = [text]

    return update_user(user_id, mut)


def next_listen(user_id: str, level: str) -> dict:
    users = load_users()
    user = get_user(users, user_id)
    ensure_user_fields(user)
    used = list(user["assessment"].get("listen_used") or [])
    text = generate_listen(level, used)

    def mut(u):
        a = u["assessment"]
        a["listen_level"] = level
        a["cefr"] = level
        a["listen_i"] = int(a.get("listen_i", 0)) + 1
        a["listen_text"] = text
        used2 = list(a.get("listen_used") or [])
        used2.append(text)
        a["listen_used"] = used2

    return update_user(user_id, mut)


def begin_write(user_id: str, level: str) -> dict:
    topic = generate_write_topic(level)

    def mut(user):
        a = user["assessment"]
        a["phase"] = "write"
        a["write_level"] = level
        a["cefr"] = level
        a["write_topic"] = topic
        a["write_replacements_left"] = 3
        a["write_failed"] = False

    return update_user(user_id, mut)


def replace_write_topic(user_id: str) -> tuple[dict | None, str]:
    """
    Заменить тему письма.
    Возвращает (user, status):
      - "ok" — тема заменена
      - "ended" — использована последняя замена, задание провалено
      - "none" — замен уже не было
    """
    users = load_users()
    user = get_user(users, user_id)
    ensure_user_fields(user)
    a = user["assessment"]
    left = int(a.get("write_replacements_left", 0))

    if left <= 0:
        return user, "none"

    # последняя замена → задание завершается как невыполненное
    if left == 1:

        def mut_end(u):
            aa = u["assessment"]
            aa["write_replacements_left"] = 0
            aa["write_failed"] = True

        return update_user(user_id, mut_end), "ended"

    left -= 1
    level = a.get("write_level") or "A2"
    topic = generate_write_topic(level)

    def mut(u):
        aa = u["assessment"]
        aa["write_replacements_left"] = left
        aa["write_topic"] = topic

    return update_user(user_id, mut), "ok"


def finish_assessment(user_id: str, final_level: str) -> dict:
    if final_level not in LEVELS:
        final_level = "A1"

    def mut(user):
        user["level"] = final_level
        user["assessment_done"] = True
        # После калибровки открыт только этот уровень и ниже
        user["grammar_unlock_ceiling"] = final_level
        user["assessment"] = _blank_assessment()

    return update_user(user_id, mut)


def clear_assessment_phase(user_id: str) -> dict:
    def mut(user):
        user["assessment"] = _blank_assessment()

    return update_user(user_id, mut)


def average_level(levels: list[str]) -> str:
    if not levels:
        return "A1"
    idxs = [level_index(x) for x in levels if x in LEVELS]
    if not idxs:
        return "A1"
    # строже: округляем вниз
    avg = int(sum(idxs) / len(idxs))
    return LEVELS[avg]


def adjust_level(level: str, success: bool) -> str:
    return raise_level(level) if success else lower_level(level)
