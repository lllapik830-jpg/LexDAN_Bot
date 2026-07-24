# -*- coding: utf-8 -*-
"""
Живые рассказы Рико для добавленных тем Grammar.
Стиль как у can_ability: эмоция → смысл → примеры с переводом → ловушки → зачем это в жизни.
"""

NARRATIVES: dict[str, str] = {
    # ─── A0 ───────────────────────────────────────────────────────────
    "colors_a0": (
        "🦜 <b>Рико:</b> Итак, раскрашиваем английский — тема <b>Colors</b>! "
        "Без цветов ты не опишешь машину, футболку и даже настроение. "
        "А носители спрашивают про цвет постоянно 🎨\n\n"
        "База: red, blue, green, yellow, black, white, orange, pink, brown, grey. "
        "В английском цвет обычно идёт <b>после</b> is/are: "
        "The car is red — <i>Машина красная</i>. "
        "The flowers are yellow — <i>Цветы жёлтые</i>. "
        "Не «the car red» ❌ — без is фраза «хромает».\n\n"
        "Вопрос: What color is it? — <i>Какого оно цвета?</i> "
        "It's blue — <i>Синее</i>. "
        "Grey (BrE) и gray (AmE) — одно и то же, оба ок. "
        "Дальше потренируем — и цвета начнут выскакивать сами!"
    ),
    "family_a0": (
        "🦜 <b>Рико:</b> Переходим к семье — <b>Family</b>! "
        "Это слова первого знакомства: без них трудно рассказать, кто ты и кто рядом.\n\n"
        "mother / mum, father / dad, sister, brother, parents, grandparents, "
        "son, daughter, friend. "
        "This is my mum — <i>Это моя мама</i>. "
        "I have one brother — <i>У меня один брат</i>. "
        "They are my parents — <i>Это мои родители</i>.\n\n"
        "Вопрос: Have you got a sister? / Do you have a sister? — "
        "<i>У тебя есть сестра?</i> "
        "Mum и dad — разговорные и очень живые; friend тоже «свой круг». "
        "Учи целиком фразы — так быстрее заговоришь про близких 💚"
    ),
    "prepositions_place_a0": (
        "🦜 <b>Рико:</b> Три крошечных слова — и огромная ясность: "
        "<b>in / on / at</b> для места! "
        "Без них «кот коробка» звучит как загадка, а не английский 😄\n\n"
        "<b>in</b> — внутри: in the room, in the bag — "
        "<i>в комнате, в сумке</i>.\n"
        "<b>on</b> — на поверхности: on the table, on the wall — "
        "<i>на столе, на стене</i>.\n"
        "<b>at</b> — точка / место «нахождения»: at school, at the door, at home — "
        "<i>в школе, у двери, дома</i>.\n\n"
        "The cat is in the box — <i>Кот в коробке</i>. "
        "The book is on the table — <i>Книга на столе</i>. "
        "She is at school now — <i>Она сейчас в школе</i>.\n\n"
        "Лайфхак: <b>at home</b> — без the. "
        "Картинка в голове (внутри / на / у точки) спасает лучше зубрёжки!"
    ),
    "have_got_a0": (
        "🦜 <b>Рико:</b> Британская классика — <b>have got</b>! "
        "Это «у меня есть», и ты слышишь это в сериалах и разговорах постоянно.\n\n"
        "I've got a phone — <i>У меня есть телефон</i> (= I have a phone). "
        "She's got a cat — <i>У неё есть кот</i>. "
        "We've got two dogs — <i>У нас две собаки</i>.\n\n"
        "Вопрос: Have you got a pen? — <i>У тебя есть ручка?</i> "
        "Отрицание: I haven't got any money — <i>У меня нет денег</i>.\n\n"
        "В США чаще просто have / Do you have…? — оба варианта правильные. "
        "Главное: после got не ставь to. "
        "Have got — твой быстрый способ говорить про вещи и питомцев ✨"
    ),
    "imperatives_a0": (
        "🦜 <b>Рико:</b> Команды, просьбы, «сделай!» — это <b>Imperatives</b>! "
        "Они нужны в жизни каждую минуту: открой, подожди, не трогай.\n\n"
        "Формула простая: глагол без to сразу вперёд. "
        "Open the door! — <i>Открой дверь!</i> "
        "Sit down! — <i>Садись!</i> "
        "Listen to me! — <i>Слушай меня!</i>\n\n"
        "Вежливость: Please open the window — "
        "<i>Пожалуйста, открой окно</i>. "
        "Отрицание: Don't touch! — <i>Не трогай!</i> "
        "Don't be late! — <i>Не опаздывай!</i> "
        "Let's go! — <i>Пойдём!</i> (мы вместе).\n\n"
        "Лайфхак: Don't + V1, не Doesn't. "
        "Одно Please — и тон становится дружелюбным, не командирским 💚"
    ),
    "possessives_a0": (
        "🦜 <b>Рико:</b> Чей это рюкзак? Чей телефон? "
        "Тема <b>my / your / his / her…</b> — чтобы сразу было ясно «чей»!\n\n"
        "Перед существительным: my, your, his, her, its, our, their. "
        "This is my bag — <i>Это моя сумка</i>. "
        "That's her phone — <i>Это её телефон</i>. "
        "Their house is big — <i>Их дом большой</i>.\n\n"
        "Is this your book? — <i>Это твоя книга?</i> "
        "Tom loves his dog — <i>Том любит свою собаку</i>.\n\n"
        "Осторожно с тройняшками: their (их) / there (там) / they're (they are). "
        "И ещё: its = его/её (вещь), it's = it is. "
        "Путают все — ты теперь будешь замечать ловушку сразу 😎"
    ),
    "days_weather_a0": (
        "🦜 <b>Рико:</b> Дни недели и погода — то, о чём болтают англичане "
        "каждый день (да-да, даже про дождь ☔)!\n\n"
        "Monday…Sunday. Today is Friday — <i>Сегодня пятница</i>. "
        "See you on Sunday — <i>Увидимся в воскресенье</i> "
        "(запомни: <b>on</b> + день недели).\n\n"
        "Погода: sunny, rainy, cloudy, cold, hot, windy. "
        "It's sunny today — <i>Сегодня солнечно</i>. "
        "What's the weather like? — <i>Какая погода?</i> "
        "It's cold — <i>Холодно</i>.\n\n"
        "Формула: It's + погода. Не It rainy ❌ → It's rainy ✅. "
        "Дни — с большой буквы: Monday. "
        "С этой темой small talk становится лёгким!"
    ),
    # ─── A1 ───────────────────────────────────────────────────────────
    "possessive_s_a1": (
        "🦜 <b>Рико:</b> Маленький хвостик <b>'s</b> — и сразу ясно, чей предмет! "
        "Это один из самых «английских» приёмов, его слышно повсюду.\n\n"
        "Dan's book — <i>книга Дана</i>. "
        "My sister's phone — <i>телефон моей сестры</i>. "
        "Хозяин + 's + вещь — и готово.\n\n"
        "Если хозяев много и слово уже на -s: the students' room — "
        "<i>комната студентов</i> (апостроф после s).\n\n"
        "Главная ловушка: <b>it's</b> = it is / it has, "
        "а <b>its</b> = его/её: The dog wagged its tail. "
        "Путают даже продвинутые — зато ты теперь в клубе внимательных ✨"
    ),
    "object_pronouns_a1": (
        "🦜 <b>Рико:</b> После глагола и предлога местоимения «меняются костюм» — "
        "это <b>object pronouns</b>! Без них фразы звучат ломано.\n\n"
        "I → <b>me</b>, he → <b>him</b>, she → <b>her</b>, "
        "we → <b>us</b>, they → <b>them</b> (you и it — те же).\n\n"
        "I like him — <i>Он мне нравится</i> (не I like he ❌). "
        "She called me — <i>Она мне позвонила</i>. "
        "Look at them — <i>Посмотри на них</i>. "
        "Can you help us? — <i>Можешь помочь нам?</i>\n\n"
        "Спроси себя: это «кто делает» (I/he) или «на кого действие» (me/him)? "
        "Второе — object. Один вопрос — и ошибка уходит 🎯"
    ),
    "like_ing_a1": (
        "🦜 <b>Рико:</b> Про хобби, любовь и «не люблю» — "
        "легендарная связка <b>like + -ing</b>! "
        "Именно так носители рассказывают, чем живут.\n\n"
        "I like swimming — <i>Я люблю плавать</i> (как занятие). "
        "She loves reading — <i>Она обожает читать</i>. "
        "Также: love / hate / enjoy + -ing. "
        "I enjoy cooking — <i>Мне нравится готовить</i>.\n\n"
        "А вот вежливое «хотел бы»: would like <b>to</b> + V1 — "
        "I'd like to drink coffee — <i>Я бы хотел выпить кофе</i>.\n\n"
        "Лайфхак: like + -ing = про процесс/хобби. "
        "would like to = желание сейчас. "
        "Перепутаешь — звучит странно; различишь — зазвучишь живо 🎵"
    ),
    "adverbs_frequency_a1": (
        "🦜 <b>Рико:</b> Как часто ты это делаешь? "
        "Наречия частоты — always, usually, often, sometimes, rarely, never — "
        "делают речь точной, а не «ну… иногда…»\n\n"
        "Место почти волшебное: обычно <b>перед</b> смысловым глаголом — "
        "I often play football — <i>Я часто играю в футбол</i>. "
        "Но после am/is/are: She is always late — <i>Она всегда опаздывает</i>.\n\n"
        "I sometimes watch films. We never eat meat.\n\n"
        "Шкала от always (100%) до never (0%). "
        "Sometimes можно и в начало: Sometimes I walk. "
        "Освоил место наречия — речь сразу становится «собраннее»!"
    ),
    "wh_questions_a1": (
        "🦜 <b>Рико:</b> Без вопросов диалог мёртв. "
        "Поэтому <b>Wh- questions</b> — must-have: who, what, where, when, why, how!\n\n"
        "Формула: Wh-слово + do/does/is… + остальное. "
        "Where do you live? — <i>Где ты живёшь?</i> "
        "What does she want? — <i>Чего она хочет?</i> "
        "Who is that? — <i>Кто это?</i> "
        "Why are you sad? — <i>Почему ты грустный?</i>\n\n"
        "How often…? — <i>Как часто…?</i> "
        "How much / How many…? — <i>Сколько…?</i>\n\n"
        "Лайфхак: после does глагол без -s — What does he like? ✅ "
        "What does he likes? ❌. "
        "Один вопрос — и ты уже ведёшь разговор, а не только отвечаешь 🚀"
    ),
    "countable_a1": (
        "🦜 <b>Рико:</b> Можно посчитать или нет? "
        "Тема <b>Countable / Uncountable</b> объясняет, почему «an advice» "
        "режет слух носителю!\n\n"
        "Исчисляемые: a book / books, an apple / apples. "
        "Неисчисляемые: water, rice, milk, advice, information — "
        "обычно без a/an и без привычного -s.\n\n"
        "some water — <i>немного воды</i>, many books — <i>много книг</i>, "
        "much rice — <i>много риса</i>. "
        "Хочешь «посчитать» совет? → a piece of advice — <i>один совет</i>.\n\n"
        "Лайфхак: advice и information — неисчисляемые. "
        "Не an advice ❌ → a piece of advice ✅. "
        "Запомнил пару таких слов — и звучишь аккуратнее уже на A1!"
    ),
    # ─── A2 ───────────────────────────────────────────────────────────
    "will_future_a2": (
        "🦜 <b>Рико:</b> Будущее «прямо сейчас» — это <b>will</b>! "
        "Решение у кассы, обещание другу, прогноз погоды — везде will.\n\n"
        "Формула: will + V1. "
        "I'll help you — <i>Я тебе помогу</i>. "
        "It will rain tomorrow — <i>Завтра будет дождь</i>. "
        "won't = will not: I won't forget — <i>Я не забуду</i>.\n\n"
        "А going to — для планов и очевидных признаков: "
        "I'm going to study tonight — <i>Я собираюсь заниматься вечером</i>.\n\n"
        "Лайфхак: спонтанно — I'll take this. "
        "Уже решил вчера — I'm going to take a course. "
        "Почувствуешь разницу — и будущее перестанет быть кашей 🌤️"
    ),
    "used_to_a2": (
        "🦜 <b>Рико:</b> «Раньше делал, а сейчас нет» — "
        "для этого в английском есть красивая конструкция <b>used to</b>!\n\n"
        "used to + V1: I used to play football — "
        "<i>Я раньше играл в футбол</i> (сейчас уже нет). "
        "She used to live in Paris — <i>Она раньше жила в Париже</i>.\n\n"
        "Вопрос: Did you use to…? "
        "Отрицание: I didn't use to… (после did — без -d!).\n\n"
        "Не путай с be used to + -ing = «привык сейчас»: "
        "I'm used to getting up early — <i>Я привык рано вставать</i>. "
        "Похоже на слух — разные миры по смыслу. Различишь — уровень сразу вверх 📈"
    ),
    "something_anything_a2": (
        "🦜 <b>Рико:</b> Something / anything / nothing — "
        "три слова, без которых трудно сказать «что-то / что угодно / ничего». "
        "И тут русскоязычных часто ловит двойное отрицание!\n\n"
        "<b>something</b> — чаще в утверждениях: I need something — "
        "<i>Мне что-то нужно</i>.\n"
        "<b>anything</b> — вопросы и отрицания: Do you need anything? "
        "I don't need anything.\n"
        "<b>nothing</b> — «ничего» уже внутри себя: I need nothing.\n\n"
        "Лайфхак: не ставь два отрицания — "
        "I don't need nothing ❌ → I don't need anything / I need nothing ✅. "
        "Одно правило — и речь становится чище!"
    ),
    "prepositions_time_a2": (
        "🦜 <b>Рико:</b> Время тоже любит предлоги! "
        "<b>in / on / at</b> для часов, дней и месяцев — "
        "тема, после которой «в понедельник» перестаёт быть лотереей.\n\n"
        "<b>at</b> + точное время / night: at 8 pm, at night — "
        "<i>в 8 вечера, ночью</i>.\n"
        "<b>on</b> + день / дата: on Monday, on 5 May — "
        "<i>в понедельник, пятого мая</i>. "
        "I met her on Monday — <i>Я встретил её в понедельник</i>.\n"
        "<b>in</b> + месяц / год / часть дня: in July, in 2010, in the morning.\n\n"
        "Лайфхак: at the weekend (BrE), on the weekend (AmE). "
        "in the afternoon / evening — с the. "
        "Выучи три корзины — и даты зазвучат уверенно 📅"
    ),
    "adj_adv_a2": (
        "🦜 <b>Рико:</b> Прилагательное или наречие? "
        "Тема <b>Adjective vs adverb</b> — частая причина «почти правильно, но режет ухо».\n\n"
        "Adjective описывает существительное: a careful driver — "
        "<i>осторожный водитель</i>. "
        "Adverb описывает глагол: She drives carefully — "
        "<i>Она водит осторожно</i>.\n\n"
        "Часто -ly: quick → quickly. "
        "Но well (не good!) после глагола: He speaks English well — "
        "<i>Он хорошо говорит по-английски</i>.\n\n"
        "Лайфхак: после be — прилагательное (She is careful). "
        "После действия — наречие (She drives carefully). "
        "Один вопрос — и путаница заканчивается ✅"
    ),
    # ─── B1 ───────────────────────────────────────────────────────────
    "wish_b1": (
        "🦜 <b>Рико:</b> «Жаль, что…» — конструкция <b>wish</b>! "
        "Очень живая, эмоциональная, почти как вздох в разговоре.\n\n"
        "I wish + Past Simple — жаль про сейчас: "
        "I wish I knew — <i>Жаль, что я не знаю</i>. "
        "I wish I had more time — <i>Жаль, что мало времени</i>.\n\n"
        "I wish + would — раздражение / хочу, чтобы другой изменился: "
        "I wish you would listen — <i>Хоть бы ты слушал</i>.\n\n"
        "I wish + Past Perfect — жаль о прошлом: "
        "I wish I had studied — <i>Жаль, что тогда не учился</i>.\n\n"
        "Лайфхак: после wish о настоящем — «сдвиг» во Past. "
        "I wish I can ❌ → I wish I could ✅. "
        "Освоишь — сможешь говорить не только факты, но и чувства 💭"
    ),
    "so_such_b1": (
        "🦜 <b>Рико:</b> Хочешь усилить эмоцию? На помощь — <b>so</b> и <b>such</b>! "
        "«Так устал», «такой день» — по-английски тоже есть элегантный способ.\n\n"
        "<b>so</b> + прилагательное/наречие: so tired, so quickly — "
        "<i>так устал, так быстро</i>. "
        "It was so cold — <i>Было так холодно</i>.\n\n"
        "<b>such</b> + (a/an) + существительное: such a nice day — "
        "<i>такой хороший день</i>. "
        "such cold weather — <i>такая холодная погода</i> "
        "(weather неисчисляемое — без a).\n\n"
        "Лайфхак: so beautiful ✅ / such a beautiful girl ✅. "
        "such beautiful без существительного рядом — обычно нет. "
        "Пара минут практики — и усиление станет автоматическим!"
    ),
    "quantifiers_b1": (
        "🦜 <b>Рико:</b> «Несколько», «немного», «мало», «достаточно» — "
        "это <b>quantifiers</b>: a few, a little, plenty, enough… "
        "Они делают количество точным, без размытого «много».\n\n"
        "<b>a few</b> — несколько (исчисляемые): a few friends. "
        "<b>a little</b> — немного (неисчисляемые): a little milk. "
        "few / little без a — «мало» с грустным оттенком.\n\n"
        "plenty of, a lot of, enough: We have enough time — "
        "<i>У нас достаточно времени</i>.\n\n"
        "Лайфхак: a few books ✅ / a little water ✅. "
        "Не a few water ❌. "
        "Выбрал правильную «корзину» — и звучишь естественно!"
    ),
    "question_tags_b1": (
        "🦜 <b>Рико:</b> Хвостик в конце фразы — <b>question tags</b>! "
        "Как русское «правда?» / «не так ли?» — и речь сразу становится живой.\n\n"
        "You're tired, aren't you? — <i>Ты устал, правда?</i> "
        "She works here, doesn't she? "
        "Правило-качели: плюс в предложении → минус в tag, и наоборот: "
        "You don't like it, do you?\n\n"
        "Особый случай: I'm late, aren't I? (не amn't I — так не говорят).\n\n"
        "Лайфхак: слушай интонацию — вниз = почти утверждение, "
        "вверх = правда спрашиваю. "
        "Tags — маленький секрет «как в сериале» 🎬"
    ),
    "linking_b1": (
        "🦜 <b>Рико:</b> Связки — клей умного текста: "
        "<b>because, so, although, however, therefore</b>. "
        "Без них мысли прыгают, со связками — читаются как история.\n\n"
        "because — причина: I stayed home because it was raining — "
        "<i>…потому что шёл дождь</i>. "
        "so — следствие: It was raining, so I stayed home.\n\n"
        "although / though — хотя: Although I was tired, I finished. "
        "however — однако; therefore — поэтому (чуть формальнее).\n\n"
        "Лайфхак: because + предложение. "
        "because of + существительное: because of the rain. "
        "Одна пара — и уровень письма заметно растёт ✍️"
    ),
    # ─── B2 ───────────────────────────────────────────────────────────
    "wish_if_only_b2": (
        "🦜 <b>Рико:</b> <b>If only</b> — это wish на максимальной громкости эмоций! "
        "Когда «жалко» уже мало, а хочется вздохнуть сильнее.\n\n"
        "If only I had more time! — "
        "<i>Если бы только у меня было больше времени!</i> "
        "Времена те же, что у wish: Past Simple (сейчас), "
        "would (про другого), Past Perfect (прошлое).\n\n"
        "If only he would call — <i>Хоть бы он позвонил</i>. "
        "If only I had known — <i>Знай я раньше…</i>\n\n"
        "Лайфхак: If only звучит драматичнее I wish. "
        "В дневнике, в разговоре по душам, в storytelling — настоящее золото 🔥"
    ),
    "causatives_b2": (
        "🦜 <b>Рико:</b> «Мне сделали», а не «я сам» — "
        "это каузатив <b>have / get something done</b>! "
        "Очень бытовая и очень взрослая конструкция.\n\n"
        "have/get + объект + V3: I had my hair cut — "
        "<i>Мне подстригли волосы</i>. "
        "I got my phone fixed — <i>Мне починили телефон</i>.\n\n"
        "Have someone do something: I'll have the assistant call you — "
        "<i>Пусть ассистент тебе позвонит</i>.\n\n"
        "Лайфхак: фокус не на мастере, а на результате для тебя. "
        "Выучишь — сервис, ремонт и быт зазвучат по-английски естественно ✂️"
    ),
    "future_perfect_b2": (
        "🦜 <b>Рико:</b> «К пятнице уже будет готово» — "
        "это не обычное будущее, а <b>Future Perfect</b>! "
        "Время для дедлайнов и планов с финишной чертой.\n\n"
        "will have + V3: By Friday I will have finished — "
        "<i>К пятнице я уже закончу</i>. "
        "By 2030 they will have built a new station — "
        "<i>К 2030 они уже построят…</i>\n\n"
        "Ключ — точка в будущем (by Monday, by then), "
        "к которой действие уже завершится.\n\n"
        "Лайфхак: by = «к моменту». "
        "Не путай с простым will (просто факт в будущем). "
        "Future Perfect — про «уже сделано к…» ⏳"
    ),
    "participle_adj_b2": (
        "🦜 <b>Рико:</b> Bored или boring? "
        "Классическая ловушка — прилагательные на <b>-ed / -ing</b>! "
        "Путают все уровни, пока не щёлкнет картинка.\n\n"
        "<b>-ed</b> — чувство человека: I'm bored — <i>Мне скучно</i>. "
        "I'm interested in art — <i>Мне интересно искусство</i>.\n"
        "<b>-ing</b> — качество вещи/ситуации: The film is boring — "
        "<i>Фильм скучный</i>. An interesting book.\n\n"
        "tired / tiring, excited / exciting — та же логика.\n\n"
        "Лайфхак: «кто чувствует?» → -ed. "
        "«что вызывает чувство?» → -ing. "
        "Два вопроса — и тема закрыта навсегда ✅"
    ),
    "connectors_b2": (
        "🦜 <b>Рико:</b> Связки уровня B2 — "
        "<b>despite, whereas, nevertheless, furthermore</b>… "
        "Ими эссе и уверенная речь отличаются от «ну и потом».\n\n"
        "despite / in spite of + noun/-ing: "
        "Despite the rain, we went out — <i>Несмотря на дождь…</i> "
        "(внимание: despite <b>без</b> of!).\n"
        "whereas — тогда как: I like tea, whereas she prefers coffee.\n"
        "nevertheless, furthermore, as long as — для аргументов и условий.\n\n"
        "Лайфхак: despite the rain ✅ / despite of the rain ❌. "
        "in spite of the rain ✅. "
        "Одна деталь — и текст звучит на уровень выше 📚"
    ),
    "would_rather_b2": (
        "🦜 <b>Рико:</b> Предпочтения по-взрослому — <b>would rather</b>! "
        "Мягче и естественнее, чем вечное I prefer.\n\n"
        "I'd rather stay home — <i>Я бы лучше остался дома</i>. "
        "I'd rather not talk about it — <i>Лучше не будем об этом</i>.\n\n"
        "Про другого человека — Past: "
        "I'd rather you didn't smoke — "
        "<i>Я бы предпочёл, чтобы ты не курил</i>.\n\n"
        "Лайфхак: rather + V1 про себя. "
        "rather + Past про чужое поведение. "
        "Звучит мягко, вежливо и очень native 🌿"
    ),
    # ─── C1 ───────────────────────────────────────────────────────────
    "hedging_c1": (
        "🦜 <b>Рико:</b> Академичная осторожность — <b>hedging</b>! "
        "Чтобы не звучать как человек, который «всё знает на 100%», "
        "когда данные чуть сложнее.\n\n"
        "seem / appear to / tend to: The results appear to suggest… — "
        "<i>Результаты, похоже, говорят о…</i> "
        "it could be argued that… — <i>можно утверждать, что…</i> "
        "somewhat, relatively, to some extent — мягкие дозаторы силы.\n\n"
        "Лайфхак: в эссе This proves ❌ часто грубо. "
        "This appears to indicate ✅ — зрелый тон. "
        "Hedging — не слабость, а контроль уверенности 🎓"
    ),
    "emphasis_do_c1": (
        "🦜 <b>Рико:</b> Когда нужно усилить — "
        "английский достаёт волшебные <b>do / does / did</b>! "
        "Это не вопрос, это акцент: «да я же…!»\n\n"
        "I do understand! — <i>Да я понимаю!</i> "
        "She does work hard — <i>Она правда много работает</i>. "
        "I did tell you — <i>Я же говорил тебе</i>.\n\n"
        "Do sit down! — вежливо-настойчиво: <i>Да садитесь же!</i>\n\n"
        "Лайфхак: do + V1, ударение на do. "
        "Не путай с обычным Do you…? "
        "Emphasis do — эмоция без крика 🔊"
    ),
    "collocations_c1": (
        "🦜 <b>Рико:</b> Слова живут парами — <b>collocations</b>! "
        "Носитель скажет make a decision, а не do a decision — "
        "и ухо сразу чувствует «своё / чужое».\n\n"
        "make a decision, take a risk, heavy rain, strong coffee, "
        "highly likely, deeply concerned. "
        "Учи готовые куски — так речь собирается быстрее, чем из одиночных слов.\n\n"
        "Лайфхак: из каждого текста выписывай 3 пары. "
        "Через месяц у тебя уже другой английский — более «собранный» 📈"
    ),
    "formal_informal_c1": (
        "🦜 <b>Рико:</b> Регистр — <b>formal vs informal</b>. "
        "Одна идея, разные «костюмы»: чат с другом и письмо боссу — не одно и то же.\n\n"
        "Informal: kids, gonna, a lot, Can you…? "
        "Formal: children, going to, numerous, "
        "I would be grateful if you could…\n\n"
        "I need help → I would appreciate your assistance.\n\n"
        "Лайфхак: сначала смысл, потом подкрути слова под ситуацию. "
        "Слишком formal с другом = странно; слишком slang на работе = риск. "
        "Гибкость регистра — признак C1 👔"
    ),
    "subjunctive_c1": (
        "🦜 <b>Рико:</b> В требованиях и рекомендациях живёт "
        "<b>subjunctive</b> — «чтобы он был», без привычного -s.\n\n"
        "It's essential that he <b>be</b> present — "
        "<i>Важно, чтобы он присутствовал</i>. "
        "They recommended that she take the exam.\n\n"
        "В AmE так чаще; в BrE часто should: "
        "…that she should take the exam.\n\n"
        "Лайфхак: после essential / important / recommend / suggest "
        "смотри на «голый» глагол: that he go ✅, that he goes ❌ "
        "(в этом формальном паттерне). Звучит официально и точно ⚖️"
    ),
    "fronting_c1": (
        "🦜 <b>Рико:</b> Вынос вперёд для акцента — <b>fronting</b>! "
        "Как прожектор: «смотри сюда, вот это важно».\n\n"
        "This I cannot accept — <i>Вот этого я принять не могу</i>. "
        "Never have I seen such chaos — инверсия после отрицательного наречия.\n\n"
        "Используется в убедительной и литературной речи — "
        "не в каждом предложении, а точечно.\n\n"
        "Лайфхак: после never / rarely / seldom часто инверсия: "
        "Never have I… "
        "Fronting = контроль внимания слушателя 🔦"
    ),
    # ─── C2 ───────────────────────────────────────────────────────────
    "advanced_hedging_c2": (
        "🦜 <b>Рико:</b> Hedging уровня C2 — ювелирная точность! "
        "Ты не прячешься, ты дозируешь силу утверждения как профи.\n\n"
        "to a certain extent, it is not unreasonable to suggest, "
        "one might tentatively conclude, "
        "the evidence would appear to indicate…\n\n"
        "Это не «вода», а академический и дипломатический контроль тона.\n\n"
        "Лайфхак: чем сильнее claim, тем больше ответственности. "
        "C2 умеет звучать уверенно — и при этом осторожно. Редкая суперсила 🧪"
    ),
    "understatement_c2": (
        "🦜 <b>Рико:</b> Британское преуменьшение — "
        "<b>understatement & irony</b>! "
        "Когда «not bad» может значить «очень даже хорошо» 😏\n\n"
        "It's not bad — часто комплимент. "
        "A bit of a problem — может быть серьёзно. "
        "We may have a slight issue… — мягкая тревога в вежливом костюме.\n\n"
        "Ирония через мягкие слова: слушай контекст и тон, не только словарь.\n\n"
        "Лайфхак: не переводи буквально. "
        "Understatement — культурный код. Поймёшь его — поймёшь половину British humour 🇬🇧"
    ),
    "cleft_advanced_c2": (
        "🦜 <b>Рико:</b> Расщеплённые конструкции — <b>advanced clefts</b>! "
        "Они ставят прожектор на нужную часть фразы.\n\n"
        "It was John who called — <i>Это Джон позвонил</i> (не кто-то другой). "
        "What I need is rest — <i>Что мне нужно — так это отдых</i>. "
        "The reason why… is… — объяснить причину с акцентом.\n\n"
        "Лайфхак: сначала выбери, что подсветить, "
        "потом собирай It was… who/that… или What… is… "
        "Cleft = контроль фокуса, почти режиссура речи 🎬"
    ),
    "discourse_c2": (
        "🦜 <b>Рико:</b> Управление вниманием слушателя — "
        "<b>discourse control</b>! "
        "Ты не сыплешь факты, ты ведёшь человека по мысли.\n\n"
        "Signposting: firstly, that said, crucially, in practical terms, "
        "to put it another way, what this means is…\n\n"
        "В презентации и эссе это разница между «слушали» и «поняли».\n\n"
        "Лайфхак: каждые 30–40 секунд — маленький signpost. "
        "Люди не теряются, а ты звучишь как человек, который держит карту разговора 🗺️"
    ),
    "lexical_grammar_c2": (
        "🦜 <b>Рико:</b> Грамматика через лексику — <b>lexical grammar</b>! "
        "На C2 ошибки часто не в «времени», а в слотах: rely on, не rely of.\n\n"
        "Dependent prepositions: rely on, accuse of, capable of. "
        "Patterns: suggest that / suggest -ing; "
        "prevent someone from -ing. "
        "Chunks: on the other hand, as a matter of fact.\n\n"
        "Лайфхак: учи не слово, а слот — rely __ → on. "
        "Так предлоги перестают быть лотереей и становятся привычкой 🧩"
    ),
    "persuasion_c2": (
        "🦜 <b>Рико:</b> Убеждение — <b>persuasion patterns</b>! "
        "Риторика + грамматика: как говорить так, чтобы тебя слышали, а не спорили сразу.\n\n"
        "Rhetorical questions: Isn't it time we acted? "
        "Triad (триада): clarity, care, courage. "
        "Concession–refutation: While X is true, Y remains more important…\n\n"
        "Лайфхак: сначала признай сильную сторону другого (While…), "
        "потом мягко разверни к своему тезису. "
        "Уверенно, без агрессии — стиль сильного спикера 🎤"
    ),
}

# Короткие формулы в конце (как у can) — подмешиваются через append_formula_deep_dive
FORMULA_EXTRAS: dict[str, str] = {
    "colors_a0": (
        "\n\nПовторим формулы: <b>It is + color</b>. "
        "What color is it? — It's blue — <i>Синее</i>. "
        "Цвет после is/are, не перед существительным без глагола."
    ),
    "family_a0": (
        "\n\nПовторим: This is my mum — <i>Это моя мама</i>. "
        "I have / I've got a brother. Have you got…? / Do you have…?"
    ),
    "prepositions_place_a0": (
        "\n\nПовторим: <b>in</b> = внутри, <b>on</b> = на, <b>at</b> = у точки. "
        "at home (без the). The book is on the table — <i>Книга на столе</i>."
    ),
    "have_got_a0": (
        "\n\nПовторим: I've got / She's got + noun. "
        "Have you got…? I haven't got… (= I don't have)."
    ),
    "imperatives_a0": (
        "\n\nПовторим: <b>V1!</b> Please + V1. Don't + V1. Let's + V1. "
        "Open the door! Don't touch! Let's go!"
    ),
    "possessives_a0": (
        "\n\nПовторим: my/your/his/her/its/our/their + noun. "
        "This is my bag. Не путай their / there / they're и its / it's."
    ),
    "days_weather_a0": (
        "\n\nПовторим: on Monday. <b>It's</b> + weather. "
        "It's sunny today — <i>Сегодня солнечно</i>. What's the weather like?"
    ),
    "possessive_s_a1": (
        "\n\nПовторим: Name's + thing (Dan's book). "
        "students' room (мн. на -s). it's ≠ its."
    ),
    "object_pronouns_a1": (
        "\n\nПовторим: me/him/her/us/them после глагола и предлога. "
        "I like him ✅ / I like he ❌. Look at them."
    ),
    "like_ing_a1": (
        "\n\nПовторим: like/love/hate/enjoy + <b>-ing</b>. "
        "would like <b>to</b> + V1 — I'd like to go."
    ),
    "adverbs_frequency_a1": (
        "\n\nПовторим: always…never перед глаголом; после am/is/are. "
        "I often play. She is always late."
    ),
    "wh_questions_a1": (
        "\n\nПовторим: Wh- + do/does/is…? "
        "Where do you live? What does she want? (после does — без -s)."
    ),
    "countable_a1": (
        "\n\nПовторим: a book / books; water/advice без a. "
        "many + исчисл., much + неисчисл., a piece of advice."
    ),
    "will_future_a2": (
        "\n\nПовторим: <b>will + V1</b>, won't. "
        "I'll help. Going to — планы/признаки: I'm going to study."
    ),
    "used_to_a2": (
        "\n\nПовторим: used to + V1 (раньше). "
        "Did you use to…? ≠ be used to + -ing (привык сейчас)."
    ),
    "something_anything_a2": (
        "\n\nПовторим: something (+), anything (?/−), nothing. "
        "Не I don't need nothing ❌."
    ),
    "prepositions_time_a2": (
        "\n\nПовторим: <b>at</b> + время, <b>on</b> + день/дата, <b>in</b> + месяц/год. "
        "I met her on Monday — <i>Я встретил её в понедельник</i>."
    ),
    "adj_adv_a2": (
        "\n\nПовторим: adj + noun (a careful driver); verb + adv (drives carefully). "
        "well, не good после глагола."
    ),
    "wish_b1": (
        "\n\nПовторим: I wish + Past (сейчас); + would (про другого); "
        "+ Past Perfect (прошлое). I wish I could ✅"
    ),
    "so_such_b1": (
        "\n\nПовторим: so + adj/adv; such (+ a/an) + noun. "
        "so cold / such a cold day / such cold weather."
    ),
    "quantifiers_b1": (
        "\n\nПовторим: a few + исчисл.; a little + неисчисл.; enough / plenty of."
    ),
    "question_tags_b1": (
        "\n\nПовторим: + предложение → − tag (и наоборот). "
        "You're tired, aren't you? I'm late, aren't I?"
    ),
    "linking_b1": (
        "\n\nПовторим: because / so / although / however. "
        "because + clause; because of + noun."
    ),
    "wish_if_only_b2": (
        "\n\nПовторим: If only = усиленный wish. "
        "If only I had more time! If only he would call."
    ),
    "causatives_b2": (
        "\n\nПовторим: have/get + object + V3. "
        "I had my hair cut — <i>Мне подстригли</i>."
    ),
    "future_perfect_b2": (
        "\n\nПовторим: <b>will have + V3</b>. "
        "By Friday I will have finished — <i>К пятнице уже закончу</i>."
    ),
    "participle_adj_b2": (
        "\n\nПовторим: -ed = чувство (I'm bored); -ing = качество (boring film)."
    ),
    "connectors_b2": (
        "\n\nПовторим: despite (+ noun) / in spite of; whereas; nevertheless. "
        "despite of ❌"
    ),
    "would_rather_b2": (
        "\n\nПовторим: I'd rather + V1. "
        "I'd rather you didn't… (Past про другого)."
    ),
    "hedging_c1": (
        "\n\nПовторим: seem/appear to, tend to, to some extent, "
        "it could be argued that…"
    ),
    "emphasis_do_c1": (
        "\n\nПовторим: I do understand! She does work hard. Do sit down!"
    ),
    "collocations_c1": (
        "\n\nПовторим: make a decision, take a risk, heavy rain, highly likely — "
        "учи пары."
    ),
    "formal_informal_c1": (
        "\n\nПовторим: get ↔ obtain, ask ↔ inquire, "
        "Can you…? ↔ I would be grateful if…"
    ),
    "subjunctive_c1": (
        "\n\nПовторим: It's essential that he <b>be</b>… / that she take… "
        "(или should + V1 в BrE)."
    ),
    "fronting_c1": (
        "\n\nПовторим: This I cannot accept. Never have I seen… "
        "(инверсия после never/rarely)."
    ),
    "advanced_hedging_c2": (
        "\n\nПовторим: to a certain extent; one might tentatively conclude; "
        "the evidence would appear to indicate…"
    ),
    "understatement_c2": (
        "\n\nПовторим: It's not bad (= очень даже хорошо). "
        "a bit of a problem — часто сильнее, чем звучит."
    ),
    "cleft_advanced_c2": (
        "\n\nПовторим: It was X who/that…; What I need is…; "
        "The reason why… is…"
    ),
    "discourse_c2": (
        "\n\nПовторим: firstly / that said / crucially / "
        "to put it another way — signposting."
    ),
    "lexical_grammar_c2": (
        "\n\nПовторим: rely on, prevent from -ing, suggest that / -ing — "
        "слоты важнее одиночных слов."
    ),
    "persuasion_c2": (
        "\n\nПовторим: rhetorical question; triad; "
        "While X is true, Y remains… (concession → свой тезис)."
    ),
}
