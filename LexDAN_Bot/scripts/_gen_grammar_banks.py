# -*- coding: utf-8 -*-
"""Generate curated grammar banks for all practice topics missing full coverage."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "grammar_banks_extra.py"


def mcq(instr, sen, ru, opts, ans, tip):
    assert ans in opts, f"{ans!r} not in {opts}"
    assert len(opts) == 4
    assert all(len(o) >= 1 and o.lower() not in {"b", "c", "d"} for o in opts), opts
    # reject letter-only fake MCQ like a/b/c/d (except a/an/I)
    letterish = [o for o in opts if len(o) == 1 and o.lower() not in {"a", "i"}]
    assert not letterish, opts
    return {
        "kind": "mcq",
        "subtype": "mcq",
        "instruction_ru": instr,
        "sentence_en": sen,
        "sentence_ru": ru,
        "options": opts,
        "answer": ans,
        "tip": tip,
    }


def wf(instr, sen, ru, base, ans, tip):
    return {
        "kind": "write",
        "subtype": "word_form",
        "instruction_ru": instr,
        "sentence_en": sen,
        "sentence_ru": ru,
        "base_form": base,
        "answer": ans,
        "tip": tip,
        "options": None,
    }


def te(instr, ru, ans, tip, sen=""):
    return {
        "kind": "write",
        "subtype": "translate_en",
        "instruction_ru": instr,
        "sentence_ru": ru,
        "sentence_en": sen,
        "answer": ans,
        "tip": tip,
        "options": None,
    }


def tr(instr, sen, ru, ans, tip):
    return {
        "kind": "write",
        "subtype": "translate_ru",
        "instruction_ru": instr,
        "sentence_en": sen,
        "sentence_ru": ru,
        "answer": ans,
        "tip": tip,
        "options": None,
    }


def pack8(items):
    assert len(items) == 8, len(items)
    kinds = [x["subtype"] for x in items]
    assert kinds == [
        "mcq",
        "mcq",
        "mcq",
        "word_form",
        "word_form",
        "word_form",
        "translate_en",
        "translate_ru",
    ], kinds
    return items


BANKS: dict[str, list] = {}

# --- pad / fix existing short topics ---
BANKS["this_that"] = pack8(
    [
        mcq(
            "Выбери this или that.",
            "____ is my pen (near me).",
            "Это моя ручка (рядом).",
            ["This", "That", "These", "Those"],
            "This",
            "Близко → This.",
        ),
        mcq(
            "Выбери правильное предложение.",
            "Which sentence is correct?",
            "То — машина вон там.",
            [
                "That is a car.",
                "This are a car.",
                "These is a car.",
                "That are a car.",
            ],
            "That is a car.",
            "Дальше → That is.",
        ),
        mcq(
            "Выбери вопрос.",
            "____ is this?",
            "Что это?",
            ["What", "Where", "Who", "When"],
            "What",
            "What is this?",
        ),
        wf(
            "Напиши This или That.",
            "____ book is on the table next to me.",
            "Эта книга рядом со мной.",
            "",
            "This",
            "Рядом → This.",
        ),
        wf(
            "Напиши This или That.",
            "Look over there! ____ is a big dog.",
            "Вон там большая собака.",
            "",
            "That",
            "Дальше → That.",
        ),
        wf(
            "Напиши This или That.",
            "____ is my bag here.",
            "Это моя сумка здесь.",
            "",
            "This",
            "Here → This.",
        ),
        te("Переведи (This/That):", "Это мой телефон.", "This is my phone.", "This is…"),
        tr(
            "Переведи на русский:",
            "That is a big house.",
            "То — большой дом.",
            "То — большой дом.",
            "That = то (дальше).",
        ),
    ]
)

BANKS["simple_phrases"] = pack8(
    [
        mcq(
            "Выбери перевод.",
            "Nice to meet you.",
            "",
            ["Приятно познакомиться.", "Как дела?", "Спасибо.", "Извини."],
            "Приятно познакомиться.",
            "Знакомство.",
        ),
        mcq(
            "Как ответить на How are you?",
            "How are you?",
            "Как дела?",
            ["I'm fine.", "My name is Danil.", "Thank you.", "Sorry."],
            "I'm fine.",
            "I'm fine.",
        ),
        mcq(
            "Как сказать «Спасибо»?",
            "Choose the phrase.",
            "",
            ["Thank you.", "Please.", "Sorry.", "Hello."],
            "Thank you.",
            "Thank you.",
        ),
        wf(
            "Напиши приветствие Hello или Hi.",
            "____! My name is Anna.",
            "Привет! Меня зовут Анна.",
            "",
            "Hello",
            "Hello / Hi.",
        ),
        wf(
            "Дополни фразу.",
            "Nice to ____ you.",
            "Приятно познакомиться.",
            "meet",
            "meet",
            "Nice to meet you.",
        ),
        wf(
            "Дополни фразу.",
            "What is your ____?",
            "Как тебя зовут?",
            "name",
            "name",
            "What's your name?",
        ),
        te("Переведи:", "Как тебя зовут?", "What is your name?", "What's your name?"),
        tr(
            "Переведи:",
            "Hello! How are you?",
            "Привет! Как дела?",
            "Привет! Как дела?",
            "Hello / Hi.",
        ),
    ]
)

BANKS["articles_a_an"] = pack8(
    [
        mcq(
            "Выбери a или an.",
            "I see ____ apple.",
            "Я вижу яблоко.",
            ["an", "a", "the", "some"],
            "an",
            "apple — гласный звук → an.",
        ),
        mcq(
            "Выбери a или an.",
            "She needs ____ pen.",
            "Ей нужна ручка.",
            ["a", "an", "the", "some"],
            "a",
            "pen — согласный → a.",
        ),
        mcq(
            "Выбери правильное.",
            "Which is correct?",
            "университет",
            ["a university", "an university", "a universities", "an hour university"],
            "a university",
            "university = /juː/ → a.",
        ),
        wf("Напиши a или an.", "It is ____ hour.", "Это час.", "", "an", "hour — h немой → an."),
        wf("Напиши a или an.", "He is ____ doctor.", "Он врач.", "", "a", "doctor → a."),
        wf("Напиши a или an.", "I need ____ umbrella.", "Мне нужен зонт.", "", "an", "umbrella → an."),
        te("Переведи (с a/an):", "У меня есть книга.", "I have a book.", "a book."),
        tr(
            "Переведи на русский:",
            "She has an orange.",
            "У неё есть апельсин.",
            "У неё есть апельсин.",
            "an orange.",
        ),
    ]
)

BANKS["present_simple"] = pack8(
    [
        mcq(
            "Выбери правильную форму Present Simple.",
            "She ____ to school by bus every day.",
            "Она ездит в школу на автобусе каждый день.",
            ["goes", "go", "going", "went"],
            "goes",
            "he/she/it → goes.",
        ),
        mcq(
            "Выбери грамматически правильное предложение (Present Simple).",
            "Which sentence is correct?",
            "Она читает книги каждый вечер.",
            [
                "She reads books every evening.",
                "She is reading books every evening.",
                "She reading books every evening.",
                "She read books every evening.",
            ],
            "She reads books every evening.",
            "every evening → Present Simple, не Continuous.",
        ),
        mcq(
            "Выбери вопрос в Present Simple.",
            "____ you speak English?",
            "Ты говоришь по-английски?",
            ["Do", "Does", "Are", "Is"],
            "Do",
            "Do + you + V1?",
        ),
        wf(
            "Поставь глагол в Present Simple.",
            "He ____ (go) to school every day.",
            "Он ходит в школу каждый день.",
            "go",
            "goes",
            "he → goes.",
        ),
        wf(
            "Поставь don't или doesn't.",
            "She ____ (not play) football.",
            "Она не играет в футбол.",
            "not play",
            "doesn't",
            "she → doesn't.",
        ),
        wf(
            "Поставь глагол в Present Simple.",
            "They ____ (watch) TV in the evening.",
            "Они смотрят телевизор вечером.",
            "watch",
            "watch",
            "they → без -s.",
        ),
        te(
            "Переведи (Present Simple):",
            "Я обычно встаю в 7.",
            "I usually get up at 7.",
            "usually + Present Simple.",
        ),
        tr(
            "Переведи на русский:",
            "She works in a hospital.",
            "Она работает в больнице.",
            "Она работает в больнице.",
            "works = работает.",
        ),
    ]
)

BANKS["present_continuous"] = pack8(
    [
        mcq(
            "Выбери правильную форму Present Continuous.",
            "She ____ watching a film now.",
            "Она сейчас смотрит фильм.",
            ["is", "are", "am", "be"],
            "is",
            "she → is + V-ing.",
        ),
        mcq(
            "Выбери правильное предложение (Present Continuous).",
            "Which sentence is correct?",
            "Мы сейчас учим английский.",
            [
                "We are learning English now.",
                "We learn English now.",
                "We is learning English now.",
                "We learning English now.",
            ],
            "We are learning English now.",
            "now → are + V-ing.",
        ),
        mcq(
            "Выбери форму to be.",
            "I ____ reading a book right now.",
            "Я сейчас читаю книгу.",
            ["am", "is", "are", "be"],
            "am",
            "I → am + V-ing.",
        ),
        wf(
            "Напиши форму V-ing.",
            "Look! He is ____ (run) in the park.",
            "Смотри! Он бегает в парке.",
            "run",
            "running",
            "run → running.",
        ),
        wf(
            "Напиши am / is / are.",
            "They ____ (be) playing football now.",
            "Они сейчас играют в футбол.",
            "be",
            "are",
            "they → are.",
        ),
        wf(
            "Напиши isn't или aren't.",
            "She ____ (not be) sleeping.",
            "Она не спит.",
            "not be",
            "isn't",
            "she → isn't.",
        ),
        te(
            "Переведи (Present Continuous):",
            "Я сейчас пишу сообщение.",
            "I am writing a message now.",
            "I am + writing.",
        ),
        tr(
            "Переведи на русский:",
            "They are cooking dinner now.",
            "Они сейчас готовят ужин.",
            "Они сейчас готовят ужин.",
            "are cooking = готовят.",
        ),
    ]
)


def topic_bank(
    tid,
    m1,
    m2,
    m3,
    w4,
    w5,
    w6,
    t7,
    t8,
):
    BANKS[tid] = pack8([m1, m2, m3, w4, w5, w6, t7, t8])


# Keep existing good banks by re-exporting from file later; here only missing + overrides above.

topic_bank(
    "past_simple",
    mcq(
        "Выбери Past Simple.",
        "Yesterday I ____ to the park.",
        "Вчера я ходил в парк.",
        ["went", "go", "goes", "going"],
        "went",
        "go → went.",
    ),
    mcq(
        "Выбери правильное предложение (Past Simple).",
        "Which sentence is correct?",
        "Она вчера смотрела фильм.",
        [
            "She watched a film yesterday.",
            "She watches a film yesterday.",
            "She is watching a film yesterday.",
            "She watch a film yesterday.",
        ],
        "She watched a film yesterday.",
        "yesterday → Past Simple.",
    ),
    mcq(
        "Выбери вопрос в Past Simple.",
        "____ you see him last week?",
        "Ты видел его на прошлой неделе?",
        ["Did", "Do", "Does", "Are"],
        "Did",
        "Did + subject + V1?",
    ),
    wf("Поставь глагол в Past Simple.", "She ____ (visit) London last year.", "Она ездила в Лондон в прошлом году.", "visit", "visited", "regular: +ed."),
    wf("Поставь didn't.", "He ____ (not come) to the party.", "Он не пришёл на вечеринку.", "not come", "didn't", "didn't + V1."),
    wf("Поставь форму was/were.", "They ____ (be) happy yesterday.", "Они были счастливы вчера.", "be", "were", "they → were."),
    te("Переведи (Past Simple):", "Я вчера купил книгу.", "I bought a book yesterday.", "buy → bought."),
    tr("Переведи:", "We lived in Moscow two years ago.", "Мы жили в Москве два года назад.", "Мы жили в Москве два года назад.", "lived = жили."),
)

topic_bank(
    "going_to_future",
    mcq(
        "Выбери форму be going to.",
        "I ____ going to call you later.",
        "Я собираюсь позвонить тебе позже.",
        ["am", "is", "are", "be"],
        "am",
        "I → am going to.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Они собираются путешествовать.",
        [
            "They are going to travel.",
            "They is going to travel.",
            "They going to travel.",
            "They go to travel.",
        ],
        "They are going to travel.",
        "they → are going to.",
    ),
    mcq(
        "Выбери правильный вариант.",
        "She is going ____ start a new job.",
        "Она собирается начать новую работу.",
        ["to", "for", "at", "in"],
        "to",
        "going to + V1.",
    ),
    wf("Напиши am/is/are.", "We ____ (be) going to buy a car.", "Мы собираемся купить машину.", "be", "are", "we → are."),
    wf("Напиши глагол V1.", "He is going to ____ (study) medicine.", "Он собирается изучать медицину.", "study", "study", "going to + V1."),
    wf("Напиши isn't/aren't.", "It ____ (not be) going to rain.", "Не собирается идти дождь.", "not be", "isn't", "it → isn't."),
    te("Переведи (going to):", "Я собираюсь готовить ужин.", "I am going to cook dinner.", "I am going to + V1."),
    tr("Переведи:", "She is going to visit her grandma.", "Она собирается навестить бабушку.", "Она собирается навестить бабушку.", "is going to = собирается."),
)

topic_bank(
    "much_many_some_any",
    mcq(
        "Выбери much или many.",
        "How ____ apples do you want?",
        "Сколько яблок ты хочешь?",
        ["many", "much", "a", "any"],
        "many",
        "apples = исчисляемые → many.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "У меня мало молока.",
        [
            "I don't have much milk.",
            "I don't have many milk.",
            "I don't have much milks.",
            "I don't have many milks.",
        ],
        "I don't have much milk.",
        "milk = неисчисляемое → much.",
    ),
    mcq(
        "Выбери some или any.",
        "I don't have ____ money.",
        "У меня нет денег.",
        ["any", "some", "much", "a"],
        "any",
        "отрицание → any.",
    ),
    wf("Напиши much или many.", "There isn't ____ sugar.", "Сахара мало / нет.", "", "much", "sugar → much."),
    wf("Напиши some или any.", "Have you got ____ friends here?", "У тебя есть друзья здесь?", "", "any", "вопрос → any."),
    wf("Напиши some или any.", "Would you like ____ tea?", "Хочешь чаю?", "", "some", "предложение → some."),
    te("Переведи:", "У меня много друзей.", "I have many friends.", "friends → many."),
    tr("Переведи:", "Is there any water?", "Есть вода?", "Есть вода?", "any в вопросе."),
)

topic_bank(
    "comparatives",
    mcq(
        "Выбери сравнительную степень.",
        "This book is ____ than that one.",
        "Эта книга интереснее той.",
        ["more interesting", "most interesting", "interestinger", "as interesting"],
        "more interesting",
        "длинные прил. → more + adj.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Мой брат выше меня.",
        [
            "My brother is taller than me.",
            "My brother is more tall than me.",
            "My brother is tallest than me.",
            "My brother is as taller me.",
        ],
        "My brother is taller than me.",
        "tall → taller.",
    ),
    mcq(
        "Выбери превосходную степень.",
        "This is the ____ day of my life.",
        "Это лучший день в моей жизни.",
        ["best", "better", "good", "more good"],
        "best",
        "good → better → best.",
    ),
    wf("Напиши сравнительную степень.", "She is ____ (young) than her sister.", "Она моложе сестры.", "young", "younger", "young → younger."),
    wf("Напиши превосходную степень.", "He is the ____ (fast) runner.", "Он самый быстрый бегун.", "fast", "fastest", "the + -est."),
    wf("Напиши more/most.", "This task is ____ difficult.", "Это задание сложнее.", "", "more", "more + difficult."),
    te("Переведи:", "Этот дом больше того.", "This house is bigger than that one.", "big → bigger."),
    tr("Переведи:", "She is the smartest student.", "Она самая умная ученица.", "Она самая умная ученица.", "the smartest."),
)

topic_bank(
    "modals_a2",
    mcq(
        "Выбери модальный глагол.",
        "You ____ wear a seatbelt. It's the law.",
        "Ты должен пристегнуться. Это закон.",
        ["must", "should", "can", "might"],
        "must",
        "закон / обязанность → must.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Тебе следует больше спать.",
        [
            "You should sleep more.",
            "You should to sleep more.",
            "You must to sleep more.",
            "You should sleeping more.",
        ],
        "You should sleep more.",
        "should + V1 без to.",
    ),
    mcq(
        "Выбери запрет.",
        "You ____ smoke here.",
        "Здесь нельзя курить.",
        ["mustn't", "must", "should", "can"],
        "mustn't",
        "запрет → mustn't.",
    ),
    wf("Напиши must или have to.", "I ____ (must) finish this today.", "Я должен закончить это сегодня.", "must", "must", "must + V1."),
    wf("Напиши should.", "You ____ (should) call your mum.", "Тебе стоит позвонить маме.", "should", "should", "should + V1."),
    wf("Напиши don't have to.", "You ____ (not have to) come if you're busy.", "Тебе не обязательно приходить.", "not have to", "don't have to", "нет обязанности."),
    te("Переведи:", "Ты должен сделать домашку.", "You must do your homework.", "must + V1."),
    tr("Переведи:", "You shouldn't be late.", "Тебе не следует опаздывать.", "Тебе не следует опаздывать.", "shouldn't."),
)

topic_bank(
    "present_perfect",
    mcq(
        "Выбери Present Perfect.",
        "I ____ finished my homework.",
        "Я закончил домашку.",
        ["have", "has", "had", "am"],
        "have",
        "I/you/we/they → have + V3.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Она уже видела этот фильм.",
        [
            "She has already seen this film.",
            "She have already seen this film.",
            "She has already saw this film.",
            "She already see this film.",
        ],
        "She has already seen this film.",
        "she → has + V3.",
    ),
    mcq(
        "Выбери since или for.",
        "We have lived here ____ 2020.",
        "Мы живём здесь с 2020.",
        ["since", "for", "from", "at"],
        "since",
        "since + точка во времени.",
    ),
    wf("Напиши have или has.", "He ____ (have) lost his keys.", "Он потерял ключи.", "have", "has", "he → has."),
    wf("Напиши V3.", "They have ____ (write) three emails.", "Они написали три письма.", "write", "written", "write → written."),
    wf("Напиши haven't/hasn't.", "She ____ (not have) arrived yet.", "Она ещё не приехала.", "not have", "hasn't", "she → hasn't."),
    te("Переведи (Present Perfect):", "Я никогда не был в Лондоне.", "I have never been to London.", "have + never + V3."),
    tr("Переведи:", "Have you ever eaten sushi?", "Ты когда-нибудь ел суши?", "Ты когда-нибудь ел суши?", "Have you ever…?"),
)

topic_bank(
    "past_perfect",
    mcq(
        "Выбери Past Perfect.",
        "When I arrived, the train ____ already left.",
        "Когда я приехал, поезд уже ушёл.",
        ["had", "has", "have", "was"],
        "had",
        "had + V3 — раньше другого прошлого.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Он сказал, что уже поел.",
        [
            "He said he had already eaten.",
            "He said he has already eaten.",
            "He said he already eat.",
            "He said he was already eaten.",
        ],
        "He said he had already eaten.",
        "Past Perfect после said.",
    ),
    mcq(
        "Выбери форму.",
        "She ____ never seen snow before that day.",
        "До того дня она никогда не видела снег.",
        ["had", "has", "have", "was"],
        "had",
        "had never + V3.",
    ),
    wf("Напиши had.", "They ____ (have) finished before we came.", "Они закончили до нашего прихода.", "have", "had", "had + V3."),
    wf("Напиши V3.", "I had ____ (leave) when she called.", "Я уже ушёл, когда она позвонила.", "leave", "left", "leave → left."),
    wf("Напиши hadn't.", "We ____ (not have) met before.", "Мы не встречались раньше.", "not have", "hadn't", "hadn't + V3."),
    te("Переведи:", "К тому времени я уже сделал работу.", "By then I had already done the work.", "had + V3."),
    tr("Переведи:", "She had gone home before midnight.", "Она ушла домой до полуночи.", "Она ушла домой до полуночи.", "had gone."),
)

topic_bank(
    "past_continuous",
    mcq(
        "Выбери Past Continuous.",
        "Yesterday at 5 I ____ watching TV.",
        "Вчера в 5 я смотрел телевизор.",
        ["was", "were", "am", "is"],
        "was",
        "I → was + V-ing.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Пока шёл дождь, мы сидели дома.",
        [
            "While it was raining, we were sitting at home.",
            "While it rained, we was sitting at home.",
            "While it was rain, we sat at home.",
            "While it were raining, we sit at home.",
        ],
        "While it was raining, we were sitting at home.",
        "was/were + V-ing.",
    ),
    mcq(
        "Выбери форму.",
        "They ____ playing football when I saw them.",
        "Они играли в футбол, когда я их увидел.",
        ["were", "was", "are", "is"],
        "were",
        "they → were.",
    ),
    wf("Напиши was/were.", "She ____ (be) cooking when the phone rang.", "Она готовила, когда зазвонил телефон.", "be", "was", "she → was."),
    wf("Напиши V-ing.", "We were ____ (drive) to work.", "Мы ехали на работу.", "drive", "driving", "drive → driving."),
    wf("Напиши wasn't/weren't.", "He ____ (not be) sleeping at midnight.", "Он не спал в полночь.", "not be", "wasn't", "he → wasn't."),
    te("Переведи:", "В 8 вечера я читал.", "At 8 pm I was reading.", "was + V-ing."),
    tr("Переведи:", "They were talking about the trip.", "Они говорили о поездке.", "Они говорили о поездке.", "were talking."),
)

topic_bank(
    "conditionals_0_1",
    mcq(
        "Выбери First Conditional.",
        "If it rains, we ____ stay home.",
        "Если будет дождь, мы останемся дома.",
        ["will", "would", "are", "did"],
        "will",
        "If + Present, will + V1.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Если ты греешь лёд, он тает.",
        [
            "If you heat ice, it melts.",
            "If you will heat ice, it melts.",
            "If you heat ice, it will melts.",
            "If you heated ice, it melt.",
        ],
        "If you heat ice, it melts.",
        "Zero Conditional: Present + Present.",
    ),
    mcq(
        "Выбери форму в if-части.",
        "If she ____ free, she will come.",
        "Если она будет свободна, она придёт.",
        ["is", "will be", "was", "be"],
        "is",
        "в if — Present, не will.",
    ),
    wf("Напиши will или Present.", "If I see him, I ____ (tell) him.", "Если увижу его, скажу.", "tell", "will tell", "will + V1."),
    wf("Напиши Present в if.", "If water ____ (boil), it turns into steam.", "Если вода кипит…", "boil", "boils", "Zero: Present."),
    wf("Напиши don't/doesn't.", "If it ____ (not rain), we will go out.", "Если не будет дождя…", "not rain", "doesn't", "it → doesn't."),
    te("Переведи:", "Если я буду свободен, я позвоню.", "If I am free, I will call.", "If + Present, will."),
    tr("Переведи:", "If you study, you will pass.", "Если будешь учиться, сдашь.", "Если будешь учиться, сдашь.", "First Conditional."),
)

topic_bank(
    "gerund_infinitive",
    mcq(
        "Выбери герундий или инфинитив.",
        "I enjoy ____ books.",
        "Мне нравится читать книги.",
        ["reading", "to read", "read", "reads"],
        "reading",
        "enjoy + V-ing.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Она решила уехать.",
        [
            "She decided to leave.",
            "She decided leaving.",
            "She decided leave.",
            "She decided to leaving.",
        ],
        "She decided to leave.",
        "decide + to V1.",
    ),
    mcq(
        "Выбери форму.",
        "He wants ____ a doctor.",
        "Он хочет стать врачом.",
        ["to be", "being", "be", "been"],
        "to be",
        "want + to V1.",
    ),
    wf("Напиши V-ing.", "Stop ____ (talk), please.", "Перестань говорить.", "talk", "talking", "stop + V-ing."),
    wf("Напиши to + V1.", "I hope ____ (see) you soon.", "Надеюсь увидеть тебя скоро.", "see", "to see", "hope + to V1."),
    wf("Напиши V-ing.", "She is good at ____ (cook).", "Она хорошо готовит.", "cook", "cooking", "good at + V-ing."),
    te("Переведи:", "Я люблю плавать.", "I like swimming.", "like + V-ing (или to swim)."),
    tr("Переведи:", "They agreed to help us.", "Они согласились помочь нам.", "Они согласились помочь нам.", "agree + to V1."),
)

topic_bank(
    "passive_basic",
    mcq(
        "Выбери Passive.",
        "This letter ____ written by Anna.",
        "Это письмо написано Анной.",
        ["was", "were", "is being", "has"],
        "was",
        "was/were + V3.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Английский говорят во многих странах.",
        [
            "English is spoken in many countries.",
            "English is speak in many countries.",
            "English spoken in many countries.",
            "English are spoken in many countries.",
        ],
        "English is spoken in many countries.",
        "is + V3.",
    ),
    mcq(
        "Выбери V3.",
        "The cake was ____ by my mum.",
        "Торт был сделан мамой.",
        ["made", "make", "making", "makes"],
        "made",
        "make → made.",
    ),
    wf("Напиши is/are/was/were.", "These phones ____ (be) made in China.", "Эти телефоны сделаны в Китае.", "be", "are", "phones → are + V3."),
    wf("Напиши V3.", "The window was ____ (break) yesterday.", "Окно разбили вчера.", "break", "broken", "break → broken."),
    wf("Напиши isn't/aren't.", "The museum ____ (not be) open on Mondays.", "Музей не открыт по понедельникам.", "not be", "isn't", "Passive Present."),
    te("Переведи (Passive):", "Дверь была открыта.", "The door was opened.", "was + V3."),
    tr("Переведи:", "The book was written in 1990.", "Книга была написана в 1990.", "Книга была написана в 1990.", "was written."),
)

topic_bank(
    "relative_clauses_b1",
    mcq(
        "Выбери who/which/that.",
        "The woman ____ lives next door is a doctor.",
        "Женщина, которая живёт рядом, — врач.",
        ["who", "which", "where", "whose"],
        "who",
        "люди → who.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Книга, которую я читаю, интересная.",
        [
            "The book which I am reading is interesting.",
            "The book who I am reading is interesting.",
            "The book where I am reading is interesting.",
            "The book whose I am reading is interesting.",
        ],
        "The book which I am reading is interesting.",
        "вещи → which/that.",
    ),
    mcq(
        "Выбери whose.",
        "This is the man ____ car was stolen.",
        "Это мужчина, чью машину украли.",
        ["whose", "who", "which", "whom"],
        "whose",
        "чьё → whose.",
    ),
    wf("Напиши who или which.", "The dog ____ (which) barked is mine.", "Собака, которая лаяла, моя.", "which", "which", "животные/вещи → which."),
    wf("Напиши where.", "This is the city ____ I was born.", "Это город, где я родился.", "", "where", "место → where."),
    wf("Напиши that/who.", "People ____ help others are kind.", "Люди, которые помогают…", "", "who", "people → who."),
    te("Переведи:", "Это дом, в котором я живу.", "This is the house where I live.", "where для места."),
    tr("Переведи:", "The girl who called you is my sister.", "Девушка, которая тебе звонила, — моя сестра.", "Девушка, которая тебе звонила, — моя сестра.", "who."),
)

# B2
topic_bank(
    "present_perfect_continuous",
    mcq(
        "Выбери Present Perfect Continuous.",
        "I ____ been waiting for an hour.",
        "Я жду уже час.",
        ["have", "has", "had", "am"],
        "have",
        "have/has been + V-ing.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Она учит английский уже два года.",
        [
            "She has been learning English for two years.",
            "She have been learning English for two years.",
            "She has been learn English for two years.",
            "She is learning English for two years.",
        ],
        "She has been learning English for two years.",
        "has been + V-ing + for.",
    ),
    mcq(
        "Выбери for или since.",
        "They have been working here ____ Monday.",
        "Они работают здесь с понедельника.",
        ["since", "for", "from", "at"],
        "since",
        "since + точка.",
    ),
    wf("Напиши have/has.", "He ____ (have) been running all morning.", "Он бегает всё утро.", "have", "has", "he → has."),
    wf("Напиши V-ing.", "We have been ____ (talk) for hours.", "Мы говорим уже часы.", "talk", "talking", "been + V-ing."),
    wf("Напиши haven't/hasn't.", "She ____ (not have) been feeling well.", "Она плохо себя чувствует.", "not have", "hasn't", "hasn't been + V-ing."),
    te("Переведи:", "Я читаю с утра.", "I have been reading since morning.", "have been + V-ing."),
    tr("Переведи:", "It has been raining all day.", "Весь день идёт дождь.", "Весь день идёт дождь.", "has been raining."),
)

topic_bank(
    "conditionals_2_3",
    mcq(
        "Выбери Second Conditional.",
        "If I ____ rich, I would travel the world.",
        "Если бы я был богат, я бы путешествовал.",
        ["were", "was", "am", "will be"],
        "were",
        "If + Past, would + V1 (were для всех).",
    ),
    mcq(
        "Выбери Third Conditional.",
        "If she had studied, she ____ passed.",
        "Если бы она училась, она бы сдала.",
        ["would have", "would", "will have", "had"],
        "would have",
        "If + Past Perfect, would have + V3.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Если бы у меня было время, я бы помог.",
        [
            "If I had time, I would help.",
            "If I have time, I would help.",
            "If I had time, I will help.",
            "If I would have time, I helped.",
        ],
        "If I had time, I would help.",
        "Second Conditional.",
    ),
    wf("Напиши would.", "If I lived closer, I ____ (visit) more often.", "Если бы жил ближе…", "visit", "would visit", "would + V1."),
    wf("Напиши had + V3.", "If we ____ (leave) earlier, we would have caught the train.", "Если бы уехали раньше…", "leave", "had left", "Third: had + V3."),
    wf("Напиши would have.", "He ____ (pass) if he had tried harder.", "Он бы сдал…", "pass", "would have passed", "would have + V3."),
    te("Переведи:", "Если бы я знал, я бы сказал.", "If I knew, I would tell.", "Second Conditional."),
    tr("Переведи:", "If I had known, I would have called.", "Если бы я знал, я бы позвонил.", "Если бы я знал, я бы позвонил.", "Third Conditional."),
)

topic_bank(
    "reported_speech",
    mcq(
        "Выбери Reported Speech.",
        "She said she ____ tired.",
        "Она сказала, что устала.",
        ["was", "is", "were", "be"],
        "was",
        "Present → Past при согласовании времён.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Он сказал, что живёт в Париже.",
        [
            "He said that he lived in Paris.",
            "He said that he lives in Paris.",
            "He said that he live in Paris.",
            "He told that he lived in Paris.",
        ],
        "He said that he lived in Paris.",
        "said that + Past.",
    ),
    mcq(
        "Выбери местоимение.",
        "Tom said, 'I am busy.' → Tom said that ____ was busy.",
        "Том сказал, что занят.",
        ["he", "I", "she", "they"],
        "he",
        "I → he.",
    ),
    wf("Напиши Past форму.", "She said she ____ (can) swim.", "Она сказала, что умеет плавать.", "can", "could", "can → could."),
    wf("Напиши will→would.", "He said he ____ (will) call later.", "Он сказал, что позвонит.", "will", "would", "will → would."),
    wf("Напиши told или said.", "She ____ me that she was ready.", "Она сказала мне…", "", "told", "told + object."),
    te("Переведи:", "Она сказала, что устала.", "She said that she was tired.", "said that + Past."),
    tr("Переведи:", "He told me he had finished.", "Он сказал мне, что закончил.", "Он сказал мне, что закончил.", "told me."),
)

topic_bank(
    "passives_advanced",
    mcq(
        "Выбери сложный Passive.",
        "The problem is being ____ now.",
        "Проблему сейчас решают.",
        ["discussed", "discuss", "discussing", "discusses"],
        "discussed",
        "is being + V3.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Ему дали подарок.",
        [
            "He was given a present.",
            "He was gave a present.",
            "He given a present.",
            "A present was gave him.",
        ],
        "He was given a present.",
        "was + V3 (ditransitive).",
    ),
    mcq(
        "Выбери форму.",
        "The documents have been ____.",
        "Документы были подписаны.",
        ["signed", "sign", "signing", "signs"],
        "signed",
        "have been + V3.",
    ),
    wf("Напиши being + V3.", "The house is being ____ (paint).", "Дом красят.", "paint", "painted", "is being painted."),
    wf("Напиши been + V3.", "All tickets have been ____ (sell).", "Все билеты проданы.", "sell", "sold", "have been sold."),
    wf("Напиши was/were.", "I ____ (be) told to wait.", "Мне сказали ждать.", "be", "was", "I was told."),
    te("Переведи:", "Отчёт должен быть отправлен завтра.", "The report must be sent tomorrow.", "modal + be + V3."),
    tr("Переведи:", "The decision has been made.", "Решение принято.", "Решение принято.", "has been made."),
)

topic_bank(
    "modals_deduction",
    mcq(
        "Выбери модальный вывод.",
        "He ____ be at home — the lights are on.",
        "Он, должно быть, дома — свет горит.",
        ["must", "can't", "should", "may not"],
        "must",
        "уверенность → must.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Она не может быть усталой — она только начала.",
        [
            "She can't be tired — she's just started.",
            "She mustn't be tired — she's just started.",
            "She must not to be tired.",
            "She can't to be tired.",
        ],
        "She can't be tired — she's just started.",
        "невозможно → can't.",
    ),
    mcq(
        "Выбери might.",
        "They ____ be late — the traffic is bad.",
        "Они, возможно, опоздают.",
        ["might", "must", "can't", "should"],
        "might",
        "вероятность → might/may.",
    ),
    wf("Напиши must/can't/might.", "That ____ (must) be a joke.", "Это, должно быть, шутка.", "must", "must", "must be."),
    wf("Напиши have.", "She must ____ (have) forgotten.", "Она, должно быть, забыла.", "have", "have", "must have + V3."),
    wf("Напиши been.", "He can't have ____ (be) serious.", "Он не мог быть серьёзным.", "be", "been", "can't have been."),
    te("Переведи:", "Это, должно быть, правда.", "That must be true.", "must be."),
    tr("Переведи:", "She might have left already.", "Она, возможно, уже ушла.", "Она, возможно, уже ушла.", "might have + V3."),
)

topic_bank(
    "relative_advanced",
    mcq(
        "Выбери non-defining clause.",
        "My brother, ____ lives in Berlin, is a designer.",
        "Мой брат, который живёт в Берлине, дизайнер.",
        ["who", "that", "which", "whom"],
        "who",
        "после запятой that нельзя.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Париж, который я посетил, прекрасен.",
        [
            "Paris, which I visited, is beautiful.",
            "Paris, that I visited, is beautiful.",
            "Paris which I visited is beautiful.",
            "Paris, who I visited, is beautiful.",
        ],
        "Paris, which I visited, is beautiful.",
        "non-defining: which + commas.",
    ),
    mcq(
        "Выбери whom/who.",
        "The colleague with ____ I work is helpful.",
        "Коллега, с которым я работаю…",
        ["whom", "which", "whose", "where"],
        "whom",
        "после предлога → whom.",
    ),
    wf("Напиши which.", "The report, ____ was late, annoyed the boss.", "Отчёт, который опоздал…", "", "which", "which + commas."),
    wf("Напиши whose.", "The author ____ novel won a prize is here.", "Автор, чей роман…", "", "whose", "whose."),
    wf("Напиши to whom / who.", "The person ____ I spoke was polite. (formal: to whom)", "", "", "to whom", "formal: to whom."),
    te("Переведи:", "Мой друг, который живёт в Италии, приезжает.", "My friend, who lives in Italy, is coming.", "non-defining who."),
    tr("Переведи:", "The hotel, which is near the station, is cheap.", "Отель, который рядом с вокзалом, дешёвый.", "Отель, который рядом с вокзалом, дешёвый.", "which."),
)

# C1
topic_bank(
    "inversion",
    mcq(
        "Выбери инверсию.",
        "Rarely ____ such a beautiful view.",
        "Редко я видел такой вид.",
        ["have I seen", "I have seen", "I saw", "did I saw"],
        "have I seen",
        "Rarely + вспомогательный + subject.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Никогда раньше я не чувствовал себя так.",
        [
            "Never before have I felt like this.",
            "Never before I have felt like this.",
            "Never before I felt like this.",
            "Never before did I felt like this.",
        ],
        "Never before have I felt like this.",
        "Never + inversion.",
    ),
    mcq(
        "Выбери форму.",
        "Not only ____ late, but he also forgot the keys.",
        "Он не только опоздал…",
        ["was he", "he was", "did he was", "he"],
        "was he",
        "Not only + inversion.",
    ),
    wf("Напиши инверсию do/does/did.", "Only then ____ (do) I understand.", "Только тогда я понял.", "do", "did", "Only then + did."),
    wf("Напиши have/had.", "Hardly ____ (have) we arrived when it started to rain.", "Едва мы приехали…", "have", "had", "Hardly had…"),
    wf("Напиши should.", "Should you ____ (need) help, call me.", "Если понадобится помощь…", "need", "need", "Should you need…"),
    te("Переведи:", "Никогда я не видел ничего подобного.", "Never have I seen anything like this.", "Never + inversion."),
    tr("Переведи:", "Seldom do we meet such kindness.", "Редко мы встречаем такую доброту.", "Редко мы встречаем такую доброту.", "Seldom do…"),
)

topic_bank(
    "cleft_sentences",
    mcq(
        "Выбери cleft sentence.",
        "____ was John who called you.",
        "Именно Джон тебе звонил.",
        ["It", "That", "There", "This"],
        "It",
        "It was X who/that…",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Именно в пятницу мы уезжаем.",
        [
            "It is on Friday that we are leaving.",
            "It is on Friday which we are leaving.",
            "It on Friday that we are leaving.",
            "Is it on Friday we leaving.",
        ],
        "It is on Friday that we are leaving.",
        "It is + focus + that…",
    ),
    mcq(
        "Выбери What-cleft.",
        "____ I need is a quiet place.",
        "Что мне нужно — тихое место.",
        ["What", "That", "Which", "Who"],
        "What",
        "What I need is…",
    ),
    wf("Напиши who/that.", "It was Maria ____ helped me.", "Именно Мария помогла.", "", "who", "who для людей."),
    wf("Напиши that.", "It was yesterday ____ everything changed.", "Именно вчера всё изменилось.", "", "that", "that после времени."),
    wf("Напиши is/was.", "What matters ____ honesty.", "Что важно — честность.", "", "is", "What… is…"),
    te("Переведи:", "Именно ты должен решить.", "It is you who must decide.", "It is you who…"),
    tr("Переведи:", "What surprised me was his honesty.", "Что меня удивило — его честность.", "Что меня удивило — его честность.", "What… was…"),
)

topic_bank(
    "advanced_modals",
    mcq(
        "Выбери модальность.",
        "You ____ have told me earlier!",
        "Тебе следовало сказать раньше!",
        ["should", "must", "can", "will"],
        "should",
        "should have + V3 — упрёк.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Мне не нужно было приходить (но я пришёл).",
        [
            "I needn't have come.",
            "I didn't need to come.",
            "I mustn't have come.",
            "I shouldn't come have.",
        ],
        "I needn't have come.",
        "needn't have = сделал зря.",
    ),
    mcq(
        "Выбери форму.",
        "She ____ have been at the meeting — I saw her.",
        "Она, должно быть, была на встрече.",
        ["must", "should", "can't", "would"],
        "must",
        "must have + V3 — вывод о прошлом.",
    ),
    wf("Напиши have.", "You should ____ (have) asked for help.", "Тебе следовало попросить помощи.", "have", "have", "should have + V3."),
    wf("Напиши been.", "He might have ____ (be) joking.", "Он, возможно, шутил.", "be", "been", "might have been."),
    wf("Напиши needn't.", "You ____ (need not) have bought so much food.", "Не нужно было столько еды покупать.", "need not", "needn't", "needn't have."),
    te("Переведи:", "Тебе не следовало врать.", "You shouldn't have lied.", "shouldn't have + V3."),
    tr("Переведи:", "They must have left already.", "Они, должно быть, уже ушли.", "Они, должно быть, уже ушли.", "must have."),
)

topic_bank(
    "participle_clauses",
    mcq(
        "Выбери participle clause.",
        "____ the door, she left the room.",
        "Закрыв дверь, она вышла.",
        ["Closing", "Closed", "Close", "Closes"],
        "Closing",
        "V-ing = одновременное действие.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Написав письмо, он отправил его.",
        [
            "Having written the letter, he sent it.",
            "Writing the letter, he has sent it.",
            "Written the letter, he send it.",
            "Having write the letter, he sent it.",
        ],
        "Having written the letter, he sent it.",
        "Having + V3 — раньше.",
    ),
    mcq(
        "Выбери форму.",
        "The man ____ by the window is my uncle.",
        "Мужчина, сидящий у окна — мой дядя.",
        ["sitting", "sat", "sits", "sit"],
        "sitting",
        "reduced relative: sitting.",
    ),
    wf("Напиши V-ing.", "____ (Look) at the map, I found the street.", "Глядя на карту…", "Look", "Looking", "Looking…"),
    wf("Напиши Having + V3.", "____ (finish) dinner, we went for a walk.", "Поужинав…", "finish", "Having finished", "Having + V3."),
    wf("Напиши V3 participle.", "____ (Build) in 1890, the house is historic.", "Построенный в 1890…", "Build", "Built", "Built in…"),
    te("Переведи:", "Открыв окно, она вдохнула свежий воздух.", "Opening the window, she breathed fresh air.", "V-ing clause."),
    tr("Переведи:", "Shocked by the news, he sat down.", "Потрясённый новостью, он сел.", "Потрясённый новостью, он сел.", "V3 clause."),
)

topic_bank(
    "nominalisation",
    mcq(
        "Выбери номинализацию.",
        "The ____ of the project took two years.",
        "Разработка проекта заняла два года.",
        ["development", "develop", "developing", "developed"],
        "development",
        "глагол → существительное.",
    ),
    mcq(
        "Выбери более формальный вариант.",
        "Which is more formal?",
        "",
        [
            "There was a significant increase in sales.",
            "Sales went up a lot.",
            "Sales got bigger.",
            "Sales jumped up.",
        ],
        "There was a significant increase in sales.",
        "increase = номинализация.",
    ),
    mcq(
        "Выбери существительное.",
        "Her sudden ____ surprised everyone.",
        "Её внезапный уход всех удивил.",
        ["departure", "depart", "departing", "departed"],
        "departure",
        "depart → departure.",
    ),
    wf("Напиши существительное.", "The ____ (decide) was difficult.", "Решение было трудным.", "decide", "decision", "decide → decision."),
    wf("Напиши существительное.", "We need a clear ____ (explain).", "Нужно ясное объяснение.", "explain", "explanation", "explain → explanation."),
    wf("Напиши существительное.", "His ____ (refuse) shocked us.", "Его отказ нас шокировал.", "refuse", "refusal", "refuse → refusal."),
    te("Переведи формально:", "Продажи сильно выросли.", "There was a sharp rise in sales.", "rise = существительное."),
    tr("Переведи:", "The failure of the plan was obvious.", "Провал плана был очевиден.", "Провал плана был очевиден.", "failure."),
)

topic_bank(
    "discourse_markers",
    mcq(
        "Выбери связку.",
        "I was tired. ____, I finished the work.",
        "Я устал. Тем не менее, закончил работу.",
        ["Nevertheless", "Because", "So that", "Unless"],
        "Nevertheless",
        "Nevertheless = тем не менее.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Кроме того, это дёшево.",
        [
            "Moreover, it is cheap.",
            "Moreover it cheap.",
            "Moreover, it cheap is.",
            "Moreover it is cheaply.",
        ],
        "Moreover, it is cheap.",
        "Moreover + comma.",
    ),
    mcq(
        "Выбери маркер результата.",
        "It rained hard. ____, the match was cancelled.",
        "Шёл сильный дождь. Поэтому матч отменили.",
        ["Therefore", "Although", "Whereas", "Despite"],
        "Therefore",
        "Therefore = поэтому.",
    ),
    wf("Напиши However.", "I like the idea. ____, it is expensive.", "Идея нравится. Однако дорого.", "", "However", "However,"),
    wf("Напиши Although.", "____ it was late, we continued.", "Хотя было поздно…", "", "Although", "Although + clause."),
    wf("Напиши In addition.", "____, we need more time.", "Кроме того, нужно больше времени.", "", "In addition", "In addition,"),
    te("Переведи:", "Тем не менее, я согласен.", "Nevertheless, I agree.", "Nevertheless,"),
    tr("Переведи:", "As a result, prices rose.", "В результате цены выросли.", "В результате цены выросли.", "As a result."),
)

# C2
topic_bank(
    "stylistic_inversion",
    mcq(
        "Выбери стилистическую инверсию.",
        "So rare ____ the opportunity that we took it.",
        "Возможность была столь редкой, что мы ею воспользовались.",
        ["was", "it was", "is", "were it"],
        "was",
        "So + adj + verb + subject.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Такова была его реакция.",
        [
            "Such was his reaction.",
            "Such his reaction was.",
            "Such was reaction his.",
            "His reaction such was.",
        ],
        "Such was his reaction.",
        "Such was…",
    ),
    mcq(
        "Выбери форму.",
        "Little ____ he know what was coming.",
        "Мало он знал, что будет.",
        ["did", "does", "was", "had"],
        "did",
        "Little did he know…",
    ),
    wf("Напиши did.", "Not until midnight ____ (do) they leave.", "Только в полночь они ушли.", "do", "did", "Not until… did…"),
    wf("Напиши had.", "No sooner ____ (have) I sat down than the phone rang.", "Едва я сел…", "have", "had", "No sooner had…"),
    wf("Напиши comes.", "Here ____ the bus!", "Вот и автобус!", "", "comes", "Here comes…"),
    te("Переведи:", "Мало он понимал опасность.", "Little did he understand the danger.", "Little did…"),
    tr("Переведи:", "Such was the impact of her words.", "Таково было влияние её слов.", "Таково было влияние её слов.", "Such was…"),
)

topic_bank(
    "subtle_modality",
    mcq(
        "Выбери тонкую модальность.",
        "You ____ want to check the figures again.",
        "Возможно, тебе стоит ещё раз проверить цифры.",
        ["might", "must", "shall", "needn't"],
        "might",
        "вежливый совет → might want to.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Кажется, он опоздал.",
        [
            "He appears to have been late.",
            "He appears to be late yesterday.",
            "He appears late have been.",
            "He appear to have been late.",
        ],
        "He appears to have been late.",
        "appears to have + V3.",
    ),
    mcq(
        "Выбери would.",
        "I ____ imagine that's the best option.",
        "Полагаю, это лучший вариант.",
        ["would", "must", "can", "shall"],
        "would",
        "I would imagine… — мягко.",
    ),
    wf("Напиши seem.", "They ____ (seem) to be avoiding us.", "Кажется, они нас избегают.", "seem", "seem", "seem to…"),
    wf("Напиши tend.", "She ____ (tend) to overthink things.", "Она склонна усложнять.", "tend", "tends", "tends to."),
    wf("Напиши may well.", "He ____ be right.", "Он вполне может быть прав.", "", "may well", "may well + V1."),
    te("Переведи мягко:", "Возможно, стоит подождать.", "You might want to wait.", "might want to."),
    tr("Переведи:", "She would appear to be mistaken.", "Похоже, она ошибается.", "Похоже, она ошибается.", "would appear."),
)

topic_bank(
    "mixed_conditionals",
    mcq(
        "Выбери mixed conditional.",
        "If I had taken that job, I ____ rich now.",
        "Если бы я тогда взял работу, сейчас был бы богат.",
        ["would be", "would have been", "will be", "am"],
        "would be",
        "прошлое условие → настоящий результат.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Если бы он был умнее, он бы не сделал ту ошибку.",
        [
            "If he were smarter, he wouldn't have made that mistake.",
            "If he is smarter, he wouldn't have made that mistake.",
            "If he were smarter, he won't make that mistake.",
            "If he had been smarter, he wouldn't make that mistake yesterday only.",
        ],
        "If he were smarter, he wouldn't have made that mistake.",
        "настоящее условие → прошлый результат.",
    ),
    mcq(
        "Выбери форму.",
        "If she ____ more careful, she wouldn't be in trouble now.",
        "Если бы она была осторожнее…",
        ["had been", "was being", "is", "would be"],
        "had been",
        "Past Perfect в if + would now.",
    ),
    wf("Напиши would be.", "If I had saved money, I ____ freer now.", "Если бы копил, сейчас был бы свободнее.", "", "would be", "mixed."),
    wf("Напиши had + V3.", "If he ____ (listen), he wouldn't be lost now.", "Если бы послушал…", "listen", "had listened", "had + V3."),
    wf("Напиши wouldn't have.", "If I were you, I ____ (not say) that yesterday.", "На твоём месте я бы того не сказал.", "not say", "wouldn't have said", "mixed."),
    te("Переведи:", "Если бы я тогда учился, сейчас у меня была бы работа.", "If I had studied then, I would have a job now.", "mixed conditional."),
    tr(
        "Переведи:",
        "If I were taller, I would have joined the team last year.",
        "Если бы я был выше, я бы вступил в команду в прошлом году.",
        "Если бы я был выше, я бы вступил в команду в прошлом году.",
        "mixed.",
    ),
)

topic_bank(
    "ellipsis_substitution",
    mcq(
        "Выбери эллипсис/замену.",
        "I like tea and so ____ my sister.",
        "Я люблю чай, и сестра тоже.",
        ["does", "is", "likes", "do"],
        "does",
        "so + auxiliary + subject.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Я тоже не хочу.",
        [
            "Neither do I.",
            "Neither I do.",
            "So do I not.",
            "I neither.",
        ],
        "Neither do I.",
        "Neither + aux + subject.",
    ),
    mcq(
        "Выбери one/ones.",
        "I need a pen. Pass me the blue ____.",
        "Мне нужна ручка. Передай синюю.",
        ["one", "ones", "it", "them"],
        "one",
        "one заменяет существительное.",
    ),
    wf("Напиши do/does/did.", "She works hard and so ____ he.", "Она много работает, и он тоже.", "", "does", "so does he."),
    wf("Напиши one.", "Which bag do you want? The red ____.", "Какую сумку? Красную.", "", "one", "the red one."),
    wf("Напиши so.", "A: I'm tired. B: ____ am I.", "Я тоже.", "", "So", "So am I."),
    te("Переведи:", "Я тоже.", "So do I.", "So + aux + I."),
    tr("Переведи:", "Neither have we.", "Мы тоже нет.", "Мы тоже нет.", "Neither…"),
)

topic_bank(
    "register_control",
    mcq(
        "Выбери более формальный вариант.",
        "Which is more formal?",
        "",
        [
            "I would be grateful if you could reply soon.",
            "Can you reply ASAP?",
            "Reply quick, yeah?",
            "Hit me up soon.",
        ],
        "I would be grateful if you could reply soon.",
        "формальный регистр.",
    ),
    mcq(
        "Выбери нейтральный деловой тон.",
        "Which sentence fits a work email?",
        "",
        [
            "Please find attached the report.",
            "Here's the stuff lol.",
            "I dumped the file here.",
            "Yo, check this.",
        ],
        "Please find attached the report.",
        "деловая формула.",
    ),
    mcq(
        "Выбери смягчение.",
        "____ you open the window?",
        "Не могли бы вы открыть окно?",
        ["Could", "Open", "You must", "Hey"],
        "Could",
        "Could you…? вежливо.",
    ),
    wf("Напиши We regret.", "____ to inform you that the event is cancelled.", "К сожалению сообщаем…", "", "We regret", "We regret to…"),
    wf("Напиши further.", "Should you require ____ information, contact us.", "Если нужна доп. информация…", "", "further", "further information."),
    wf("Напиши Appreciate.", "We ____ your patience.", "Мы ценим ваше терпение.", "", "appreciate", "We appreciate…"),
    te("Переведи формально:", "Напишите нам как можно скорее.", "Please contact us at your earliest convenience.", "формальный клише."),
    tr("Переведи:", "I look forward to hearing from you.", "С нетерпением жду вашего ответа.", "С нетерпением жду вашего ответа.", "look forward to."),
)

topic_bank(
    "pragmatic_softening",
    mcq(
        "Выбери смягчённую формулировку.",
        "Which is softer?",
        "",
        [
            "I was wondering if you could help.",
            "Help me now.",
            "You have to help.",
            "Help!",
        ],
        "I was wondering if you could help.",
        "I was wondering if… — мягко.",
    ),
    mcq(
        "Выбери правильное предложение.",
        "Which sentence is correct?",
        "Как бы неловко сказать…",
        [
            "This might sound awkward, but…",
            "This might sounding awkward, but…",
            "This must sound awkwardly, but…",
            "This can sounds awkward, but…",
        ],
        "This might sound awkward, but…",
        "might sound — смягчение.",
    ),
    mcq(
        "Выбери hedged opinion.",
        "____ say that the plan needs work.",
        "Я бы сказал, что план нужно доработать.",
        ["I'd", "I must", "I will", "I"],
        "I'd",
        "I'd say…",
    ),
    wf("Напиши perhaps.", "____ we could meet tomorrow.", "Возможно, встретимся завтра.", "", "Perhaps", "Perhaps…"),
    wf("Напиши sort of.", "It's ____ complicated.", "Это вроде как сложно.", "", "sort of", "sort of."),
    wf("Напиши seem.", "You ____ a bit upset.", "Ты выглядишь немного расстроенным.", "", "seem", "You seem…"),
    te("Переведи мягко:", "Мне кажется, это ошибка.", "It seems to me that this is a mistake.", "It seems to me…"),
    tr("Переведи:", "Would you mind closing the door?", "Вы не против закрыть дверь?", "Вы не против закрыть дверь?", "Would you mind…"),
)

# Also keep strong A0/A1 banks that already exist — re-declare key ones for merge completeness
# pronouns_be, there_is_are, can_ability, plurals stay in original file unless we override.

text = '''# -*- coding: utf-8 -*-
"""Curated grammar exercise banks (8 per topic). Preferred over GPT."""

EXTRA_FALLBACKS = ''' + json.dumps(BANKS, ensure_ascii=False, indent=2) + "\n"

# json.dumps makes True/False/None wrong for Python — fix
text = text.replace(": null", ": None").replace(": true", ": True").replace(": false", ": False")

OUT.write_text(text, encoding="utf-8")
print(f"Wrote {OUT} with {len(BANKS)} topics")
for k, v in sorted(BANKS.items()):
    print(f"  {k}: {len(v)}")
