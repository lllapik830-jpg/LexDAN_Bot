"""Темы Reading по CEFR — ~8 тем на уровень."""

from __future__ import annotations

READING_TOPICS: dict[str, list[dict]] = {
    "A0": [
        {"id": "family", "title_ru": "Семья", "title_en": "Family", "focus": "mum, dad, brother, sister, names"},
        {"id": "colors", "title_ru": "Цвета", "title_en": "Colors", "focus": "red, blue, green, bag, T-shirt"},
        {"id": "food", "title_ru": "Еда", "title_en": "Food", "focus": "apple, water, bread, tea, like"},
        {"id": "pets", "title_ru": "Питомцы", "title_en": "Pets", "focus": "cat, dog, name, play"},
        {"id": "home", "title_ru": "Дом", "title_en": "Home", "focus": "room, kitchen, door, window"},
        {"id": "school", "title_ru": "Школа", "title_en": "School", "focus": "pen, book, teacher, class"},
        {"id": "days", "title_ru": "Дни недели", "title_en": "Days", "focus": "Monday, today, tomorrow"},
        {"id": "hello", "title_ru": "Знакомство", "title_en": "Meeting people", "focus": "name, hello, nice to meet you"},
    ],
    "A1": [
        {"id": "family_a1", "title_ru": "Семья", "title_en": "My family", "focus": "family members, ages, jobs"},
        {"id": "cafe", "title_ru": "В кафе", "title_en": "At a café", "focus": "order, coffee, cake, friends"},
        {"id": "daily", "title_ru": "Распорядок дня", "title_en": "Daily routine", "focus": "wake up, breakfast, work, evening"},
        {"id": "hobbies", "title_ru": "Хобби", "title_en": "Hobbies", "focus": "sport, music, films, free time"},
        {"id": "shopping", "title_ru": "Магазин", "title_en": "Shopping", "focus": "price, size, clothes, pay"},
        {"id": "weekend", "title_ru": "Выходные", "title_en": "Weekend plans", "focus": "cinema, park, meet friends"},
        {"id": "school_day", "title_ru": "Школьный день", "title_en": "A school day", "focus": "lessons, homework, break"},
        {"id": "weather", "title_ru": "Погода", "title_en": "Weather", "focus": "sunny, rainy, cold, clothes"},
    ],
    "A2": [
        {"id": "travel", "title_ru": "Поездка", "title_en": "A short trip", "focus": "train, ticket, hotel, sightseeing"},
        {"id": "doctor", "title_ru": "У врача", "title_en": "At the doctor", "focus": "symptoms, medicine, rest"},
        {"id": "party", "title_ru": "Вечеринка", "title_en": "A birthday party", "focus": "guests, gifts, food, music"},
        {"id": "sport", "title_ru": "Спорт", "title_en": "Sport and health", "focus": "gym, run, tired, healthy"},
        {"id": "neighbours", "title_ru": "Соседи", "title_en": "Neighbours", "focus": "noise, help, flat, evening"},
        {"id": "lost", "title_ru": "Потерянная вещь", "title_en": "A lost bag", "focus": "describe, colour, find, thank"},
        {"id": "restaurant", "title_ru": "Ресторан", "title_en": "Restaurant", "focus": "menu, order, bill, tip"},
        {"id": "city", "title_ru": "Город", "title_en": "My city", "focus": "park, museum, bus, favourite place"},
    ],
    "B1": [
        {"id": "interview", "title_ru": "Собеседование", "title_en": "Job interview", "focus": "experience, hours, skills, start date"},
        {"id": "flatshare", "title_ru": "Совместная аренда", "title_en": "Sharing a flat", "focus": "chores, rent, rules, guests"},
        {"id": "online", "title_ru": "Онлайн-покупки", "title_en": "Online shopping", "focus": "delivery, return, review, discount"},
        {"id": "volunteer", "title_ru": "Волонтёрство", "title_en": "Volunteering", "focus": "weekend, help, team, local event"},
        {"id": "exam", "title_ru": "Экзамен", "title_en": "Preparing for an exam", "focus": "study plan, stress, library, results"},
        {"id": "move", "title_ru": "Переезд", "title_en": "Moving house", "focus": "boxes, neighbours, new area, rent"},
        {"id": "travel_b1", "title_ru": "Путешествие", "title_en": "Travel story", "focus": "flight, delay, hotel, advice"},
        {"id": "hobby_club", "title_ru": "Клуб по интересам", "title_en": "A hobby club", "focus": "members, meeting, project, join"},
    ],
    "B2": [
        {"id": "business", "title_ru": "Бизнес", "title_en": "Business meeting", "focus": "deadline, remote work, clients, proposal"},
        {"id": "startup", "title_ru": "Стартап", "title_en": "Startup idea", "focus": "product, users, funding, pitch"},
        {"id": "remote", "title_ru": "Удалёнка", "title_en": "Working from home", "focus": "focus, meetings, balance, office days"},
        {"id": "news", "title_ru": "Городские новости", "title_en": "Local news", "focus": "project, opinion, impact, citizens"},
        {"id": "uni", "title_ru": "Университет", "title_en": "University life", "focus": "essay, deadline, sources, feedback"},
        {"id": "customer", "title_ru": "Клиентский сервис", "title_en": "Customer support", "focus": "complaint, refund, apology, solution"},
        {"id": "health", "title_ru": "ЗОЖ", "title_en": "Healthy lifestyle", "focus": "habits, sleep, diet, motivation"},
        {"id": "culture", "title_ru": "Культура", "title_en": "A cultural event", "focus": "exhibition, tickets, review, atmosphere"},
    ],
    "C1": [
        {"id": "negotiation", "title_ru": "Переговоры", "title_en": "Negotiation", "focus": "terms, compromise, contract, leverage"},
        {"id": "media", "title_ru": "Медиа", "title_en": "Media and attention", "focus": "headline, bias, sources, audience"},
        {"id": "climate", "title_ru": "Климат", "title_en": "Climate action locally", "focus": "policy, costs, community, trade-offs"},
        {"id": "hr", "title_ru": "HR", "title_en": "HR feedback", "focus": "performance, promotion, goals, soft skills"},
        {"id": "research", "title_ru": "Исследование", "title_en": "A research summary", "focus": "method, findings, limits, next steps"},
        {"id": "ethics", "title_ru": "Этика технологий", "title_en": "Tech ethics", "focus": "privacy, AI, regulation, users"},
        {"id": "city_plan", "title_ru": "Градостроительство", "title_en": "City planning", "focus": "transport, housing, debate, budget"},
        {"id": "leadership", "title_ru": "Лидерство", "title_en": "Leadership challenge", "focus": "team, conflict, decision, outcome"},
    ],
    "C2": [
        {"id": "board", "title_ru": "Совет директоров", "title_en": "Boardroom debate", "focus": "risk, strategy, PR, long-term value"},
        {"id": "policy", "title_ru": "Политика", "title_en": "Public policy brief", "focus": "stakeholders, incentives, unintended effects"},
        {"id": "lit", "title_ru": "Литература", "title_en": "A short literary review", "focus": "theme, tone, symbolism, critique"},
        {"id": "finance", "title_ru": "Финансы", "title_en": "Market commentary", "focus": "volatility, rates, outlook, caution"},
        {"id": "diplomacy", "title_ru": "Дипломатия", "title_en": "Diplomatic note", "focus": "talks, wording, interests, compromise"},
        {"id": "science", "title_ru": "Наука", "title_en": "Science communication", "focus": "evidence, uncertainty, public trust"},
        {"id": "art", "title_ru": "Искусство", "title_en": "Contemporary art essay", "focus": "interpretation, context, controversy"},
        {"id": "philosophy", "title_ru": "Философия выбора", "title_en": "A moral dilemma", "focus": "principles, consequences, judgment"},
    ],
}


def topics_for_level(level: str) -> list[dict]:
    return list(READING_TOPICS.get((level or "A1").upper(), READING_TOPICS["A1"]))


def get_topic(level: str, topic_id: str) -> dict | None:
    for t in topics_for_level(level):
        if t["id"] == topic_id:
            return t
    return None


def topic_by_button_label(level: str, label: str) -> dict | None:
    raw = (label or "").strip()
    if raw.endswith("✅"):
        raw = raw[:-1].strip()
    if ". " in raw[:5]:
        try:
            idx = int(raw.split(".", 1)[0].strip()) - 1
            topics = topics_for_level(level)
            if 0 <= idx < len(topics):
                return topics[idx]
        except ValueError:
            pass
    for t in topics_for_level(level):
        if t["title_ru"] == raw or t["title_en"] == raw:
            return t
    return None
