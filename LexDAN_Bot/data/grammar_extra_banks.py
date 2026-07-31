"""
Доп. задания Grammar A1–C2 (по 100 шт. на уровень).
A0 не использует этот банк.
Сгенерировано scripts/_gen_grammar_extra_banks.py
"""

from __future__ import annotations

import json

_RAW = r"""{
  "A1": [
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She go to school every day.",
      "answer": "She goes to school every day.",
      "accept": [
        "She goes to school every day"
      ],
      "example": "She goes to school every day.",
      "id": 1
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He like pizza.",
      "answer": "He likes pizza.",
      "accept": [
        "He likes pizza"
      ],
      "example": "He likes pizza.",
      "id": 2
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "It work well.",
      "answer": "It works well.",
      "accept": [
        "It works well"
      ],
      "example": "It works well.",
      "id": 3
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "My brother play football.",
      "answer": "My brother plays football.",
      "accept": [
        "My brother plays football"
      ],
      "example": "My brother plays football.",
      "id": 4
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "The cat sleep on the sofa.",
      "answer": "The cat sleeps on the sofa.",
      "accept": [
        "The cat sleeps on the sofa"
      ],
      "example": "The cat sleeps on the sofa.",
      "id": 5
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Tom want a new phone.",
      "answer": "Tom wants a new phone.",
      "accept": [
        "Tom wants a new phone"
      ],
      "example": "Tom wants a new phone.",
      "id": 6
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Anna live in London.",
      "answer": "Anna lives in London.",
      "accept": [
        "Anna lives in London"
      ],
      "example": "Anna lives in London.",
      "id": 7
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "The dog run in the park.",
      "answer": "The dog runs in the park.",
      "accept": [
        "The dog runs in the park"
      ],
      "example": "The dog runs in the park.",
      "id": 8
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She watch TV at night.",
      "answer": "She watches TV at night.",
      "accept": [
        "She watches TV at night"
      ],
      "example": "She watches TV at night.",
      "id": 9
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He study English.",
      "answer": "He studies English.",
      "accept": [
        "He studies English"
      ],
      "example": "He studies English.",
      "id": 10
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Mary teach maths.",
      "answer": "Mary teaches maths.",
      "accept": [
        "Mary teaches maths"
      ],
      "example": "Mary teaches maths.",
      "id": 11
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "John wash the car.",
      "answer": "John washes the car.",
      "accept": [
        "John washes the car"
      ],
      "example": "John washes the car.",
      "id": 12
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She do her homework.",
      "answer": "She does her homework.",
      "accept": [
        "She does her homework"
      ],
      "example": "She does her homework.",
      "id": 13
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He have two sisters.",
      "answer": "He has two sisters.",
      "accept": [
        "He has two sisters"
      ],
      "example": "He has two sisters.",
      "id": 14
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "My friend have a bike.",
      "answer": "My friend has a bike.",
      "accept": [
        "My friend has a bike"
      ],
      "example": "My friend has a bike.",
      "id": 15
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I is happy.",
      "answer": "I am happy.",
      "accept": [
        "I am happy"
      ],
      "example": "I am happy.",
      "id": 16
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He am a doctor.",
      "answer": "He is a doctor.",
      "accept": [
        "He is a doctor"
      ],
      "example": "He is a doctor.",
      "id": 17
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "They is students.",
      "answer": "They are students.",
      "accept": [
        "They are students"
      ],
      "example": "They are students.",
      "id": 18
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "We is ready.",
      "answer": "We are ready.",
      "accept": [
        "We are ready"
      ],
      "example": "We are ready.",
      "id": 19
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She are my sister.",
      "answer": "She is my sister.",
      "accept": [
        "She is my sister"
      ],
      "example": "She is my sister.",
      "id": 20
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "You is late.",
      "answer": "You are late.",
      "accept": [
        "You are late"
      ],
      "example": "You are late.",
      "id": 21
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "It are a book.",
      "answer": "It is a book.",
      "accept": [
        "It is a book"
      ],
      "example": "It is a book.",
      "id": 22
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I are tired.",
      "answer": "I am tired.",
      "accept": [
        "I am tired"
      ],
      "example": "I am tired.",
      "id": 23
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Tom am at home.",
      "answer": "Tom is at home.",
      "accept": [
        "Tom is at home"
      ],
      "example": "Tom is at home.",
      "id": 24
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "The books is new.",
      "answer": "The books are new.",
      "accept": [
        "The books are new"
      ],
      "example": "The books are new.",
      "id": 25
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I have a apple.",
      "answer": "I have an apple.",
      "accept": [
        "I have an apple"
      ],
      "example": "I have an apple.",
      "id": 26
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She is a engineer.",
      "answer": "She is an engineer.",
      "accept": [
        "She is an engineer"
      ],
      "example": "She is an engineer.",
      "id": 27
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He bought a umbrella.",
      "answer": "He bought an umbrella.",
      "accept": [
        "He bought an umbrella"
      ],
      "example": "He bought an umbrella.",
      "id": 28
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "This is a honest man.",
      "answer": "This is an honest man.",
      "accept": [
        "This is an honest man"
      ],
      "example": "This is an honest man.",
      "id": 29
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I need a hour.",
      "answer": "I need an hour.",
      "accept": [
        "I need an hour"
      ],
      "example": "I need an hour.",
      "id": 30
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She has an book.",
      "answer": "She has a book.",
      "accept": [
        "She has a book"
      ],
      "example": "She has a book.",
      "id": 31
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He is an teacher.",
      "answer": "He is a teacher.",
      "accept": [
        "He is a teacher"
      ],
      "example": "He is a teacher.",
      "id": 32
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I saw an dog.",
      "answer": "I saw a dog.",
      "accept": [
        "I saw a dog"
      ],
      "example": "I saw a dog.",
      "id": 33
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "We need a orange.",
      "answer": "We need an orange.",
      "accept": [
        "We need an orange"
      ],
      "example": "We need an orange.",
      "id": 34
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "It is a interesting film.",
      "answer": "It is an interesting film.",
      "accept": [
        "It is an interesting film"
      ],
      "example": "It is an interesting film.",
      "id": 35
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I have two book.",
      "answer": "I have two books.",
      "accept": [
        "I have two books"
      ],
      "example": "I have two books.",
      "id": 36
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "There is three cats.",
      "answer": "There are three cats.",
      "accept": [
        "There are three cats"
      ],
      "example": "There are three cats.",
      "id": 37
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "There are a car.",
      "answer": "There is a car.",
      "accept": [
        "There is a car"
      ],
      "example": "There is a car.",
      "id": 38
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She has many friend.",
      "answer": "She has many friends.",
      "accept": [
        "She has many friends"
      ],
      "example": "She has many friends.",
      "id": 39
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "These is my keys.",
      "answer": "These are my keys.",
      "accept": [
        "These are my keys"
      ],
      "example": "These are my keys.",
      "id": 40
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Those is flowers.",
      "answer": "Those are flowers.",
      "accept": [
        "Those are flowers"
      ],
      "example": "Those are flowers.",
      "id": 41
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I need five pen.",
      "answer": "I need five pens.",
      "accept": [
        "I need five pens"
      ],
      "example": "I need five pens.",
      "id": 42
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "There is people here.",
      "answer": "There are people here.",
      "accept": [
        "There are people here"
      ],
      "example": "There are people here.",
      "id": 43
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He bought two ticket.",
      "answer": "He bought two tickets.",
      "accept": [
        "He bought two tickets"
      ],
      "example": "He bought two tickets.",
      "id": 44
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "My childs are happy.",
      "answer": "My children are happy.",
      "accept": [
        "My children are happy"
      ],
      "example": "My children are happy.",
      "id": 45
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She don't like tea.",
      "answer": "She doesn't like tea.",
      "accept": [
        "She doesn't like tea",
        "She doesn't like tea"
      ],
      "example": "She doesn't like tea.",
      "id": 46
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He don't work here.",
      "answer": "He doesn't work here.",
      "accept": [
        "He doesn't work here",
        "He doesn't work here"
      ],
      "example": "He doesn't work here.",
      "id": 47
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "It don't matter.",
      "answer": "It doesn't matter.",
      "accept": [
        "It doesn't matter",
        "It doesn't matter"
      ],
      "example": "It doesn't matter.",
      "id": 48
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Does she likes coffee.",
      "answer": "Does she like coffee.",
      "accept": [
        "Does she like coffee",
        "Does she like coffee"
      ],
      "example": "Does she like coffee.",
      "id": 49
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Do he play tennis.",
      "answer": "Does he play tennis.",
      "accept": [
        "Does he play tennis",
        "Does he play tennis"
      ],
      "example": "Does he play tennis.",
      "id": 50
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Where he live.",
      "answer": "Where does he live.",
      "accept": [
        "Where does he live",
        "Where does he live"
      ],
      "example": "Where does he live.",
      "id": 51
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "What you do.",
      "answer": "What do you do.",
      "accept": [
        "What do you do",
        "What do you do"
      ],
      "example": "What do you do.",
      "id": 52
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She can plays piano.",
      "answer": "She can play piano.",
      "accept": [
        "She can play piano",
        "She can play piano"
      ],
      "example": "She can play piano.",
      "id": 53
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I can to swim.",
      "answer": "I can swim.",
      "accept": [
        "I can swim",
        "I can swim"
      ],
      "example": "I can swim.",
      "id": 54
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He must to go.",
      "answer": "He must go.",
      "accept": [
        "He must go",
        "He must go"
      ],
      "example": "He must go.",
      "id": 55
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I didn't went.",
      "answer": "I didn't go.",
      "accept": [
        "I didn't go",
        "I didn't go"
      ],
      "example": "I didn't go.",
      "id": 56
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She wasn't went.",
      "answer": "She didn't go.",
      "accept": [
        "She didn't go",
        "She didn't go"
      ],
      "example": "She didn't go.",
      "id": 57
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Did you went home.",
      "answer": "Did you go home.",
      "accept": [
        "Did you go home",
        "Did you go home"
      ],
      "example": "Did you go home.",
      "id": 58
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I am go to school.",
      "answer": "I go to school.",
      "accept": [
        "I go to school",
        "I go to school"
      ],
      "example": "I go to school.",
      "id": 59
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He is like football.",
      "answer": "He likes football.",
      "accept": [
        "He likes football",
        "He likes football"
      ],
      "example": "He likes football.",
      "id": 60
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She usually going by bus.",
      "answer": "She usually goes by bus.",
      "accept": [
        "She usually goes by bus",
        "She usually goes by bus"
      ],
      "example": "She usually goes by bus.",
      "id": 61
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I every day wake up early.",
      "answer": "I wake up early every day.",
      "accept": [
        "I wake up early every day",
        "I wake up early every day"
      ],
      "example": "I wake up early every day.",
      "id": 62
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "My parents lives in Moscow.",
      "answer": "My parents live in Moscow.",
      "accept": [
        "My parents live in Moscow",
        "My parents live in Moscow"
      ],
      "example": "My parents live in Moscow.",
      "id": 63
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "The news are interesting.",
      "answer": "The news is interesting.",
      "accept": [
        "The news is interesting",
        "The news is interesting"
      ],
      "example": "The news is interesting.",
      "id": 64
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Everybody know this.",
      "answer": "Everybody knows this.",
      "accept": [
        "Everybody knows this",
        "Everybody knows this"
      ],
      "example": "Everybody knows this.",
      "id": 65
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Someone have called.",
      "answer": "Someone has called.",
      "accept": [
        "Someone has called",
        "Someone has called"
      ],
      "example": "Someone has called.",
      "id": 66
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Nobody don't care.",
      "answer": "Nobody cares.",
      "accept": [
        "Nobody cares",
        "Nobody cares"
      ],
      "example": "Nobody cares.",
      "id": 67
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I haven't got no money.",
      "answer": "I haven't got any money.",
      "accept": [
        "I haven't got any money",
        "I haven't got any money"
      ],
      "example": "I haven't got any money.",
      "id": 68
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She speak English good.",
      "answer": "She speaks English well.",
      "accept": [
        "She speaks English well",
        "She speaks English well"
      ],
      "example": "She speaks English well.",
      "id": 69
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He runned fast.",
      "answer": "He ran fast.",
      "accept": [
        "He ran fast",
        "He ran fast"
      ],
      "example": "He ran fast.",
      "id": 70
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I eated pizza.",
      "answer": "I ate pizza.",
      "accept": [
        "I ate pizza",
        "I ate pizza"
      ],
      "example": "I ate pizza.",
      "id": 71
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She buyed a dress.",
      "answer": "She bought a dress.",
      "accept": [
        "She bought a dress",
        "She bought a dress"
      ],
      "example": "She bought a dress.",
      "id": 72
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He goed home.",
      "answer": "He went home.",
      "accept": [
        "He went home",
        "He went home"
      ],
      "example": "He went home.",
      "id": 73
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "We was happy.",
      "answer": "We were happy.",
      "accept": [
        "We were happy",
        "We were happy"
      ],
      "example": "We were happy.",
      "id": 74
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "They was late.",
      "answer": "They were late.",
      "accept": [
        "They were late",
        "They were late"
      ],
      "example": "They were late.",
      "id": 75
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Yesterday I go to the park.",
      "answer": "Yesterday I went to the park.",
      "accept": [
        "Yesterday I went to the park",
        "Yesterday I went to the park"
      ],
      "example": "Yesterday I went to the park.",
      "id": 76
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Last week she visit us.",
      "answer": "Last week she visited us.",
      "accept": [
        "Last week she visited us",
        "Last week she visited us"
      ],
      "example": "Last week she visited us.",
      "id": 77
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I am agree with you.",
      "answer": "I agree with you.",
      "accept": [
        "I agree with you",
        "I agree with you"
      ],
      "example": "I agree with you.",
      "id": 78
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He said me the truth.",
      "answer": "He told me the truth.",
      "accept": [
        "He told me the truth",
        "He told me the truth"
      ],
      "example": "He told me the truth.",
      "id": 79
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I look forward to meet you.",
      "answer": "I look forward to meeting you.",
      "accept": [
        "I look forward to meeting you",
        "I look forward to meeting you"
      ],
      "example": "I look forward to meeting you.",
      "id": 80
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She interested in music.",
      "answer": "She is interested in music.",
      "accept": [
        "She is interested in music",
        "She is interested in music"
      ],
      "example": "She is interested in music.",
      "id": 81
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "The weather are cold.",
      "answer": "The weather is cold.",
      "accept": [
        "The weather is cold",
        "The weather is cold"
      ],
      "example": "The weather is cold.",
      "id": 82
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I very like this film.",
      "answer": "I like this film very much.",
      "accept": [
        "I like this film very much",
        "I like this film very much"
      ],
      "example": "I like this film very much.",
      "id": 83
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He more taller than me.",
      "answer": "He is taller than me.",
      "accept": [
        "He is taller than me",
        "He is taller than me"
      ],
      "example": "He is taller than me.",
      "id": 84
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "This is more better.",
      "answer": "This is better.",
      "accept": [
        "This is better",
        "This is better"
      ],
      "example": "This is better.",
      "id": 85
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She gave to me a gift.",
      "answer": "She gave me a gift.",
      "accept": [
        "She gave me a gift",
        "She gave me a gift"
      ],
      "example": "She gave me a gift.",
      "id": 86
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I asked to him a question.",
      "answer": "I asked him a question.",
      "accept": [
        "I asked him a question",
        "I asked him a question"
      ],
      "example": "I asked him a question.",
      "id": 87
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Please explain me this.",
      "answer": "Please explain this to me.",
      "accept": [
        "Please explain this to me",
        "Please explain this to me"
      ],
      "example": "Please explain this to me.",
      "id": 88
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I waiting for you.",
      "answer": "I am waiting for you.",
      "accept": [
        "I am waiting for you",
        "I am waiting for you"
      ],
      "example": "I am waiting for you.",
      "id": 89
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She living in Paris now.",
      "answer": "She is living in Paris now.",
      "accept": [
        "She is living in Paris now",
        "She is living in Paris now"
      ],
      "example": "She is living in Paris now.",
      "id": 90
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Listen! Someone knock.",
      "answer": "Listen! Someone is knocking.",
      "accept": [
        "Listen! Someone is knocking",
        "Listen! Someone is knocking"
      ],
      "example": "Listen! Someone is knocking.",
      "id": 91
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "Look! It rain.",
      "answer": "Look! It is raining.",
      "accept": [
        "Look! It is raining",
        "Look! It is raining"
      ],
      "example": "Look! It is raining.",
      "id": 92
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I see him yesterday.",
      "answer": "I saw him yesterday.",
      "accept": [
        "I saw him yesterday",
        "I saw him yesterday"
      ],
      "example": "I saw him yesterday.",
      "id": 93
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She already finish.",
      "answer": "She has already finished.",
      "accept": [
        "She has already finished",
        "She has already finished"
      ],
      "example": "She has already finished.",
      "id": 94
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "I never been to Spain.",
      "answer": "I have never been to Spain.",
      "accept": [
        "I have never been to Spain",
        "I have never been to Spain"
      ],
      "example": "I have never been to Spain.",
      "id": 95
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "She go to school every day.",
      "answer": "She goes to school every day.",
      "accept": [
        "She goes to school every day"
      ],
      "example": "She goes to school every day.",
      "id": 96
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "He like pizza.",
      "answer": "He likes pizza.",
      "accept": [
        "He likes pizza"
      ],
      "example": "He likes pizza.",
      "id": 97
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "It work well.",
      "answer": "It works well.",
      "accept": [
        "It works well"
      ],
      "example": "It works well.",
      "id": 98
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "My brother play football.",
      "answer": "My brother plays football.",
      "accept": [
        "My brother plays football"
      ],
      "example": "My brother plays football.",
      "id": 99
    },
    {
      "subtype": "fix_sentence",
      "instruction_ru": "Исправь ошибку в предложении:",
      "prompt_en": "The cat sleep on the sofa.",
      "answer": "The cat sleeps on the sofa.",
      "accept": [
        "The cat sleeps on the sofa"
      ],
      "example": "The cat sleeps on the sofa.",
      "id": 100
    }
  ],
  "A2": [
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "usually",
        "drink",
        "coffee",
        "in",
        "the",
        "morning"
      ],
      "answer": "I usually drink coffee in the morning.",
      "accept": [
        "I usually drink coffee in the morning",
        "I usually drink coffee in the morning"
      ],
      "example": "I usually drink coffee in the morning.",
      "id": 1
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "goes",
        "to",
        "work",
        "by",
        "bus"
      ],
      "answer": "She goes to work by bus.",
      "accept": [
        "She goes to work by bus",
        "She goes to work by bus"
      ],
      "example": "She goes to work by bus.",
      "id": 2
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "are",
        "watching",
        "a",
        "film",
        "now"
      ],
      "answer": "They are watching a film now.",
      "accept": [
        "They are watching a film now",
        "They are watching a film now"
      ],
      "example": "They are watching a film now.",
      "id": 3
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "visited",
        "our",
        "grandparents",
        "last",
        "Sunday"
      ],
      "answer": "We visited our grandparents last Sunday.",
      "accept": [
        "We visited our grandparents last Sunday",
        "We visited our grandparents last Sunday"
      ],
      "example": "We visited our grandparents last Sunday.",
      "id": 4
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "can",
        "speak",
        "three",
        "languages"
      ],
      "answer": "He can speak three languages.",
      "accept": [
        "He can speak three languages",
        "He can speak three languages"
      ],
      "example": "He can speak three languages.",
      "id": 5
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "My",
        "sister",
        "is",
        "taller",
        "than",
        "me"
      ],
      "answer": "My sister is taller than me.",
      "accept": [
        "My sister is taller than me",
        "My sister is taller than me"
      ],
      "example": "My sister is taller than me.",
      "id": 6
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "There",
        "are",
        "many",
        "books",
        "on",
        "the",
        "shelf"
      ],
      "answer": "There are many books on the shelf.",
      "accept": [
        "There are many books on the shelf",
        "There are many books on the shelf"
      ],
      "example": "There are many books on the shelf.",
      "id": 7
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "have",
        "already",
        "finished",
        "my",
        "homework"
      ],
      "answer": "I have already finished my homework.",
      "accept": [
        "I have already finished my homework",
        "I have already finished my homework"
      ],
      "example": "I have already finished my homework.",
      "id": 8
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "was",
        "cooking",
        "dinner",
        "when",
        "I",
        "arrived"
      ],
      "answer": "She was cooking dinner when I arrived.",
      "accept": [
        "She was cooking dinner when I arrived",
        "She was cooking dinner when I arrived"
      ],
      "example": "She was cooking dinner when I arrived.",
      "id": 9
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "If",
        "it",
        "rains",
        "we",
        "will",
        "stay",
        "at",
        "home"
      ],
      "answer": "If it rains we will stay at home.",
      "accept": [
        "If it rains we will stay at home",
        "If it rains we will stay at home"
      ],
      "example": "If it rains we will stay at home.",
      "id": 10
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "has",
        "lived",
        "here",
        "for",
        "five",
        "years"
      ],
      "answer": "He has lived here for five years.",
      "accept": [
        "He has lived here for five years",
        "He has lived here for five years"
      ],
      "example": "He has lived here for five years.",
      "id": 11
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "don't",
        "like",
        "spicy",
        "food"
      ],
      "answer": "They don't like spicy food.",
      "accept": [
        "They don't like spicy food",
        "They don't like spicy food"
      ],
      "example": "They don't like spicy food.",
      "id": 12
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "Where",
        "did",
        "you",
        "buy",
        "this",
        "jacket"
      ],
      "answer": "Where did you buy this jacket.",
      "accept": [
        "Where did you buy this jacket",
        "Where did you buy this jacket"
      ],
      "example": "Where did you buy this jacket.",
      "id": 13
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "am",
        "going",
        "to",
        "call",
        "you",
        "tomorrow"
      ],
      "answer": "I am going to call you tomorrow.",
      "accept": [
        "I am going to call you tomorrow",
        "I am going to call you tomorrow"
      ],
      "example": "I am going to call you tomorrow.",
      "id": 14
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "The",
        "train",
        "leaves",
        "at",
        "half",
        "past",
        "eight"
      ],
      "answer": "The train leaves at half past eight.",
      "accept": [
        "The train leaves at half past eight",
        "The train leaves at half past eight"
      ],
      "example": "The train leaves at half past eight.",
      "id": 15
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "asked",
        "me",
        "to",
        "help",
        "her"
      ],
      "answer": "She asked me to help her.",
      "accept": [
        "She asked me to help her",
        "She asked me to help her"
      ],
      "example": "She asked me to help her.",
      "id": 16
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "should",
        "take",
        "an",
        "umbrella",
        "today"
      ],
      "answer": "We should take an umbrella today.",
      "accept": [
        "We should take an umbrella today",
        "We should take an umbrella today"
      ],
      "example": "We should take an umbrella today.",
      "id": 17
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "looks",
        "tired",
        "after",
        "the",
        "trip"
      ],
      "answer": "He looks tired after the trip.",
      "accept": [
        "He looks tired after the trip",
        "He looks tired after the trip"
      ],
      "example": "He looks tired after the trip.",
      "id": 18
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "prefer",
        "tea",
        "to",
        "coffee"
      ],
      "answer": "I prefer tea to coffee.",
      "accept": [
        "I prefer tea to coffee",
        "I prefer tea to coffee"
      ],
      "example": "I prefer tea to coffee.",
      "id": 19
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "The",
        "children",
        "are",
        "playing",
        "in",
        "the",
        "garden"
      ],
      "answer": "The children are playing in the garden.",
      "accept": [
        "The children are playing in the garden",
        "The children are playing in the garden"
      ],
      "example": "The children are playing in the garden.",
      "id": 20
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "has",
        "never",
        "seen",
        "snow",
        "before"
      ],
      "answer": "She has never seen snow before.",
      "accept": [
        "She has never seen snow before",
        "She has never seen snow before"
      ],
      "example": "She has never seen snow before.",
      "id": 21
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "Please",
        "close",
        "the",
        "window"
      ],
      "answer": "Please close the window.",
      "accept": [
        "Please close the window",
        "Please close the window"
      ],
      "example": "Please close the window.",
      "id": 22
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "met",
        "him",
        "at",
        "the",
        "station",
        "yesterday"
      ],
      "answer": "I met him at the station yesterday.",
      "accept": [
        "I met him at the station yesterday",
        "I met him at the station yesterday"
      ],
      "example": "I met him at the station yesterday.",
      "id": 23
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "will",
        "arrive",
        "in",
        "an",
        "hour"
      ],
      "answer": "They will arrive in an hour.",
      "accept": [
        "They will arrive in an hour",
        "They will arrive in an hour"
      ],
      "example": "They will arrive in an hour.",
      "id": 24
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "is",
        "interested",
        "in",
        "photography"
      ],
      "answer": "He is interested in photography.",
      "accept": [
        "He is interested in photography",
        "He is interested in photography"
      ],
      "example": "He is interested in photography.",
      "id": 25
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "need",
        "to",
        "buy",
        "some",
        "bread"
      ],
      "answer": "We need to buy some bread.",
      "accept": [
        "We need to buy some bread",
        "We need to buy some bread"
      ],
      "example": "We need to buy some bread.",
      "id": 26
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "works",
        "as",
        "a",
        "nurse",
        "in",
        "a",
        "hospital"
      ],
      "answer": "She works as a nurse in a hospital.",
      "accept": [
        "She works as a nurse in a hospital",
        "She works as a nurse in a hospital"
      ],
      "example": "She works as a nurse in a hospital.",
      "id": 27
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "forgot",
        "my",
        "keys",
        "at",
        "home"
      ],
      "answer": "I forgot my keys at home.",
      "accept": [
        "I forgot my keys at home",
        "I forgot my keys at home"
      ],
      "example": "I forgot my keys at home.",
      "id": 28
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "The",
        "weather",
        "was",
        "sunny",
        "and",
        "warm"
      ],
      "answer": "The weather was sunny and warm.",
      "accept": [
        "The weather was sunny and warm",
        "The weather was sunny and warm"
      ],
      "example": "The weather was sunny and warm.",
      "id": 29
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "didn't",
        "understand",
        "the",
        "question"
      ],
      "answer": "He didn't understand the question.",
      "accept": [
        "He didn't understand the question",
        "He didn't understand the question"
      ],
      "example": "He didn't understand the question.",
      "id": 30
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "Can",
        "you",
        "open",
        "the",
        "door",
        "please"
      ],
      "answer": "Can you open the door please.",
      "accept": [
        "Can you open the door please",
        "Can you open the door please"
      ],
      "example": "Can you open the door please.",
      "id": 31
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "have",
        "been",
        "waiting",
        "for",
        "twenty",
        "minutes"
      ],
      "answer": "I have been waiting for twenty minutes.",
      "accept": [
        "I have been waiting for twenty minutes",
        "I have been waiting for twenty minutes"
      ],
      "example": "I have been waiting for twenty minutes.",
      "id": 32
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "used",
        "to",
        "live",
        "in",
        "Spain"
      ],
      "answer": "She used to live in Spain.",
      "accept": [
        "She used to live in Spain",
        "She used to live in Spain"
      ],
      "example": "She used to live in Spain.",
      "id": 33
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "are",
        "going",
        "to",
        "open",
        "a",
        "new",
        "shop"
      ],
      "answer": "They are going to open a new shop.",
      "accept": [
        "They are going to open a new shop",
        "They are going to open a new shop"
      ],
      "example": "They are going to open a new shop.",
      "id": 34
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "My",
        "phone",
        "is",
        "more",
        "expensive",
        "than",
        "yours"
      ],
      "answer": "My phone is more expensive than yours.",
      "accept": [
        "My phone is more expensive than yours",
        "My phone is more expensive than yours"
      ],
      "example": "My phone is more expensive than yours.",
      "id": 35
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "spoke",
        "so",
        "quietly",
        "that",
        "I",
        "couldn't",
        "hear"
      ],
      "answer": "He spoke so quietly that I couldn't hear.",
      "accept": [
        "He spoke so quietly that I couldn't hear",
        "He spoke so quietly that I couldn't hear"
      ],
      "example": "He spoke so quietly that I couldn't hear.",
      "id": 36
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "had",
        "dinner",
        "and",
        "then",
        "watched",
        "TV"
      ],
      "answer": "We had dinner and then watched TV.",
      "accept": [
        "We had dinner and then watched TV",
        "We had dinner and then watched TV"
      ],
      "example": "We had dinner and then watched TV.",
      "id": 37
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "is",
        "the",
        "best",
        "student",
        "in",
        "the",
        "class"
      ],
      "answer": "She is the best student in the class.",
      "accept": [
        "She is the best student in the class",
        "She is the best student in the class"
      ],
      "example": "She is the best student in the class.",
      "id": 38
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "would",
        "like",
        "a",
        "glass",
        "of",
        "water"
      ],
      "answer": "I would like a glass of water.",
      "accept": [
        "I would like a glass of water",
        "I would like a glass of water"
      ],
      "example": "I would like a glass of water.",
      "id": 39
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "must",
        "wear",
        "a",
        "uniform",
        "at",
        "work"
      ],
      "answer": "He must wear a uniform at work.",
      "accept": [
        "He must wear a uniform at work",
        "He must wear a uniform at work"
      ],
      "example": "He must wear a uniform at work.",
      "id": 40
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "The",
        "film",
        "was",
        "more",
        "interesting",
        "than",
        "the",
        "book"
      ],
      "answer": "The film was more interesting than the book.",
      "accept": [
        "The film was more interesting than the book",
        "The film was more interesting than the book"
      ],
      "example": "The film was more interesting than the book.",
      "id": 41
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "haven't",
        "seen",
        "her",
        "since",
        "Monday"
      ],
      "answer": "I haven't seen her since Monday.",
      "accept": [
        "I haven't seen her since Monday",
        "I haven't seen her since Monday"
      ],
      "example": "I haven't seen her since Monday.",
      "id": 42
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "is",
        "talking",
        "to",
        "her",
        "friend",
        "now"
      ],
      "answer": "She is talking to her friend now.",
      "accept": [
        "She is talking to her friend now",
        "She is talking to her friend now"
      ],
      "example": "She is talking to her friend now.",
      "id": 43
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "cleaned",
        "the",
        "house",
        "before",
        "the",
        "guests",
        "came"
      ],
      "answer": "They cleaned the house before the guests came.",
      "accept": [
        "They cleaned the house before the guests came",
        "They cleaned the house before the guests came"
      ],
      "example": "They cleaned the house before the guests came.",
      "id": 44
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "What",
        "time",
        "does",
        "the",
        "museum",
        "open"
      ],
      "answer": "What time does the museum open.",
      "accept": [
        "What time does the museum open",
        "What time does the museum open"
      ],
      "example": "What time does the museum open.",
      "id": 45
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "am",
        "looking",
        "for",
        "my",
        "black",
        "bag"
      ],
      "answer": "I am looking for my black bag.",
      "accept": [
        "I am looking for my black bag",
        "I am looking for my black bag"
      ],
      "example": "I am looking for my black bag.",
      "id": 46
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "gave",
        "me",
        "a",
        "very",
        "useful",
        "tip"
      ],
      "answer": "He gave me a very useful tip.",
      "accept": [
        "He gave me a very useful tip",
        "He gave me a very useful tip"
      ],
      "example": "He gave me a very useful tip.",
      "id": 47
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "walked",
        "along",
        "the",
        "river",
        "yesterday"
      ],
      "answer": "We walked along the river yesterday.",
      "accept": [
        "We walked along the river yesterday",
        "We walked along the river yesterday"
      ],
      "example": "We walked along the river yesterday.",
      "id": 48
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "can't",
        "find",
        "her",
        "glasses"
      ],
      "answer": "She can't find her glasses.",
      "accept": [
        "She can't find her glasses",
        "She can't find her glasses"
      ],
      "example": "She can't find her glasses.",
      "id": 49
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "think",
        "this",
        "idea",
        "is",
        "brilliant"
      ],
      "answer": "I think this idea is brilliant.",
      "accept": [
        "I think this idea is brilliant",
        "I think this idea is brilliant"
      ],
      "example": "I think this idea is brilliant.",
      "id": 50
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "always",
        "arrives",
        "on",
        "time"
      ],
      "answer": "He always arrives on time.",
      "accept": [
        "He always arrives on time",
        "He always arrives on time"
      ],
      "example": "He always arrives on time.",
      "id": 51
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "have",
        "just",
        "started",
        "a",
        "new",
        "project"
      ],
      "answer": "They have just started a new project.",
      "accept": [
        "They have just started a new project",
        "They have just started a new project"
      ],
      "example": "They have just started a new project.",
      "id": 52
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "was",
        "reading",
        "when",
        "the",
        "phone",
        "rang"
      ],
      "answer": "I was reading when the phone rang.",
      "accept": [
        "I was reading when the phone rang",
        "I was reading when the phone rang"
      ],
      "example": "I was reading when the phone rang.",
      "id": 53
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "will",
        "help",
        "you",
        "if",
        "you",
        "ask"
      ],
      "answer": "She will help you if you ask.",
      "accept": [
        "She will help you if you ask",
        "She will help you if you ask"
      ],
      "example": "She will help you if you ask.",
      "id": 54
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "enjoy",
        "listening",
        "to",
        "music"
      ],
      "answer": "We enjoy listening to music.",
      "accept": [
        "We enjoy listening to music",
        "We enjoy listening to music"
      ],
      "example": "We enjoy listening to music.",
      "id": 55
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "bought",
        "a",
        "ticket",
        "for",
        "the",
        "concert"
      ],
      "answer": "He bought a ticket for the concert.",
      "accept": [
        "He bought a ticket for the concert",
        "He bought a ticket for the concert"
      ],
      "example": "He bought a ticket for the concert.",
      "id": 56
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "There",
        "isn't",
        "any",
        "milk",
        "in",
        "the",
        "fridge"
      ],
      "answer": "There isn't any milk in the fridge.",
      "accept": [
        "There isn't any milk in the fridge",
        "There isn't any milk in the fridge"
      ],
      "example": "There isn't any milk in the fridge.",
      "id": 57
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "need",
        "to",
        "finish",
        "this",
        "report",
        "today"
      ],
      "answer": "I need to finish this report today.",
      "accept": [
        "I need to finish this report today",
        "I need to finish this report today"
      ],
      "example": "I need to finish this report today.",
      "id": 58
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "has",
        "written",
        "three",
        "emails",
        "already"
      ],
      "answer": "She has written three emails already.",
      "accept": [
        "She has written three emails already",
        "She has written three emails already"
      ],
      "example": "She has written three emails already.",
      "id": 59
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "moved",
        "to",
        "a",
        "bigger",
        "flat",
        "last",
        "year"
      ],
      "answer": "They moved to a bigger flat last year.",
      "accept": [
        "They moved to a bigger flat last year",
        "They moved to a bigger flat last year"
      ],
      "example": "They moved to a bigger flat last year.",
      "id": 60
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "Could",
        "you",
        "pass",
        "me",
        "the",
        "salt"
      ],
      "answer": "Could you pass me the salt.",
      "accept": [
        "Could you pass me the salt",
        "Could you pass me the salt"
      ],
      "example": "Could you pass me the salt.",
      "id": 61
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "have",
        "to",
        "wake",
        "up",
        "early",
        "tomorrow"
      ],
      "answer": "I have to wake up early tomorrow.",
      "accept": [
        "I have to wake up early tomorrow",
        "I have to wake up early tomorrow"
      ],
      "example": "I have to wake up early tomorrow.",
      "id": 62
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "doesn't",
        "eat",
        "meat",
        "anymore"
      ],
      "answer": "He doesn't eat meat anymore.",
      "accept": [
        "He doesn't eat meat anymore",
        "He doesn't eat meat anymore"
      ],
      "example": "He doesn't eat meat anymore.",
      "id": 63
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "are",
        "meeting",
        "our",
        "friends",
        "this",
        "evening"
      ],
      "answer": "We are meeting our friends this evening.",
      "accept": [
        "We are meeting our friends this evening",
        "We are meeting our friends this evening"
      ],
      "example": "We are meeting our friends this evening.",
      "id": 64
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "felt",
        "happy",
        "after",
        "the",
        "exam"
      ],
      "answer": "She felt happy after the exam.",
      "accept": [
        "She felt happy after the exam",
        "She felt happy after the exam"
      ],
      "example": "She felt happy after the exam.",
      "id": 65
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "The",
        "shop",
        "closes",
        "at",
        "nine",
        "o'clock"
      ],
      "answer": "The shop closes at nine o'clock.",
      "accept": [
        "The shop closes at nine o'clock",
        "The shop closes at nine o'clock"
      ],
      "example": "The shop closes at nine o'clock.",
      "id": 66
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "lost",
        "my",
        "wallet",
        "on",
        "the",
        "bus"
      ],
      "answer": "I lost my wallet on the bus.",
      "accept": [
        "I lost my wallet on the bus",
        "I lost my wallet on the bus"
      ],
      "example": "I lost my wallet on the bus.",
      "id": 67
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "is",
        "learning",
        "how",
        "to",
        "drive"
      ],
      "answer": "He is learning how to drive.",
      "accept": [
        "He is learning how to drive",
        "He is learning how to drive"
      ],
      "example": "He is learning how to drive.",
      "id": 68
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "invited",
        "us",
        "to",
        "their",
        "wedding"
      ],
      "answer": "They invited us to their wedding.",
      "accept": [
        "They invited us to their wedding",
        "They invited us to their wedding"
      ],
      "example": "They invited us to their wedding.",
      "id": 69
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "would",
        "rather",
        "stay",
        "at",
        "home",
        "tonight"
      ],
      "answer": "I would rather stay at home tonight.",
      "accept": [
        "I would rather stay at home tonight",
        "I would rather stay at home tonight"
      ],
      "example": "I would rather stay at home tonight.",
      "id": 70
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "has",
        "known",
        "him",
        "for",
        "a",
        "long",
        "time"
      ],
      "answer": "She has known him for a long time.",
      "accept": [
        "She has known him for a long time",
        "She has known him for a long time"
      ],
      "example": "She has known him for a long time.",
      "id": 71
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "should",
        "leave",
        "before",
        "it",
        "gets",
        "dark"
      ],
      "answer": "We should leave before it gets dark.",
      "accept": [
        "We should leave before it gets dark",
        "We should leave before it gets dark"
      ],
      "example": "We should leave before it gets dark.",
      "id": 72
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "asked",
        "where",
        "the",
        "nearest",
        "bank",
        "was"
      ],
      "answer": "He asked where the nearest bank was.",
      "accept": [
        "He asked where the nearest bank was",
        "He asked where the nearest bank was"
      ],
      "example": "He asked where the nearest bank was.",
      "id": 73
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "am",
        "not",
        "used",
        "to",
        "cold",
        "weather"
      ],
      "answer": "I am not used to cold weather.",
      "accept": [
        "I am not used to cold weather",
        "I am not used to cold weather"
      ],
      "example": "I am not used to cold weather.",
      "id": 74
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "have",
        "been",
        "friends",
        "since",
        "childhood"
      ],
      "answer": "They have been friends since childhood.",
      "accept": [
        "They have been friends since childhood",
        "They have been friends since childhood"
      ],
      "example": "They have been friends since childhood.",
      "id": 75
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "made",
        "a",
        "cake",
        "for",
        "his",
        "birthday"
      ],
      "answer": "She made a cake for his birthday.",
      "accept": [
        "She made a cake for his birthday",
        "She made a cake for his birthday"
      ],
      "example": "She made a cake for his birthday.",
      "id": 76
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "Please",
        "turn",
        "off",
        "the",
        "lights"
      ],
      "answer": "Please turn off the lights.",
      "accept": [
        "Please turn off the lights",
        "Please turn off the lights"
      ],
      "example": "Please turn off the lights.",
      "id": 77
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "saw",
        "a",
        "strange",
        "bird",
        "in",
        "the",
        "tree"
      ],
      "answer": "I saw a strange bird in the tree.",
      "accept": [
        "I saw a strange bird in the tree",
        "I saw a strange bird in the tree"
      ],
      "example": "I saw a strange bird in the tree.",
      "id": 78
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "didn't",
        "sleep",
        "well",
        "last",
        "night"
      ],
      "answer": "He didn't sleep well last night.",
      "accept": [
        "He didn't sleep well last night",
        "He didn't sleep well last night"
      ],
      "example": "He didn't sleep well last night.",
      "id": 79
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "need",
        "more",
        "information",
        "about",
        "the",
        "course"
      ],
      "answer": "We need more information about the course.",
      "accept": [
        "We need more information about the course",
        "We need more information about the course"
      ],
      "example": "We need more information about the course.",
      "id": 80
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "is",
        "better",
        "at",
        "English",
        "than",
        "maths"
      ],
      "answer": "She is better at English than maths.",
      "accept": [
        "She is better at English than maths",
        "She is better at English than maths"
      ],
      "example": "She is better at English than maths.",
      "id": 81
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "will",
        "send",
        "you",
        "a",
        "message",
        "later"
      ],
      "answer": "I will send you a message later.",
      "accept": [
        "I will send you a message later",
        "I will send you a message later"
      ],
      "example": "I will send you a message later.",
      "id": 82
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "are",
        "building",
        "a",
        "new",
        "bridge"
      ],
      "answer": "They are building a new bridge.",
      "accept": [
        "They are building a new bridge",
        "They are building a new bridge"
      ],
      "example": "They are building a new bridge.",
      "id": 83
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "forgot",
        "to",
        "lock",
        "the",
        "door"
      ],
      "answer": "He forgot to lock the door.",
      "accept": [
        "He forgot to lock the door",
        "He forgot to lock the door"
      ],
      "example": "He forgot to lock the door.",
      "id": 84
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "have",
        "never",
        "tried",
        "Japanese",
        "food"
      ],
      "answer": "I have never tried Japanese food.",
      "accept": [
        "I have never tried Japanese food",
        "I have never tried Japanese food"
      ],
      "example": "I have never tried Japanese food.",
      "id": 85
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "was",
        "born",
        "in",
        "a",
        "small",
        "town"
      ],
      "answer": "She was born in a small town.",
      "accept": [
        "She was born in a small town",
        "She was born in a small town"
      ],
      "example": "She was born in a small town.",
      "id": 86
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "can",
        "take",
        "a",
        "taxi",
        "if",
        "you",
        "want"
      ],
      "answer": "We can take a taxi if you want.",
      "accept": [
        "We can take a taxi if you want",
        "We can take a taxi if you want"
      ],
      "example": "We can take a taxi if you want.",
      "id": 87
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "speaks",
        "English",
        "very",
        "fluently"
      ],
      "answer": "He speaks English very fluently.",
      "accept": [
        "He speaks English very fluently",
        "He speaks English very fluently"
      ],
      "example": "He speaks English very fluently.",
      "id": 88
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "The",
        "results",
        "will",
        "be",
        "ready",
        "next",
        "week"
      ],
      "answer": "The results will be ready next week.",
      "accept": [
        "The results will be ready next week",
        "The results will be ready next week"
      ],
      "example": "The results will be ready next week.",
      "id": 89
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "enjoy",
        "cooking",
        "for",
        "my",
        "family"
      ],
      "answer": "I enjoy cooking for my family.",
      "accept": [
        "I enjoy cooking for my family",
        "I enjoy cooking for my family"
      ],
      "example": "I enjoy cooking for my family.",
      "id": 90
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "has",
        "already",
        "booked",
        "the",
        "tickets"
      ],
      "answer": "She has already booked the tickets.",
      "accept": [
        "She has already booked the tickets",
        "She has already booked the tickets"
      ],
      "example": "She has already booked the tickets.",
      "id": 91
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "waited",
        "until",
        "the",
        "rain",
        "stopped"
      ],
      "answer": "They waited until the rain stopped.",
      "accept": [
        "They waited until the rain stopped",
        "They waited until the rain stopped"
      ],
      "example": "They waited until the rain stopped.",
      "id": 92
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "am",
        "afraid",
        "of",
        "spiders"
      ],
      "answer": "I am afraid of spiders.",
      "accept": [
        "I am afraid of spiders",
        "I am afraid of spiders"
      ],
      "example": "I am afraid of spiders.",
      "id": 93
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "usually",
        "checks",
        "his",
        "email",
        "in",
        "the",
        "morning"
      ],
      "answer": "He usually checks his email in the morning.",
      "accept": [
        "He usually checks his email in the morning",
        "He usually checks his email in the morning"
      ],
      "example": "He usually checks his email in the morning.",
      "id": 94
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "We",
        "decided",
        "to",
        "go",
        "by",
        "train"
      ],
      "answer": "We decided to go by train.",
      "accept": [
        "We decided to go by train",
        "We decided to go by train"
      ],
      "example": "We decided to go by train.",
      "id": 95
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "She",
        "lent",
        "me",
        "her",
        "favourite",
        "book"
      ],
      "answer": "She lent me her favourite book.",
      "accept": [
        "She lent me her favourite book",
        "She lent me her favourite book"
      ],
      "example": "She lent me her favourite book.",
      "id": 96
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "I",
        "can't",
        "believe",
        "this",
        "news"
      ],
      "answer": "I can't believe this news.",
      "accept": [
        "I can't believe this news",
        "I can't believe this news"
      ],
      "example": "I can't believe this news.",
      "id": 97
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "They",
        "are",
        "still",
        "waiting",
        "for",
        "an",
        "answer"
      ],
      "answer": "They are still waiting for an answer.",
      "accept": [
        "They are still waiting for an answer",
        "They are still waiting for an answer"
      ],
      "example": "They are still waiting for an answer.",
      "id": 98
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "He",
        "found",
        "a",
        "job",
        "in",
        "another",
        "city"
      ],
      "answer": "He found a job in another city.",
      "accept": [
        "He found a job in another city",
        "He found a job in another city"
      ],
      "example": "He found a job in another city.",
      "id": 99
    },
    {
      "subtype": "order_words",
      "instruction_ru": "Составь предложение из слов:",
      "prompt_en": "",
      "words": [
        "Please",
        "remind",
        "me",
        "about",
        "the",
        "meeting"
      ],
      "answer": "Please remind me about the meeting.",
      "accept": [
        "Please remind me about the meeting",
        "Please remind me about the meeting"
      ],
      "example": "Please remind me about the meeting.",
      "id": 100
    }
  ],
  "B1": [
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She is taller than her brother.",
      "answer": "Her brother is shorter than she is.",
      "accept": [
        "Her brother is not as tall as she is",
        "Her brother is shorter than her",
        "Her brother is shorter than she is"
      ],
      "example": "Her brother is shorter than she is.",
      "id": 1
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I started learning English two years ago.",
      "answer": "I have been learning English for two years.",
      "accept": [
        "I've been learning English for two years",
        "I have learnt English for two years",
        "I have been learning English for two years"
      ],
      "example": "I have been learning English for two years.",
      "id": 2
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "This book is more interesting than that one.",
      "answer": "That book is less interesting than this one.",
      "accept": [
        "That one is not as interesting as this book",
        "That book is less interesting than this one"
      ],
      "example": "That book is less interesting than this one.",
      "id": 3
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "They postponed the meeting.",
      "answer": "They put the meeting off.",
      "accept": [
        "They delayed the meeting",
        "The meeting was postponed",
        "They put the meeting off"
      ],
      "example": "They put the meeting off.",
      "id": 4
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I regret not taking the job.",
      "answer": "I wish I had taken the job.",
      "accept": [
        "I wish I'd taken the job",
        "I am sorry I didn't take the job",
        "I wish I had taken the job"
      ],
      "example": "I wish I had taken the job.",
      "id": 5
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "It is not necessary to come early.",
      "answer": "You don't have to come early.",
      "accept": [
        "You needn't come early",
        "You do not have to come early",
        "You don't have to come early"
      ],
      "example": "You don't have to come early.",
      "id": 6
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "Someone stole my bike.",
      "answer": "My bike was stolen.",
      "accept": [
        "My bike got stolen",
        "My bike was stolen"
      ],
      "example": "My bike was stolen.",
      "id": 7
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "Although it was raining, we went out.",
      "answer": "It was raining, but we went out anyway.",
      "accept": [
        "Despite the rain we went out",
        "Even though it was raining we went out",
        "It was raining, but we went out anyway"
      ],
      "example": "It was raining, but we went out anyway.",
      "id": 8
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I haven't seen her for ages.",
      "answer": "It's been ages since I last saw her.",
      "accept": [
        "I haven't seen her in a long time",
        "It's been ages since I last saw her"
      ],
      "example": "It's been ages since I last saw her.",
      "id": 9
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He is too young to drive.",
      "answer": "He isn't old enough to drive.",
      "accept": [
        "He is not old enough to drive",
        "He isn't old enough to drive"
      ],
      "example": "He isn't old enough to drive.",
      "id": 10
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She managed to finish on time.",
      "answer": "She succeeded in finishing on time.",
      "accept": [
        "She was able to finish on time",
        "She succeeded in finishing on time"
      ],
      "example": "She succeeded in finishing on time.",
      "id": 11
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I'm sure he is at home.",
      "answer": "He must be at home.",
      "accept": [
        "He has to be at home",
        "He must be at home"
      ],
      "example": "He must be at home.",
      "id": 12
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "Perhaps she will call later.",
      "answer": "She might call later.",
      "accept": [
        "She may call later",
        "She could call later",
        "She might call later"
      ],
      "example": "She might call later.",
      "id": 13
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I advise you to rest.",
      "answer": "You should rest.",
      "accept": [
        "You ought to rest",
        "I'd advise you to rest",
        "You should rest"
      ],
      "example": "You should rest.",
      "id": 14
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "The room was so small that we couldn't move.",
      "answer": "The room was too small to move in.",
      "accept": [
        "It was such a small room that we couldn't move",
        "The room was too small to move in"
      ],
      "example": "The room was too small to move in.",
      "id": 15
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He said, 'I am tired.'",
      "answer": "He said that he was tired.",
      "accept": [
        "He told me that he was tired",
        "He said that he was tired"
      ],
      "example": "He said that he was tired.",
      "id": 16
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "'Where do you live?' she asked.",
      "answer": "She asked where I lived.",
      "accept": [
        "She asked me where I lived",
        "She asked where I lived"
      ],
      "example": "She asked where I lived.",
      "id": 17
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I prefer tea to coffee.",
      "answer": "I like tea more than coffee.",
      "accept": [
        "I'd rather have tea than coffee",
        "I like tea more than coffee"
      ],
      "example": "I like tea more than coffee.",
      "id": 18
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "As soon as he arrived, we started.",
      "answer": "We started the moment he arrived.",
      "accept": [
        "No sooner had he arrived than we started",
        "We started the moment he arrived"
      ],
      "example": "We started the moment he arrived.",
      "id": 19
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She has a talent for music.",
      "answer": "She is talented at music.",
      "accept": [
        "She is good at music",
        "She is talented at music"
      ],
      "example": "She is talented at music.",
      "id": 20
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I find this task difficult.",
      "answer": "This task is difficult for me.",
      "accept": [
        "This task seems difficult to me",
        "This task is difficult for me"
      ],
      "example": "This task is difficult for me.",
      "id": 21
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "They made me wait.",
      "answer": "I was made to wait.",
      "accept": [
        "They forced me to wait",
        "I was made to wait"
      ],
      "example": "I was made to wait.",
      "id": 22
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I can't afford a new car.",
      "answer": "A new car is too expensive for me.",
      "accept": [
        "I don't have enough money for a new car",
        "A new car is too expensive for me"
      ],
      "example": "A new car is too expensive for me.",
      "id": 23
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He rarely visits us.",
      "answer": "He doesn't visit us often.",
      "accept": [
        "He hardly ever visits us",
        "He doesn't visit us often"
      ],
      "example": "He doesn't visit us often.",
      "id": 24
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "Let's go for a walk.",
      "answer": "How about going for a walk?",
      "accept": [
        "Why don't we go for a walk",
        "Shall we go for a walk",
        "How about going for a walk?"
      ],
      "example": "How about going for a walk?",
      "id": 25
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I am not used to waking up early.",
      "answer": "Waking up early is unusual for me.",
      "accept": [
        "I am unused to waking up early",
        "Waking up early is unusual for me"
      ],
      "example": "Waking up early is unusual for me.",
      "id": 26
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "The film was boring.",
      "answer": "I was bored by the film.",
      "accept": [
        "I found the film boring",
        "I was bored by the film"
      ],
      "example": "I was bored by the film.",
      "id": 27
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She looks after her younger sister.",
      "answer": "She takes care of her younger sister.",
      "accept": [
        "She cares for her younger sister",
        "She takes care of her younger sister"
      ],
      "example": "She takes care of her younger sister.",
      "id": 28
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "We ran out of sugar.",
      "answer": "There was no sugar left.",
      "accept": [
        "We had no sugar left",
        "There was no sugar left"
      ],
      "example": "There was no sugar left.",
      "id": 29
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He gave up smoking.",
      "answer": "He stopped smoking.",
      "accept": [
        "He quit smoking",
        "He stopped smoking"
      ],
      "example": "He stopped smoking.",
      "id": 30
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I look forward to seeing you.",
      "answer": "I can't wait to see you.",
      "accept": [
        "I'm looking forward to seeing you",
        "I can't wait to see you"
      ],
      "example": "I can't wait to see you.",
      "id": 31
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "The test was easier than I expected.",
      "answer": "I expected the test to be more difficult.",
      "accept": [
        "The test wasn't as hard as I expected",
        "I expected the test to be more difficult"
      ],
      "example": "I expected the test to be more difficult.",
      "id": 32
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She is responsible for the project.",
      "answer": "The project is her responsibility.",
      "accept": [
        "She takes responsibility for the project",
        "The project is her responsibility"
      ],
      "example": "The project is her responsibility.",
      "id": 33
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I haven't got enough time.",
      "answer": "I don't have enough time.",
      "accept": [
        "I lack time",
        "I don't have enough time"
      ],
      "example": "I don't have enough time.",
      "id": 34
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He arrived later than usual.",
      "answer": "He was later than usual.",
      "accept": [
        "He came later than usual",
        "He was later than usual"
      ],
      "example": "He was later than usual.",
      "id": 35
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "It seems that she is busy.",
      "answer": "She seems to be busy.",
      "accept": [
        "She appears to be busy",
        "She seems to be busy"
      ],
      "example": "She seems to be busy.",
      "id": 36
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I wish I could speak French.",
      "answer": "I regret that I can't speak French.",
      "accept": [
        "I'd like to be able to speak French",
        "I regret that I can't speak French"
      ],
      "example": "I regret that I can't speak French.",
      "id": 37
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "They built this house in 1990.",
      "answer": "This house was built in 1990.",
      "accept": [
        "This house was constructed in 1990",
        "This house was built in 1990"
      ],
      "example": "This house was built in 1990.",
      "id": 38
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "You mustn't park here.",
      "answer": "Parking here is forbidden.",
      "accept": [
        "You are not allowed to park here",
        "Parking here is forbidden"
      ],
      "example": "Parking here is forbidden.",
      "id": 39
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I'll help you if you want.",
      "answer": "Let me know if you need help.",
      "accept": [
        "I can help you if you want",
        "Let me know if you need help"
      ],
      "example": "Let me know if you need help.",
      "id": 40
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She is as clever as her brother.",
      "answer": "Her brother is no cleverer than she is.",
      "accept": [
        "Her brother is as clever as she is",
        "Her brother is no cleverer than she is"
      ],
      "example": "Her brother is no cleverer than she is.",
      "id": 41
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I spent two hours on the report.",
      "answer": "It took me two hours to write the report.",
      "accept": [
        "Writing the report took me two hours",
        "It took me two hours to write the report"
      ],
      "example": "It took me two hours to write the report.",
      "id": 42
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He failed to open the door.",
      "answer": "He didn't manage to open the door.",
      "accept": [
        "He couldn't open the door",
        "He didn't manage to open the door"
      ],
      "example": "He didn't manage to open the door.",
      "id": 43
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "Despite the noise, I slept well.",
      "answer": "I slept well even though it was noisy.",
      "accept": [
        "Although it was noisy I slept well",
        "I slept well even though it was noisy"
      ],
      "example": "I slept well even though it was noisy.",
      "id": 44
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I'm thinking of changing jobs.",
      "answer": "I'm considering changing jobs.",
      "accept": [
        "I may change jobs",
        "I'm considering changing jobs"
      ],
      "example": "I'm considering changing jobs.",
      "id": 45
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She insisted on paying.",
      "answer": "She insisted that she should pay.",
      "accept": [
        "She was determined to pay",
        "She insisted that she should pay"
      ],
      "example": "She insisted that she should pay.",
      "id": 46
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "The sooner we leave, the better.",
      "answer": "It's better if we leave sooner.",
      "accept": [
        "We should leave as soon as possible",
        "It's better if we leave sooner"
      ],
      "example": "It's better if we leave sooner.",
      "id": 47
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I have never eaten sushi before.",
      "answer": "This is the first time I have eaten sushi.",
      "accept": [
        "I've never tried sushi before",
        "This is the first time I have eaten sushi"
      ],
      "example": "This is the first time I have eaten sushi.",
      "id": 48
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He speaks English fluently.",
      "answer": "He is a fluent English speaker.",
      "accept": [
        "His English is fluent",
        "He is a fluent English speaker"
      ],
      "example": "He is a fluent English speaker.",
      "id": 49
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "We cancelled the trip because of the storm.",
      "answer": "The storm caused us to cancel the trip.",
      "accept": [
        "We called off the trip because of the storm",
        "The storm caused us to cancel the trip"
      ],
      "example": "The storm caused us to cancel the trip.",
      "id": 50
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "It's worth visiting the museum.",
      "answer": "You should visit the museum.",
      "accept": [
        "The museum is worth a visit",
        "You should visit the museum"
      ],
      "example": "You should visit the museum.",
      "id": 51
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She avoided talking about it.",
      "answer": "She didn't want to talk about it.",
      "accept": [
        "She kept away from the topic",
        "She didn't want to talk about it"
      ],
      "example": "She didn't want to talk about it.",
      "id": 52
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I can't stand waiting in queues.",
      "answer": "I hate waiting in queues.",
      "accept": [
        "I dislike waiting in queues",
        "I hate waiting in queues"
      ],
      "example": "I hate waiting in queues.",
      "id": 53
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He denied stealing the money.",
      "answer": "He said he hadn't stolen the money.",
      "accept": [
        "He claimed he didn't steal the money",
        "He said he hadn't stolen the money"
      ],
      "example": "He said he hadn't stolen the money.",
      "id": 54
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "They accused him of lying.",
      "answer": "They said he had lied.",
      "accept": [
        "He was accused of lying",
        "They said he had lied"
      ],
      "example": "They said he had lied.",
      "id": 55
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I remember locking the door.",
      "answer": "I remember that I locked the door.",
      "accept": [
        "I recall locking the door",
        "I remember that I locked the door"
      ],
      "example": "I remember that I locked the door.",
      "id": 56
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "Don't forget to call me.",
      "answer": "Remember to call me.",
      "accept": [
        "Make sure you call me",
        "Remember to call me"
      ],
      "example": "Remember to call me.",
      "id": 57
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She suggested going to the cinema.",
      "answer": "She suggested that we go to the cinema.",
      "accept": [
        "She proposed going to the cinema",
        "She suggested that we go to the cinema"
      ],
      "example": "She suggested that we go to the cinema.",
      "id": 58
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I'm sorry for being late.",
      "answer": "I apologise for being late.",
      "accept": [
        "Sorry I'm late",
        "I apologise for being late"
      ],
      "example": "I apologise for being late.",
      "id": 59
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He is likely to win.",
      "answer": "He will probably win.",
      "accept": [
        "He's probably going to win",
        "He will probably win"
      ],
      "example": "He will probably win.",
      "id": 60
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "The problem is hard to solve.",
      "answer": "It's hard to solve the problem.",
      "accept": [
        "Solving the problem is hard",
        "It's hard to solve the problem"
      ],
      "example": "It's hard to solve the problem.",
      "id": 61
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I need someone to help me.",
      "answer": "I need help from someone.",
      "accept": [
        "I need somebody's help",
        "I need help from someone"
      ],
      "example": "I need help from someone.",
      "id": 62
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She got used to the noise.",
      "answer": "The noise became normal for her.",
      "accept": [
        "She became accustomed to the noise",
        "The noise became normal for her"
      ],
      "example": "The noise became normal for her.",
      "id": 63
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He almost never smiles.",
      "answer": "He hardly ever smiles.",
      "accept": [
        "He rarely smiles",
        "He hardly ever smiles"
      ],
      "example": "He hardly ever smiles.",
      "id": 64
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I would rather stay home.",
      "answer": "I'd prefer to stay home.",
      "accept": [
        "I prefer staying home",
        "I'd prefer to stay home"
      ],
      "example": "I'd prefer to stay home.",
      "id": 65
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "There's no point in arguing.",
      "answer": "It's useless to argue.",
      "accept": [
        "Arguing is pointless",
        "It's useless to argue"
      ],
      "example": "It's useless to argue.",
      "id": 66
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She made rapid progress.",
      "answer": "She progressed quickly.",
      "accept": [
        "She improved quickly",
        "She progressed quickly"
      ],
      "example": "She progressed quickly.",
      "id": 67
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "The news came as a surprise.",
      "answer": "I was surprised by the news.",
      "accept": [
        "The news surprised me",
        "I was surprised by the news"
      ],
      "example": "I was surprised by the news.",
      "id": 68
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He took part in the race.",
      "answer": "He participated in the race.",
      "accept": [
        "He joined the race",
        "He participated in the race"
      ],
      "example": "He participated in the race.",
      "id": 69
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I came across an old photo.",
      "answer": "I found an old photo by chance.",
      "accept": [
        "I happened to find an old photo",
        "I found an old photo by chance"
      ],
      "example": "I found an old photo by chance.",
      "id": 70
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She brought up an interesting point.",
      "answer": "She raised an interesting point.",
      "accept": [
        "She mentioned an interesting point",
        "She raised an interesting point"
      ],
      "example": "She raised an interesting point.",
      "id": 71
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "We put off the decision.",
      "answer": "We delayed the decision.",
      "accept": [
        "We postponed the decision",
        "We delayed the decision"
      ],
      "example": "We delayed the decision.",
      "id": 72
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He turned down the offer.",
      "answer": "He rejected the offer.",
      "accept": [
        "He refused the offer",
        "He rejected the offer"
      ],
      "example": "He rejected the offer.",
      "id": 73
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I ran into an old friend.",
      "answer": "I met an old friend by chance.",
      "accept": [
        "I unexpectedly met an old friend",
        "I met an old friend by chance"
      ],
      "example": "I met an old friend by chance.",
      "id": 74
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She sorted out the problem.",
      "answer": "She solved the problem.",
      "accept": [
        "She dealt with the problem",
        "She solved the problem"
      ],
      "example": "She solved the problem.",
      "id": 75
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "Keep an eye on the kids.",
      "answer": "Watch the kids carefully.",
      "accept": [
        "Look after the kids",
        "Watch the kids carefully"
      ],
      "example": "Watch the kids carefully.",
      "id": 76
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He made up his mind.",
      "answer": "He decided.",
      "accept": [
        "He reached a decision",
        "He decided"
      ],
      "example": "He decided.",
      "id": 77
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I can't make out what he means.",
      "answer": "I can't understand what he means.",
      "accept": [
        "I don't understand him",
        "I can't understand what he means"
      ],
      "example": "I can't understand what he means.",
      "id": 78
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She looks down on others.",
      "answer": "She thinks she is better than others.",
      "accept": [
        "She is arrogant towards others",
        "She thinks she is better than others"
      ],
      "example": "She thinks she is better than others.",
      "id": 79
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "We got on well.",
      "answer": "We had a good relationship.",
      "accept": [
        "We had a friendly relationship",
        "We had a good relationship"
      ],
      "example": "We had a good relationship.",
      "id": 80
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "The plan fell through.",
      "answer": "The plan failed.",
      "accept": [
        "The plan didn't work",
        "The plan failed"
      ],
      "example": "The plan failed.",
      "id": 81
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He broke the news gently.",
      "answer": "He told the news carefully.",
      "accept": [
        "He announced the news carefully",
        "He told the news carefully"
      ],
      "example": "He told the news carefully.",
      "id": 82
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I take after my mother.",
      "answer": "I resemble my mother.",
      "accept": [
        "I'm similar to my mother",
        "I resemble my mother"
      ],
      "example": "I resemble my mother.",
      "id": 83
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She carried out the experiment.",
      "answer": "She performed the experiment.",
      "accept": [
        "She did the experiment",
        "She performed the experiment"
      ],
      "example": "She performed the experiment.",
      "id": 84
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "We need to cut down on sugar.",
      "answer": "We should reduce sugar.",
      "accept": [
        "We ought to eat less sugar",
        "We should reduce sugar"
      ],
      "example": "We should reduce sugar.",
      "id": 85
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He pointed out the mistake.",
      "answer": "He showed the mistake.",
      "accept": [
        "He drew attention to the mistake",
        "He showed the mistake"
      ],
      "example": "He showed the mistake.",
      "id": 86
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I ended up staying late.",
      "answer": "Finally I stayed late.",
      "accept": [
        "In the end I stayed late",
        "Finally I stayed late"
      ],
      "example": "Finally I stayed late.",
      "id": 87
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She came up with a solution.",
      "answer": "She invented a solution.",
      "accept": [
        "She thought of a solution",
        "She invented a solution"
      ],
      "example": "She invented a solution.",
      "id": 88
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "They set off early.",
      "answer": "They started their journey early.",
      "accept": [
        "They left early",
        "They started their journey early"
      ],
      "example": "They started their journey early.",
      "id": 89
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I work out at the gym.",
      "answer": "I exercise at the gym.",
      "accept": [
        "I train at the gym",
        "I exercise at the gym"
      ],
      "example": "I exercise at the gym.",
      "id": 90
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He checked in at the hotel.",
      "answer": "He registered at the hotel.",
      "accept": [
        "He arrived and registered at the hotel",
        "He registered at the hotel"
      ],
      "example": "He registered at the hotel.",
      "id": 91
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She filled in the form.",
      "answer": "She completed the form.",
      "accept": [
        "She filled out the form",
        "She completed the form"
      ],
      "example": "She completed the form.",
      "id": 92
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "We ran into difficulties.",
      "answer": "We faced difficulties.",
      "accept": [
        "We encountered problems",
        "We faced difficulties"
      ],
      "example": "We faced difficulties.",
      "id": 93
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He got over the flu.",
      "answer": "He recovered from the flu.",
      "accept": [
        "He recovered after the flu",
        "He recovered from the flu"
      ],
      "example": "He recovered from the flu.",
      "id": 94
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I put up with the noise.",
      "answer": "I tolerated the noise.",
      "accept": [
        "I endured the noise",
        "I tolerated the noise"
      ],
      "example": "I tolerated the noise.",
      "id": 95
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She looked into the matter.",
      "answer": "She investigated the matter.",
      "accept": [
        "She examined the matter",
        "She investigated the matter"
      ],
      "example": "She investigated the matter.",
      "id": 96
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "They called off the match.",
      "answer": "They cancelled the match.",
      "accept": [
        "The match was cancelled",
        "They cancelled the match"
      ],
      "example": "They cancelled the match.",
      "id": 97
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "I bumped into her downtown.",
      "answer": "I met her by chance downtown.",
      "accept": [
        "I unexpectedly met her downtown",
        "I met her by chance downtown"
      ],
      "example": "I met her by chance downtown.",
      "id": 98
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "He held up the traffic.",
      "answer": "He delayed the traffic.",
      "accept": [
        "He caused a traffic delay",
        "He delayed the traffic"
      ],
      "example": "He delayed the traffic.",
      "id": 99
    },
    {
      "subtype": "paraphrase",
      "instruction_ru": "Перефразируй предложение другими словами:",
      "prompt_en": "She passed out from the heat.",
      "answer": "She fainted because of the heat.",
      "accept": [
        "She lost consciousness from the heat",
        "She fainted because of the heat"
      ],
      "example": "She fainted because of the heat.",
      "id": 100
    }
  ],
  "B2": [
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "If I had more free time,",
      "answer": "If I had more free time, I would travel more often.",
      "accept": [
        "I would travel more often",
        "If I had more free time, I would travel more often.",
        "If I had more free time, I would travel more often."
      ],
      "example": "I would travel more often.",
      "id": 1
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She suggested that we",
      "answer": "She suggested that we meet earlier next week.",
      "accept": [
        "meet earlier next week",
        "She suggested that we meet earlier next week.",
        "She suggested that we meet earlier next week."
      ],
      "example": "meet earlier next week.",
      "id": 2
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Despite the difficulties,",
      "answer": "Despite the difficulties, they managed to finish the project.",
      "accept": [
        "they managed to finish the project",
        "Despite the difficulties, they managed to finish the project.",
        "Despite the difficulties, they managed to finish the project."
      ],
      "example": "they managed to finish the project.",
      "id": 3
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Not only did he apologise,",
      "answer": "Not only did he apologise, but he also offered to help.",
      "accept": [
        "but he also offered to help",
        "Not only did he apologise, but he also offered to help.",
        "Not only did he apologise, but he also offered to help."
      ],
      "example": "but he also offered to help.",
      "id": 4
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I wish I",
      "answer": "I wish I had studied harder for the exam.",
      "accept": [
        "had studied harder for the exam",
        "I wish I had studied harder for the exam.",
        "I wish I had studied harder for the exam."
      ],
      "example": "had studied harder for the exam.",
      "id": 5
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The more you practise,",
      "answer": "The more you practise, the better you become.",
      "accept": [
        "the better you become",
        "The more you practise, the better you become.",
        "The more you practise, the better you become."
      ],
      "example": "the better you become.",
      "id": 6
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Had I known about the traffic,",
      "answer": "Had I known about the traffic, I would have left earlier.",
      "accept": [
        "I would have left earlier",
        "Had I known about the traffic, I would have left earlier.",
        "Had I known about the traffic, I would have left earlier."
      ],
      "example": "I would have left earlier.",
      "id": 7
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She is rumoured to",
      "answer": "She is rumoured to be starting a new company.",
      "accept": [
        "be starting a new company",
        "She is rumoured to be starting a new company.",
        "She is rumoured to be starting a new company."
      ],
      "example": "be starting a new company.",
      "id": 8
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "What surprised me most was",
      "answer": "What surprised me most was how calm she remained.",
      "accept": [
        "how calm she remained",
        "What surprised me most was how calm she remained.",
        "What surprised me most was how calm she remained."
      ],
      "example": "how calm she remained.",
      "id": 9
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It's high time we",
      "answer": "It's high time we discussed this problem seriously.",
      "accept": [
        "discussed this problem seriously",
        "It's high time we discussed this problem seriously.",
        "It's high time we discussed this problem seriously."
      ],
      "example": "discussed this problem seriously.",
      "id": 10
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "No sooner had we arrived than",
      "answer": "No sooner had we arrived than it started to rain.",
      "accept": [
        "it started to rain",
        "No sooner had we arrived than it started to rain.",
        "No sooner had we arrived than it started to rain."
      ],
      "example": "it started to rain.",
      "id": 11
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He denied",
      "answer": "He denied having seen the document.",
      "accept": [
        "having seen the document",
        "He denied having seen the document.",
        "He denied having seen the document."
      ],
      "example": "having seen the document.",
      "id": 12
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I'd rather you",
      "answer": "I'd rather you didn't smoke in here.",
      "accept": [
        "didn't smoke in here",
        "I'd rather you didn't smoke in here.",
        "I'd rather you didn't smoke in here."
      ],
      "example": "didn't smoke in here.",
      "id": 13
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She spoke as if",
      "answer": "She spoke as if she knew everything about it.",
      "accept": [
        "she knew everything about it",
        "She spoke as if she knew everything about it.",
        "She spoke as if she knew everything about it."
      ],
      "example": "she knew everything about it.",
      "id": 14
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The reason why I called is",
      "answer": "The reason why I called is that I need your advice.",
      "accept": [
        "that I need your advice",
        "The reason why I called is that I need your advice.",
        "The reason why I called is that I need your advice."
      ],
      "example": "that I need your advice.",
      "id": 15
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Unless we act now,",
      "answer": "Unless we act now, the situation will get worse.",
      "accept": [
        "the situation will get worse",
        "Unless we act now, the situation will get worse.",
        "Unless we act now, the situation will get worse."
      ],
      "example": "the situation will get worse.",
      "id": 16
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Having finished the report,",
      "answer": "Having finished the report, he went home.",
      "accept": [
        "he went home",
        "Having finished the report, he went home.",
        "Having finished the report, he went home."
      ],
      "example": "he went home.",
      "id": 17
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It was such a difficult decision that",
      "answer": "It was such a difficult decision that I needed more time.",
      "accept": [
        "I needed more time",
        "It was such a difficult decision that I needed more time.",
        "It was such a difficult decision that I needed more time."
      ],
      "example": "I needed more time.",
      "id": 18
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "By the time we got there,",
      "answer": "By the time we got there, the shop had already closed.",
      "accept": [
        "the shop had already closed",
        "By the time we got there, the shop had already closed.",
        "By the time we got there, the shop had already closed."
      ],
      "example": "the shop had already closed.",
      "id": 19
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She insisted on",
      "answer": "She insisted on paying for the meal herself.",
      "accept": [
        "paying for the meal herself",
        "She insisted on paying for the meal herself.",
        "She insisted on paying for the meal herself."
      ],
      "example": "paying for the meal herself.",
      "id": 20
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I can't help",
      "answer": "I can't help thinking about what happened.",
      "accept": [
        "thinking about what happened",
        "I can't help thinking about what happened.",
        "I can't help thinking about what happened."
      ],
      "example": "thinking about what happened.",
      "id": 21
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Were I in your position,",
      "answer": "Were I in your position, I would accept the offer.",
      "accept": [
        "I would accept the offer",
        "Were I in your position, I would accept the offer.",
        "Were I in your position, I would accept the offer."
      ],
      "example": "I would accept the offer.",
      "id": 22
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The film was so gripping that",
      "answer": "The film was so gripping that I watched it twice.",
      "accept": [
        "I watched it twice",
        "The film was so gripping that I watched it twice.",
        "The film was so gripping that I watched it twice."
      ],
      "example": "I watched it twice.",
      "id": 23
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He is believed to",
      "answer": "He is believed to have left the country.",
      "accept": [
        "have left the country",
        "He is believed to have left the country.",
        "He is believed to have left the country."
      ],
      "example": "have left the country.",
      "id": 24
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Far from being angry,",
      "answer": "Far from being angry, she seemed amused.",
      "accept": [
        "she seemed amused",
        "Far from being angry, she seemed amused.",
        "Far from being angry, she seemed amused."
      ],
      "example": "she seemed amused.",
      "id": 25
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "On no account should you",
      "answer": "On no account should you share your password.",
      "accept": [
        "share your password",
        "On no account should you share your password.",
        "On no account should you share your password."
      ],
      "example": "share your password.",
      "id": 26
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Little did she know that",
      "answer": "Little did she know that everything would change.",
      "accept": [
        "everything would change",
        "Little did she know that everything would change.",
        "Little did she know that everything would change."
      ],
      "example": "everything would change.",
      "id": 27
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The proposal aims to",
      "answer": "The proposal aims to reduce costs without cutting staff.",
      "accept": [
        "reduce costs without cutting staff",
        "The proposal aims to reduce costs without cutting staff.",
        "The proposal aims to reduce costs without cutting staff."
      ],
      "example": "reduce costs without cutting staff.",
      "id": 28
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In spite of being tired,",
      "answer": "In spite of being tired, he continued working.",
      "accept": [
        "he continued working",
        "In spite of being tired, he continued working.",
        "In spite of being tired, he continued working."
      ],
      "example": "he continued working.",
      "id": 29
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I'd prefer it if you",
      "answer": "I'd prefer it if you came a bit earlier.",
      "accept": [
        "came a bit earlier",
        "I'd prefer it if you came a bit earlier.",
        "I'd prefer it if you came a bit earlier."
      ],
      "example": "came a bit earlier.",
      "id": 30
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She apologised for",
      "answer": "She apologised for being late to the meeting.",
      "accept": [
        "being late to the meeting",
        "She apologised for being late to the meeting.",
        "She apologised for being late to the meeting."
      ],
      "example": "being late to the meeting.",
      "id": 31
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "There's no point in",
      "answer": "There's no point in arguing about it now.",
      "accept": [
        "arguing about it now",
        "There's no point in arguing about it now.",
        "There's no point in arguing about it now."
      ],
      "example": "arguing about it now.",
      "id": 32
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He turned out to be",
      "answer": "He turned out to be a reliable colleague.",
      "accept": [
        "a reliable colleague",
        "He turned out to be a reliable colleague.",
        "He turned out to be a reliable colleague."
      ],
      "example": "a reliable colleague.",
      "id": 33
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "What I need is",
      "answer": "What I need is a clear plan for next week.",
      "accept": [
        "a clear plan for next week",
        "What I need is a clear plan for next week.",
        "What I need is a clear plan for next week."
      ],
      "example": "a clear plan for next week.",
      "id": 34
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Should you need any help,",
      "answer": "Should you need any help, just let me know.",
      "accept": [
        "just let me know",
        "Should you need any help, just let me know.",
        "Should you need any help, just let me know."
      ],
      "example": "just let me know.",
      "id": 35
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The results indicate that",
      "answer": "The results indicate that the method works well.",
      "accept": [
        "the method works well",
        "The results indicate that the method works well.",
        "The results indicate that the method works well."
      ],
      "example": "the method works well.",
      "id": 36
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She went to the library so that",
      "answer": "She went to the library so that she could study in peace.",
      "accept": [
        "she could study in peace",
        "She went to the library so that she could study in peace.",
        "She went to the library so that she could study in peace."
      ],
      "example": "she could study in peace.",
      "id": 37
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He is used to",
      "answer": "He is used to working under pressure.",
      "accept": [
        "working under pressure",
        "He is used to working under pressure.",
        "He is used to working under pressure."
      ],
      "example": "working under pressure.",
      "id": 38
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It looks as though",
      "answer": "It looks as though they have reached an agreement.",
      "accept": [
        "they have reached an agreement",
        "It looks as though they have reached an agreement.",
        "It looks as though they have reached an agreement."
      ],
      "example": "they have reached an agreement.",
      "id": 39
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Only after the meeting did I",
      "answer": "Only after the meeting did I understand the full picture.",
      "accept": [
        "understand the full picture",
        "Only after the meeting did I understand the full picture.",
        "Only after the meeting did I understand the full picture."
      ],
      "example": "understand the full picture.",
      "id": 40
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She prevented me from",
      "answer": "She prevented me from making a serious mistake.",
      "accept": [
        "making a serious mistake",
        "She prevented me from making a serious mistake.",
        "She prevented me from making a serious mistake."
      ],
      "example": "making a serious mistake.",
      "id": 41
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I take it for granted that",
      "answer": "I take it for granted that everyone will arrive on time.",
      "accept": [
        "everyone will arrive on time",
        "I take it for granted that everyone will arrive on time.",
        "I take it for granted that everyone will arrive on time."
      ],
      "example": "everyone will arrive on time.",
      "id": 42
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The company is considering",
      "answer": "The company is considering expanding into new markets.",
      "accept": [
        "expanding into new markets",
        "The company is considering expanding into new markets.",
        "The company is considering expanding into new markets."
      ],
      "example": "expanding into new markets.",
      "id": 43
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He spoke so quietly that",
      "answer": "He spoke so quietly that hardly anyone could hear him.",
      "accept": [
        "hardly anyone could hear him",
        "He spoke so quietly that hardly anyone could hear him.",
        "He spoke so quietly that hardly anyone could hear him."
      ],
      "example": "hardly anyone could hear him.",
      "id": 44
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I'd be grateful if you",
      "answer": "I'd be grateful if you could send the files today.",
      "accept": [
        "could send the files today",
        "I'd be grateful if you could send the files today.",
        "I'd be grateful if you could send the files today."
      ],
      "example": "could send the files today.",
      "id": 45
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The problem lies in",
      "answer": "The problem lies in a lack of clear communication.",
      "accept": [
        "a lack of clear communication",
        "The problem lies in a lack of clear communication.",
        "The problem lies in a lack of clear communication."
      ],
      "example": "a lack of clear communication.",
      "id": 46
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She made it clear that",
      "answer": "She made it clear that she would not change her mind.",
      "accept": [
        "she would not change her mind",
        "She made it clear that she would not change her mind.",
        "She made it clear that she would not change her mind."
      ],
      "example": "she would not change her mind.",
      "id": 47
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "As far as I'm concerned,",
      "answer": "As far as I'm concerned, this is the best option.",
      "accept": [
        "this is the best option",
        "As far as I'm concerned, this is the best option.",
        "As far as I'm concerned, this is the best option."
      ],
      "example": "this is the best option.",
      "id": 48
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He claimed to have",
      "answer": "He claimed to have finished the work already.",
      "accept": [
        "finished the work already",
        "He claimed to have finished the work already.",
        "He claimed to have finished the work already."
      ],
      "example": "finished the work already.",
      "id": 49
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The longer we wait,",
      "answer": "The longer we wait, the harder it will become.",
      "accept": [
        "the harder it will become",
        "The longer we wait, the harder it will become.",
        "The longer we wait, the harder it will become."
      ],
      "example": "the harder it will become.",
      "id": 50
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "If I had more free time,",
      "answer": "If I had more free time, I would travel more often as planned.",
      "accept": [
        "I would travel more often as planned",
        "If I had more free time, I would travel more often as planned.",
        "If I had more free time, I would travel more often as planned."
      ],
      "example": "I would travel more often as planned.",
      "id": 51
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She suggested that we",
      "answer": "She suggested that we meet earlier next week as planned.",
      "accept": [
        "meet earlier next week as planned",
        "She suggested that we meet earlier next week as planned.",
        "She suggested that we meet earlier next week as planned."
      ],
      "example": "meet earlier next week as planned.",
      "id": 52
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Despite the difficulties,",
      "answer": "Despite the difficulties, they managed to finish the project as planned.",
      "accept": [
        "they managed to finish the project as planned",
        "Despite the difficulties, they managed to finish the project as planned.",
        "Despite the difficulties, they managed to finish the project as planned."
      ],
      "example": "they managed to finish the project as planned.",
      "id": 53
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Not only did he apologise,",
      "answer": "Not only did he apologise, but he also offered to help as planned.",
      "accept": [
        "but he also offered to help as planned",
        "Not only did he apologise, but he also offered to help as planned.",
        "Not only did he apologise, but he also offered to help as planned."
      ],
      "example": "but he also offered to help as planned.",
      "id": 54
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I wish I",
      "answer": "I wish I had studied harder for the exam as planned.",
      "accept": [
        "had studied harder for the exam as planned",
        "I wish I had studied harder for the exam as planned.",
        "I wish I had studied harder for the exam as planned."
      ],
      "example": "had studied harder for the exam as planned.",
      "id": 55
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The more you practise,",
      "answer": "The more you practise, the better you become as planned.",
      "accept": [
        "the better you become as planned",
        "The more you practise, the better you become as planned.",
        "The more you practise, the better you become as planned."
      ],
      "example": "the better you become as planned.",
      "id": 56
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Had I known about the traffic,",
      "answer": "Had I known about the traffic, I would have left earlier as planned.",
      "accept": [
        "I would have left earlier as planned",
        "Had I known about the traffic, I would have left earlier as planned.",
        "Had I known about the traffic, I would have left earlier as planned."
      ],
      "example": "I would have left earlier as planned.",
      "id": 57
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She is rumoured to",
      "answer": "She is rumoured to be starting a new company as planned.",
      "accept": [
        "be starting a new company as planned",
        "She is rumoured to be starting a new company as planned.",
        "She is rumoured to be starting a new company as planned."
      ],
      "example": "be starting a new company as planned.",
      "id": 58
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "What surprised me most was",
      "answer": "What surprised me most was how calm she remained as planned.",
      "accept": [
        "how calm she remained as planned",
        "What surprised me most was how calm she remained as planned.",
        "What surprised me most was how calm she remained as planned."
      ],
      "example": "how calm she remained as planned.",
      "id": 59
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It's high time we",
      "answer": "It's high time we discussed this problem seriously as planned.",
      "accept": [
        "discussed this problem seriously as planned",
        "It's high time we discussed this problem seriously as planned.",
        "It's high time we discussed this problem seriously as planned."
      ],
      "example": "discussed this problem seriously as planned.",
      "id": 60
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "No sooner had we arrived than",
      "answer": "No sooner had we arrived than it started to rain as planned.",
      "accept": [
        "it started to rain as planned",
        "No sooner had we arrived than it started to rain as planned.",
        "No sooner had we arrived than it started to rain as planned."
      ],
      "example": "it started to rain as planned.",
      "id": 61
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He denied",
      "answer": "He denied having seen the document as planned.",
      "accept": [
        "having seen the document as planned",
        "He denied having seen the document as planned.",
        "He denied having seen the document as planned."
      ],
      "example": "having seen the document as planned.",
      "id": 62
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I'd rather you",
      "answer": "I'd rather you didn't smoke in here as planned.",
      "accept": [
        "didn't smoke in here as planned",
        "I'd rather you didn't smoke in here as planned.",
        "I'd rather you didn't smoke in here as planned."
      ],
      "example": "didn't smoke in here as planned.",
      "id": 63
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She spoke as if",
      "answer": "She spoke as if she knew everything about it as planned.",
      "accept": [
        "she knew everything about it as planned",
        "She spoke as if she knew everything about it as planned.",
        "She spoke as if she knew everything about it as planned."
      ],
      "example": "she knew everything about it as planned.",
      "id": 64
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The reason why I called is",
      "answer": "The reason why I called is that I need your advice as planned.",
      "accept": [
        "that I need your advice as planned",
        "The reason why I called is that I need your advice as planned.",
        "The reason why I called is that I need your advice as planned."
      ],
      "example": "that I need your advice as planned.",
      "id": 65
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Unless we act now,",
      "answer": "Unless we act now, the situation will get worse as planned.",
      "accept": [
        "the situation will get worse as planned",
        "Unless we act now, the situation will get worse as planned.",
        "Unless we act now, the situation will get worse as planned."
      ],
      "example": "the situation will get worse as planned.",
      "id": 66
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Having finished the report,",
      "answer": "Having finished the report, he went home as planned.",
      "accept": [
        "he went home as planned",
        "Having finished the report, he went home as planned.",
        "Having finished the report, he went home as planned."
      ],
      "example": "he went home as planned.",
      "id": 67
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It was such a difficult decision that",
      "answer": "It was such a difficult decision that I needed more time as planned.",
      "accept": [
        "I needed more time as planned",
        "It was such a difficult decision that I needed more time as planned.",
        "It was such a difficult decision that I needed more time as planned."
      ],
      "example": "I needed more time as planned.",
      "id": 68
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "By the time we got there,",
      "answer": "By the time we got there, the shop had already closed as planned.",
      "accept": [
        "the shop had already closed as planned",
        "By the time we got there, the shop had already closed as planned.",
        "By the time we got there, the shop had already closed as planned."
      ],
      "example": "the shop had already closed as planned.",
      "id": 69
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She insisted on",
      "answer": "She insisted on paying for the meal herself as planned.",
      "accept": [
        "paying for the meal herself as planned",
        "She insisted on paying for the meal herself as planned.",
        "She insisted on paying for the meal herself as planned."
      ],
      "example": "paying for the meal herself as planned.",
      "id": 70
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I can't help",
      "answer": "I can't help thinking about what happened as planned.",
      "accept": [
        "thinking about what happened as planned",
        "I can't help thinking about what happened as planned.",
        "I can't help thinking about what happened as planned."
      ],
      "example": "thinking about what happened as planned.",
      "id": 71
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Were I in your position,",
      "answer": "Were I in your position, I would accept the offer as planned.",
      "accept": [
        "I would accept the offer as planned",
        "Were I in your position, I would accept the offer as planned.",
        "Were I in your position, I would accept the offer as planned."
      ],
      "example": "I would accept the offer as planned.",
      "id": 72
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The film was so gripping that",
      "answer": "The film was so gripping that I watched it twice as planned.",
      "accept": [
        "I watched it twice as planned",
        "The film was so gripping that I watched it twice as planned.",
        "The film was so gripping that I watched it twice as planned."
      ],
      "example": "I watched it twice as planned.",
      "id": 73
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He is believed to",
      "answer": "He is believed to have left the country as planned.",
      "accept": [
        "have left the country as planned",
        "He is believed to have left the country as planned.",
        "He is believed to have left the country as planned."
      ],
      "example": "have left the country as planned.",
      "id": 74
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Far from being angry,",
      "answer": "Far from being angry, she seemed amused as planned.",
      "accept": [
        "she seemed amused as planned",
        "Far from being angry, she seemed amused as planned.",
        "Far from being angry, she seemed amused as planned."
      ],
      "example": "she seemed amused as planned.",
      "id": 75
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "On no account should you",
      "answer": "On no account should you share your password as planned.",
      "accept": [
        "share your password as planned",
        "On no account should you share your password as planned.",
        "On no account should you share your password as planned."
      ],
      "example": "share your password as planned.",
      "id": 76
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Little did she know that",
      "answer": "Little did she know that everything would change as planned.",
      "accept": [
        "everything would change as planned",
        "Little did she know that everything would change as planned.",
        "Little did she know that everything would change as planned."
      ],
      "example": "everything would change as planned.",
      "id": 77
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The proposal aims to",
      "answer": "The proposal aims to reduce costs without cutting staff as planned.",
      "accept": [
        "reduce costs without cutting staff as planned",
        "The proposal aims to reduce costs without cutting staff as planned.",
        "The proposal aims to reduce costs without cutting staff as planned."
      ],
      "example": "reduce costs without cutting staff as planned.",
      "id": 78
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In spite of being tired,",
      "answer": "In spite of being tired, he continued working as planned.",
      "accept": [
        "he continued working as planned",
        "In spite of being tired, he continued working as planned.",
        "In spite of being tired, he continued working as planned."
      ],
      "example": "he continued working as planned.",
      "id": 79
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I'd prefer it if you",
      "answer": "I'd prefer it if you came a bit earlier as planned.",
      "accept": [
        "came a bit earlier as planned",
        "I'd prefer it if you came a bit earlier as planned.",
        "I'd prefer it if you came a bit earlier as planned."
      ],
      "example": "came a bit earlier as planned.",
      "id": 80
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She apologised for",
      "answer": "She apologised for being late to the meeting as planned.",
      "accept": [
        "being late to the meeting as planned",
        "She apologised for being late to the meeting as planned.",
        "She apologised for being late to the meeting as planned."
      ],
      "example": "being late to the meeting as planned.",
      "id": 81
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "There's no point in",
      "answer": "There's no point in arguing about it now as planned.",
      "accept": [
        "arguing about it now as planned",
        "There's no point in arguing about it now as planned.",
        "There's no point in arguing about it now as planned."
      ],
      "example": "arguing about it now as planned.",
      "id": 82
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He turned out to be",
      "answer": "He turned out to be a reliable colleague as planned.",
      "accept": [
        "a reliable colleague as planned",
        "He turned out to be a reliable colleague as planned.",
        "He turned out to be a reliable colleague as planned."
      ],
      "example": "a reliable colleague as planned.",
      "id": 83
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "What I need is",
      "answer": "What I need is a clear plan for next week as planned.",
      "accept": [
        "a clear plan for next week as planned",
        "What I need is a clear plan for next week as planned.",
        "What I need is a clear plan for next week as planned."
      ],
      "example": "a clear plan for next week as planned.",
      "id": 84
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Should you need any help,",
      "answer": "Should you need any help, just let me know as planned.",
      "accept": [
        "just let me know as planned",
        "Should you need any help, just let me know as planned.",
        "Should you need any help, just let me know as planned."
      ],
      "example": "just let me know as planned.",
      "id": 85
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The results indicate that",
      "answer": "The results indicate that the method works well as planned.",
      "accept": [
        "the method works well as planned",
        "The results indicate that the method works well as planned.",
        "The results indicate that the method works well as planned."
      ],
      "example": "the method works well as planned.",
      "id": 86
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She went to the library so that",
      "answer": "She went to the library so that she could study in peace as planned.",
      "accept": [
        "she could study in peace as planned",
        "She went to the library so that she could study in peace as planned.",
        "She went to the library so that she could study in peace as planned."
      ],
      "example": "she could study in peace as planned.",
      "id": 87
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He is used to",
      "answer": "He is used to working under pressure as planned.",
      "accept": [
        "working under pressure as planned",
        "He is used to working under pressure as planned.",
        "He is used to working under pressure as planned."
      ],
      "example": "working under pressure as planned.",
      "id": 88
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It looks as though",
      "answer": "It looks as though they have reached an agreement as planned.",
      "accept": [
        "they have reached an agreement as planned",
        "It looks as though they have reached an agreement as planned.",
        "It looks as though they have reached an agreement as planned."
      ],
      "example": "they have reached an agreement as planned.",
      "id": 89
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Only after the meeting did I",
      "answer": "Only after the meeting did I understand the full picture as planned.",
      "accept": [
        "understand the full picture as planned",
        "Only after the meeting did I understand the full picture as planned.",
        "Only after the meeting did I understand the full picture as planned."
      ],
      "example": "understand the full picture as planned.",
      "id": 90
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She prevented me from",
      "answer": "She prevented me from making a serious mistake as planned.",
      "accept": [
        "making a serious mistake as planned",
        "She prevented me from making a serious mistake as planned.",
        "She prevented me from making a serious mistake as planned."
      ],
      "example": "making a serious mistake as planned.",
      "id": 91
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I take it for granted that",
      "answer": "I take it for granted that everyone will arrive on time as planned.",
      "accept": [
        "everyone will arrive on time as planned",
        "I take it for granted that everyone will arrive on time as planned.",
        "I take it for granted that everyone will arrive on time as planned."
      ],
      "example": "everyone will arrive on time as planned.",
      "id": 92
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The company is considering",
      "answer": "The company is considering expanding into new markets as planned.",
      "accept": [
        "expanding into new markets as planned",
        "The company is considering expanding into new markets as planned.",
        "The company is considering expanding into new markets as planned."
      ],
      "example": "expanding into new markets as planned.",
      "id": 93
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He spoke so quietly that",
      "answer": "He spoke so quietly that hardly anyone could hear him as planned.",
      "accept": [
        "hardly anyone could hear him as planned",
        "He spoke so quietly that hardly anyone could hear him as planned.",
        "He spoke so quietly that hardly anyone could hear him as planned."
      ],
      "example": "hardly anyone could hear him as planned.",
      "id": 94
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "I'd be grateful if you",
      "answer": "I'd be grateful if you could send the files today as planned.",
      "accept": [
        "could send the files today as planned",
        "I'd be grateful if you could send the files today as planned.",
        "I'd be grateful if you could send the files today as planned."
      ],
      "example": "could send the files today as planned.",
      "id": 95
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The problem lies in",
      "answer": "The problem lies in a lack of clear communication as planned.",
      "accept": [
        "a lack of clear communication as planned",
        "The problem lies in a lack of clear communication as planned.",
        "The problem lies in a lack of clear communication as planned."
      ],
      "example": "a lack of clear communication as planned.",
      "id": 96
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She made it clear that",
      "answer": "She made it clear that she would not change her mind as planned.",
      "accept": [
        "she would not change her mind as planned",
        "She made it clear that she would not change her mind as planned.",
        "She made it clear that she would not change her mind as planned."
      ],
      "example": "she would not change her mind as planned.",
      "id": 97
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "As far as I'm concerned,",
      "answer": "As far as I'm concerned, this is the best option as planned.",
      "accept": [
        "this is the best option as planned",
        "As far as I'm concerned, this is the best option as planned.",
        "As far as I'm concerned, this is the best option as planned."
      ],
      "example": "this is the best option as planned.",
      "id": 98
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He claimed to have",
      "answer": "He claimed to have finished the work already as planned.",
      "accept": [
        "finished the work already as planned",
        "He claimed to have finished the work already as planned.",
        "He claimed to have finished the work already as planned."
      ],
      "example": "finished the work already as planned.",
      "id": 99
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The longer we wait,",
      "answer": "The longer we wait, the harder it will become as planned.",
      "accept": [
        "the harder it will become as planned",
        "The longer we wait, the harder it will become as planned.",
        "The longer we wait, the harder it will become as planned."
      ],
      "example": "the harder it will become as planned.",
      "id": 100
    }
  ],
  "C1": [
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Were it not for her support,",
      "answer": "Were it not for her support, I would never have completed the research.",
      "accept": [
        "I would never have completed the research",
        "Were it not for her support, I would never have completed the research.",
        "Were it not for her support, I would never have completed the research."
      ],
      "example": "I would never have completed the research.",
      "id": 1
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is widely acknowledged that",
      "answer": "It is widely acknowledged that climate policy requires global cooperation.",
      "accept": [
        "climate policy requires global cooperation",
        "It is widely acknowledged that climate policy requires global cooperation.",
        "It is widely acknowledged that climate policy requires global cooperation."
      ],
      "example": "climate policy requires global cooperation.",
      "id": 2
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The committee recommended that the policy",
      "answer": "The committee recommended that the policy be reviewed within six months.",
      "accept": [
        "be reviewed within six months",
        "The committee recommended that the policy be reviewed within six months.",
        "The committee recommended that the policy be reviewed within six months."
      ],
      "example": "be reviewed within six months.",
      "id": 3
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Such was the complexity of the case that",
      "answer": "Such was the complexity of the case that experts struggled to agree.",
      "accept": [
        "experts struggled to agree",
        "Such was the complexity of the case that experts struggled to agree.",
        "Such was the complexity of the case that experts struggled to agree."
      ],
      "example": "experts struggled to agree.",
      "id": 4
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Scarcely had the announcement been made when",
      "answer": "Scarcely had the announcement been made when the markets reacted sharply.",
      "accept": [
        "the markets reacted sharply",
        "Scarcely had the announcement been made when the markets reacted sharply.",
        "Scarcely had the announcement been made when the markets reacted sharply."
      ],
      "example": "the markets reacted sharply.",
      "id": 5
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In light of recent findings,",
      "answer": "In light of recent findings, we should revise our assumptions.",
      "accept": [
        "we should revise our assumptions",
        "In light of recent findings, we should revise our assumptions.",
        "In light of recent findings, we should revise our assumptions."
      ],
      "example": "we should revise our assumptions.",
      "id": 6
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He is unlikely to",
      "answer": "He is unlikely to accept the terms without negotiation.",
      "accept": [
        "accept the terms without negotiation",
        "He is unlikely to accept the terms without negotiation.",
        "He is unlikely to accept the terms without negotiation."
      ],
      "example": "accept the terms without negotiation.",
      "id": 7
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "What remains unclear is",
      "answer": "What remains unclear is how the funding will be allocated.",
      "accept": [
        "how the funding will be allocated",
        "What remains unclear is how the funding will be allocated.",
        "What remains unclear is how the funding will be allocated."
      ],
      "example": "how the funding will be allocated.",
      "id": 8
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Far be it from me to criticise, but",
      "answer": "Far be it from me to criticise, but the timeline seems unrealistic.",
      "accept": [
        "the timeline seems unrealistic",
        "Far be it from me to criticise, but the timeline seems unrealistic.",
        "Far be it from me to criticise, but the timeline seems unrealistic."
      ],
      "example": "the timeline seems unrealistic.",
      "id": 9
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The data suggest a correlation between",
      "answer": "The data suggest a correlation between stress levels and productivity.",
      "accept": [
        "stress levels and productivity",
        "The data suggest a correlation between stress levels and productivity.",
        "The data suggest a correlation between stress levels and productivity."
      ],
      "example": "stress levels and productivity.",
      "id": 10
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Irrespective of the cost,",
      "answer": "Irrespective of the cost, safety must remain the priority.",
      "accept": [
        "safety must remain the priority",
        "Irrespective of the cost, safety must remain the priority.",
        "Irrespective of the cost, safety must remain the priority."
      ],
      "example": "safety must remain the priority.",
      "id": 11
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She framed the argument in terms of",
      "answer": "She framed the argument in terms of long-term sustainability.",
      "accept": [
        "long-term sustainability",
        "She framed the argument in terms of long-term sustainability.",
        "She framed the argument in terms of long-term sustainability."
      ],
      "example": "long-term sustainability.",
      "id": 12
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It goes without saying that",
      "answer": "It goes without saying that transparency builds public trust.",
      "accept": [
        "transparency builds public trust",
        "It goes without saying that transparency builds public trust.",
        "It goes without saying that transparency builds public trust."
      ],
      "example": "transparency builds public trust.",
      "id": 13
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Having been delayed twice already,",
      "answer": "Having been delayed twice already, the launch was postponed again.",
      "accept": [
        "the launch was postponed again",
        "Having been delayed twice already, the launch was postponed again.",
        "Having been delayed twice already, the launch was postponed again."
      ],
      "example": "the launch was postponed again.",
      "id": 14
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The proposal falls short of",
      "answer": "The proposal falls short of addressing the core issue.",
      "accept": [
        "addressing the core issue",
        "The proposal falls short of addressing the core issue.",
        "The proposal falls short of addressing the core issue."
      ],
      "example": "addressing the core issue.",
      "id": 15
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "At no point did he",
      "answer": "At no point did he admit that he was wrong.",
      "accept": [
        "admit that he was wrong",
        "At no point did he admit that he was wrong.",
        "At no point did he admit that he was wrong."
      ],
      "example": "admit that he was wrong.",
      "id": 16
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The more nuanced the analysis becomes,",
      "answer": "The more nuanced the analysis becomes, the harder it is to summarise.",
      "accept": [
        "the harder it is to summarise",
        "The more nuanced the analysis becomes, the harder it is to summarise.",
        "The more nuanced the analysis becomes, the harder it is to summarise."
      ],
      "example": "the harder it is to summarise.",
      "id": 17
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She took issue with",
      "answer": "She took issue with the way the results were presented.",
      "accept": [
        "the way the results were presented",
        "She took issue with the way the results were presented.",
        "She took issue with the way the results were presented."
      ],
      "example": "the way the results were presented.",
      "id": 18
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In the event of a system failure,",
      "answer": "In the event of a system failure, backup procedures will apply.",
      "accept": [
        "backup procedures will apply",
        "In the event of a system failure, backup procedures will apply.",
        "In the event of a system failure, backup procedures will apply."
      ],
      "example": "backup procedures will apply.",
      "id": 19
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He remains sceptical as to whether",
      "answer": "He remains sceptical as to whether the reform will deliver results.",
      "accept": [
        "the reform will deliver results",
        "He remains sceptical as to whether the reform will deliver results.",
        "He remains sceptical as to whether the reform will deliver results."
      ],
      "example": "the reform will deliver results.",
      "id": 20
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The findings cast doubt on",
      "answer": "The findings cast doubt on the previous methodology.",
      "accept": [
        "the previous methodology",
        "The findings cast doubt on the previous methodology.",
        "The findings cast doubt on the previous methodology."
      ],
      "example": "the previous methodology.",
      "id": 21
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is imperative that we",
      "answer": "It is imperative that we act before the deadline.",
      "accept": [
        "act before the deadline",
        "It is imperative that we act before the deadline.",
        "It is imperative that we act before the deadline."
      ],
      "example": "act before the deadline.",
      "id": 22
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Not until the audit was complete did",
      "answer": "Not until the audit was complete did the full extent of the losses emerge.",
      "accept": [
        "the full extent of the losses emerge",
        "Not until the audit was complete did the full extent of the losses emerge.",
        "Not until the audit was complete did the full extent of the losses emerge."
      ],
      "example": "the full extent of the losses emerge.",
      "id": 23
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She attributed the delay to",
      "answer": "She attributed the delay to unforeseen logistical problems.",
      "accept": [
        "unforeseen logistical problems",
        "She attributed the delay to unforeseen logistical problems.",
        "She attributed the delay to unforeseen logistical problems."
      ],
      "example": "unforeseen logistical problems.",
      "id": 24
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The framework seeks to reconcile",
      "answer": "The framework seeks to reconcile innovation with regulation.",
      "accept": [
        "innovation with regulation",
        "The framework seeks to reconcile innovation with regulation.",
        "The framework seeks to reconcile innovation with regulation."
      ],
      "example": "innovation with regulation.",
      "id": 25
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "There is growing consensus that",
      "answer": "There is growing consensus that remote work is here to stay.",
      "accept": [
        "remote work is here to stay",
        "There is growing consensus that remote work is here to stay.",
        "There is growing consensus that remote work is here to stay."
      ],
      "example": "remote work is here to stay.",
      "id": 26
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He challenged the assumption that",
      "answer": "He challenged the assumption that growth alone ensures stability.",
      "accept": [
        "growth alone ensures stability",
        "He challenged the assumption that growth alone ensures stability.",
        "He challenged the assumption that growth alone ensures stability."
      ],
      "example": "growth alone ensures stability.",
      "id": 27
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In retrospect,",
      "answer": "In retrospect, the decision appears short-sighted.",
      "accept": [
        "the decision appears short-sighted",
        "In retrospect, the decision appears short-sighted.",
        "In retrospect, the decision appears short-sighted."
      ],
      "example": "the decision appears short-sighted.",
      "id": 28
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The report highlights the need for",
      "answer": "The report highlights the need for more rigorous oversight.",
      "accept": [
        "more rigorous oversight",
        "The report highlights the need for more rigorous oversight.",
        "The report highlights the need for more rigorous oversight."
      ],
      "example": "more rigorous oversight.",
      "id": 29
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Be that as it may,",
      "answer": "Be that as it may, we still need a practical solution.",
      "accept": [
        "we still need a practical solution",
        "Be that as it may, we still need a practical solution.",
        "Be that as it may, we still need a practical solution."
      ],
      "example": "we still need a practical solution.",
      "id": 30
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She was instrumental in",
      "answer": "She was instrumental in securing the partnership.",
      "accept": [
        "securing the partnership",
        "She was instrumental in securing the partnership.",
        "She was instrumental in securing the partnership."
      ],
      "example": "securing the partnership.",
      "id": 31
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The argument hinges on",
      "answer": "The argument hinges on the reliability of the data.",
      "accept": [
        "the reliability of the data",
        "The argument hinges on the reliability of the data.",
        "The argument hinges on the reliability of the data."
      ],
      "example": "the reliability of the data.",
      "id": 32
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It would be premature to",
      "answer": "It would be premature to draw firm conclusions yet.",
      "accept": [
        "draw firm conclusions yet",
        "It would be premature to draw firm conclusions yet.",
        "It would be premature to draw firm conclusions yet."
      ],
      "example": "draw firm conclusions yet.",
      "id": 33
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He dismissed the criticism as",
      "answer": "He dismissed the criticism as politically motivated.",
      "accept": [
        "politically motivated",
        "He dismissed the criticism as politically motivated.",
        "He dismissed the criticism as politically motivated."
      ],
      "example": "politically motivated.",
      "id": 34
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The initiative is geared towards",
      "answer": "The initiative is geared towards reducing inequality.",
      "accept": [
        "reducing inequality",
        "The initiative is geared towards reducing inequality.",
        "The initiative is geared towards reducing inequality."
      ],
      "example": "reducing inequality.",
      "id": 35
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Only by collaborating closely can we",
      "answer": "Only by collaborating closely can we achieve meaningful change.",
      "accept": [
        "achieve meaningful change",
        "Only by collaborating closely can we achieve meaningful change.",
        "Only by collaborating closely can we achieve meaningful change."
      ],
      "example": "achieve meaningful change.",
      "id": 36
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She raised concerns regarding",
      "answer": "She raised concerns regarding the ethical implications.",
      "accept": [
        "the ethical implications",
        "She raised concerns regarding the ethical implications.",
        "She raised concerns regarding the ethical implications."
      ],
      "example": "the ethical implications.",
      "id": 37
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The evidence is insufficient to",
      "answer": "The evidence is insufficient to support such a strong claim.",
      "accept": [
        "support such a strong claim",
        "The evidence is insufficient to support such a strong claim.",
        "The evidence is insufficient to support such a strong claim."
      ],
      "example": "support such a strong claim.",
      "id": 38
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Insofar as the budget allows,",
      "answer": "Insofar as the budget allows, we will expand the programme.",
      "accept": [
        "we will expand the programme",
        "Insofar as the budget allows, we will expand the programme.",
        "Insofar as the budget allows, we will expand the programme."
      ],
      "example": "we will expand the programme.",
      "id": 39
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He failed to account for",
      "answer": "He failed to account for seasonal variations in demand.",
      "accept": [
        "seasonal variations in demand",
        "He failed to account for seasonal variations in demand.",
        "He failed to account for seasonal variations in demand."
      ],
      "example": "seasonal variations in demand.",
      "id": 40
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The discussion centred on",
      "answer": "The discussion centred on how to balance risk and reward.",
      "accept": [
        "how to balance risk and reward",
        "The discussion centred on how to balance risk and reward.",
        "The discussion centred on how to balance risk and reward."
      ],
      "example": "how to balance risk and reward.",
      "id": 41
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is conceivable that",
      "answer": "It is conceivable that the policy will be revised soon.",
      "accept": [
        "the policy will be revised soon",
        "It is conceivable that the policy will be revised soon.",
        "It is conceivable that the policy will be revised soon."
      ],
      "example": "the policy will be revised soon.",
      "id": 42
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She underscored the importance of",
      "answer": "She underscored the importance of continuous professional development.",
      "accept": [
        "continuous professional development",
        "She underscored the importance of continuous professional development.",
        "She underscored the importance of continuous professional development."
      ],
      "example": "continuous professional development.",
      "id": 43
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The outcome hinges largely on",
      "answer": "The outcome hinges largely on public engagement.",
      "accept": [
        "public engagement",
        "The outcome hinges largely on public engagement.",
        "The outcome hinges largely on public engagement."
      ],
      "example": "public engagement.",
      "id": 44
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Notwithstanding earlier objections,",
      "answer": "Notwithstanding earlier objections, the bill was approved.",
      "accept": [
        "the bill was approved",
        "Notwithstanding earlier objections, the bill was approved.",
        "Notwithstanding earlier objections, the bill was approved."
      ],
      "example": "the bill was approved.",
      "id": 45
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He ventured to suggest that",
      "answer": "He ventured to suggest that a compromise was still possible.",
      "accept": [
        "a compromise was still possible",
        "He ventured to suggest that a compromise was still possible.",
        "He ventured to suggest that a compromise was still possible."
      ],
      "example": "a compromise was still possible.",
      "id": 46
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The analysis falls into the trap of",
      "answer": "The analysis falls into the trap of oversimplifying the causes.",
      "accept": [
        "oversimplifying the causes",
        "The analysis falls into the trap of oversimplifying the causes.",
        "The analysis falls into the trap of oversimplifying the causes."
      ],
      "example": "oversimplifying the causes.",
      "id": 47
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In practical terms,",
      "answer": "In practical terms, this means higher operating costs.",
      "accept": [
        "this means higher operating costs",
        "In practical terms, this means higher operating costs.",
        "In practical terms, this means higher operating costs."
      ],
      "example": "this means higher operating costs.",
      "id": 48
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She remains ambivalent about",
      "answer": "She remains ambivalent about accepting the promotion.",
      "accept": [
        "accepting the promotion",
        "She remains ambivalent about accepting the promotion.",
        "She remains ambivalent about accepting the promotion."
      ],
      "example": "accepting the promotion.",
      "id": 49
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The strategy is predicated on",
      "answer": "The strategy is predicated on sustained investment.",
      "accept": [
        "sustained investment",
        "The strategy is predicated on sustained investment.",
        "The strategy is predicated on sustained investment."
      ],
      "example": "sustained investment.",
      "id": 50
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Were it not for her support,",
      "answer": "Were it not for her support, I would never have completed the research as planned.",
      "accept": [
        "I would never have completed the research as planned",
        "Were it not for her support, I would never have completed the research as planned.",
        "Were it not for her support, I would never have completed the research as planned."
      ],
      "example": "I would never have completed the research as planned.",
      "id": 51
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is widely acknowledged that",
      "answer": "It is widely acknowledged that climate policy requires global cooperation as planned.",
      "accept": [
        "climate policy requires global cooperation as planned",
        "It is widely acknowledged that climate policy requires global cooperation as planned.",
        "It is widely acknowledged that climate policy requires global cooperation as planned."
      ],
      "example": "climate policy requires global cooperation as planned.",
      "id": 52
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The committee recommended that the policy",
      "answer": "The committee recommended that the policy be reviewed within six months as planned.",
      "accept": [
        "be reviewed within six months as planned",
        "The committee recommended that the policy be reviewed within six months as planned.",
        "The committee recommended that the policy be reviewed within six months as planned."
      ],
      "example": "be reviewed within six months as planned.",
      "id": 53
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Such was the complexity of the case that",
      "answer": "Such was the complexity of the case that experts struggled to agree as planned.",
      "accept": [
        "experts struggled to agree as planned",
        "Such was the complexity of the case that experts struggled to agree as planned.",
        "Such was the complexity of the case that experts struggled to agree as planned."
      ],
      "example": "experts struggled to agree as planned.",
      "id": 54
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Scarcely had the announcement been made when",
      "answer": "Scarcely had the announcement been made when the markets reacted sharply as planned.",
      "accept": [
        "the markets reacted sharply as planned",
        "Scarcely had the announcement been made when the markets reacted sharply as planned.",
        "Scarcely had the announcement been made when the markets reacted sharply as planned."
      ],
      "example": "the markets reacted sharply as planned.",
      "id": 55
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In light of recent findings,",
      "answer": "In light of recent findings, we should revise our assumptions as planned.",
      "accept": [
        "we should revise our assumptions as planned",
        "In light of recent findings, we should revise our assumptions as planned.",
        "In light of recent findings, we should revise our assumptions as planned."
      ],
      "example": "we should revise our assumptions as planned.",
      "id": 56
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He is unlikely to",
      "answer": "He is unlikely to accept the terms without negotiation as planned.",
      "accept": [
        "accept the terms without negotiation as planned",
        "He is unlikely to accept the terms without negotiation as planned.",
        "He is unlikely to accept the terms without negotiation as planned."
      ],
      "example": "accept the terms without negotiation as planned.",
      "id": 57
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "What remains unclear is",
      "answer": "What remains unclear is how the funding will be allocated as planned.",
      "accept": [
        "how the funding will be allocated as planned",
        "What remains unclear is how the funding will be allocated as planned.",
        "What remains unclear is how the funding will be allocated as planned."
      ],
      "example": "how the funding will be allocated as planned.",
      "id": 58
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Far be it from me to criticise, but",
      "answer": "Far be it from me to criticise, but the timeline seems unrealistic as planned.",
      "accept": [
        "the timeline seems unrealistic as planned",
        "Far be it from me to criticise, but the timeline seems unrealistic as planned.",
        "Far be it from me to criticise, but the timeline seems unrealistic as planned."
      ],
      "example": "the timeline seems unrealistic as planned.",
      "id": 59
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The data suggest a correlation between",
      "answer": "The data suggest a correlation between stress levels and productivity as planned.",
      "accept": [
        "stress levels and productivity as planned",
        "The data suggest a correlation between stress levels and productivity as planned.",
        "The data suggest a correlation between stress levels and productivity as planned."
      ],
      "example": "stress levels and productivity as planned.",
      "id": 60
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Irrespective of the cost,",
      "answer": "Irrespective of the cost, safety must remain the priority as planned.",
      "accept": [
        "safety must remain the priority as planned",
        "Irrespective of the cost, safety must remain the priority as planned.",
        "Irrespective of the cost, safety must remain the priority as planned."
      ],
      "example": "safety must remain the priority as planned.",
      "id": 61
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She framed the argument in terms of",
      "answer": "She framed the argument in terms of long-term sustainability as planned.",
      "accept": [
        "long-term sustainability as planned",
        "She framed the argument in terms of long-term sustainability as planned.",
        "She framed the argument in terms of long-term sustainability as planned."
      ],
      "example": "long-term sustainability as planned.",
      "id": 62
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It goes without saying that",
      "answer": "It goes without saying that transparency builds public trust as planned.",
      "accept": [
        "transparency builds public trust as planned",
        "It goes without saying that transparency builds public trust as planned.",
        "It goes without saying that transparency builds public trust as planned."
      ],
      "example": "transparency builds public trust as planned.",
      "id": 63
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Having been delayed twice already,",
      "answer": "Having been delayed twice already, the launch was postponed again as planned.",
      "accept": [
        "the launch was postponed again as planned",
        "Having been delayed twice already, the launch was postponed again as planned.",
        "Having been delayed twice already, the launch was postponed again as planned."
      ],
      "example": "the launch was postponed again as planned.",
      "id": 64
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The proposal falls short of",
      "answer": "The proposal falls short of addressing the core issue as planned.",
      "accept": [
        "addressing the core issue as planned",
        "The proposal falls short of addressing the core issue as planned.",
        "The proposal falls short of addressing the core issue as planned."
      ],
      "example": "addressing the core issue as planned.",
      "id": 65
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "At no point did he",
      "answer": "At no point did he admit that he was wrong as planned.",
      "accept": [
        "admit that he was wrong as planned",
        "At no point did he admit that he was wrong as planned.",
        "At no point did he admit that he was wrong as planned."
      ],
      "example": "admit that he was wrong as planned.",
      "id": 66
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The more nuanced the analysis becomes,",
      "answer": "The more nuanced the analysis becomes, the harder it is to summarise as planned.",
      "accept": [
        "the harder it is to summarise as planned",
        "The more nuanced the analysis becomes, the harder it is to summarise as planned.",
        "The more nuanced the analysis becomes, the harder it is to summarise as planned."
      ],
      "example": "the harder it is to summarise as planned.",
      "id": 67
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She took issue with",
      "answer": "She took issue with the way the results were presented as planned.",
      "accept": [
        "the way the results were presented as planned",
        "She took issue with the way the results were presented as planned.",
        "She took issue with the way the results were presented as planned."
      ],
      "example": "the way the results were presented as planned.",
      "id": 68
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In the event of a system failure,",
      "answer": "In the event of a system failure, backup procedures will apply as planned.",
      "accept": [
        "backup procedures will apply as planned",
        "In the event of a system failure, backup procedures will apply as planned.",
        "In the event of a system failure, backup procedures will apply as planned."
      ],
      "example": "backup procedures will apply as planned.",
      "id": 69
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He remains sceptical as to whether",
      "answer": "He remains sceptical as to whether the reform will deliver results as planned.",
      "accept": [
        "the reform will deliver results as planned",
        "He remains sceptical as to whether the reform will deliver results as planned.",
        "He remains sceptical as to whether the reform will deliver results as planned."
      ],
      "example": "the reform will deliver results as planned.",
      "id": 70
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The findings cast doubt on",
      "answer": "The findings cast doubt on the previous methodology as planned.",
      "accept": [
        "the previous methodology as planned",
        "The findings cast doubt on the previous methodology as planned.",
        "The findings cast doubt on the previous methodology as planned."
      ],
      "example": "the previous methodology as planned.",
      "id": 71
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is imperative that we",
      "answer": "It is imperative that we act before the deadline as planned.",
      "accept": [
        "act before the deadline as planned",
        "It is imperative that we act before the deadline as planned.",
        "It is imperative that we act before the deadline as planned."
      ],
      "example": "act before the deadline as planned.",
      "id": 72
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Not until the audit was complete did",
      "answer": "Not until the audit was complete did the full extent of the losses emerge as planned.",
      "accept": [
        "the full extent of the losses emerge as planned",
        "Not until the audit was complete did the full extent of the losses emerge as planned.",
        "Not until the audit was complete did the full extent of the losses emerge as planned."
      ],
      "example": "the full extent of the losses emerge as planned.",
      "id": 73
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She attributed the delay to",
      "answer": "She attributed the delay to unforeseen logistical problems as planned.",
      "accept": [
        "unforeseen logistical problems as planned",
        "She attributed the delay to unforeseen logistical problems as planned.",
        "She attributed the delay to unforeseen logistical problems as planned."
      ],
      "example": "unforeseen logistical problems as planned.",
      "id": 74
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The framework seeks to reconcile",
      "answer": "The framework seeks to reconcile innovation with regulation as planned.",
      "accept": [
        "innovation with regulation as planned",
        "The framework seeks to reconcile innovation with regulation as planned.",
        "The framework seeks to reconcile innovation with regulation as planned."
      ],
      "example": "innovation with regulation as planned.",
      "id": 75
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "There is growing consensus that",
      "answer": "There is growing consensus that remote work is here to stay as planned.",
      "accept": [
        "remote work is here to stay as planned",
        "There is growing consensus that remote work is here to stay as planned.",
        "There is growing consensus that remote work is here to stay as planned."
      ],
      "example": "remote work is here to stay as planned.",
      "id": 76
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He challenged the assumption that",
      "answer": "He challenged the assumption that growth alone ensures stability as planned.",
      "accept": [
        "growth alone ensures stability as planned",
        "He challenged the assumption that growth alone ensures stability as planned.",
        "He challenged the assumption that growth alone ensures stability as planned."
      ],
      "example": "growth alone ensures stability as planned.",
      "id": 77
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In retrospect,",
      "answer": "In retrospect, the decision appears short-sighted as planned.",
      "accept": [
        "the decision appears short-sighted as planned",
        "In retrospect, the decision appears short-sighted as planned.",
        "In retrospect, the decision appears short-sighted as planned."
      ],
      "example": "the decision appears short-sighted as planned.",
      "id": 78
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The report highlights the need for",
      "answer": "The report highlights the need for more rigorous oversight as planned.",
      "accept": [
        "more rigorous oversight as planned",
        "The report highlights the need for more rigorous oversight as planned.",
        "The report highlights the need for more rigorous oversight as planned."
      ],
      "example": "more rigorous oversight as planned.",
      "id": 79
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Be that as it may,",
      "answer": "Be that as it may, we still need a practical solution as planned.",
      "accept": [
        "we still need a practical solution as planned",
        "Be that as it may, we still need a practical solution as planned.",
        "Be that as it may, we still need a practical solution as planned."
      ],
      "example": "we still need a practical solution as planned.",
      "id": 80
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She was instrumental in",
      "answer": "She was instrumental in securing the partnership as planned.",
      "accept": [
        "securing the partnership as planned",
        "She was instrumental in securing the partnership as planned.",
        "She was instrumental in securing the partnership as planned."
      ],
      "example": "securing the partnership as planned.",
      "id": 81
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The argument hinges on",
      "answer": "The argument hinges on the reliability of the data as planned.",
      "accept": [
        "the reliability of the data as planned",
        "The argument hinges on the reliability of the data as planned.",
        "The argument hinges on the reliability of the data as planned."
      ],
      "example": "the reliability of the data as planned.",
      "id": 82
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It would be premature to",
      "answer": "It would be premature to draw firm conclusions yet as planned.",
      "accept": [
        "draw firm conclusions yet as planned",
        "It would be premature to draw firm conclusions yet as planned.",
        "It would be premature to draw firm conclusions yet as planned."
      ],
      "example": "draw firm conclusions yet as planned.",
      "id": 83
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He dismissed the criticism as",
      "answer": "He dismissed the criticism as politically motivated as planned.",
      "accept": [
        "politically motivated as planned",
        "He dismissed the criticism as politically motivated as planned.",
        "He dismissed the criticism as politically motivated as planned."
      ],
      "example": "politically motivated as planned.",
      "id": 84
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The initiative is geared towards",
      "answer": "The initiative is geared towards reducing inequality as planned.",
      "accept": [
        "reducing inequality as planned",
        "The initiative is geared towards reducing inequality as planned.",
        "The initiative is geared towards reducing inequality as planned."
      ],
      "example": "reducing inequality as planned.",
      "id": 85
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Only by collaborating closely can we",
      "answer": "Only by collaborating closely can we achieve meaningful change as planned.",
      "accept": [
        "achieve meaningful change as planned",
        "Only by collaborating closely can we achieve meaningful change as planned.",
        "Only by collaborating closely can we achieve meaningful change as planned."
      ],
      "example": "achieve meaningful change as planned.",
      "id": 86
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She raised concerns regarding",
      "answer": "She raised concerns regarding the ethical implications as planned.",
      "accept": [
        "the ethical implications as planned",
        "She raised concerns regarding the ethical implications as planned.",
        "She raised concerns regarding the ethical implications as planned."
      ],
      "example": "the ethical implications as planned.",
      "id": 87
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The evidence is insufficient to",
      "answer": "The evidence is insufficient to support such a strong claim as planned.",
      "accept": [
        "support such a strong claim as planned",
        "The evidence is insufficient to support such a strong claim as planned.",
        "The evidence is insufficient to support such a strong claim as planned."
      ],
      "example": "support such a strong claim as planned.",
      "id": 88
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Insofar as the budget allows,",
      "answer": "Insofar as the budget allows, we will expand the programme as planned.",
      "accept": [
        "we will expand the programme as planned",
        "Insofar as the budget allows, we will expand the programme as planned.",
        "Insofar as the budget allows, we will expand the programme as planned."
      ],
      "example": "we will expand the programme as planned.",
      "id": 89
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He failed to account for",
      "answer": "He failed to account for seasonal variations in demand as planned.",
      "accept": [
        "seasonal variations in demand as planned",
        "He failed to account for seasonal variations in demand as planned.",
        "He failed to account for seasonal variations in demand as planned."
      ],
      "example": "seasonal variations in demand as planned.",
      "id": 90
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The discussion centred on",
      "answer": "The discussion centred on how to balance risk and reward as planned.",
      "accept": [
        "how to balance risk and reward as planned",
        "The discussion centred on how to balance risk and reward as planned.",
        "The discussion centred on how to balance risk and reward as planned."
      ],
      "example": "how to balance risk and reward as planned.",
      "id": 91
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is conceivable that",
      "answer": "It is conceivable that the policy will be revised soon as planned.",
      "accept": [
        "the policy will be revised soon as planned",
        "It is conceivable that the policy will be revised soon as planned.",
        "It is conceivable that the policy will be revised soon as planned."
      ],
      "example": "the policy will be revised soon as planned.",
      "id": 92
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She underscored the importance of",
      "answer": "She underscored the importance of continuous professional development as planned.",
      "accept": [
        "continuous professional development as planned",
        "She underscored the importance of continuous professional development as planned.",
        "She underscored the importance of continuous professional development as planned."
      ],
      "example": "continuous professional development as planned.",
      "id": 93
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The outcome hinges largely on",
      "answer": "The outcome hinges largely on public engagement as planned.",
      "accept": [
        "public engagement as planned",
        "The outcome hinges largely on public engagement as planned.",
        "The outcome hinges largely on public engagement as planned."
      ],
      "example": "public engagement as planned.",
      "id": 94
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Notwithstanding earlier objections,",
      "answer": "Notwithstanding earlier objections, the bill was approved as planned.",
      "accept": [
        "the bill was approved as planned",
        "Notwithstanding earlier objections, the bill was approved as planned.",
        "Notwithstanding earlier objections, the bill was approved as planned."
      ],
      "example": "the bill was approved as planned.",
      "id": 95
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He ventured to suggest that",
      "answer": "He ventured to suggest that a compromise was still possible as planned.",
      "accept": [
        "a compromise was still possible as planned",
        "He ventured to suggest that a compromise was still possible as planned.",
        "He ventured to suggest that a compromise was still possible as planned."
      ],
      "example": "a compromise was still possible as planned.",
      "id": 96
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The analysis falls into the trap of",
      "answer": "The analysis falls into the trap of oversimplifying the causes as planned.",
      "accept": [
        "oversimplifying the causes as planned",
        "The analysis falls into the trap of oversimplifying the causes as planned.",
        "The analysis falls into the trap of oversimplifying the causes as planned."
      ],
      "example": "oversimplifying the causes as planned.",
      "id": 97
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In practical terms,",
      "answer": "In practical terms, this means higher operating costs as planned.",
      "accept": [
        "this means higher operating costs as planned",
        "In practical terms, this means higher operating costs as planned.",
        "In practical terms, this means higher operating costs as planned."
      ],
      "example": "this means higher operating costs as planned.",
      "id": 98
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She remains ambivalent about",
      "answer": "She remains ambivalent about accepting the promotion as planned.",
      "accept": [
        "accepting the promotion as planned",
        "She remains ambivalent about accepting the promotion as planned.",
        "She remains ambivalent about accepting the promotion as planned."
      ],
      "example": "accepting the promotion as planned.",
      "id": 99
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The strategy is predicated on",
      "answer": "The strategy is predicated on sustained investment as planned.",
      "accept": [
        "sustained investment as planned",
        "The strategy is predicated on sustained investment as planned.",
        "The strategy is predicated on sustained investment as planned."
      ],
      "example": "sustained investment as planned.",
      "id": 100
    }
  ],
  "C2": [
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Quintessentially,",
      "answer": "Quintessentially, the debate revolves around competing notions of fairness.",
      "accept": [
        "the debate revolves around competing notions of fairness",
        "Quintessentially, the debate revolves around competing notions of fairness.",
        "Quintessentially, the debate revolves around competing notions of fairness."
      ],
      "example": "the debate revolves around competing notions of fairness.",
      "id": 1
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "To the extent that evidence permits,",
      "answer": "To the extent that evidence permits, we may infer a causal link.",
      "accept": [
        "we may infer a causal link",
        "To the extent that evidence permits, we may infer a causal link.",
        "To the extent that evidence permits, we may infer a causal link."
      ],
      "example": "we may infer a causal link.",
      "id": 2
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It would be disingenuous to claim that",
      "answer": "It would be disingenuous to claim that the reform has been an unqualified success.",
      "accept": [
        "the reform has been an unqualified success",
        "It would be disingenuous to claim that the reform has been an unqualified success.",
        "It would be disingenuous to claim that the reform has been an unqualified success."
      ],
      "example": "the reform has been an unqualified success.",
      "id": 3
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The paradox lies in the fact that",
      "answer": "The paradox lies in the fact that greater choice can reduce satisfaction.",
      "accept": [
        "greater choice can reduce satisfaction",
        "The paradox lies in the fact that greater choice can reduce satisfaction.",
        "The paradox lies in the fact that greater choice can reduce satisfaction."
      ],
      "example": "greater choice can reduce satisfaction.",
      "id": 4
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "One cannot but admire",
      "answer": "One cannot but admire the elegance of the theoretical model.",
      "accept": [
        "the elegance of the theoretical model",
        "One cannot but admire the elegance of the theoretical model.",
        "One cannot but admire the elegance of the theoretical model."
      ],
      "example": "the elegance of the theoretical model.",
      "id": 5
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Inasmuch as the law is ambiguous,",
      "answer": "Inasmuch as the law is ambiguous, interpretation becomes contested.",
      "accept": [
        "interpretation becomes contested",
        "Inasmuch as the law is ambiguous, interpretation becomes contested.",
        "Inasmuch as the law is ambiguous, interpretation becomes contested."
      ],
      "example": "interpretation becomes contested.",
      "id": 6
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The critique cuts to the heart of",
      "answer": "The critique cuts to the heart of the institution's legitimacy.",
      "accept": [
        "the institution's legitimacy",
        "The critique cuts to the heart of the institution's legitimacy.",
        "The critique cuts to the heart of the institution's legitimacy."
      ],
      "example": "the institution's legitimacy.",
      "id": 7
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is a moot point whether",
      "answer": "It is a moot point whether technology alone can resolve inequality.",
      "accept": [
        "technology alone can resolve inequality",
        "It is a moot point whether technology alone can resolve inequality.",
        "It is a moot point whether technology alone can resolve inequality."
      ],
      "example": "technology alone can resolve inequality.",
      "id": 8
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "His reasoning, though ingenious,",
      "answer": "His reasoning, though ingenious, rests on a fragile premise.",
      "accept": [
        "rests on a fragile premise",
        "His reasoning, though ingenious, rests on a fragile premise.",
        "His reasoning, though ingenious, rests on a fragile premise."
      ],
      "example": "rests on a fragile premise.",
      "id": 9
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The discourse has been hijacked by",
      "answer": "The discourse has been hijacked by oversimplified narratives.",
      "accept": [
        "oversimplified narratives",
        "The discourse has been hijacked by oversimplified narratives.",
        "The discourse has been hijacked by oversimplified narratives."
      ],
      "example": "oversimplified narratives.",
      "id": 10
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "To put it more precisely,",
      "answer": "To put it more precisely, the issue is one of allocation, not scarcity.",
      "accept": [
        "the issue is one of allocation, not scarcity",
        "To put it more precisely, the issue is one of allocation, not scarcity.",
        "To put it more precisely, the issue is one of allocation, not scarcity."
      ],
      "example": "the issue is one of allocation, not scarcity.",
      "id": 11
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She repudiated the suggestion that",
      "answer": "She repudiated the suggestion that compromise equals weakness.",
      "accept": [
        "compromise equals weakness",
        "She repudiated the suggestion that compromise equals weakness.",
        "She repudiated the suggestion that compromise equals weakness."
      ],
      "example": "compromise equals weakness.",
      "id": 12
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The implications are far-reaching,",
      "answer": "The implications are far-reaching, touching both ethics and governance.",
      "accept": [
        "touching both ethics and governance",
        "The implications are far-reaching, touching both ethics and governance.",
        "The implications are far-reaching, touching both ethics and governance."
      ],
      "example": "touching both ethics and governance.",
      "id": 13
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It would be remiss of us not to",
      "answer": "It would be remiss of us not to acknowledge the dissenting voices.",
      "accept": [
        "acknowledge the dissenting voices",
        "It would be remiss of us not to acknowledge the dissenting voices.",
        "It would be remiss of us not to acknowledge the dissenting voices."
      ],
      "example": "acknowledge the dissenting voices.",
      "id": 14
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The thesis is underpinned by",
      "answer": "The thesis is underpinned by a meticulous empirical design.",
      "accept": [
        "a meticulous empirical design",
        "The thesis is underpinned by a meticulous empirical design.",
        "The thesis is underpinned by a meticulous empirical design."
      ],
      "example": "a meticulous empirical design.",
      "id": 15
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In the final analysis,",
      "answer": "In the final analysis, agency remains with human decision-makers.",
      "accept": [
        "agency remains with human decision-makers",
        "In the final analysis, agency remains with human decision-makers.",
        "In the final analysis, agency remains with human decision-makers."
      ],
      "example": "agency remains with human decision-makers.",
      "id": 16
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He took umbrage at",
      "answer": "He took umbrage at the implication of negligence.",
      "accept": [
        "the implication of negligence",
        "He took umbrage at the implication of negligence.",
        "He took umbrage at the implication of negligence."
      ],
      "example": "the implication of negligence.",
      "id": 17
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The argument is not without merit, yet",
      "answer": "The argument is not without merit, yet it overlooks structural constraints.",
      "accept": [
        "it overlooks structural constraints",
        "The argument is not without merit, yet it overlooks structural constraints.",
        "The argument is not without merit, yet it overlooks structural constraints."
      ],
      "example": "it overlooks structural constraints.",
      "id": 18
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Arguably the most contentious claim is that",
      "answer": "Arguably the most contentious claim is that neutrality is ever fully attainable.",
      "accept": [
        "neutrality is ever fully attainable",
        "Arguably the most contentious claim is that neutrality is ever fully attainable.",
        "Arguably the most contentious claim is that neutrality is ever fully attainable."
      ],
      "example": "neutrality is ever fully attainable.",
      "id": 19
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She navigated the impasse by",
      "answer": "She navigated the impasse by reframing the stakeholders' interests.",
      "accept": [
        "reframing the stakeholders' interests",
        "She navigated the impasse by reframing the stakeholders' interests.",
        "She navigated the impasse by reframing the stakeholders' interests."
      ],
      "example": "reframing the stakeholders' interests.",
      "id": 20
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The literature remains inconclusive as to",
      "answer": "The literature remains inconclusive as to long-term behavioural effects.",
      "accept": [
        "long-term behavioural effects",
        "The literature remains inconclusive as to long-term behavioural effects.",
        "The literature remains inconclusive as to long-term behavioural effects."
      ],
      "example": "long-term behavioural effects.",
      "id": 21
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It borders on the absurd to insist that",
      "answer": "It borders on the absurd to insist that markets self-correct in all cases.",
      "accept": [
        "markets self-correct in all cases",
        "It borders on the absurd to insist that markets self-correct in all cases.",
        "It borders on the absurd to insist that markets self-correct in all cases."
      ],
      "example": "markets self-correct in all cases.",
      "id": 22
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "His prose is marked by",
      "answer": "His prose is marked by a rare combination of clarity and depth.",
      "accept": [
        "a rare combination of clarity and depth",
        "His prose is marked by a rare combination of clarity and depth.",
        "His prose is marked by a rare combination of clarity and depth."
      ],
      "example": "a rare combination of clarity and depth.",
      "id": 23
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The policy, ostensibly neutral,",
      "answer": "The policy, ostensibly neutral, disproportionately affects vulnerable groups.",
      "accept": [
        "disproportionately affects vulnerable groups",
        "The policy, ostensibly neutral, disproportionately affects vulnerable groups.",
        "The policy, ostensibly neutral, disproportionately affects vulnerable groups."
      ],
      "example": "disproportionately affects vulnerable groups.",
      "id": 24
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "One is left wondering whether",
      "answer": "One is left wondering whether the promised transparency will materialise.",
      "accept": [
        "the promised transparency will materialise",
        "One is left wondering whether the promised transparency will materialise.",
        "One is left wondering whether the promised transparency will materialise."
      ],
      "example": "the promised transparency will materialise.",
      "id": 25
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She dismantled the counterargument with",
      "answer": "She dismantled the counterargument with clinical precision.",
      "accept": [
        "clinical precision",
        "She dismantled the counterargument with clinical precision.",
        "She dismantled the counterargument with clinical precision."
      ],
      "example": "clinical precision.",
      "id": 26
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The episode serves as a cautionary tale about",
      "answer": "The episode serves as a cautionary tale about unchecked algorithmic authority.",
      "accept": [
        "unchecked algorithmic authority",
        "The episode serves as a cautionary tale about unchecked algorithmic authority.",
        "The episode serves as a cautionary tale about unchecked algorithmic authority."
      ],
      "example": "unchecked algorithmic authority.",
      "id": 27
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In contradistinction to earlier models,",
      "answer": "In contradistinction to earlier models, this approach foregrounds context.",
      "accept": [
        "this approach foregrounds context",
        "In contradistinction to earlier models, this approach foregrounds context.",
        "In contradistinction to earlier models, this approach foregrounds context."
      ],
      "example": "this approach foregrounds context.",
      "id": 28
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He equivocated when pressed on",
      "answer": "He equivocated when pressed on the question of accountability.",
      "accept": [
        "the question of accountability",
        "He equivocated when pressed on the question of accountability.",
        "He equivocated when pressed on the question of accountability."
      ],
      "example": "the question of accountability.",
      "id": 29
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The findings, provisional though they are,",
      "answer": "The findings, provisional though they are, warrant further scrutiny.",
      "accept": [
        "warrant further scrutiny",
        "The findings, provisional though they are, warrant further scrutiny.",
        "The findings, provisional though they are, warrant further scrutiny."
      ],
      "example": "warrant further scrutiny.",
      "id": 30
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is scarcely surprising that",
      "answer": "It is scarcely surprising that trust has eroded over time.",
      "accept": [
        "trust has eroded over time",
        "It is scarcely surprising that trust has eroded over time.",
        "It is scarcely surprising that trust has eroded over time."
      ],
      "example": "trust has eroded over time.",
      "id": 31
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She articulated a vision that",
      "answer": "She articulated a vision that transcends partisan divides.",
      "accept": [
        "transcends partisan divides",
        "She articulated a vision that transcends partisan divides.",
        "She articulated a vision that transcends partisan divides."
      ],
      "example": "transcends partisan divides.",
      "id": 32
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The metaphor, while evocative,",
      "answer": "The metaphor, while evocative, risks obscuring the mechanics.",
      "accept": [
        "risks obscuring the mechanics",
        "The metaphor, while evocative, risks obscuring the mechanics.",
        "The metaphor, while evocative, risks obscuring the mechanics."
      ],
      "example": "risks obscuring the mechanics.",
      "id": 33
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "To all intents and purposes,",
      "answer": "To all intents and purposes, the negotiation had already collapsed.",
      "accept": [
        "the negotiation had already collapsed",
        "To all intents and purposes, the negotiation had already collapsed.",
        "To all intents and purposes, the negotiation had already collapsed."
      ],
      "example": "the negotiation had already collapsed.",
      "id": 34
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He refused to be drawn on",
      "answer": "He refused to be drawn on speculation about future mergers.",
      "accept": [
        "speculation about future mergers",
        "He refused to be drawn on speculation about future mergers.",
        "He refused to be drawn on speculation about future mergers."
      ],
      "example": "speculation about future mergers.",
      "id": 35
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The framework privileges efficiency over",
      "answer": "The framework privileges efficiency over procedural fairness.",
      "accept": [
        "procedural fairness",
        "The framework privileges efficiency over procedural fairness.",
        "The framework privileges efficiency over procedural fairness."
      ],
      "example": "procedural fairness.",
      "id": 36
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "There is a palpable tension between",
      "answer": "There is a palpable tension between innovation and precaution.",
      "accept": [
        "innovation and precaution",
        "There is a palpable tension between innovation and precaution.",
        "There is a palpable tension between innovation and precaution."
      ],
      "example": "innovation and precaution.",
      "id": 37
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She remained unfazed by",
      "answer": "She remained unfazed by the intensity of public scrutiny.",
      "accept": [
        "the intensity of public scrutiny",
        "She remained unfazed by the intensity of public scrutiny.",
        "She remained unfazed by the intensity of public scrutiny."
      ],
      "example": "the intensity of public scrutiny.",
      "id": 38
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The claim does not withstand",
      "answer": "The claim does not withstand even modest empirical testing.",
      "accept": [
        "even modest empirical testing",
        "The claim does not withstand even modest empirical testing.",
        "The claim does not withstand even modest empirical testing."
      ],
      "example": "even modest empirical testing.",
      "id": 39
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In a nutshell,",
      "answer": "In a nutshell, incentives shape behaviour more than rhetoric.",
      "accept": [
        "incentives shape behaviour more than rhetoric",
        "In a nutshell, incentives shape behaviour more than rhetoric.",
        "In a nutshell, incentives shape behaviour more than rhetoric."
      ],
      "example": "incentives shape behaviour more than rhetoric.",
      "id": 40
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He cast aspersions on",
      "answer": "He cast aspersions on the integrity of the review process.",
      "accept": [
        "the integrity of the review process",
        "He cast aspersions on the integrity of the review process.",
        "He cast aspersions on the integrity of the review process."
      ],
      "example": "the integrity of the review process.",
      "id": 41
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The elegance of the proof belies",
      "answer": "The elegance of the proof belies the complexity of the underlying assumptions.",
      "accept": [
        "the complexity of the underlying assumptions",
        "The elegance of the proof belies the complexity of the underlying assumptions.",
        "The elegance of the proof belies the complexity of the underlying assumptions."
      ],
      "example": "the complexity of the underlying assumptions.",
      "id": 42
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She hedged her conclusions carefully,",
      "answer": "She hedged her conclusions carefully, aware of the political stakes.",
      "accept": [
        "aware of the political stakes",
        "She hedged her conclusions carefully, aware of the political stakes.",
        "She hedged her conclusions carefully, aware of the political stakes."
      ],
      "example": "aware of the political stakes.",
      "id": 43
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is incumbent upon policymakers to",
      "answer": "It is incumbent upon policymakers to anticipate unintended consequences.",
      "accept": [
        "anticipate unintended consequences",
        "It is incumbent upon policymakers to anticipate unintended consequences.",
        "It is incumbent upon policymakers to anticipate unintended consequences."
      ],
      "example": "anticipate unintended consequences.",
      "id": 44
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The narrative arc of the novel mirrors",
      "answer": "The narrative arc of the novel mirrors the protagonist's moral disintegration.",
      "accept": [
        "the protagonist's moral disintegration",
        "The narrative arc of the novel mirrors the protagonist's moral disintegration.",
        "The narrative arc of the novel mirrors the protagonist's moral disintegration."
      ],
      "example": "the protagonist's moral disintegration.",
      "id": 45
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He was at pains to stress that",
      "answer": "He was at pains to stress that correlation is not causation.",
      "accept": [
        "correlation is not causation",
        "He was at pains to stress that correlation is not causation.",
        "He was at pains to stress that correlation is not causation."
      ],
      "example": "correlation is not causation.",
      "id": 46
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The orthodoxy is being challenged by",
      "answer": "The orthodoxy is being challenged by a new generation of scholars.",
      "accept": [
        "a new generation of scholars",
        "The orthodoxy is being challenged by a new generation of scholars.",
        "The orthodoxy is being challenged by a new generation of scholars."
      ],
      "example": "a new generation of scholars.",
      "id": 47
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She struck a delicate balance between",
      "answer": "She struck a delicate balance between candour and diplomacy.",
      "accept": [
        "candour and diplomacy",
        "She struck a delicate balance between candour and diplomacy.",
        "She struck a delicate balance between candour and diplomacy."
      ],
      "example": "candour and diplomacy.",
      "id": 48
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Ultimately, the question reduces to",
      "answer": "Ultimately, the question reduces to what kind of society we wish to inhabit.",
      "accept": [
        "what kind of society we wish to inhabit",
        "Ultimately, the question reduces to what kind of society we wish to inhabit.",
        "Ultimately, the question reduces to what kind of society we wish to inhabit."
      ],
      "example": "what kind of society we wish to inhabit.",
      "id": 49
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The symposium crystallised a shift towards",
      "answer": "The symposium crystallised a shift towards interdisciplinary collaboration.",
      "accept": [
        "interdisciplinary collaboration",
        "The symposium crystallised a shift towards interdisciplinary collaboration.",
        "The symposium crystallised a shift towards interdisciplinary collaboration."
      ],
      "example": "interdisciplinary collaboration.",
      "id": 50
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Quintessentially,",
      "answer": "Quintessentially, the debate revolves around competing notions of fairness as planned.",
      "accept": [
        "the debate revolves around competing notions of fairness as planned",
        "Quintessentially, the debate revolves around competing notions of fairness as planned.",
        "Quintessentially, the debate revolves around competing notions of fairness as planned."
      ],
      "example": "the debate revolves around competing notions of fairness as planned.",
      "id": 51
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "To the extent that evidence permits,",
      "answer": "To the extent that evidence permits, we may infer a causal link as planned.",
      "accept": [
        "we may infer a causal link as planned",
        "To the extent that evidence permits, we may infer a causal link as planned.",
        "To the extent that evidence permits, we may infer a causal link as planned."
      ],
      "example": "we may infer a causal link as planned.",
      "id": 52
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It would be disingenuous to claim that",
      "answer": "It would be disingenuous to claim that the reform has been an unqualified success as planned.",
      "accept": [
        "the reform has been an unqualified success as planned",
        "It would be disingenuous to claim that the reform has been an unqualified success as planned.",
        "It would be disingenuous to claim that the reform has been an unqualified success as planned."
      ],
      "example": "the reform has been an unqualified success as planned.",
      "id": 53
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The paradox lies in the fact that",
      "answer": "The paradox lies in the fact that greater choice can reduce satisfaction as planned.",
      "accept": [
        "greater choice can reduce satisfaction as planned",
        "The paradox lies in the fact that greater choice can reduce satisfaction as planned.",
        "The paradox lies in the fact that greater choice can reduce satisfaction as planned."
      ],
      "example": "greater choice can reduce satisfaction as planned.",
      "id": 54
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "One cannot but admire",
      "answer": "One cannot but admire the elegance of the theoretical model as planned.",
      "accept": [
        "the elegance of the theoretical model as planned",
        "One cannot but admire the elegance of the theoretical model as planned.",
        "One cannot but admire the elegance of the theoretical model as planned."
      ],
      "example": "the elegance of the theoretical model as planned.",
      "id": 55
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Inasmuch as the law is ambiguous,",
      "answer": "Inasmuch as the law is ambiguous, interpretation becomes contested as planned.",
      "accept": [
        "interpretation becomes contested as planned",
        "Inasmuch as the law is ambiguous, interpretation becomes contested as planned.",
        "Inasmuch as the law is ambiguous, interpretation becomes contested as planned."
      ],
      "example": "interpretation becomes contested as planned.",
      "id": 56
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The critique cuts to the heart of",
      "answer": "The critique cuts to the heart of the institution's legitimacy as planned.",
      "accept": [
        "the institution's legitimacy as planned",
        "The critique cuts to the heart of the institution's legitimacy as planned.",
        "The critique cuts to the heart of the institution's legitimacy as planned."
      ],
      "example": "the institution's legitimacy as planned.",
      "id": 57
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is a moot point whether",
      "answer": "It is a moot point whether technology alone can resolve inequality as planned.",
      "accept": [
        "technology alone can resolve inequality as planned",
        "It is a moot point whether technology alone can resolve inequality as planned.",
        "It is a moot point whether technology alone can resolve inequality as planned."
      ],
      "example": "technology alone can resolve inequality as planned.",
      "id": 58
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "His reasoning, though ingenious,",
      "answer": "His reasoning, though ingenious, rests on a fragile premise as planned.",
      "accept": [
        "rests on a fragile premise as planned",
        "His reasoning, though ingenious, rests on a fragile premise as planned.",
        "His reasoning, though ingenious, rests on a fragile premise as planned."
      ],
      "example": "rests on a fragile premise as planned.",
      "id": 59
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The discourse has been hijacked by",
      "answer": "The discourse has been hijacked by oversimplified narratives as planned.",
      "accept": [
        "oversimplified narratives as planned",
        "The discourse has been hijacked by oversimplified narratives as planned.",
        "The discourse has been hijacked by oversimplified narratives as planned."
      ],
      "example": "oversimplified narratives as planned.",
      "id": 60
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "To put it more precisely,",
      "answer": "To put it more precisely, the issue is one of allocation, not scarcity as planned.",
      "accept": [
        "the issue is one of allocation, not scarcity as planned",
        "To put it more precisely, the issue is one of allocation, not scarcity as planned.",
        "To put it more precisely, the issue is one of allocation, not scarcity as planned."
      ],
      "example": "the issue is one of allocation, not scarcity as planned.",
      "id": 61
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She repudiated the suggestion that",
      "answer": "She repudiated the suggestion that compromise equals weakness as planned.",
      "accept": [
        "compromise equals weakness as planned",
        "She repudiated the suggestion that compromise equals weakness as planned.",
        "She repudiated the suggestion that compromise equals weakness as planned."
      ],
      "example": "compromise equals weakness as planned.",
      "id": 62
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The implications are far-reaching,",
      "answer": "The implications are far-reaching, touching both ethics and governance as planned.",
      "accept": [
        "touching both ethics and governance as planned",
        "The implications are far-reaching, touching both ethics and governance as planned.",
        "The implications are far-reaching, touching both ethics and governance as planned."
      ],
      "example": "touching both ethics and governance as planned.",
      "id": 63
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It would be remiss of us not to",
      "answer": "It would be remiss of us not to acknowledge the dissenting voices as planned.",
      "accept": [
        "acknowledge the dissenting voices as planned",
        "It would be remiss of us not to acknowledge the dissenting voices as planned.",
        "It would be remiss of us not to acknowledge the dissenting voices as planned."
      ],
      "example": "acknowledge the dissenting voices as planned.",
      "id": 64
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The thesis is underpinned by",
      "answer": "The thesis is underpinned by a meticulous empirical design as planned.",
      "accept": [
        "a meticulous empirical design as planned",
        "The thesis is underpinned by a meticulous empirical design as planned.",
        "The thesis is underpinned by a meticulous empirical design as planned."
      ],
      "example": "a meticulous empirical design as planned.",
      "id": 65
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In the final analysis,",
      "answer": "In the final analysis, agency remains with human decision-makers as planned.",
      "accept": [
        "agency remains with human decision-makers as planned",
        "In the final analysis, agency remains with human decision-makers as planned.",
        "In the final analysis, agency remains with human decision-makers as planned."
      ],
      "example": "agency remains with human decision-makers as planned.",
      "id": 66
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He took umbrage at",
      "answer": "He took umbrage at the implication of negligence as planned.",
      "accept": [
        "the implication of negligence as planned",
        "He took umbrage at the implication of negligence as planned.",
        "He took umbrage at the implication of negligence as planned."
      ],
      "example": "the implication of negligence as planned.",
      "id": 67
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The argument is not without merit, yet",
      "answer": "The argument is not without merit, yet it overlooks structural constraints as planned.",
      "accept": [
        "it overlooks structural constraints as planned",
        "The argument is not without merit, yet it overlooks structural constraints as planned.",
        "The argument is not without merit, yet it overlooks structural constraints as planned."
      ],
      "example": "it overlooks structural constraints as planned.",
      "id": 68
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Arguably the most contentious claim is that",
      "answer": "Arguably the most contentious claim is that neutrality is ever fully attainable as planned.",
      "accept": [
        "neutrality is ever fully attainable as planned",
        "Arguably the most contentious claim is that neutrality is ever fully attainable as planned.",
        "Arguably the most contentious claim is that neutrality is ever fully attainable as planned."
      ],
      "example": "neutrality is ever fully attainable as planned.",
      "id": 69
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She navigated the impasse by",
      "answer": "She navigated the impasse by reframing the stakeholders' interests as planned.",
      "accept": [
        "reframing the stakeholders' interests as planned",
        "She navigated the impasse by reframing the stakeholders' interests as planned.",
        "She navigated the impasse by reframing the stakeholders' interests as planned."
      ],
      "example": "reframing the stakeholders' interests as planned.",
      "id": 70
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The literature remains inconclusive as to",
      "answer": "The literature remains inconclusive as to long-term behavioural effects as planned.",
      "accept": [
        "long-term behavioural effects as planned",
        "The literature remains inconclusive as to long-term behavioural effects as planned.",
        "The literature remains inconclusive as to long-term behavioural effects as planned."
      ],
      "example": "long-term behavioural effects as planned.",
      "id": 71
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It borders on the absurd to insist that",
      "answer": "It borders on the absurd to insist that markets self-correct in all cases as planned.",
      "accept": [
        "markets self-correct in all cases as planned",
        "It borders on the absurd to insist that markets self-correct in all cases as planned.",
        "It borders on the absurd to insist that markets self-correct in all cases as planned."
      ],
      "example": "markets self-correct in all cases as planned.",
      "id": 72
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "His prose is marked by",
      "answer": "His prose is marked by a rare combination of clarity and depth as planned.",
      "accept": [
        "a rare combination of clarity and depth as planned",
        "His prose is marked by a rare combination of clarity and depth as planned.",
        "His prose is marked by a rare combination of clarity and depth as planned."
      ],
      "example": "a rare combination of clarity and depth as planned.",
      "id": 73
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The policy, ostensibly neutral,",
      "answer": "The policy, ostensibly neutral, disproportionately affects vulnerable groups as planned.",
      "accept": [
        "disproportionately affects vulnerable groups as planned",
        "The policy, ostensibly neutral, disproportionately affects vulnerable groups as planned.",
        "The policy, ostensibly neutral, disproportionately affects vulnerable groups as planned."
      ],
      "example": "disproportionately affects vulnerable groups as planned.",
      "id": 74
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "One is left wondering whether",
      "answer": "One is left wondering whether the promised transparency will materialise as planned.",
      "accept": [
        "the promised transparency will materialise as planned",
        "One is left wondering whether the promised transparency will materialise as planned.",
        "One is left wondering whether the promised transparency will materialise as planned."
      ],
      "example": "the promised transparency will materialise as planned.",
      "id": 75
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She dismantled the counterargument with",
      "answer": "She dismantled the counterargument with clinical precision as planned.",
      "accept": [
        "clinical precision as planned",
        "She dismantled the counterargument with clinical precision as planned.",
        "She dismantled the counterargument with clinical precision as planned."
      ],
      "example": "clinical precision as planned.",
      "id": 76
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The episode serves as a cautionary tale about",
      "answer": "The episode serves as a cautionary tale about unchecked algorithmic authority as planned.",
      "accept": [
        "unchecked algorithmic authority as planned",
        "The episode serves as a cautionary tale about unchecked algorithmic authority as planned.",
        "The episode serves as a cautionary tale about unchecked algorithmic authority as planned."
      ],
      "example": "unchecked algorithmic authority as planned.",
      "id": 77
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In contradistinction to earlier models,",
      "answer": "In contradistinction to earlier models, this approach foregrounds context as planned.",
      "accept": [
        "this approach foregrounds context as planned",
        "In contradistinction to earlier models, this approach foregrounds context as planned.",
        "In contradistinction to earlier models, this approach foregrounds context as planned."
      ],
      "example": "this approach foregrounds context as planned.",
      "id": 78
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He equivocated when pressed on",
      "answer": "He equivocated when pressed on the question of accountability as planned.",
      "accept": [
        "the question of accountability as planned",
        "He equivocated when pressed on the question of accountability as planned.",
        "He equivocated when pressed on the question of accountability as planned."
      ],
      "example": "the question of accountability as planned.",
      "id": 79
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The findings, provisional though they are,",
      "answer": "The findings, provisional though they are, warrant further scrutiny as planned.",
      "accept": [
        "warrant further scrutiny as planned",
        "The findings, provisional though they are, warrant further scrutiny as planned.",
        "The findings, provisional though they are, warrant further scrutiny as planned."
      ],
      "example": "warrant further scrutiny as planned.",
      "id": 80
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is scarcely surprising that",
      "answer": "It is scarcely surprising that trust has eroded over time as planned.",
      "accept": [
        "trust has eroded over time as planned",
        "It is scarcely surprising that trust has eroded over time as planned.",
        "It is scarcely surprising that trust has eroded over time as planned."
      ],
      "example": "trust has eroded over time as planned.",
      "id": 81
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She articulated a vision that",
      "answer": "She articulated a vision that transcends partisan divides as planned.",
      "accept": [
        "transcends partisan divides as planned",
        "She articulated a vision that transcends partisan divides as planned.",
        "She articulated a vision that transcends partisan divides as planned."
      ],
      "example": "transcends partisan divides as planned.",
      "id": 82
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The metaphor, while evocative,",
      "answer": "The metaphor, while evocative, risks obscuring the mechanics as planned.",
      "accept": [
        "risks obscuring the mechanics as planned",
        "The metaphor, while evocative, risks obscuring the mechanics as planned.",
        "The metaphor, while evocative, risks obscuring the mechanics as planned."
      ],
      "example": "risks obscuring the mechanics as planned.",
      "id": 83
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "To all intents and purposes,",
      "answer": "To all intents and purposes, the negotiation had already collapsed as planned.",
      "accept": [
        "the negotiation had already collapsed as planned",
        "To all intents and purposes, the negotiation had already collapsed as planned.",
        "To all intents and purposes, the negotiation had already collapsed as planned."
      ],
      "example": "the negotiation had already collapsed as planned.",
      "id": 84
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He refused to be drawn on",
      "answer": "He refused to be drawn on speculation about future mergers as planned.",
      "accept": [
        "speculation about future mergers as planned",
        "He refused to be drawn on speculation about future mergers as planned.",
        "He refused to be drawn on speculation about future mergers as planned."
      ],
      "example": "speculation about future mergers as planned.",
      "id": 85
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The framework privileges efficiency over",
      "answer": "The framework privileges efficiency over procedural fairness as planned.",
      "accept": [
        "procedural fairness as planned",
        "The framework privileges efficiency over procedural fairness as planned.",
        "The framework privileges efficiency over procedural fairness as planned."
      ],
      "example": "procedural fairness as planned.",
      "id": 86
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "There is a palpable tension between",
      "answer": "There is a palpable tension between innovation and precaution as planned.",
      "accept": [
        "innovation and precaution as planned",
        "There is a palpable tension between innovation and precaution as planned.",
        "There is a palpable tension between innovation and precaution as planned."
      ],
      "example": "innovation and precaution as planned.",
      "id": 87
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She remained unfazed by",
      "answer": "She remained unfazed by the intensity of public scrutiny as planned.",
      "accept": [
        "the intensity of public scrutiny as planned",
        "She remained unfazed by the intensity of public scrutiny as planned.",
        "She remained unfazed by the intensity of public scrutiny as planned."
      ],
      "example": "the intensity of public scrutiny as planned.",
      "id": 88
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The claim does not withstand",
      "answer": "The claim does not withstand even modest empirical testing as planned.",
      "accept": [
        "even modest empirical testing as planned",
        "The claim does not withstand even modest empirical testing as planned.",
        "The claim does not withstand even modest empirical testing as planned."
      ],
      "example": "even modest empirical testing as planned.",
      "id": 89
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "In a nutshell,",
      "answer": "In a nutshell, incentives shape behaviour more than rhetoric as planned.",
      "accept": [
        "incentives shape behaviour more than rhetoric as planned",
        "In a nutshell, incentives shape behaviour more than rhetoric as planned.",
        "In a nutshell, incentives shape behaviour more than rhetoric as planned."
      ],
      "example": "incentives shape behaviour more than rhetoric as planned.",
      "id": 90
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He cast aspersions on",
      "answer": "He cast aspersions on the integrity of the review process as planned.",
      "accept": [
        "the integrity of the review process as planned",
        "He cast aspersions on the integrity of the review process as planned.",
        "He cast aspersions on the integrity of the review process as planned."
      ],
      "example": "the integrity of the review process as planned.",
      "id": 91
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The elegance of the proof belies",
      "answer": "The elegance of the proof belies the complexity of the underlying assumptions as planned.",
      "accept": [
        "the complexity of the underlying assumptions as planned",
        "The elegance of the proof belies the complexity of the underlying assumptions as planned.",
        "The elegance of the proof belies the complexity of the underlying assumptions as planned."
      ],
      "example": "the complexity of the underlying assumptions as planned.",
      "id": 92
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She hedged her conclusions carefully,",
      "answer": "She hedged her conclusions carefully, aware of the political stakes as planned.",
      "accept": [
        "aware of the political stakes as planned",
        "She hedged her conclusions carefully, aware of the political stakes as planned.",
        "She hedged her conclusions carefully, aware of the political stakes as planned."
      ],
      "example": "aware of the political stakes as planned.",
      "id": 93
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "It is incumbent upon policymakers to",
      "answer": "It is incumbent upon policymakers to anticipate unintended consequences as planned.",
      "accept": [
        "anticipate unintended consequences as planned",
        "It is incumbent upon policymakers to anticipate unintended consequences as planned.",
        "It is incumbent upon policymakers to anticipate unintended consequences as planned."
      ],
      "example": "anticipate unintended consequences as planned.",
      "id": 94
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The narrative arc of the novel mirrors",
      "answer": "The narrative arc of the novel mirrors the protagonist's moral disintegration as planned.",
      "accept": [
        "the protagonist's moral disintegration as planned",
        "The narrative arc of the novel mirrors the protagonist's moral disintegration as planned.",
        "The narrative arc of the novel mirrors the protagonist's moral disintegration as planned."
      ],
      "example": "the protagonist's moral disintegration as planned.",
      "id": 95
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "He was at pains to stress that",
      "answer": "He was at pains to stress that correlation is not causation as planned.",
      "accept": [
        "correlation is not causation as planned",
        "He was at pains to stress that correlation is not causation as planned.",
        "He was at pains to stress that correlation is not causation as planned."
      ],
      "example": "correlation is not causation as planned.",
      "id": 96
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The orthodoxy is being challenged by",
      "answer": "The orthodoxy is being challenged by a new generation of scholars as planned.",
      "accept": [
        "a new generation of scholars as planned",
        "The orthodoxy is being challenged by a new generation of scholars as planned.",
        "The orthodoxy is being challenged by a new generation of scholars as planned."
      ],
      "example": "a new generation of scholars as planned.",
      "id": 97
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "She struck a delicate balance between",
      "answer": "She struck a delicate balance between candour and diplomacy as planned.",
      "accept": [
        "candour and diplomacy as planned",
        "She struck a delicate balance between candour and diplomacy as planned.",
        "She struck a delicate balance between candour and diplomacy as planned."
      ],
      "example": "candour and diplomacy as planned.",
      "id": 98
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "Ultimately, the question reduces to",
      "answer": "Ultimately, the question reduces to what kind of society we wish to inhabit as planned.",
      "accept": [
        "what kind of society we wish to inhabit as planned",
        "Ultimately, the question reduces to what kind of society we wish to inhabit as planned.",
        "Ultimately, the question reduces to what kind of society we wish to inhabit as planned."
      ],
      "example": "what kind of society we wish to inhabit as planned.",
      "id": 99
    },
    {
      "subtype": "continue_sentence",
      "instruction_ru": "Продолжи предложение логично:",
      "prompt_en": "The symposium crystallised a shift towards",
      "answer": "The symposium crystallised a shift towards interdisciplinary collaboration as planned.",
      "accept": [
        "interdisciplinary collaboration as planned",
        "The symposium crystallised a shift towards interdisciplinary collaboration as planned.",
        "The symposium crystallised a shift towards interdisciplinary collaboration as planned."
      ],
      "example": "interdisciplinary collaboration as planned.",
      "id": 100
    }
  ]
}"""

EXTRA_BANKS: dict[str, list[dict]] = json.loads(_RAW)

LEVEL_SUBTYPE = {
    "A1": "fix_sentence",
    "A2": "order_words",
    "B1": "paraphrase",
    "B2": "continue_sentence",
    "C1": "continue_sentence",
    "C2": "continue_sentence",
}

LEVEL_TITLE_RU = {
    "A1": "Исправь ошибку в предложении",
    "A2": "Составь предложение из слов",
    "B1": "Перефразируй предложение",
    "B2": "Продолжи предложение",
    "C1": "Продолжи предложение",
    "C2": "Продолжи предложение",
}


def has_extra_for_level(level: str) -> bool:
    return str(level or "").upper() in EXTRA_BANKS


def get_extra_bank(level: str) -> list[dict]:
    return list(EXTRA_BANKS.get(str(level or "").upper()) or [])


def get_extra_item(level: str, index: int) -> dict | None:
    bank = get_extra_bank(level)
    if not bank:
        return None
    return dict(bank[int(index) % len(bank)])
