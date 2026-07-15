"""
Грамматические темы по уровням A0–C2.
Каждая тема: id, title, rico_intro (подробное объяснение от Рико).
"""

from __future__ import annotations

from data.grammar_enrichments import GRAMMAR_SECTION_INTRO, get_enrichment
from data.grammar_narratives import get_narrative_intro

# Структура: LEVEL -> list[{id, title, rico_intro}]

GRAMMAR_BY_LEVEL: dict[str, list[dict]] = {
    "A0": [
        {
            "id": "alphabet",
            "title": "Alphabet / Алфавит",
            "mode": "ack",
            "rico_intro": (
                "🦜 <b>Рико:</b> Эй, дружище! 👋 Рад, что мы начинаем с алфавита — "
                "это самый честный и правильный старт! 🌱\n\n"
                "В английском <b>26 букв</b> — те же, что ты видишь на клавиатуре:\n"
                "<b>A B C D E F G H I J K L M N O P Q R S T U V W X Y Z</b>\n\n"
                "У каждой буквы есть <b>название</b> (как «эм» у русской М):\n"
                "A = /eɪ/ «эй», B = /biː/ «би», C = /siː/ «си»…\n\n"
                "<b>Зачем это тебе?</b> 🤔\n"
                "• диктовать имя, email, пароль по буквам\n"
                "• читать слова вслух правильно\n"
                "• понимать, когда тебе «произносят» буквы\n\n"
                "<b>Гласные (vowels):</b> A, E, I, O, U — иногда ещё Y (my, yes).\n"
                "<b>Согласные (consonants):</b> все остальные.\n\n"
                "<b>Пример в жизни:</b>\n"
                "— How do you spell your name?\n"
                "<i>— Как по буквам пишется твоё имя?</i>\n"
                "— D-A-N-I-L.\n"
                "<i>— Д-А-Н-И-Л.</i>\n\n"
                "— What's your email?\n"
                "<i>— Какой у тебя email?</i>\n"
                "— d-a-n at gmail dot com.\n"
                "<i>— d-a-n «собака» gmail «точка» com.</i>\n\n"
                "Здесь <b>не нужны задания</b> — просто прочитай, посмотри примеры "
                "и жми <b>✅ Ознакомился</b>. Тема засчитается! 🎉"
            ),
        },
        {
            "id": "numbers_1_20",
            "title": "Numbers 1–20 / Цифры 1–20",
            "mode": "ack",
            "rico_intro": (
                "🦜 <b>Рико:</b> Цифры — must-have с первого дня!\n\n"
                "1 one, 2 two, 3 three, 4 four, 5 five, 6 six, 7 seven, 8 eight, 9 nine, 10 ten,\n"
                "11 eleven, 12 twelve, 13 thirteen, 14 fourteen, 15 fifteen,\n"
                "16 sixteen, 17 seventeen, 18 eighteen, 19 nineteen, 20 twenty.\n\n"
                "<b>Зачем?</b> возраст, цена, номер телефона, время позже.\n\n"
                "Полезные фразы:\n"
                "• How old are you? — I’m …\n"
                "<i>• Сколько тебе лет? — Мне …</i>\n"
                "• What’s your number?\n"
                "<i>• Какой у тебя номер?</i>\n\n"
                "Заданий нет — жми <b>✅ Ознакомился</b>, и тема в зачёт.\n"
                "Пиши вопросы текстом — разберём вместе! 🦜"
            ),
        },
        {
            "id": "pronouns_be",
            "title": "I / You + to be / Я есть…",
            "mode": "practice",
            "rico_intro": (
                "🦜 <b>Рико:</b> Самый важный глагол на старте — <b>to be</b> (быть)!\n\n"
                "Сейчас (Present):\n"
                "• I <b>am</b>\n"
                "• you <b>are</b>\n"
                "• he/she/it <b>is</b>\n"
                "• we/you/they <b>are</b>\n\n"
                "Примеры:\n"
                "• I am Danil.\n"
                "<i>• Я — Данил. / Меня зовут Данил.</i>\n"
                "• She is a student.\n"
                "<i>• Она студентка.</i>\n"
                "• They are friends.\n"
                "<i>• Они друзья.</i>\n\n"
                "Отрицание: I’m not / isn’t / aren’t.\n"
                "Вопрос: Am I…? Is she…? Are you…?\n\n"
                "После заданий откроется тест по теме.\n"
                "💡 В заданиях я помогаю: 1-я подсказка — намёк, 2-я — уже ответ "
                "(и задание засчитывается). В тесте — только 2 подсказки.\n"
                "Пиши вопросы текстом! ✨"
            ),
        },
        {
            "id": "this_that",
            "title": "This / That / Это / То",
            "mode": "practice",
            "rico_intro": (
                "🦜 <b>Рико:</b>\n\n"
                "<b>This</b> — это (близко), <b>That</b> — то (дальше).\n\n"
                "• This is a book.\n"
                "<i>• Это книга. (книга рядом)</i>\n"
                "• That is a car.\n"
                "<i>• То — машина. (машина вон там)</i>\n\n"
                "Вопросы:\n"
                "What’s this? / What’s that?\n"
                "<i>Что это? / Что это там?</i>\n\n"
                "Дальше — задания, потом тест. Вопросы пиши мне сюда текстом 🦜"
            ),
        },
        {
            "id": "simple_phrases",
            "title": "Simple phrases / Простые фразы",
            "mode": "practice",
            "rico_intro": (
                "🦜 <b>Рико:</b> Собираем первые «живые» фразы!\n\n"
                "• Hello! / Hi!\n"
                "<i>• Привет!</i>\n"
                "• What’s your name? — My name is…\n"
                "<i>• Как тебя зовут? — Меня зовут…</i>\n"
                "• Nice to meet you.\n"
                "<i>• Приятно познакомиться.</i>\n"
                "• Thank you. / Please. / Sorry.\n"
                "<i>• Спасибо. / Пожалуйста. / Извини.</i>\n"
                "• How are you? — I’m fine.\n"
                "<i>• Как дела? — Хорошо.</i>\n\n"
                "Это каркас вежливого общения. Дальше — задания и тест.\n"
                "Я рядом, пиши текстом! ✨"
            ),
        },
    ],
    "A1": [
        {
            "id": "present_simple",
            "title": "Present Simple",
            "rico_intro": (
                "🦜 <b>Рико:</b> Present Simple — король уровня A1!\n\n"
                "<b>Когда используем:</b>\n"
                "• привычки и факты: I go to school every day.\n"
                "• постоянные ситуации: She lives in Moscow.\n\n"
                "<b>Формула:</b> I/you/we/they + V1 · he/she/it + V1<b>s/es</b>\n"
                "• I like tea. / He like<b>s</b> tea.\n\n"
                "<b>Отрицание:</b> don’t / doesn’t + V1\n"
                "• I don’t like coffee. / She doesn’t play football.\n\n"
                "<b>Вопрос:</b> Do/Does + subject + V1?\n"
                "• Do you speak English? — Yes, I do.\n\n"
                "Частые слова-подсказки: always, usually, often, sometimes, never, every day.\n\n"
                "⚠️ После he/she/it почти всегда -s (goes, watches, studies).\n\n"
                "После заданий откроется тест. В заданиях помогаю всегда, в тесте — 2 раза.\n"
                "Спрашивай тонкости прямо здесь! 🦜"
            ),
        },
        {
            "id": "articles_a_an",
            "title": "Articles a / an",
            "rico_intro": (
                "🦜 <b>Рико:</b> Артикли a/an — мелочь, а путают часто!\n\n"
                "• <b>a</b> + согласный звук: a book, a university (/juː/ — звук согласный!)\n"
                "• <b>an</b> + гласный звук: an apple, an hour (/aʊ/ — h не слышен)\n\n"
                "Говорим о чём-то один раз, неконкретном: I need a pen.\n\n"
                "После заданий будет тест. Пиши вопросы — разберём на примерах!"
            ),
        },
        {
            "id": "plurals",
            "title": "Plurals (мн. число)",
            "rico_intro": (
                "🦜 <b>Рико:</b> Один — book, много — book<b>s</b>.\n\n"
                "Правила:\n"
                "• обычно +s: cats, dogs\n"
                "• -ch/-sh/-x/-s/-o → +es: watches, boxes\n"
                "• согласная + y → ies: city → cities\n"
                "• исключения: child→children, man→men, woman→women\n\n"
                "Тренируем в заданиях, потом тест. Я помогу! 🦜"
            ),
        },
        {
            "id": "there_is_are",
            "title": "There is / There are",
            "rico_intro": (
                "🦜 <b>Рико:</b> Как сказать «есть / находится»?\n\n"
                "• There <b>is</b> + единственное: There is a cat.\n"
                "• There <b>are</b> + множественное: There are two books.\n\n"
                "Отрицание: there isn’t / there aren’t\n"
                "Вопрос: Is there…? Are there…?\n\n"
                "Суперполезно для описания комнаты и города!"
            ),
        },
        {
            "id": "can_ability",
            "title": "Can (умею / могу)",
            "rico_intro": (
                "🦜 <b>Рико:</b> Can = умение или возможность.\n\n"
                "• I can swim.\n"
                "• She can’t drive.\n"
                "• Can you help me?\n\n"
                "После can глагол <b>без to</b>: can go (не can to go).\n\n"
                "Вперёд к заданиям! После них — тест."
            ),
        },
        {
            "id": "numbers_1_100",
            "title": "Numbers 1–100",
            "rico_intro": (
                "🦜 <b>Рико:</b> На A1 расширяем цифры до 100!\n\n"
                "20 twenty, 30 thirty, 40 forty, 50 fifty, 60 sixty, 70 seventy, 80 eighty, 90 ninety, 100 a hundred.\n"
                "21 twenty-one, 45 forty-five…\n\n"
                "Нужны для цен, возраста, номеров.\n\n"
                "Пример:\n"
                "How much is it? — It’s fifty pounds.\n"
                "<i>Сколько это стоит? — Пятьдесят фунтов.</i>\n\n"
                "Заданий нет — жми <b>✅ Ознакомился</b>, тема в зачёт.\n"
                "Вопросы пиши текстом! 🦜"
            ),
        },
    ],
    "A2": [
        {
            "id": "numbers_time_dates",
            "title": "Numbers, time & dates",
            "rico_intro": (
                "🦜 <b>Рико:</b> На A2 цифры уже «живут» во времени и датах!\n\n"
                "• It’s half past two.\n"
                "<i>• Сейчас половина третьего.</i>\n"
                "• It’s a quarter to five.\n"
                "<i>• Без пятнадцати пять.</i>\n"
                "• the 3rd of May / May 3rd\n"
                "<i>• третье мая</i>\n"
                "• 1999 = nineteen ninety-nine\n"
                "• 100 one hundred, 1,000 one thousand\n\n"
                "Полезно для расписаний, билетов, встреч.\n\n"
                "Заданий нет — жми <b>✅ Ознакомился</b>, и тема засчитается.\n"
                "Спрашивай текстом! ✨"
            ),
        },
        {
            "id": "present_continuous",
            "title": "Present Continuous",
            "rico_intro": (
                "🦜 <b>Рико:</b> Present Continuous — «сейчас происходит».\n\n"
                "Формула: am/is/are + V-ing\n"
                "• I am reading now.\n"
                "• They are playing football.\n\n"
                "Vs Present Simple: привычка (I read every day) ≠ сейчас (I am reading now).\n\n"
                "Отрицание: I’m not / isn’t / aren’t + V-ing\n"
                "Вопрос: Are you working?\n\n"
                "После заданий — тест (2 подсказки). Спрашивай меня тут! 🦜"
            ),
        },
        {
            "id": "past_simple",
            "title": "Past Simple",
            "rico_intro": (
                "🦜 <b>Рико:</b> Past Simple — про вчера и «уже случилось».\n\n"
                "• регулярные: work → worked\n"
                "• неправильные: go→went, see→saw, have→had, do→did\n\n"
                "+/−/?:\n"
                "• I visited London.\n"
                "• I didn’t visit Paris. (после didn’t — V1!)\n"
                "• Did you visit Berlin?\n\n"
                "Слова-подсказки: yesterday, last week, ago, in 2020.\n\n"
                "Это ключ к историям. Тренируем → тест."
            ),
        },
        {
            "id": "going_to_future",
            "title": "Going to (планы)",
            "rico_intro": (
                "🦜 <b>Рико:</b> Going to — планы и намерения.\n\n"
                "am/is/are + going to + V1\n"
                "• I’m going to study tonight.\n"
                "• She’s going to buy a car.\n\n"
                "Will тоже бывает, но на A2 часто начинаем с going to для планов.\n\n"
                "Задания ждут! Потом тест."
            ),
        },
        {
            "id": "much_many_some_any",
            "title": "Much / Many / Some / Any",
            "rico_intro": (
                "🦜 <b>Рико:</b>\n\n"
                "• <b>many</b> + countable: many books\n"
                "• <b>much</b> + uncountable: much water (часто в отрицаниях/вопросах)\n"
                "• <b>some</b> в утверждениях: some tea\n"
                "• <b>any</b> в вопросах/отрицаниях: any milk? / I don’t have any.\n\n"
                "Путают все — поэтому закрепляем заданиями!"
            ),
        },
        {
            "id": "comparatives",
            "title": "Comparatives (сравнение)",
            "rico_intro": (
                "🦜 <b>Рико:</b> bigger / more interesting\n\n"
                "• короткие: old → older, big → bigger\n"
                "• длинные: beautiful → more beautiful\n"
                "• good→better, bad→worse\n\n"
                "than: She is taller than me.\n\n"
                "Практика → тест. Я на связи 🦜"
            ),
        },
        {
            "id": "modals_a2",
            "title": "Must / Have to / Should",
            "rico_intro": (
                "🦜 <b>Рико:</b> Модальные на A2:\n\n"
                "• must / have to — должен\n"
                "• should — совет\n"
                "• can — уже знаешь\n\n"
                "You should sleep more. / I have to work tomorrow.\n\n"
                "Разберём в заданиях и тесте!"
            ),
        },
    ],
    "B1": [
        {
            "id": "present_perfect",
            "title": "Present Perfect",
            "rico_intro": (
                "🦜 <b>Рико:</b> Present Perfect — мост между прошлым и настоящим.\n\n"
                "have/has + V3 (Past Participle)\n"
                "• I have visited London. (опыт)\n"
                "• She has lost her keys. (результат важен сейчас)\n\n"
                "Слова: ever, never, already, yet, just, since, for.\n\n"
                "Vs Past Simple: фиксированное время → Past Simple (yesterday).\n"
                "Опыт без точного времени → Present Perfect.\n\n"
                "После заданий откроется тест. В заданиях помогаю всегда, в тесте — 2 раза.\n"
                "Спроси что угодно по теме прямо сейчас! 🦜"
            ),
        },
        {
            "id": "past_perfect",
            "title": "Past Perfect",
            "rico_intro": (
                "🦜 <b>Рико:</b> Past Perfect — «ещё более прошлое»!\n\n"
                "Формула: <b>had + V3</b> (had done, had gone, had seen…)\n"
                "Одинаково для I/you/he/we/they: всегда <b>had</b>.\n\n"
                "<b>Зачем нужно?</b>\n"
                "Когда в прошлом уже было действие №1, а потом действие №2 — "
                "Past Perfect показывает, что было <b>раньше</b>.\n\n"
                "Примеры:\n"
                "• When I arrived, the train <b>had left</b>. "
                "(поезд ушёл раньше, чем я приехал)\n"
                "• She was tired because she <b>had worked</b> all day.\n"
                "• I <b>had never seen</b> snow before that trip.\n\n"
                "Отрицание: hadn’t + V3.\n"
                "Вопрос: Had you … before …?\n\n"
                "Часто рядом слова: before, after, already, by the time, until.\n\n"
                "💡 Не путай с Present Perfect (have/has) — здесь прошлое про прошлое: <b>had</b>.\n\n"
                "После заданий откроется <b>тест</b> по теме.\n"
                "В заданиях я помогаю всегда. В тесте — только <b>2 подсказки</b>.\n"
                "Пиши вопросы сюда — разберём на примерах! ✨"
            ),
        },
        {
            "id": "past_continuous",
            "title": "Past Continuous",
            "rico_intro": (
                "🦜 <b>Рико:</b> Past Continuous = был в процессе.\n\n"
                "was/were + V-ing\n"
                "• I was watching TV at 8.\n"
                "• They were playing when I called.\n\n"
                "Часто вместе с Past Simple: длинное действие + короткое прерывание.\n\n"
                "После заданий — тест. В заданиях помогаю всегда, в тесте — 2 раза.\n"
                "Спрашивай, если что-то мутно! 🦜"
            ),
        },
        {
            "id": "conditionals_0_1",
            "title": "Conditionals 0 & 1",
            "rico_intro": (
                "🦜 <b>Рико:</b> Условные предложения 0 и 1 — «если… то…».\n\n"
                "<b>Zero Conditional:</b> If + Present, Present — законы/привычки\n"
                "If you heat water, it boils.\n\n"
                "<b>First Conditional:</b> If + Present, will + V1 — реальное будущее\n"
                "If it rains, I’ll stay home.\n\n"
                "Запятая после if-части, когда она в начале.\n"
                "Не пиши will сразу после if (ошибка: If it will rain…).\n\n"
                "После заданий откроется тест (2 подсказки в тесте).\n"
                "Пиши вопросы — объясню на твоих примерах! 🦜"
            ),
        },
        {
            "id": "gerund_infinitive",
            "title": "Gerund / Infinitive",
            "rico_intro": (
                "🦜 <b>Рико:</b> V-ing или to V?\n\n"
                "• like/love/enjoy + V-ing: I enjoy reading.\n"
                "• want/decide/hope + to V: I want to go.\n"
                "• stop smoking vs stop to smoke — разный смысл!\n\n"
                "Список глаголов учим через практику.\n"
                "После заданий — тест. Я рядом с подсказками! ✨"
            ),
        },
        {
            "id": "passive_basic",
            "title": "Passive Voice (база)",
            "rico_intro": (
                "🦜 <b>Рико:</b> Passive — когда важен объект действия, а не кто сделал.\n\n"
                "Формула: <b>be + V3</b>\n"
                "• The letter was sent.\n"
                "• English is spoken here.\n\n"
                "Актив: Someone sent the letter.\n"
                "Пассив: The letter was sent.\n\n"
                "После заданий откроется тест. В заданиях помогаю всегда, в тесте — 2 раза.\n"
                "Спроси тонкости прямо здесь! 🦜"
            ),
        },
        {
            "id": "relative_clauses_b1",
            "title": "Relative clauses (who/which/that)",
            "rico_intro": (
                "🦜 <b>Рико:</b> Who / which / that соединяют две идеи в одну умную фразу.\n\n"
                "• who — люди: The man who called you…\n"
                "• which / that — вещи: The book which/that I bought…\n\n"
                "Это делает речь «взрослее» и короче.\n"
                "После практики — тест. Пиши вопросы! 🦜"
            ),
        },
    ],
    "B2": [
        {
            "id": "present_perfect_continuous",
            "title": "Present Perfect Continuous",
            "rico_intro": (
                "🦜 <b>Рико:</b> have/has been + V-ing\n\n"
                "Длительность до сейчас: I have been waiting for an hour.\n"
                "Vs Present Perfect: I’ve written 3 emails (результат) / I’ve been writing emails (процесс).\n\n"
                "После заданий — тест (2 подсказки в тесте)."
            ),
        },
        {
            "id": "conditionals_2_3",
            "title": "Conditionals 2 & 3",
            "rico_intro": (
                "🦜 <b>Рико:</b>\n\n"
                "<b>Second:</b> If + Past, would + V1 — нереально сейчас\n"
                "If I had time, I would travel.\n\n"
                "<b>Third:</b> If + Past Perfect, would have + V3 — нереально в прошлом\n"
                "If I had studied, I would have passed.\n\n"
                "Мощный инструмент для мнений и сожалений!"
            ),
        },
        {
            "id": "reported_speech",
            "title": "Reported Speech",
            "rico_intro": (
                "🦜 <b>Рико:</b> Передаём чужие слова.\n\n"
                "He said (that) he was tired.\n"
                "She told me she had finished.\n\n"
                "Времена часто «сдвигаются» назад. Вопросы: He asked where I lived.\n\n"
                "Тренируем внимательность к сдвигу времён."
            ),
        },
        {
            "id": "passives_advanced",
            "title": "Passive (все времена)",
            "rico_intro": (
                "🦜 <b>Рико:</b> Passive во разных временах:\n\n"
                "is being built / has been done / will be sent / was being repaired…\n\n"
                "В новостях и формальных текстах — must-have."
            ),
        },
        {
            "id": "modals_deduction",
            "title": "Modals of deduction",
            "rico_intro": (
                "🦜 <b>Рико:</b> Догадки:\n\n"
                "• must be — почти уверен\n"
                "• might/may/could be — возможно\n"
                "• can’t be — невозможно\n"
                "• must have + V3 — догадка о прошлом\n\n"
                "She must be at work. / He can’t have forgotten."
            ),
        },
        {
            "id": "relative_advanced",
            "title": "Relative clauses (advanced)",
            "rico_intro": (
                "🦜 <b>Рико:</b> whose, where, when + defining/non-defining.\n\n"
                "The author whose book I read…\n"
                "Paris, where I lived, is beautiful. (запятые!)\n\n"
                "Практика на уровне B2 — точнее и естественнее."
            ),
        },
    ],
    "C1": [
        {
            "id": "inversion",
            "title": "Inversion (инверсия)",
            "rico_intro": (
                "🦜 <b>Рико:</b> Инверсия — когда меняем порядок слов для силы и стиля.\n\n"
                "После негативных/ограничивающих наречий часто идёт вспомогательный глагол:\n"
                "• Never have I seen such a film.\n"
                "• Rarely does she complain.\n"
                "• Not only did she win, but she also broke a record.\n\n"
                "Звучит «книжнее» и сильнее обычного I have never seen…\n\n"
                "После заданий откроется тест. В заданиях помогаю всегда, в тесте — 2 раза.\n"
                "Пиши вопросы — разберём на примерах! ✨"
            ),
        },
        {
            "id": "cleft_sentences",
            "title": "Cleft sentences",
            "rico_intro": (
                "🦜 <b>Рико:</b> Cleft — «разделяем» фразу, чтобы выделить главное.\n\n"
                "• It was John who called. (именно Джон)\n"
                "• What I need is a break. (именно отдых)\n\n"
                "Это как прожектор на нужную часть смысла.\n"
                "После практики — тест. Спрашивай тонкости! 🦜"
            ),
        },
        {
            "id": "advanced_modals",
            "title": "Advanced modals",
            "rico_intro": (
                "🦜 <b>Рико:</b> Модальные «с историей»:\n\n"
                "• should have + V3 — надо было, а не сделал\n"
                "• needn’t have + V3 — зря сделал (не нужно было)\n"
                "• might have been — возможно, было так\n\n"
                "Тонкие оттенки сожаления, критики и вероятности.\n"
                "После заданий — тест (2 подсказки). Я рядом! ✨"
            ),
        },
        {
            "id": "participle_clauses",
            "title": "Participle clauses",
            "rico_intro": (
                "🦜 <b>Рико:</b> Причастные обороты сжимают две идеи в одну элегантную.\n\n"
                "• Walking down the street, I saw a friend.\n"
                "• Built in 1900, the house looks unique.\n\n"
                "Важно: подлежащее должно совпадать, иначе получится смешно "
                "(Looking out the window, the rain… — дождь не смотрел).\n\n"
                "После заданий — тест. Пиши вопросы! 🦜"
            ),
        },
        {
            "id": "nominalisation",
            "title": "Nominalisation",
            "rico_intro": (
                "🦜 <b>Рико:</b> Nominalisation — глагол/прилагательное → существительное.\n\n"
                "decide → decision, develop → development, important → importance.\n"
                "The development of technology… — стиль академических и формальных текстов.\n\n"
                "После практики откроется тест. Подсказки в заданиях безлимит! ✨"
            ),
        },
        {
            "id": "discourse_markers",
            "title": "Discourse markers",
            "rico_intro": (
                "🦜 <b>Рико:</b> Связки держат мысль:\n\n"
                "however, nevertheless, that said, in contrast, furthermore…\n\n"
                "Они делают речь как у сильного автора/оратора. Важно уместность, не «лепить пачками».\n"
                "После заданий — тест. Спроси примеры под свою тему! 🦜"
            ),
        },
    ],
    "C2": [
        {
            "id": "stylistic_inversion",
            "title": "Stylistic nuance & inversion",
            "rico_intro": (
                "🦜 <b>Рико:</b> На C2 грамматика = стиль и эффект.\n\n"
                "Инверсия, эмфаза, ритм фразы. Мы выбираем конструкцию не «по формуле из учебника», "
                "а по тому, какое ощущение хотим дать слушателю.\n\n"
                "После заданий — тест (2 подсказки). Пиши: разберём стилистику на примерах! ✨"
            ),
        },
        {
            "id": "subtle_modality",
            "title": "Subtle modality",
            "rico_intro": (
                "🦜 <b>Рико:</b> Тонкая модальность — оттенки «уверенности».\n\n"
                "may have / might have / could have — разная сила догадки о прошлом.\n"
                "Хеджирование: It would seem… / Arguably…\n\n"
                "После практики — тест. В заданиях помогаю всегда! 🦜"
            ),
        },
        {
            "id": "mixed_conditionals",
            "title": "Mixed conditionals",
            "rico_intro": (
                "🦜 <b>Рико:</b> Mixed conditionals — смешиваем времена.\n\n"
                "If I had taken that job, I would be in London now.\n"
                "(прошлое условие → нынешний результат)\n\n"
                "If I were more organised, I wouldn’t have missed the deadline.\n"
                "(настоящая «черта» → прошлое следствие)\n\n"
                "После заданий откроется тест. Спрашивай! ✨"
            ),
        },
        {
            "id": "ellipsis_substitution",
            "title": "Ellipsis & substitution",
            "rico_intro": (
                "🦜 <b>Рико:</b> Носители не любят повторяться.\n\n"
                "• So do I / Neither have I\n"
                "• If you want to (go)…\n"
                "• I think so / I hope not\n\n"
                "Учимся опускать очевидное — речь становится естественной.\n"
                "После заданий — тест. Я на связи! 🦜"
            ),
        },
        {
            "id": "register_control",
            "title": "Register control",
            "rico_intro": (
                "🦜 <b>Рико:</b> Register — «костюм» языка.\n\n"
                "Formal / informal / academic: одна идея — разные формулировки.\n"
                "На C2 это важнее новых времён: знать, где can, а где would be able to.\n\n"
                "После практики — тест. Пиши примеры — подберём тон! ✨"
            ),
        },
        {
            "id": "pragmatic_softening",
            "title": "Pragmatic softening",
            "rico_intro": (
                "🦜 <b>Рико:</b> Смягчение просьб и мнений:\n\n"
                "• I was wondering if…\n"
                "• Would you mind…\n"
                "• It might be better if…\n\n"
                "Вежливость и прагматика — секрет «почти native» звучания.\n"
                "После заданий — тест (2 подсказки). Давай тренироваться! 🦜"
            ),
        },
    ],
}


# Английское название → русское (для единого вида «EN / RU»)
_TITLE_RU: dict[str, str] = {
    "alphabet": "Alphabet / Алфавит",
    "numbers_1_20": "Numbers 1–20 / Цифры 1–20",
    "pronouns_be": "I / You + to be / Я есть…",
    "this_that": "This / That / Это / То",
    "simple_phrases": "Simple phrases / Простые фразы",
    "present_simple": "Present Simple / Настоящее простое",
    "articles_a_an": "Articles a / an / Артикли a и an",
    "plurals": "Plurals / Множественное число",
    "there_is_are": "There is / There are / Есть…",
    "can_ability": "Can / Умею, могу",
    "numbers_1_100": "Numbers 1–100 / Цифры 1–100",
    "numbers_time_dates": "Numbers, time & dates / Числа, время и даты",
    "present_continuous": "Present Continuous / Настоящее длительное",
    "past_simple": "Past Simple / Прошедшее простое",
    "going_to_future": "Going to / Планы (going to)",
    "much_many_some_any": "Much / Many / Some / Any",
    "comparatives": "Comparatives / Степени сравнения",
    "modals_a2": "Must / Have to / Should / Модальные",
    "present_perfect": "Present Perfect / Настоящее совершённое",
    "past_perfect": "Past Perfect / Предпрошедшее",
    "past_continuous": "Past Continuous / Прошедшее длительное",
    "conditionals_0_1": "Conditionals 0 & 1 / Условные 0 и 1",
    "gerund_infinitive": "Gerund / Infinitive / Герундий и инфинитив",
    "passive_basic": "Passive Voice / Страдательный залог (база)",
    "relative_clauses_b1": "Relative clauses / Относительные предложения",
    "present_perfect_continuous": "Present Perfect Continuous / Настоящее совершённо-длительное",
    "conditionals_2_3": "Conditionals 2 & 3 / Условные 2 и 3",
    "reported_speech": "Reported Speech / Косвенная речь",
    "passives_advanced": "Passive (all tenses) / Пассив (все времена)",
    "modals_deduction": "Modals of deduction / Модальные догадки",
    "relative_advanced": "Relative clauses (advanced) / Относительные (продвинутые)",
    "inversion": "Inversion / Инверсия",
    "cleft_sentences": "Cleft sentences / Расщеплённые предложения",
    "advanced_modals": "Advanced modals / Продвинутые модальные",
    "participle_clauses": "Participle clauses / Причастные обороты",
    "nominalisation": "Nominalisation / Номинализация",
    "discourse_markers": "Discourse markers / Связки речи",
    "stylistic_inversion": "Stylistic nuance & inversion / Стиль и инверсия",
    "subtle_modality": "Subtle modality / Тонкая модальность",
    "mixed_conditionals": "Mixed conditionals / Смешанные условные",
    "ellipsis_substitution": "Ellipsis & substitution / Пропуски и замены",
    "register_control": "Register control / Стиль речи (register)",
    "pragmatic_softening": "Pragmatic softening / Вежливое смягчение",
}

# Темы без заданий: только «Ознакомился»
ACK_TOPIC_IDS = {
    "alphabet",
    "numbers_1_20",
    "numbers_1_100",
    "numbers_time_dates",
}


def _normalize_topic(raw: dict) -> dict:
    t = dict(raw)
    tid = t.get("id") or ""
    if tid in _TITLE_RU:
        t["title"] = _TITLE_RU[tid]
    if tid in ACK_TOPIC_IDS:
        t["mode"] = "ack"
    else:
        t["mode"] = t.get("mode") or "practice"

    narrative = get_narrative_intro(tid)
    if narrative:
        t["rico_intro"] = narrative
    else:
        intro = t.get("rico_intro") or ""
        extra = get_enrichment(tid, t["mode"])
        if extra and extra not in intro:
            t["rico_intro"] = intro + extra
    return t


def get_grammar_section_intro(level: str) -> str:
    return GRAMMAR_SECTION_INTRO.get(
        level,
        f"🦜 <b>Рико:</b> Грамматика уровня <b>{level}</b> — поехали! ✨",
    )


def get_topics(level: str) -> list[dict]:
    return [_normalize_topic(t) for t in GRAMMAR_BY_LEVEL.get(level, [])]


def get_topic(level: str, topic_id: str) -> dict | None:
    for t in get_topics(level):
        if t["id"] == topic_id:
            return t
    return None


def get_topic_by_index(level: str, index_1based: int) -> dict | None:
    topics = get_topics(level)
    if index_1based < 1 or index_1based > len(topics):
        return None
    return topics[index_1based - 1]


def is_ack_topic(topic: dict | None) -> bool:
    if not topic:
        return False
    return topic.get("mode") == "ack" or topic.get("id") in ACK_TOPIC_IDS


def format_topics_list(
    level: str,
    completed_topic_ids: set[str] | None = None,
) -> str:
    topics = get_topics(level)
    done = completed_topic_ids or set()
    lines = [f"📘 <b>Grammar · уровень {level}</b>\n", "Выбери тему:\n"]
    for i, t in enumerate(topics, start=1):
        mark = "✅ " if t["id"] in done else ""
        lines.append(f"<b>{i}.</b> {mark}{t['title']}")
    lines.append(
        "\n🦜 Темы алфавита/цифр — «Ознакомился». Остальные: 8 заданий → ✅.\n"
        "Все темы пройдены → <b>🎯 Тест по Grammar</b>."
    )
    return "\n".join(lines)
