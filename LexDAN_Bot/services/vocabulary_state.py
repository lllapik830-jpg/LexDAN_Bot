"""
Прогресс Vocabulary: слова и фразы по level:topic (не пересекаются между уровнями).
"""

from services.database import load_users, save_users, get_user
from services.lesson_state import ensure_lesson, update_lesson


def _blank_vocab_progress() -> dict:
    return {"words": [], "phrases": []}


def ensure_vocab_progress(user: dict) -> dict:
    if "vocabulary_progress" not in user or not isinstance(user["vocabulary_progress"], dict):
        user["vocabulary_progress"] = _blank_vocab_progress()
    else:
        user["vocabulary_progress"].setdefault("words", [])
        user["vocabulary_progress"].setdefault("phrases", [])
    return user["vocabulary_progress"]


def item_key(level: str, topic_id: str, en: str) -> str:
    return f"{level}:{topic_id}:{en.strip().lower()}"


def is_word_learned(user: dict, level: str, topic_id: str, en: str) -> bool:
    ensure_vocab_progress(user)
    return item_key(level, topic_id, en) in set(user["vocabulary_progress"]["words"])


def is_phrase_learned(user: dict, level: str, topic_id: str, en: str) -> bool:
    ensure_vocab_progress(user)
    return item_key(level, topic_id, en) in set(user["vocabulary_progress"]["phrases"])


def mark_word_learned(user_id: str, level: str, topic_id: str, en: str) -> dict:
    key = item_key(level, topic_id, en)

    def mut(u):
        ensure_vocab_progress(u)
        words = list(u["vocabulary_progress"]["words"])
        if key not in words:
            words.append(key)
        u["vocabulary_progress"]["words"] = words
        u["words_learned"] = len(words)

    return update_lesson(user_id, mut)


def mark_phrase_learned(user_id: str, level: str, topic_id: str, en: str) -> dict:
    key = item_key(level, topic_id, en)

    def mut(u):
        ensure_vocab_progress(u)
        phrases = list(u["vocabulary_progress"]["phrases"])
        if key not in phrases:
            phrases.append(key)
        u["vocabulary_progress"]["phrases"] = phrases
        u["phrases_learned"] = len(phrases)

    return update_lesson(user_id, mut)


def topic_words_progress(user: dict, level: str, topic_id: str, total: int) -> tuple[int, int, bool]:
    ensure_vocab_progress(user)
    prefix = f"{level}:{topic_id}:"
    learned = sum(1 for k in user["vocabulary_progress"]["words"] if k.startswith(prefix))
    done = total > 0 and learned >= total
    return learned, total, done


def topic_phrases_progress(user: dict, level: str, topic_id: str, total: int) -> tuple[int, int, bool]:
    ensure_vocab_progress(user)
    prefix = f"{level}:{topic_id}:"
    learned = sum(1 for k in user["vocabulary_progress"]["phrases"] if k.startswith(prefix))
    done = total > 0 and learned >= total
    return learned, total, done


def topic_combined_progress(user: dict, level: str, topic_id: str, words_total: int, phrases_total: int):
    wl, wt, wd = topic_words_progress(user, level, topic_id, words_total)
    pl, pt, pd = topic_phrases_progress(user, level, topic_id, phrases_total)
    learned = wl + pl
    total = wt + pt
    done = (wt == 0 or wd) and (pt == 0 or pd) and total > 0
    return learned, total, done


def get_all_learned_word_entries(user: dict) -> list[tuple[str, str, str]]:
    """[(level, topic_id, en), ...]"""
    from data.vocabulary_words import get_word_entry

    ensure_vocab_progress(user)
    out = []
    for key in user["vocabulary_progress"]["words"]:
        parts = key.split(":", 2)
        if len(parts) != 3:
            continue
        level, topic_id, en = parts
        entry = get_word_entry(level, topic_id, en)
        if entry:
            out.append((level, topic_id, entry["en"]))
    return out


def get_all_learned_phrase_entries(user: dict) -> list[tuple[str, str, str]]:
    from data.vocabulary_phrases import get_phrase_entry

    ensure_vocab_progress(user)
    out = []
    for key in user["vocabulary_progress"]["phrases"]:
        parts = key.split(":", 2)
        if len(parts) != 3:
            continue
        level, topic_id, en = parts
        entry = get_phrase_entry(level, topic_id, en)
        if entry:
            out.append((level, topic_id, entry["en"]))
    return out


def set_vocab_hub(user_id: str, hub: str, **fields) -> dict:
    def mut(u):
        ensure_lesson(u)
        ensure_vocab_progress(u)
        u["lesson"]["hub"] = hub
        for k, v in fields.items():
            u["lesson"][k] = v

    return update_lesson(user_id, mut)


def update_vocab_lesson(user_id: str, **fields) -> dict:
    def mut(u):
        ensure_lesson(u)
        for k, v in fields.items():
            u["lesson"][k] = v

    return update_lesson(user_id, mut)


def clear_vocab_session(user_id: str) -> dict:
    def mut(u):
        ensure_lesson(u)
        for k in (
            "vocab_topic_id",
            "vocab_mode",
            "vocab_batch",
            "vocab_active_item",
            "vocab_practice_step",
            "vocab_last_sentence",
            "vocab_text_en",
            "vocab_text_ru",
            "drill_kind",
            "drill_queue",
            "drill_index",
            "drill_dirs",
            "drill_current",
        ):
            u["lesson"].pop(k, None)

    return update_lesson(user_id, mut)
