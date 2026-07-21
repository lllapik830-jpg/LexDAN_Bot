"""
Дополнительные блоки Рико: подводки, исключения, советы — для каждой темы.
"""

TOPIC_ENRICHMENTS: dict[str, str] = {
    "alphabet": (
        "\n\n⚠️ <b>Подводки для русскоязычных:</b>\n"
        "• <b>W</b> читается как «дубль-ю», не «в»: water = /ˈwɔːtər/\n"
        "• <b>Th</b> — язык между зубами: think, this (не «с» и не «з»!)\n"
        "• <b>R</b> мягче, чем русское «р»\n"
        "• <b>H</b> часто слышна: house; но в <b>hour</b> — нет (/aʊər/)\n"
        "• <b>Y</b> иногда гласная: yes, my; иногда согласная: yellow\n\n"
        "💡 <b>Лайфхак:</b> учи буквы парами с примером слова: B — book, C — cat.\n"
        "Не спеши — алфавит = база для всего остального 🌱"
    ),
    "numbers_1_20": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• 13–19 на -teen (stress на teen): thir<b>teen</b>, four<b>teen</b>\n"
        "• 11 eleven, 12 twelve — запомни отдельно!\n"
        "• Не путай thirteen (13) и thirty (30)\n\n"
        "💡 Сначала 1–10, потом 11–12, потом -teen — так легче 🦜"
    ),
    "pronouns_be": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• После <b>he/she/it</b> только <b>is</b>, не are!\n"
        "• I'm = I am, he's = he is — апостроф = сокращение\n"
        "• В вопросе порядок меняется: <b>Are you</b> OK? (не You are OK?)\n\n"
        "💡 В заданиях жми <b>🌍 Перевести</b>, если не понимаешь слова в предложении!"
    ),
    "this_that": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• This + is → This's редко; обычно This is\n"
        "• What's = What is — частый вопрос\n"
        "• That is → That's в речи\n\n"
        "💡 This — то, что можешь потрогать; That — дальше 👐"
    ),
    "simple_phrases": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• How are you? — не «как ты», а «как дела»\n"
        "• Please — и «пожалуйста (дай)», и «пожалуйста (прошу)»\n"
        "• Sorry — извини; Excuse me — извините, можно пройти?\n\n"
        "💡 Учи фразы целиком — так быстрее заговоришь 🗣️"
    ),
    "present_simple": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• he/she/it → глагол + <b>s</b>: he work<b>s</b>, she go<b>es</b>\n"
        "• После doesn't — V1: She doesn't like (не likes!)\n"
        "• every day / usually → Present Simple, не Continuous\n\n"
        "💡 Слова always, often, never — твои подсказки ⏰"
    ),
    "articles_a_an": (
        "\n\n⚠️ <b>Исключения:</b>\n"
        "• an hour — h не слышна → an\n"
        "• a university — звук /juː/ → a\n"
        "• a one-way street — one звучит как /w/\n\n"
        "💡 Смотри на <b>звук</b>, не на букву!"
    ),
    "plurals": (
        "\n\n⚠️ <b>Исключения (основные):</b>\n"
        "• man→men, woman→women, child→children\n"
        "• foot→feet, tooth→teeth, mouse→mice\n"
        "• person→people; sheep/fish часто без -s\n"
        "• knife→knives; city→cities (-y→ies)\n"
        "• potato→potatoes, но photo→photos\n\n"
        "💡 Неправильные множественные — учи списком 📋"
    ),
    "there_is_are": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• There is + ед.; There are + мн.\n"
        "• Переводи с конца: … in the bag → There is …\n"
        "• Конкретная вещь → the; любая → a\n"
        "• There is ≠ It is!\n\n"
        "💡 There is a cat = «есть котик» 🐱"
    ),
    "can_ability": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• can + V1 (без to): I can swim ✅ / I can to swim ❌\n"
        "• can't = cannot\n"
        "• Can you…? — вежливая просьба\n\n"
        "💡 Can = умею/могу; could — вежливее или прошлое 🎵"
    ),
    "numbers_1_100": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• 21 twenty-one (через дефис), 100 a/one hundred\n"
        "• forty без u (не fourty!)\n\n"
        "💡 Сначала десятки (20,30…), потом составные 🧮"
    ),
    "numbers_time_dates": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• half past two = 2:30; quarter to five = 4:45\n"
        "• May 3rd = the third of May\n"
        "• 2000s = two thousands / twenty hundreds в речи\n\n"
        "💡 Время — at, даты — on 📅"
    ),
    "present_continuous": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• now / at the moment → Continuous\n"
        "• Стативные глаголы (know, like, want) — редко в Continuous\n"
        "• I am working vs I work every day — разница важна!\n\n"
        "💡 Continuous = процесс прямо сейчас ⏳"
    ),
    "past_simple": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• После did — V1: Did you go? (не went!)\n"
        "• yesterday, last week, ago → Past Simple\n"
        "• Неправильные глаголы — учи таблицу 📖\n\n"
        "💡 -ed: watched; но go→went, see→saw"
    ),
    "going_to_future": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• going to = план/намерение; will = спонтанное решение\n"
        "• I'm going to study (уже решил)\n\n"
        "💡 Look at those clouds! It's going to rain — видим признаки 🌧️"
    ),
    "much_many_some_any": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• many + исчисл.; much + неисчисл.\n"
        "• some в утвержд.; any в вопросах/отриц.\n"
        "• a lot of — универсально в разговоре\n\n"
        "💡 How many? / How much? — разные вопросы 🔢"
    ),
    "comparatives": (
        "\n\n⚠️ <b>Исключения:</b>\n"
        "• good→better, bad→worse, far→farther/further\n"
        "• big→bigger (удвоение согласной)\n"
        "• more + длинное прилаг.: more beautiful\n\n"
        "💡 than после сравнения: taller than me 📏"
    ),
    "modals_a2": (
        "\n\n⚠️ <b>Разница:</b>\n"
        "• must — я считаю нужным; have to — правило/обязанность\n"
        "• should — совет; must not — запрет\n\n"
        "💡 must + V1, без to ✅"
    ),
    "present_perfect": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• ever, never, already, yet, just → часто Perfect\n"
        "• yesterday → Past Simple, не Perfect\n"
        "• have been to vs have gone to — разница!\n\n"
        "💡 Результат важен сейчас → Perfect ✨"
    ),
    "past_perfect": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• had + V3 — «ещё раньше» в прошлом\n"
        "• When I arrived, the train had left\n"
        "• before, by the time, already — подсказки\n\n"
        "💡 Два прошлых — более раннее = Past Perfect ⏪"
    ),
    "past_continuous": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• длинное действие + when + короткое (Past Simple)\n"
        "• While I was cooking, he called\n\n"
        "💡 was/were + V-ing — фон в прошлом 🎬"
    ),
    "conditionals_0_1": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• Zero: If + Present, Present — факты\n"
        "• First: If + Present, will — реальное будущее\n"
        "• Не пиши will сразу после if ❌\n\n"
        "💡 Запятая, если if-часть в начале 📝"
    ),
    "gerund_infinitive": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• enjoy/avoid/mind + V-ing\n"
        "• want/hope/decide + to V\n"
        "• stop smoking vs stop to smoke — разный смысл!\n\n"
        "💡 Списки глаголов учи через практику 📚"
    ),
    "passive_basic": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• be + V3: is made, was built\n"
        "• by + кто сделал (можно опустить)\n"
        "• Active: They built it. → Passive: It was built.\n\n"
        "💡 Когда важен объект, не автор 🎯"
    ),
    "relative_clauses_b1": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• who — люди; which/that — вещи\n"
        "• Можно опустить which/that если объект: The book (that) I bought\n\n"
        "💡 Одна фраза вместо двух — звучит взрослее 🎓"
    ),
    "present_perfect_continuous": (
        "\n\n⚠️ <b>vs Present Perfect:</b>\n"
        "• I've been waiting — процесс/длительность\n"
        "• I've written 3 emails — результат\n\n"
        "💡 for/since + Perfect Continuous ⏱️"
    ),
    "conditionals_2_3": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• 2nd: If I had money, I would travel (сейчас нереально)\n"
        "• 3rd: If I had studied, I would have passed (прошлое)\n\n"
        "💡 would have + V3 в 3rd conditional 🔮"
    ),
    "reported_speech": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• said (that)… / told me (that)…\n"
        "• Времена часто сдвигаются назад\n"
        "• He said: «I am tired» → He said he was tired\n\n"
        "💡 say + слова; tell + кому 📢"
    ),
    "passives_advanced": (
        "\n\n⚠️ <b>Формы:</b>\n"
        "• is being done, has been done, will be sent\n"
        "• Часто в новостях и формальных текстах\n\n"
        "💡 Modal + be + V3: must be finished 🔒"
    ),
    "modals_deduction": (
        "\n\n⚠️ <b>Шкала уверенности:</b>\n"
        "• must be — почти уверен\n"
        "• might/may/could — возможно\n"
        "• can't be — невозможно\n"
        "• must have + V3 — про прошлое\n\n"
        "💡 Deduction ≠ obligation! 🕵️"
    ),
    "relative_advanced": (
        "\n\n⚠️ <b>Подводки:</b>\n"
        "• whose — чей; where/when — место/время\n"
        "• Non-defining: запятые! My brother, who lives in London, …\n\n"
        "💡 Defining — без запятых, важно для смысла 📌"
    ),
    "inversion": (
        "\n\n⚠️ <b>Когда:</b>\n"
        "• Never have I…, Rarely does he…\n"
        "• Not only… but also…\n"
        "• Формальный/письменный стиль\n\n"
        "💡 Для эссе и сильной речи ✍️"
    ),
    "cleft_sentences": (
        "\n\n⚠️ <b>Примеры:</b>\n"
        "• It was John who called\n"
        "• What I need is a break\n\n"
        "💡 Выделяешь главное — как прожектор 🔦"
    ),
    "advanced_modals": (
        "\n\n⚠️ <b>Оттенки:</b>\n"
        "• should have — надо было (а не сделал)\n"
        "• needn't have — зря сделал\n"
        "• might have been — возможно было\n\n"
        "💡 Сожаление и критика через модальные 💭"
    ),
    "participle_clauses": (
        "\n\n⚠️ <b>Опасность:</b>\n"
        "• Подлежащее должно совпадать!\n"
        "• Walking down the street, I saw… ✅\n"
        "• Walking…, the street looked… ❌\n\n"
        "💡 Сжимаем два предложения в одно 🎯"
    ),
    "nominalisation": (
        "\n\n⚠️ <b>Примеры:</b>\n"
        "• decide → decision, develop → development\n"
        "• Академический стиль, формальные тексты\n\n"
        "💡 Не перегибай в разговоре — звучит тяжело 📄"
    ),
    "discourse_markers": (
        "\n\n⚠️ <b>Уместность:</b>\n"
        "• however, nevertheless, furthermore\n"
        "• Не в каждом предложении — только где нужна связка\n\n"
        "💡 Структура эссе: firstly, moreover, in conclusion 📝"
    ),
    "stylistic_inversion": (
        "\n\n⚠️ <b>Эффект:</b>\n"
        "• Инверсия = акцент и стиль, не «для галочки»\n"
        "• Little did he know…\n\n"
        "💡 C2 = выбор формы по эффекту 🎭"
    ),
    "subtle_modality": (
        "\n\n⚠️ <b>Нюансы:</b>\n"
        "• may have vs might have — сила догадки\n"
        "• It would seem… — хеджирование\n\n"
        "💡 Мягче мнение = вежливее в дискуссии 🤝"
    ),
    "mixed_conditionals": (
        "\n\n⚠️ <b>Пример:</b>\n"
        "• If I had taken the job, I would be in London now\n"
        "• Прошлое условие → настоящий результат\n\n"
        "💡 Смешиваем времена осознанно 🔀"
    ),
    "ellipsis_substitution": (
        "\n\n⚠️ <b>Примеры:</b>\n"
        "• So do I / Neither have I\n"
        "• I think so / I hope not\n\n"
        "💡 Носители экономят слова — учись у них 🗣️"
    ),
    "register_control": (
        "\n\n⚠️ <b>Register:</b>\n"
        "• Get vs obtain, ask vs inquire\n"
        "• Formal email ≠ чат с другом\n\n"
        "💡 Один смысл — разные «костюмы» 👔"
    ),
    "pragmatic_softening": (
        "\n\n⚠️ <b>Фразы:</b>\n"
        "• I was wondering if… / Would you mind…\n"
        "• Could you possibly… — очень вежливо\n\n"
        "💡 Смягчение = меньше конфликтов 🕊️"
    ),
}

ACK_FOOTER = (
    "\n\n💬 <b>Есть вопросы?</b> Пиши текстом — объясню ещё проще!\n"
    "✅ Когда всё понятно — жми <b>Ознакомился</b>, тема засчитается 🎉"
)

PRACTICE_FOOTER = (
    "\n\n💬 <b>Есть вопросы?</b> Пиши текстом — разберём на твоих примерах!\n"
    "📝 Потом жми <b>Задания</b>. Там есть <b>🌍 Перевести</b>, если фраза непонятна.\n"
    "🦜 Помощь: 1-я подсказка — намёк, 2-я — ответ (зачёт)."
)

GRAMMAR_SECTION_INTRO: dict[str, str] = {
    "A0": (
        "🦜 <b>Рико:</b> Ну что, заходим в грамматику A0! 🌱\n"
        "Я расскажу каждую тему как историю — с переводом, примерами и ловушками. "
        "Не зубри — понимай, и будет легко ✨\n\n"
        "💬 В <b>Общении с Рико</b> можно спросить про любую тему и поболтать — "
        "он всё объяснит."
    ),
    "A1": (
        "🦜 <b>Рико:</b> Грамматика A1 — строим фундамент! "
        "Каждая тема — связный рассказ, не сухие правила. Спрашивай что угодно 💪\n\n"
        "💬 В <b>Общении с Рико</b> можно спросить про любую тему и поболтать — "
        "он всё объяснит."
    ),
    "A2": (
        "🦜 <b>Рико:</b> A2 — уже интереснее! Времена, сравнения, типичные ошибки — "
        "всё объясню по-человечески, с душой 🔥\n\n"
        "💬 В <b>Общении с Рико</b> можно спросить про любую тему и поболтать — "
        "он всё объяснит."
    ),
    "B1": (
        "🦜 <b>Рико:</b> B1 — время говорить точнее! Perfect, условные, пассив — "
        "разберём на живых примерах с переводом 🎯\n\n"
        "💬 В <b>Общении с Рико</b> можно спросить про любую тему и поболтать — "
        "он всё объяснит."
    ),
    "B2": (
        "🦜 <b>Рико:</b> B2 — серьёзные темы, но я объясню просто и увлекательно. "
        "Нюансы и подводки — всё здесь 😎\n\n"
        "💬 В <b>Общении с Рико</b> можно спросить про любую тему и поболтать — "
        "он всё объяснит."
    ),
    "C1": (
        "🦜 <b>Рико:</b> C1 — полируем стиль! Инверсия, cleft, номинализация — "
        "как рассказ, не как справочник 👑\n\n"
        "💬 В <b>Общении с Рико</b> можно спросить про любую тему и поболтать — "
        "он всё объяснит."
    ),
    "C2": (
        "🦜 <b>Рико:</b> C2 — вершина! Тонкости носителя — "
        "расскажу так, чтобы было интересно и понятно 🏔️✨\n\n"
        "💬 В <b>Общении с Рико</b> можно спросить про любую тему и поболтать — "
        "он всё объяснит."
    ),
}


def get_enrichment(topic_id: str, mode: str) -> str:
    parts = [TOPIC_ENRICHMENTS.get(topic_id, "")]
    if mode == "ack":
        parts.append(ACK_FOOTER)
    else:
        parts.append(PRACTICE_FOOTER)
    return "".join(p for p in parts if p)
