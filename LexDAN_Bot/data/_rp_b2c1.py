# -*- coding: utf-8 -*-
"""Curated Reading packs for B2 and C1 — unique on-topic narratives."""

PACKS = {
    "B2": {
        "business": {
            "full_text": (
                "Elena led Thursday's client call from the Berlin office while two colleagues joined by "
                "remote work from Lisbon. The proposal for a logistics dashboard had to reach the client "
                "before Friday's deadline, so she opened with the delivery timeline and risk list. "
                "Two clients asked for clearer pricing and a pilot week in March. Elena noted every "
                "objection in the shared sheet and assigned owners for each follow-up. After the call she "
                "rewrote the executive summary, cut three weak slides, and sent the revised deck by "
                "six. The team agreed that working from afar saved travel time, yet the Friday cutoff still required "
                "one late evening. By Friday noon the client approved the pilot week and asked for a signed "
                "statement of work next week."
            ),
            "gapped_text": (
                "Elena led Thursday's client call from the Berlin office while two colleagues joined by "
                "(1)___ from Lisbon. The document for a logistics dashboard had to reach the client "
                "before Friday's (2)___, so she opened with the delivery timeline and risk list. "
                "Two (3)___ asked for clearer pricing and a trial week in March. Elena noted every "
                "objection in the shared sheet and assigned owners for each follow-up. After the call she "
                "rewrote the executive summary, cut three weak slides, and sent the revised (4)___ by "
                "six. The team agreed that working from afar saved travel time, yet the Friday cutoff still required "
                "one late evening. By Friday noon the client approved the (5)___ week and asked for a signed "
                "statement of work next week."
            ),
            "answers": ["remote work", "deadline", "clients", "proposal", "pilot"],
            "word_bank": ["remote work", "deadline", "clients", "proposal", "pilot", "invoice"],
            "questions": [
                {
                    "q": "Where were Elena's two colleagues during the call?",
                    "accept": ["Lisbon", "in Lisbon", "remote from Lisbon"],
                    "hint_ru": "Откуда подключались коллеги?",
                    "quote": "…joined by remote work from Lisbon.",
                    "model_en": "They joined by remote work from Lisbon.",
                },
                {
                    "q": "When did the proposal have to reach the client?",
                    "accept": ["before Friday's deadline", "Friday", "before Friday"],
                    "hint_ru": "К какому сроку нужен был proposal?",
                    "quote": "…before Friday's deadline…",
                    "model_en": "It had to reach the client before Friday's deadline.",
                },
                {
                    "q": "What did the clients ask for besides clearer pricing?",
                    "accept": ["a pilot week in March", "pilot week", "March", "a trial week in March"],
                    "hint_ru": "Что ещё попросили клиенты?",
                    "quote": "…a pilot week in March.",
                    "model_en": "They asked for a pilot week in March.",
                },
                {
                    "q": "What did the client approve by Friday noon?",
                    "accept": ["the pilot", "pilot", "approved the pilot", "the pilot week", "pilot week"],
                    "hint_ru": "Что одобрил клиент?",
                    "quote": "…the client approved the pilot week…",
                    "model_en": "The client approved the pilot week.",
                },
            ],
            "plan": [
                "Client call setup and remote colleagues",
                "Deadline pressure and client requests",
                "Rewriting and sending the proposal",
                "Pilot approval and next step",
            ],
            "facts": [
                "Elena led the call from Berlin; colleagues joined from Lisbon.",
                "The proposal had to arrive before Friday's deadline.",
                "Clients wanted clearer pricing and a March pilot week.",
                "By Friday noon the client approved the pilot week.",
            ],
        },
        "startup": {
            "full_text": (
                "Maya's team spent Monday refining a meal-planning product for busy parents. Early users "
                "liked the shopping list, but churn rose after week two, so the founders tracked which "
                "screens people abandoned. For the investor pitch they kept one clear problem slide and "
                "a demo of the weekly menu builder. Funding talks with a seed fund hinged on proving "
                "repeat orders, not vanity downloads. Maya cut the feature list, added a short onboarding "
                "quiz, and invited twenty unpaid testers to a feedback call. After that presentation the partners "
                "offered a soft commitment if the next cohort hit a sixty-percent retention target. The "
                "team left the room tired but focused on that single metric."
            ),
            "gapped_text": (
                "Maya's team spent Monday refining a meal-planning (1)___ for busy parents. Early (2)___ "
                "liked the shopping list, but churn rose after week two, so the founders tracked which "
                "screens people abandoned. For the investor (3)___ they kept one clear problem slide and "
                "a demo of the weekly menu builder. (4)___ talks with a seed fund hinged on proving "
                "repeat orders, not vanity downloads. Maya cut the feature list, added a short onboarding "
                "quiz, and invited twenty unpaid testers to a feedback call. After that presentation the partners "
                "offered a soft commitment if the next cohort hit a sixty-percent (5)___ target. The "
                "team left the room tired but focused on that single metric."
            ),
            "answers": ["product", "users", "pitch", "Funding", "retention"],
            "word_bank": ["product", "users", "pitch", "Funding", "retention", "warehouse"],
            "questions": [
                {
                    "q": "Who is the meal-planning product for?",
                    "accept": ["busy parents", "parents"],
                    "hint_ru": "Для кого продукт?",
                    "quote": "…product for busy parents.",
                    "model_en": "It is for busy parents.",
                },
                {
                    "q": "What problem rose after week two?",
                    "accept": ["churn", "churn rose", "users left"],
                    "hint_ru": "Что выросло после второй недели?",
                    "quote": "…churn rose after week two…",
                    "model_en": "Churn rose after week two.",
                },
                {
                    "q": "What did funding talks depend on proving?",
                    "accept": ["repeat orders", "not vanity downloads", "orders"],
                    "hint_ru": "Что нужно было доказать инвесторам?",
                    "quote": "…proving repeat orders, not vanity downloads.",
                    "model_en": "They had to prove repeat orders, not vanity downloads.",
                },
                {
                    "q": "What retention target did partners require?",
                    "accept": ["sixty-percent", "60%", "sixty percent", "sixty-percent retention"],
                    "hint_ru": "Какой целевой retention?",
                    "quote": "…sixty-percent retention target.",
                    "model_en": "They required a sixty-percent retention target.",
                },
            ],
            "plan": [
                "Product and early-user problem",
                "Pitch focus and funding condition",
                "Product cuts and feedback calls",
                "Soft commitment and retention goal",
            ],
            "facts": [
                "The product helps busy parents plan meals.",
                "Churn rose after week two despite liking the shopping list.",
                "Funding hinged on repeat orders, not downloads.",
                "Partners offered a soft commitment if retention hit sixty percent.",
            ],
        },
        "remote": {
            "full_text": (
                "After six months of working from home, Jonas still struggled with afternoon focus. "
                "His calendar filled with back-to-back meetings, so deep work slipped to late evenings "
                "and his sleep suffered. The company introduced two office days each week and protected "
                "Wednesday mornings as meeting-free. Jonas tested a simple priority rule: camera on for "
                "decisions, async notes for updates. He also moved the desk away from the kitchen and "
                "set a hard stop at six. Within a month his deep-work blocks lengthened, and he used on-site "
                "days for brainstorming while keeping quiet writing at home. The change did not remove "
                "calendar clutter, but it restored a workable balance."
            ),
            "gapped_text": (
                "After six months of working from home, Jonas still struggled with afternoon (1)___. "
                "His calendar filled with back-to-back (2)___, so deep work slipped to late evenings "
                "and his sleep suffered. The company introduced two (3)___ each week and protected "
                "Wednesday mornings as meeting-free. Jonas tested a simple (4)___ rule: camera on for "
                "decisions, async notes for updates. He also moved the desk away from the kitchen and "
                "set a hard stop at six. Within a month his deep-work blocks lengthened, and he used on-site "
                "days for brainstorming while keeping quiet writing at home. The change did not remove "
                "calendar clutter, but it restored a workable (5)___."
            ),
            "answers": ["focus", "meetings", "office days", "priority", "balance"],
            "word_bank": ["focus", "meetings", "office days", "priority", "balance", "overtime"],
            "questions": [
                {
                    "q": "What did Jonas struggle with in the afternoon?",
                    "accept": ["focus", "afternoon focus"],
                    "hint_ru": "С чем были проблемы днём?",
                    "quote": "…struggled with afternoon focus.",
                    "model_en": "He struggled with afternoon focus.",
                },
                {
                    "q": "How many office days did the company introduce each week?",
                    "accept": ["two", "two office days", "2"],
                    "hint_ru": "Сколько офисных дней ввели?",
                    "quote": "…two office days each week…",
                    "model_en": "The company introduced two office days each week.",
                },
                {
                    "q": "Which morning was protected as meeting-free?",
                    "accept": ["Wednesday", "Wednesday mornings"],
                    "hint_ru": "Какое утро без встреч?",
                    "quote": "…Wednesday mornings as meeting-free.",
                    "model_en": "Wednesday mornings were meeting-free.",
                },
                {
                    "q": "What did Jonas use office days for?",
                    "accept": ["brainstorming", "for brainstorming"],
                    "hint_ru": "Для чего офисные дни?",
                    "quote": "…on-site days for brainstorming…",
                    "model_en": "He used on-site days for brainstorming.",
                },
            ],
            "plan": [
                "Focus problems at home",
                "Meetings overload and new office policy",
                "Balance rules and desk changes",
                "Results after one month",
            ],
            "facts": [
                "Jonas struggled with afternoon focus after six months at home.",
                "Back-to-back meetings pushed deep work into evenings.",
                "The company added two office days and meeting-free Wednesdays.",
                "He used on-site days for brainstorming and writing at home.",
            ],
        },
        "news": {
            "full_text": (
                "The local evening bulletin opened with a riverside park project that would close two "
                "lanes for eight months. Locals flooded the comments with mixed opinion: some wanted "
                "safer walking paths, others feared longer bus rides to school. A councillor argued the "
                "impact on shopkeepers near the bridge had been underestimated. Reporters interviewed "
                "a café owner who already saw fewer lunch customers and a cycling group that welcomed "
                "the plan. By Friday the mayor promised a public Q&A and a temporary shuttle. The "
                "story showed how one infrastructure scheme can split a neighbourhood while still "
                "claiming to serve the same citizens. Readers shared the article widely, turning a "
                "planning notice into the week's leading local news."
            ),
            "gapped_text": (
                "The local evening bulletin opened with a riverside park (1)___ that would close two "
                "lanes for eight months. Locals flooded the comments with mixed (2)___: some wanted "
                "safer walking paths, others feared longer bus rides to school. A councillor argued the "
                "(3)___ on shopkeepers near the bridge had been underestimated. Reporters interviewed "
                "a café owner who already saw fewer lunch customers and a cycling group that welcomed "
                "the plan. By Friday the mayor promised a public Q&A and a temporary shuttle. The "
                "story showed how one infrastructure scheme can split a neighbourhood while still "
                "claiming to serve the same (4)___. Readers shared the article widely, turning a "
                "planning notice into the week's leading local (5)___."
            ),
            "answers": ["project", "opinion", "impact", "citizens", "news"],
            "word_bank": ["project", "opinion", "impact", "citizens", "news", "election"],
            "questions": [
                {
                    "q": "What would the riverside park project close for eight months?",
                    "accept": ["two lanes", "lanes", "two lanes for eight months"],
                    "hint_ru": "Что закроют на восемь месяцев?",
                    "quote": "…close two lanes for eight months.",
                    "model_en": "It would close two lanes for eight months.",
                },
                {
                    "q": "Whose impact did a councillor say was underestimated?",
                    "accept": ["shopkeepers", "shopkeepers near the bridge", "on shopkeepers"],
                    "hint_ru": "На ком недооценили влияние?",
                    "quote": "…impact on shopkeepers near the bridge…",
                    "model_en": "The impact on shopkeepers near the bridge.",
                },
                {
                    "q": "What did the mayor promise by Friday?",
                    "accept": ["a public Q&A and a temporary shuttle", "Q&A", "temporary shuttle"],
                    "hint_ru": "Что пообещал мэр?",
                    "quote": "…a public Q&A and a temporary shuttle.",
                    "model_en": "A public Q&A and a temporary shuttle.",
                },
                {
                    "q": "Who welcomed the plan according to reporters?",
                    "accept": ["a cycling group", "cycling group"],
                    "hint_ru": "Кто приветствовал план?",
                    "quote": "…a cycling group that welcomed the plan.",
                    "model_en": "A cycling group welcomed the plan.",
                },
            ],
            "plan": [
                "Park project and lane closures",
                "Mixed citizen opinion",
                "Shopkeeper impact and interviews",
                "Mayor's response and wider reaction",
            ],
            "facts": [
                "A riverside park project would close two lanes for eight months.",
                "Citizen opinion was mixed between safer paths and longer bus rides.",
                "A councillor said shopkeeper impact was underestimated.",
                "The mayor promised a Q&A and a temporary shuttle.",
            ],
        },
        "uni": {
            "full_text": (
                "Omar had twelve days left to finish a sociology essay on urban loneliness. The "
                "module handbook demanded at least eight academic sources, yet half of his notes came "
                "from blogs. His tutor's previous feedback warned him to define terms early and avoid "
                "sweeping claims. Omar booked a library desk, rebuilt the outline around three case "
                "cities, and replaced weak links with journal articles. He still feared the Friday "
                "deadline, so he drafted the conclusion first and wrote the methods section overnight. "
                "On Thursday he uploaded a draft for peer review and used the comments to tighten "
                "citations. The final piece was shorter, but the references were stronger and last term's "
                "advice finally shaped the structure."
            ),
            "gapped_text": (
                "Omar had twelve days left to finish a sociology (1)___ on urban loneliness. The "
                "module handbook demanded at least eight academic (2)___, yet half of his notes came "
                "from blogs. His tutor's previous (3)___ warned him to define terms early and avoid "
                "sweeping claims. Omar booked a library desk, rebuilt the outline around three case "
                "cities, and replaced weak links with journal articles. He still feared the Friday "
                "(4)___, so he drafted the conclusion first and wrote the methods section overnight. "
                "On Thursday he uploaded a draft for peer review and used the comments to tighten "
                "citations. The final piece was shorter, but the references were stronger and last term's "
                "advice finally shaped the (5)___."
            ),
            "answers": ["essay", "sources", "feedback", "deadline", "structure"],
            "word_bank": ["essay", "sources", "feedback", "deadline", "structure", "campus"],
            "questions": [
                {
                    "q": "What was Omar's sociology essay about?",
                    "accept": ["urban loneliness", "loneliness"],
                    "hint_ru": "О чём эссе?",
                    "quote": "…essay on urban loneliness.",
                    "model_en": "It was about urban loneliness.",
                },
                {
                    "q": "How many academic sources did the handbook demand?",
                    "accept": ["at least eight", "eight", "8"],
                    "hint_ru": "Сколько академических источников требовали?",
                    "quote": "…at least eight academic sources…",
                    "model_en": "At least eight academic sources.",
                },
                {
                    "q": "When was the deadline?",
                    "accept": ["Friday", "Friday deadline"],
                    "hint_ru": "Какой был дедлайн?",
                    "quote": "…feared the Friday deadline…",
                    "model_en": "The deadline was on Friday.",
                },
                {
                    "q": "What did last term's feedback finally shape?",
                    "accept": ["the structure", "structure"],
                    "hint_ru": "Что сформировал прошлый feedback?",
                    "quote": "…last term's advice finally shaped the structure.",
                    "model_en": "It shaped the structure.",
                },
            ],
            "plan": [
                "Essay topic and weak sources",
                "Tutor feedback and library work",
                "Deadline pressure and drafting order",
                "Peer review and stronger final version",
            ],
            "facts": [
                "Omar wrote a sociology essay on urban loneliness.",
                "He needed at least eight academic sources.",
                "Previous feedback told him to define terms early.",
                "He feared Friday's deadline and used peer review on Thursday.",
            ],
        },
        "customer": {
            "full_text": (
                "A customer emailed support after a blender arrived with a cracked lid and no spare "
                "gasket in the box. The complaint listed two failed chat attempts and a demand for a "
                "full refund within three days. Mira, the agent on duty, opened with a clear apology "
                "and confirmed the order photo matched the damaged parcel. She offered either a "
                "replacement overnight or a repayment to the original card, plus a discount code for the "
                "next purchase. The customer chose repayment and asked that the warehouse check the "
                "packing process. Mira logged the solution, escalated the packaging note, and closed "
                "the ticket only after the payment reversal appeared. The exchange turned a sharp "
                "message into a documented packing overhaul."
            ),
            "gapped_text": (
                "A customer emailed support after a blender arrived with a cracked lid and no spare "
                "gasket in the box. The (1)___ listed two failed chat attempts and a demand for a "
                "full (2)___ within three days. Mira, the agent on duty, opened with a clear (3)___ "
                "and confirmed the order photo matched the damaged parcel. She offered either a "
                "replacement overnight or a repayment to the original card, plus a discount code for the "
                "next purchase. The customer chose repayment and asked that the warehouse check the "
                "packing process. Mira logged the (4)___, escalated the packaging note, and closed "
                "the ticket only after the payment reversal appeared. The exchange turned a sharp "
                "message into a documented packing (5)___."
            ),
            "answers": ["complaint", "refund", "apology", "solution", "overhaul"],
            "word_bank": ["complaint", "refund", "apology", "solution", "overhaul", "loyalty"],
            "questions": [
                {
                    "q": "What was wrong with the blender delivery?",
                    "accept": ["cracked lid", "no spare gasket", "cracked lid and no spare gasket"],
                    "hint_ru": "Что было не так с доставкой?",
                    "quote": "…cracked lid and no spare gasket…",
                    "model_en": "The lid was cracked and the spare gasket was missing.",
                },
                {
                    "q": "How soon did the customer want a full refund?",
                    "accept": ["within three days", "three days", "3 days"],
                    "hint_ru": "За сколько дней требовали refund?",
                    "quote": "…full refund within three days.",
                    "model_en": "Within three days.",
                },
                {
                    "q": "What two options did Mira offer?",
                    "accept": [
                        "replacement overnight or a repayment",
                        "replacement overnight or a refund",
                        "replacement or refund",
                        "replacement or repayment",
                        "overnight replacement or refund",
                    ],
                    "hint_ru": "Какие варианты предложила Mira?",
                    "quote": "…replacement overnight or a repayment…",
                    "model_en": "A replacement overnight or a repayment to the original card.",
                },
                {
                    "q": "Which option did the customer choose?",
                    "accept": ["repayment", "the repayment", "the refund", "refund"],
                    "hint_ru": "Что выбрал клиент?",
                    "quote": "The customer chose repayment…",
                    "model_en": "The customer chose repayment.",
                },
            ],
            "plan": [
                "Damaged delivery and complaint",
                "Apology and verification",
                "Options offered",
                "Repayment choice and packing overhaul",
            ],
            "facts": [
                "The blender arrived with a cracked lid and no spare gasket.",
                "The complaint demanded a full refund within three days.",
                "Mira opened with an apology and offered replacement or repayment.",
                "The customer chose repayment; Mira logged the solution.",
            ],
        },
        "health": {
            "full_text": (
                "After a winter of late screens, Nadia rebuilt her healthy lifestyle in small steps. "
                "She tracked three habits for thirty days: a phone-free last hour, a ten-minute walk "
                "after lunch, and water before coffee. Sleep improved once she fixed a consistent "
                "bedtime, and her diet shifted from desk snacks to prepared lunches twice a week. "
                "Motivation dipped in week two, so she joined a Friday park group instead of relying "
                "on willpower alone. A nurse friend reminded her that progress is uneven and that "
                "rest days still count. By the end of the month Nadia slept longer, skipped fewer "
                "breakfasts, and kept the walk even on busy days. The experiment proved that boring "
                "routines beat dramatic resolutions."
            ),
            "gapped_text": (
                "After a winter of late screens, Nadia rebuilt her healthy lifestyle in small steps. "
                "She tracked three (1)___ for thirty days: a phone-free last hour, a ten-minute walk "
                "after lunch, and water before coffee. (2)___ improved once she fixed a consistent "
                "bedtime, and her (3)___ shifted from desk snacks to prepared lunches twice a week. "
                "(4)___ dipped in week two, so she joined a Friday park group instead of relying "
                "on willpower alone. A nurse friend reminded her that progress is uneven and that "
                "rest days still count. By the end of the month Nadia slept longer, skipped fewer "
                "breakfasts, and kept the walk even on busy days. The experiment proved that boring "
                "routines beat dramatic (5)___."
            ),
            "answers": ["habits", "Sleep", "diet", "Motivation", "resolutions"],
            "word_bank": ["habits", "Sleep", "diet", "Motivation", "resolutions", "gym"],
            "questions": [
                {
                    "q": "How long did Nadia track her three habits?",
                    "accept": ["thirty days", "30 days", "a month"],
                    "hint_ru": "Сколько дней она отслеживала привычки?",
                    "quote": "…three habits for thirty days…",
                    "model_en": "For thirty days.",
                },
                {
                    "q": "What improved after she fixed a consistent bedtime?",
                    "accept": ["Sleep", "sleep"],
                    "hint_ru": "Что улучшилось после стабильного отбоя?",
                    "quote": "Sleep improved once she fixed a consistent bedtime…",
                    "model_en": "Sleep improved.",
                },
                {
                    "q": "When did motivation dip?",
                    "accept": ["week two", "in week two"],
                    "hint_ru": "Когда упала мотивация?",
                    "quote": "Motivation dipped in week two…",
                    "model_en": "Motivation dipped in week two.",
                },
                {
                    "q": "What did she join instead of relying on willpower alone?",
                    "accept": ["a Friday park group", "Friday park group", "park group"],
                    "hint_ru": "К чему она присоединилась?",
                    "quote": "…joined a Friday park group…",
                    "model_en": "She joined a Friday park group.",
                },
            ],
            "plan": [
                "Three tracked habits",
                "Sleep and diet changes",
                "Motivation dip and park group",
                "Month-end results",
            ],
            "facts": [
                "Nadia tracked three habits for thirty days.",
                "Sleep improved with a consistent bedtime; diet shifted to prepared lunches.",
                "Motivation dipped in week two, so she joined a Friday park group.",
                "By month's end she slept longer and kept the walk on busy days.",
            ],
        },
        "culture": {
            "full_text": (
                "On Saturday Lena queued for an evening exhibition of Baltic photography at the city "
                "gallery. Tickets were timed entry, so she arrived twenty minutes early and read the "
                "curator's note on post-industrial light. Inside, the rooms stayed quiet; the "
                "atmosphere mixed cool concrete with warm amber lamps over large prints. Lena took "
                "no photos, only short notes for a review she owed her student magazine. A guide "
                "explained why one series used expired film, and visitors lingered longest at a "
                "harbour triptych. Afterward Lena wrote that the show avoided nostalgia and "
                "trusted empty space. Her editor kept her piece almost unchanged and printed it "
                "beside the weekend listings."
            ),
            "gapped_text": (
                "On Saturday Lena queued for an evening (1)___ of Baltic photography at the city "
                "gallery. (2)___ were timed entry, so she arrived twenty minutes early and read the "
                "curator's note on post-industrial light. Inside, the rooms stayed quiet; the "
                "(3)___ mixed cool concrete with warm amber lamps over large prints. Lena took "
                "no photos, only short notes for a (4)___ she owed her student magazine. A guide "
                "explained why one series used expired film, and visitors lingered longest at a "
                "harbour triptych. Afterward Lena wrote that the show avoided nostalgia and "
                "trusted empty space. Her editor kept her piece almost unchanged and printed it "
                "beside the weekend (5)___."
            ),
            "answers": ["exhibition", "Tickets", "atmosphere", "review", "listings"],
            "word_bank": ["exhibition", "Tickets", "atmosphere", "review", "listings", "auction"],
            "questions": [
                {
                    "q": "What kind of exhibition did Lena visit?",
                    "accept": ["Baltic photography", "photography", "evening exhibition of Baltic photography"],
                    "hint_ru": "Какая была выставка?",
                    "quote": "…exhibition of Baltic photography…",
                    "model_en": "An evening exhibition of Baltic photography.",
                },
                {
                    "q": "Why did she arrive twenty minutes early?",
                    "accept": ["timed entry", "Tickets were timed entry", "timed tickets"],
                    "hint_ru": "Почему пришла заранее?",
                    "quote": "Tickets were timed entry…",
                    "model_en": "Because tickets were timed entry.",
                },
                {
                    "q": "Who was the review for?",
                    "accept": ["her student magazine", "student magazine"],
                    "hint_ru": "Для кого рецензия?",
                    "quote": "…a review she owed her student magazine.",
                    "model_en": "For her student magazine.",
                },
                {
                    "q": "Where did visitors linger longest?",
                    "accept": ["harbour triptych", "at a harbour triptych"],
                    "hint_ru": "Где дольше всего задерживались посетители?",
                    "quote": "…lingered longest at a harbour triptych.",
                    "model_en": "At a harbour triptych.",
                },
            ],
            "plan": [
                "Exhibition visit and timed tickets",
                "Gallery atmosphere",
                "Notes for a review",
                "Published piece beside listings",
            ],
            "facts": [
                "Lena attended an evening Baltic photography exhibition.",
                "Tickets were timed entry; she arrived early.",
                "She wrote a review for her student magazine.",
                "The editor printed the review beside weekend listings.",
            ],
        },
    },
    "C1": {
        "negotiation": {
            "full_text": (
                "Across a polished table in Rotterdam, two supply-chain teams bargained over a "
                "three-year logistics contract. The buyer's opening terms demanded price cuts that "
                "would erase the vendor's thin margin, while the vendor cited fuel volatility as "
                "leverage for a flexible surcharge clause. After two hours neither side moved, so "
                "the mediators reframed the deal around volume guarantees and shared risk. A narrow "
                "compromise emerged: a modest discount in year one, indexed rates thereafter, and "
                "penalties only if on-time delivery fell below ninety-four percent. Legal counsel "
                "redrafted the ambiguous force-majeure wording before anyone initialled the pages. "
                "Both parties left with less than they wanted, yet with an agreement they could defend "
                "internally—and with bargaining power reserved for the mid-term review."
            ),
            "gapped_text": (
                "Across a polished table in Rotterdam, two supply-chain teams bargained over a "
                "three-year logistics (1)___. The buyer's opening (2)___ demanded price cuts that "
                "would erase the vendor's thin margin, while the vendor cited fuel volatility as "
                "(3)___ for a flexible surcharge clause. After two hours neither side moved, so "
                "the mediators reframed the deal around volume guarantees and shared risk. A narrow "
                "(4)___ emerged: a modest discount in year one, indexed rates thereafter, and "
                "penalties only if on-time delivery fell below ninety-four percent. Legal counsel "
                "redrafted the ambiguous force-majeure wording before anyone initialled the pages. "
                "Both parties left with less than they wanted, yet with an agreement they could defend "
                "internally—and with bargaining power reserved for the mid-term (5)___."
            ),
            "answers": ["contract", "terms", "leverage", "compromise", "review"],
            "word_bank": ["contract", "terms", "leverage", "compromise", "review", "warehouse"],
            "questions": [
                {
                    "q": "Where did the negotiation take place?",
                    "accept": ["Rotterdam", "in Rotterdam"],
                    "hint_ru": "Где проходили переговоры?",
                    "quote": "…table in Rotterdam…",
                    "model_en": "In Rotterdam.",
                },
                {
                    "q": "What did the vendor use as leverage?",
                    "accept": ["fuel volatility", "volatility"],
                    "hint_ru": "Что использовал vendor как leverage?",
                    "quote": "…cited fuel volatility as leverage…",
                    "model_en": "Fuel volatility.",
                },
                {
                    "q": "Below what on-time delivery rate would penalties apply?",
                    "accept": ["ninety-four percent", "94%", "94 percent"],
                    "hint_ru": "Ниже какого процента штрафы?",
                    "quote": "…fell below ninety-four percent.",
                    "model_en": "Below ninety-four percent.",
                },
                {
                    "q": "What wording did legal counsel redraft?",
                    "accept": ["force-majeure", "force-majeure wording", "ambiguous force-majeure wording"],
                    "hint_ru": "Какую формулировку переписали юристы?",
                    "quote": "…ambiguous force-majeure wording…",
                    "model_en": "The ambiguous force-majeure wording.",
                },
            ],
            "plan": [
                "Contract stakes and opening terms",
                "Leverage and deadlock",
                "Compromise structure",
                "Legal redraft and reserved leverage",
            ],
            "facts": [
                "Teams negotiated a three-year logistics contract in Rotterdam.",
                "The vendor used fuel volatility as leverage for a surcharge clause.",
                "Compromise included year-one discount and indexed rates later.",
                "Penalties applied only below ninety-four percent on-time delivery.",
            ],
        },
        "media": {
            "full_text": (
                "A national outlet led Tuesday with a headline that framed a hospital IT outage as "
                "deliberate sabotage, though early police statements only confirmed a system failure. "
                "Critics accused the desk of bias for elevating an unnamed blogger while burying "
                "quotes from the hospital's own engineers. Editors later insisted they had checked "
                "three independent sources, yet the timeline on the page still omitted the vendor's "
                "maintenance window. Audience metrics rewarded the dramatic framing: shares spiked "
                "before a correction appeared under the fold. By evening a quieter update walked "
                "back the sabotage claim, but the original banner lingered in screenshots. The "
                "episode illustrated how speed, slant, and incomplete citations can lock readers "
                "into a narrative that facts later soften."
            ),
            "gapped_text": (
                "A national outlet led Tuesday with a (1)___ that framed a hospital IT outage as "
                "deliberate sabotage, though early police statements only confirmed a system failure. "
                "Critics accused the desk of (2)___ for elevating an unnamed blogger while burying "
                "quotes from the hospital's own engineers. Editors later insisted they had checked "
                "three independent (3)___, yet the timeline on the page still omitted the vendor's "
                "maintenance window. (4)___ metrics rewarded the dramatic framing: shares spiked "
                "before a correction appeared under the fold. By evening a quieter update walked "
                "back the sabotage claim, but the original banner lingered in screenshots. The "
                "episode illustrated how speed, slant, and incomplete citations can lock readers "
                "into a (5)___ that facts later soften."
            ),
            "answers": ["headline", "bias", "sources", "Audience", "narrative"],
            "word_bank": ["headline", "bias", "sources", "Audience", "narrative", "paywall"],
            "questions": [
                {
                    "q": "How did the headline frame the hospital IT outage?",
                    "accept": ["deliberate sabotage", "as deliberate sabotage", "sabotage"],
                    "hint_ru": "Как заголовок подал сбой?",
                    "quote": "…framed a hospital IT outage as deliberate sabotage…",
                    "model_en": "As deliberate sabotage.",
                },
                {
                    "q": "How many independent sources did editors claim to have checked?",
                    "accept": ["three", "3", "three independent sources"],
                    "hint_ru": "Сколько независимых источников?",
                    "quote": "…checked three independent sources…",
                    "model_en": "Three independent sources.",
                },
                {
                    "q": "What did the page timeline omit?",
                    "accept": ["the vendor's maintenance window", "maintenance window"],
                    "hint_ru": "Что пропустила timeline?",
                    "quote": "…omitted the vendor's maintenance window.",
                    "model_en": "The vendor's maintenance window.",
                },
                {
                    "q": "What happened to the sabotage claim by evening?",
                    "accept": ["walked back", "walked back the sabotage claim", "softened", "corrected"],
                    "hint_ru": "Что сделали с утверждением о саботаже к вечеру?",
                    "quote": "…walked back the sabotage claim…",
                    "model_en": "A quieter update walked back the sabotage claim.",
                },
            ],
            "plan": [
                "Dramatic headline vs early facts",
                "Bias accusation and sources claim",
                "Audience metrics and correction",
                "Lingering screenshots and lesson",
            ],
            "facts": [
                "A headline framed an IT outage as deliberate sabotage.",
                "Critics alleged bias for elevating an unnamed blogger.",
                "Editors claimed three independent sources; the timeline omitted a maintenance window.",
                "An evening update walked back the sabotage claim.",
            ],
        },
        "climate": {
            "full_text": (
                "The city council's climate brief proposed a low-emission zone that would charge older "
                "vans entering the centre after next April. Officials framed the policy as public-health "
                "protection, yet small traders warned that compliance costs could close family shops. "
                "Community workshops produced maps of delivery routes and lists of balances: cleaner "
                "air against higher grocery prices, quieter streets against longer last-mile trips. "
                "A revised draft offered grants for electric vans and a phased map that spared the "
                "eastern market for eighteen months. Budget officers still questioned whether the "
                "outlays were fully scored. Residents left the hall divided, convinced that climate "
                "ambition without honest trade-offs would either stall or punish the least flexible "
                "firms."
            ),
            "gapped_text": (
                "The city council's climate brief proposed a low-emission zone that would charge older "
                "vans entering the centre after next April. Officials framed the (1)___ as public-health "
                "protection, yet small traders warned that compliance (2)___ could close family shops. "
                "(3)___ workshops produced maps of delivery routes and lists of balances: cleaner "
                "air against higher grocery prices, quieter streets against longer last-mile trips. "
                "A revised draft offered grants for electric vans and a phased map that spared the "
                "eastern market for eighteen months. Budget officers still questioned whether the "
                "outlays were fully scored. Residents left the hall divided, convinced that climate "
                "ambition without honest (4)___ would either stall or punish the least flexible "
                "(5)___."
            ),
            "answers": ["policy", "costs", "Community", "trade-offs", "firms"],
            "word_bank": ["policy", "costs", "Community", "trade-offs", "firms", "referendum"],
            "questions": [
                {
                    "q": "When would older vans start being charged in the centre?",
                    "accept": ["after next April", "next April", "April"],
                    "hint_ru": "С какого срока начнут брать плату?",
                    "quote": "…after next April.",
                    "model_en": "After next April.",
                },
                {
                    "q": "What did small traders fear compliance costs could do?",
                    "accept": ["close family shops", "close shops"],
                    "hint_ru": "Чего боялись торговцы?",
                    "quote": "…compliance costs could close family shops.",
                    "model_en": "Close family shops.",
                },
                {
                    "q": "How long would the eastern market be spared?",
                    "accept": ["eighteen months", "18 months"],
                    "hint_ru": "На сколько месяцев отложили для восточного рынка?",
                    "quote": "…spared the eastern market for eighteen months.",
                    "model_en": "For eighteen months.",
                },
                {
                    "q": "What did the revised draft offer for electric vans?",
                    "accept": ["grants", "grants for electric vans"],
                    "hint_ru": "Что предложили для электрофургонов?",
                    "quote": "…grants for electric vans…",
                    "model_en": "Grants for electric vans.",
                },
            ],
            "plan": [
                "Low-emission policy proposal",
                "Cost concerns from traders",
                "Community trade-offs and revised draft",
                "Budget doubts and divided residents",
            ],
            "facts": [
                "A low-emission zone would charge older vans after next April.",
                "Traders warned compliance costs could close family shops.",
                "Workshops listed trade-offs between cleaner air and higher prices.",
                "The revised draft offered grants and spared the eastern market for eighteen months.",
            ],
        },
        "hr": {
            "full_text": (
                "During Helena's mid-year review, her manager opened with performance data from two "
                "product launches and a customer-escalation week that had tested the whole squad. "
                "Targets for delivery were met, yet soft skills scores lagged: peers wanted clearer "
                "escalation paths and fewer last-minute changes to shared documents. Helena asked "
                "bluntly about promotion timing; the answer hinged on leading one cross-team project "
                "and documenting mentoring goals for a junior hire. HR later circulated a written "
                "plan with quarterly check-ins rather than vague encouragement, plus a short course "
                "on facilitation. Helena left frustrated but oriented—she knew which behaviours "
                "blocked advancement and which outcomes would reopen the advancement conversation in "
                "December if the coaching notes stayed green."
            ),
            "gapped_text": (
                "During Helena's mid-year review, her manager opened with (1)___ data from two "
                "product launches and a customer-escalation week that had tested the whole squad. "
                "Targets for delivery were met, yet (2)___ scores lagged: peers wanted clearer "
                "escalation paths and fewer last-minute changes to shared documents. Helena asked "
                "bluntly about (3)___ timing; the answer hinged on leading one cross-team project "
                "and documenting mentoring (4)___ for a junior hire. HR later circulated a written "
                "plan with quarterly check-ins rather than vague encouragement, plus a short course "
                "on facilitation. Helena left frustrated but oriented—she knew which behaviours "
                "blocked advancement and which outcomes would reopen the advancement conversation in "
                "(5)___ if the coaching notes stayed green."
            ),
            "answers": ["performance", "soft skills", "promotion", "goals", "December"],
            "word_bank": ["performance", "soft skills", "promotion", "goals", "December", "severance"],
            "questions": [
                {
                    "q": "What performance data did the manager open with?",
                    "accept": [
                        "two product launches and a customer-escalation week",
                        "product launches",
                        "customer-escalation week",
                    ],
                    "hint_ru": "С каких данных начал менеджер?",
                    "quote": "…performance data from two product launches and a customer-escalation week.",
                    "model_en": "Data from two product launches and a customer-escalation week.",
                },
                {
                    "q": "Which scores lagged despite met delivery targets?",
                    "accept": ["soft skills", "soft skills scores"],
                    "hint_ru": "Какие оценки отставали?",
                    "quote": "…soft skills scores lagged…",
                    "model_en": "Soft skills scores.",
                },
                {
                    "q": "What two conditions hinged on for promotion timing?",
                    "accept": [
                        "leading one cross-team project and documenting mentoring goals",
                        "cross-team project and mentoring goals",
                    ],
                    "hint_ru": "От чего зависел срок promotion?",
                    "quote": "…leading one cross-team project and documenting mentoring goals…",
                    "model_en": "Leading a cross-team project and documenting mentoring goals.",
                },
                {
                    "q": "When might the promotion conversation reopen?",
                    "accept": ["December", "in December"],
                    "hint_ru": "Когда снова обсудят promotion?",
                    "quote": "…advancement conversation in December…",
                    "model_en": "In December.",
                },
            ],
            "plan": [
                "Performance data presented",
                "Soft-skills gap",
                "Promotion conditions and mentoring goals",
                "Written HR plan and December checkpoint",
            ],
            "facts": [
                "Helena's delivery targets were met; soft skills scores lagged.",
                "Peers wanted clearer escalation paths and fewer last-minute changes.",
                "Promotion hinged on a cross-team project and mentoring goals.",
                "HR issued a written plan; the next promotion talk was set for December.",
            ],
        },
        "research": {
            "full_text": (
                "A university team summarised a twelve-month study of night-shift alertness among "
                "warehouse staff in three regional hubs. Their method combined wearable sleep trackers "
                "with fortnightly cognitive tests and anonymised incident logs from supervisors. "
                "Preliminary findings suggested that split rest breaks reduced near-miss reports more "
                "than caffeine stipends alone, though the sample excluded contractors. The authors "
                "listed clear limits: self-reported caffeine intake was unreliable, and winter darkness "
                "may have confounded fatigue scores across sites. Recommended next steps included a "
                "randomised schedule trial and partnership with occupational clinicians. Funders "
                "praised the cautious tone; managers asked for a one-page brief before changing rotas. "
                "The summary refused hype and treated uncertainty as part of the evidence, not a "
                "footnote to ignore."
            ),
            "gapped_text": (
                "A university team summarised a twelve-month study of night-shift alertness among "
                "warehouse staff in three regional hubs. Their (1)___ combined wearable sleep trackers "
                "with fortnightly cognitive tests and anonymised incident logs from supervisors. "
                "Preliminary (2)___ suggested that split rest breaks reduced near-miss reports more "
                "than caffeine stipends alone, though the sample excluded contractors. The authors "
                "listed clear (3)___: self-reported caffeine intake was unreliable, and winter darkness "
                "may have confounded fatigue scores across sites. Recommended (4)___ included a "
                "randomised schedule trial and partnership with occupational clinicians. Funders "
                "praised the cautious tone; managers asked for a one-page brief before changing rotas. "
                "The summary refused hype and treated uncertainty as part of the (5)___, not a "
                "footnote to ignore."
            ),
            "answers": ["method", "findings", "limits", "next steps", "evidence"],
            "word_bank": ["method", "findings", "limits", "next steps", "evidence", "budget"],
            "questions": [
                {
                    "q": "How long was the night-shift alertness study?",
                    "accept": ["twelve-month", "twelve months", "12 months"],
                    "hint_ru": "Сколько длилось исследование?",
                    "quote": "…a twelve-month study…",
                    "model_en": "Twelve months.",
                },
                {
                    "q": "What reduced near-miss reports more than caffeine stipends alone?",
                    "accept": ["split rest breaks", "rest breaks"],
                    "hint_ru": "Что снизило near-miss сильнее кофеина?",
                    "quote": "…split rest breaks reduced near-miss reports…",
                    "model_en": "Split rest breaks.",
                },
                {
                    "q": "Who was excluded from the sample?",
                    "accept": ["contractors", "the sample excluded contractors"],
                    "hint_ru": "Кого исключили из выборки?",
                    "quote": "…the sample excluded contractors.",
                    "model_en": "Contractors were excluded.",
                },
                {
                    "q": "What next steps did the authors recommend?",
                    "accept": [
                        "a randomised schedule trial and partnership with occupational clinicians",
                        "randomised schedule trial",
                        "partnership with occupational clinicians",
                    ],
                    "hint_ru": "Какие next steps рекомендовали?",
                    "quote": "…a randomised schedule trial and partnership with occupational clinicians.",
                    "model_en": "A randomised schedule trial and partnership with occupational clinicians.",
                },
            ],
            "plan": [
                "Study topic and method",
                "Key findings and sample limit",
                "Stated limits of the evidence",
                "Next steps and reception",
            ],
            "facts": [
                "The study lasted twelve months and used trackers, tests, and incident logs.",
                "Split rest breaks outperformed caffeine stipends alone for near-miss reduction.",
                "Limits included unreliable caffeine self-reports and winter darkness effects.",
                "Next steps: randomised schedule trial and clinician partnership.",
            ],
        },
        "ethics": {
            "full_text": (
                "A consumer-tech advisory panel spent the afternoon dissecting a voice-assistant update "
                "that stored ambient snippets by default in several markets. Privacy advocates argued "
                "that opaque consent screens failed ordinary people, while the company's counsel insisted "
                "current regulation already required notice and an opt-out. Engineers described how "
                "on-device AI could trim retention windows, yet product managers feared accuracy losses "
                "if cloud training shrank. The chair forced a practical vote: delay the launch, publish "
                "a plain-language retention table, and commission an external audit of deletion logs. "
                "Nobody claimed the compromise solved deeper power imbalances, but it treated users as "
                "stakeholders rather than telemetry streams. Minutes closed with a warning that ethics "
                "after deployment is damage control, not design."
            ),
            "gapped_text": (
                "A consumer-tech advisory panel spent the afternoon dissecting a voice-assistant update "
                "that stored ambient snippets by default in several markets. (1)___ advocates argued "
                "that opaque consent screens failed ordinary people, while the company's counsel insisted "
                "current (2)___ already required notice and an opt-out. Engineers described how "
                "on-device (3)___ could trim retention windows, yet product managers feared accuracy "
                "losses if cloud training shrank. The chair forced a practical vote: delay the launch, "
                "publish a plain-language retention table, and commission an external audit of deletion "
                "logs. Nobody claimed the compromise solved deeper power imbalances, but it treated "
                "(4)___ as stakeholders rather than telemetry streams. Minutes closed with a warning "
                "that (5)___ after deployment is damage control, not design."
            ),
            "answers": ["Privacy", "regulation", "AI", "users", "ethics"],
            "word_bank": ["Privacy", "regulation", "AI", "users", "ethics", "encryption"],
            "questions": [
                {
                    "q": "What did the voice-assistant update store by default?",
                    "accept": ["ambient snippets", "snippets"],
                    "hint_ru": "Что хранилось по умолчанию?",
                    "quote": "…stored ambient snippets by default.",
                    "model_en": "Ambient snippets.",
                },
                {
                    "q": "What did privacy advocates say failed ordinary users?",
                    "accept": ["opaque consent screens", "consent screens"],
                    "hint_ru": "Что, по мнению активистов, подвело пользователей?",
                    "quote": "…opaque consent screens failed ordinary people…",
                    "model_en": "Opaque consent screens.",
                },
                {
                    "q": "What three actions did the chair's vote require?",
                    "accept": [
                        "delay the launch, publish a retention table, and commission an audit",
                        "delay, retention table, audit",
                        "delay the launch",
                    ],
                    "hint_ru": "Какие три действия проголосовали?",
                    "quote": "…delay the launch, publish a plain-language retention table, and commission an external audit…",
                    "model_en": "Delay the launch, publish a retention table, and commission an external audit.",
                },
                {
                    "q": "How did the minutes describe ethics after deployment?",
                    "accept": ["damage control, not design", "damage control"],
                    "hint_ru": "Как описали ethics после релиза?",
                    "quote": "…ethics after deployment is damage control, not design.",
                    "model_en": "As damage control, not design.",
                },
            ],
            "plan": [
                "Default snippet storage problem",
                "Privacy vs regulation arguments",
                "On-device AI trade-off",
                "Voted remedies and closing warning",
            ],
            "facts": [
                "The update stored ambient snippets by default.",
                "Privacy advocates criticised opaque consent screens.",
                "Engineers proposed on-device AI to trim retention.",
                "The panel voted to delay launch, publish retention details, and audit deletion logs.",
            ],
        },
        "city_plan": {
            "full_text": (
                "Planners unveiled a corridor plan that paired a tram extension with mid-rise housing "
                "above new stations. The public debate split along familiar lines: residents wanted "
                "reliable transport before denser blocks, while developers insisted dwelling finance "
                "required the ridership numbers first. Budget sheets showed a funding gap unless "
                "regional grants arrived by autumn. Architects offered courtyards and quieter street "
                "edges to soften opposition, yet heritage groups still feared shadow on a listed "
                "square. After three hearings the mayor endorsed a phased build—tracks first, then "
                "two residential pilots—contingent on a transparent spending revision. The compromise "
                "pleased few enthusiasts, but it kept mobility and dwellings on the same map instead "
                "of rival petitions."
            ),
            "gapped_text": (
                "Planners unveiled a corridor plan that paired a tram extension with mid-rise (1)___ "
                "above new stations. The public (2)___ split along familiar lines: residents wanted "
                "reliable (3)___ before denser blocks, while developers insisted dwelling finance "
                "required the ridership numbers first. (4)___ sheets showed a funding gap unless "
                "regional grants arrived by autumn. Architects offered courtyards and quieter street "
                "edges to soften opposition, yet heritage groups still feared shadow on a listed "
                "square. After three hearings the mayor endorsed a phased build—tracks first, then "
                "two residential pilots—contingent on a transparent spending revision. The compromise "
                "pleased few enthusiasts, but it kept mobility and dwellings on the same map instead "
                "of rival (5)___."
            ),
            "answers": ["housing", "debate", "transport", "Budget", "petitions"],
            "word_bank": ["housing", "debate", "transport", "Budget", "petitions", "tolls"],
            "questions": [
                {
                    "q": "What two elements did the corridor plan pair?",
                    "accept": [
                        "a tram extension with mid-rise housing",
                        "tram extension and housing",
                        "tram and housing",
                    ],
                    "hint_ru": "Что сочетал план коридора?",
                    "quote": "…a tram extension with mid-rise housing…",
                    "model_en": "A tram extension with mid-rise housing above new stations.",
                },
                {
                    "q": "What did residents want before denser blocks?",
                    "accept": ["reliable transport", "transport first", "reliable transport before denser blocks"],
                    "hint_ru": "Что жители хотели раньше уплотнения?",
                    "quote": "…reliable transport before denser blocks…",
                    "model_en": "Reliable transport before denser blocks.",
                },
                {
                    "q": "By when did regional grants need to arrive?",
                    "accept": ["by autumn", "autumn"],
                    "hint_ru": "К какому сроку нужны гранты?",
                    "quote": "…grants arrived by autumn.",
                    "model_en": "By autumn.",
                },
                {
                    "q": "What phased order did the mayor endorse?",
                    "accept": [
                        "tracks first, then two residential pilots",
                        "tracks first, then two housing pilots",
                        "tracks first",
                        "phased build",
                    ],
                    "hint_ru": "Какой поэтапный порядок одобрил мэр?",
                    "quote": "…tracks first, then two residential pilots…",
                    "model_en": "Tracks first, then two residential pilots.",
                },
            ],
            "plan": [
                "Corridor plan elements",
                "Public debate positions",
                "Budget gap and design mitigations",
                "Phased mayoral endorsement",
            ],
            "facts": [
                "The plan paired a tram extension with mid-rise housing above stations.",
                "Residents wanted reliable transport before denser blocks.",
                "Budget sheets showed a gap unless regional grants arrived by autumn.",
                "The mayor endorsed tracks first, then two residential pilots.",
            ],
        },
        "leadership": {
            "full_text": (
                "When two product squads stalled over ownership of a shared checkout service, Mira "
                "called an emergency leadership huddle rather than another ticket war. The team "
                "arrived defensive; a quiet conflict had already leaked into stand-ups and delayed "
                "a release. Mira refused to pick a winner on seniority alone and instead forced a "
                "written decision matrix: customer impact, maintenance load, and roadmap fit. After "
                "ninety minutes the group chose a single owning squad with a published interface "
                "contract and a rotating on-call from the other side. The outcome was imperfect—some "
                "engineers still felt overruled—yet the arrangement held through the next launch. Mira "
                "later noted that calm facilitation here meant ending ambiguity faster than it bred "
                "resentment."
            ),
            "gapped_text": (
                "When two product squads stalled over ownership of a shared checkout service, Mira "
                "called an emergency (1)___ huddle rather than another ticket war. The (2)___ "
                "arrived defensive; a quiet (3)___ had already leaked into stand-ups and delayed "
                "a release. Mira refused to pick a winner on seniority alone and instead forced a "
                "written (4)___ matrix: customer impact, maintenance load, and roadmap fit. After "
                "ninety minutes the group chose a single owning squad with a published interface "
                "contract and a rotating on-call from the other side. The meeting's (5)___ was imperfect—some "
                "engineers still felt overruled—yet the arrangement held through the next launch. Mira "
                "later noted that calm facilitation here meant ending ambiguity faster than it bred "
                "resentment."
            ),
            "answers": ["leadership", "team", "conflict", "decision", "outcome"],
            "word_bank": ["leadership", "team", "conflict", "decision", "outcome", "bonus"],
            "questions": [
                {
                    "q": "What were the two squads arguing over?",
                    "accept": [
                        "ownership of a shared checkout service",
                        "checkout service ownership",
                        "shared checkout service",
                    ],
                    "hint_ru": "Из-за чего спорили команды?",
                    "quote": "…ownership of a shared checkout service…",
                    "model_en": "Ownership of a shared checkout service.",
                },
                {
                    "q": "What three criteria were in the decision matrix?",
                    "accept": [
                        "customer impact, maintenance load, and roadmap fit",
                        "customer impact",
                        "maintenance load",
                        "roadmap fit",
                    ],
                    "hint_ru": "Какие три критерия в матрице?",
                    "quote": "…customer impact, maintenance load, and roadmap fit.",
                    "model_en": "Customer impact, maintenance load, and roadmap fit.",
                },
                {
                    "q": "What arrangement did the group choose after ninety minutes?",
                    "accept": [
                        "a single owning squad with a published interface contract and rotating on-call",
                        "single owning squad",
                        "rotating on-call",
                    ],
                    "hint_ru": "Какое решение приняли?",
                    "quote": "…a single owning squad with a published interface contract and a rotating on-call…",
                    "model_en": "One owning squad, a published interface contract, and rotating on-call.",
                },
                {
                    "q": "Did the decision hold through the next launch?",
                    "accept": ["yes", "the arrangement held", "held through the next launch", "the decision held"],
                    "hint_ru": "Удержалось ли решение до следующего релиза?",
                    "quote": "…the arrangement held through the next launch.",
                    "model_en": "Yes, the arrangement held through the next launch.",
                },
            ],
            "plan": [
                "Ownership conflict between squads",
                "Leadership huddle instead of ticket war",
                "Decision matrix and chosen ownership model",
                "Imperfect outcome that still held",
            ],
            "facts": [
                "Two squads stalled over shared checkout ownership.",
                "A quiet conflict had leaked into stand-ups and delayed a release.",
                "Mira used a decision matrix: impact, maintenance, roadmap fit.",
                "One squad owned the service; the other provided rotating on-call.",
            ],
        },
    },
}
