"""
Прогресс Vocabulary: слова и фразы по level:topic (не пересекаются между уровнями).
"""

from services.database import load_users, save_users, get_user
from services.lesson_state import ensure_lesson, update_lesson


def _blank_vocab_progress() -> dict:
    return {"words": [], "phrases": [], "final_test_passed": {}}


def ensure_vocab_progress(user: dict) -> dict:
    if "vocabulary_progress" not in user or not isinstance(user["vocabulary_progress"], dict):
        user["vocabulary_progress"] = _blank_vocab_progress()
    else:
        user["vocabulary_progress"].setdefault("words", [])
        user["vocabulary_progress"].setdefault("phrases", [])
        user["vocabulary_progress"].setdefault("final_test_passed", {})
    # Счётчики профиля всегда = длина списков
    user["words_learned"] = len(user["vocabulary_progress"]["words"])
    user["phrases_learned"] = len(user["vocabulary_progress"]["phrases"])
    return user["vocabulary_progress"]


def sync_vocab_counters(user: dict) -> None:
    ensure_vocab_progress(user)


def item_key(level: str, topic_id: str, en: str) -> str:
    return f"{level}:{topic_id}:{(en or '').strip().lower()}"


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


def finish_word_practice(user_id: str, level: str, topic_id: str, en: str) -> dict:
    """Засчитать слово + убрать из батча + вернуть hub к списку слов — одним сохранением."""
    key = item_key(level, topic_id, en)
    en_l = (en or "").strip().lower()

    def mut(u):
        ensure_lesson(u)
        ensure_vocab_progress(u)
        words = list(u["vocabulary_progress"]["words"])
        if key not in words:
            words.append(key)
        u["vocabulary_progress"]["words"] = words
        u["words_learned"] = len(words)

        batch = list(u["lesson"].get("vocab_batch") or [])
        batch = [w for w in batch if (w or "").strip().lower() != en_l]
        u["lesson"]["vocab_batch"] = batch
        u["lesson"]["hub"] = "vocab_topic"
        u["lesson"]["vocab_active_item"] = None
        u["lesson"]["vocab_practice_done"] = 0
        u["lesson"]["vocab_practice_step"] = 0
        u["lesson"]["vocab_last_sentence"] = ""
        u["lesson"]["vocab_used_sentences"] = []
        u["lesson"]["vocab_mode"] = "words"

    return update_lesson(user_id, mut)


def finish_phrase_practice(user_id: str, level: str, topic_id: str, en: str) -> dict:
    """Засчитать фразу + убрать из батча + вернуть к списку фраз."""
    key = item_key(level, topic_id, en)
    en_l = (en or "").strip().lower()

    def mut(u):
        ensure_lesson(u)
        ensure_vocab_progress(u)
        phrases = list(u["vocabulary_progress"]["phrases"])
        if key not in phrases:
            phrases.append(key)
        u["vocabulary_progress"]["phrases"] = phrases
        u["phrases_learned"] = len(phrases)

        batch = list(u["lesson"].get("vocab_batch") or [])
        batch = [p for p in batch if (p or "").strip().lower() != en_l]
        u["lesson"]["vocab_batch"] = batch
        u["lesson"]["hub"] = "vocab_phrases"
        u["lesson"]["vocab_active_item"] = None
        u["lesson"]["vocab_practice_done"] = 0
        u["lesson"]["vocab_practice_step"] = 0
        u["lesson"]["vocab_last_sentence"] = ""
        u["lesson"]["vocab_used_sentences"] = []
        u["lesson"]["vocab_mode"] = "phrases"

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
            "vocab_practice_done",
            "vocab_last_sentence",
            "vocab_text_en",
            "vocab_text_ru",
            "drill_kind",
            "drill_queue",
            "drill_index",
            "drill_dirs",
            "drill_current",
            "vocab_final",
        ):
            u["lesson"].pop(k, None)

    return update_lesson(user_id, mut)
