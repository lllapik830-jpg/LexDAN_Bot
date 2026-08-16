"""Диалоги Живой речи: A1–B2. Слушаешь реплики → отвечаешь на вопросы голосом."""

from __future__ import annotations

from data.street_talk import _prod

# Cast: Ed (м) и Emmaline (ж). Рико в репликах персонажей нельзя.
VOICE_MALE = "dHd5gvgSOzSfduK4CvEg"
VOICE_FEMALE = "nDJIICjR9zfJExIFeSCN"
MALE_NAMES = {"mark", "jack", "oliver", "noah"}
VOICE_META = {
    "male": {"voice_id": VOICE_MALE, "accent": "American", "flag": "🇺🇸"},
    "female": {"voice_id": VOICE_FEMALE, "accent": "British", "flag": "🇬🇧"},
}


def speaker_meta(who: str) -> dict:
    key = (who or "").strip().lower()
    return VOICE_META["male" if key in MALE_NAMES else "female"]


def voice_id_for_who(who: str) -> str:
    return speaker_meta(who)["voice_id"]


def speaker_label(who: str, n: int | None = None) -> str:
    meta = speaker_meta(who)
    name = (who or "").strip() or "…"
    bit = f"{name} · {meta['accent']} {meta['flag']}".strip()
    if n:
        return f"{bit} {n}"
    return bit


def _line(who: str, text: str) -> dict:
    return {"who": who, "text": text}


def _q(prompt: str, must: list[str], answer: str, *, min_words: int = 1) -> dict:
    return _prod(
        must,
        prompt,
        min_words=min_words,
        remind_html=answer,
        as_question=True,
    )


def _dlg(
    level: str,
    n: int,
    title: str,
    who_a: str,
    who_b: str,
    slang: str,
    lines: list[dict],
    questions: list[dict],
) -> dict:
    return {
        "id": f"{level.lower()}_dlg_{n}",
        "level": level,
        "kind": "dialogue",
        "title_ru": f"🎧 Диалог {n} · {title}",
        "slang": slang,
        "intro_html": f"🧃 {slang}",
        "done_html": (
            f"🏁 Диалог «{title}» закрыт.\n\n"
            "🦜 Сценка осела. Можно следующий 🎧"
        ),
        "lines": lines,
        "produce": questions,
    }


# --- A1 ---

A1_D1 = _dlg(
    "A1",
    1,
    "Встреча в парке",
    "Марк",
    "Анна",
    "wanna, gonna, kinda, gotta, dunno, don'tcha, see ya, c'mon",
    [
        _line("Mark", "Hey Anna! How's it going?"),
        _line("Anna", "Hey Mark! Wanna sit down?"),
        _line("Mark", "Sure. I'm kinda tired today."),
        _line("Anna", "Yeah, me too. I dunno why."),
        _line("Mark", "Don'tcha wanna go for a walk?"),
        _line("Anna", "Maybe later. I gotta go home soon."),
        _line("Mark", "Okay, see ya. C'mon, I'll walk with you."),
    ],
    [
        _q("What does Mark want to do?", ["sit", "sit down"], "Sit down."),
        _q("How is Mark feeling?", ["tired", "kinda tired"], "He's kinda tired."),
        _q("What does Mark suggest doing?", ["walk", "for a walk"], "Going for a walk."),
        _q(
            "Why does Anna have to go home?",
            ["gotta", "has to", "go home"],
            "She's gotta go home soon.",
        ),
        _q("How does Mark say goodbye?", ["see ya", "see you"], "See ya."),
    ],
)

A1_D2 = _dlg(
    "A1",
    2,
    "В кафе",
    "Джек",
    "Эмма",
    "wanna, gonna, kinda, gotta, dunno, hafta, hasta",
    [
        _line("Jack", "You wanna get something to drink?"),
        _line("Emma", "Yeah, I'm kinda thirsty."),
        _line("Jack", "I'm gonna have a coffee."),
        _line("Emma", "Me too. But I dunno if they have decaf."),
        _line("Jack", "Don't worry, I'll ask."),
        _line("Emma", "Okay. I gotta get back to work soon."),
        _line("Jack", "We'll drink fast then."),
        _line("Emma", "Hafta. I'll pay. The shift hasta start soon."),
    ],
    [
        _q(
            "What is Jack suggesting?",
            ["drink", "something to drink"],
            "Getting something to drink.",
        ),
        _q("How is Emma feeling?", ["thirsty", "kinda thirsty"], "She's kinda thirsty."),
        _q("What is Jack going to order?", ["coffee"], "Coffee."),
        _q(
            "Why is Emma worried?",
            ["decaf", "don't know", "dunno"],
            "She doesn't know if they have decaf.",
        ),
        _q(
            "Why do they have to drink fast?",
            ["work", "gotta", "get back"],
            "Emma's gotta get back to work.",
        ),
    ],
)

A1_D3 = _dlg(
    "A1",
    3,
    "Планы на выходные",
    "София",
    "Оливер",
    "gonna, wanna, dunno, kinda, tryna",
    [
        _line("Sofia", "What are you gonna do this weekend?"),
        _line("Oliver", "I dunno yet. Maybe just chill."),
        _line("Sofia", "You wanna go to the beach?"),
        _line("Oliver", "That sounds nice. Is it gonna be warm?"),
        _line("Sofia", "I think so. Let's go on Saturday."),
        _line("Oliver", "Okay. I'm gonna pack some snacks."),
        _line("Sofia", "Great. I'll bring water."),
        _line("Oliver", "I'm tryna save money, but it's okay."),
    ],
    [
        _q(
            "What is Sofia asking about?",
            ["weekend", "plans"],
            "Oliver's weekend plans.",
        ),
        _q("What does Sofia suggest?", ["beach"], "Going to the beach."),
        _q(
            "What does Oliver ask about the weather?",
            ["warm", "gonna be warm"],
            "If it's gonna be warm.",
        ),
        _q("When are they going?", ["saturday"], "On Saturday."),
        _q(
            "What is Oliver trying to do?",
            ["save", "tryna", "trying to"],
            "He's tryna save money.",
        ),
    ],
)

A1_D4 = _dlg(
    "A1",
    4,
    "Новый телефон",
    "Марк",
    "Лена",
    "kinda, wanna, gotta, gonna, gimme, lemme, ok, cuz",
    [
        _line("Mark", "You got a new phone?"),
        _line("Lena", "Yeah, I kinda love it."),
        _line("Mark", "It looks cool. Is it expensive?"),
        _line("Lena", "A bit, but I gotta have a good camera, cuz I love photos."),
        _line("Mark", "You wanna take a photo now?"),
        _line("Lena", "Sure. Lemme take one of you."),
        _line("Mark", "OK. Smile!"),
        _line("Lena", "Done. Gimme your phone, I'll send it to you."),
        _line("Mark", "Thanks."),
    ],
    [
        _q("What is Mark asking about?", ["phone", "new phone"], "Lena's new phone."),
        _q(
            "How does Lena feel about her phone?",
            ["love", "kinda love"],
            "She kinda loves it.",
        ),
        _q(
            "Why did Lena buy it?",
            ["camera", "photos", "cuz", "because"],
            "She gotta have a good camera, cuz she loves photos.",
        ),
        _q("What does Mark suggest doing?", ["photo", "take a photo"], "Taking a photo."),
        _q(
            "What is Lena going to do?",
            ["photo", "lemme", "let me", "take one"],
            "She's gonna take a photo of Mark.",
        ),
    ],
)

A1_D5 = _dlg(
    "A1",
    5,
    "Новый сосед",
    "Ной",
    "Мила",
    "wanna, don'tcha, gonna, gotta, see ya, sure, whatcha",
    [
        _line("Noah", "Don'tcha wanna meet the new neighbor?"),
        _line("Mila", "Maybe later. I'm kinda busy now."),
        _line("Noah", "You're gonna miss him."),
        _line("Mila", "Is he nice?"),
        _line("Noah", "Yeah, he's pretty cool."),
        _line("Mila", "Okay. I'm gonna go say hi tomorrow."),
        _line("Noah", "Good. I'll come with you."),
        _line("Mila", "See ya then. Whatcha think?"),
    ],
    [
        _q(
            "What is Noah suggesting?",
            ["neighbor", "neighbour", "meet"],
            "Meeting the new neighbor.",
        ),
        _q("Why doesn't Mila want to go now?", ["busy", "kinda busy"], "She's kinda busy."),
        _q(
            "What does Noah say about the neighbor?",
            ["cool", "pretty cool"],
            "He's pretty cool.",
        ),
        _q("When is Mila going to meet him?", ["tomorrow"], "Tomorrow."),
        _q("Who is going to come with her?", ["noah"], "Noah."),
    ],
)

# --- A2 ---

A2_D1 = _dlg(
    "A2",
    1,
    "Что делаем в пятницу?",
    "Джек",
    "Эмма",
    "hang out, I'm down, for sure, idk, whatcha, gonna",
    [
        _line("Jack", "What are you gonna do on Friday?"),
        _line("Emma", "I dunno yet. Maybe just chill at home."),
        _line("Jack", "You wanna hang out?"),
        _line("Emma", "With who?"),
        _line("Jack", "Me and some friends. We're gonna grab pizza."),
        _line("Emma", "I'm down. What time?"),
        _line("Jack", "Around 7. For sure."),
        _line("Emma", "Cool. Whatcha gonna do before that?"),
        _line("Jack", "Idk. Probably work."),
    ],
    [
        _q(
            "What is Jack asking about?",
            ["friday", "plans"],
            "Emma's Friday plans.",
        ),
        _q("What does Jack suggest doing?", ["hang out", "hangout"], "Hanging out."),
        _q("What are they gonna eat?", ["pizza"], "Pizza."),
        _q("Is Emma interested?", ["down", "yes", "interested"], "Yes, she's down."),
        _q("What time are they meeting?", ["7", "seven", "around 7"], "Around 7."),
    ],
)

A2_D2 = _dlg(
    "A2",
    2,
    "Переписка с подругой",
    "София",
    "Лена",
    "tbh, ngl, idk, brb, lol, omg, gonna, kinda, wanna",
    [
        _line("Sofia", "Omg, did you see the new series?"),
        _line("Lena", "Not yet. Is it good?"),
        _line("Sofia", "Tbh, I'm kinda obsessed."),
        _line("Lena", "Ngl, I've been busy, but I wanna watch it."),
        _line("Sofia", "You should. It's so good, lol."),
        _line("Lena", "Okay, I'll start tonight. Brb, I'm gonna get snacks."),
        _line("Sofia", "Idk if I can finish it tonight."),
        _line("Lena", "Me neither. We'll see."),
    ],
    [
        _q("What is Sofia talking about?", ["series", "show"], "A new series."),
        _q(
            "How does Sofia feel about it?",
            ["obsessed", "kinda obsessed"],
            "She's kinda obsessed.",
        ),
        _q("What does Lena want to do?", ["watch"], "Watch it."),
        _q(
            "Why is Lena going to be right back?",
            ["snacks", "brb"],
            "To get snacks.",
        ),
        _q(
            "Does Sofia think she'll finish it tonight?",
            ["idk", "don't know", "does not know", "no"],
            "She says idk.",
        ),
    ],
)

A2_D3 = _dlg(
    "A2",
    3,
    "Встречаемся или нет?",
    "Марк",
    "Анна",
    "maybe later, whatever, catch up, for sure, gonna, wanna, dunno",
    [
        _line("Mark", "You wanna catch up this weekend?"),
        _line("Anna", "Maybe later. I'm kinda busy now."),
        _line("Mark", "Whatever. Just tell me when."),
        _line("Anna", "I dunno yet. Maybe Sunday?"),
        _line("Mark", "For sure. What are you gonna do?"),
        _line("Anna", "I'm gonna clean my place."),
        _line("Mark", "I can help. If you want."),
        _line("Anna", "That'd be cool. Thanks."),
    ],
    [
        _q("What does Mark suggest?", ["catch up", "catchup"], "Catching up."),
        _q("Why does Anna say maybe later?", ["busy"], "She's busy."),
        _q("When might they meet?", ["sunday"], "On Sunday."),
        _q("What is Anna gonna do?", ["clean"], "Clean her place."),
        _q("Is Mark going to help?", ["yes", "help", "offers"], "Yes, he offers."),
    ],
)

A2_D4 = _dlg(
    "A2",
    4,
    "Как прошёл твой день?",
    "Оливер",
    "Мила",
    "I'm at…, I went / I saw, I'm gonna, I'll…, Did you…?, idk, wanna, gonna",
    [
        _line("Oliver", "How was your day?"),
        _line("Mila", "Good. I went to the gym."),
        _line("Oliver", "Nice. I'm at work rn."),
        _line("Mila", "Did you see the new movie?"),
        _line("Oliver", "Not yet. I'm gonna watch it this weekend."),
        _line("Mila", "I'll go with you if you want."),
        _line("Oliver", "For sure. That'd be cool."),
        _line("Mila", "What time are you gonna go?"),
        _line("Oliver", "Idk yet. I'll let you know."),
    ],
    [
        _q("What did Mila do today?", ["gym"], "She went to the gym."),
        _q("Where is Oliver right now?", ["work", "at work"], "He's at work."),
        _q(
            "What is Oliver gonna do this weekend?",
            ["movie", "watch"],
            "Watch the new movie.",
        ),
        _q("Who is going to go with him?", ["mila"], "Mila."),
        _q(
            "Does Oliver know what time he's going?",
            ["idk", "don't know", "no", "not yet"],
            "No, he says idk yet.",
        ),
    ],
)

A2_D5 = _dlg(
    "A2",
    5,
    "Планы на выходные",
    "Ной",
    "Зоя",
    "What are you gonna do?, I didn't…, I'm gonna, Do you…?, for sure, gonna, gotta, wanna, lemme, kinda, I'm down",
    [
        _line("Noah", "What are you gonna do this weekend?"),
        _line("Zoe", "I didn't think about it yet. Maybe rest."),
        _line("Noah", "You wanna go to the beach?"),
        _line("Zoe", "I'm down. Is it gonna be warm?"),
        _line("Noah", "For sure. I'm gonna check the weather."),
        _line("Zoe", "Cool. Lemme know."),
        _line("Noah", "Do you wanna invite anyone else?"),
        _line("Zoe", "I'm kinda tired of people. Let's just go."),
        _line("Noah", "I gotta say, that sounds perfect."),
    ],
    [
        _q(
            "What is Noah asking Zoe about?",
            ["weekend", "plans"],
            "Her weekend plans.",
        ),
        _q("What does Noah suggest doing?", ["beach"], "Going to the beach."),
        _q("Is Zoe interested?", ["down", "yes"], "Yes, she's down."),
        _q("What is Noah going to check?", ["weather"], "The weather."),
        _q(
            "What does Noah say about Zoe's suggestion?",
            ["perfect"],
            "It sounds perfect.",
        ),
    ],
)

# --- B1 ---

B1_D1 = _dlg(
    "B1",
    1,
    "Сюрприз",
    "Джек",
    "Эмма",
    "no way, come on, dude, seriously, I guess, wait, what?, wanna, gonna, I'm at…",
    [
        _line("Jack", "Dude, you won't believe what happened."),
        _line("Emma", "What? What happened?"),
        _line("Jack", "I got the job!"),
        _line("Emma", "No way! Seriously?"),
        _line("Jack", "Yeah! I can't believe it."),
        _line("Emma", "Wait, what? I thought you didn't apply."),
        _line("Jack", "I guess I did. I'm at the office now."),
        _line("Emma", "Come on! That's amazing."),
        _line("Jack", "I know, right? We're gonna celebrate!"),
    ],
    [
        _q("What is Jack excited about?", ["job"], "He got the job."),
        _q(
            "What is Emma's reaction?",
            ["no way", "seriously"],
            "She says «no way» and «seriously».",
        ),
        _q(
            "What did Emma think?",
            ["didn't apply", "did not apply", "apply"],
            "She thought he didn't apply.",
        ),
        _q("Where is Jack now?", ["office"], "He's at the office."),
        _q("What are they gonna do?", ["celebrate"], "Celebrate."),
    ],
)

B1_D2 = _dlg(
    "B1",
    2,
    "Чаты и чувства",
    "София",
    "Лена",
    "lowkey, ghost, I'm in, that's fair, I'm good, same, idk, ngl, gonna",
    [
        _line("Sofia", "Have you talked to Mark lately?"),
        _line("Lena", "No, he ghosted me like two weeks ago."),
        _line("Sofia", "That's lowkey rude."),
        _line("Lena", "I guess. But I'm good."),
        _line("Sofia", "That's fair. Ngl, I'm in the same situation."),
        _line("Lena", "We should just forget about them."),
        _line("Sofia", "I'm in. Let's go out tonight."),
        _line("Lena", "Same. I'm gonna call you later."),
    ],
    [
        _q(
            "What happened between Lena and Mark?",
            ["ghost", "ghosted"],
            "He ghosted her.",
        ),
        _q(
            "How does Sofia describe Mark's behavior?",
            ["lowkey", "rude"],
            "Lowkey rude.",
        ),
        _q("How does Lena feel about it?", ["good", "I'm good", "i am good"], "She's good."),
        _q(
            "What is Sofia's situation?",
            ["same"],
            "She's in the same situation.",
        ),
        _q("What are they going to do?", ["go out", "tonight"], "Go out tonight."),
    ],
)

B1_D3 = _dlg(
    "B1",
    3,
    "Уже видел?",
    "Марк",
    "Анна",
    "already, yesterday, Have you ever…?, I've never…, I've already…, I just…, gonna, gotta, I'm at…",
    [
        _line("Mark", "Have you ever watched this series?"),
        _line("Anna", "I've already seen it. Last year."),
        _line("Mark", "Really? I just started it yesterday."),
        _line("Anna", "It's really good. I've never seen anything like it."),
        _line("Mark", "I'm at episode 3 right now."),
        _line("Anna", "You're gonna love the ending."),
        _line("Mark", "I gotta finish it this week."),
        _line("Anna", "I'll join you if you want."),
        _line("Mark", "I'm down."),
    ],
    [
        _q(
            "Has Anna seen the series?",
            ["already", "yes", "seen"],
            "Yes, she's already seen it.",
        ),
        _q("When did Mark start watching it?", ["yesterday"], "Yesterday."),
        _q(
            "What does Anna say about the series?",
            ["never", "anything like"],
            "She's never seen anything like it.",
        ),
        _q("What episode is Mark on?", ["3", "three", "episode 3"], "Episode 3."),
        _q(
            "What are they going to do?",
            ["watch", "join", "together", "down"],
            "Watch the rest together.",
        ),
    ],
)

B1_D4 = _dlg(
    "B1",
    4,
    "Планы и мысли",
    "Оливер",
    "Мила",
    "I've never…, I used to, Not yet, wanna, gonna, gotta, Don'tcha, tbh, idk",
    [
        _line("Oliver", "Have you ever been to Italy?"),
        _line("Mila", "I've never been. Not yet."),
        _line("Oliver", "I used to go there every summer with my family."),
        _line("Mila", "That sounds amazing."),
        _line("Oliver", "You wanna go together next year?"),
        _line("Mila", "Tbh, I'm not sure. I gotta save money."),
        _line("Oliver", "Don'tcha wanna try at least once?"),
        _line("Mila", "Idk. Maybe later."),
        _line("Oliver", "For sure. Just let me know."),
    ],
    [
        _q(
            "Has Mila ever been to Italy?",
            ["never", "no", "not yet"],
            "No, she's never been.",
        ),
        _q(
            "What did Oliver use to do?",
            ["italy", "summer", "used to"],
            "Go to Italy every summer.",
        ),
        _q(
            "What does Oliver suggest?",
            ["together", "next year", "go"],
            "Going together next year.",
        ),
        _q(
            "Why is Mila not sure?",
            ["save", "money", "gotta"],
            "She's gotta save money.",
        ),
        _q(
            "What does Oliver say to her?",
            ["don'tcha", "don't you", "try"],
            "Don'tcha wanna try at least once?",
        ),
    ],
)

B1_D5 = _dlg(
    "B1",
    5,
    "Встреча с другом",
    "Ной",
    "Зоя",
    "I just…, I've already…, Have you ever…?, I'm good, same, gonna, kinda, lemme, c'mon, I'm down",
    [
        _line("Noah", "I just saw the new movie."),
        _line("Zoe", "Really? I've already seen it."),
        _line("Noah", "Have you ever watched something twice?"),
        _line("Zoe", "I'm good. Once is enough."),
        _line("Noah", "Same. But this one is really good."),
        _line("Zoe", "I'm down to watch it again if you want."),
        _line("Noah", "Lemme check if I have time."),
        _line("Zoe", "C'mon, you know you wanna."),
        _line("Noah", "I'll let you know."),
    ],
    [
        _q("What did Noah just see?", ["movie"], "The new movie."),
        _q(
            "Has Zoe seen it?",
            ["already", "yes", "seen"],
            "Yes, she's already seen it.",
        ),
        _q(
            "Does Zoe like watching things twice?",
            ["once", "enough", "no", "good"],
            "No, she's good with once.",
        ),
        _q("Is Zoe willing to watch it again?", ["down", "yes"], "Yes, she's down."),
        _q(
            "What does Zoe say to convince Noah?",
            ["c'mon", "come on", "cmon", "wanna"],
            "C'mon, you know you wanna.",
        ),
    ],
)

# --- B2 ---

B2_D1 = _dlg(
    "B2",
    1,
    "Сплетни и планы",
    "Джек",
    "Эмма",
    "spill the tea, no cap, for real, I'm gonna vs I'll, I've been meaning to…, It's been a while, gotta, lemme, kinda",
    [
        _line("Jack", "Have you heard about Mark and Sofia?"),
        _line("Emma", "No, spill the tea."),
        _line("Jack", "They broke up."),
        _line("Emma", "No cap? For real?"),
        _line("Jack", "Yeah. It's been a while since I talked to him."),
        _line("Emma", "I've been meaning to call him too."),
        _line("Jack", "I'm gonna call him tonight."),
        _line("Emma", "I'll join you if you want."),
        _line("Jack", "Lemme check my plans first."),
    ],
    [
        _q(
            "What is Jack talking about?",
            ["broke up", "break up", "mark and sofia"],
            "Mark and Sofia broke up.",
        ),
        _q(
            "What is Emma's reaction?",
            ["no cap", "for real"],
            "She says «no cap» and «for real».",
        ),
        _q(
            "How long has it been since Jack talked to Mark?",
            ["a while", "while"],
            "It's been a while.",
        ),
        _q(
            "What has Emma been meaning to do?",
            ["call"],
            "Call Mark.",
        ),
        _q("When is Jack gonna call Mark?", ["tonight"], "Tonight."),
    ],
)

B2_D2 = _dlg(
    "B2",
    2,
    "Онлайн-покупки",
    "София",
    "Лена",
    "bet, slay, vibe, for real, gonna, wanna, stuff, kids, yeah, I'm at…",
    [
        _line("Sofia", "I just bought a new bag online."),
        _line("Lena", "Bet. Show me."),
        _line("Sofia", "Here. Isn't it slay?"),
        _line("Lena", "For real. It's a vibe."),
        _line("Sofia", "I'm gonna wear it to the party."),
        _line("Lena", "I wanna get one too. Where did you get it?"),
        _line("Sofia", "That online store. They have a lot of stuff."),
        _line("Lena", "Yeah, I'll check it out later."),
    ],
    [
        _q("What did Sofia just buy?", ["bag"], "A new bag."),
        _q(
            "What is Lena's reaction?",
            ["bet", "slay", "vibe"],
            "She says «bet» and «slay».",
        ),
        _q("When is Sofia gonna wear it?", ["party"], "To the party."),
        _q("What does Lena wanna do?", ["get one", "get a", "buy"], "Get one too."),
        _q(
            "Where did Sofia get it?",
            ["online", "store"],
            "At an online store.",
        ),
    ],
)

B2_D3 = _dlg(
    "B2",
    3,
    "Занят или нет",
    "Марк",
    "Анна",
    "I'm meeting…, I saw vs I've seen, I've been…, I was gonna, I would always, gotta, wanna, for sure, whatcha",
    [
        _line("Mark", "Are you free tonight?"),
        _line("Anna", "I'm meeting some friends actually."),
        _line("Mark", "I saw you at the café yesterday."),
        _line("Anna", "Oh, I've been there a lot lately."),
        _line("Mark", "I was gonna go, but I got busy."),
        _line("Anna", "I would always go there after work."),
        _line("Mark", "You wanna grab coffee later this week?"),
        _line("Anna", "For sure. Whatcha thinking?"),
        _line("Mark", "I gotta check my schedule first."),
    ],
    [
        _q(
            "Is Anna free tonight?",
            ["no", "meeting", "friends"],
            "No, she's meeting friends.",
        ),
        _q("Where did Mark see Anna yesterday?", ["cafe", "café"], "At the café."),
        _q(
            "What was Mark gonna do?",
            ["cafe", "café", "busy", "gonna go"],
            "Go to the café, but he got busy.",
        ),
        _q(
            "What would Anna always do after work?",
            ["cafe", "café", "go there"],
            "Go to the café.",
        ),
        _q(
            "When are they gonna grab coffee?",
            ["later this week", "this week", "later"],
            "Later this week.",
        ),
    ],
)

B2_D4 = _dlg(
    "B2",
    4,
    "Давно не виделись",
    "Оливер",
    "Мила",
    "I've been meaning to…, It's been a while, I used to, I've been…, gonna, wanna, I'll…",
    [
        _line("Oliver", "It's been a while since we talked."),
        _line("Mila", "I know. I've been meaning to call you."),
        _line("Oliver", "I've been so busy with work."),
        _line("Mila", "Same. I used to have more free time."),
        _line("Oliver", "You wanna grab a drink this weekend?"),
        _line("Mila", "I'm gonna try to free up Saturday."),
        _line("Oliver", "I'll text you later this week."),
        _line("Mila", "Please do. I miss our talks."),
        _line("Oliver", "Me too."),
    ],
    [
        _q(
            "How long has it been since they talked?",
            ["a while", "while"],
            "It's been a while.",
        ),
        _q(
            "What has Mila been meaning to do?",
            ["call"],
            "Call Oliver.",
        ),
        _q("What has Oliver been busy with?", ["work"], "Work."),
        _q("What did Mila use to have?", ["free time", "time"], "More free time."),
        _q(
            "What are they gonna try to do this weekend?",
            ["drink", "saturday"],
            "Grab a drink.",
        ),
    ],
)

B2_D5 = _dlg(
    "B2",
    5,
    "Планы и намерения",
    "Ной",
    "Зоя",
    "I'm gonna vs I'll, I've been…, I was gonna, I would always, for real, bet, gotta, wanna, stuff, yeah",
    [
        _line("Noah", "I'm gonna go to the gym tonight. Wanna join?"),
        _line("Zoe", "I was gonna go earlier, but I got stuck."),
        _line("Noah", "It's fine. I would always go after work."),
        _line("Zoe", "I've been too lazy lately. For real."),
        _line("Noah", "That's okay. I'll pick you up if you want."),
        _line("Zoe", "Bet. What time?"),
        _line("Noah", "I gotta finish some stuff first."),
        _line("Zoe", "Yeah, I'll wait."),
        _line("Noah", "I'll text you when I'm ready."),
    ],
    [
        _q("What is Noah gonna do tonight?", ["gym"], "Go to the gym."),
        _q(
            "What was Zoe gonna do?",
            ["earlier", "stuck", "gonna go"],
            "Go earlier, but she got stuck.",
        ),
        _q(
            "What would Noah always do?",
            ["after work", "gym", "work"],
            "Go to the gym after work.",
        ),
        _q("How has Zoe been lately?", ["lazy"], "Too lazy."),
        _q("What is Noah gonna do for her?", ["pick", "pick you up"], "Pick her up."),
    ],
)

DIALOGUE_PACKS: list[dict] = [
    A1_D1,
    A1_D2,
    A1_D3,
    A1_D4,
    A1_D5,
    A2_D1,
    A2_D2,
    A2_D3,
    A2_D4,
    A2_D5,
    B1_D1,
    B1_D2,
    B1_D3,
    B1_D4,
    B1_D5,
    B2_D1,
    B2_D2,
    B2_D3,
    B2_D4,
    B2_D5,
]
