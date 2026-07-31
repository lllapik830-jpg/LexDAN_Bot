"""
Фиксированный контент Listening C2: диалоги + Task1/Task2.
Task3 (порядок реплик) строится из turns как обычно.
"""

from __future__ import annotations

C2_FIXED: dict[str, dict] = {
    "boardroom": {
        "speakers": [
            {"name": "Olga", "gender": "female", "role": "CEO"},
            {"name": "Andrey", "gender": "male", "role": "CFO"},
        ],
        "turns": [
            (0, "Andrey, what's the current situation with the budget for next quarter?"),
            (1, "We're forecasting a deficit of fifteen percent against the plan."),
            (0, "That's serious. We need to review our priorities."),
            (1, "I suggest cutting marketing spend first."),
            (0, "That could hurt our presence in the market."),
            (1, "Then we can optimise operating costs."),
            (0, "That's a more reasonable approach. Which items can we cut?"),
            (1, "Administrative expenses, for example."),
            (0, "I agree. Let's prepare a cost-cutting plan."),
            (1, "The documents will be ready by the next board meeting."),
            (0, "Excellent. Keep me updated."),
            (1, "Certainly. This is our shared responsibility."),
        ],
        "task1": [
            {
                "question": "What budget deficit does Andrey forecast?",
                "options": ["5%", "10%", "15%", "20%"],
                "correct": 2,
                "explain_wrong_ru": "Дефицит 15% от запланированного.",
            },
            {
                "question": "What did Andrey suggest cutting first?",
                "options": ["administrative expenses", "marketing spend", "salaries", "rent"],
                "correct": 1,
                "explain_wrong_ru": "Сначала — расходы на маркетинг.",
            },
            {
                "question": "What did Olga agree to in the end?",
                "options": ["prepare a cost-cutting plan", "increase the budget", "leave everything as is", "cut marketing"],
                "correct": 0,
                "explain_wrong_ru": "Подготовить план сокращений.",
            },
        ],
        "task2": [
            {
                "statement": "Andrey thinks administrative expenses should not be touched.",
                "is_true": False,
                "explain_ru": "Он предложил урезать административные расходы.",
            },
            {
                "statement": "Olga wants to be kept updated.",
                "is_true": True,
                "explain_ru": "Она сказала: держи меня в курсе.",
            },
            {
                "statement": "The cost-cutting plan will be ready by the end of the year.",
                "is_true": False,
                "explain_ru": "Документы будут к следующему заседанию.",
            },
        ],
    },
    "ethics": {
        "speakers": [
            {"name": "Anna", "gender": "female", "role": "researcher"},
            {"name": "Denis", "gender": "male", "role": "philosopher"},
        ],
        "turns": [
            (0, "Denis, how ethical is it to use AI in judicial decision-making?"),
            (1, "That's one of the most controversial questions of our time."),
            (0, "On the one hand, AI can reduce the number of mistakes."),
            (1, "On the other hand, it can reinforce existing biases."),
            (0, "How can we guarantee its impartiality?"),
            (1, "Only through algorithm transparency and constant oversight."),
            (0, "So we can't fully trust the system?"),
            (1, "We can't allow it to act without supervision."),
            (0, "Where is the line between assistance and replacement?"),
            (1, "AI should be a tool, not a judge."),
            (0, "I agree that the human factor must remain central."),
            (1, "Exactly. Responsibility always lies with the human."),
        ],
        "task1": [
            {
                "question": "What does Anna see as a positive aspect of AI in courts?",
                "options": ["it is always right", "it can reduce the number of mistakes", "it is cheaper", "it is faster"],
                "correct": 1,
                "explain_wrong_ru": "Может уменьшить количество ошибок.",
            },
            {
                "question": "What does Denis see as the main danger of AI?",
                "options": ["it can reinforce biases", "it is too expensive", "it is slow", "it doesn't understand people"],
                "correct": 0,
                "explain_wrong_ru": "Может укрепить существующие предубеждения.",
            },
            {
                "question": "Where, in Denis's view, is the limit for using AI?",
                "options": [
                    "AI should be the main judge",
                    "AI should be a tool",
                    "AI should make all decisions",
                    "AI should not be used in courts",
                ],
                "correct": 1,
                "explain_wrong_ru": "ИИ должен быть инструментом, а не судьёй.",
            },
        ],
        "task2": [
            {
                "statement": "Anna thinks AI can act without supervision.",
                "is_true": False,
                "explain_ru": "Она согласилась, что человеческий фактор главный.",
            },
            {
                "statement": "Denis believes responsibility always lies with the human.",
                "is_true": True,
                "explain_ru": "Ответственность всегда лежит на человеке.",
            },
            {
                "statement": "Denis fully trusts AI.",
                "is_true": False,
                "explain_ru": "Без надзора системе доверять нельзя.",
            },
        ],
    },
    "diplomacy": {
        "speakers": [
            {"name": "Smirnov", "gender": "male", "role": "ambassador"},
            {"name": "Petrov", "gender": "male", "role": "attaché"},
        ],
        "turns": [
            (0, "Petrov, what is our country's position on this issue?"),
            (1, "We stick to the principle of non-interference in internal affairs."),
            (0, "That's sensible. But we must also take our allies' views into account."),
            (1, "We're ready for dialogue, but with clear conditions."),
            (0, "We need to stress our commitment to international law."),
            (1, "I've already prepared a draft joint statement."),
            (0, "It needs to be agreed with our partners."),
            (1, "I've requested a meeting to discuss the details."),
            (0, "We have time until the next session begins."),
            (1, "We should use this window of opportunity."),
            (0, "Agreed. Our task is to preserve a balance of interests."),
            (1, "We're acting strictly within the established rules."),
        ],
        "task1": [
            {
                "question": "What position does the country take on this issue?",
                "options": [
                    "full interference",
                    "non-interference in internal affairs",
                    "military presence",
                    "economic sanctions",
                ],
                "correct": 1,
                "explain_wrong_ru": "Принцип невмешательства во внутренние дела.",
            },
            {
                "question": "What has Petrov already prepared?",
                "options": ["a draft joint statement", "a list of sanctions", "a meeting plan", "a new treaty"],
                "correct": 0,
                "explain_wrong_ru": "Проект совместного заявления.",
            },
            {
                "question": "What is the diplomats' task, according to Smirnov?",
                "options": [
                    "preserve a balance of interests",
                    "increase pressure",
                    "break off relations",
                    "sign a new treaty",
                ],
                "correct": 0,
                "explain_wrong_ru": "Сохранить баланс интересов.",
            },
        ],
        "task2": [
            {
                "statement": "Smirnov does not take allies' views into account.",
                "is_true": False,
                "explain_ru": "Нужно учитывать мнение союзников.",
            },
            {
                "statement": "Petrov requested a meeting to discuss the details.",
                "is_true": True,
                "explain_ru": "Он запросил встречу.",
            },
            {
                "statement": "They have no time before the next session begins.",
                "is_true": False,
                "explain_ru": "Время до следующей сессии есть.",
            },
        ],
    },
    "critique": {
        "speakers": [
            {"name": "Maria", "gender": "female", "role": "film critic"},
            {"name": "Andrey", "gender": "male", "role": "director"},
        ],
        "turns": [
            (0, "Andrey, your film has drawn a mixed reaction from the public."),
            (1, "I expected that. Good art is rarely unambiguous."),
            (0, "Critics note the unusual visual style."),
            (1, "That was a conscious choice. I wanted to create a certain atmosphere."),
            (0, "However, the plot seems too complex for a mass audience."),
            (1, "I'm not chasing a mass audience."),
            (0, "Did you deliberately complicate the narrative?"),
            (1, "Yes, so the viewer would stay engaged."),
            (0, "The film definitely requires a second viewing."),
            (1, "For me that's a compliment."),
            (0, "I hope the film finds its audience."),
            (1, "That's the most important thing for any director."),
        ],
        "task1": [
            {
                "question": "What do critics note about Andrey's film?",
                "options": ["an unusual visual style", "a simple plot", "long dialogues", "weak acting"],
                "correct": 0,
                "explain_wrong_ru": "Необычный визуальный стиль.",
            },
            {
                "question": "Why did Andrey deliberately complicate the narrative?",
                "options": [
                    "so the viewer would stay engaged",
                    "to show off his erudition",
                    "to make the film longer",
                    "so it wouldn't be understood",
                ],
                "correct": 0,
                "explain_wrong_ru": "Чтобы зритель оставался вовлечённым.",
            },
            {
                "question": "What does Andrey treat as a compliment to the film?",
                "options": [
                    "its simplicity",
                    "that it requires a second viewing",
                    "its box-office takings",
                    "its popularity",
                ],
                "correct": 1,
                "explain_wrong_ru": "Повторный просмотр — для него комплимент.",
            },
        ],
        "task2": [
            {
                "statement": "Andrey did not expect a mixed reaction.",
                "is_true": False,
                "explain_ru": "Он ожидал этого.",
            },
            {
                "statement": "Andrey is not chasing a mass audience.",
                "is_true": True,
                "explain_ru": "Он не гонится за массовым зрителем.",
            },
            {
                "statement": "Maria thinks the film is too simple.",
                "is_true": False,
                "explain_ru": "Она считает сюжет слишком сложным.",
            },
        ],
    },
    "academia": {
        "speakers": [
            {"name": "Sergeev", "gender": "male", "role": "professor"},
            {"name": "Lebedeva", "gender": "female", "role": "PhD student"},
        ],
        "turns": [
            (0, "Lebedeva, how is your dissertation research going?"),
            (1, "I've finished the data analysis, but the interpretation raises questions."),
            (0, "What exactly is the problem?"),
            (1, "The results diverge from my original hypothesis."),
            (0, "That's not rare in science. Perhaps you should revise the hypothesis."),
            (1, "I've thought about that, but I wouldn't want to give up on the idea."),
            (0, "Then try looking at the data from a different angle."),
            (1, "I'll try. That might give a new understanding of the question."),
            (0, "You must be prepared for the hypothesis not being confirmed."),
            (1, "I understand. Science requires honesty, not stubbornness."),
            (0, "Go in that direction. I believe you'll manage."),
            (1, "Thank you, professor. Your support means a lot to me."),
        ],
        "task1": [
            {
                "question": "What has Lebedeva finished in her research?",
                "options": ["data collection", "data analysis", "writing the thesis", "publication"],
                "correct": 1,
                "explain_wrong_ru": "Она завершила анализ данных.",
            },
            {
                "question": "Why doesn't Lebedeva want to abandon her hypothesis?",
                "options": [
                    "she is afraid of the professor",
                    "she has put a lot of effort into it",
                    "she is sure she is right",
                    "she has no alternative",
                ],
                "correct": 1,
                "explain_wrong_ru": "Ей не хочется отказываться от идеи.",
            },
            {
                "question": "What did the professor advise Lebedeva?",
                "options": [
                    "abandon the hypothesis",
                    "look at the data from a different angle",
                    "change the topic",
                    "stop the research",
                ],
                "correct": 1,
                "explain_wrong_ru": "Взглянуть на данные под другим углом.",
            },
        ],
        "task2": [
            {
                "statement": "Lebedeva does not know how to interpret the results.",
                "is_true": True,
                "explain_ru": "Интерпретация вызывает у неё вопросы.",
            },
            {
                "statement": "The professor thinks abandoning a hypothesis is normal.",
                "is_true": True,
                "explain_ru": "В науке это не редкость — можно пересмотреть гипотезу.",
            },
            {
                "statement": "Lebedeva got fully confirmed results.",
                "is_true": False,
                "explain_ru": "Результаты расходятся с гипотезой.",
            },
        ],
    },
    "court": {
        "speakers": [
            {"name": "Ivanov", "gender": "male", "role": "prosecutor"},
            {"name": "Sokolova", "gender": "female", "role": "defence counsel"},
        ],
        "turns": [
            (0, "Your Honour, the prosecution considers the evidence sufficient."),
            (1, "The defence categorically disagrees with that assessment."),
            (0, "There is direct testimony pointing to the defendant's guilt."),
            (1, "That testimony was obtained in violation of the law."),
            (0, "The investigation acted strictly within procedural norms."),
            (1, "I insist that it be ruled inadmissible."),
            (0, "That will delay the process and be inefficient."),
            (1, "Justice matters more than speed."),
            (0, "I insist the case be heard on the merits."),
            (1, "We will appeal any decision that restricts the defence's rights."),
            (0, "That is your right."),
            (1, "We are ready for any development."),
        ],
        "task1": [
            {
                "question": "What does the defence, through Sokolova, insist on?",
                "options": [
                    "hearing the case on the merits",
                    "ruling the evidence inadmissible",
                    "speeding up the process",
                    "changing the judge",
                ],
                "correct": 1,
                "explain_wrong_ru": "Признание доказательств недопустимыми.",
            },
            {
                "question": "What does Sokolova consider more important than speed?",
                "options": ["budget savings", "justice", "reputation", "public opinion"],
                "correct": 1,
                "explain_wrong_ru": "Справедливость важнее скорости.",
            },
            {
                "question": "What, according to Sokolova, is the defence ready for?",
                "options": ["any development", "defeat", "a compromise", "suspending the case"],
                "correct": 0,
                "explain_wrong_ru": "К любому развитию событий.",
            },
        ],
        "task2": [
            {
                "statement": "The prosecutor believes the evidence was obtained lawfully.",
                "is_true": True,
                "explain_ru": "Следствие действовало в рамках норм.",
            },
            {
                "statement": "The defence will not appeal the court's decision.",
                "is_true": False,
                "explain_ru": "Они будут обжаловать решения, ущемляющие защиту.",
            },
            {
                "statement": "The counsel thinks speed matters more than justice.",
                "is_true": False,
                "explain_ru": "Справедливость важнее скорости.",
            },
        ],
    },
    "climate": {
        "speakers": [
            {"name": "Orlova", "gender": "female", "role": "climatologist"},
            {"name": "Volkov", "gender": "male", "role": "activist"},
        ],
        "turns": [
            (0, "Volkov, how do you assess the current climate situation?"),
            (1, "This is no longer just a threat — it's a crisis that grows every year."),
            (0, "What measures do you consider most effective?"),
            (1, "Besides global agreements, we need changes at city level."),
            (0, "But such changes take time and political will."),
            (1, "We can no longer afford to wait."),
            (0, "I understand your impatience, but without international cooperation we won't manage."),
            (1, "Then we must demand more decisive action from governments."),
            (0, "I agree that we need to increase pressure on all sides."),
            (1, "That's the only path to real change."),
            (0, "We must act now, before it's too late."),
            (1, "Exactly. Time won't wait."),
        ],
        "task1": [
            {
                "question": "How does Volkov assess the current climate situation?",
                "options": [
                    "as a minor problem",
                    "as a crisis that is growing",
                    "as a temporary phenomenon",
                    "as a solved problem",
                ],
                "correct": 1,
                "explain_wrong_ru": "Это кризис, который нарастает.",
            },
            {
                "question": "What measures does Volkov consider most effective?",
                "options": [
                    "only international agreements",
                    "changes at city level",
                    "a total ban on emissions",
                    "population reduction",
                ],
                "correct": 1,
                "explain_wrong_ru": "Нужны изменения на уровне городов (помимо соглашений).",
            },
            {
                "question": "What does Orlova insist on in her approach?",
                "options": [
                    "international cooperation",
                    "individual actions",
                    "economic sanctions",
                    "military intervention",
                ],
                "correct": 0,
                "explain_wrong_ru": "Без международного сотрудничества не справимся.",
            },
        ],
        "task2": [
            {
                "statement": "Volkov thinks we still have time to wait.",
                "is_true": False,
                "explain_ru": "Мы больше не можем ждать.",
            },
            {
                "statement": "Orlova believes efforts are needed from all sides.",
                "is_true": True,
                "explain_ru": "Нужно усиливать давление на все стороны.",
            },
            {
                "statement": "Volkov is satisfied with governments' current actions.",
                "is_true": False,
                "explain_ru": "Он требует более решительных действий.",
            },
        ],
    },
    "philosophy": {
        "speakers": [
            {"name": "Mikhail", "gender": "male", "role": "philosopher"},
            {"name": "Ekaterina", "gender": "female", "role": "student"},
        ],
        "turns": [
            (0, "Ekaterina, how do you understand the concept of free will?"),
            (1, "I believe free will is an illusion created by our consciousness."),
            (0, "That's a rather radical point of view."),
            (1, "I start from the idea that all our actions are predetermined."),
            (0, "Predetermined by what?"),
            (1, "By our desires, fears and external circumstances."),
            (0, "Do you deny the possibility of choice in principle?"),
            (1, "I deny the existence of absolutely free choice."),
            (0, "Then how do you explain the sense of moral responsibility?"),
            (1, "It's a social construct, not proof of freedom."),
            (0, "Your position isn't without logic, but I can't agree with it."),
            (1, "That's fine. Philosophy is a dialogue, not a monologue."),
        ],
        "task1": [
            {
                "question": "How does Ekaterina understand the concept of free will?",
                "options": [
                    "it is absolute reality",
                    "it is an illusion created by consciousness",
                    "it is a gift from above",
                    "it is a result of upbringing",
                ],
                "correct": 1,
                "explain_wrong_ru": "Иллюзия, созданная сознанием.",
            },
            {
                "question": "By what, in Ekaterina's view, are our actions predetermined?",
                "options": [
                    "external circumstances alone",
                    "desires, fears and circumstances",
                    "fate",
                    "other people",
                ],
                "correct": 1,
                "explain_wrong_ru": "Желаниями, страхами и внешними обстоятельствами.",
            },
            {
                "question": "How does Ekaterina explain the sense of moral responsibility?",
                "options": [
                    "it is a social construct",
                    "it is proof of freedom",
                    "it is a result of upbringing",
                    "it does not exist",
                ],
                "correct": 0,
                "explain_wrong_ru": "Это социальный конструкт.",
            },
        ],
        "task2": [
            {
                "statement": "Mikhail shares Ekaterina's point of view.",
                "is_true": False,
                "explain_ru": "Он не может с ней согласиться.",
            },
            {
                "statement": "Ekaterina believes in absolutely free choice.",
                "is_true": False,
                "explain_ru": "Она отрицает абсолютно свободный выбор.",
            },
            {
                "statement": "Mikhail believes that philosophy is a dialogue.",
                "is_true": False,
                "explain_ru": "Это сказала Екатерина, не Михаил.",
            },
        ],
    },
    "finance": {
        "speakers": [
            {"name": "Borisov", "gender": "male", "role": "financial adviser"},
            {"name": "Smirnova", "gender": "female", "role": "investor"},
        ],
        "turns": [
            (0, "Smirnova, how do you assess the current market situation?"),
            (1, "I think we're on the brink of a correction."),
            (0, "That could be an opportunity for long-term investments."),
            (1, "Exactly. I'm looking at several promising sectors right now."),
            (0, "Which sectors interest you?"),
            (1, "Technology and renewable energy."),
            (0, "That's a logical choice given global trends."),
            (1, "I'm also considering investing in startups."),
            (0, "That's riskier, but potentially more profitable."),
            (1, "I'm ready to take on that risk."),
            (0, "It's important to diversify the portfolio to reduce risk."),
            (1, "I agree. Risks need to be spread."),
        ],
        "task1": [
            {
                "question": "Which sector interests Smirnova for investment?",
                "options": [
                    "real estate",
                    "technology and renewable energy",
                    "resource extraction",
                    "financial services",
                ],
                "correct": 1,
                "explain_wrong_ru": "Технологии и возобновляемая энергия.",
            },
            {
                "question": "What else is Smirnova considering investing in?",
                "options": ["bonds", "startups", "cryptocurrency", "real estate"],
                "correct": 1,
                "explain_wrong_ru": "Вложиться в стартапы.",
            },
            {
                "question": "What does Borisov advise to reduce risk?",
                "options": [
                    "diversify the portfolio",
                    "put all money in one sector",
                    "not invest at all",
                    "invest in real estate",
                ],
                "correct": 0,
                "explain_wrong_ru": "Диверсифицировать портфель.",
            },
        ],
        "task2": [
            {
                "statement": "Smirnova thinks the market will correct soon.",
                "is_true": True,
                "explain_ru": "Она на пороге коррекции.",
            },
            {
                "statement": "Borisov considers startups completely safe.",
                "is_true": False,
                "explain_ru": "Стартапы более рискованны.",
            },
            {
                "statement": "Smirnova is not ready to take risk.",
                "is_true": False,
                "explain_ru": "Она готова взять на себя риск.",
            },
        ],
    },
    "literature": {
        "speakers": [
            {"name": "Maximov", "gender": "male", "role": "writer"},
            {"name": "Ivanova", "gender": "female", "role": "literary critic"},
        ],
        "turns": [
            (0, "Ivanova, how do you assess contemporary literature?"),
            (1, "It's going through a difficult period, but I also see encouraging trends."),
            (0, "What do you see as the biggest problem?"),
            (1, "Commercialisation. Many authors write for sales, not for art."),
            (0, "That's an inevitable process in any market society."),
            (1, "I'm not arguing, but it leads to a drop in quality."),
            (0, "Which authors, in your view, retain literary value?"),
            (1, "Those who stay true to themselves and don't chase trends."),
            (0, "That's a rare quality nowadays."),
            (1, "I hope literature will find the strength for a revival."),
            (0, "I hope so too."),
            (1, "We must keep reading and supporting authors."),
        ],
        "task1": [
            {
                "question": "What does Ivanova see as the main problem of contemporary literature?",
                "options": ["a lack of new authors", "commercialisation", "low print runs", "poor translation"],
                "correct": 1,
                "explain_wrong_ru": "Коммерциализация.",
            },
            {
                "question": "Which authors does Ivanova consider valuable?",
                "options": [
                    "those who write for sales",
                    "those who stay true to themselves",
                    "those who follow trends",
                    "those who write quickly",
                ],
                "correct": 1,
                "explain_wrong_ru": "Кто остаётся верен себе.",
            },
            {
                "question": "What does Ivanova hope for in the future?",
                "options": [
                    "that literature will find strength for a revival",
                    "that books will get cheaper",
                    "that there will be more adaptations",
                    "that literature will disappear",
                ],
                "correct": 0,
                "explain_wrong_ru": "Надеется на возрождение литературы.",
            },
        ],
        "task2": [
            {
                "statement": "Maximov does not see a problem with commercialisation.",
                "is_true": False,
                "explain_ru": "Он обсуждает проблему и надеется на возрождение.",
            },
            {
                "statement": "Ivanova thinks commercialisation does not affect quality.",
                "is_true": False,
                "explain_ru": "Она говорит, что это снижает качество.",
            },
            {
                "statement": "Maximov hopes for a revival of literature.",
                "is_true": True,
                "explain_ru": "Он тоже на это надеется.",
            },
        ],
    },
}


def has_c2_fixed(topic_id: str) -> bool:
    return str(topic_id or "") in C2_FIXED


def get_c2_fixed(topic_id: str) -> dict | None:
    return C2_FIXED.get(str(topic_id or ""))
