"""
Фиксированный контент Listening B1: диалоги + Task1/Task2.
Task3 (порядок реплик) строится из turns как обычно.
"""

from __future__ import annotations

B1_FIXED: dict[str, dict] = {
    "job_interview": {
        "speakers": [
            {"name": "Mikhail", "gender": "male", "role": "HR manager"},
            {"name": "Anna", "gender": "female", "role": "applicant"},
        ],
        "turns": [
            (0, "Good afternoon, Anna. Tell me a little about yourself."),
            (1, "Hello, Mikhail. I graduated from university with a degree in Marketing."),
            (0, "Do you have work experience in this field?"),
            (1, "Yes, I worked in a small company for two years."),
            (0, "Why did you decide to change jobs?"),
            (1, "I'd like to grow in a larger company."),
            (0, "That makes sense. What are your strengths?"),
            (1, "I can work in a team and I learn quickly."),
            (0, "That's important for our company."),
            (1, "Also, I speak English quite well."),
            (0, "That's an excellent bonus! We'll contact you within a week."),
            (1, "Thank you. I'll be waiting for your call."),
        ],
        "task1": [
            {
                "question": "What is Anna's speciality?",
                "options": ["Finance", "Marketing", "IT", "Law"],
                "correct": 1,
                "explain_wrong_ru": "Специальность Анны — маркетинг.",
            },
            {
                "question": "How many years did she work at the previous company?",
                "options": ["one year", "two years", "three years", "four years"],
                "correct": 1,
                "explain_wrong_ru": "Она работала два года.",
            },
            {
                "question": "What extra bonus did Anna mention?",
                "options": ["a driving licence", "English", "programming skills", "sales experience"],
                "correct": 1,
                "explain_wrong_ru": "Она хорошо владеет английским.",
            },
        ],
        "task2": [
            {
                "statement": "Anna is looking for a job in a small company.",
                "is_true": False,
                "explain_ru": "Она хочет расти в более крупной компании.",
            },
            {
                "statement": "She thinks she works well in a team.",
                "is_true": True,
                "explain_ru": "Она умеет работать в команде.",
            },
            {
                "statement": "Mikhail said he would contact her in two weeks.",
                "is_true": False,
                "explain_ru": "Он свяжется в течение недели.",
            },
        ],
    },
    "travel_plans": {
        "speakers": [
            {"name": "Igor", "gender": "male", "role": "Igor"},
            {"name": "Marina", "gender": "female", "role": "Marina"},
        ],
        "turns": [
            (0, "Marina, have we started planning the summer holiday yet?"),
            (1, "Not yet. But I think we should go to the seaside."),
            (0, "I agree. I've wanted a beach holiday for a long time."),
            (1, "I've already looked at tickets and hotels."),
            (0, "And what about the prices?"),
            (1, "Everything is quite expensive, but we can save money."),
            (0, "How?"),
            (1, "If we don't fly in peak season, tickets are cheaper."),
            (0, "That sounds reasonable. I don't mind flying at the end of August."),
            (1, "Great. Then I'll look for a hotel."),
            (0, "And I'll look at excursions."),
            (1, "Deal. I hope the holiday works out."),
        ],
        "task1": [
            {
                "question": "What are they planning for the summer?",
                "options": ["a trip to the mountains", "a seaside holiday", "a city trip", "camping"],
                "correct": 1,
                "explain_wrong_ru": "Они планируют отдых на море.",
            },
            {
                "question": "What can save money on the trip?",
                "options": ["flying in peak season", "flying not in peak season", "a more expensive hotel", "excursions"],
                "correct": 1,
                "explain_wrong_ru": "Вылет не в пик сезона дешевле.",
            },
            {
                "question": "Who will look for a hotel?",
                "options": ["Igor", "Marina", "both", "nobody"],
                "correct": 1,
                "explain_wrong_ru": "Отелем займётся Марина.",
            },
        ],
        "task2": [
            {
                "statement": "Igor does not want to go to the seaside.",
                "is_true": False,
                "explain_ru": "Игорь давно мечтает о море.",
            },
            {
                "statement": "Igor doesn't mind flying in August.",
                "is_true": True,
                "explain_ru": "Он не против вылететь в конце августа.",
            },
            {
                "statement": "The excursions will be cheap.",
                "is_true": False,
                "explain_ru": "О цене экскурсий не говорят.",
            },
        ],
    },
    "flatmates": {
        "speakers": [
            {"name": "Dmitry", "gender": "male", "role": "Dmitry"},
            {"name": "Olga", "gender": "female", "role": "Olga"},
        ],
        "turns": [
            (0, "Olga, do you know we have new neighbours?"),
            (1, "Yes, I saw them yesterday. They seem like nice people."),
            (0, "I hope they won't make noise at night."),
            (1, "Anyway, we can get to know them."),
            (0, "I don't mind. But first we should just say hello."),
            (1, "I agree. I think they'll be happy to meet us."),
            (0, "The main thing is that they respect the shared rules."),
            (1, "That would be ideal."),
            (0, "I hope we'll get along."),
            (1, "Me too. Good neighbours are a rarity."),
            (0, "As for me, I always try to be polite."),
            (1, "That's the right approach."),
        ],
        "task1": [
            {
                "question": "What does Dmitry hope about the new neighbours?",
                "options": ["that they are rich", "that they won't make noise", "that they cook", "that they work"],
                "correct": 1,
                "explain_wrong_ru": "Он надеется, что не будут шуметь.",
            },
            {
                "question": "What does Olga think about the new neighbours?",
                "options": ["they seem nice", "they look suspicious", "they are strange", "they are noisy"],
                "correct": 0,
                "explain_wrong_ru": "Они кажутся приятными.",
            },
            {
                "question": "What does Olga say about good neighbours?",
                "options": ["they are rare", "they are always there", "they are easy to find", "they are not important"],
                "correct": 0,
                "explain_wrong_ru": "Хорошие соседи — большая редкость.",
            },
        ],
        "task2": [
            {
                "statement": "Olga has already talked to the new neighbours.",
                "is_true": False,
                "explain_ru": "Она только видела их вчера.",
            },
            {
                "statement": "Dmitry doesn't mind getting to know them.",
                "is_true": True,
                "explain_ru": "Дмитрий не против познакомиться.",
            },
            {
                "statement": "Dmitry thinks they should invite them over right away.",
                "is_true": False,
                "explain_ru": "Сначала просто поздороваться.",
            },
        ],
    },
    "restaurant": {
        "speakers": [
            {"name": "Andrey", "gender": "male", "role": "Andrey"},
            {"name": "Ekaterina", "gender": "female", "role": "Ekaterina"},
        ],
        "turns": [
            (0, "Ekaterina, have you ever been to this restaurant?"),
            (1, "No, but I've heard a lot of good things about it."),
            (0, "Me too. People say the food here is excellent."),
            (1, "Let's order something unusual."),
            (0, "I'd suggest trying the signature dish."),
            (1, "I agree. That's always interesting."),
            (0, "The atmosphere here is very pleasant."),
            (1, "Yes, and the service is high quality."),
            (0, "I can't disagree."),
            (1, "I hope the food will be just as good. As for the bill, I can split it with you."),
            (0, "No need. I'm treating you."),
            (1, "Thank you, Andrey."),
        ],
        "task1": [
            {
                "question": "What has Ekaterina heard about this restaurant?",
                "options": ["that it's expensive", "that the food is excellent", "that it's boring", "that portions are small"],
                "correct": 1,
                "explain_wrong_ru": "Говорят, здесь отличная кухня.",
            },
            {
                "question": "What did they decide to order?",
                "options": ["a salad", "the signature dish", "soup", "dessert"],
                "correct": 1,
                "explain_wrong_ru": "Они закажут фирменное блюдо.",
            },
            {
                "question": "What did Andrey offer about the bill?",
                "options": ["to split it", "to treat her", "to ask for a discount", "to pay by card"],
                "correct": 1,
                "explain_wrong_ru": "Андрей угощает.",
            },
        ],
        "task2": [
            {
                "statement": "Ekaterina has already been to this restaurant.",
                "is_true": False,
                "explain_ru": "Она здесь ещё не была.",
            },
            {
                "statement": "Andrey thinks the atmosphere is pleasant.",
                "is_true": True,
                "explain_ru": "Атмосфера приятная.",
            },
            {
                "statement": "Andrey offered to split the bill.",
                "is_true": False,
                "explain_ru": "Он угощает, не делит счёт.",
            },
        ],
    },
    "bank": {
        "speakers": [
            {"name": "Pavel", "gender": "male", "role": "customer"},
            {"name": "Natalia", "gender": "female", "role": "clerk"},
        ],
        "turns": [
            (0, "Hello, I'd like to open an account at your bank."),
            (1, "Good afternoon. Do you have your documents with you?"),
            (0, "Yes, my passport and social insurance card."),
            (1, "Excellent. What type of account are you interested in?"),
            (0, "I'd like to open a savings account."),
            (1, "The interest rate on it is quite good."),
            (0, "That's what I need. I plan to save money."),
            (1, "You can top up the account at any time."),
            (0, "Are there any limits on withdrawals?"),
            (1, "No, you can withdraw money at any moment."),
            (0, "That's very convenient. Thanks for your help."),
            (1, "You're welcome. If you have questions, just ask."),
        ],
        "task1": [
            {
                "question": "What account does Pavel want to open?",
                "options": ["a credit account", "a savings account", "an investment account", "a current account"],
                "correct": 1,
                "explain_wrong_ru": "Накопительный счёт.",
            },
            {
                "question": "Which documents did he provide?",
                "options": ["only a passport", "a passport and a social insurance card", "a driving licence", "a tax ID"],
                "correct": 1,
                "explain_wrong_ru": "Паспорт и карта соцстрахования.",
            },
            {
                "question": "What does Pavel plan to do with the money?",
                "options": ["spend it", "save it", "invest it", "transfer it"],
                "correct": 1,
                "explain_wrong_ru": "Он планирует откладывать деньги.",
            },
        ],
        "task2": [
            {
                "statement": "The savings account has a low interest rate.",
                "is_true": False,
                "explain_ru": "Ставка довольно выгодная.",
            },
            {
                "statement": "Pavel can withdraw money at any time.",
                "is_true": True,
                "explain_ru": "Снимать можно в любой момент.",
            },
            {
                "statement": "Pavel did not bring his passport.",
                "is_true": False,
                "explain_ru": "Паспорт у него с собой.",
            },
        ],
    },
    "landlord_b1": {
        "speakers": [
            {"name": "Ksenia", "gender": "female", "role": "tenant"},
            {"name": "Sergey", "gender": "male", "role": "landlord"},
        ],
        "turns": [
            (0, "Hello, I'd like to look at the flat."),
            (1, "Good afternoon. Come in, I'll show you everything."),
            (0, "The flat looks spacious and bright."),
            (1, "Yes, there's a good renovation and new furniture."),
            (0, "What is the monthly rent?"),
            (1, "Thirty thousand roubles. That doesn't include utilities."),
            (0, "That's acceptable. Is there parking nearby?"),
            (1, "Yes, there's free parking in the courtyard."),
            (0, "I need a couple of days to think."),
            (1, "Of course. I'm ready to wait until the end of the week."),
            (0, "Okay, I'll let you know about my decision."),
            (1, "I'll be waiting for your call."),
        ],
        "task1": [
            {
                "question": "How much is the monthly rent?",
                "options": ["20,000 roubles", "30,000 roubles", "40,000 roubles", "50,000 roubles"],
                "correct": 1,
                "explain_wrong_ru": "Аренда 30 тысяч рублей.",
            },
            {
                "question": "What is included in the rent?",
                "options": ["utilities", "only the rent", "internet", "parking"],
                "correct": 1,
                "explain_wrong_ru": "Коммунальные не включены — только аренда.",
            },
            {
                "question": "How much time did Ksenia ask to think?",
                "options": ["one day", "a couple of days", "a week", "a month"],
                "correct": 1,
                "explain_wrong_ru": "Пара дней на раздумья.",
            },
        ],
        "task2": [
            {
                "statement": "The flat looks dark.",
                "is_true": False,
                "explain_ru": "Квартира просторная и светлая.",
            },
            {
                "statement": "Parking in the courtyard is paid.",
                "is_true": False,
                "explain_ru": "Парковка бесплатная.",
            },
            {
                "statement": "Sergey is ready to wait until the end of the week.",
                "is_true": True,
                "explain_ru": "Он готов ждать до конца недели.",
            },
        ],
    },
    "airport_b1": {
        "speakers": [
            {"name": "Irina", "gender": "female", "role": "passenger"},
            {"name": "Artem", "gender": "male", "role": "airport staff"},
        ],
        "turns": [
            (0, "Excuse me, I can't find the boarding gate."),
            (1, "What is your flight number?"),
            (0, "Flight four five six to London."),
            (1, "That's terminal three. Go straight, then left."),
            (0, "I have little time left before departure."),
            (1, "Don't worry, you still have twenty minutes."),
            (0, "Okay. As for my luggage, I've already checked it in."),
            (1, "Then you only need to go through security."),
            (0, "Are there any limits on hand luggage?"),
            (1, "Hand luggage should not exceed ten kilograms."),
            (0, "Perfect. Thanks for your help."),
            (1, "Have a good flight and a pleasant journey."),
        ],
        "task1": [
            {
                "question": "What is Irina's flight number?",
                "options": ["456", "789", "123", "321"],
                "correct": 0,
                "explain_wrong_ru": "Рейс 456.",
            },
            {
                "question": "Which terminal does she need?",
                "options": ["terminal one", "terminal two", "terminal three", "terminal four"],
                "correct": 2,
                "explain_wrong_ru": "Третий терминал.",
            },
            {
                "question": "How much time is left before departure?",
                "options": ["10 minutes", "15 minutes", "20 minutes", "30 minutes"],
                "correct": 2,
                "explain_wrong_ru": "Осталось 20 минут.",
            },
        ],
        "task2": [
            {
                "statement": "Irina has already checked in her luggage.",
                "is_true": True,
                "explain_ru": "Багаж уже сдан.",
            },
            {
                "statement": "Hand luggage can weigh up to fifteen kilograms.",
                "is_true": False,
                "explain_ru": "Лимит — 10 килограммов.",
            },
            {
                "statement": "Irina is flying to Paris.",
                "is_true": False,
                "explain_ru": "Она летит в Лондон.",
            },
        ],
    },
    "salon": {
        "speakers": [
            {"name": "Kristina", "gender": "female", "role": "client"},
            {"name": "Elena", "gender": "female", "role": "stylist"},
        ],
        "turns": [
            (0, "I'd like to change my hair colour."),
            (1, "Which colours do you prefer?"),
            (0, "I'd like to try warm shades."),
            (1, "Then I can offer chestnut or honey."),
            (0, "Honey sounds interesting."),
            (1, "It will look beautiful on you."),
            (0, "How long will the procedure take?"),
            (1, "Usually about an hour and a half."),
            (0, "That's rather long. But I'm ready to wait."),
            (1, "We can do it on Wednesday in the morning."),
            (0, "That works for me. Let's book Wednesday."),
            (1, "Deal. I'll write you down."),
        ],
        "task1": [
            {
                "question": "Which hair colour did Kristina choose?",
                "options": ["chestnut", "honey", "ash", "red"],
                "correct": 1,
                "explain_wrong_ru": "Она выбрала медовый.",
            },
            {
                "question": "How long does the procedure usually take?",
                "options": ["about 30 minutes", "about 1 hour", "about 1.5 hours", "about 2 hours"],
                "correct": 2,
                "explain_wrong_ru": "Около полутора часов.",
            },
            {
                "question": "Which day did they book?",
                "options": ["Tuesday", "Wednesday", "Thursday", "Friday"],
                "correct": 1,
                "explain_wrong_ru": "Запись на среду.",
            },
        ],
        "task2": [
            {
                "statement": "Kristina wanted a radical colour change.",
                "is_true": False,
                "explain_ru": "Она хотела тёплые оттенки, не радикальную смену.",
            },
            {
                "statement": "The procedure will take about an hour.",
                "is_true": False,
                "explain_ru": "Около полутора часов.",
            },
            {
                "statement": "They agreed on Wednesday.",
                "is_true": True,
                "explain_ru": "Договорились на среду.",
            },
        ],
    },
    "news_chat": {
        "speakers": [
            {"name": "Sergey", "gender": "male", "role": "Sergey"},
            {"name": "Tatiana", "gender": "female", "role": "Tatiana"},
        ],
        "turns": [
            (0, "Have you heard the news about the new metro station?"),
            (1, "Yes, I read about it yesterday."),
            (0, "They say it will be very modern."),
            (1, "And that's a great solution for the city."),
            (0, "I agree. It should improve the transport situation."),
            (1, "When is the opening planned?"),
            (0, "According to the news, next year."),
            (1, "That's good news."),
            (0, "And the construction won't cost the city too much."),
            (1, "That's good. It's important that money is spent wisely."),
            (0, "I hope everything will be done well."),
            (1, "Me too."),
        ],
        "task1": [
            {
                "question": "What are they discussing?",
                "options": ["a new park", "a new metro station", "a new bridge", "a new shopping centre"],
                "correct": 1,
                "explain_wrong_ru": "Новую станцию метро.",
            },
            {
                "question": "When is the opening planned?",
                "options": ["this year", "next year", "in two years", "in three years"],
                "correct": 1,
                "explain_wrong_ru": "Открытие в следующем году.",
            },
            {
                "question": "How does Sergey assess the construction cost?",
                "options": ["very high", "not too expensive", "minimal", "unknown"],
                "correct": 1,
                "explain_wrong_ru": "Не слишком дорого для города.",
            },
        ],
        "task2": [
            {
                "statement": "Tatiana had not heard about the new station.",
                "is_true": False,
                "explain_ru": "Она читала об этом вчера.",
            },
            {
                "statement": "The new station will be modern.",
                "is_true": True,
                "explain_ru": "Станция будет современной.",
            },
            {
                "statement": "The opening is planned for next year.",
                "is_true": True,
                "explain_ru": "Открытие — в следующем году.",
            },
        ],
    },
    "volunteer": {
        "speakers": [
            {"name": "Alexey", "gender": "male", "role": "volunteer"},
            {"name": "Nadezhda", "gender": "female", "role": "organiser"},
        ],
        "turns": [
            (0, "Hello, I'd like to become a volunteer."),
            (1, "Good afternoon! Do you have volunteering experience?"),
            (0, "I took part in a couple of park clean-up events."),
            (1, "That's great experience! What are you interested in?"),
            (0, "I'm interested in working with children."),
            (1, "We have a project teaching schoolchildren basic IT."),
            (0, "That sounds great. I have skills in that area."),
            (1, "We'll be happy to see you on our team."),
            (0, "When does volunteer training start?"),
            (1, "Tomorrow at six p.m. in the city centre."),
            (0, "I'll definitely come."),
            (1, "Thanks for your interest. See you tomorrow."),
        ],
        "task1": [
            {
                "question": "What skills does Alexey have?",
                "options": ["IT skills", "construction skills", "medical skills", "design skills"],
                "correct": 0,
                "explain_wrong_ru": "У него навыки в IT.",
            },
            {
                "question": "Where will the volunteer training take place?",
                "options": ["in the city centre", "at a school", "at a university", "in a park"],
                "correct": 0,
                "explain_wrong_ru": "В городском центре.",
            },
            {
                "question": "Which project does he want to join?",
                "options": ["park clean-up", "working with children", "helping animals", "construction"],
                "correct": 1,
                "explain_wrong_ru": "Ему интересна работа с детьми.",
            },
        ],
        "task2": [
            {
                "statement": "Nadezhda would like to see Alexey on the team.",
                "is_true": True,
                "explain_ru": "Она рада видеть его в команде.",
            },
            {
                "statement": "Tomorrow's training starts at 7 p.m.",
                "is_true": False,
                "explain_ru": "Обучение в 18:00, не в 19:00.",
            },
            {
                "statement": "The training will take place at a school.",
                "is_true": False,
                "explain_ru": "В городском центре, не в школе.",
            },
        ],
    },
}


def has_b1_fixed(topic_id: str) -> bool:
    return str(topic_id or "") in B1_FIXED


def get_b1_fixed(topic_id: str) -> dict | None:
    return B1_FIXED.get(str(topic_id or ""))
