"""
Фиксированный контент Listening B2: диалоги + Task1/Task2.
Task3 (порядок реплик) строится из turns как обычно.
"""

from __future__ import annotations

B2_FIXED: dict[str, dict] = {
    "workplace": {
        "speakers": [
            {"name": "Anton", "gender": "male", "role": "Anton"},
            {"name": "Elena", "gender": "female", "role": "Elena"},
        ],
        "turns": [
            (0, "Lena, could you take a look at this report?"),
            (1, "Sure, I'll look now. What exactly worries you?"),
            (0, "I just can't balance the debit and credit. The numbers don't match."),
            (1, "It looks like you made a mistake in last month's calculations."),
            (0, "Damn, I knew it. I'll have to redo it."),
            (1, "Don't worry. If needed, I'll help you figure it out."),
            (0, "Thanks, you're saving me. Shall we grab coffee after work?"),
            (1, "Great idea. I could use a break right now."),
            (0, "I'm treating. As usual, do you prefer cappuccino?"),
            (1, "Yes, but this time I want to try something new."),
            (0, "Then let's get caramel lattes."),
            (1, "Sounds tempting. Let's go!"),
        ],
        "task1": [
            {
                "question": "What can't Anton do with the report?",
                "options": ["find the mistakes", "balance debit and credit", "send it to the boss", "sign it"],
                "correct": 1,
                "explain_wrong_ru": "Он не может свести дебет с кредитом.",
            },
            {
                "question": "What drink does Elena usually prefer?",
                "options": ["latte", "cappuccino", "tea", "americano"],
                "correct": 1,
                "explain_wrong_ru": "Обычно она предпочитает капучино.",
            },
            {
                "question": "What are they going to do after work?",
                "options": ["go to a bar", "get coffee", "go home", "go to the gym"],
                "correct": 1,
                "explain_wrong_ru": "Они идут за кофе.",
            },
        ],
        "task2": [
            {
                "statement": "Anton made a mistake in the calculations.",
                "is_true": True,
                "explain_ru": "Он ошибся в расчётах за прошлый месяц.",
            },
            {
                "statement": "Elena flatly refused to help.",
                "is_true": False,
                "explain_ru": "Елена предложила помочь.",
            },
            {
                "statement": "Anton is treating Elena to coffee.",
                "is_true": True,
                "explain_ru": "Антон угощает.",
            },
        ],
    },
    "university": {
        "speakers": [
            {"name": "Mikhail", "gender": "male", "role": "Mikhail"},
            {"name": "Anastasia", "gender": "female", "role": "Anastasia"},
        ],
        "turns": [
            (0, "Hi, Anastasia! Have you chosen a topic for your thesis yet?"),
            (1, "Not yet. I just can't decide."),
            (0, "I'd advise you to choose something more practical."),
            (1, "What do you mean?"),
            (0, "Something connected to your future profession, for example."),
            (1, "That makes sense. I'll think about it."),
            (0, "Do you have a deadline?"),
            (1, "My supervisor said I need to decide by the end of the month."),
            (0, "You still have time. Don't rush."),
            (1, "You're right. The main thing is not to leave it to the last moment."),
            (0, "If you need help — just ask."),
            (1, "Thanks, I appreciate that. I hope everything works out."),
        ],
        "task1": [
            {
                "question": "What kind of thesis topic did Mikhail suggest?",
                "options": ["theoretical", "practical", "historical", "abstract"],
                "correct": 1,
                "explain_wrong_ru": "Он посоветовал что-то практичное.",
            },
            {
                "question": "When does she need to decide on the topic?",
                "options": ["next week", "by the end of the month", "in two months", "tomorrow"],
                "correct": 1,
                "explain_wrong_ru": "К концу месяца.",
            },
            {
                "question": "What did Mikhail offer Anastasia at the end?",
                "options": ["to write the thesis for her", "to ask him for help", "to take academic leave", "to change the topic"],
                "correct": 1,
                "explain_wrong_ru": "Он предложил обращаться за помощью.",
            },
        ],
        "task2": [
            {
                "statement": "Anastasia has already chosen a topic.",
                "is_true": False,
                "explain_ru": "Она ещё не определилась.",
            },
            {
                "statement": "Mikhail advises leaving everything to the last moment.",
                "is_true": False,
                "explain_ru": "Главное — не откладывать на последний момент.",
            },
            {
                "statement": "Mikhail is ready to help Anastasia.",
                "is_true": True,
                "explain_ru": "Он готов помочь.",
            },
        ],
    },
    "customer": {
        "speakers": [
            {"name": "Victor", "gender": "male", "role": "customer"},
            {"name": "Oksana", "gender": "female", "role": "operator"},
        ],
        "turns": [
            (0, "Hello, I have a problem with my internet connection."),
            (1, "Good afternoon! What exactly is happening?"),
            (0, "The speed has dropped to a ridiculous level."),
            (1, "I understand your frustration. Let's check."),
            (0, "I restarted the router — that didn't help."),
            (1, "We can check the connection remotely."),
            (0, "Let's try."),
            (1, "I can see the problem is with your equipment."),
            (0, "So do I need to replace the router?"),
            (1, "Not necessarily. We can send a technician to you."),
            (0, "When can he come?"),
            (1, "Tomorrow in the morning. We'll contact you to confirm."),
        ],
        "task1": [
            {
                "question": "What problem did Victor face?",
                "options": ["the lights went out", "the internet speed dropped", "the TV doesn't work", "the phone broke"],
                "correct": 1,
                "explain_wrong_ru": "Упала скорость интернета.",
            },
            {
                "question": "What has Victor already done?",
                "options": ["restarted the router", "replaced the cable", "called another service", "nothing"],
                "correct": 0,
                "explain_wrong_ru": "Он перезагружал роутер.",
            },
            {
                "question": "When is the technician's visit planned?",
                "options": ["tomorrow morning", "the day after tomorrow", "in a week", "tomorrow evening"],
                "correct": 0,
                "explain_wrong_ru": "Завтра в первой половине дня.",
            },
        ],
        "task2": [
            {
                "statement": "The problem is related to the equipment.",
                "is_true": True,
                "explain_ru": "Проблема в оборудовании.",
            },
            {
                "statement": "Oksana offered to replace the router immediately.",
                "is_true": False,
                "explain_ru": "Она сказала «не факт» и предложила техника.",
            },
            {
                "statement": "The technician will come tomorrow in the afternoon.",
                "is_true": False,
                "explain_ru": "Приедет завтра утром / в первой половине дня.",
            },
        ],
    },
    "airport": {
        "speakers": [
            {"name": "Alex", "gender": "male", "role": "passenger"},
            {"name": "Flight attendant", "gender": "female", "role": "flight attendant"},
        ],
        "turns": [
            (0, "Excuse me, I can't find the boarding gate."),
            (1, "What is your flight number?"),
            (0, "Flight two two four to Berlin."),
            (1, "You need to go to terminal C."),
            (0, "Is that far from here?"),
            (1, "No, go through the duty-free zone and turn left."),
            (0, "I did that, but I got lost."),
            (1, "Let me walk you to the gate."),
            (0, "That would be very kind of you."),
            (1, "It's no problem for me."),
            (0, "I only have fifteen minutes left before departure."),
            (1, "We'll make it. Don't worry. Have a good flight!"),
        ],
        "task1": [
            {
                "question": "Where is Alex going?",
                "options": ["to London", "to Berlin", "to Paris", "to Rome"],
                "correct": 1,
                "explain_wrong_ru": "Он летит в Берлин.",
            },
            {
                "question": "What happened to Alex?",
                "options": ["he missed the flight", "he got lost", "he lost his luggage", "he forgot his passport"],
                "correct": 1,
                "explain_wrong_ru": "Он заблудился.",
            },
            {
                "question": "How much time is left before departure?",
                "options": ["5 minutes", "10 minutes", "15 minutes", "30 minutes"],
                "correct": 2,
                "explain_wrong_ru": "Осталось 15 минут.",
            },
        ],
        "task2": [
            {
                "statement": "Terminal C is far from the duty-free zone.",
                "is_true": False,
                "explain_ru": "Нужно пройти через дьюти-фри — это недалеко.",
            },
            {
                "statement": "The flight attendant refused to help.",
                "is_true": False,
                "explain_ru": "Она проводит его до выхода.",
            },
            {
                "statement": "Alex lost his ticket.",
                "is_true": False,
                "explain_ru": "Он заблудился, билет не терял.",
            },
        ],
    },
    "dating": {
        "speakers": [
            {"name": "Denis", "gender": "male", "role": "Denis"},
            {"name": "Veronica", "gender": "female", "role": "Veronica"},
        ],
        "turns": [
            (0, "Hi, Veronica! You look amazing today."),
            (1, "Thanks, Denis! I'm glad to see you."),
            (0, "I chose a restaurant with a view of the river. I hope you'll like it."),
            (1, "That sounds very romantic."),
            (0, "I'd like to get to know you better."),
            (1, "Me too. Tell me, what are your hobbies?"),
            (0, "I love travelling and trying new cuisine."),
            (1, "That's great! And in my free time I do yoga."),
            (0, "Yoga is a great way to relax."),
            (1, "I agree. It helps me stay in shape."),
            (0, "I hope this evening will be the start of something good."),
            (1, "I hope so too."),
        ],
        "task1": [
            {
                "question": "What did Denis choose for the date?",
                "options": ["a restaurant with a river view", "a walk in the park", "a cinema", "a concert"],
                "correct": 0,
                "explain_wrong_ru": "Ресторан с видом на реку.",
            },
            {
                "question": "What does Veronica do in her free time?",
                "options": ["travelling", "yoga", "cooking", "dancing"],
                "correct": 1,
                "explain_wrong_ru": "Она ходит на йогу.",
            },
            {
                "question": "What is Denis's hobby?",
                "options": ["fishing", "travelling and food", "music", "sport"],
                "correct": 1,
                "explain_wrong_ru": "Путешествия и новая кухня.",
            },
        ],
        "task2": [
            {
                "statement": "Veronica was unhappy with the restaurant choice.",
                "is_true": False,
                "explain_ru": "Она назвала выбор романтичным.",
            },
            {
                "statement": "Denis doesn't know what Veronica is into.",
                "is_true": False,
                "explain_ru": "Она рассказала про йогу.",
            },
            {
                "statement": "Veronica thinks yoga helps her stay in shape.",
                "is_true": True,
                "explain_ru": "Йога помогает ей оставаться в форме.",
            },
        ],
    },
    "court_soft": {
        "speakers": [
            {"name": "Igor", "gender": "male", "role": "client"},
            {"name": "Ekaterina", "gender": "female", "role": "lawyer"},
        ],
        "turns": [
            (0, "Hello, I'd like advice on an employment contract."),
            (1, "Good afternoon. What exactly interests you?"),
            (0, "I'm worried about the clause on overtime pay."),
            (1, "I've carefully studied your contract."),
            (0, "And what are your comments?"),
            (1, "This clause is not drafted quite correctly."),
            (0, "What do you mean?"),
            (1, "It doesn't state clear criteria for the calculation."),
            (0, "Is that bad for me?"),
            (1, "Most likely yes. I'd advise you to review the terms."),
            (0, "Thanks. I'll sort this out with my employer."),
            (1, "If you need more help, get in touch."),
        ],
        "task1": [
            {
                "question": "What does Igor want to discuss with the lawyer?",
                "options": ["the overtime clause", "salary size", "holiday leave", "dismissal"],
                "correct": 0,
                "explain_wrong_ru": "Пункт о сверхурочных.",
            },
            {
                "question": "What did Ekaterina say about the clause?",
                "options": ["it's drafted correctly", "it's drafted incorrectly", "it's not important", "it should be deleted"],
                "correct": 1,
                "explain_wrong_ru": "Пункт составлен некорректно.",
            },
            {
                "question": "What did Ekaterina advise Igor?",
                "options": ["to sign the contract", "to review the terms", "to quit", "to ignore it"],
                "correct": 1,
                "explain_wrong_ru": "Пересмотреть условия.",
            },
        ],
        "task2": [
            {
                "statement": "Igor asked for advice on family law.",
                "is_true": False,
                "explain_ru": "Консультация по трудовому договору.",
            },
            {
                "statement": "The contract has no clear criteria for calculating overtime.",
                "is_true": True,
                "explain_ru": "Нет чётких критериев расчёта.",
            },
            {
                "statement": "Ekaterina refused to help further.",
                "is_true": False,
                "explain_ru": "Она предложила обращаться снова.",
            },
        ],
    },
    "podcast_b2": {
        "speakers": [
            {"name": "Dmitry", "gender": "male", "role": "host"},
            {"name": "Anna", "gender": "female", "role": "guest"},
        ],
        "turns": [
            (0, "Anna, tell us how you came up with the idea to start your business."),
            (1, "It all started when I couldn't find a quality service."),
            (0, "And you decided to create it yourself?"),
            (1, "Exactly. I realised that if not me, then who?"),
            (0, "That's a bold decision. What was the first step?"),
            (1, "I did serious market research."),
            (0, "How long did the preparation take?"),
            (1, "About six months. That was the hardest stage."),
            (0, "What was the most difficult part?"),
            (1, "Finding a team of like-minded people."),
            (0, "But you managed. What would you advise people who want to start?"),
            (1, "Don't be afraid of mistakes and take action. I don't regret the time spent."),
        ],
        "task1": [
            {
                "question": "What made Anna start a business?",
                "options": ["lack of money", "no quality service", "wanting to be famous", "friends' example"],
                "correct": 1,
                "explain_wrong_ru": "Не могла найти качественный сервис.",
            },
            {
                "question": "How long did the preparation take?",
                "options": ["three months", "six months", "a year", "two years"],
                "correct": 1,
                "explain_wrong_ru": "Около полугода.",
            },
            {
                "question": "What does Anna find hardest at the start?",
                "options": ["raising money", "finding a team", "marketing", "company registration"],
                "correct": 1,
                "explain_wrong_ru": "Найти команду единомышленников.",
            },
        ],
        "task2": [
            {
                "statement": "Anna started the business with no preparation.",
                "is_true": False,
                "explain_ru": "Подготовка заняла около полугода.",
            },
            {
                "statement": "Anna thinks mistakes are part of the journey.",
                "is_true": True,
                "explain_ru": "Она советует не бояться ошибок.",
            },
            {
                "statement": "Dmitry doesn't believe Anna can succeed.",
                "is_true": False,
                "explain_ru": "Он отмечает, что у неё получилось.",
            },
        ],
    },
    "hospital": {
        "speakers": [
            {"name": "Pavel", "gender": "male", "role": "patient"},
            {"name": "Maria", "gender": "female", "role": "doctor"},
        ],
        "turns": [
            (0, "Doctor, I feel constant tiredness."),
            (1, "How long has this been going on?"),
            (0, "About a month."),
            (1, "Have you had any tests recently?"),
            (0, "No, I didn't have time."),
            (1, "I'd recommend a full check-up."),
            (0, "Will that take a lot of time?"),
            (1, "About a day. We'll take all the necessary tests."),
            (0, "Can I do it next week?"),
            (1, "Yes, book an appointment at reception."),
            (0, "Do I need to change anything in my lifestyle?"),
            (1, "I'd advise you to rest more and eat properly. Take care of yourself."),
        ],
        "task1": [
            {
                "question": "How long has Pavel felt tired?",
                "options": ["about a week", "about a month", "about two months", "about six months"],
                "correct": 1,
                "explain_wrong_ru": "Около месяца.",
            },
            {
                "question": "What did the doctor recommend to Pavel?",
                "options": ["a full check-up", "taking vitamins", "staying in hospital", "changing jobs"],
                "correct": 0,
                "explain_wrong_ru": "Полное обследование.",
            },
            {
                "question": "When does Pavel plan to book?",
                "options": ["tomorrow", "next week", "in a month", "today"],
                "correct": 1,
                "explain_wrong_ru": "На следующей неделе.",
            },
        ],
        "task2": [
            {
                "statement": "Pavel has already had all the tests.",
                "is_true": False,
                "explain_ru": "Он ещё не сдавал анализы.",
            },
            {
                "statement": "The doctor advised Pavel to rest more.",
                "is_true": True,
                "explain_ru": "Больше отдыхать и правильно питаться.",
            },
            {
                "statement": "Pavel is not going to change his lifestyle.",
                "is_true": False,
                "explain_ru": "Он сказал, что последует советам.",
            },
        ],
    },
    "startup": {
        "speakers": [
            {"name": "Pavel", "gender": "male", "role": "developer"},
            {"name": "Ksenia", "gender": "female", "role": "designer"},
        ],
        "turns": [
            (0, "Ksyusha, how is the work on the app going?"),
            (1, "We've already finished the interface prototype."),
            (0, "Cool! When can we show it to the test group?"),
            (1, "In a couple of weeks, I think. Some details still need work."),
            (0, "Which ones exactly?"),
            (1, "For example, the loading animation. It still lags."),
            (0, "I can take that on."),
            (1, "That would be great! You know this stuff."),
            (0, "Yes, I've dealt with this kind of task before."),
            (1, "Then let's meet tomorrow and discuss the details."),
            (0, "Perfect. We'll make it before the deadline."),
            (1, "I hope we can finish everything on time. Thanks for the support."),
        ],
        "task1": [
            {
                "question": "What stage is the app development at?",
                "options": ["idea", "prototype is ready", "testing", "launch"],
                "correct": 1,
                "explain_wrong_ru": "Прототип интерфейса готов.",
            },
            {
                "question": "What needs more work in the prototype?",
                "options": ["fonts", "the loading animation", "the colour scheme", "the buttons"],
                "correct": 1,
                "explain_wrong_ru": "Анимация загрузки тормозит.",
            },
            {
                "question": "When do they plan to meet?",
                "options": ["tomorrow", "the day after tomorrow", "in a week", "in a month"],
                "correct": 0,
                "explain_wrong_ru": "Встреча завтра.",
            },
        ],
        "task2": [
            {
                "statement": "Pavel doesn't understand animation.",
                "is_true": False,
                "explain_ru": "Он разбирается и уже сталкивался с задачей.",
            },
            {
                "statement": "Ksenia thinks they will make the deadline.",
                "is_true": True,
                "explain_ru": "Она надеется закончить вовремя.",
            },
            {
                "statement": "The interface prototype is not ready yet.",
                "is_true": False,
                "explain_ru": "Прототип уже закончен.",
            },
        ],
    },
    "immigration": {
        "speakers": [
            {"name": "Maxim", "gender": "male", "role": "applicant"},
            {"name": "Irina", "gender": "female", "role": "officer"},
        ],
        "turns": [
            (0, "Hello, I'd like to ask about renewing a visa."),
            (1, "Good afternoon. What is your status?"),
            (0, "I'm a temporary resident."),
            (1, "You need to submit an application two weeks before the expiry date."),
            (0, "What documents do I need?"),
            (1, "A passport, a photograph and proof of income."),
            (0, "Are there any special rules for my country?"),
            (1, "No, the procedure is standard for everyone."),
            (0, "How long does the review take?"),
            (1, "Usually up to thirty working days."),
            (0, "That's rather long. I'll submit the application tomorrow."),
            (1, "Good luck. I hope everything goes well."),
        ],
        "task1": [
            {
                "question": "When should the visa renewal application be submitted?",
                "options": ["on the expiry day", "two weeks before expiry", "a month before", "after expiry"],
                "correct": 1,
                "explain_wrong_ru": "За две недели до окончания срока.",
            },
            {
                "question": "What documents are required for renewal?",
                "options": ["only a passport", "a passport and a photo", "a passport, a photo and proof of income", "only proof of income"],
                "correct": 2,
                "explain_wrong_ru": "Паспорт, фото и подтверждение дохода.",
            },
            {
                "question": "How long does the review take?",
                "options": ["up to 10 days", "up to 30 working days", "up to 60 days", "up to 90 days"],
                "correct": 1,
                "explain_wrong_ru": "До 30 рабочих дней.",
            },
        ],
        "task2": [
            {
                "statement": "Maxim has permanent residence.",
                "is_true": False,
                "explain_ru": "Он временно проживающий.",
            },
            {
                "statement": "The officer said the procedure is standard for everyone.",
                "is_true": True,
                "explain_ru": "Процедура стандартная для всех.",
            },
            {
                "statement": "Maxim has already submitted the application.",
                "is_true": False,
                "explain_ru": "Он подаст заявление завтра.",
            },
        ],
    },
}


def has_b2_fixed(topic_id: str) -> bool:
    return str(topic_id or "") in B2_FIXED


def get_b2_fixed(topic_id: str) -> dict | None:
    return B2_FIXED.get(str(topic_id or ""))
