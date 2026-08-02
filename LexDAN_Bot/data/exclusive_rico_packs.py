"""
Эксклюзивные задания Рико — призы за 1 / 2 / 3 место ивента.
Три разных набора (не один пул).
"""

from __future__ import annotations

# kind: write | fix | voice | mcq
# chapter — для группировки в UI

PLACE_1_PACK: dict = {
    "place": 1,
    "title": "🏆 Легенда LexDan",
    "subtitle": "Сюжетный мини-курс с Рико · 20 заданий",
    "intro_html": (
        "🦜 <b>Легенда LexDan</b>\n\n"
        "Это твой личный мини-курс. Четыре главы:\n"
        "🗺 квест из 5 актов · 🎙 голос мастера · ✍️ перефраз уровня C · 🔎 ошибки профи.\n\n"
        "Пиши текстом или кидай голос, где просят. Я рядом 💛"
    ),
    "tasks": [
        # ── Quest: The Midnight Feather (5) ──
        {
            "id": "p1_q1",
            "chapter": "quest",
            "chapter_title": "🗺 Квест · The Midnight Feather",
            "kind": "write",
            "title_ru": "Акт 1 · Звонок",
            "prompt_html": (
                "История: ночью Рико получает странное сообщение — "
                "«The feather is missing. Meet me where the river forgets its name.»\n\n"
                "✍️ Напиши <b>3–5 предложений</b> от лица детектива: "
                "что ты чувствуешь и куда пойдёшь сначала. Английский."
            ),
            "check": "free_write",
            "min_words": 12,
            "hint_ru": "Past/present — на твой вкус. Главное — атмосфера и план.",
        },
        {
            "id": "p1_q2",
            "chapter": "quest",
            "chapter_title": "🗺 Квест · The Midnight Feather",
            "kind": "fix",
            "title_ru": "Акт 2 · Записка с ошибками",
            "prompt_html": (
                "На мосту нашли записку:\n"
                "<i>If I would know the truth yesterday, I will told you.</i>\n\n"
                "✍️ Перепиши <b>грамматически верно</b> (одна фраза)."
            ),
            "answer": "If I had known the truth yesterday, I would have told you.",
            "accept": [
                "If I had known the truth yesterday, I would have told you",
                "If I'd known the truth yesterday, I would've told you",
                "If I had known the truth yesterday I would have told you",
            ],
            "hint_ru": "3-я условная: If + Past Perfect → would have + V3.",
        },
        {
            "id": "p1_q3",
            "chapter": "quest",
            "chapter_title": "🗺 Квест · The Midnight Feather",
            "kind": "write",
            "title_ru": "Акт 3 · Диалог в тумане",
            "prompt_html": (
                "Незнакомец шепчет: <i>«Trust is a luxury tonight.»</i>\n\n"
                "✍️ Напиши <b>ответную реплику</b> (2–3 предложения) — "
                "осторожно, умно, по-английски. Покажи характер."
            ),
            "check": "free_write",
            "min_words": 8,
            "hint_ru": "Можно согласиться, отказать или задать вопрос — главное, живо.",
        },
        {
            "id": "p1_q4",
            "chapter": "quest",
            "chapter_title": "🗺 Квест · The Midnight Feather",
            "kind": "mcq",
            "title_ru": "Акт 4 · Выбор тропы",
            "prompt_html": (
                "Две двери. Надпись: <i>«Only one leads to the feather.»</i>\n"
                "Какая фраза звучит естественнее для героя, который уже устал, но не сдаётся?"
            ),
            "options": [
                "I'm too tired for continuing.",
                "I'm too tired to give up now.",
                "I'm enough tired to stop.",
            ],
            "answer": "I'm too tired to give up now.",
            "hint_ru": "too + adjective + to-infinitive.",
        },
        {
            "id": "p1_q5",
            "chapter": "quest",
            "chapter_title": "🗺 Квест · The Midnight Feather",
            "kind": "write",
            "title_ru": "Акт 5 · Финал",
            "prompt_html": (
                "Перо найдено. Но это было твоё собственное перо — символ голоса, "
                "который ты чуть не потерял.\n\n"
                "✍️ Финальный абзац (4–6 предложений): чему научился герой? Английский."
            ),
            "check": "free_write",
            "min_words": 20,
            "hint_ru": "Можно past simple + present perfect. Смысл важнее идеала.",
        },
        # ── Voice master (5) ──
        {
            "id": "p1_v1",
            "chapter": "voice",
            "chapter_title": "🎙 Голос мастера",
            "kind": "voice",
            "title_ru": "Реплика 1 · Boundary",
            "prompt_html": (
                "Произнеси (голосом или текстом) естественно:\n"
                "<b>I'm protecting my focus today — can we talk tomorrow?</b>"
            ),
            "voice_text": "I'm protecting my focus today — can we talk tomorrow?",
            "hint_ru": "Мягкий отказ без «I'm busy».",
        },
        {
            "id": "p1_v2",
            "chapter": "voice",
            "chapter_title": "🎙 Голос мастера",
            "kind": "voice",
            "title_ru": "Реплика 2 · Soften",
            "prompt_html": (
                "Произнеси:\n"
                "<b>I might be wrong, but that deadline feels unrealistic.</b>"
            ),
            "voice_text": "I might be wrong, but that deadline feels unrealistic.",
            "hint_ru": "Смягчение перед жёсткой мыслью.",
        },
        {
            "id": "p1_v3",
            "chapter": "voice",
            "chapter_title": "🎙 Голос мастера",
            "kind": "voice",
            "title_ru": "Реплика 3 · Pushback",
            "prompt_html": (
                "Произнеси:\n"
                "<b>I hear you — and I still need clearer priorities.</b>"
            ),
            "voice_text": "I hear you — and I still need clearer priorities.",
            "hint_ru": "Признать + своя граница.",
        },
        {
            "id": "p1_v4",
            "chapter": "voice",
            "chapter_title": "🎙 Голос мастера",
            "kind": "voice",
            "title_ru": "Реплика 4 · Story beat",
            "prompt_html": (
                "Произнеси с вайбом сторителлинга:\n"
                "<b>Long story short — we shipped it at 2 a.m. and somehow it worked.</b>"
            ),
            "voice_text": "Long story short — we shipped it at 2 a.m. and somehow it worked.",
            "hint_ru": "Разговорный ритм, не диктор.",
        },
        {
            "id": "p1_v5",
            "chapter": "voice",
            "chapter_title": "🎙 Голос мастера",
            "kind": "voice",
            "title_ru": "Реплика 5 · Close",
            "prompt_html": (
                "Произнеси:\n"
                "<b>Let's leave it here for now — solid progress for one day.</b>"
            ),
            "voice_text": "Let's leave it here for now — solid progress for one day.",
            "hint_ru": "Закрытие разговора по-взрослому.",
        },
        # ── Paraphrase C (5) ──
        {
            "id": "p1_p1",
            "chapter": "paraphrase",
            "chapter_title": "✍️ Перефраз · уровень C",
            "kind": "write",
            "title_ru": "Перефраз 1",
            "prompt_html": (
                "Исходник: <i>I'm busy.</i>\n\n"
                "✍️ Перефразируй <b>взрослее и конкретнее</b> (1–2 предложения). "
                "Время/смысл те же."
            ),
            "check": "paraphrase",
            "source": "I'm busy.",
            "hint_ru": "Например про фокус, дедлайн, слот — без грубости.",
        },
        {
            "id": "p1_p2",
            "chapter": "paraphrase",
            "chapter_title": "✍️ Перефраз · уровень C",
            "kind": "write",
            "title_ru": "Перефраз 2",
            "prompt_html": (
                "Исходник: <i>Your idea is bad.</i>\n\n"
                "✍️ Скажи то же <b>дипломатично</b>, сохранив критику."
            ),
            "check": "paraphrase",
            "source": "Your idea is bad.",
            "hint_ru": "I see the intention, but… / Have we considered…",
        },
        {
            "id": "p1_p3",
            "chapter": "paraphrase",
            "chapter_title": "✍️ Перефраз · уровень C",
            "kind": "write",
            "title_ru": "Перефраз 3",
            "prompt_html": (
                "Исходник: <i>I don't understand.</i>\n\n"
                "✍️ Перефраз для созвона с командой — коротко и по делу."
            ),
            "check": "paraphrase",
            "source": "I don't understand.",
            "hint_ru": "Could you walk me through… / I'm not following the part about…",
        },
        {
            "id": "p1_p4",
            "chapter": "paraphrase",
            "chapter_title": "✍️ Перефраз · уровень C",
            "kind": "write",
            "title_ru": "Перефраз 4",
            "prompt_html": (
                "Исходник: <i>We need to hurry.</i>\n\n"
                "✍️ Более «взрослая» версия без паники."
            ),
            "check": "paraphrase",
            "source": "We need to hurry.",
            "hint_ru": "We're tight on time / Let's prioritise…",
        },
        {
            "id": "p1_p5",
            "chapter": "paraphrase",
            "chapter_title": "✍️ Перефраз · уровень C",
            "kind": "write",
            "title_ru": "Перефраз 5",
            "prompt_html": (
                "Исходник: <i>This is very important.</i>\n\n"
                "✍️ Перефраз с нюансом: важно <b>почему</b>."
            ),
            "check": "paraphrase",
            "source": "This is very important.",
            "hint_ru": "This blocks the launch / This affects the client…",
        },
        # ── Pro errors (5) ──
        {
            "id": "p1_e1",
            "chapter": "pro_errors",
            "chapter_title": "🔎 Ошибки профи",
            "kind": "fix",
            "title_ru": "Тонкая ошибка 1",
            "prompt_html": (
                "Почини:\n<i>I look forward to meet you.</i>"
            ),
            "answer": "I look forward to meeting you.",
            "accept": [
                "I look forward to meeting you",
                "I'm looking forward to meeting you",
                "I am looking forward to meeting you",
            ],
            "hint_ru": "look forward to + V-ing (to — предлог).",
        },
        {
            "id": "p1_e2",
            "chapter": "pro_errors",
            "chapter_title": "🔎 Ошибки профи",
            "kind": "fix",
            "title_ru": "Тонкая ошибка 2",
            "prompt_html": "Почини:\n<i>She suggested me to leave early.</i>",
            "answer": "She suggested that I leave early.",
            "accept": [
                "She suggested that I leave early",
                "She suggested I leave early",
                "She suggested leaving early",
                "She suggested that I should leave early",
            ],
            "hint_ru": "suggest + that-clause / V-ing — не suggest someone to.",
        },
        {
            "id": "p1_e3",
            "chapter": "pro_errors",
            "chapter_title": "🔎 Ошибки профи",
            "kind": "fix",
            "title_ru": "Тонкая ошибка 3",
            "prompt_html": "Почини:\n<i>Despite of the rain, we went out.</i>",
            "answer": "Despite the rain, we went out.",
            "accept": [
                "Despite the rain, we went out",
                "In spite of the rain, we went out",
                "Despite the rain we went out",
            ],
            "hint_ru": "despite + noun (без of). in spite of — ок.",
        },
        {
            "id": "p1_e4",
            "chapter": "pro_errors",
            "chapter_title": "🔎 Ошибки профи",
            "kind": "fix",
            "title_ru": "Тонкая ошибка 4",
            "prompt_html": "Почини:\n<i>I am used to wake up early.</i>",
            "answer": "I am used to waking up early.",
            "accept": [
                "I am used to waking up early",
                "I'm used to waking up early",
                "I got used to waking up early",
            ],
            "hint_ru": "be used to + V-ing.",
        },
        {
            "id": "p1_e5",
            "chapter": "pro_errors",
            "chapter_title": "🔎 Ошибки профи",
            "kind": "fix",
            "title_ru": "Тонкая ошибка 5",
            "prompt_html": "Почини:\n<i>It's high time we go home.</i>",
            "answer": "It's high time we went home.",
            "accept": [
                "It's high time we went home",
                "It is high time we went home",
                "It's high time we were going home",
            ],
            "hint_ru": "It's high time + Past Simple (unreal past).",
        },
    ],
}

PLACE_2_PACK: dict = {
    "place": 2,
    "title": "🥈 Мастер коллекции",
    "subtitle": "Редкие обороты и карты слов · 8 заданий",
    "intro_html": (
        "🦜 <b>Мастер коллекции</b>\n\n"
        "Ты собираешь редкости языка:\n"
        "💬 4 живых оборота · 🗂 4 карты слов (origin → пример → своё предложение).\n\n"
        "Это не учебник — это коллекция ✨"
    ),
    "tasks": [
        {
            "id": "p2_s1",
            "chapter": "slang",
            "chapter_title": "💬 Сленг / идиомы",
            "kind": "write",
            "title_ru": "Оборот 1 · spill the tea",
            "prompt_html": (
                "<b>spill the tea</b> — рассказать сочные подробности / сплетни (разговорно).\n\n"
                "✍️ Одно предложение со <b>spill the tea</b> — как в чате с другом."
            ),
            "check": "must_include",
            "must_include": ["spill the tea", "spilling the tea", "spilled the tea"],
            "min_words": 5,
            "hint_ru": "Не для собеседования — для сторис и друзей.",
        },
        {
            "id": "p2_s2",
            "chapter": "slang",
            "chapter_title": "💬 Сленг / идиомы",
            "kind": "write",
            "title_ru": "Оборот 2 · read the room",
            "prompt_html": (
                "<b>read the room</b> — считать атмосферу, понимать, что уместно.\n\n"
                "✍️ Предложение с <b>read the room</b>."
            ),
            "check": "must_include",
            "must_include": ["read the room", "reading the room", "reads the room"],
            "min_words": 5,
            "hint_ru": "Часто про шутки не вовремя.",
        },
        {
            "id": "p2_s3",
            "chapter": "slang",
            "chapter_title": "💬 Сленг / идиомы",
            "kind": "write",
            "title_ru": "Оборот 3 · move the goalposts",
            "prompt_html": (
                "<b>move the goalposts</b> — менять правила / критерии по ходу.\n\n"
                "✍️ Предложение про работу или учёбу с этим оборотом."
            ),
            "check": "must_include",
            "must_include": ["move the goalposts", "moving the goalposts", "moved the goalposts"],
            "min_words": 5,
            "hint_ru": "Классика бесконечных правок ТЗ.",
        },
        {
            "id": "p2_s4",
            "chapter": "slang",
            "chapter_title": "💬 Сленг / идиомы",
            "kind": "write",
            "title_ru": "Оборот 4 · a blessing in disguise",
            "prompt_html": (
                "<b>a blessing in disguise</b> — скрытое благо.\n\n"
                "✍️ Предложение: что сначала казалось плохим, а вышло в плюс."
            ),
            "check": "must_include",
            "must_include": ["blessing in disguise"],
            "min_words": 5,
            "hint_ru": "Losing X was a blessing in disguise…",
        },
        {
            "id": "p2_w1",
            "chapter": "word_map",
            "chapter_title": "🗂 Карта слова",
            "kind": "write",
            "title_ru": "Карта · serendipity",
            "prompt_html": (
                "<b>serendipity</b> — счастливая случайность.\n"
                "🕰 Origin: от старого названия Шри-Ланки (Serendip) + сказка о находках.\n"
                "💬 Пример: <i>I found this café by pure serendipity.</i>\n\n"
                "✍️ Своё предложение с <b>serendipity</b>."
            ),
            "check": "must_include",
            "must_include": ["serendipity"],
            "min_words": 5,
            "hint_ru": "Не «удача» в казино — именно неожиданная находка.",
        },
        {
            "id": "p2_w2",
            "chapter": "word_map",
            "chapter_title": "🗂 Карта слова",
            "kind": "write",
            "title_ru": "Карта · petrichor",
            "prompt_html": (
                "<b>petrichor</b> — запах земли после дождя.\n"
                "🕰 От греч. petra (камень) + ichor.\n"
                "💬 <i>The petrichor after the storm made the city smell new.</i>\n\n"
                "✍️ Своё предложение с <b>petrichor</b>."
            ),
            "check": "must_include",
            "must_include": ["petrichor"],
            "min_words": 5,
            "hint_ru": "Поэтично, но можно и в быту.",
        },
        {
            "id": "p2_w3",
            "chapter": "word_map",
            "chapter_title": "🗂 Карта слова",
            "kind": "write",
            "title_ru": "Карта · ephemeral",
            "prompt_html": (
                "<b>ephemeral</b> — мимолётный, недолговечный.\n"
                "🕰 От греч. «для одного дня».\n"
                "💬 <i>Street art is often ephemeral.</i>\n\n"
                "✍️ Своё предложение с <b>ephemeral</b>."
            ),
            "check": "must_include",
            "must_include": ["ephemeral"],
            "min_words": 5,
            "hint_ru": "Закат, пенка, тренд — всё ephemeral.",
        },
        {
            "id": "p2_w4",
            "chapter": "word_map",
            "chapter_title": "🗂 Карта слова",
            "kind": "write",
            "title_ru": "Карта · flabbergasted",
            "prompt_html": (
                "<b>flabbergasted</b> — ошарашенный (разговорно, театрально).\n"
                "💬 <i>I was flabbergasted by how good the tiny café was.</i>\n\n"
                "✍️ Своё предложение с <b>flabbergasted</b>."
            ),
            "check": "must_include",
            "must_include": ["flabbergasted"],
            "min_words": 5,
            "hint_ru": "Сильнее, чем surprised.",
        },
    ],
}

PLACE_3_PACK: dict = {
    "place": 3,
    "title": "🥉 Охотник за картами",
    "subtitle": "Охота на ошибки и загадки · 8 заданий",
    "intro_html": (
        "🦜 <b>Охотник за картами</b>\n\n"
        "Быстрые раунды:\n"
        "🎯 4 охоты на ошибку · 🧩 4 спойлер-квеста (угадай конструкцию).\n\n"
        "Поймал — забрал. Поехали 🔥"
    ),
    "tasks": [
        {
            "id": "p3_h1",
            "chapter": "hunt",
            "chapter_title": "🎯 Охота на ошибку",
            "kind": "fix",
            "title_ru": "Охота 1",
            "prompt_html": (
                "Диалог:\n"
                "A: How long do you wait here?\n"
                "B: <i>I wait since 6 o'clock.</i>\n\n"
                "✍️ Исправь реплику B."
            ),
            "answer": "I have been waiting since 6 o'clock.",
            "accept": [
                "I have been waiting since 6 o'clock",
                "I've been waiting since 6 o'clock",
                "I have been waiting since six o'clock",
                "I've been waiting since six",
            ],
            "hint_ru": "since + Present Perfect Continuous.",
        },
        {
            "id": "p3_h2",
            "chapter": "hunt",
            "chapter_title": "🎯 Охота на ошибку",
            "kind": "fix",
            "title_ru": "Охота 2",
            "prompt_html": (
                "A: Want coffee?\n"
                "B: <i>I am agree.</i>\n\n"
                "✍️ Исправь B."
            ),
            "answer": "I agree.",
            "accept": ["I agree", "Yes, I agree", "I agree with that"],
            "hint_ru": "agree — глагол, без am.",
        },
        {
            "id": "p3_h3",
            "chapter": "hunt",
            "chapter_title": "🎯 Охота на ошибку",
            "kind": "fix",
            "title_ru": "Охота 3",
            "prompt_html": (
                "Note on the fridge:\n"
                "<i>Don't forget buying milk.</i>\n\n"
                "✍️ Почини."
            ),
            "answer": "Don't forget to buy milk.",
            "accept": [
                "Don't forget to buy milk",
                "Do not forget to buy milk",
                "Don't forget to buy some milk",
            ],
            "hint_ru": "forget + to-infinitive = не забудь сделать.",
        },
        {
            "id": "p3_h4",
            "chapter": "hunt",
            "chapter_title": "🎯 Охота на ошибку",
            "kind": "fix",
            "title_ru": "Охота 4",
            "prompt_html": (
                "Chat:\n"
                "<i>If I will see her, I tell her.</i>\n\n"
                "✍️ Почини (1-я условная)."
            ),
            "answer": "If I see her, I will tell her.",
            "accept": [
                "If I see her, I will tell her",
                "If I see her I'll tell her",
                "If I see her, I'll tell her",
            ],
            "hint_ru": "If + Present, will + V1 — без will в if.",
        },
        {
            "id": "p3_r1",
            "chapter": "riddle",
            "chapter_title": "🧩 Спойлер-квест",
            "kind": "mcq",
            "title_ru": "Загадка 1",
            "prompt_html": (
                "Рико шепчет: <i>«Гипотеза про сейчас: If + Past… then would + V1.»</i>\n\n"
                "Что это за конструкция?"
            ),
            "options": [
                "1st conditional",
                "2nd conditional",
                "Present Perfect",
            ],
            "answer": "2nd conditional",
            "hint_ru": "If I had more time, I would…",
        },
        {
            "id": "p3_r2",
            "chapter": "riddle",
            "chapter_title": "🧩 Спойлер-квест",
            "kind": "write",
            "title_ru": "Загадка 2 · допиши",
            "prompt_html": (
                "Стем 2-й условной: <i>If I had more free time,</i>\n\n"
                "✍️ Допиши конец с <b>would + V1</b> (не would have)."
            ),
            "check": "must_include",
            "must_include": ["would"],
            "forbid": ["would have", "would've", "would of"],
            "min_words": 4,
            "hint_ru": "I would train / travel / sleep…",
        },
        {
            "id": "p3_r3",
            "chapter": "riddle",
            "chapter_title": "🧩 Спойлер-квест",
            "kind": "mcq",
            "title_ru": "Загадка 3",
            "prompt_html": (
                "Рико: <i>«Действие началось в прошлом и всё ещё идёт: have/has been + V-ing.»</i>\n\n"
                "Что это?"
            ),
            "options": [
                "Past Simple",
                "Present Perfect Continuous",
                "Future Perfect",
            ],
            "answer": "Present Perfect Continuous",
            "hint_ru": "I've been waiting since…",
        },
        {
            "id": "p3_r4",
            "chapter": "riddle",
            "chapter_title": "🧩 Спойлер-квест",
            "kind": "write",
            "title_ru": "Загадка 4 · допиши",
            "prompt_html": (
                "Стем: <i>I've been learning English</i>\n\n"
                "✍️ Допиши естественно (с for/since или результатом)."
            ),
            "check": "must_include",
            "must_include": ["i've been learning", "i have been learning"],
            "min_words": 6,
            "hint_ru": "…for two years / since 2024 / and I still love it.",
        },
    ],
}

PACKS_BY_PLACE: dict[int, dict] = {
    1: PLACE_1_PACK,
    2: PLACE_2_PACK,
    3: PLACE_3_PACK,
}


def get_pack(place: int) -> dict | None:
    return PACKS_BY_PLACE.get(int(place))


def pack_task_count(place: int) -> int:
    p = get_pack(place)
    return len((p or {}).get("tasks") or [])
