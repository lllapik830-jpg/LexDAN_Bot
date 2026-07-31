"""
Фиксированный контент Listening A1: диалоги + Task1/Task2.
Task3 (порядок реплик) строится из turns как обычно.
"""

from __future__ import annotations

A1_FIXED: dict[str, dict] = {
    "cafe_simple": {
        "speakers": [
            {"name": "Jack", "gender": "male", "role": "Jack"},
            {"name": "Emily", "gender": "female", "role": "Emily"},
        ],
        "turns": [
            (0, "Hi, Emily! Have you chosen what to order?"),
            (1, "Hi, Jack! Yes, I want coffee and a croissant."),
            (0, "I'll have tea and toast with butter."),
            (1, "Sounds tasty! I love morning coffee."),
            (0, "The waiter just brought our order quickly."),
            (1, "The croissant looks fresh. Very tasty!"),
            (0, "I'll pay for both of us. Is that okay?"),
            (1, "Oh, thank you! You're very kind."),
            (0, "You're welcome! It was a nice morning."),
            (1, "I love this café. It's cosy and quiet here."),
            (0, "Yes, it's nice to sit and talk here."),
            (1, "Deal! Next time I'll treat you."),
        ],
        "task1": [
            {
                "question": "What did Emily order?",
                "options": ["tea and toast", "coffee and a croissant", "juice and a sandwich", "milk and a muffin"],
                "correct": 1,
                "explain_wrong_ru": "Эмили заказала кофе и круассан.",
            },
            {
                "question": "What did Jack order?",
                "options": ["coffee and a croissant", "juice and a sandwich", "tea and toast", "hot chocolate"],
                "correct": 2,
                "explain_wrong_ru": "Джек заказал чай и тост.",
            },
            {
                "question": "Who paid for the order?",
                "options": ["Emily", "the waiter", "nobody", "Jack"],
                "correct": 3,
                "explain_wrong_ru": "Заказ оплатил Джек.",
            },
        ],
        "task2": [
            {
                "statement": "The waiter brought the order quickly.",
                "is_true": True,
                "explain_ru": "Официант быстро принёс заказ.",
            },
            {
                "statement": "Emily paid for the order.",
                "is_true": False,
                "explain_ru": "Платил Джек, не Эмили.",
            },
            {
                "statement": "Jack ordered juice.",
                "is_true": False,
                "explain_ru": "Джек заказал чай, не сок.",
            },
        ],
    },
    "school": {
        "speakers": [
            {"name": "Sophie", "gender": "female", "role": "Sophie"},
            {"name": "Noah", "gender": "male", "role": "Noah"},
        ],
        "turns": [
            (0, "Noah, are you ready for the maths test?"),
            (1, "Hi, Sophie! Yes, I'm almost ready."),
            (0, "We have four lessons today. That's a lot."),
            (1, "Yes, I was tired after the third lesson."),
            (0, "Our teacher says we are doing well."),
            (1, "I like maths, but it's hard."),
            (0, "Do you like history?"),
            (1, "No, history is not my favourite."),
            (0, "My favourite subject is art."),
            (1, "Art is interesting! Do you draw?"),
            (0, "Yes, I love drawing. It relaxes me."),
            (1, "Maybe we can go to an exhibition together?"),
        ],
        "task1": [
            {
                "question": "What subject does Sophie like?",
                "options": ["maths", "history", "art", "sport"],
                "correct": 2,
                "explain_wrong_ru": "Софи любит искусство.",
            },
            {
                "question": "How many lessons do they have today?",
                "options": ["2", "3", "4", "5"],
                "correct": 2,
                "explain_wrong_ru": "Сегодня четыре урока.",
            },
            {
                "question": "What does Noah like?",
                "options": ["history", "art", "maths", "sport"],
                "correct": 2,
                "explain_wrong_ru": "Ной любит математику.",
            },
        ],
        "task2": [
            {
                "statement": "Sophie loves drawing.",
                "is_true": True,
                "explain_ru": "Софи любит рисовать.",
            },
            {
                "statement": "Noah was tired after the second lesson.",
                "is_true": False,
                "explain_ru": "Он устал после третьего урока.",
            },
            {
                "statement": "Noah does not like history.",
                "is_true": True,
                "explain_ru": "История — не любимый предмет Ноя.",
            },
        ],
    },
    "hobbies": {
        "speakers": [
            {"name": "Olivia", "gender": "female", "role": "Olivia"},
            {"name": "Mason", "gender": "male", "role": "Mason"},
        ],
        "turns": [
            (0, "Mason, what do you like doing in your free time?"),
            (1, "Hi, Olivia! I like playing the guitar."),
            (0, "Cool! I can't play any musical instruments."),
            (1, "It's not hard. I can teach you."),
            (0, "Really? That would be wonderful."),
            (1, "My hobbies are fishing and walks in nature."),
            (0, "I like reading books and watching films."),
            (1, "Reading is a great hobby!"),
            (0, "But I want to try something new."),
            (1, "You can start with music. It's fun."),
            (0, "Yes, I want to learn to play the guitar."),
            (1, "Then let's start today!"),
        ],
        "task1": [
            {
                "question": "What is Mason's hobby?",
                "options": ["reading", "fishing", "films", "sport"],
                "correct": 1,
                "explain_wrong_ru": "Хобби Мэйсона — рыбалка (и гитара).",
            },
            {
                "question": "What does Olivia like doing?",
                "options": ["playing the guitar", "fishing", "reading books", "sport"],
                "correct": 2,
                "explain_wrong_ru": "Оливия любит читать книги.",
            },
            {
                "question": "What does Mason want to teach Olivia?",
                "options": ["the piano", "the guitar", "the violin", "the drums"],
                "correct": 1,
                "explain_wrong_ru": "Он хочет научить её игре на гитаре.",
            },
        ],
        "task2": [
            {
                "statement": "Mason can play the guitar.",
                "is_true": True,
                "explain_ru": "Мэйсон умеет играть на гитаре.",
            },
            {
                "statement": "Olivia does not like reading.",
                "is_true": False,
                "explain_ru": "Оливия любит читать.",
            },
            {
                "statement": "Mason offered to teach Olivia music.",
                "is_true": True,
                "explain_ru": "Мэйсон предложил научить её музыке.",
            },
        ],
    },
    "shopping_easy": {
        "speakers": [
            {"name": "Isabella", "gender": "female", "role": "Isabella"},
            {"name": "Luke", "gender": "male", "role": "Luke"},
        ],
        "turns": [
            (0, "Luke, we need to buy food for dinner."),
            (1, "Okay. What are we going to cook?"),
            (0, "We'll make pasta with vegetables."),
            (1, "Sounds tasty! What do we need to buy?"),
            (0, "We need tomatoes and greens."),
            (1, "I'll take a basket. Have you chosen the pasta?"),
            (0, "Yes, I took spaghetti."),
            (1, "I bought tomatoes. They are red and fresh."),
            (0, "I found greens and onion."),
            (1, "We need to get bread."),
            (0, "I'll take white bread."),
            (1, "Great, we're ready to pay."),
        ],
        "task1": [
            {
                "question": "What are they going to cook?",
                "options": ["soup", "pasta", "rice", "salad"],
                "correct": 1,
                "explain_wrong_ru": "Они готовят пасту.",
            },
            {
                "question": "What bread did they buy?",
                "options": ["white", "brown", "gluten-free", "seeded"],
                "correct": 0,
                "explain_wrong_ru": "Они взяли белый хлеб.",
            },
            {
                "question": "What did Isabella buy?",
                "options": ["bread", "spaghetti", "fruit", "meat"],
                "correct": 1,
                "explain_wrong_ru": "Изабелла взяла спагетти.",
            },
        ],
        "task2": [
            {
                "statement": "Luke took a basket.",
                "is_true": True,
                "explain_ru": "Люк взял корзину.",
            },
            {
                "statement": "The tomatoes were green.",
                "is_true": False,
                "explain_ru": "Помидоры были красные и свежие.",
            },
            {
                "statement": "Isabella bought spaghetti.",
                "is_true": True,
                "explain_ru": "Изабелла купила спагетти.",
            },
        ],
    },
    "daily": {
        "speakers": [
            {"name": "Chloe", "gender": "female", "role": "Chloe"},
            {"name": "Ethan", "gender": "male", "role": "Ethan"},
        ],
        "turns": [
            (0, "Ethan, how does your usual day go?"),
            (1, "I get up at seven and have breakfast."),
            (0, "I also get up early. I go to work at eight."),
            (1, "I have lunch at twelve."),
            (0, "I also have lunch at twelve. That's convenient."),
            (1, "I come home at six in the evening."),
            (0, "I come home at seven. I have dinner and rest."),
            (1, "At the weekend I go to the gym."),
            (0, "I don't go to the gym. I go for walks."),
            (1, "Walking is healthy too."),
            (0, "At the weekend I like watching films."),
            (1, "Great plan! I like films too."),
        ],
        "task1": [
            {
                "question": "What time does Ethan have lunch?",
                "options": ["11:00", "12:00", "13:00", "14:00"],
                "correct": 1,
                "explain_wrong_ru": "Итан обедает в 12:00.",
            },
            {
                "question": "What time does Chloe come home?",
                "options": ["6 pm", "7 pm", "8 pm", "5 pm"],
                "correct": 1,
                "explain_wrong_ru": "Хлоя возвращается в 7 вечера.",
            },
            {
                "question": "What does Ethan do at the weekend?",
                "options": ["watches films", "goes to the gym", "goes for walks", "works"],
                "correct": 1,
                "explain_wrong_ru": "По выходным Итан ходит в спортзал.",
            },
        ],
        "task2": [
            {
                "statement": "Chloe gets up at six in the morning.",
                "is_true": False,
                "explain_ru": "В диалоге нет, что Хлоя встаёт в 6.",
            },
            {
                "statement": "Chloe has dinner at seven in the evening.",
                "is_true": True,
                "explain_ru": "Хлоя возвращается в 7 и ужинает.",
            },
            {
                "statement": "Ethan does not like films.",
                "is_true": False,
                "explain_ru": "Итан тоже любит кино.",
            },
        ],
    },
    "bus": {
        "speakers": [
            {"name": "Jake", "gender": "male", "role": "Jake"},
            {"name": "Aurora", "gender": "female", "role": "Aurora"},
        ],
        "turns": [
            (0, "Aurora, do you often take the bus?"),
            (1, "Yes, every day to work."),
            (0, "I take the bus too. It's convenient."),
            (1, "Today there were many people, but we found seats."),
            (0, "I give my seat to older people."),
            (1, "That's very kind! You're a good person."),
            (0, "How many stops to your work?"),
            (1, "Three stops. And you?"),
            (0, "I have five stops. That's a bit far."),
            (1, "But you can read a book on the way."),
            (0, "Yes, I love reading on the bus."),
            (1, "Do we get off at the next stop?"),
        ],
        "task1": [
            {
                "question": "How many stops to Aurora's work?",
                "options": ["2", "3", "4", "5"],
                "correct": 1,
                "explain_wrong_ru": "До работы Авроры три остановки.",
            },
            {
                "question": "How many stops to Jake's work?",
                "options": ["3", "4", "5", "6"],
                "correct": 2,
                "explain_wrong_ru": "До работы Джейка пять остановок.",
            },
            {
                "question": "What does Jake do on the bus?",
                "options": ["sleeps", "listens to music", "reads books", "talks"],
                "correct": 2,
                "explain_wrong_ru": "Джейк читает в автобусе.",
            },
        ],
        "task2": [
            {
                "statement": "Aurora gives her seat to older people.",
                "is_true": False,
                "explain_ru": "Место уступает Джейк, не Аврора.",
            },
            {
                "statement": "There were many people on the bus today.",
                "is_true": True,
                "explain_ru": "Сегодня в автобусе было много людей.",
            },
            {
                "statement": "Jake does not like reading.",
                "is_true": False,
                "explain_ru": "Джейк любит читать в автобусе.",
            },
        ],
    },
    "library": {
        "speakers": [
            {"name": "Mila", "gender": "female", "role": "Mila"},
            {"name": "Noah", "gender": "male", "role": "Noah"},
        ],
        "turns": [
            (0, "Noah, do you often go to the library?"),
            (1, "Yes, every week. I borrow books there."),
            (0, "I love reading too. What are you reading now?"),
            (1, "I'm reading an adventure novel."),
            (0, "Sounds interesting! I'm reading a detective story."),
            (1, "The library is quiet and calm."),
            (0, "Yes, it's cosy here and there are many books."),
            (1, "I already took two books this week."),
            (0, "I have a library card."),
            (1, "With a library card you can borrow many books."),
            (0, "I'm glad we go to the same library."),
            (1, "Yes, it's convenient. We can exchange books."),
        ],
        "task1": [
            {
                "question": "What book is Noah reading?",
                "options": ["a detective story", "an adventure novel", "science fiction", "poetry"],
                "correct": 1,
                "explain_wrong_ru": "Ноа читает роман о приключениях.",
            },
            {
                "question": "How many books did Noah take this week?",
                "options": ["1", "2", "3", "4"],
                "correct": 1,
                "explain_wrong_ru": "Ноа взял две книги.",
            },
            {
                "question": "What does Mila say about the library?",
                "options": ["it's noisy", "it's boring", "it's cosy", "it's dark"],
                "correct": 2,
                "explain_wrong_ru": "Мила говорит, что там уютно.",
            },
        ],
        "task2": [
            {
                "statement": "Noah borrows books every week.",
                "is_true": True,
                "explain_ru": "Ноа ходит в библиотеку каждую неделю.",
            },
            {
                "statement": "Mila is reading an adventure novel.",
                "is_true": False,
                "explain_ru": "Мила читает детектив, роман читает Ноа.",
            },
            {
                "statement": "Mila has a library card.",
                "is_true": True,
                "explain_ru": "У Милы есть библиотечный билет.",
            },
        ],
    },
    "park": {
        "speakers": [
            {"name": "Zara", "gender": "female", "role": "Zara"},
            {"name": "Liam", "gender": "male", "role": "Liam"},
        ],
        "turns": [
            (0, "Liam, how do you like this park?"),
            (1, "It's very beautiful here! I love this place."),
            (0, "I love walking in the park at the weekend."),
            (1, "There are big trees and flowers here."),
            (0, "I see people walking with dogs."),
            (1, "Yes, you can walk dogs here."),
            (0, "I want to sit on a bench and rest."),
            (1, "Good idea! Let's rest a little."),
            (0, "There's a small café here. We can have coffee."),
            (1, "Great! I love coffee."),
            (0, "I'm already tired. Let's go home."),
            (1, "Okay. The walk was nice."),
        ],
        "task1": [
            {
                "question": "What does Zara want to do in the park?",
                "options": ["run", "sit on a bench", "play ball", "ride a bike"],
                "correct": 1,
                "explain_wrong_ru": "Зара хочет посидеть на скамейке.",
            },
            {
                "question": "What is there in the park?",
                "options": ["a pool", "a shop", "a café", "a gym"],
                "correct": 2,
                "explain_wrong_ru": "В парке есть кафе.",
            },
            {
                "question": "What is allowed in the park?",
                "options": ["play football", "walk dogs", "make a fire", "make noise"],
                "correct": 1,
                "explain_wrong_ru": "В парке можно выгуливать собак.",
            },
        ],
        "task2": [
            {
                "statement": "Zara is tired.",
                "is_true": True,
                "explain_ru": "Зара устала.",
            },
            {
                "statement": "Liam does not like coffee.",
                "is_true": False,
                "explain_ru": "Лиам любит кофе.",
            },
            {
                "statement": "Zara wants to sit on a bench.",
                "is_true": True,
                "explain_ru": "Зара хочет посидеть на скамейке.",
            },
        ],
    },
    "phone_easy": {
        "speakers": [
            {"name": "Ella", "gender": "female", "role": "Ella"},
            {"name": "Oliver", "gender": "male", "role": "Oliver"},
        ],
        "turns": [
            (0, "Hi, Oliver! How are you?"),
            (1, "Hi, Ella! I'm fine."),
            (0, "I'm calling to invite you to my place."),
            (1, "Thanks! When?"),
            (0, "On Saturday at six in the evening."),
            (1, "I'm free. I'll definitely come."),
            (0, "I'll make dinner. Do you like pizza?"),
            (1, "Yes, I love pizza a lot!"),
            (0, "Great! I'll order pizza."),
            (1, "I'll bring drinks."),
            (0, "It will be a wonderful evening."),
            (1, "I can't wait for Saturday!"),
        ],
        "task1": [
            {
                "question": "What time did Ella invite Oliver?",
                "options": ["5 pm", "6 pm", "7 pm", "8 pm"],
                "correct": 1,
                "explain_wrong_ru": "Приглашение на 6 вечера.",
            },
            {
                "question": "What does Ella plan to make?",
                "options": ["salad", "pizza", "soup", "pasta"],
                "correct": 1,
                "explain_wrong_ru": "Элла закажет пиццу.",
            },
            {
                "question": "What did Oliver promise to bring?",
                "options": ["dessert", "drinks", "bread", "fruit"],
                "correct": 1,
                "explain_wrong_ru": "Оливер принесёт напитки.",
            },
        ],
        "task2": [
            {
                "statement": "Oliver is busy on Saturday.",
                "is_true": False,
                "explain_ru": "Оливер свободен в субботу.",
            },
            {
                "statement": "Ella will order pizza.",
                "is_true": True,
                "explain_ru": "Элла закажет пиццу.",
            },
            {
                "statement": "Oliver will bring a salad.",
                "is_true": False,
                "explain_ru": "Оливер принесёт напитки, не салат.",
            },
        ],
    },
    "clinic": {
        "speakers": [
            {"name": "Sophia", "gender": "female", "role": "Sophia"},
            {"name": "Mason", "gender": "male", "role": "Mason"},
        ],
        "turns": [
            (0, "Mason, I don't feel very well."),
            (1, "What happened, Sophia?"),
            (0, "I have a headache and a temperature."),
            (1, "You need to see a doctor."),
            (0, "Yes, I made an appointment at the clinic."),
            (1, "Have you already been to the doctor?"),
            (0, "Yes, just now. The doctor said it's a cold."),
            (1, "Good. You need to rest more."),
            (0, "The doctor prescribed medicine for me."),
            (1, "Don't forget to take it on time."),
            (0, "I feel a bit better now. Thanks for caring, Mason."),
            (1, "Rest and don't worry. I'm always here to help."),
        ],
        "task1": [
            {
                "question": "What did the doctor tell Sophia?",
                "options": ["she has the flu", "she has a cold", "she has an allergy", "she has a migraine"],
                "correct": 1,
                "explain_wrong_ru": "Врач сказал, что это простуда.",
            },
            {
                "question": "What did the doctor prescribe?",
                "options": ["tablets", "medicine", "vitamins", "syrup"],
                "correct": 1,
                "explain_wrong_ru": "Врач прописал лекарства.",
            },
            {
                "question": "How does Sophia feel now?",
                "options": ["worse", "a bit better", "the same", "tired"],
                "correct": 1,
                "explain_wrong_ru": "Софии немного лучше.",
            },
        ],
        "task2": [
            {
                "statement": "Sophia has a stomach ache.",
                "is_true": False,
                "explain_ru": "Болит голова и температура, не живот.",
            },
            {
                "statement": "Mason is always ready to help.",
                "is_true": True,
                "explain_ru": "Мэйсон всегда готов помочь.",
            },
            {
                "statement": "Sophia has already been to the doctor.",
                "is_true": True,
                "explain_ru": "София уже была у врача.",
            },
        ],
    },
}


def has_a1_fixed(topic_id: str) -> bool:
    return str(topic_id or "") in A1_FIXED


def get_a1_fixed(topic_id: str) -> dict | None:
    return A1_FIXED.get(str(topic_id or ""))
