# -*- coding: utf-8 -*-
"""
LexDAN course placement bank (CEFR A0–B2).

Original items for grammar, vocab, reading, listening, writing, speaking.
Not a copy of Cambridge CEPT or any commercial test.
"""

from __future__ import annotations

LEVEL_ORDER = ["A0", "A1", "A2", "B1", "B2"]

# ─── Grammar (40): easiest → hardest, ~8 per band ─────────────

GRAMMAR: list[dict] = [
    # ── A0 ──
    {
        "id": "g01",
        "level": "A0",
        "topic": "be",
        "subtype": "mcq",
        "prompt": "Choose the correct form:\nI ___ a student.",
        "options": ["am", "is", "are", "be"],
        "correct": 0,
    },
    {
        "id": "g02",
        "level": "A0",
        "topic": "be",
        "subtype": "gap_choice",
        "prompt": "Fill the gap:\nShe ___ my sister.",
        "options": ["is", "am", "are", "be"],
        "correct": 0,
    },
    {
        "id": "g03",
        "level": "A0",
        "topic": "articles",
        "subtype": "mcq",
        "prompt": "Choose the correct article:\nThis is ___ apple.",
        "options": ["an", "a", "the", "—"],
        "correct": 0,
    },
    {
        "id": "g04",
        "level": "A0",
        "topic": "plurals",
        "subtype": "word_form",
        "prompt": "Write the plural:\nI have two ____ (book).",
        "answer": "books",
        "accept": ["books"],
    },
    {
        "id": "g05",
        "level": "A0",
        "topic": "there_is",
        "subtype": "mcq",
        "prompt": "Choose the correct form:\n___ a cat on the sofa.",
        "options": ["There is", "There are", "There be", "It is"],
        "correct": 0,
    },
    {
        "id": "g06",
        "level": "A0",
        "topic": "possessives",
        "subtype": "gap_choice",
        "prompt": "Fill the gap:\nThis is ___ bag. (I)",
        "options": ["my", "me", "mine", "I"],
        "correct": 0,
    },
    {
        "id": "g07",
        "level": "A0",
        "topic": "be",
        "subtype": "order",
        "prompt": "Put the words in the correct order.",
        "words": ["are", "They", "happy", "."],
        "answer": "They are happy.",
        "accept": ["They are happy.", "They are happy"],
    },
    {
        "id": "g08",
        "level": "A0",
        "topic": "demonstratives",
        "subtype": "mcq",
        "prompt": "Choose the correct word (near you):\n___ is my phone.",
        "options": ["This", "That", "These", "Those"],
        "correct": 0,
    },
    # ── A1 ──
    {
        "id": "g09",
        "level": "A1",
        "topic": "present_simple",
        "subtype": "mcq",
        "prompt": "Choose the correct form:\nShe ___ in London.",
        "options": ["live", "lives", "living", "lived"],
        "correct": 1,
    },
    {
        "id": "g10",
        "level": "A1",
        "topic": "present_simple",
        "subtype": "gap_choice",
        "prompt": "Fill the gap:\nWe ___ coffee every morning.",
        "options": ["drink", "drinks", "drinking", "drank"],
        "correct": 0,
    },
    {
        "id": "g11",
        "level": "A1",
        "topic": "present_continuous",
        "subtype": "mcq",
        "prompt": "Choose the correct form:\nLook! He ___ right now.",
        "options": ["runs", "is running", "run", "running"],
        "correct": 1,
    },
    {
        "id": "g12",
        "level": "A1",
        "topic": "articles",
        "subtype": "gap_choice",
        "prompt": "Fill the gap:\nI need ___ umbrella. It's raining.",
        "options": ["an", "a", "the", "some"],
        "correct": 0,
    },
    {
        "id": "g13",
        "level": "A1",
        "topic": "there_is",
        "subtype": "mcq",
        "prompt": "Choose the correct form:\n___ three chairs in the room.",
        "options": ["There is", "There are", "There be", "It are"],
        "correct": 1,
    },
    {
        "id": "g14",
        "level": "A1",
        "topic": "past_simple",
        "subtype": "word_form",
        "prompt": "Write the past form:\nYesterday she ____ (go) to school.",
        "answer": "went",
        "accept": ["went"],
    },
    {
        "id": "g15",
        "level": "A1",
        "topic": "modals",
        "subtype": "mcq",
        "prompt": "Choose the correct modal (ability):\nI ___ swim, but I can't dive.",
        "options": ["can", "must", "should", "may"],
        "correct": 0,
    },
    {
        "id": "g16",
        "level": "A1",
        "topic": "present_simple",
        "subtype": "order",
        "prompt": "Put the words in the correct order.",
        "words": ["does", "Where", "she", "work", "?"],
        "answer": "Where does she work?",
        "accept": ["Where does she work?", "Where does she work"],
    },
    # ── A2 ──
    {
        "id": "g17",
        "level": "A2",
        "topic": "past_simple",
        "subtype": "mcq",
        "prompt": "Choose the correct form:\nThey ___ a film last night.",
        "options": ["watch", "watched", "watching", "watches"],
        "correct": 1,
    },
    {
        "id": "g18",
        "level": "A2",
        "topic": "future",
        "subtype": "gap_choice",
        "prompt": "Fill the gap (plan already decided):\nI ___ my friends tomorrow. We booked a table.",
        "options": ["am meeting", "meet", "will meeting", "meeting"],
        "correct": 0,
    },
    {
        "id": "g19",
        "level": "A2",
        "topic": "comparatives",
        "subtype": "word_form",
        "prompt": "Write the correct comparative:\nThis bag is ____ (cheap) than that one.",
        "answer": "cheaper",
        "accept": ["cheaper"],
    },
    {
        "id": "g20",
        "level": "A2",
        "topic": "quantifiers",
        "subtype": "mcq",
        "prompt": "Choose the correct quantifier:\nThere isn't ___ milk left.",
        "options": ["many", "much", "a few", "several"],
        "correct": 1,
    },
    {
        "id": "g21",
        "level": "A2",
        "topic": "present_perfect",
        "subtype": "gap_choice",
        "prompt": "Fill the gap:\nI ___ this film before.",
        "options": ["have seen", "saw", "see", "am seeing"],
        "correct": 0,
    },
    {
        "id": "g22",
        "level": "A2",
        "topic": "modals",
        "subtype": "mcq",
        "prompt": "Choose the best modal (advice):\nYou ___ drink more water.",
        "options": ["should", "must to", "can to", "would"],
        "correct": 0,
    },
    {
        "id": "g23",
        "level": "A2",
        "topic": "past_continuous",
        "subtype": "rewrite",
        "prompt": "Rewrite in past continuous (same meaning):\nShe was in the middle of cooking when I called.",
        "answer": "She was cooking when I called.",
        "accept": [
            "She was cooking when I called.",
            "She was cooking when I called",
            "When I called, she was cooking.",
            "When I called, she was cooking",
        ],
    },
    {
        "id": "g24",
        "level": "A2",
        "topic": "superlatives",
        "subtype": "word_form",
        "prompt": "Write the superlative:\nThis is the ____ (good) café in town.",
        "answer": "best",
        "accept": ["best"],
    },
    # ── B1 ──
    {
        "id": "g25",
        "level": "B1",
        "topic": "present_perfect",
        "subtype": "mcq",
        "prompt": "Choose the correct form:\nShe ___ here since 2019.",
        "options": ["lives", "has lived", "is living", "lived"],
        "correct": 1,
    },
    {
        "id": "g26",
        "level": "B1",
        "topic": "conditionals",
        "subtype": "gap_choice",
        "prompt": "Fill the gap (first conditional):\nIf it rains, we ___ at home.",
        "options": ["will stay", "stay", "stayed", "would stay"],
        "correct": 0,
    },
    {
        "id": "g27",
        "level": "B1",
        "topic": "passive",
        "subtype": "rewrite",
        "prompt": "Rewrite in the passive:\nSomeone stole my bike.",
        "answer": "My bike was stolen.",
        "accept": [
            "My bike was stolen.",
            "My bike was stolen",
            "My bike has been stolen.",
            "My bike has been stolen",
        ],
    },
    {
        "id": "g28",
        "level": "B1",
        "topic": "relative_clauses",
        "subtype": "mcq",
        "prompt": "Choose the correct relative pronoun:\nThe man ___ lives next door is a doctor.",
        "options": ["which", "who", "whose", "where"],
        "correct": 1,
    },
    {
        "id": "g29",
        "level": "B1",
        "topic": "gerund_infinitive",
        "subtype": "gap_choice",
        "prompt": "Fill the gap:\nI enjoy ___ early on Sundays.",
        "options": ["to wake", "waking", "wake", "woken"],
        "correct": 1,
    },
    {
        "id": "g30",
        "level": "B1",
        "topic": "reported_speech",
        "subtype": "rewrite",
        "prompt": "Rewrite in reported speech:\nShe said, \"I am tired.\"",
        "answer": "She said (that) she was tired.",
        "accept": [
            "She said (that) she was tired.",
            "She said that she was tired.",
            "She said she was tired.",
            "She said (that) she was tired",
            "She said that she was tired",
            "She said she was tired",
        ],
    },
    {
        "id": "g31",
        "level": "B1",
        "topic": "conditionals",
        "subtype": "mcq",
        "prompt": "Choose the correct second conditional:\nIf I ___ more time, I would travel more.",
        "options": ["have", "had", "would have", "will have"],
        "correct": 1,
    },
    {
        "id": "g32",
        "level": "B1",
        "topic": "used_to",
        "subtype": "word_form",
        "prompt": "Complete with the correct form of used to:\nHe ____ (live) in a small village, but now he lives in a city.",
        "answer": "used to live",
        "accept": ["used to live", "used to live"],
    },
    # ── B2 ──
    {
        "id": "g33",
        "level": "B2",
        "topic": "conditionals",
        "subtype": "mcq",
        "prompt": "Choose the correct third conditional:\nIf she had left earlier, she ___ the train.",
        "options": ["would catch", "would have caught", "caught", "will catch"],
        "correct": 1,
    },
    {
        "id": "g34",
        "level": "B2",
        "topic": "passive",
        "subtype": "rewrite",
        "prompt": "Rewrite in the passive (present perfect):\nThey have cancelled the meeting.",
        "answer": "The meeting has been cancelled.",
        "accept": [
            "The meeting has been cancelled.",
            "The meeting has been cancelled",
            "The meeting has been canceled.",
            "The meeting has been canceled",
        ],
    },
    {
        "id": "g35",
        "level": "B2",
        "topic": "relative_clauses",
        "subtype": "gap_choice",
        "prompt": "Fill the gap (non-defining):\nParis, ___ is the capital of France, attracts millions of tourists.",
        "options": ["that", "which", "who", "where"],
        "correct": 1,
    },
    {
        "id": "g36",
        "level": "B2",
        "topic": "reported_speech",
        "subtype": "mcq",
        "prompt": "Choose the correct reported question:\nHe asked me where ___.",
        "options": ["did I live", "I lived", "do I live", "I live"],
        "correct": 1,
    },
    {
        "id": "g37",
        "level": "B2",
        "topic": "gerund_infinitive",
        "subtype": "mcq",
        "prompt": "Choose the correct form:\nI stopped ___ sugar last year. (I quit the habit)",
        "options": ["to eat", "eating", "eat", "eaten"],
        "correct": 1,
    },
    {
        "id": "g38",
        "level": "B2",
        "topic": "modals",
        "subtype": "gap_choice",
        "prompt": "Fill the gap (deduction about the past):\nHe ___ left already — his coat is gone.",
        "options": ["must have", "must", "can't have", "should"],
        "correct": 0,
    },
    {
        "id": "g39",
        "level": "B2",
        "topic": "wish",
        "subtype": "rewrite",
        "prompt": "Rewrite using I wish (regret about the past):\nI didn't study harder.",
        "answer": "I wish I had studied harder.",
        "accept": [
            "I wish I had studied harder.",
            "I wish I had studied harder",
            "I wish I'd studied harder.",
            "I wish I'd studied harder",
        ],
    },
    {
        "id": "g40",
        "level": "B2",
        "topic": "cleft_sentences",
        "subtype": "order",
        "prompt": "Put the words in the correct order (cleft sentence).",
        "words": ["was", "the noise", "It", "that", "woke", "me", "up", "."],
        "answer": "It was the noise that woke me up.",
        "accept": [
            "It was the noise that woke me up.",
            "It was the noise that woke me up",
        ],
    },
]

# ─── Vocab (50): 25 en→ru + 25 ru→en, easier first ────────────

VOCAB: list[dict] = [
    # en_ru v01–v25
    {
        "id": "v01",
        "level": "A0",
        "topic": "daily",
        "direction": "en_ru",
        "prompt_en": "apple",
        "options_ru": ["яблоко", "яблоня", "абрикос", "апельсин"],
        "correct": 0,
    },
    {
        "id": "v02",
        "level": "A0",
        "topic": "family",
        "direction": "en_ru",
        "prompt_en": "mother",
        "options_ru": ["мать", "мачеха", "мамаша", "матрона"],
        "correct": 0,
    },
    {
        "id": "v03",
        "level": "A0",
        "topic": "colors",
        "direction": "en_ru",
        "prompt_en": "blue",
        "options_ru": ["синий", "сиреневый", "серый", "салатовый"],
        "correct": 0,
    },
    {
        "id": "v04",
        "level": "A0",
        "topic": "numbers",
        "direction": "en_ru",
        "prompt_en": "twelve",
        "options_ru": ["двенадцать", "двадцать", "два", "двадцать два"],
        "correct": 0,
    },
    {
        "id": "v05",
        "level": "A1",
        "topic": "food",
        "direction": "en_ru",
        "prompt_en": "bread",
        "options_ru": ["хлеб", "хлебница", "булка", "батон"],
        "correct": 0,
    },
    {
        "id": "v06",
        "level": "A1",
        "topic": "home",
        "direction": "en_ru",
        "prompt_en": "kitchen",
        "options_ru": ["кухня", "кухонный", "кухарка", "кладовая"],
        "correct": 0,
    },
    {
        "id": "v07",
        "level": "A1",
        "topic": "travel",
        "direction": "en_ru",
        "prompt_en": "ticket",
        "options_ru": ["билет", "билетаж", "посадочный", "проезд"],
        "correct": 0,
    },
    {
        "id": "v08",
        "level": "A1",
        "topic": "shopping",
        "direction": "en_ru",
        "prompt_en": "price",
        "options_ru": ["цена", "ценник", "ценность", "расценка"],
        "correct": 0,
    },
    {
        "id": "v09",
        "level": "A1",
        "topic": "weather",
        "direction": "en_ru",
        "prompt_en": "cloudy",
        "options_ru": ["облачный", "облако", "облачность", "пасмурный"],
        "correct": 0,
        "correct_any": [0, 3],
    },
    {
        "id": "v10",
        "level": "A1",
        "topic": "work",
        "direction": "en_ru",
        "prompt_en": "office",
        "options_ru": ["офис", "офицер", "кабинет", "приемная"],
        "correct": 0,
        "correct_any": [0, 2],
    },
    {
        "id": "v11",
        "level": "A2",
        "topic": "health",
        "direction": "en_ru",
        "prompt_en": "illness",
        "options_ru": ["болезнь", "больница", "больной", "боль"],
        "correct": 0,
    },
    {
        "id": "v12",
        "level": "A2",
        "topic": "education",
        "direction": "en_ru",
        "prompt_en": "homework",
        "options_ru": ["домашнее задание", "домашняя работа", "домашка", "задание"],
        "correct": 0,
        "correct_any": [0, 1, 2],
    },
    {
        "id": "v13",
        "level": "A2",
        "topic": "environment",
        "direction": "en_ru",
        "prompt_en": "pollution",
        "options_ru": ["загрязнение", "загрязнять", "грязь", "отходы"],
        "correct": 0,
    },
    {
        "id": "v14",
        "level": "A2",
        "topic": "culture",
        "direction": "en_ru",
        "prompt_en": "tradition",
        "options_ru": ["традиция", "традиционный", "обычай", "ритуал"],
        "correct": 0,
        "correct_any": [0, 2],
    },
    {
        "id": "v15",
        "level": "A2",
        "topic": "tech",
        "direction": "en_ru",
        "prompt_en": "password",
        "options_ru": ["пароль", "парольная", "код", "ключ"],
        "correct": 0,
        "correct_any": [0, 2],
    },
    {
        "id": "v16",
        "level": "B1",
        "topic": "work",
        "direction": "en_ru",
        "prompt_en": "deadline",
        "options_ru": ["срок сдачи", "срочность", "дедлайн", "расписание"],
        "correct": 0,
        "correct_any": [0, 2],
    },
    {
        "id": "v17",
        "level": "B1",
        "topic": "feelings",
        "direction": "en_ru",
        "prompt_en": "anxious",
        "options_ru": ["тревожный", "тревога", "активный", "злой"],
        "correct": 0,
    },
    {
        "id": "v18",
        "level": "B1",
        "topic": "travel",
        "direction": "en_ru",
        "prompt_en": "itinerary",
        "options_ru": ["маршрут поездки", "маршрут автобуса", "расписание", "направление"],
        "correct": 0,
    },
    {
        "id": "v19",
        "level": "B1",
        "topic": "environment",
        "direction": "en_ru",
        "prompt_en": "sustainable",
        "options_ru": ["устойчивый / экологичный", "поддержанный", "постоянный", "стабильный"],
        "correct": 0,
    },
    {
        "id": "v20",
        "level": "B1",
        "topic": "education",
        "direction": "en_ru",
        "prompt_en": "scholarship",
        "options_ru": ["стипендия", "школа", "учёба", "семинар"],
        "correct": 0,
    },
    {
        "id": "v21",
        "level": "B2",
        "topic": "work",
        "direction": "en_ru",
        "prompt_en": "negotiate",
        "options_ru": ["вести переговоры", "отрицать", "назначить", "отметить"],
        "correct": 0,
    },
    {
        "id": "v22",
        "level": "B2",
        "topic": "feelings",
        "direction": "en_ru",
        "prompt_en": "reluctant",
        "options_ru": ["неохотный", "релевантный", "расслабленный", "надёжный"],
        "correct": 0,
    },
    {
        "id": "v23",
        "level": "B2",
        "topic": "tech",
        "direction": "en_ru",
        "prompt_en": "obsolete",
        "options_ru": ["устаревший", "обязательный", "очевидный", "абсолютный"],
        "correct": 0,
    },
    {
        "id": "v24",
        "level": "B2",
        "topic": "culture",
        "direction": "en_ru",
        "prompt_en": "heritage",
        "options_ru": ["наследие", "наследование", "наследник", "наследие права"],
        "correct": 0,
    },
    {
        "id": "v25",
        "level": "B2",
        "topic": "health",
        "direction": "en_ru",
        "prompt_en": "recovery",
        "options_ru": ["выздоровление", "возврат", "рецидив", "реанимация"],
        "correct": 0,
    },
    # ru_en v26–v50
    {
        "id": "v26",
        "level": "A0",
        "topic": "daily",
        "direction": "ru_en",
        "prompt_ru": "яблоко",
        "options_en": ["apple", "apply", "apricot", "appeal"],
        "correct": 0,
    },
    {
        "id": "v27",
        "level": "A0",
        "topic": "family",
        "direction": "ru_en",
        "prompt_ru": "отец",
        "options_en": ["father", "further", "farmer", "feather"],
        "correct": 0,
    },
    {
        "id": "v28",
        "level": "A0",
        "topic": "colors",
        "direction": "ru_en",
        "prompt_ru": "красный",
        "options_en": ["red", "read", "reed", "raid"],
        "correct": 0,
    },
    {
        "id": "v29",
        "level": "A0",
        "topic": "numbers",
        "direction": "ru_en",
        "prompt_ru": "семь",
        "options_en": ["seven", "several", "severe", "sever"],
        "correct": 0,
    },
    {
        "id": "v30",
        "level": "A1",
        "topic": "food",
        "direction": "ru_en",
        "prompt_ru": "сыр",
        "options_en": ["cheese", "chase", "chess", "cheap"],
        "correct": 0,
    },
    {
        "id": "v31",
        "level": "A1",
        "topic": "home",
        "direction": "ru_en",
        "prompt_ru": "окно",
        "options_en": ["window", "widow", "winter", "winner"],
        "correct": 0,
    },
    {
        "id": "v32",
        "level": "A1",
        "topic": "travel",
        "direction": "ru_en",
        "prompt_ru": "аэропорт",
        "options_en": ["airport", "airplane", "airfield", "airspace"],
        "correct": 0,
    },
    {
        "id": "v33",
        "level": "A1",
        "topic": "shopping",
        "direction": "ru_en",
        "prompt_ru": "скидка",
        "options_en": ["discount", "discuss", "discover", "display"],
        "correct": 0,
    },
    {
        "id": "v34",
        "level": "A1",
        "topic": "weather",
        "direction": "ru_en",
        "prompt_ru": "дождь",
        "options_en": ["rain", "reign", "rail", "raise"],
        "correct": 0,
    },
    {
        "id": "v35",
        "level": "A1",
        "topic": "work",
        "direction": "ru_en",
        "prompt_ru": "коллега",
        "options_en": ["colleague", "college", "collection", "collision"],
        "correct": 0,
    },
    {
        "id": "v36",
        "level": "A2",
        "topic": "health",
        "direction": "ru_en",
        "prompt_ru": "температура",
        "options_en": ["temperature", "temporary", "temper", "tempo"],
        "correct": 0,
    },
    {
        "id": "v37",
        "level": "A2",
        "topic": "education",
        "direction": "ru_en",
        "prompt_ru": "экзамен",
        "options_en": ["exam", "example", "exit", "exact"],
        "correct": 0,
    },
    {
        "id": "v38",
        "level": "A2",
        "topic": "environment",
        "direction": "ru_en",
        "prompt_ru": "перерабатывать",
        "options_en": ["recycle", "recall", "recover", "receive"],
        "correct": 0,
    },
    {
        "id": "v39",
        "level": "A2",
        "topic": "culture",
        "direction": "ru_en",
        "prompt_ru": "музей",
        "options_en": ["museum", "music", "muscle", "mustard"],
        "correct": 0,
    },
    {
        "id": "v40",
        "level": "A2",
        "topic": "tech",
        "direction": "ru_en",
        "prompt_ru": "загрузить",
        "options_en": ["download", "downfall", "downgrade", "downtown"],
        "correct": 0,
    },
    {
        "id": "v41",
        "level": "B1",
        "topic": "work",
        "direction": "ru_en",
        "prompt_ru": "продвижение (по службе)",
        "options_en": ["promotion", "proposal", "proportion", "provision"],
        "correct": 0,
    },
    {
        "id": "v42",
        "level": "B1",
        "topic": "feelings",
        "direction": "ru_en",
        "prompt_ru": "разочарованный",
        "options_en": ["disappointed", "disapproved", "disappeared", "discharged"],
        "correct": 0,
    },
    {
        "id": "v43",
        "level": "B1",
        "topic": "travel",
        "direction": "ru_en",
        "prompt_ru": "бронировать",
        "options_en": ["book", "board", "border", "borrow"],
        "correct": 0,
    },
    {
        "id": "v44",
        "level": "B1",
        "topic": "environment",
        "direction": "ru_en",
        "prompt_ru": "выбросы",
        "options_en": ["emissions", "omissions", "admissions", "permissions"],
        "correct": 0,
    },
    {
        "id": "v45",
        "level": "B1",
        "topic": "education",
        "direction": "ru_en",
        "prompt_ru": "посещаемость",
        "options_en": ["attendance", "attention", "intention", "extension"],
        "correct": 0,
    },
    {
        "id": "v46",
        "level": "B2",
        "topic": "work",
        "direction": "ru_en",
        "prompt_ru": "компромисс",
        "options_en": ["compromise", "comprise", "compose", "compress"],
        "correct": 0,
    },
    {
        "id": "v47",
        "level": "B2",
        "topic": "feelings",
        "direction": "ru_en",
        "prompt_ru": "возмущённый",
        "options_en": ["outraged", "outgoing", "outstanding", "outspoken"],
        "correct": 0,
    },
    {
        "id": "v48",
        "level": "B2",
        "topic": "tech",
        "direction": "ru_en",
        "prompt_ru": "уязвимость (системы)",
        "options_en": ["vulnerability", "availability", "visibility", "versatility"],
        "correct": 0,
    },
    {
        "id": "v49",
        "level": "B2",
        "topic": "culture",
        "direction": "ru_en",
        "prompt_ru": "предрассудок",
        "options_en": ["prejudice", "privilege", "preference", "presence"],
        "correct": 0,
    },
    {
        "id": "v50",
        "level": "B2",
        "topic": "health",
        "direction": "ru_en",
        "prompt_ru": "профилактика",
        "options_en": ["prevention", "prediction", "prescription", "presentation"],
        "correct": 0,
    },
]

# ─── Reading: 6 passages, 30 questions total ──────────────────

READING_PASSAGES: list[dict] = [
    {
        "id": "rpass1",
        "level": "A1",
        "topic": "daily",
        "title": "Anna's Morning",
        "text": (
            "Anna wakes up at seven. She drinks tea, but she never drinks coffee "
            "before work. Her bus comes at half past seven, yet today she leaves "
            "the house ten minutes earlier than usual because she wants a seat. "
            "On the bus she reads messages from her sister. At the office she "
            "says hello to her colleague Tom, who always arrives after her. "
            "Anna prefers quiet mornings and does not like long meetings before lunch."
        ),
        "questions": [
            {
                "id": "rq1",
                "prompt": "Why does Anna leave home earlier than usual today?",
                "options": [
                    "She wants a seat on the bus",
                    "She wants to drink coffee first",
                    "She wants to meet Tom earlier",
                    "She wants to avoid her sister's messages",
                ],
                "correct": 0,
            },
            {
                "id": "rq2",
                "prompt": "What is true about Anna's drinks before work?",
                "options": [
                    "She drinks tea, not coffee",
                    "She drinks coffee, not tea",
                    "She drinks both tea and coffee",
                    "She drinks neither tea nor coffee",
                ],
                "correct": 0,
            },
            {
                "id": "rq3",
                "prompt": "What can we infer about Tom?",
                "options": [
                    "He usually arrives later than Anna",
                    "He always arrives before Anna",
                    "He never comes to the office",
                    "He leaves with Anna every morning",
                ],
                "correct": 0,
            },
            {
                "id": "rq4",
                "prompt": "How does Anna feel about early meetings?",
                "options": [
                    "She dislikes long ones before lunch",
                    "She enjoys them more than quiet mornings",
                    "She prefers them to reading messages",
                    "She wants them every day with Tom",
                ],
                "correct": 0,
            },
        ],
    },
    {
        "id": "rpass2",
        "level": "A2",
        "topic": "travel",
        "title": "A Weekend Trip",
        "text": (
            "Last Saturday Maya and her brother took a slow train to a small coastal town. "
            "They had planned to stay two nights, but the guesthouse only had one free room "
            "after a storm damaged the roof of the other wing. Maya almost cancelled, yet "
            "her brother suggested sharing the room and walking more during the day. "
            "On Sunday morning the weather cleared, so they rented bikes instead of joining "
            "a crowded boat tour. Maya later said the trip felt better than their usual "
            "city weekends, mainly because they spent less time waiting in lines."
        ),
        "questions": [
            {
                "id": "rq5",
                "prompt": "Why did they end up with only one room?",
                "options": [
                    "Storm damage limited the guesthouse rooms",
                    "They booked only one room from the start",
                    "The boat tour required a single booking",
                    "The train delay made them arrive too late",
                ],
                "correct": 0,
            },
            {
                "id": "rq6",
                "prompt": "What alternative did they choose on Sunday?",
                "options": [
                    "Renting bikes instead of a boat tour",
                    "Joining a boat tour instead of walking",
                    "Staying indoors because of the storm",
                    "Returning home earlier than planned",
                ],
                "correct": 0,
            },
            {
                "id": "rq7",
                "prompt": "What mainly made the trip feel better for Maya?",
                "options": [
                    "Less time spent waiting in lines",
                    "A longer stay than usual",
                    "A private boat tour",
                    "Cheaper train tickets",
                ],
                "correct": 0,
            },
            {
                "id": "rq8",
                "prompt": "What was Maya's first reaction to the room problem?",
                "options": [
                    "She nearly cancelled the stay",
                    "She immediately rented bikes",
                    "She insisted on a boat tour",
                    "She asked for a second night free",
                ],
                "correct": 0,
            },
            {
                "id": "rq9",
                "prompt": "How long had they originally intended to stay?",
                "options": [
                    "Two nights",
                    "One night",
                    "A full week",
                    "Only Sunday morning",
                ],
                "correct": 0,
            },
        ],
    },
    {
        "id": "rpass3",
        "level": "A2",
        "topic": "work",
        "title": "Changing Schedules",
        "text": (
            "At the design studio where Leo works, Friday used to be the quietest day. "
            "Clients rarely called, and the team finished early. After a new project "
            "manager arrived, Fridays became the day for status meetings that often "
            "run into the afternoon. Leo does not mind the meetings themselves, but he "
            "misses the time he used for checking details in his drawings. He now does "
            "that work on Thursday evenings at home, which makes his weekends shorter. "
            "His manager says the change helps the team catch problems sooner."
        ),
        "questions": [
            {
                "id": "rq10",
                "prompt": "What changed Fridays at Leo's studio?",
                "options": [
                    "Status meetings filled much of the day",
                    "Clients stopped calling completely",
                    "The team began finishing even earlier",
                    "Leo moved all meetings to Thursday",
                ],
                "correct": 0,
            },
            {
                "id": "rq11",
                "prompt": "What does Leo miss most about the old Fridays?",
                "options": [
                    "Time to check details in his drawings",
                    "Longer status meetings with clients",
                    "Working from home every Friday",
                    "Shorter weekends with his manager",
                ],
                "correct": 0,
            },
            {
                "id": "rq12",
                "prompt": "How has Leo adapted?",
                "options": [
                    "He reviews drawings on Thursday evenings",
                    "He skips Friday meetings entirely",
                    "He asks clients to call only on Monday",
                    "He finishes all work before Thursday",
                ],
                "correct": 0,
            },
            {
                "id": "rq13",
                "prompt": "What is the manager's stated reason for the change?",
                "options": [
                    "Problems are noticed earlier",
                    "Weekends should be shorter",
                    "Clients prefer Friday calls",
                    "Drawings need fewer details",
                ],
                "correct": 0,
            },
        ],
    },
    {
        "id": "rpass4",
        "level": "B1",
        "topic": "environment",
        "title": "A Local Plastic Ban",
        "text": (
            "When the city banned single-use plastic bags in grocery stores, many shoppers "
            "expected long queues and angry cashiers. The first week was messy: people "
            "forgot reusable bags and bought paper ones that tore easily. After a month, "
            "however, most regulars carried fabric bags, and stores reported fewer bags "
            "left in parking lots. Critics still argue that paper production uses more "
            "water, while supporters point to cleaner streets near markets. The council "
            "plans to review the ban after one year and may extend it to takeaway packaging "
            "if small businesses receive free starter kits."
        ),
        "questions": [
            {
                "id": "rq14",
                "prompt": "What was the main early problem after the ban?",
                "options": [
                    "Shoppers forgot reusable bags and used weak paper ones",
                    "Cashiers refused to sell any bags at all",
                    "Parking lots filled with fabric bags",
                    "Stores closed for a full month",
                ],
                "correct": 0,
            },
            {
                "id": "rq15",
                "prompt": "What positive change did stores notice later?",
                "options": [
                    "Fewer bags left in parking lots",
                    "Longer queues every morning",
                    "More water used by customers",
                    "Takeaway packaging banned immediately",
                ],
                "correct": 0,
            },
            {
                "id": "rq16",
                "prompt": "What do critics of the ban emphasize?",
                "options": [
                    "Paper production's water use",
                    "Cleaner streets near markets",
                    "Free starter kits for businesses",
                    "Fabric bags becoming too cheap",
                ],
                "correct": 0,
            },
            {
                "id": "rq17",
                "prompt": "Under what condition might the ban expand?",
                "options": [
                    "If small businesses get free starter kits",
                    "If paper bags stop tearing completely",
                    "If cashiers demand longer queues",
                    "If parking lots fill with fabric bags",
                ],
                "correct": 0,
            },
            {
                "id": "rq18",
                "prompt": "When will the council formally review the ban?",
                "options": [
                    "After one year",
                    "After the first messy week",
                    "After one month only",
                    "Before stores report any change",
                ],
                "correct": 0,
            },
        ],
    },
    {
        "id": "rpass5",
        "level": "B1",
        "topic": "tech",
        "title": "Quiet Mode at School",
        "text": (
            "Northvale Secondary introduced a 'quiet mode' policy for phones during lessons. "
            "Students may keep devices in their bags, but notifications must be silenced. "
            "Teachers noticed that group projects finished faster, yet some pupils said they "
            "felt anxious without constant access to messages. The school did not ban phones "
            "completely because parents wanted a way to reach children after clubs. Instead, "
            "the office now holds urgent messages and delivers them between periods. A survey "
            "showed mixed feelings: older students supported the rule more than younger ones."
        ),
        "questions": [
            {
                "id": "rq19",
                "prompt": "What does quiet mode require during lessons?",
                "options": [
                    "Silenced notifications while phones stay in bags",
                    "Phones left at home every day",
                    "Constant checking of parent messages",
                    "Office staff using phones in class",
                ],
                "correct": 0,
            },
            {
                "id": "rq20",
                "prompt": "What unexpected downside did some students report?",
                "options": [
                    "Anxiety without constant message access",
                    "Slower group projects than before",
                    "Parents unable to call after clubs",
                    "Teachers banning bags in classrooms",
                ],
                "correct": 0,
            },
            {
                "id": "rq21",
                "prompt": "Why weren't phones banned completely?",
                "options": [
                    "Parents wanted contact after clubs",
                    "Teachers preferred louder notifications",
                    "Younger students demanded free messaging",
                    "The office refused to hold any messages",
                ],
                "correct": 0,
            },
            {
                "id": "rq22",
                "prompt": "How are urgent messages handled now?",
                "options": [
                    "The office passes them between periods",
                    "Teachers read them aloud in every lesson",
                    "Students check phones every five minutes",
                    "Parents must wait until the next school year",
                ],
                "correct": 0,
            },
            {
                "id": "rq23",
                "prompt": "What did the survey suggest about age and support?",
                "options": [
                    "Older students supported the rule more",
                    "Younger students supported it more",
                    "Support was equal across all ages",
                    "Only parents supported the rule",
                ],
                "correct": 0,
            },
        ],
    },
    {
        "id": "rpass6",
        "level": "B2",
        "topic": "health",
        "title": "Shift Work and Sleep",
        "text": (
            "A regional hospital trial asked night-shift nurses to keep a fixed sleep window "
            "even on days off, rather than switching back to daytime sleep. Early results "
            "suggested fewer reported headaches and slightly faster reaction times on simple "
            "alertness tests. However, participants with young children found the schedule "
            "harder to maintain, and several dropped out after three weeks. Researchers "
            "caution that the sample was small and that caffeine use was not controlled. "
            "They recommend larger studies before hospitals rewrite staffing guidelines, "
            "while noting that consistent darkness and cooler bedrooms helped those who stayed."
        ),
        "questions": [
            {
                "id": "rq24",
                "prompt": "What sleep strategy did the trial promote?",
                "options": [
                    "Keeping a fixed sleep window even on days off",
                    "Switching freely between day and night sleep",
                    "Sleeping only during hospital breaks",
                    "Avoiding darkness in bedrooms at all costs",
                ],
                "correct": 0,
            },
            {
                "id": "rq25",
                "prompt": "Which early benefit was reported?",
                "options": [
                    "Fewer headaches and slightly faster alertness reactions",
                    "Larger samples and controlled caffeine use",
                    "Easier schedules for parents of young children",
                    "Immediate changes to all staffing guidelines",
                ],
                "correct": 0,
            },
            {
                "id": "rq26",
                "prompt": "Who struggled most with the schedule?",
                "options": [
                    "Participants with young children",
                    "Researchers measuring reaction times",
                    "Nurses without any days off",
                    "Patients waiting for larger studies",
                ],
                "correct": 0,
            },
            {
                "id": "rq27",
                "prompt": "Why do researchers urge caution?",
                "options": [
                    "The sample was small and caffeine was uncontrolled",
                    "All participants finished the full trial easily",
                    "Darkness and cool rooms made results invalid",
                    "Hospitals already rewrote every guideline",
                ],
                "correct": 0,
            },
            {
                "id": "rq28",
                "prompt": "What environmental factors helped those who continued?",
                "options": [
                    "Consistent darkness and cooler bedrooms",
                    "Brighter lights and warmer rooms",
                    "More caffeine during night shifts",
                    "Switching sleep times every weekend",
                ],
                "correct": 0,
            },
            {
                "id": "rq29",
                "prompt": "What should happen before guidelines change?",
                "options": [
                    "Larger studies should be completed",
                    "All nurses with children should leave",
                    "Caffeine must be banned hospital-wide",
                    "Sleep windows should become optional only",
                ],
                "correct": 0,
            },
            {
                "id": "rq30",
                "prompt": "What can be inferred about dropout timing?",
                "options": [
                    "Several people left after about three weeks",
                    "Nobody left until the final year",
                    "Dropouts happened only on the first night",
                    "Everyone stayed despite childcare issues",
                ],
                "correct": 0,
            },
        ],
    },
]

# ─── Listening (25): script + one hard context question each ──

LISTENING_ITEMS: list[dict] = [
    {
        "id": "L01",
        "level": "A0",
        "topic": "daily",
        "script": (
            "Hi, I'm Sam. This is my bag. My book is in the bag. "
            "My keys are not in the bag. They are on the table."
        ),
        "question": {
            "prompt": "Where are Sam's keys right now?",
            "options": [
                "On the table",
                "In the bag with the book",
                "In Sam's hand",
                "Under the book",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L02",
        "level": "A0",
        "topic": "food",
        "script": (
            "Woman: Do you want tea or juice? "
            "Man: Juice, please. No sugar. "
            "Woman: Okay. Here you are."
        ),
        "question": {
            "prompt": "What does the man want in his drink?",
            "options": [
                "Juice without sugar",
                "Tea with sugar",
                "Juice with sugar",
                "Tea without sugar",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L03",
        "level": "A1",
        "topic": "shopping",
        "script": (
            "Customer: How much is this blue shirt? "
            "Assistant: It's twenty pounds, but the red one is on sale for fifteen. "
            "Customer: I'll take the red one then."
        ),
        "question": {
            "prompt": "Why does the customer choose the red shirt?",
            "options": [
                "It costs less because it is on sale",
                "It is the only size left in the shop",
                "The assistant refuses to sell the blue one",
                "Blue shirts are not available today",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L04",
        "level": "A1",
        "topic": "travel",
        "script": (
            "The next bus to the airport leaves at ten fifteen from gate three. "
            "Gate four is for city buses only. Please have your ticket ready."
        ),
        "question": {
            "prompt": "Where should airport passengers wait?",
            "options": [
                "At gate three",
                "At gate four",
                "At any free gate",
                "Outside without a ticket",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L05",
        "level": "A1",
        "topic": "home",
        "script": (
            "Mum: Can you close the window? It's getting cold. "
            "Teen: Sure. Should I turn on the heater too? "
            "Mum: Not yet. Just the window for now."
        ),
        "question": {
            "prompt": "What does Mum want done immediately?",
            "options": [
                "Only close the window",
                "Turn on the heater now",
                "Open the window wider",
                "Leave everything as it is",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L06",
        "level": "A1",
        "topic": "work",
        "script": (
            "Boss: The meeting starts at nine, but please arrive by eight forty-five "
            "to set up the laptop. "
            "Employee: Got it. I'll be there early."
        ),
        "question": {
            "prompt": "Why should the employee come before nine?",
            "options": [
                "To prepare the laptop before the meeting",
                "Because the meeting was moved to eight forty-five",
                "To cancel the meeting with the boss",
                "To leave the laptop at home",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L07",
        "level": "A2",
        "topic": "health",
        "script": (
            "Doctor: Your tests look fine, but you still feel tired. "
            "Try sleeping earlier for two weeks and cut late coffee. "
            "Patient: I usually drink coffee after dinner. I'll stop that."
        ),
        "question": {
            "prompt": "What change did the patient agree to make?",
            "options": [
                "Stop drinking coffee after dinner",
                "Take new medicine every night",
                "Sleep later than usual",
                "Drink more coffee in the morning only",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L08",
        "level": "A2",
        "topic": "travel",
        "script": (
            "Agent: Your flight is delayed by forty minutes due to weather. "
            "Gate B12 is unchanged. Free water is available near the desk. "
            "Passenger: Thanks. I'll wait here rather than leave the area."
        ),
        "question": {
            "prompt": "What does the passenger decide to do?",
            "options": [
                "Stay near the gate area and wait",
                "Change to a different gate immediately",
                "Leave the airport for forty minutes",
                "Ask for a new ticket at gate B12",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L09",
        "level": "A2",
        "topic": "education",
        "script": (
            "Teacher: The essay is due Friday, but you may submit a draft on Wednesday "
            "for comments. "
            "Student: I'll send a draft then. I still need one more source."
        ),
        "question": {
            "prompt": "Why is the student sending something on Wednesday?",
            "options": [
                "To get feedback before the final deadline",
                "Because the final essay is due on Wednesday",
                "To replace the missing source with a draft",
                "Because Friday submissions are not allowed",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L10",
        "level": "A2",
        "topic": "shopping",
        "script": (
            "Clerk: We can order the black jacket in your size, but it takes five days. "
            "Shopper: I need it for a trip on Saturday, so I'll try another store."
        ),
        "question": {
            "prompt": "Why does the shopper leave without ordering?",
            "options": [
                "The wait is too long for her trip timing",
                "The store does not sell black jackets",
                "Saturday delivery is free only here",
                "Her size is permanently unavailable",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L11",
        "level": "A2",
        "topic": "weather",
        "script": (
            "Host: Tomorrow looks sunny in the morning, but heavy rain is likely after three. "
            "If you're hiking, start early and be down by mid-afternoon."
        ),
        "question": {
            "prompt": "What advice is given to hikers?",
            "options": [
                "Begin early and finish before the afternoon rain",
                "Wait until after three to start climbing",
                "Hike only when it is already raining",
                "Ignore the forecast and stay out late",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L12",
        "level": "B1",
        "topic": "work",
        "script": (
            "Manager: We won't renew the old software licence. Training on the new tool "
            "starts Monday. "
            "Staff: Some of us still have reports due this week on the old system. "
            "Manager: Finish those first, then switch."
        ),
        "question": {
            "prompt": "What should staff do about this week's reports?",
            "options": [
                "Complete them on the old system before switching",
                "Ignore them until after Monday training",
                "Rewrite them only in the new tool now",
                "Cancel the reports and renew the licence",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L13",
        "level": "B1",
        "topic": "culture",
        "script": (
            "Guide: The exhibition opens at ten, but the first hour is reserved for members. "
            "General tickets are valid from eleven. Photography is allowed without flash."
        ),
        "question": {
            "prompt": "When can a non-member visitor enter with a general ticket?",
            "options": [
                "From eleven onwards",
                "From ten with any ticket",
                "Only after flash photography ends",
                "During the members-only first hour",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L14",
        "level": "B1",
        "topic": "environment",
        "script": (
            "Speaker: The riverside clean-up is still on Sunday, even if it rains lightly. "
            "Only strong wind will postpone it. Bring gloves; bags are provided."
        ),
        "question": {
            "prompt": "Under what condition will the event be postponed?",
            "options": [
                "Strong wind",
                "Light rain",
                "Missing gloves from volunteers",
                "Too many bags at the river",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L15",
        "level": "B1",
        "topic": "feelings",
        "script": (
            "Friend A: You seem quiet today. "
            "Friend B: I'm fine. I just didn't sleep well after that long call with work. "
            "Friend A: Want to reschedule dinner? "
            "Friend B: No, dinner helps. Let's keep it."
        ),
        "question": {
            "prompt": "Why does Friend B want to keep dinner plans?",
            "options": [
                "Dinner feels helpful despite poor sleep",
                "Work asked them to cancel all plans",
                "They slept well and feel energetic",
                "They want another long work call instead",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L16",
        "level": "B1",
        "topic": "tech",
        "script": (
            "Support: I can reset your password now, but two-factor codes will still go "
            "to your old phone until you update the number in settings. "
            "User: I'll update it after this call."
        ),
        "question": {
            "prompt": "What remains a problem after the password reset?",
            "options": [
                "Codes still go to the old phone number",
                "The password cannot be reset at all",
                "Settings block all future logins forever",
                "Support refuses to help during the call",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L17",
        "level": "B1",
        "topic": "education",
        "script": (
            "Advisor: If your attendance stays below eighty percent, you can't sit the final. "
            "You've missed four seminars, so one more absence puts you at risk. "
            "Student: I'll make Thursday's class for sure."
        ),
        "question": {
            "prompt": "What is the student's immediate plan?",
            "options": [
                "Attend Thursday's class to avoid further risk",
                "Skip Thursday and retake the final later",
                "Ask to ignore the eighty percent rule",
                "Miss four more seminars this month",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L18",
        "level": "B2",
        "topic": "work",
        "script": (
            "Director: We're pausing the marketing campaign, not cancelling it. Budget "
            "will move to customer support until complaints fall. "
            "Analyst: So creative work stops, but the team stays employed? "
            "Director: Exactly — reassigned, not laid off."
        ),
        "question": {
            "prompt": "What happens to the marketing team?",
            "options": [
                "They are reassigned while the campaign is paused",
                "They are laid off because the campaign is cancelled",
                "They keep running ads with a larger budget",
                "They move permanently out of customer support",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L19",
        "level": "B2",
        "topic": "health",
        "script": (
            "Researcher: Participants improved when they walked after meals, not when they "
            "only walked in the morning. Timing mattered more than total weekly minutes "
            "in this small study."
        ),
        "question": {
            "prompt": "What does the study suggest was more important?",
            "options": [
                "When people walked relative to meals",
                "Only the total minutes walked each week",
                "Walking exclusively in the morning",
                "Avoiding all walking after meals",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L20",
        "level": "B2",
        "topic": "culture",
        "script": (
            "Critic: The play's second act is weaker, yet the cast's timing saves several "
            "scenes that would otherwise feel slow. I'd still recommend it, with that caveat."
        ),
        "question": {
            "prompt": "What is the critic's overall stance?",
            "options": [
                "Recommend it, while noting a weaker second act",
                "Reject it because timing ruins every scene",
                "Praise only the second act as the strongest part",
                "Say the cast makes the whole play feel slow",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L21",
        "level": "B2",
        "topic": "environment",
        "script": (
            "Official: The bridge repair will close the east lane for six weeks. Buses "
            "will detour via Mill Road, adding about twelve minutes. Cyclists may still "
            "use the west path."
        ),
        "question": {
            "prompt": "Who is least affected in terms of route access?",
            "options": [
                "Cyclists using the west path",
                "Bus passengers with no time change",
                "Drivers keeping the east lane open",
                "Everyone equally, with no detours",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L22",
        "level": "B2",
        "topic": "tech",
        "script": (
            "Engineer: We delayed the update because a rare bug wiped drafts for users "
            "on older tablets. Phones were unaffected. A patched version ships Friday."
        ),
        "question": {
            "prompt": "Why was the update delayed?",
            "options": [
                "A bug risked wiping drafts on older tablets",
                "Phones crashed for every user overnight",
                "Friday shipping was banned by policy",
                "Drafts were safer without any patch",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L23",
        "level": "B2",
        "topic": "travel",
        "script": (
            "Host: If your connection is under forty-five minutes in Hub Airport, "
            "buy travel insurance that covers missed links. The airport is large, "
            "and security lines vary by terminal."
        ),
        "question": {
            "prompt": "Who is this advice mainly for?",
            "options": [
                "Travellers with short connections at Hub Airport",
                "Travellers with no connections at all",
                "Only staff who work in security lines",
                "Anyone avoiding insurance on long stays",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L24",
        "level": "B2",
        "topic": "feelings",
        "script": (
            "Mentor: Feeling nervous before the presentation is normal. What worries me "
            "is skipping rehearsal. Confidence usually follows preparation, not the other "
            "way around."
        ),
        "question": {
            "prompt": "What does the mentor see as the real problem?",
            "options": [
                "Skipping rehearsal rather than normal nerves",
                "Feeling any nervousness at all",
                "Preparing too much before speaking",
                "Confidence coming before any practice",
            ],
            "correct": 0,
        },
    },
    {
        "id": "L25",
        "level": "B2",
        "topic": "daily",
        "script": (
            "Neighbour: I'll water your plants while you're away, but I can't take the cat "
            "to the vet on Thursday — I've got a hospital appointment myself. "
            "Owner: No problem. My sister can do the vet run."
        ),
        "question": {
            "prompt": "What will the neighbour definitely help with?",
            "options": [
                "Watering the plants during the trip",
                "Taking the cat to the vet on Thursday",
                "Going to the hospital for the owner",
                "Asking the sister to water plants",
            ],
            "correct": 0,
        },
    },
]

# ─── Writing prompts by level ─────────────────────────────────

WRITING_PROMPTS: dict[str, dict] = {
    "A0": {
        "prompt": (
            "Write 8 short English sentences about yourself: name, age, city, "
            "family, food you like, and one daily activity."
        ),
        "min_sentences": 8,
        "min_chars": 120,
        "topic": "daily",
    },
    "A1": {
        "prompt": (
            "Write 8 English sentences about your typical day: morning, work or school, "
            "meals, and evening. Use present simple."
        ),
        "min_sentences": 8,
        "min_chars": 180,
        "topic": "daily",
    },
    "A2": {
        "prompt": (
            "Write 8 English sentences about a trip you took (or want to take): where, "
            "how you travelled, what you did, and what you liked or disliked."
        ),
        "min_sentences": 8,
        "min_chars": 220,
        "topic": "travel",
    },
    "B1": {
        "prompt": (
            "Write at least 8 English sentences giving your opinion: Should people work "
            "from home more often? Give reasons and one counter-argument."
        ),
        "min_sentences": 8,
        "min_chars": 280,
        "topic": "work",
    },
    "B2": {
        "prompt": (
            "Write at least 8 English sentences discussing this statement: "
            "'Technology makes people less social.' Agree, disagree, or partly agree. "
            "Support your view with examples and a short conclusion."
        ),
        "min_sentences": 8,
        "min_chars": 350,
        "topic": "tech",
    },
}

# ─── Speaking interview (~25), A0 → B2 ────────────────────────

SPEAKING_INTERVIEW: list[dict] = [
    {"id": "s01", "level": "A0", "prompt": "What is your name? Tell me in English."},
    {"id": "s02", "level": "A0", "prompt": "How old are you?"},
    {"id": "s03", "level": "A0", "prompt": "Where do you live?"},
    {"id": "s04", "level": "A0", "prompt": "Say three colours you like."},
    {"id": "s05", "level": "A1", "prompt": "Tell me about your family in a few sentences."},
    {"id": "s06", "level": "A1", "prompt": "What do you usually eat for breakfast?"},
    {"id": "s07", "level": "A1", "prompt": "Describe your room or apartment briefly."},
    {"id": "s08", "level": "A1", "prompt": "What time do you start work or school?"},
    {"id": "s09", "level": "A1", "prompt": "What do you like doing at the weekend?"},
    {"id": "s10", "level": "A2", "prompt": "Talk about a place you visited recently."},
    {"id": "s11", "level": "A2", "prompt": "Describe the weather today and compare it to yesterday."},
    {"id": "s12", "level": "A2", "prompt": "Tell me about your favourite film or series and why you like it."},
    {"id": "s13", "level": "A2", "prompt": "What are your plans for next month?"},
    {"id": "s14", "level": "A2", "prompt": "Explain how you usually shop for food."},
    {"id": "s15", "level": "B1", "prompt": "What are the advantages and disadvantages of living in a big city?"},
    {"id": "s16", "level": "B1", "prompt": "Describe a challenge you faced at work or school and how you handled it."},
    {"id": "s17", "level": "B1", "prompt": "If you could learn any new skill this year, what would it be and why?"},
    {"id": "s18", "level": "B1", "prompt": "How has technology changed the way you communicate with friends?"},
    {"id": "s19", "level": "B1", "prompt": "Talk about an environmental problem in your area and a possible solution."},
    {"id": "s20", "level": "B2", "prompt": "Some people say exams are the best way to measure learning. What is your view?"},
    {
        "id": "s21",
        "level": "B2",
        "prompt": "If your city banned cars in the centre, how would daily life change for residents?",
    },
    {
        "id": "s22",
        "level": "B2",
        "prompt": "Describe a cultural tradition you value and explain whether it should be preserved.",
    },
    {
        "id": "s23",
        "level": "B2",
        "prompt": "Would you rather have a high salary with long hours or more free time with less pay? Justify.",
    },
    {
        "id": "s24",
        "level": "B2",
        "prompt": "How should schools balance screen time and face-to-face learning?",
    },
    {
        "id": "s25",
        "level": "B2",
        "prompt": "Imagine you could change one law in your country. What would you change and why?",
    },
]

# ─── Topic labels (RU) for weak-spot reports ──────────────────

TOPIC_LABELS_RU: dict[str, str] = {
    "be": "глагол be",
    "articles": "артикли",
    "plurals": "множественное число",
    "there_is": "there is / there are",
    "possessives": "притяжательные",
    "demonstratives": "указательные местоимения",
    "present_simple": "Present Simple",
    "present_continuous": "Present Continuous",
    "past_simple": "Past Simple",
    "past_continuous": "Past Continuous",
    "present_perfect": "Present Perfect",
    "future": "будущее время",
    "modals": "модальные глаголы",
    "comparatives": "сравнительная степень",
    "superlatives": "превосходная степень",
    "quantifiers": "квантификаторы",
    "conditionals": "условные предложения",
    "passive": "пассивный залог",
    "relative_clauses": "относительные придаточные",
    "reported_speech": "косвенная речь",
    "gerund_infinitive": "герундий и инфинитив",
    "used_to": "used to",
    "wish": "конструкции с wish",
    "cleft_sentences": "расщеплённые предложения",
    "daily": "повседневная жизнь",
    "family": "семья",
    "colors": "цвета",
    "numbers": "числа",
    "food": "еда",
    "home": "дом",
    "travel": "путешествия",
    "shopping": "покупки",
    "weather": "погода",
    "work": "работа",
    "health": "здоровье",
    "education": "образование",
    "environment": "окружающая среда",
    "culture": "культура",
    "tech": "технологии",
    "feelings": "чувства и эмоции",
}


def grammar_by_id(gid: str) -> dict | None:
    for item in GRAMMAR:
        if item["id"] == gid:
            return item
    return None


def vocab_by_id(vid: str) -> dict | None:
    for item in VOCAB:
        if item["id"] == vid:
            return item
    return None
