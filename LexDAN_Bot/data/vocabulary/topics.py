"""
Темы Vocabulary по уровням CEFR.
"""

VOCAB_TOPICS: dict[str, list[dict]] = {
    "A0": [
        {"id": "greetings", "title": "Приветствия / Greetings"},
        {"id": "family", "title": "Семья / Family"},
        {"id": "home", "title": "Дом / Home"},
        {"id": "food", "title": "Еда / Food"},
        {"id": "basics", "title": "Базовые слова / Basics"},
    ],
    "A1": [
        {"id": "family", "title": "Семья / Family"},
        {"id": "home", "title": "Дом / Home"},
        {"id": "work", "title": "Работа и учёба / Work & School"},
        {"id": "food", "title": "Еда / Food"},
        {"id": "travel", "title": "Путешествия / Travel"},
        {"id": "body", "title": "Тело / Body"},
        {"id": "daily", "title": "Будни / Daily life"},
        {"id": "hobbies", "title": "Хобби / Hobbies"},
    ],
    "A2": [
        {"id": "family", "title": "Семья / Family"},
        {"id": "home", "title": "Дом / Home"},
        {"id": "work", "title": "Работа / Work"},
        {"id": "health", "title": "Здоровье / Health"},
        {"id": "shopping", "title": "Покупки / Shopping"},
        {"id": "city", "title": "Город / City"},
        {"id": "nature", "title": "Природа / Nature"},
        {"id": "communication", "title": "Общение / Communication"},
    ],
    "B1": [
        {"id": "family", "title": "Семья / Family"},
        {"id": "career", "title": "Карьера / Career"},
        {"id": "home", "title": "Дом / Home"},
        {"id": "media", "title": "Медиа / Media"},
        {"id": "society", "title": "Общество / Society"},
        {"id": "environment", "title": "Экология / Environment"},
        {"id": "emotions", "title": "Эмоции / Emotions"},
    ],
    "B2": [
        {"id": "work", "title": "Работа / Work"},
        {"id": "education", "title": "Образование / Education"},
        {"id": "technology", "title": "Технологии / Technology"},
        {"id": "culture", "title": "Культура / Culture"},
        {"id": "law", "title": "Право / Law & Rules"},
        {"id": "science", "title": "Наука / Science"},
    ],
    "C1": [
        {"id": "business", "title": "Бизнес / Business"},
        {"id": "politics", "title": "Политика / Politics"},
        {"id": "psychology", "title": "Психология / Psychology"},
        {"id": "art", "title": "Искусство / Art"},
        {"id": "global", "title": "Мир / Global issues"},
    ],
    "C2": [
        {"id": "academic", "title": "Академический / Academic"},
        {"id": "literature", "title": "Литература / Literature"},
        {"id": "philosophy", "title": "Философия / Philosophy"},
        {"id": "specialized", "title": "Специализированный / Specialized"},
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
