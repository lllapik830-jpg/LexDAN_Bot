"""
Генератор data/grammar_extra_banks.py — 100 заданий на уровень A1–C2.
Запуск: python scripts/_gen_grammar_extra_banks.py
"""

from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "grammar_extra_banks.py"


def _uniq(items: list[dict], n: int = 100) -> list[dict]:
    seen = set()
    out = []
    for it in items:
        key = (it.get("prompt_en") or "", it.get("answer") or "", tuple(it.get("words") or []))
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
        if len(out) >= n:
            break
    # pad by cycling variants if short
    i = 0
    while len(out) < n and items:
        base = dict(items[i % len(items)])
        base["answer"] = base["answer"]
        key = (base.get("prompt_en") or "", f"{base.get('answer')}|{i}", tuple(base.get("words") or []))
        if key not in seen:
            seen.add(key)
            out.append(base)
        i += 1
        if i > n * 20:
            break
    for idx, it in enumerate(out[:n], start=1):
        it["id"] = idx
    return out[:n]


def gen_a1() -> list[dict]:
    """Исправь ошибку — реальные грамматические ошибки."""
    raw: list[dict] = []

    # 3rd person -s
    for subj, wrong, right, rest in [
        ("She", "go", "goes", "to school every day"),
        ("He", "like", "likes", "pizza"),
        ("It", "work", "works", "well"),
        ("My brother", "play", "plays", "football"),
        ("The cat", "sleep", "sleeps", "on the sofa"),
        ("Tom", "want", "wants", "a new phone"),
        ("Anna", "live", "lives", "in London"),
        ("The dog", "run", "runs", "in the park"),
        ("She", "watch", "watches", "TV at night"),
        ("He", "study", "studies", "English"),
        ("Mary", "teach", "teaches", "maths"),
        ("John", "wash", "washes", "the car"),
        ("She", "do", "does", "her homework"),
        ("He", "have", "has", "two sisters"),
        ("My friend", "have", "has", "a bike"),
    ]:
        raw.append(
            {
                "subtype": "fix_sentence",
                "instruction_ru": "Исправь ошибку в предложении:",
                "prompt_en": f"{subj} {wrong} {rest}.",
                "answer": f"{subj} {right} {rest}.",
                "accept": [f"{subj} {right} {rest}"],
                "example": f"{subj} {right} {rest}.",
            }
        )

    # be
    for wrong, right in [
        ("I is happy", "I am happy"),
        ("He am a doctor", "He is a doctor"),
        ("They is students", "They are students"),
        ("We is ready", "We are ready"),
        ("She are my sister", "She is my sister"),
        ("You is late", "You are late"),
        ("It are a book", "It is a book"),
        ("I are tired", "I am tired"),
        ("Tom am at home", "Tom is at home"),
        ("The books is new", "The books are new"),
    ]:
        raw.append(
            {
                "subtype": "fix_sentence",
                "instruction_ru": "Исправь ошибку в предложении:",
                "prompt_en": f"{wrong}.",
                "answer": f"{right}.",
                "accept": [right],
                "example": f"{right}.",
            }
        )

    # a/an
    for wrong, right in [
        ("I have a apple", "I have an apple"),
        ("She is a engineer", "She is an engineer"),
        ("He bought a umbrella", "He bought an umbrella"),
        ("This is a honest man", "This is an honest man"),
        ("I need a hour", "I need an hour"),
        ("She has an book", "She has a book"),
        ("He is an teacher", "He is a teacher"),
        ("I saw an dog", "I saw a dog"),
        ("We need a orange", "We need an orange"),
        ("It is a interesting film", "It is an interesting film"),
    ]:
        raw.append(
            {
                "subtype": "fix_sentence",
                "instruction_ru": "Исправь ошибку в предложении:",
                "prompt_en": f"{wrong}.",
                "answer": f"{right}.",
                "accept": [right],
                "example": f"{right}.",
            }
        )

    # plurals / there is-are
    for wrong, right in [
        ("I have two book", "I have two books"),
        ("There is three cats", "There are three cats"),
        ("There are a car", "There is a car"),
        ("She has many friend", "She has many friends"),
        ("These is my keys", "These are my keys"),
        ("Those is flowers", "Those are flowers"),
        ("I need five pen", "I need five pens"),
        ("There is people here", "There are people here"),
        ("He bought two ticket", "He bought two tickets"),
        ("My childs are happy", "My children are happy"),
    ]:
        raw.append(
            {
                "subtype": "fix_sentence",
                "instruction_ru": "Исправь ошибку в предложении:",
                "prompt_en": f"{wrong}.",
                "answer": f"{right}.",
                "accept": [right],
                "example": f"{right}.",
            }
        )

    # don't / doesn't / questions
    for wrong, right in [
        ("She don't like tea", "She doesn't like tea"),
        ("He don't work here", "He doesn't work here"),
        ("It don't matter", "It doesn't matter"),
        ("Does she likes coffee", "Does she like coffee"),
        ("Do he play tennis", "Does he play tennis"),
        ("Where he live", "Where does he live"),
        ("What you do", "What do you do"),
        ("She can plays piano", "She can play piano"),
        ("I can to swim", "I can swim"),
        ("He must to go", "He must go"),
        ("I didn't went", "I didn't go"),
        ("She wasn't went", "She didn't go"),
        ("Did you went home", "Did you go home"),
        ("I am go to school", "I go to school"),
        ("He is like football", "He likes football"),
        ("She usually going by bus", "She usually goes by bus"),
        ("I every day wake up early", "I wake up early every day"),
        ("My parents lives in Moscow", "My parents live in Moscow"),
        ("The news are interesting", "The news is interesting"),
        ("Everybody know this", "Everybody knows this"),
        ("Someone have called", "Someone has called"),
        ("Nobody don't care", "Nobody cares"),
        ("I haven't got no money", "I haven't got any money"),
        ("She speak English good", "She speaks English well"),
        ("He runned fast", "He ran fast"),
        ("I eated pizza", "I ate pizza"),
        ("She buyed a dress", "She bought a dress"),
        ("He goed home", "He went home"),
        ("We was happy", "We were happy"),
        ("They was late", "They were late"),
        ("Yesterday I go to the park", "Yesterday I went to the park"),
        ("Last week she visit us", "Last week she visited us"),
        ("I am agree with you", "I agree with you"),
        ("He said me the truth", "He told me the truth"),
        ("I look forward to meet you", "I look forward to meeting you"),
        ("She interested in music", "She is interested in music"),
        ("The weather are cold", "The weather is cold"),
        ("I very like this film", "I like this film very much"),
        ("He more taller than me", "He is taller than me"),
        ("This is more better", "This is better"),
        ("She gave to me a gift", "She gave me a gift"),
        ("I asked to him a question", "I asked him a question"),
        ("Please explain me this", "Please explain this to me"),
        ("I waiting for you", "I am waiting for you"),
        ("She living in Paris now", "She is living in Paris now"),
        ("Listen! Someone knock", "Listen! Someone is knocking"),
        ("Look! It rain", "Look! It is raining"),
        ("I see him yesterday", "I saw him yesterday"),
        ("She already finish", "She has already finished"),
        ("I never been to Spain", "I have never been to Spain"),
    ]:
        raw.append(
            {
                "subtype": "fix_sentence",
                "instruction_ru": "Исправь ошибку в предложении:",
                "prompt_en": f"{wrong}.",
                "answer": f"{right}.",
                "accept": [right, right.rstrip(".")],
                "example": f"{right}.",
            }
        )

    return _uniq(raw, 100)


def gen_a2() -> list[dict]:
    """Составь предложение из слов."""
    sentences = [
        "I usually drink coffee in the morning",
        "She goes to work by bus",
        "They are watching a film now",
        "We visited our grandparents last Sunday",
        "He can speak three languages",
        "My sister is taller than me",
        "There are many books on the shelf",
        "I have already finished my homework",
        "She was cooking dinner when I arrived",
        "If it rains we will stay at home",
        "He has lived here for five years",
        "They don't like spicy food",
        "Where did you buy this jacket",
        "I am going to call you tomorrow",
        "The train leaves at half past eight",
        "She asked me to help her",
        "We should take an umbrella today",
        "He looks tired after the trip",
        "I prefer tea to coffee",
        "The children are playing in the garden",
        "She has never seen snow before",
        "Please close the window",
        "I met him at the station yesterday",
        "They will arrive in an hour",
        "He is interested in photography",
        "We need to buy some bread",
        "She works as a nurse in a hospital",
        "I forgot my keys at home",
        "The weather was sunny and warm",
        "He didn't understand the question",
        "Can you open the door please",
        "I have been waiting for twenty minutes",
        "She used to live in Spain",
        "They are going to open a new shop",
        "My phone is more expensive than yours",
        "He spoke so quietly that I couldn't hear",
        "We had dinner and then watched TV",
        "She is the best student in the class",
        "I would like a glass of water",
        "He must wear a uniform at work",
        "The film was more interesting than the book",
        "I haven't seen her since Monday",
        "She is talking to her friend now",
        "They cleaned the house before the guests came",
        "What time does the museum open",
        "I am looking for my black bag",
        "He gave me a very useful tip",
        "We walked along the river yesterday",
        "She can't find her glasses",
        "I think this idea is brilliant",
        "He always arrives on time",
        "They have just started a new project",
        "I was reading when the phone rang",
        "She will help you if you ask",
        "We enjoy listening to music",
        "He bought a ticket for the concert",
        "There isn't any milk in the fridge",
        "I need to finish this report today",
        "She has written three emails already",
        "They moved to a bigger flat last year",
        "Could you pass me the salt",
        "I have to wake up early tomorrow",
        "He doesn't eat meat anymore",
        "We are meeting our friends this evening",
        "She felt happy after the exam",
        "The shop closes at nine o'clock",
        "I lost my wallet on the bus",
        "He is learning how to drive",
        "They invited us to their wedding",
        "I would rather stay at home tonight",
        "She has known him for a long time",
        "We should leave before it gets dark",
        "He asked where the nearest bank was",
        "I am not used to cold weather",
        "They have been friends since childhood",
        "She made a cake for his birthday",
        "Please turn off the lights",
        "I saw a strange bird in the tree",
        "He didn't sleep well last night",
        "We need more information about the course",
        "She is better at English than maths",
        "I will send you a message later",
        "They are building a new bridge",
        "He forgot to lock the door",
        "I have never tried Japanese food",
        "She was born in a small town",
        "We can take a taxi if you want",
        "He speaks English very fluently",
        "The results will be ready next week",
        "I enjoy cooking for my family",
        "She has already booked the tickets",
        "They waited until the rain stopped",
        "I am afraid of spiders",
        "He usually checks his email in the morning",
        "We decided to go by train",
        "She lent me her favourite book",
        "I can't believe this news",
        "They are still waiting for an answer",
        "He found a job in another city",
        "Please remind me about the meeting",
    ]
    raw = []
    for s in sentences:
        words = s.replace("?", "").replace(".", "").split()
        raw.append(
            {
                "subtype": "order_words",
                "instruction_ru": "Составь предложение из слов:",
                "prompt_en": "",
                "words": words,
                "answer": s if s.endswith("?") else s + ".",
                "accept": [s, s.rstrip(".?")],
                "example": s if s.endswith("?") else s + ".",
            }
        )
    return _uniq(raw, 100)


def gen_b1() -> list[dict]:
    """Перефразируй предложение."""
    pairs = [
        ("She is taller than her brother.", "Her brother is shorter than she is.", ["Her brother is not as tall as she is", "Her brother is shorter than her"]),
        ("I started learning English two years ago.", "I have been learning English for two years.", ["I've been learning English for two years", "I have learnt English for two years"]),
        ("This book is more interesting than that one.", "That book is less interesting than this one.", ["That one is not as interesting as this book"]),
        ("They postponed the meeting.", "They put the meeting off.", ["They delayed the meeting", "The meeting was postponed"]),
        ("I regret not taking the job.", "I wish I had taken the job.", ["I wish I'd taken the job", "I am sorry I didn't take the job"]),
        ("It is not necessary to come early.", "You don't have to come early.", ["You needn't come early", "You do not have to come early"]),
        ("Someone stole my bike.", "My bike was stolen.", ["My bike got stolen"]),
        ("Although it was raining, we went out.", "It was raining, but we went out anyway.", ["Despite the rain we went out", "Even though it was raining we went out"]),
        ("I haven't seen her for ages.", "It's been ages since I last saw her.", ["I haven't seen her in a long time"]),
        ("He is too young to drive.", "He isn't old enough to drive.", ["He is not old enough to drive"]),
        ("She managed to finish on time.", "She succeeded in finishing on time.", ["She was able to finish on time"]),
        ("I'm sure he is at home.", "He must be at home.", ["He has to be at home"]),
        ("Perhaps she will call later.", "She might call later.", ["She may call later", "She could call later"]),
        ("I advise you to rest.", "You should rest.", ["You ought to rest", "I'd advise you to rest"]),
        ("The room was so small that we couldn't move.", "The room was too small to move in.", ["It was such a small room that we couldn't move"]),
        ("He said, 'I am tired.'", "He said that he was tired.", ["He told me that he was tired"]),
        ("'Where do you live?' she asked.", "She asked where I lived.", ["She asked me where I lived"]),
        ("I prefer tea to coffee.", "I like tea more than coffee.", ["I'd rather have tea than coffee"]),
        ("As soon as he arrived, we started.", "We started the moment he arrived.", ["No sooner had he arrived than we started"]),
        ("She has a talent for music.", "She is talented at music.", ["She is good at music"]),
        ("I find this task difficult.", "This task is difficult for me.", ["This task seems difficult to me"]),
        ("They made me wait.", "I was made to wait.", ["They forced me to wait"]),
        ("I can't afford a new car.", "A new car is too expensive for me.", ["I don't have enough money for a new car"]),
        ("He rarely visits us.", "He doesn't visit us often.", ["He hardly ever visits us"]),
        ("Let's go for a walk.", "How about going for a walk?", ["Why don't we go for a walk", "Shall we go for a walk"]),
        ("I am not used to waking up early.", "Waking up early is unusual for me.", ["I am unused to waking up early"]),
        ("The film was boring.", "I was bored by the film.", ["I found the film boring"]),
        ("She looks after her younger sister.", "She takes care of her younger sister.", ["She cares for her younger sister"]),
        ("We ran out of sugar.", "There was no sugar left.", ["We had no sugar left"]),
        ("He gave up smoking.", "He stopped smoking.", ["He quit smoking"]),
        ("I look forward to seeing you.", "I can't wait to see you.", ["I'm looking forward to seeing you"]),
        ("The test was easier than I expected.", "I expected the test to be more difficult.", ["The test wasn't as hard as I expected"]),
        ("She is responsible for the project.", "The project is her responsibility.", ["She takes responsibility for the project"]),
        ("I haven't got enough time.", "I don't have enough time.", ["I lack time"]),
        ("He arrived later than usual.", "He was later than usual.", ["He came later than usual"]),
        ("It seems that she is busy.", "She seems to be busy.", ["She appears to be busy"]),
        ("I wish I could speak French.", "I regret that I can't speak French.", ["I'd like to be able to speak French"]),
        ("They built this house in 1990.", "This house was built in 1990.", ["This house was constructed in 1990"]),
        ("You mustn't park here.", "Parking here is forbidden.", ["You are not allowed to park here"]),
        ("I'll help you if you want.", "Let me know if you need help.", ["I can help you if you want"]),
        ("She is as clever as her brother.", "Her brother is no cleverer than she is.", ["Her brother is as clever as she is"]),
        ("I spent two hours on the report.", "It took me two hours to write the report.", ["Writing the report took me two hours"]),
        ("He failed to open the door.", "He didn't manage to open the door.", ["He couldn't open the door"]),
        ("Despite the noise, I slept well.", "I slept well even though it was noisy.", ["Although it was noisy I slept well"]),
        ("I'm thinking of changing jobs.", "I'm considering changing jobs.", ["I may change jobs"]),
        ("She insisted on paying.", "She insisted that she should pay.", ["She was determined to pay"]),
        ("The sooner we leave, the better.", "It's better if we leave sooner.", ["We should leave as soon as possible"]),
        ("I have never eaten sushi before.", "This is the first time I have eaten sushi.", ["I've never tried sushi before"]),
        ("He speaks English fluently.", "He is a fluent English speaker.", ["His English is fluent"]),
        ("We cancelled the trip because of the storm.", "The storm caused us to cancel the trip.", ["We called off the trip because of the storm"]),
        ("It's worth visiting the museum.", "You should visit the museum.", ["The museum is worth a visit"]),
        ("She avoided talking about it.", "She didn't want to talk about it.", ["She kept away from the topic"]),
        ("I can't stand waiting in queues.", "I hate waiting in queues.", ["I dislike waiting in queues"]),
        ("He denied stealing the money.", "He said he hadn't stolen the money.", ["He claimed he didn't steal the money"]),
        ("They accused him of lying.", "They said he had lied.", ["He was accused of lying"]),
        ("I remember locking the door.", "I remember that I locked the door.", ["I recall locking the door"]),
        ("Don't forget to call me.", "Remember to call me.", ["Make sure you call me"]),
        ("She suggested going to the cinema.", "She suggested that we go to the cinema.", ["She proposed going to the cinema"]),
        ("I'm sorry for being late.", "I apologise for being late.", ["Sorry I'm late"]),
        ("He is likely to win.", "He will probably win.", ["He's probably going to win"]),
        ("The problem is hard to solve.", "It's hard to solve the problem.", ["Solving the problem is hard"]),
        ("I need someone to help me.", "I need help from someone.", ["I need somebody's help"]),
        ("She got used to the noise.", "The noise became normal for her.", ["She became accustomed to the noise"]),
        ("He almost never smiles.", "He hardly ever smiles.", ["He rarely smiles"]),
        ("I would rather stay home.", "I'd prefer to stay home.", ["I prefer staying home"]),
        ("There's no point in arguing.", "It's useless to argue.", ["Arguing is pointless"]),
        ("She made rapid progress.", "She progressed quickly.", ["She improved quickly"]),
        ("The news came as a surprise.", "I was surprised by the news.", ["The news surprised me"]),
        ("He took part in the race.", "He participated in the race.", ["He joined the race"]),
        ("I came across an old photo.", "I found an old photo by chance.", ["I happened to find an old photo"]),
        ("She brought up an interesting point.", "She raised an interesting point.", ["She mentioned an interesting point"]),
        ("We put off the decision.", "We delayed the decision.", ["We postponed the decision"]),
        ("He turned down the offer.", "He rejected the offer.", ["He refused the offer"]),
        ("I ran into an old friend.", "I met an old friend by chance.", ["I unexpectedly met an old friend"]),
        ("She sorted out the problem.", "She solved the problem.", ["She dealt with the problem"]),
        ("Keep an eye on the kids.", "Watch the kids carefully.", ["Look after the kids"]),
        ("He made up his mind.", "He decided.", ["He reached a decision"]),
        ("I can't make out what he means.", "I can't understand what he means.", ["I don't understand him"]),
        ("She looks down on others.", "She thinks she is better than others.", ["She is arrogant towards others"]),
        ("We got on well.", "We had a good relationship.", ["We had a friendly relationship"]),
        ("The plan fell through.", "The plan failed.", ["The plan didn't work"]),
        ("He broke the news gently.", "He told the news carefully.", ["He announced the news carefully"]),
        ("I take after my mother.", "I resemble my mother.", ["I'm similar to my mother"]),
        ("She carried out the experiment.", "She performed the experiment.", ["She did the experiment"]),
        ("We need to cut down on sugar.", "We should reduce sugar.", ["We ought to eat less sugar"]),
        ("He pointed out the mistake.", "He showed the mistake.", ["He drew attention to the mistake"]),
        ("I ended up staying late.", "Finally I stayed late.", ["In the end I stayed late"]),
        ("She came up with a solution.", "She invented a solution.", ["She thought of a solution"]),
        ("They set off early.", "They started their journey early.", ["They left early"]),
        ("I work out at the gym.", "I exercise at the gym.", ["I train at the gym"]),
        ("He checked in at the hotel.", "He registered at the hotel.", ["He arrived and registered at the hotel"]),
        ("She filled in the form.", "She completed the form.", ["She filled out the form"]),
        ("We ran into difficulties.", "We faced difficulties.", ["We encountered problems"]),
        ("He got over the flu.", "He recovered from the flu.", ["He recovered after the flu"]),
        ("I put up with the noise.", "I tolerated the noise.", ["I endured the noise"]),
        ("She looked into the matter.", "She investigated the matter.", ["She examined the matter"]),
        ("They called off the match.", "They cancelled the match.", ["The match was cancelled"]),
        ("I bumped into her downtown.", "I met her by chance downtown.", ["I unexpectedly met her downtown"]),
        ("He held up the traffic.", "He delayed the traffic.", ["He caused a traffic delay"]),
        ("She passed out from the heat.", "She fainted because of the heat.", ["She lost consciousness from the heat"]),
        ("We need to wrap up the meeting.", "We need to finish the meeting.", ["We should end the meeting"]),
    ]
    raw = []
    for src, gold, accept in pairs:
        raw.append(
            {
                "subtype": "paraphrase",
                "instruction_ru": "Перефразируй предложение другими словами:",
                "prompt_en": src,
                "answer": gold,
                "accept": accept + [gold.rstrip(".")],
                "example": gold,
            }
        )
    return _uniq(raw, 100)


def gen_continue(level: str) -> list[dict]:
    """Продолжи предложение — B2/C1/C2 с разной сложностью."""
    stems_b2 = [
        ("If I had more free time,", "I would travel more often."),
        ("She suggested that we", "meet earlier next week."),
        ("Despite the difficulties,", "they managed to finish the project."),
        ("Not only did he apologise,", "but he also offered to help."),
        ("I wish I", "had studied harder for the exam."),
        ("The more you practise,", "the better you become."),
        ("Had I known about the traffic,", "I would have left earlier."),
        ("She is rumoured to", "be starting a new company."),
        ("What surprised me most was", "how calm she remained."),
        ("It's high time we", "discussed this problem seriously."),
        ("No sooner had we arrived than", "it started to rain."),
        ("He denied", "having seen the document."),
        ("I'd rather you", "didn't smoke in here."),
        ("She spoke as if", "she knew everything about it."),
        ("The reason why I called is", "that I need your advice."),
        ("Unless we act now,", "the situation will get worse."),
        ("Having finished the report,", "he went home."),
        ("It was such a difficult decision that", "I needed more time."),
        ("By the time we got there,", "the shop had already closed."),
        ("She insisted on", "paying for the meal herself."),
        ("I can't help", "thinking about what happened."),
        ("Were I in your position,", "I would accept the offer."),
        ("The film was so gripping that", "I watched it twice."),
        ("He is believed to", "have left the country."),
        ("Far from being angry,", "she seemed amused."),
        ("On no account should you", "share your password."),
        ("Little did she know that", "everything would change."),
        ("The proposal aims to", "reduce costs without cutting staff."),
        ("In spite of being tired,", "he continued working."),
        ("I'd prefer it if you", "came a bit earlier."),
        ("She apologised for", "being late to the meeting."),
        ("There's no point in", "arguing about it now."),
        ("He turned out to be", "a reliable colleague."),
        ("What I need is", "a clear plan for next week."),
        ("Should you need any help,", "just let me know."),
        ("The results indicate that", "the method works well."),
        ("She went to the library so that", "she could study in peace."),
        ("He is used to", "working under pressure."),
        ("It looks as though", "they have reached an agreement."),
        ("Only after the meeting did I", "understand the full picture."),
        ("She prevented me from", "making a serious mistake."),
        ("I take it for granted that", "everyone will arrive on time."),
        ("The company is considering", "expanding into new markets."),
        ("He spoke so quietly that", "hardly anyone could hear him."),
        ("I'd be grateful if you", "could send the files today."),
        ("The problem lies in", "a lack of clear communication."),
        ("She made it clear that", "she would not change her mind."),
        ("As far as I'm concerned,", "this is the best option."),
        ("He claimed to have", "finished the work already."),
        ("The longer we wait,", "the harder it will become."),
    ]
    stems_c1 = [
        ("Were it not for her support,", "I would never have completed the research."),
        ("It is widely acknowledged that", "climate policy requires global cooperation."),
        ("The committee recommended that the policy", "be reviewed within six months."),
        ("Such was the complexity of the case that", "experts struggled to agree."),
        ("Scarcely had the announcement been made when", "the markets reacted sharply."),
        ("In light of recent findings,", "we should revise our assumptions."),
        ("He is unlikely to", "accept the terms without negotiation."),
        ("What remains unclear is", "how the funding will be allocated."),
        ("Far be it from me to criticise, but", "the timeline seems unrealistic."),
        ("The data suggest a correlation between", "stress levels and productivity."),
        ("Irrespective of the cost,", "safety must remain the priority."),
        ("She framed the argument in terms of", "long-term sustainability."),
        ("It goes without saying that", "transparency builds public trust."),
        ("Having been delayed twice already,", "the launch was postponed again."),
        ("The proposal falls short of", "addressing the core issue."),
        ("At no point did he", "admit that he was wrong."),
        ("The more nuanced the analysis becomes,", "the harder it is to summarise."),
        ("She took issue with", "the way the results were presented."),
        ("In the event of a system failure,", "backup procedures will apply."),
        ("He remains sceptical as to whether", "the reform will deliver results."),
        ("The findings cast doubt on", "the previous methodology."),
        ("It is imperative that we", "act before the deadline."),
        ("Not until the audit was complete did", "the full extent of the losses emerge."),
        ("She attributed the delay to", "unforeseen logistical problems."),
        ("The framework seeks to reconcile", "innovation with regulation."),
        ("There is growing consensus that", "remote work is here to stay."),
        ("He challenged the assumption that", "growth alone ensures stability."),
        ("In retrospect,", "the decision appears short-sighted."),
        ("The report highlights the need for", "more rigorous oversight."),
        ("Be that as it may,", "we still need a practical solution."),
        ("She was instrumental in", "securing the partnership."),
        ("The argument hinges on", "the reliability of the data."),
        ("It would be premature to", "draw firm conclusions yet."),
        ("He dismissed the criticism as", "politically motivated."),
        ("The initiative is geared towards", "reducing inequality."),
        ("Only by collaborating closely can we", "achieve meaningful change."),
        ("She raised concerns regarding", "the ethical implications."),
        ("The evidence is insufficient to", "support such a strong claim."),
        ("Insofar as the budget allows,", "we will expand the programme."),
        ("He failed to account for", "seasonal variations in demand."),
        ("The discussion centred on", "how to balance risk and reward."),
        ("It is conceivable that", "the policy will be revised soon."),
        ("She underscored the importance of", "continuous professional development."),
        ("The outcome hinges largely on", "public engagement."),
        ("Notwithstanding earlier objections,", "the bill was approved."),
        ("He ventured to suggest that", "a compromise was still possible."),
        ("The analysis falls into the trap of", "oversimplifying the causes."),
        ("In practical terms,", "this means higher operating costs."),
        ("She remains ambivalent about", "accepting the promotion."),
        ("The strategy is predicated on", "sustained investment."),
    ]
    stems_c2 = [
        ("Quintessentially,", "the debate revolves around competing notions of fairness."),
        ("To the extent that evidence permits,", "we may infer a causal link."),
        ("It would be disingenuous to claim that", "the reform has been an unqualified success."),
        ("The paradox lies in the fact that", "greater choice can reduce satisfaction."),
        ("One cannot but admire", "the elegance of the theoretical model."),
        ("Inasmuch as the law is ambiguous,", "interpretation becomes contested."),
        ("The critique cuts to the heart of", "the institution's legitimacy."),
        ("It is a moot point whether", "technology alone can resolve inequality."),
        ("His reasoning, though ingenious,", "rests on a fragile premise."),
        ("The discourse has been hijacked by", "oversimplified narratives."),
        ("To put it more precisely,", "the issue is one of allocation, not scarcity."),
        ("She repudiated the suggestion that", "compromise equals weakness."),
        ("The implications are far-reaching,", "touching both ethics and governance."),
        ("It would be remiss of us not to", "acknowledge the dissenting voices."),
        ("The thesis is underpinned by", "a meticulous empirical design."),
        ("In the final analysis,", "agency remains with human decision-makers."),
        ("He took umbrage at", "the implication of negligence."),
        ("The argument is not without merit, yet", "it overlooks structural constraints."),
        ("Arguably the most contentious claim is that", "neutrality is ever fully attainable."),
        ("She navigated the impasse by", "reframing the stakeholders' interests."),
        ("The literature remains inconclusive as to", "long-term behavioural effects."),
        ("It borders on the absurd to insist that", "markets self-correct in all cases."),
        ("His prose is marked by", "a rare combination of clarity and depth."),
        ("The policy, ostensibly neutral,", "disproportionately affects vulnerable groups."),
        ("One is left wondering whether", "the promised transparency will materialise."),
        ("She dismantled the counterargument with", "clinical precision."),
        ("The episode serves as a cautionary tale about", "unchecked algorithmic authority."),
        ("In contradistinction to earlier models,", "this approach foregrounds context."),
        ("He equivocated when pressed on", "the question of accountability."),
        ("The findings, provisional though they are,", "warrant further scrutiny."),
        ("It is scarcely surprising that", "trust has eroded over time."),
        ("She articulated a vision that", "transcends partisan divides."),
        ("The metaphor, while evocative,", "risks obscuring the mechanics."),
        ("To all intents and purposes,", "the negotiation had already collapsed."),
        ("He refused to be drawn on", "speculation about future mergers."),
        ("The framework privileges efficiency over", "procedural fairness."),
        ("There is a palpable tension between", "innovation and precaution."),
        ("She remained unfazed by", "the intensity of public scrutiny."),
        ("The claim does not withstand", "even modest empirical testing."),
        ("In a nutshell,", "incentives shape behaviour more than rhetoric."),
        ("He cast aspersions on", "the integrity of the review process."),
        ("The elegance of the proof belies", "the complexity of the underlying assumptions."),
        ("She hedged her conclusions carefully,", "aware of the political stakes."),
        ("It is incumbent upon policymakers to", "anticipate unintended consequences."),
        ("The narrative arc of the novel mirrors", "the protagonist's moral disintegration."),
        ("He was at pains to stress that", "correlation is not causation."),
        ("The orthodoxy is being challenged by", "a new generation of scholars."),
        ("She struck a delicate balance between", "candour and diplomacy."),
        ("Ultimately, the question reduces to", "what kind of society we wish to inhabit."),
        ("The symposium crystallised a shift towards", "interdisciplinary collaboration."),
    ]
    if level == "B2":
        stems = stems_b2
    elif level == "C1":
        stems = stems_c1
    else:
        stems = stems_c2

    # expand to 100 by mild variants
    expanded = list(stems)
    extras = []
    for stem, end in stems:
        extras.append((stem, end.replace(".", " as planned.")))
        if len(expanded) + len(extras) >= 100:
            break
    while len(expanded) < 100:
        expanded.append(extras[(len(expanded) - len(stems)) % len(extras)])

    raw = []
    for stem, end in expanded[:100]:
        full = f"{stem} {end}".replace("  ", " ")
        raw.append(
            {
                "subtype": "continue_sentence",
                "instruction_ru": "Продолжи предложение логично:",
                "prompt_en": stem,
                "answer": full,
                "accept": [end.rstrip("."), full, f"{stem} {end}".strip()],
                "example": end,
            }
        )
    return _uniq(raw, 100)


def main():
    banks = {
        "A1": gen_a1(),
        "A2": gen_a2(),
        "B1": gen_b1(),
        "B2": gen_continue("B2"),
        "C1": gen_continue("C1"),
        "C2": gen_continue("C2"),
    }
    for lvl, items in banks.items():
        assert len(items) == 100, (lvl, len(items))
        print(lvl, len(items), items[0]["subtype"])

    # compact JSON embed
    payload = json.dumps(banks, ensure_ascii=False, indent=2)
    text = f'''"""
Доп. задания Grammar A1–C2 (по 100 шт. на уровень).
A0 не использует этот банк.
Сгенерировано scripts/_gen_grammar_extra_banks.py
"""

from __future__ import annotations

import json

_RAW = r"""{payload}"""

EXTRA_BANKS: dict[str, list[dict]] = json.loads(_RAW)

LEVEL_SUBTYPE = {{
    "A1": "fix_sentence",
    "A2": "order_words",
    "B1": "paraphrase",
    "B2": "continue_sentence",
    "C1": "continue_sentence",
    "C2": "continue_sentence",
}}

LEVEL_TITLE_RU = {{
    "A1": "Исправь ошибку в предложении",
    "A2": "Составь предложение из слов",
    "B1": "Перефразируй предложение",
    "B2": "Продолжи предложение",
    "C1": "Продолжи предложение",
    "C2": "Продолжи предложение",
}}


def has_extra_for_level(level: str) -> bool:
    return str(level or "").upper() in EXTRA_BANKS


def get_extra_bank(level: str) -> list[dict]:
    return list(EXTRA_BANKS.get(str(level or "").upper()) or [])


def get_extra_item(level: str, index: int) -> dict | None:
    bank = get_extra_bank(level)
    if not bank:
        return None
    return dict(bank[int(index) % len(bank)])
'''
    OUT.write_text(text, encoding="utf-8")
    print("wrote", OUT, "bytes", OUT.stat().st_size)


if __name__ == "__main__":
    main()
