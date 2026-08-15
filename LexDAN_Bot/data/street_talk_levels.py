"""Паки Живой речи: A2 / B1 / B2. Слайды + голос."""

from __future__ import annotations

from data.street_talk import _WARN_CHAT, _item, _prod

_WARN_NET = (
    "понимать — да. Сыпать в каждое сообщение — нет. "
    "На работе и в письме — нейтральный английский."
)
_WARN_TENSE = (
    "носители в болтовне живут в simple. Сложные времена — когда правда нужны, "
    "не чтобы «звучать умно»."
)


def _pack(level: str, pid: str, title: str, intro: str, done: str, items: list, produce: list) -> dict:
    return {
        "id": pid,
        "level": level,
        "title_ru": title,
        "intro_html": intro,
        "done_html": done,
        "items": items,
        "produce": produce,
    }


# --- A2 ---

A2_PLANS = _pack(
    "A2",
    "a2_plans",
    "Планы с друзьями",
    (
        "🤙 <b>Планы с друзьями</b> · A2\n\n"
        "🦜 <b>Рико:</b> Не «Shall we convene?». Живые люди говорят "
        "<b>hang out</b>, <b>I'm down</b>, <b>catch up</b>.\n\n"
        "Слайды: форма → смысл → пример. Я озвучу, ты повторишь, потом свои планы голосом."
    ),
    "🏁 Планы закрыты. Теперь можно звать друга не как из учебника 🧃",
    [
        _item("hang out", "spend time together", "встречи с друзьями, чат.", "Wanna hang out later?"),
        _item("I'm down", "I'm in / I agree", "согласие пойти.", "I'm down. What time?", accept=["I'm down", "I am down"]),
        _item("catch up", "meet and talk / get news", "увидеться или нагнать новости.", "Let's catch up this week."),
        _item("maybe later", "not now, perhaps afterwards", "мягкий не-сейчас.", "Maybe later. I'm busy now."),
        _item("whatever", "as you like / I don't mind", "как хочешь — не всегда грубо.", "Whatever, you pick."),
        _item("for sure", "definitely", "уверенное «точно».", "For sure. I'll be there."),
    ],
    [
        _prod(["hang out"], "Позови друга <b>hang out</b> — когда и куда.", remind_html="hang out = потусить / провести время вместе."),
        _prod(["down", "I'm down", "I am down"], "Согласись: <b>I'm down</b> + во сколько.", remind_html="I'm down = я за, я в деле."),
        _prod(["catch up"], "Предложи <b>catch up</b> на этой неделе.", remind_html="catch up = увидеться и нагнать, что нового."),
        _prod(["maybe later", "for sure"], "Ответь <b>maybe later</b> или <b>for sure</b> на приглашение.", remind_html="maybe later = не сейчас. for sure = точно да."),
    ],
)

A2_CHAT = _pack(
    "A2",
    "a2_chat",
    "Переписка",
    (
        "💬 <b>Переписка</b> · A2\n\n"
        "🦜 Чаты не пишут «I do not know». Пишут <b>idk</b>, <b>tbh</b>, <b>brb</b>.\n"
        "Говорить это вслух тоже можно — как читается. Повтори и кинь свою реплику голосом."
    ),
    "🏁 Переписка пройдена. idk больше не иероглиф 📱",
    [
        _item("tbh", "to be honest", "чат и сторис.", "Tbh, I'm tired."),
        _item("ngl", "not gonna lie", "чат, чуть живее чем tbh.", "Ngl, that was good."),
        _item("idk", "I don't know", "чат и речь.", "Idk. Ask him."),
        _item("brb", "be right back", "чат, когда отошёл.", "Brb, two minutes."),
        _item("lol", "laughing / that's funny", "чат. Вслух почти не говорят.", "Lol that's crazy.", warn="в голосе лучше просто посмеяться. В чате lol — ок."),
        _item("omg", "oh my god", "чат и живая реакция.", "Omg I forgot."),
    ],
    [
        _prod(["tbh", "to be honest"], "Честно скажи через <b>tbh</b>.", remind_html="tbh = to be honest, если честно."),
        _prod(["idk", "I don't know", "don't know"], "Ответь <b>idk</b> + что не знаешь.", remind_html="idk = I don't know."),
        _prod(["omg", "oh my god"], "Удивись: <b>omg</b> + что случилось.", remind_html="omg = oh my god, вау/ужас/шок."),
    ],
)

A2_TENSES = _pack(
    "A2",
    "a2_tenses",
    "Времена как говорят",
    (
        "🕰 <b>Времена как говорят</b> · A2\n\n"
        "🦜 <b>Рико:</b> Носители почти не жонглируют двенадцатью временами. "
        "В болтовне три столпа:\n"
        "• <b>Present simple</b> — как живу, что делаю обычно\n"
        "• <b>Past simple</b> — что было вчера\n"
        "• <b>gonna / will</b> — что будет\n\n"
        "Present perfect на A2 почти не тащим. Сначала научись звучать просто и живо."
    ),
    "🏁 Три столпа на месте: сейчас / вчера / завтра. Perfect подождёт B1.",
    [
        _item(
            "I work / I go",
            "present simple — привычка",
            "рассказать, как устроена жизнь.",
            "I work from home.",
            warn=_WARN_TENSE,
            extra="💡 Не I am work. Просто I work / I go / I live.",
        ),
        _item(
            "I'm at…",
            "present — прямо сейчас (состояние)",
            "где ты, как себя чувствуешь.",
            "I'm at home.",
            warn=_WARN_TENSE,
        ),
        _item(
            "I went / I saw",
            "past simple — история",
            "вчера, на прошлой неделе, тогда.",
            "I went there yesterday.",
            warn=_WARN_TENSE,
            extra="💡 Носитель рассказывает день past simple, не present perfect.",
        ),
        _item(
            "I'm gonna",
            "going to — план",
            "что уже решил на вечер / выходные.",
            "I'm gonna stay in.",
            warn="с другом gonna. На собеседовании — I'm going to / I plan to.",
        ),
        _item(
            "I'll…",
            "will — решение сейчас / обещание",
            "быстрый ответ: ладно, сделаю.",
            "I'll text you.",
            warn=_WARN_TENSE,
            extra="💡 I'll — когда решил в момент речи. Gonna — план уже был.",
        ),
        _item(
            "Do you…? / Did you…?",
            "вопрос: сейчас vs вчера",
            "уточнить привычку или факт из прошлого.",
            "Did you see it?",
            warn=_WARN_TENSE,
        ),
        _item(
            "I didn't",
            "past simple отрицание",
            "не было / не сделал.",
            "I didn't go.",
            warn=_WARN_TENSE,
        ),
        _item(
            "What are you gonna do?",
            "вопрос про план",
            "вечер, выходные, после учёбы.",
            "What are you gonna do tonight?",
            warn="в учебнике What are you going to do? В жизни — gonna.",
        ),
    ],
    [
        _prod(
            ["I work", "I go", "I live", "I study", "I play"],
            "Скажи, что ты обычно делаешь — <b>present simple</b> (I work / I go / I live…).",
            remind_html="Present simple: I work, I go, I live. Без am/is с глаголом действия.",
        ),
        _prod(
            ["yesterday", "went", "saw", "did", "had"],
            "Коротко: что ты делал <b>вчера</b> — past simple.",
            remind_html="Вчера = past simple: I went, I saw, I did. Не I've gone yesterday.",
        ),
        _prod(
            ["gonna", "going to", "I'll", "I will"],
            "План на вечер: <b>I'm gonna</b> или быстрое <b>I'll</b>.",
            remind_html="gonna = план. I'll = решил сейчас / обещание.",
        ),
        _prod(
            ["Did you", "did you"],
            "Задай другу вопрос про вчера: <b>Did you…?</b>",
            remind_html="Did you…? — вопрос про прошлое. Do you…? — про обычно.",
        ),
    ],
)

# --- B1 ---

B1_SERIES = _pack(
    "B1",
    "b1_series",
    "Как в сериале",
    (
        "🎬 <b>Как в сериале</b> · B1\n\n"
        "🦜 Реакции, которые слышишь в каждом эпизоде. "
        "Не сюжет — рот: no way, come on, wait what."
    ),
    "🏁 Сериальные реакции в кармане. Не переигрывай ими в офисе 📺",
    [
        _item("no way", "I don't believe it / impossible", "шок, отказ поверить.", "No way. That's crazy."),
        _item("come on", "please / I don't believe you", "ну же / да ладно.", "Come on, it's easy."),
        _item("dude", "man / friend (informal)", "к своему, не к боссу.", "Dude, look at this.", warn=_WARN_CHAT),
        _item("seriously", "for real / are you kidding", "серьёзно? / без шуток.", "Seriously? He said that?"),
        _item("I guess", "I suppose", "мягкое «ну наверное».", "I guess we can wait."),
        _item("wait, what?", "I didn't catch that / shock", "переспрос + вау.", "Wait, what? Say that again."),
    ],
    [
        _prod(["no way"], "Удивись: <b>no way</b> + почему.", remind_html="no way = быть не может."),
        _prod(["come on"], "Подгони или не поверь: <b>come on</b>.", remind_html="come on = ну же / да ладно."),
        _prod(["I guess", "guess"], "Согласись неуверенно: <b>I guess</b> + что.", remind_html="I guess = ну, наверное."),
        _prod(["wait", "what"], "Переспроси: <b>wait, what?</b>", remind_html="wait, what? = стоп, что? не догнал / шок."),
    ],
)

B1_FEELS = _pack(
    "B1",
    "b1_feels",
    "Чаты и чувства",
    (
        "💛 <b>Чаты и чувства</b> · B1\n\n"
        "🦜 Как сказать «я в деле», «мне норм», «он пропал» без учебника."
    ),
    "🏁 Чувства в чате больше не через Google Translate.",
    [
        _item("lowkey", "kind of / secretly a bit", "чат и речь, смягчение.", "I lowkey want pizza.", warn=_WARN_NET),
        _item("ghost", "stop answering / disappear", "чат: пропал без слова.", "He ghosted me."),
        _item("I'm in", "I want to join", "согласие участвовать.", "I'm in. Let's go."),
        _item("that's fair", "that makes sense", "признать, что человек прав.", "That's fair. I get it."),
        _item("I'm good", "no thanks / I'm okay", "вежливый отказ или «я ок».", "I'm good, thanks."),
        _item("same", "me too", "короткое «тоже».", "Same. I feel that."),
    ],
    [
        _prod(["lowkey"], "Скажи желание через <b>lowkey</b>.", remind_html="lowkey = вроде / по-тихому / немного."),
        _prod(["I'm in", "I am in"], "Впиши себя: <b>I'm in</b> + куда.", remind_html="I'm in = я в деле."),
        _prod(["I'm good", "I am good"], "Откажись или скажи что ок: <b>I'm good</b>.", remind_html="I'm good = мне норм / не надо, спасибо."),
        _prod(["that's fair", "that is fair", "same"], "Ответь <b>that's fair</b> или <b>same</b>.", remind_html="that's fair = справедливо. same = тоже самое."),
    ],
)

B1_TENSES = _pack(
    "B1",
    "b1_tenses",
    "Времена: already / yesterday",
    (
        "🕰 <b>already / yesterday</b> · B1\n\n"
        "🦜 Носители по-прежнему живут в simple. "
        "Present perfect влезает точечно: <b>already, yet, just, never, ever</b>.\n\n"
        "История с датой — <b>past simple</b>: I went there last year. "
        "Не I've gone last year. Это частая ловушка."
    ),
    "🏁 Already и yesterday больше не путаются. Это уже B1-слух 🎯",
    [
        _item(
            "I've seen…",
            "present perfect — опыт",
            "без даты: в жизни / в этом году.",
            "I've seen that movie.",
            warn=_WARN_TENSE,
            extra="💡 Не I've seen it yesterday.",
        ),
        _item(
            "I've already…",
            "already — уже сделал",
            "еда, домашка, сообщение.",
            "I've already eaten.",
            warn=_WARN_TENSE,
        ),
        _item(
            "I just…",
            "just — только что",
            "речь: I just got home (часто past). Или I've just got home.",
            "I just got home.",
            warn=_WARN_TENSE,
            extra="💡 В американской речи just часто с past simple.",
        ),
        _item(
            "I went … yesterday",
            "past simple + дата",
            "вчера, last week, in 2020.",
            "I went there yesterday.",
            warn=_WARN_TENSE,
        ),
        _item(
            "Have you ever…?",
            "опыт — вопрос",
            "пробовал ли когда-нибудь.",
            "Have you ever been there?",
            warn=_WARN_TENSE,
        ),
        _item(
            "I've never…",
            "never — опыта нет",
            "честный ответ на ever.",
            "I've never tried it.",
            warn=_WARN_TENSE,
        ),
        _item(
            "I used to",
            "привычка в прошлом, сейчас нет",
            "жил, играл, ненавидел.",
            "I used to live there.",
            warn=_WARN_TENSE,
        ),
        _item(
            "Not yet",
            "yet — ещё нет",
            "короткий ответ.",
            "Not yet. Give me a minute.",
            warn=_WARN_TENSE,
        ),
    ],
    [
        _prod(
            ["already", "I've already", "I have already"],
            "Скажи, что ты <b>already</b> сделал сегодня.",
            remind_html="I've already + V3: I've already eaten. Уже сделано.",
        ),
        _prod(
            ["yesterday", "last", "went", "saw", "did"],
            "История с датой: <b>yesterday / last week</b> + past simple.",
            remind_html="Есть yesterday/last year — только past simple, не present perfect.",
        ),
        _prod(
            ["Have you ever", "have you ever", "I've never", "I have never"],
            "Спроси <b>Have you ever…?</b> или ответь <b>I've never…</b>",
            remind_html="ever/never = опыт за жизнь. Have you ever been…? I've never tried…",
        ),
        _prod(
            ["used to", "I used to"],
            "Что ты <b>used to</b> делать, а сейчас нет.",
            remind_html="used to = раньше делал, сейчас нет. I used to play football.",
        ),
    ],
)

# --- B2 ---

B2_NET = _pack(
    "B2",
    "b2_net",
    "Интернет, осторожно",
    (
        "📱 <b>Интернет, осторожно</b> · B2\n\n"
        "🦜 Чтобы понимать рилсы и чаты. "
        "Не чтобы стать мемом на собеседовании. У каждого слова — рамка."
    ),
    "🏁 Сленг понятен. Ты решаешь, когда его не говорить — это и есть уровень 👑",
    [
        _item("no cap", "no lie / for real", "чат, рилсы.", "No cap, that was good.", warn=_WARN_NET),
        _item("bet", "ok / it's a deal / I agree", "чат: ок, договорились.", "Bet. See you at 8.", warn=_WARN_NET),
        _item("slay", "do great / look great", "комплимент, очень неформально.", "You slayed that.", warn=_WARN_NET),
        _item("vibe", "mood / atmosphere", "атмосфера места или человека.", "I like the vibe here.", warn=_WARN_NET),
        _item("spill the tea", "tell the gossip", "сочные подробности с другом.", "Spill the tea. What happened?", warn=_WARN_NET),
        _item("for real", "seriously / truly", "универсальнее no cap.", "For real, I'm done.", warn=_WARN_NET),
    ],
    [
        _prod(["no cap", "for real"], "Подтверди всерьёз: <b>no cap</b> или <b>for real</b>.", remind_html="no cap / for real = без вранья, серьёзно. Не в письмо HR."),
        _prod(["bet"], "Согласись коротко: <b>bet</b> + когда.", remind_html="bet = ок, договорились."),
        _prod(["vibe"], "Оцени место: <b>vibe</b>.", remind_html="vibe = атмосфера / вайб."),
        _prod(["spill the tea", "tea"], "Попроси подробности: <b>spill the tea</b>.", remind_html="spill the tea = расскажи, что там за история."),
    ],
)

B2_REGISTER = _pack(
    "B2",
    "b2_register",
    "Где нельзя",
    (
        "⚖️ <b>Где нельзя</b> · B2\n\n"
        "🦜 Навык не «знать сленг», а <b>выключать</b> его. "
        "Друг / чат / HR / эссе — разные рты."
    ),
    "🏁 Регистр щёлкается. Это уже взрослый английский, не набор слов.",
    [
        _item("wanna → want to", "register switch", "друг vs собеседование.", "I want to join the team.", warn="wanna другу. want to — HR и эссе.", extra="💡 I wanna join your awesome team в cover letter = красный флаг."),
        _item("gonna → going to / I will", "register switch", "план другу vs письмо.", "I am going to start on Monday."),
        _item("kids → children / students", "register switch", "свой круг vs формальный текст.", "The children are already here."),
        _item("yeah → yes", "register switch", "голос другу vs встреча.", "Yes, I can do that."),
        _item("stuff → things / work", "register switch", "stuff — слишком размыто в отчёте.", "I finished the work."),
        _item("I gotta → I have to / I need to", "register switch", "пора бежать vs обязанность в письме.", "I have to leave at five."),
    ],
    [
        _prod(
            ["want to", "I want to", "I would like"],
            "Скажи желание <b>как на собеседовании</b> — без wanna.",
            remind_html="Друг: I wanna. HR: I want to / I'd like to.",
        ),
        _prod(
            ["have to", "I have to", "I need to"],
            "Обязанность нейтрально: <b>I have to</b> / <b>I need to</b> — не gotta.",
            remind_html="gotta — другу. have to / need to — работа.",
        ),
        _prod(
            ["Yes", "yes I"],
            "Короткий официальный ответ: начни с <b>Yes</b>, не yeah.",
            remind_html="yeah — свой. yes — встреча, учитель, клиент.",
        ),
    ],
)

B2_TENSES = _pack(
    "B2",
    "b2_tenses",
    "Времена native",
    (
        "🕰 <b>Времена native</b> · B2\n\n"
        "🦜 Три столпа никуда не делись. Добавляются оттенки:\n"
        "• <b>gonna</b> — план уже был\n"
        "• <b>I'll</b> — решил сейчас / обещание\n"
        "• <b>I'm meeting</b> — в календаре\n"
        "• <b>I was gonna</b> — собирался, но…\n"
        "• <b>I've been …</b> — тянется до сейчас\n\n"
        "История вчера — всё ещё past simple. Не надо пихать perfect для красоты."
    ),
    "🏁 Gonna / I'll / I've been — ты выбираешь оттенок, не зубришь таблицу.",
    [
        _item(
            "I'm gonna vs I'll",
            "план vs решение сейчас",
            "вечер с другом vs «ок, напишу».",
            "I'll get it. I'm gonna cook later.",
            warn=_WARN_TENSE,
            extra="💡 I'll get it — решил сейчас. I'm gonna cook — план.",
        ),
        _item(
            "I'm meeting…",
            "present continuous = договорённость",
            "время уже стоит в календаре.",
            "I'm meeting Jake at six.",
            warn=_WARN_TENSE,
        ),
        _item(
            "I saw vs I've seen",
            "дата vs опыт",
            "yesterday / last year vs this week / in my life.",
            "I saw him yesterday. I've seen him this week.",
            warn=_WARN_TENSE,
        ),
        _item(
            "I've been …",
            "present perfect continuous — тянется",
            "работа, ожидание, учёба до сейчас.",
            "I've been working all day.",
            warn=_WARN_TENSE,
        ),
        _item(
            "I was gonna",
            "собирался, но жизнь случилась",
            "извинение / смена плана.",
            "I was gonna call you.",
            warn=_WARN_TENSE,
        ),
        _item(
            "I would always / I used to",
            "привычка в прошлом",
            "used to — факт. would — живая картинка в истории.",
            "I used to run every morning.",
            warn=_WARN_TENSE,
        ),
        _item(
            "I've been meaning to…",
            "давно собираюсь и всё не…",
            "написать, позвонить, начать.",
            "I've been meaning to text you.",
            warn=_WARN_TENSE,
        ),
        _item(
            "It's been a while",
            "давно не виделись / не делали",
            "тёплое воссоединение.",
            "It's been a while. How are you?",
            warn=_WARN_TENSE,
        ),
    ],
    [
        _prod(
            ["gonna", "I'll", "I will", "I'm meeting", "I am meeting"],
            "Планы: одно <b>gonna</b> или <b>I'll</b>, и если есть встреча в календаре — <b>I'm meeting</b>.",
            remind_html="gonna = план. I'll = сейчас решил. I'm meeting = уже договорено.",
        ),
        _prod(
            ["yesterday", "last", "I've been", "I have been"],
            "Либо история с датой (past simple), либо <b>I've been … all day</b>.",
            remind_html="Дата → I went. Тянется до сейчас → I've been working.",
        ),
        _prod(
            ["I was gonna", "was gonna", "I've been meaning"],
            "Извинись за срыв плана: <b>I was gonna…</b> или <b>I've been meaning to…</b>",
            remind_html="I was gonna call you = собирался. I've been meaning to = давно собираюсь.",
        ),
        _prod(
            ["It's been a while", "It has been a while", "used to"],
            "Либо <b>It's been a while</b>, либо что ты <b>used to</b> делать.",
            remind_html="It's been a while = давно не… used to = раньше, сейчас нет.",
        ),
    ],
)

EXTRA_PACKS: list[dict] = [
    A2_PLANS,
    A2_CHAT,
    A2_TENSES,
    B1_SERIES,
    B1_FEELS,
    B1_TENSES,
    B2_NET,
    B2_REGISTER,
    B2_TENSES,
]
