"""
Логика входного теста уровня (состояние пользователя).
"""

from data.assessment_data import (
    LEVELS,
    get_translation,
    pick_vocab,
    pick_listen,
    pick_topic,
    lower_level,
    raise_level,
    level_index,
)
from services.database import load_users, save_users, get_user


def _blank_assessment() -> dict:
    return {
        "phase": None,  # translate | vocab | listen | write
        "cefr": "B2",
        "translate_level": "B2",
        "translate_variant": 0,
        "translate_source_en": "",
        "translate_reference_ru": "",
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
    def mut(user):
        user["assessment"] = _blank_assessment()
        user["assessment"]["phase"] = "translate"
        user["assessment"]["cefr"] = "B2"
        user["assessment"]["translate_level"] = "B2"
        item = get_translation("B2", 0)
        user["assessment"]["translate_variant"] = 0
        user["assessment"]["translate_source_en"] = item["en"]
        user["assessment"]["translate_reference_ru"] = item["ru"]
        user["assessment"]["a0_second_shown"] = False

    return update_user(user_id, mut)


def set_translation_item(user_id: str, level: str, variant: int) -> dict:
    def mut(user):
        a = user["assessment"]
        item = get_translation(level, variant)
        a["translate_level"] = level
        a["translate_variant"] = variant
        a["translate_source_en"] = item["en"]
        a["translate_reference_ru"] = item["ru"]
        if level == "A0" and variant == 1:
            a["a0_second_shown"] = True

    return update_user(user_id, mut)


def begin_vocab(user_id: str, level: str) -> dict:
    def mut(user):
        a = user["assessment"]
        a["phase"] = "vocab"
        a["cefr"] = level
        a["vocab_level"] = level
        a["vocab_i"] = 0
        a["vocab_used"] = []
        word = pick_vocab(level, [])
        a["vocab_en"] = word["en"]
        a["vocab_ru"] = word["ru"]
        a["vocab_used"] = [word["en"]]

    return update_user(user_id, mut)


def next_vocab(user_id: str, level: str) -> dict:
    def mut(user):
        a = user["assessment"]
        a["vocab_level"] = level
        a["cefr"] = level
        a["vocab_i"] = int(a.get("vocab_i", 0)) + 1
        word = pick_vocab(level, a.get("vocab_used") or [])
        a["vocab_en"] = word["en"]
        a["vocab_ru"] = word["ru"]
        used = list(a.get("vocab_used") or [])
        used.append(word["en"])
        a["vocab_used"] = used

    return update_user(user_id, mut)


def begin_listen(user_id: str, level: str) -> dict:
    def mut(user):
        a = user["assessment"]
        a["phase"] = "listen"
        a["listen_level"] = level
        a["cefr"] = level
        a["listen_i"] = 0
        a["listen_used"] = []
        text = pick_listen(level, [])
        a["listen_text"] = text
        a["listen_used"] = [text]

    return update_user(user_id, mut)


def next_listen(user_id: str, level: str) -> dict:
    def mut(user):
        a = user["assessment"]
        a["listen_level"] = level
        a["cefr"] = level
        a["listen_i"] = int(a.get("listen_i", 0)) + 1
        text = pick_listen(level, a.get("listen_used") or [])
        a["listen_text"] = text
        used = list(a.get("listen_used") or [])
        used.append(text)
        a["listen_used"] = used

    return update_user(user_id, mut)


def begin_write(user_id: str, level: str) -> dict:
    def mut(user):
        a = user["assessment"]
        a["phase"] = "write"
        a["write_level"] = level
        a["cefr"] = level
        a["write_topic"] = pick_topic(level)

    return update_user(user_id, mut)


def finish_assessment(user_id: str, final_level: str) -> dict:
    if final_level not in LEVELS:
        final_level = "A1"

    def mut(user):
        user["level"] = final_level
        user["assessment_done"] = True
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
    avg = round(sum(idxs) / len(idxs))
    return LEVELS[avg]


def adjust_level(level: str, success: bool) -> str:
    return raise_level(level) if success else lower_level(level)
