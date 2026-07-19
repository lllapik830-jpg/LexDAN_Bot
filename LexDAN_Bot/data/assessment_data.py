"""
Материалы для входного теста уровня.
Тексты: английский оригинал + эталонный русский перевод (не длиннее 4–5 предложений).
"""

LEVELS = ["A0", "A1", "A2", "B1", "B2", "C1", "C2"]

# Два варианта текста на каждый уровень (второй нужен на A0 перед «Пропустить»)
TRANSLATION_TEXTS = {
    "C2": [
        {
            "en": (
                "Despite mounting evidence to the contrary, many policymakers remain reluctant to revise long-standing strategies. "
                "Critics argue that such hesitation stems less from ignorance than from institutional inertia. "
                "Reformers, meanwhile, insist that incremental change is no longer sufficient. "
                "Ultimately, the debate reveals a deeper conflict between short-term political gains and long-term social responsibility."
            ),
            "ru": (
                "Несмотря на растущие доказательства обратного, многие политики по-прежнему не хотят пересматривать давние стратегии. "
                "Критики утверждают, что такая нерешительность связана не столько с незнанием, сколько с инерцией учреждений. "
                "Реформаторы же настаивают, что постепенных изменений уже недостаточно. "
                "В итоге спор показывает более глубокий конфликт между краткосрочной политической выгодой и долгосрочной социальной ответственностью."
            ),
        },
        {
            "en": (
                "The artist's latest exhibition invites viewers to question the boundary between memory and invention. "
                "Familiar objects appear slightly distorted, as if recalled through emotion rather than fact. "
                "Visitors often leave unsettled, yet oddly reflective. "
                "In this sense, the work succeeds not by offering answers, but by complicating certainty."
            ),
            "ru": (
                "Последняя выставка художника предлагает зрителям усомниться в границе между памятью и вымыслом. "
                "Привычные предметы кажутся слегка искажёнными — будто вспомненными через эмоцию, а не через факт. "
                "Посетители часто уходят растревоженными, но странно задумчивыми. "
                "В этом смысле работа удаётся не тем, что даёт ответы, а тем, что усложняет уверенность."
            ),
        },
    ],
    "C1": [
        {
            "en": (
                "Remote work has reshaped how teams communicate and measure productivity. "
                "Some employees appreciate the flexibility, while others miss the informal conversations of an office. "
                "Managers now face a challenge: how to build trust without constant supervision. "
                "Companies that adapt quickly tend to keep talent longer."
            ),
            "ru": (
                "Удалённая работа изменила то, как команды общаются и оценивают продуктивность. "
                "Кому-то нравится гибкость, а кому-то не хватает неформальных разговоров в офисе. "
                "Руководителям теперь нужно решать, как строить доверие без постоянного контроля. "
                "Компании, которые быстро адаптируются, чаще удерживают сотрудников."
            ),
        },
        {
            "en": (
                "Learning a language as an adult requires patience more than talent. "
                "Progress often feels slow until sudden breakthroughs appear. "
                "Regular speaking practice matters more than memorizing long word lists. "
                "Over time, small daily efforts create surprising results."
            ),
            "ru": (
                "Изучение языка во взрослом возрасте требует терпения больше, чем таланта. "
                "Прогресс часто кажется медленным, пока вдруг не случаются прорывы. "
                "Регулярная практика речи важнее заучивания длинных списков слов. "
                "Со временем небольшие ежедневные усилия дают удивительный результат."
            ),
        },
    ],
    "B2": [
        {
            "en": (
                "Many people start exercising in January and stop by March. "
                "The main reason is not laziness, but unrealistic goals. "
                "If you choose small habits, it is easier to continue. "
                "For example, a short walk every day can improve both health and mood."
            ),
            "ru": (
                "Многие начинают заниматься спортом в январе и бросают к марту. "
                "Главная причина — не лень, а нереалистичные цели. "
                "Если выбирать маленькие привычки, продолжать проще. "
                "Например, короткая прогулка каждый день может улучшить и здоровье, и настроение."
            ),
        },
        {
            "en": (
                "Online courses are popular because they save time and money. "
                "However, students need strong self-discipline to finish them. "
                "Without a clear schedule, it is easy to postpone lessons. "
                "That is why good planning often decides success."
            ),
            "ru": (
                "Онлайн-курсы популярны, потому что экономят время и деньги. "
                "Однако чтобы их закончить, нужна сильная самодисциплина. "
                "Без чёткого расписания занятия легко откладывать. "
                "Поэтому хороший план часто решает успех."
            ),
        },
    ],
    "B1": [
        {
            "en": (
                "Last weekend I visited my friend in another city. "
                "We walked in the park and talked about our plans. "
                "In the evening we cooked dinner together. "
                "It was a simple day, but I felt happy."
            ),
            "ru": (
                "В прошлые выходные я навестил друга в другом городе. "
                "Мы гуляли в парке и говорили о своих планах. "
                "Вечером мы вместе готовили ужин. "
                "День был простой, но я чувствовал себя счастливым."
            ),
        },
        {
            "en": (
                "My sister wants to learn how to drive. "
                "She takes lessons twice a week. "
                "At first she felt nervous, but now she is more confident. "
                "Soon she hopes to get her own car."
            ),
            "ru": (
                "Моя сестра хочет научиться водить. "
                "Она ходит на занятия два раза в неделю. "
                "Сначала она нервничала, а сейчас увереннее. "
                "Скоро она надеется получить свою машину."
            ),
        },
    ],
    "A2": [
        {
            "en": (
                "I usually wake up at seven. "
                "I drink tea and eat breakfast. "
                "Then I go to work by bus. "
                "In the evening I watch a film."
            ),
            "ru": (
                "Я обычно встаю в семь. "
                "Я пью чай и завтракаю. "
                "Потом я еду на работу на автобусе. "
                "Вечером я смотрю фильм."
            ),
        },
        {
            "en": (
                "Tom has a small dog. "
                "Every morning he takes it for a walk. "
                "The dog likes to play with a ball. "
                "Tom is very happy with his pet."
            ),
            "ru": (
                "У Тома маленькая собака. "
                "Каждое утро он выводит её на прогулку. "
                "Собака любит играть с мячом. "
                "Том очень рад своему питомцу."
            ),
        },
    ],
    "A1": [
        {
            "en": (
                "This is my room. "
                "There is a bed and a table. "
                "I like my room. "
                "It is quiet and clean."
            ),
            "ru": (
                "Это моя комната. "
                "Здесь есть кровать и стол. "
                "Мне нравится моя комната. "
                "Она тихая и чистая."
            ),
        },
        {
            "en": (
                "I have a brother. "
                "His name is Max. "
                "He is ten years old. "
                "We play games together."
            ),
            "ru": (
                "У меня есть брат. "
                "Его зовут Макс. "
                "Ему десять лет. "
                "Мы вместе играем в игры."
            ),
        },
    ],
    "A0": [
        {
            "en": (
                "I am Anna. "
                "I live in a city. "
                "I like tea. "
                "Good morning!"
            ),
            "ru": (
                "Я Анна. "
                "Я живу в городе. "
                "Я люблю чай. "
                "Доброе утро!"
            ),
        },
        {
            "en": (
                "This is a cat. "
                "The cat is small. "
                "I see a book. "
                "Thank you."
            ),
            "ru": (
                "Это кот. "
                "Кот маленький. "
                "Я вижу книгу. "
                "Спасибо."
            ),
        },
    ],
}

# Слова для задания 2: en -> возможные русские ответы (основной эталон первый)
VOCAB_BANK = {
    "C2": [
        {"en": "reluctant", "ru": ["нежелающий", "неохотный", "несклонный"]},
        {"en": "undermine", "ru": ["подрывать", "ослаблять"]},
        {"en": "nuance", "ru": ["нюанс", "оттенок"]},
        {"en": "coherence", "ru": ["согласованность", "связность", "целостность"]},
        {"en": "scrutinize", "ru": ["тщательно изучать", "пристально рассматривать"]},
        {"en": "ambiguous", "ru": ["неоднозначный", "двусмысленный"]},
    ],
    "C1": [
        {"en": "afford", "ru": ["позволять себе", "быть в состоянии"]},
        {"en": "assume", "ru": ["предполагать", "допускать"]},
        {"en": "benefit", "ru": ["польза", "выгода", "преимущество"]},
        {"en": "consequence", "ru": ["последствие"]},
        {"en": "efficient", "ru": ["эффективный"]},
        {"en": "maintain", "ru": ["поддерживать", "сохранять"]},
    ],
    "B2": [
        {"en": "improve", "ru": ["улучшать", "улучшить"]},
        {"en": "decide", "ru": ["решать", "решить"]},
        {"en": "prefer", "ru": ["предпочитать"]},
        {"en": "suggest", "ru": ["предлагать", "советовать"]},
        {"en": "available", "ru": ["доступный", "имеющийся"]},
        {"en": "experience", "ru": ["опыт", "переживание"]},
    ],
    "B1": [
        {"en": "travel", "ru": ["путешествовать", "поездка", "путешествие"]},
        {"en": "busy", "ru": ["занятый"]},
        {"en": "weather", "ru": ["погода"]},
        {"en": "hungry", "ru": ["голодный"]},
        {"en": "invite", "ru": ["приглашать", "пригласить"]},
        {"en": "problem", "ru": ["проблема", "задача"]},
    ],
    "A2": [
        {"en": "school", "ru": ["школа"]},
        {"en": "family", "ru": ["семья"]},
        {"en": "morning", "ru": ["утро"]},
        {"en": "friend", "ru": ["друг", "подруга"]},
        {"en": "water", "ru": ["вода"]},
        {"en": "happy", "ru": ["счастливый", "радостный"]},
    ],
    "A1": [
        {"en": "cat", "ru": ["кот", "кошка"]},
        {"en": "house", "ru": ["дом"]},
        {"en": "book", "ru": ["книга"]},
        {"en": "milk", "ru": ["молоко"]},
        {"en": "yes", "ru": ["да"]},
        {"en": "name", "ru": ["имя", "название"]},
    ],
    "A0": [
        {"en": "I", "ru": ["я"]},
        {"en": "you", "ru": ["ты", "вы"]},
        {"en": "hello", "ru": ["привет", "здравствуйте", "здравствуй"]},
        {"en": "dog", "ru": ["собака", "пёс", "пес"]},
        {"en": "big", "ru": ["большой"]},
        {"en": "red", "ru": ["красный"]},
    ],
}

# Фразы для аудирования (короткие, до ~10 секунд речи)
LISTEN_BANK = {
    "C2": [
        "Although the proposal seemed reasonable at first, several committee members raised concerns about long-term funding.",
        "She argued that genuine innovation requires both creativity and the discipline to test ideas carefully.",
        "In retrospect, the project's delays were caused more by unclear priorities than by a lack of resources.",
    ],
    "C1": [
        "Many students struggle with speaking because they fear making mistakes in public.",
        "If companies invest in training, employees usually feel more motivated and confident.",
        "The article explains why small daily habits can change your health over time.",
    ],
    "B2": [
        "I would like to visit London next summer if I can save enough money.",
        "Please call me when you arrive at the station this evening.",
        "Learning English becomes easier when you practice a little every day.",
    ],
    "B1": [
        "My brother works in a shop near our house.",
        "We are going to the cinema on Saturday.",
        "Can you help me with my homework tonight?",
    ],
    "A2": [
        "I drink coffee every morning.",
        "She has two brothers and one sister.",
        "The weather is cold today.",
    ],
    "A1": [
        "I like apples.",
        "This is my bag.",
        "He is my friend.",
    ],
    "A0": [
        "I am fine.",
        "Good morning.",
        "This is a book.",
    ],
}

WRITE_TOPICS = {
    "C2": "Write about a social issue in your country and propose a realistic solution.",
    "C1": "Describe a difficult decision you made and explain what you learned from it.",
    "B2": "Write about your plans for the next five years and why they matter to you.",
    "B1": "Describe your typical weekend and what you enjoy most.",
    "A2": "Write about your family and your daily routine.",
    "A1": "Write about your home and your favourite food.",
    "A0": "Write simple sentences about yourself: name, city, likes.",
}


def level_index(level: str) -> int:
    try:
        return LEVELS.index(level)
    except ValueError:
        return LEVELS.index("A1")


def lower_level(level: str) -> str:
    i = level_index(level)
    return LEVELS[max(0, i - 1)]


def max_accessible_level(user_level: str) -> str:
    """
    Потолок только по калибровке: свой уровень и всё ниже (без +1).
    Для прогресса через Grammar используй user_level_ceiling(user).
    """
    if user_level not in LEVELS:
        return "A1"
    return user_level


def user_level_ceiling(user: dict | None) -> str:
    """Максимальный открытый уровень: калибровка + прогресс Grammar-тестов."""
    if not user:
        return "A1"
    if user.get("dev_unlock"):
        return "C2"
    base = user.get("level") or "A1"
    if base not in LEVELS:
        base = "A1"
    extra = user.get("grammar_unlock_ceiling") or base
    if extra not in LEVELS:
        extra = base
    return extra if level_index(extra) >= level_index(base) else base


def is_level_accessible(user_level: str, selected: str) -> bool:
    """Совместимость: сравнение с калибровочным уровнем (без grammar unlock)."""
    return level_index(selected) <= level_index(max_accessible_level(user_level))


def is_level_accessible_for_user(user: dict | None, selected: str) -> bool:
    if user and user.get("dev_unlock"):
        return True
    return level_index(selected) <= level_index(user_level_ceiling(user))


def raise_level(level: str) -> str:
    i = level_index(level)
    return LEVELS[min(len(LEVELS) - 1, i + 1)]


def unlock_next_level_after_grammar(user: dict, passed_level: str) -> str | None:
    """
    После сдачи Grammar-теста на passed_level открыть ровно следующий.
    Возвращает открытый уровень или None, если уже был открыт / C2.
    """
    if passed_level not in LEVELS:
        return None
    nxt = raise_level(passed_level)
    if nxt == passed_level:
        return None  # уже C2
    cur = user_level_ceiling(user)
    if level_index(nxt) <= level_index(cur):
        return None
    user["grammar_unlock_ceiling"] = nxt
    return nxt


def get_translation(level: str, variant: int = 0) -> dict:
    items = TRANSLATION_TEXTS.get(level) or TRANSLATION_TEXTS["A1"]
    return items[variant % len(items)]


def pick_vocab(level: str, used_ens: list[str] | None = None) -> dict:
    import random

    used = set(used_ens or [])
    bank = list(VOCAB_BANK.get(level) or VOCAB_BANK["A1"])
    unused = [w for w in bank if w["en"] not in used]
    choice = random.choice(unused or bank)
    return choice


def pick_listen(level: str, used: list[str] | None = None) -> str:
    import random

    used_set = set(used or [])
    bank = list(LISTEN_BANK.get(level) or LISTEN_BANK["A1"])
    unused = [x for x in bank if x not in used_set]
    return random.choice(unused or bank)


def pick_topic(level: str) -> str:
    return WRITE_TOPICS.get(level) or WRITE_TOPICS["A1"]
