"""Пак «Живая речь»: сжатая речь носителей (reductions)."""

from __future__ import annotations

BTN_STREET = "💬 Живая речь"
BTN_TASKS = "📝 Задания"
BTN_BACK_PACKS = "⬅️ К пакам"
BTN_BACK_SECTIONS = "⬅️ К разделам"
BTN_REPLAY = "🔊 Ещё раз"
BTN_SKIP_SPEAK = "⏭ Пропустить произношение"

SECTION_INTRO_HTML = (
    "💬 <b>Живая речь</b>\n\n"
    "🦜 <b>Рико:</b> Учебник говорит <i>want to</i>. "
    "Человек в сериале говорит <b>wanna</b>. "
    "Это не ошибка — так склеивается живая речь.\n\n"
    "Здесь учимся <b>слышать</b> сжатые формы и понимать, "
    "что за ними стоит. Писать <i>donchu</i> как «правильное слово» не будем.\n\n"
    "Пока один пак — чтобы поймать тон. Выбери его ниже."
)

SWALLOW_PACK: dict = {
    "id": "swallow",
    "title_ru": "Как они глотают слова",
    "card_html": (
        "🦜 <b>Рико:</b> Носители не произносят каждое слово, как диктор в учебнике. "
        "Они склеивают. Ниже — шесть штук, которые слышишь постоянно.\n\n"
        "У каждой: сжатая форма → полная → где живёт → рамка.\n\n"
        "<b>wanna</b> → want to\n"
        "Где: речь и чат. <i>I wanna go home.</i>\n"
        "Рамка: с другом — да. В письме HR пиши <i>want to</i>.\n\n"
        "<b>gonna</b> → going to\n"
        "Где: речь и чат. <i>I'm gonna be late.</i>\n"
        "Рамка: планы с друзьями, не эссе.\n\n"
        "<b>gotta</b> → have (got) to\n"
        "Где: речь. <i>I gotta run.</i> — «мне пора / надо бежать».\n"
        "Рамка: срочность, не формальная обязанность в договоре.\n\n"
        "<b>dunno</b> → don't know\n"
        "Где: речь и чат. <i>Dunno, maybe later.</i>\n"
        "Рамка: пожимание плечами, не доклад.\n\n"
        "<b>kinda</b> → kind of\n"
        "Где: речь. <i>I'm kinda busy.</i> — смягчает: «ну такое, типа занят».\n\n"
        "<b>don'tcha</b> → don't you\n"
        "Так <b>слышится</b>. Иногда пишут don'tcha. "
        "<b>donchu</b> — это как звучит, не словарное слово. "
        "В нормальном тексте: <i>don't you</i>.\n\n"
        "Прочитал — жми <b>Задания</b>. Сначала слух, потом письмо, потом голос."
    ),
    "tasks": [
        {
            "id": "t1",
            "kind": "listen_mcq",
            "voice_en": "I wanna go home.",
            "prompt_html": (
                "1/6 🎧 Послушай Рико.\n"
                "Какое <b>полное</b> выражение спряталось в сжатом слове?"
            ),
            "options": ["want to", "going to", "have to"],
            "answer": "want to",
            "ok_html": (
                "✅ <b>wanna</b> = want to.\n"
                "<i>I wanna go home</i> → I want to go home."
            ),
        },
        {
            "id": "t2",
            "kind": "write",
            "prompt_html": (
                "2/6 ✍️ В чате написали:\n"
                "<i>I'm gonna be late.</i>\n\n"
                "Напиши <b>полную форму</b> слова gonna — как в учебнике, два слова."
            ),
            "answer": "going to",
            "accept": ["going to", "i am going to", "i'm going to", "im going to"],
            "ok_html": (
                "✅ <b>gonna</b> = going to.\n"
                "В чате так пишут часто. В школе и на работе — going to."
            ),
        },
        {
            "id": "t3",
            "kind": "mcq",
            "prompt_html": (
                "3/6 🗣 Как это скорее скажет друг, не учебник?\n\n"
                "<i>I am going to call you later.</i>"
            ),
            "options": [
                "I'm gonna call you later.",
                "I'm gotta call you later.",
                "I'm dunno call you later.",
            ],
            "answer": "I'm gonna call you later.",
            "ok_html": (
                "✅ going to в живой речи часто сжимается в <b>gonna</b>.\n"
                "gotta сюда не лезет — это «надо», не «собираюсь»."
            ),
        },
        {
            "id": "t4",
            "kind": "listen_mcq",
            "voice_en": "Don'tcha like pizza?",
            "prompt_html": (
                "4/6 🎧 Послушай вопрос.\n"
                "Какая <b>полная</b> форма спряталась в начале?"
            ),
            "options": ["don't you", "don't know", "kind of"],
            "answer": "don't you",
            "ok_html": (
                "✅ Прозвучало как <b>don'tcha</b> / donchu.\n"
                "Это <i>don't you</i>. Так слышится — писать donchu как слово не надо."
            ),
        },
        {
            "id": "t5",
            "kind": "listen_mcq",
            "voice_en": "Hey, you wanna grab food? Dunno. I'm kinda busy.",
            "prompt_html": "5/6 🎧 Короткий диалог. О чём речь?",
            "options": [
                "Зовут поесть, второй не уверен — занят",
                "Они опаздывают на работу",
                "Кто-то не знает дорогу",
            ],
            "answer": "Зовут поесть, второй не уверен — занят",
            "ok_html": (
                "✅ wanna = приглашение, dunno = не уверен, kinda busy = типа занят.\n"
                "Смысл держится, даже если слова склеены."
            ),
        },
        {
            "id": "t6",
            "kind": "speak",
            "phrase": "I wanna go",
            "accept": ["I wanna go", "I want to go", "I wanna go.", "I want to go."],
            "prompt_html": (
                "6/6 🎤 Скажи в микрофон, как другу:\n"
                "<b>I wanna go</b>\n\n"
                "Расшифровка может написать want to — это нормально. "
                "Главное произнести сжато, не по слогам."
            ),
            "ok_html": "✅ Есть. Wanna — это want to, только живее.",
        },
    ],
}

PACKS: list[dict] = [SWALLOW_PACK]


def get_pack(pack_id: str) -> dict | None:
    for p in PACKS:
        if p["id"] == pack_id:
            return p
    return None


def pack_by_button_label(text: str) -> dict | None:
    raw = (text or "").strip()
    if raw.endswith(" ✅"):
        raw = raw[: -len(" ✅")].rstrip()
    for i, p in enumerate(PACKS, start=1):
        label = f"{i}. {p['title_ru']}"
        if raw == label or raw == p["title_ru"]:
            return p
    return None


def pack_button_label(pack: dict, *, done: bool) -> str:
    idx = next((i for i, p in enumerate(PACKS, start=1) if p["id"] == pack["id"]), 1)
    mark = " ✅" if done else ""
    return f"{idx}. {pack['title_ru']}{mark}"
