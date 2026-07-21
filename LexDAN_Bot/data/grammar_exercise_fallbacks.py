"""
Тема-ориентированные запасные задания Grammar.
Ключ = topic_id из curriculum.

Сначала — проверенные банки (EXTRA + локальные), GPT только если банка нет.
"""

from data.grammar_banks_extra import EXTRA_FALLBACKS

FALLBACKS: dict[str, list[dict]] = {
    "there_is_are": [
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери правильную форму.",
            "sentence_en": "____ a cat on the sofa.",
            "sentence_ru": "На диване есть кот.",
            "options": ["There is", "There are", "It is", "There"],
            "answer": "There is",
            "tip": "Ед. число → There is.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери правильное предложение.",
            "sentence_en": "Which sentence is correct?",
            "sentence_ru": "В комнате две книги.",
            "options": [
                "There are two books in the room.",
                "There is two books in the room.",
                "It are two books in the room.",
                "There two books in the room.",
            ],
            "answer": "There are two books in the room.",
            "tip": "Мн. число → There are.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери верный вариант.",
            "sentence_en": "____ any milk in the fridge?",
            "sentence_ru": "Есть молоко в холодильнике?",
            "options": ["Is there", "Are there", "There is", "There are"],
            "answer": "Is there",
            "tip": "Вопрос + неисчисляемое → Is there…?",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши is или are.",
            "sentence_en": "There ____ (be) three chairs here.",
            "sentence_ru": "Здесь три стула.",
            "base_form": "be",
            "answer": "are",
            "tip": "three chairs = мн. число → are.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши is или are.",
            "sentence_en": "There ____ (be) a park near my house.",
            "sentence_ru": "Рядом с домом есть парк.",
            "base_form": "be",
            "answer": "is",
            "tip": "a park = ед. число → is.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши isn't или aren't.",
            "sentence_en": "There ____ (not be) any apples.",
            "sentence_ru": "Яблок нет.",
            "base_form": "not be",
            "answer": "aren't",
            "tip": "apples = мн. → aren't.",
        },
        {
            "kind": "write",
            "subtype": "translate_en",
            "instruction_ru": "Переведи на английский (There is / There are):",
            "sentence_ru": "В сумке есть телефон.",
            "sentence_en": "",
            "answer": "There is a phone in the bag.",
            "accept": [
                "There is a phone in the bag",
                "There's a phone in the bag.",
                "There's a phone in the bag",
                "There is a phone in a bag.",
                "There's a phone in a bag.",
                "There is a telephone in the bag.",
            ],
            "tip": (
                "Переводи с конца: «в сумке» → in the bag "
                "(конкретная сумка → the). Телефон один → There is."
            ),
        },
        {
            "kind": "write",
            "subtype": "translate_ru",
            "instruction_ru": "Переведи на русский:",
            "sentence_en": "There are five students in the class.",
            "sentence_ru": "В классе пять студентов.",
            "answer": "В классе пять студентов.",
            "accept": [
                "В классе пять учеников.",
                "В классе пять учащихся.",
                "Пять студентов в классе.",
                "Пять учеников в классе.",
                "В классе есть пять студентов.",
                "В классе есть пять учеников.",
            ],
            "tip": "There are = есть (много). students ≈ студенты / ученики.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери верный вариант.",
            "sentence_en": "____ two windows in the room.",
            "sentence_ru": "В комнате два окна.",
            "options": ["There are", "There is", "It is", "There"],
            "answer": "There are",
            "tip": "two windows → There are.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши is или are.",
            "sentence_en": "There ____ a big table in the kitchen.",
            "sentence_ru": "На кухне есть большой стол.",
            "base_form": "be",
            "answer": "is",
            "tip": "a table = ед. → is.",
        },
    ],
    "pronouns_be": [
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери форму to be.",
            "sentence_en": "I ____ a student.",
            "sentence_ru": "Я студент.",
            "options": ["am", "is", "are", "be"],
            "answer": "am",
            "tip": "I → am.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери правильное предложение.",
            "sentence_en": "Which is correct?",
            "sentence_ru": "Она учитель.",
            "options": [
                "She is a teacher.",
                "She am a teacher.",
                "She are a teacher.",
                "She be a teacher.",
            ],
            "answer": "She is a teacher.",
            "tip": "She/he/it → is.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери форму.",
            "sentence_en": "They ____ my friends.",
            "sentence_ru": "Они мои друзья.",
            "options": ["are", "is", "am", "be"],
            "answer": "are",
            "tip": "They/we/you → are.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши am/is/are.",
            "sentence_en": "He ____ (be) happy.",
            "sentence_ru": "Он счастлив.",
            "base_form": "be",
            "answer": "is",
            "tip": "He → is.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши am/is/are.",
            "sentence_en": "We ____ (be) from Russia.",
            "sentence_ru": "Мы из России.",
            "base_form": "be",
            "answer": "are",
            "tip": "We → are.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши aren't или isn't.",
            "sentence_en": "It ____ (not be) cold.",
            "sentence_ru": "Не холодно.",
            "base_form": "not be",
            "answer": "isn't",
            "tip": "It → isn't.",
        },
        {
            "kind": "write",
            "subtype": "translate_en",
            "instruction_ru": "Переведи (am/is/are):",
            "sentence_ru": "Ты мой друг.",
            "sentence_en": "",
            "answer": "You are my friend.",
            "tip": "You → are.",
        },
        {
            "kind": "write",
            "subtype": "translate_ru",
            "instruction_ru": "Переведи на русский:",
            "sentence_en": "I am hungry.",
            "sentence_ru": "Я голодный.",
            "answer": "Я голодный.",
            "tip": "I am = я есть/я …",
        },
    ],
    "can_ability": [
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери правильный вариант.",
            "sentence_en": "I ____ swim.",
            "sentence_ru": "Я умею плавать.",
            "options": ["can", "cans", "can to", "am can"],
            "answer": "can",
            "tip": "can + глагол без to.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери правильное предложение.",
            "sentence_en": "Which is correct?",
            "sentence_ru": "Она не умеет водить.",
            "options": [
                "She can't drive.",
                "She can't to drive.",
                "She can not drives.",
                "She don't can drive.",
            ],
            "answer": "She can't drive.",
            "tip": "can't + V1 без to и без -s.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери вопрос.",
            "sentence_en": "____ you help me?",
            "sentence_ru": "Ты можешь мне помочь?",
            "options": ["Can", "Do can", "Are", "Is"],
            "answer": "Can",
            "tip": "Can + subject + V1?",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши can или can't.",
            "sentence_en": "Birds ____ (can) fly.",
            "sentence_ru": "Птицы умеют летать.",
            "base_form": "can",
            "answer": "can",
            "tip": "умеют = can.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши can или can't — смотри на смысл второй фразы.",
            "sentence_en": "I ____ speak Chinese. I don't know this language at all.",
            "sentence_ru": "Я не умею говорить по-китайски — совсем не знаю язык.",
            "base_form": "can/can't",
            "answer": "can't",
            "accept": ["cannot", "can not"],
            "tip": "Вторая фраза = не знаю язык → can't / cannot.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши can или can't по смыслу.",
            "sentence_en": "Babies ____ walk when they are newborn.",
            "sentence_ru": "Новорождённые малыши ещё не умеют ходить.",
            "base_form": "can/can't",
            "answer": "can't",
            "accept": ["cannot", "can not"],
            "tip": "Новорождённые не ходят → can't.",
        },
        {
            "kind": "write",
            "subtype": "translate_en",
            "instruction_ru": "Переведи (can):",
            "sentence_ru": "Я могу открыть дверь.",
            "sentence_en": "",
            "answer": "I can open the door.",
            "accept": [
                "I can open the door",
                "I can open it",
                "I can open this door",
            ],
            "tip": "can + open.",
        },
        {
            "kind": "write",
            "subtype": "translate_ru",
            "instruction_ru": "Переведи:",
            "sentence_en": "Can you cook?",
            "sentence_ru": "Ты умеешь готовить?",
            "answer": "Ты умеешь готовить?",
            "accept": [
                "Ты можешь готовить?",
                "Умеешь ли ты готовить?",
                "Можешь ли ты готовить?",
            ],
            "tip": "Can you…? = умеешь/можешь…?",
        },
        # банк для итогового теста (9–10)
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери правильный вариант.",
            "sentence_en": "He ____ play the guitar.",
            "sentence_ru": "Он умеет играть на гитаре.",
            "options": ["can", "cans", "can to", "is can"],
            "answer": "can",
            "tip": "can без -s и без to.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши can или can't.",
            "sentence_en": "Fish ____ breathe under water.",
            "sentence_ru": "Рыбы умеют дышать под водой.",
            "base_form": "can/can't",
            "answer": "can",
            "tip": "умеют = can.",
        },
    ],
    "plurals": [
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери мн. число.",
            "sentence_en": "one book → two ____",
            "sentence_ru": "одна книга → две книги",
            "options": ["books", "bookes", "book", "bookies"],
            "answer": "books",
            "tip": "обычно +s.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери правильное.",
            "sentence_en": "Which is correct?",
            "sentence_ru": "две коробки",
            "options": ["two boxes", "two boxs", "two box", "two boxies"],
            "answer": "two boxes",
            "tip": "-x → +es.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери форму.",
            "sentence_en": "one child → two ____",
            "sentence_ru": "один ребёнок → двое детей",
            "options": ["children", "childs", "childes", "child"],
            "answer": "children",
            "tip": "исключение: child → children.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши мн. число.",
            "sentence_en": "I see two ____ (cat).",
            "sentence_ru": "Я вижу двух кошек.",
            "base_form": "cat",
            "answer": "cats",
            "tip": "+s.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши мн. число.",
            "sentence_en": "There are many ____ (city) here.",
            "sentence_ru": "Здесь много городов.",
            "base_form": "city",
            "answer": "cities",
            "tip": "согласная + y → ies.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши мн. число.",
            "sentence_en": "two ____ (man)",
            "sentence_ru": "два мужчины",
            "base_form": "man",
            "answer": "men",
            "tip": "man → men.",
        },
        {
            "kind": "write",
            "subtype": "translate_en",
            "instruction_ru": "Переведи:",
            "sentence_ru": "У меня три яблока.",
            "sentence_en": "",
            "answer": "I have three apples.",
            "accept": [
                "I have three apples",
                "I've got three apples.",
                "I've got three apples",
                "I have 3 apples.",
            ],
            "tip": "apple → apples.",
        },
        {
            "kind": "write",
            "subtype": "translate_ru",
            "instruction_ru": "Переведи:",
            "sentence_en": "These are my books.",
            "sentence_ru": "Это мои книги.",
            "answer": "Это мои книги.",
            "accept": [
                "Это мои книжки.",
                "Вот мои книги.",
                "Эти книги мои.",
            ],
            "tip": "books = книги.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери мн. число (исключение).",
            "sentence_en": "one woman → two ____",
            "sentence_ru": "одна женщина → две женщины",
            "options": ["women", "womans", "womanes", "woman"],
            "answer": "women",
            "tip": "woman → women.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши мн. число (исключение).",
            "sentence_en": "I brushed my ____ (tooth).",
            "sentence_ru": "Я почистил зубы.",
            "base_form": "tooth",
            "answer": "teeth",
            "tip": "tooth → teeth.",
        },
    ],
    "this_that": [
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери this или that.",
            "sentence_en": "____ is my pen (near me).",
            "sentence_ru": "Это моя ручка (рядом).",
            "options": ["This", "That", "These", "Those"],
            "answer": "This",
            "tip": "Близко → This.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери правильное.",
            "sentence_en": "Which is correct?",
            "sentence_ru": "То — машина вон там.",
            "options": [
                "That is a car.",
                "This is a car.",
                "These is a car.",
                "That are a car.",
            ],
            "answer": "That is a car.",
            "tip": "Дальше → That.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери вопрос.",
            "sentence_en": "____ is this?",
            "sentence_ru": "Что это?",
            "options": ["What", "Where", "Who", "When"],
            "answer": "What",
            "tip": "What is this?",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши This или That.",
            "sentence_en": "____ book is on the table next to me.",
            "sentence_ru": "Эта книга на столе рядом со мной.",
            "base_form": "",
            "answer": "This",
            "tip": "Рядом → This.",
        },
        {
            "kind": "write",
            "subtype": "translate_en",
            "instruction_ru": "Переведи (This/That):",
            "sentence_ru": "Это мой телефон.",
            "sentence_en": "",
            "answer": "This is my phone.",
            "tip": "This is…",
        },
        {
            "kind": "write",
            "subtype": "translate_ru",
            "instruction_ru": "Переведи:",
            "sentence_en": "That is a big house.",
            "sentence_ru": "То — большой дом.",
            "answer": "То — большой дом.",
            "tip": "That = то (дальше).",
        },
    ],
    "simple_phrases": [
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери перевод.",
            "sentence_en": "Nice to meet you.",
            "sentence_ru": "",
            "options": [
                "Приятно познакомиться.",
                "Как дела?",
                "Спасибо.",
                "Извини.",
            ],
            "answer": "Приятно познакомиться.",
            "tip": "Знакомство.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Как ответить на How are you?",
            "sentence_en": "How are you?",
            "sentence_ru": "Как дела?",
            "options": ["I'm fine.", "My name is Danil.", "Thank you.", "Sorry."],
            "answer": "I'm fine.",
            "tip": "I am fine / I'm fine.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери фразу.",
            "sentence_en": "Как сказать «Спасибо»?",
            "sentence_ru": "",
            "options": ["Thank you.", "Please.", "Sorry.", "Hello."],
            "answer": "Thank you.",
            "tip": "Thank you.",
        },
        {
            "kind": "write",
            "subtype": "translate_en",
            "instruction_ru": "Переведи:",
            "sentence_ru": "Как тебя зовут?",
            "sentence_en": "",
            "answer": "What is your name?",
            "tip": "What's your name?",
        },
        {
            "kind": "write",
            "subtype": "translate_en",
            "instruction_ru": "Переведи:",
            "sentence_ru": "Меня зовут Анна.",
            "sentence_en": "",
            "answer": "My name is Anna.",
            "tip": "My name is…",
        },
        {
            "kind": "write",
            "subtype": "translate_ru",
            "instruction_ru": "Переведи:",
            "sentence_en": "Hello! How are you?",
            "sentence_ru": "Привет! Как дела?",
            "answer": "Привет! Как дела?",
            "tip": "Hello / Hi.",
        },
    ],
    "articles_a_an": [
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери a или an.",
            "sentence_en": "I see ____ apple.",
            "sentence_ru": "Я вижу яблоко.",
            "options": ["an", "a", "the", "—"],
            "answer": "an",
            "tip": "apple — гласный звук → an.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери a или an.",
            "sentence_en": "She needs ____ pen.",
            "sentence_ru": "Ей нужна ручка.",
            "options": ["a", "an", "the", "—"],
            "answer": "a",
            "tip": "pen — согласный → a.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери правильное.",
            "sentence_en": "Which is correct?",
            "sentence_ru": "университет",
            "options": [
                "a university",
                "an university",
                "a universities",
                "an hour university",
            ],
            "answer": "a university",
            "tip": "university = /juː/ → a.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши a или an.",
            "sentence_en": "It is ____ hour.",
            "sentence_ru": "Это час.",
            "base_form": "",
            "answer": "an",
            "tip": "hour — h немой → an.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Напиши a или an.",
            "sentence_en": "He is ____ doctor.",
            "sentence_ru": "Он врач.",
            "base_form": "",
            "answer": "a",
            "tip": "doctor → a.",
        },
        {
            "kind": "write",
            "subtype": "translate_en",
            "instruction_ru": "Переведи (с a/an):",
            "sentence_ru": "У меня есть книга.",
            "sentence_en": "",
            "answer": "I have a book.",
            "tip": "a book.",
        },
    ],
    "present_simple": [
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери форму.",
            "sentence_en": "She ____ tea every morning.",
            "sentence_ru": "Она пьёт чай каждое утро.",
            "options": ["drinks", "drink", "drinking", "drank"],
            "answer": "drinks",
            "tip": "he/she/it → +s.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери отрицание.",
            "sentence_en": "I ____ like coffee.",
            "sentence_ru": "Я не люблю кофе.",
            "options": ["don't", "doesn't", "am not", "not"],
            "answer": "don't",
            "tip": "I/you/we/they → don't.",
        },
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери вопрос.",
            "sentence_en": "____ you speak English?",
            "sentence_ru": "Ты говоришь по-английски?",
            "options": ["Do", "Does", "Are", "Is"],
            "answer": "Do",
            "tip": "Do + you + V1?",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Поставь глагол в Present Simple.",
            "sentence_en": "He ____ (go) to school every day.",
            "sentence_ru": "Он ходит в школу каждый день.",
            "base_form": "go",
            "answer": "goes",
            "tip": "he → goes.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Поставь don't/doesn't.",
            "sentence_en": "She ____ (not play) football.",
            "sentence_ru": "Она не играет в футбол.",
            "base_form": "not play",
            "answer": "doesn't",
            "tip": "she → doesn't.",
        },
        {
            "kind": "write",
            "subtype": "translate_en",
            "instruction_ru": "Переведи (Present Simple):",
            "sentence_ru": "Я обычно встаю в 7.",
            "sentence_en": "",
            "answer": "I usually get up at 7.",
            "tip": "usually + Present Simple.",
        },
        {
            "kind": "write",
            "subtype": "word_form",
            "instruction_ru": "Поставь глагол в Present Simple.",
            "sentence_en": "They ____ (watch) TV in the evening.",
            "sentence_ru": "Они смотрят телевизор вечером.",
            "base_form": "watch",
            "answer": "watch",
            "tip": "they → без -s.",
        },
        {
            "kind": "write",
            "subtype": "translate_ru",
            "instruction_ru": "Переведи на русский:",
            "sentence_en": "She works in a hospital.",
            "sentence_ru": "Она работает в больнице.",
            "answer": "Она работает в больнице.",
            "tip": "works = работает.",
        },
    ],
}

# Проверенные банки перекрывают старые/короткие (this_that, articles, present_simple, …)
FALLBACKS.update(EXTRA_FALLBACKS)

# Добиваем до ≥10 заданий на тему — пул для итогового теста
_BANK_TOP_UPS: dict[str, list[dict]] = {
    "present_simple": [
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери форму.",
            "sentence_en": "My brother ____ football on Sundays.",
            "sentence_ru": "Мой брат играет в футбол по воскресеньям.",
            "options": ["plays", "play", "playing", "played"],
            "answer": "plays",
            "tip": "he/brother → +s.",
        },
        {
            "kind": "write",
            "subtype": "translate_en",
            "instruction_ru": "Переведи (Present Simple):",
            "sentence_ru": "Она живёт в Москве.",
            "sentence_en": "",
            "answer": "She lives in Moscow.",
            "accept": [
                "She lives in Moscow",
                "She lives in Moskva.",
            ],
            "tip": "she → lives.",
        },
    ],
    "articles_a_an": [
        {
            "kind": "mcq",
            "subtype": "mcq",
            "instruction_ru": "Выбери a или an.",
            "sentence_en": "She is ____ engineer.",
            "sentence_ru": "Она инженер.",
            "options": ["an", "a", "the", "—"],
            "answer": "an",
            "tip": "engineer → гласный звук → an.",
        },
        {
            "kind": "write",
            "subtype": "translate_ru",
            "instruction_ru": "Переведи:",
            "sentence_en": "I need an umbrella.",
            "sentence_ru": "Мне нужен зонт.",
            "answer": "Мне нужен зонт.",
            "accept": [
                "Мне нужна зонтик.",
                "Мне нужен зонтик.",
                "Мне нужен umbrella.",
            ],
            "tip": "an umbrella.",
        },
    ],
}

for _tid, _items in _BANK_TOP_UPS.items():
    bank = FALLBACKS.setdefault(_tid, [])
    if len(bank) < 10:
        bank.extend(_items)

from data.grammar_level_expansion import BANKS as _EXP_BANKS

FALLBACKS.update(_EXP_BANKS)


TOPIC_FOCUS: dict[str, str] = {
    "there_is_are": (
            "ONLY practice There is / There are / Is there / Are there / There isn't / There aren't. "
            "Every item MUST use this construction. NEVER Past Simple visit/visited drills."
        ),
    "pronouns_be": "ONLY I/you/he + am/is/are. Present of to be. Not was/were.",
    "to_be": "ONLY am/is/are (Present of to be). Not was/were.",
    "to_be_past": "ONLY was/were.",
    "this_that": "ONLY this/that (near/far). Prefer This is… / That is…. Avoid Past Simple.",
    "simple_phrases": (
            "ONLY beginner phrases: Hello, Hi, What's your name, My name is, "
            "Nice to meet you, Thank you, Please, Sorry, How are you, I'm fine."
        ),
    "present_simple": "ONLY Present Simple (habits/facts). Not continuous/past.",
    "present_continuous": "ONLY am/is/are + V-ing.",
    "past_simple": "ONLY Past Simple (V2 / was/were) with past time markers.",
    "past_continuous": "ONLY was/were + V-ing.",
    "plurals": "ONLY singular↔plural noun forms.",
    "articles_a_an": "ONLY a/an choice (sound rule). Not the.",
    "can_ability": "ONLY can/can't + verb without to.",
    "have_got": "ONLY have got / has got.",
    "much_many_some_any": "ONLY much/many/some/any.",
    "comparatives": "ONLY comparative/superlative adjectives.",
    "modals_a2": "ONLY must/have to/should/mustn't.",
    "conditionals_0_1": "ONLY zero/first conditional.",
    "passive_basic": "ONLY passive (be + V3).",
    "present_perfect": "ONLY Present Perfect (have/has + V3).",
    "going_to_future": "ONLY be going to + V1.",
    "future_will_going_to": "ONLY will or going to.",
}


def focus_for(topic_id: str | None, topic_title: str) -> str:
    if topic_id and topic_id in TOPIC_FOCUS:
        return TOPIC_FOCUS[topic_id]
    return (
        f"Train ONLY the grammar of topic «{topic_title}». "
        "Do not switch to unrelated tenses."
    )


def get_topic_fallback(topic_id: str | None, exercise_num: int) -> dict | None:
    if not topic_id:
        return None
    bank = FALLBACKS.get(topic_id)
    if not bank:
        return None
    idx = max(0, min(exercise_num - 1, len(bank) - 1))
    return dict(bank[idx])


def looks_on_topic(
    topic_id: str | None, sentence_en: str, options: list | None, answer: str
) -> bool:
    if not topic_id:
        return True
    blob = " ".join(
        [
            (sentence_en or "").lower(),
            (answer or "").lower(),
            " ".join(str(o).lower() for o in (options or [])),
        ]
    )
    padded = f" {blob} "

    # Жёсткий запрет путаницы Present Simple ↔ Continuous
    if topic_id == "present_simple":
        ans = (answer or "").lower()
        # Правильный ответ не должен быть Continuous
        if any(x in ans for x in (" is ", " are ", " am ", "'s ", "'re ", "'m ")) and "ing" in ans:
            return False
        if ans.endswith("ing") and " " not in ans.strip():
            return False
        # Маркеры Simple или do/does / -s у he/she
        ok = any(
            n in padded
            for n in (
                " every ",
                " usually ",
                " often ",
                " always ",
                " don't ",
                " doesn't ",
                " do ",
                " does ",
            )
        )
        return ok or any(
            w in ans for w in ("goes", "works", "likes", "plays", "watches", "reads", "drinks")
        )

    if topic_id == "present_continuous":
        # Не принимать чистый Present Simple с every day как Continuous
        if any(n in padded for n in (" every day", " every morning", " usually ", " often ")):
            if "ing" not in blob and " now" not in padded and " right now" not in padded:
                return False
        return any(n in padded or n in blob for n in (" am ", " is ", " are ", "ing", "now"))

    checks = {
        "there_is_are": (
            "there is",
            "there are",
            "is there",
            "are there",
            "there isn't",
            "there aren't",
            "there's",
        ),
        "can_ability": ("can ", "can't", "cannot"),
        "past_simple": (" yesterday", " ago", " last ", "ed ", " went", " did "),
        "pronouns_be": (" am ", " is ", " are ", "i'm", "she's", "he's", "you're"),
        "to_be": (" am ", " is ", " are ", "i'm", "she's", "he's"),
        "plurals": ("books", "cats", "children", "men", "boxes", "cities"),
        "articles_a_an": (" a ", " an "),
        "this_that": ("this", "that"),
        "simple_phrases": (
            "hello",
            "thank",
            "sorry",
            "please",
            "name",
            "fine",
            "nice to meet",
            "how are you",
        ),
        "past_continuous": (" was ", " were ", "ing"),
        "present_perfect": (" have ", " has ", " already", " yet", " ever", " never"),
        "going_to_future": ("going to",),
    }
    needles = checks.get(topic_id)
    if not needles:
        return True
    return any(n in padded or n in blob for n in needles)
