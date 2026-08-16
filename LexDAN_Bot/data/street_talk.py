"""Живая речь: слайды + голос. Пока A1, только MANAGER_ID."""

from __future__ import annotations

BTN_STREET = "🤙 Живая речь"
BTN_NEXT = "➡️ Далее"
BTN_PREV = "⬅️ Назад"
BTN_BACK_PACKS = "⬅️ К пакам"
BTN_BACK_SECTIONS = "⬅️ К разделам"
BTN_REPLAY = "🔊 Ещё раз"
BTN_SKIP_SPEAK = "⏭ Пропустить произношение"
BTN_REMIND = "🦜 Напомнить"

SECTION_INTRO_HTML = (
    "🤙 <b>Живая речь</b> · A1\n\n"
    "🦜 <b>Рико:</b> Учебник говорит по слогам. Люди — нет. "
    "Они склеивают слова и кивают короткими ответами.\n\n"
    "Здесь паки и <b>пять диалогов</b> 🎧\n"
    "🌀 <b>«Глотание слов»</b> · 1–3 — как звучит wanna, don'tcha, c'mon\n"
    "😎 <b>По-свойски</b> — короткие живые ответы: yeah, nope, see ya\n\n"
    "На слайдах я озвучу пример, ты повторишь. "
    "В диалогах — слушай, потом отвечай на вопросы голосом 🎤"
)

_WARN_CHAT = (
    "на собеседовании, в письме HR и в официальном разговоре так не говорят — "
    "это слишком расслабленно."
)
_WARN_HEAR = (
    "так <b>слышится</b>. В чате иногда пишут так же. "
    "В нормальном тексте — правая колонка. На собеседовании — только полная форма."
)
_WARN_REPLY = (
    "с друзьями и в чате — да. На собеседовании лучше yes / no / thank you / goodbye."
)


def _item(
    form: str,
    full: str,
    where: str,
    example: str,
    *,
    warn: str = _WARN_CHAT,
    voice_en: str | None = None,
    accept: list[str] | None = None,
    extra: str = "",
) -> dict:
    full_ex = example
    if form.lower() in example.lower() and full.lower() not in example.lower():
        # грубая замена для accept: I wanna → I want to
        idx = example.lower().find(form.lower())
        if idx >= 0:
            full_ex = example[:idx] + full + example[idx + len(form) :]
    acc = list(accept or [])
    for x in (example, full_ex, form, full):
        if x and x not in acc:
            acc.append(x)
    return {
        "form": form,
        "full": full,
        "where": where,
        "example": example,
        "warn": warn,
        "voice_en": (voice_en or example).strip(),
        "accept": acc,
        "extra": extra,
    }


def _prod(
    must: list[str],
    prompt_html: str,
    *,
    min_words: int = 3,
    remind_html: str = "",
    as_question: bool = False,
) -> dict:
    return {
        "must": must,
        "prompt_html": prompt_html,
        "min_words": min_words,
        "remind_html": remind_html,
        "as_question": as_question,
    }


def format_remind_html(task: dict) -> str:
    custom = (task.get("remind_html") or "").strip()
    if custom:
        if custom.startswith("🦜"):
            return custom
        return f"🦜 <b>Рико:</b> {custom}"
    must = [str(x) for x in (task.get("must") or []) if x]
    if len(must) >= 2:
        return (
            f"🦜 <b>Рико:</b> <b>{must[0]}</b> → <i>{must[1]}</i>. "
            "Скажи это вслух, как другу."
        )
    if must:
        return f"🦜 <b>Рико:</b> Держи форму: <b>{must[0]}</b>."
    return "🦜 <b>Рико:</b> Скажи живую фразу по заданию — коротко и вслух."


def format_item_html(pack_title: str, n: int, total: int, item: dict) -> str:
    extra = (item.get("extra") or "").strip()
    extra_block = f"\n\n{extra}" if extra else ""
    return (
        f"🤙 <b>{n}/{total}</b> · {pack_title}\n\n"
        f"<b>{item['form']}</b>  →  <i>{item['full']}</i>\n\n"
        f"📍 <b>Где:</b> {item['where']}\n"
        f"💬 <b>Пример:</b> <i>{item['example']}</i>\n"
        f"⚠️ <b>Важно:</b> {item['warn']}"
        f"{extra_block}\n\n"
        "🦜 Послушай пример и <b>повтори в микрофон</b>.\n"
        "<i>Расшифровка может написать полную форму — это нормально.</i>"
    )


def format_produce_html(pack_title: str, n: int, total: int, task: dict) -> str:
    if task.get("as_question"):
        return (
            f"❓ <b>Вопрос {n}/{total}</b> · {pack_title}\n\n"
            f"{task['prompt_html']}\n\n"
            "🦜 Ответь <b>голосом</b> по-английски. Можно своими словами.\n"
            "Напомнить — если забыл, о чём речь."
        )
    return (
        f"🎤 <b>Своя фраза {n}/{total}</b> · {pack_title}\n\n"
        f"{task['prompt_html']}\n\n"
        "🦜 Скажи это <b>голосом</b>, как другу. Не читай с листа идеально — "
        "главное, чтобы конструкция прозвучала."
    )


def format_line_html(pack_title: str, n: int, total: int, line: dict) -> str:
    who = line.get("who") or "…"
    text = line.get("text") or ""
    return (
        f"🎧 <b>Реплика {n}/{total}</b> · {pack_title}\n\n"
        f"👤 <b>{who}:</b>\n"
        f"<i>{text}</i>\n\n"
        "Слушай. Потом <b>Далее</b> — следующая реплика, в конце вопросы."
    )


SWALLOW_1 = {
    "id": "swallow_1",
    "title_ru": "«Глотание слов» · 1",
    "intro_html": (
        "🦜 <b>Рико:</b> Носители не произносят каждое слово, как диктор в учебнике. "
        "Они склеивают 🧃\n\n"
        "Это <b>часть 1 из 3</b> — десять склеек, которые слышишь постоянно: "
        "wanna, gonna, gotta, hafta…\n\n"
        "На слайде: сжатая форма → как писать правильно → где живёт → пример.\n"
        "Я озвучу пример, ты повторишь. В конце — свои фразы в микрофон 🎤\n\n"
        "Жми <b>Далее</b> — поехали."
    ),
    "done_html": (
        "🏁 <b>«Глотание слов» · 1</b> — есть!\n\n"
        "🦜 Теперь wanna и gonna не шум: ты их слышишь и можешь сказать. "
        "Дальше — часть 2, про вопросы."
    ),
    "items": [
        _item(
            "wanna",
            "want to",
            "повседневная речь и переписка с друзьями.",
            "I wanna go home.",
        ),
        _item(
            "gonna",
            "going to",
            "планы с друзьями, речь и чат.",
            "I'm gonna call you later.",
        ),
        _item(
            "gotta",
            "have got to / have to",
            "живая речь, когда «надо / пора».",
            "I gotta run.",
            accept=["I gotta run", "I have to run", "I have got to run", "I've got to run"],
        ),
        _item(
            "hafta",
            "have to",
            "речь: have to склеивается в hafta.",
            "I hafta go now.",
            accept=["I hafta go now", "I have to go now", "I have to go"],
        ),
        _item(
            "hasta",
            "has to",
            "речь, про he/she/it: has to → hasta.",
            "She hasta work today.",
            accept=["She hasta work today", "She has to work today"],
        ),
        _item(
            "dunno",
            "don't know",
            "речь и чат — пожимание плечами.",
            "I dunno. Maybe later.",
            accept=["I dunno", "I don't know", "I dunno maybe later", "I don't know maybe later"],
        ),
        _item(
            "kinda",
            "kind of",
            "речь: смягчает, «типа / вроде».",
            "I'm kinda tired.",
            accept=["I'm kinda tired", "I am kinda tired", "I'm kind of tired", "I am kind of tired"],
        ),
        _item(
            "sorta",
            "sort of",
            "речь, почти как kinda.",
            "It's sorta weird.",
            accept=["It's sorta weird", "It is sorta weird", "It's sort of weird", "It is sort of weird"],
        ),
        _item(
            "lemme",
            "let me",
            "речь и чат, когда просишь секунду.",
            "Lemme see.",
            accept=["Lemme see", "Let me see"],
        ),
        _item(
            "gimme",
            "give me",
            "речь и чат — «дай / подожди».",
            "Gimme a second.",
            accept=["Gimme a second", "Give me a second"],
        ),
    ],
    "produce": [
        _prod(
            ["wanna", "want to"],
            "Скажи, <b>куда ты wanna go</b> — одно короткое предложение.\n"
            "Например думай: домой / в кафе / гулять.",
        ),
        _prod(
            ["gonna", "going to"],
            "Скажи, что ты <b>gonna</b> делать вечером.",
        ),
        _prod(
            ["dunno", "don't know", "do not know"],
            "Тебя спросили «что будем делать?». Ответь через <b>dunno</b>.",
        ),
        _prod(
            ["gimme", "give me", "lemme", "let me"],
            "Попроси паузу: <b>gimme a second</b> или <b>lemme see</b>.",
        ),
        _prod(
            ["kinda", "kind of", "sorta", "sort of"],
            "Скажи, что ты <b>kinda</b> или <b>sorta</b> устал / занят.",
        ),
    ],
}

SWALLOW_2 = {
    "id": "swallow_2",
    "title_ru": "«Глотание слов» · 2",
    "intro_html": (
        "🦜 <b>Рико:</b> Часть 2 — вопросы. "
        "Don't you в речи часто звучит как <b>don'tcha</b>. "
        "Did you — как <b>didja</b>. Это не новые слова, это склейка 👂\n\n"
        "Писать donchu как словарное слово не надо. "
        "Слышать — надо. Повторяй за мной, потом свои вопросы голосом."
    ),
    "done_html": (
        "🏁 <b>«Глотание слов» · 2</b> закрыта.\n\n"
        "🦜 Don'tcha и whatcha больше не пугают. "
        "Часть 3 — woulda, outta, c'mon."
    ),
    "items": [
        _item(
            "don'tcha",
            "don't you",
            "живая речь, вопросы к собеседнику.",
            "Don'tcha like pizza?",
            warn=_WARN_HEAR,
            extra="💡 <i>donchu</i> — только как звучит, не как слово в словаре.",
            accept=["Don'tcha like pizza", "Don't you like pizza", "Dontcha like pizza"],
        ),
        _item(
            "won'tcha",
            "won't you",
            "речь: мягкое «а не хочешь…?».",
            "Won'tcha come with us?",
            warn=_WARN_HEAR,
            accept=["Won'tcha come with us", "Won't you come with us", "Will you not come with us"],
        ),
        _item(
            "didja",
            "did you",
            "речь, вопрос про прошлое.",
            "Didja see that?",
            warn=_WARN_HEAR,
            accept=["Didja see that", "Did you see that", "Did ya see that"],
        ),
        _item(
            "d'ya",
            "do you",
            "речь, быстрый вопрос.",
            "D'ya want coffee?",
            warn=_WARN_HEAR,
            voice_en="Dya want coffee?",
            accept=["D'ya want coffee", "Do you want coffee", "Do ya want coffee", "Dya want coffee"],
        ),
        _item(
            "wouldja",
            "would you",
            "речь: вежливая просьба, но разговорная.",
            "Wouldja help me?",
            warn=_WARN_HEAR,
            accept=["Wouldja help me", "Would you help me", "Would ya help me"],
        ),
        _item(
            "couldja",
            "could you",
            "речь: «можешь…?».",
            "Couldja wait a minute?",
            warn=_WARN_HEAR,
            accept=["Couldja wait a minute", "Could you wait a minute", "Could ya wait a minute"],
        ),
        _item(
            "whatcha",
            "what are you / what do you",
            "речь и чат: Whatcha doing?",
            "Whatcha doing?",
            warn=_WARN_HEAR,
            accept=[
                "Whatcha doing",
                "What are you doing",
                "What do you doing",
                "What you doing",
                "Watcha doing",
            ],
        ),
        _item(
            "gotcha",
            "got you",
            "речь и чат: «понял / поймал».",
            "Gotcha. I get it.",
            accept=["Gotcha", "Got you", "Gotcha I get it", "I get it"],
        ),
        _item(
            "betcha",
            "bet you",
            "речь: «спорим / почти уверен».",
            "Betcha he's late.",
            warn=_WARN_HEAR,
            accept=["Betcha he's late", "Bet you he's late", "I betcha he's late", "I bet he's late"],
        ),
        _item(
            "aren'tcha",
            "aren't you",
            "речь, вопрос-уточнение.",
            "Aren'tcha coming?",
            warn=_WARN_HEAR,
            accept=["Aren'tcha coming", "Aren't you coming", "Are you not coming"],
        ),
    ],
    "produce": [
        _prod(
            ["don'tcha", "don't you", "dontcha", "do not you"],
            "Задай вопрос с <b>don'tcha</b> — например про еду или фильм.",
        ),
        _prod(
            ["whatcha", "what are you", "what you"],
            "Спроси друга: <b>whatcha doing</b>?",
        ),
        _prod(
            ["wouldja", "would you", "couldja", "could you"],
            "Попроси о помощи через <b>wouldja</b> или <b>couldja</b>.",
        ),
        _prod(
            ["gotcha", "got you"],
            "Ответь, что понял: коротко скажи <b>gotcha</b> и добавь пару слов.",
            min_words=2,
        ),
        _prod(
            ["didja", "did you"],
            "Спроси про прошлое: <b>didja see…</b> / <b>didja finish…</b>",
        ),
    ],
}

SWALLOW_3 = {
    "id": "swallow_3",
    "title_ru": "«Глотание слов» · 3",
    "intro_html": (
        "🦜 <b>Рико:</b> Часть 3 — would have сжимается в <b>woulda</b>, "
        "out of — в <b>outta</b>, come on — в <b>c'mon</b>.\n\n"
        "Это уже «как в сериале». Послушай, повтори, потом свои фразы 🎬"
    ),
    "done_html": (
        "🏁 Три части «Глотания слов» позади — ты зверь 🔥\n\n"
        "🦜 Остался пробник <b>По-свойски</b>: yeah, nope, see ya. Коротко и по делу."
    ),
    "items": [
        _item(
            "woulda",
            "would have",
            "речь про то, что могло бы быть.",
            "I woulda called you.",
            accept=["I woulda called you", "I would have called you", "I would've called you"],
        ),
        _item(
            "coulda",
            "could have",
            "речь: «мог бы».",
            "I coulda won.",
            accept=["I coulda won", "I could have won", "I could've won"],
        ),
        _item(
            "shoulda",
            "should have",
            "речь: «надо было».",
            "I shoulda left earlier.",
            accept=["I shoulda left earlier", "I should have left earlier", "I should've left earlier"],
        ),
        _item(
            "outta",
            "out of",
            "речь и чат: out of → outta.",
            "I'm outta time.",
            accept=["I'm outta time", "I am outta time", "I'm out of time", "I am out of time"],
        ),
        _item(
            "lotta",
            "a lot of",
            "речь: a lot of → lotta.",
            "That's a lotta work.",
            accept=["That's a lotta work", "That is a lotta work", "That's a lot of work", "That is a lot of work"],
        ),
        _item(
            "'cause",
            "because",
            "речь и чат. Иногда пишут cuz.",
            "I'm staying in 'cause I'm tired.",
            voice_en="I'm staying in cause I'm tired.",
            accept=[
                "I'm staying in 'cause I'm tired",
                "I'm staying in because I'm tired",
                "I'm staying in cause I'm tired",
                "I am staying in because I'm tired",
            ],
        ),
        _item(
            "'em",
            "them",
            "речь: them часто сжимается в 'em.",
            "Tell 'em I'll be late.",
            voice_en="Tell em I'll be late.",
            extra="💡 В тексте пиши <i>them</i>. В речи можно 'em.",
            accept=["Tell 'em I'll be late", "Tell them I'll be late", "Tell em I'll be late"],
        ),
        _item(
            "tryna",
            "trying to",
            "речь и чат.",
            "I'm tryna sleep.",
            accept=["I'm tryna sleep", "I am tryna sleep", "I'm trying to sleep", "I am trying to sleep"],
        ),
        _item(
            "useta",
            "used to",
            "речь про привычку в прошлом.",
            "I useta live there.",
            voice_en="I used ta live there.",
            accept=["I useta live there", "I used to live there", "I used ta live there"],
        ),
        _item(
            "c'mon",
            "come on",
            "речь и чат: подгон / «ну же».",
            "C'mon, let's go.",
            voice_en="Cmon, let's go.",
            accept=["C'mon let's go", "Come on let's go", "Cmon let's go", "Come on"],
        ),
    ],
    "produce": [
        _prod(
            ["shoulda", "should have", "should've"],
            "Скажи, что ты <b>shoulda</b> сделал раньше.",
        ),
        _prod(
            ["outta", "out of"],
            "Скажи, что ты <b>outta</b> time / money / energy.",
        ),
        _prod(
            ["cause", "because", "cuz"],
            "Объясни почему — через <b>'cause</b>.",
        ),
        _prod(
            ["tryna", "trying to"],
            "Скажи, что ты <b>tryna</b> сделать прямо сейчас.",
        ),
        _prod(
            ["c'mon", "come on", "cmon"],
            "Подгони друга: <b>c'mon</b> + куда идём / что делаем.",
        ),
    ],
}

CASUAL_PACK = {
    "id": "casual_a1",
    "title_ru": "По-свойски",
    "intro_html": (
        "😎 <b>По-свойски</b> · пробник A1\n\n"
        "🦜 <b>Рико:</b> Это не склейка, а короткие живые ответы. "
        "В учебнике — yes. В жизни — <b>yeah</b>. "
        "В учебнике — goodbye. В чате — <b>see ya</b>.\n\n"
        "Шесть штук, голос, повтор — и три своих реплики. Короткий заход ✌️"
    ),
    "done_html": (
        "🏁 Пробник <b>По-свойски</b> пройден.\n\n"
        "🦜 Yeah / nope / see ya — уже можно кидать в чат с другом. "
        "Официально по-прежнему yes, no, goodbye."
    ),
    "items": [
        _item(
            "yeah",
            "yes",
            "согласие с другом, чат, голос.",
            "Yeah, I'm coming.",
            warn=_WARN_REPLY,
            accept=["Yeah I'm coming", "Yes I'm coming", "Yeah I am coming"],
        ),
        _item(
            "nope",
            "no",
            "лёгкий отказ, не злой.",
            "Nope, not today.",
            warn=_WARN_REPLY,
            accept=["Nope not today", "No not today", "Nope"],
        ),
        _item(
            "ok",
            "all right / okay",
            "везде, даже на работе ок. Okay — чуть спокойнее.",
            "Ok, let's do it.",
            warn="это нейтрально. Okay тоже ок. На очень формальном письме лучше all right / certainly.",
            accept=["Ok let's do it", "Okay let's do it", "OK let's do it"],
        ),
        _item(
            "thanks",
            "thank you",
            "речь и чат. Thank you — вежливее и длиннее.",
            "Thanks, that's kind.",
            warn="с друзьями thanks. Чужому человеку / на работе часто thank you.",
            accept=["Thanks that's kind", "Thank you that's kind", "Thanks"],
        ),
        _item(
            "see ya",
            "see you",
            "прощание с другом, в конце чата.",
            "See ya tomorrow.",
            warn=_WARN_REPLY,
            accept=["See ya tomorrow", "See you tomorrow", "See ya"],
        ),
        _item(
            "sure",
            "yes / of course",
            "лёгкое «конечно / ок, сделаю».",
            "Sure, I can help.",
            warn="с друзьями и коллегами норм. В очень сухом письме — of course / certainly.",
            accept=["Sure I can help", "Sure", "Of course I can help"],
        ),
    ],
    "produce": [
        _prod(
            ["yeah", "yes"],
            "Согласись по-свойски: <b>yeah</b> + что ты делаешь / куда идёшь.",
        ),
        _prod(
            ["nope", "no"],
            "Откажись мягко: <b>nope</b> + почему / когда не можешь.",
        ),
        _prod(
            ["see ya", "see you"],
            "Попрощайся: <b>see ya</b> + когда (tomorrow / later / on Friday).",
        ),
    ],
}

for _p in (SWALLOW_1, SWALLOW_2, SWALLOW_3, CASUAL_PACK):
    _p["level"] = "A1"

A1_PACKS: list[dict] = [SWALLOW_1, SWALLOW_2, SWALLOW_3, CASUAL_PACK]


def all_packs() -> list[dict]:
    from data.street_talk_levels import EXTRA_PACKS
    from data.street_talk_dialogues import DIALOGUE_PACKS

    return [*A1_PACKS, *EXTRA_PACKS, *DIALOGUE_PACKS]


def packs_for_level(level: str | None) -> list[dict]:
    lv = str(level or "A1").upper()
    if lv == "A0":
        lv = "A1"
    if lv in {"C1", "C2"}:
        lv = "B2"
    return [p for p in all_packs() if str(p.get("level") or "A1").upper() == lv]


def section_intro_html(level: str | None) -> str:
    lv = str(level or "A1").upper()
    if lv == "A0":
        lv = "A1"
    if lv in {"C1", "C2"}:
        lv = "B2"
    by_lv = {
        "A1": (
            "🤙 <b>Живая речь</b> · A1\n\n"
            "🦜 <b>Рико:</b> Учебник говорит по слогам. Люди — нет.\n\n"
            "🌀 <b>«Глотание слов»</b> · 1–3 — wanna, don'tcha, c'mon\n"
            "😎 <b>По-свойски</b> — yeah, nope, see ya\n"
            "🎧 <b>Диалоги</b> — пять сценок, потом вопросы голосом\n\n"
            "Слайд не копится в чате: старое голосовое уходит, карточка меняется."
        ),
        "A2": (
            "🤙 <b>Живая речь</b> · A2\n\n"
            "🦜 Планы, переписка, времена как говорят — и <b>пять диалогов</b> 🎧"
        ),
        "B1": (
            "🤙 <b>Живая речь</b> · B1\n\n"
            "🦜 Сериалы, чаты, already/yesterday — и <b>пять диалогов</b> 🎧"
        ),
        "B2": (
            "🤙 <b>Живая речь</b> · B2\n\n"
            "🦜 Интернет, регистр, времена native — и <b>пять диалогов</b> 🎧"
        ),
    }
    return by_lv.get(lv, by_lv["A1"])


def get_pack(pack_id: str) -> dict | None:
    for p in all_packs():
        if p["id"] == pack_id:
            return p
    return None


def pack_by_button_label(text: str, *, level: str | None = None) -> dict | None:
    raw = (text or "").strip()
    if raw.endswith(" ✅"):
        raw = raw[: -len(" ✅")].rstrip()
    pool = packs_for_level(level) if level else all_packs()
    for p in pool:
        if raw == p["title_ru"] or raw == f"{p['title_ru']} ✅":
            return p
    return None


def pack_button_label(pack: dict, *, done: bool) -> str:
    mark = " ✅" if done else ""
    return f"{pack['title_ru']}{mark}"


def listen_steps(pack: dict) -> list:
    if pack.get("kind") == "dialogue":
        return list(pack.get("lines") or [])
    return list(pack.get("items") or [])


def slide_count(pack: dict) -> int:
    return 1 + len(listen_steps(pack)) + len(pack.get("produce") or [])
