"""
Связные объяснения Рико по темам грамматики (формат «рассказ», не списки).
"""

NARRATIVE_INTROS: dict[str, str] = {
    "alphabet": (
        "🦜 <b>Рико:</b> Итак, друг, мы начинаем с самого фундамента — с <b>алфавита</b>! "
        "Знаешь, многие хотят сразу «говорить фразы», а буквы откладывают… "
        "А зря 😄 Без алфавита ты не продиктуешь email, не поймёшь имя по буквам и будешь "
        "путаться в чтении.\n\n"
        "В английском <b>26 букв</b> — те же, что на клавиатуре: "
        "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z. "
        "У каждой есть своё <b>название</b>: A = /eɪ/ «эй», B = /biː/ «би»… "
        "Гласные — A, E, I, O, U (иногда Y в yes, my). Остальные — согласные.\n\n"
        "Представь ситуацию: тебя спрашивают имя по телефону.\n"
        "— How do you spell your name?\n"
        "<i>— Как по буквам пишется твоё имя?</i>\n"
        "— D-A-N-I-L.\n"
        "<i>— Д-А-Н-И-Л.</i>\n\n"
        "А вот подводка для нас, русскоязычных: буква <b>W</b> — это «дубль-ю», не «в»; "
        "<b>Th</b> в think — язык между зубами; <b>H</b> в hour почти не слышна. "
        "Не пугайся — это приходит с практикой 🌱\n\n"
        "Заданий здесь нет — просто прочитай, и когда будешь готов, жми "
        "<b>✅ Ознакомился</b>. Я рядом, если что-то непонятно!"
    ),
    "numbers_1_20": (
        "🦜 <b>Рико:</b> Отлично, идём дальше — к <b>цифрам от 1 до 20</b>! "
        "Они нужны с первого дня: возраст, цена, номер, «сколько?».\n\n"
        "Слушай, как это звучит: one, two, three… ten, потом eleven и twelve — "
        "их лучше запомнить отдельно, они «особенные». "
        "Дальше thirteen, fourteen… twenty — с окончанием -teen.\n\n"
        "Пример из жизни:\n"
        "— How old are you?\n"
        "<i>— Сколько тебе лет?</i>\n"
        "— I'm eighteen.\n"
        "<i>— Мне восемнадцать.</i>\n\n"
        "Главная ловушка: не путай <b>thirteen</b> (13) и <b>thirty</b> (30) — "
        "звучат похоже, а разница огромная 😅 "
        "Жми <b>✅ Ознакомился</b>, когда запомнишь — и погнали дальше!"
    ),
    "pronouns_be": (
        "🦜 <b>Рико:</b> А теперь — легендарный глагол <b>to be</b> (быть)! "
        "Без него в английском почти никуда: ни представиться, ни сказать «я студент», "
        "ни спросить «ты дома?».\n\n"
        "Смотри, как он работает сейчас, в настоящем: "
        "I <b>am</b>, you <b>are</b>, he/she/it <b>is</b>, we/you/they <b>are</b>. "
        "Пример: I am Danil — <i>Я Данил / Меня зовут Данил</i>. "
        "She is a student — <i>Она студентка</i>. "
        "They are friends — <i>Они друзья</i>.\n\n"
        "В вопросе порядок меняется: <b>Are you</b> OK? — <i>Ты в порядке?</i> "
        "А после he/she/it всегда <b>is</b>, не are — это частая ошибка!\n\n"
        "Дальше будут задания — там есть кнопка <b>🌍 Перевести</b>, "
        "если не понимаешь слова в предложении. Я помогу 💪"
    ),
    "this_that": (
        "🦜 <b>Рико:</b> Сегодня разберём <b>this</b> и <b>that</b> — "
        "два маленьких слова, которые показывают «это рядом» или «то там».\n\n"
        "<b>This</b> — когда предмет близко к тебе: This is a book — "
        "<i>Это книга (вот она, рядом)</i>. "
        "<b>That</b> — когда далеко: That is a car — "
        "<i>То — машина (вон там)</i>.\n\n"
        "В разговоре часто слышишь: What's this? — <i>Что это?</i> "
        "What's that? — <i>Что это там?</i> "
        "Запомни: this — «вот это», that — «вон то» 👆\n\n"
        "Потренируем в заданиях — я рядом!"
    ),
    "simple_phrases": (
        "🦜 <b>Рико:</b> Ну что, собираем первые <b>живые фразы</b> — "
        "те, что реально говорят люди, а не только в учебнике!\n\n"
        "Hello! / Hi! — <i>Привет!</i> "
        "What's your name? — My name is… — <i>Как тебя зовут? — Меня зовут…</i> "
        "Nice to meet you — <i>Приятно познакомиться</i>. "
        "How are you? — I'm fine — <i>Как дела? — Хорошо</i>.\n\n"
        "И пара волшебных слов: Thank you — <i>Спасибо</i>, Please — <i>Пожалуйста</i>, "
        "Sorry — <i>Извини</i>. Они делают речь вежливой с первого дня ✨\n\n"
        "Учи фразы целиком — так быстрее заговоришь. Дальше — задания!"
    ),
    "present_simple": (
        "🦜 <b>Рико:</b> Итак, встречай — <b>Present Simple</b>, король повседневной речи! "
        "Это время для привычек, распорядка и фактов: «я хожу в школу», «она живёт в Москве», "
        "«вода кипит при 100°». Когда видишь always, usually, every day — почти всегда Simple.\n\n"
        "Разберём <b>формулы</b> по шагам. Утверждение: "
        "<b>I / You / We / They + V1</b> (глагол без окончания). "
        "I like tea — <i>Я люблю чай</i>. We live here — <i>Мы живём здесь</i>. "
        "С he/she/it добавляем <b>-s</b> или <b>-es</b>: He likes tea — <i>Он любит чай</i>. "
        "She watches TV — <i>Она смотрит телевизор</i>.\n\n"
        "Отрицание: <b>don't / doesn't + V1</b>. "
        "I don't like coffee — <i>Я не люблю кофе</i>. "
        "She doesn't work on Sundays — <i>Она не работает по воскресеньям</i>. "
        "После doesn't глагол без -s!\n\n"
        "Вопрос: <b>Do / Does + подлежащее + V1?</b> "
        "Do you speak English? — <i>Ты говоришь по-английски?</i> "
        "Does he play football? — <i>Он играет в футбол?</i>\n\n"
        "Это база A1 — освоишь её, и Past Simple, Continuous и модальные станут в разы проще. "
        "В заданиях жми <b>🌍 Перевести</b> — покажу русский смысл английской фразы 🚀"
    ),
    "articles_a_an": (
        "🦜 <b>Рико:</b> Сегодня про крошечные, но коварные слова — <b>a</b> и <b>an</b>. "
        "Они как «один / какой-то» перед существительным: a book — <i>книга</i>, "
        "an apple — <i>яблоко</i>.\n\n"
        "Правило простое: смотри на <b>звук</b>, не на букву! "
        "a university (звук /juː/), an hour (h не слышна). "
        "I need a pen — <i>Мне нужна ручка</i> (любая, не конкретная).\n\n"
        "Русскоязычным кажется, что артикль «лишний» — но без него фраза часто звучит "
        "неправильно. Потренируем — и рука сама начнёт ставить a/an 😄"
    ),
    "plurals": (
        "🦜 <b>Рико:</b> Переходим к <b>множественному числу</b> — когда предметов больше одного!\n\n"
        "Обычно добавляем -s: book → books, cat → cats. "
        "Но есть красивые исключения: man → men, child → children, foot → feet. "
        "Two books — <i>Две книги</i>, Three children — <i>Трое детей</i>.\n\n"
        "После -s, -x, -ch иногда -es: box → boxes. "
        "А potato → potatoes, но photo → photos — да, английский любит сюрпризы 🙃\n\n"
        "Запоминай частые неправильные формы списком — потом они идут сами."
    ),
    "there_is_are": (
        "🦜 <b>Рико:</b> Знакомься с конструкцией <b>There is / There are</b> — "
        "по-русски это «есть / имеется».\n\n"
        "There is a cat on the sofa — <i>На диване есть кот</i> (один). "
        "There are two books — <i>Есть две книги</i>. "
        "Вопрос: Is there a shop near here? — <i>Здесь рядом есть магазин?</i>\n\n"
        "Не путай с It is! There is a problem — <i>Есть проблема</i>, "
        "а It is a problem — <i>Это проблема</i> (разный акцент). "
        "Единственное → is, множественное → are — и ты в теме ✅"
    ),
    "can_ability": (
        "🦜 <b>Рико:</b> Итак, мы переходим к легендарному <b>can</b> — "
        "он очень распространён в речи и крайне нужен для связи в предложении! "
        "Can — это <b>умение</b> и <b>возможность</b>: что ты умеешь или что тебе разрешено.\n\n"
        "I can swim — <i>Я умею плавать</i>. "
        "She can speak English — <i>Она может / умеет говорить по-английски</i>. "
        "Can you help me? — <i>Ты можешь помочь мне?</i> "
        "После can всегда глагол без to: I can swim ✅, I can to swim ❌.\n\n"
        "Can't = cannot — «не могу / не умею». "
        "Could — более вежливая форма или прошлое: Could you open the door? — "
        "<i>Не мог бы ты открыть дверь?</i> "
        "Can — один из первых модальных, и ты будешь слышать его каждый день 🎵"
    ),
    "numbers_1_100": (
        "🦜 <b>Рико:</b> Расширяем цифры до <b>100</b> — теперь сможешь называть цены, "
        "возраст и номера без пауз!\n\n"
        "Десятки: twenty, thirty, forty (без u!), fifty… a hundred. "
        "Составные: twenty-one, forty-five — через дефис. "
        "It's fifty pounds — <i>Это пятьдесят фунтов</i>.\n\n"
        "Сначала выучи десятки, потом собирай составные — как конструктор 🧱 "
        "Жми <b>✅ Ознакомился</b>, когда будешь готов!"
    ),
    "numbers_time_dates": (
        "🦜 <b>Рико:</b> Цифры оживают — учим <b>время и даты</b>! "
        "Без этого сложно договориться о встрече или понять расписание.\n\n"
        "It's half past two — <i>Половина третьего</i>. "
        "It's a quarter to five — <i>Без пятнадцати пять</i>. "
        "The third of May / May 3rd — <i>Третье мая</i>. "
        "1999 — nineteen ninety-nine.\n\n"
        "Время — с <b>at</b> (at 5 o'clock), даты — с <b>on</b> (on Monday). "
        "Ознакомься и жми <b>✅ Ознакомился</b> ✨"
    ),
    "present_continuous": (
        "🦜 <b>Рико:</b> Сейчас разберём <b>Present Continuous</b> — "
        "когда действие происходит <b>прямо сейчас</b> или временно, но не «навсегда».\n\n"
        "Формула: <b>am / is / are + V-ing</b>. "
        "I am reading now — <i>Я читаю сейчас</i>. "
        "She is working at the moment — <i>Она работает в данный момент</i>. "
        "They are playing football — <i>Они играют в футбол (прямо сейчас)</i>.\n\n"
        "Отрицание: am not / isn't / aren't + V-ing. "
        "I'm not sleeping — <i>Я не сплю</i>. "
        "Вопрос: <b>Am/Is/Are + подлежащее + V-ing?</b> "
        "Are you listening? — <i>Ты слушаешь?</i>\n\n"
        "Сравни с Simple: I read every day — <i>привычка</i>; "
        "I am reading now — <i>прямо сейчас</i>. "
        "Слова now, at the moment, today (иногда) — подсказки Continuous. "
        "Но know, like, want — почти не ставят в Continuous: I know ✅, I am knowing ❌. "
        "Поймаешь ритм — и заговоришь естественнее 🔥"
    ),
    "past_simple": (
        "🦜 <b>Рико:</b> Итак, друг, мы подходим к одному из самых важных времён — "
        "<b>Past Simple</b>! Это «прошлое простое»: всё, что уже случилось и закончилось. "
        "Вчера, год назад, last week — когда видишь такие слова, почти всегда нужен Past Simple.\n\n"
        "Давай разберём, <b>как строится предложение</b> — это ключ ко всему. "
        "В утверждении мы берём подлежащее и глагол в форме прошлого: "
        "<b>I/You/He/She/It/We/They + V2</b> (вторая форма). "
        "У правильных глаголов V2 = V1 + <b>-ed</b>: work → worked, play → played. "
        "I worked yesterday — <i>Я работал вчера</i>. She played tennis — <i>Она играла в теннис</i>.\n\n"
        "У <b>неправильных</b> глаголов форма особая — её просто запоминают: "
        "go → went, see → saw, have → had, do → did. "
        "I went home — <i>Я пошёл домой</i>. He saw a film — <i>Он посмотрел фильм</i>.\n\n"
        "В <b>отрицании</b> появляется помощник <b>did not (didn't)</b> + глагол в первой форме: "
        "I didn't go — <i>Я не ходил</i>. She didn't like it — <i>Ей не понравилось</i>. "
        "Запомни ловушку: после didn't НИКОГДА не ставь went/saw — только go, see!\n\n"
        "В <b>вопросе</b> did выходит вперёд: <b>Did + подлежащее + V1?</b> "
        "Did you visit London? — <i>Ты был в Лондоне?</i> "
        "Did she call you? — <i>Она тебе звонила?</i>\n\n"
        "Слова-подсказки: yesterday, last week/month/year, ago, in 2020. "
        "С этим временем ты наконец сможешь рассказывать истории о себе — "
        "что делал, куда ходил, что видел. А в заданиях жми <b>🌍 Перевести</b>, "
        "если не понимаешь английскую фразу — переведу смысл, не инструкцию 📖"
    ),
    "going_to_future": (
        "🦜 <b>Рико:</b> Планы и намерения — время <b>going to</b>! "
        "Когда ты уже решил, что сделаешь, или видишь очевидный признак будущего.\n\n"
        "Формула: <b>am / is / are + going to + V1</b>. "
        "I'm going to study tonight — <i>Сегодня вечером буду учиться</i>. "
        "She's going to buy a car — <i>Она собирается купить машину</i>. "
        "Look at the clouds! It's going to rain — <i>Сейчас пойдёт дождь</i> (видим признаки).\n\n"
        "Вопрос: <b>Am/Is/Are + подлежащее + going to + V1?</b> "
        "Are you going to travel? — <i>Ты собираешься путешествовать?</i> "
        "Отрицание: I'm not going to wait — <i>Я не собираюсь ждать</i>.\n\n"
        "Going to = заранее решённый план; <b>will</b> — спонтанное решение на месте: "
        "The phone is ringing — I'll answer! — <i>Я отвечу!</i> "
        "Оба про будущее, но оттенок разный 🎯"
    ),
    "much_many_some_any": (
        "🦜 <b>Рико:</b> Сегодня про <b>much, many, some, any</b> — "
        "сколько и «есть ли вообще».\n\n"
        "Many + исчисляемое: many books — <i>много книг</i>. "
        "Much + неисчисляемое: much water — <i>много воды</i> (часто в вопросах). "
        "Some — в утверждениях: some tea — <i>чай (какой-то)</i>. "
        "Any — в вопросах: any milk? — <i>есть молоко?</i>\n\n"
        "How many? / How much? — разные вопросы. "
        "A lot of — универсально в разговоре 👍"
    ),
    "comparatives": (
        "🦜 <b>Рико:</b> Сравниваем! <b>Comparatives</b> — bigger, better, more interesting.\n\n"
        "Short adjectives: old → older, big → bigger. "
        "Long: beautiful → more beautiful. "
        "She is taller than me — <i>Она выше меня</i>. "
        "Good → better, bad → worse — запомни отдельно!\n\n"
        "Than — обязательный спутник сравнения. "
        "С этим легко описывать мир вокруг 📏"
    ),
    "modals_a2": (
        "🦜 <b>Рико:</b> Модальные глаголы — must, have to, should. "
        "Must — «должен» по убеждению; have to — по правилу; should — совет.\n\n"
        "You should sleep more — <i>Тебе стоит больше спать</i>. "
        "I have to work tomorrow — <i>Завтра я должен работать</i>. "
        "Must not — запрет: You must not smoke — <i>Нельзя курить</i>.\n\n"
        "После них — глагол без to. Must go ✅. Потренируем в заданиях!"
    ),
    "present_perfect": (
        "🦜 <b>Рико:</b> <b>Present Perfect</b> — мост между прошлым и настоящим. "
        "Связь «было когда-то» с «важно сейчас»: опыт, результат, незаконченный период.\n\n"
        "Формула: <b>have / has + V3</b> (третья форма глагола). "
        "I have visited London — <i>Я был в Лондоне (опыт в жизни)</i>. "
        "She has lost her keys — <i>Она потеряла ключи (и сейчас их нет)</i>. "
        "We have lived here for five years — <i>Мы живём здесь пять лет (и до сих пор)</i>.\n\n"
        "Вопрос: <b>Have/Has + подлежащее + V3?</b> "
        "Have you ever been to Paris? — <i>Ты когда-нибудь был в Париже?</i> "
        "Отрицание: haven't / hasn't + V3.\n\n"
        "Маркеры: ever, never, already, yet, just, for, since. "
        "Yesterday, last week, in 2020 → <b>Past Simple</b>, не Perfect! "
        "Разница тонкая — поймаем на примерах в заданиях ✨"
    ),
    "past_perfect": (
        "🦜 <b>Рико:</b> <b>Past Perfect</b> — «ещё более прошлое»! Had + V3.\n\n"
        "When I arrived, the train had left — <i>Когда я приехал, поезд уже ушёл</i>. "
        "Сначала ушёл поезд, потом ты приехал — Perfect показывает, что было раньше.\n\n"
        "Before, by the time, already — подсказки. "
        "Не путай с Present Perfect — здесь всё в прошлом ⏪"
    ),
    "past_continuous": (
        "🦜 <b>Рико:</b> <b>Past Continuous</b> — длинное действие в прошлом: was/were + V-ing.\n\n"
        "I was watching TV when he called — <i>Я смотрел телевизор, когда он позвонил</i>. "
        "Фон (смотрел) + короткое прерывание (позвонил). "
        "Классическая связка с Past Simple 🎬"
    ),
    "conditionals_0_1": (
        "🦜 <b>Рико:</b> Условные предложения — «если…, то…». "
        "Zero: If you heat water, it boils — <i>если нагреешь воду, она кипит</i> (факт). "
        "First: If it rains, I'll stay home — <i>если пойдёт дождь, останусь дома</i> (реальное будущее).\n\n"
        "Не пиши will сразу после if ❌. Запятая, если if в начале. "
        "Мощный инструмент для планов и правил 🎯"
    ),
    "gerund_infinitive": (
        "🦜 <b>Рико:</b> V-ing или to V? Enjoy reading — <i>наслаждаюсь чтением</i>. "
        "Want to go — <i>хочу пойти</i>. Stop smoking vs stop to smoke — разный смысл!\n\n"
        "Списки глаголов учим через практику — я подскажу в заданиях 📚"
    ),
    "passive_basic": (
        "🦜 <b>Рико:</b> <b>Passive</b> — когда важен результат, а не кто сделал. "
        "The letter was sent — <i>Письмо отправили</i>. Be + V3. "
        "English is spoken here — <i>Здесь говорят по-английски</i>.\n\n"
        "Актив: Someone sent the letter. Пассив: The letter was sent. "
        "Часто в новостях и инструкциях 📰"
    ),
    "relative_clauses_b1": (
        "🦜 <b>Рико:</b> Who, which, that — соединяем две мысли в одну умную фразу. "
        "The man who called you — <i>Человек, который тебе звонил</i>. "
        "The book which I bought — <i>Книга, которую я купил</i>.\n\n"
        "Речь становится «взрослее» и короче — как у носителей 🎓"
    ),
    "present_perfect_continuous": (
        "🦜 <b>Рико:</b> Have been + V-ing — процесс до сейчас. "
        "I've been waiting for an hour — <i>Я жду уже час</i>. "
        "Vs I've written 3 emails — <i>Написал три письма</i> (результат).\n\n"
        "For/since — твои маркеры длительности ⏱️"
    ),
    "conditionals_2_3": (
        "🦜 <b>Рико:</b> Second: If I had time, I would travel — нереально сейчас. "
        "Third: If I had studied, I would have passed — нереально в прошлом.\n\n"
        "Сожаления, мечты, «а что если» — B2-level мышление 🔮"
    ),
    "reported_speech": (
        "🦜 <b>Рико:</b> Передаём чужие слова: He said he was tired — "
        "<i>Он сказал, что устал</i>. Времена часто сдвигаются назад. "
        "Say + слова; tell + кому. He told me that… 📢"
    ),
    "passives_advanced": (
        "🦜 <b>Рико:</b> Passive во всех временах: is being built, has been done, will be sent. "
        "Must be finished — <i>должно быть закончено</i>. Формальный стиль и новости 📰"
    ),
    "modals_deduction": (
        "🦜 <b>Рико:</b> Догадки: She must be at work — <i>наверняка на работе</i>. "
        "It can't be true — <i>не может быть правдой</i>. "
        "Must have + V3 — про прошлое. Шкала уверенности 🕵️"
    ),
    "relative_advanced": (
        "🦜 <b>Рико:</b> Whose, where, when + defining/non-defining. "
        "Paris, where I lived, is beautiful — запятые в non-defining! "
        "Точнее и естественнее на B2 📌"
    ),
    "inversion": (
        "🦜 <b>Рико:</b> Never have I seen… — стильная инверсия для эссе. "
        "После Never, Rarely, Not only… — вспомогательный вперёд. "
        "Сильная, «книжная» речь ✍️"
    ),
    "cleft_sentences": (
        "🦜 <b>Рико:</b> It was John who called — <i>Именно Джон позвонил</i>. "
        "What I need is a break — <i>Мне нужен отдых</i>. Прожектор на главное 🔦"
    ),
    "advanced_modals": (
        "🦜 <b>Рико:</b> Should have — <i>надо было</i>. Needn't have — <i>зря сделал</i>. "
        "Might have been — <i>возможно, было так</i>. Оттенки сожаления и критики 💭"
    ),
    "participle_clauses": (
        "🦜 <b>Рико:</b> Walking down the street, I saw a friend — "
        "сжимаем две идеи. Подлежащее должно совпадать! "
        "Walking…, the rain… ❌ — дождь не идёт пешком 😄"
    ),
    "nominalisation": (
        "🦜 <b>Рико:</b> Decide → decision, develop → development. "
        "The development of technology… — академический стиль. "
        "В разговоре не перегибай 📄"
    ),
    "discourse_markers": (
        "🦜 <b>Рико:</b> However, furthermore, in contrast — связки для эссе. "
        "Структура мысли: firstly, moreover, in conclusion 📝"
    ),
    "stylistic_inversion": (
        "🦜 <b>Рико:</b> На C2 грамматика = стиль. Инверсия, эмфаза, ритм. "
        "Выбираем форму по эффекту, не по формуле 🎭"
    ),
    "subtle_modality": (
        "🦜 <b>Рико:</b> May have vs might have — сила догадки. "
        "It would seem… — мягче мнение. Почти native 🤝"
    ),
    "mixed_conditionals": (
        "🦜 <b>Рико:</b> If I had taken that job, I would be in London now — "
        "прошлое условие, настоящий результат. Смешиваем времена 🔀"
    ),
    "ellipsis_substitution": (
        "🦜 <b>Рико:</b> So do I, I think so — носители не повторяются. "
        "Естественная экономия слов 🗣️"
    ),
    "register_control": (
        "🦜 <b>Рико:</b> Formal vs informal: obtain vs get, inquire vs ask. "
        "Одна идея — разные «костюмы» 👔"
    ),
    "pragmatic_softening": (
        "🦜 <b>Рико:</b> I was wondering if…, Would you mind… — "
        "вежливость и смягчение. Секрет «почти native» 🕊️"
    ),
}


def get_narrative_intro(topic_id: str) -> str | None:
    from data.grammar_formula_deep import append_formula_deep_dive

    base = NARRATIVE_INTROS.get(topic_id)
    if not base:
        return None
    return append_formula_deep_dive(topic_id, base)
