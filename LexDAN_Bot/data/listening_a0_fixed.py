"""
Фиксированный контент Listening A0: диалоги + Task1/Task2.
Task3 (порядок реплик) строится из turns как обычно.
"""

from __future__ import annotations

# topic_id → speakers + 12 turns + task1 + task2
A0_FIXED: dict[str, dict] = {
    "hello": {
        "speakers": [
            {"name": "Oliver", "gender": "male", "role": "Oliver"},
            {"name": "Mia", "gender": "female", "role": "Mia"},
        ],
        "turns": [
            (0, "Hi! My name is Oliver."),
            (1, "Hi, Oliver! I'm Mia. Nice to meet you."),
            (0, "I'm from London. And you?"),
            (1, "I'm from London too! What a surprise!"),
            (0, "I'm twenty-five years old. And you?"),
            (1, "I'm twenty-two. I'm younger than you."),
            (0, "You wear glasses. They look nice."),
            (1, "Thanks! Yes, I like them."),
            (0, "We met at the fountain. Do you like it here?"),
            (1, "Yes, it's very beautiful. I love this park."),
            (0, "Great. Shall we have coffee?"),
            (1, "I'd love to! Let's go."),
        ],
        "task1": [
            {
                "question": "Where is Oliver from?",
                "options": ["London", "New York", "Paris", "Moscow"],
                "correct": 0,
                "explain_wrong_ru": "Оливер из Лондона.",
            },
            {
                "question": "How old is Oliver?",
                "options": ["20", "25", "30", "35"],
                "correct": 1,
                "explain_wrong_ru": "Оливеру 25 лет.",
            },
            {
                "question": "How old is Mia?",
                "options": ["20", "22", "25", "30"],
                "correct": 1,
                "explain_wrong_ru": "Миа 22 года.",
            },
        ],
        "task2": [
            {
                "statement": "Oliver came to London by train.",
                "is_true": False,
                "explain_ru": "В диалоге не говорят, что Оливер приехал на поезде.",
            },
            {
                "statement": "Mia wears glasses.",
                "is_true": True,
                "explain_ru": "Оливер говорит, что Миа носит очки.",
            },
            {
                "statement": "They met at the fountain.",
                "is_true": True,
                "explain_ru": "Оливер говорит: we met at the fountain.",
            },
        ],
    },
    "numbers": {
        "speakers": [
            {"name": "Ethan", "gender": "male", "role": "Ethan"},
            {"name": "Sophia", "gender": "female", "role": "Sophia"},
        ],
        "turns": [
            (0, "Hi, Sophia! How are you?"),
            (1, "Hi, Ethan! I'm fine."),
            (0, "My phone number is five five five, one two three four. Write it down."),
            (1, "Five five five, one two three four? Got it. My number is five five five, five six seven eight."),
            (0, "I have two brothers. Do you have any brothers or sisters?"),
            (1, "I have one sister. Her name is Ava."),
            (0, "I'm older than you. I'm twenty-four."),
            (1, "And I'm twenty-two. You're a bit older."),
            (0, "I wrote your number on a napkin."),
            (1, "And I remembered your number. It starts with five five five."),
            (0, "Great. I'll call you tomorrow!"),
            (1, "Okay. I'll wait!"),
        ],
        "task1": [
            {
                "question": "What is Ethan's phone number?",
                "options": ["555-1234", "555-5678", "555-9101", "555-1122"],
                "correct": 0,
                "explain_wrong_ru": "Номер Итана — 555-1234.",
            },
            {
                "question": "How many brothers does Ethan have?",
                "options": ["1", "2", "3", "4"],
                "correct": 1,
                "explain_wrong_ru": "У Итана два брата.",
            },
            {
                "question": "How old is Sophia?",
                "options": ["25", "26", "27", "22"],
                "correct": 3,
                "explain_wrong_ru": "Софии 22 года.",
            },
        ],
        "task2": [
            {
                "statement": "Ethan has two sisters.",
                "is_true": False,
                "explain_ru": "У Итана два брата, не две сестры.",
            },
            {
                "statement": "Ethan wrote the number on a napkin.",
                "is_true": True,
                "explain_ru": "Итан записал номер на салфетке.",
            },
            {
                "statement": "Ethan's number starts with four.",
                "is_true": False,
                "explain_ru": "Номер начинается с 555, не с 4.",
            },
        ],
    },
    "family": {
        "speakers": [
            {"name": "Emma", "gender": "female", "role": "Emma"},
            {"name": "Friend", "gender": "female", "role": "listener"},
        ],
        "turns": [
            (0, "My family is my mum, my dad, and my little brother."),
            (0, "My mum's name is Mary."),
            (0, "My dad works in a hospital. He is a doctor."),
            (0, "My mum wears glasses. She is very beautiful."),
            (0, "My brother is very little. He is ten years old."),
            (0, "We are a happy family. There are four of us."),
            (0, "My brother is the youngest."),
            (0, "We all love spending time together."),
            (0, "I don't have an older sister."),
            (0, "I am the big sister for my brother."),
            (0, "I love my family."),
            (0, "They always support me."),
        ],
        "task1": [
            {
                "question": "How old is Emma's brother?",
                "options": ["5", "7", "10", "12"],
                "correct": 2,
                "explain_wrong_ru": "Брату Эммы 10 лет.",
            },
            {
                "question": "How many people are in Emma's family?",
                "options": ["3", "4", "5", "6"],
                "correct": 1,
                "explain_wrong_ru": "В семье четверо.",
            },
            {
                "question": "Who is the youngest in the family?",
                "options": ["Mum", "Dad", "Emma", "Brother"],
                "correct": 3,
                "explain_wrong_ru": "Младший — брат.",
            },
        ],
        "task2": [
            {
                "statement": "Emma's dad works in a hospital.",
                "is_true": True,
                "explain_ru": "Папа работает в больнице, он врач.",
            },
            {
                "statement": "Emma's mum wears glasses.",
                "is_true": True,
                "explain_ru": "Мама носит очки.",
            },
            {
                "statement": "Emma has an older sister.",
                "is_true": False,
                "explain_ru": "У Эммы нет старшей сестры.",
            },
        ],
    },
    "colors": {
        "speakers": [
            {"name": "Noah", "gender": "male", "role": "Noah"},
            {"name": "Lily", "gender": "female", "role": "Lily"},
        ],
        "turns": [
            (0, "Hi, Lily! What's your favourite colour?"),
            (1, "My favourite colour is red. And yours?"),
            (0, "I love blue. It's my favourite."),
            (1, "Blue is a beautiful colour. It looks good on you."),
            (0, "Today I'm wearing a blue T-shirt. Look."),
            (1, "It's very nice! And I like green and red."),
            (0, "I have a blue pen. Do you want it?"),
            (1, "No, thanks. I have a red pen."),
            (0, "I see you don't wear green clothes."),
            (1, "You're right. Green is not my colour."),
            (0, "I bought a red bag yesterday. But it doesn't suit me."),
            (1, "Ha! Red is my colour. I love it."),
        ],
        "task1": [
            {
                "question": "What colour does Noah like?",
                "options": ["red", "blue", "green", "yellow"],
                "correct": 1,
                "explain_wrong_ru": "Ноа любит синий.",
            },
            {
                "question": "What colour does Lily like?",
                "options": ["blue", "green", "red", "yellow"],
                "correct": 2,
                "explain_wrong_ru": "Лили любит красный.",
            },
            {
                "question": "What colour is Lily's pen?",
                "options": ["black", "blue", "red", "green"],
                "correct": 2,
                "explain_wrong_ru": "У Лили красная ручка.",
            },
        ],
        "task2": [
            {
                "statement": "Noah is wearing a blue T-shirt.",
                "is_true": True,
                "explain_ru": "Ноа в синей футболке.",
            },
            {
                "statement": "Lily bought a red bag.",
                "is_true": False,
                "explain_ru": "Красную сумку купил Ноа, не Лили.",
            },
            {
                "statement": "Green is not Lily's colour.",
                "is_true": True,
                "explain_ru": "Лили говорит, что зелёный — не её цвет.",
            },
        ],
    },
    "food_words": {
        "speakers": [
            {"name": "Liam", "gender": "male", "role": "Liam"},
            {"name": "Chloe", "gender": "female", "role": "Chloe"},
        ],
        "turns": [
            (0, "Hi, Chloe! Are you hungry?"),
            (1, "Yes, I'm very hungry. Let's order food."),
            (0, "I want to order a burger. And you?"),
            (1, "I want a salad. It's healthy."),
            (0, "Okay. I'll order a burger, and you a salad."),
            (1, "And I want coffee. What about you?"),
            (0, "I want coffee too. Two coffees, please."),
            (1, "The waiter brought our order in five minutes."),
            (0, "Yes, that was fast. I'll pay for both of us."),
            (1, "Thanks, Liam! You're very kind."),
            (1, "I want to ask for extra sauce."),
            (0, "Sure! I'll ask the waiter."),
        ],
        "task1": [
            {
                "question": "What did Liam order?",
                "options": ["pizza", "salad", "burger", "soup"],
                "correct": 2,
                "explain_wrong_ru": "Лиам заказал бургер.",
            },
            {
                "question": "What did Chloe order?",
                "options": ["burger", "salad", "pizza", "soup"],
                "correct": 1,
                "explain_wrong_ru": "Хлоя заказала салат.",
            },
            {
                "question": "What do they drink?",
                "options": ["water", "juice", "coffee", "tea"],
                "correct": 2,
                "explain_wrong_ru": "Они пьют кофе.",
            },
        ],
        "task2": [
            {
                "statement": "The waiter brought the order in five minutes.",
                "is_true": True,
                "explain_ru": "Заказ принесли через 5 минут.",
            },
            {
                "statement": "Liam paid for both of them.",
                "is_true": True,
                "explain_ru": "Лиам платит за обоих.",
            },
            {
                "statement": "Chloe asked for extra sauce.",
                "is_true": True,
                "explain_ru": "Хлоя хочет дополнительный соус.",
            },
        ],
    },
    "classroom": {
        "speakers": [
            {"name": "Jake", "gender": "male", "role": "Jake"},
            {"name": "Zara", "gender": "female", "role": "Zara"},
        ],
        "turns": [
            (0, "Hi, Zara! How was your day?"),
            (1, "Hi, Jake! All good. And yours?"),
            (0, "I had maths. It's my favourite subject."),
            (1, "Maths is cool! And I love sport."),
            (0, "There are fifteen students in our class. That's a lot."),
            (1, "Yes, we have a big class. I like our class."),
            (0, "Our teacher was in a red dress today."),
            (1, "Yes, I noticed. It's very beautiful."),
            (0, "There was a test today. It was hard."),
            (1, "You're right. But I think I did okay."),
            (0, "You sit in the front row. That's a good place."),
            (1, "I like sitting near the board."),
        ],
        "task1": [
            {
                "question": "What subject does Jake like?",
                "options": ["maths", "history", "literature", "sport"],
                "correct": 0,
                "explain_wrong_ru": "Джейку нравится математика.",
            },
            {
                "question": "What subject does Zara like?",
                "options": ["maths", "history", "sport", "music"],
                "correct": 2,
                "explain_wrong_ru": "Заре нравится спорт.",
            },
            {
                "question": "How many students are in the class?",
                "options": ["10", "15", "20", "25"],
                "correct": 1,
                "explain_wrong_ru": "В классе 15 учеников.",
            },
        ],
        "task2": [
            {
                "statement": "The teacher is wearing a red dress.",
                "is_true": True,
                "explain_ru": "Учительница в красном платье.",
            },
            {
                "statement": "Jake sits in the front row.",
                "is_true": False,
                "explain_ru": "На первой парте сидит Зара, не Джейк.",
            },
            {
                "statement": "There was a test today.",
                "is_true": True,
                "explain_ru": "Сегодня была контрольная.",
            },
        ],
    },
    "pets": {
        "speakers": [
            {"name": "Zack", "gender": "male", "role": "Zack"},
            {"name": "Mila", "gender": "female", "role": "Mila"},
        ],
        "turns": [
            (0, "Hi, Mila! How is your pet?"),
            (1, "I have a cat. Her name is Bella."),
            (0, "So cute! And I have a dog."),
            (1, "You have a dog? That's great!"),
            (0, "Yes, she loves playing in the park."),
            (1, "My cat loves sleeping in the sun."),
            (0, "I bought my dog at a pet shop."),
            (1, "And someone gave me my cat as a gift."),
            (0, "My dog is not afraid of loud sounds."),
            (1, "But my cat is afraid of noise. She is very careful."),
            (0, "Let's walk with them together sometime."),
            (1, "Great! That will be fun."),
        ],
        "task1": [
            {
                "question": "What pet does Zack have?",
                "options": ["a cat", "a dog", "a hamster", "a fish"],
                "correct": 1,
                "explain_wrong_ru": "У Зака собака.",
            },
            {
                "question": "What pet does Mila have?",
                "options": ["a dog", "a cat", "a hamster", "a parrot"],
                "correct": 1,
                "explain_wrong_ru": "У Милы кошка.",
            },
            {
                "question": "What is Mila's cat's name?",
                "options": ["Max", "Bella", "Mimi", "Lucky"],
                "correct": 1,
                "explain_wrong_ru": "Кошку зовут Белла.",
            },
        ],
        "task2": [
            {
                "statement": "Zack's dog loves playing in the park.",
                "is_true": True,
                "explain_ru": "Собака любит играть в парке.",
            },
            {
                "statement": "Mila's cat is afraid of loud sounds.",
                "is_true": True,
                "explain_ru": "Кошка боится шума.",
            },
            {
                "statement": "Zack bought his dog at a pet shop.",
                "is_true": True,
                "explain_ru": "Зак купил собаку в зоомагазине.",
            },
        ],
    },
    "days": {
        "speakers": [
            {"name": "Connor", "gender": "male", "role": "Connor"},
            {"name": "Aurora", "gender": "female", "role": "Aurora"},
        ],
        "turns": [
            (0, "Hi, Aurora! What are you doing today?"),
            (1, "Today I'm resting. And you?"),
            (0, "I work on Mondays. That's my work day."),
            (1, "I study on Wednesdays. I have three lessons."),
            (0, "I go to the gym on Fridays."),
            (1, "And I go to the library on Tuesdays."),
            (0, "What do you do on Saturday?"),
            (1, "On Saturday I go to the cinema. And you?"),
            (0, "I want to go to the cinema too. Let's go together."),
            (1, "Let's! We can go on Sunday."),
            (0, "On Sunday I rest at home. That's my rest day."),
            (1, "Okay. Then see you on Saturday!"),
        ],
        "task1": [
            {
                "question": "What does Connor do on Monday?",
                "options": ["works", "rests", "studies", "plays"],
                "correct": 0,
                "explain_wrong_ru": "В понедельник Коннор работает.",
            },
            {
                "question": "What does Aurora do on Wednesday?",
                "options": ["works", "rests", "studies", "plays"],
                "correct": 2,
                "explain_wrong_ru": "В среду Аврора учится.",
            },
            {
                "question": "What do they do on Saturday?",
                "options": ["play tennis", "go to the cinema", "walk", "study"],
                "correct": 1,
                "explain_wrong_ru": "В субботу они идут в кино.",
            },
        ],
        "task2": [
            {
                "statement": "Connor usually goes to the gym on Fridays.",
                "is_true": True,
                "explain_ru": "По пятницам Коннор ходит в спортзал.",
            },
            {
                "statement": "Aurora goes to the library on Tuesdays.",
                "is_true": True,
                "explain_ru": "По вторникам Аврора ходит в библиотеку.",
            },
            {
                "statement": "On Sunday they both rest at home.",
                "is_true": False,
                "explain_ru": "В воскресенье дома отдыхает Коннор; встречаются они в субботу.",
            },
        ],
    },
    "weather_easy": {
        "speakers": [
            {"name": "Felix", "gender": "male", "role": "Felix"},
            {"name": "Ella", "gender": "female", "role": "Ella"},
        ],
        "turns": [
            (0, "Hi, Ella! How is the weather today?"),
            (1, "It's sunny today! Very warm."),
            (0, "Yesterday there was a strong wind. And today it's perfect."),
            (1, "Yes, today it's twenty degrees. That's nice."),
            (0, "Tomorrow it will be rainy. Did you take an umbrella?"),
            (1, "No, I forgot. But I can take a jacket."),
            (0, "On Saturday it will be colder than today."),
            (1, "I hope it's not too cold."),
            (0, "I love this weather. Sun and warmth."),
            (1, "I love the sun too. It makes me happy."),
            (0, "Shall we go for a walk this evening?"),
            (1, "I'd love to! Let's go."),
        ],
        "task1": [
            {
                "question": "What is the weather like today?",
                "options": ["rainy", "cloudy", "sunny", "windy"],
                "correct": 2,
                "explain_wrong_ru": "Сегодня солнечно.",
            },
            {
                "question": "What will the weather be like tomorrow?",
                "options": ["sunny", "rainy", "cloudy", "windy"],
                "correct": 1,
                "explain_wrong_ru": "Завтра будет дождливо.",
            },
            {
                "question": "What is the temperature today?",
                "options": ["10°", "15°", "20°", "25°"],
                "correct": 2,
                "explain_wrong_ru": "Сегодня 20 градусов.",
            },
        ],
        "task2": [
            {
                "statement": "Yesterday there was a strong wind.",
                "is_true": True,
                "explain_ru": "Вчера был сильный ветер.",
            },
            {
                "statement": "Felix took an umbrella for the rain.",
                "is_true": False,
                "explain_ru": "Зонт забыла Элла; Феликс только спросил.",
            },
            {
                "statement": "On Saturday it will be colder than today.",
                "is_true": True,
                "explain_ru": "В субботу будет холоднее.",
            },
        ],
    },
    "home": {
        "speakers": [
            {"name": "Mason", "gender": "male", "role": "Mason"},
            {"name": "Amelia", "gender": "female", "role": "Amelia"},
        ],
        "turns": [
            (0, "Hi, Amelia! How is your new home?"),
            (1, "Hi, Mason! I like it a lot."),
            (0, "I have my own room. It's cosy."),
            (1, "And I have a garden. I love the garden."),
            (0, "In my room there is a TV. I love watching films."),
            (1, "In my garden I planted roses. They are beautiful."),
            (0, "I live in a dormitory. It's not very cosy."),
            (1, "A dormitory is fun. There are many friends."),
            (0, "I live alone. Sometimes I feel sad."),
            (1, "You can come and visit me."),
            (0, "Thanks, Amelia! I'll come at the weekend."),
            (1, "I'll be happy. We'll drink tea."),
        ],
        "task1": [
            {
                "question": "What does Mason have?",
                "options": ["a garden", "a room", "a garage", "a pool"],
                "correct": 1,
                "explain_wrong_ru": "У Мейсона есть своя комната.",
            },
            {
                "question": "What does Amelia have?",
                "options": ["a room", "a garden", "a garage", "a pool"],
                "correct": 1,
                "explain_wrong_ru": "У Амелии есть сад.",
            },
            {
                "question": "Where does Mason live?",
                "options": ["in a house", "in a flat", "in a dormitory", "in a hotel"],
                "correct": 2,
                "explain_wrong_ru": "Мейсон живёт в общежитии.",
            },
        ],
        "task2": [
            {
                "statement": "There is a TV in Mason's room.",
                "is_true": True,
                "explain_ru": "В комнате Мейсона есть телевизор.",
            },
            {
                "statement": "Amelia planted roses in the garden.",
                "is_true": True,
                "explain_ru": "Амелия посадила розы.",
            },
            {
                "statement": "Mason lives alone.",
                "is_true": True,
                "explain_ru": "Мейсон живёт один.",
            },
        ],
    },
}


def has_a0_fixed(topic_id: str) -> bool:
    return str(topic_id or "") in A0_FIXED


def get_a0_fixed(topic_id: str) -> dict | None:
    return A0_FIXED.get(str(topic_id or ""))
