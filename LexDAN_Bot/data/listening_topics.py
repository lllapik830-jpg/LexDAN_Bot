"""Темы Listening по CEFR — до 10 ситуаций на уровень, разные роли."""

from __future__ import annotations

# roles: краткое описание пары говорящих для промпта
LISTENING_TOPICS: dict[str, list[dict]] = {
    "A0": [
        {"id": "hello", "title_ru": "Знакомство", "title_en": "Meeting someone", "roles": "Oliver and Mia", "setting": "park fountain, names, ages, glasses, coffee"},
        {"id": "numbers", "title_ru": "Числа и телефон", "title_en": "Numbers", "roles": "Ethan and Sophia", "setting": "phone numbers, brothers, ages, napkin"},
        {"id": "family", "title_ru": "Семья", "title_en": "Family", "roles": "Emma talking about family", "setting": "mum Mary, dad doctor, brother age 10, four people"},
        {"id": "colors", "title_ru": "Цвета", "title_en": "Colors", "roles": "Noah and Lily", "setting": "favourite colours, blue T-shirt, red pen, red bag"},
        {"id": "food_words", "title_ru": "Еда", "title_en": "Food words", "roles": "Liam and Chloe", "setting": "burger, salad, coffee, tip, extra sauce"},
        {"id": "classroom", "title_ru": "В классе", "title_en": "In class", "roles": "Jake and Zara", "setting": "maths, sport, 15 students, red dress, test, front row"},
        {"id": "pets", "title_ru": "Питомцы", "title_en": "Pets", "roles": "Zack and Mila", "setting": "dog and cat Bella, park, pet shop, noise"},
        {"id": "days", "title_ru": "Дни недели", "title_en": "Days", "roles": "Connor and Aurora", "setting": "Monday work, Wednesday study, Friday gym, Saturday cinema"},
        {"id": "weather_easy", "title_ru": "Погода просто", "title_en": "Simple weather", "roles": "Felix and Ella", "setting": "sunny 20 degrees, rainy tomorrow, Saturday colder"},
        {"id": "home", "title_ru": "Дом", "title_en": "Home", "roles": "Mason and Amelia", "setting": "room with TV, garden roses, dormitory, tea"},
    ],
    "A1": [
        {"id": "cafe_simple", "title_ru": "В кафе", "title_en": "At a café", "roles": "Jack and Emily", "setting": "coffee croissant tea toast, Jack pays"},
        {"id": "school", "title_ru": "Школа", "title_en": "School", "roles": "Sophie and Noah", "setting": "maths test, four lessons, art, history"},
        {"id": "hobbies", "title_ru": "Хобби", "title_en": "Hobbies", "roles": "Olivia and Mason", "setting": "guitar, fishing, reading, films"},
        {"id": "shopping_easy", "title_ru": "В магазине", "title_en": "Shopping", "roles": "Isabella and Luke", "setting": "pasta, tomatoes, spaghetti, white bread"},
        {"id": "daily", "title_ru": "Распорядок дня", "title_en": "Daily routine", "roles": "Chloe and Ethan", "setting": "wake up, lunch at 12, home, gym, films"},
        {"id": "bus", "title_ru": "На автобусе", "title_en": "On the bus", "roles": "Jake and Aurora", "setting": "three and five stops, reading, seats"},
        {"id": "library", "title_ru": "В библиотеке", "title_en": "Library", "roles": "Mila and Noah", "setting": "adventure novel, detective, two books, library card"},
        {"id": "park", "title_ru": "В парке", "title_en": "In the park", "roles": "Zara and Liam", "setting": "bench, dogs, café, coffee, tired"},
        {"id": "phone_easy", "title_ru": "Звонок другу", "title_en": "Phone call", "roles": "Ella and Oliver", "setting": "Saturday 6 pm, pizza, drinks"},
        {"id": "clinic", "title_ru": "В поликлинике", "title_en": "Clinic", "roles": "Sophia and Mason", "setting": "cold, medicine, headache, temperature"},
    ],
    "A2": [
        {"id": "cafe", "title_ru": "Кафе с другом", "title_en": "Café with a friend", "roles": "Mark and Lena", "setting": "cappuccino dessert black coffee sandwich Friday"},
        {"id": "station", "title_ru": "На вокзале", "title_en": "Train station", "roles": "Andrey and Katya", "setting": "platform 5, carriage 3, five minutes"},
        {"id": "doctor", "title_ru": "У врача", "title_en": "Doctor", "roles": "Natalia and Doctor Petrov", "setting": "viral infection, tablets 5 days, liquids"},
        {"id": "hotel", "title_ru": "В отеле", "title_en": "Hotel", "roles": "Oleg and Anna", "setting": "room 104, breakfast 7-10, free Wi-Fi, car park"},
        {"id": "police", "title_ru": "Полиция", "title_en": "Police", "roles": "Mike and Steve", "setting": "stolen bicycle, cameras, 555-9090"},
        {"id": "bar", "title_ru": "В баре", "title_en": "Bar", "roles": "Dan and Sergey", "setting": "light beer, nuts, live music"},
        {"id": "taxi", "title_ru": "Такси", "title_en": "Taxi", "roles": "Irina and Victor", "setting": "airport, 30 minutes, terminal, tip"},
        {"id": "post", "title_ru": "На почте", "title_en": "Post office", "roles": "Pavel and Maria", "setting": "2 kg parcel, 3-5 days, insurance"},
        {"id": "gym_a2", "title_ru": "Спортзал", "title_en": "Gym", "roles": "Ivan and Olga", "setting": "treadmill, three times a week, Monday"},
        {"id": "weather_plans", "title_ru": "Погода и планы", "title_en": "Weather plans", "roles": "Kristina and Denis", "setting": "rain tomorrow, picnic Saturday 10 am"},
    ],
    "B1": [
        {"id": "job_interview", "title_ru": "Собеседование", "title_en": "Job interview", "roles": "Mikhail and Anna", "setting": "marketing, two years, English, contact in a week"},
        {"id": "travel_plans", "title_ru": "Планы поездки", "title_en": "Travel plans", "roles": "Igor and Marina", "setting": "seaside, off-peak August, hotel, excursions"},
        {"id": "flatmates", "title_ru": "Соседи", "title_en": "Flatmates", "roles": "Dmitry and Olga", "setting": "new neighbours, noise, say hello, rules"},
        {"id": "restaurant", "title_ru": "Ресторан", "title_en": "Restaurant", "roles": "Andrey and Ekaterina", "setting": "signature dish, atmosphere, Andrey treats"},
        {"id": "bank", "title_ru": "В банке", "title_en": "Bank", "roles": "Pavel and Natalia", "setting": "savings account, passport, withdraw anytime"},
        {"id": "landlord_b1", "title_ru": "Аренда", "title_en": "Renting", "roles": "Ksenia and Sergey", "setting": "30000 rent, free parking, couple of days"},
        {"id": "airport_b1", "title_ru": "Аэропорт", "title_en": "Airport", "roles": "Irina and Artem", "setting": "flight 456 London, terminal 3, 20 minutes, 10 kg"},
        {"id": "salon", "title_ru": "Салон", "title_en": "Hair salon", "roles": "Kristina and Elena", "setting": "honey colour, 1.5 hours, Wednesday"},
        {"id": "news_chat", "title_ru": "Новости", "title_en": "News chat", "roles": "Sergey and Tatiana", "setting": "new metro station, next year, not too expensive"},
        {"id": "volunteer", "title_ru": "Волонтёры", "title_en": "Volunteering", "roles": "Alexey and Nadezhda", "setting": "children IT, training 18:00 city centre"},
    ],
    "B2": [
        {"id": "workplace", "title_ru": "На работе", "title_en": "Workplace", "roles": "Anton and Elena", "setting": "report, debit credit, coffee after work"},
        {"id": "university", "title_ru": "Университет", "title_en": "University", "roles": "Mikhail and Anastasia", "setting": "thesis topic, practical, end of month"},
        {"id": "customer", "title_ru": "Служба поддержки", "title_en": "Support", "roles": "Victor and Oksana", "setting": "slow internet, router, technician tomorrow"},
        {"id": "airport", "title_ru": "Пересадка", "title_en": "Missed connection", "roles": "Alex and flight attendant", "setting": "flight 224 Berlin, terminal C, 15 minutes"},
        {"id": "dating", "title_ru": "Свидание", "title_en": "Date", "roles": "Denis and Veronica", "setting": "river restaurant, travel, yoga"},
        {"id": "court_soft", "title_ru": "Консультация юриста", "title_en": "Legal advice", "roles": "Igor and Ekaterina", "setting": "overtime clause, unclear criteria"},
        {"id": "podcast_b2", "title_ru": "Подкаст", "title_en": "Podcast", "roles": "Dmitry and Anna", "setting": "business idea, six months, team"},
        {"id": "hospital", "title_ru": "Больница", "title_en": "Hospital", "roles": "Pavel and Maria", "setting": "tiredness, full check-up, next week"},
        {"id": "startup", "title_ru": "Стартап", "title_en": "Startup", "roles": "Pavel and Ksenia", "setting": "prototype, loading animation, meet tomorrow"},
        {"id": "immigration", "title_ru": "Миграционная служба", "title_en": "Immigration desk", "roles": "Maxim and Irina", "setting": "visa renewal, two weeks, 30 working days"},
    ],
    "C1": [
        {"id": "negotiation", "title_ru": "Переговоры", "title_en": "Negotiation", "roles": "two business partners", "setting": "contract terms, discount"},
        {"id": "conference", "title_ru": "Конференция", "title_en": "Conference", "roles": "speaker and attendee", "setting": "networking after a talk"},
        {"id": "healthcare", "title_ru": "Страховка", "title_en": "Insurance", "roles": "agent and client", "setting": "claim, coverage, paperwork"},
        {"id": "debate_soft", "title_ru": "Дискуссия", "title_en": "Debate", "roles": "two journalists", "setting": "social media and free time"},
        {"id": "hr", "title_ru": "HR-разговор", "title_en": "HR talk", "roles": "HR and employee", "setting": "promotion, performance"},
        {"id": "mediator", "title_ru": "Медиация", "title_en": "Mediation", "roles": "mediator and neighbour", "setting": "noise dispute"},
        {"id": "research", "title_ru": "Исследование", "title_en": "Research chat", "roles": "two researchers", "setting": "methodology, results"},
        {"id": "politics_soft", "title_ru": "Городская политика", "title_en": "City policy", "roles": "councillor and resident", "setting": "new bike lanes"},
        {"id": "culture_c1", "title_ru": "Культура", "title_en": "Culture", "roles": "curator and visitor", "setting": "exhibition themes"},
        {"id": "tech_support", "title_ru": "IT-поддержка", "title_en": "IT support", "roles": "engineer and user", "setting": "outage, workaround"},
    ],
    "C2": [
        {"id": "boardroom", "title_ru": "Совет директоров", "title_en": "Boardroom", "roles": "CEO and board member", "setting": "risk, strategy, PR"},
        {"id": "ethics", "title_ru": "Этика ИИ", "title_en": "AI ethics", "roles": "ethicist and engineer", "setting": "privacy, responsibility"},
        {"id": "diplomacy", "title_ru": "Дипломатия", "title_en": "Diplomacy", "roles": "two diplomats", "setting": "resolve a misunderstanding"},
        {"id": "critique", "title_ru": "Критика фильма", "title_en": "Film critique", "roles": "two critics", "setting": "themes, cinematography"},
        {"id": "academia", "title_ru": "Академия", "title_en": "Academia", "roles": "supervisor and PhD student", "setting": "thesis argument"},
        {"id": "court", "title_ru": "Судебные прения", "title_en": "Courtroom", "roles": "prosecutor and defence", "setting": "key evidence dispute"},
        {"id": "climate", "title_ru": "Климат", "title_en": "Climate panel", "roles": "scientist and policymaker", "setting": "targets, trade-offs"},
        {"id": "literature", "title_ru": "Литература", "title_en": "Literature salon", "roles": "author and interviewer", "setting": "style, influences"},
        {"id": "finance", "title_ru": "Финансы", "title_en": "Finance", "roles": "analyst and client", "setting": "portfolio risk"},
        {"id": "philosophy", "title_ru": "Философия", "title_en": "Philosophy", "roles": "two philosophers", "setting": "free will debate"},
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
