"""
Эксклюзивные задания Рико — призы за 1 / 2 / 3 место ивента.
Три разных набора (не один пул).
"""

from __future__ import annotations

# kind: write | fix | voice | mcq
# chapter — для группировки в UI

# 1 место — полноценная сказка в data/exclusive_legend_story.py (20 заданий в сюжете).
# Здесь оставляем метаданные + пустой tasks: контент грузится story-движком.
PLACE_1_PACK: dict = {
    "place": 1,
    "title": "🏆 Легенда LexDan",
    "subtitle": "Сказка: как Рико стал учителем · 20 заданий",
    "mode": "story",
    "intro_html": (
        "📖 <b>Легенда LexDan</b>\n\n"
        "Сказка о том, как Рико получил силу английского и вернул язык королевству."
    ),
    "tasks": [],  # см. exclusive_legend_story.LEGEND_SCENES
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
            "learn": {"kind": "phrase", "en": "spill the tea"},
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
            "learn": {"kind": "phrase", "en": "read the room"},
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
            "learn": {"kind": "phrase", "en": "move the goalposts"},
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
            "learn": {"kind": "phrase", "en": "a blessing in disguise"},
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
            "learn": {"kind": "word", "en": "serendipity"},
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
            "learn": {"kind": "word", "en": "petrichor"},
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
            "learn": {"kind": "word", "en": "ephemeral"},
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
            "learn": {"kind": "word", "en": "flabbergasted"},
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
            "learn": {"kind": "phrase", "en": "I have been waiting since 6 o'clock"},
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
            "learn": {"kind": "phrase", "en": "I agree"},
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
            "learn": {"kind": "phrase", "en": "Don't forget to buy milk"},
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
            "learn": {"kind": "phrase", "en": "If I see her, I will tell her"},
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
            "learn": {"kind": "phrase", "en": "If I had more free time, I would travel"},
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
            "learn": {"kind": "phrase", "en": "If I had more free time, I would travel"},
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
            "learn": {"kind": "phrase", "en": "I've been learning English for two years"},
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
            "learn": {"kind": "phrase", "en": "I've been learning English for two years"},
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
    if int(place) == 1:
        from data.exclusive_legend_story import TOTAL_TASKS

        return TOTAL_TASKS
    p = get_pack(place)
    return len((p or {}).get("tasks") or [])
