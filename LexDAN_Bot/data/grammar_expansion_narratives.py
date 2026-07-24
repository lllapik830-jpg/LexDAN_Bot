# -*- coding: utf-8 -*-
"""
Полные рассказы Рико для добавленных тем Grammar (формат как у базовых тем:
история → правило → примеры с переводом → лайфхак).
"""

NARRATIVES: dict[str, str] = {
    # ─── A0 ───────────────────────────────────────────────────────────
    "colors_a0": (
        "🦜 <b>Рико:</b> Сегодня раскрасим английский — тема <b>Colors / Цвета</b>! "
        "Без цветов не описать машину, одежду и даже настроение 🎨\n\n"
        "База: <b>red, blue, green, yellow, black, white, orange, pink, brown, grey</b>. "
        "Цвет почти всегда стоит <b>после</b> is/are: "
        "The car is red — <i>Машина красная</i>. "
        "The flowers are yellow — <i>Цветы жёлтые</i>.\n\n"
        "Вопрос: What color is it? — <i>Какого оно цвета?</i> "
        "It's blue — <i>Синее</i>.\n\n"
        "<b>Лайфхак:</b> не говори «the car red» ❌ — нужен глагол is. "
        "И grey (BrE) = gray (AmE), оба ок. Дальше — задания!"
    ),
    "family_a0": (
        "🦜 <b>Рико:</b> Идём в семью — <b>Family</b>! Эти слова нужны с первого знакомства.\n\n"
        "mother / mum, father / dad, sister, brother, parents, grandparents, "
        "son, daughter, friend. "
        "This is my mum — <i>Это моя мама</i>. "
        "I have one brother — <i>У меня один брат</i>. "
        "They are my parents — <i>Это мои родители</i>.\n\n"
        "Вопрос: Have you got a sister? / Do you have a sister? — "
        "<i>У тебя есть сестра?</i>\n\n"
        "<b>Лайфхак:</b> mum/dad — разговорные и очень частые. "
        "friend тоже «семья круга» — смело используй. Погнали к заданиям!"
    ),
    "prepositions_place_a0": (
        "🦜 <b>Рико:</b> Три маленьких слова — и огромная ясность: "
        "<b>in / on / at</b> (место)!\n\n"
        "<b>in</b> — внутри: in the room, in the bag — "
        "<i>в комнате, в сумке</i>.\n"
        "<b>on</b> — на поверхности: on the table, on the wall — "
        "<i>на столе, на стене</i>.\n"
        "<b>at</b> — точка / место встречи: at school, at the door, at home — "
        "<i>в школе, у двери, дома</i>.\n\n"
        "The cat is in the box — <i>Кот в коробке</i>. "
        "The book is on the table — <i>Книга на столе</i>. "
        "She is at school — <i>Она в школе</i>.\n\n"
        "<b>Лайфхак:</b> at home без the. Не путай in school (процесс учёбы) "
        "и at school (там сейчас). Тренируем!"
    ),
    "have_got_a0": (
        "🦜 <b>Рико:</b> Британская классика — <b>have got</b> («у меня есть»)!\n\n"
        "I've got a phone — <i>У меня есть телефон</i> (= I have a phone). "
        "She's got a cat — <i>У неё есть кот</i>. "
        "We've got two dogs — <i>У нас две собаки</i>.\n\n"
        "Вопрос: Have you got a pen? — <i>У тебя есть ручка?</i> "
        "Отрицание: I haven't got any money — <i>У меня нет денег</i>.\n\n"
        "<b>Лайфхак:</b> в США чаще просто have / do you have. "
        "Оба варианта правильные — выбирай тот, что слышишь чаще. "
        "После got не ставь to 😄"
    ),
    "imperatives_a0": (
        "🦜 <b>Рико:</b> Команды и просьбы — <b>Imperatives</b>! "
        "Это когда глагол идёт сразу, без to.\n\n"
        "Open the door! — <i>Открой дверь!</i> "
        "Sit down! — <i>Садись!</i> "
        "Listen to me! — <i>Слушай меня!</i>\n\n"
        "Вежливо добавь Please: Please open the window — "
        "<i>Пожалуйста, открой окно</i>. "
        "Отрицание: Don't touch! — <i>Не трогай!</i> "
        "Don't be late! — <i>Не опаздывай!</i>\n\n"
        "Let's go! — <i>Пойдём!</i> (мы вместе).\n\n"
        "<b>Лайфхак:</b> Don't + V1, не Doesn't. "
        "В жизни Please спасает тон — звучишь дружелюбнее 💚"
    ),
    "possessives_a0": (
        "🦜 <b>Рико:</b> Чей это? Тема <b>my / your / his / her…</b>!\n\n"
        "Перед существительным: "
        "<b>my, your, his, her, its, our, their</b>. "
        "This is my bag — <i>Это моя сумка</i>. "
        "That's her phone — <i>Это её телефон</i>. "
        "Their house is big — <i>Их дом большой</i>.\n\n"
        "Is this your book? — <i>Это твоя книга?</i> "
        "Tom loves his dog — <i>Том любит свою собаку</i>.\n\n"
        "<b>Лайфхак:</b> не путай their (их), there (там) и they're (they are). "
        "its = его/её (вещь), it's = it is. Классика ловушек!"
    ),
    "days_weather_a0": (
        "🦜 <b>Рико:</b> Дни недели и погода — то, о чём болтают каждый день!\n\n"
        "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. "
        "Today is Friday — <i>Сегодня пятница</i>. "
        "See you on Sunday — <i>Увидимся в воскресенье</i> (on + день).\n\n"
        "Погода: sunny, rainy, cloudy, cold, hot, windy. "
        "It's sunny today — <i>Сегодня солнечно</i>. "
        "What's the weather like? — <i>Какая погода?</i> "
        "It's cold — <i>Холодно</i>.\n\n"
        "<b>Лайфхак:</b> It's + погода (It's rainy), не It rainy. "
        "Дни с большой буквы: Monday ✅"
    ),
    # ─── A1 ───────────────────────────────────────────────────────────
    "possessive_s_a1": (
        "🦜 <b>Рико:</b> Маленький хвостик <b>'s</b> — и сразу ясно «чей» предмет!\n\n"
        "Dan's book — <i>книга Дана</i>. "
        "My sister's phone — <i>телефон моей сестры</i>. "
        "Это possessive 's: хозяин + 's + вещь.\n\n"
        "Если хозяев много и слово уже на -s: the students' room — "
        "<i>комната студентов</i> (апостроф после s).\n\n"
        "<b>Лайфхак:</b> <b>it's</b> = it is / it has. "
        "<b>its</b> = его/её (принадлежность): The dog wagged its tail. "
        "Путают все — ты теперь нет 😎"
    ),
    "object_pronouns_a1": (
        "🦜 <b>Рико:</b> После глагола и предлога нужны другие местоимения — "
        "<b>object pronouns</b>!\n\n"
        "I → <b>me</b>, you → you, he → <b>him</b>, she → <b>her</b>, "
        "it → it, we → <b>us</b>, they → <b>them</b>.\n\n"
        "I like him — <i>Он мне нравится</i> (не I like he ❌). "
        "She called me — <i>Она мне позвонила</i>. "
        "Look at them — <i>Посмотри на них</i>. "
        "Can you help us? — <i>Можешь помочь нам?</i>\n\n"
        "<b>Лайфхак:</b> спроси себя: это «кто делает» (I/he) или "
        "«на кого действие» (me/him)? Второе — object 🎯"
    ),
    "like_ing_a1": (
        "🦜 <b>Рико:</b> Про хобби и удовольствия — конструкция <b>like + -ing</b>!\n\n"
        "I like swimming — <i>Я люблю плавать</i> (как занятие). "
        "She loves reading — <i>Она обожает читать</i>. "
        "Также: love / hate / enjoy + -ing. "
        "I enjoy cooking — <i>Мне нравится готовить</i>.\n\n"
        "Вежливое желание: would like <b>to</b> + V1 — "
        "I'd like to drink coffee — <i>Я бы хотел выпить кофе</i>.\n\n"
        "<b>Лайфхак:</b> like + -ing = про процесс/хобби. "
        "would like to = «хотел бы» сейчас. Не путай их!"
    ),
    "adverbs_frequency_a1": (
        "🦜 <b>Рико:</b> Как часто? Наречия частоты — "
        "<b>always, usually, often, sometimes, rarely, never</b>!\n\n"
        "Место: обычно <b>перед</b> смысловым глаголом: "
        "I often play football — <i>Я часто играю в футбол</i>. "
        "Но после am/is/are: She is always late — <i>Она всегда опаздывает</i>.\n\n"
        "I sometimes watch films. We never eat meat.\n\n"
        "<b>Лайфхак:</b> шкала от always (100%) до never (0%). "
        "sometimes можно ставить и в начале: Sometimes I walk. Удобно!"
    ),
    "wh_questions_a1": (
        "🦜 <b>Рико:</b> Вопросы «кто-что-где» — <b>Wh- questions</b>! "
        "Без них диалог не живёт.\n\n"
        "What, where, when, who, why, how + вспомогательный (do/does/is…).\n"
        "Where do you live? — <i>Где ты живёшь?</i> "
        "What does she want? — <i>Чего она хочет?</i> "
        "Who is that? — <i>Кто это?</i> "
        "Why are you sad? — <i>Почему ты грустный?</i>\n\n"
        "How often…? — <i>Как часто…?</i> "
        "How much / How many…? — <i>Сколько…?</i>\n\n"
        "<b>Лайфхак:</b> после does глагол без -s: What does he like? ✅"
    ),
    "countable_a1": (
        "🦜 <b>Рико:</b> Можно посчитать или нет? "
        "<b>Countable / Uncountable</b>!\n\n"
        "Исчисляемые: a book / books, an apple / apples. "
        "Неисчисляемые: water, rice, milk, advice, information — "
        "обычно без a/an и без -s.\n\n"
        "some water — <i>немного воды</i>, many books — <i>много книг</i>, "
        "much rice — <i>много риса</i>. "
        "a piece of advice — <i>один совет</i> (чтобы «посчитать»).\n\n"
        "<b>Лайфхак:</b> advice и information — неисчисляемые. "
        "Не an advice ❌ → a piece of advice ✅"
    ),
    # ─── A2 ───────────────────────────────────────────────────────────
    "will_future_a2": (
        "🦜 <b>Рико:</b> Будущее «на месте» — <b>will</b>! "
        "Решение сейчас, обещание, прогноз.\n\n"
        "will + V1: I'll help you — <i>Я тебе помогу</i>. "
        "It will rain tomorrow — <i>Завтра будет дождь</i>. "
        "won't = will not: I won't forget — <i>Я не забуду</i>.\n\n"
        "Going to — для планов и очевидных признаков: "
        "I'm going to study tonight — <i>Я собираюсь заниматься вечером</i>.\n\n"
        "<b>Лайфхак:</b> спонтанно у кассы — I'll take this. "
        "Уже решил вчера — I'm going to take a course. Чувствуешь разницу?"
    ),
    "used_to_a2": (
        "🦜 <b>Рико:</b> «Раньше делал, а сейчас нет» — это <b>used to</b>!\n\n"
        "used to + V1: I used to play football — "
        "<i>Я раньше играл в футбол</i> (сейчас уже нет). "
        "She used to live in Paris — <i>Она раньше жила в Париже</i>.\n\n"
        "Вопрос: Did you use to…? Отрицание: I didn't use to… "
        "(без -d после did).\n\n"
        "<b>Лайфхак:</b> не путай с be used to + -ing = «привык сейчас»: "
        "I'm used to getting up early — <i>Я привык рано вставать</i>. "
        "Разные миры!"
    ),
    "something_anything_a2": (
        "🦜 <b>Рико:</b> Something / anything / nothing — "
        "три слова про «что-то / что угодно / ничего».\n\n"
        "<b>something</b> — чаще в утверждениях: I need something — "
        "<i>Мне что-то нужно</i>.\n"
        "<b>anything</b> — вопросы и отрицания: Do you need anything? "
        "I don't need anything.\n"
        "<b>nothing</b> — «ничего» (уже отрицание в себе): I need nothing.\n\n"
        "<b>Лайфхак:</b> не ставь два отрицания: "
        "I don't need nothing ❌ → I don't need anything / I need nothing ✅"
    ),
    "prepositions_time_a2": (
        "🦜 <b>Рико:</b> Время тоже любит предлоги — "
        "<b>in / on / at</b> для часов, дней и месяцев!\n\n"
        "<b>at</b> + точное время / night: at 8 pm, at night — "
        "<i>в 8 вечера, ночью</i>.\n"
        "<b>on</b> + день / дата: on Monday, on 5 May — "
        "<i>в понедельник, пятого мая</i>. "
        "I met her on Monday — <i>Я встретил её в понедельник</i>.\n"
        "<b>in</b> + месяц / год / часть дня: in July, in 2010, in the morning.\n\n"
        "<b>Лайфхак:</b> at the weekend (BrE), on the weekend (AmE). "
        "in the afternoon / evening — с the!"
    ),
    "adj_adv_a2": (
        "🦜 <b>Рико:</b> Прилагательное или наречие? "
        "<b>Adjective vs adverb</b> — частая путаница!\n\n"
        "Adjective описывает существительное: a careful driver — "
        "<i>осторожный водитель</i>. "
        "Adverb описывает глагол: She drives carefully — "
        "<i>Она водит осторожно</i>.\n\n"
        "Часто -ly: quick → quickly, slow → slowly. "
        "Но well (не good) после глагола: He speaks English well — "
        "<i>Он хорошо говорит по-английски</i>.\n\n"
        "<b>Лайфхак:</b> после be — прилагательное: She is careful. "
        "После действия — наречие: She drives carefully."
    ),
    # ─── B1 ───────────────────────────────────────────────────────────
    "wish_b1": (
        "🦜 <b>Рико:</b> «Жаль, что…» — конструкция <b>wish</b>! "
        "Очень живая и эмоциональная.\n\n"
        "I wish + Past Simple — жаль про сейчас: "
        "I wish I knew — <i>Жаль, что я не знаю</i>. "
        "I wish I had more time — <i>Жаль, что у меня мало времени</i>.\n\n"
        "I wish + would — раздражение / хочу, чтобы другой изменился: "
        "I wish you would listen — <i>Хоть бы ты слушал</i>.\n\n"
        "I wish + Past Perfect — жаль о прошлом: "
        "I wish I had studied — <i>Жаль, что я не учился тогда</i>.\n\n"
        "<b>Лайфхак:</b> после wish о настоящем — «сдвиг» во Past. "
        "I wish I can ❌ → I wish I could ✅"
    ),
    "so_such_b1": (
        "🦜 <b>Рико:</b> Усиление эмоции — <b>so</b> и <b>such</b>!\n\n"
        "<b>so</b> + прилагательное/наречие: so tired, so quickly — "
        "<i>так устал, так быстро</i>. "
        "It was so cold — <i>Было так холодно</i>.\n\n"
        "<b>such</b> + (a/an) + существительное: such a nice day — "
        "<i>такой хороший день</i>. "
        "such cold weather — <i>такая холодная погода</i> (без a, weather неисчисл.).\n\n"
        "<b>Лайфхак:</b> so beautiful ✅ / such a beautiful girl ✅. "
        "such beautiful ❌ без существительного рядом."
    ),
    "quantifiers_b1": (
        "🦜 <b>Рико:</b> Сколько именно? <b>Quantifiers</b> — "
        "a few, a little, plenty…\n\n"
        "<b>a few</b> — несколько (исчисляемые): a few friends. "
        "<b>a little</b> — немного (неисчисляемые): a little milk. "
        "few / little без a — «мало» с негативным оттенком.\n\n"
        "plenty of, a lot of, enough — «достаточно / много». "
        "We have enough time — <i>У нас достаточно времени</i>.\n\n"
        "<b>Лайфхак:</b> a few books ✅ / a little water ✅. "
        "Не a few water ❌"
    ),
    "question_tags_b1": (
        "🦜 <b>Рико:</b> Хвостик-вопрос в конце — <b>question tags</b>! "
        "Как «правда?» / «не так ли?»\n\n"
        "You're tired, aren't you? — <i>Ты устал, правда?</i> "
        "She works here, doesn't she? "
        "Положительное предложение → отрицательный tag, и наоборот: "
        "You don't like it, do you?\n\n"
        "Особый случай: I'm late, aren't I? (не amn't I).\n\n"
        "<b>Лайфхак:</b> слушай интонацию: вниз = уверен, вверх = реально спрашивает."
    ),
    "linking_b1": (
        "🦜 <b>Рико:</b> Связки делают текст взрослым — "
        "<b>because, so, although, however…</b>!\n\n"
        "because — причина: I stayed home because it was raining — "
        "<i>…потому что шёл дождь</i>. "
        "so — следствие: It was raining, so I stayed home.\n\n"
        "although / though — хотя: Although I was tired, I finished. "
        "however — однако (часто с запятой). "
        "therefore — поэтому (формальнее).\n\n"
        "<b>Лайфхак:</b> because + предложение. "
        "because of + существительное: because of the rain."
    ),
    # ─── B2 ───────────────────────────────────────────────────────────
    "wish_if_only_b2": (
        "🦜 <b>Рико:</b> <b>If only</b> — это wish на максимуме эмоций!\n\n"
        "If only I had more time! — <i>Если бы только у меня было больше времени!</i> "
        "Те же времена, что у wish: Past Simple (сейчас), "
        "would (про другого), Past Perfect (прошлое).\n\n"
        "If only he would call — <i>Хоть бы он позвонил</i>. "
        "If only I had known — <i>Знай я раньше…</i>\n\n"
        "<b>Лайфхак:</b> If only звучит сильнее и драматичнее, чем I wish. "
        "В дневнике и разговорах — огонь 🔥"
    ),
    "causatives_b2": (
        "🦜 <b>Рико:</b> «Мне сделали» — каузатив <b>have / get something done</b>!\n\n"
        "have/get + объект + V3: I had my hair cut — "
        "<i>Мне подстригли волосы</i> (не сам). "
        "I got my phone fixed — <i>Мне починили телефон</i>.\n\n"
        "Have someone do something: I'll have the assistant call you — "
        "<i>Пусть ассистент тебе позвонит</i>.\n\n"
        "<b>Лайфхак:</b> фокус не на том, кто сделал, а что сделали тебе/для тебя. "
        "Очень частая конструкция в быту!"
    ),
    "future_perfect_b2": (
        "🦜 <b>Рико:</b> К пятнице уже будет готово — это <b>Future Perfect</b>!\n\n"
        "will have + V3: By Friday I will have finished — "
        "<i>К пятнице я уже закончу</i>. "
        "By 2030 they will have built a new station — "
        "<i>К 2030 они уже построят…</i>\n\n"
        "Ключ — точка в будущем (by Monday, by then), "
        "к которой действие уже завершится.\n\n"
        "<b>Лайфхак:</b> by = «к моменту». "
        "Не путай с Future Simple (просто факт в будущем)."
    ),
    "participle_adj_b2": (
        "🦜 <b>Рико:</b> Bored или boring? Классика — "
        "<b>-ed / -ing adjectives</b>!\n\n"
        "<b>-ed</b> — чувство человека: I'm bored — <i>Мне скучно</i>. "
        "I'm interested in art — <i>Мне интересно искусство</i>.\n"
        "<b>-ing</b> — качество вещи/ситуации: The film is boring — "
        "<i>Фильм скучный</i>. An interesting book.\n\n"
        "tired / tiring, excited / exciting — та же логика.\n\n"
        "<b>Лайфхак:</b> спроси: «кто чувствует?» → -ed. "
        "«что вызывает чувство?» → -ing."
    ),
    "connectors_b2": (
        "🦜 <b>Рико:</b> Связки уровня B2 — "
        "<b>despite, whereas, nevertheless…</b>!\n\n"
        "despite / in spite of + noun/-ing: "
        "Despite the rain, we went out — <i>Несмотря на дождь…</i> "
        "(despite без of!).\n"
        "whereas — тогда как: I like tea, whereas she prefers coffee.\n"
        "nevertheless / furthermore / as long as — "
        "для эссе и уверенной речи.\n\n"
        "<b>Лайфхак:</b> despite the rain ✅ / despite of the rain ❌. "
        "in spite of the rain ✅"
    ),
    "would_rather_b2": (
        "🦜 <b>Рико:</b> Предпочтения по-взрослому — <b>would rather</b>!\n\n"
        "I'd rather stay home — <i>Я бы лучше остался дома</i> (= prefer). "
        "I'd rather not talk about it — <i>Лучше не будем об этом</i>.\n\n"
        "Про другого человека — Past: "
        "I'd rather you didn't smoke — <i>Я бы предпочёл, чтобы ты не курил</i>.\n\n"
        "<b>Лайфхак:</b> rather + V1 про себя. "
        "rather + Past про чужое поведение. Звучит мягко и естественно."
    ),
    # ─── C1 ───────────────────────────────────────────────────────────
    "hedging_c1": (
        "🦜 <b>Рико:</b> Академичная осторожность — <b>hedging</b>! "
        "Чтобы не звучать слишком категорично.\n\n"
        "seem / appear to / tend to: The results appear to suggest… — "
        "<i>Результаты, похоже, говорят о…</i> "
        "it could be argued that… — <i>можно утверждать, что…</i> "
        "somewhat, relatively, to some extent — смягчители.\n\n"
        "<b>Лайфхак:</b> в эссе и отчётах hedging = зрелость стиля. "
        "This proves ❌ → This appears to indicate ✅"
    ),
    "emphasis_do_c1": (
        "🦜 <b>Рико:</b> Когда хочешь усилить — <b>do / does / did</b> для emphasis!\n\n"
        "I do understand! — <i>Да я понимаю!</i> "
        "She does work hard — <i>Она правда много работает</i>. "
        "I did tell you — <i>Я же говорил тебе</i>.\n\n"
        "Do sit down! — вежливо-настойчиво: <i>Да садитесь же!</i>\n\n"
        "<b>Лайфхак:</b> do + V1, ударение на do. "
        "Не путай с обычным вопросом Do you…?"
    ),
    "collocations_c1": (
        "🦜 <b>Рико:</b> Слова живут парами — <b>collocations</b>! "
        "Носители говорят make a decision, не do a decision.\n\n"
        "make a decision, take a risk, heavy rain, strong coffee, "
        "highly likely, deeply concerned. "
        "Учи готовые куски — так речь звучит «своей».\n\n"
        "<b>Лайфхак:</b> веди мини-список collocations из текстов, "
        "которые читаешь. Один день — 3 пары. Через месяц — другой английский 📈"
    ),
    "formal_informal_c1": (
        "🦜 <b>Рико:</b> Регистр — <b>formal vs informal</b>. "
        "Одно и то же по-разному в чате и в письме боссу.\n\n"
        "Informal: kids, gonna, a lot, Can you…? "
        "Formal: children, going to, numerous, "
        "I would be grateful if you could…\n\n"
        "I need help → I would appreciate your assistance.\n\n"
        "<b>Лайфхак:</b> сначала смысл, потом «подкрути» слова под ситуацию. "
        "Слишком formal в чате с другом = странно; слишком slang на работе = риск."
    ),
    "subjunctive_c1": (
        "🦜 <b>Рико:</b> Сослагательное в требованиях — <b>subjunctive</b>!\n\n"
        "It's essential that he <b>be</b> present — "
        "<i>Важно, чтобы он присутствовал</i> (bare infinitive). "
        "They recommended that she take the exam.\n\n"
        "В AmE это чаще; в BrE часто should: "
        "…that she should take the exam.\n\n"
        "<b>Лайфхак:</b> после essential / important / recommend / suggest "
        "смотри на «голый» глагол без -s: that he go ✅"
    ),
    "fronting_c1": (
        "🦜 <b>Рико:</b> Вынос вперёд для акцента — <b>fronting</b>!\n\n"
        "This I cannot accept — <i>Вот этого я принять не могу</i>. "
        "Never have I seen such chaos — инверсия после отрицательного наречия.\n\n"
        "Используется в убедительной и литературной речи, "
        "не в каждом предложении.\n\n"
        "<b>Лайфхак:</b> fronting = «смотри сюда». "
        "После never / rarely / seldom часто инверсия: Never have I…"
    ),
    # ─── C2 ───────────────────────────────────────────────────────────
    "advanced_hedging_c2": (
        "🦜 <b>Рико:</b> Hedging уровня C2 — ювелирная точность формулировок!\n\n"
        "to a certain extent, it is not unreasonable to suggest, "
        "one might tentatively conclude, "
        "the evidence would appear to indicate…\n\n"
        "Это не «вода», а контроль силы утверждения в академическом и "
        "дипломатическом стиле.\n\n"
        "<b>Лайфхак:</b> чем сильнее claim, тем больше ответственности. "
        "C2 умеет дозировать уверенность."
    ),
    "understatement_c2": (
        "🦜 <b>Рико:</b> Британское преуменьшение — <b>understatement & irony</b>!\n\n"
        "It's not bad — часто значит «очень даже хорошо». "
        "A bit of a problem — может быть серьёзно. "
        "We may have a slight issue… — мягкая тревога.\n\n"
        "Ирония через мягкие слова: слушай контекст и тон.\n\n"
        "<b>Лайфхак:</b> не переводи буквально. "
        "Understatement — культурный код, не грамматика учебника."
    ),
    "cleft_advanced_c2": (
        "🦜 <b>Рико:</b> Расщеплённые конструкции — <b>advanced clefts</b>! "
        "Фокус на нужной части фразы.\n\n"
        "It was John who called — <i>Это Джон позвонил</i> (не кто-то другой). "
        "What I need is rest — <i>Что мне нужно — так это отдых</i>. "
        "The reason why… is… — объяснить причину с акцентом.\n\n"
        "<b>Лайфхак:</b> cleft = прожектор. "
        "Сначала выбери, что подсветить, потом собирай It was… / What… is…"
    ),
    "discourse_c2": (
        "🦜 <b>Рико:</b> Управление вниманием слушателя — "
        "<b>discourse control</b>!\n\n"
        "Signposting: firstly, that said, crucially, in practical terms, "
        "to put it another way, what this means is…\n\n"
        "Ты не просто говоришь факты — ты ведёшь человека по мысли.\n\n"
        "<b>Лайфхак:</b> в презентации каждые 30–40 секунд — "
        "маленький signpost. Люди не теряются."
    ),
    "lexical_grammar_c2": (
        "🦜 <b>Рико:</b> Грамматика через лексику — <b>lexical grammar</b>!\n\n"
        "Dependent prepositions: rely on, accuse of, capable of. "
        "Patterns: suggest that / suggest -ing; "
        "prevent someone from -ing. "
        "Chunking: on the other hand, as a matter of fact.\n\n"
        "<b>Лайфхак:</b> учи не слово, а слот: rely __ → on. "
        "Так ошибки с предлогами уходят сами."
    ),
    "persuasion_c2": (
        "🦜 <b>Рико:</b> Убеждение — <b>persuasion patterns</b>! "
        "Риторика + грамматика.\n\n"
        "Rhetorical questions: Isn't it time we acted? "
        "Triad (триада): clarity, care, courage. "
        "Concession–refutation: While X is true, Y remains more important…\n\n"
        "<b>Лайфхак:</b> сначала признай сильную сторону оппонента (while…), "
        "потом мягко разверни к своему тезису. Звучит уверенно, не агрессивно."
    ),
}
