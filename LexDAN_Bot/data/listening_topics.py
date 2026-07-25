"""Темы Listening по CEFR — типичные ситуации уровня."""

from __future__ import annotations

LISTENING_TOPICS: dict[str, list[dict]] = {
    "A0": [
        {"id": "hello", "title_ru": "Знакомство", "title_en": "Meeting someone", "setting": "two people meet and say hello"},
        {"id": "numbers", "title_ru": "Числа и возраст", "title_en": "Numbers and age", "setting": "friends talk about age and phone numbers"},
        {"id": "family", "title_ru": "Семья", "title_en": "Family", "setting": "simple talk about mum, dad, brother, sister"},
        {"id": "colors", "title_ru": "Цвета и вещи", "title_en": "Colors and things", "setting": "choosing a bag, phone or T-shirt by color"},
    ],
    "A1": [
        {"id": "cafe_simple", "title_ru": "В кафе", "title_en": "At a café", "setting": "ordering coffee and a snack"},
        {"id": "school", "title_ru": "Школа / учёба", "title_en": "School day", "setting": "talking about classes and homework"},
        {"id": "hobbies", "title_ru": "Хобби", "title_en": "Hobbies", "setting": "weekend hobbies: sport, music, films"},
        {"id": "shopping_easy", "title_ru": "В магазине", "title_en": "Shopping", "setting": "buying fruit or clothes, asking the price"},
        {"id": "daily", "title_ru": "Распорядок дня", "title_en": "Daily routine", "setting": "morning routine: wake up, breakfast, work"},
    ],
    "A2": [
        {"id": "cafe", "title_ru": "В кафе с другом", "title_en": "Café with a friend", "setting": "friends meet in a café, order food and drinks, talk about evening plans"},
        {"id": "station", "title_ru": "На вокзале", "title_en": "At the station", "setting": "buying tickets, finding the platform, train delay"},
        {"id": "doctor", "title_ru": "У врача", "title_en": "At the doctor's", "setting": "describing symptoms, appointment time, medicine"},
        {"id": "hotel", "title_ru": "В отеле", "title_en": "At a hotel", "setting": "check-in, room number, breakfast time"},
        {"id": "phone", "title_ru": "Разговор по телефону", "title_en": "Phone call", "setting": "calling a friend to change meeting time"},
        {"id": "weather", "title_ru": "Погода и планы", "title_en": "Weather plans", "setting": "weekend plans depending on weather"},
    ],
    "B1": [
        {"id": "job_interview", "title_ru": "Собеседование", "title_en": "Job interview", "setting": "short informal chat before/after a job interview"},
        {"id": "travel_plans", "title_ru": "Планы поездки", "title_en": "Travel plans", "setting": "friends planning a weekend trip: transport, hotel, budget"},
        {"id": "flatmates", "title_ru": "Соседи по квартире", "title_en": "Flatmates", "setting": "discussing chores, noise, and guests"},
        {"id": "restaurant", "title_ru": "В ресторане", "title_en": "At a restaurant", "setting": "ordering a meal, complaining politely, paying the bill"},
        {"id": "gym", "title_ru": "В спортзале", "title_en": "At the gym", "setting": "membership, training schedule, feeling tired"},
        {"id": "news_chat", "title_ru": "Новости дня", "title_en": "Everyday news chat", "setting": "friends react to a local news story"},
    ],
    "B2": [
        {"id": "workplace", "title_ru": "На работе", "title_en": "At work", "setting": "colleagues discuss a project deadline and remote work"},
        {"id": "university", "title_ru": "В университете", "title_en": "At university", "setting": "students talk about exams, essays and group work"},
        {"id": "landlord", "title_ru": "С арендодателем", "title_en": "With a landlord", "setting": "reporting a problem in a rented flat"},
        {"id": "airport", "title_ru": "В аэропорту", "title_en": "At the airport", "setting": "missed connection, rebooking, baggage"},
        {"id": "dating", "title_ru": "На свидании", "title_en": "On a date", "setting": "first date conversation: work, hobbies, future plans"},
        {"id": "customer", "title_ru": "Жалоба клиенту", "title_en": "Customer service", "setting": "calling support about a wrong delivery"},
    ],
    "C1": [
        {"id": "negotiation", "title_ru": "Переговоры", "title_en": "Negotiation", "setting": "business partners negotiate a contract detail"},
        {"id": "podcast", "title_ru": "Подкаст о городе", "title_en": "City life podcast", "setting": "two hosts discuss housing prices and nightlife"},
        {"id": "debate_soft", "title_ru": "Мягкий спор", "title_en": "Friendly debate", "setting": "friends disagree about social media and free time"},
        {"id": "conference", "title_ru": "На конференции", "title_en": "At a conference", "setting": "networking: exchanging ideas after a talk"},
        {"id": "healthcare", "title_ru": "Страховка и здоровье", "title_en": "Insurance call", "setting": "explaining a claim to an insurance agent"},
    ],
    "C2": [
        {"id": "boardroom", "title_ru": "Совет директоров", "title_en": "Boardroom chat", "setting": "executives discuss risk, strategy and PR"},
        {"id": "culture", "title_ru": "Культура и идентичность", "title_en": "Culture talk", "setting": "nuanced talk about belonging and language"},
        {"id": "ethics", "title_ru": "Этика технологий", "title_en": "Tech ethics", "setting": "debate on AI, privacy and responsibility"},
        {"id": "diplomacy", "title_ru": "Дипломатичный разговор", "title_en": "Diplomatic talk", "setting": "carefully resolving a misunderstanding between partners"},
        {"id": "critique", "title_ru": "Разбор фильма", "title_en": "Film critique", "setting": "two critics discuss themes and cinematography"},
    ],
}


def topics_for_level(level: str) -> list[dict]:
    lvl = (level or "A1").upper()
    if lvl not in LISTENING_TOPICS:
        lvl = "A1"
    return list(LISTENING_TOPICS[lvl])


def get_topic(level: str, topic_id: str) -> dict | None:
    for t in topics_for_level(level):
        if t["id"] == topic_id:
            return t
    return None


def topic_by_button_label(level: str, label: str) -> dict | None:
    """Кнопка: '1. Кафе ✅' или '1. Кафе'."""
    raw = (label or "").strip()
    if raw.endswith("✅"):
        raw = raw[:-1].strip()
    # "1. Title"
    if ". " in raw[:4]:
        try:
            idx = int(raw.split(".", 1)[0].strip()) - 1
            topics = topics_for_level(level)
            if 0 <= idx < len(topics):
                return topics[idx]
        except ValueError:
            pass
    title = raw
    for t in topics_for_level(level):
        if t["title_ru"] == title or t["title_en"] == title:
            return t
    return None
