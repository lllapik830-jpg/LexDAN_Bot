# -*- coding: utf-8 -*-
"""Curated C2 Reading packs — sophisticated on-topic texts (not seminar templates)."""

from __future__ import annotations

PACKS: dict[str, dict[str, dict]] = {
    "C2": {
        "board": {
            "full_text": (
                "At the quarterly board meeting, the non-executive directors challenged the CEO "
                "on whether a rapid acquisition served long-term value or merely short-term optics. "
                "The CFO presented downside scenarios in which regulatory delay and integration "
                "friction could erase projected synergies within eighteen months. Marketing "
                "warned that aggressive messaging might trigger a PR backlash among institutional "
                "investors already uneasy about leverage. Strategy, they argued, had to privilege "
                "resilience over headline growth: retaining cash for contingencies rather than "
                "stretching the balance sheet. After a tense exchange, the board approved a "
                "conditional offer subject to stricter risk covenants and an independent review "
                "of cultural fit. Minutes recorded that any breach of those covenants would "
                "trigger an automatic pause, not a quiet renegotiation behind closed doors."
            ),
            "gapped_text": (
                "At the quarterly board meeting, the non-executive directors challenged the CEO "
                "on whether a rapid acquisition served long-term (1)___ or merely short-term optics. "
                "The CFO presented downside scenarios in which regulatory delay and integration "
                "friction could erase projected synergies within eighteen months. Marketing "
                "warned that aggressive messaging might trigger a (2)___ backlash among institutional "
                "investors already uneasy about leverage. (3)___, they argued, had to privilege "
                "resilience over headline growth: retaining cash for contingencies rather than "
                "stretching the balance sheet. After a tense exchange, the board approved a "
                "conditional offer subject to stricter (4)___ covenants and an independent review "
                "of cultural fit. Minutes recorded that any breach of those covenants would "
                "trigger an automatic (5)___, not a quiet renegotiation behind closed doors."
            ),
            "answers": ["value", "PR", "Strategy", "risk", "pause"],
            "word_bank": ["value", "PR", "Strategy", "risk", "pause", "dividend"],
            "questions": [
                {
                    "q": "What concern did non-executive directors raise about the acquisition?",
                    "accept": [
                        "long-term value vs short-term optics",
                        "short-term optics",
                        "long-term value",
                        "optics",
                    ],
                    "hint_ru": "Что ставили под сомнение неисполнительные директора?",
                    "quote": "…served long-term value or merely short-term optics.",
                    "model_en": "They questioned whether it served long-term value or only short-term optics.",
                },
                {
                    "q": "What did Marketing warn could happen among investors?",
                    "accept": [
                        "PR backlash",
                        "a PR backlash",
                        "backlash",
                        "public relations backlash",
                    ],
                    "hint_ru": "О чём предупредил маркетинг?",
                    "quote": "…might trigger a PR backlash among institutional investors…",
                    "model_en": "Marketing warned of a PR backlash among institutional investors.",
                },
                {
                    "q": "What condition was attached to the board's approval?",
                    "accept": [
                        "stricter risk covenants",
                        "risk covenants",
                        "conditional offer",
                        "independent review",
                    ],
                    "hint_ru": "На каких условиях совет одобрил предложение?",
                    "quote": "…approved a conditional offer subject to stricter risk covenants…",
                    "model_en": "Approval was conditional on stricter risk covenants and an independent review.",
                },
                {
                    "q": "What would a breach of the covenants trigger?",
                    "accept": [
                        "an automatic pause",
                        "automatic pause",
                        "a pause",
                        "pause",
                    ],
                    "hint_ru": "Что произойдёт при нарушении ковенантов?",
                    "quote": "…would trigger an automatic pause…",
                    "model_en": "A breach would trigger an automatic pause.",
                },
            ],
            "plan": [
                "Challenge to the acquisition's rationale",
                "Financial and PR risks raised",
                "Preference for resilience over growth",
                "Conditional approval and pause mechanism",
            ],
            "facts": [
                "Non-executives questioned long-term value versus short-term optics.",
                "CFO flagged regulatory delay and integration friction; Marketing feared a PR backlash.",
                "Strategy favoured cash resilience over leverage-driven growth.",
                "The board approved a conditional offer with risk covenants; breach triggers an automatic pause.",
            ],
        },
        "policy": {
            "full_text": (
                "The draft housing brief conceded that rent caps might please tenants yet "
                "distort incentives for landlords to maintain and expand supply. Officials "
                "mapped stakeholders carefully: municipal planners sought denser zoning, "
                "developers demanded predictability, and community groups insisted on "
                "affordable units near transit. Evidence from neighbouring cities suggested "
                "unintended effects — informal subletting, deferred repairs, and a flight of "
                "capital into holiday lets. The recommended package therefore paired modest "
                "caps with tax credits for long-term leases and faster permits for mid-rise "
                "projects. Ministers were urged to publish a monitoring dashboard so that "
                "policy could be adjusted before political pressure froze a flawed design "
                "in place. Without such feedback, the brief warned, goodwill would evaporate "
                "faster than any waiting list could shrink."
            ),
            "gapped_text": (
                "The draft housing brief conceded that rent caps might please tenants yet "
                "distort (1)___ for landlords to maintain and expand supply. Officials "
                "mapped (2)___ carefully: municipal planners sought denser zoning, "
                "developers demanded predictability, and community groups insisted on "
                "affordable units near transit. Evidence from neighbouring cities suggested "
                "(3)___ effects — informal subletting, deferred repairs, and a flight of "
                "capital into holiday lets. The recommended package therefore paired modest "
                "caps with tax credits for long-term leases and faster permits for mid-rise "
                "projects. Ministers were urged to publish a monitoring dashboard so that "
                "(4)___ could be adjusted before political pressure froze a flawed design "
                "in place. Without such feedback, the brief warned, goodwill would evaporate "
                "faster than any waiting (5)___ could shrink."
            ),
            "answers": ["incentives", "stakeholders", "unintended", "policy", "list"],
            "word_bank": ["incentives", "stakeholders", "unintended", "policy", "list", "subsidy"],
            "questions": [
                {
                    "q": "What risk do rent caps pose for landlords according to the brief?",
                    "accept": [
                        "distort incentives",
                        "distort incentives for landlords",
                        "incentives to maintain and expand supply",
                        "reduce supply incentives",
                    ],
                    "hint_ru": "Как потолки аренды влияют на стимулы арендодателей?",
                    "quote": "…distort incentives for landlords to maintain and expand supply.",
                    "model_en": "They may distort incentives for landlords to maintain and expand supply.",
                },
                {
                    "q": "Name one unintended effect observed in neighbouring cities.",
                    "accept": [
                        "informal subletting",
                        "deferred repairs",
                        "flight of capital into holiday lets",
                        "holiday lets",
                        "subletting",
                    ],
                    "hint_ru": "Какой побочный эффект уже видели в соседних городах?",
                    "quote": "…informal subletting, deferred repairs, and a flight of capital…",
                    "model_en": "Examples include informal subletting, deferred repairs, or capital fleeing into holiday lets.",
                },
                {
                    "q": "What did the recommended package pair with modest rent caps?",
                    "accept": [
                        "tax credits for long-term leases",
                        "tax credits",
                        "faster permits",
                        "tax credits and faster permits",
                    ],
                    "hint_ru": "С чем сочетали умеренные потолки аренды?",
                    "quote": "…paired modest caps with tax credits for long-term leases and faster permits…",
                    "model_en": "It paired modest caps with tax credits for long-term leases and faster permits.",
                },
                {
                    "q": "Why should ministers publish a monitoring dashboard?",
                    "accept": [
                        "so policy could be adjusted",
                        "adjust policy",
                        "adjust before political pressure",
                        "to adjust policy",
                    ],
                    "hint_ru": "Зачем нужен мониторинговый дашборд?",
                    "quote": "…so that policy could be adjusted before political pressure froze a flawed design…",
                    "model_en": "So that policy could be adjusted before politics froze a flawed design.",
                },
            ],
            "plan": [
                "Trade-off of rent caps and landlord incentives",
                "Stakeholder map and unintended effects",
                "Recommended mixed package",
                "Monitoring to allow policy adjustment",
            ],
            "facts": [
                "Rent caps may distort landlords' incentives to maintain and expand supply.",
                "Stakeholders include planners, developers, and community groups; unintended effects include subletting and holiday lets.",
                "The package pairs modest caps with tax credits and faster mid-rise permits.",
                "A monitoring dashboard is urged so policy can be adjusted before politics locks errors in.",
            ],
        },
        "lit": {
            "full_text": (
                "In her slim review of the coastal novella, Mira argued that the central theme "
                "is not nostalgia but the ethics of witnessing: who is entitled to narrate "
                "a drowning town. The narrator's tone shifts from wry detachment to something "
                "almost liturgical whenever the tide tables appear, a rhythm that critics "
                "once dismissed as ornamental. Mira instead reads the recurring lighthouse "
                "as symbolism of withheld rescue — light without intervention. Her critique "
                "is sharpest where the plot romanticises silence: the absent father's letters "
                "are beautiful, she grants, yet they excuse complicity rather than expose it. "
                "Still, she praises the prose for refusing neat catharsis. The review closes "
                "by urging readers to sit with unresolved grief instead of hunting for a "
                "moral that the text deliberately withholds."
            ),
            "gapped_text": (
                "In her slim review of the coastal novella, Mira argued that the central (1)___ "
                "is not nostalgia but the ethics of witnessing: who is entitled to narrate "
                "a drowning town. The narrator's (2)___ shifts from wry detachment to something "
                "almost liturgical whenever the tide tables appear, a rhythm that critics "
                "once dismissed as ornamental. Mira instead reads the recurring lighthouse "
                "as (3)___ of withheld rescue — light without intervention. Her (4)___ "
                "is sharpest where the plot romanticises silence: the absent father's letters "
                "are beautiful, she grants, yet they excuse complicity rather than expose it. "
                "Still, she praises the prose for refusing neat catharsis. The review closes "
                "by urging readers to sit with unresolved grief instead of hunting for a "
                "(5)___ that the text deliberately withholds."
            ),
            "answers": ["theme", "tone", "symbolism", "critique", "moral"],
            "word_bank": ["theme", "tone", "symbolism", "critique", "moral", "epilogue"],
            "questions": [
                {
                    "q": "What does Mira say the central theme is?",
                    "accept": [
                        "ethics of witnessing",
                        "the ethics of witnessing",
                        "witnessing",
                        "who is entitled to narrate",
                    ],
                    "hint_ru": "Какова, по Мире, центральная тема?",
                    "quote": "…the central theme is not nostalgia but the ethics of witnessing…",
                    "model_en": "She says the central theme is the ethics of witnessing.",
                },
                {
                    "q": "How does the narrator's tone change when tide tables appear?",
                    "accept": [
                        "from wry detachment to almost liturgical",
                        "wry detachment to liturgical",
                        "becomes liturgical",
                        "almost liturgical",
                    ],
                    "hint_ru": "Как меняется тон рассказчика у таблиц приливов?",
                    "quote": "…tone shifts from wry detachment to something almost liturgical…",
                    "model_en": "It shifts from wry detachment to something almost liturgical.",
                },
                {
                    "q": "What does Mira say the lighthouse symbolises?",
                    "accept": [
                        "withheld rescue",
                        "light without intervention",
                        "rescue withheld",
                        "withheld rescue — light without intervention",
                    ],
                    "hint_ru": "Что символизирует маяк?",
                    "quote": "…symbolism of withheld rescue — light without intervention.",
                    "model_en": "It symbolises withheld rescue: light without intervention.",
                },
                {
                    "q": "Why does Mira criticise the father's letters?",
                    "accept": [
                        "they excuse complicity",
                        "excuse complicity rather than expose it",
                        "romanticises silence",
                        "excuse complicity",
                    ],
                    "hint_ru": "За что она критикует письма отца?",
                    "quote": "…they excuse complicity rather than expose it.",
                    "model_en": "She says they excuse complicity rather than expose it.",
                },
            ],
            "plan": [
                "Central theme: ethics of witnessing",
                "Tone shift and lighthouse symbolism",
                "Critique of romanticised silence",
                "Refusal of neat moral closure",
            ],
            "facts": [
                "Mira locates the theme in the ethics of witnessing, not nostalgia.",
                "Tone turns almost liturgical at tide tables; the lighthouse symbolises withheld rescue.",
                "Her critique targets silence that excuses complicity, including the father's letters.",
                "She praises the refusal of neat catharsis and a withheld moral.",
            ],
        },
        "finance": {
            "full_text": (
                "Tuesday's note to clients opened with a blunt admission: equity markets had "
                "priced a soft landing too neatly, leaving little cushion against fresh "
                "volatility in energy and currency pairs. The desk expected policy rates to "
                "stay restrictive longer than consensus forecasts implied, which would keep "
                "refinancing costs elevated for highly leveraged issuers across emerging "
                "and developed markets alike. Their baseline outlook still favoured selective "
                "credit over broad equity beta, but only with explicit hedges on duration "
                "and foreign exchange. Caution, the strategists insisted, was not pessimism; "
                "it was recognition that liquidity could vanish faster than models assumed "
                "once margin calls cascaded through prime brokerage. Positions were trimmed "
                "in cyclical names and rotated toward shorter-duration sovereign paper until "
                "clearer data arrived on wage growth and inventory rebuilds."
            ),
            "gapped_text": (
                "Tuesday's note to clients opened with a blunt admission: equity markets had "
                "priced a soft landing too neatly, leaving little cushion against fresh "
                "(1)___ in energy and currency pairs. The desk expected policy (2)___ to "
                "stay restrictive longer than consensus forecasts implied, which would keep "
                "refinancing costs elevated for highly leveraged issuers across emerging "
                "and developed markets alike. Their baseline (3)___ still favoured selective "
                "credit over broad equity beta, but only with explicit hedges on duration "
                "and foreign exchange. (4)___, the strategists insisted, was not pessimism; "
                "it was recognition that liquidity could vanish faster than models assumed "
                "once margin calls cascaded through prime brokerage. Positions were trimmed "
                "in cyclical names and rotated toward shorter-duration sovereign paper until "
                "clearer (5)___ arrived on wage growth and inventory rebuilds."
            ),
            "answers": ["volatility", "rates", "outlook", "Caution", "data"],
            "word_bank": ["volatility", "rates", "outlook", "Caution", "data", "dividend"],
            "questions": [
                {
                    "q": "What had equity markets priced too neatly?",
                    "accept": [
                        "a soft landing",
                        "soft landing",
                        "soft landing too neatly",
                    ],
                    "hint_ru": "Что рынки акций заложили слишком гладко?",
                    "quote": "…equity markets had priced a soft landing too neatly…",
                    "model_en": "They had priced a soft landing too neatly.",
                },
                {
                    "q": "How long did the desk expect policy rates to stay restrictive?",
                    "accept": [
                        "longer than consensus",
                        "longer than consensus forecasts",
                        "longer than forecasts implied",
                        "longer than consensus forecasts implied",
                    ],
                    "hint_ru": "Как долго, по мнению деска, ставки останутся жёсткими?",
                    "quote": "…policy rates to stay restrictive longer than consensus forecasts implied…",
                    "model_en": "Longer than consensus forecasts implied.",
                },
                {
                    "q": "What did their baseline outlook favour?",
                    "accept": [
                        "selective credit over broad equity beta",
                        "selective credit",
                        "credit over equity beta",
                    ],
                    "hint_ru": "Что предпочитал базовый outlook?",
                    "quote": "…outlook still favoured selective credit over broad equity beta…",
                    "model_en": "It favoured selective credit over broad equity beta.",
                },
                {
                    "q": "Where were positions rotated after trimming cyclicals?",
                    "accept": [
                        "shorter-duration sovereign paper",
                        "sovereign paper",
                        "shorter-duration sovereign",
                    ],
                    "hint_ru": "Куда переложили позиции после сокращения циклических бумаг?",
                    "quote": "…rotated toward shorter-duration sovereign paper…",
                    "model_en": "Toward shorter-duration sovereign paper.",
                },
            ],
            "plan": [
                "Soft-landing pricing and volatility risk",
                "Restrictive rates and refinancing costs",
                "Outlook: selective credit with hedges",
                "Rotation into shorter sovereign paper",
            ],
            "facts": [
                "Markets had priced a soft landing with little cushion against volatility.",
                "Policy rates were expected to stay restrictive longer than consensus implied.",
                "Baseline outlook favoured selective credit with hedges; caution ≠ pessimism.",
                "Cyclicals were trimmed in favour of shorter-duration sovereign paper pending clearer data.",
            ],
        },
        "diplomacy": {
            "full_text": (
                "The communiqué after midnight talks avoided naming the disputed corridor, "
                "substituting a studied ambiguity that both capitals could sell as progress "
                "to restless domestic audiences. Negotiators spent hours on wording: whether "
                "'provisional access' implied recognition, and whether 'security guarantees' "
                "bound third parties not present at the table. National interests remained "
                "asymmetrical — one side sought trade corridors, the other buffer zones — "
                "yet neither could afford a public rupture before elections. A narrow "
                "compromise emerged: observers for ninety days, a freeze on new "
                "fortifications, and a technical committee on customs and water rights. "
                "Envoys privately conceded the deal was fragile, but argued that silence "
                "had become more dangerous than an imperfect text. The note closed with a "
                "pledge to resume negotiations within a fortnight if verification stalled."
            ),
            "gapped_text": (
                "The communiqué after midnight (1)___ avoided naming the disputed corridor, "
                "substituting a studied ambiguity that both capitals could sell as progress "
                "to restless domestic audiences. Negotiators spent hours on (2)___: whether "
                "'provisional access' implied recognition, and whether 'security guarantees' "
                "bound third parties not present at the table. National (3)___ remained "
                "asymmetrical — one side sought trade corridors, the other buffer zones — "
                "yet neither could afford a public rupture before elections. A narrow "
                "(4)___ emerged: observers for ninety days, a freeze on new "
                "fortifications, and a technical committee on customs and water rights. "
                "Envoys privately conceded the deal was fragile, but argued that silence "
                "had become more dangerous than an imperfect text. The note closed with a "
                "pledge to resume negotiations within a fortnight if (5)___ stalled."
            ),
            "answers": ["talks", "wording", "interests", "compromise", "verification"],
            "word_bank": ["talks", "wording", "interests", "compromise", "verification", "embargo"],
            "questions": [
                {
                    "q": "What did the communiqué avoid naming?",
                    "accept": [
                        "the disputed corridor",
                        "disputed corridor",
                        "corridor",
                    ],
                    "hint_ru": "Что коммюнике намеренно не назвало?",
                    "quote": "…avoided naming the disputed corridor…",
                    "model_en": "It avoided naming the disputed corridor.",
                },
                {
                    "q": "What asymmetrical interests did the two sides pursue?",
                    "accept": [
                        "trade corridors and buffer zones",
                        "trade corridors / buffer zones",
                        "trade corridors",
                        "buffer zones",
                    ],
                    "hint_ru": "Какие асимметричные интересы были у сторон?",
                    "quote": "…one side sought trade corridors, the other buffer zones…",
                    "model_en": "One sought trade corridors; the other sought buffer zones.",
                },
                {
                    "q": "What elements made up the narrow compromise?",
                    "accept": [
                        "observers, freeze, customs committee",
                        "observers for ninety days",
                        "freeze on fortifications",
                        "observers, freeze on fortifications, technical committee",
                    ],
                    "hint_ru": "Из чего состоял узкий компромисс?",
                    "quote": "…observers for ninety days, a freeze on new fortifications, and a technical committee…",
                    "model_en": "Observers for ninety days, a freeze on fortifications, and a customs committee.",
                },
                {
                    "q": "When would talks resume if verification stalled?",
                    "accept": [
                        "within a fortnight",
                        "in a fortnight",
                        "fortnight",
                        "within two weeks",
                    ],
                    "hint_ru": "Когда возобновят переговоры, если верификация застопорится?",
                    "quote": "…resume negotiations within a fortnight if verification stalled.",
                    "model_en": "Within a fortnight.",
                },
            ],
            "plan": [
                "Ambiguous communiqué after midnight talks",
                "Disputes over wording and asymmetrical interests",
                "Narrow compromise package",
                "Pledge to resume if verification stalls",
            ],
            "facts": [
                "Midnight talks produced ambiguity instead of naming the disputed corridor.",
                "Hours went into wording; national interests were trade corridors vs buffer zones.",
                "Compromise: ninety-day observers, freeze on fortifications, customs committee.",
                "Talks would resume within a fortnight if verification stalled.",
            ],
        },
        "science": {
            "full_text": (
                "The laboratory's public briefing on the antiviral trial stressed what the "
                "data could and could not show. Preliminary evidence suggested a meaningful "
                "reduction in hospitalisation among high-risk adults, yet sample sizes for "
                "older cohorts remained thin and secondary endpoints were exploratory. "
                "Researchers foregrounded uncertainty rather than burying confidence "
                "intervals in an appendix, arguing that public trust erodes when caveats "
                "arrive only after headlines have hardened into certainty. Journalists were "
                "given access to anonymised protocols and invited to ask how endpoints had "
                "been pre-registered before unblinding. The director refused to call the "
                "compound a breakthrough, preferring 'promising under defined conditions.' "
                "She noted that replication across climates and comorbidities would decide "
                "whether the signal survived outside controlled wards and specialised hospital ICUs."
            ),
            "gapped_text": (
                "The laboratory's public briefing on the antiviral trial stressed what the "
                "data could and could not show. Preliminary (1)___ suggested a meaningful "
                "reduction in hospitalisation among high-risk adults, yet sample sizes for "
                "older cohorts remained thin and secondary endpoints were exploratory. "
                "Researchers foregrounded (2)___ rather than burying confidence "
                "intervals in an appendix, arguing that public (3)___ erodes when caveats "
                "arrive only after headlines have hardened into certainty. Journalists were "
                "given access to anonymised protocols and invited to ask how endpoints had "
                "been pre-registered before unblinding. The director refused to call the "
                "compound a breakthrough, preferring 'promising under defined conditions.' "
                "She noted that (4)___ across climates and comorbidities would decide "
                "whether the (5)___ survived outside controlled wards and specialised hospital ICUs."
            ),
            "answers": ["evidence", "uncertainty", "trust", "replication", "signal"],
            "word_bank": ["evidence", "uncertainty", "trust", "replication", "signal", "patent"],
            "questions": [
                {
                    "q": "What did preliminary evidence suggest?",
                    "accept": [
                        "reduction in hospitalisation",
                        "meaningful reduction in hospitalisation",
                        "fewer hospitalisations among high-risk adults",
                        "hospitalisation reduction",
                    ],
                    "hint_ru": "На что указывали предварительные данные?",
                    "quote": "…meaningful reduction in hospitalisation among high-risk adults…",
                    "model_en": "A meaningful reduction in hospitalisation among high-risk adults.",
                },
                {
                    "q": "Why did researchers foreground uncertainty?",
                    "accept": [
                        "public trust erodes when caveats arrive after headlines",
                        "public trust",
                        "trust erodes",
                        "caveats after headlines",
                    ],
                    "hint_ru": "Почему учёные выносили неопределённость на первый план?",
                    "quote": "…public trust erodes when caveats arrive only after headlines.",
                    "model_en": "Because public trust erodes when caveats arrive only after headlines.",
                },
                {
                    "q": "How did the director describe the compound?",
                    "accept": [
                        "promising under defined conditions",
                        "not a breakthrough",
                        "refused to call it a breakthrough",
                    ],
                    "hint_ru": "Как директор назвала препарат?",
                    "quote": "…preferring 'promising under defined conditions.'",
                    "model_en": "She preferred 'promising under defined conditions,' not 'breakthrough.'",
                },
                {
                    "q": "What would decide whether the signal survived outside wards?",
                    "accept": [
                        "replication across climates and comorbidities",
                        "replication",
                        "replication across climates",
                    ],
                    "hint_ru": "Что решит, сохранится ли сигнал вне палат?",
                    "quote": "…replication across climates and comorbidities would decide…",
                    "model_en": "Replication across climates and comorbidities.",
                },
            ],
            "plan": [
                "What trial data can and cannot show",
                "Foregrounding uncertainty for public trust",
                "Access to protocols and careful wording",
                "Need for replication beyond controlled wards",
            ],
            "facts": [
                "Preliminary evidence suggested reduced hospitalisation in high-risk adults; older cohorts were thin.",
                "Researchers foregrounded uncertainty to protect public trust.",
                "The director called the compound promising under defined conditions, not a breakthrough.",
                "Replication across climates and comorbidities would test whether the signal survived.",
            ],
        },
        "art": {
            "full_text": (
                "The biennale essay on the mirrored plaza installation refuses a single "
                "interpretation, inviting visitors to treat reflection as both vanity and "
                "surveillance under a civic sky. Context matters: the plaza once hosted "
                "immigration hearings, and the polished steel still catches courthouse "
                "windows at dusk, folding bureaucracy into the spectacle. Controversy "
                "erupted when a sponsor demanded softer lighting after protesters used the "
                "mirrors to project slogans overnight. Curators held firm, arguing that "
                "sanitising the work would convert critique into décor for weekend tourism. "
                "Critics split between those who saw manipulative spectacle and those who "
                "praised the piece for making complicity visible to ordinary pedestrians. "
                "The essay concludes that contemporary art rarely settles arguments; it "
                "stages them where passers-by cannot pretend neutrality."
            ),
            "gapped_text": (
                "The biennale essay on the mirrored plaza installation refuses a single "
                "(1)___, inviting visitors to treat reflection as both vanity and "
                "surveillance under a civic sky. (2)___ matters: the plaza once hosted "
                "immigration hearings, and the polished steel still catches courthouse "
                "windows at dusk, folding bureaucracy into the spectacle. (3)___ "
                "erupted when a sponsor demanded softer lighting after protesters used the "
                "mirrors to project slogans overnight. Curators held firm, arguing that "
                "sanitising the work would convert critique into décor for weekend tourism. "
                "Critics split between those who saw manipulative spectacle and those who "
                "praised the piece for making complicity visible to ordinary pedestrians. "
                "The essay concludes that contemporary (4)___ rarely settles arguments; it "
                "stages them where passers-by cannot pretend (5)___."
            ),
            "answers": ["interpretation", "Context", "Controversy", "art", "neutrality"],
            "word_bank": ["interpretation", "Context", "Controversy", "art", "neutrality", "auction"],
            "questions": [
                {
                    "q": "How does the essay invite visitors to treat reflection?",
                    "accept": [
                        "as both vanity and surveillance",
                        "vanity and surveillance",
                        "vanity",
                        "surveillance",
                    ],
                    "hint_ru": "Как эссе предлагает воспринимать отражение?",
                    "quote": "…treat reflection as both vanity and surveillance.",
                    "model_en": "As both vanity and surveillance.",
                },
                {
                    "q": "What historical use of the plaza does the essay mention?",
                    "accept": [
                        "immigration hearings",
                        "hosted immigration hearings",
                        "hearings",
                    ],
                    "hint_ru": "Какое историческое использование площади упоминается?",
                    "quote": "…the plaza once hosted immigration hearings…",
                    "model_en": "It once hosted immigration hearings.",
                },
                {
                    "q": "Why did controversy erupt with the sponsor?",
                    "accept": [
                        "demanded softer lighting",
                        "softer lighting after protesters",
                        "sponsor demanded softer lighting",
                        "protesters projected slogans",
                    ],
                    "hint_ru": "Из-за чего разгорелся спор со спонсором?",
                    "quote": "…sponsor demanded softer lighting after protesters used the mirrors…",
                    "model_en": "The sponsor demanded softer lighting after protesters projected slogans.",
                },
                {
                    "q": "What do curators say sanitising the work would do?",
                    "accept": [
                        "convert critique into décor",
                        "turn critique into décor",
                        "critique into décor",
                    ],
                    "hint_ru": "Во что, по кураторам, превратится критика при «смягчении» работы?",
                    "quote": "…sanitising the work would convert critique into décor.",
                    "model_en": "It would convert critique into décor.",
                },
            ],
            "plan": [
                "Refusal of a single interpretation",
                "Historical context of the plaza",
                "Sponsor controversy and curatorial stance",
                "Art as staging unresolved arguments",
            ],
            "facts": [
                "Reflection is framed as vanity and surveillance; no single interpretation.",
                "Context: former immigration hearings; steel catches courthouse windows.",
                "Controversy after a sponsor sought softer lighting post-protest projections.",
                "Curators refused sanitising; the essay says art stages arguments, not settles them.",
            ],
        },
        "philosophy": {
            "full_text": (
                "The seminar on the trolley variant asked whether rescue drones should "
                "prioritise the many strangers or the single identified child whose face "
                "fills the live feed during a flood. Students defending utilitarianism "
                "cited aggregate consequences, while deontologists insisted that some "
                "principles forbid treating any person as expendable arithmetic for the "
                "sake of a cleaner spreadsheet. A third camp stressed judgment under "
                "uncertainty: operators rarely know probabilities cleanly, so moral "
                "theory must leave room for tragic choice without demanding omniscience. "
                "The tutor refused a neat ranking, noting that public institutions still "
                "need decision rules even when philosophy remains divided in the seminar "
                "room. Homework required each student to state which principle they "
                "would stake a career on — and which results they were prepared "
                "to own if that principle failed in the field."
            ),
            "gapped_text": (
                "The seminar on the trolley variant asked whether rescue drones should "
                "prioritise the many strangers or the single identified child whose face "
                "fills the live feed during a flood. Students defending utilitarianism "
                "cited aggregate (1)___, while deontologists insisted that some "
                "(2)___ forbid treating any person as expendable arithmetic for the "
                "sake of a cleaner spreadsheet. A third camp stressed (3)___ under "
                "uncertainty: operators rarely know probabilities cleanly, so moral "
                "theory must leave room for tragic choice without demanding omniscience. "
                "The tutor refused a neat ranking, noting that public institutions still "
                "need decision rules even when philosophy remains divided in the seminar "
                "room. Homework required each student to state which principle they "
                "would stake a career on — and which results they were prepared "
                "to (4)___ if that principle failed in the (5)___."
            ),
            "answers": ["consequences", "principles", "judgment", "own", "field"],
            "word_bank": ["consequences", "principles", "judgment", "own", "field", "syllabus"],
            "questions": [
                {
                    "q": "What dilemma did the trolley-variant seminar pose for rescue drones?",
                    "accept": [
                        "many strangers or single identified child",
                        "prioritise the many or the child",
                        "many strangers vs identified child",
                        "strangers or child",
                    ],
                    "hint_ru": "Какую дилемму ставил семинар для дронов спасения?",
                    "quote": "…prioritise the many strangers or the single identified child…",
                    "model_en": "Whether to prioritise many strangers or one identified child.",
                },
                {
                    "q": "What did deontologists insist some principles forbid?",
                    "accept": [
                        "treating any person as expendable arithmetic",
                        "expendable arithmetic",
                        "treating a person as expendable",
                    ],
                    "hint_ru": "Что, по деонтологам, запрещают некоторые принципы?",
                    "quote": "…forbid treating any person as expendable arithmetic.",
                    "model_en": "Treating any person as expendable arithmetic.",
                },
                {
                    "q": "What did the third camp stress?",
                    "accept": [
                        "judgment under uncertainty",
                        "judgment",
                        "tragic choice without omniscience",
                    ],
                    "hint_ru": "На чём настаивал третий лагерь?",
                    "quote": "A third camp stressed judgment under uncertainty…",
                    "model_en": "Judgment under uncertainty.",
                },
                {
                    "q": "What did homework ask students to stake a career on?",
                    "accept": [
                        "which principle",
                        "a principle",
                        "which principle they would stake a career on",
                        "principle and consequences they would own",
                    ],
                    "hint_ru": "Что домашнее задание просило «поставить на карту карьеры»?",
                    "quote": "…state which principle they would stake a career on…",
                    "model_en": "Which principle they would stake a career on — and which consequences they would own.",
                },
            ],
            "plan": [
                "Drone trolley dilemma setup",
                "Utilitarian vs deontological clash",
                "Judgment under uncertainty",
                "Homework: own a principle and its failures",
            ],
            "facts": [
                "The dilemma: many strangers versus one identified child on the feed.",
                "Utilitarians cited aggregate consequences; deontologists invoked non-expendable principles.",
                "A third camp stressed judgment under uncertainty without demanding omniscience.",
                "Students had to stake a career on a principle and own consequences if it failed in the field.",
            ],
        },
    }
}
