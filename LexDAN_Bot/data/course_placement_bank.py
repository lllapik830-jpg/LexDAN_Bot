"""
Банк вступительного теста курса LexDAN (placement → CEFR A0–B2).

Ориентир: Cambridge English Placement Test —
Language Knowledge (grammar/vocab) + Reading + Listening,
плюс Writing и Speaking для профиля слабостей (нужны курсу).
Задания оригинальные, в логике CEFR / English File, не копия CEPT.
"""

from __future__ import annotations

# ─── Language Knowledge: MCQ ─────────────────────────────────
# level — целевой CEFR задания; correct — индекс options (0-based)

LK_ITEMS: list[dict] = [
    # A0 / Pre-A1
    {
        "id": "lk01",
        "level": "A0",
        "skill": "vocab",
        "prompt": "Choose the greeting:\n«___! My name is Anna.»",
        "options": ["Hello", "Goodbye", "Thanks", "Sorry"],
        "correct": 0,
    },
    {
        "id": "lk02",
        "level": "A0",
        "skill": "grammar",
        "prompt": "Complete: «I ___ a student.»",
        "options": ["am", "is", "are", "be"],
        "correct": 0,
    },
    {
        "id": "lk03",
        "level": "A0",
        "skill": "vocab",
        "prompt": "What number is this: 12?",
        "options": ["twelve", "twenty", "two", "twenty-two"],
        "correct": 0,
    },
    # A1
    {
        "id": "lk04",
        "level": "A1",
        "skill": "grammar",
        "prompt": "Complete: «She ___ in Moscow.»",
        "options": ["live", "lives", "living", "lived"],
        "correct": 1,
    },
    {
        "id": "lk05",
        "level": "A1",
        "skill": "grammar",
        "prompt": "Choose the question:\n«___ do you work?» — «In an office.»",
        "options": ["Where", "When", "Who", "Which"],
        "correct": 0,
    },
    {
        "id": "lk06",
        "level": "A1",
        "skill": "vocab",
        "prompt": "«I wake up at 7 and then I have ___.»",
        "options": ["breakfast", "luggage", "weather", "password"],
        "correct": 0,
    },
    # A2
    {
        "id": "lk07",
        "level": "A2",
        "skill": "grammar",
        "prompt": "Complete: «Yesterday I ___ to the cinema.»",
        "options": ["go", "goes", "went", "going"],
        "correct": 2,
    },
    {
        "id": "lk08",
        "level": "A2",
        "skill": "grammar",
        "prompt": "«There isn’t ___ milk in the fridge.»",
        "options": ["some", "any", "many", "a"],
        "correct": 1,
    },
    {
        "id": "lk09",
        "level": "A2",
        "skill": "grammar",
        "prompt": "«This bag is ___ than that one.»",
        "options": ["expensive", "more expensive", "most expensive", "as expensive"],
        "correct": 1,
    },
    {
        "id": "lk10",
        "level": "A2",
        "skill": "vocab",
        "prompt": "You buy a ticket and wait for a train at the ___.",
        "options": ["airport", "station", "kitchen", "pharmacy"],
        "correct": 1,
    },
    # B1
    {
        "id": "lk11",
        "level": "B1",
        "skill": "grammar",
        "prompt": "«I ___ here since 2020.»",
        "options": ["work", "worked", "have worked", "am working"],
        "correct": 2,
    },
    {
        "id": "lk12",
        "level": "B1",
        "skill": "grammar",
        "prompt": "«If it rains tomorrow, we ___ at home.»",
        "options": ["stay", "will stay", "stayed", "would stay"],
        "correct": 1,
    },
    {
        "id": "lk13",
        "level": "B1",
        "skill": "grammar",
        "prompt": "«The email ___ yesterday.»",
        "options": ["sent", "was sent", "was sending", "has send"],
        "correct": 1,
    },
    {
        "id": "lk14",
        "level": "B1",
        "skill": "vocab",
        "prompt": "A person who pays you for work is your ___.",
        "options": ["neighbour", "employer", "passenger", "stranger"],
        "correct": 1,
    },
    # B2
    {
        "id": "lk15",
        "level": "B2",
        "skill": "grammar",
        "prompt": "«If I had known earlier, I ___ you.»",
        "options": ["will tell", "would tell", "would have told", "told"],
        "correct": 2,
    },
    {
        "id": "lk16",
        "level": "B2",
        "skill": "grammar",
        "prompt": "«Despite ___ tired, she finished the report.»",
        "options": ["she was", "being", "be", "to be"],
        "correct": 1,
    },
    {
        "id": "lk17",
        "level": "B2",
        "skill": "vocab",
        "prompt": "«The company needs to ___ its carbon footprint.»",
        "options": ["reduce", "refuse", "replace", "remind"],
        "correct": 0,
    },
    {
        "id": "lk18",
        "level": "B2",
        "skill": "grammar",
        "prompt": "«She said she ___ the film before.»",
        "options": ["never saw", "had never seen", "has never see", "never see"],
        "correct": 1,
    },
]

# Первый проход (оценка «середины») + второй проход (уточнение)
LK_ROUND1_IDS = ["lk04", "lk05", "lk07", "lk08", "lk11", "lk12"]  # A1–B1 mix
LK_ROUND2_LOW_IDS = ["lk01", "lk02", "lk03", "lk06", "lk09", "lk10"]  # A0–A2
LK_ROUND2_HIGH_IDS = ["lk13", "lk14", "lk15", "lk16", "lk17", "lk18"]  # B1–B2

# ─── Reading passages ────────────────────────────────────────

READING: dict[str, dict] = {
    "A1": {
        "text": (
            "My name is Tom. I live in a small flat in London with my sister. "
            "I work in a café from Monday to Friday. At the weekend I play football "
            "with my friends. I like my job, but I want to learn English better."
        ),
        "questions": [
            {
                "prompt": "Where does Tom live?",
                "options": ["In a house", "In a flat", "In a hotel", "In a school"],
                "correct": 1,
            },
            {
                "prompt": "When does Tom play football?",
                "options": ["Every morning", "At the weekend", "On Mondays only", "Never"],
                "correct": 1,
            },
            {
                "prompt": "What does Tom want?",
                "options": [
                    "A new café",
                    "To learn English better",
                    "To leave London",
                    "A bigger flat only",
                ],
                "correct": 1,
            },
        ],
    },
    "A2": {
        "text": (
            "Last summer Mia went to Spain with her family. They stayed in a hotel "
            "near the beach. Every morning they swam, and in the evening they tried "
            "local food. Mia didn’t speak much Spanish, but people were friendly. "
            "She says it was the best holiday of her life."
        ),
        "questions": [
            {
                "prompt": "Where did Mia stay?",
                "options": ["With friends", "In a hotel", "In a tent", "At school"],
                "correct": 1,
            },
            {
                "prompt": "What did they do in the evening?",
                "options": [
                    "They swam",
                    "They tried local food",
                    "They flew home",
                    "They worked",
                ],
                "correct": 1,
            },
            {
                "prompt": "How does Mia feel about the holiday?",
                "options": [
                    "It was boring",
                    "It was too expensive",
                    "It was her best holiday",
                    "She hated the food",
                ],
                "correct": 2,
            },
        ],
    },
    "B1": {
        "text": (
            "More people are working from home than before. For some, it saves time "
            "on travel and helps them focus. Others miss talking to colleagues and "
            "find it hard to stop working in the evening. Experts say the best option "
            "is often a mix: some days at home, some days in the office."
        ),
        "questions": [
            {
                "prompt": "What is one advantage of working from home?",
                "options": [
                    "Longer meetings",
                    "Less travel time",
                    "No internet needed",
                    "More office parties",
                ],
                "correct": 1,
            },
            {
                "prompt": "What problem do some people have?",
                "options": [
                    "They sleep too much",
                    "They miss colleagues / can’t switch off",
                    "They never work",
                    "They hate coffee",
                ],
                "correct": 1,
            },
            {
                "prompt": "What do experts often recommend?",
                "options": [
                    "Only office work",
                    "Only home work",
                    "A mix of home and office",
                    "Stopping work completely",
                ],
                "correct": 2,
            },
        ],
    },
    "B2": {
        "text": (
            "Although social media can help people stay connected, it may also increase "
            "anxiety. Studies suggest that constantly comparing yourself to others online "
            "can reduce self-esteem. However, when used carefully — for learning and "
            "real communication — these platforms can still be useful. The challenge is "
            "balance rather than total disconnection."
        ),
        "questions": [
            {
                "prompt": "What negative effect is mentioned?",
                "options": [
                    "Better sleep",
                    "Possible anxiety / lower self-esteem",
                    "Cheaper phones",
                    "More exercise",
                ],
                "correct": 1,
            },
            {
                "prompt": "When can social media still be useful?",
                "options": [
                    "Only for shopping",
                    "Never",
                    "For learning and real communication",
                    "Only after midnight",
                ],
                "correct": 2,
            },
            {
                "prompt": "What is described as the main challenge?",
                "options": [
                    "Deleting all apps forever",
                    "Finding balance",
                    "Buying new devices",
                    "Ignoring friends offline",
                ],
                "correct": 1,
            },
        ],
    },
}

# A0 reading = ultra short
READING["A0"] = {
    "text": "Anna is from Russia. She is 20. She has a cat.",
    "questions": [
        {
            "prompt": "Where is Anna from?",
            "options": ["Russia", "Spain", "Italy", "USA"],
            "correct": 0,
        },
        {
            "prompt": "How old is Anna?",
            "options": ["12", "20", "30", "40"],
            "correct": 1,
        },
        {
            "prompt": "What animal does she have?",
            "options": ["A dog", "A cat", "A bird", "No animal"],
            "correct": 1,
        },
    ],
}

# ─── Listening scripts (озвучиваем TTS) ───────────────────────

LISTENING: dict[str, dict] = {
    "A0": {
        "script": "Hello. My name is Ben. I am from London.",
        "questions": [
            {
                "prompt": "What is his name?",
                "options": ["Ben", "Tom", "Sam", "Dan"],
                "correct": 0,
            },
            {
                "prompt": "Where is he from?",
                "options": ["Paris", "London", "Rome", "Berlin"],
                "correct": 1,
            },
        ],
    },
    "A1": {
        "script": (
            "Hi, I’m Sara. I work in a school. I start work at eight o’clock "
            "and I finish at four. I like my job."
        ),
        "questions": [
            {
                "prompt": "Where does Sara work?",
                "options": ["In a school", "In a shop", "In a bank", "At home"],
                "correct": 0,
            },
            {
                "prompt": "When does she finish?",
                "options": ["At 8", "At 4", "At 6", "At 10"],
                "correct": 1,
            },
            {
                "prompt": "Does she like her job?",
                "options": ["Yes", "No", "We don’t know", "Only on Mondays"],
                "correct": 0,
            },
        ],
    },
    "A2": {
        "script": (
            "Last weekend we went to the museum. It was crowded, but the exhibition "
            "was amazing. After that we had lunch in a small café near the park."
        ),
        "questions": [
            {
                "prompt": "Where did they go?",
                "options": ["To a museum", "To a stadium", "To a beach", "To a zoo"],
                "correct": 0,
            },
            {
                "prompt": "How was the place?",
                "options": ["Empty", "Crowded", "Closed", "Scary"],
                "correct": 1,
            },
            {
                "prompt": "What did they do after?",
                "options": [
                    "Went home immediately",
                    "Had lunch in a café",
                    "Played football",
                    "Bought a car",
                ],
                "correct": 1,
            },
        ],
    },
    "B1": {
        "script": (
            "I’ve been learning English for three years. At first it was difficult, "
            "especially listening. Now I can watch short videos without subtitles, "
            "but I still need more practice with speaking at work."
        ),
        "questions": [
            {
                "prompt": "How long has the speaker learned English?",
                "options": ["Three months", "Three years", "Thirteen years", "One week"],
                "correct": 1,
            },
            {
                "prompt": "What was especially difficult at first?",
                "options": ["Spelling", "Listening", "Writing emails", "Grammar only"],
                "correct": 1,
            },
            {
                "prompt": "What does the speaker still need?",
                "options": [
                    "More speaking practice at work",
                    "A new phone",
                    "Less vocabulary",
                    "To stop learning",
                ],
                "correct": 0,
            },
        ],
    },
    "B2": {
        "script": (
            "Remote interviews have become common. Candidates should test their camera "
            "and internet connection in advance. It’s also wise to prepare examples "
            "of past achievements, because interviewers often ask for evidence, not "
            "just general statements."
        ),
        "questions": [
            {
                "prompt": "What should candidates test in advance?",
                "options": [
                    "Their salary demands only",
                    "Camera and internet",
                    "The company’s shares",
                    "Nothing",
                ],
                "correct": 1,
            },
            {
                "prompt": "What should they prepare?",
                "options": [
                    "Holiday photos",
                    "Examples of past achievements",
                    "A long joke",
                    "Only yes/no answers",
                ],
                "correct": 1,
            },
            {
                "prompt": "What do interviewers often want?",
                "options": [
                    "Evidence, not only general statements",
                    "Silence",
                    "Gifts",
                    "Handwriting samples only",
                ],
                "correct": 0,
            },
        ],
    },
}

# ─── Writing prompts ─────────────────────────────────────────

WRITING: dict[str, dict] = {
    "A0": {
        "prompt": "Write 3–4 short sentences about yourself (name, city, job/study).",
        "min_chars": 25,
        "min_sentences": 2,
    },
    "A1": {
        "prompt": "Write 5–6 sentences about your typical day.",
        "min_chars": 60,
        "min_sentences": 4,
    },
    "A2": {
        "prompt": "Write about a trip or weekend in the past (6–8 sentences).",
        "min_chars": 90,
        "min_sentences": 5,
    },
    "B1": {
        "prompt": (
            "Write about your work or studies and one goal for this year "
            "(8–10 sentences)."
        ),
        "min_chars": 140,
        "min_sentences": 6,
    },
    "B2": {
        "prompt": (
            "What are advantages and disadvantages of social media? "
            "Write a short opinion (10–12 sentences)."
        ),
        "min_chars": 180,
        "min_sentences": 7,
    },
}

# ─── Speaking prompts (повторить / ответить голосом) ─────────

SPEAKING: dict[str, list[dict]] = {
    "A0": [
        {"prompt": "Say: «Hello, my name is …» (use your name).", "expect_any": True},
        {"prompt": "Say: «I am from …» (your country/city).", "expect_any": True},
    ],
    "A1": [
        {
            "prompt": "Answer in English: What do you do? (job or studies)",
            "expect_any": True,
        },
        {
            "prompt": "Answer: What time do you usually wake up?",
            "expect_any": True,
        },
    ],
    "A2": [
        {
            "prompt": "Talk for ~20 seconds: What did you do last weekend?",
            "expect_any": True,
        },
        {
            "prompt": "Answer: Where would you like to travel next? Why?",
            "expect_any": True,
        },
    ],
    "B1": [
        {
            "prompt": "Speak ~30 seconds: Describe your job or studies and one challenge.",
            "expect_any": True,
        },
        {
            "prompt": "Answer: Have you ever changed a habit? What happened?",
            "expect_any": True,
        },
    ],
    "B2": [
        {
            "prompt": (
                "Speak ~40 seconds: Do you think remote work is better than office work? Why?"
            ),
            "expect_any": True,
        },
        {
            "prompt": "Give your opinion: Should schools teach more practical skills?",
            "expect_any": True,
        },
    ],
}


def lk_by_id(item_id: str) -> dict | None:
    for it in LK_ITEMS:
        if it["id"] == item_id:
            return it
    return None


LEVEL_ORDER = ["A0", "A1", "A2", "B1", "B2"]


def nearest_reading_level(level: str) -> str:
    return level if level in READING else "A2"


def nearest_listening_level(level: str) -> str:
    return level if level in LISTENING else "A2"
