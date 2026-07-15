"""
Темы Vocabulary по уровням CEFR.
Слова и фразы хранятся отдельно: vocabulary_words, vocabulary_phrases.
"""

from __future__ import annotations

VOCAB_TOPICS: dict[str, list[dict]] = {
    "A0": [
        {"id": "greetings", "title": "Greetings / Приветствия"},
        {"id": "family", "title": "Family / Семья"},
        {"id": "home", "title": "Home / Дом"},
        {"id": "food", "title": "Food / Еда"},
        {"id": "colors_numbers", "title": "Colors & numbers / Цвета и цифры"},
    ],
    "A1": [
        {"id": "family", "title": "Family / Семья"},
        {"id": "home", "title": "Home / Дом"},
        {"id": "work_school", "title": "Work & school / Работа и учёба"},
        {"id": "food", "title": "Food / Еда"},
        {"id": "travel", "title": "Travel / Путешествия"},
        {"id": "body_health", "title": "Body & health / Тело и здоровье"},
        {"id": "hobbies", "title": "Hobbies / Хобби"},
        {"id": "shopping", "title": "Shopping / Покупки"},
    ],
    "A2": [
        {"id": "family", "title": "Family / Семья"},
        {"id": "home", "title": "Home / Дом"},
        {"id": "work", "title": "Work / Работа"},
        {"id": "city", "title": "City / Город"},
        {"id": "travel", "title": "Travel / Путешествия"},
        {"id": "health", "title": "Health / Здоровье"},
        {"id": "technology", "title": "Technology / Технологии"},
        {"id": "nature", "title": "Nature / Природа"},
    ],
    "B1": [
        {"id": "family_relations", "title": "Family & relations / Семья и отношения"},
        {"id": "career", "title": "Career / Карьера"},
        {"id": "education", "title": "Education / Образование"},
        {"id": "media", "title": "Media / СМИ"},
        {"id": "environment", "title": "Environment / Экология"},
        {"id": "culture", "title": "Culture / Культура"},
        {"id": "emotions", "title": "Emotions / Эмоции"},
        {"id": "communication", "title": "Communication / Общение"},
    ],
    "B2": [
        {"id": "society", "title": "Society / Общество"},
        {"id": "business", "title": "Business / Бизнес"},
        {"id": "science", "title": "Science / Наука"},
        {"id": "law", "title": "Law / Право"},
        {"id": "psychology", "title": "Psychology / Психология"},
        {"id": "arts", "title": "Arts / Искусство"},
        {"id": "global_issues", "title": "Global issues / Мировые проблемы"},
        {"id": "lifestyle", "title": "Lifestyle / Образ жизни"},
    ],
    "C1": [
        {"id": "academic", "title": "Academic / Академический"},
        {"id": "professional", "title": "Professional / Профессиональный"},
        {"id": "politics", "title": "Politics / Политика"},
        {"id": "economics", "title": "Economics / Экономика"},
        {"id": "philosophy", "title": "Philosophy / Философия"},
        {"id": "literature", "title": "Literature / Литература"},
        {"id": "debate", "title": "Debate / Дискуссия"},
        {"id": "innovation", "title": "Innovation / Инновации"},
    ],
    "C2": [
        {"id": "nuance", "title": "Nuanced vocabulary / Нюансы"},
        {"id": "rhetoric", "title": "Rhetoric / Риторика"},
        {"id": "specialized", "title": "Specialized terms / Спецтермины"},
        {"id": "idioms_advanced", "title": "Advanced idioms / Идиомы"},
        {"id": "register", "title": "Register / Регистры речи"},
        {"id": "collocations", "title": "Collocations / Коллокации"},
        {"id": "abstract", "title": "Abstract concepts / Абстракции"},
        {"id": "mastery", "title": "Mastery lexis / Лексика мастерства"},
    ],
}


def get_vocab_topics(level: str) -> list[dict]:
    return list(VOCAB_TOPICS.get(level, VOCAB_TOPICS["A1"]))


def get_vocab_topic(level: str, topic_id: str) -> dict | None:
    for t in get_vocab_topics(level):
        if t["id"] == topic_id:
            return t
    return None


def get_vocab_topic_by_index(level: str, index_1based: int) -> dict | None:
    topics = get_vocab_topics(level)
    if index_1based < 1 or index_1based > len(topics):
        return None
    return topics[index_1based - 1]


def format_vocab_topics_list(
    level: str,
    progress_fn,
) -> str:
    """progress_fn(level, topic_id) -> (learned: int, total: int, done: bool)"""
    topics = get_vocab_topics(level)
    lines = [f"📗 <b>Vocabulary · уровень {level}</b>\n", "Выбери тему:\n"]
    for i, t in enumerate(topics, start=1):
        learned, total, done = progress_fn(level, t["id"])
        mark = "✅ " if done else ""
        counter = f" ({learned}/{total})" if total else ""
        lines.append(f"<b>{i}.</b> {mark}{t['title']}{counter}")
    lines.append(
        "\n🦜 В каждой теме — текст со словами, карточки Рико и практика.\n"
        "Есть отдельно <b>устойчивые фразы</b>."
    )
    return "\n".join(lines)
