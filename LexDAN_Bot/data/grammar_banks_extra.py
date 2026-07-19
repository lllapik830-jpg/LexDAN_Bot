# -*- coding: utf-8 -*-
"""Curated grammar exercise banks (8 per topic). Preferred over GPT."""

EXTRA_FALLBACKS = {
  "this_that": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери this или that.",
      "sentence_en": "____ is my pen (near me).",
      "sentence_ru": "Это моя ручка (рядом).",
      "options": [
        "This",
        "That",
        "These",
        "Those"
      ],
      "answer": "This",
      "tip": "Близко → This."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "То — машина вон там.",
      "options": [
        "That is a car.",
        "This are a car.",
        "These is a car.",
        "That are a car."
      ],
      "answer": "That is a car.",
      "tip": "Дальше → That is."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери вопрос.",
      "sentence_en": "____ is this?",
      "sentence_ru": "Что это?",
      "options": [
        "What",
        "Where",
        "Who",
        "When"
      ],
      "answer": "What",
      "tip": "What is this?"
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши This или That.",
      "sentence_en": "____ book is on the table next to me.",
      "sentence_ru": "Эта книга рядом со мной.",
      "base_form": "",
      "answer": "This",
      "tip": "Рядом → This.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши This или That.",
      "sentence_en": "Look over there! ____ is a big dog.",
      "sentence_ru": "Вон там большая собака.",
      "base_form": "",
      "answer": "That",
      "tip": "Дальше → That.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши This или That.",
      "sentence_en": "____ is my bag here.",
      "sentence_ru": "Это моя сумка здесь.",
      "base_form": "",
      "answer": "This",
      "tip": "Here → This.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи (This/That):",
      "sentence_ru": "Это мой телефон.",
      "sentence_en": "",
      "answer": "This is my phone.",
      "tip": "This is…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи на русский:",
      "sentence_en": "That is a big house.",
      "sentence_ru": "То — большой дом.",
      "answer": "То — большой дом.",
      "tip": "That = то (дальше).",
      "options": None
    }
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
        "Извини."
      ],
      "answer": "Приятно познакомиться.",
      "tip": "Знакомство."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Как ответить на How are you?",
      "sentence_en": "How are you?",
      "sentence_ru": "Как дела?",
      "options": [
        "I'm fine.",
        "My name is Danil.",
        "Thank you.",
        "Sorry."
      ],
      "answer": "I'm fine.",
      "tip": "I'm fine."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Как сказать «Спасибо»?",
      "sentence_en": "Choose the phrase.",
      "sentence_ru": "",
      "options": [
        "Thank you.",
        "Please.",
        "Sorry.",
        "Hello."
      ],
      "answer": "Thank you.",
      "tip": "Thank you."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши приветствие Hello или Hi.",
      "sentence_en": "____! My name is Anna.",
      "sentence_ru": "Привет! Меня зовут Анна.",
      "base_form": "",
      "answer": "Hello",
      "tip": "Hello / Hi.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Дополни фразу.",
      "sentence_en": "Nice to ____ you.",
      "sentence_ru": "Приятно познакомиться.",
      "base_form": "meet",
      "answer": "meet",
      "tip": "Nice to meet you.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Дополни фразу.",
      "sentence_en": "What is your ____?",
      "sentence_ru": "Как тебя зовут?",
      "base_form": "name",
      "answer": "name",
      "tip": "What's your name?",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Как тебя зовут?",
      "sentence_en": "",
      "answer": "What is your name?",
      "tip": "What's your name?",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "Hello! How are you?",
      "sentence_ru": "Привет! Как дела?",
      "answer": "Привет! Как дела?",
      "tip": "Hello / Hi.",
      "options": None
    }
  ],
  "articles_a_an": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери a или an.",
      "sentence_en": "I see ____ apple.",
      "sentence_ru": "Я вижу яблоко.",
      "options": [
        "an",
        "a",
        "the",
        "some"
      ],
      "answer": "an",
      "tip": "apple — гласный звук → an."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери a или an.",
      "sentence_en": "She needs ____ pen.",
      "sentence_ru": "Ей нужна ручка.",
      "options": [
        "a",
        "an",
        "the",
        "some"
      ],
      "answer": "a",
      "tip": "pen — согласный → a."
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
        "an hour university"
      ],
      "answer": "a university",
      "tip": "university = /juː/ → a."
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
      "options": None
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
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши a или an.",
      "sentence_en": "I need ____ umbrella.",
      "sentence_ru": "Мне нужен зонт.",
      "base_form": "",
      "answer": "an",
      "tip": "umbrella → an.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи (с a/an):",
      "sentence_ru": "У меня есть книга.",
      "sentence_en": "",
      "answer": "I have a book.",
      "tip": "a book.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи на русский:",
      "sentence_en": "She has an orange.",
      "sentence_ru": "У неё есть апельсин.",
      "answer": "У неё есть апельсин.",
      "tip": "an orange.",
      "options": None
    }
  ],
  "present_simple": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильную форму Present Simple.",
      "sentence_en": "She ____ to school by bus every day.",
      "sentence_ru": "Она ездит в школу на автобусе каждый день.",
      "options": [
        "goes",
        "go",
        "going",
        "went"
      ],
      "answer": "goes",
      "tip": "he/she/it → goes."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери грамматически правильное предложение (Present Simple).",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Она читает книги каждый вечер.",
      "options": [
        "She reads books every evening.",
        "She is reading books every evening.",
        "She reading books every evening.",
        "She read books every evening."
      ],
      "answer": "She reads books every evening.",
      "tip": "every evening → Present Simple, не Continuous."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери вопрос в Present Simple.",
      "sentence_en": "____ you speak English?",
      "sentence_ru": "Ты говоришь по-английски?",
      "options": [
        "Do",
        "Does",
        "Are",
        "Is"
      ],
      "answer": "Do",
      "tip": "Do + you + V1?"
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
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Поставь don't или doesn't.",
      "sentence_en": "She ____ (not play) football.",
      "sentence_ru": "Она не играет в футбол.",
      "base_form": "not play",
      "answer": "doesn't",
      "tip": "she → doesn't.",
      "options": None
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
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи (Present Simple):",
      "sentence_ru": "Я обычно встаю в 7.",
      "sentence_en": "",
      "answer": "I usually get up at 7.",
      "tip": "usually + Present Simple.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи на русский:",
      "sentence_en": "She works in a hospital.",
      "sentence_ru": "Она работает в больнице.",
      "answer": "Она работает в больнице.",
      "tip": "works = работает.",
      "options": None
    }
  ],
  "present_continuous": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильную форму Present Continuous.",
      "sentence_en": "She ____ watching a film now.",
      "sentence_ru": "Она сейчас смотрит фильм.",
      "options": [
        "is",
        "are",
        "am",
        "be"
      ],
      "answer": "is",
      "tip": "she → is + V-ing."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение (Present Continuous).",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Мы сейчас учим английский.",
      "options": [
        "We are learning English now.",
        "We learn English now.",
        "We is learning English now.",
        "We learning English now."
      ],
      "answer": "We are learning English now.",
      "tip": "now → are + V-ing."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму to be.",
      "sentence_en": "I ____ reading a book right now.",
      "sentence_ru": "Я сейчас читаю книгу.",
      "options": [
        "am",
        "is",
        "are",
        "be"
      ],
      "answer": "am",
      "tip": "I → am + V-ing."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши форму V-ing.",
      "sentence_en": "Look! He is ____ (run) in the park.",
      "sentence_ru": "Смотри! Он бегает в парке.",
      "base_form": "run",
      "answer": "running",
      "tip": "run → running.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши am / is / are.",
      "sentence_en": "They ____ (be) playing football now.",
      "sentence_ru": "Они сейчас играют в футбол.",
      "base_form": "be",
      "answer": "are",
      "tip": "they → are.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши isn't или aren't.",
      "sentence_en": "She ____ (not be) sleeping.",
      "sentence_ru": "Она не спит.",
      "base_form": "not be",
      "answer": "isn't",
      "tip": "she → isn't.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи (Present Continuous):",
      "sentence_ru": "Я сейчас пишу сообщение.",
      "sentence_en": "",
      "answer": "I am writing a message now.",
      "tip": "I am + writing.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи на русский:",
      "sentence_en": "They are cooking dinner now.",
      "sentence_ru": "Они сейчас готовят ужин.",
      "answer": "Они сейчас готовят ужин.",
      "tip": "are cooking = готовят.",
      "options": None
    }
  ],
  "past_simple": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери Past Simple.",
      "sentence_en": "Yesterday I ____ to the park.",
      "sentence_ru": "Вчера я ходил в парк.",
      "options": [
        "went",
        "go",
        "goes",
        "going"
      ],
      "answer": "went",
      "tip": "go → went."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение (Past Simple).",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Она вчера смотрела фильм.",
      "options": [
        "She watched a film yesterday.",
        "She watches a film yesterday.",
        "She is watching a film yesterday.",
        "She watch a film yesterday."
      ],
      "answer": "She watched a film yesterday.",
      "tip": "yesterday → Past Simple."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери вопрос в Past Simple.",
      "sentence_en": "____ you see him last week?",
      "sentence_ru": "Ты видел его на прошлой неделе?",
      "options": [
        "Did",
        "Do",
        "Does",
        "Are"
      ],
      "answer": "Did",
      "tip": "Did + subject + V1?"
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Поставь глагол в Past Simple.",
      "sentence_en": "She ____ (visit) London last year.",
      "sentence_ru": "Она ездила в Лондон в прошлом году.",
      "base_form": "visit",
      "answer": "visited",
      "tip": "regular: +ed.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Поставь didn't.",
      "sentence_en": "He ____ (not come) to the party.",
      "sentence_ru": "Он не пришёл на вечеринку.",
      "base_form": "not come",
      "answer": "didn't",
      "tip": "didn't + V1.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Поставь форму was/were.",
      "sentence_en": "They ____ (be) happy yesterday.",
      "sentence_ru": "Они были счастливы вчера.",
      "base_form": "be",
      "answer": "were",
      "tip": "they → were.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи (Past Simple):",
      "sentence_ru": "Я вчера купил книгу.",
      "sentence_en": "",
      "answer": "I bought a book yesterday.",
      "tip": "buy → bought.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "We lived in Moscow two years ago.",
      "sentence_ru": "Мы жили в Москве два года назад.",
      "answer": "Мы жили в Москве два года назад.",
      "tip": "lived = жили.",
      "options": None
    }
  ],
  "going_to_future": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму be going to.",
      "sentence_en": "I ____ going to call you later.",
      "sentence_ru": "Я собираюсь позвонить тебе позже.",
      "options": [
        "am",
        "is",
        "are",
        "be"
      ],
      "answer": "am",
      "tip": "I → am going to."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Они собираются путешествовать.",
      "options": [
        "They are going to travel.",
        "They is going to travel.",
        "They going to travel.",
        "They go to travel."
      ],
      "answer": "They are going to travel.",
      "tip": "they → are going to."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильный вариант.",
      "sentence_en": "She is going ____ start a new job.",
      "sentence_ru": "Она собирается начать новую работу.",
      "options": [
        "to",
        "for",
        "at",
        "in"
      ],
      "answer": "to",
      "tip": "going to + V1."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши am/is/are.",
      "sentence_en": "We ____ (be) going to buy a car.",
      "sentence_ru": "Мы собираемся купить машину.",
      "base_form": "be",
      "answer": "are",
      "tip": "we → are.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши глагол V1.",
      "sentence_en": "He is going to ____ (study) medicine.",
      "sentence_ru": "Он собирается изучать медицину.",
      "base_form": "study",
      "answer": "study",
      "tip": "going to + V1.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши isn't/aren't.",
      "sentence_en": "It ____ (not be) going to rain.",
      "sentence_ru": "Не собирается идти дождь.",
      "base_form": "not be",
      "answer": "isn't",
      "tip": "it → isn't.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи (going to):",
      "sentence_ru": "Я собираюсь готовить ужин.",
      "sentence_en": "",
      "answer": "I am going to cook dinner.",
      "tip": "I am going to + V1.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "She is going to visit her grandma.",
      "sentence_ru": "Она собирается навестить бабушку.",
      "answer": "Она собирается навестить бабушку.",
      "tip": "is going to = собирается.",
      "options": None
    }
  ],
  "much_many_some_any": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери much или many.",
      "sentence_en": "How ____ apples do you want?",
      "sentence_ru": "Сколько яблок ты хочешь?",
      "options": [
        "many",
        "much",
        "a",
        "any"
      ],
      "answer": "many",
      "tip": "apples = исчисляемые → many."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "У меня мало молока.",
      "options": [
        "I don't have much milk.",
        "I don't have many milk.",
        "I don't have much milks.",
        "I don't have many milks."
      ],
      "answer": "I don't have much milk.",
      "tip": "milk = неисчисляемое → much."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери some или any.",
      "sentence_en": "I don't have ____ money.",
      "sentence_ru": "У меня нет денег.",
      "options": [
        "any",
        "some",
        "much",
        "a"
      ],
      "answer": "any",
      "tip": "отрицание → any."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши much или many.",
      "sentence_en": "There isn't ____ sugar.",
      "sentence_ru": "Сахара мало / нет.",
      "base_form": "",
      "answer": "much",
      "tip": "sugar → much.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши some или any.",
      "sentence_en": "Have you got ____ friends here?",
      "sentence_ru": "У тебя есть друзья здесь?",
      "base_form": "",
      "answer": "any",
      "tip": "вопрос → any.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши some или any.",
      "sentence_en": "Would you like ____ tea?",
      "sentence_ru": "Хочешь чаю?",
      "base_form": "",
      "answer": "some",
      "tip": "предложение → some.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "У меня много друзей.",
      "sentence_en": "",
      "answer": "I have many friends.",
      "tip": "friends → many.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "Is there any water?",
      "sentence_ru": "Есть вода?",
      "answer": "Есть вода?",
      "tip": "any в вопросе.",
      "options": None
    }
  ],
  "comparatives": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери сравнительную степень.",
      "sentence_en": "This book is ____ than that one.",
      "sentence_ru": "Эта книга интереснее той.",
      "options": [
        "more interesting",
        "most interesting",
        "interestinger",
        "as interesting"
      ],
      "answer": "more interesting",
      "tip": "длинные прил. → more + adj."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Мой брат выше меня.",
      "options": [
        "My brother is taller than me.",
        "My brother is more tall than me.",
        "My brother is tallest than me.",
        "My brother is as taller me."
      ],
      "answer": "My brother is taller than me.",
      "tip": "tall → taller."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери превосходную степень.",
      "sentence_en": "This is the ____ day of my life.",
      "sentence_ru": "Это лучший день в моей жизни.",
      "options": [
        "best",
        "better",
        "good",
        "more good"
      ],
      "answer": "best",
      "tip": "good → better → best."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши сравнительную степень.",
      "sentence_en": "She is ____ (young) than her sister.",
      "sentence_ru": "Она моложе сестры.",
      "base_form": "young",
      "answer": "younger",
      "tip": "young → younger.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши превосходную степень.",
      "sentence_en": "He is the ____ (fast) runner.",
      "sentence_ru": "Он самый быстрый бегун.",
      "base_form": "fast",
      "answer": "fastest",
      "tip": "the + -est.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши more/most.",
      "sentence_en": "This task is ____ difficult.",
      "sentence_ru": "Это задание сложнее.",
      "base_form": "",
      "answer": "more",
      "tip": "more + difficult.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Этот дом больше того.",
      "sentence_en": "",
      "answer": "This house is bigger than that one.",
      "tip": "big → bigger.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "She is the smartest student.",
      "sentence_ru": "Она самая умная ученица.",
      "answer": "Она самая умная ученица.",
      "tip": "the smartest.",
      "options": None
    }
  ],
  "modals_a2": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери модальный глагол.",
      "sentence_en": "You ____ wear a seatbelt. It's the law.",
      "sentence_ru": "Ты должен пристегнуться. Это закон.",
      "options": [
        "must",
        "should",
        "can",
        "might"
      ],
      "answer": "must",
      "tip": "закон / обязанность → must."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Тебе следует больше спать.",
      "options": [
        "You should sleep more.",
        "You should to sleep more.",
        "You must to sleep more.",
        "You should sleeping more."
      ],
      "answer": "You should sleep more.",
      "tip": "should + V1 без to."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери запрет.",
      "sentence_en": "You ____ smoke here.",
      "sentence_ru": "Здесь нельзя курить.",
      "options": [
        "mustn't",
        "must",
        "should",
        "can"
      ],
      "answer": "mustn't",
      "tip": "запрет → mustn't."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши must или have to.",
      "sentence_en": "I ____ (must) finish this today.",
      "sentence_ru": "Я должен закончить это сегодня.",
      "base_form": "must",
      "answer": "must",
      "tip": "must + V1.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши should.",
      "sentence_en": "You ____ (should) call your mum.",
      "sentence_ru": "Тебе стоит позвонить маме.",
      "base_form": "should",
      "answer": "should",
      "tip": "should + V1.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши don't have to.",
      "sentence_en": "You ____ (not have to) come if you're busy.",
      "sentence_ru": "Тебе не обязательно приходить.",
      "base_form": "not have to",
      "answer": "don't have to",
      "tip": "нет обязанности.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Ты должен сделать домашку.",
      "sentence_en": "",
      "answer": "You must do your homework.",
      "tip": "must + V1.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "You shouldn't be late.",
      "sentence_ru": "Тебе не следует опаздывать.",
      "answer": "Тебе не следует опаздывать.",
      "tip": "shouldn't.",
      "options": None
    }
  ],
  "present_perfect": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери Present Perfect.",
      "sentence_en": "I ____ finished my homework.",
      "sentence_ru": "Я закончил домашку.",
      "options": [
        "have",
        "has",
        "had",
        "am"
      ],
      "answer": "have",
      "tip": "I/you/we/they → have + V3."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Она уже видела этот фильм.",
      "options": [
        "She has already seen this film.",
        "She have already seen this film.",
        "She has already saw this film.",
        "She already see this film."
      ],
      "answer": "She has already seen this film.",
      "tip": "she → has + V3."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери since или for.",
      "sentence_en": "We have lived here ____ 2020.",
      "sentence_ru": "Мы живём здесь с 2020.",
      "options": [
        "since",
        "for",
        "from",
        "at"
      ],
      "answer": "since",
      "tip": "since + точка во времени."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши have или has.",
      "sentence_en": "He ____ (have) lost his keys.",
      "sentence_ru": "Он потерял ключи.",
      "base_form": "have",
      "answer": "has",
      "tip": "he → has.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши V3.",
      "sentence_en": "They have ____ (write) three emails.",
      "sentence_ru": "Они написали три письма.",
      "base_form": "write",
      "answer": "written",
      "tip": "write → written.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши haven't/hasn't.",
      "sentence_en": "She ____ (not have) arrived yet.",
      "sentence_ru": "Она ещё не приехала.",
      "base_form": "not have",
      "answer": "hasn't",
      "tip": "she → hasn't.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи (Present Perfect):",
      "sentence_ru": "Я никогда не был в Лондоне.",
      "sentence_en": "",
      "answer": "I have never been to London.",
      "tip": "have + never + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "Have you ever eaten sushi?",
      "sentence_ru": "Ты когда-нибудь ел суши?",
      "answer": "Ты когда-нибудь ел суши?",
      "tip": "Have you ever…?",
      "options": None
    }
  ],
  "past_perfect": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери Past Perfect.",
      "sentence_en": "When I arrived, the train ____ already left.",
      "sentence_ru": "Когда я приехал, поезд уже ушёл.",
      "options": [
        "had",
        "has",
        "have",
        "was"
      ],
      "answer": "had",
      "tip": "had + V3 — раньше другого прошлого."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Он сказал, что уже поел.",
      "options": [
        "He said he had already eaten.",
        "He said he has already eaten.",
        "He said he already eat.",
        "He said he was already eaten."
      ],
      "answer": "He said he had already eaten.",
      "tip": "Past Perfect после said."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму.",
      "sentence_en": "She ____ never seen snow before that day.",
      "sentence_ru": "До того дня она никогда не видела снег.",
      "options": [
        "had",
        "has",
        "have",
        "was"
      ],
      "answer": "had",
      "tip": "had never + V3."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши had.",
      "sentence_en": "They ____ (have) finished before we came.",
      "sentence_ru": "Они закончили до нашего прихода.",
      "base_form": "have",
      "answer": "had",
      "tip": "had + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши V3.",
      "sentence_en": "I had ____ (leave) when she called.",
      "sentence_ru": "Я уже ушёл, когда она позвонила.",
      "base_form": "leave",
      "answer": "left",
      "tip": "leave → left.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши hadn't.",
      "sentence_en": "We ____ (not have) met before.",
      "sentence_ru": "Мы не встречались раньше.",
      "base_form": "not have",
      "answer": "hadn't",
      "tip": "hadn't + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "К тому времени я уже сделал работу.",
      "sentence_en": "",
      "answer": "By then I had already done the work.",
      "tip": "had + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "She had gone home before midnight.",
      "sentence_ru": "Она ушла домой до полуночи.",
      "answer": "Она ушла домой до полуночи.",
      "tip": "had gone.",
      "options": None
    }
  ],
  "past_continuous": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери Past Continuous.",
      "sentence_en": "Yesterday at 5 I ____ watching TV.",
      "sentence_ru": "Вчера в 5 я смотрел телевизор.",
      "options": [
        "was",
        "were",
        "am",
        "is"
      ],
      "answer": "was",
      "tip": "I → was + V-ing."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Пока шёл дождь, мы сидели дома.",
      "options": [
        "While it was raining, we were sitting at home.",
        "While it rained, we was sitting at home.",
        "While it was rain, we sat at home.",
        "While it were raining, we sit at home."
      ],
      "answer": "While it was raining, we were sitting at home.",
      "tip": "was/were + V-ing."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму.",
      "sentence_en": "They ____ playing football when I saw them.",
      "sentence_ru": "Они играли в футбол, когда я их увидел.",
      "options": [
        "were",
        "was",
        "are",
        "is"
      ],
      "answer": "were",
      "tip": "they → were."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши was/were.",
      "sentence_en": "She ____ (be) cooking when the phone rang.",
      "sentence_ru": "Она готовила, когда зазвонил телефон.",
      "base_form": "be",
      "answer": "was",
      "tip": "she → was.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши V-ing.",
      "sentence_en": "We were ____ (drive) to work.",
      "sentence_ru": "Мы ехали на работу.",
      "base_form": "drive",
      "answer": "driving",
      "tip": "drive → driving.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши wasn't/weren't.",
      "sentence_en": "He ____ (not be) sleeping at midnight.",
      "sentence_ru": "Он не спал в полночь.",
      "base_form": "not be",
      "answer": "wasn't",
      "tip": "he → wasn't.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "В 8 вечера я читал.",
      "sentence_en": "",
      "answer": "At 8 pm I was reading.",
      "tip": "was + V-ing.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "They were talking about the trip.",
      "sentence_ru": "Они говорили о поездке.",
      "answer": "Они говорили о поездке.",
      "tip": "were talking.",
      "options": None
    }
  ],
  "conditionals_0_1": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери First Conditional.",
      "sentence_en": "If it rains, we ____ stay home.",
      "sentence_ru": "Если будет дождь, мы останемся дома.",
      "options": [
        "will",
        "would",
        "are",
        "did"
      ],
      "answer": "will",
      "tip": "If + Present, will + V1."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Если ты греешь лёд, он тает.",
      "options": [
        "If you heat ice, it melts.",
        "If you will heat ice, it melts.",
        "If you heat ice, it will melts.",
        "If you heated ice, it melt."
      ],
      "answer": "If you heat ice, it melts.",
      "tip": "Zero Conditional: Present + Present."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму в if-части.",
      "sentence_en": "If she ____ free, she will come.",
      "sentence_ru": "Если она будет свободна, она придёт.",
      "options": [
        "is",
        "will be",
        "was",
        "be"
      ],
      "answer": "is",
      "tip": "в if — Present, не will."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши will или Present.",
      "sentence_en": "If I see him, I ____ (tell) him.",
      "sentence_ru": "Если увижу его, скажу.",
      "base_form": "tell",
      "answer": "will tell",
      "tip": "will + V1.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши Present в if.",
      "sentence_en": "If water ____ (boil), it turns into steam.",
      "sentence_ru": "Если вода кипит…",
      "base_form": "boil",
      "answer": "boils",
      "tip": "Zero: Present.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши don't/doesn't.",
      "sentence_en": "If it ____ (not rain), we will go out.",
      "sentence_ru": "Если не будет дождя…",
      "base_form": "not rain",
      "answer": "doesn't",
      "tip": "it → doesn't.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Если я буду свободен, я позвоню.",
      "sentence_en": "",
      "answer": "If I am free, I will call.",
      "tip": "If + Present, will.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "If you study, you will pass.",
      "sentence_ru": "Если будешь учиться, сдашь.",
      "answer": "Если будешь учиться, сдашь.",
      "tip": "First Conditional.",
      "options": None
    }
  ],
  "gerund_infinitive": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери герундий или инфинитив.",
      "sentence_en": "I enjoy ____ books.",
      "sentence_ru": "Мне нравится читать книги.",
      "options": [
        "reading",
        "to read",
        "read",
        "reads"
      ],
      "answer": "reading",
      "tip": "enjoy + V-ing."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Она решила уехать.",
      "options": [
        "She decided to leave.",
        "She decided leaving.",
        "She decided leave.",
        "She decided to leaving."
      ],
      "answer": "She decided to leave.",
      "tip": "decide + to V1."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму.",
      "sentence_en": "He wants ____ a doctor.",
      "sentence_ru": "Он хочет стать врачом.",
      "options": [
        "to be",
        "being",
        "be",
        "been"
      ],
      "answer": "to be",
      "tip": "want + to V1."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши V-ing.",
      "sentence_en": "Stop ____ (talk), please.",
      "sentence_ru": "Перестань говорить.",
      "base_form": "talk",
      "answer": "talking",
      "tip": "stop + V-ing.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши to + V1.",
      "sentence_en": "I hope ____ (see) you soon.",
      "sentence_ru": "Надеюсь увидеть тебя скоро.",
      "base_form": "see",
      "answer": "to see",
      "tip": "hope + to V1.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши V-ing.",
      "sentence_en": "She is good at ____ (cook).",
      "sentence_ru": "Она хорошо готовит.",
      "base_form": "cook",
      "answer": "cooking",
      "tip": "good at + V-ing.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Я люблю плавать.",
      "sentence_en": "",
      "answer": "I like swimming.",
      "tip": "like + V-ing (или to swim).",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "They agreed to help us.",
      "sentence_ru": "Они согласились помочь нам.",
      "answer": "Они согласились помочь нам.",
      "tip": "agree + to V1.",
      "options": None
    }
  ],
  "passive_basic": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери Passive.",
      "sentence_en": "This letter ____ written by Anna.",
      "sentence_ru": "Это письмо написано Анной.",
      "options": [
        "was",
        "were",
        "is being",
        "has"
      ],
      "answer": "was",
      "tip": "was/were + V3."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Английский говорят во многих странах.",
      "options": [
        "English is spoken in many countries.",
        "English is speak in many countries.",
        "English spoken in many countries.",
        "English are spoken in many countries."
      ],
      "answer": "English is spoken in many countries.",
      "tip": "is + V3."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери V3.",
      "sentence_en": "The cake was ____ by my mum.",
      "sentence_ru": "Торт был сделан мамой.",
      "options": [
        "made",
        "make",
        "making",
        "makes"
      ],
      "answer": "made",
      "tip": "make → made."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши is/are/was/were.",
      "sentence_en": "These phones ____ (be) made in China.",
      "sentence_ru": "Эти телефоны сделаны в Китае.",
      "base_form": "be",
      "answer": "are",
      "tip": "phones → are + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши V3.",
      "sentence_en": "The window was ____ (break) yesterday.",
      "sentence_ru": "Окно разбили вчера.",
      "base_form": "break",
      "answer": "broken",
      "tip": "break → broken.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши isn't/aren't.",
      "sentence_en": "The museum ____ (not be) open on Mondays.",
      "sentence_ru": "Музей не открыт по понедельникам.",
      "base_form": "not be",
      "answer": "isn't",
      "tip": "Passive Present.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи (Passive):",
      "sentence_ru": "Дверь была открыта.",
      "sentence_en": "",
      "answer": "The door was opened.",
      "tip": "was + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "The book was written in 1990.",
      "sentence_ru": "Книга была написана в 1990.",
      "answer": "Книга была написана в 1990.",
      "tip": "was written.",
      "options": None
    }
  ],
  "relative_clauses_b1": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери who/which/that.",
      "sentence_en": "The woman ____ lives next door is a doctor.",
      "sentence_ru": "Женщина, которая живёт рядом, — врач.",
      "options": [
        "who",
        "which",
        "where",
        "whose"
      ],
      "answer": "who",
      "tip": "люди → who."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Книга, которую я читаю, интересная.",
      "options": [
        "The book which I am reading is interesting.",
        "The book who I am reading is interesting.",
        "The book where I am reading is interesting.",
        "The book whose I am reading is interesting."
      ],
      "answer": "The book which I am reading is interesting.",
      "tip": "вещи → which/that."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери whose.",
      "sentence_en": "This is the man ____ car was stolen.",
      "sentence_ru": "Это мужчина, чью машину украли.",
      "options": [
        "whose",
        "who",
        "which",
        "whom"
      ],
      "answer": "whose",
      "tip": "чьё → whose."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши who или which.",
      "sentence_en": "The dog ____ (which) barked is mine.",
      "sentence_ru": "Собака, которая лаяла, моя.",
      "base_form": "which",
      "answer": "which",
      "tip": "животные/вещи → which.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши where.",
      "sentence_en": "This is the city ____ I was born.",
      "sentence_ru": "Это город, где я родился.",
      "base_form": "",
      "answer": "where",
      "tip": "место → where.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши that/who.",
      "sentence_en": "People ____ help others are kind.",
      "sentence_ru": "Люди, которые помогают…",
      "base_form": "",
      "answer": "who",
      "tip": "people → who.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Это дом, в котором я живу.",
      "sentence_en": "",
      "answer": "This is the house where I live.",
      "tip": "where для места.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "The girl who called you is my sister.",
      "sentence_ru": "Девушка, которая тебе звонила, — моя сестра.",
      "answer": "Девушка, которая тебе звонила, — моя сестра.",
      "tip": "who.",
      "options": None
    }
  ],
  "present_perfect_continuous": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери Present Perfect Continuous.",
      "sentence_en": "I ____ been waiting for an hour.",
      "sentence_ru": "Я жду уже час.",
      "options": [
        "have",
        "has",
        "had",
        "am"
      ],
      "answer": "have",
      "tip": "have/has been + V-ing."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Она учит английский уже два года.",
      "options": [
        "She has been learning English for two years.",
        "She have been learning English for two years.",
        "She has been learn English for two years.",
        "She is learning English for two years."
      ],
      "answer": "She has been learning English for two years.",
      "tip": "has been + V-ing + for."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери for или since.",
      "sentence_en": "They have been working here ____ Monday.",
      "sentence_ru": "Они работают здесь с понедельника.",
      "options": [
        "since",
        "for",
        "from",
        "at"
      ],
      "answer": "since",
      "tip": "since + точка."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши have/has.",
      "sentence_en": "He ____ (have) been running all morning.",
      "sentence_ru": "Он бегает всё утро.",
      "base_form": "have",
      "answer": "has",
      "tip": "he → has.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши V-ing.",
      "sentence_en": "We have been ____ (talk) for hours.",
      "sentence_ru": "Мы говорим уже часы.",
      "base_form": "talk",
      "answer": "talking",
      "tip": "been + V-ing.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши haven't/hasn't.",
      "sentence_en": "She ____ (not have) been feeling well.",
      "sentence_ru": "Она плохо себя чувствует.",
      "base_form": "not have",
      "answer": "hasn't",
      "tip": "hasn't been + V-ing.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Я читаю с утра.",
      "sentence_en": "",
      "answer": "I have been reading since morning.",
      "tip": "have been + V-ing.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "It has been raining all day.",
      "sentence_ru": "Весь день идёт дождь.",
      "answer": "Весь день идёт дождь.",
      "tip": "has been raining.",
      "options": None
    }
  ],
  "conditionals_2_3": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери Second Conditional.",
      "sentence_en": "If I ____ rich, I would travel the world.",
      "sentence_ru": "Если бы я был богат, я бы путешествовал.",
      "options": [
        "were",
        "was",
        "am",
        "will be"
      ],
      "answer": "were",
      "tip": "If + Past, would + V1 (were для всех)."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери Third Conditional.",
      "sentence_en": "If she had studied, she ____ passed.",
      "sentence_ru": "Если бы она училась, она бы сдала.",
      "options": [
        "would have",
        "would",
        "will have",
        "had"
      ],
      "answer": "would have",
      "tip": "If + Past Perfect, would have + V3."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Если бы у меня было время, я бы помог.",
      "options": [
        "If I had time, I would help.",
        "If I have time, I would help.",
        "If I had time, I will help.",
        "If I would have time, I helped."
      ],
      "answer": "If I had time, I would help.",
      "tip": "Second Conditional."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши would.",
      "sentence_en": "If I lived closer, I ____ (visit) more often.",
      "sentence_ru": "Если бы жил ближе…",
      "base_form": "visit",
      "answer": "would visit",
      "tip": "would + V1.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши had + V3.",
      "sentence_en": "If we ____ (leave) earlier, we would have caught the train.",
      "sentence_ru": "Если бы уехали раньше…",
      "base_form": "leave",
      "answer": "had left",
      "tip": "Third: had + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши would have.",
      "sentence_en": "He ____ (pass) if he had tried harder.",
      "sentence_ru": "Он бы сдал…",
      "base_form": "pass",
      "answer": "would have passed",
      "tip": "would have + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Если бы я знал, я бы сказал.",
      "sentence_en": "",
      "answer": "If I knew, I would tell.",
      "tip": "Second Conditional.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "If I had known, I would have called.",
      "sentence_ru": "Если бы я знал, я бы позвонил.",
      "answer": "Если бы я знал, я бы позвонил.",
      "tip": "Third Conditional.",
      "options": None
    }
  ],
  "reported_speech": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери Reported Speech.",
      "sentence_en": "She said she ____ tired.",
      "sentence_ru": "Она сказала, что устала.",
      "options": [
        "was",
        "is",
        "were",
        "be"
      ],
      "answer": "was",
      "tip": "Present → Past при согласовании времён."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Он сказал, что живёт в Париже.",
      "options": [
        "He said that he lived in Paris.",
        "He said that he lives in Paris.",
        "He said that he live in Paris.",
        "He told that he lived in Paris."
      ],
      "answer": "He said that he lived in Paris.",
      "tip": "said that + Past."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери местоимение.",
      "sentence_en": "Tom said, 'I am busy.' → Tom said that ____ was busy.",
      "sentence_ru": "Том сказал, что занят.",
      "options": [
        "he",
        "I",
        "she",
        "they"
      ],
      "answer": "he",
      "tip": "I → he."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши Past форму.",
      "sentence_en": "She said she ____ (can) swim.",
      "sentence_ru": "Она сказала, что умеет плавать.",
      "base_form": "can",
      "answer": "could",
      "tip": "can → could.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши will→would.",
      "sentence_en": "He said he ____ (will) call later.",
      "sentence_ru": "Он сказал, что позвонит.",
      "base_form": "will",
      "answer": "would",
      "tip": "will → would.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши told или said.",
      "sentence_en": "She ____ me that she was ready.",
      "sentence_ru": "Она сказала мне…",
      "base_form": "",
      "answer": "told",
      "tip": "told + object.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Она сказала, что устала.",
      "sentence_en": "",
      "answer": "She said that she was tired.",
      "tip": "said that + Past.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "He told me he had finished.",
      "sentence_ru": "Он сказал мне, что закончил.",
      "answer": "Он сказал мне, что закончил.",
      "tip": "told me.",
      "options": None
    }
  ],
  "passives_advanced": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери сложный Passive.",
      "sentence_en": "The problem is being ____ now.",
      "sentence_ru": "Проблему сейчас решают.",
      "options": [
        "discussed",
        "discuss",
        "discussing",
        "discusses"
      ],
      "answer": "discussed",
      "tip": "is being + V3."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Ему дали подарок.",
      "options": [
        "He was given a present.",
        "He was gave a present.",
        "He given a present.",
        "A present was gave him."
      ],
      "answer": "He was given a present.",
      "tip": "was + V3 (ditransitive)."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму.",
      "sentence_en": "The documents have been ____.",
      "sentence_ru": "Документы были подписаны.",
      "options": [
        "signed",
        "sign",
        "signing",
        "signs"
      ],
      "answer": "signed",
      "tip": "have been + V3."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши being + V3.",
      "sentence_en": "The house is being ____ (paint).",
      "sentence_ru": "Дом красят.",
      "base_form": "paint",
      "answer": "painted",
      "tip": "is being painted.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши been + V3.",
      "sentence_en": "All tickets have been ____ (sell).",
      "sentence_ru": "Все билеты проданы.",
      "base_form": "sell",
      "answer": "sold",
      "tip": "have been sold.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши was/were.",
      "sentence_en": "I ____ (be) told to wait.",
      "sentence_ru": "Мне сказали ждать.",
      "base_form": "be",
      "answer": "was",
      "tip": "I was told.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Отчёт должен быть отправлен завтра.",
      "sentence_en": "",
      "answer": "The report must be sent tomorrow.",
      "tip": "modal + be + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "The decision has been made.",
      "sentence_ru": "Решение принято.",
      "answer": "Решение принято.",
      "tip": "has been made.",
      "options": None
    }
  ],
  "modals_deduction": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери модальный вывод.",
      "sentence_en": "He ____ be at home — the lights are on.",
      "sentence_ru": "Он, должно быть, дома — свет горит.",
      "options": [
        "must",
        "can't",
        "should",
        "may not"
      ],
      "answer": "must",
      "tip": "уверенность → must."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Она не может быть усталой — она только начала.",
      "options": [
        "She can't be tired — she's just started.",
        "She mustn't be tired — she's just started.",
        "She must not to be tired.",
        "She can't to be tired."
      ],
      "answer": "She can't be tired — she's just started.",
      "tip": "невозможно → can't."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери might.",
      "sentence_en": "They ____ be late — the traffic is bad.",
      "sentence_ru": "Они, возможно, опоздают.",
      "options": [
        "might",
        "must",
        "can't",
        "should"
      ],
      "answer": "might",
      "tip": "вероятность → might/may."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши must/can't/might.",
      "sentence_en": "That ____ (must) be a joke.",
      "sentence_ru": "Это, должно быть, шутка.",
      "base_form": "must",
      "answer": "must",
      "tip": "must be.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши have.",
      "sentence_en": "She must ____ (have) forgotten.",
      "sentence_ru": "Она, должно быть, забыла.",
      "base_form": "have",
      "answer": "have",
      "tip": "must have + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши been.",
      "sentence_en": "He can't have ____ (be) serious.",
      "sentence_ru": "Он не мог быть серьёзным.",
      "base_form": "be",
      "answer": "been",
      "tip": "can't have been.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Это, должно быть, правда.",
      "sentence_en": "",
      "answer": "That must be true.",
      "tip": "must be.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "She might have left already.",
      "sentence_ru": "Она, возможно, уже ушла.",
      "answer": "Она, возможно, уже ушла.",
      "tip": "might have + V3.",
      "options": None
    }
  ],
  "relative_advanced": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери non-defining clause.",
      "sentence_en": "My brother, ____ lives in Berlin, is a designer.",
      "sentence_ru": "Мой брат, который живёт в Берлине, дизайнер.",
      "options": [
        "who",
        "that",
        "which",
        "whom"
      ],
      "answer": "who",
      "tip": "после запятой that нельзя."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Париж, который я посетил, прекрасен.",
      "options": [
        "Paris, which I visited, is beautiful.",
        "Paris, that I visited, is beautiful.",
        "Paris which I visited is beautiful.",
        "Paris, who I visited, is beautiful."
      ],
      "answer": "Paris, which I visited, is beautiful.",
      "tip": "non-defining: which + commas."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери whom/who.",
      "sentence_en": "The colleague with ____ I work is helpful.",
      "sentence_ru": "Коллега, с которым я работаю…",
      "options": [
        "whom",
        "which",
        "whose",
        "where"
      ],
      "answer": "whom",
      "tip": "после предлога → whom."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши which.",
      "sentence_en": "The report, ____ was late, annoyed the boss.",
      "sentence_ru": "Отчёт, который опоздал…",
      "base_form": "",
      "answer": "which",
      "tip": "which + commas.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши whose.",
      "sentence_en": "The author ____ novel won a prize is here.",
      "sentence_ru": "Автор, чей роман…",
      "base_form": "",
      "answer": "whose",
      "tip": "whose.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши to whom / who.",
      "sentence_en": "The person ____ I spoke was polite. (formal: to whom)",
      "sentence_ru": "",
      "base_form": "",
      "answer": "to whom",
      "tip": "formal: to whom.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Мой друг, который живёт в Италии, приезжает.",
      "sentence_en": "",
      "answer": "My friend, who lives in Italy, is coming.",
      "tip": "non-defining who.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "The hotel, which is near the station, is cheap.",
      "sentence_ru": "Отель, который рядом с вокзалом, дешёвый.",
      "answer": "Отель, который рядом с вокзалом, дешёвый.",
      "tip": "which.",
      "options": None
    }
  ],
  "inversion": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери инверсию.",
      "sentence_en": "Rarely ____ such a beautiful view.",
      "sentence_ru": "Редко я видел такой вид.",
      "options": [
        "have I seen",
        "I have seen",
        "I saw",
        "did I saw"
      ],
      "answer": "have I seen",
      "tip": "Rarely + вспомогательный + subject."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Никогда раньше я не чувствовал себя так.",
      "options": [
        "Never before have I felt like this.",
        "Never before I have felt like this.",
        "Never before I felt like this.",
        "Never before did I felt like this."
      ],
      "answer": "Never before have I felt like this.",
      "tip": "Never + inversion."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму.",
      "sentence_en": "Not only ____ late, but he also forgot the keys.",
      "sentence_ru": "Он не только опоздал…",
      "options": [
        "was he",
        "he was",
        "did he was",
        "he"
      ],
      "answer": "was he",
      "tip": "Not only + inversion."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши инверсию do/does/did.",
      "sentence_en": "Only then ____ (do) I understand.",
      "sentence_ru": "Только тогда я понял.",
      "base_form": "do",
      "answer": "did",
      "tip": "Only then + did.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши have/had.",
      "sentence_en": "Hardly ____ (have) we arrived when it started to rain.",
      "sentence_ru": "Едва мы приехали…",
      "base_form": "have",
      "answer": "had",
      "tip": "Hardly had…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши should.",
      "sentence_en": "Should you ____ (need) help, call me.",
      "sentence_ru": "Если понадобится помощь…",
      "base_form": "need",
      "answer": "need",
      "tip": "Should you need…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Никогда я не видел ничего подобного.",
      "sentence_en": "",
      "answer": "Never have I seen anything like this.",
      "tip": "Never + inversion.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "Seldom do we meet such kindness.",
      "sentence_ru": "Редко мы встречаем такую доброту.",
      "answer": "Редко мы встречаем такую доброту.",
      "tip": "Seldom do…",
      "options": None
    }
  ],
  "cleft_sentences": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери cleft sentence.",
      "sentence_en": "____ was John who called you.",
      "sentence_ru": "Именно Джон тебе звонил.",
      "options": [
        "It",
        "That",
        "There",
        "This"
      ],
      "answer": "It",
      "tip": "It was X who/that…"
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Именно в пятницу мы уезжаем.",
      "options": [
        "It is on Friday that we are leaving.",
        "It is on Friday which we are leaving.",
        "It on Friday that we are leaving.",
        "Is it on Friday we leaving."
      ],
      "answer": "It is on Friday that we are leaving.",
      "tip": "It is + focus + that…"
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери What-cleft.",
      "sentence_en": "____ I need is a quiet place.",
      "sentence_ru": "Что мне нужно — тихое место.",
      "options": [
        "What",
        "That",
        "Which",
        "Who"
      ],
      "answer": "What",
      "tip": "What I need is…"
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши who/that.",
      "sentence_en": "It was Maria ____ helped me.",
      "sentence_ru": "Именно Мария помогла.",
      "base_form": "",
      "answer": "who",
      "tip": "who для людей.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши that.",
      "sentence_en": "It was yesterday ____ everything changed.",
      "sentence_ru": "Именно вчера всё изменилось.",
      "base_form": "",
      "answer": "that",
      "tip": "that после времени.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши is/was.",
      "sentence_en": "What matters ____ honesty.",
      "sentence_ru": "Что важно — честность.",
      "base_form": "",
      "answer": "is",
      "tip": "What… is…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Именно ты должен решить.",
      "sentence_en": "",
      "answer": "It is you who must decide.",
      "tip": "It is you who…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "What surprised me was his honesty.",
      "sentence_ru": "Что меня удивило — его честность.",
      "answer": "Что меня удивило — его честность.",
      "tip": "What… was…",
      "options": None
    }
  ],
  "advanced_modals": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери модальность.",
      "sentence_en": "You ____ have told me earlier!",
      "sentence_ru": "Тебе следовало сказать раньше!",
      "options": [
        "should",
        "must",
        "can",
        "will"
      ],
      "answer": "should",
      "tip": "should have + V3 — упрёк."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Мне не нужно было приходить (но я пришёл).",
      "options": [
        "I needn't have come.",
        "I didn't need to come.",
        "I mustn't have come.",
        "I shouldn't come have."
      ],
      "answer": "I needn't have come.",
      "tip": "needn't have = сделал зря."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму.",
      "sentence_en": "She ____ have been at the meeting — I saw her.",
      "sentence_ru": "Она, должно быть, была на встрече.",
      "options": [
        "must",
        "should",
        "can't",
        "would"
      ],
      "answer": "must",
      "tip": "must have + V3 — вывод о прошлом."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши have.",
      "sentence_en": "You should ____ (have) asked for help.",
      "sentence_ru": "Тебе следовало попросить помощи.",
      "base_form": "have",
      "answer": "have",
      "tip": "should have + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши been.",
      "sentence_en": "He might have ____ (be) joking.",
      "sentence_ru": "Он, возможно, шутил.",
      "base_form": "be",
      "answer": "been",
      "tip": "might have been.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши needn't.",
      "sentence_en": "You ____ (need not) have bought so much food.",
      "sentence_ru": "Не нужно было столько еды покупать.",
      "base_form": "need not",
      "answer": "needn't",
      "tip": "needn't have.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Тебе не следовало врать.",
      "sentence_en": "",
      "answer": "You shouldn't have lied.",
      "tip": "shouldn't have + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "They must have left already.",
      "sentence_ru": "Они, должно быть, уже ушли.",
      "answer": "Они, должно быть, уже ушли.",
      "tip": "must have.",
      "options": None
    }
  ],
  "participle_clauses": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери participle clause.",
      "sentence_en": "____ the door, she left the room.",
      "sentence_ru": "Закрыв дверь, она вышла.",
      "options": [
        "Closing",
        "Closed",
        "Close",
        "Closes"
      ],
      "answer": "Closing",
      "tip": "V-ing = одновременное действие."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Написав письмо, он отправил его.",
      "options": [
        "Having written the letter, he sent it.",
        "Writing the letter, he has sent it.",
        "Written the letter, he send it.",
        "Having write the letter, he sent it."
      ],
      "answer": "Having written the letter, he sent it.",
      "tip": "Having + V3 — раньше."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму.",
      "sentence_en": "The man ____ by the window is my uncle.",
      "sentence_ru": "Мужчина, сидящий у окна — мой дядя.",
      "options": [
        "sitting",
        "sat",
        "sits",
        "sit"
      ],
      "answer": "sitting",
      "tip": "reduced relative: sitting."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши V-ing.",
      "sentence_en": "____ (Look) at the map, I found the street.",
      "sentence_ru": "Глядя на карту…",
      "base_form": "Look",
      "answer": "Looking",
      "tip": "Looking…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши Having + V3.",
      "sentence_en": "____ (finish) dinner, we went for a walk.",
      "sentence_ru": "Поужинав…",
      "base_form": "finish",
      "answer": "Having finished",
      "tip": "Having + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши V3 participle.",
      "sentence_en": "____ (Build) in 1890, the house is historic.",
      "sentence_ru": "Построенный в 1890…",
      "base_form": "Build",
      "answer": "Built",
      "tip": "Built in…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Открыв окно, она вдохнула свежий воздух.",
      "sentence_en": "",
      "answer": "Opening the window, she breathed fresh air.",
      "tip": "V-ing clause.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "Shocked by the news, he sat down.",
      "sentence_ru": "Потрясённый новостью, он сел.",
      "answer": "Потрясённый новостью, он сел.",
      "tip": "V3 clause.",
      "options": None
    }
  ],
  "nominalisation": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери номинализацию.",
      "sentence_en": "The ____ of the project took two years.",
      "sentence_ru": "Разработка проекта заняла два года.",
      "options": [
        "development",
        "develop",
        "developing",
        "developed"
      ],
      "answer": "development",
      "tip": "глагол → существительное."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери более формальный вариант.",
      "sentence_en": "Which is more formal?",
      "sentence_ru": "",
      "options": [
        "There was a significant increase in sales.",
        "Sales went up a lot.",
        "Sales got bigger.",
        "Sales jumped up."
      ],
      "answer": "There was a significant increase in sales.",
      "tip": "increase = номинализация."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери существительное.",
      "sentence_en": "Her sudden ____ surprised everyone.",
      "sentence_ru": "Её внезапный уход всех удивил.",
      "options": [
        "departure",
        "depart",
        "departing",
        "departed"
      ],
      "answer": "departure",
      "tip": "depart → departure."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши существительное.",
      "sentence_en": "The ____ (decide) was difficult.",
      "sentence_ru": "Решение было трудным.",
      "base_form": "decide",
      "answer": "decision",
      "tip": "decide → decision.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши существительное.",
      "sentence_en": "We need a clear ____ (explain).",
      "sentence_ru": "Нужно ясное объяснение.",
      "base_form": "explain",
      "answer": "explanation",
      "tip": "explain → explanation.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши существительное.",
      "sentence_en": "His ____ (refuse) shocked us.",
      "sentence_ru": "Его отказ нас шокировал.",
      "base_form": "refuse",
      "answer": "refusal",
      "tip": "refuse → refusal.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи формально:",
      "sentence_ru": "Продажи сильно выросли.",
      "sentence_en": "",
      "answer": "There was a sharp rise in sales.",
      "tip": "rise = существительное.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "The failure of the plan was obvious.",
      "sentence_ru": "Провал плана был очевиден.",
      "answer": "Провал плана был очевиден.",
      "tip": "failure.",
      "options": None
    }
  ],
  "discourse_markers": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери связку.",
      "sentence_en": "I was tired. ____, I finished the work.",
      "sentence_ru": "Я устал. Тем не менее, закончил работу.",
      "options": [
        "Nevertheless",
        "Because",
        "So that",
        "Unless"
      ],
      "answer": "Nevertheless",
      "tip": "Nevertheless = тем не менее."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Кроме того, это дёшево.",
      "options": [
        "Moreover, it is cheap.",
        "Moreover it cheap.",
        "Moreover, it cheap is.",
        "Moreover it is cheaply."
      ],
      "answer": "Moreover, it is cheap.",
      "tip": "Moreover + comma."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери маркер результата.",
      "sentence_en": "It rained hard. ____, the match was cancelled.",
      "sentence_ru": "Шёл сильный дождь. Поэтому матч отменили.",
      "options": [
        "Therefore",
        "Although",
        "Whereas",
        "Despite"
      ],
      "answer": "Therefore",
      "tip": "Therefore = поэтому."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши However.",
      "sentence_en": "I like the idea. ____, it is expensive.",
      "sentence_ru": "Идея нравится. Однако дорого.",
      "base_form": "",
      "answer": "However",
      "tip": "However,",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши Although.",
      "sentence_en": "____ it was late, we continued.",
      "sentence_ru": "Хотя было поздно…",
      "base_form": "",
      "answer": "Although",
      "tip": "Although + clause.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши In addition.",
      "sentence_en": "____, we need more time.",
      "sentence_ru": "Кроме того, нужно больше времени.",
      "base_form": "",
      "answer": "In addition",
      "tip": "In addition,",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Тем не менее, я согласен.",
      "sentence_en": "",
      "answer": "Nevertheless, I agree.",
      "tip": "Nevertheless,",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "As a result, prices rose.",
      "sentence_ru": "В результате цены выросли.",
      "answer": "В результате цены выросли.",
      "tip": "As a result.",
      "options": None
    }
  ],
  "stylistic_inversion": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери стилистическую инверсию.",
      "sentence_en": "So rare ____ the opportunity that we took it.",
      "sentence_ru": "Возможность была столь редкой, что мы ею воспользовались.",
      "options": [
        "was",
        "it was",
        "is",
        "were it"
      ],
      "answer": "was",
      "tip": "So + adj + verb + subject."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Такова была его реакция.",
      "options": [
        "Such was his reaction.",
        "Such his reaction was.",
        "Such was reaction his.",
        "His reaction such was."
      ],
      "answer": "Such was his reaction.",
      "tip": "Such was…"
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму.",
      "sentence_en": "Little ____ he know what was coming.",
      "sentence_ru": "Мало он знал, что будет.",
      "options": [
        "did",
        "does",
        "was",
        "had"
      ],
      "answer": "did",
      "tip": "Little did he know…"
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши did.",
      "sentence_en": "Not until midnight ____ (do) they leave.",
      "sentence_ru": "Только в полночь они ушли.",
      "base_form": "do",
      "answer": "did",
      "tip": "Not until… did…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши had.",
      "sentence_en": "No sooner ____ (have) I sat down than the phone rang.",
      "sentence_ru": "Едва я сел…",
      "base_form": "have",
      "answer": "had",
      "tip": "No sooner had…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши comes.",
      "sentence_en": "Here ____ the bus!",
      "sentence_ru": "Вот и автобус!",
      "base_form": "",
      "answer": "comes",
      "tip": "Here comes…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Мало он понимал опасность.",
      "sentence_en": "",
      "answer": "Little did he understand the danger.",
      "tip": "Little did…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "Such was the impact of her words.",
      "sentence_ru": "Таково было влияние её слов.",
      "answer": "Таково было влияние её слов.",
      "tip": "Such was…",
      "options": None
    }
  ],
  "subtle_modality": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери тонкую модальность.",
      "sentence_en": "You ____ want to check the figures again.",
      "sentence_ru": "Возможно, тебе стоит ещё раз проверить цифры.",
      "options": [
        "might",
        "must",
        "shall",
        "needn't"
      ],
      "answer": "might",
      "tip": "вежливый совет → might want to."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Кажется, он опоздал.",
      "options": [
        "He appears to have been late.",
        "He appears to be late yesterday.",
        "He appears late have been.",
        "He appear to have been late."
      ],
      "answer": "He appears to have been late.",
      "tip": "appears to have + V3."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери would.",
      "sentence_en": "I ____ imagine that's the best option.",
      "sentence_ru": "Полагаю, это лучший вариант.",
      "options": [
        "would",
        "must",
        "can",
        "shall"
      ],
      "answer": "would",
      "tip": "I would imagine… — мягко."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши seem.",
      "sentence_en": "They ____ (seem) to be avoiding us.",
      "sentence_ru": "Кажется, они нас избегают.",
      "base_form": "seem",
      "answer": "seem",
      "tip": "seem to…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши tend.",
      "sentence_en": "She ____ (tend) to overthink things.",
      "sentence_ru": "Она склонна усложнять.",
      "base_form": "tend",
      "answer": "tends",
      "tip": "tends to.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши may well.",
      "sentence_en": "He ____ be right.",
      "sentence_ru": "Он вполне может быть прав.",
      "base_form": "",
      "answer": "may well",
      "tip": "may well + V1.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи мягко:",
      "sentence_ru": "Возможно, стоит подождать.",
      "sentence_en": "",
      "answer": "You might want to wait.",
      "tip": "might want to.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "She would appear to be mistaken.",
      "sentence_ru": "Похоже, она ошибается.",
      "answer": "Похоже, она ошибается.",
      "tip": "would appear.",
      "options": None
    }
  ],
  "mixed_conditionals": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери mixed conditional.",
      "sentence_en": "If I had taken that job, I ____ rich now.",
      "sentence_ru": "Если бы я тогда взял работу, сейчас был бы богат.",
      "options": [
        "would be",
        "would have been",
        "will be",
        "am"
      ],
      "answer": "would be",
      "tip": "прошлое условие → настоящий результат."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Если бы он был умнее, он бы не сделал ту ошибку.",
      "options": [
        "If he were smarter, he wouldn't have made that mistake.",
        "If he is smarter, he wouldn't have made that mistake.",
        "If he were smarter, he won't make that mistake.",
        "If he had been smarter, he wouldn't make that mistake yesterday only."
      ],
      "answer": "If he were smarter, he wouldn't have made that mistake.",
      "tip": "настоящее условие → прошлый результат."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери форму.",
      "sentence_en": "If she ____ more careful, she wouldn't be in trouble now.",
      "sentence_ru": "Если бы она была осторожнее…",
      "options": [
        "had been",
        "was being",
        "is",
        "would be"
      ],
      "answer": "had been",
      "tip": "Past Perfect в if + would now."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши would be.",
      "sentence_en": "If I had saved money, I ____ freer now.",
      "sentence_ru": "Если бы копил, сейчас был бы свободнее.",
      "base_form": "",
      "answer": "would be",
      "tip": "mixed.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши had + V3.",
      "sentence_en": "If he ____ (listen), he wouldn't be lost now.",
      "sentence_ru": "Если бы послушал…",
      "base_form": "listen",
      "answer": "had listened",
      "tip": "had + V3.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши wouldn't have.",
      "sentence_en": "If I were you, I ____ (not say) that yesterday.",
      "sentence_ru": "На твоём месте я бы того не сказал.",
      "base_form": "not say",
      "answer": "wouldn't have said",
      "tip": "mixed.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Если бы я тогда учился, сейчас у меня была бы работа.",
      "sentence_en": "",
      "answer": "If I had studied then, I would have a job now.",
      "tip": "mixed conditional.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "If I were taller, I would have joined the team last year.",
      "sentence_ru": "Если бы я был выше, я бы вступил в команду в прошлом году.",
      "answer": "Если бы я был выше, я бы вступил в команду в прошлом году.",
      "tip": "mixed.",
      "options": None
    }
  ],
  "ellipsis_substitution": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери эллипсис/замену.",
      "sentence_en": "I like tea and so ____ my sister.",
      "sentence_ru": "Я люблю чай, и сестра тоже.",
      "options": [
        "does",
        "is",
        "likes",
        "do"
      ],
      "answer": "does",
      "tip": "so + auxiliary + subject."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Я тоже не хочу.",
      "options": [
        "Neither do I.",
        "Neither I do.",
        "So do I not.",
        "I neither."
      ],
      "answer": "Neither do I.",
      "tip": "Neither + aux + subject."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери one/ones.",
      "sentence_en": "I need a pen. Pass me the blue ____.",
      "sentence_ru": "Мне нужна ручка. Передай синюю.",
      "options": [
        "one",
        "ones",
        "it",
        "them"
      ],
      "answer": "one",
      "tip": "one заменяет существительное."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши do/does/did.",
      "sentence_en": "She works hard and so ____ he.",
      "sentence_ru": "Она много работает, и он тоже.",
      "base_form": "",
      "answer": "does",
      "tip": "so does he.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши one.",
      "sentence_en": "Which bag do you want? The red ____.",
      "sentence_ru": "Какую сумку? Красную.",
      "base_form": "",
      "answer": "one",
      "tip": "the red one.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши so.",
      "sentence_en": "A: I'm tired. B: ____ am I.",
      "sentence_ru": "Я тоже.",
      "base_form": "",
      "answer": "So",
      "tip": "So am I.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи:",
      "sentence_ru": "Я тоже.",
      "sentence_en": "",
      "answer": "So do I.",
      "tip": "So + aux + I.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "Neither have we.",
      "sentence_ru": "Мы тоже нет.",
      "answer": "Мы тоже нет.",
      "tip": "Neither…",
      "options": None
    }
  ],
  "register_control": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери более формальный вариант.",
      "sentence_en": "Which is more formal?",
      "sentence_ru": "",
      "options": [
        "I would be grateful if you could reply soon.",
        "Can you reply ASAP?",
        "Reply quick, yeah?",
        "Hit me up soon."
      ],
      "answer": "I would be grateful if you could reply soon.",
      "tip": "формальный регистр."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери нейтральный деловой тон.",
      "sentence_en": "Which sentence fits a work email?",
      "sentence_ru": "",
      "options": [
        "Please find attached the report.",
        "Here's the stuff lol.",
        "I dumped the file here.",
        "Yo, check this."
      ],
      "answer": "Please find attached the report.",
      "tip": "деловая формула."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери смягчение.",
      "sentence_en": "____ you open the window?",
      "sentence_ru": "Не могли бы вы открыть окно?",
      "options": [
        "Could",
        "Open",
        "You must",
        "Hey"
      ],
      "answer": "Could",
      "tip": "Could you…? вежливо."
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши We regret.",
      "sentence_en": "____ to inform you that the event is cancelled.",
      "sentence_ru": "К сожалению сообщаем…",
      "base_form": "",
      "answer": "We regret",
      "tip": "We regret to…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши further.",
      "sentence_en": "Should you require ____ information, contact us.",
      "sentence_ru": "Если нужна доп. информация…",
      "base_form": "",
      "answer": "further",
      "tip": "further information.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши Appreciate.",
      "sentence_en": "We ____ your patience.",
      "sentence_ru": "Мы ценим ваше терпение.",
      "base_form": "",
      "answer": "appreciate",
      "tip": "We appreciate…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи формально:",
      "sentence_ru": "Напишите нам как можно скорее.",
      "sentence_en": "",
      "answer": "Please contact us at your earliest convenience.",
      "tip": "формальный клише.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "I look forward to hearing from you.",
      "sentence_ru": "С нетерпением жду вашего ответа.",
      "answer": "С нетерпением жду вашего ответа.",
      "tip": "look forward to.",
      "options": None
    }
  ],
  "pragmatic_softening": [
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери смягчённую формулировку.",
      "sentence_en": "Which is softer?",
      "sentence_ru": "",
      "options": [
        "I was wondering if you could help.",
        "Help me now.",
        "You have to help.",
        "Help!"
      ],
      "answer": "I was wondering if you could help.",
      "tip": "I was wondering if… — мягко."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери правильное предложение.",
      "sentence_en": "Which sentence is correct?",
      "sentence_ru": "Как бы неловко сказать…",
      "options": [
        "This might sound awkward, but…",
        "This might sounding awkward, but…",
        "This must sound awkwardly, but…",
        "This can sounds awkward, but…"
      ],
      "answer": "This might sound awkward, but…",
      "tip": "might sound — смягчение."
    },
    {
      "kind": "mcq",
      "subtype": "mcq",
      "instruction_ru": "Выбери hedged opinion.",
      "sentence_en": "____ say that the plan needs work.",
      "sentence_ru": "Я бы сказал, что план нужно доработать.",
      "options": [
        "I'd",
        "I must",
        "I will",
        "I"
      ],
      "answer": "I'd",
      "tip": "I'd say…"
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши perhaps.",
      "sentence_en": "____ we could meet tomorrow.",
      "sentence_ru": "Возможно, встретимся завтра.",
      "base_form": "",
      "answer": "Perhaps",
      "tip": "Perhaps…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши sort of.",
      "sentence_en": "It's ____ complicated.",
      "sentence_ru": "Это вроде как сложно.",
      "base_form": "",
      "answer": "sort of",
      "tip": "sort of.",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "word_form",
      "instruction_ru": "Напиши seem.",
      "sentence_en": "You ____ a bit upset.",
      "sentence_ru": "Ты выглядишь немного расстроенным.",
      "base_form": "",
      "answer": "seem",
      "tip": "You seem…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_en",
      "instruction_ru": "Переведи мягко:",
      "sentence_ru": "Мне кажется, это ошибка.",
      "sentence_en": "",
      "answer": "It seems to me that this is a mistake.",
      "tip": "It seems to me…",
      "options": None
    },
    {
      "kind": "write",
      "subtype": "translate_ru",
      "instruction_ru": "Переведи:",
      "sentence_en": "Would you mind closing the door?",
      "sentence_ru": "Вы не против закрыть дверь?",
      "answer": "Вы не против закрыть дверь?",
      "tip": "Would you mind…",
      "options": None
    }
  ]
}
