"""
Фиксированный контент Listening C1: диалоги + Task1/Task2.
Task3 (порядок реплик) строится из turns как обычно.
Тема tech_support — пока без фикса (ждём авторский текст).
"""

from __future__ import annotations

C1_FIXED: dict[str, dict] = {
    "negotiation": {
        "speakers": [
            {"name": "Alexey", "gender": "male", "role": "company director"},
            {"name": "Sergey", "gender": "male", "role": "partner"},
        ],
        "turns": [
            (0, "Sergey, I'm glad we finally met in person."),
            (1, "Alexey, likewise. We've wanted to discuss this partnership for a long time."),
            (0, "I've carefully studied your proposal. It looks convincing."),
            (1, "We have all the resources to deliver this project."),
            (0, "However, I'd like to discuss the financing terms."),
            (1, "We're ready to consider your adjustments."),
            (0, "We need more flexibility in the payment schedule."),
            (1, "That's possible. We can split the payment into stages."),
            (0, "That sounds reasonable. In that case, we're ready to sign the agreement."),
            (1, "Excellent. I'll prepare the final version of the contract."),
            (0, "Agreed. I hope this will be the start of a successful collaboration."),
            (1, "I'm sure of it."),
        ],
        "task1": [
            {
                "question": "What does Alexey want to discuss first?",
                "options": ["project deadlines", "financing terms", "headcount", "legal aspects"],
                "correct": 1,
                "explain_wrong_ru": "Он хочет обсудить условия финансирования.",
            },
            {
                "question": "What is Sergey ready to do at Alexey's request?",
                "options": ["increase the budget", "split the payment into stages", "bring in new investors", "reduce the price"],
                "correct": 1,
                "explain_wrong_ru": "Разбить оплату на этапы.",
            },
            {
                "question": "What decision did they reach in the end?",
                "options": ["postpone signing", "sign the agreement", "call off the talks", "hold another meeting"],
                "correct": 1,
                "explain_wrong_ru": "Они готовы подписать соглашение.",
            },
        ],
        "task2": [
            {
                "statement": "Alexey has not studied Sergey's proposal.",
                "is_true": False,
                "explain_ru": "Он внимательно изучил предложение.",
            },
            {
                "statement": "Sergey is ready to consider Alexey's adjustments.",
                "is_true": True,
                "explain_ru": "Он готов рассмотреть корректировки.",
            },
            {
                "statement": "Signing the agreement is being postponed.",
                "is_true": False,
                "explain_ru": "Они готовы подписать сейчас.",
            },
        ],
    },
    "conference": {
        "speakers": [
            {"name": "Anna", "gender": "female", "role": "coordinator"},
            {"name": "Dmitry", "gender": "male", "role": "speaker"},
        ],
        "turns": [
            (0, "Dmitry, we've confirmed your participation in the conference."),
            (1, "Excellent. I'm preparing a presentation on the latest research."),
            (0, "We'll have about forty minutes for your talk."),
            (1, "That's more than enough. I'll stay within the timing."),
            (0, "After the talk there will be a Q and A session."),
            (1, "I'm always happy to answer participants' questions."),
            (0, "We're also planning to record a video of the talk."),
            (1, "I don't mind if it's published."),
            (0, "Then let's discuss the technical details."),
            (1, "I'll need a projector and a microphone."),
            (0, "Everything will be prepared."),
            (1, "Thanks. I'm looking forward to the event."),
        ],
        "task1": [
            {
                "question": "How much time is allocated for Dmitry's talk?",
                "options": ["30 minutes", "40 minutes", "50 minutes", "60 minutes"],
                "correct": 1,
                "explain_wrong_ru": "Около 40 минут.",
            },
            {
                "question": "What happens after the talk?",
                "options": ["a break", "a Q and A session", "lunch", "a round table"],
                "correct": 1,
                "explain_wrong_ru": "Сессия вопросов и ответов.",
            },
            {
                "question": "What does Dmitry need for the talk?",
                "options": ["a laptop and a flip chart", "a projector and a microphone", "a chair and a table", "a paper presentation"],
                "correct": 1,
                "explain_wrong_ru": "Проектор и микрофон.",
            },
        ],
        "task2": [
            {
                "statement": "Dmitry will not stay within the allocated time.",
                "is_true": False,
                "explain_ru": "Он сказал, что уложится в тайминг.",
            },
            {
                "statement": "Anna plans to record a video of the talk.",
                "is_true": True,
                "explain_ru": "Она планирует записать видео.",
            },
            {
                "statement": "This is Dmitry's first time speaking.",
                "is_true": False,
                "explain_ru": "Об этом в диалоге не сказано.",
            },
        ],
    },
    "healthcare": {
        "speakers": [
            {"name": "Irina", "gender": "female", "role": "client"},
            {"name": "Elena", "gender": "female", "role": "agent"},
        ],
        "turns": [
            (0, "Hello, I'd like to insure my flat."),
            (1, "Good afternoon. What type of insurance are you interested in?"),
            (0, "I need full insurance against all risks."),
            (1, "That's a good choice. We offer several plans."),
            (0, "What's the difference between them?"),
            (1, "Depending on the plan, the coverage can be broader."),
            (0, "I'd like to choose the maximum coverage."),
            (1, "Then I recommend the premium plan."),
            (0, "What's the annual cost of the insurance?"),
            (1, "About fifteen thousand roubles."),
            (0, "That's acceptable. I'm ready to take out the policy."),
            (1, "Excellent. I'll prepare all the necessary documents."),
        ],
        "task1": [
            {
                "question": "What type of insurance interests Irina?",
                "options": ["theft insurance", "flood insurance", "full all-risks insurance", "fire insurance"],
                "correct": 2,
                "explain_wrong_ru": "Полная страховка от всех рисков.",
            },
            {
                "question": "Which plan did Elena recommend?",
                "options": ["basic", "premium", "economy", "standard"],
                "correct": 1,
                "explain_wrong_ru": "Премиум-тариф.",
            },
            {
                "question": "How much does the insurance cost per year?",
                "options": ["10,000 roubles", "15,000 roubles", "20,000 roubles", "25,000 roubles"],
                "correct": 1,
                "explain_wrong_ru": "Около 15 000 рублей.",
            },
        ],
        "task2": [
            {
                "statement": "Irina doesn't know what type of insurance she needs.",
                "is_true": False,
                "explain_ru": "Она хочет полную страховку от всех рисков.",
            },
            {
                "statement": "Irina chose the premium plan.",
                "is_true": True,
                "explain_ru": "Она выбрала максимальное покрытие / премиум.",
            },
            {
                "statement": "Elena refused to issue the policy.",
                "is_true": False,
                "explain_ru": "Елена готовит документы.",
            },
        ],
    },
    "debate_soft": {
        "speakers": [
            {"name": "Dmitry", "gender": "male", "role": "Dmitry"},
            {"name": "Ekaterina", "gender": "female", "role": "Ekaterina"},
        ],
        "turns": [
            (0, "Ekaterina, I believe online learning is the future."),
            (1, "I don't entirely agree with you. Traditional education is still important."),
            (0, "But it's losing its relevance."),
            (1, "You're partly right, but not everything can be replaced by a screen."),
            (0, "For example?"),
            (1, "Live communication and teamwork skills, for example."),
            (0, "Those can be developed in an online environment too."),
            (1, "I think a hybrid approach is the most optimal."),
            (0, "I agree. It's important to keep a balance."),
            (1, "The main thing is that learning stays high-quality."),
            (0, "I hope technology will help, not harm."),
            (1, "I hope so too."),
        ],
        "task1": [
            {
                "question": "What does Dmitry see as the future of education?",
                "options": ["traditional learning", "online learning", "hybrid learning", "self-education"],
                "correct": 1,
                "explain_wrong_ru": "Онлайн-обучение.",
            },
            {
                "question": "What is Ekaterina's view on online learning?",
                "options": [
                    "she is completely against it",
                    "she thinks it is losing relevance",
                    "she thinks a hybrid approach is needed",
                    "she hasn't decided",
                ],
                "correct": 2,
                "explain_wrong_ru": "Гибридный подход — самый оптимальный.",
            },
            {
                "question": "What does Ekaterina consider important in learning?",
                "options": ["quality", "speed", "cost", "accessibility"],
                "correct": 0,
                "explain_wrong_ru": "Чтобы обучение оставалось качественным.",
            },
        ],
        "task2": [
            {
                "statement": "Dmitry sees no point in hybrid learning.",
                "is_true": False,
                "explain_ru": "Он согласился с гибридным подходом.",
            },
            {
                "statement": "Ekaterina believes live communication is important.",
                "is_true": True,
                "explain_ru": "Живое общение нельзя полностью заменить экраном.",
            },
            {
                "statement": "Dmitry thinks technology will harm education.",
                "is_true": False,
                "explain_ru": "Он надеется, что технологии помогут, а не навредят.",
            },
        ],
    },
    "hr": {
        "speakers": [
            {"name": "Anton", "gender": "male", "role": "department head"},
            {"name": "Maxim", "gender": "male", "role": "applicant"},
        ],
        "turns": [
            (0, "Maxim, we've carefully studied your CV."),
            (1, "Thank you. I'm glad I was noticed."),
            (0, "You have impressive experience in your field."),
            (1, "I've worked on several major projects."),
            (0, "What attracts you to our company?"),
            (1, "I want to work in a team with professionals."),
            (0, "That's one of our strengths."),
            (1, "I also value opportunities for growth."),
            (0, "We offer good prospects."),
            (1, "I'm ready for new challenges."),
            (0, "We'll contact you in the near future."),
            (1, "I'll be waiting for your decision."),
        ],
        "task1": [
            {
                "question": "What attracts Maxim to this company?",
                "options": ["high salary", "working with professionals", "a convenient office", "flexible hours"],
                "correct": 1,
                "explain_wrong_ru": "Работа в команде с профессионалами.",
            },
            {
                "question": "What does Maxim value at work?",
                "options": ["stability", "opportunities for growth", "a friendly team", "a short working day"],
                "correct": 1,
                "explain_wrong_ru": "Возможности для роста.",
            },
            {
                "question": "What decision did Anton make?",
                "options": ["hire Maxim", "contact him later", "reject him", "hold another interview"],
                "correct": 1,
                "explain_wrong_ru": "Свяжутся в ближайшее время.",
            },
        ],
        "task2": [
            {
                "statement": "Maxim is unhappy with his previous job.",
                "is_true": False,
                "explain_ru": "Об этом в диалоге не сказано.",
            },
            {
                "statement": "Anton wants Maxim to work on his team.",
                "is_true": True,
                "explain_ru": "Антон хвалит опыт и обещает связаться.",
            },
            {
                "statement": "Maxim is not ready for new challenges.",
                "is_true": False,
                "explain_ru": "Он сказал, что готов к новым вызовам.",
            },
        ],
    },
    "mediator": {
        "speakers": [
            {"name": "Olga", "gender": "female", "role": "mediator"},
            {"name": "Ivan", "gender": "male", "role": "neighbour"},
            {"name": "Mikhail", "gender": "male", "role": "neighbour"},
        ],
        "turns": [
            (0, "Good afternoon. I invited you to help resolve the conflict."),
            (1, "We're here because of the noise in the evenings."),
            (2, "I disagree. I'm not breaking the quiet hours."),
            (0, "Let's hear each other without accusations."),
            (1, "He plays loud music until midnight."),
            (2, "Only sometimes, and I'm not breaking the law."),
            (0, "It's important to find a compromise that works for both of you."),
            (1, "I suggest we discuss specific hours."),
            (2, "I can turn the music down after ten p.m."),
            (1, "That would be a good solution."),
            (0, "I'm glad you've reached an agreement."),
            (2, "Thanks for your help."),
        ],
        "task1": [
            {
                "question": "What is the conflict between the neighbours about?",
                "options": ["parking", "noise in the evenings", "pets", "rubbish"],
                "correct": 1,
                "explain_wrong_ru": "Шум по вечерам.",
            },
            {
                "question": "What solution did Ivan propose?",
                "options": ["ban music", "discuss specific hours", "move out", "call the police"],
                "correct": 1,
                "explain_wrong_ru": "Обсудить конкретные часы.",
            },
            {
                "question": "What did Mikhail agree to do?",
                "options": [
                    "stop listening to music",
                    "turn the music down after 10 p.m.",
                    "buy headphones",
                    "compromise with the neighbours",
                ],
                "correct": 1,
                "explain_wrong_ru": "Убавлять музыку после 22:00.",
            },
        ],
        "task2": [
            {
                "statement": "Mikhail plays loud music every night.",
                "is_true": False,
                "explain_ru": "Он сказал, что только иногда.",
            },
            {
                "statement": "Olga helped them find a compromise.",
                "is_true": True,
                "explain_ru": "Она вела медиацию к компромиссу.",
            },
            {
                "statement": "Ivan and Mikhail did not reach an agreement.",
                "is_true": False,
                "explain_ru": "Они пришли к соглашению.",
            },
        ],
    },
    "research": {
        "speakers": [
            {"name": "Natalia", "gender": "female", "role": "researcher"},
            {"name": "Alexey", "gender": "male", "role": "participant"},
        ],
        "turns": [
            (0, "Alexey, thank you for agreeing to take part in our study."),
            (1, "I'm curious what the study is about."),
            (0, "We're studying the effect of stress on productivity."),
            (1, "That's a relevant topic in today's world."),
            (0, "We'll be collecting data for two months."),
            (1, "What will I need to do?"),
            (0, "Fill in daily reports about how you feel."),
            (1, "That's not hard. I can do that."),
            (0, "It's important to answer honestly so the results are accurate."),
            (1, "I understand. I'll try to be objective."),
            (0, "At the end of the study we'll sum up the results."),
            (1, "I'm looking forward to the results."),
        ],
        "task1": [
            {
                "question": "What is this study examining?",
                "options": [
                    "the effect of diet on health",
                    "the effect of stress on productivity",
                    "the effect of sport on mood",
                    "the effect of sleep on memory",
                ],
                "correct": 1,
                "explain_wrong_ru": "Влияние стресса на продуктивность.",
            },
            {
                "question": "How long will the study last?",
                "options": ["one month", "two months", "three months", "six months"],
                "correct": 1,
                "explain_wrong_ru": "Два месяца.",
            },
            {
                "question": "What will Alexey need to do?",
                "options": ["take medical tests", "fill in daily reports", "see a doctor", "change his lifestyle"],
                "correct": 1,
                "explain_wrong_ru": "Заполнять ежедневные отчёты.",
            },
        ],
        "task2": [
            {
                "statement": "Alexey agreed to take part in the study.",
                "is_true": True,
                "explain_ru": "Он согласился участвовать.",
            },
            {
                "statement": "Natalia did not say what the study is for.",
                "is_true": False,
                "explain_ru": "Она объяснила тему: стресс и продуктивность.",
            },
            {
                "statement": "Alexey promised to answer honestly.",
                "is_true": True,
                "explain_ru": "Он будет стараться быть объективным.",
            },
        ],
    },
    "politics_soft": {
        "speakers": [
            {"name": "Polina", "gender": "female", "role": "activist"},
            {"name": "Sergey", "gender": "male", "role": "official"},
        ],
        "turns": [
            (0, "Sergey, I want to discuss the problem of green spaces in our district."),
            (1, "I'm listening. What exactly concerns you?"),
            (0, "The number of parks is shrinking while development is growing."),
            (1, "We're already planning to create new recreation areas."),
            (0, "When will that happen?"),
            (1, "We'll start next year, if the budget allows."),
            (0, "We can't wait another year."),
            (1, "I understand your impatience, but there are bureaucratic procedures."),
            (0, "We're ready to take part in the discussion."),
            (1, "That's a good approach. It's important to take residents' views into account."),
            (0, "Then let's organise a meeting with the public."),
            (1, "I agree. We'll set a date in the near future."),
        ],
        "task1": [
            {
                "question": "What problem concerns Polina?",
                "options": ["bad roads", "a lack of green spaces", "air pollution", "no schools"],
                "correct": 1,
                "explain_wrong_ru": "Нехватка зелёных зон / парков.",
            },
            {
                "question": "When is the creation of new recreation areas planned to start?",
                "options": ["this year", "next year", "in two years", "in three years"],
                "correct": 1,
                "explain_wrong_ru": "В следующем году.",
            },
            {
                "question": "What did Polina propose during the conversation?",
                "options": [
                    "organise a public meeting",
                    "write a petition",
                    "run a survey",
                    "complain to higher authorities",
                ],
                "correct": 0,
                "explain_wrong_ru": "Встречу с общественностью.",
            },
        ],
        "task2": [
            {
                "statement": "Sergey is not ready to listen to residents.",
                "is_true": False,
                "explain_ru": "Он считает важным учитывать мнение жителей.",
            },
            {
                "statement": "Polina thinks waiting another year is too long.",
                "is_true": True,
                "explain_ru": "Она сказала, что нельзя ждать ещё год.",
            },
            {
                "statement": "The budget for green spaces has already been approved.",
                "is_true": False,
                "explain_ru": "Начнут, если бюджет позволит.",
            },
        ],
    },
    "culture_c1": {
        "speakers": [
            {"name": "Elena", "gender": "female", "role": "art critic"},
            {"name": "Konstantin", "gender": "male", "role": "artist"},
        ],
        "turns": [
            (0, "Konstantin, your exhibition has received a lot of feedback."),
            (1, "I'm glad it sparked the public's interest."),
            (0, "Your works combine the classical and the contemporary."),
            (1, "I want art to be accessible to everyone."),
            (0, "What inspires you?"),
            (1, "The world around us and people's emotions."),
            (0, "That's visible in your works."),
            (1, "I believe art should spark dialogue."),
            (0, "I agree. That makes it more valuable."),
            (1, "I hope my works will stay relevant."),
            (0, "I'm sure they'll delight viewers for a long time."),
            (1, "Thank you for the kind words."),
        ],
        "task1": [
            {
                "question": "How does Elena describe Konstantin's works?",
                "options": [
                    "they are very simple",
                    "they combine the classical and the contemporary",
                    "they are hard to understand",
                    "they are very dark",
                ],
                "correct": 1,
                "explain_wrong_ru": "Сочетают классику и современность.",
            },
            {
                "question": "What inspires Konstantin?",
                "options": ["music", "the world around us and emotions", "other artists", "travel"],
                "correct": 1,
                "explain_wrong_ru": "Окружающий мир и эмоции людей.",
            },
            {
                "question": "What does Konstantin consider important in art?",
                "options": ["sparking dialogue", "being profitable", "being easy to understand", "being beautiful"],
                "correct": 0,
                "explain_wrong_ru": "Искусство должно вызывать диалог.",
            },
        ],
        "task2": [
            {
                "statement": "Konstantin is not sure his works will stay relevant.",
                "is_true": True,
                "explain_ru": "Он надеется, что работы останутся актуальными.",
            },
            {
                "statement": "Elena believes his works will spark dialogue.",
                "is_true": True,
                "explain_ru": "Она согласна, что это делает искусство ценнее.",
            },
            {
                "statement": "Konstantin doesn't like giving interviews.",
                "is_true": False,
                "explain_ru": "Об этом в диалоге не сказано.",
            },
        ],
    },
}


def has_c1_fixed(topic_id: str) -> bool:
    return str(topic_id or "") in C1_FIXED


def get_c1_fixed(topic_id: str) -> dict | None:
    return C1_FIXED.get(str(topic_id or ""))
