"""
Фиксированный контент Listening A2: диалоги + Task1/Task2.
Task3 (порядок реплик) строится из turns как обычно.
"""

from __future__ import annotations

A2_FIXED: dict[str, dict] = {
    "cafe": {
        "speakers": [
            {"name": "Mark", "gender": "male", "role": "Mark"},
            {"name": "Lena", "gender": "female", "role": "Lena"},
        ],
        "turns": [
            (0, "Hi, Lena! Have you chosen already?"),
            (1, "Hi, Mark! Yes, I want a cappuccino and a dessert."),
            (0, "I'll have black coffee and a sandwich."),
            (1, "You always drink black coffee. And I love sweet things."),
            (0, "Today I'm treating you. Don't worry about the price."),
            (1, "Thanks, Mark! You're very generous."),
            (0, "It's the least I can do for a friend."),
            (1, "It's very cosy here. I love this place."),
            (0, "Yes, and the music is nice."),
            (1, "Shall we meet here again on Friday?"),
            (0, "Good idea! I'll be waiting."),
            (1, "Then it's a deal. See you on Friday!"),
        ],
        "task1": [
            {
                "question": "What did Lena order?",
                "options": ["black coffee and a sandwich", "a cappuccino and a dessert", "tea and a cake", "juice and a salad"],
                "correct": 1,
                "explain_wrong_ru": "Лена взяла капучино и десерт.",
            },
            {
                "question": "What did Mark order?",
                "options": ["a cappuccino and a dessert", "tea and toast", "black coffee and a sandwich", "hot chocolate"],
                "correct": 2,
                "explain_wrong_ru": "Марк взял чёрный кофе и сэндвич.",
            },
            {
                "question": "When did they agree to meet again?",
                "options": ["on Saturday", "on Friday", "on Sunday", "on Monday"],
                "correct": 1,
                "explain_wrong_ru": "Они договорились на пятницу.",
            },
        ],
        "task2": [
            {
                "statement": "Lena does not like sweet things.",
                "is_true": False,
                "explain_ru": "Лена любит сладкое.",
            },
            {
                "statement": "Mark treated Lena.",
                "is_true": True,
                "explain_ru": "Марк угощает Лену.",
            },
            {
                "statement": "The music in the café was loud.",
                "is_true": False,
                "explain_ru": "Музыка приятная, не громкая.",
            },
        ],
    },
    "station": {
        "speakers": [
            {"name": "Andrey", "gender": "male", "role": "Andrey"},
            {"name": "Katya", "gender": "female", "role": "Katya"},
        ],
        "turns": [
            (0, "Katya, we're almost late for the train!"),
            (1, "Don't worry, we still have ten minutes."),
            (0, "We need to find platform five."),
            (1, "I see the sign. Platform five is to the left."),
            (0, "We made it! The train is already here."),
            (1, "Let's find our seats. Our tickets are for carriage three."),
            (0, "We're sitting. I really love travelling!"),
            (1, "Me too. It's always an adventure."),
            (0, "The train leaves in five minutes."),
            (1, "Everything will be fine. We have food and water."),
            (0, "I really want to see our city in three hours."),
            (1, "Me too. Let's rest a little."),
        ],
        "task1": [
            {
                "question": "Which platform did they need?",
                "options": ["platform 3", "platform 4", "platform 5", "platform 6"],
                "correct": 2,
                "explain_wrong_ru": "Им нужна платформа 5.",
            },
            {
                "question": "Which carriage are their tickets for?",
                "options": ["carriage 1", "carriage 2", "carriage 3", "carriage 4"],
                "correct": 2,
                "explain_wrong_ru": "Билеты в вагон 3.",
            },
            {
                "question": "How much time is left before the train leaves?",
                "options": ["2 minutes", "5 minutes", "10 minutes", "15 minutes"],
                "correct": 1,
                "explain_wrong_ru": "До отправления 5 минут.",
            },
        ],
        "task2": [
            {
                "statement": "Andrey and Katya missed the train.",
                "is_true": False,
                "explain_ru": "Они успели на поезд.",
            },
            {
                "statement": "Platform five was to the right.",
                "is_true": False,
                "explain_ru": "Платформа 5 была налево.",
            },
            {
                "statement": "Andrey loves travelling.",
                "is_true": True,
                "explain_ru": "Андрей любит путешествовать.",
            },
        ],
    },
    "doctor": {
        "speakers": [
            {"name": "Natalia", "gender": "female", "role": "patient"},
            {"name": "Doctor Petrov", "gender": "male", "role": "doctor"},
        ],
        "turns": [
            (0, "Doctor, I don't feel very well."),
            (1, "What is bothering you, Natalia?"),
            (0, "I have a sore throat and a strong cough."),
            (1, "It looks like a viral infection."),
            (0, "I also have a slight temperature."),
            (1, "You need to take these tablets three times a day."),
            (0, "How many days should I take them?"),
            (1, "Usually five days. And drink a lot of liquids."),
            (0, "Thank you, doctor. I'll do everything you said."),
            (1, "If you don't feel better in three days, come again."),
            (0, "Okay, I'll remember."),
            (1, "Take care of yourself and get well soon."),
        ],
        "task1": [
            {
                "question": "What did the doctor say about Natalia's illness?",
                "options": ["it's an allergy", "it's a viral infection", "it's the flu", "it's a throat infection"],
                "correct": 1,
                "explain_wrong_ru": "Это вирусная инфекция.",
            },
            {
                "question": "How many days should she take the tablets?",
                "options": ["3 days", "5 days", "7 days", "10 days"],
                "correct": 1,
                "explain_wrong_ru": "Таблетки — обычно 5 дней.",
            },
            {
                "question": "What else did the doctor advise besides tablets?",
                "options": ["sleep more", "drink a lot of liquids", "eat less", "walk more"],
                "correct": 1,
                "explain_wrong_ru": "Пить много жидкости.",
            },
        ],
        "task2": [
            {
                "statement": "Natalia has a stomach ache.",
                "is_true": False,
                "explain_ru": "Болит горло и кашель, не живот.",
            },
            {
                "statement": "If she doesn't feel better, she should come back in three days.",
                "is_true": True,
                "explain_ru": "Если не лучше — прийти через 3 дня.",
            },
            {
                "statement": "The tablets should be taken twice a day.",
                "is_true": False,
                "explain_ru": "Таблетки — три раза в день.",
            },
        ],
    },
    "hotel": {
        "speakers": [
            {"name": "Oleg", "gender": "male", "role": "guest"},
            {"name": "Anna", "gender": "female", "role": "receptionist"},
        ],
        "turns": [
            (0, "Hello! I have a reservation under the name Oleg."),
            (1, "Good afternoon, Oleg. Yes, your room one hundred four is ready."),
            (0, "Great! Do you have breakfast at the hotel?"),
            (1, "Yes, breakfast is from seven to ten in the morning in the restaurant on the first floor."),
            (0, "Do you have Wi-Fi in the room?"),
            (1, "Yes, Wi-Fi is free. The password is at the reception desk."),
            (0, "Where can I park my car?"),
            (1, "We have a car park behind the building."),
            (0, "That's very convenient. Thanks for the information."),
            (1, "If you have questions, call support twenty-four hours a day."),
            (0, "Okay, I'll remember."),
            (1, "Enjoy your stay!"),
        ],
        "task1": [
            {
                "question": "Which room did Oleg get?",
                "options": ["102", "103", "104", "105"],
                "correct": 2,
                "explain_wrong_ru": "Номер 104.",
            },
            {
                "question": "When is breakfast served at the hotel?",
                "options": ["from 6 to 9 am", "from 7 to 10 am", "from 8 to 11 am", "from 9 to 12 am"],
                "correct": 1,
                "explain_wrong_ru": "Завтрак с 7 до 10 утра.",
            },
            {
                "question": "Where is the car park?",
                "options": ["in front of the building", "behind the building", "on the roof", "in the basement"],
                "correct": 1,
                "explain_wrong_ru": "Парковка за зданием.",
            },
        ],
        "task2": [
            {
                "statement": "Wi-Fi at the hotel is paid.",
                "is_true": False,
                "explain_ru": "Wi-Fi бесплатный.",
            },
            {
                "statement": "Oleg can call support at any time.",
                "is_true": True,
                "explain_ru": "Поддержка работает 24 часа.",
            },
            {
                "statement": "Breakfast is served in the room.",
                "is_true": False,
                "explain_ru": "Завтрак в ресторане на первом этаже.",
            },
        ],
    },
    "police": {
        "speakers": [
            {"name": "Mike", "gender": "male", "role": "victim"},
            {"name": "Steve", "gender": "male", "role": "officer"},
        ],
        "turns": [
            (0, "Officer! I want to report a theft."),
            (1, "What happened, sir?"),
            (0, "Someone stole my bicycle!"),
            (1, "Where did it happen?"),
            (0, "Near my house, about an hour ago."),
            (1, "Did you see who stole it?"),
            (0, "No, I didn't see anything."),
            (1, "We'll check the security cameras."),
            (0, "It was my only transport."),
            (1, "We'll do everything we can. What's your phone number?"),
            (0, "My number is five five five, nine zero nine zero."),
            (1, "We'll contact you if we learn anything."),
        ],
        "task1": [
            {
                "question": "What was stolen from Mike?",
                "options": ["a car", "a bicycle", "a bag", "a phone"],
                "correct": 1,
                "explain_wrong_ru": "Украли велосипед.",
            },
            {
                "question": "Where did the theft happen?",
                "options": ["near work", "near a shop", "near his house", "near the park"],
                "correct": 2,
                "explain_wrong_ru": "Возле дома.",
            },
            {
                "question": "What phone number did Mike leave?",
                "options": ["555-8080", "555-9090", "555-7070", "555-6060"],
                "correct": 1,
                "explain_wrong_ru": "Номер 555-9090.",
            },
        ],
        "task2": [
            {
                "statement": "Mike saw the thief.",
                "is_true": False,
                "explain_ru": "Майк ничего не видел.",
            },
            {
                "statement": "The police will check the cameras.",
                "is_true": True,
                "explain_ru": "Полиция проверит камеры.",
            },
            {
                "statement": "Mike said it was his only transport.",
                "is_true": True,
                "explain_ru": "Это был его единственный транспорт.",
            },
        ],
    },
    "bar": {
        "speakers": [
            {"name": "Dan", "gender": "male", "role": "bartender"},
            {"name": "Sergey", "gender": "male", "role": "customer"},
        ],
        "turns": [
            (0, "Hi! What would you like to order?"),
            (1, "Hi! A glass of beer, please."),
            (0, "What beer do you prefer? We have dark and light."),
            (1, "Light, please. And some snacks."),
            (0, "I can offer nuts or crackers."),
            (1, "Nuts, please. They always go well with beer."),
            (0, "Good choice! Everything will be ready in a minute."),
            (1, "Thanks. It's quite cosy here."),
            (0, "Yes, we often have live music."),
            (1, "That's nice. I love the atmosphere of places like this."),
            (0, "Come again. We often have interesting events."),
            (1, "I definitely will. I know where to have a good time."),
        ],
        "task1": [
            {
                "question": "What did Sergey order?",
                "options": ["whisky", "a glass of beer", "a cocktail", "water"],
                "correct": 1,
                "explain_wrong_ru": "Сергей заказал бокал пива.",
            },
            {
                "question": "What snack did he choose?",
                "options": ["crackers", "nuts", "chips", "cheese"],
                "correct": 1,
                "explain_wrong_ru": "Он выбрал орешки.",
            },
            {
                "question": "What did Dan say about the bar?",
                "options": ["there is often live music", "it's always quiet", "there's no food", "it's expensive"],
                "correct": 0,
                "explain_wrong_ru": "Часто играет живая музыка.",
            },
        ],
        "task2": [
            {
                "statement": "Sergey ordered dark beer.",
                "is_true": False,
                "explain_ru": "Он заказал светлое пиво.",
            },
            {
                "statement": "There is live music in the bar.",
                "is_true": True,
                "explain_ru": "В баре бывает живая музыка.",
            },
            {
                "statement": "Sergey was in this bar for the first time.",
                "is_true": False,
                "explain_ru": "Он знает это место — не впервые.",
            },
        ],
    },
    "taxi": {
        "speakers": [
            {"name": "Irina", "gender": "female", "role": "passenger"},
            {"name": "Victor", "gender": "male", "role": "driver"},
        ],
        "turns": [
            (0, "Victor, good afternoon! I need to go to the airport."),
            (1, "Good afternoon, Irina! Of course. Please get in."),
            (0, "How long will the journey take?"),
            (1, "Usually about thirty minutes, if there's no traffic."),
            (0, "I'm in a hurry. My flight is in two hours."),
            (1, "I'll try to go faster. Don't worry."),
            (0, "Can you stop near the entrance?"),
            (1, "Yes, I'll drive right up to the terminal."),
            (0, "That's very convenient. Thank you."),
            (1, "That's my job. Have a good trip!"),
            (0, "Thanks! Here's the payment — you can keep the change."),
            (1, "Thank you! Have a nice day!"),
        ],
        "task1": [
            {
                "question": "How long does the journey to the airport usually take?",
                "options": ["15 minutes", "20 minutes", "30 minutes", "45 minutes"],
                "correct": 2,
                "explain_wrong_ru": "Обычно около 30 минут.",
            },
            {
                "question": "Where did Irina ask to stop?",
                "options": ["near the car park", "near the entrance", "near the taxi stand", "near the hotel"],
                "correct": 1,
                "explain_wrong_ru": "Возле входа / к терминалу.",
            },
            {
                "question": "Where was Irina going?",
                "options": ["to the station", "to the airport", "to a hotel", "to a shopping centre"],
                "correct": 1,
                "explain_wrong_ru": "Ирина ехала в аэропорт.",
            },
        ],
        "task2": [
            {
                "statement": "Irina was not in a hurry.",
                "is_true": False,
                "explain_ru": "Ирина очень спешила.",
            },
            {
                "statement": "The taxi driver will drive up to the terminal.",
                "is_true": True,
                "explain_ru": "Виктор подъедет к терминалу.",
            },
            {
                "statement": "Irina left a tip.",
                "is_true": True,
                "explain_ru": "Она оставила сдачу как чаевые.",
            },
        ],
    },
    "post": {
        "speakers": [
            {"name": "Pavel", "gender": "male", "role": "customer"},
            {"name": "Maria", "gender": "female", "role": "clerk"},
        ],
        "turns": [
            (0, "Hello! I want to send a parcel."),
            (1, "Hello! Where are you sending it?"),
            (0, "To another city. It's a gift for a friend."),
            (1, "How much does your parcel weigh?"),
            (0, "About two kilograms."),
            (1, "The cost will be five hundred roubles."),
            (0, "That's fine. How long does delivery usually take?"),
            (1, "Usually it takes three to five days."),
            (0, "Okay. Can I insure the parcel?"),
            (1, "Yes, for an extra fee."),
            (0, "I agree to the insurance."),
            (1, "Then please fill in this form."),
        ],
        "task1": [
            {
                "question": "How much does Pavel's parcel weigh?",
                "options": ["1 kilogram", "2 kilograms", "3 kilograms", "4 kilograms"],
                "correct": 1,
                "explain_wrong_ru": "Посылка около 2 кг.",
            },
            {
                "question": "How many days does delivery usually take?",
                "options": ["1–2 days", "3–5 days", "7–10 days", "2 weeks"],
                "correct": 1,
                "explain_wrong_ru": "Доставка обычно 3–5 дней.",
            },
            {
                "question": "What did Pavel ask to add to the shipment?",
                "options": ["express delivery", "insurance", "gift wrapping", "a notification"],
                "correct": 1,
                "explain_wrong_ru": "Он попросил страховку.",
            },
        ],
        "task2": [
            {
                "statement": "Pavel is sending the parcel abroad.",
                "is_true": False,
                "explain_ru": "Он отправляет в другой город.",
            },
            {
                "statement": "The parcel weighs more than three kilograms.",
                "is_true": False,
                "explain_ru": "Вес около 2 кг.",
            },
            {
                "statement": "Pavel agreed to the insurance.",
                "is_true": True,
                "explain_ru": "Павел согласился на страховку.",
            },
        ],
    },
    "gym_a2": {
        "speakers": [
            {"name": "Ivan", "gender": "male", "role": "beginner"},
            {"name": "Olga", "gender": "female", "role": "trainer"},
        ],
        "turns": [
            (0, "Olga, I want to start doing sport."),
            (1, "That's a great decision! Have you trained before?"),
            (0, "No, I'm a complete beginner."),
            (1, "Then we'll start with simple exercises."),
            (0, "Which exercises do you recommend?"),
            (1, "Start with walking on the treadmill."),
            (0, "That's not hard. I can do it every day."),
            (1, "It's also important to eat well."),
            (0, "I'll try to watch my diet."),
            (1, "Come three times a week."),
            (0, "I can do that. What is your schedule?"),
            (1, "We work from eight in the morning to ten in the evening. You can start on Monday."),
        ],
        "task1": [
            {
                "question": "Which exercises did the trainer recommend?",
                "options": ["running outside", "walking on the treadmill", "swimming", "yoga"],
                "correct": 1,
                "explain_wrong_ru": "Ходьба на беговой дорожке.",
            },
            {
                "question": "How often does the trainer suggest coming?",
                "options": ["once a week", "twice a week", "three times a week", "every day"],
                "correct": 2,
                "explain_wrong_ru": "Три раза в неделю.",
            },
            {
                "question": "Which day does Ivan plan to start?",
                "options": ["Monday", "Tuesday", "Wednesday", "Thursday"],
                "correct": 0,
                "explain_wrong_ru": "Иван начнёт с понедельника.",
            },
        ],
        "task2": [
            {
                "statement": "Ivan has trained before.",
                "is_true": False,
                "explain_ru": "Иван полный новичок.",
            },
            {
                "statement": "The trainer said it's important to eat well.",
                "is_true": True,
                "explain_ru": "Важно правильно питаться.",
            },
            {
                "statement": "The gym is open only in the mornings.",
                "is_true": False,
                "explain_ru": "Работают с 8 утра до 10 вечера.",
            },
        ],
    },
    "weather_plans": {
        "speakers": [
            {"name": "Kristina", "gender": "female", "role": "Kristina"},
            {"name": "Denis", "gender": "male", "role": "Denis"},
        ],
        "turns": [
            (0, "Denis, did you see the weather forecast for tomorrow?"),
            (1, "Yes, they promise rain and wind."),
            (0, "What a pity. I wanted to go on a picnic."),
            (1, "Maybe we can move it to Saturday?"),
            (0, "On Saturday it will be sunny. That's a good idea."),
            (1, "We can take food and drinks with us."),
            (0, "And of course a good mood."),
            (1, "I hope the rain won't spoil our plans."),
            (0, "I don't like rain, but sometimes it's nice."),
            (1, "The main thing is that we're together."),
            (0, "You're right. That's the most important thing."),
            (1, "Then see you on Saturday at ten in the morning!"),
        ],
        "task1": [
            {
                "question": "What is the weather forecast for tomorrow?",
                "options": ["sunny", "rain", "snow", "fog"],
                "correct": 1,
                "explain_wrong_ru": "Завтра дождь и ветер.",
            },
            {
                "question": "Which day did they move the picnic to?",
                "options": ["Friday", "Saturday", "Sunday", "Monday"],
                "correct": 1,
                "explain_wrong_ru": "Пикник перенесли на субботу.",
            },
            {
                "question": "What time did they agree to meet?",
                "options": ["9 am", "10 am", "11 am", "12 am"],
                "correct": 1,
                "explain_wrong_ru": "Встреча в 10 утра.",
            },
        ],
        "task2": [
            {
                "statement": "Denis wants to go on a picnic in any weather.",
                "is_true": False,
                "explain_ru": "Денис предложил перенести из‑за дождя.",
            },
            {
                "statement": "Kristina does not like rain.",
                "is_true": True,
                "explain_ru": "Кристина не любит дождь.",
            },
            {
                "statement": "The picnic will be on Sunday.",
                "is_true": False,
                "explain_ru": "Пикник в субботу, не в воскресенье.",
            },
        ],
    },
}


def has_a2_fixed(topic_id: str) -> bool:
    return str(topic_id or "") in A2_FIXED


def get_a2_fixed(topic_id: str) -> dict | None:
    return A2_FIXED.get(str(topic_id or ""))
