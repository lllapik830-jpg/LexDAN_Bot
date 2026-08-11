# -*- coding: utf-8 -*-
"""Curated Reading packs for A2 and B1."""

PACKS = {
    "A2": {
        "travel": {
            "full_text": (
                "Last Saturday Olga took a morning train to the sea. "
                "She bought a ticket at the station and put it in her bag. "
                "The journey lasted two hours, and she looked out of the window. "
                "In the town she found a small hotel near the beach. "
                "After lunch she went sightseeing with a free city map. "
                "She visited an old castle and took many photos. "
                "In the evening she walked along the coast and bought ice cream. "
                "On Sunday she packed her suitcase and returned home the same way. "
                "Olga said the trip was short but very nice."
            ),
            "gapped_text": (
                "Last Saturday Olga took a morning (1)___ to the sea. "
                "She bought a (2)___ at the station and put it in her bag. "
                "The journey lasted two hours, and she looked out of the window. "
                "In the town she found a small (3)___ near the beach. "
                "After lunch she went (4)___ with a free city map. "
                "She visited an old castle and took many photos. "
                "In the evening she walked along the coast and bought ice cream. "
                "On Sunday she packed her (5)___ and returned home the same way. "
                "Olga said the trip was short but very nice."
            ),
            "answers": ["train", "ticket", "hotel", "sightseeing", "suitcase"],
            "word_bank": ["train", "ticket", "hotel", "sightseeing", "suitcase", "airport"],
            "questions": [
                {
                    "q": "How did Olga travel to the sea?",
                    "accept": ["by train", "train", "morning train"],
                    "hint_ru": "На чём Ольга доехала до моря?",
                    "quote": "…took a morning train to the sea.",
                    "model_en": "Olga travelled by train.",
                },
                {
                    "q": "Where did she buy her ticket?",
                    "accept": ["at the station", "station"],
                    "hint_ru": "Где она купила билет?",
                    "quote": "…bought a ticket at the station…",
                    "model_en": "She bought her ticket at the station.",
                },
                {
                    "q": "Where was the hotel?",
                    "accept": ["near the beach", "by the beach", "beach"],
                    "hint_ru": "Где находился отель?",
                    "quote": "…a small hotel near the beach.",
                    "model_en": "The hotel was near the beach.",
                },
                {
                    "q": "What did she visit with the map?",
                    "accept": ["an old castle", "castle", "old castle"],
                    "hint_ru": "Что она посетила с картой?",
                    "quote": "She visited an old castle…",
                    "model_en": "She visited an old castle.",
                },
            ],
            "plan": [
                "Train journey and ticket",
                "Hotel near the beach",
                "Sightseeing and castle",
                "Sunday return home",
            ],
            "facts": [
                "Olga took a morning train and bought a ticket at the station.",
                "She stayed in a small hotel near the beach.",
                "She went sightseeing and visited an old castle.",
                "On Sunday she packed her suitcase and returned home the same way.",
            ],
        },
        "doctor": {
            "full_text": (
                "On Monday Tom woke up with a sore throat and a high temperature. "
                "His mother took him to the clinic after breakfast. "
                "The doctor asked about his symptoms and checked his throat. "
                "She said Tom had a cold and needed rest at home. "
                "Then she wrote a prescription for medicine and cough syrup. "
                "Tom must drink warm tea and sleep more for three days. "
                "He should not go to football practice this week. "
                "At the pharmacy they bought the syrup and went home. "
                "By Thursday Tom felt much better and smiled again."
            ),
            "gapped_text": (
                "On Monday Tom woke up with a sore throat and a high temperature. "
                "His mother took him to the clinic after breakfast. "
                "The doctor asked about his (1)___ and checked his throat. "
                "She said Tom had a cold and needed (2)___ at home. "
                "Then she wrote a prescription for (3)___ and cough syrup. "
                "Tom must drink warm tea and sleep more for three days. "
                "He should not go to football (4)___ this week. "
                "At the pharmacy they bought the syrup and went home. "
                "By Thursday Tom felt much (5)___ and smiled again."
            ),
            "answers": ["symptoms", "rest", "medicine", "practice", "better"],
            "word_bank": ["symptoms", "rest", "medicine", "practice", "better", "injection"],
            "questions": [
                {
                    "q": "What was wrong with Tom on Monday?",
                    "accept": [
                        "sore throat and high temperature",
                        "sore throat",
                        "cold",
                        "high temperature",
                    ],
                    "hint_ru": "Что было не так с Томом в понедельник?",
                    "quote": "…sore throat and a high temperature.",
                    "model_en": "Tom had a sore throat and a high temperature.",
                },
                {
                    "q": "What did the doctor say Tom needed?",
                    "accept": ["rest", "rest at home", "needed rest"],
                    "hint_ru": "Что, по словам врача, нужно Тому?",
                    "quote": "…needed rest at home.",
                    "model_en": "The doctor said Tom needed rest at home.",
                },
                {
                    "q": "Where did they buy the medicine?",
                    "accept": ["at the pharmacy", "pharmacy"],
                    "hint_ru": "Где они купили лекарство?",
                    "quote": "At the pharmacy they bought the syrup…",
                    "model_en": "They bought the medicine at the pharmacy.",
                },
                {
                    "q": "When did Tom feel better?",
                    "accept": ["by Thursday", "Thursday"],
                    "hint_ru": "Когда Тому стало лучше?",
                    "quote": "By Thursday Tom felt much better…",
                    "model_en": "Tom felt better by Thursday.",
                },
            ],
            "plan": [
                "Symptoms and clinic visit",
                "Doctor's advice and medicine",
                "Rules at home",
                "Feeling better on Thursday",
            ],
            "facts": [
                "Tom had a sore throat and high temperature.",
                "The doctor checked symptoms and said he needed rest.",
                "They got medicine and cough syrup from the pharmacy.",
                "By Thursday Tom felt much better.",
            ],
        },
        "party": {
            "full_text": (
                "Sara invited ten guests to her birthday party on Friday evening. "
                "Her brother hung colourful balloons in the living room before anyone arrived. "
                "Friends brought gifts and a big chocolate cake with her name on top. "
                "Sara put snacks and lemonade on the long table near the window. "
                "They played music and danced for almost an hour. "
                "Later everyone sang for Sara and she blew out the candles. "
                "Mum took photos while Dad poured more lemonade for the children. "
                "At ten o'clock everyone said goodbye and went home happily. "
                "Sara thanked everyone and kept the thank-you cards near her bed."
            ),
            "gapped_text": (
                "Sara invited ten (1)___ to her birthday party on Friday evening. "
                "Her brother hung colourful balloons in the living room before anyone arrived. "
                "Friends brought (2)___ and a big chocolate cake with her name on top. "
                "Sara put snacks and lemonade on the long table near the window. "
                "They played (3)___ and danced for almost an hour. "
                "Later everyone sang for Sara and she blew out the (4)___. "
                "Mum took photos while Dad poured more lemonade for the children. "
                "At ten o'clock everyone said goodbye and went home happily. "
                "Sara thanked everyone and kept the thank-you (5)___ near her bed."
            ),
            "answers": ["guests", "gifts", "music", "candles", "cards"],
            "word_bank": ["guests", "gifts", "music", "candles", "cards", "fireworks"],
            "questions": [
                {
                    "q": "How many guests did Sara invite?",
                    "accept": ["ten", "10", "ten guests"],
                    "hint_ru": "Сколько гостей пригласила Сара?",
                    "quote": "Sara invited ten guests…",
                    "model_en": "Sara invited ten guests.",
                },
                {
                    "q": "What cake did friends bring?",
                    "accept": ["chocolate cake", "big chocolate cake", "chocolate"],
                    "hint_ru": "Какой торт принесли друзья?",
                    "quote": "…a big chocolate cake.",
                    "model_en": "Friends brought a big chocolate cake.",
                },
                {
                    "q": "What did they do while the music played?",
                    "accept": ["danced", "dance", "danced for almost an hour"],
                    "hint_ru": "Что они делали под музыку?",
                    "quote": "…played music and danced…",
                    "model_en": "They danced while the music played.",
                },
                {
                    "q": "When did the guests go home?",
                    "accept": ["at ten o'clock", "ten o'clock", "at ten", "10 o'clock"],
                    "hint_ru": "Когда гости ушли домой?",
                    "quote": "At ten o'clock everyone said goodbye…",
                    "model_en": "The guests went home at ten o'clock.",
                },
            ],
            "plan": [
                "Guests and decorations",
                "Gifts, cake and table",
                "Music, singing and candles",
                "Goodbye and thank-you cards",
            ],
            "facts": [
                "Sara invited ten guests on Friday evening.",
                "Friends brought gifts and a chocolate cake.",
                "They played music, danced and blew out candles.",
                "Everyone left at ten; Sara kept the thank-you cards.",
            ],
        },
        "sport": {
            "full_text": (
                "Every Tuesday Ben goes to the gym near his school after classes. "
                "He runs on the treadmill for twenty minutes first. "
                "Then he lifts light weights and stretches carefully. "
                "After training he feels tired but also healthy and strong. "
                "His coach says water and sleep are important for sport. "
                "On Thursdays Ben plays football with friends in the park. "
                "Last week he scored one goal and his team won the match. "
                "Ben wants to join a running club next month if he has time. "
                "He believes sport helps him study better at school."
            ),
            "gapped_text": (
                "Every Tuesday Ben goes to the (1)___ near his school after classes. "
                "He (2)___ on the treadmill for twenty minutes first. "
                "Then he lifts light weights and stretches carefully. "
                "After training he feels (3)___ but also healthy and strong. "
                "His coach says water and sleep are important for sport. "
                "On Thursdays Ben plays (4)___ with friends in the park. "
                "Last week he scored one goal and his team won the match. "
                "Ben wants to join a running (5)___ next month if he has time. "
                "He believes sport helps him study better at school."
            ),
            "answers": ["gym", "runs", "tired", "football", "club"],
            "word_bank": ["gym", "runs", "tired", "football", "club", "swimming"],
            "questions": [
                {
                    "q": "When does Ben go to the gym?",
                    "accept": ["every Tuesday", "Tuesday", "on Tuesday"],
                    "hint_ru": "Когда Бен ходит в спортзал?",
                    "quote": "Every Tuesday Ben goes to the gym…",
                    "model_en": "Ben goes to the gym every Tuesday.",
                },
                {
                    "q": "How long does he run on the treadmill?",
                    "accept": ["twenty minutes", "20 minutes", "for twenty minutes"],
                    "hint_ru": "Сколько он бегает на беговой дорожке?",
                    "quote": "…runs on the treadmill for twenty minutes…",
                    "model_en": "He runs for twenty minutes.",
                },
                {
                    "q": "What does he play on Thursdays?",
                    "accept": ["football", "plays football"],
                    "hint_ru": "Во что он играет по четвергам?",
                    "quote": "…plays football with friends…",
                    "model_en": "Ben plays football on Thursdays.",
                },
                {
                    "q": "What does Ben want to join next month?",
                    "accept": ["a running club", "running club", "club"],
                    "hint_ru": "Куда Бен хочет вступить в следующем месяце?",
                    "quote": "…join a running club next month.",
                    "model_en": "Ben wants to join a running club.",
                },
            ],
            "plan": [
                "Gym routine on Tuesday",
                "Feeling after training",
                "Football on Thursday",
                "Plans for a running club",
            ],
            "facts": [
                "Ben goes to the gym every Tuesday and runs twenty minutes.",
                "After training he feels tired but healthy.",
                "On Thursdays he plays football in the park.",
                "He wants to join a running club next month.",
            ],
        },
        "neighbours": {
            "full_text": (
                "Lena lives on the third floor next to a friendly family with two children. "
                "Sometimes in the evening she hears music through the wall. "
                "Last Friday the noise was loud, so she knocked politely on their door. "
                "Her neighbour Max apologised and turned the music down at once. "
                "On Saturday Max helped Lena carry a heavy box upstairs. "
                "Later Lena baked cookies and shared them with his flat. "
                "They often chat near the postboxes after work about the weather. "
                "Lena likes her neighbours because they are kind and quiet. "
                "Next week they will water plants for each other during holidays."
            ),
            "gapped_text": (
                "Lena lives on the third floor next to a friendly family with two children. "
                "Sometimes in the (1)___ she hears music through the wall. "
                "Last Friday the (2)___ was loud, so she knocked politely on their door. "
                "Her neighbour Max apologised and turned the music down at once. "
                "On Saturday Max helped Lena carry a heavy (3)___ upstairs. "
                "Later Lena baked cookies and shared them with his (4)___. "
                "They often chat near the postboxes after work about the weather. "
                "Lena likes her neighbours because they are kind and (5)___. "
                "Next week they will water plants for each other during holidays."
            ),
            "answers": ["evening", "noise", "box", "flat", "quiet"],
            "word_bank": ["evening", "noise", "box", "flat", "quiet", "angry"],
            "questions": [
                {
                    "q": "What does Lena sometimes hear through the wall?",
                    "accept": ["music", "hears music"],
                    "hint_ru": "Что Лена иногда слышит через стену?",
                    "quote": "…hears music through the wall.",
                    "model_en": "Lena sometimes hears music through the wall.",
                },
                {
                    "q": "What did Max do after Lena knocked?",
                    "accept": [
                        "apologised and turned the music down",
                        "turned the music down",
                        "apologised",
                    ],
                    "hint_ru": "Что сделал Макс после того, как Лена постучала?",
                    "quote": "…apologised and turned the music down.",
                    "model_en": "Max apologised and turned the music down.",
                },
                {
                    "q": "How did Max help Lena on Saturday?",
                    "accept": [
                        "carry a heavy box upstairs",
                        "helped carry a box",
                        "carried a box",
                    ],
                    "hint_ru": "Как Макс помог Лене в субботу?",
                    "quote": "…helped Lena carry a heavy box upstairs.",
                    "model_en": "Max helped Lena carry a heavy box upstairs.",
                },
                {
                    "q": "Why does Lena like her neighbours?",
                    "accept": ["kind and quiet", "they are kind and quiet", "kind"],
                    "hint_ru": "Почему Лене нравятся соседи?",
                    "quote": "…because they are kind and quiet.",
                    "model_en": "Lena likes her neighbours because they are kind and quiet.",
                },
            ],
            "plan": [
                "Evening music through the wall",
                "Polite talk about noise",
                "Help with a heavy box",
                "Cookies and friendly neighbours",
            ],
            "facts": [
                "Lena sometimes hears music in the evening.",
                "Max apologised and turned the music down.",
                "Max helped carry a heavy box; Lena shared cookies.",
                "She likes neighbours who are kind and quiet.",
            ],
        },
        "lost": {
            "full_text": (
                "Yesterday Mia lost her blue bag on the bus to town. "
                "Inside there was a purse, keys and a small notebook. "
                "She described it to the driver at the next stop. "
                "The colour was bright blue with a yellow zip. "
                "A passenger found it under a seat and gave it back. "
                "Mia checked everything and smiled with relief. "
                "She thanked the passenger and the driver many times. "
                "Then she wrote her phone number on a paper inside it. "
                "Now Mia is more careful when she travels alone."
            ),
            "gapped_text": (
                "Yesterday Mia lost her blue (1)___ on the bus to town. "
                "Inside there was a purse, keys and a small notebook. "
                "She (2)___ it to the driver at the next stop. "
                "The (3)___ was bright blue with a yellow zip. "
                "A passenger found it under a seat and gave it back. "
                "Mia checked everything and smiled with relief. "
                "She (4)___ the passenger and the driver many times. "
                "Then she wrote her phone number on a paper inside it. "
                "Now Mia is more careful when she (5)___ alone."
            ),
            "answers": ["bag", "described", "colour", "thanked", "travels"],
            "word_bank": ["bag", "described", "colour", "thanked", "travels", "wallet"],
            "questions": [
                {
                    "q": "Where did Mia lose her bag?",
                    "accept": ["on the bus", "bus", "on the bus to town"],
                    "hint_ru": "Где Миа потеряла сумку?",
                    "quote": "…lost her blue bag on the bus to town.",
                    "model_en": "Mia lost her bag on the bus.",
                },
                {
                    "q": "What colour was the bag?",
                    "accept": ["bright blue", "blue", "blue with a yellow zip"],
                    "hint_ru": "Какого цвета была сумка?",
                    "quote": "The colour was bright blue with a yellow zip.",
                    "model_en": "The bag was bright blue with a yellow zip.",
                },
                {
                    "q": "Who found the bag?",
                    "accept": ["a passenger", "passenger"],
                    "hint_ru": "Кто нашёл сумку?",
                    "quote": "A passenger found it under a seat…",
                    "model_en": "A passenger found the bag.",
                },
                {
                    "q": "What did Mia write inside the bag?",
                    "accept": ["her phone number", "phone number", "a phone number"],
                    "hint_ru": "Что Миа написала внутри сумки?",
                    "quote": "…wrote her phone number on a paper inside it.",
                    "model_en": "Mia wrote her phone number inside the bag.",
                },
            ],
            "plan": [
                "Lost bag on the bus",
                "Description to the driver",
                "Passenger finds it",
                "Thanks and phone number",
            ],
            "facts": [
                "Mia lost a blue bag on the bus.",
                "She described the colour: bright blue with a yellow zip.",
                "A passenger found it under a seat.",
                "Mia thanked them and wrote her phone number inside.",
            ],
        },
        "restaurant": {
            "full_text": (
                "Anna and Paul chose a small Italian restaurant downtown for dinner. "
                "A server gave them a menu and a glass of water right away. "
                "Anna ordered pasta with tomato sauce, and Paul ordered fish. "
                "They shared a salad and talked about their busy week at work. "
                "The food arrived quickly and tasted fresh and hot. "
                "After dessert Paul asked for the bill and left a tip. "
                "The total was forty pounds including service. "
                "They thanked the waiter and promised to return soon. "
                "Outside it was raining, so they took a taxi home together."
            ),
            "gapped_text": (
                "Anna and Paul chose a small Italian restaurant downtown for dinner. "
                "A server gave them a (1)___ and a glass of water right away. "
                "Anna ordered pasta with tomato sauce, and Paul ordered fish. "
                "They shared a salad and talked about their busy week at work. "
                "The food arrived quickly and tasted fresh and hot. "
                "After dessert Paul asked for the (2)___ and left a (3)___. "
                "The total was forty pounds including service. "
                "They thanked the (4)___ and promised to return soon. "
                "Outside it was raining, so they took a (5)___ home together."
            ),
            "answers": ["menu", "bill", "tip", "waiter", "taxi"],
            "word_bank": ["menu", "bill", "tip", "waiter", "taxi", "kitchen"],
            "questions": [
                {
                    "q": "What kind of restaurant did they choose?",
                    "accept": ["Italian", "small Italian", "Italian restaurant"],
                    "hint_ru": "Какой ресторан они выбрали?",
                    "quote": "…a small Italian restaurant downtown.",
                    "model_en": "They chose a small Italian restaurant.",
                },
                {
                    "q": "What did Anna order?",
                    "accept": ["pasta", "pasta with tomato sauce"],
                    "hint_ru": "Что заказала Анна?",
                    "quote": "Anna ordered pasta with tomato sauce…",
                    "model_en": "Anna ordered pasta with tomato sauce.",
                },
                {
                    "q": "How much was the total bill?",
                    "accept": ["forty pounds", "40 pounds", "forty"],
                    "hint_ru": "Сколько составил счёт?",
                    "quote": "The total was forty pounds including service.",
                    "model_en": "The total was forty pounds.",
                },
                {
                    "q": "How did they go home?",
                    "accept": ["by taxi", "taxi", "took a taxi"],
                    "hint_ru": "Как они добрались домой?",
                    "quote": "…they took a taxi home.",
                    "model_en": "They took a taxi home.",
                },
            ],
            "plan": [
                "Choosing the restaurant and menu",
                "Orders and salad",
                "Bill and tip",
                "Thanking the waiter and taxi home",
            ],
            "facts": [
                "They ate at a small Italian restaurant.",
                "Anna ordered pasta; Paul ordered fish.",
                "Paul asked for the bill and left a tip; total forty pounds.",
                "They thanked the waiter and took a taxi home.",
            ],
        },
        "city": {
            "full_text": (
                "Dana lives in a green city with wide streets and old bridges. "
                "Her favourite place is the grassy central park near the river. "
                "On Sundays she rides the bus to the museum with her sister. "
                "They look at paintings and then drink coffee outside. "
                "In summer there are open concerts in the main square. "
                "Dana also likes the market where farmers sell fresh fruit. "
                "She can walk everywhere, so she rarely needs a car. "
                "Tourists often ask her for directions to the medieval castle. "
                "Dana is proud of her city because it feels safe and friendly."
            ),
            "gapped_text": (
                "Dana lives in a green city with wide streets and old bridges. "
                "Her favourite place is the grassy central (1)___ near the river. "
                "On Sundays she rides the (2)___ to the (3)___ with her sister. "
                "They look at paintings and then drink coffee outside. "
                "In summer there are open concerts in the main square. "
                "Dana also likes the market where farmers sell fresh fruit. "
                "She can walk everywhere, so she rarely needs a car. "
                "Tourists often ask her for directions to the medieval (4)___. "
                "Dana is proud of her city because it feels (5)___ and friendly."
            ),
            "answers": ["park", "bus", "museum", "castle", "safe"],
            "word_bank": ["park", "bus", "museum", "castle", "safe", "airport"],
            "questions": [
                {
                    "q": "What is Dana's favourite place?",
                    "accept": [
                        "the central park",
                        "central park",
                        "park near the river",
                        "park",
                    ],
                    "hint_ru": "Какое любимое место у Даны?",
                    "quote": "Her favourite place is the grassy central park…",
                    "model_en": "Dana's favourite place is the central park.",
                },
                {
                    "q": "Where does she go by bus on Sundays?",
                    "accept": ["to the museum", "museum", "the museum"],
                    "hint_ru": "Куда она ездит на автобусе по воскресеньям?",
                    "quote": "…rides the bus to the museum…",
                    "model_en": "On Sundays she goes to the museum by bus.",
                },
                {
                    "q": "What do farmers sell at the market?",
                    "accept": ["fresh fruit", "fruit"],
                    "hint_ru": "Что фермеры продают на рынке?",
                    "quote": "…farmers sell fresh fruit.",
                    "model_en": "Farmers sell fresh fruit at the market.",
                },
                {
                    "q": "Why is Dana proud of her city?",
                    "accept": [
                        "safe and friendly",
                        "it feels safe and friendly",
                        "safe",
                    ],
                    "hint_ru": "Почему Дана гордится своим городом?",
                    "quote": "…because it feels safe and friendly.",
                    "model_en": "Dana is proud because her city feels safe and friendly.",
                },
            ],
            "plan": [
                "Favourite park by the river",
                "Sunday bus to the museum",
                "Concerts and market",
                "Safe friendly city",
            ],
            "facts": [
                "Dana's favourite place is the central park near the river.",
                "On Sundays she takes the bus to the museum.",
                "There is a market with fresh fruit and summer concerts.",
                "She is proud because the city feels safe and friendly.",
            ],
        },
    },
    "B1": {
        "interview": {
            "full_text": (
                "Last Thursday Kate had a job interview at a small design studio in the city centre. "
                "She prepared a short portfolio of three recent projects on a tablet. "
                "The manager asked about her design skills and how she handles deadlines. "
                "Kate explained that she can work flexible hours and learn quickly. "
                "They also discussed the start date and the monthly salary for the role. "
                "After forty minutes the manager offered her a trial week. "
                "Kate asked two questions about the team and remote work options. "
                "She left feeling nervous but hopeful about the role. "
                "On Monday she will send a thank-you email and wait for news."
            ),
            "gapped_text": (
                "Last Thursday Kate had a job (1)___ at a small design studio in the city centre. "
                "She prepared a short (2)___ of three recent projects on a tablet. "
                "The manager asked about her design (3)___ and how she handles deadlines. "
                "Kate explained that she can work flexible hours and learn quickly. "
                "They also discussed the (4)___ date and the monthly salary for the role. "
                "After forty minutes the manager offered her a trial week. "
                "Kate asked two questions about the team and remote work options. "
                "She left feeling nervous but hopeful about the role. "
                "On Monday she will send a thank-you email and wait for (5)___."
            ),
            "answers": ["interview", "portfolio", "skills", "start", "news"],
            "word_bank": ["interview", "portfolio", "skills", "start", "news", "uniform"],
            "questions": [
                {
                    "q": "Where was Kate's interview?",
                    "accept": [
                        "at a small design studio",
                        "design studio",
                        "a design studio",
                    ],
                    "hint_ru": "Где было собеседование у Кейт?",
                    "quote": "…job interview at a small design studio.",
                    "model_en": "Kate's interview was at a small design studio.",
                },
                {
                    "q": "What did the manager ask about?",
                    "accept": [
                        "design skills and how she handles deadlines",
                        "her design skills",
                        "design skills",
                        "skills",
                        "deadlines",
                    ],
                    "hint_ru": "О чём спросил менеджер?",
                    "quote": "…asked about her design skills and how she handles deadlines.",
                    "model_en": "The manager asked about her design skills and deadlines.",
                },
                {
                    "q": "What did the manager offer after forty minutes?",
                    "accept": ["a trial week", "trial week"],
                    "hint_ru": "Что предложил менеджер через сорок минут?",
                    "quote": "…offered her a trial week.",
                    "model_en": "The manager offered her a trial week.",
                },
                {
                    "q": "What will Kate send on Monday?",
                    "accept": ["a thank-you email", "thank-you email", "email"],
                    "hint_ru": "Что Кейт отправит в понедельник?",
                    "quote": "…send a thank-you email…",
                    "model_en": "Kate will send a thank-you email on Monday.",
                },
            ],
            "plan": [
                "Interview at the design studio",
                "Portfolio, design skills and hours",
                "Start date and trial week",
                "Follow-up email on Monday",
            ],
            "facts": [
                "Kate interviewed at a small design studio on Thursday.",
                "She showed a portfolio and talked about design skills, hours and start date.",
                "The manager offered a trial week.",
                "On Monday she will send a thank-you email.",
            ],
        },
        "flatshare": {
            "full_text": (
                "Omar shares a two-room flat with two students near the university. "
                "They split the rent equally and keep a list of weekly chores. "
                "Omar cleans the kitchen on Mondays, and Rita takes out the rubbish. "
                "Their main rules are quiet after eleven and no overnight guests "
                "without a message first. "
                "Last month a friend stayed two nights and washed the bathroom after. "
                "When bills arrive, they pay online from a shared account. "
                "Sometimes they cook together and watch a film in the living room. "
                "Omar likes flatshare life because it is cheaper and less lonely. "
                "Next term they may invite a fourth person if the price rises."
            ),
            "gapped_text": (
                "Omar shares a two-room flat with two students near the university. "
                "They split the (1)___ equally and keep a list of weekly (2)___. "
                "Omar cleans the kitchen on Mondays, and Rita takes out the rubbish. "
                "Their main (3)___ are quiet after eleven and no overnight (4)___ "
                "without a message first. "
                "Last month a friend stayed two nights and washed the bathroom after. "
                "When bills arrive, they pay online from a shared account. "
                "Sometimes they cook together and watch a film in the living room. "
                "Omar likes flatshare life because it is cheaper and less lonely. "
                "Next term they may invite a fourth person if the price (5)___."
            ),
            "answers": ["rent", "chores", "rules", "guests", "rises"],
            "word_bank": ["rent", "chores", "rules", "guests", "rises", "landlord"],
            "questions": [
                {
                    "q": "How do they split the rent?",
                    "accept": ["equally", "split equally", "they split it equally"],
                    "hint_ru": "Как они делят аренду?",
                    "quote": "They split the rent equally…",
                    "model_en": "They split the rent equally.",
                },
                {
                    "q": "What does Omar clean on Mondays?",
                    "accept": ["the kitchen", "kitchen"],
                    "hint_ru": "Что Омар убирает по понедельникам?",
                    "quote": "Omar cleans the kitchen on Mondays…",
                    "model_en": "Omar cleans the kitchen on Mondays.",
                },
                {
                    "q": "What are the quiet hours?",
                    "accept": ["after eleven", "quiet after eleven", "after 11"],
                    "hint_ru": "С какого времени нужна тишина?",
                    "quote": "…quiet after eleven…",
                    "model_en": "They must be quiet after eleven.",
                },
                {
                    "q": "Why does Omar like flatshare life?",
                    "accept": [
                        "cheaper and less lonely",
                        "it is cheaper and less lonely",
                        "cheaper",
                    ],
                    "hint_ru": "Почему Омару нравится совместная аренда?",
                    "quote": "…because it is cheaper and less lonely.",
                    "model_en": "Omar likes it because it is cheaper and less lonely.",
                },
            ],
            "plan": [
                "Rent and weekly chores",
                "House rules about noise and guests",
                "Bills and shared cooking",
                "Pros of flatshare life",
            ],
            "facts": [
                "Omar shares a flat; they split rent and chores.",
                "Rules: quiet after eleven; guests need a message.",
                "They pay bills from a shared account.",
                "Omar likes it because it is cheaper and less lonely.",
            ],
        },
        "online": {
            "full_text": (
                "Last weekend Nina ordered running shoes from an online shop. "
                "She chose a pair with a twenty-percent discount and free delivery. "
                "The parcel arrived in three days, but one shoe was the wrong size. "
                "Nina opened a return request and printed the label at home. "
                "The company collected the box and sent a refund within a week. "
                "Before buying again, she read a short review from other buyers. "
                "This time she checked the size chart carefully and measured her foot. "
                "Nina prefers online shopping when she needs a clear refund policy. "
                "She still visits real stores for clothes she wants to try on."
            ),
            "gapped_text": (
                "Last weekend Nina ordered running shoes from an online shop. "
                "She chose a pair with a twenty-percent (1)___ and free (2)___. "
                "The parcel arrived in three days, but one shoe was the wrong size. "
                "Nina opened a (3)___ request and printed the label at home. "
                "The company collected the box and sent a refund within a week. "
                "Before buying again, she read a short (4)___ from other buyers. "
                "This time she checked the size chart carefully and measured her foot. "
                "Nina prefers online shopping when she needs a clear refund policy. "
                "She still visits real stores for clothes she wants to (5)___ on."
            ),
            "answers": ["discount", "delivery", "return", "review", "try"],
            "word_bank": ["discount", "delivery", "return", "review", "try", "auction"],
            "questions": [
                {
                    "q": "What did Nina order online?",
                    "accept": ["running shoes", "shoes"],
                    "hint_ru": "Что Нина заказала онлайн?",
                    "quote": "…ordered running shoes from an online shop.",
                    "model_en": "Nina ordered running shoes online.",
                },
                {
                    "q": "What was wrong with the first order?",
                    "accept": [
                        "wrong size",
                        "one shoe was the wrong size",
                        "the wrong size",
                    ],
                    "hint_ru": "Что было не так с первым заказом?",
                    "quote": "…one shoe was the wrong size.",
                    "model_en": "One shoe was the wrong size.",
                },
                {
                    "q": "How long did the refund take?",
                    "accept": ["within a week", "a week", "one week"],
                    "hint_ru": "Сколько ждали возврат денег?",
                    "quote": "…sent a refund within a week.",
                    "model_en": "The refund arrived within a week.",
                },
                {
                    "q": "When does Nina prefer online shopping?",
                    "accept": [
                        "when she needs a clear refund policy",
                        "clear refund policy",
                        "refund policy",
                        "clear return policy",
                        "return policy",
                    ],
                    "hint_ru": "Когда Нина предпочитает онлайн-покупки?",
                    "quote": "…when she needs a clear refund policy.",
                    "model_en": "She prefers online shopping with a clear refund policy.",
                },
            ],
            "plan": [
                "Discount order and delivery",
                "Wrong size and return",
                "Refund and reading a review",
                "Careful second attempt",
            ],
            "facts": [
                "Nina ordered shoes with a discount and free delivery.",
                "One shoe was the wrong size, so she opened a return.",
                "She got a refund within a week and read a review.",
                "She likes clear refund policies for online shopping.",
            ],
        },
        "volunteer": {
            "full_text": (
                "Every weekend Ivan volunteers at a local food bank near the station. "
                "His team sorts donations and packs bags for families in need. "
                "Last Saturday they helped at a charity event in the town hall. "
                "Ivan welcomed visitors, explained the project and collected forms. "
                "The organiser said teamwork matters more than perfect English. "
                "After three hours they cleaned the tables and locked the doors carefully. "
                "Ivan feels useful because he meets neighbours and learns new skills. "
                "Next month the group will plant trees in the park by the river. "
                "He hopes more students will join the volunteer group this autumn."
            ),
            "gapped_text": (
                "Every (1)___ Ivan volunteers at a local food bank near the station. "
                "His (2)___ sorts donations and packs bags for families in need. "
                "Last Saturday they helped at a charity (3)___ in the town hall. "
                "Ivan welcomed visitors, explained the project and collected forms. "
                "The organiser said teamwork matters more than perfect English. "
                "After three hours they cleaned the tables and locked the doors carefully. "
                "Ivan feels useful because he meets neighbours and learns new skills. "
                "Next month the group will plant trees in the park by the river. "
                "He hopes more students will (4)___ the volunteer group this (5)___."
            ),
            "answers": ["weekend", "team", "event", "join", "autumn"],
            "word_bank": ["weekend", "team", "event", "join", "autumn", "salary"],
            "questions": [
                {
                    "q": "Where does Ivan volunteer?",
                    "accept": [
                        "at a local food bank",
                        "food bank",
                        "local food bank near the station",
                    ],
                    "hint_ru": "Где Иван волонтёрит?",
                    "quote": "…volunteers at a local food bank near the station.",
                    "model_en": "Ivan volunteers at a local food bank.",
                },
                {
                    "q": "What did they do at the town hall?",
                    "accept": [
                        "helped at a charity event",
                        "charity event",
                        "a charity event",
                    ],
                    "hint_ru": "Что они делали в ратуше?",
                    "quote": "…helped at a charity event in the town hall.",
                    "model_en": "They helped at a charity event in the town hall.",
                },
                {
                    "q": "What will the group do next month?",
                    "accept": [
                        "plant trees in the park",
                        "plant trees",
                        "plant trees by the river",
                    ],
                    "hint_ru": "Что группа сделает в следующем месяце?",
                    "quote": "…will plant trees in the park by the river.",
                    "model_en": "Next month they will plant trees in the park.",
                },
                {
                    "q": "Why does Ivan feel useful?",
                    "accept": [
                        "meets neighbours and learns new skills",
                        "he meets neighbours",
                        "learns new skills",
                    ],
                    "hint_ru": "Почему Иван чувствует себя полезным?",
                    "quote": "…meets neighbours and learns new skills.",
                    "model_en": "He feels useful because he meets neighbours and learns skills.",
                },
            ],
            "plan": [
                "Weekend work at the food bank",
                "Charity event in the town hall",
                "Teamwork and cleaning up",
                "Tree planting and new members",
            ],
            "facts": [
                "Ivan volunteers every weekend at a food bank.",
                "His team helped at a charity event last Saturday.",
                "He feels useful meeting neighbours and learning skills.",
                "Next month they will plant trees; he hopes students join.",
            ],
        },
        "exam": {
            "full_text": (
                "Helen is preparing for an important English exam in June at her language school. "
                "She made a study plan with short goals for each week of revision. "
                "To reduce stress she walks before revision and drinks less coffee. "
                "Most afternoons she works in the library because it is quiet. "
                "Her teacher checked practice papers and gave clear feedback on mistakes. "
                "Helen still worries about listening, so she trains with podcasts. "
                "On the morning of the test she arrived early and read the rules. "
                "Two weeks later the results arrived by email: she passed with a B. "
                "Helen says good planning helped more than last-minute studying."
            ),
            "gapped_text": (
                "Helen is preparing for an important English (1)___ in June at her language school. "
                "She made a study (2)___ with short goals for each week of revision. "
                "To reduce (3)___ she walks before revision and drinks less coffee. "
                "Most afternoons she works in the (4)___ because it is quiet. "
                "Her teacher checked practice papers and gave clear feedback on mistakes. "
                "Helen still worries about listening, so she trains with podcasts. "
                "On the morning of the test she arrived early and read the rules. "
                "Two weeks later the (5)___ arrived by email: she passed with a B. "
                "Helen says good planning helped more than last-minute studying."
            ),
            "answers": ["exam", "plan", "stress", "library", "results"],
            "word_bank": ["exam", "plan", "stress", "library", "results", "holiday"],
            "questions": [
                {
                    "q": "When is Helen's English exam?",
                    "accept": ["in June", "June"],
                    "hint_ru": "Когда у Хелен экзамен по английскому?",
                    "quote": "…English exam in June.",
                    "model_en": "Helen's English exam is in June.",
                },
                {
                    "q": "Where does she study most afternoons?",
                    "accept": ["in the library", "library", "the library"],
                    "hint_ru": "Где она занимается почти каждый день после обеда?",
                    "quote": "…works in the library because it is quiet.",
                    "model_en": "She studies in the library most afternoons.",
                },
                {
                    "q": "How does she train for listening?",
                    "accept": ["with podcasts", "podcasts", "trains with podcasts"],
                    "hint_ru": "Как она тренирует аудирование?",
                    "quote": "…trains with podcasts.",
                    "model_en": "She trains for listening with podcasts.",
                },
                {
                    "q": "What were her exam results?",
                    "accept": ["passed with a B", "a B", "B", "she passed with a B"],
                    "hint_ru": "Какой был результат экзамена?",
                    "quote": "…she passed with a B.",
                    "model_en": "Helen passed with a B.",
                },
            ],
            "plan": [
                "Study plan and stress control",
                "Library practice and feedback",
                "Listening with podcasts",
                "Exam day and results",
            ],
            "facts": [
                "Helen prepared for a June English exam with a study plan.",
                "She reduced stress and worked in the library.",
                "She trained listening with podcasts.",
                "Results came by email: she passed with a B.",
            ],
        },
        "move": {
            "full_text": (
                "In March Alex moved to a new flat across the river with help from friends. "
                "Friends helped him carry heavy boxes up three floors without a lift. "
                "The neighbours brought tea and offered spare shelves for his books. "
                "Alex likes the new area because shops and a tram stop are close. "
                "The rent is higher, but the rooms get more daylight in the morning. "
                "He spent the first weekend unpacking clothes and books carefully. "
                "On Monday he registered his address at the local office. "
                "Moving was tiring, yet he already feels at home in the new place. "
                "Next Saturday he will invite old friends to a small housewarming."
            ),
            "gapped_text": (
                "In March Alex moved to a new flat across the river with help from friends. "
                "Friends helped him carry heavy (1)___ up three floors without a lift. "
                "The (2)___ brought tea and offered spare shelves for his books. "
                "Alex likes the new (3)___ because shops and a tram stop are close. "
                "The (4)___ is higher, but the rooms get more daylight in the morning. "
                "He spent the first weekend unpacking clothes and books carefully. "
                "On Monday he registered his address at the local office. "
                "Moving was tiring, yet he already feels at home in the new place. "
                "Next Saturday he will invite old friends to a small (5)___."
            ),
            "answers": ["boxes", "neighbours", "area", "rent", "housewarming"],
            "word_bank": ["boxes", "neighbours", "area", "rent", "housewarming", "elevator"],
            "questions": [
                {
                    "q": "When did Alex move?",
                    "accept": ["in March", "March"],
                    "hint_ru": "Когда Алекс переехал?",
                    "quote": "In March Alex moved to a new flat…",
                    "model_en": "Alex moved in March.",
                },
                {
                    "q": "Why does he like the new area?",
                    "accept": [
                        "shops and a tram stop are close",
                        "shops are close",
                        "tram stop are close",
                        "close shops and tram",
                    ],
                    "hint_ru": "Почему ему нравится новый район?",
                    "quote": "…shops and a tram stop are close.",
                    "model_en": "He likes it because shops and a tram stop are close.",
                },
                {
                    "q": "What is different about the rent?",
                    "accept": ["higher", "the rent is higher", "rent is higher"],
                    "hint_ru": "Что изменилось с арендой?",
                    "quote": "The rent is higher…",
                    "model_en": "The rent is higher.",
                },
                {
                    "q": "What will he do next Saturday?",
                    "accept": [
                        "invite old friends to a housewarming",
                        "housewarming",
                        "invite friends",
                    ],
                    "hint_ru": "Что он сделает в следующую субботу?",
                    "quote": "…invite old friends to a small housewarming.",
                    "model_en": "Next Saturday he will invite friends to a housewarming.",
                },
            ],
            "plan": [
                "Moving with boxes and neighbours",
                "New area and higher rent",
                "Unpacking and registration",
                "Housewarming plans",
            ],
            "facts": [
                "Alex moved in March; friends carried heavy boxes.",
                "Neighbours brought tea; he likes the new area.",
                "Rent is higher but rooms get more daylight.",
                "He will host a housewarming next Saturday.",
            ],
        },
        "travel_b1": {
            "full_text": (
                "Chris flew to Lisbon for a four-day city break in May. "
                "His flight left two hours late because of a storm at the airport. "
                "He used the delay to message the hotel and change the check-in time. "
                "At midnight a shuttle finally took tired passengers to the city. "
                "The receptionist was kind and upgraded him to a quieter room. "
                "Next morning Chris explored tram lines and a viewpoint above the river. "
                "He advises travellers to pack a book and download offline maps. "
                "Despite the late departure, the trip taught him to stay calm and flexible. "
                "He already plans a longer holiday there next spring."
            ),
            "gapped_text": (
                "Chris flew to Lisbon for a four-day city break in May. "
                "His (1)___ left two hours late because of a storm at the airport. "
                "He used the (2)___ to message the (3)___ and change the check-in time. "
                "At midnight a shuttle finally took tired passengers to the city. "
                "The receptionist was kind and upgraded him to a quieter room. "
                "Next morning Chris explored tram lines and a viewpoint above the river. "
                "He advises travellers to pack a book and download offline maps. "
                "Despite the late departure, the trip taught him to stay calm and flexible. "
                "He already plans a longer (4)___ there next (5)___."
            ),
            "answers": ["flight", "delay", "hotel", "holiday", "spring"],
            "word_bank": ["flight", "delay", "hotel", "holiday", "spring", "passport"],
            "questions": [
                {
                    "q": "Why was Chris's flight late?",
                    "accept": [
                        "because of a storm",
                        "storm at the airport",
                        "a storm",
                        "storm",
                    ],
                    "hint_ru": "Почему рейс Криса задержался?",
                    "quote": "…late because of a storm at the airport.",
                    "model_en": "The flight was late because of a storm at the airport.",
                },
                {
                    "q": "What did he do during the delay?",
                    "accept": [
                        "message the hotel and change the check-in time",
                        "messaged the hotel",
                        "change the check-in time",
                    ],
                    "hint_ru": "Что он сделал во время задержки?",
                    "quote": "…message the hotel and change the check-in time.",
                    "model_en": "He messaged the hotel and changed the check-in time.",
                },
                {
                    "q": "What upgrade did the receptionist give?",
                    "accept": ["a quieter room", "quieter room", "quiet room"],
                    "hint_ru": "Какой апгрейд сделала администратор?",
                    "quote": "…upgraded him to a quieter room.",
                    "model_en": "The receptionist upgraded him to a quieter room.",
                },
                {
                    "q": "What advice does Chris give travellers?",
                    "accept": [
                        "pack a book and download offline maps",
                        "pack a book",
                        "download offline maps",
                        "offline maps",
                    ],
                    "hint_ru": "Какой совет даёт Крис путешественникам?",
                    "quote": "…pack a book and download offline maps.",
                    "model_en": "He advises packing a book and downloading offline maps.",
                },
            ],
            "plan": [
                "Delayed flight to Lisbon",
                "Hotel message and late shuttle",
                "Quieter room and city exploration",
                "Advice and future holiday plans",
            ],
            "facts": [
                "Chris's flight to Lisbon was delayed by a storm.",
                "He messaged the hotel during the delay.",
                "The receptionist gave him a quieter room.",
                "He advises books and offline maps; plans another holiday.",
            ],
        },
        "hobby_club": {
            "full_text": (
                "Rita joined a photography hobby club that meets every Wednesday evening. "
                "There are twelve members, from beginners to people with real cameras. "
                "At each meeting they share photos and choose a small weekly project. "
                "Last month their work was night lights in the old town centre. "
                "Rita learned to use manual settings and edit colours carefully. "
                "The club also organises short trips when the weather is clear. "
                "New people can join after a free trial evening and a short chat. "
                "Rita says the group is patient and gives honest feedback. "
                "She wants to show her best pictures at the spring exhibition."
            ),
            "gapped_text": (
                "Rita joined a photography hobby club that meets every Wednesday evening. "
                "There are twelve (1)___, from beginners to people with real cameras. "
                "At each (2)___ they share photos and choose a small weekly (3)___. "
                "Last month their work was night lights in the old town centre. "
                "Rita learned to use manual settings and edit colours carefully. "
                "The club also organises short trips when the weather is clear. "
                "New people can (4)___ after a free trial evening and a short chat. "
                "Rita says the group is patient and gives honest feedback. "
                "She wants to show her best pictures at the spring (5)___."
            ),
            "answers": ["members", "meeting", "project", "join", "exhibition"],
            "word_bank": ["members", "meeting", "project", "join", "exhibition", "ticket"],
            "questions": [
                {
                    "q": "How often does the club meet?",
                    "accept": ["every Wednesday", "Wednesday", "on Wednesday"],
                    "hint_ru": "Как часто встречается клуб?",
                    "quote": "…meets every Wednesday.",
                    "model_en": "The club meets every Wednesday.",
                },
                {
                    "q": "How many members are there?",
                    "accept": ["twelve", "12", "twelve members"],
                    "hint_ru": "Сколько участников в клубе?",
                    "quote": "There are twelve members…",
                    "model_en": "There are twelve members.",
                },
                {
                    "q": "What was last month's project?",
                    "accept": [
                        "night lights in the old town",
                        "night lights",
                        "lights in the old town",
                    ],
                    "hint_ru": "Какой был проект в прошлом месяце?",
                    "quote": "…their work was night lights in the old town centre.",
                    "model_en": "Last month their work was night lights in the old town centre.",
                },
                {
                    "q": "How can new people join?",
                    "accept": [
                        "after a free trial evening and a short chat",
                        "free trial evening",
                        "after a free trial",
                    ],
                    "hint_ru": "Как новые люди могут вступить?",
                    "quote": "…join after a free trial evening and a short chat.",
                    "model_en": "New people can join after a free trial evening and a short chat.",
                },
            ],
            "plan": [
                "Club members and Wednesday meetings",
                "Weekly projects and learning",
                "Trips and how to join",
                "Feedback and spring exhibition",
            ],
            "facts": [
                "Rita's photography club meets every Wednesday.",
                "There are twelve members with weekly projects.",
                "New people join after a free trial evening.",
                "Rita wants to show pictures at the spring exhibition.",
            ],
        },
    },
}
