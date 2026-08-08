"""Фиксированные Reading-пакеты: все уровни и темы.

Сгенерировано scripts/build_reading_packs.py — править вручную можно,
но проще пересобрать скриптом после правок шаблонов.
В рантайме GPT для текстов не вызывается.
"""

from __future__ import annotations

READING_PACKS: dict[str, dict[str, dict]] = {'A0': {'family': {'full_text': 'My name is Lena. I live with my family in a small flat. I have '
                                'one sister. Her name is Olga. Olga is ten years old and she likes '
                                'school. My father is a doctor. Dad helps sick people at the '
                                'hospital. My mother is a teacher. Mum works at our school and '
                                'teaches English. At weekends we cook together in the kitchen. I '
                                'love my family very much. Next Sunday we will visit grandma.',
                   'gapped_text': 'My name is Lena. I live with my family in a small flat. I have '
                                  'one sister. Her name is Olga. Olga is ten years old and she '
                                  "likes school. My sister's name is (1)___. My father is a "
                                  '(2)___. Dad helps sick people at the hospital. My mother is a '
                                  'teacher. Mum works at our school and teaches (3)___. At '
                                  'weekends we cook together in the (4)___. I love my family very '
                                  'much. Next Sunday we will visit (5)___.',
                   'answers': ['Olga', 'doctor', 'English', 'kitchen', 'grandma'],
                   'word_bank': ['Olga', 'doctor', 'English', 'kitchen', 'grandma', 'twelve'],
                   'questions': [{'q': 'How old is Olga?',
                                  'accept': ['ten', '10', 'ten years old'],
                                  'hint_ru': 'Сколько лет Ольге? Возраст уже написан в тексте '
                                             'целиком.',
                                  'quote': 'Olga is ten years old…',
                                  'model_en': 'Olga is ten years old.'},
                                 {'q': "What is Lena's father's job?",
                                  'accept': ['doctor', 'a doctor'],
                                  'hint_ru': 'Кем работает папа? Смотри, что он делает в больнице.',
                                  'quote': 'My father is a doctor…',
                                  'model_en': "Lena's father is a doctor."},
                                 {'q': 'What does Mum teach?',
                                  'accept': ['English', 'English language'],
                                  'hint_ru': 'Что преподаёт мама?',
                                  'quote': '…teaches English.',
                                  'model_en': 'Mum teaches English.'},
                                 {'q': 'Where do they cook at weekends?',
                                  'accept': ['in the kitchen', 'kitchen'],
                                  'hint_ru': 'Где они готовят?',
                                  'quote': '…cook together in the kitchen.',
                                  'model_en': 'They cook in the kitchen at weekends.'}],
                   'plan': ['Who Lena lives with',
                            'Facts about Olga (name and age from the text)',
                            "Parents' jobs",
                            'Weekend cooking and Sunday visit'],
                   'facts': ['Lena lives with her family; she has a sister Olga.',
                             'Olga is ten and likes school.',
                             'Father is a doctor; mother is a teacher of English.',
                             'They cook in the kitchen; next Sunday they visit grandma.']},
        'colors': {'full_text': 'Ben reads a short text about Colors. The text focuses on red, '
                                'blue, green, bag, T-shirt. Ben makes a plan before practice. At '
                                'ten Ben meets Ivan near the school. Ivan wants to visit a museum, '
                                'but Ben prefers the school. In the end they choose the school '
                                'because it is warm. They buy water and sit for half an hour. Ben '
                                'pays five pounds for the drinks. Ivan takes notes and sends one '
                                'photo to family. They agree to meet again next Friday and Ben '
                                'puts the notes in a bag. Before leaving, Ivan checks the time on '
                                'a phone.',
                   'gapped_text': 'Ben reads a short text about Colors. The text focuses on red, '
                                  'blue, green, bag, T-shirt. Ben makes a (1)___ before practice. '
                                  'At ten Ben meets Ivan near the school. Ivan wants to visit a '
                                  'museum, but Ben prefers the school. In the end they choose the '
                                  'school because it is (2)___. They buy water and sit for half an '
                                  'hour. Ben pays five pounds for the drinks. Ivan takes notes and '
                                  'sends one photo to family. They agree to meet again next (3)___ '
                                  'and Ben puts the notes in a (4)___. Before leaving, Ivan checks '
                                  'the time on a (5)___.',
                   'answers': ['plan', 'warm', 'Friday', 'bag', 'phone'],
                   'word_bank': ['plan', 'warm', 'Friday', 'bag', 'phone', 'silent'],
                   'questions': [{'q': "What is Ben's text about?",
                                  'accept': ['Colors', 'colors'],
                                  'hint_ru': 'О чём текст в начале?',
                                  'quote': '…text about Colors.',
                                  'model_en': 'The text is about Colors.'},
                                 {'q': 'What time does Ben meet Ivan?',
                                  'accept': ['ten', '10', 'at ten'],
                                  'hint_ru': 'Во сколько они встречаются?',
                                  'quote': 'At ten Ben meets Ivan…',
                                  'model_en': 'Ben meets Ivan at ten.'},
                                 {'q': 'Why do they choose the school?',
                                  'accept': ['warm', 'it is warm', 'because it is warm'],
                                  'hint_ru': 'Почему они выбирают это место?',
                                  'quote': '…because it is warm.',
                                  'model_en': 'They choose the school because it is warm.'},
                                 {'q': 'When do they agree to meet again?',
                                  'accept': ['next Friday', 'Friday'],
                                  'hint_ru': 'Когда следующая встреча?',
                                  'quote': '…meet again next Friday…',
                                  'model_en': 'They agree to meet again next Friday.'}],
                   'plan': ['Topic of the text (Colors)',
                            'Meeting near the school',
                            'Why they stay there',
                            'Payment and next day'],
                   'facts': ['Ben reads about Colors (red, blue, green, bag, T-shirt).',
                             'They meet at ten near the school.',
                             'They choose it because it is warm.',
                             'Ben pays five pounds; next meeting is Friday.']},
        'food': {'full_text': 'Anna likes simple food. For breakfast she eats bread and cheese. '
                              'She drinks tea with lemon, not coffee. At lunch she takes an apple '
                              'and a sandwich. In the evening her family cooks soup together. Anna '
                              'does not like fish, but she loves fruit. On Sundays they buy fresh '
                              'bread at the shop. Anna puts the bread in a basket on the table. '
                              'Then they sit and eat slowly. After dinner Anna washes the cups.',
                 'gapped_text': 'Anna likes simple food. For breakfast she eats bread and cheese. '
                                'She drinks (1)___ with lemon, not coffee. At lunch she takes an '
                                '(2)___ and a sandwich. In the evening her family cooks (3)___ '
                                'together. Anna does not like fish, but she loves fruit. On '
                                'Sundays they buy fresh bread at the shop. Anna puts the bread in '
                                'a (4)___ on the table. Then they sit and eat slowly. After dinner '
                                'Anna washes the (5)___.',
                 'answers': ['tea', 'apple', 'soup', 'basket', 'cups'],
                 'word_bank': ['tea', 'apple', 'soup', 'basket', 'cups', 'pizza'],
                 'questions': [{'q': 'What does Anna drink with lemon?',
                                'accept': ['tea', 'tea with lemon'],
                                'hint_ru': 'Что Анна пьёт с лимоном?',
                                'quote': 'She drinks tea with lemon…',
                                'model_en': 'Anna drinks tea with lemon.'},
                               {'q': 'What fruit does she take at lunch?',
                                'accept': ['apple', 'an apple'],
                                'hint_ru': 'Какой фрукт она берёт в обед?',
                                'quote': '…takes an apple and a sandwich.',
                                'model_en': 'She takes an apple at lunch.'},
                               {'q': 'What do they cook in the evening?',
                                'accept': ['soup'],
                                'hint_ru': 'Что они готовят вечером?',
                                'quote': '…cooks soup together.',
                                'model_en': 'They cook soup in the evening.'},
                               {'q': 'Where does Anna put the bread?',
                                'accept': ['in a basket', 'basket', 'on the table'],
                                'hint_ru': 'Куда Анна кладёт хлеб?',
                                'quote': '…in a basket on the table.',
                                'model_en': 'Anna puts the bread in a basket on the table.'}],
                 'plan': ['Breakfast drinks and food',
                          'Lunch',
                          'Evening cooking',
                          'Sunday shop and dinner'],
                 'facts': ['Anna drinks tea with lemon, not coffee.',
                           'At lunch she takes an apple and a sandwich.',
                           'In the evening they cook soup.',
                           'On Sundays they buy bread; she puts it in a basket.']},
        'pets': {'full_text': 'Victor reads a short text about Pets. The text focuses on cat, dog, '
                              'name, play. Victor makes a plan before practice. At ten Victor '
                              'meets Eva near the library. Eva wants to visit a museum, but Victor '
                              'prefers the library. In the end they choose the library because it '
                              'is free. They buy water and sit for half an hour. Victor pays six '
                              'pounds for the drinks. Eva takes notes and sends one photo to '
                              'family. They agree to meet again next Sunday and Victor puts the '
                              'notes in a backpack. Before leaving, Eva checks the time on a '
                              'phone.',
                 'gapped_text': 'Victor reads a short text about Pets. The text focuses on cat, '
                                'dog, name, play. Victor makes a (1)___ before practice. At ten '
                                'Victor meets Eva near the library. Eva wants to visit a museum, '
                                'but Victor prefers the library. In the end they choose the '
                                'library because it is (2)___. They buy water and sit for half an '
                                'hour. Victor pays six pounds for the drinks. Eva takes notes and '
                                'sends one photo to family. They agree to meet again next (3)___ '
                                'and Victor puts the notes in a (4)___. Before leaving, Eva checks '
                                'the time on a (5)___.',
                 'answers': ['plan', 'free', 'Sunday', 'backpack', 'phone'],
                 'word_bank': ['plan', 'free', 'Sunday', 'backpack', 'phone', 'heavy'],
                 'questions': [{'q': "What is Victor's text about?",
                                'accept': ['Pets', 'pets'],
                                'hint_ru': 'О чём текст в начале?',
                                'quote': '…text about Pets.',
                                'model_en': 'The text is about Pets.'},
                               {'q': 'What time does Victor meet Eva?',
                                'accept': ['ten', '10', 'at ten'],
                                'hint_ru': 'Во сколько они встречаются?',
                                'quote': 'At ten Victor meets Eva…',
                                'model_en': 'Victor meets Eva at ten.'},
                               {'q': 'Why do they choose the library?',
                                'accept': ['free', 'it is free', 'because it is free'],
                                'hint_ru': 'Почему они выбирают это место?',
                                'quote': '…because it is free.',
                                'model_en': 'They choose the library because it is free.'},
                               {'q': 'When do they agree to meet again?',
                                'accept': ['next Sunday', 'Sunday'],
                                'hint_ru': 'Когда следующая встреча?',
                                'quote': '…meet again next Sunday…',
                                'model_en': 'They agree to meet again next Sunday.'}],
                 'plan': ['Topic of the text (Pets)',
                          'Meeting near the library',
                          'Why they stay there',
                          'Payment and next day'],
                 'facts': ['Victor reads about Pets (cat, dog, name, play).',
                           'They meet at ten near the library.',
                           'They choose it because it is free.',
                           'Victor pays six pounds; next meeting is Sunday.']},
        'home': {'full_text': 'Leo lives in a small flat with two rooms. The kitchen is bright '
                              'because of a big window. His bedroom has a bed, a desk and a blue '
                              'chair. Near the door there is a green plant. In the evening Leo '
                              'reads a book on the sofa. His sister draws pictures at the desk. '
                              'Mum opens the window when it is hot. Dad fixes the door when it '
                              'makes a noise. They keep shoes next to the door. Leo likes his home '
                              'because it is quiet.',
                 'gapped_text': 'Leo lives in a small flat with two rooms. The kitchen is bright '
                                'because of a big (1)___. His bedroom has a bed, a desk and a blue '
                                '(2)___. Near the door there is a green plant. In the evening Leo '
                                'reads a book on the (3)___. His sister draws pictures at the '
                                'desk. Mum opens the window when it is hot. Dad fixes the (4)___ '
                                'when it makes a noise. They keep shoes next to the door. Leo '
                                'likes his home because it is (5)___.',
                 'answers': ['window', 'chair', 'sofa', 'door', 'quiet'],
                 'word_bank': ['window', 'chair', 'sofa', 'door', 'quiet', 'noisy'],
                 'questions': [{'q': 'Why is the kitchen bright?',
                                'accept': ['big window', 'window', 'because of a big window'],
                                'hint_ru': 'Почему кухня светлая?',
                                'quote': '…because of a big window.',
                                'model_en': 'The kitchen is bright because of a big window.'},
                               {'q': 'What colour is the chair?',
                                'accept': ['blue', 'blue chair'],
                                'hint_ru': 'Какого цвета стул?',
                                'quote': '…a blue chair.',
                                'model_en': 'The chair is blue.'},
                               {'q': 'Where does Leo read in the evening?',
                                'accept': ['on the sofa', 'sofa'],
                                'hint_ru': 'Где Лео читает вечером?',
                                'quote': '…reads a book on the sofa.',
                                'model_en': 'Leo reads a book on the sofa in the evening.'},
                               {'q': 'Why does Leo like his home?',
                                'accept': ['quiet', 'because it is quiet'],
                                'hint_ru': 'Почему Лео нравится дом?',
                                'quote': '…because it is quiet.',
                                'model_en': 'Leo likes his home because it is quiet.'}],
                 'plan': ['Flat and kitchen',
                          'Bedroom things',
                          'Evening at home',
                          'Door, shoes, feeling'],
                 'facts': ['Kitchen is bright because of a big window.',
                           'Bedroom has a bed, desk and blue chair.',
                           'Leo reads on the sofa; sister draws at the desk.',
                           'Dad fixes the door; Leo likes the quiet home.']},
        'school': {'full_text': 'Lena reads a short text about School. The text focuses on pen, '
                                'book, teacher, class. Lena makes a plan before practice. At ten '
                                'Lena meets Ivan near the library. Ivan wants to visit a museum, '
                                'but Lena prefers the library. In the end they choose the library '
                                'because it is sunny. They buy water and sit for half an hour. '
                                'Lena pays three pounds for the drinks. Ivan takes notes and sends '
                                'one photo to family. They agree to meet again next Saturday and '
                                'Lena puts the notes in a folder. Before leaving, Ivan checks the '
                                'time on a phone.',
                   'gapped_text': 'Lena reads a short text about School. The text focuses on pen, '
                                  'book, teacher, class. Lena makes a (1)___ before practice. At '
                                  'ten Lena meets Ivan near the library. Ivan wants to visit a '
                                  'museum, but Lena prefers the library. In the end they choose '
                                  'the library because it is (2)___. They buy water and sit for '
                                  'half an hour. Lena pays three pounds for the drinks. Ivan takes '
                                  'notes and sends one photo to family. They agree to meet again '
                                  'next (3)___ and Lena puts the notes in a (4)___. Before '
                                  'leaving, Ivan checks the time on a (5)___.',
                   'answers': ['plan', 'sunny', 'Saturday', 'folder', 'phone'],
                   'word_bank': ['plan', 'sunny', 'Saturday', 'folder', 'phone', 'winter'],
                   'questions': [{'q': "What is Lena's text about?",
                                  'accept': ['School', 'school'],
                                  'hint_ru': 'О чём текст в начале?',
                                  'quote': '…text about School.',
                                  'model_en': 'The text is about School.'},
                                 {'q': 'What time does Lena meet Ivan?',
                                  'accept': ['ten', '10', 'at ten'],
                                  'hint_ru': 'Во сколько они встречаются?',
                                  'quote': 'At ten Lena meets Ivan…',
                                  'model_en': 'Lena meets Ivan at ten.'},
                                 {'q': 'Why do they choose the library?',
                                  'accept': ['sunny', 'it is sunny', 'because it is sunny'],
                                  'hint_ru': 'Почему они выбирают это место?',
                                  'quote': '…because it is sunny.',
                                  'model_en': 'They choose the library because it is sunny.'},
                                 {'q': 'When do they agree to meet again?',
                                  'accept': ['next Saturday', 'Saturday'],
                                  'hint_ru': 'Когда следующая встреча?',
                                  'quote': '…meet again next Saturday…',
                                  'model_en': 'They agree to meet again next Saturday.'}],
                   'plan': ['Topic of the text (School)',
                            'Meeting near the library',
                            'Why they stay there',
                            'Payment and next day'],
                   'facts': ['Lena reads about School (pen, book, teacher, class).',
                             'They meet at ten near the library.',
                             'They choose it because it is sunny.',
                             'Lena pays three pounds; next meeting is Saturday.']},
        'days': {'full_text': 'Mia reads a short text about Days. The text focuses on Monday, '
                              'today, tomorrow. Mia makes a plan before practice. At ten Mia meets '
                              'Alex near the office. Alex wants to visit a museum, but Mia prefers '
                              'the office. In the end they choose the office because it is warm. '
                              'They buy water and sit for half an hour. Mia pays four pounds for '
                              'the drinks. Alex takes notes and sends one photo to family. They '
                              'agree to meet again next Monday and Mia puts the notes in a '
                              'backpack. Before leaving, Alex checks the time on a phone.',
                 'gapped_text': 'Mia reads a short text about Days. The text focuses on Monday, '
                                'today, tomorrow. Mia makes a (1)___ before practice. At ten Mia '
                                'meets Alex near the office. Alex wants to visit a museum, but Mia '
                                'prefers the office. In the end they choose the office because it '
                                'is (2)___. They buy water and sit for half an hour. Mia pays four '
                                'pounds for the drinks. Alex takes notes and sends one photo to '
                                'family. They agree to meet again next (3)___ and Mia puts the '
                                'notes in a (4)___. Before leaving, Alex checks the time on a '
                                '(5)___.',
                 'answers': ['plan', 'warm', 'Monday', 'backpack', 'phone'],
                 'word_bank': ['plan', 'warm', 'Monday', 'backpack', 'phone', 'purple'],
                 'questions': [{'q': "What is Mia's text about?",
                                'accept': ['Days', 'days'],
                                'hint_ru': 'О чём текст в начале?',
                                'quote': '…text about Days.',
                                'model_en': 'The text is about Days.'},
                               {'q': 'What time does Mia meet Alex?',
                                'accept': ['ten', '10', 'at ten'],
                                'hint_ru': 'Во сколько они встречаются?',
                                'quote': 'At ten Mia meets Alex…',
                                'model_en': 'Mia meets Alex at ten.'},
                               {'q': 'Why do they choose the office?',
                                'accept': ['warm', 'it is warm', 'because it is warm'],
                                'hint_ru': 'Почему они выбирают это место?',
                                'quote': '…because it is warm.',
                                'model_en': 'They choose the office because it is warm.'},
                               {'q': 'When do they agree to meet again?',
                                'accept': ['next Monday', 'Monday'],
                                'hint_ru': 'Когда следующая встреча?',
                                'quote': '…meet again next Monday…',
                                'model_en': 'They agree to meet again next Monday.'}],
                 'plan': ['Topic of the text (Days)',
                          'Meeting near the office',
                          'Why they stay there',
                          'Payment and next day'],
                 'facts': ['Mia reads about Days (Monday, today, tomorrow).',
                           'They meet at ten near the office.',
                           'They choose it because it is warm.',
                           'Mia pays four pounds; next meeting is Monday.']},
        'hello': {'full_text': 'Ben reads a short text about Meeting people. The text focuses on '
                               'name, hello, nice to meet you. Ben makes a plan before practice. '
                               'At ten Ben meets Paul near the library. Paul wants to visit a '
                               'museum, but Ben prefers the library. In the end they choose the '
                               'library because it is sunny. They buy water and sit for half an '
                               'hour. Ben pays three pounds for the drinks. Paul takes notes and '
                               'sends one photo to family. They agree to meet again next Wednesday '
                               'and Ben puts the notes in a backpack. Before leaving, Paul checks '
                               'the time on a phone.',
                  'gapped_text': 'Ben reads a short text about Meeting people. The text focuses on '
                                 'name, hello, nice to meet you. Ben makes a (1)___ before '
                                 'practice. At ten Ben meets Paul near the library. Paul wants to '
                                 'visit a museum, but Ben prefers the library. In the end they '
                                 'choose the library because it is (2)___. They buy water and sit '
                                 'for half an hour. Ben pays three pounds for the drinks. Paul '
                                 'takes notes and sends one photo to family. They agree to meet '
                                 'again next (3)___ and Ben puts the notes in a (4)___. Before '
                                 'leaving, Paul checks the time on a (5)___.',
                  'answers': ['plan', 'sunny', 'Wednesday', 'backpack', 'phone'],
                  'word_bank': ['plan', 'sunny', 'Wednesday', 'backpack', 'phone', 'heavy'],
                  'questions': [{'q': "What is Ben's text about?",
                                 'accept': ['Meeting people', 'meeting people'],
                                 'hint_ru': 'О чём текст в начале?',
                                 'quote': '…text about Meeting people.',
                                 'model_en': 'The text is about Meeting people.'},
                                {'q': 'What time does Ben meet Paul?',
                                 'accept': ['ten', '10', 'at ten'],
                                 'hint_ru': 'Во сколько они встречаются?',
                                 'quote': 'At ten Ben meets Paul…',
                                 'model_en': 'Ben meets Paul at ten.'},
                                {'q': 'Why do they choose the library?',
                                 'accept': ['sunny', 'it is sunny', 'because it is sunny'],
                                 'hint_ru': 'Почему они выбирают это место?',
                                 'quote': '…because it is sunny.',
                                 'model_en': 'They choose the library because it is sunny.'},
                                {'q': 'When do they agree to meet again?',
                                 'accept': ['next Wednesday', 'Wednesday'],
                                 'hint_ru': 'Когда следующая встреча?',
                                 'quote': '…meet again next Wednesday…',
                                 'model_en': 'They agree to meet again next Wednesday.'}],
                  'plan': ['Topic of the text (Meeting people)',
                           'Meeting near the library',
                           'Why they stay there',
                           'Payment and next day'],
                  'facts': ['Ben reads about Meeting people (name, hello, nice to meet you).',
                            'They meet at ten near the library.',
                            'They choose it because it is sunny.',
                            'Ben pays three pounds; next meeting is Wednesday.']}},
 'A1': {'family_a1': {'full_text': 'My name is Lena. I live with my family in a small flat. I have '
                                   'one sister. Her name is Olga. Olga is ten years old and she '
                                   'likes school. My father is a doctor. Dad helps sick people at '
                                   'the hospital. My mother is a teacher. Mum works at our school '
                                   'and teaches English. At weekends we cook together in the '
                                   'kitchen. I love my family very much. Next Sunday we will visit '
                                   'grandma.',
                      'gapped_text': 'My name is Lena. I live with my family in a small flat. I '
                                     'have one sister. Her name is Olga. Olga is ten years old and '
                                     "she likes school. My sister's name is (1)___. My father is a "
                                     '(2)___. Dad helps sick people at the hospital. My mother is '
                                     'a teacher. Mum works at our school and teaches (3)___. At '
                                     'weekends we cook together in the (4)___. I love my family '
                                     'very much. Next Sunday we will visit (5)___.',
                      'answers': ['Olga', 'doctor', 'English', 'kitchen', 'grandma'],
                      'word_bank': ['Olga', 'doctor', 'English', 'kitchen', 'grandma', 'twelve'],
                      'questions': [{'q': 'How old is Olga?',
                                     'accept': ['ten', '10', 'ten years old'],
                                     'hint_ru': 'Сколько лет Ольге? Возраст уже написан в тексте '
                                                'целиком.',
                                     'quote': 'Olga is ten years old…',
                                     'model_en': 'Olga is ten years old.'},
                                    {'q': "What is Lena's father's job?",
                                     'accept': ['doctor', 'a doctor'],
                                     'hint_ru': 'Кем работает папа? Смотри, что он делает в '
                                                'больнице.',
                                     'quote': 'My father is a doctor…',
                                     'model_en': "Lena's father is a doctor."},
                                    {'q': 'What does Mum teach?',
                                     'accept': ['English', 'English language'],
                                     'hint_ru': 'Что преподаёт мама?',
                                     'quote': '…teaches English.',
                                     'model_en': 'Mum teaches English.'},
                                    {'q': 'Where do they cook at weekends?',
                                     'accept': ['in the kitchen', 'kitchen'],
                                     'hint_ru': 'Где они готовят?',
                                     'quote': '…cook together in the kitchen.',
                                     'model_en': 'They cook in the kitchen at weekends.'}],
                      'plan': ['Who Lena lives with',
                               'Facts about Olga (name and age from the text)',
                               "Parents' jobs",
                               'Weekend cooking and Sunday visit'],
                      'facts': ['Lena lives with her family; she has a sister Olga.',
                                'Olga is ten and likes school.',
                                'Father is a doctor; mother is a teacher of English.',
                                'They cook in the kitchen; next Sunday they visit grandma.']},
        'cafe': {'full_text': 'Michael and Anna met at a café at 2 p.m. Michael ordered a cup of '
                              'coffee and a piece of chocolate cake. Anna ordered green tea and a '
                              'fruit salad. They talked about their plans for the weekend. In the '
                              'end they decided to go to the cinema first and then walk in the '
                              'park. Michael paid for the order — 15 pounds. Anna preferred quiet '
                              'weekends with books, but today she wanted something fun. Michael '
                              'wanted to try a new film and then get some fresh air. The café was '
                              'busy, but their table near the window was free. They left happy and '
                              'already planned to meet again next Saturday.',
                 'gapped_text': 'Michael and Anna (1)___ at a café at 2 p.m. Michael ordered a cup '
                                'of coffee and a (2)___ of chocolate cake. Anna ordered green tea '
                                'and a (3)___ salad. They talked about their (4)___ for the '
                                'weekend. In the end they decided to go to the cinema first and '
                                'then (5)___ in the park. Michael paid for the order — 15 pounds. '
                                'Anna preferred quiet weekends with books, but today she wanted '
                                'something fun. Michael wanted to try a new film and then get some '
                                'fresh air. The café was busy, but their table near the window was '
                                'free. They left happy and already planned to meet again next '
                                'Saturday.',
                 'answers': ['met', 'piece', 'fruit', 'plans', 'walk'],
                 'word_bank': ['met', 'piece', 'fruit', 'plans', 'walk', 'red'],
                 'questions': [{'q': "How much did Michael's order cost?",
                                'accept': ['15 pounds', '15', 'fifteen pounds', '£15'],
                                'hint_ru': 'Найди в тексте сумму, которую заплатил Майкл.',
                                'quote': 'Michael paid for the order — 15 pounds.',
                                'model_en': "Michael's order cost 15 pounds."},
                               {'q': 'What kind of weekends did Anna usually prefer?',
                                'accept': ['quiet weekends with books',
                                           'quiet',
                                           'books',
                                           'reading'],
                                'hint_ru': 'Что Анна обычно предпочитала делать на выходных?',
                                'quote': 'Anna preferred quiet weekends with books…',
                                'model_en': 'Anna usually preferred quiet weekends with books.'},
                               {'q': 'What time did the friends meet?',
                                'accept': ['2 p.m.', '2 pm', '2', 'two', 'at 2'],
                                'hint_ru': 'Во сколько друзья встретились?',
                                'quote': '…met at a café at 2 p.m.',
                                'model_en': 'The friends met at 2 p.m.'},
                               {'q': 'What did Michael want to do after the cinema?',
                                'accept': ['walk in the park',
                                           'get fresh air',
                                           'park',
                                           'fresh air'],
                                'hint_ru': 'Что Майкл хотел сделать после кино?',
                                'quote': '…then walk in the park / get some fresh air.',
                                'model_en': 'Michael wanted to walk in the park after the '
                                            'cinema.'}],
                 'plan': ['Where and when the friends met',
                          'What they ordered',
                          'What they discussed and decided',
                          'Who paid and how much'],
                 'facts': ['They met at a café at 2 p.m.',
                           'Michael ordered coffee and chocolate cake; Anna ordered green tea and '
                           'fruit salad.',
                           'They discussed weekend plans and decided on cinema then park.',
                           'Michael paid 15 pounds.']},
        'daily': {'full_text': 'Dana reads a short text about Daily routine. The text focuses on '
                               'wake up, breakfast, work, evening. Dana makes a plan before '
                               'practice. At ten Dana meets Chris near the café. Chris wants to '
                               'visit a museum, but Dana prefers the café. In the end they choose '
                               'the café because it is warm. They buy water and sit for half an '
                               'hour. Dana pays three pounds for the drinks. Chris takes notes and '
                               'sends one photo to family. They agree to meet again next Friday '
                               'and Dana puts the notes in a bag. Before leaving, Chris checks the '
                               'time on a phone.',
                  'gapped_text': 'Dana reads a short text about Daily routine. The text focuses on '
                                 'wake up, breakfast, work, evening. Dana makes a (1)___ before '
                                 'practice. At ten Dana meets Chris near the café. Chris wants to '
                                 'visit a museum, but Dana prefers the café. In the end they '
                                 'choose the café because it is (2)___. They buy water and sit for '
                                 'half an hour. Dana pays three pounds for the drinks. Chris takes '
                                 'notes and sends one photo to family. They agree to meet again '
                                 'next (3)___ and Dana puts the notes in a (4)___. Before leaving, '
                                 'Chris checks the time on a (5)___.',
                  'answers': ['plan', 'warm', 'Friday', 'bag', 'phone'],
                  'word_bank': ['plan', 'warm', 'Friday', 'bag', 'phone', 'winter'],
                  'questions': [{'q': "What is Dana's text about?",
                                 'accept': ['Daily routine', 'daily routine'],
                                 'hint_ru': 'О чём текст в начале?',
                                 'quote': '…text about Daily routine.',
                                 'model_en': 'The text is about Daily routine.'},
                                {'q': 'What time does Dana meet Chris?',
                                 'accept': ['ten', '10', 'at ten'],
                                 'hint_ru': 'Во сколько они встречаются?',
                                 'quote': 'At ten Dana meets Chris…',
                                 'model_en': 'Dana meets Chris at ten.'},
                                {'q': 'Why do they choose the café?',
                                 'accept': ['warm', 'it is warm', 'because it is warm'],
                                 'hint_ru': 'Почему они выбирают это место?',
                                 'quote': '…because it is warm.',
                                 'model_en': 'They choose the café because it is warm.'},
                                {'q': 'When do they agree to meet again?',
                                 'accept': ['next Friday', 'Friday'],
                                 'hint_ru': 'Когда следующая встреча?',
                                 'quote': '…meet again next Friday…',
                                 'model_en': 'They agree to meet again next Friday.'}],
                  'plan': ['Topic of the text (Daily routine)',
                           'Meeting near the café',
                           'Why they stay there',
                           'Payment and next day'],
                  'facts': ['Dana reads about Daily routine (wake up, breakfast, work, evening).',
                            'They meet at ten near the café.',
                            'They choose it because it is warm.',
                            'Dana pays three pounds; next meeting is Friday.']},
        'hobbies': {'full_text': 'Omar reads a short text about Hobbies. The text focuses on '
                                 'sport, music, films, free time. Omar makes a plan before '
                                 'practice. At ten Omar meets Olga near the library. Olga wants to '
                                 'visit a museum, but Omar prefers the library. In the end they '
                                 'choose the library because it is warm. They buy water and sit '
                                 'for half an hour. Omar pays five pounds for the drinks. Olga '
                                 'takes notes and sends one photo to family. They agree to meet '
                                 'again next Tuesday and Omar puts the notes in a folder. Before '
                                 'leaving, Olga checks the time on a phone.',
                    'gapped_text': 'Omar reads a short text about Hobbies. The text focuses on '
                                   'sport, music, films, free time. Omar makes a (1)___ before '
                                   'practice. At ten Omar meets Olga near the library. Olga wants '
                                   'to visit a museum, but Omar prefers the library. In the end '
                                   'they choose the library because it is (2)___. They buy water '
                                   'and sit for half an hour. Omar pays five pounds for the '
                                   'drinks. Olga takes notes and sends one photo to family. They '
                                   'agree to meet again next (3)___ and Omar puts the notes in a '
                                   '(4)___. Before leaving, Olga checks the time on a (5)___.',
                    'answers': ['plan', 'warm', 'Tuesday', 'folder', 'phone'],
                    'word_bank': ['plan', 'warm', 'Tuesday', 'folder', 'phone', 'purple'],
                    'questions': [{'q': "What is Omar's text about?",
                                   'accept': ['Hobbies', 'hobbies'],
                                   'hint_ru': 'О чём текст в начале?',
                                   'quote': '…text about Hobbies.',
                                   'model_en': 'The text is about Hobbies.'},
                                  {'q': 'What time does Omar meet Olga?',
                                   'accept': ['ten', '10', 'at ten'],
                                   'hint_ru': 'Во сколько они встречаются?',
                                   'quote': 'At ten Omar meets Olga…',
                                   'model_en': 'Omar meets Olga at ten.'},
                                  {'q': 'Why do they choose the library?',
                                   'accept': ['warm', 'it is warm', 'because it is warm'],
                                   'hint_ru': 'Почему они выбирают это место?',
                                   'quote': '…because it is warm.',
                                   'model_en': 'They choose the library because it is warm.'},
                                  {'q': 'When do they agree to meet again?',
                                   'accept': ['next Tuesday', 'Tuesday'],
                                   'hint_ru': 'Когда следующая встреча?',
                                   'quote': '…meet again next Tuesday…',
                                   'model_en': 'They agree to meet again next Tuesday.'}],
                    'plan': ['Topic of the text (Hobbies)',
                             'Meeting near the library',
                             'Why they stay there',
                             'Payment and next day'],
                    'facts': ['Omar reads about Hobbies (sport, music, films, free time).',
                              'They meet at ten near the library.',
                              'They choose it because it is warm.',
                              'Omar pays five pounds; next meeting is Tuesday.']},
        'shopping': {'full_text': 'Sara reads a short text about Shopping. The text focuses on '
                                  'price, size, clothes, pay. Sara makes a plan before practice. '
                                  'At ten Sara meets Rita near the museum. Rita wants to visit a '
                                  'cinema, but Sara prefers the museum. In the end they choose the '
                                  'museum because it is warm. They buy water and sit for half an '
                                  'hour. Sara pays six pounds for the drinks. Rita takes notes and '
                                  'sends one photo to family. They agree to meet again next '
                                  'Wednesday and Sara puts the notes in a backpack. Before '
                                  'leaving, Rita checks the time on a phone.',
                     'gapped_text': 'Sara reads a short text about Shopping. The text focuses on '
                                    'price, size, clothes, pay. Sara makes a (1)___ before '
                                    'practice. At ten Sara meets Rita near the museum. Rita wants '
                                    'to visit a cinema, but Sara prefers the museum. In the end '
                                    'they choose the museum because it is (2)___. They buy water '
                                    'and sit for half an hour. Sara pays six pounds for the '
                                    'drinks. Rita takes notes and sends one photo to family. They '
                                    'agree to meet again next (3)___ and Sara puts the notes in a '
                                    '(4)___. Before leaving, Rita checks the time on a (5)___.',
                     'answers': ['plan', 'warm', 'Wednesday', 'backpack', 'phone'],
                     'word_bank': ['plan', 'warm', 'Wednesday', 'backpack', 'phone', 'zebra'],
                     'questions': [{'q': "What is Sara's text about?",
                                    'accept': ['Shopping', 'shopping'],
                                    'hint_ru': 'О чём текст в начале?',
                                    'quote': '…text about Shopping.',
                                    'model_en': 'The text is about Shopping.'},
                                   {'q': 'What time does Sara meet Rita?',
                                    'accept': ['ten', '10', 'at ten'],
                                    'hint_ru': 'Во сколько они встречаются?',
                                    'quote': 'At ten Sara meets Rita…',
                                    'model_en': 'Sara meets Rita at ten.'},
                                   {'q': 'Why do they choose the museum?',
                                    'accept': ['warm', 'it is warm', 'because it is warm'],
                                    'hint_ru': 'Почему они выбирают это место?',
                                    'quote': '…because it is warm.',
                                    'model_en': 'They choose the museum because it is warm.'},
                                   {'q': 'When do they agree to meet again?',
                                    'accept': ['next Wednesday', 'Wednesday'],
                                    'hint_ru': 'Когда следующая встреча?',
                                    'quote': '…meet again next Wednesday…',
                                    'model_en': 'They agree to meet again next Wednesday.'}],
                     'plan': ['Topic of the text (Shopping)',
                              'Meeting near the museum',
                              'Why they stay there',
                              'Payment and next day'],
                     'facts': ['Sara reads about Shopping (price, size, clothes, pay).',
                               'They meet at ten near the museum.',
                               'They choose it because it is warm.',
                               'Sara pays six pounds; next meeting is Wednesday.']},
        'weekend': {'full_text': 'Omar reads a short text about Weekend plans. The text focuses on '
                                 'cinema, park, meet friends. Omar makes a plan before practice. '
                                 'At ten Omar meets Rita near the park. Rita wants to visit a '
                                 'museum, but Omar prefers the park. In the end they choose the '
                                 'park because it is quiet. They buy water and sit for half an '
                                 'hour. Omar pays four pounds for the drinks. Rita takes notes and '
                                 'sends one photo to family. They agree to meet again next '
                                 'Saturday and Omar puts the notes in a folder. Before leaving, '
                                 'Rita checks the time on a phone.',
                    'gapped_text': 'Omar reads a short text about Weekend plans. The text focuses '
                                   'on cinema, park, meet friends. Omar makes a (1)___ before '
                                   'practice. At ten Omar meets Rita near the park. Rita wants to '
                                   'visit a museum, but Omar prefers the park. In the end they '
                                   'choose the park because it is (2)___. They buy water and sit '
                                   'for half an hour. Omar pays four pounds for the drinks. Rita '
                                   'takes notes and sends one photo to family. They agree to meet '
                                   'again next (3)___ and Omar puts the notes in a (4)___. Before '
                                   'leaving, Rita checks the time on a (5)___.',
                    'answers': ['plan', 'quiet', 'Saturday', 'folder', 'phone'],
                    'word_bank': ['plan', 'quiet', 'Saturday', 'folder', 'phone', 'silent'],
                    'questions': [{'q': "What is Omar's text about?",
                                   'accept': ['Weekend plans', 'weekend plans'],
                                   'hint_ru': 'О чём текст в начале?',
                                   'quote': '…text about Weekend plans.',
                                   'model_en': 'The text is about Weekend plans.'},
                                  {'q': 'What time does Omar meet Rita?',
                                   'accept': ['ten', '10', 'at ten'],
                                   'hint_ru': 'Во сколько они встречаются?',
                                   'quote': 'At ten Omar meets Rita…',
                                   'model_en': 'Omar meets Rita at ten.'},
                                  {'q': 'Why do they choose the park?',
                                   'accept': ['quiet', 'it is quiet', 'because it is quiet'],
                                   'hint_ru': 'Почему они выбирают это место?',
                                   'quote': '…because it is quiet.',
                                   'model_en': 'They choose the park because it is quiet.'},
                                  {'q': 'When do they agree to meet again?',
                                   'accept': ['next Saturday', 'Saturday'],
                                   'hint_ru': 'Когда следующая встреча?',
                                   'quote': '…meet again next Saturday…',
                                   'model_en': 'They agree to meet again next Saturday.'}],
                    'plan': ['Topic of the text (Weekend plans)',
                             'Meeting near the park',
                             'Why they stay there',
                             'Payment and next day'],
                    'facts': ['Omar reads about Weekend plans (cinema, park, meet friends).',
                              'They meet at ten near the park.',
                              'They choose it because it is quiet.',
                              'Omar pays four pounds; next meeting is Saturday.']},
        'school_day': {'full_text': 'Sara reads a short text about A school day. The text focuses '
                                    'on lessons, homework, break. Sara makes a plan before '
                                    'practice. At ten Sara meets Rita near the school. Rita wants '
                                    'to visit a museum, but Sara prefers the school. In the end '
                                    'they choose the school because it is warm. They buy water and '
                                    'sit for half an hour. Sara pays six pounds for the drinks. '
                                    'Rita takes notes and sends one photo to family. They agree to '
                                    'meet again next Wednesday and Sara puts the notes in a bag. '
                                    'Before leaving, Rita checks the time on a phone.',
                       'gapped_text': 'Sara reads a short text about A school day. The text '
                                      'focuses on lessons, homework, break. Sara makes a (1)___ '
                                      'before practice. At ten Sara meets Rita near the school. '
                                      'Rita wants to visit a museum, but Sara prefers the school. '
                                      'In the end they choose the school because it is (2)___. '
                                      'They buy water and sit for half an hour. Sara pays six '
                                      'pounds for the drinks. Rita takes notes and sends one photo '
                                      'to family. They agree to meet again next (3)___ and Sara '
                                      'puts the notes in a (4)___. Before leaving, Rita checks the '
                                      'time on a (5)___.',
                       'answers': ['plan', 'warm', 'Wednesday', 'bag', 'phone'],
                       'word_bank': ['plan', 'warm', 'Wednesday', 'bag', 'phone', 'purple'],
                       'questions': [{'q': "What is Sara's text about?",
                                      'accept': ['A school day', 'a school day'],
                                      'hint_ru': 'О чём текст в начале?',
                                      'quote': '…text about A school day.',
                                      'model_en': 'The text is about A school day.'},
                                     {'q': 'What time does Sara meet Rita?',
                                      'accept': ['ten', '10', 'at ten'],
                                      'hint_ru': 'Во сколько они встречаются?',
                                      'quote': 'At ten Sara meets Rita…',
                                      'model_en': 'Sara meets Rita at ten.'},
                                     {'q': 'Why do they choose the school?',
                                      'accept': ['warm', 'it is warm', 'because it is warm'],
                                      'hint_ru': 'Почему они выбирают это место?',
                                      'quote': '…because it is warm.',
                                      'model_en': 'They choose the school because it is warm.'},
                                     {'q': 'When do they agree to meet again?',
                                      'accept': ['next Wednesday', 'Wednesday'],
                                      'hint_ru': 'Когда следующая встреча?',
                                      'quote': '…meet again next Wednesday…',
                                      'model_en': 'They agree to meet again next Wednesday.'}],
                       'plan': ['Topic of the text (A school day)',
                                'Meeting near the school',
                                'Why they stay there',
                                'Payment and next day'],
                       'facts': ['Sara reads about A school day (lessons, homework, break).',
                                 'They meet at ten near the school.',
                                 'They choose it because it is warm.',
                                 'Sara pays six pounds; next meeting is Wednesday.']},
        'weather': {'full_text': 'Yesterday the weather was rainy and cold. Mia wore a warm coat '
                                 'and took an umbrella. She walked to the bus stop slowly. Today '
                                 'the sky is blue and the sun is bright. Mia puts the umbrella '
                                 'back in the hall. She chooses a light jacket instead of the '
                                 'coat. Her brother wants to play football in the park. Mum says '
                                 'they can go if it stays sunny. In the evening it may become '
                                 'windy. Mia checks the weather on her phone again.',
                    'gapped_text': 'Yesterday the weather was rainy and cold. Mia wore a warm coat '
                                   'and took an (1)___. She walked to the bus stop slowly. Today '
                                   'the sky is blue and the sun is bright. Mia puts the umbrella '
                                   'back in the hall. She chooses a light (2)___ instead of the '
                                   'coat. Her brother wants to play football in the (3)___. Mum '
                                   'says they can go if it stays (4)___. In the evening it may '
                                   'become windy. Mia checks the weather on her (5)___ again.',
                    'answers': ['umbrella', 'jacket', 'park', 'sunny', 'phone'],
                    'word_bank': ['umbrella', 'jacket', 'park', 'sunny', 'phone', 'snowy'],
                    'questions': [{'q': 'What was the weather like yesterday?',
                                   'accept': ['rainy and cold', 'rainy', 'cold'],
                                   'hint_ru': 'Какая была погода вчера?',
                                   'quote': 'Yesterday the weather was rainy and cold.',
                                   'model_en': 'Yesterday the weather was rainy and cold.'},
                                  {'q': 'What does Mia choose today instead of the coat?',
                                   'accept': ['light jacket', 'jacket'],
                                   'hint_ru': 'Что она выбирает вместо пальто?',
                                   'quote': '…a light jacket instead of the coat.',
                                   'model_en': 'Mia chooses a light jacket instead of the coat.'},
                                  {'q': 'Where does her brother want to play football?',
                                   'accept': ['in the park', 'park'],
                                   'hint_ru': 'Где брат хочет играть в футбол?',
                                   'quote': '…in the park.',
                                   'model_en': 'Her brother wants to play football in the park.'},
                                  {'q': 'When may it become windy?',
                                   'accept': ['in the evening', 'evening'],
                                   'hint_ru': 'Когда может стать ветрено?',
                                   'quote': 'In the evening it may become windy.',
                                   'model_en': 'It may become windy in the evening.'}],
                    'plan': ['Yesterday weather and clothes',
                             'Today sky and jacket',
                             'Park plans',
                             'Evening wind and phone'],
                    'facts': ['Yesterday was rainy and cold; Mia took an umbrella.',
                              'Today is sunny; she chooses a light jacket.',
                              'Brother wants football in the park if it stays sunny.',
                              'Evening may be windy; Mia checks her phone.']}},
 'A2': {'travel': {'full_text': 'Last week Nora prepared a short presentation about A short trip. '
                                'Examples were related to train, ticket, hotel, sightseeing. Nora '
                                'made a clear plan before writing. On Tuesday Nora met Nina in the '
                                'city park. Nina wanted a museum first, but Nora preferred the '
                                'quiet park. They stayed because it was raining outside. They '
                                'worked for two hours and shared water. Nora paid three pounds for '
                                'printing. Nina saved the notes on a laptop. They agreed to '
                                'practise again next Thursday and Nora put the printouts in a '
                                'folder. Before leaving, Nina locked the laptop in a bag.',
                   'gapped_text': 'Last week Nora prepared a short presentation about A short '
                                  'trip. Examples were related to train, ticket, hotel, '
                                  'sightseeing. Nora made a clear (1)___ before writing. On '
                                  'Tuesday Nora met Nina in the city park. Nina wanted a museum '
                                  'first, but Nora preferred the quiet park. They stayed because '
                                  'it was (2)___ outside. They worked for two hours and shared '
                                  'water. Nora paid three pounds for printing. Nina saved the '
                                  'notes on a laptop. They agreed to practise again next (3)___ '
                                  'and Nora put the printouts in a (4)___. Before leaving, Nina '
                                  'locked the (5)___ in a bag.',
                   'answers': ['plan', 'raining', 'Thursday', 'folder', 'laptop'],
                   'word_bank': ['plan', 'raining', 'Thursday', 'folder', 'laptop', 'purple'],
                   'questions': [{'q': "What was Nora's presentation about?",
                                  'accept': ['A short trip', 'a short trip'],
                                  'hint_ru': 'О чём презентация?',
                                  'quote': '…presentation about A short trip.',
                                  'model_en': 'The presentation was about A short trip.'},
                                 {'q': 'Why did they stay?',
                                  'accept': ['raining', 'because it was raining', 'rain'],
                                  'hint_ru': 'Почему они остались?',
                                  'quote': '…because it was raining outside.',
                                  'model_en': 'They stayed because it was raining outside.'},
                                 {'q': 'How much did Nora pay for printing?',
                                  'accept': ['three pounds', 'three'],
                                  'hint_ru': 'Сколько заплатили за печать?',
                                  'quote': 'Nora paid three pounds for printing.',
                                  'model_en': 'Nora paid three pounds for printing.'},
                                 {'q': 'When will they practise again?',
                                  'accept': ['next Thursday', 'Thursday'],
                                  'hint_ru': 'Когда следующая практика?',
                                  'quote': '…practise again next Thursday…',
                                  'model_en': 'They will practise again next Thursday.'}],
                   'plan': ['Presentation topic (A short trip)',
                            'Meeting at the park',
                            'Why they stayed',
                            'Payment and next practice'],
                   'facts': ['Nora presented about A short trip.',
                             'It was raining, so they stayed.',
                             'Nora paid three pounds for printing.',
                             'Next practice is Thursday.']},
        'doctor': {'full_text': 'Last week Nora prepared a short presentation about At the doctor. '
                                'Examples were related to symptoms, medicine, rest. Nora made a '
                                'clear plan before writing. On Tuesday Nora met Nina in the city '
                                'museum. Nina wanted a cinema first, but Nora preferred the quiet '
                                'museum. They stayed because it was raining outside. They worked '
                                'for two hours and shared water. Nora paid three pounds for '
                                'printing. Nina saved the notes on a laptop. They agreed to '
                                'practise again next Thursday and Nora put the printouts in a '
                                'folder. Before leaving, Nina locked the laptop in a bag.',
                   'gapped_text': 'Last week Nora prepared a short presentation about At the '
                                  'doctor. Examples were related to symptoms, medicine, rest. Nora '
                                  'made a clear (1)___ before writing. On Tuesday Nora met Nina in '
                                  'the city museum. Nina wanted a cinema first, but Nora preferred '
                                  'the quiet museum. They stayed because it was (2)___ outside. '
                                  'They worked for two hours and shared water. Nora paid three '
                                  'pounds for printing. Nina saved the notes on a laptop. They '
                                  'agreed to practise again next (3)___ and Nora put the printouts '
                                  'in a (4)___. Before leaving, Nina locked the (5)___ in a bag.',
                   'answers': ['plan', 'raining', 'Thursday', 'folder', 'laptop'],
                   'word_bank': ['plan', 'raining', 'Thursday', 'folder', 'laptop', 'silent'],
                   'questions': [{'q': "What was Nora's presentation about?",
                                  'accept': ['At the doctor', 'at the doctor'],
                                  'hint_ru': 'О чём презентация?',
                                  'quote': '…presentation about At the doctor.',
                                  'model_en': 'The presentation was about At the doctor.'},
                                 {'q': 'Why did they stay?',
                                  'accept': ['raining', 'because it was raining', 'rain'],
                                  'hint_ru': 'Почему они остались?',
                                  'quote': '…because it was raining outside.',
                                  'model_en': 'They stayed because it was raining outside.'},
                                 {'q': 'How much did Nora pay for printing?',
                                  'accept': ['three pounds', 'three'],
                                  'hint_ru': 'Сколько заплатили за печать?',
                                  'quote': 'Nora paid three pounds for printing.',
                                  'model_en': 'Nora paid three pounds for printing.'},
                                 {'q': 'When will they practise again?',
                                  'accept': ['next Thursday', 'Thursday'],
                                  'hint_ru': 'Когда следующая практика?',
                                  'quote': '…practise again next Thursday…',
                                  'model_en': 'They will practise again next Thursday.'}],
                   'plan': ['Presentation topic (At the doctor)',
                            'Meeting at the museum',
                            'Why they stayed',
                            'Payment and next practice'],
                   'facts': ['Nora presented about At the doctor.',
                             'It was raining, so they stayed.',
                             'Nora paid three pounds for printing.',
                             'Next practice is Thursday.']},
        'party': {'full_text': 'Last week Tom prepared a short presentation about A birthday '
                               'party. Examples were related to guests, gifts, food, music. Tom '
                               'made a clear plan before writing. On Tuesday Tom met Nick in the '
                               'city library. Nick wanted a museum first, but Tom preferred the '
                               'quiet library. They stayed because it was raining outside. They '
                               'worked for two hours and shared water. Tom paid three pounds for '
                               'printing. Nick saved the notes on a laptop. They agreed to '
                               'practise again next Wednesday and Tom put the printouts in a '
                               'backpack. Before leaving, Nick locked the laptop in a bag.',
                  'gapped_text': 'Last week Tom prepared a short presentation about A birthday '
                                 'party. Examples were related to guests, gifts, food, music. Tom '
                                 'made a clear (1)___ before writing. On Tuesday Tom met Nick in '
                                 'the city library. Nick wanted a museum first, but Tom preferred '
                                 'the quiet library. They stayed because it was (2)___ outside. '
                                 'They worked for two hours and shared water. Tom paid three '
                                 'pounds for printing. Nick saved the notes on a laptop. They '
                                 'agreed to practise again next (3)___ and Tom put the printouts '
                                 'in a (4)___. Before leaving, Nick locked the (5)___ in a bag.',
                  'answers': ['plan', 'raining', 'Wednesday', 'backpack', 'laptop'],
                  'word_bank': ['plan', 'raining', 'Wednesday', 'backpack', 'laptop', 'purple'],
                  'questions': [{'q': "What was Tom's presentation about?",
                                 'accept': ['A birthday party', 'a birthday party'],
                                 'hint_ru': 'О чём презентация?',
                                 'quote': '…presentation about A birthday party.',
                                 'model_en': 'The presentation was about A birthday party.'},
                                {'q': 'Why did they stay?',
                                 'accept': ['raining', 'because it was raining', 'rain'],
                                 'hint_ru': 'Почему они остались?',
                                 'quote': '…because it was raining outside.',
                                 'model_en': 'They stayed because it was raining outside.'},
                                {'q': 'How much did Tom pay for printing?',
                                 'accept': ['three pounds', 'three'],
                                 'hint_ru': 'Сколько заплатили за печать?',
                                 'quote': 'Tom paid three pounds for printing.',
                                 'model_en': 'Tom paid three pounds for printing.'},
                                {'q': 'When will they practise again?',
                                 'accept': ['next Wednesday', 'Wednesday'],
                                 'hint_ru': 'Когда следующая практика?',
                                 'quote': '…practise again next Wednesday…',
                                 'model_en': 'They will practise again next Wednesday.'}],
                  'plan': ['Presentation topic (A birthday party)',
                           'Meeting at the library',
                           'Why they stayed',
                           'Payment and next practice'],
                  'facts': ['Tom presented about A birthday party.',
                            'It was raining, so they stayed.',
                            'Tom paid three pounds for printing.',
                            'Next practice is Wednesday.']},
        'sport': {'full_text': 'Last week Mia prepared a short presentation about Sport and '
                               'health. Examples were related to gym, run, tired, healthy. Mia '
                               'made a clear plan before writing. On Tuesday Mia met Sam in the '
                               'city café. Sam wanted a museum first, but Mia preferred the quiet '
                               'café. They stayed because it was raining outside. They worked for '
                               'two hours and shared water. Mia paid three pounds for printing. '
                               'Sam saved the notes on a laptop. They agreed to practise again '
                               'next Tuesday and Mia put the printouts in a backpack. Before '
                               'leaving, Sam locked the laptop in a bag.',
                  'gapped_text': 'Last week Mia prepared a short presentation about Sport and '
                                 'health. Examples were related to gym, run, tired, healthy. Mia '
                                 'made a clear (1)___ before writing. On Tuesday Mia met Sam in '
                                 'the city café. Sam wanted a museum first, but Mia preferred the '
                                 'quiet café. They stayed because it was (2)___ outside. They '
                                 'worked for two hours and shared water. Mia paid three pounds for '
                                 'printing. Sam saved the notes on a laptop. They agreed to '
                                 'practise again next (3)___ and Mia put the printouts in a '
                                 '(4)___. Before leaving, Sam locked the (5)___ in a bag.',
                  'answers': ['plan', 'raining', 'Tuesday', 'backpack', 'laptop'],
                  'word_bank': ['plan', 'raining', 'Tuesday', 'backpack', 'laptop', 'silent'],
                  'questions': [{'q': "What was Mia's presentation about?",
                                 'accept': ['Sport and health', 'sport and health'],
                                 'hint_ru': 'О чём презентация?',
                                 'quote': '…presentation about Sport and health.',
                                 'model_en': 'The presentation was about Sport and health.'},
                                {'q': 'Why did they stay?',
                                 'accept': ['raining', 'because it was raining', 'rain'],
                                 'hint_ru': 'Почему они остались?',
                                 'quote': '…because it was raining outside.',
                                 'model_en': 'They stayed because it was raining outside.'},
                                {'q': 'How much did Mia pay for printing?',
                                 'accept': ['three pounds', 'three'],
                                 'hint_ru': 'Сколько заплатили за печать?',
                                 'quote': 'Mia paid three pounds for printing.',
                                 'model_en': 'Mia paid three pounds for printing.'},
                                {'q': 'When will they practise again?',
                                 'accept': ['next Tuesday', 'Tuesday'],
                                 'hint_ru': 'Когда следующая практика?',
                                 'quote': '…practise again next Tuesday…',
                                 'model_en': 'They will practise again next Tuesday.'}],
                  'plan': ['Presentation topic (Sport and health)',
                           'Meeting at the café',
                           'Why they stayed',
                           'Payment and next practice'],
                  'facts': ['Mia presented about Sport and health.',
                            'It was raining, so they stayed.',
                            'Mia paid three pounds for printing.',
                            'Next practice is Tuesday.']},
        'neighbours': {'full_text': 'Last week Ben prepared a short presentation about Neighbours. '
                                    'Examples were related to noise, help, flat, evening. Ben made '
                                    'a clear plan before writing. On Tuesday Ben met Alex in the '
                                    'city museum. Alex wanted a cinema first, but Ben preferred '
                                    'the quiet museum. They stayed because it was raining outside. '
                                    'They worked for two hours and shared water. Ben paid four '
                                    'pounds for printing. Alex saved the notes on a laptop. They '
                                    'agreed to practise again next Tuesday and Ben put the '
                                    'printouts in a folder. Before leaving, Alex locked the laptop '
                                    'in a bag.',
                       'gapped_text': 'Last week Ben prepared a short presentation about '
                                      'Neighbours. Examples were related to noise, help, flat, '
                                      'evening. Ben made a clear (1)___ before writing. On Tuesday '
                                      'Ben met Alex in the city museum. Alex wanted a cinema '
                                      'first, but Ben preferred the quiet museum. They stayed '
                                      'because it was (2)___ outside. They worked for two hours '
                                      'and shared water. Ben paid four pounds for printing. Alex '
                                      'saved the notes on a laptop. They agreed to practise again '
                                      'next (3)___ and Ben put the printouts in a (4)___. Before '
                                      'leaving, Alex locked the (5)___ in a bag.',
                       'answers': ['plan', 'raining', 'Tuesday', 'folder', 'laptop'],
                       'word_bank': ['plan', 'raining', 'Tuesday', 'folder', 'laptop', 'heavy'],
                       'questions': [{'q': "What was Ben's presentation about?",
                                      'accept': ['Neighbours', 'neighbours'],
                                      'hint_ru': 'О чём презентация?',
                                      'quote': '…presentation about Neighbours.',
                                      'model_en': 'The presentation was about Neighbours.'},
                                     {'q': 'Why did they stay?',
                                      'accept': ['raining', 'because it was raining', 'rain'],
                                      'hint_ru': 'Почему они остались?',
                                      'quote': '…because it was raining outside.',
                                      'model_en': 'They stayed because it was raining outside.'},
                                     {'q': 'How much did Ben pay for printing?',
                                      'accept': ['four pounds', 'four'],
                                      'hint_ru': 'Сколько заплатили за печать?',
                                      'quote': 'Ben paid four pounds for printing.',
                                      'model_en': 'Ben paid four pounds for printing.'},
                                     {'q': 'When will they practise again?',
                                      'accept': ['next Tuesday', 'Tuesday'],
                                      'hint_ru': 'Когда следующая практика?',
                                      'quote': '…practise again next Tuesday…',
                                      'model_en': 'They will practise again next Tuesday.'}],
                       'plan': ['Presentation topic (Neighbours)',
                                'Meeting at the museum',
                                'Why they stayed',
                                'Payment and next practice'],
                       'facts': ['Ben presented about Neighbours.',
                                 'It was raining, so they stayed.',
                                 'Ben paid four pounds for printing.',
                                 'Next practice is Tuesday.']},
        'lost': {'full_text': 'Last week Nora prepared a short presentation about A lost bag. '
                              'Examples were related to describe, colour, find, thank. Nora made a '
                              'clear plan before writing. On Tuesday Nora met Paul in the city '
                              'café. Paul wanted a museum first, but Nora preferred the quiet '
                              'café. They stayed because it was raining outside. They worked for '
                              'two hours and shared water. Nora paid three pounds for printing. '
                              'Paul saved the notes on a laptop. They agreed to practise again '
                              'next Tuesday and Nora put the printouts in a folder. Before '
                              'leaving, Paul locked the laptop in a bag.',
                 'gapped_text': 'Last week Nora prepared a short presentation about A lost bag. '
                                'Examples were related to describe, colour, find, thank. Nora made '
                                'a clear (1)___ before writing. On Tuesday Nora met Paul in the '
                                'city café. Paul wanted a museum first, but Nora preferred the '
                                'quiet café. They stayed because it was (2)___ outside. They '
                                'worked for two hours and shared water. Nora paid three pounds for '
                                'printing. Paul saved the notes on a laptop. They agreed to '
                                'practise again next (3)___ and Nora put the printouts in a '
                                '(4)___. Before leaving, Paul locked the (5)___ in a bag.',
                 'answers': ['plan', 'raining', 'Tuesday', 'folder', 'laptop'],
                 'word_bank': ['plan', 'raining', 'Tuesday', 'folder', 'laptop', 'winter'],
                 'questions': [{'q': "What was Nora's presentation about?",
                                'accept': ['A lost bag', 'a lost bag'],
                                'hint_ru': 'О чём презентация?',
                                'quote': '…presentation about A lost bag.',
                                'model_en': 'The presentation was about A lost bag.'},
                               {'q': 'Why did they stay?',
                                'accept': ['raining', 'because it was raining', 'rain'],
                                'hint_ru': 'Почему они остались?',
                                'quote': '…because it was raining outside.',
                                'model_en': 'They stayed because it was raining outside.'},
                               {'q': 'How much did Nora pay for printing?',
                                'accept': ['three pounds', 'three'],
                                'hint_ru': 'Сколько заплатили за печать?',
                                'quote': 'Nora paid three pounds for printing.',
                                'model_en': 'Nora paid three pounds for printing.'},
                               {'q': 'When will they practise again?',
                                'accept': ['next Tuesday', 'Tuesday'],
                                'hint_ru': 'Когда следующая практика?',
                                'quote': '…practise again next Tuesday…',
                                'model_en': 'They will practise again next Tuesday.'}],
                 'plan': ['Presentation topic (A lost bag)',
                          'Meeting at the café',
                          'Why they stayed',
                          'Payment and next practice'],
                 'facts': ['Nora presented about A lost bag.',
                           'It was raining, so they stayed.',
                           'Nora paid three pounds for printing.',
                           'Next practice is Tuesday.']},
        'restaurant': {'full_text': 'Last week Anna prepared a short presentation about '
                                    'Restaurant. Examples were related to menu, order, bill, tip. '
                                    'Anna made a clear plan before writing. On Tuesday Anna met '
                                    'Ivan in the city café. Ivan wanted a museum first, but Anna '
                                    'preferred the quiet café. They stayed because it was raining '
                                    'outside. They worked for two hours and shared water. Anna '
                                    'paid four pounds for printing. Ivan saved the notes on a '
                                    'laptop. They agreed to practise again next Friday and Anna '
                                    'put the printouts in a bag. Before leaving, Ivan locked the '
                                    'laptop in a bag.',
                       'gapped_text': 'Last week Anna prepared a short presentation about '
                                      'Restaurant. Examples were related to menu, order, bill, '
                                      'tip. Anna made a clear (1)___ before writing. On Tuesday '
                                      'Anna met Ivan in the city café. Ivan wanted a museum first, '
                                      'but Anna preferred the quiet café. They stayed because it '
                                      'was (2)___ outside. They worked for two hours and shared '
                                      'water. Anna paid four pounds for printing. Ivan saved the '
                                      'notes on a laptop. They agreed to practise again next '
                                      '(3)___ and Anna put the printouts in a (4)___. Before '
                                      'leaving, Ivan locked the (5)___ in a bag.',
                       'answers': ['plan', 'raining', 'Friday', 'bag', 'laptop'],
                       'word_bank': ['plan', 'raining', 'Friday', 'bag', 'laptop', 'purple'],
                       'questions': [{'q': "What was Anna's presentation about?",
                                      'accept': ['Restaurant', 'restaurant'],
                                      'hint_ru': 'О чём презентация?',
                                      'quote': '…presentation about Restaurant.',
                                      'model_en': 'The presentation was about Restaurant.'},
                                     {'q': 'Why did they stay?',
                                      'accept': ['raining', 'because it was raining', 'rain'],
                                      'hint_ru': 'Почему они остались?',
                                      'quote': '…because it was raining outside.',
                                      'model_en': 'They stayed because it was raining outside.'},
                                     {'q': 'How much did Anna pay for printing?',
                                      'accept': ['four pounds', 'four'],
                                      'hint_ru': 'Сколько заплатили за печать?',
                                      'quote': 'Anna paid four pounds for printing.',
                                      'model_en': 'Anna paid four pounds for printing.'},
                                     {'q': 'When will they practise again?',
                                      'accept': ['next Friday', 'Friday'],
                                      'hint_ru': 'Когда следующая практика?',
                                      'quote': '…practise again next Friday…',
                                      'model_en': 'They will practise again next Friday.'}],
                       'plan': ['Presentation topic (Restaurant)',
                                'Meeting at the café',
                                'Why they stayed',
                                'Payment and next practice'],
                       'facts': ['Anna presented about Restaurant.',
                                 'It was raining, so they stayed.',
                                 'Anna paid four pounds for printing.',
                                 'Next practice is Friday.']},
        'city': {'full_text': 'Last week Dana prepared a short presentation about My city. '
                              'Examples were related to park, museum, bus, favourite place. Dana '
                              'made a clear plan before writing. On Tuesday Dana met Nina in the '
                              'city park. Nina wanted a museum first, but Dana preferred the quiet '
                              'park. They stayed because it was raining outside. They worked for '
                              'two hours and shared water. Dana paid six pounds for printing. Nina '
                              'saved the notes on a laptop. They agreed to practise again next '
                              'Friday and Dana put the printouts in a backpack. Before leaving, '
                              'Nina locked the laptop in a bag.',
                 'gapped_text': 'Last week Dana prepared a short presentation about My city. '
                                'Examples were related to park, museum, bus, favourite place. Dana '
                                'made a clear (1)___ before writing. On Tuesday Dana met Nina in '
                                'the city park. Nina wanted a museum first, but Dana preferred the '
                                'quiet park. They stayed because it was (2)___ outside. They '
                                'worked for two hours and shared water. Dana paid six pounds for '
                                'printing. Nina saved the notes on a laptop. They agreed to '
                                'practise again next (3)___ and Dana put the printouts in a '
                                '(4)___. Before leaving, Nina locked the (5)___ in a bag.',
                 'answers': ['plan', 'raining', 'Friday', 'backpack', 'laptop'],
                 'word_bank': ['plan', 'raining', 'Friday', 'backpack', 'laptop', 'zebra'],
                 'questions': [{'q': "What was Dana's presentation about?",
                                'accept': ['My city', 'my city'],
                                'hint_ru': 'О чём презентация?',
                                'quote': '…presentation about My city.',
                                'model_en': 'The presentation was about My city.'},
                               {'q': 'Why did they stay?',
                                'accept': ['raining', 'because it was raining', 'rain'],
                                'hint_ru': 'Почему они остались?',
                                'quote': '…because it was raining outside.',
                                'model_en': 'They stayed because it was raining outside.'},
                               {'q': 'How much did Dana pay for printing?',
                                'accept': ['six pounds', 'six'],
                                'hint_ru': 'Сколько заплатили за печать?',
                                'quote': 'Dana paid six pounds for printing.',
                                'model_en': 'Dana paid six pounds for printing.'},
                               {'q': 'When will they practise again?',
                                'accept': ['next Friday', 'Friday'],
                                'hint_ru': 'Когда следующая практика?',
                                'quote': '…practise again next Friday…',
                                'model_en': 'They will practise again next Friday.'}],
                 'plan': ['Presentation topic (My city)',
                          'Meeting at the park',
                          'Why they stayed',
                          'Payment and next practice'],
                 'facts': ['Dana presented about My city.',
                           'It was raining, so they stayed.',
                           'Dana paid six pounds for printing.',
                           'Next practice is Friday.']}},
 'B1': {'interview': {'full_text': 'Last week Kate prepared a short presentation about Job '
                                   'interview. Examples were related to experience, hours, skills, '
                                   'start date. Kate made a clear plan before writing. On Tuesday '
                                   'Kate met Chris in the city office. Chris wanted a museum '
                                   'first, but Kate preferred the quiet office. They stayed '
                                   'because it was raining outside. They worked for two hours and '
                                   'shared water. Kate paid four pounds for printing. Chris saved '
                                   'the notes on a laptop. They agreed to practise again next '
                                   'Wednesday and Kate put the printouts in a folder. Before '
                                   'leaving, Chris locked the laptop in a bag.',
                      'gapped_text': 'Last week Kate prepared a short presentation about Job '
                                     'interview. Examples were related to experience, hours, '
                                     'skills, start date. Kate made a clear (1)___ before writing. '
                                     'On Tuesday Kate met Chris in the city office. Chris wanted a '
                                     'museum first, but Kate preferred the quiet office. They '
                                     'stayed because it was (2)___ outside. They worked for two '
                                     'hours and shared water. Kate paid four pounds for printing. '
                                     'Chris saved the notes on a laptop. They agreed to practise '
                                     'again next (3)___ and Kate put the printouts in a (4)___. '
                                     'Before leaving, Chris locked the (5)___ in a bag.',
                      'answers': ['plan', 'raining', 'Wednesday', 'folder', 'laptop'],
                      'word_bank': ['plan', 'raining', 'Wednesday', 'folder', 'laptop', 'heavy'],
                      'questions': [{'q': "What was Kate's presentation about?",
                                     'accept': ['Job interview', 'job interview'],
                                     'hint_ru': 'О чём презентация?',
                                     'quote': '…presentation about Job interview.',
                                     'model_en': 'The presentation was about Job interview.'},
                                    {'q': 'Why did they stay?',
                                     'accept': ['raining', 'because it was raining', 'rain'],
                                     'hint_ru': 'Почему они остались?',
                                     'quote': '…because it was raining outside.',
                                     'model_en': 'They stayed because it was raining outside.'},
                                    {'q': 'How much did Kate pay for printing?',
                                     'accept': ['four pounds', 'four'],
                                     'hint_ru': 'Сколько заплатили за печать?',
                                     'quote': 'Kate paid four pounds for printing.',
                                     'model_en': 'Kate paid four pounds for printing.'},
                                    {'q': 'When will they practise again?',
                                     'accept': ['next Wednesday', 'Wednesday'],
                                     'hint_ru': 'Когда следующая практика?',
                                     'quote': '…practise again next Wednesday…',
                                     'model_en': 'They will practise again next Wednesday.'}],
                      'plan': ['Presentation topic (Job interview)',
                               'Meeting at the office',
                               'Why they stayed',
                               'Payment and next practice'],
                      'facts': ['Kate presented about Job interview.',
                                'It was raining, so they stayed.',
                                'Kate paid four pounds for printing.',
                                'Next practice is Wednesday.']},
        'flatshare': {'full_text': 'Last week Sara prepared a short presentation about Sharing a '
                                   'flat. Examples were related to chores, rent, rules, guests. '
                                   'Sara made a clear plan before writing. On Tuesday Sara met '
                                   'Rita in the city park. Rita wanted a museum first, but Sara '
                                   'preferred the quiet park. They stayed because it was raining '
                                   'outside. They worked for two hours and shared water. Sara paid '
                                   'six pounds for printing. Rita saved the notes on a laptop. '
                                   'They agreed to practise again next Saturday and Sara put the '
                                   'printouts in a folder. Before leaving, Rita locked the laptop '
                                   'in a bag.',
                      'gapped_text': 'Last week Sara prepared a short presentation about Sharing a '
                                     'flat. Examples were related to chores, rent, rules, guests. '
                                     'Sara made a clear (1)___ before writing. On Tuesday Sara met '
                                     'Rita in the city park. Rita wanted a museum first, but Sara '
                                     'preferred the quiet park. They stayed because it was (2)___ '
                                     'outside. They worked for two hours and shared water. Sara '
                                     'paid six pounds for printing. Rita saved the notes on a '
                                     'laptop. They agreed to practise again next (3)___ and Sara '
                                     'put the printouts in a (4)___. Before leaving, Rita locked '
                                     'the (5)___ in a bag.',
                      'answers': ['plan', 'raining', 'Saturday', 'folder', 'laptop'],
                      'word_bank': ['plan', 'raining', 'Saturday', 'folder', 'laptop', 'zebra'],
                      'questions': [{'q': "What was Sara's presentation about?",
                                     'accept': ['Sharing a flat', 'sharing a flat'],
                                     'hint_ru': 'О чём презентация?',
                                     'quote': '…presentation about Sharing a flat.',
                                     'model_en': 'The presentation was about Sharing a flat.'},
                                    {'q': 'Why did they stay?',
                                     'accept': ['raining', 'because it was raining', 'rain'],
                                     'hint_ru': 'Почему они остались?',
                                     'quote': '…because it was raining outside.',
                                     'model_en': 'They stayed because it was raining outside.'},
                                    {'q': 'How much did Sara pay for printing?',
                                     'accept': ['six pounds', 'six'],
                                     'hint_ru': 'Сколько заплатили за печать?',
                                     'quote': 'Sara paid six pounds for printing.',
                                     'model_en': 'Sara paid six pounds for printing.'},
                                    {'q': 'When will they practise again?',
                                     'accept': ['next Saturday', 'Saturday'],
                                     'hint_ru': 'Когда следующая практика?',
                                     'quote': '…practise again next Saturday…',
                                     'model_en': 'They will practise again next Saturday.'}],
                      'plan': ['Presentation topic (Sharing a flat)',
                               'Meeting at the park',
                               'Why they stayed',
                               'Payment and next practice'],
                      'facts': ['Sara presented about Sharing a flat.',
                                'It was raining, so they stayed.',
                                'Sara paid six pounds for printing.',
                                'Next practice is Saturday.']},
        'online': {'full_text': 'Last week Kate prepared a short presentation about Online '
                                'shopping. Examples were related to delivery, return, review, '
                                'discount. Kate made a clear plan before writing. On Tuesday Kate '
                                'met Helen in the city museum. Helen wanted a cinema first, but '
                                'Kate preferred the quiet museum. They stayed because it was '
                                'raining outside. They worked for two hours and shared water. Kate '
                                'paid five pounds for printing. Helen saved the notes on a laptop. '
                                'They agreed to practise again next Friday and Kate put the '
                                'printouts in a backpack. Before leaving, Helen locked the laptop '
                                'in a bag.',
                   'gapped_text': 'Last week Kate prepared a short presentation about Online '
                                  'shopping. Examples were related to delivery, return, review, '
                                  'discount. Kate made a clear (1)___ before writing. On Tuesday '
                                  'Kate met Helen in the city museum. Helen wanted a cinema first, '
                                  'but Kate preferred the quiet museum. They stayed because it was '
                                  '(2)___ outside. They worked for two hours and shared water. '
                                  'Kate paid five pounds for printing. Helen saved the notes on a '
                                  'laptop. They agreed to practise again next (3)___ and Kate put '
                                  'the printouts in a (4)___. Before leaving, Helen locked the '
                                  '(5)___ in a bag.',
                   'answers': ['plan', 'raining', 'Friday', 'backpack', 'laptop'],
                   'word_bank': ['plan', 'raining', 'Friday', 'backpack', 'laptop', 'silent'],
                   'questions': [{'q': "What was Kate's presentation about?",
                                  'accept': ['Online shopping', 'online shopping'],
                                  'hint_ru': 'О чём презентация?',
                                  'quote': '…presentation about Online shopping.',
                                  'model_en': 'The presentation was about Online shopping.'},
                                 {'q': 'Why did they stay?',
                                  'accept': ['raining', 'because it was raining', 'rain'],
                                  'hint_ru': 'Почему они остались?',
                                  'quote': '…because it was raining outside.',
                                  'model_en': 'They stayed because it was raining outside.'},
                                 {'q': 'How much did Kate pay for printing?',
                                  'accept': ['five pounds', 'five'],
                                  'hint_ru': 'Сколько заплатили за печать?',
                                  'quote': 'Kate paid five pounds for printing.',
                                  'model_en': 'Kate paid five pounds for printing.'},
                                 {'q': 'When will they practise again?',
                                  'accept': ['next Friday', 'Friday'],
                                  'hint_ru': 'Когда следующая практика?',
                                  'quote': '…practise again next Friday…',
                                  'model_en': 'They will practise again next Friday.'}],
                   'plan': ['Presentation topic (Online shopping)',
                            'Meeting at the museum',
                            'Why they stayed',
                            'Payment and next practice'],
                   'facts': ['Kate presented about Online shopping.',
                             'It was raining, so they stayed.',
                             'Kate paid five pounds for printing.',
                             'Next practice is Friday.']},
        'volunteer': {'full_text': 'Last week Lena prepared a short presentation about '
                                   'Volunteering. Examples were related to weekend, help, team, '
                                   'local event. Lena made a clear plan before writing. On Tuesday '
                                   'Lena met Rita in the city park. Rita wanted a museum first, '
                                   'but Lena preferred the quiet park. They stayed because it was '
                                   'raining outside. They worked for two hours and shared water. '
                                   'Lena paid five pounds for printing. Rita saved the notes on a '
                                   'laptop. They agreed to practise again next Monday and Lena put '
                                   'the printouts in a folder. Before leaving, Rita locked the '
                                   'laptop in a bag.',
                      'gapped_text': 'Last week Lena prepared a short presentation about '
                                     'Volunteering. Examples were related to weekend, help, team, '
                                     'local event. Lena made a clear (1)___ before writing. On '
                                     'Tuesday Lena met Rita in the city park. Rita wanted a museum '
                                     'first, but Lena preferred the quiet park. They stayed '
                                     'because it was (2)___ outside. They worked for two hours and '
                                     'shared water. Lena paid five pounds for printing. Rita saved '
                                     'the notes on a laptop. They agreed to practise again next '
                                     '(3)___ and Lena put the printouts in a (4)___. Before '
                                     'leaving, Rita locked the (5)___ in a bag.',
                      'answers': ['plan', 'raining', 'Monday', 'folder', 'laptop'],
                      'word_bank': ['plan', 'raining', 'Monday', 'folder', 'laptop', 'zebra'],
                      'questions': [{'q': "What was Lena's presentation about?",
                                     'accept': ['Volunteering', 'volunteering'],
                                     'hint_ru': 'О чём презентация?',
                                     'quote': '…presentation about Volunteering.',
                                     'model_en': 'The presentation was about Volunteering.'},
                                    {'q': 'Why did they stay?',
                                     'accept': ['raining', 'because it was raining', 'rain'],
                                     'hint_ru': 'Почему они остались?',
                                     'quote': '…because it was raining outside.',
                                     'model_en': 'They stayed because it was raining outside.'},
                                    {'q': 'How much did Lena pay for printing?',
                                     'accept': ['five pounds', 'five'],
                                     'hint_ru': 'Сколько заплатили за печать?',
                                     'quote': 'Lena paid five pounds for printing.',
                                     'model_en': 'Lena paid five pounds for printing.'},
                                    {'q': 'When will they practise again?',
                                     'accept': ['next Monday', 'Monday'],
                                     'hint_ru': 'Когда следующая практика?',
                                     'quote': '…practise again next Monday…',
                                     'model_en': 'They will practise again next Monday.'}],
                      'plan': ['Presentation topic (Volunteering)',
                               'Meeting at the park',
                               'Why they stayed',
                               'Payment and next practice'],
                      'facts': ['Lena presented about Volunteering.',
                                'It was raining, so they stayed.',
                                'Lena paid five pounds for printing.',
                                'Next practice is Monday.']},
        'exam': {'full_text': 'Last week Mia prepared a short presentation about Preparing for an '
                              'exam. Examples were related to study plan, stress, library, '
                              'results. Mia made a clear plan before writing. On Tuesday Mia met '
                              'Alex in the city park. Alex wanted a museum first, but Mia '
                              'preferred the quiet park. They stayed because it was raining '
                              'outside. They worked for two hours and shared water. Mia paid five '
                              'pounds for printing. Alex saved the notes on a laptop. They agreed '
                              'to practise again next Thursday and Mia put the printouts in a bag. '
                              'Before leaving, Alex locked the laptop in a bag.',
                 'gapped_text': 'Last week Mia prepared a short presentation about Preparing for '
                                'an exam. Examples were related to study plan, stress, library, '
                                'results. Mia made a clear (1)___ before writing. On Tuesday Mia '
                                'met Alex in the city park. Alex wanted a museum first, but Mia '
                                'preferred the quiet park. They stayed because it was (2)___ '
                                'outside. They worked for two hours and shared water. Mia paid '
                                'five pounds for printing. Alex saved the notes on a laptop. They '
                                'agreed to practise again next (3)___ and Mia put the printouts in '
                                'a (4)___. Before leaving, Alex locked the (5)___ in a bag.',
                 'answers': ['plan', 'raining', 'Thursday', 'bag', 'laptop'],
                 'word_bank': ['plan', 'raining', 'Thursday', 'bag', 'laptop', 'winter'],
                 'questions': [{'q': "What was Mia's presentation about?",
                                'accept': ['Preparing for an exam', 'preparing for an exam'],
                                'hint_ru': 'О чём презентация?',
                                'quote': '…presentation about Preparing for an exam.',
                                'model_en': 'The presentation was about Preparing for an exam.'},
                               {'q': 'Why did they stay?',
                                'accept': ['raining', 'because it was raining', 'rain'],
                                'hint_ru': 'Почему они остались?',
                                'quote': '…because it was raining outside.',
                                'model_en': 'They stayed because it was raining outside.'},
                               {'q': 'How much did Mia pay for printing?',
                                'accept': ['five pounds', 'five'],
                                'hint_ru': 'Сколько заплатили за печать?',
                                'quote': 'Mia paid five pounds for printing.',
                                'model_en': 'Mia paid five pounds for printing.'},
                               {'q': 'When will they practise again?',
                                'accept': ['next Thursday', 'Thursday'],
                                'hint_ru': 'Когда следующая практика?',
                                'quote': '…practise again next Thursday…',
                                'model_en': 'They will practise again next Thursday.'}],
                 'plan': ['Presentation topic (Preparing for an exam)',
                          'Meeting at the park',
                          'Why they stayed',
                          'Payment and next practice'],
                 'facts': ['Mia presented about Preparing for an exam.',
                           'It was raining, so they stayed.',
                           'Mia paid five pounds for printing.',
                           'Next practice is Thursday.']},
        'move': {'full_text': 'Last week Omar prepared a short presentation about Moving house. '
                              'Examples were related to boxes, neighbours, new area, rent. Omar '
                              'made a clear plan before writing. On Tuesday Omar met Paul in the '
                              'city café. Paul wanted a museum first, but Omar preferred the quiet '
                              'café. They stayed because it was raining outside. They worked for '
                              'two hours and shared water. Omar paid four pounds for printing. '
                              'Paul saved the notes on a laptop. They agreed to practise again '
                              'next Monday and Omar put the printouts in a folder. Before leaving, '
                              'Paul locked the laptop in a bag.',
                 'gapped_text': 'Last week Omar prepared a short presentation about Moving house. '
                                'Examples were related to boxes, neighbours, new area, rent. Omar '
                                'made a clear (1)___ before writing. On Tuesday Omar met Paul in '
                                'the city café. Paul wanted a museum first, but Omar preferred the '
                                'quiet café. They stayed because it was (2)___ outside. They '
                                'worked for two hours and shared water. Omar paid four pounds for '
                                'printing. Paul saved the notes on a laptop. They agreed to '
                                'practise again next (3)___ and Omar put the printouts in a '
                                '(4)___. Before leaving, Paul locked the (5)___ in a bag.',
                 'answers': ['plan', 'raining', 'Monday', 'folder', 'laptop'],
                 'word_bank': ['plan', 'raining', 'Monday', 'folder', 'laptop', 'winter'],
                 'questions': [{'q': "What was Omar's presentation about?",
                                'accept': ['Moving house', 'moving house'],
                                'hint_ru': 'О чём презентация?',
                                'quote': '…presentation about Moving house.',
                                'model_en': 'The presentation was about Moving house.'},
                               {'q': 'Why did they stay?',
                                'accept': ['raining', 'because it was raining', 'rain'],
                                'hint_ru': 'Почему они остались?',
                                'quote': '…because it was raining outside.',
                                'model_en': 'They stayed because it was raining outside.'},
                               {'q': 'How much did Omar pay for printing?',
                                'accept': ['four pounds', 'four'],
                                'hint_ru': 'Сколько заплатили за печать?',
                                'quote': 'Omar paid four pounds for printing.',
                                'model_en': 'Omar paid four pounds for printing.'},
                               {'q': 'When will they practise again?',
                                'accept': ['next Monday', 'Monday'],
                                'hint_ru': 'Когда следующая практика?',
                                'quote': '…practise again next Monday…',
                                'model_en': 'They will practise again next Monday.'}],
                 'plan': ['Presentation topic (Moving house)',
                          'Meeting at the café',
                          'Why they stayed',
                          'Payment and next practice'],
                 'facts': ['Omar presented about Moving house.',
                           'It was raining, so they stayed.',
                           'Omar paid four pounds for printing.',
                           'Next practice is Monday.']},
        'travel_b1': {'full_text': 'Last week Tom prepared a short presentation about Travel '
                                   'story. Examples were related to flight, delay, hotel, advice. '
                                   'Tom made a clear plan before writing. On Tuesday Tom met Alex '
                                   'in the city school. Alex wanted a museum first, but Tom '
                                   'preferred the quiet school. They stayed because it was raining '
                                   'outside. They worked for two hours and shared water. Tom paid '
                                   'six pounds for printing. Alex saved the notes on a laptop. '
                                   'They agreed to practise again next Sunday and Tom put the '
                                   'printouts in a backpack. Before leaving, Alex locked the '
                                   'laptop in a bag.',
                      'gapped_text': 'Last week Tom prepared a short presentation about Travel '
                                     'story. Examples were related to flight, delay, hotel, '
                                     'advice. Tom made a clear (1)___ before writing. On Tuesday '
                                     'Tom met Alex in the city school. Alex wanted a museum first, '
                                     'but Tom preferred the quiet school. They stayed because it '
                                     'was (2)___ outside. They worked for two hours and shared '
                                     'water. Tom paid six pounds for printing. Alex saved the '
                                     'notes on a laptop. They agreed to practise again next (3)___ '
                                     'and Tom put the printouts in a (4)___. Before leaving, Alex '
                                     'locked the (5)___ in a bag.',
                      'answers': ['plan', 'raining', 'Sunday', 'backpack', 'laptop'],
                      'word_bank': ['plan', 'raining', 'Sunday', 'backpack', 'laptop', 'silent'],
                      'questions': [{'q': "What was Tom's presentation about?",
                                     'accept': ['Travel story', 'travel story'],
                                     'hint_ru': 'О чём презентация?',
                                     'quote': '…presentation about Travel story.',
                                     'model_en': 'The presentation was about Travel story.'},
                                    {'q': 'Why did they stay?',
                                     'accept': ['raining', 'because it was raining', 'rain'],
                                     'hint_ru': 'Почему они остались?',
                                     'quote': '…because it was raining outside.',
                                     'model_en': 'They stayed because it was raining outside.'},
                                    {'q': 'How much did Tom pay for printing?',
                                     'accept': ['six pounds', 'six'],
                                     'hint_ru': 'Сколько заплатили за печать?',
                                     'quote': 'Tom paid six pounds for printing.',
                                     'model_en': 'Tom paid six pounds for printing.'},
                                    {'q': 'When will they practise again?',
                                     'accept': ['next Sunday', 'Sunday'],
                                     'hint_ru': 'Когда следующая практика?',
                                     'quote': '…practise again next Sunday…',
                                     'model_en': 'They will practise again next Sunday.'}],
                      'plan': ['Presentation topic (Travel story)',
                               'Meeting at the school',
                               'Why they stayed',
                               'Payment and next practice'],
                      'facts': ['Tom presented about Travel story.',
                                'It was raining, so they stayed.',
                                'Tom paid six pounds for printing.',
                                'Next practice is Sunday.']},
        'hobby_club': {'full_text': 'Last week Tom prepared a short presentation about A hobby '
                                    'club. Examples were related to members, meeting, project, '
                                    'join. Tom made a clear plan before writing. On Tuesday Tom '
                                    'met Rita in the city café. Rita wanted a museum first, but '
                                    'Tom preferred the quiet café. They stayed because it was '
                                    'raining outside. They worked for two hours and shared water. '
                                    'Tom paid five pounds for printing. Rita saved the notes on a '
                                    'laptop. They agreed to practise again next Friday and Tom put '
                                    'the printouts in a bag. Before leaving, Rita locked the '
                                    'laptop in a bag.',
                       'gapped_text': 'Last week Tom prepared a short presentation about A hobby '
                                      'club. Examples were related to members, meeting, project, '
                                      'join. Tom made a clear (1)___ before writing. On Tuesday '
                                      'Tom met Rita in the city café. Rita wanted a museum first, '
                                      'but Tom preferred the quiet café. They stayed because it '
                                      'was (2)___ outside. They worked for two hours and shared '
                                      'water. Tom paid five pounds for printing. Rita saved the '
                                      'notes on a laptop. They agreed to practise again next '
                                      '(3)___ and Tom put the printouts in a (4)___. Before '
                                      'leaving, Rita locked the (5)___ in a bag.',
                       'answers': ['plan', 'raining', 'Friday', 'bag', 'laptop'],
                       'word_bank': ['plan', 'raining', 'Friday', 'bag', 'laptop', 'purple'],
                       'questions': [{'q': "What was Tom's presentation about?",
                                      'accept': ['A hobby club', 'a hobby club'],
                                      'hint_ru': 'О чём презентация?',
                                      'quote': '…presentation about A hobby club.',
                                      'model_en': 'The presentation was about A hobby club.'},
                                     {'q': 'Why did they stay?',
                                      'accept': ['raining', 'because it was raining', 'rain'],
                                      'hint_ru': 'Почему они остались?',
                                      'quote': '…because it was raining outside.',
                                      'model_en': 'They stayed because it was raining outside.'},
                                     {'q': 'How much did Tom pay for printing?',
                                      'accept': ['five pounds', 'five'],
                                      'hint_ru': 'Сколько заплатили за печать?',
                                      'quote': 'Tom paid five pounds for printing.',
                                      'model_en': 'Tom paid five pounds for printing.'},
                                     {'q': 'When will they practise again?',
                                      'accept': ['next Friday', 'Friday'],
                                      'hint_ru': 'Когда следующая практика?',
                                      'quote': '…practise again next Friday…',
                                      'model_en': 'They will practise again next Friday.'}],
                       'plan': ['Presentation topic (A hobby club)',
                                'Meeting at the café',
                                'Why they stayed',
                                'Payment and next practice'],
                       'facts': ['Tom presented about A hobby club.',
                                 'It was raining, so they stayed.',
                                 'Tom paid five pounds for printing.',
                                 'Next practice is Friday.']}},
 'B2': {'business': {'full_text': 'For a seminar on Business meeting, Nora drafted a brief '
                                  'analysis linked to deadline, remote work, clients, proposal. '
                                  'Nora outlined a careful plan before drafting. On Wednesday Nora '
                                  'joined Olga at a quiet coworking space. Olga suggested a noisy '
                                  'café, but Nora insisted on the coworking space. They stayed '
                                  'because the café was overcrowded and loud. After three focused '
                                  'hours they summarised the key arguments. Nora paid twelve '
                                  'pounds for day passes. Olga uploaded the shared document. They '
                                  'scheduled a follow-up next Monday and Nora filed printouts in a '
                                  'portfolio. Before leaving, Olga switched off a tablet.',
                     'gapped_text': 'For a seminar on Business meeting, Nora drafted a brief '
                                    'analysis linked to deadline, remote work, clients, proposal. '
                                    'Nora outlined a careful (1)___ before drafting. On Wednesday '
                                    'Nora joined Olga at a quiet coworking space. Olga suggested a '
                                    'noisy café, but Nora insisted on the coworking space. They '
                                    'stayed because the café was overcrowded and (2)___. After '
                                    'three focused hours they summarised the key arguments. Nora '
                                    'paid twelve pounds for day passes. Olga uploaded the shared '
                                    'document. They scheduled a follow-up next (3)___ and Nora '
                                    'filed printouts in a (4)___. Before leaving, Olga switched '
                                    'off a (5)___.',
                     'answers': ['plan', 'loud', 'Monday', 'portfolio', 'tablet'],
                     'word_bank': ['plan', 'loud', 'Monday', 'portfolio', 'tablet', 'purple'],
                     'questions': [{'q': 'What seminar topic was being prepared?',
                                    'accept': ['Business meeting', 'business meeting'],
                                    'hint_ru': 'Тема семинара?',
                                    'quote': 'For a seminar on Business meeting…',
                                    'model_en': 'The seminar was on Business meeting.'},
                                   {'q': 'Why did they stay at the coworking space?',
                                    'accept': ['loud',
                                               'overcrowded',
                                               'café was overcrowded and loud'],
                                    'hint_ru': 'Почему коворкинг?',
                                    'quote': '…overcrowded and loud.',
                                    'model_en': 'They stayed because the café was overcrowded and '
                                                'loud.'},
                                   {'q': 'How much did Nora pay?',
                                    'accept': ['twelve pounds', '12 pounds', '12'],
                                    'hint_ru': 'Сколько заплатили?',
                                    'quote': 'Nora paid twelve pounds…',
                                    'model_en': 'Nora paid twelve pounds for day passes.'},
                                   {'q': 'When is the follow-up?',
                                    'accept': ['next Monday', 'Monday'],
                                    'hint_ru': 'Когда follow-up?',
                                    'quote': '…follow-up next Monday…',
                                    'model_en': 'The follow-up is next Monday.'}],
                     'plan': ['Seminar topic (Business meeting)',
                              'Workplace choice',
                              'Work session',
                              'Payment and follow-up'],
                     'facts': ['Seminar on Business meeting; focus deadline, remote work, clients, '
                               'proposal.',
                               'Café was loud; they used coworking.',
                               'Nora paid twelve pounds.',
                               'Follow-up next Monday.']},
        'startup': {'full_text': 'For a seminar on Startup idea, Ben drafted a brief analysis '
                                 'linked to product, users, funding, pitch. Ben outlined a careful '
                                 'plan before drafting. On Wednesday Ben joined Alex at a quiet '
                                 'coworking space. Alex suggested a noisy café, but Ben insisted '
                                 'on the coworking space. They stayed because the café was '
                                 'overcrowded and loud. After three focused hours they summarised '
                                 'the key arguments. Ben paid twelve pounds for day passes. Alex '
                                 'uploaded the shared document. They scheduled a follow-up next '
                                 'Thursday and Ben filed printouts in a portfolio. Before leaving, '
                                 'Alex switched off a tablet.',
                    'gapped_text': 'For a seminar on Startup idea, Ben drafted a brief analysis '
                                   'linked to product, users, funding, pitch. Ben outlined a '
                                   'careful (1)___ before drafting. On Wednesday Ben joined Alex '
                                   'at a quiet coworking space. Alex suggested a noisy café, but '
                                   'Ben insisted on the coworking space. They stayed because the '
                                   'café was overcrowded and (2)___. After three focused hours '
                                   'they summarised the key arguments. Ben paid twelve pounds for '
                                   'day passes. Alex uploaded the shared document. They scheduled '
                                   'a follow-up next (3)___ and Ben filed printouts in a (4)___. '
                                   'Before leaving, Alex switched off a (5)___.',
                    'answers': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet'],
                    'word_bank': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet', 'heavy'],
                    'questions': [{'q': 'What seminar topic was being prepared?',
                                   'accept': ['Startup idea', 'startup idea'],
                                   'hint_ru': 'Тема семинара?',
                                   'quote': 'For a seminar on Startup idea…',
                                   'model_en': 'The seminar was on Startup idea.'},
                                  {'q': 'Why did they stay at the coworking space?',
                                   'accept': ['loud',
                                              'overcrowded',
                                              'café was overcrowded and loud'],
                                   'hint_ru': 'Почему коворкинг?',
                                   'quote': '…overcrowded and loud.',
                                   'model_en': 'They stayed because the café was overcrowded and '
                                               'loud.'},
                                  {'q': 'How much did Ben pay?',
                                   'accept': ['twelve pounds', '12 pounds', '12'],
                                   'hint_ru': 'Сколько заплатили?',
                                   'quote': 'Ben paid twelve pounds…',
                                   'model_en': 'Ben paid twelve pounds for day passes.'},
                                  {'q': 'When is the follow-up?',
                                   'accept': ['next Thursday', 'Thursday'],
                                   'hint_ru': 'Когда follow-up?',
                                   'quote': '…follow-up next Thursday…',
                                   'model_en': 'The follow-up is next Thursday.'}],
                    'plan': ['Seminar topic (Startup idea)',
                             'Workplace choice',
                             'Work session',
                             'Payment and follow-up'],
                    'facts': ['Seminar on Startup idea; focus product, users, funding, pitch.',
                              'Café was loud; they used coworking.',
                              'Ben paid twelve pounds.',
                              'Follow-up next Thursday.']},
        'remote': {'full_text': 'For a seminar on Working from home, Ben drafted a brief analysis '
                                'linked to focus, meetings, balance, office days. Ben outlined a '
                                'careful plan before drafting. On Wednesday Ben joined Alex at a '
                                'quiet coworking space. Alex suggested a noisy café, but Ben '
                                'insisted on the coworking space. They stayed because the café was '
                                'overcrowded and loud. After three focused hours they summarised '
                                'the key arguments. Ben paid twelve pounds for day passes. Alex '
                                'uploaded the shared document. They scheduled a follow-up next '
                                'Thursday and Ben filed printouts in a portfolio. Before leaving, '
                                'Alex switched off a tablet.',
                   'gapped_text': 'For a seminar on Working from home, Ben drafted a brief '
                                  'analysis linked to focus, meetings, balance, office days. Ben '
                                  'outlined a careful (1)___ before drafting. On Wednesday Ben '
                                  'joined Alex at a quiet coworking space. Alex suggested a noisy '
                                  'café, but Ben insisted on the coworking space. They stayed '
                                  'because the café was overcrowded and (2)___. After three '
                                  'focused hours they summarised the key arguments. Ben paid '
                                  'twelve pounds for day passes. Alex uploaded the shared '
                                  'document. They scheduled a follow-up next (3)___ and Ben filed '
                                  'printouts in a (4)___. Before leaving, Alex switched off a '
                                  '(5)___.',
                   'answers': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet'],
                   'word_bank': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet', 'winter'],
                   'questions': [{'q': 'What seminar topic was being prepared?',
                                  'accept': ['Working from home', 'working from home'],
                                  'hint_ru': 'Тема семинара?',
                                  'quote': 'For a seminar on Working from home…',
                                  'model_en': 'The seminar was on Working from home.'},
                                 {'q': 'Why did they stay at the coworking space?',
                                  'accept': ['loud',
                                             'overcrowded',
                                             'café was overcrowded and loud'],
                                  'hint_ru': 'Почему коворкинг?',
                                  'quote': '…overcrowded and loud.',
                                  'model_en': 'They stayed because the café was overcrowded and '
                                              'loud.'},
                                 {'q': 'How much did Ben pay?',
                                  'accept': ['twelve pounds', '12 pounds', '12'],
                                  'hint_ru': 'Сколько заплатили?',
                                  'quote': 'Ben paid twelve pounds…',
                                  'model_en': 'Ben paid twelve pounds for day passes.'},
                                 {'q': 'When is the follow-up?',
                                  'accept': ['next Thursday', 'Thursday'],
                                  'hint_ru': 'Когда follow-up?',
                                  'quote': '…follow-up next Thursday…',
                                  'model_en': 'The follow-up is next Thursday.'}],
                   'plan': ['Seminar topic (Working from home)',
                            'Workplace choice',
                            'Work session',
                            'Payment and follow-up'],
                   'facts': ['Seminar on Working from home; focus focus, meetings, balance, office '
                             'days.',
                             'Café was loud; they used coworking.',
                             'Ben paid twelve pounds.',
                             'Follow-up next Thursday.']},
        'news': {'full_text': 'For a seminar on Local news, Victor drafted a brief analysis linked '
                              'to project, opinion, impact, citizens. Victor outlined a careful '
                              'plan before drafting. On Wednesday Victor joined Chris at a quiet '
                              'coworking space. Chris suggested a noisy café, but Victor insisted '
                              'on the coworking space. They stayed because the café was '
                              'overcrowded and loud. After three focused hours they summarised the '
                              'key arguments. Victor paid twelve pounds for day passes. Chris '
                              'uploaded the shared document. They scheduled a follow-up next '
                              'Thursday and Victor filed printouts in a portfolio. Before leaving, '
                              'Chris switched off a tablet.',
                 'gapped_text': 'For a seminar on Local news, Victor drafted a brief analysis '
                                'linked to project, opinion, impact, citizens. Victor outlined a '
                                'careful (1)___ before drafting. On Wednesday Victor joined Chris '
                                'at a quiet coworking space. Chris suggested a noisy café, but '
                                'Victor insisted on the coworking space. They stayed because the '
                                'café was overcrowded and (2)___. After three focused hours they '
                                'summarised the key arguments. Victor paid twelve pounds for day '
                                'passes. Chris uploaded the shared document. They scheduled a '
                                'follow-up next (3)___ and Victor filed printouts in a (4)___. '
                                'Before leaving, Chris switched off a (5)___.',
                 'answers': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet'],
                 'word_bank': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet', 'winter'],
                 'questions': [{'q': 'What seminar topic was being prepared?',
                                'accept': ['Local news', 'local news'],
                                'hint_ru': 'Тема семинара?',
                                'quote': 'For a seminar on Local news…',
                                'model_en': 'The seminar was on Local news.'},
                               {'q': 'Why did they stay at the coworking space?',
                                'accept': ['loud', 'overcrowded', 'café was overcrowded and loud'],
                                'hint_ru': 'Почему коворкинг?',
                                'quote': '…overcrowded and loud.',
                                'model_en': 'They stayed because the café was overcrowded and '
                                            'loud.'},
                               {'q': 'How much did Victor pay?',
                                'accept': ['twelve pounds', '12 pounds', '12'],
                                'hint_ru': 'Сколько заплатили?',
                                'quote': 'Victor paid twelve pounds…',
                                'model_en': 'Victor paid twelve pounds for day passes.'},
                               {'q': 'When is the follow-up?',
                                'accept': ['next Thursday', 'Thursday'],
                                'hint_ru': 'Когда follow-up?',
                                'quote': '…follow-up next Thursday…',
                                'model_en': 'The follow-up is next Thursday.'}],
                 'plan': ['Seminar topic (Local news)',
                          'Workplace choice',
                          'Work session',
                          'Payment and follow-up'],
                 'facts': ['Seminar on Local news; focus project, opinion, impact, citizens.',
                           'Café was loud; they used coworking.',
                           'Victor paid twelve pounds.',
                           'Follow-up next Thursday.']},
        'uni': {'full_text': 'For a seminar on University life, Kate drafted a brief analysis '
                             'linked to essay, deadline, sources, feedback. Kate outlined a '
                             'careful plan before drafting. On Wednesday Kate joined Nina at a '
                             'quiet coworking space. Nina suggested a noisy café, but Kate '
                             'insisted on the coworking space. They stayed because the café was '
                             'overcrowded and loud. After three focused hours they summarised the '
                             'key arguments. Kate paid twelve pounds for day passes. Nina uploaded '
                             'the shared document. They scheduled a follow-up next Tuesday and '
                             'Kate filed printouts in a portfolio. Before leaving, Nina switched '
                             'off a tablet.',
                'gapped_text': 'For a seminar on University life, Kate drafted a brief analysis '
                               'linked to essay, deadline, sources, feedback. Kate outlined a '
                               'careful (1)___ before drafting. On Wednesday Kate joined Nina at a '
                               'quiet coworking space. Nina suggested a noisy café, but Kate '
                               'insisted on the coworking space. They stayed because the café was '
                               'overcrowded and (2)___. After three focused hours they summarised '
                               'the key arguments. Kate paid twelve pounds for day passes. Nina '
                               'uploaded the shared document. They scheduled a follow-up next '
                               '(3)___ and Kate filed printouts in a (4)___. Before leaving, Nina '
                               'switched off a (5)___.',
                'answers': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet'],
                'word_bank': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet', 'heavy'],
                'questions': [{'q': 'What seminar topic was being prepared?',
                               'accept': ['University life', 'university life'],
                               'hint_ru': 'Тема семинара?',
                               'quote': 'For a seminar on University life…',
                               'model_en': 'The seminar was on University life.'},
                              {'q': 'Why did they stay at the coworking space?',
                               'accept': ['loud', 'overcrowded', 'café was overcrowded and loud'],
                               'hint_ru': 'Почему коворкинг?',
                               'quote': '…overcrowded and loud.',
                               'model_en': 'They stayed because the café was overcrowded and '
                                           'loud.'},
                              {'q': 'How much did Kate pay?',
                               'accept': ['twelve pounds', '12 pounds', '12'],
                               'hint_ru': 'Сколько заплатили?',
                               'quote': 'Kate paid twelve pounds…',
                               'model_en': 'Kate paid twelve pounds for day passes.'},
                              {'q': 'When is the follow-up?',
                               'accept': ['next Tuesday', 'Tuesday'],
                               'hint_ru': 'Когда follow-up?',
                               'quote': '…follow-up next Tuesday…',
                               'model_en': 'The follow-up is next Tuesday.'}],
                'plan': ['Seminar topic (University life)',
                         'Workplace choice',
                         'Work session',
                         'Payment and follow-up'],
                'facts': ['Seminar on University life; focus essay, deadline, sources, feedback.',
                          'Café was loud; they used coworking.',
                          'Kate paid twelve pounds.',
                          'Follow-up next Tuesday.']},
        'customer': {'full_text': 'For a seminar on Customer support, Ben drafted a brief analysis '
                                  'linked to complaint, refund, apology, solution. Ben outlined a '
                                  'careful plan before drafting. On Wednesday Ben joined Chris at '
                                  'a quiet coworking space. Chris suggested a noisy café, but Ben '
                                  'insisted on the coworking space. They stayed because the café '
                                  'was overcrowded and loud. After three focused hours they '
                                  'summarised the key arguments. Ben paid twelve pounds for day '
                                  'passes. Chris uploaded the shared document. They scheduled a '
                                  'follow-up next Saturday and Ben filed printouts in a portfolio. '
                                  'Before leaving, Chris switched off a tablet.',
                     'gapped_text': 'For a seminar on Customer support, Ben drafted a brief '
                                    'analysis linked to complaint, refund, apology, solution. Ben '
                                    'outlined a careful (1)___ before drafting. On Wednesday Ben '
                                    'joined Chris at a quiet coworking space. Chris suggested a '
                                    'noisy café, but Ben insisted on the coworking space. They '
                                    'stayed because the café was overcrowded and (2)___. After '
                                    'three focused hours they summarised the key arguments. Ben '
                                    'paid twelve pounds for day passes. Chris uploaded the shared '
                                    'document. They scheduled a follow-up next (3)___ and Ben '
                                    'filed printouts in a (4)___. Before leaving, Chris switched '
                                    'off a (5)___.',
                     'answers': ['plan', 'loud', 'Saturday', 'portfolio', 'tablet'],
                     'word_bank': ['plan', 'loud', 'Saturday', 'portfolio', 'tablet', 'purple'],
                     'questions': [{'q': 'What seminar topic was being prepared?',
                                    'accept': ['Customer support', 'customer support'],
                                    'hint_ru': 'Тема семинара?',
                                    'quote': 'For a seminar on Customer support…',
                                    'model_en': 'The seminar was on Customer support.'},
                                   {'q': 'Why did they stay at the coworking space?',
                                    'accept': ['loud',
                                               'overcrowded',
                                               'café was overcrowded and loud'],
                                    'hint_ru': 'Почему коворкинг?',
                                    'quote': '…overcrowded and loud.',
                                    'model_en': 'They stayed because the café was overcrowded and '
                                                'loud.'},
                                   {'q': 'How much did Ben pay?',
                                    'accept': ['twelve pounds', '12 pounds', '12'],
                                    'hint_ru': 'Сколько заплатили?',
                                    'quote': 'Ben paid twelve pounds…',
                                    'model_en': 'Ben paid twelve pounds for day passes.'},
                                   {'q': 'When is the follow-up?',
                                    'accept': ['next Saturday', 'Saturday'],
                                    'hint_ru': 'Когда follow-up?',
                                    'quote': '…follow-up next Saturday…',
                                    'model_en': 'The follow-up is next Saturday.'}],
                     'plan': ['Seminar topic (Customer support)',
                              'Workplace choice',
                              'Work session',
                              'Payment and follow-up'],
                     'facts': ['Seminar on Customer support; focus complaint, refund, apology, '
                               'solution.',
                               'Café was loud; they used coworking.',
                               'Ben paid twelve pounds.',
                               'Follow-up next Saturday.']},
        'health': {'full_text': 'For a seminar on Healthy lifestyle, Lena drafted a brief analysis '
                                'linked to habits, sleep, diet, motivation. Lena outlined a '
                                'careful plan before drafting. On Wednesday Lena joined Alex at a '
                                'quiet coworking space. Alex suggested a noisy café, but Lena '
                                'insisted on the coworking space. They stayed because the café was '
                                'overcrowded and loud. After three focused hours they summarised '
                                'the key arguments. Lena paid twelve pounds for day passes. Alex '
                                'uploaded the shared document. They scheduled a follow-up next '
                                'Friday and Lena filed printouts in a portfolio. Before leaving, '
                                'Alex switched off a tablet.',
                   'gapped_text': 'For a seminar on Healthy lifestyle, Lena drafted a brief '
                                  'analysis linked to habits, sleep, diet, motivation. Lena '
                                  'outlined a careful (1)___ before drafting. On Wednesday Lena '
                                  'joined Alex at a quiet coworking space. Alex suggested a noisy '
                                  'café, but Lena insisted on the coworking space. They stayed '
                                  'because the café was overcrowded and (2)___. After three '
                                  'focused hours they summarised the key arguments. Lena paid '
                                  'twelve pounds for day passes. Alex uploaded the shared '
                                  'document. They scheduled a follow-up next (3)___ and Lena filed '
                                  'printouts in a (4)___. Before leaving, Alex switched off a '
                                  '(5)___.',
                   'answers': ['plan', 'loud', 'Friday', 'portfolio', 'tablet'],
                   'word_bank': ['plan', 'loud', 'Friday', 'portfolio', 'tablet', 'purple'],
                   'questions': [{'q': 'What seminar topic was being prepared?',
                                  'accept': ['Healthy lifestyle', 'healthy lifestyle'],
                                  'hint_ru': 'Тема семинара?',
                                  'quote': 'For a seminar on Healthy lifestyle…',
                                  'model_en': 'The seminar was on Healthy lifestyle.'},
                                 {'q': 'Why did they stay at the coworking space?',
                                  'accept': ['loud',
                                             'overcrowded',
                                             'café was overcrowded and loud'],
                                  'hint_ru': 'Почему коворкинг?',
                                  'quote': '…overcrowded and loud.',
                                  'model_en': 'They stayed because the café was overcrowded and '
                                              'loud.'},
                                 {'q': 'How much did Lena pay?',
                                  'accept': ['twelve pounds', '12 pounds', '12'],
                                  'hint_ru': 'Сколько заплатили?',
                                  'quote': 'Lena paid twelve pounds…',
                                  'model_en': 'Lena paid twelve pounds for day passes.'},
                                 {'q': 'When is the follow-up?',
                                  'accept': ['next Friday', 'Friday'],
                                  'hint_ru': 'Когда follow-up?',
                                  'quote': '…follow-up next Friday…',
                                  'model_en': 'The follow-up is next Friday.'}],
                   'plan': ['Seminar topic (Healthy lifestyle)',
                            'Workplace choice',
                            'Work session',
                            'Payment and follow-up'],
                   'facts': ['Seminar on Healthy lifestyle; focus habits, sleep, diet, motivation.',
                             'Café was loud; they used coworking.',
                             'Lena paid twelve pounds.',
                             'Follow-up next Friday.']},
        'culture': {'full_text': 'For a seminar on A cultural event, Anna drafted a brief analysis '
                                 'linked to exhibition, tickets, review, atmosphere. Anna outlined '
                                 'a careful plan before drafting. On Wednesday Anna joined Rita at '
                                 'a quiet coworking space. Rita suggested a noisy café, but Anna '
                                 'insisted on the coworking space. They stayed because the café '
                                 'was overcrowded and loud. After three focused hours they '
                                 'summarised the key arguments. Anna paid twelve pounds for day '
                                 'passes. Rita uploaded the shared document. They scheduled a '
                                 'follow-up next Saturday and Anna filed printouts in a portfolio. '
                                 'Before leaving, Rita switched off a tablet.',
                    'gapped_text': 'For a seminar on A cultural event, Anna drafted a brief '
                                   'analysis linked to exhibition, tickets, review, atmosphere. '
                                   'Anna outlined a careful (1)___ before drafting. On Wednesday '
                                   'Anna joined Rita at a quiet coworking space. Rita suggested a '
                                   'noisy café, but Anna insisted on the coworking space. They '
                                   'stayed because the café was overcrowded and (2)___. After '
                                   'three focused hours they summarised the key arguments. Anna '
                                   'paid twelve pounds for day passes. Rita uploaded the shared '
                                   'document. They scheduled a follow-up next (3)___ and Anna '
                                   'filed printouts in a (4)___. Before leaving, Rita switched off '
                                   'a (5)___.',
                    'answers': ['plan', 'loud', 'Saturday', 'portfolio', 'tablet'],
                    'word_bank': ['plan', 'loud', 'Saturday', 'portfolio', 'tablet', 'purple'],
                    'questions': [{'q': 'What seminar topic was being prepared?',
                                   'accept': ['A cultural event', 'a cultural event'],
                                   'hint_ru': 'Тема семинара?',
                                   'quote': 'For a seminar on A cultural event…',
                                   'model_en': 'The seminar was on A cultural event.'},
                                  {'q': 'Why did they stay at the coworking space?',
                                   'accept': ['loud',
                                              'overcrowded',
                                              'café was overcrowded and loud'],
                                   'hint_ru': 'Почему коворкинг?',
                                   'quote': '…overcrowded and loud.',
                                   'model_en': 'They stayed because the café was overcrowded and '
                                               'loud.'},
                                  {'q': 'How much did Anna pay?',
                                   'accept': ['twelve pounds', '12 pounds', '12'],
                                   'hint_ru': 'Сколько заплатили?',
                                   'quote': 'Anna paid twelve pounds…',
                                   'model_en': 'Anna paid twelve pounds for day passes.'},
                                  {'q': 'When is the follow-up?',
                                   'accept': ['next Saturday', 'Saturday'],
                                   'hint_ru': 'Когда follow-up?',
                                   'quote': '…follow-up next Saturday…',
                                   'model_en': 'The follow-up is next Saturday.'}],
                    'plan': ['Seminar topic (A cultural event)',
                             'Workplace choice',
                             'Work session',
                             'Payment and follow-up'],
                    'facts': ['Seminar on A cultural event; focus exhibition, tickets, review, '
                              'atmosphere.',
                              'Café was loud; they used coworking.',
                              'Anna paid twelve pounds.',
                              'Follow-up next Saturday.']}},
 'C1': {'negotiation': {'full_text': 'For a seminar on Negotiation, Dana drafted a brief analysis '
                                     'linked to terms, compromise, contract, leverage. Dana '
                                     'outlined a careful plan before drafting. On Wednesday Dana '
                                     'joined Olga at a quiet coworking space. Olga suggested a '
                                     'noisy café, but Dana insisted on the coworking space. They '
                                     'stayed because the café was overcrowded and loud. After '
                                     'three focused hours they summarised the key arguments. Dana '
                                     'paid twelve pounds for day passes. Olga uploaded the shared '
                                     'document. They scheduled a follow-up next Tuesday and Dana '
                                     'filed printouts in a portfolio. Before leaving, Olga '
                                     'switched off a tablet.',
                        'gapped_text': 'For a seminar on Negotiation, Dana drafted a brief '
                                       'analysis linked to terms, compromise, contract, leverage. '
                                       'Dana outlined a careful (1)___ before drafting. On '
                                       'Wednesday Dana joined Olga at a quiet coworking space. '
                                       'Olga suggested a noisy café, but Dana insisted on the '
                                       'coworking space. They stayed because the café was '
                                       'overcrowded and (2)___. After three focused hours they '
                                       'summarised the key arguments. Dana paid twelve pounds for '
                                       'day passes. Olga uploaded the shared document. They '
                                       'scheduled a follow-up next (3)___ and Dana filed printouts '
                                       'in a (4)___. Before leaving, Olga switched off a (5)___.',
                        'answers': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet'],
                        'word_bank': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet', 'heavy'],
                        'questions': [{'q': 'What seminar topic was being prepared?',
                                       'accept': ['Negotiation', 'negotiation'],
                                       'hint_ru': 'Тема семинара?',
                                       'quote': 'For a seminar on Negotiation…',
                                       'model_en': 'The seminar was on Negotiation.'},
                                      {'q': 'Why did they stay at the coworking space?',
                                       'accept': ['loud',
                                                  'overcrowded',
                                                  'café was overcrowded and loud'],
                                       'hint_ru': 'Почему коворкинг?',
                                       'quote': '…overcrowded and loud.',
                                       'model_en': 'They stayed because the café was overcrowded '
                                                   'and loud.'},
                                      {'q': 'How much did Dana pay?',
                                       'accept': ['twelve pounds', '12 pounds', '12'],
                                       'hint_ru': 'Сколько заплатили?',
                                       'quote': 'Dana paid twelve pounds…',
                                       'model_en': 'Dana paid twelve pounds for day passes.'},
                                      {'q': 'When is the follow-up?',
                                       'accept': ['next Tuesday', 'Tuesday'],
                                       'hint_ru': 'Когда follow-up?',
                                       'quote': '…follow-up next Tuesday…',
                                       'model_en': 'The follow-up is next Tuesday.'}],
                        'plan': ['Seminar topic (Negotiation)',
                                 'Workplace choice',
                                 'Work session',
                                 'Payment and follow-up'],
                        'facts': ['Seminar on Negotiation; focus terms, compromise, contract, '
                                  'leverage.',
                                  'Café was loud; they used coworking.',
                                  'Dana paid twelve pounds.',
                                  'Follow-up next Tuesday.']},
        'media': {'full_text': 'For a seminar on Media and attention, Kate drafted a brief '
                               'analysis linked to headline, bias, sources, audience. Kate '
                               'outlined a careful plan before drafting. On Wednesday Kate joined '
                               'Helen at a quiet coworking space. Helen suggested a noisy café, '
                               'but Kate insisted on the coworking space. They stayed because the '
                               'café was overcrowded and loud. After three focused hours they '
                               'summarised the key arguments. Kate paid twelve pounds for day '
                               'passes. Helen uploaded the shared document. They scheduled a '
                               'follow-up next Sunday and Kate filed printouts in a portfolio. '
                               'Before leaving, Helen switched off a tablet.',
                  'gapped_text': 'For a seminar on Media and attention, Kate drafted a brief '
                                 'analysis linked to headline, bias, sources, audience. Kate '
                                 'outlined a careful (1)___ before drafting. On Wednesday Kate '
                                 'joined Helen at a quiet coworking space. Helen suggested a noisy '
                                 'café, but Kate insisted on the coworking space. They stayed '
                                 'because the café was overcrowded and (2)___. After three focused '
                                 'hours they summarised the key arguments. Kate paid twelve pounds '
                                 'for day passes. Helen uploaded the shared document. They '
                                 'scheduled a follow-up next (3)___ and Kate filed printouts in a '
                                 '(4)___. Before leaving, Helen switched off a (5)___.',
                  'answers': ['plan', 'loud', 'Sunday', 'portfolio', 'tablet'],
                  'word_bank': ['plan', 'loud', 'Sunday', 'portfolio', 'tablet', 'zebra'],
                  'questions': [{'q': 'What seminar topic was being prepared?',
                                 'accept': ['Media and attention', 'media and attention'],
                                 'hint_ru': 'Тема семинара?',
                                 'quote': 'For a seminar on Media and attention…',
                                 'model_en': 'The seminar was on Media and attention.'},
                                {'q': 'Why did they stay at the coworking space?',
                                 'accept': ['loud', 'overcrowded', 'café was overcrowded and loud'],
                                 'hint_ru': 'Почему коворкинг?',
                                 'quote': '…overcrowded and loud.',
                                 'model_en': 'They stayed because the café was overcrowded and '
                                             'loud.'},
                                {'q': 'How much did Kate pay?',
                                 'accept': ['twelve pounds', '12 pounds', '12'],
                                 'hint_ru': 'Сколько заплатили?',
                                 'quote': 'Kate paid twelve pounds…',
                                 'model_en': 'Kate paid twelve pounds for day passes.'},
                                {'q': 'When is the follow-up?',
                                 'accept': ['next Sunday', 'Sunday'],
                                 'hint_ru': 'Когда follow-up?',
                                 'quote': '…follow-up next Sunday…',
                                 'model_en': 'The follow-up is next Sunday.'}],
                  'plan': ['Seminar topic (Media and attention)',
                           'Workplace choice',
                           'Work session',
                           'Payment and follow-up'],
                  'facts': ['Seminar on Media and attention; focus headline, bias, sources, '
                            'audience.',
                            'Café was loud; they used coworking.',
                            'Kate paid twelve pounds.',
                            'Follow-up next Sunday.']},
        'climate': {'full_text': 'For a seminar on Climate action locally, Anna drafted a brief '
                                 'analysis linked to policy, costs, community, trade-offs. Anna '
                                 'outlined a careful plan before drafting. On Wednesday Anna '
                                 'joined Max at a quiet coworking space. Max suggested a noisy '
                                 'café, but Anna insisted on the coworking space. They stayed '
                                 'because the café was overcrowded and loud. After three focused '
                                 'hours they summarised the key arguments. Anna paid twelve pounds '
                                 'for day passes. Max uploaded the shared document. They scheduled '
                                 'a follow-up next Tuesday and Anna filed printouts in a '
                                 'portfolio. Before leaving, Max switched off a tablet.',
                    'gapped_text': 'For a seminar on Climate action locally, Anna drafted a brief '
                                   'analysis linked to policy, costs, community, trade-offs. Anna '
                                   'outlined a careful (1)___ before drafting. On Wednesday Anna '
                                   'joined Max at a quiet coworking space. Max suggested a noisy '
                                   'café, but Anna insisted on the coworking space. They stayed '
                                   'because the café was overcrowded and (2)___. After three '
                                   'focused hours they summarised the key arguments. Anna paid '
                                   'twelve pounds for day passes. Max uploaded the shared '
                                   'document. They scheduled a follow-up next (3)___ and Anna '
                                   'filed printouts in a (4)___. Before leaving, Max switched off '
                                   'a (5)___.',
                    'answers': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet'],
                    'word_bank': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet', 'purple'],
                    'questions': [{'q': 'What seminar topic was being prepared?',
                                   'accept': ['Climate action locally', 'climate action locally'],
                                   'hint_ru': 'Тема семинара?',
                                   'quote': 'For a seminar on Climate action locally…',
                                   'model_en': 'The seminar was on Climate action locally.'},
                                  {'q': 'Why did they stay at the coworking space?',
                                   'accept': ['loud',
                                              'overcrowded',
                                              'café was overcrowded and loud'],
                                   'hint_ru': 'Почему коворкинг?',
                                   'quote': '…overcrowded and loud.',
                                   'model_en': 'They stayed because the café was overcrowded and '
                                               'loud.'},
                                  {'q': 'How much did Anna pay?',
                                   'accept': ['twelve pounds', '12 pounds', '12'],
                                   'hint_ru': 'Сколько заплатили?',
                                   'quote': 'Anna paid twelve pounds…',
                                   'model_en': 'Anna paid twelve pounds for day passes.'},
                                  {'q': 'When is the follow-up?',
                                   'accept': ['next Tuesday', 'Tuesday'],
                                   'hint_ru': 'Когда follow-up?',
                                   'quote': '…follow-up next Tuesday…',
                                   'model_en': 'The follow-up is next Tuesday.'}],
                    'plan': ['Seminar topic (Climate action locally)',
                             'Workplace choice',
                             'Work session',
                             'Payment and follow-up'],
                    'facts': ['Seminar on Climate action locally; focus policy, costs, community, '
                              'trade-offs.',
                              'Café was loud; they used coworking.',
                              'Anna paid twelve pounds.',
                              'Follow-up next Tuesday.']},
        'hr': {'full_text': 'For a seminar on HR feedback, Dana drafted a brief analysis linked to '
                            'performance, promotion, goals, soft skills. Dana outlined a careful '
                            'plan before drafting. On Wednesday Dana joined Nina at a quiet '
                            'coworking space. Nina suggested a noisy café, but Dana insisted on '
                            'the coworking space. They stayed because the café was overcrowded and '
                            'loud. After three focused hours they summarised the key arguments. '
                            'Dana paid twelve pounds for day passes. Nina uploaded the shared '
                            'document. They scheduled a follow-up next Sunday and Dana filed '
                            'printouts in a portfolio. Before leaving, Nina switched off a tablet.',
               'gapped_text': 'For a seminar on HR feedback, Dana drafted a brief analysis linked '
                              'to performance, promotion, goals, soft skills. Dana outlined a '
                              'careful (1)___ before drafting. On Wednesday Dana joined Nina at a '
                              'quiet coworking space. Nina suggested a noisy café, but Dana '
                              'insisted on the coworking space. They stayed because the café was '
                              'overcrowded and (2)___. After three focused hours they summarised '
                              'the key arguments. Dana paid twelve pounds for day passes. Nina '
                              'uploaded the shared document. They scheduled a follow-up next '
                              '(3)___ and Dana filed printouts in a (4)___. Before leaving, Nina '
                              'switched off a (5)___.',
               'answers': ['plan', 'loud', 'Sunday', 'portfolio', 'tablet'],
               'word_bank': ['plan', 'loud', 'Sunday', 'portfolio', 'tablet', 'silent'],
               'questions': [{'q': 'What seminar topic was being prepared?',
                              'accept': ['HR feedback', 'hr feedback'],
                              'hint_ru': 'Тема семинара?',
                              'quote': 'For a seminar on HR feedback…',
                              'model_en': 'The seminar was on HR feedback.'},
                             {'q': 'Why did they stay at the coworking space?',
                              'accept': ['loud', 'overcrowded', 'café was overcrowded and loud'],
                              'hint_ru': 'Почему коворкинг?',
                              'quote': '…overcrowded and loud.',
                              'model_en': 'They stayed because the café was overcrowded and loud.'},
                             {'q': 'How much did Dana pay?',
                              'accept': ['twelve pounds', '12 pounds', '12'],
                              'hint_ru': 'Сколько заплатили?',
                              'quote': 'Dana paid twelve pounds…',
                              'model_en': 'Dana paid twelve pounds for day passes.'},
                             {'q': 'When is the follow-up?',
                              'accept': ['next Sunday', 'Sunday'],
                              'hint_ru': 'Когда follow-up?',
                              'quote': '…follow-up next Sunday…',
                              'model_en': 'The follow-up is next Sunday.'}],
               'plan': ['Seminar topic (HR feedback)',
                        'Workplace choice',
                        'Work session',
                        'Payment and follow-up'],
               'facts': ['Seminar on HR feedback; focus performance, promotion, goals, soft '
                         'skills.',
                         'Café was loud; they used coworking.',
                         'Dana paid twelve pounds.',
                         'Follow-up next Sunday.']},
        'research': {'full_text': 'For a seminar on A research summary, Omar drafted a brief '
                                  'analysis linked to method, findings, limits, next steps. Omar '
                                  'outlined a careful plan before drafting. On Wednesday Omar '
                                  'joined Eva at a quiet coworking space. Eva suggested a noisy '
                                  'café, but Omar insisted on the coworking space. They stayed '
                                  'because the café was overcrowded and loud. After three focused '
                                  'hours they summarised the key arguments. Omar paid twelve '
                                  'pounds for day passes. Eva uploaded the shared document. They '
                                  'scheduled a follow-up next Tuesday and Omar filed printouts in '
                                  'a portfolio. Before leaving, Eva switched off a tablet.',
                     'gapped_text': 'For a seminar on A research summary, Omar drafted a brief '
                                    'analysis linked to method, findings, limits, next steps. Omar '
                                    'outlined a careful (1)___ before drafting. On Wednesday Omar '
                                    'joined Eva at a quiet coworking space. Eva suggested a noisy '
                                    'café, but Omar insisted on the coworking space. They stayed '
                                    'because the café was overcrowded and (2)___. After three '
                                    'focused hours they summarised the key arguments. Omar paid '
                                    'twelve pounds for day passes. Eva uploaded the shared '
                                    'document. They scheduled a follow-up next (3)___ and Omar '
                                    'filed printouts in a (4)___. Before leaving, Eva switched off '
                                    'a (5)___.',
                     'answers': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet'],
                     'word_bank': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet', 'purple'],
                     'questions': [{'q': 'What seminar topic was being prepared?',
                                    'accept': ['A research summary', 'a research summary'],
                                    'hint_ru': 'Тема семинара?',
                                    'quote': 'For a seminar on A research summary…',
                                    'model_en': 'The seminar was on A research summary.'},
                                   {'q': 'Why did they stay at the coworking space?',
                                    'accept': ['loud',
                                               'overcrowded',
                                               'café was overcrowded and loud'],
                                    'hint_ru': 'Почему коворкинг?',
                                    'quote': '…overcrowded and loud.',
                                    'model_en': 'They stayed because the café was overcrowded and '
                                                'loud.'},
                                   {'q': 'How much did Omar pay?',
                                    'accept': ['twelve pounds', '12 pounds', '12'],
                                    'hint_ru': 'Сколько заплатили?',
                                    'quote': 'Omar paid twelve pounds…',
                                    'model_en': 'Omar paid twelve pounds for day passes.'},
                                   {'q': 'When is the follow-up?',
                                    'accept': ['next Tuesday', 'Tuesday'],
                                    'hint_ru': 'Когда follow-up?',
                                    'quote': '…follow-up next Tuesday…',
                                    'model_en': 'The follow-up is next Tuesday.'}],
                     'plan': ['Seminar topic (A research summary)',
                              'Workplace choice',
                              'Work session',
                              'Payment and follow-up'],
                     'facts': ['Seminar on A research summary; focus method, findings, limits, '
                               'next steps.',
                               'Café was loud; they used coworking.',
                               'Omar paid twelve pounds.',
                               'Follow-up next Tuesday.']},
        'ethics': {'full_text': 'For a seminar on Tech ethics, Anna drafted a brief analysis '
                                'linked to privacy, AI, regulation, users. Anna outlined a careful '
                                'plan before drafting. On Wednesday Anna joined Nick at a quiet '
                                'coworking space. Nick suggested a noisy café, but Anna insisted '
                                'on the coworking space. They stayed because the café was '
                                'overcrowded and loud. After three focused hours they summarised '
                                'the key arguments. Anna paid twelve pounds for day passes. Nick '
                                'uploaded the shared document. They scheduled a follow-up next '
                                'Thursday and Anna filed printouts in a portfolio. Before leaving, '
                                'Nick switched off a tablet.',
                   'gapped_text': 'For a seminar on Tech ethics, Anna drafted a brief analysis '
                                  'linked to privacy, AI, regulation, users. Anna outlined a '
                                  'careful (1)___ before drafting. On Wednesday Anna joined Nick '
                                  'at a quiet coworking space. Nick suggested a noisy café, but '
                                  'Anna insisted on the coworking space. They stayed because the '
                                  'café was overcrowded and (2)___. After three focused hours they '
                                  'summarised the key arguments. Anna paid twelve pounds for day '
                                  'passes. Nick uploaded the shared document. They scheduled a '
                                  'follow-up next (3)___ and Anna filed printouts in a (4)___. '
                                  'Before leaving, Nick switched off a (5)___.',
                   'answers': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet'],
                   'word_bank': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet', 'zebra'],
                   'questions': [{'q': 'What seminar topic was being prepared?',
                                  'accept': ['Tech ethics', 'tech ethics'],
                                  'hint_ru': 'Тема семинара?',
                                  'quote': 'For a seminar on Tech ethics…',
                                  'model_en': 'The seminar was on Tech ethics.'},
                                 {'q': 'Why did they stay at the coworking space?',
                                  'accept': ['loud',
                                             'overcrowded',
                                             'café was overcrowded and loud'],
                                  'hint_ru': 'Почему коворкинг?',
                                  'quote': '…overcrowded and loud.',
                                  'model_en': 'They stayed because the café was overcrowded and '
                                              'loud.'},
                                 {'q': 'How much did Anna pay?',
                                  'accept': ['twelve pounds', '12 pounds', '12'],
                                  'hint_ru': 'Сколько заплатили?',
                                  'quote': 'Anna paid twelve pounds…',
                                  'model_en': 'Anna paid twelve pounds for day passes.'},
                                 {'q': 'When is the follow-up?',
                                  'accept': ['next Thursday', 'Thursday'],
                                  'hint_ru': 'Когда follow-up?',
                                  'quote': '…follow-up next Thursday…',
                                  'model_en': 'The follow-up is next Thursday.'}],
                   'plan': ['Seminar topic (Tech ethics)',
                            'Workplace choice',
                            'Work session',
                            'Payment and follow-up'],
                   'facts': ['Seminar on Tech ethics; focus privacy, AI, regulation, users.',
                             'Café was loud; they used coworking.',
                             'Anna paid twelve pounds.',
                             'Follow-up next Thursday.']},
        'city_plan': {'full_text': 'For a seminar on City planning, Leo drafted a brief analysis '
                                   'linked to transport, housing, debate, budget. Leo outlined a '
                                   'careful plan before drafting. On Wednesday Leo joined Helen at '
                                   'a quiet coworking space. Helen suggested a noisy café, but Leo '
                                   'insisted on the coworking space. They stayed because the café '
                                   'was overcrowded and loud. After three focused hours they '
                                   'summarised the key arguments. Leo paid twelve pounds for day '
                                   'passes. Helen uploaded the shared document. They scheduled a '
                                   'follow-up next Tuesday and Leo filed printouts in a portfolio. '
                                   'Before leaving, Helen switched off a tablet.',
                      'gapped_text': 'For a seminar on City planning, Leo drafted a brief analysis '
                                     'linked to transport, housing, debate, budget. Leo outlined a '
                                     'careful (1)___ before drafting. On Wednesday Leo joined '
                                     'Helen at a quiet coworking space. Helen suggested a noisy '
                                     'café, but Leo insisted on the coworking space. They stayed '
                                     'because the café was overcrowded and (2)___. After three '
                                     'focused hours they summarised the key arguments. Leo paid '
                                     'twelve pounds for day passes. Helen uploaded the shared '
                                     'document. They scheduled a follow-up next (3)___ and Leo '
                                     'filed printouts in a (4)___. Before leaving, Helen switched '
                                     'off a (5)___.',
                      'answers': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet'],
                      'word_bank': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet', 'purple'],
                      'questions': [{'q': 'What seminar topic was being prepared?',
                                     'accept': ['City planning', 'city planning'],
                                     'hint_ru': 'Тема семинара?',
                                     'quote': 'For a seminar on City planning…',
                                     'model_en': 'The seminar was on City planning.'},
                                    {'q': 'Why did they stay at the coworking space?',
                                     'accept': ['loud',
                                                'overcrowded',
                                                'café was overcrowded and loud'],
                                     'hint_ru': 'Почему коворкинг?',
                                     'quote': '…overcrowded and loud.',
                                     'model_en': 'They stayed because the café was overcrowded and '
                                                 'loud.'},
                                    {'q': 'How much did Leo pay?',
                                     'accept': ['twelve pounds', '12 pounds', '12'],
                                     'hint_ru': 'Сколько заплатили?',
                                     'quote': 'Leo paid twelve pounds…',
                                     'model_en': 'Leo paid twelve pounds for day passes.'},
                                    {'q': 'When is the follow-up?',
                                     'accept': ['next Tuesday', 'Tuesday'],
                                     'hint_ru': 'Когда follow-up?',
                                     'quote': '…follow-up next Tuesday…',
                                     'model_en': 'The follow-up is next Tuesday.'}],
                      'plan': ['Seminar topic (City planning)',
                               'Workplace choice',
                               'Work session',
                               'Payment and follow-up'],
                      'facts': ['Seminar on City planning; focus transport, housing, debate, '
                                'budget.',
                                'Café was loud; they used coworking.',
                                'Leo paid twelve pounds.',
                                'Follow-up next Tuesday.']},
        'leadership': {'full_text': 'For a seminar on Leadership challenge, Omar drafted a brief '
                                    'analysis linked to team, conflict, decision, outcome. Omar '
                                    'outlined a careful plan before drafting. On Wednesday Omar '
                                    'joined Chris at a quiet coworking space. Chris suggested a '
                                    'noisy café, but Omar insisted on the coworking space. They '
                                    'stayed because the café was overcrowded and loud. After three '
                                    'focused hours they summarised the key arguments. Omar paid '
                                    'twelve pounds for day passes. Chris uploaded the shared '
                                    'document. They scheduled a follow-up next Monday and Omar '
                                    'filed printouts in a portfolio. Before leaving, Chris '
                                    'switched off a tablet.',
                       'gapped_text': 'For a seminar on Leadership challenge, Omar drafted a brief '
                                      'analysis linked to team, conflict, decision, outcome. Omar '
                                      'outlined a careful (1)___ before drafting. On Wednesday '
                                      'Omar joined Chris at a quiet coworking space. Chris '
                                      'suggested a noisy café, but Omar insisted on the coworking '
                                      'space. They stayed because the café was overcrowded and '
                                      '(2)___. After three focused hours they summarised the key '
                                      'arguments. Omar paid twelve pounds for day passes. Chris '
                                      'uploaded the shared document. They scheduled a follow-up '
                                      'next (3)___ and Omar filed printouts in a (4)___. Before '
                                      'leaving, Chris switched off a (5)___.',
                       'answers': ['plan', 'loud', 'Monday', 'portfolio', 'tablet'],
                       'word_bank': ['plan', 'loud', 'Monday', 'portfolio', 'tablet', 'zebra'],
                       'questions': [{'q': 'What seminar topic was being prepared?',
                                      'accept': ['Leadership challenge', 'leadership challenge'],
                                      'hint_ru': 'Тема семинара?',
                                      'quote': 'For a seminar on Leadership challenge…',
                                      'model_en': 'The seminar was on Leadership challenge.'},
                                     {'q': 'Why did they stay at the coworking space?',
                                      'accept': ['loud',
                                                 'overcrowded',
                                                 'café was overcrowded and loud'],
                                      'hint_ru': 'Почему коворкинг?',
                                      'quote': '…overcrowded and loud.',
                                      'model_en': 'They stayed because the café was overcrowded '
                                                  'and loud.'},
                                     {'q': 'How much did Omar pay?',
                                      'accept': ['twelve pounds', '12 pounds', '12'],
                                      'hint_ru': 'Сколько заплатили?',
                                      'quote': 'Omar paid twelve pounds…',
                                      'model_en': 'Omar paid twelve pounds for day passes.'},
                                     {'q': 'When is the follow-up?',
                                      'accept': ['next Monday', 'Monday'],
                                      'hint_ru': 'Когда follow-up?',
                                      'quote': '…follow-up next Monday…',
                                      'model_en': 'The follow-up is next Monday.'}],
                       'plan': ['Seminar topic (Leadership challenge)',
                                'Workplace choice',
                                'Work session',
                                'Payment and follow-up'],
                       'facts': ['Seminar on Leadership challenge; focus team, conflict, decision, '
                                 'outcome.',
                                 'Café was loud; they used coworking.',
                                 'Omar paid twelve pounds.',
                                 'Follow-up next Monday.']}},
 'C2': {'board': {'full_text': 'For a seminar on Boardroom debate, Lena drafted a brief analysis '
                               'linked to risk, strategy, PR, long-term value. Lena outlined a '
                               'careful plan before drafting. On Wednesday Lena joined Rita at a '
                               'quiet coworking space. Rita suggested a noisy café, but Lena '
                               'insisted on the coworking space. They stayed because the café was '
                               'overcrowded and loud. After three focused hours they summarised '
                               'the key arguments. Lena paid twelve pounds for day passes. Rita '
                               'uploaded the shared document. They scheduled a follow-up next '
                               'Wednesday and Lena filed printouts in a portfolio. Before leaving, '
                               'Rita switched off a tablet.',
                  'gapped_text': 'For a seminar on Boardroom debate, Lena drafted a brief analysis '
                                 'linked to risk, strategy, PR, long-term value. Lena outlined a '
                                 'careful (1)___ before drafting. On Wednesday Lena joined Rita at '
                                 'a quiet coworking space. Rita suggested a noisy café, but Lena '
                                 'insisted on the coworking space. They stayed because the café '
                                 'was overcrowded and (2)___. After three focused hours they '
                                 'summarised the key arguments. Lena paid twelve pounds for day '
                                 'passes. Rita uploaded the shared document. They scheduled a '
                                 'follow-up next (3)___ and Lena filed printouts in a (4)___. '
                                 'Before leaving, Rita switched off a (5)___.',
                  'answers': ['plan', 'loud', 'Wednesday', 'portfolio', 'tablet'],
                  'word_bank': ['plan', 'loud', 'Wednesday', 'portfolio', 'tablet', 'winter'],
                  'questions': [{'q': 'What seminar topic was being prepared?',
                                 'accept': ['Boardroom debate', 'boardroom debate'],
                                 'hint_ru': 'Тема семинара?',
                                 'quote': 'For a seminar on Boardroom debate…',
                                 'model_en': 'The seminar was on Boardroom debate.'},
                                {'q': 'Why did they stay at the coworking space?',
                                 'accept': ['loud', 'overcrowded', 'café was overcrowded and loud'],
                                 'hint_ru': 'Почему коворкинг?',
                                 'quote': '…overcrowded and loud.',
                                 'model_en': 'They stayed because the café was overcrowded and '
                                             'loud.'},
                                {'q': 'How much did Lena pay?',
                                 'accept': ['twelve pounds', '12 pounds', '12'],
                                 'hint_ru': 'Сколько заплатили?',
                                 'quote': 'Lena paid twelve pounds…',
                                 'model_en': 'Lena paid twelve pounds for day passes.'},
                                {'q': 'When is the follow-up?',
                                 'accept': ['next Wednesday', 'Wednesday'],
                                 'hint_ru': 'Когда follow-up?',
                                 'quote': '…follow-up next Wednesday…',
                                 'model_en': 'The follow-up is next Wednesday.'}],
                  'plan': ['Seminar topic (Boardroom debate)',
                           'Workplace choice',
                           'Work session',
                           'Payment and follow-up'],
                  'facts': ['Seminar on Boardroom debate; focus risk, strategy, PR, long-term '
                            'value.',
                            'Café was loud; they used coworking.',
                            'Lena paid twelve pounds.',
                            'Follow-up next Wednesday.']},
        'policy': {'full_text': 'For a seminar on Public policy brief, Mia drafted a brief '
                                'analysis linked to stakeholders, incentives, unintended effects. '
                                'Mia outlined a careful plan before drafting. On Wednesday Mia '
                                'joined Sam at a quiet coworking space. Sam suggested a noisy '
                                'café, but Mia insisted on the coworking space. They stayed '
                                'because the café was overcrowded and loud. After three focused '
                                'hours they summarised the key arguments. Mia paid twelve pounds '
                                'for day passes. Sam uploaded the shared document. They scheduled '
                                'a follow-up next Thursday and Mia filed printouts in a portfolio. '
                                'Before leaving, Sam switched off a tablet.',
                   'gapped_text': 'For a seminar on Public policy brief, Mia drafted a brief '
                                  'analysis linked to stakeholders, incentives, unintended '
                                  'effects. Mia outlined a careful (1)___ before drafting. On '
                                  'Wednesday Mia joined Sam at a quiet coworking space. Sam '
                                  'suggested a noisy café, but Mia insisted on the coworking '
                                  'space. They stayed because the café was overcrowded and (2)___. '
                                  'After three focused hours they summarised the key arguments. '
                                  'Mia paid twelve pounds for day passes. Sam uploaded the shared '
                                  'document. They scheduled a follow-up next (3)___ and Mia filed '
                                  'printouts in a (4)___. Before leaving, Sam switched off a '
                                  '(5)___.',
                   'answers': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet'],
                   'word_bank': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet', 'silent'],
                   'questions': [{'q': 'What seminar topic was being prepared?',
                                  'accept': ['Public policy brief', 'public policy brief'],
                                  'hint_ru': 'Тема семинара?',
                                  'quote': 'For a seminar on Public policy brief…',
                                  'model_en': 'The seminar was on Public policy brief.'},
                                 {'q': 'Why did they stay at the coworking space?',
                                  'accept': ['loud',
                                             'overcrowded',
                                             'café was overcrowded and loud'],
                                  'hint_ru': 'Почему коворкинг?',
                                  'quote': '…overcrowded and loud.',
                                  'model_en': 'They stayed because the café was overcrowded and '
                                              'loud.'},
                                 {'q': 'How much did Mia pay?',
                                  'accept': ['twelve pounds', '12 pounds', '12'],
                                  'hint_ru': 'Сколько заплатили?',
                                  'quote': 'Mia paid twelve pounds…',
                                  'model_en': 'Mia paid twelve pounds for day passes.'},
                                 {'q': 'When is the follow-up?',
                                  'accept': ['next Thursday', 'Thursday'],
                                  'hint_ru': 'Когда follow-up?',
                                  'quote': '…follow-up next Thursday…',
                                  'model_en': 'The follow-up is next Thursday.'}],
                   'plan': ['Seminar topic (Public policy brief)',
                            'Workplace choice',
                            'Work session',
                            'Payment and follow-up'],
                   'facts': ['Seminar on Public policy brief; focus stakeholders, incentives, '
                             'unintended effects.',
                             'Café was loud; they used coworking.',
                             'Mia paid twelve pounds.',
                             'Follow-up next Thursday.']},
        'lit': {'full_text': 'For a seminar on A short literary review, Anna drafted a brief '
                             'analysis linked to theme, tone, symbolism, critique. Anna outlined a '
                             'careful plan before drafting. On Wednesday Anna joined Ivan at a '
                             'quiet coworking space. Ivan suggested a noisy café, but Anna '
                             'insisted on the coworking space. They stayed because the café was '
                             'overcrowded and loud. After three focused hours they summarised the '
                             'key arguments. Anna paid twelve pounds for day passes. Ivan uploaded '
                             'the shared document. They scheduled a follow-up next Sunday and Anna '
                             'filed printouts in a portfolio. Before leaving, Ivan switched off a '
                             'tablet.',
                'gapped_text': 'For a seminar on A short literary review, Anna drafted a brief '
                               'analysis linked to theme, tone, symbolism, critique. Anna outlined '
                               'a careful (1)___ before drafting. On Wednesday Anna joined Ivan at '
                               'a quiet coworking space. Ivan suggested a noisy café, but Anna '
                               'insisted on the coworking space. They stayed because the café was '
                               'overcrowded and (2)___. After three focused hours they summarised '
                               'the key arguments. Anna paid twelve pounds for day passes. Ivan '
                               'uploaded the shared document. They scheduled a follow-up next '
                               '(3)___ and Anna filed printouts in a (4)___. Before leaving, Ivan '
                               'switched off a (5)___.',
                'answers': ['plan', 'loud', 'Sunday', 'portfolio', 'tablet'],
                'word_bank': ['plan', 'loud', 'Sunday', 'portfolio', 'tablet', 'purple'],
                'questions': [{'q': 'What seminar topic was being prepared?',
                               'accept': ['A short literary review', 'a short literary review'],
                               'hint_ru': 'Тема семинара?',
                               'quote': 'For a seminar on A short literary review…',
                               'model_en': 'The seminar was on A short literary review.'},
                              {'q': 'Why did they stay at the coworking space?',
                               'accept': ['loud', 'overcrowded', 'café was overcrowded and loud'],
                               'hint_ru': 'Почему коворкинг?',
                               'quote': '…overcrowded and loud.',
                               'model_en': 'They stayed because the café was overcrowded and '
                                           'loud.'},
                              {'q': 'How much did Anna pay?',
                               'accept': ['twelve pounds', '12 pounds', '12'],
                               'hint_ru': 'Сколько заплатили?',
                               'quote': 'Anna paid twelve pounds…',
                               'model_en': 'Anna paid twelve pounds for day passes.'},
                              {'q': 'When is the follow-up?',
                               'accept': ['next Sunday', 'Sunday'],
                               'hint_ru': 'Когда follow-up?',
                               'quote': '…follow-up next Sunday…',
                               'model_en': 'The follow-up is next Sunday.'}],
                'plan': ['Seminar topic (A short literary review)',
                         'Workplace choice',
                         'Work session',
                         'Payment and follow-up'],
                'facts': ['Seminar on A short literary review; focus theme, tone, symbolism, '
                          'critique.',
                          'Café was loud; they used coworking.',
                          'Anna paid twelve pounds.',
                          'Follow-up next Sunday.']},
        'finance': {'full_text': 'For a seminar on Market commentary, Leo drafted a brief analysis '
                                 'linked to volatility, rates, outlook, caution. Leo outlined a '
                                 'careful plan before drafting. On Wednesday Leo joined Max at a '
                                 'quiet coworking space. Max suggested a noisy café, but Leo '
                                 'insisted on the coworking space. They stayed because the café '
                                 'was overcrowded and loud. After three focused hours they '
                                 'summarised the key arguments. Leo paid twelve pounds for day '
                                 'passes. Max uploaded the shared document. They scheduled a '
                                 'follow-up next Monday and Leo filed printouts in a portfolio. '
                                 'Before leaving, Max switched off a tablet.',
                    'gapped_text': 'For a seminar on Market commentary, Leo drafted a brief '
                                   'analysis linked to volatility, rates, outlook, caution. Leo '
                                   'outlined a careful (1)___ before drafting. On Wednesday Leo '
                                   'joined Max at a quiet coworking space. Max suggested a noisy '
                                   'café, but Leo insisted on the coworking space. They stayed '
                                   'because the café was overcrowded and (2)___. After three '
                                   'focused hours they summarised the key arguments. Leo paid '
                                   'twelve pounds for day passes. Max uploaded the shared '
                                   'document. They scheduled a follow-up next (3)___ and Leo filed '
                                   'printouts in a (4)___. Before leaving, Max switched off a '
                                   '(5)___.',
                    'answers': ['plan', 'loud', 'Monday', 'portfolio', 'tablet'],
                    'word_bank': ['plan', 'loud', 'Monday', 'portfolio', 'tablet', 'zebra'],
                    'questions': [{'q': 'What seminar topic was being prepared?',
                                   'accept': ['Market commentary', 'market commentary'],
                                   'hint_ru': 'Тема семинара?',
                                   'quote': 'For a seminar on Market commentary…',
                                   'model_en': 'The seminar was on Market commentary.'},
                                  {'q': 'Why did they stay at the coworking space?',
                                   'accept': ['loud',
                                              'overcrowded',
                                              'café was overcrowded and loud'],
                                   'hint_ru': 'Почему коворкинг?',
                                   'quote': '…overcrowded and loud.',
                                   'model_en': 'They stayed because the café was overcrowded and '
                                               'loud.'},
                                  {'q': 'How much did Leo pay?',
                                   'accept': ['twelve pounds', '12 pounds', '12'],
                                   'hint_ru': 'Сколько заплатили?',
                                   'quote': 'Leo paid twelve pounds…',
                                   'model_en': 'Leo paid twelve pounds for day passes.'},
                                  {'q': 'When is the follow-up?',
                                   'accept': ['next Monday', 'Monday'],
                                   'hint_ru': 'Когда follow-up?',
                                   'quote': '…follow-up next Monday…',
                                   'model_en': 'The follow-up is next Monday.'}],
                    'plan': ['Seminar topic (Market commentary)',
                             'Workplace choice',
                             'Work session',
                             'Payment and follow-up'],
                    'facts': ['Seminar on Market commentary; focus volatility, rates, outlook, '
                              'caution.',
                              'Café was loud; they used coworking.',
                              'Leo paid twelve pounds.',
                              'Follow-up next Monday.']},
        'diplomacy': {'full_text': 'For a seminar on Diplomatic note, Nora drafted a brief '
                                   'analysis linked to talks, wording, interests, compromise. Nora '
                                   'outlined a careful plan before drafting. On Wednesday Nora '
                                   'joined Paul at a quiet coworking space. Paul suggested a noisy '
                                   'café, but Nora insisted on the coworking space. They stayed '
                                   'because the café was overcrowded and loud. After three focused '
                                   'hours they summarised the key arguments. Nora paid twelve '
                                   'pounds for day passes. Paul uploaded the shared document. They '
                                   'scheduled a follow-up next Thursday and Nora filed printouts '
                                   'in a portfolio. Before leaving, Paul switched off a tablet.',
                      'gapped_text': 'For a seminar on Diplomatic note, Nora drafted a brief '
                                     'analysis linked to talks, wording, interests, compromise. '
                                     'Nora outlined a careful (1)___ before drafting. On Wednesday '
                                     'Nora joined Paul at a quiet coworking space. Paul suggested '
                                     'a noisy café, but Nora insisted on the coworking space. They '
                                     'stayed because the café was overcrowded and (2)___. After '
                                     'three focused hours they summarised the key arguments. Nora '
                                     'paid twelve pounds for day passes. Paul uploaded the shared '
                                     'document. They scheduled a follow-up next (3)___ and Nora '
                                     'filed printouts in a (4)___. Before leaving, Paul switched '
                                     'off a (5)___.',
                      'answers': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet'],
                      'word_bank': ['plan', 'loud', 'Thursday', 'portfolio', 'tablet', 'heavy'],
                      'questions': [{'q': 'What seminar topic was being prepared?',
                                     'accept': ['Diplomatic note', 'diplomatic note'],
                                     'hint_ru': 'Тема семинара?',
                                     'quote': 'For a seminar on Diplomatic note…',
                                     'model_en': 'The seminar was on Diplomatic note.'},
                                    {'q': 'Why did they stay at the coworking space?',
                                     'accept': ['loud',
                                                'overcrowded',
                                                'café was overcrowded and loud'],
                                     'hint_ru': 'Почему коворкинг?',
                                     'quote': '…overcrowded and loud.',
                                     'model_en': 'They stayed because the café was overcrowded and '
                                                 'loud.'},
                                    {'q': 'How much did Nora pay?',
                                     'accept': ['twelve pounds', '12 pounds', '12'],
                                     'hint_ru': 'Сколько заплатили?',
                                     'quote': 'Nora paid twelve pounds…',
                                     'model_en': 'Nora paid twelve pounds for day passes.'},
                                    {'q': 'When is the follow-up?',
                                     'accept': ['next Thursday', 'Thursday'],
                                     'hint_ru': 'Когда follow-up?',
                                     'quote': '…follow-up next Thursday…',
                                     'model_en': 'The follow-up is next Thursday.'}],
                      'plan': ['Seminar topic (Diplomatic note)',
                               'Workplace choice',
                               'Work session',
                               'Payment and follow-up'],
                      'facts': ['Seminar on Diplomatic note; focus talks, wording, interests, '
                                'compromise.',
                                'Café was loud; they used coworking.',
                                'Nora paid twelve pounds.',
                                'Follow-up next Thursday.']},
        'science': {'full_text': 'For a seminar on Science communication, Kate drafted a brief '
                                 'analysis linked to evidence, uncertainty, public trust. Kate '
                                 'outlined a careful plan before drafting. On Wednesday Kate '
                                 'joined Nina at a quiet coworking space. Nina suggested a noisy '
                                 'café, but Kate insisted on the coworking space. They stayed '
                                 'because the café was overcrowded and loud. After three focused '
                                 'hours they summarised the key arguments. Kate paid twelve pounds '
                                 'for day passes. Nina uploaded the shared document. They '
                                 'scheduled a follow-up next Tuesday and Kate filed printouts in a '
                                 'portfolio. Before leaving, Nina switched off a tablet.',
                    'gapped_text': 'For a seminar on Science communication, Kate drafted a brief '
                                   'analysis linked to evidence, uncertainty, public trust. Kate '
                                   'outlined a careful (1)___ before drafting. On Wednesday Kate '
                                   'joined Nina at a quiet coworking space. Nina suggested a noisy '
                                   'café, but Kate insisted on the coworking space. They stayed '
                                   'because the café was overcrowded and (2)___. After three '
                                   'focused hours they summarised the key arguments. Kate paid '
                                   'twelve pounds for day passes. Nina uploaded the shared '
                                   'document. They scheduled a follow-up next (3)___ and Kate '
                                   'filed printouts in a (4)___. Before leaving, Nina switched off '
                                   'a (5)___.',
                    'answers': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet'],
                    'word_bank': ['plan', 'loud', 'Tuesday', 'portfolio', 'tablet', 'zebra'],
                    'questions': [{'q': 'What seminar topic was being prepared?',
                                   'accept': ['Science communication', 'science communication'],
                                   'hint_ru': 'Тема семинара?',
                                   'quote': 'For a seminar on Science communication…',
                                   'model_en': 'The seminar was on Science communication.'},
                                  {'q': 'Why did they stay at the coworking space?',
                                   'accept': ['loud',
                                              'overcrowded',
                                              'café was overcrowded and loud'],
                                   'hint_ru': 'Почему коворкинг?',
                                   'quote': '…overcrowded and loud.',
                                   'model_en': 'They stayed because the café was overcrowded and '
                                               'loud.'},
                                  {'q': 'How much did Kate pay?',
                                   'accept': ['twelve pounds', '12 pounds', '12'],
                                   'hint_ru': 'Сколько заплатили?',
                                   'quote': 'Kate paid twelve pounds…',
                                   'model_en': 'Kate paid twelve pounds for day passes.'},
                                  {'q': 'When is the follow-up?',
                                   'accept': ['next Tuesday', 'Tuesday'],
                                   'hint_ru': 'Когда follow-up?',
                                   'quote': '…follow-up next Tuesday…',
                                   'model_en': 'The follow-up is next Tuesday.'}],
                    'plan': ['Seminar topic (Science communication)',
                             'Workplace choice',
                             'Work session',
                             'Payment and follow-up'],
                    'facts': ['Seminar on Science communication; focus evidence, uncertainty, '
                              'public trust.',
                              'Café was loud; they used coworking.',
                              'Kate paid twelve pounds.',
                              'Follow-up next Tuesday.']},
        'art': {'full_text': 'For a seminar on Contemporary art essay, Sara drafted a brief '
                             'analysis linked to interpretation, context, controversy. Sara '
                             'outlined a careful plan before drafting. On Wednesday Sara joined '
                             'Eva at a quiet coworking space. Eva suggested a noisy café, but Sara '
                             'insisted on the coworking space. They stayed because the café was '
                             'overcrowded and loud. After three focused hours they summarised the '
                             'key arguments. Sara paid twelve pounds for day passes. Eva uploaded '
                             'the shared document. They scheduled a follow-up next Saturday and '
                             'Sara filed printouts in a portfolio. Before leaving, Eva switched '
                             'off a tablet.',
                'gapped_text': 'For a seminar on Contemporary art essay, Sara drafted a brief '
                               'analysis linked to interpretation, context, controversy. Sara '
                               'outlined a careful (1)___ before drafting. On Wednesday Sara '
                               'joined Eva at a quiet coworking space. Eva suggested a noisy café, '
                               'but Sara insisted on the coworking space. They stayed because the '
                               'café was overcrowded and (2)___. After three focused hours they '
                               'summarised the key arguments. Sara paid twelve pounds for day '
                               'passes. Eva uploaded the shared document. They scheduled a '
                               'follow-up next (3)___ and Sara filed printouts in a (4)___. Before '
                               'leaving, Eva switched off a (5)___.',
                'answers': ['plan', 'loud', 'Saturday', 'portfolio', 'tablet'],
                'word_bank': ['plan', 'loud', 'Saturday', 'portfolio', 'tablet', 'zebra'],
                'questions': [{'q': 'What seminar topic was being prepared?',
                               'accept': ['Contemporary art essay', 'contemporary art essay'],
                               'hint_ru': 'Тема семинара?',
                               'quote': 'For a seminar on Contemporary art essay…',
                               'model_en': 'The seminar was on Contemporary art essay.'},
                              {'q': 'Why did they stay at the coworking space?',
                               'accept': ['loud', 'overcrowded', 'café was overcrowded and loud'],
                               'hint_ru': 'Почему коворкинг?',
                               'quote': '…overcrowded and loud.',
                               'model_en': 'They stayed because the café was overcrowded and '
                                           'loud.'},
                              {'q': 'How much did Sara pay?',
                               'accept': ['twelve pounds', '12 pounds', '12'],
                               'hint_ru': 'Сколько заплатили?',
                               'quote': 'Sara paid twelve pounds…',
                               'model_en': 'Sara paid twelve pounds for day passes.'},
                              {'q': 'When is the follow-up?',
                               'accept': ['next Saturday', 'Saturday'],
                               'hint_ru': 'Когда follow-up?',
                               'quote': '…follow-up next Saturday…',
                               'model_en': 'The follow-up is next Saturday.'}],
                'plan': ['Seminar topic (Contemporary art essay)',
                         'Workplace choice',
                         'Work session',
                         'Payment and follow-up'],
                'facts': ['Seminar on Contemporary art essay; focus interpretation, context, '
                          'controversy.',
                          'Café was loud; they used coworking.',
                          'Sara paid twelve pounds.',
                          'Follow-up next Saturday.']},
        'philosophy': {'full_text': 'For a seminar on A moral dilemma, Sara drafted a brief '
                                    'analysis linked to principles, consequences, judgment. Sara '
                                    'outlined a careful plan before drafting. On Wednesday Sara '
                                    'joined Alex at a quiet coworking space. Alex suggested a '
                                    'noisy café, but Sara insisted on the coworking space. They '
                                    'stayed because the café was overcrowded and loud. After three '
                                    'focused hours they summarised the key arguments. Sara paid '
                                    'twelve pounds for day passes. Alex uploaded the shared '
                                    'document. They scheduled a follow-up next Wednesday and Sara '
                                    'filed printouts in a portfolio. Before leaving, Alex switched '
                                    'off a tablet.',
                       'gapped_text': 'For a seminar on A moral dilemma, Sara drafted a brief '
                                      'analysis linked to principles, consequences, judgment. Sara '
                                      'outlined a careful (1)___ before drafting. On Wednesday '
                                      'Sara joined Alex at a quiet coworking space. Alex suggested '
                                      'a noisy café, but Sara insisted on the coworking space. '
                                      'They stayed because the café was overcrowded and (2)___. '
                                      'After three focused hours they summarised the key '
                                      'arguments. Sara paid twelve pounds for day passes. Alex '
                                      'uploaded the shared document. They scheduled a follow-up '
                                      'next (3)___ and Sara filed printouts in a (4)___. Before '
                                      'leaving, Alex switched off a (5)___.',
                       'answers': ['plan', 'loud', 'Wednesday', 'portfolio', 'tablet'],
                       'word_bank': ['plan', 'loud', 'Wednesday', 'portfolio', 'tablet', 'zebra'],
                       'questions': [{'q': 'What seminar topic was being prepared?',
                                      'accept': ['A moral dilemma', 'a moral dilemma'],
                                      'hint_ru': 'Тема семинара?',
                                      'quote': 'For a seminar on A moral dilemma…',
                                      'model_en': 'The seminar was on A moral dilemma.'},
                                     {'q': 'Why did they stay at the coworking space?',
                                      'accept': ['loud',
                                                 'overcrowded',
                                                 'café was overcrowded and loud'],
                                      'hint_ru': 'Почему коворкинг?',
                                      'quote': '…overcrowded and loud.',
                                      'model_en': 'They stayed because the café was overcrowded '
                                                  'and loud.'},
                                     {'q': 'How much did Sara pay?',
                                      'accept': ['twelve pounds', '12 pounds', '12'],
                                      'hint_ru': 'Сколько заплатили?',
                                      'quote': 'Sara paid twelve pounds…',
                                      'model_en': 'Sara paid twelve pounds for day passes.'},
                                     {'q': 'When is the follow-up?',
                                      'accept': ['next Wednesday', 'Wednesday'],
                                      'hint_ru': 'Когда follow-up?',
                                      'quote': '…follow-up next Wednesday…',
                                      'model_en': 'The follow-up is next Wednesday.'}],
                       'plan': ['Seminar topic (A moral dilemma)',
                                'Workplace choice',
                                'Work session',
                                'Payment and follow-up'],
                       'facts': ['Seminar on A moral dilemma; focus principles, consequences, '
                                 'judgment.',
                                 'Café was loud; they used coworking.',
                                 'Sara paid twelve pounds.',
                                 'Follow-up next Wednesday.']}}}


def get_reading_pack(level: str, topic_id: str) -> dict | None:
    lvl = (level or "A1").upper()
    tid = (topic_id or "").strip()
    block = READING_PACKS.get(lvl) or {}
    pack = block.get(tid)
    if not pack:
        return None
    # копия + shuffle банка на вызывающей стороне
    return {
        "full_text": pack["full_text"],
        "gapped_text": pack["gapped_text"],
        "answers": list(pack["answers"]),
        "word_bank": list(pack["word_bank"]),
        "questions": [dict(q) for q in pack["questions"]],
        "plan": list(pack["plan"]),
        "facts": list(pack["facts"]),
    }
