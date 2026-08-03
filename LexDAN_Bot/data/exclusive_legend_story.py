"""
Легенда LexDan — сказочная история 1 места.
20 заданий внутри сюжета: зайчик(1) → карта(5) → путь к замку(9) → дракон(5).
"""

from __future__ import annotations

# Голоса (ElevenLabs voice library)
VOICE_NARRATOR = "ktrGUw7rURIQyMrQZqCu"  # выбранный голос рассказчика
VOICE_RICO = None  # → RICO_VOICE_ID в рантайме
VOICE_BUNNY = "nDJIICjR9zfJExIFeSCN"  # Emmaline · British
VOICE_FOX = "dHd5gvgSOzSfduK4CvEg"  # Ed · American
VOICE_OWL = "NfUrCNRReUL9RXS9upG1"  # Scotty · British
VOICE_SQUIRREL = "b8gbDO0ybjX1VA89pBdX"  # Ruby · Australian
VOICE_HEDGEHOG = "YLbQE9U7P1K6rBNJWNSv"  # Jimbo · Australian
VOICE_DRAGON = "ktrGUw7rURIQyMrQZqCu"  # тот же голос, что у рассказчика (по запросу)
VOICE_BUTTERFLY = "TC0Zp7WVFzhA8zpTlRqV"  # Aria · American (мягкий)

READY_HTML = (
    "📖 <b>Легенда LexDan</b>\n\n"
    "Сейчас начнётся увлекательная история о том, как Рико стал преподавателем "
    "и одарил знаниями весь мир.\n\n"
    "Готов?"
)

BTN_READY = "✨ Я готов!"
BTN_STORY_NEXT = "➡️ Далее"
BTN_STORY_TRANSLATE = "🌍 Перевести"
BTN_STORY_HINT = "💡 Подсказка"
BTN_STORY_SKIP = "⏭ Пропустить"
BTN_STORY_EXIT = "🚪 Выйти из эксклюзива"

TITLE = "🏆 Легенда LexDan"
TOTAL_TASKS = 20


def _line(
    speaker: str,
    en: str,
    ru: str,
    *,
    voice: str | None = "narrator",
    label: str | None = None,
) -> dict:
    return {
        "type": "line",
        "speaker": speaker,  # narrator | rico | bunny | fox | owl | squirrel | hedgehog | dragon | butterfly
        "label": label,
        "en": en,
        "ru": ru,
        "voice": voice,
    }


def _task(task: dict, *, chapter: str, chapter_title: str) -> dict:
    t = dict(task)
    t["type"] = "task"
    t["chapter"] = chapter
    t["chapter_title"] = chapter_title
    return t


# ─── 20 заданий ─────────────────────────────────────────────────────────────

T1 = {
    "id": "leg_t01",
    "kind": "scramble",
    "title_ru": "Верёвка терпения",
    "prompt_html": (
        "🐰 Зайчик держится за камень из последних сил.\n"
        "Рико чувствует: сила английского отвечает на верные слова.\n\n"
        "🧩 Собери предложение из слов ниже (про терпение и учёбу).\n"
        "В правильной фразе должно появиться слово <b>rope</b> — "
        "тогда Рико наколдует верёвку!"
    ),
    "words": [
        "patience",
        "is",
        "the",
        "rope",
        "that",
        "lifts",
        "every",
        "English",
        "learner",
    ],
    "answer": "Patience is the rope that lifts every English learner.",
    "accept": [
        "Patience is the rope that lifts every English learner",
        "patience is the rope that lifts every english learner",
    ],
    "hint_ru": "Начни с Patience… и не забудь rope посередине.",
}

T2 = {
    "id": "leg_t02",
    "kind": "fix",
    "title_ru": "Крик лисы",
    "prompt_html": (
        "🦊 Лиса дрожит:\n"
        "<i>The dragon have stole all our English yesterday!</i>\n\n"
        "✍️ Исправь фразу грамматически (одна правильная)."
    ),
    "answer": "The dragon stole all our English yesterday.",
    "accept": [
        "The dragon has stolen all our English yesterday.",
        "The dragon stole all our English yesterday",
        "Yesterday the dragon stole all our English.",
    ],
    "hint_ru": "Past Simple: steal → stole (или Present Perfect: has stolen).",
}

T3 = {
    "id": "leg_t03",
    "kind": "mcq",
    "title_ru": "Что украл дракон?",
    "prompt_html": "🦉 Сова шепчет загадку. Что исчезло из деревни?",
    "options": [
        "All the honey from the bees",
        "Every English word from the village",
        "Rico's favourite crackers",
        "The moon itself",
    ],
    "answer": "Every English word from the village",
    "hint_ru": "Смысл беды — язык, не еда.",
}

T4 = {
    "id": "leg_t04",
    "kind": "write",
    "title_ru": "Просьба к белке",
    "prompt_html": (
        "🐿️ Белка прячется на дубе. Попроси её о помощи по-английски "
        "(2–3 предложения). Упомяни <b>map</b> или <b>dragon</b>."
    ),
    "check": "must_include",
    "must_include": ["map", "dragon"],
    "min_words": 8,
    "hint_ru": "Please help me find a map / the dragon…",
}

T5 = {
    "id": "leg_t05",
    "kind": "scramble",
    "title_ru": "Шёпот ветра",
    "prompt_html": "Ветер приносит обрывок заклинания. Собери предложение из слов ниже:",
    "words": ["clues", "hide", "where", "brave", "hearts", "look"],
    "answer": "Clues hide where brave hearts look.",
    "accept": ["Clues hide where brave hearts look"],
    "hint_ru": "Clues hide where…",
}

T6 = {
    "id": "leg_t06",
    "kind": "write",
    "title_ru": "Фрагмент карты",
    "prompt_html": (
        "На коре дерева выжжено:\n"
        "<i>Follow the river until the stones sing.</i>\n\n"
        "✍️ Перефразируй своими словами (английский), сохрани смысл."
    ),
    "check": "paraphrase",
    "source": "Follow the river until the stones sing.",
    "min_words": 5,
    "hint_ru": "Go along the river… until you hear the singing stones.",
}

T7 = {
    "id": "leg_t07",
    "kind": "mcq",
    "title_ru": "Тропа на развилке",
    "prompt_html": "На камне три стрелки. Какая ведёт к замку дракона?",
    "options": [
        "The path of silence and shadows",
        "The candy road to nowhere",
        "The shortcut through soap bubbles",
        "The elevator to the clouds",
    ],
    "answer": "The path of silence and shadows",
    "hint_ru": "Карта шепчет про тишину и тени.",
}

T8 = {
    "id": "leg_t08",
    "kind": "fix",
    "title_ru": "Табличка у болота",
    "prompt_html": (
        "Табличка:\n"
        "<i>If you will enter here, you must spoke true words.</i>\n\n"
        "✍️ Исправь."
    ),
    "answer": "If you enter here, you must speak true words.",
    "accept": [
        "If you enter here, you must speak true words",
        "If you enter here you must speak true words.",
    ],
    "hint_ru": "1-я условная: If + Present → will/must + V1.",
}

T9 = {
    "id": "leg_t09",
    "kind": "voice",
    "title_ru": "Заклинание тумана",
    "prompt_html": (
        "Туман закрывает тропу. Произнеси <b>голосом</b> или напиши текстом:\n"
        "<b>Clear the mist with English.</b>"
    ),
    "voice_text": "Clear the mist with English.",
    "accept": [
        "Clear the mist with English",
        "Clear the mist with honest English",
        "clear mist with English",
    ],
    "hint_ru": "Clear the mist with English — можно чуть короче, смысл тот же.",
}

T10 = {
    "id": "leg_t10",
    "kind": "write",
    "title_ru": "Диалог с ежом-стражем",
    "prompt_html": (
        "🦔 Ёж: <i>Why should I let a parrot pass?</i>\n\n"
        "✍️ Ответь 2–3 предложениями по-английски: ты идёшь спасать язык деревни."
    ),
    "check": "must_include",
    "must_include": ["english", "help"],
    "require_all": True,
    "min_words": 10,
    "hint_ru": "I'm going to help … save English / the village from the dragon…",
}

T11 = {
    "id": "leg_t11",
    "kind": "scramble",
    "title_ru": "Мост из слов",
    "prompt_html": "Мост строится из фразы. Собери предложение из слов ниже:",
    "words": ["courage", "builds", "bridges", "where", "fear", "digs", "holes"],
    "answer": "Courage builds bridges where fear digs holes.",
    "accept": ["Courage builds bridges where fear digs holes"],
    "hint_ru": "Courage builds bridges…",
}

T12 = {
    "id": "leg_t12",
    "kind": "mcq",
    "title_ru": "Голодный ворон",
    "prompt_html": "Ворон каркает загадку: что сильнее огня дракона?",
    "options": [
        "A bigger fire",
        "A kind and clear sentence",
        "Three bananas",
        "Louder shouting",
    ],
    "answer": "A kind and clear sentence",
    "hint_ru": "В этой сказке побеждает ясное слово.",
}

T13 = {
    "id": "leg_t13",
    "kind": "fix",
    "title_ru": "Письмо на скале",
    "prompt_html": (
        "<i>Rico don't never give up, even when the night feel endless.</i>\n\n"
        "✍️ Исправь."
    ),
    "answer": "Rico doesn't ever give up, even when the night feels endless.",
    "accept": [
        "Rico never gives up, even when the night feels endless.",
        "Rico doesn't give up, even when the night feels endless.",
        "Rico does not ever give up, even when the night feels endless.",
    ],
    "hint_ru": "Убери двойное отрицание; night → feels.",
}

T14 = {
    "id": "leg_t14",
    "kind": "write",
    "title_ru": "Открытка сове",
    "prompt_html": (
        "🦉 Сова просит короткое обещание путешественника.\n"
        "✍️ Одно предложение с <b>I will</b> про путь к замку."
    ),
    "check": "must_include",
    "must_include": ["i will"],
    "min_words": 6,
    "hint_ru": "I will follow the map to the dragon's castle…",
}

T15 = {
    "id": "leg_t15",
    "kind": "voice",
    "title_ru": "Пароль у ворот",
    "prompt_html": (
        "Ворота гремят. Пароль:\n"
        "<b>Words are my wings.</b>\n"
        "🎙 Скажи или напиши."
    ),
    "voice_text": "Words are my wings.",
    "hint_ru": "Точная фраза: Words are my wings.",
}

T16 = {
    "id": "leg_t16",
    "kind": "scramble",
    "title_ru": "Меч из букв",
    "prompt_html": (
        "В зале дракона вспыхивает свет — рождается <b>Sword of Sentences</b>.\n"
        "Собери заклинание меча из слов ниже:"
    ),
    "words": ["the", "sword", "of", "words", "cuts", "through", "fear"],
    "answer": "The sword of words cuts through fear.",
    "accept": ["The sword of words cuts through fear"],
    "hint_ru": "The sword of words…",
}

T17 = {
    "id": "leg_t17",
    "kind": "fix",
    "title_ru": "Насмешка дракона",
    "prompt_html": (
        "🐉 Дракон рычит:\n"
        "<i>You is too small for fight I!</i>\n\n"
        "✍️ Исправь его английский — и ударь правдой."
    ),
    "answer": "You are too small to fight me!",
    "accept": [
        "You are too small to fight me.",
        "You are too small to fight me!",
        "You're too small to fight me!",
    ],
    "hint_ru": "You are… too small to fight me.",
}

T18 = {
    "id": "leg_t18",
    "kind": "voice",
    "title_ru": "Боевой клич",
    "prompt_html": (
        "Меч в лапах Рико звенит. Крикни:\n"
        "<b>For every silent village — I speak!</b>"
    ),
    "voice_text": "For every silent village — I speak!",
    "hint_ru": "Можно без тире: For every silent village I speak!",
}

T19 = {
    "id": "leg_t19",
    "kind": "write",
    "title_ru": "Удар мечом",
    "prompt_html": (
        "✍️ Напиши 2–3 предложения: как Рико побеждает дракона "
        "<b>sword</b>-ом из слов. Обязательно слово <b>sword</b>."
    ),
    "check": "must_include",
    "must_include": ["sword"],
    "min_words": 12,
    "hint_ru": "Rico raises the sword of words and…",
}

T20 = {
    "id": "leg_t20",
    "kind": "mcq",
    "title_ru": "Последнее слово",
    "prompt_html": "Дракон падает. Что Рико возвращает королевству?",
    "options": [
        "A chest of gold coins",
        "The English language and the joy of speaking",
        "Three extra winters",
        "A bigger dragon",
    ],
    "answer": "The English language and the joy of speaking",
    "hint_ru": "Он пришёл вернуть язык.",
}


# ─── Сцены сказки ───────────────────────────────────────────────────────────

LEGEND_SCENES: list[dict] = [
    # Пролог
    _line(
        "narrator",
        "Once upon a time, in a green kingdom of talking animals, "
        "there lived a clever parrot named Rico. He was experienced, cheerful, "
        "and loved sunny mornings more than golden coins.",
        "Жил-был в зелёном королевстве говорящих зверей умный попугай по имени Рико. "
        "Он был опытный, весёлый и любил солнечные утра больше золотых монет.",
    ),
    _line(
        "narrator",
        "Rico spent his days singing soft songs, sharing jokes with foxes, "
        "and teaching little birds how to greet the wind. Life felt bright and simple.",
        "Дни Рико проходили в мягких песнях, шутках с лисами и уроках для птенцов — "
        "как здороваться с ветром. Жизнь казалась светлой и простой.",
    ),
    _line(
        "rico",
        "What a wonderful day! The forest hums, my friends laugh, "
        "and my heart is as light as a feather.",
        "Какой чудесный день! Лес гудит, друзья смеются, "
        "а сердце лёгкое, как перо.",
        voice="rico",
        label="🦜 Рико",
    ),
    _line(
        "narrator",
        "And everything could have stayed the same forever… "
        "until Rico met a magical butterfly with wings like stained glass.",
        "И всё могло бы оставаться как всегда… "
        "пока Рико не встретил волшебную бабочку с крыльями, как витражное стекло.",
    ),
    _line(
        "rico",
        "Oh my! What is this? I have never seen such a glowing creature before!",
        "Ух ты! Что это такое? Я впервые вижу такое сияющее существо!",
        voice="rico",
        label="🦜 Рико",
    ),
    _line(
        "butterfly",
        "Do not be afraid, bright bird. Wonder is knocking.",
        "Не бойся, яркая птица. Чудо стучится.",
        voice="butterfly",
        label="🦋 Бабочка",
    ),
    _line(
        "narrator",
        "The butterfly landed gently on Rico's beak. Suddenly the world flashed, "
        "blinked, and filled with sparkling light. English poured into Rico's mind "
        "like a river of silver words.",
        "Бабочка села Рико на клюв. Вдруг мир вспыхнул, моргнул и наполнился блеском. "
        "Английский влился в разум Рико серебряной рекой слов.",
    ),
    _line(
        "rico",
        "I can speak English perfectly! Listen — patience, courage, curiosity… "
        "the whole language lives in me now!",
        "Я говорю по-английски в совершенстве! Слушайте — patience, courage, curiosity… "
        "весь язык теперь живёт во мне!",
        voice="rico",
        label="🦜 Рико",
    ),
    _line(
        "narrator",
        "Rico danced with joy — and then he heard cries for help beyond the river.",
        "Рико затанцевал от радости — и тут услышал крики о помощи за рекой.",
    ),
    _line(
        "narrator",
        "A little bunny had fallen from the bridge. He clung to a wet stone "
        "while the current tried to pull him away. His strength was almost gone.",
        "Маленький зайчик упал с моста. Он цеплялся за мокрый камень, "
        "а течение сносило его. Силы были на исходе.",
    ),
    _line(
        "bunny",
        "Help… please… I cannot hold on much longer!",
        "Помогите… пожалуйста… я почти не держусь!",
        voice="bunny",
        label="🐰 Зайчик",
    ),
    _line(
        "narrator",
        "Rico felt the new power rising. To conjure a rescue rope, "
        "he needed the true English sentence about patience and learning.",
        "Рико почувствовал, как поднимается новая сила. Чтобы наколдовать верёвку спасения, "
        "нужно верное английское предложение про терпение и учёбу.",
    ),
    _task(T1, chapter="bunny", chapter_title="🌊 Спасение зайчика · 1/20"),
    _line(
        "narrator",
        "The moment the sentence was complete, a strong rope of light appeared. "
        "Rico cast it to the bunny and pulled him safely to the shore.",
        "Как только фраза сложилась, явилась крепкая светящаяся верёвка — rope. "
        "Рико забросил её зайчику и вытащил его на берег.",
    ),
    _line(
        "bunny",
        "Thank you, Rico! Your words saved my life. I will never forget this kindness.",
        "Спасибо, Рико! Твои слова спасли мне жизнь. Я никогда не забуду эту доброту.",
        voice="bunny",
        label="🐰 Зайчик",
    ),
    _line(
        "rico",
        "Stay safe, little friend. English can be a rope when hope feels thin.",
        "Береги себя, малыш. Английский может стать верёвкой, когда надежда тонка.",
        voice="rico",
        label="🦜 Рико",
    ),
    # Возвращение — дракон украл английский
    _line(
        "narrator",
        "Rico returned to the animal kingdom — but the streets were strangely quiet. "
        "Signs were blank. Songs had no words. Something precious was missing.",
        "Рико вернулся в королевство зверей — но улицы были странно тихими. "
        "Вывески пусты. В песнях не было слов. Чего-то драгоценного не хватало.",
    ),
    _line(
        "rico",
        "Hello? Is anyone here? Why is everyone whispering?",
        "Эй? Есть кто-нибудь? Почему все шепчут?",
        voice="rico",
        label="🦜 Рико",
    ),
    _line(
        "narrator",
        "From behind a broken market stall, a red fox stepped out, trembling, "
        "and ran straight to Rico.",
        "Из-за сломанного прилавка вышла рыжая лиса — дрожала "
        "и сразу побежала к Рико.",
    ),
    _line(
        "fox",
        "Rico! While you were away, a dragon came. He stole every English word "
        "from our village! We cannot learn, cannot greet, cannot dream aloud!",
        "Рико! Пока тебя не было, пришёл дракон. Он украл все английские слова "
        "из нашей деревни! Мы не можем учиться, здороваться, мечтать вслух!",
        voice="fox",
        label="🦊 Лиса",
    ),
    _line(
        "rico",
        "Then I will bring English home. Tell me everything — we start now.",
        "Тогда я верну английский домой. Расскажите всё — начинаем сейчас.",
        voice="rico",
        label="🦜 Рико",
    ),
    _line(
        "fox",
        "First, fix my cry — fear twisted my English. Then we can ask the owl.",
        "Сначала почини мой крик — страх скрутил мой английский. Потом спросим сову.",
        voice="fox",
        label="🦊 Лиса",
    ),
    _task(T2, chapter="map_hunt", chapter_title="🗺 Путь к карте · 2/20"),
    _line(
        "fox",
        "Thank you. Come — the old owl lives in the tall pine. She sees what others miss.",
        "Спасибо. Идём — старая сова живёт на высокой сосне. Она видит то, что другие пропускают.",
        voice="fox",
        label="🦊 Лиса",
    ),
    _line(
        "narrator",
        "They walked to the pine. Soft wings opened above them, and a grey owl "
        "landed on a branch like a quiet judge.",
        "Они дошли до сосны. Мягкие крылья раскрылись сверху, и серая сова "
        "села на ветку, словно тихий судья.",
    ),
    _line(
        "owl",
        "I heard the fox. Wise bird, listen well. The dragon hides behind riddles. Answer me.",
        "Я слышала лису. Мудрая птица, слушай внимательно. Дракон прячется за загадками. Ответь мне.",
        voice="owl",
        label="🦉 Сова",
    ),
    _task(T3, chapter="map_hunt", chapter_title="🗺 Путь к карте · 3/20"),
    _line(
        "owl",
        "Correct. Now seek the squirrel in the oak market — she stole a scrap of the map "
        "to keep it safe from the dragon.",
        "Верно. Теперь ищи белку на дубовом рынке — она спрятала клочок карты, "
        "чтобы дракон его не забрал.",
        voice="owl",
        label="🦉 Сова",
    ),
    _line(
        "rico",
        "Thank you, Owl. Fox, will you wait here while I climb?",
        "Спасибо, Сова. Лиса, подождёшь здесь, пока я залезу?",
        voice="rico",
        label="🦜 Рико",
    ),
    _line(
        "fox",
        "I will wait. Be gentle — she is brave, but very shy.",
        "Подожду. Будь мягче — она храбрая, но очень стеснительная.",
        voice="fox",
        label="🦊 Лиса",
    ),
    _line(
        "narrator",
        "High in an oak, a nervous squirrel held a scrap of parchment. "
        "She peeked down and almost dropped it.",
        "Высоко на дубе нервная белка держала клочок пергамента. "
        "Она выглянула вниз и чуть не уронила его.",
    ),
    _line(
        "squirrel",
        "W-who are you? If you want the paper, ask politely. Dragons shout. Heroes ask.",
        "К-кто ты? Если хочешь бумажку — проси вежливо. Драконы орют. Герои просят.",
        voice="squirrel",
        label="🐿️ Белка",
    ),
    _task(T4, chapter="map_hunt", chapter_title="🗺 Путь к карте · 4/20"),
    _line(
        "squirrel",
        "Okay, okay! Take this clue. The rest of the map waits by the singing stones.",
        "Ладно-ладно! Держи подсказку. Остальная карта ждёт у поющих камней.",
        voice="squirrel",
        label="🐿️ Белка",
    ),
    _line(
        "rico",
        "You are braver than you think. We will bring English back — for you too.",
        "Ты храбрее, чем думаешь. Мы вернём английский — и для тебя тоже.",
        voice="rico",
        label="🦜 Рико",
    ),
    _line(
        "narrator",
        "Rico flew down to the fox. Together they followed the river toward the singing stones, "
        "where the wind itself seemed to spell.",
        "Рико спустился к лисе. Вместе они пошли вдоль реки к поющим камням, "
        "где сам ветер будто складывал буквы.",
    ),
    _line(
        "fox",
        "Listen — the wind is trying to speak. Catch the words before they blow away!",
        "Слушай — ветер хочет говорить. Поймай слова, пока их не унесло!",
        voice="fox",
        label="🦊 Лиса",
    ),
    _task(T5, chapter="map_hunt", chapter_title="🗺 Путь к карте · 5/20"),
    _line(
        "owl",
        "Well done. One more step: read the bark writing and say it in your own words.",
        "Отлично. Ещё шаг: прочти надпись на коре и скажи своими словами.",
        voice="owl",
        label="🦉 Сова",
    ),
    _task(T6, chapter="map_hunt", chapter_title="🗺 Путь к карте · 6/20"),
    _line(
        "narrator",
        "At the singing stones the pieces joined. A full map glowed in Rico's wings: "
        "the path to the Dragon's Castle through silence and shadow.",
        "У поющих камней куски сошлись. Полная карта засветилась в крыльях Рико: "
        "путь к Замку Дракона через тишину и тень.",
    ),
    _line(
        "squirrel",
        "You did it! Go carefully. We will cheer from the trees!",
        "У вас получилось! Идите осторожно. Мы будем болеть с деревьев!",
        voice="squirrel",
        label="🐿️ Белка",
    ),
    _line(
        "fox",
        "Bring our words home, Rico. We believe in you.",
        "Верни наши слова домой, Рико. Мы в тебя верим.",
        voice="fox",
        label="🦊 Лиса",
    ),
    _line(
        "rico",
        "I see the road. Courage first, fear later. Let's go!",
        "Я вижу дорогу. Сначала смелость, страх — потом. Вперёд!",
        voice="rico",
        label="🦜 Рико",
    ),
    # Путь к замку — 9 заданий
    _line(
        "narrator",
        "The map pointed to a fork of three paths. An old stone whispered choices into the dusk.",
        "Карта указывала на развилку из трёх троп. Старый камень шептал выборы в сумерки.",
    ),
    _task(T7, chapter="road", chapter_title="🛤 Дорога к замку · 7/20"),
    _line(
        "narrator",
        "The chosen path smelled of moss and old secrets. A crooked sign leaned over a swamp.",
        "Выбранная тропа пахла мхом и старыми тайнами. Кривая табличка нависала над болотом.",
    ),
    _task(T8, chapter="road", chapter_title="🛤 Дорога к замку · 8/20"),
    _line(
        "narrator",
        "Fog rose like a wall. Only a spoken charm could open a way.",
        "Туман встал стеной. Лишь произнесённое заклинание откроет путь.",
    ),
    _line(
        "rico",
        "I will speak the charm clear and strong. Join me if you can!",
        "Я скажу заклинание ясно и сильно. Присоединяйся, если можешь!",
        voice="rico",
        label="🦜 Рико",
    ),
    _task(T9, chapter="road", chapter_title="🛤 Дорога к замку · 9/20"),
    _line(
        "narrator",
        "The mist opened onto a rocky ridge. Spikes of quills glittered — "
        "a hedgehog guard blocked the only bridge.",
        "Туман раскрылся на каменистый хребет. Блестели иглы — "
        "ёж-страж перекрыл единственный мост.",
    ),
    _line(
        "hedgehog",
        "Halt! I guard this ridge. Speak your purpose, parrot.",
        "Стой! Я стерегу этот хребет. Назови цель, попугай.",
        voice="hedgehog",
        label="🦔 Ёж",
    ),
    _task(T10, chapter="road", chapter_title="🛤 Дорога к замку · 10/20"),
    _line(
        "hedgehog",
        "Brave answer. Cross my bridge of words — if you can build it.",
        "Смелый ответ. Перейди мой мост из слов — если сумеешь его собрать.",
        voice="hedgehog",
        label="🦔 Ёж",
    ),
    _task(T11, chapter="road", chapter_title="🛤 Дорога к замку · 11/20"),
    _line(
        "hedgehog",
        "The bridge holds. Pass, teacher-bird. A raven ahead loves riddles more than worms.",
        "Мост держит. Проходи, птица-учитель. Впереди ворон любит загадки больше червей.",
        voice="hedgehog",
        label="🦔 Ёж",
    ),
    _line(
        "narrator",
        "A raven circled above, black as ink, and tossed a riddle into the wind.",
        "Над головой кружил ворон, чёрный как чернила, и бросил загадку в ветер.",
    ),
    _task(T12, chapter="road", chapter_title="🛤 Дорога к замку · 12/20"),
    _line(
        "narrator",
        "Beyond the raven, on a cliff wall, someone had scratched a tired sentence. It needed healing.",
        "За вороном на скале кто-то выцарапал усталую фразу. Ей нужно было исцеление.",
    ),
    _task(T13, chapter="road", chapter_title="🛤 Дорога к замку · 13/20"),
    _line(
        "narrator",
        "Soft wings returned — the owl had followed from afar, proud and quiet.",
        "Снова мягкие крылья — сова шла следом издалека, гордая и тихая.",
    ),
    _line(
        "owl",
        "Traveller, seal your promise before the castle gates appear.",
        "Путник, скрепи обещание, пока не показались ворота замка.",
        voice="owl",
        label="🦉 Сова",
    ),
    _task(T14, chapter="road", chapter_title="🛤 Дорога к замку · 14/20"),
    _line(
        "narrator",
        "At last the dark towers rose. Iron gates waited for a password of wings.",
        "Наконец поднялись тёмные башни. Железные ворота ждали пароль крыльев.",
    ),
    _task(T15, chapter="road", chapter_title="🛤 Дорога к замку · 15/20"),
    # Битва с драконом — 5 заданий
    _line(
        "narrator",
        "Inside the hall, fire painted the walls. Scales scraped stone. The dragon woke.",
        "В зале огонь рисовал стены. Чешуя скребла камень. Дракон проснулся.",
    ),
    _line(
        "dragon",
        "Who dares enter my hall? Your village words belong to ME now!",
        "Кто смеет входить в мой зал? Слова вашей деревни теперь МОИ!",
        voice="dragon",
        label="🐉 Дракон",
    ),
    _line(
        "rico",
        "I dare. I came to take English home — and I am not alone. Words walk with me.",
        "Я смею. Я пришёл вернуть английский домой — и я не один. Со мной идут слова.",
        voice="rico",
        label="🦜 Рико",
    ),
    _line(
        "narrator",
        "From sparks of grammar and sparks of heart, a shining sword appeared in Rico's wings: "
        "the Sword of Sentences.",
        "Из искр грамматики и искр сердца в крыльях Рико явился сияющий меч — "
        "Меч Предложений.",
    ),
    _task(T16, chapter="dragon", chapter_title="⚔️ Замок дракона · 16/20"),
    _line(
        "dragon",
        "Ha! Your grammar cannot hurt me!",
        "Ха! Твоя грамматика меня не ранит!",
        voice="dragon",
        label="🐉 Дракон",
    ),
    _line(
        "narrator",
        "But the dragon's own broken English gave Rico an opening — fix the taunt, break the spell.",
        "Но собственный ломаный английский дракона дал Рико шанс — исправь насмешку, сломай чары.",
    ),
    _task(T17, chapter="dragon", chapter_title="⚔️ Замок дракона · 17/20"),
    _line(
        "narrator",
        "The dragon staggered. Rico lifted the sword high and called the village in his voice.",
        "Дракон пошатнулся. Рико поднял меч высоко и позвал деревню своим голосом.",
    ),
    _task(T18, chapter="dragon", chapter_title="⚔️ Замок дракона · 18/20"),
    _task(T19, chapter="dragon", chapter_title="⚔️ Замок дракона · 19/20"),
    _line(
        "dragon",
        "Enough… take the words… they burn my claws…",
        "Довольно… забирай слова… они жгут мне когти…",
        voice="dragon",
        label="🐉 Дракон",
    ),
    _task(T20, chapter="dragon", chapter_title="⚔️ Замок дракона · 20/20"),
    # Эпилог
    _line(
        "narrator",
        "Rico flew home with a storm of glowing words behind him. "
        "English returned to every sign, every song, every smile.",
        "Рико полетел домой, а за ним — буря светящихся слов. "
        "Английский вернулся на каждую вывеску, в каждую песню, в каждую улыбку.",
    ),
    _line(
        "fox",
        "Teacher Rico! You gave our voices back. Will you teach us every day?",
        "Учитель Рико! Ты вернул нам голоса. Будешь учить нас каждый день?",
        voice="fox",
        label="🦊 Лиса",
    ),
    _line(
        "owl",
        "And I will help with the hard questions.",
        "А я помогу со сложными вопросами.",
        voice="owl",
        label="🦉 Сова",
    ),
    _line(
        "squirrel",
        "And I will bring nuts for every good answer!",
        "А я буду носить орехи за каждый хороший ответ!",
        voice="squirrel",
        label="🐿️ Белка",
    ),
    _line(
        "rico",
        "Yes. From this day I am your teacher. English is a gift — and gifts grow when shared.",
        "Да. С этого дня я ваш учитель. Английский — дар, а дары растут, когда ими делятся.",
        voice="rico",
        label="🦜 Рико",
    ),
    _line(
        "narrator",
        "And so Rico became the teacher who gifted knowledge to the whole wide world. "
        "The End — and a new beginning.",
        "Так Рико стал преподавателем, который одарил знаниями весь широкий мир. "
        "Конец — и новое начало.",
    ),
]


def count_story_tasks() -> int:
    return sum(1 for s in LEGEND_SCENES if s.get("type") == "task")


def get_scene(index: int) -> dict | None:
    if index < 0 or index >= len(LEGEND_SCENES):
        return None
    return LEGEND_SCENES[index]


assert count_story_tasks() == TOTAL_TASKS, count_story_tasks()
