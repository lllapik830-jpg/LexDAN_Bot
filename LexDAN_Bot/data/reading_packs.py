"""Фиксированные Reading-пакеты: все уровни и темы.

Собрано из curated источников data/_rp_*.py через scripts/build_reading_packs.py.
В рантайме GPT для текстов не вызывается.
"""

from __future__ import annotations

READING_PACKS: dict[str, dict[str, dict]] = {'A0': {'family': {'full_text': 'My name is Tom. I live with my family in a small house. I have '
                                'one brother. His name is Max. He is eight years old and he likes '
                                'football. My mother is a nurse. Mum helps sick people at the '
                                'hospital. My father is a driver. Dad drives a big bus in the '
                                'city. In the evening we eat dinner in the kitchen. I love my '
                                'family very much. Next Sunday we will visit grandpa.',
                   'gapped_text': 'My name is Tom. I live with my family in a small house. I have '
                                  'one brother. His name is (1)___. He is eight years old and he '
                                  'likes (2)___. My mother is a (3)___. Mum helps sick people at '
                                  'the hospital. My father is a driver. Dad drives a big bus in '
                                  'the city. In the evening we eat dinner in the (4)___. I love my '
                                  'family very much. Next Sunday we will visit (5)___.',
                   'answers': ['Max', 'football', 'nurse', 'kitchen', 'grandpa'],
                   'word_bank': ['Max', 'football', 'nurse', 'kitchen', 'grandpa', 'bus'],
                   'questions': [{'q': 'How old is Max?',
                                  'accept': ['eight', '8', 'eight years old'],
                                  'hint_ru': 'Сколько лет Максу?',
                                  'quote': 'He is eight years old…',
                                  'model_en': 'Max is eight years old.'},
                                 {'q': "What is Tom's mother's job?",
                                  'accept': ['nurse', 'a nurse'],
                                  'hint_ru': 'Кем работает мама?',
                                  'quote': 'My mother is a nurse…',
                                  'model_en': "Tom's mother is a nurse."},
                                 {'q': 'What does Dad drive?',
                                  'accept': ['a big bus', 'bus', 'a bus'],
                                  'hint_ru': 'Что водит папа?',
                                  'quote': 'Dad drives a big bus…',
                                  'model_en': 'Dad drives a big bus.'},
                                 {'q': 'Where do they eat dinner?',
                                  'accept': ['in the kitchen', 'kitchen'],
                                  'hint_ru': 'Где они ужинают?',
                                  'quote': '…eat dinner in the kitchen.',
                                  'model_en': 'They eat dinner in the kitchen.'}],
                   'plan': ['Who Tom lives with',
                            'Facts about Max',
                            "Parents' jobs",
                            'Evening dinner and Sunday visit'],
                   'facts': ['Tom has a brother named Max.',
                             'Max is eight and likes football.',
                             'Mum is a nurse; Dad is a driver.',
                             'They eat in the kitchen; next Sunday they visit grandpa.']},
        'colors': {'full_text': 'Nina draws with crayons at the table. She colours a big red apple '
                                'first. Then she paints the sky blue on the paper. The grass under '
                                'the tree is green. Her favourite crayon is the colour of the sun '
                                '— yellow. She keeps the crayons in a small box. She shows the '
                                'picture to her friend Sam. Sam says the apple looks real. Nina '
                                'puts the crayons away carefully. She likes bright colours every '
                                'day.',
                   'gapped_text': 'Nina draws with crayons at the table. She colours a big (1)___ '
                                  'apple first. Then she paints the sky (2)___ on the paper. The '
                                  'grass under the tree is (3)___. Her favourite crayon is the '
                                  'colour of the sun — (4)___. She keeps the crayons in a small '
                                  '(5)___. She shows the picture to her friend Sam. Sam says the '
                                  'apple looks real. Nina puts the crayons away carefully. She '
                                  'likes bright colours every day.',
                   'answers': ['red', 'blue', 'green', 'yellow', 'box'],
                   'word_bank': ['red', 'blue', 'green', 'yellow', 'box', 'dog'],
                   'questions': [{'q': "What colour is the apple in Nina's picture?",
                                  'accept': ['red', 'a red apple'],
                                  'hint_ru': 'Какого цвета яблоко на рисунке?',
                                  'quote': '…a big red apple…',
                                  'model_en': 'The apple is red.'},
                                 {'q': 'What colour does she paint the sky?',
                                  'accept': ['blue'],
                                  'hint_ru': 'Каким цветом она красит небо?',
                                  'quote': '…paints the sky blue…',
                                  'model_en': 'She paints the sky blue.'},
                                 {'q': "What colour is Nina's favourite crayon?",
                                  'accept': ['yellow'],
                                  'hint_ru': 'Какого цвета любимый мелок Нины?',
                                  'quote': '…the colour of the sun — yellow.',
                                  'model_en': "Nina's favourite crayon is yellow."},
                                 {'q': 'Where does she keep the crayons?',
                                  'accept': ['in a small box', 'box', 'a small box'],
                                  'hint_ru': 'Где она хранит мелки?',
                                  'quote': '…keeps the crayons in a small box.',
                                  'model_en': 'She keeps the crayons in a small box.'}],
                   'plan': ['Red apple on the paper',
                            'Blue sky and green grass',
                            'Yellow crayon like the sun',
                            'Crayons in a box; showing Sam'],
                   'facts': ['Nina colours a red apple first.',
                             'The sky is blue and the grass is green.',
                             'Her favourite crayon is yellow like the sun.',
                             'She keeps the crayons in a small box.']},
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
                 'word_bank': ['tea', 'apple', 'soup', 'basket', 'cups', 'pencil'],
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
        'pets': {'full_text': 'Rita has two pets at home. Her cat is soft and grey. Its name is '
                              'Mimi. Rita also has a small brown dog. Its name is Buddy. Every '
                              'morning Buddy wants to play with a ball in the garden. Mimi sleeps '
                              'on a soft chair near the window. Rita gives water to them after '
                              'school. On Friday they visit the vet for a short check. Rita loves '
                              'her pets very much.',
                 'gapped_text': 'Rita has two animals at home. Her (1)___ is soft and grey. Its '
                                'name is Mimi. Rita also has a small brown (2)___. Its name is '
                                'Buddy. Every morning Buddy wants to play with a (3)___ in the '
                                'garden. Mimi sleeps on a soft chair near the window. Rita gives '
                                'water to them after school. On Friday they visit the (4)___ for a '
                                'short check. Rita loves her (5)___ very much.',
                 'answers': ['cat', 'dog', 'ball', 'vet', 'pets'],
                 'word_bank': ['cat', 'dog', 'ball', 'vet', 'pets', 'car'],
                 'questions': [{'q': "What is the cat's name?",
                                'accept': ['Mimi'],
                                'hint_ru': 'Как зовут кошку?',
                                'quote': 'Its name is Mimi.',
                                'model_en': "The cat's name is Mimi."},
                               {'q': 'What colour is the dog?',
                                'accept': ['brown', 'small brown'],
                                'hint_ru': 'Какого цвета собака?',
                                'quote': '…a small brown dog.',
                                'model_en': 'The dog is brown.'},
                               {'q': 'What does Buddy play with in the garden?',
                                'accept': ['a ball', 'ball'],
                                'hint_ru': 'С чем играет Бадди в саду?',
                                'quote': '…play with a ball in the garden.',
                                'model_en': 'Buddy plays with a ball in the garden.'},
                               {'q': 'Where do they go on Friday?',
                                'accept': ['the vet', 'vet', 'to the vet'],
                                'hint_ru': 'Куда они идут в пятницу?',
                                'quote': '…visit the vet for a short check.',
                                'model_en': 'They visit the vet on Friday.'}],
                 'plan': ["Rita's cat Mimi",
                          "Rita's dog Buddy",
                          'Morning play and rest',
                          'Friday visit to the vet'],
                 'facts': ['Rita has a grey cat named Mimi.',
                           'She has a brown dog named Buddy.',
                           'Buddy plays with a ball in the garden.',
                           'On Friday they visit the vet.']},
        'home': {'full_text': 'Leo lives in a small flat with two rooms. The kitchen is bright '
                              'because of a big window. His bedroom has a bed, a desk and a blue '
                              'chair at the desk. Near the entrance there is a green plant. In the '
                              'evening Leo reads a book on the soft sofa. His sister draws '
                              'pictures at the desk. Mum opens it when it is hot. Dad fixes the '
                              'door when it makes a noise. They keep shoes next to it. Leo likes '
                              'his home because it is peaceful and quiet.',
                 'gapped_text': 'Leo lives in a small flat with two rooms. The kitchen is bright '
                                'because of a big (1)___. His bedroom has a bed, a desk and a blue '
                                '(2)___ at the desk. Near the entrance there is a green plant. In '
                                'the evening Leo reads a book on the soft (3)___. His sister draws '
                                'pictures at the desk. Mum opens it when it is hot. Dad fixes the '
                                '(4)___ when it makes a noise. They keep shoes next to it. Leo '
                                'likes his home because it is peaceful and (5)___.',
                 'answers': ['window', 'chair', 'sofa', 'door', 'quiet'],
                 'word_bank': ['window', 'chair', 'sofa', 'door', 'quiet', 'garden'],
                 'questions': [{'q': 'Why is the kitchen bright?',
                                'accept': ['big window', 'window', 'because of a big window'],
                                'hint_ru': 'Почему кухня светлая?',
                                'quote': '…because of a big window.',
                                'model_en': 'The kitchen is bright because of a big window.'},
                               {'q': 'What colour is the chair?',
                                'accept': ['blue', 'blue chair'],
                                'hint_ru': 'Какого цвета стул?',
                                'quote': '…a blue chair at the desk.',
                                'model_en': 'The chair is blue.'},
                               {'q': 'Where does Leo read in the evening?',
                                'accept': ['on the soft sofa', 'on the sofa', 'sofa'],
                                'hint_ru': 'Где Лео читает вечером?',
                                'quote': '…reads a book on the soft sofa.',
                                'model_en': 'Leo reads a book on the soft sofa in the evening.'},
                               {'q': 'Why does Leo like his home?',
                                'accept': ['peaceful and quiet',
                                           'quiet',
                                           'because it is peaceful and quiet'],
                                'hint_ru': 'Почему Лео нравится дом?',
                                'quote': '…peaceful and quiet.',
                                'model_en': 'Leo likes his home because it is peaceful and '
                                            'quiet.'}],
                 'plan': ['Flat and kitchen',
                          'Bedroom chair at the desk',
                          'Evening on the soft sofa',
                          'Door, shoes, peaceful quiet home'],
                 'facts': ['Kitchen is bright because of a big window.',
                           'Bedroom has a bed, desk and blue chair at the desk.',
                           'Leo reads on the soft sofa; sister draws at the desk.',
                           'Dad fixes the door; Leo likes the peaceful quiet home.']},
        'school': {'full_text': 'Omar goes to school every morning with a blue bag. In the bag he '
                                'has a pen and a book. His teacher is kind and smiles in the '
                                'classroom. Today the class reads a short story. Omar writes new '
                                'words in his notebook. At break he talks with his friend Kate. In '
                                'the afternoon Omar does homework at the desk. He puts it next to '
                                'the book. Tomorrow someone will check his work carefully. Omar '
                                'likes school very much.',
                   'gapped_text': 'Omar goes every morning with a blue bag. In the bag he has a '
                                  '(1)___ and a notebook. His (2)___ is kind and smiles in the '
                                  'classroom. Today the class reads a short story. Omar writes new '
                                  'words in his notebook. At break he talks with his friend Kate. '
                                  'In the afternoon Omar does (3)___ at the desk. He puts it next '
                                  'to the (4)___. Tomorrow someone will check his work carefully. '
                                  'Omar likes (5)___ very much.',
                   'answers': ['pen', 'teacher', 'homework', 'book', 'school'],
                   'word_bank': ['pen', 'teacher', 'homework', 'book', 'school', 'banana'],
                   'questions': [{'q': "What colour is Omar's bag?",
                                  'accept': ['blue', 'a blue bag'],
                                  'hint_ru': 'Какого цвета сумка Омара?',
                                  'quote': '…with a blue bag.',
                                  'model_en': "Omar's bag is blue."},
                                 {'q': 'Who smiles in the classroom?',
                                  'accept': ['his teacher', 'the teacher', 'teacher'],
                                  'hint_ru': 'Кто улыбается в классе?',
                                  'quote': 'His teacher is kind and smiles…',
                                  'model_en': 'His teacher smiles in the classroom.'},
                                 {'q': 'What does Omar do in the afternoon?',
                                  'accept': ['homework', 'does homework', 'homework at the desk'],
                                  'hint_ru': 'Что Омар делает днём?',
                                  'quote': '…does homework at the desk.',
                                  'model_en': 'Omar does homework in the afternoon.'},
                                 {'q': 'What will happen to his work tomorrow?',
                                  'accept': ['someone will check',
                                             'check his work',
                                             'will check his work carefully'],
                                  'hint_ru': 'Что будет с его работой завтра?',
                                  'quote': 'Tomorrow someone will check his work carefully.',
                                  'model_en': 'Someone will check his work carefully tomorrow.'}],
                   'plan': ['Bag with pen and book',
                            'Teacher and classroom',
                            'Break with Kate',
                            'Homework after school'],
                   'facts': ['Omar carries a pen and a book in a blue bag.',
                             'His teacher is kind in the classroom.',
                             'At break he talks with Kate.',
                             'After school he does homework at the desk.']},
        'days': {'full_text': 'Today is Monday, the first school day of the week. Eva goes to '
                              'school and has English class. On Tuesday she plays tennis with her '
                              'sister. Wednesday is a busy day with maths. On Thursday Eva helps '
                              'Mum in the shop. Friday is her favourite day because school ends '
                              'early. On Saturday the family goes to the market. Sunday is a quiet '
                              'day at home with no lessons. Eva writes the days in her calendar. '
                              'She likes the week when it is clear.',
                 'gapped_text': 'Today is (1)___, the first school day of the week. Eva goes to '
                                'school and has English class. On Tuesday she plays (2)___ with '
                                'her sister. Wednesday is a busy day with maths. On Thursday Eva '
                                'helps Mum in the shop. (3)___ is her favourite day because school '
                                'ends early. On Saturday the family goes to the (4)___. (5)___ is '
                                'a quiet day at home with no lessons. Eva writes the days in her '
                                'calendar. She likes the week when it is clear.',
                 'answers': ['Monday', 'tennis', 'Friday', 'market', 'Sunday'],
                 'word_bank': ['Monday', 'tennis', 'Friday', 'market', 'Sunday', 'Thursday'],
                 'questions': [{'q': 'What day is today?',
                                'accept': ['Monday'],
                                'hint_ru': 'Какой сегодня день?',
                                'quote': 'Today is Monday…',
                                'model_en': 'Today is Monday.'},
                               {'q': 'When does Eva play tennis?',
                                'accept': ['on Tuesday', 'Tuesday'],
                                'hint_ru': 'Когда Эва играет в теннис?',
                                'quote': 'On Tuesday she plays tennis…',
                                'model_en': 'Eva plays tennis on Tuesday.'},
                               {'q': "Which day is Eva's favourite?",
                                'accept': ['Friday'],
                                'hint_ru': 'Какой день любимый у Эвы?',
                                'quote': 'Friday is her favourite day…',
                                'model_en': "Friday is Eva's favourite day."},
                               {'q': 'What do they do on Saturday?',
                                'accept': ['go to the market', 'market', 'goes to the market'],
                                'hint_ru': 'Что они делают в субботу?',
                                'quote': '…the family goes to the market.',
                                'model_en': 'The family goes to the market on Saturday.'}],
                 'plan': ['Monday first school day',
                          'Tuesday tennis',
                          'Favourite Friday',
                          'Saturday market and quiet Sunday'],
                 'facts': ['Today is Monday, the first school day.',
                           'On Tuesday Eva plays tennis.',
                           'Friday is her favourite day.',
                           'Saturday is market day; Sunday is quiet at home.']},
        'hello': {'full_text': 'Ben meets a new girl near the school gate. He says hello with a '
                               'big smile. The girl says her name is Lara. Ben says he is Ben. '
                               'They say nice to meet you and laugh a little. Lara is a new '
                               'student in class. Ben shows Lara the classroom door. The teacher '
                               'says welcome to Lara. At break Ben and Lara sit together. Ben is '
                               'happy to have a new friend.',
                  'gapped_text': 'Ben meets a new girl near the school gate. He says (1)___ with a '
                                 'big (2)___. The girl says her (3)___ is Lara. Ben says he is '
                                 'Ben. They say nice to (4)___ you and laugh a little. Lara is a '
                                 'new student in class. Ben shows Lara the classroom door. The '
                                 'teacher says welcome to Lara. At break Ben and Lara sit '
                                 'together. Ben is happy to have a new (5)___.',
                  'answers': ['hello', 'smile', 'name', 'meet', 'friend'],
                  'word_bank': ['hello', 'smile', 'name', 'meet', 'friend', 'goodbye'],
                  'questions': [{'q': 'Where does Ben meet the new girl?',
                                 'accept': ['near the school gate', 'school gate', 'gate'],
                                 'hint_ru': 'Где Бен встречает новую девочку?',
                                 'quote': '…near the school gate.',
                                 'model_en': 'Ben meets her near the school gate.'},
                                {'q': "What is the girl's name?",
                                 'accept': ['Lara'],
                                 'hint_ru': 'Как зовут девочку?',
                                 'quote': '…her name is Lara.',
                                 'model_en': "The girl's name is Lara."},
                                {'q': 'What do they say after names?',
                                 'accept': ['nice to meet you', 'nice to meet'],
                                 'hint_ru': 'Что они говорят после имён?',
                                 'quote': 'They say nice to meet you…',
                                 'model_en': 'They say nice to meet you.'},
                                {'q': 'Who says welcome to Lara?',
                                 'accept': ['the teacher', 'teacher'],
                                 'hint_ru': 'Кто говорит Ларе welcome?',
                                 'quote': 'The teacher says welcome to Lara.',
                                 'model_en': 'The teacher says welcome to Lara.'}],
                  'plan': ['Meeting near the gate',
                           'Saying names',
                           'Nice to meet you',
                           'New friend at break'],
                  'facts': ['Ben says hello near the school gate.',
                            "The girl's name is Lara.",
                            'They say nice to meet you.',
                            'Ben is happy to have a new friend.']}},
 'A1': {'family_a1': {'full_text': 'My name is Carlos. I live with my parents and my sister Rosa '
                                   'in a flat near the park. She is fourteen years old and she '
                                   'studies art after school. My father is an engineer. Dad '
                                   'designs bridges for the city. My mother is a dentist. Mum '
                                   'works in a small clinic and looks after teeth. At weekends '
                                   'Uncle Pedro visits us with fresh fruit. We cook together and '
                                   'talk about our week. I am proud of my family.',
                      'gapped_text': 'My name is Carlos. I live with my parents and my sister '
                                     '(1)___ in a flat near the park. She is (2)___ years old and '
                                     'she studies art after school. My father is an (3)___. Dad '
                                     'designs bridges for the city. My mother is a (4)___. Mum '
                                     'works in a small clinic and looks after teeth. At weekends '
                                     'Uncle (5)___ visits us with fresh fruit. We cook together '
                                     'and talk about our week. I am proud of my family.',
                      'answers': ['Rosa', 'fourteen', 'engineer', 'dentist', 'Pedro'],
                      'word_bank': ['Rosa', 'fourteen', 'engineer', 'dentist', 'Pedro', 'teacher'],
                      'questions': [{'q': 'How old is Rosa?',
                                     'accept': ['fourteen', '14', 'fourteen years old'],
                                     'hint_ru': 'Сколько лет Росе?',
                                     'quote': 'She is fourteen years old…',
                                     'model_en': 'Rosa is fourteen years old.'},
                                    {'q': "What is Carlos's father's job?",
                                     'accept': ['engineer', 'an engineer'],
                                     'hint_ru': 'Кем работает папа Карлоса?',
                                     'quote': 'My father is an engineer…',
                                     'model_en': "Carlos's father is an engineer."},
                                    {'q': 'Where does Mum work?',
                                     'accept': ['in a small clinic', 'clinic', 'a small clinic'],
                                     'hint_ru': 'Где работает мама?',
                                     'quote': 'Mum works in a small clinic…',
                                     'model_en': 'Mum works in a small clinic.'},
                                    {'q': 'Who visits at weekends?',
                                     'accept': ['Uncle Pedro', 'Pedro', 'uncle'],
                                     'hint_ru': 'Кто приходит в выходные?',
                                     'quote': '…Uncle Pedro visits us…',
                                     'model_en': 'Uncle Pedro visits them at weekends.'}],
                      'plan': ['Carlos and sister Rosa',
                               "Father's job as engineer",
                               "Mother's job as dentist",
                               'Weekend visit from Uncle Pedro'],
                      'facts': ['Carlos lives with parents and sister Rosa.',
                                'Rosa is fourteen and studies art.',
                                'Dad is an engineer; Mum is a dentist.',
                                'Uncle Pedro visits at weekends.']},
        'cafe': {'full_text': 'Sara and Dan sit at a small café near the station. The waiter '
                              'brings a list of drinks and food to their table. Sara orders a cup '
                              'of black coffee and a piece of chocolate cake. Dan chooses green '
                              'tea and a cheese sandwich. They look at the menu again and share '
                              'one small cookie. The café is quiet and the table by the window is '
                              'free. Sara pays eight pounds for the order. They thank him and '
                              'leave happy.',
                 'gapped_text': 'Sara and Dan sit at a small café near the station. The (1)___ '
                                'brings a list of drinks and food to their table. Sara orders a '
                                'cup of black (2)___ and a piece of chocolate (3)___. Dan chooses '
                                'green (4)___ and a cheese sandwich. They look at the (5)___ again '
                                'and share one small cookie. The café is quiet and the table by '
                                'the window is free. Sara pays eight pounds for the order. They '
                                'thank him and leave happy.',
                 'answers': ['waiter', 'coffee', 'cake', 'tea', 'menu'],
                 'word_bank': ['waiter', 'coffee', 'cake', 'tea', 'menu', 'juice'],
                 'questions': [{'q': 'Who brings the list of drinks and food?',
                                'accept': ['the waiter', 'waiter'],
                                'hint_ru': 'Кто приносит список напитков и еды?',
                                'quote': 'The waiter brings a list of drinks and food…',
                                'model_en': 'The waiter brings a list of drinks and food.'},
                               {'q': 'What does Sara order to drink?',
                                'accept': ['coffee',
                                           'black coffee',
                                           'a cup of black coffee',
                                           'a cup of coffee'],
                                'hint_ru': 'Что Сара заказывает выпить?',
                                'quote': 'Sara orders a cup of black coffee…',
                                'model_en': 'Sara orders a cup of black coffee.'},
                               {'q': 'What does Dan choose to drink?',
                                'accept': ['green tea', 'a green tea', 'green tea and a cheese sandwich'],
                                'hint_ru': 'Что выбирает Дэн?',
                                'quote': 'Dan chooses green tea…',
                                'model_en': 'Dan chooses green tea.'},
                               {'q': 'How much does Sara pay?',
                                'accept': ['eight pounds', '8 pounds', 'eight', '£8'],
                                'hint_ru': 'Сколько платит Сара?',
                                'quote': 'Sara pays eight pounds…',
                                'model_en': 'Sara pays eight pounds.'}],
                 'plan': ['Sitting at the café',
                          "Sara's black coffee and cake",
                          "Dan's tea and sandwich",
                          'Payment and thanking the waiter'],
                 'facts': ['The waiter brings a list of drinks and food.',
                           'Sara orders black coffee and chocolate cake.',
                           'Dan chooses green tea and a cheese sandwich.',
                           'Sara pays eight pounds.']},
        'daily': {'full_text': 'Every morning Kate wakes up at seven. She washes her face and eats '
                               'breakfast quickly. Then she takes the bus to work and listens to '
                               "music on the way. At one o'clock she has a short lunch at the "
                               'office with a sandwich. In the afternoon Kate answers emails and '
                               'calls clients. In the evening she cooks a simple dinner and reads '
                               'a book. Before bed she checks her plan for tomorrow. Kate likes a '
                               'clear daily routine.',
                  'gapped_text': 'Every morning Kate (1)___ up at seven. She washes her face and '
                                 'eats (2)___ quickly. Then she takes the (3)___ to work and '
                                 "listens to music on the way. At one o'clock she has a short "
                                 '(4)___ at the office with a sandwich. In the afternoon Kate '
                                 'answers emails and calls clients. In the (5)___ she cooks a '
                                 'simple dinner and reads a book. Before bed she checks her plan '
                                 'for tomorrow. Kate likes a clear daily routine.',
                  'answers': ['wakes', 'breakfast', 'bus', 'lunch', 'evening'],
                  'word_bank': ['wakes', 'breakfast', 'bus', 'lunch', 'evening', 'shower'],
                  'questions': [{'q': 'What time does Kate wake up?',
                                 'accept': ['seven', 'at seven', '7'],
                                 'hint_ru': 'Во сколько Кейт просыпается?',
                                 'quote': '…wakes up at seven.',
                                 'model_en': 'Kate wakes up at seven.'},
                                {'q': 'How does she go to work?',
                                 'accept': ['by bus', 'bus', 'takes the bus'],
                                 'hint_ru': 'Как она добирается на работу?',
                                 'quote': '…takes the bus to work…',
                                 'model_en': 'She takes the bus to work.'},
                                {'q': 'When does she have lunch?',
                                 'accept': ["at one o'clock", "one o'clock", "1 o'clock", 'at one'],
                                 'hint_ru': 'Когда у неё обед?',
                                 'quote': "At one o'clock she has a short lunch…",
                                 'model_en': "She has lunch at one o'clock."},
                                {'q': 'What does she do in the evening?',
                                 'accept': ['cooks dinner and reads',
                                            'cooks a simple dinner',
                                            'reads a book',
                                            'cooks and reads'],
                                 'hint_ru': 'Что она делает вечером?',
                                 'quote': '…cooks a simple dinner and reads a book.',
                                 'model_en': 'In the evening she cooks dinner and reads a book.'}],
                  'plan': ['Morning wake-up and breakfast',
                           'Bus to work',
                           'Lunch at the office',
                           'Evening dinner and reading'],
                  'facts': ['Kate wakes up at seven.',
                            'She takes the bus to work.',
                            "She has lunch at one o'clock.",
                            'In the evening she cooks and reads.']},
        'hobbies': {'full_text': 'In his free time Alex plays football with friends in the park '
                                 'near his house. On rainy days he plays the guitar at home and '
                                 'writes short songs. Alex also likes films and watches one every '
                                 'Friday night with popcorn. His sister prefers reading long '
                                 'stories on the sofa. At the weekend Alex goes swimming at the '
                                 'sports centre for one hour. These hobbies help him relax after a '
                                 'busy week at school.',
                    'gapped_text': 'In his free time Alex plays (1)___ with friends in the park '
                                   'near his house. On rainy days he plays the (2)___ at home and '
                                   'writes short songs. Alex also likes (3)___ and watches one '
                                   'every Friday night with popcorn. His sister prefers (4)___ '
                                   'long stories on the sofa. At the weekend Alex goes (5)___ at '
                                   'the sports centre for one hour. These hobbies help him relax '
                                   'after a busy week at school.',
                    'answers': ['football', 'guitar', 'films', 'reading', 'swimming'],
                    'word_bank': ['football', 'guitar', 'films', 'reading', 'swimming', 'kitchen'],
                    'questions': [{'q': 'What does Alex play in the park?',
                                   'accept': ['football'],
                                   'hint_ru': 'Во что Алекс играет в парке?',
                                   'quote': '…plays football with friends in the park…',
                                   'model_en': 'Alex plays football in the park.'},
                                  {'q': 'What does he play on rainy days?',
                                   'accept': ['the guitar', 'guitar'],
                                   'hint_ru': 'На чём он играет в дождливые дни?',
                                   'quote': '…plays the guitar at home…',
                                   'model_en': 'He plays the guitar on rainy days.'},
                                  {'q': 'When does Alex watch a film?',
                                   'accept': ['every Friday night', 'Friday night', 'Friday'],
                                   'hint_ru': 'Когда Алекс смотрит фильм?',
                                   'quote': '…watches one every Friday night…',
                                   'model_en': 'Alex watches a film every Friday night.'},
                                  {'q': 'Where does Alex go swimming?',
                                   'accept': ['at the sports centre', 'sports centre'],
                                   'hint_ru': 'Где Алекс плавает?',
                                   'quote': '…swimming at the sports centre…',
                                   'model_en': 'Alex goes swimming at the sports centre.'}],
                    'plan': ['Football in the park',
                             'Guitar on rainy days',
                             "Films and sister's reading",
                             'Weekend swimming'],
                    'facts': ['Alex plays football with friends.',
                              'On rainy days he plays the guitar.',
                              'He watches films on Friday night.',
                              'At the weekend he goes swimming.']},
        'shopping': {'full_text': 'Maya goes to a clothes shop on High Street after school. She '
                                  'needs new jeans for school. The assistant asks about the size. '
                                  'Maya tries a medium pair in the fitting room. The price is '
                                  'twenty pounds. Maya likes the colour and decides to pay by '
                                  'card. She also buys a small scarf for her mum as a gift. The '
                                  'assistant puts everything in a paper bag. Maya leaves with a '
                                  'smile.',
                     'gapped_text': 'Maya goes to a clothes (1)___ on High Street after school. '
                                    'She needs new (2)___ for school. The assistant asks about the '
                                    '(3)___. Maya tries a medium pair in the fitting room. The '
                                    '(4)___ is twenty pounds. Maya likes the colour and decides to '
                                    '(5)___ by card. She also buys a small scarf for her mum as a '
                                    'gift. The assistant puts everything in a paper bag. Maya '
                                    'leaves with a smile.',
                     'answers': ['shop', 'jeans', 'size', 'price', 'pay'],
                     'word_bank': ['shop', 'jeans', 'size', 'price', 'pay', 'lemon'],
                     'questions': [{'q': 'What does Maya need for school?',
                                    'accept': ['new jeans', 'jeans'],
                                    'hint_ru': 'Что нужно Майе для школы?',
                                    'quote': 'She needs new jeans for school.',
                                    'model_en': 'Maya needs new jeans for school.'},
                                   {'q': 'What size does she try?',
                                    'accept': ['medium', 'a medium pair'],
                                    'hint_ru': 'Какой размер она примеряет?',
                                    'quote': 'Maya tries a medium pair…',
                                    'model_en': 'She tries a medium pair.'},
                                   {'q': 'How much are the jeans?',
                                    'accept': ['twenty pounds', '20 pounds', 'twenty', '£20'],
                                    'hint_ru': 'Сколько стоят джинсы?',
                                    'quote': 'The price is twenty pounds.',
                                    'model_en': 'The jeans cost twenty pounds.'},
                                   {'q': 'How does Maya pay?',
                                    'accept': ['by card', 'card'],
                                    'hint_ru': 'Как Майя платит?',
                                    'quote': '…pay by card.',
                                    'model_en': 'Maya pays by card.'}],
                     'plan': ['Clothes shop on High Street',
                              'Trying jeans and size',
                              'Price and payment',
                              'Scarf for mum'],
                     'facts': ['Maya needs new jeans for school.',
                               'She tries a medium size.',
                               'The price is twenty pounds.',
                               'She pays by card and buys a scarf.']},
        'weekend': {'full_text': 'On Saturday morning Nora meets her friends at the bus stop near '
                                 'the station. They go to the cinema and watch a funny film '
                                 'together. After the film they walk in the park and buy ice '
                                 'cream. On Sunday Nora stays at home and calls her grandma for a '
                                 'long chat. In the afternoon the family has a small picnic in the '
                                 'garden. Nora likes weekends because she can rest and see '
                                 'friends.',
                    'gapped_text': 'On (1)___ morning Nora meets them at the bus stop near the '
                                   'station. They go to the (2)___ and watch a funny film '
                                   'together. After the film they walk in the (3)___ and buy ice '
                                   'cream. On Sunday Nora stays at home and calls her grandma for '
                                   'a long chat. In the afternoon the family has a small (4)___ in '
                                   'the garden. Nora likes weekends because she can rest and see '
                                   '(5)___.',
                    'answers': ['Saturday', 'cinema', 'park', 'picnic', 'friends'],
                    'word_bank': ['Saturday', 'cinema', 'park', 'picnic', 'friends', 'museum'],
                    'questions': [{'q': 'Where do they watch a film?',
                                   'accept': ['at the cinema', 'cinema', 'the cinema'],
                                   'hint_ru': 'Где они смотрят фильм?',
                                   'quote': 'They go to the cinema…',
                                   'model_en': 'They watch a film at the cinema.'},
                                  {'q': 'Where do they walk after the film?',
                                   'accept': ['in the park', 'park', 'the park'],
                                   'hint_ru': 'Где они гуляют после фильма?',
                                   'quote': '…walk in the park…',
                                   'model_en': 'They walk in the park after the film.'},
                                  {'q': 'What does Nora do on Sunday at home?',
                                   'accept': ['calls her grandma',
                                              'calls grandma',
                                              'stays at home'],
                                   'hint_ru': 'Что Нора делает дома в воскресенье?',
                                   'quote': '…stays at home and calls her grandma…',
                                   'model_en': 'Nora stays at home and calls her grandma.'},
                                  {'q': 'Where is the picnic?',
                                   'accept': ['in the garden', 'garden'],
                                   'hint_ru': 'Где проходит пикник?',
                                   'quote': '…picnic in the garden.',
                                   'model_en': 'The picnic is in the garden.'}],
                    'plan': ['Saturday meet friends',
                             'Cinema and park',
                             'Sunday call to grandma',
                             'Garden picnic'],
                    'facts': ['On Saturday they go to the cinema.',
                              'After the film they walk in the park.',
                              'On Sunday Nora calls her grandma.',
                              'The family has a picnic in the garden.']},
        'school_day': {'full_text': 'Yesterday was a long school day for Jade. She had five '
                                    'lessons before lunch. In the morning she had maths and '
                                    'English with her class. At break she ate an apple in the yard '
                                    'with her friends. After lunch there was history and art. The '
                                    'teacher gave tasks in three subjects. Jade wrote the tasks in '
                                    'her diary carefully. In the evening she finished the homework '
                                    'at her desk. She felt tired but happy.',
                       'gapped_text': 'Yesterday was a long school day for Jade. She had five '
                                      '(1)___ before lunch. In the morning she had (2)___ and '
                                      'English with her class. At (3)___ she ate an apple in the '
                                      'yard with her friends. After lunch there was history and '
                                      'art. The (4)___ gave tasks in three subjects. Jade wrote '
                                      'the tasks in her diary carefully. In the evening she '
                                      'finished the (5)___ at her desk. She felt tired but happy.',
                       'answers': ['lessons', 'maths', 'break', 'teacher', 'homework'],
                       'word_bank': ['lessons', 'maths', 'break', 'teacher', 'homework', 'garden'],
                       'questions': [{'q': 'How many lessons did Jade have before lunch?',
                                      'accept': ['five', '5', 'five lessons'],
                                      'hint_ru': 'Сколько уроков было до обеда?',
                                      'quote': 'She had five lessons before lunch.',
                                      'model_en': 'Jade had five lessons before lunch.'},
                                     {'q': 'What subjects did she have in the morning?',
                                      'accept': ['maths and English', 'maths', 'English'],
                                      'hint_ru': 'Какие предметы были утром?',
                                      'quote': '…she had maths and English…',
                                      'model_en': 'In the morning she had maths and English.'},
                                     {'q': 'What did she eat at break?',
                                      'accept': ['an apple', 'apple'],
                                      'hint_ru': 'Что она ела на перемене?',
                                      'quote': '…ate an apple in the yard…',
                                      'model_en': 'She ate an apple at break.'},
                                     {'q': 'When did she finish the homework?',
                                      'accept': ['in the evening', 'evening'],
                                      'hint_ru': 'Когда она закончила домашнее задание?',
                                      'quote': 'In the evening she finished the homework…',
                                      'model_en': 'She finished the homework in the evening.'}],
                       'plan': ['Five lessons before lunch',
                                'Morning subjects and break',
                                'Afternoon history and art',
                                'Evening homework'],
                       'facts': ['Jade had five lessons before lunch.',
                                 'Morning subjects were maths and English.',
                                 'At break she ate an apple.',
                                 'She finished homework in the evening.']},
        'weather': {'full_text': 'Yesterday the weather was rainy — water fell from the sky — and '
                                 'cold. Mia wore a warm coat and took an umbrella. She walked to '
                                 'the bus stop slowly. Today the sky is blue and the sun is '
                                 'bright. Mia puts it back in the hall. She chooses a light jacket '
                                 'instead of the coat. Her brother wants to play football outside. '
                                 'Mum says they can go if it stays sunny. In the evening it may '
                                 'become windy. Mia checks the weather again before dinner.',
                    'gapped_text': 'Yesterday the weather was (1)___ — water fell from the sky — '
                                   'and (2)___. Mia wore a warm coat and took an (3)___. She '
                                   'walked to the bus stop slowly. Today the sky is blue and the '
                                   'sun is bright. Mia puts it back in the hall. She chooses a '
                                   'light (4)___ instead of the coat. Her brother wants to play '
                                   'football outside. Mum says they can go if it stays (5)___. In '
                                   'the evening it may become windy. Mia checks the weather again '
                                   'before dinner.',
                    'answers': ['rainy', 'cold', 'umbrella', 'jacket', 'sunny'],
                    'word_bank': ['rainy', 'cold', 'umbrella', 'jacket', 'sunny', 'snowy'],
                    'questions': [{'q': 'What was the weather like yesterday?',
                                   'accept': ['rainy and cold', 'rainy', 'cold'],
                                   'hint_ru': 'Какая была погода вчера?',
                                   'quote': 'Yesterday the weather was rainy — water fell from the '
                                            'sky — and cold.',
                                   'model_en': 'Yesterday the weather was rainy and cold.'},
                                  {'q': 'What does Mia choose today instead of the coat?',
                                   'accept': ['light jacket', 'jacket', 'a light jacket'],
                                   'hint_ru': 'Что она выбирает вместо пальто?',
                                   'quote': '…a light jacket instead of the coat.',
                                   'model_en': 'Mia chooses a light jacket instead of the coat.'},
                                  {'q': 'When can her brother play outside?',
                                   'accept': ['if it stays sunny', 'if sunny', 'when sunny'],
                                   'hint_ru': 'Когда брат может играть на улице?',
                                   'quote': '…if it stays sunny.',
                                   'model_en': 'They can go if it stays sunny.'},
                                  {'q': 'What may the evening become?',
                                   'accept': ['windy', 'become windy'],
                                   'hint_ru': 'Каким может стать вечер?',
                                   'quote': 'In the evening it may become windy.',
                                   'model_en': 'The evening may become windy.'}],
                    'plan': ['Yesterday rainy and cold',
                             'Umbrella and coat',
                             'Today jacket and sunny plans',
                             'Evening may be windy'],
                    'facts': ['Yesterday was rainy and cold; Mia took an umbrella.',
                              'Today she chooses a light jacket.',
                              'Brother can play outside if it stays sunny.',
                              'Evening may become windy.']}},
 'A2': {'travel': {'full_text': 'Last Saturday Olga took a morning train to the sea. She bought a '
                                'ticket at the station and put it in her bag. The journey lasted '
                                'two hours, and she looked out of the window. In the town she '
                                'found a small hotel near the beach. After lunch she went '
                                'sightseeing with a free city map. She visited an old castle and '
                                'took many photos. In the evening she walked along the coast and '
                                'bought ice cream. On Sunday she packed her suitcase and returned '
                                'home the same way. Olga said the trip was short but very nice.',
                   'gapped_text': 'Last Saturday Olga took a morning (1)___ to the sea. She bought '
                                  'a (2)___ at the station and put it in her bag. The journey '
                                  'lasted two hours, and she looked out of the window. In the town '
                                  'she found a small (3)___ near the beach. After lunch she went '
                                  '(4)___ with a free city map. She visited an old castle and took '
                                  'many photos. In the evening she walked along the coast and '
                                  'bought ice cream. On Sunday she packed her (5)___ and returned '
                                  'home the same way. Olga said the trip was short but very nice.',
                   'answers': ['train', 'ticket', 'hotel', 'sightseeing', 'suitcase'],
                   'word_bank': ['train', 'ticket', 'hotel', 'sightseeing', 'suitcase', 'airport'],
                   'questions': [{'q': 'How did Olga travel to the sea?',
                                  'accept': ['by train', 'train', 'morning train'],
                                  'hint_ru': 'На чём Ольга доехала до моря?',
                                  'quote': '…took a morning train to the sea.',
                                  'model_en': 'Olga travelled by train.'},
                                 {'q': 'Where did she buy her ticket?',
                                  'accept': ['at the station', 'station'],
                                  'hint_ru': 'Где она купила билет?',
                                  'quote': '…bought a ticket at the station…',
                                  'model_en': 'She bought her ticket at the station.'},
                                 {'q': 'Where was the hotel?',
                                  'accept': ['near the beach', 'by the beach', 'beach'],
                                  'hint_ru': 'Где находился отель?',
                                  'quote': '…a small hotel near the beach.',
                                  'model_en': 'The hotel was near the beach.'},
                                 {'q': 'What did she visit with the map?',
                                  'accept': ['an old castle', 'castle', 'old castle'],
                                  'hint_ru': 'Что она посетила с картой?',
                                  'quote': 'She visited an old castle…',
                                  'model_en': 'She visited an old castle.'}],
                   'plan': ['Train journey and ticket',
                            'Hotel near the beach',
                            'Sightseeing and castle',
                            'Sunday return home'],
                   'facts': ['Olga took a morning train and bought a ticket at the station.',
                             'She stayed in a small hotel near the beach.',
                             'She went sightseeing and visited an old castle.',
                             'On Sunday she packed her suitcase and returned home the same way.']},
        'doctor': {'full_text': 'On Monday Tom woke up with a sore throat and a high temperature. '
                                'His mother took him to the clinic after breakfast. The doctor '
                                'asked about his symptoms and checked his throat. She said Tom had '
                                'a cold and needed rest at home. Then she wrote a prescription for '
                                'medicine and cough syrup. Tom must drink warm tea and sleep more '
                                'for three days. He should not go to football practice this week. '
                                'At the pharmacy they bought the syrup and went home. By Thursday '
                                'Tom felt much better and smiled again.',
                   'gapped_text': 'On Monday Tom woke up with a sore throat and a high '
                                  'temperature. His mother took him to the clinic after breakfast. '
                                  'The doctor asked about his (1)___ and checked his throat. She '
                                  'said Tom had a cold and needed (2)___ at home. Then she wrote a '
                                  'prescription for (3)___ and cough syrup. Tom must drink warm '
                                  'tea and sleep more for three days. He should not go to football '
                                  '(4)___ this week. At the pharmacy they bought the syrup and '
                                  'went home. By Thursday Tom felt much (5)___ and smiled again.',
                   'answers': ['symptoms', 'rest', 'medicine', 'practice', 'better'],
                   'word_bank': ['symptoms', 'rest', 'medicine', 'practice', 'better', 'injection'],
                   'questions': [{'q': 'What was wrong with Tom on Monday?',
                                  'accept': ['sore throat and high temperature',
                                             'sore throat',
                                             'cold',
                                             'high temperature'],
                                  'hint_ru': 'Что было не так с Томом в понедельник?',
                                  'quote': '…sore throat and a high temperature.',
                                  'model_en': 'Tom had a sore throat and a high temperature.'},
                                 {'q': 'What did the doctor say Tom needed?',
                                  'accept': ['rest', 'rest at home', 'needed rest'],
                                  'hint_ru': 'Что, по словам врача, нужно Тому?',
                                  'quote': '…needed rest at home.',
                                  'model_en': 'The doctor said Tom needed rest at home.'},
                                 {'q': 'Where did they buy the medicine?',
                                  'accept': ['at the pharmacy', 'pharmacy'],
                                  'hint_ru': 'Где они купили лекарство?',
                                  'quote': 'At the pharmacy they bought the syrup…',
                                  'model_en': 'They bought the medicine at the pharmacy.'},
                                 {'q': 'When did Tom feel better?',
                                  'accept': ['by Thursday', 'Thursday'],
                                  'hint_ru': 'Когда Тому стало лучше?',
                                  'quote': 'By Thursday Tom felt much better…',
                                  'model_en': 'Tom felt better by Thursday.'}],
                   'plan': ['Symptoms and clinic visit',
                            "Doctor's advice and medicine",
                            'Rules at home',
                            'Feeling better on Thursday'],
                   'facts': ['Tom had a sore throat and high temperature.',
                             'The doctor checked symptoms and said he needed rest.',
                             'They got medicine and cough syrup from the pharmacy.',
                             'By Thursday Tom felt much better.']},
        'party': {'full_text': 'Sara invited ten guests to her birthday party on Friday evening. '
                               'Her brother hung colourful balloons in the living room before '
                               'anyone arrived. Friends brought gifts and a big chocolate cake '
                               'with her name on top. Sara put snacks and lemonade on the long '
                               'table near the window. They played music and danced for almost an '
                               'hour. Later everyone sang for Sara and she blew out the candles. '
                               'Mum took photos while Dad poured more lemonade for the children. '
                               "At ten o'clock everyone said goodbye and went home happily. Sara "
                               'thanked everyone and kept the thank-you cards near her bed.',
                  'gapped_text': 'Sara invited ten (1)___ to her birthday party on Friday evening. '
                                 'Her brother hung colourful balloons in the living room before '
                                 'anyone arrived. Friends brought (2)___ and a big chocolate cake '
                                 'with her name on top. Sara put snacks and lemonade on the long '
                                 'table near the window. They played (3)___ and danced for almost '
                                 'an hour. Later everyone sang for Sara and she blew out the '
                                 '(4)___. Mum took photos while Dad poured more lemonade for the '
                                 "children. At ten o'clock everyone said goodbye and went home "
                                 'happily. Sara thanked everyone and kept the thank-you (5)___ '
                                 'near her bed.',
                  'answers': ['guests', 'gifts', 'music', 'candles', 'cards'],
                  'word_bank': ['guests', 'gifts', 'music', 'candles', 'cards', 'fireworks'],
                  'questions': [{'q': 'How many guests did Sara invite?',
                                 'accept': ['ten', '10', 'ten guests'],
                                 'hint_ru': 'Сколько гостей пригласила Сара?',
                                 'quote': 'Sara invited ten guests…',
                                 'model_en': 'Sara invited ten guests.'},
                                {'q': 'What cake did friends bring?',
                                 'accept': ['chocolate cake', 'big chocolate cake', 'chocolate'],
                                 'hint_ru': 'Какой торт принесли друзья?',
                                 'quote': '…a big chocolate cake.',
                                 'model_en': 'Friends brought a big chocolate cake.'},
                                {'q': 'What did they do while the music played?',
                                 'accept': ['danced', 'dance', 'danced for almost an hour'],
                                 'hint_ru': 'Что они делали под музыку?',
                                 'quote': '…played music and danced…',
                                 'model_en': 'They danced while the music played.'},
                                {'q': 'When did the guests go home?',
                                 'accept': ["at ten o'clock",
                                            "ten o'clock",
                                            'at ten',
                                            "10 o'clock"],
                                 'hint_ru': 'Когда гости ушли домой?',
                                 'quote': "At ten o'clock everyone said goodbye…",
                                 'model_en': "The guests went home at ten o'clock."}],
                  'plan': ['Guests and decorations',
                           'Gifts, cake and table',
                           'Music, singing and candles',
                           'Goodbye and thank-you cards'],
                  'facts': ['Sara invited ten guests on Friday evening.',
                            'Friends brought gifts and a chocolate cake.',
                            'They played music, danced and blew out candles.',
                            'Everyone left at ten; Sara kept the thank-you cards.']},
        'sport': {'full_text': 'Every Tuesday Ben goes to the gym near his school after classes. '
                               'He runs on the treadmill for twenty minutes first. Then he lifts '
                               'light weights and stretches carefully. After training he feels '
                               'tired but also healthy and strong. His coach says water and sleep '
                               'are important for sport. On Thursdays Ben plays football with '
                               'friends in the park. Last week he scored one goal and his team won '
                               'the match. Ben wants to join a running club next month if he has '
                               'time. He believes sport helps him study better at school.',
                  'gapped_text': 'Every Tuesday Ben goes to the (1)___ near his school after '
                                 'classes. He (2)___ on the treadmill for twenty minutes first. '
                                 'Then he lifts light weights and stretches carefully. After '
                                 'training he feels (3)___ but also healthy and strong. His coach '
                                 'says water and sleep are important for sport. On Thursdays Ben '
                                 'plays (4)___ with friends in the park. Last week he scored one '
                                 'goal and his team won the match. Ben wants to join a running '
                                 '(5)___ next month if he has time. He believes sport helps him '
                                 'study better at school.',
                  'answers': ['gym', 'runs', 'tired', 'football', 'club'],
                  'word_bank': ['gym', 'runs', 'tired', 'football', 'club', 'swimming'],
                  'questions': [{'q': 'When does Ben go to the gym?',
                                 'accept': ['every Tuesday', 'Tuesday', 'on Tuesday'],
                                 'hint_ru': 'Когда Бен ходит в спортзал?',
                                 'quote': 'Every Tuesday Ben goes to the gym…',
                                 'model_en': 'Ben goes to the gym every Tuesday.'},
                                {'q': 'How long does he run on the treadmill?',
                                 'accept': ['twenty minutes', '20 minutes', 'for twenty minutes'],
                                 'hint_ru': 'Сколько он бегает на беговой дорожке?',
                                 'quote': '…runs on the treadmill for twenty minutes…',
                                 'model_en': 'He runs for twenty minutes.'},
                                {'q': 'What does he play on Thursdays?',
                                 'accept': ['football', 'plays football'],
                                 'hint_ru': 'Во что он играет по четвергам?',
                                 'quote': '…plays football with friends…',
                                 'model_en': 'Ben plays football on Thursdays.'},
                                {'q': 'What does Ben want to join next month?',
                                 'accept': ['a running club', 'running club', 'club'],
                                 'hint_ru': 'Куда Бен хочет вступить в следующем месяце?',
                                 'quote': '…join a running club next month.',
                                 'model_en': 'Ben wants to join a running club.'}],
                  'plan': ['Gym routine on Tuesday',
                           'Feeling after training',
                           'Football on Thursday',
                           'Plans for a running club'],
                  'facts': ['Ben goes to the gym every Tuesday and runs twenty minutes.',
                            'After training he feels tired but healthy.',
                            'On Thursdays he plays football in the park.',
                            'He wants to join a running club next month.']},
        'neighbours': {'full_text': 'Lena lives on the third floor next to a friendly family with '
                                    'two children. Sometimes in the evening she hears music '
                                    'through the wall. Last Friday the noise was loud, so she '
                                    'knocked politely on their door. Her neighbour Max apologised '
                                    'and turned the music down at once. On Saturday Max helped '
                                    'Lena carry a heavy box upstairs. Later Lena baked cookies and '
                                    'shared them with his flat. They often chat near the postboxes '
                                    'after work about the weather. Lena likes her neighbours '
                                    'because they are kind and quiet. Next week they will water '
                                    'plants for each other during holidays.',
                       'gapped_text': 'Lena lives on the third floor next to a friendly family '
                                      'with two children. Sometimes in the (1)___ she hears music '
                                      'through the wall. Last Friday the (2)___ was loud, so she '
                                      'knocked politely on their door. Her neighbour Max '
                                      'apologised and turned the music down at once. On Saturday '
                                      'Max helped Lena carry a heavy (3)___ upstairs. Later Lena '
                                      'baked cookies and shared them with his (4)___. They often '
                                      'chat near the postboxes after work about the weather. Lena '
                                      'likes her neighbours because they are kind and (5)___. Next '
                                      'week they will water plants for each other during holidays.',
                       'answers': ['evening', 'noise', 'box', 'flat', 'quiet'],
                       'word_bank': ['evening', 'noise', 'box', 'flat', 'quiet', 'angry'],
                       'questions': [{'q': 'What does Lena sometimes hear through the wall?',
                                      'accept': ['music', 'hears music'],
                                      'hint_ru': 'Что Лена иногда слышит через стену?',
                                      'quote': '…hears music through the wall.',
                                      'model_en': 'Lena sometimes hears music through the wall.'},
                                     {'q': 'What did Max do after Lena knocked?',
                                      'accept': ['apologised and turned the music down',
                                                 'turned the music down',
                                                 'apologised'],
                                      'hint_ru': 'Что сделал Макс после того, как Лена постучала?',
                                      'quote': '…apologised and turned the music down.',
                                      'model_en': 'Max apologised and turned the music down.'},
                                     {'q': 'How did Max help Lena on Saturday?',
                                      'accept': ['carry a heavy box upstairs',
                                                 'helped carry a box',
                                                 'carried a box'],
                                      'hint_ru': 'Как Макс помог Лене в субботу?',
                                      'quote': '…helped Lena carry a heavy box upstairs.',
                                      'model_en': 'Max helped Lena carry a heavy box upstairs.'},
                                     {'q': 'Why does Lena like her neighbours?',
                                      'accept': ['kind and quiet',
                                                 'they are kind and quiet',
                                                 'kind'],
                                      'hint_ru': 'Почему Лене нравятся соседи?',
                                      'quote': '…because they are kind and quiet.',
                                      'model_en': 'Lena likes her neighbours because they are kind '
                                                  'and quiet.'}],
                       'plan': ['Evening music through the wall',
                                'Polite talk about noise',
                                'Help with a heavy box',
                                'Cookies and friendly neighbours'],
                       'facts': ['Lena sometimes hears music in the evening.',
                                 'Max apologised and turned the music down.',
                                 'Max helped carry a heavy box; Lena shared cookies.',
                                 'She likes neighbours who are kind and quiet.']},
        'lost': {'full_text': 'Yesterday Mia lost her blue bag on the bus to town. Inside there '
                              'was a purse, keys and a small notebook. She described it to the '
                              'driver at the next stop. The colour was bright blue with a yellow '
                              'zip. A passenger found it under a seat and gave it back. Mia '
                              'checked everything and smiled with relief. She thanked the '
                              'passenger and the driver many times. Then she wrote her phone '
                              'number on a paper inside it. Now Mia is more careful when she '
                              'travels alone.',
                 'gapped_text': 'Yesterday Mia lost her blue (1)___ on the bus to town. Inside '
                                'there was a purse, keys and a small notebook. She (2)___ it to '
                                'the driver at the next stop. The (3)___ was bright blue with a '
                                'yellow zip. A passenger found it under a seat and gave it back. '
                                'Mia checked everything and smiled with relief. She (4)___ the '
                                'passenger and the driver many times. Then she wrote her phone '
                                'number on a paper inside it. Now Mia is more careful when she '
                                '(5)___ alone.',
                 'answers': ['bag', 'described', 'colour', 'thanked', 'travels'],
                 'word_bank': ['bag', 'described', 'colour', 'thanked', 'travels', 'wallet'],
                 'questions': [{'q': 'Where did Mia lose her bag?',
                                'accept': ['on the bus', 'bus', 'on the bus to town'],
                                'hint_ru': 'Где Миа потеряла сумку?',
                                'quote': '…lost her blue bag on the bus to town.',
                                'model_en': 'Mia lost her bag on the bus.'},
                               {'q': 'What colour was the bag?',
                                'accept': ['bright blue', 'blue', 'blue with a yellow zip'],
                                'hint_ru': 'Какого цвета была сумка?',
                                'quote': 'The colour was bright blue with a yellow zip.',
                                'model_en': 'The bag was bright blue with a yellow zip.'},
                               {'q': 'Who found the bag?',
                                'accept': ['a passenger', 'passenger'],
                                'hint_ru': 'Кто нашёл сумку?',
                                'quote': 'A passenger found it under a seat…',
                                'model_en': 'A passenger found the bag.'},
                               {'q': 'What did Mia write inside the bag?',
                                'accept': ['her phone number', 'phone number', 'a phone number'],
                                'hint_ru': 'Что Миа написала внутри сумки?',
                                'quote': '…wrote her phone number on a paper inside it.',
                                'model_en': 'Mia wrote her phone number inside the bag.'}],
                 'plan': ['Lost bag on the bus',
                          'Description to the driver',
                          'Passenger finds it',
                          'Thanks and phone number'],
                 'facts': ['Mia lost a blue bag on the bus.',
                           'She described the colour: bright blue with a yellow zip.',
                           'A passenger found it under a seat.',
                           'Mia thanked them and wrote her phone number inside.']},
        'restaurant': {'full_text': 'Anna and Paul chose a small Italian restaurant downtown for '
                                    'dinner. A server gave them a menu and a glass of water right '
                                    'away. Anna ordered pasta with tomato sauce, and Paul ordered '
                                    'fish. They shared a salad and talked about their busy week at '
                                    'work. The food arrived quickly and tasted fresh and hot. '
                                    'After dessert Paul asked for the bill and left a tip. The '
                                    'total was forty pounds including service. They thanked the '
                                    'waiter and promised to return soon. Outside it was raining, '
                                    'so they took a taxi home together.',
                       'gapped_text': 'Anna and Paul chose a small Italian restaurant downtown for '
                                      'dinner. A server gave them a (1)___ and a glass of water '
                                      'right away. Anna ordered pasta with tomato sauce, and Paul '
                                      'ordered fish. They shared a salad and talked about their '
                                      'busy week at work. The food arrived quickly and tasted '
                                      'fresh and hot. After dessert Paul asked for the (2)___ and '
                                      'left a (3)___. The total was forty pounds including '
                                      'service. They thanked the (4)___ and promised to return '
                                      'soon. Outside it was raining, so they took a (5)___ home '
                                      'together.',
                       'answers': ['menu', 'bill', 'tip', 'waiter', 'taxi'],
                       'word_bank': ['menu', 'bill', 'tip', 'waiter', 'taxi', 'kitchen'],
                       'questions': [{'q': 'What kind of restaurant did they choose?',
                                      'accept': ['Italian', 'small Italian', 'Italian restaurant'],
                                      'hint_ru': 'Какой ресторан они выбрали?',
                                      'quote': '…a small Italian restaurant downtown.',
                                      'model_en': 'They chose a small Italian restaurant.'},
                                     {'q': 'What did Anna order?',
                                      'accept': ['pasta', 'pasta with tomato sauce'],
                                      'hint_ru': 'Что заказала Анна?',
                                      'quote': 'Anna ordered pasta with tomato sauce…',
                                      'model_en': 'Anna ordered pasta with tomato sauce.'},
                                     {'q': 'How much was the total bill?',
                                      'accept': ['forty pounds', '40 pounds', 'forty'],
                                      'hint_ru': 'Сколько составил счёт?',
                                      'quote': 'The total was forty pounds including service.',
                                      'model_en': 'The total was forty pounds.'},
                                     {'q': 'How did they go home?',
                                      'accept': ['by taxi', 'taxi', 'took a taxi'],
                                      'hint_ru': 'Как они добрались домой?',
                                      'quote': '…they took a taxi home.',
                                      'model_en': 'They took a taxi home.'}],
                       'plan': ['Choosing the restaurant and menu',
                                'Orders and salad',
                                'Bill and tip',
                                'Thanking the waiter and taxi home'],
                       'facts': ['They ate at a small Italian restaurant.',
                                 'Anna ordered pasta; Paul ordered fish.',
                                 'Paul asked for the bill and left a tip; total forty pounds.',
                                 'They thanked the waiter and took a taxi home.']},
        'city': {'full_text': 'Dana lives in a green city with wide streets and old bridges. Her '
                              'favourite place is the grassy central park near the river. On '
                              'Sundays she rides the bus to the museum with her sister. They look '
                              'at paintings and then drink coffee outside. In summer there are '
                              'open concerts in the main square. Dana also likes the market where '
                              'farmers sell fresh fruit. She can walk everywhere, so she rarely '
                              'needs a car. Tourists often ask her for directions to the medieval '
                              'castle. Dana is proud of her city because it feels safe and '
                              'friendly.',
                 'gapped_text': 'Dana lives in a green city with wide streets and old bridges. Her '
                                'favourite place is the grassy central (1)___ near the river. On '
                                'Sundays she rides the (2)___ to the (3)___ with her sister. They '
                                'look at paintings and then drink coffee outside. In summer there '
                                'are open concerts in the main square. Dana also likes the market '
                                'where farmers sell fresh fruit. She can walk everywhere, so she '
                                'rarely needs a car. Tourists often ask her for directions to the '
                                'medieval (4)___. Dana is proud of her city because it feels '
                                '(5)___ and friendly.',
                 'answers': ['park', 'bus', 'museum', 'castle', 'safe'],
                 'word_bank': ['park', 'bus', 'museum', 'castle', 'safe', 'airport'],
                 'questions': [{'q': "What is Dana's favourite place?",
                                'accept': ['the central park',
                                           'central park',
                                           'park near the river',
                                           'park'],
                                'hint_ru': 'Какое любимое место у Даны?',
                                'quote': 'Her favourite place is the grassy central park…',
                                'model_en': "Dana's favourite place is the central park."},
                               {'q': 'Where does she go by bus on Sundays?',
                                'accept': ['to the museum', 'museum', 'the museum'],
                                'hint_ru': 'Куда она ездит на автобусе по воскресеньям?',
                                'quote': '…rides the bus to the museum…',
                                'model_en': 'On Sundays she goes to the museum by bus.'},
                               {'q': 'What do farmers sell at the market?',
                                'accept': ['fresh fruit', 'fruit'],
                                'hint_ru': 'Что фермеры продают на рынке?',
                                'quote': '…farmers sell fresh fruit.',
                                'model_en': 'Farmers sell fresh fruit at the market.'},
                               {'q': 'Why is Dana proud of her city?',
                                'accept': ['safe and friendly',
                                           'it feels safe and friendly',
                                           'safe'],
                                'hint_ru': 'Почему Дана гордится своим городом?',
                                'quote': '…because it feels safe and friendly.',
                                'model_en': 'Dana is proud because her city feels safe and '
                                            'friendly.'}],
                 'plan': ['Favourite park by the river',
                          'Sunday bus to the museum',
                          'Concerts and market',
                          'Safe friendly city'],
                 'facts': ["Dana's favourite place is the central park near the river.",
                           'On Sundays she takes the bus to the museum.',
                           'There is a market with fresh fruit and summer concerts.',
                           'She is proud because the city feels safe and friendly.']}},
 'B1': {'interview': {'full_text': 'Last Thursday Kate had a job interview at a small design '
                                   'studio in the city centre. She prepared a short portfolio of '
                                   'three recent projects on a tablet. The manager asked about her '
                                   'design skills and how she handles deadlines. Kate explained '
                                   'that she can work flexible hours and learn quickly. They also '
                                   'discussed the start date and the monthly salary for the role. '
                                   'After forty minutes the manager offered her a trial week. Kate '
                                   'asked two questions about the team and remote work options. '
                                   'She left feeling nervous but hopeful about the role. On Monday '
                                   'she will send a thank-you email and wait for news.',
                      'gapped_text': 'Last Thursday Kate had a job (1)___ at a small design studio '
                                     'in the city centre. She prepared a short (2)___ of three '
                                     'recent projects on a tablet. The manager asked about her '
                                     'design (3)___ and how she handles deadlines. Kate explained '
                                     'that she can work flexible hours and learn quickly. They '
                                     'also discussed the (4)___ date and the monthly salary for '
                                     'the role. After forty minutes the manager offered her a '
                                     'trial week. Kate asked two questions about the team and '
                                     'remote work options. She left feeling nervous but hopeful '
                                     'about the role. On Monday she will send a thank-you email '
                                     'and wait for (5)___.',
                      'answers': ['interview', 'portfolio', 'skills', 'start', 'news'],
                      'word_bank': ['interview', 'portfolio', 'skills', 'start', 'news', 'uniform'],
                      'questions': [{'q': "Where was Kate's interview?",
                                     'accept': ['at a small design studio',
                                                'design studio',
                                                'a design studio'],
                                     'hint_ru': 'Где было собеседование у Кейт?',
                                     'quote': '…job interview at a small design studio.',
                                     'model_en': "Kate's interview was at a small design studio."},
                                    {'q': 'What did the manager ask about?',
                                     'accept': ['design skills and how she handles deadlines',
                                                'her design skills',
                                                'design skills',
                                                'skills',
                                                'deadlines'],
                                     'hint_ru': 'О чём спросил менеджер?',
                                     'quote': '…asked about her design skills and how she handles '
                                              'deadlines.',
                                     'model_en': 'The manager asked about her design skills and '
                                                 'deadlines.'},
                                    {'q': 'What did the manager offer after forty minutes?',
                                     'accept': ['a trial week', 'trial week'],
                                     'hint_ru': 'Что предложил менеджер через сорок минут?',
                                     'quote': '…offered her a trial week.',
                                     'model_en': 'The manager offered her a trial week.'},
                                    {'q': 'What will Kate send on Monday?',
                                     'accept': ['a thank-you email', 'thank-you email', 'email'],
                                     'hint_ru': 'Что Кейт отправит в понедельник?',
                                     'quote': '…send a thank-you email…',
                                     'model_en': 'Kate will send a thank-you email on Monday.'}],
                      'plan': ['Interview at the design studio',
                               'Portfolio, design skills and hours',
                               'Start date and trial week',
                               'Follow-up email on Monday'],
                      'facts': ['Kate interviewed at a small design studio on Thursday.',
                                'She showed a portfolio and talked about design skills, hours and '
                                'start date.',
                                'The manager offered a trial week.',
                                'On Monday she will send a thank-you email.']},
        'flatshare': {'full_text': 'Omar shares a two-room flat with two students near the '
                                   'university. They split the rent equally and keep a list of '
                                   'weekly chores. Omar cleans the kitchen on Mondays, and Rita '
                                   'takes out the rubbish. Their main rules are quiet after eleven '
                                   'and no overnight guests without a message first. Last month a '
                                   'friend stayed two nights and washed the bathroom after. When '
                                   'bills arrive, they pay online from a shared account. Sometimes '
                                   'they cook together and watch a film in the living room. Omar '
                                   'likes flatshare life because it is cheaper and less lonely. '
                                   'Next term they may invite a fourth person if the price rises.',
                      'gapped_text': 'Omar shares a two-room flat with two students near the '
                                     'university. They split the (1)___ equally and keep a list of '
                                     'weekly (2)___. Omar cleans the kitchen on Mondays, and Rita '
                                     'takes out the rubbish. Their main (3)___ are quiet after '
                                     'eleven and no overnight (4)___ without a message first. Last '
                                     'month a friend stayed two nights and washed the bathroom '
                                     'after. When bills arrive, they pay online from a shared '
                                     'account. Sometimes they cook together and watch a film in '
                                     'the living room. Omar likes flatshare life because it is '
                                     'cheaper and less lonely. Next term they may invite a fourth '
                                     'person if the price (5)___.',
                      'answers': ['rent', 'chores', 'rules', 'guests', 'rises'],
                      'word_bank': ['rent', 'chores', 'rules', 'guests', 'rises', 'landlord'],
                      'questions': [{'q': 'How do they split the rent?',
                                     'accept': ['equally',
                                                'split equally',
                                                'they split it equally'],
                                     'hint_ru': 'Как они делят аренду?',
                                     'quote': 'They split the rent equally…',
                                     'model_en': 'They split the rent equally.'},
                                    {'q': 'What does Omar clean on Mondays?',
                                     'accept': ['the kitchen', 'kitchen'],
                                     'hint_ru': 'Что Омар убирает по понедельникам?',
                                     'quote': 'Omar cleans the kitchen on Mondays…',
                                     'model_en': 'Omar cleans the kitchen on Mondays.'},
                                    {'q': 'What are the quiet hours?',
                                     'accept': ['after eleven', 'quiet after eleven', 'after 11'],
                                     'hint_ru': 'С какого времени нужна тишина?',
                                     'quote': '…quiet after eleven…',
                                     'model_en': 'They must be quiet after eleven.'},
                                    {'q': 'Why does Omar like flatshare life?',
                                     'accept': ['cheaper and less lonely',
                                                'it is cheaper and less lonely',
                                                'cheaper'],
                                     'hint_ru': 'Почему Омару нравится совместная аренда?',
                                     'quote': '…because it is cheaper and less lonely.',
                                     'model_en': 'Omar likes it because it is cheaper and less '
                                                 'lonely.'}],
                      'plan': ['Rent and weekly chores',
                               'House rules about noise and guests',
                               'Bills and shared cooking',
                               'Pros of flatshare life'],
                      'facts': ['Omar shares a flat; they split rent and chores.',
                                'Rules: quiet after eleven; guests need a message.',
                                'They pay bills from a shared account.',
                                'Omar likes it because it is cheaper and less lonely.']},
        'online': {'full_text': 'Last weekend Nina ordered running shoes from an online shop. She '
                                'chose a pair with a twenty-percent discount and free delivery. '
                                'The parcel arrived in three days, but one shoe was the wrong '
                                'size. Nina opened a return request and printed the label at home. '
                                'The company collected the box and sent a refund within a week. '
                                'Before buying again, she read a short review from other buyers. '
                                'This time she checked the size chart carefully and measured her '
                                'foot. Nina prefers online shopping when she needs a clear refund '
                                'policy. She still visits real stores for clothes she wants to try '
                                'on.',
                   'gapped_text': 'Last weekend Nina ordered running shoes from an online shop. '
                                  'She chose a pair with a twenty-percent (1)___ and free (2)___. '
                                  'The parcel arrived in three days, but one shoe was the wrong '
                                  'size. Nina opened a (3)___ request and printed the label at '
                                  'home. The company collected the box and sent a refund within a '
                                  'week. Before buying again, she read a short (4)___ from other '
                                  'buyers. This time she checked the size chart carefully and '
                                  'measured her foot. Nina prefers online shopping when she needs '
                                  'a clear refund policy. She still visits real stores for clothes '
                                  'she wants to (5)___ on.',
                   'answers': ['discount', 'delivery', 'return', 'review', 'try'],
                   'word_bank': ['discount', 'delivery', 'return', 'review', 'try', 'auction'],
                   'questions': [{'q': 'What did Nina order online?',
                                  'accept': ['running shoes', 'shoes'],
                                  'hint_ru': 'Что Нина заказала онлайн?',
                                  'quote': '…ordered running shoes from an online shop.',
                                  'model_en': 'Nina ordered running shoes online.'},
                                 {'q': 'What was wrong with the first order?',
                                  'accept': ['wrong size',
                                             'one shoe was the wrong size',
                                             'the wrong size'],
                                  'hint_ru': 'Что было не так с первым заказом?',
                                  'quote': '…one shoe was the wrong size.',
                                  'model_en': 'One shoe was the wrong size.'},
                                 {'q': 'How long did the refund take?',
                                  'accept': ['within a week', 'a week', 'one week'],
                                  'hint_ru': 'Сколько ждали возврат денег?',
                                  'quote': '…sent a refund within a week.',
                                  'model_en': 'The refund arrived within a week.'},
                                 {'q': 'When does Nina prefer online shopping?',
                                  'accept': ['when she needs a clear refund policy',
                                             'clear refund policy',
                                             'refund policy',
                                             'clear return policy',
                                             'return policy'],
                                  'hint_ru': 'Когда Нина предпочитает онлайн-покупки?',
                                  'quote': '…when she needs a clear refund policy.',
                                  'model_en': 'She prefers online shopping with a clear refund '
                                              'policy.'}],
                   'plan': ['Discount order and delivery',
                            'Wrong size and return',
                            'Refund and reading a review',
                            'Careful second attempt'],
                   'facts': ['Nina ordered shoes with a discount and free delivery.',
                             'One shoe was the wrong size, so she opened a return.',
                             'She got a refund within a week and read a review.',
                             'She likes clear refund policies for online shopping.']},
        'volunteer': {'full_text': 'Every weekend Ivan volunteers at a local food bank near the '
                                   'station. His team sorts donations and packs bags for families '
                                   'in need. Last Saturday they helped at a charity event in the '
                                   'town hall. Ivan welcomed visitors, explained the project and '
                                   'collected forms. The organiser said teamwork matters more than '
                                   'perfect English. After three hours they cleaned the tables and '
                                   'locked the doors carefully. Ivan feels useful because he meets '
                                   'neighbours and learns new skills. Next month the group will '
                                   'plant trees in the park by the river. He hopes more students '
                                   'will join the volunteer group this autumn.',
                      'gapped_text': 'Every (1)___ Ivan volunteers at a local food bank near the '
                                     'station. His (2)___ sorts donations and packs bags for '
                                     'families in need. Last Saturday they helped at a charity '
                                     '(3)___ in the town hall. Ivan welcomed visitors, explained '
                                     'the project and collected forms. The organiser said teamwork '
                                     'matters more than perfect English. After three hours they '
                                     'cleaned the tables and locked the doors carefully. Ivan '
                                     'feels useful because he meets neighbours and learns new '
                                     'skills. Next month the group will plant trees in the park by '
                                     'the river. He hopes more students will (4)___ the volunteer '
                                     'group this (5)___.',
                      'answers': ['weekend', 'team', 'event', 'join', 'autumn'],
                      'word_bank': ['weekend', 'team', 'event', 'join', 'autumn', 'salary'],
                      'questions': [{'q': 'Where does Ivan volunteer?',
                                     'accept': ['at a local food bank',
                                                'food bank',
                                                'local food bank near the station'],
                                     'hint_ru': 'Где Иван волонтёрит?',
                                     'quote': '…volunteers at a local food bank near the station.',
                                     'model_en': 'Ivan volunteers at a local food bank.'},
                                    {'q': 'What did they do at the town hall?',
                                     'accept': ['helped at a charity event',
                                                'charity event',
                                                'a charity event'],
                                     'hint_ru': 'Что они делали в ратуше?',
                                     'quote': '…helped at a charity event in the town hall.',
                                     'model_en': 'They helped at a charity event in the town '
                                                 'hall.'},
                                    {'q': 'What will the group do next month?',
                                     'accept': ['plant trees in the park',
                                                'plant trees',
                                                'plant trees by the river'],
                                     'hint_ru': 'Что группа сделает в следующем месяце?',
                                     'quote': '…will plant trees in the park by the river.',
                                     'model_en': 'Next month they will plant trees in the park.'},
                                    {'q': 'Why does Ivan feel useful?',
                                     'accept': ['meets neighbours and learns new skills',
                                                'he meets neighbours',
                                                'learns new skills'],
                                     'hint_ru': 'Почему Иван чувствует себя полезным?',
                                     'quote': '…meets neighbours and learns new skills.',
                                     'model_en': 'He feels useful because he meets neighbours and '
                                                 'learns skills.'}],
                      'plan': ['Weekend work at the food bank',
                               'Charity event in the town hall',
                               'Teamwork and cleaning up',
                               'Tree planting and new members'],
                      'facts': ['Ivan volunteers every weekend at a food bank.',
                                'His team helped at a charity event last Saturday.',
                                'He feels useful meeting neighbours and learning skills.',
                                'Next month they will plant trees; he hopes students join.']},
        'exam': {'full_text': 'Helen is preparing for an important English exam in June at her '
                              'language school. She made a study plan with short goals for each '
                              'week of revision. To reduce stress she walks before revision and '
                              'drinks less coffee. Most afternoons she works in the library '
                              'because it is quiet. Her teacher checked practice papers and gave '
                              'clear feedback on mistakes. Helen still worries about listening, so '
                              'she trains with podcasts. On the morning of the test she arrived '
                              'early and read the rules. Two weeks later the results arrived by '
                              'email: she passed with a B. Helen says good planning helped more '
                              'than last-minute studying.',
                 'gapped_text': 'Helen is preparing for an important English (1)___ in June at her '
                                'language school. She made a study (2)___ with short goals for '
                                'each week of revision. To reduce (3)___ she walks before revision '
                                'and drinks less coffee. Most afternoons she works in the (4)___ '
                                'because it is quiet. Her teacher checked practice papers and gave '
                                'clear feedback on mistakes. Helen still worries about listening, '
                                'so she trains with podcasts. On the morning of the test she '
                                'arrived early and read the rules. Two weeks later the (5)___ '
                                'arrived by email: she passed with a B. Helen says good planning '
                                'helped more than last-minute studying.',
                 'answers': ['exam', 'plan', 'stress', 'library', 'results'],
                 'word_bank': ['exam', 'plan', 'stress', 'library', 'results', 'holiday'],
                 'questions': [{'q': "When is Helen's English exam?",
                                'accept': ['in June', 'June'],
                                'hint_ru': 'Когда у Хелен экзамен по английскому?',
                                'quote': '…English exam in June.',
                                'model_en': "Helen's English exam is in June."},
                               {'q': 'Where does she study most afternoons?',
                                'accept': ['in the library', 'library', 'the library'],
                                'hint_ru': 'Где она занимается почти каждый день после обеда?',
                                'quote': '…works in the library because it is quiet.',
                                'model_en': 'She studies in the library most afternoons.'},
                               {'q': 'How does she train for listening?',
                                'accept': ['with podcasts', 'podcasts', 'trains with podcasts'],
                                'hint_ru': 'Как она тренирует аудирование?',
                                'quote': '…trains with podcasts.',
                                'model_en': 'She trains for listening with podcasts.'},
                               {'q': 'What were her exam results?',
                                'accept': ['passed with a B', 'a B', 'B', 'she passed with a B'],
                                'hint_ru': 'Какой был результат экзамена?',
                                'quote': '…she passed with a B.',
                                'model_en': 'Helen passed with a B.'}],
                 'plan': ['Study plan and stress control',
                          'Library practice and feedback',
                          'Listening with podcasts',
                          'Exam day and results'],
                 'facts': ['Helen prepared for a June English exam with a study plan.',
                           'She reduced stress and worked in the library.',
                           'She trained listening with podcasts.',
                           'Results came by email: she passed with a B.']},
        'move': {'full_text': 'In March Alex moved to a new flat across the river with help from '
                              'friends. Friends helped him carry heavy boxes up three floors '
                              'without a lift. The neighbours brought tea and offered spare '
                              'shelves for his books. Alex likes the new area because shops and a '
                              'tram stop are close. The rent is higher, but the rooms get more '
                              'daylight in the morning. He spent the first weekend unpacking '
                              'clothes and books carefully. On Monday he registered his address at '
                              'the local office. Moving was tiring, yet he already feels at home '
                              'in the new place. Next Saturday he will invite old friends to a '
                              'small housewarming.',
                 'gapped_text': 'In March Alex moved to a new flat across the river with help from '
                                'friends. Friends helped him carry heavy (1)___ up three floors '
                                'without a lift. The (2)___ brought tea and offered spare shelves '
                                'for his books. Alex likes the new (3)___ because shops and a tram '
                                'stop are close. The (4)___ is higher, but the rooms get more '
                                'daylight in the morning. He spent the first weekend unpacking '
                                'clothes and books carefully. On Monday he registered his address '
                                'at the local office. Moving was tiring, yet he already feels at '
                                'home in the new place. Next Saturday he will invite old friends '
                                'to a small (5)___.',
                 'answers': ['boxes', 'neighbours', 'area', 'rent', 'housewarming'],
                 'word_bank': ['boxes', 'neighbours', 'area', 'rent', 'housewarming', 'elevator'],
                 'questions': [{'q': 'When did Alex move?',
                                'accept': ['in March', 'March'],
                                'hint_ru': 'Когда Алекс переехал?',
                                'quote': 'In March Alex moved to a new flat…',
                                'model_en': 'Alex moved in March.'},
                               {'q': 'Why does he like the new area?',
                                'accept': ['shops and a tram stop are close',
                                           'shops are close',
                                           'tram stop are close',
                                           'close shops and tram'],
                                'hint_ru': 'Почему ему нравится новый район?',
                                'quote': '…shops and a tram stop are close.',
                                'model_en': 'He likes it because shops and a tram stop are close.'},
                               {'q': 'What is different about the rent?',
                                'accept': ['higher', 'the rent is higher', 'rent is higher'],
                                'hint_ru': 'Что изменилось с арендой?',
                                'quote': 'The rent is higher…',
                                'model_en': 'The rent is higher.'},
                               {'q': 'What will he do next Saturday?',
                                'accept': ['invite old friends to a housewarming',
                                           'housewarming',
                                           'invite friends'],
                                'hint_ru': 'Что он сделает в следующую субботу?',
                                'quote': '…invite old friends to a small housewarming.',
                                'model_en': 'Next Saturday he will invite friends to a '
                                            'housewarming.'}],
                 'plan': ['Moving with boxes and neighbours',
                          'New area and higher rent',
                          'Unpacking and registration',
                          'Housewarming plans'],
                 'facts': ['Alex moved in March; friends carried heavy boxes.',
                           'Neighbours brought tea; he likes the new area.',
                           'Rent is higher but rooms get more daylight.',
                           'He will host a housewarming next Saturday.']},
        'travel_b1': {'full_text': 'Chris flew to Lisbon for a four-day city break in May. His '
                                   'flight left two hours late because of a storm at the airport. '
                                   'He used the delay to message the hotel and change the check-in '
                                   'time. At midnight a shuttle finally took tired passengers to '
                                   'the city. The receptionist was kind and upgraded him to a '
                                   'quieter room. Next morning Chris explored tram lines and a '
                                   'viewpoint above the river. He advises travellers to pack a '
                                   'book and download offline maps. Despite the late departure, '
                                   'the trip taught him to stay calm and flexible. He already '
                                   'plans a longer holiday there next spring.',
                      'gapped_text': 'Chris flew to Lisbon for a four-day city break in May. His '
                                     '(1)___ left two hours late because of a storm at the '
                                     'airport. He used the (2)___ to message the (3)___ and change '
                                     'the check-in time. At midnight a shuttle finally took tired '
                                     'passengers to the city. The receptionist was kind and '
                                     'upgraded him to a quieter room. Next morning Chris explored '
                                     'tram lines and a viewpoint above the river. He advises '
                                     'travellers to pack a book and download offline maps. Despite '
                                     'the late departure, the trip taught him to stay calm and '
                                     'flexible. He already plans a longer (4)___ there next '
                                     '(5)___.',
                      'answers': ['flight', 'delay', 'hotel', 'holiday', 'spring'],
                      'word_bank': ['flight', 'delay', 'hotel', 'holiday', 'spring', 'passport'],
                      'questions': [{'q': "Why was Chris's flight late?",
                                     'accept': ['because of a storm',
                                                'storm at the airport',
                                                'a storm',
                                                'storm'],
                                     'hint_ru': 'Почему рейс Криса задержался?',
                                     'quote': '…late because of a storm at the airport.',
                                     'model_en': 'The flight was late because of a storm at the '
                                                 'airport.'},
                                    {'q': 'What did he do during the delay?',
                                     'accept': ['message the hotel and change the check-in time',
                                                'messaged the hotel',
                                                'change the check-in time'],
                                     'hint_ru': 'Что он сделал во время задержки?',
                                     'quote': '…message the hotel and change the check-in time.',
                                     'model_en': 'He messaged the hotel and changed the check-in '
                                                 'time.'},
                                    {'q': 'What upgrade did the receptionist give?',
                                     'accept': ['a quieter room', 'quieter room', 'quiet room'],
                                     'hint_ru': 'Какой апгрейд сделала администратор?',
                                     'quote': '…upgraded him to a quieter room.',
                                     'model_en': 'The receptionist upgraded him to a quieter '
                                                 'room.'},
                                    {'q': 'What advice does Chris give travellers?',
                                     'accept': ['pack a book and download offline maps',
                                                'pack a book',
                                                'download offline maps',
                                                'offline maps'],
                                     'hint_ru': 'Какой совет даёт Крис путешественникам?',
                                     'quote': '…pack a book and download offline maps.',
                                     'model_en': 'He advises packing a book and downloading '
                                                 'offline maps.'}],
                      'plan': ['Delayed flight to Lisbon',
                               'Hotel message and late shuttle',
                               'Quieter room and city exploration',
                               'Advice and future holiday plans'],
                      'facts': ["Chris's flight to Lisbon was delayed by a storm.",
                                'He messaged the hotel during the delay.',
                                'The receptionist gave him a quieter room.',
                                'He advises books and offline maps; plans another holiday.']},
        'hobby_club': {'full_text': 'Rita joined a photography hobby club that meets every '
                                    'Wednesday evening. There are twelve members, from beginners '
                                    'to people with real cameras. At each meeting they share '
                                    'photos and choose a small weekly project. Last month their '
                                    'work was night lights in the old town centre. Rita learned to '
                                    'use manual settings and edit colours carefully. The club also '
                                    'organises short trips when the weather is clear. New people '
                                    'can join after a free trial evening and a short chat. Rita '
                                    'says the group is patient and gives honest feedback. She '
                                    'wants to show her best pictures at the spring exhibition.',
                       'gapped_text': 'Rita joined a photography hobby club that meets every '
                                      'Wednesday evening. There are twelve (1)___, from beginners '
                                      'to people with real cameras. At each (2)___ they share '
                                      'photos and choose a small weekly (3)___. Last month their '
                                      'work was night lights in the old town centre. Rita learned '
                                      'to use manual settings and edit colours carefully. The club '
                                      'also organises short trips when the weather is clear. New '
                                      'people can (4)___ after a free trial evening and a short '
                                      'chat. Rita says the group is patient and gives honest '
                                      'feedback. She wants to show her best pictures at the spring '
                                      '(5)___.',
                       'answers': ['members', 'meeting', 'project', 'join', 'exhibition'],
                       'word_bank': ['members',
                                     'meeting',
                                     'project',
                                     'join',
                                     'exhibition',
                                     'ticket'],
                       'questions': [{'q': 'How often does the club meet?',
                                      'accept': ['every Wednesday', 'Wednesday', 'on Wednesday'],
                                      'hint_ru': 'Как часто встречается клуб?',
                                      'quote': '…meets every Wednesday.',
                                      'model_en': 'The club meets every Wednesday.'},
                                     {'q': 'How many members are there?',
                                      'accept': ['twelve', '12', 'twelve members'],
                                      'hint_ru': 'Сколько участников в клубе?',
                                      'quote': 'There are twelve members…',
                                      'model_en': 'There are twelve members.'},
                                     {'q': "What was last month's project?",
                                      'accept': ['night lights in the old town',
                                                 'night lights',
                                                 'lights in the old town'],
                                      'hint_ru': 'Какой был проект в прошлом месяце?',
                                      'quote': '…their work was night lights in the old town '
                                               'centre.',
                                      'model_en': 'Last month their work was night lights in the '
                                                  'old town centre.'},
                                     {'q': 'How can new people join?',
                                      'accept': ['after a free trial evening and a short chat',
                                                 'free trial evening',
                                                 'after a free trial'],
                                      'hint_ru': 'Как новые люди могут вступить?',
                                      'quote': '…join after a free trial evening and a short chat.',
                                      'model_en': 'New people can join after a free trial evening '
                                                  'and a short chat.'}],
                       'plan': ['Club members and Wednesday meetings',
                                'Weekly projects and learning',
                                'Trips and how to join',
                                'Feedback and spring exhibition'],
                       'facts': ["Rita's photography club meets every Wednesday.",
                                 'There are twelve members with weekly projects.',
                                 'New people join after a free trial evening.',
                                 'Rita wants to show pictures at the spring exhibition.']}},
 'B2': {'business': {'full_text': "Elena led Thursday's client call from the Berlin office while "
                                  'two colleagues joined by remote work from Lisbon. The proposal '
                                  'for a logistics dashboard had to reach the client before '
                                  "Friday's deadline, so she opened with the delivery timeline and "
                                  'risk list. Two clients asked for clearer pricing and a pilot '
                                  'week in March. Elena noted every objection in the shared sheet '
                                  'and assigned owners for each follow-up. After the call she '
                                  'rewrote the executive summary, cut three weak slides, and sent '
                                  'the revised deck by six. The team agreed that working from afar '
                                  'saved travel time, yet the Friday cutoff still required one '
                                  'late evening. By Friday noon the client approved the pilot week '
                                  'and asked for a signed statement of work next week.',
                     'gapped_text': "Elena led Thursday's client call from the Berlin office while "
                                    'two colleagues joined by (1)___ from Lisbon. The document for '
                                    "a logistics dashboard had to reach the client before Friday's "
                                    '(2)___, so she opened with the delivery timeline and risk '
                                    'list. Two (3)___ asked for clearer pricing and a trial week '
                                    'in March. Elena noted every objection in the shared sheet and '
                                    'assigned owners for each follow-up. After the call she '
                                    'rewrote the executive summary, cut three weak slides, and '
                                    'sent the revised (4)___ by six. The team agreed that working '
                                    'from afar saved travel time, yet the Friday cutoff still '
                                    'required one late evening. By Friday noon the client approved '
                                    'the (5)___ week and asked for a signed statement of work next '
                                    'week.',
                     'answers': ['remote work', 'deadline', 'clients', 'proposal', 'pilot'],
                     'word_bank': ['remote work',
                                   'deadline',
                                   'clients',
                                   'proposal',
                                   'pilot',
                                   'invoice'],
                     'questions': [{'q': "Where were Elena's two colleagues during the call?",
                                    'accept': ['Lisbon', 'in Lisbon', 'remote from Lisbon'],
                                    'hint_ru': 'Откуда подключались коллеги?',
                                    'quote': '…joined by remote work from Lisbon.',
                                    'model_en': 'They joined by remote work from Lisbon.'},
                                   {'q': 'When did the proposal have to reach the client?',
                                    'accept': ["before Friday's deadline",
                                               'Friday',
                                               'before Friday'],
                                    'hint_ru': 'К какому сроку нужен был proposal?',
                                    'quote': "…before Friday's deadline…",
                                    'model_en': "It had to reach the client before Friday's "
                                                'deadline.'},
                                   {'q': 'What did the clients ask for besides clearer pricing?',
                                    'accept': ['a pilot week in March',
                                               'pilot week',
                                               'March',
                                               'a trial week in March'],
                                    'hint_ru': 'Что ещё попросили клиенты?',
                                    'quote': '…a pilot week in March.',
                                    'model_en': 'They asked for a pilot week in March.'},
                                   {'q': 'What did the client approve by Friday noon?',
                                    'accept': ['the pilot',
                                               'pilot',
                                               'approved the pilot',
                                               'the pilot week',
                                               'pilot week'],
                                    'hint_ru': 'Что одобрил клиент?',
                                    'quote': '…the client approved the pilot week…',
                                    'model_en': 'The client approved the pilot week.'}],
                     'plan': ['Client call setup and remote colleagues',
                              'Deadline pressure and client requests',
                              'Rewriting and sending the proposal',
                              'Pilot approval and next step'],
                     'facts': ['Elena led the call from Berlin; colleagues joined from Lisbon.',
                               "The proposal had to arrive before Friday's deadline.",
                               'Clients wanted clearer pricing and a March pilot week.',
                               'By Friday noon the client approved the pilot week.']},
        'startup': {'full_text': "Maya's team spent Monday refining a meal-planning product for "
                                 'busy parents. Early users liked the shopping list, but churn '
                                 'rose after week two, so the founders tracked which screens '
                                 'people abandoned. For the investor pitch they kept one clear '
                                 'problem slide and a demo of the weekly menu builder. Funding '
                                 'talks with a seed fund hinged on proving repeat orders, not '
                                 'vanity downloads. Maya cut the feature list, added a short '
                                 'onboarding quiz, and invited twenty unpaid testers to a feedback '
                                 'call. After that presentation the partners offered a soft '
                                 'commitment if the next cohort hit a sixty-percent retention '
                                 'target. The team left the room tired but focused on that single '
                                 'metric.',
                    'gapped_text': "Maya's team spent Monday refining a meal-planning (1)___ for "
                                   'busy parents. Early (2)___ liked the shopping list, but churn '
                                   'rose after week two, so the founders tracked which screens '
                                   'people abandoned. For the investor (3)___ they kept one clear '
                                   'problem slide and a demo of the weekly menu builder. (4)___ '
                                   'talks with a seed fund hinged on proving repeat orders, not '
                                   'vanity downloads. Maya cut the feature list, added a short '
                                   'onboarding quiz, and invited twenty unpaid testers to a '
                                   'feedback call. After that presentation the partners offered a '
                                   'soft commitment if the next cohort hit a sixty-percent (5)___ '
                                   'target. The team left the room tired but focused on that '
                                   'single metric.',
                    'answers': ['product', 'users', 'pitch', 'Funding', 'retention'],
                    'word_bank': ['product', 'users', 'pitch', 'Funding', 'retention', 'warehouse'],
                    'questions': [{'q': 'Who is the meal-planning product for?',
                                   'accept': ['busy parents', 'parents'],
                                   'hint_ru': 'Для кого продукт?',
                                   'quote': '…product for busy parents.',
                                   'model_en': 'It is for busy parents.'},
                                  {'q': 'What problem rose after week two?',
                                   'accept': ['churn', 'churn rose', 'users left'],
                                   'hint_ru': 'Что выросло после второй недели?',
                                   'quote': '…churn rose after week two…',
                                   'model_en': 'Churn rose after week two.'},
                                  {'q': 'What did funding talks depend on proving?',
                                   'accept': ['repeat orders', 'not vanity downloads', 'orders'],
                                   'hint_ru': 'Что нужно было доказать инвесторам?',
                                   'quote': '…proving repeat orders, not vanity downloads.',
                                   'model_en': 'They had to prove repeat orders, not vanity '
                                               'downloads.'},
                                  {'q': 'What retention target did partners require?',
                                   'accept': ['sixty-percent',
                                              '60%',
                                              'sixty percent',
                                              'sixty-percent retention'],
                                   'hint_ru': 'Какой целевой retention?',
                                   'quote': '…sixty-percent retention target.',
                                   'model_en': 'They required a sixty-percent retention target.'}],
                    'plan': ['Product and early-user problem',
                             'Pitch focus and funding condition',
                             'Product cuts and feedback calls',
                             'Soft commitment and retention goal'],
                    'facts': ['The product helps busy parents plan meals.',
                              'Churn rose after week two despite liking the shopping list.',
                              'Funding hinged on repeat orders, not downloads.',
                              'Partners offered a soft commitment if retention hit sixty '
                              'percent.']},
        'remote': {'full_text': 'After six months of working from home, Jonas still struggled with '
                                'afternoon focus. His calendar filled with back-to-back meetings, '
                                'so deep work slipped to late evenings and his sleep suffered. The '
                                'company introduced two office days each week and protected '
                                'Wednesday mornings as meeting-free. Jonas tested a simple '
                                'priority rule: camera on for decisions, async notes for updates. '
                                'He also moved the desk away from the kitchen and set a hard stop '
                                'at six. Within a month his deep-work blocks lengthened, and he '
                                'used on-site days for brainstorming while keeping quiet writing '
                                'at home. The change did not remove calendar clutter, but it '
                                'restored a workable balance.',
                   'gapped_text': 'After six months of working from home, Jonas still struggled '
                                  'with afternoon (1)___. His calendar filled with back-to-back '
                                  '(2)___, so deep work slipped to late evenings and his sleep '
                                  'suffered. The company introduced two (3)___ each week and '
                                  'protected Wednesday mornings as meeting-free. Jonas tested a '
                                  'simple (4)___ rule: camera on for decisions, async notes for '
                                  'updates. He also moved the desk away from the kitchen and set a '
                                  'hard stop at six. Within a month his deep-work blocks '
                                  'lengthened, and he used on-site days for brainstorming while '
                                  'keeping quiet writing at home. The change did not remove '
                                  'calendar clutter, but it restored a workable (5)___.',
                   'answers': ['focus', 'meetings', 'office days', 'priority', 'balance'],
                   'word_bank': ['focus',
                                 'meetings',
                                 'office days',
                                 'priority',
                                 'balance',
                                 'overtime'],
                   'questions': [{'q': 'What did Jonas struggle with in the afternoon?',
                                  'accept': ['focus', 'afternoon focus'],
                                  'hint_ru': 'С чем были проблемы днём?',
                                  'quote': '…struggled with afternoon focus.',
                                  'model_en': 'He struggled with afternoon focus.'},
                                 {'q': 'How many office days did the company introduce each week?',
                                  'accept': ['two', 'two office days', '2'],
                                  'hint_ru': 'Сколько офисных дней ввели?',
                                  'quote': '…two office days each week…',
                                  'model_en': 'The company introduced two office days each week.'},
                                 {'q': 'Which morning was protected as meeting-free?',
                                  'accept': ['Wednesday', 'Wednesday mornings'],
                                  'hint_ru': 'Какое утро без встреч?',
                                  'quote': '…Wednesday mornings as meeting-free.',
                                  'model_en': 'Wednesday mornings were meeting-free.'},
                                 {'q': 'What did Jonas use office days for?',
                                  'accept': ['brainstorming', 'for brainstorming'],
                                  'hint_ru': 'Для чего офисные дни?',
                                  'quote': '…on-site days for brainstorming…',
                                  'model_en': 'He used on-site days for brainstorming.'}],
                   'plan': ['Focus problems at home',
                            'Meetings overload and new office policy',
                            'Balance rules and desk changes',
                            'Results after one month'],
                   'facts': ['Jonas struggled with afternoon focus after six months at home.',
                             'Back-to-back meetings pushed deep work into evenings.',
                             'The company added two office days and meeting-free Wednesdays.',
                             'He used on-site days for brainstorming and writing at home.']},
        'news': {'full_text': 'The local evening bulletin opened with a riverside park project '
                              'that would close two lanes for eight months. Locals flooded the '
                              'comments with mixed opinion: some wanted safer walking paths, '
                              'others feared longer bus rides to school. A councillor argued the '
                              'impact on shopkeepers near the bridge had been underestimated. '
                              'Reporters interviewed a café owner who already saw fewer lunch '
                              'customers and a cycling group that welcomed the plan. By Friday the '
                              'mayor promised a public Q&A and a temporary shuttle. The story '
                              'showed how one infrastructure scheme can split a neighbourhood '
                              'while still claiming to serve the same citizens. Readers shared the '
                              "article widely, turning a planning notice into the week's leading "
                              'local news.',
                 'gapped_text': 'The local evening bulletin opened with a riverside park (1)___ '
                                'that would close two lanes for eight months. Locals flooded the '
                                'comments with mixed (2)___: some wanted safer walking paths, '
                                'others feared longer bus rides to school. A councillor argued the '
                                '(3)___ on shopkeepers near the bridge had been underestimated. '
                                'Reporters interviewed a café owner who already saw fewer lunch '
                                'customers and a cycling group that welcomed the plan. By Friday '
                                'the mayor promised a public Q&A and a temporary shuttle. The '
                                'story showed how one infrastructure scheme can split a '
                                'neighbourhood while still claiming to serve the same (4)___. '
                                'Readers shared the article widely, turning a planning notice into '
                                "the week's leading local (5)___.",
                 'answers': ['project', 'opinion', 'impact', 'citizens', 'news'],
                 'word_bank': ['project', 'opinion', 'impact', 'citizens', 'news', 'election'],
                 'questions': [{'q': 'What would the riverside park project close for eight '
                                     'months?',
                                'accept': ['two lanes', 'lanes', 'two lanes for eight months'],
                                'hint_ru': 'Что закроют на восемь месяцев?',
                                'quote': '…close two lanes for eight months.',
                                'model_en': 'It would close two lanes for eight months.'},
                               {'q': 'Whose impact did a councillor say was underestimated?',
                                'accept': ['shopkeepers',
                                           'shopkeepers near the bridge',
                                           'on shopkeepers'],
                                'hint_ru': 'На ком недооценили влияние?',
                                'quote': '…impact on shopkeepers near the bridge…',
                                'model_en': 'The impact on shopkeepers near the bridge.'},
                               {'q': 'What did the mayor promise by Friday?',
                                'accept': ['a public Q&A and a temporary shuttle',
                                           'Q&A',
                                           'temporary shuttle'],
                                'hint_ru': 'Что пообещал мэр?',
                                'quote': '…a public Q&A and a temporary shuttle.',
                                'model_en': 'A public Q&A and a temporary shuttle.'},
                               {'q': 'Who welcomed the plan according to reporters?',
                                'accept': ['a cycling group', 'cycling group'],
                                'hint_ru': 'Кто приветствовал план?',
                                'quote': '…a cycling group that welcomed the plan.',
                                'model_en': 'A cycling group welcomed the plan.'}],
                 'plan': ['Park project and lane closures',
                          'Mixed citizen opinion',
                          'Shopkeeper impact and interviews',
                          "Mayor's response and wider reaction"],
                 'facts': ['A riverside park project would close two lanes for eight months.',
                           'Citizen opinion was mixed between safer paths and longer bus rides.',
                           'A councillor said shopkeeper impact was underestimated.',
                           'The mayor promised a Q&A and a temporary shuttle.']},
        'uni': {'full_text': 'Omar had twelve days left to finish a sociology essay on urban '
                             'loneliness. The module handbook demanded at least eight academic '
                             "sources, yet half of his notes came from blogs. His tutor's previous "
                             'feedback warned him to define terms early and avoid sweeping claims. '
                             'Omar booked a library desk, rebuilt the outline around three case '
                             'cities, and replaced weak links with journal articles. He still '
                             'feared the Friday deadline, so he drafted the conclusion first and '
                             'wrote the methods section overnight. On Thursday he uploaded a draft '
                             'for peer review and used the comments to tighten citations. The '
                             'final piece was shorter, but the references were stronger and last '
                             "term's advice finally shaped the structure.",
                'gapped_text': 'Omar had twelve days left to finish a sociology (1)___ on urban '
                               'loneliness. The module handbook demanded at least eight academic '
                               "(2)___, yet half of his notes came from blogs. His tutor's "
                               'previous (3)___ warned him to define terms early and avoid '
                               'sweeping claims. Omar booked a library desk, rebuilt the outline '
                               'around three case cities, and replaced weak links with journal '
                               'articles. He still feared the Friday (4)___, so he drafted the '
                               'conclusion first and wrote the methods section overnight. On '
                               'Thursday he uploaded a draft for peer review and used the comments '
                               'to tighten citations. The final piece was shorter, but the '
                               "references were stronger and last term's advice finally shaped the "
                               '(5)___.',
                'answers': ['essay', 'sources', 'feedback', 'deadline', 'structure'],
                'word_bank': ['essay', 'sources', 'feedback', 'deadline', 'structure', 'campus'],
                'questions': [{'q': "What was Omar's sociology essay about?",
                               'accept': ['urban loneliness', 'loneliness'],
                               'hint_ru': 'О чём эссе?',
                               'quote': '…essay on urban loneliness.',
                               'model_en': 'It was about urban loneliness.'},
                              {'q': 'How many academic sources did the handbook demand?',
                               'accept': ['at least eight', 'eight', '8'],
                               'hint_ru': 'Сколько академических источников требовали?',
                               'quote': '…at least eight academic sources…',
                               'model_en': 'At least eight academic sources.'},
                              {'q': 'When was the deadline?',
                               'accept': ['Friday', 'Friday deadline'],
                               'hint_ru': 'Какой был дедлайн?',
                               'quote': '…feared the Friday deadline…',
                               'model_en': 'The deadline was on Friday.'},
                              {'q': "What did last term's feedback finally shape?",
                               'accept': ['the structure', 'structure'],
                               'hint_ru': 'Что сформировал прошлый feedback?',
                               'quote': "…last term's advice finally shaped the structure.",
                               'model_en': 'It shaped the structure.'}],
                'plan': ['Essay topic and weak sources',
                         'Tutor feedback and library work',
                         'Deadline pressure and drafting order',
                         'Peer review and stronger final version'],
                'facts': ['Omar wrote a sociology essay on urban loneliness.',
                          'He needed at least eight academic sources.',
                          'Previous feedback told him to define terms early.',
                          "He feared Friday's deadline and used peer review on Thursday."]},
        'customer': {'full_text': 'A customer emailed support after a blender arrived with a '
                                  'cracked lid and no spare gasket in the box. The complaint '
                                  'listed two failed chat attempts and a demand for a full refund '
                                  'within three days. Mira, the agent on duty, opened with a clear '
                                  'apology and confirmed the order photo matched the damaged '
                                  'parcel. She offered either a replacement overnight or a '
                                  'repayment to the original card, plus a discount code for the '
                                  'next purchase. The customer chose repayment and asked that the '
                                  'warehouse check the packing process. Mira logged the solution, '
                                  'escalated the packaging note, and closed the ticket only after '
                                  'the payment reversal appeared. The exchange turned a sharp '
                                  'message into a documented packing overhaul.',
                     'gapped_text': 'A customer emailed support after a blender arrived with a '
                                    'cracked lid and no spare gasket in the box. The (1)___ listed '
                                    'two failed chat attempts and a demand for a full (2)___ '
                                    'within three days. Mira, the agent on duty, opened with a '
                                    'clear (3)___ and confirmed the order photo matched the '
                                    'damaged parcel. She offered either a replacement overnight or '
                                    'a repayment to the original card, plus a discount code for '
                                    'the next purchase. The customer chose repayment and asked '
                                    'that the warehouse check the packing process. Mira logged the '
                                    '(4)___, escalated the packaging note, and closed the ticket '
                                    'only after the payment reversal appeared. The exchange turned '
                                    'a sharp message into a documented packing (5)___.',
                     'answers': ['complaint', 'refund', 'apology', 'solution', 'overhaul'],
                     'word_bank': ['complaint',
                                   'refund',
                                   'apology',
                                   'solution',
                                   'overhaul',
                                   'loyalty'],
                     'questions': [{'q': 'What was wrong with the blender delivery?',
                                    'accept': ['cracked lid',
                                               'no spare gasket',
                                               'cracked lid and no spare gasket'],
                                    'hint_ru': 'Что было не так с доставкой?',
                                    'quote': '…cracked lid and no spare gasket…',
                                    'model_en': 'The lid was cracked and the spare gasket was '
                                                'missing.'},
                                   {'q': 'How soon did the customer want a full refund?',
                                    'accept': ['within three days', 'three days', '3 days'],
                                    'hint_ru': 'За сколько дней требовали refund?',
                                    'quote': '…full refund within three days.',
                                    'model_en': 'Within three days.'},
                                   {'q': 'What two options did Mira offer?',
                                    'accept': ['replacement overnight or a repayment',
                                               'replacement overnight or a refund',
                                               'replacement or refund',
                                               'replacement or repayment',
                                               'overnight replacement or refund'],
                                    'hint_ru': 'Какие варианты предложила Mira?',
                                    'quote': '…replacement overnight or a repayment…',
                                    'model_en': 'A replacement overnight or a repayment to the '
                                                'original card.'},
                                   {'q': 'Which option did the customer choose?',
                                    'accept': ['repayment',
                                               'the repayment',
                                               'the refund',
                                               'refund'],
                                    'hint_ru': 'Что выбрал клиент?',
                                    'quote': 'The customer chose repayment…',
                                    'model_en': 'The customer chose repayment.'}],
                     'plan': ['Damaged delivery and complaint',
                              'Apology and verification',
                              'Options offered',
                              'Repayment choice and packing overhaul'],
                     'facts': ['The blender arrived with a cracked lid and no spare gasket.',
                               'The complaint demanded a full refund within three days.',
                               'Mira opened with an apology and offered replacement or repayment.',
                               'The customer chose repayment; Mira logged the solution.']},
        'health': {'full_text': 'After a winter of late screens, Nadia rebuilt her healthy '
                                'lifestyle in small steps. She tracked three habits for thirty '
                                'days: a phone-free last hour, a ten-minute walk after lunch, and '
                                'water before coffee. Sleep improved once she fixed a consistent '
                                'bedtime, and her diet shifted from desk snacks to prepared '
                                'lunches twice a week. Motivation dipped in week two, so she '
                                'joined a Friday park group instead of relying on willpower alone. '
                                'A nurse friend reminded her that progress is uneven and that rest '
                                'days still count. By the end of the month Nadia slept longer, '
                                'skipped fewer breakfasts, and kept the walk even on busy days. '
                                'The experiment proved that boring routines beat dramatic '
                                'resolutions.',
                   'gapped_text': 'After a winter of late screens, Nadia rebuilt her healthy '
                                  'lifestyle in small steps. She tracked three (1)___ for thirty '
                                  'days: a phone-free last hour, a ten-minute walk after lunch, '
                                  'and water before coffee. (2)___ improved once she fixed a '
                                  'consistent bedtime, and her (3)___ shifted from desk snacks to '
                                  'prepared lunches twice a week. (4)___ dipped in week two, so '
                                  'she joined a Friday park group instead of relying on willpower '
                                  'alone. A nurse friend reminded her that progress is uneven and '
                                  'that rest days still count. By the end of the month Nadia slept '
                                  'longer, skipped fewer breakfasts, and kept the walk even on '
                                  'busy days. The experiment proved that boring routines beat '
                                  'dramatic (5)___.',
                   'answers': ['habits', 'Sleep', 'diet', 'Motivation', 'resolutions'],
                   'word_bank': ['habits', 'Sleep', 'diet', 'Motivation', 'resolutions', 'gym'],
                   'questions': [{'q': 'How long did Nadia track her three habits?',
                                  'accept': ['thirty days', '30 days', 'a month'],
                                  'hint_ru': 'Сколько дней она отслеживала привычки?',
                                  'quote': '…three habits for thirty days…',
                                  'model_en': 'For thirty days.'},
                                 {'q': 'What improved after she fixed a consistent bedtime?',
                                  'accept': ['Sleep', 'sleep'],
                                  'hint_ru': 'Что улучшилось после стабильного отбоя?',
                                  'quote': 'Sleep improved once she fixed a consistent bedtime…',
                                  'model_en': 'Sleep improved.'},
                                 {'q': 'When did motivation dip?',
                                  'accept': ['week two', 'in week two'],
                                  'hint_ru': 'Когда упала мотивация?',
                                  'quote': 'Motivation dipped in week two…',
                                  'model_en': 'Motivation dipped in week two.'},
                                 {'q': 'What did she join instead of relying on willpower alone?',
                                  'accept': ['a Friday park group',
                                             'Friday park group',
                                             'park group'],
                                  'hint_ru': 'К чему она присоединилась?',
                                  'quote': '…joined a Friday park group…',
                                  'model_en': 'She joined a Friday park group.'}],
                   'plan': ['Three tracked habits',
                            'Sleep and diet changes',
                            'Motivation dip and park group',
                            'Month-end results'],
                   'facts': ['Nadia tracked three habits for thirty days.',
                             'Sleep improved with a consistent bedtime; diet shifted to prepared '
                             'lunches.',
                             'Motivation dipped in week two, so she joined a Friday park group.',
                             "By month's end she slept longer and kept the walk on busy days."]},
        'culture': {'full_text': 'On Saturday Lena queued for an evening exhibition of Baltic '
                                 'photography at the city gallery. Tickets were timed entry, so '
                                 "she arrived twenty minutes early and read the curator's note on "
                                 'post-industrial light. Inside, the rooms stayed quiet; the '
                                 'atmosphere mixed cool concrete with warm amber lamps over large '
                                 'prints. Lena took no photos, only short notes for a review she '
                                 'owed her student magazine. A guide explained why one series used '
                                 'expired film, and visitors lingered longest at a harbour '
                                 'triptych. Afterward Lena wrote that the show avoided nostalgia '
                                 'and trusted empty space. Her editor kept her piece almost '
                                 'unchanged and printed it beside the weekend listings.',
                    'gapped_text': 'On Saturday Lena queued for an evening (1)___ of Baltic '
                                   'photography at the city gallery. (2)___ were timed entry, so '
                                   "she arrived twenty minutes early and read the curator's note "
                                   'on post-industrial light. Inside, the rooms stayed quiet; the '
                                   '(3)___ mixed cool concrete with warm amber lamps over large '
                                   'prints. Lena took no photos, only short notes for a (4)___ she '
                                   'owed her student magazine. A guide explained why one series '
                                   'used expired film, and visitors lingered longest at a harbour '
                                   'triptych. Afterward Lena wrote that the show avoided nostalgia '
                                   'and trusted empty space. Her editor kept her piece almost '
                                   'unchanged and printed it beside the weekend (5)___.',
                    'answers': ['exhibition', 'Tickets', 'atmosphere', 'review', 'listings'],
                    'word_bank': ['exhibition',
                                  'Tickets',
                                  'atmosphere',
                                  'review',
                                  'listings',
                                  'auction'],
                    'questions': [{'q': 'What kind of exhibition did Lena visit?',
                                   'accept': ['Baltic photography',
                                              'photography',
                                              'evening exhibition of Baltic photography'],
                                   'hint_ru': 'Какая была выставка?',
                                   'quote': '…exhibition of Baltic photography…',
                                   'model_en': 'An evening exhibition of Baltic photography.'},
                                  {'q': 'Why did she arrive twenty minutes early?',
                                   'accept': ['timed entry',
                                              'Tickets were timed entry',
                                              'timed tickets'],
                                   'hint_ru': 'Почему пришла заранее?',
                                   'quote': 'Tickets were timed entry…',
                                   'model_en': 'Because tickets were timed entry.'},
                                  {'q': 'Who was the review for?',
                                   'accept': ['her student magazine', 'student magazine'],
                                   'hint_ru': 'Для кого рецензия?',
                                   'quote': '…a review she owed her student magazine.',
                                   'model_en': 'For her student magazine.'},
                                  {'q': 'Where did visitors linger longest?',
                                   'accept': ['harbour triptych', 'at a harbour triptych'],
                                   'hint_ru': 'Где дольше всего задерживались посетители?',
                                   'quote': '…lingered longest at a harbour triptych.',
                                   'model_en': 'At a harbour triptych.'}],
                    'plan': ['Exhibition visit and timed tickets',
                             'Gallery atmosphere',
                             'Notes for a review',
                             'Published piece beside listings'],
                    'facts': ['Lena attended an evening Baltic photography exhibition.',
                              'Tickets were timed entry; she arrived early.',
                              'She wrote a review for her student magazine.',
                              'The editor printed the review beside weekend listings.']}},
 'C1': {'negotiation': {'full_text': 'Across a polished table in Rotterdam, two supply-chain teams '
                                     "bargained over a three-year logistics contract. The buyer's "
                                     'opening terms demanded price cuts that would erase the '
                                     "vendor's thin margin, while the vendor cited fuel volatility "
                                     'as leverage for a flexible surcharge clause. After two hours '
                                     'neither side moved, so the mediators reframed the deal '
                                     'around volume guarantees and shared risk. A narrow '
                                     'compromise emerged: a modest discount in year one, indexed '
                                     'rates thereafter, and penalties only if on-time delivery '
                                     'fell below ninety-four percent. Legal counsel redrafted the '
                                     'ambiguous force-majeure wording before anyone initialled the '
                                     'pages. Both parties left with less than they wanted, yet '
                                     'with an agreement they could defend internally—and with '
                                     'bargaining power reserved for the mid-term review.',
                        'gapped_text': 'Across a polished table in Rotterdam, two supply-chain '
                                       'teams bargained over a three-year logistics (1)___. The '
                                       "buyer's opening (2)___ demanded price cuts that would "
                                       "erase the vendor's thin margin, while the vendor cited "
                                       'fuel volatility as (3)___ for a flexible surcharge clause. '
                                       'After two hours neither side moved, so the mediators '
                                       'reframed the deal around volume guarantees and shared '
                                       'risk. A narrow (4)___ emerged: a modest discount in year '
                                       'one, indexed rates thereafter, and penalties only if '
                                       'on-time delivery fell below ninety-four percent. Legal '
                                       'counsel redrafted the ambiguous force-majeure wording '
                                       'before anyone initialled the pages. Both parties left with '
                                       'less than they wanted, yet with an agreement they could '
                                       'defend internally—and with bargaining power reserved for '
                                       'the mid-term (5)___.',
                        'answers': ['contract', 'terms', 'leverage', 'compromise', 'review'],
                        'word_bank': ['contract',
                                      'terms',
                                      'leverage',
                                      'compromise',
                                      'review',
                                      'warehouse'],
                        'questions': [{'q': 'Where did the negotiation take place?',
                                       'accept': ['Rotterdam', 'in Rotterdam'],
                                       'hint_ru': 'Где проходили переговоры?',
                                       'quote': '…table in Rotterdam…',
                                       'model_en': 'In Rotterdam.'},
                                      {'q': 'What did the vendor use as leverage?',
                                       'accept': ['fuel volatility', 'volatility'],
                                       'hint_ru': 'Что использовал vendor как leverage?',
                                       'quote': '…cited fuel volatility as leverage…',
                                       'model_en': 'Fuel volatility.'},
                                      {'q': 'Below what on-time delivery rate would penalties '
                                            'apply?',
                                       'accept': ['ninety-four percent', '94%', '94 percent'],
                                       'hint_ru': 'Ниже какого процента штрафы?',
                                       'quote': '…fell below ninety-four percent.',
                                       'model_en': 'Below ninety-four percent.'},
                                      {'q': 'What wording did legal counsel redraft?',
                                       'accept': ['force-majeure',
                                                  'force-majeure wording',
                                                  'ambiguous force-majeure wording'],
                                       'hint_ru': 'Какую формулировку переписали юристы?',
                                       'quote': '…ambiguous force-majeure wording…',
                                       'model_en': 'The ambiguous force-majeure wording.'}],
                        'plan': ['Contract stakes and opening terms',
                                 'Leverage and deadlock',
                                 'Compromise structure',
                                 'Legal redraft and reserved leverage'],
                        'facts': ['Teams negotiated a three-year logistics contract in Rotterdam.',
                                  'The vendor used fuel volatility as leverage for a surcharge '
                                  'clause.',
                                  'Compromise included year-one discount and indexed rates later.',
                                  'Penalties applied only below ninety-four percent on-time '
                                  'delivery.']},
        'media': {'full_text': 'A national outlet led Tuesday with a headline that framed a '
                               'hospital IT outage as deliberate sabotage, though early police '
                               'statements only confirmed a system failure. Critics accused the '
                               'desk of bias for elevating an unnamed blogger while burying quotes '
                               "from the hospital's own engineers. Editors later insisted they had "
                               'checked three independent sources, yet the timeline on the page '
                               "still omitted the vendor's maintenance window. Audience metrics "
                               'rewarded the dramatic framing: shares spiked before a correction '
                               'appeared under the fold. By evening a quieter update walked back '
                               'the sabotage claim, but the original banner lingered in '
                               'screenshots. The episode illustrated how speed, slant, and '
                               'incomplete citations can lock readers into a narrative that facts '
                               'later soften.',
                  'gapped_text': 'A national outlet led Tuesday with a (1)___ that framed a '
                                 'hospital IT outage as deliberate sabotage, though early police '
                                 'statements only confirmed a system failure. Critics accused the '
                                 'desk of (2)___ for elevating an unnamed blogger while burying '
                                 "quotes from the hospital's own engineers. Editors later insisted "
                                 'they had checked three independent (3)___, yet the timeline on '
                                 "the page still omitted the vendor's maintenance window. (4)___ "
                                 'metrics rewarded the dramatic framing: shares spiked before a '
                                 'correction appeared under the fold. By evening a quieter update '
                                 'walked back the sabotage claim, but the original banner lingered '
                                 'in screenshots. The episode illustrated how speed, slant, and '
                                 'incomplete citations can lock readers into a (5)___ that facts '
                                 'later soften.',
                  'answers': ['headline', 'bias', 'sources', 'Audience', 'narrative'],
                  'word_bank': ['headline', 'bias', 'sources', 'Audience', 'narrative', 'paywall'],
                  'questions': [{'q': 'How did the headline frame the hospital IT outage?',
                                 'accept': ['deliberate sabotage',
                                            'as deliberate sabotage',
                                            'sabotage'],
                                 'hint_ru': 'Как заголовок подал сбой?',
                                 'quote': '…framed a hospital IT outage as deliberate sabotage…',
                                 'model_en': 'As deliberate sabotage.'},
                                {'q': 'How many independent sources did editors claim to have '
                                      'checked?',
                                 'accept': ['three', '3', 'three independent sources'],
                                 'hint_ru': 'Сколько независимых источников?',
                                 'quote': '…checked three independent sources…',
                                 'model_en': 'Three independent sources.'},
                                {'q': 'What did the page timeline omit?',
                                 'accept': ["the vendor's maintenance window",
                                            'maintenance window'],
                                 'hint_ru': 'Что пропустила timeline?',
                                 'quote': "…omitted the vendor's maintenance window.",
                                 'model_en': "The vendor's maintenance window."},
                                {'q': 'What happened to the sabotage claim by evening?',
                                 'accept': ['walked back',
                                            'walked back the sabotage claim',
                                            'softened',
                                            'corrected'],
                                 'hint_ru': 'Что сделали с утверждением о саботаже к вечеру?',
                                 'quote': '…walked back the sabotage claim…',
                                 'model_en': 'A quieter update walked back the sabotage claim.'}],
                  'plan': ['Dramatic headline vs early facts',
                           'Bias accusation and sources claim',
                           'Audience metrics and correction',
                           'Lingering screenshots and lesson'],
                  'facts': ['A headline framed an IT outage as deliberate sabotage.',
                            'Critics alleged bias for elevating an unnamed blogger.',
                            'Editors claimed three independent sources; the timeline omitted a '
                            'maintenance window.',
                            'An evening update walked back the sabotage claim.']},
        'climate': {'full_text': "The city council's climate brief proposed a low-emission zone "
                                 'that would charge older vans entering the centre after next '
                                 'April. Officials framed the policy as public-health protection, '
                                 'yet small traders warned that compliance costs could close '
                                 'family shops. Community workshops produced maps of delivery '
                                 'routes and lists of balances: cleaner air against higher grocery '
                                 'prices, quieter streets against longer last-mile trips. A '
                                 'revised draft offered grants for electric vans and a phased map '
                                 'that spared the eastern market for eighteen months. Budget '
                                 'officers still questioned whether the outlays were fully scored. '
                                 'Residents left the hall divided, convinced that climate ambition '
                                 'without honest trade-offs would either stall or punish the least '
                                 'flexible firms.',
                    'gapped_text': "The city council's climate brief proposed a low-emission zone "
                                   'that would charge older vans entering the centre after next '
                                   'April. Officials framed the (1)___ as public-health '
                                   'protection, yet small traders warned that compliance (2)___ '
                                   'could close family shops. (3)___ workshops produced maps of '
                                   'delivery routes and lists of balances: cleaner air against '
                                   'higher grocery prices, quieter streets against longer '
                                   'last-mile trips. A revised draft offered grants for electric '
                                   'vans and a phased map that spared the eastern market for '
                                   'eighteen months. Budget officers still questioned whether the '
                                   'outlays were fully scored. Residents left the hall divided, '
                                   'convinced that climate ambition without honest (4)___ would '
                                   'either stall or punish the least flexible (5)___.',
                    'answers': ['policy', 'costs', 'Community', 'trade-offs', 'firms'],
                    'word_bank': ['policy',
                                  'costs',
                                  'Community',
                                  'trade-offs',
                                  'firms',
                                  'referendum'],
                    'questions': [{'q': 'When would older vans start being charged in the centre?',
                                   'accept': ['after next April', 'next April', 'April'],
                                   'hint_ru': 'С какого срока начнут брать плату?',
                                   'quote': '…after next April.',
                                   'model_en': 'After next April.'},
                                  {'q': 'What did small traders fear compliance costs could do?',
                                   'accept': ['close family shops', 'close shops'],
                                   'hint_ru': 'Чего боялись торговцы?',
                                   'quote': '…compliance costs could close family shops.',
                                   'model_en': 'Close family shops.'},
                                  {'q': 'How long would the eastern market be spared?',
                                   'accept': ['eighteen months', '18 months'],
                                   'hint_ru': 'На сколько месяцев отложили для восточного рынка?',
                                   'quote': '…spared the eastern market for eighteen months.',
                                   'model_en': 'For eighteen months.'},
                                  {'q': 'What did the revised draft offer for electric vans?',
                                   'accept': ['grants', 'grants for electric vans'],
                                   'hint_ru': 'Что предложили для электрофургонов?',
                                   'quote': '…grants for electric vans…',
                                   'model_en': 'Grants for electric vans.'}],
                    'plan': ['Low-emission policy proposal',
                             'Cost concerns from traders',
                             'Community trade-offs and revised draft',
                             'Budget doubts and divided residents'],
                    'facts': ['A low-emission zone would charge older vans after next April.',
                              'Traders warned compliance costs could close family shops.',
                              'Workshops listed trade-offs between cleaner air and higher prices.',
                              'The revised draft offered grants and spared the eastern market for '
                              'eighteen months.']},
        'hr': {'full_text': "During Helena's mid-year review, her manager opened with performance "
                            'data from two product launches and a customer-escalation week that '
                            'had tested the whole squad. Targets for delivery were met, yet soft '
                            'skills scores lagged: peers wanted clearer escalation paths and fewer '
                            'last-minute changes to shared documents. Helena asked bluntly about '
                            'promotion timing; the answer hinged on leading one cross-team project '
                            'and documenting mentoring goals for a junior hire. HR later '
                            'circulated a written plan with quarterly check-ins rather than vague '
                            'encouragement, plus a short course on facilitation. Helena left '
                            'frustrated but oriented—she knew which behaviours blocked advancement '
                            'and which outcomes would reopen the advancement conversation in '
                            'December if the coaching notes stayed green.',
               'gapped_text': "During Helena's mid-year review, her manager opened with (1)___ "
                              'data from two product launches and a customer-escalation week that '
                              'had tested the whole squad. Targets for delivery were met, yet '
                              '(2)___ scores lagged: peers wanted clearer escalation paths and '
                              'fewer last-minute changes to shared documents. Helena asked bluntly '
                              'about (3)___ timing; the answer hinged on leading one cross-team '
                              'project and documenting mentoring (4)___ for a junior hire. HR '
                              'later circulated a written plan with quarterly check-ins rather '
                              'than vague encouragement, plus a short course on facilitation. '
                              'Helena left frustrated but oriented—she knew which behaviours '
                              'blocked advancement and which outcomes would reopen the advancement '
                              'conversation in (5)___ if the coaching notes stayed green.',
               'answers': ['performance', 'soft skills', 'promotion', 'goals', 'December'],
               'word_bank': ['performance',
                             'soft skills',
                             'promotion',
                             'goals',
                             'December',
                             'severance'],
               'questions': [{'q': 'What performance data did the manager open with?',
                              'accept': ['two product launches and a customer-escalation week',
                                         'product launches',
                                         'customer-escalation week'],
                              'hint_ru': 'С каких данных начал менеджер?',
                              'quote': '…performance data from two product launches and a '
                                       'customer-escalation week.',
                              'model_en': 'Data from two product launches and a '
                                          'customer-escalation week.'},
                             {'q': 'Which scores lagged despite met delivery targets?',
                              'accept': ['soft skills', 'soft skills scores'],
                              'hint_ru': 'Какие оценки отставали?',
                              'quote': '…soft skills scores lagged…',
                              'model_en': 'Soft skills scores.'},
                             {'q': 'What two conditions hinged on for promotion timing?',
                              'accept': ['leading one cross-team project and documenting mentoring '
                                         'goals',
                                         'cross-team project and mentoring goals'],
                              'hint_ru': 'От чего зависел срок promotion?',
                              'quote': '…leading one cross-team project and documenting mentoring '
                                       'goals…',
                              'model_en': 'Leading a cross-team project and documenting mentoring '
                                          'goals.'},
                             {'q': 'When might the promotion conversation reopen?',
                              'accept': ['December', 'in December'],
                              'hint_ru': 'Когда снова обсудят promotion?',
                              'quote': '…advancement conversation in December…',
                              'model_en': 'In December.'}],
               'plan': ['Performance data presented',
                        'Soft-skills gap',
                        'Promotion conditions and mentoring goals',
                        'Written HR plan and December checkpoint'],
               'facts': ["Helena's delivery targets were met; soft skills scores lagged.",
                         'Peers wanted clearer escalation paths and fewer last-minute changes.',
                         'Promotion hinged on a cross-team project and mentoring goals.',
                         'HR issued a written plan; the next promotion talk was set for '
                         'December.']},
        'research': {'full_text': 'A university team summarised a twelve-month study of '
                                  'night-shift alertness among warehouse staff in three regional '
                                  'hubs. Their method combined wearable sleep trackers with '
                                  'fortnightly cognitive tests and anonymised incident logs from '
                                  'supervisors. Preliminary findings suggested that split rest '
                                  'breaks reduced near-miss reports more than caffeine stipends '
                                  'alone, though the sample excluded contractors. The authors '
                                  'listed clear limits: self-reported caffeine intake was '
                                  'unreliable, and winter darkness may have confounded fatigue '
                                  'scores across sites. Recommended next steps included a '
                                  'randomised schedule trial and partnership with occupational '
                                  'clinicians. Funders praised the cautious tone; managers asked '
                                  'for a one-page brief before changing rotas. The summary refused '
                                  'hype and treated uncertainty as part of the evidence, not a '
                                  'footnote to ignore.',
                     'gapped_text': 'A university team summarised a twelve-month study of '
                                    'night-shift alertness among warehouse staff in three regional '
                                    'hubs. Their (1)___ combined wearable sleep trackers with '
                                    'fortnightly cognitive tests and anonymised incident logs from '
                                    'supervisors. Preliminary (2)___ suggested that split rest '
                                    'breaks reduced near-miss reports more than caffeine stipends '
                                    'alone, though the sample excluded contractors. The authors '
                                    'listed clear (3)___: self-reported caffeine intake was '
                                    'unreliable, and winter darkness may have confounded fatigue '
                                    'scores across sites. Recommended (4)___ included a randomised '
                                    'schedule trial and partnership with occupational clinicians. '
                                    'Funders praised the cautious tone; managers asked for a '
                                    'one-page brief before changing rotas. The summary refused '
                                    'hype and treated uncertainty as part of the (5)___, not a '
                                    'footnote to ignore.',
                     'answers': ['method', 'findings', 'limits', 'next steps', 'evidence'],
                     'word_bank': ['method',
                                   'findings',
                                   'limits',
                                   'next steps',
                                   'evidence',
                                   'budget'],
                     'questions': [{'q': 'How long was the night-shift alertness study?',
                                    'accept': ['twelve-month', 'twelve months', '12 months'],
                                    'hint_ru': 'Сколько длилось исследование?',
                                    'quote': '…a twelve-month study…',
                                    'model_en': 'Twelve months.'},
                                   {'q': 'What reduced near-miss reports more than caffeine '
                                         'stipends alone?',
                                    'accept': ['split rest breaks', 'rest breaks'],
                                    'hint_ru': 'Что снизило near-miss сильнее кофеина?',
                                    'quote': '…split rest breaks reduced near-miss reports…',
                                    'model_en': 'Split rest breaks.'},
                                   {'q': 'Who was excluded from the sample?',
                                    'accept': ['contractors', 'the sample excluded contractors'],
                                    'hint_ru': 'Кого исключили из выборки?',
                                    'quote': '…the sample excluded contractors.',
                                    'model_en': 'Contractors were excluded.'},
                                   {'q': 'What next steps did the authors recommend?',
                                    'accept': ['a randomised schedule trial and partnership with '
                                               'occupational clinicians',
                                               'randomised schedule trial',
                                               'partnership with occupational clinicians'],
                                    'hint_ru': 'Какие next steps рекомендовали?',
                                    'quote': '…a randomised schedule trial and partnership with '
                                             'occupational clinicians.',
                                    'model_en': 'A randomised schedule trial and partnership with '
                                                'occupational clinicians.'}],
                     'plan': ['Study topic and method',
                              'Key findings and sample limit',
                              'Stated limits of the evidence',
                              'Next steps and reception'],
                     'facts': ['The study lasted twelve months and used trackers, tests, and '
                               'incident logs.',
                               'Split rest breaks outperformed caffeine stipends alone for '
                               'near-miss reduction.',
                               'Limits included unreliable caffeine self-reports and winter '
                               'darkness effects.',
                               'Next steps: randomised schedule trial and clinician partnership.']},
        'ethics': {'full_text': 'A consumer-tech advisory panel spent the afternoon dissecting a '
                                'voice-assistant update that stored ambient snippets by default in '
                                'several markets. Privacy advocates argued that opaque consent '
                                "screens failed ordinary people, while the company's counsel "
                                'insisted current regulation already required notice and an '
                                'opt-out. Engineers described how on-device AI could trim '
                                'retention windows, yet product managers feared accuracy losses if '
                                'cloud training shrank. The chair forced a practical vote: delay '
                                'the launch, publish a plain-language retention table, and '
                                'commission an external audit of deletion logs. Nobody claimed the '
                                'compromise solved deeper power imbalances, but it treated users '
                                'as stakeholders rather than telemetry streams. Minutes closed '
                                'with a warning that ethics after deployment is damage control, '
                                'not design.',
                   'gapped_text': 'A consumer-tech advisory panel spent the afternoon dissecting a '
                                  'voice-assistant update that stored ambient snippets by default '
                                  'in several markets. (1)___ advocates argued that opaque consent '
                                  "screens failed ordinary people, while the company's counsel "
                                  'insisted current (2)___ already required notice and an opt-out. '
                                  'Engineers described how on-device (3)___ could trim retention '
                                  'windows, yet product managers feared accuracy losses if cloud '
                                  'training shrank. The chair forced a practical vote: delay the '
                                  'launch, publish a plain-language retention table, and '
                                  'commission an external audit of deletion logs. Nobody claimed '
                                  'the compromise solved deeper power imbalances, but it treated '
                                  '(4)___ as stakeholders rather than telemetry streams. Minutes '
                                  'closed with a warning that (5)___ after deployment is damage '
                                  'control, not design.',
                   'answers': ['Privacy', 'regulation', 'AI', 'users', 'ethics'],
                   'word_bank': ['Privacy', 'regulation', 'AI', 'users', 'ethics', 'encryption'],
                   'questions': [{'q': 'What did the voice-assistant update store by default?',
                                  'accept': ['ambient snippets', 'snippets'],
                                  'hint_ru': 'Что хранилось по умолчанию?',
                                  'quote': '…stored ambient snippets by default.',
                                  'model_en': 'Ambient snippets.'},
                                 {'q': 'What did privacy advocates say failed ordinary users?',
                                  'accept': ['opaque consent screens', 'consent screens'],
                                  'hint_ru': 'Что, по мнению активистов, подвело пользователей?',
                                  'quote': '…opaque consent screens failed ordinary people…',
                                  'model_en': 'Opaque consent screens.'},
                                 {'q': "What three actions did the chair's vote require?",
                                  'accept': ['delay the launch, publish a retention table, and '
                                             'commission an audit',
                                             'delay, retention table, audit',
                                             'delay the launch'],
                                  'hint_ru': 'Какие три действия проголосовали?',
                                  'quote': '…delay the launch, publish a plain-language retention '
                                           'table, and commission an external audit…',
                                  'model_en': 'Delay the launch, publish a retention table, and '
                                              'commission an external audit.'},
                                 {'q': 'How did the minutes describe ethics after deployment?',
                                  'accept': ['damage control, not design', 'damage control'],
                                  'hint_ru': 'Как описали ethics после релиза?',
                                  'quote': '…ethics after deployment is damage control, not '
                                           'design.',
                                  'model_en': 'As damage control, not design.'}],
                   'plan': ['Default snippet storage problem',
                            'Privacy vs regulation arguments',
                            'On-device AI trade-off',
                            'Voted remedies and closing warning'],
                   'facts': ['The update stored ambient snippets by default.',
                             'Privacy advocates criticised opaque consent screens.',
                             'Engineers proposed on-device AI to trim retention.',
                             'The panel voted to delay launch, publish retention details, and '
                             'audit deletion logs.']},
        'city_plan': {'full_text': 'Planners unveiled a corridor plan that paired a tram extension '
                                   'with mid-rise housing above new stations. The public debate '
                                   'split along familiar lines: residents wanted reliable '
                                   'transport before denser blocks, while developers insisted '
                                   'dwelling finance required the ridership numbers first. Budget '
                                   'sheets showed a funding gap unless regional grants arrived by '
                                   'autumn. Architects offered courtyards and quieter street edges '
                                   'to soften opposition, yet heritage groups still feared shadow '
                                   'on a listed square. After three hearings the mayor endorsed a '
                                   'phased build—tracks first, then two residential '
                                   'pilots—contingent on a transparent spending revision. The '
                                   'compromise pleased few enthusiasts, but it kept mobility and '
                                   'dwellings on the same map instead of rival petitions.',
                      'gapped_text': 'Planners unveiled a corridor plan that paired a tram '
                                     'extension with mid-rise (1)___ above new stations. The '
                                     'public (2)___ split along familiar lines: residents wanted '
                                     'reliable (3)___ before denser blocks, while developers '
                                     'insisted dwelling finance required the ridership numbers '
                                     'first. (4)___ sheets showed a funding gap unless regional '
                                     'grants arrived by autumn. Architects offered courtyards and '
                                     'quieter street edges to soften opposition, yet heritage '
                                     'groups still feared shadow on a listed square. After three '
                                     'hearings the mayor endorsed a phased build—tracks first, '
                                     'then two residential pilots—contingent on a transparent '
                                     'spending revision. The compromise pleased few enthusiasts, '
                                     'but it kept mobility and dwellings on the same map instead '
                                     'of rival (5)___.',
                      'answers': ['housing', 'debate', 'transport', 'Budget', 'petitions'],
                      'word_bank': ['housing',
                                    'debate',
                                    'transport',
                                    'Budget',
                                    'petitions',
                                    'tolls'],
                      'questions': [{'q': 'What two elements did the corridor plan pair?',
                                     'accept': ['a tram extension with mid-rise housing',
                                                'tram extension and housing',
                                                'tram and housing'],
                                     'hint_ru': 'Что сочетал план коридора?',
                                     'quote': '…a tram extension with mid-rise housing…',
                                     'model_en': 'A tram extension with mid-rise housing above new '
                                                 'stations.'},
                                    {'q': 'What did residents want before denser blocks?',
                                     'accept': ['reliable transport',
                                                'transport first',
                                                'reliable transport before denser blocks'],
                                     'hint_ru': 'Что жители хотели раньше уплотнения?',
                                     'quote': '…reliable transport before denser blocks…',
                                     'model_en': 'Reliable transport before denser blocks.'},
                                    {'q': 'By when did regional grants need to arrive?',
                                     'accept': ['by autumn', 'autumn'],
                                     'hint_ru': 'К какому сроку нужны гранты?',
                                     'quote': '…grants arrived by autumn.',
                                     'model_en': 'By autumn.'},
                                    {'q': 'What phased order did the mayor endorse?',
                                     'accept': ['tracks first, then two residential pilots',
                                                'tracks first, then two housing pilots',
                                                'tracks first',
                                                'phased build'],
                                     'hint_ru': 'Какой поэтапный порядок одобрил мэр?',
                                     'quote': '…tracks first, then two residential pilots…',
                                     'model_en': 'Tracks first, then two residential pilots.'}],
                      'plan': ['Corridor plan elements',
                               'Public debate positions',
                               'Budget gap and design mitigations',
                               'Phased mayoral endorsement'],
                      'facts': ['The plan paired a tram extension with mid-rise housing above '
                                'stations.',
                                'Residents wanted reliable transport before denser blocks.',
                                'Budget sheets showed a gap unless regional grants arrived by '
                                'autumn.',
                                'The mayor endorsed tracks first, then two residential pilots.']},
        'leadership': {'full_text': 'When two product squads stalled over ownership of a shared '
                                    'checkout service, Mira called an emergency leadership huddle '
                                    'rather than another ticket war. The team arrived defensive; a '
                                    'quiet conflict had already leaked into stand-ups and delayed '
                                    'a release. Mira refused to pick a winner on seniority alone '
                                    'and instead forced a written decision matrix: customer '
                                    'impact, maintenance load, and roadmap fit. After ninety '
                                    'minutes the group chose a single owning squad with a '
                                    'published interface contract and a rotating on-call from the '
                                    'other side. The outcome was imperfect—some engineers still '
                                    'felt overruled—yet the arrangement held through the next '
                                    'launch. Mira later noted that calm facilitation here meant '
                                    'ending ambiguity faster than it bred resentment.',
                       'gapped_text': 'When two product squads stalled over ownership of a shared '
                                      'checkout service, Mira called an emergency (1)___ huddle '
                                      'rather than another ticket war. The (2)___ arrived '
                                      'defensive; a quiet (3)___ had already leaked into stand-ups '
                                      'and delayed a release. Mira refused to pick a winner on '
                                      'seniority alone and instead forced a written (4)___ matrix: '
                                      'customer impact, maintenance load, and roadmap fit. After '
                                      'ninety minutes the group chose a single owning squad with a '
                                      'published interface contract and a rotating on-call from '
                                      "the other side. The meeting's (5)___ was imperfect—some "
                                      'engineers still felt overruled—yet the arrangement held '
                                      'through the next launch. Mira later noted that calm '
                                      'facilitation here meant ending ambiguity faster than it '
                                      'bred resentment.',
                       'answers': ['leadership', 'team', 'conflict', 'decision', 'outcome'],
                       'word_bank': ['leadership',
                                     'team',
                                     'conflict',
                                     'decision',
                                     'outcome',
                                     'bonus'],
                       'questions': [{'q': 'What were the two squads arguing over?',
                                      'accept': ['ownership of a shared checkout service',
                                                 'checkout service ownership',
                                                 'shared checkout service'],
                                      'hint_ru': 'Из-за чего спорили команды?',
                                      'quote': '…ownership of a shared checkout service…',
                                      'model_en': 'Ownership of a shared checkout service.'},
                                     {'q': 'What three criteria were in the decision matrix?',
                                      'accept': ['customer impact, maintenance load, and roadmap '
                                                 'fit',
                                                 'customer impact',
                                                 'maintenance load',
                                                 'roadmap fit'],
                                      'hint_ru': 'Какие три критерия в матрице?',
                                      'quote': '…customer impact, maintenance load, and roadmap '
                                               'fit.',
                                      'model_en': 'Customer impact, maintenance load, and roadmap '
                                                  'fit.'},
                                     {'q': 'What arrangement did the group choose after ninety '
                                           'minutes?',
                                      'accept': ['a single owning squad with a published interface '
                                                 'contract and rotating on-call',
                                                 'single owning squad',
                                                 'rotating on-call'],
                                      'hint_ru': 'Какое решение приняли?',
                                      'quote': '…a single owning squad with a published interface '
                                               'contract and a rotating on-call…',
                                      'model_en': 'One owning squad, a published interface '
                                                  'contract, and rotating on-call.'},
                                     {'q': 'Did the decision hold through the next launch?',
                                      'accept': ['yes',
                                                 'the arrangement held',
                                                 'held through the next launch',
                                                 'the decision held'],
                                      'hint_ru': 'Удержалось ли решение до следующего релиза?',
                                      'quote': '…the arrangement held through the next launch.',
                                      'model_en': 'Yes, the arrangement held through the next '
                                                  'launch.'}],
                       'plan': ['Ownership conflict between squads',
                                'Leadership huddle instead of ticket war',
                                'Decision matrix and chosen ownership model',
                                'Imperfect outcome that still held'],
                       'facts': ['Two squads stalled over shared checkout ownership.',
                                 'A quiet conflict had leaked into stand-ups and delayed a '
                                 'release.',
                                 'Mira used a decision matrix: impact, maintenance, roadmap fit.',
                                 'One squad owned the service; the other provided rotating '
                                 'on-call.']}},
 'C2': {'board': {'full_text': 'At the quarterly board meeting, the non-executive directors '
                               'challenged the CEO on whether a rapid acquisition served long-term '
                               'value or merely short-term optics. The CFO presented downside '
                               'scenarios in which regulatory delay and integration friction could '
                               'erase projected synergies within eighteen months. Marketing warned '
                               'that aggressive messaging might trigger a PR backlash among '
                               'institutional investors already uneasy about leverage. Strategy, '
                               'they argued, had to privilege resilience over headline growth: '
                               'retaining cash for contingencies rather than stretching the '
                               'balance sheet. After a tense exchange, the board approved a '
                               'conditional offer subject to stricter risk covenants and an '
                               'independent review of cultural fit. Minutes recorded that any '
                               'breach of those covenants would trigger an automatic pause, not a '
                               'quiet renegotiation behind closed doors.',
                  'gapped_text': 'At the quarterly board meeting, the non-executive directors '
                                 'challenged the CEO on whether a rapid acquisition served '
                                 'long-term (1)___ or merely short-term optics. The CFO presented '
                                 'downside scenarios in which regulatory delay and integration '
                                 'friction could erase projected synergies within eighteen months. '
                                 'Marketing warned that aggressive messaging might trigger a '
                                 '(2)___ backlash among institutional investors already uneasy '
                                 'about leverage. (3)___, they argued, had to privilege resilience '
                                 'over headline growth: retaining cash for contingencies rather '
                                 'than stretching the balance sheet. After a tense exchange, the '
                                 'board approved a conditional offer subject to stricter (4)___ '
                                 'covenants and an independent review of cultural fit. Minutes '
                                 'recorded that any breach of those covenants would trigger an '
                                 'automatic (5)___, not a quiet renegotiation behind closed doors.',
                  'answers': ['value', 'PR', 'Strategy', 'risk', 'pause'],
                  'word_bank': ['value', 'PR', 'Strategy', 'risk', 'pause', 'dividend'],
                  'questions': [{'q': 'What concern did non-executive directors raise about the '
                                      'acquisition?',
                                 'accept': ['long-term value vs short-term optics',
                                            'short-term optics',
                                            'long-term value',
                                            'optics'],
                                 'hint_ru': 'Что ставили под сомнение неисполнительные директора?',
                                 'quote': '…served long-term value or merely short-term optics.',
                                 'model_en': 'They questioned whether it served long-term value or '
                                             'only short-term optics.'},
                                {'q': 'What did Marketing warn could happen among investors?',
                                 'accept': ['PR backlash',
                                            'a PR backlash',
                                            'backlash',
                                            'public relations backlash'],
                                 'hint_ru': 'О чём предупредил маркетинг?',
                                 'quote': '…might trigger a PR backlash among institutional '
                                          'investors…',
                                 'model_en': 'Marketing warned of a PR backlash among '
                                             'institutional investors.'},
                                {'q': "What condition was attached to the board's approval?",
                                 'accept': ['stricter risk covenants',
                                            'risk covenants',
                                            'conditional offer',
                                            'independent review'],
                                 'hint_ru': 'На каких условиях совет одобрил предложение?',
                                 'quote': '…approved a conditional offer subject to stricter risk '
                                          'covenants…',
                                 'model_en': 'Approval was conditional on stricter risk covenants '
                                             'and an independent review.'},
                                {'q': 'What would a breach of the covenants trigger?',
                                 'accept': ['an automatic pause',
                                            'automatic pause',
                                            'a pause',
                                            'pause'],
                                 'hint_ru': 'Что произойдёт при нарушении ковенантов?',
                                 'quote': '…would trigger an automatic pause…',
                                 'model_en': 'A breach would trigger an automatic pause.'}],
                  'plan': ["Challenge to the acquisition's rationale",
                           'Financial and PR risks raised',
                           'Preference for resilience over growth',
                           'Conditional approval and pause mechanism'],
                  'facts': ['Non-executives questioned long-term value versus short-term optics.',
                            'CFO flagged regulatory delay and integration friction; Marketing '
                            'feared a PR backlash.',
                            'Strategy favoured cash resilience over leverage-driven growth.',
                            'The board approved a conditional offer with risk covenants; breach '
                            'triggers an automatic pause.']},
        'policy': {'full_text': 'The draft housing brief conceded that rent caps might please '
                                'tenants yet distort incentives for landlords to maintain and '
                                'expand supply. Officials mapped stakeholders carefully: municipal '
                                'planners sought denser zoning, developers demanded '
                                'predictability, and community groups insisted on affordable units '
                                'near transit. Evidence from neighbouring cities suggested '
                                'unintended effects — informal subletting, deferred repairs, and a '
                                'flight of capital into holiday lets. The recommended package '
                                'therefore paired modest caps with tax credits for long-term '
                                'leases and faster permits for mid-rise projects. Ministers were '
                                'urged to publish a monitoring dashboard so that policy could be '
                                'adjusted before political pressure froze a flawed design in '
                                'place. Without such feedback, the brief warned, goodwill would '
                                'evaporate faster than any waiting list could shrink.',
                   'gapped_text': 'The draft housing brief conceded that rent caps might please '
                                  'tenants yet distort (1)___ for landlords to maintain and expand '
                                  'supply. Officials mapped (2)___ carefully: municipal planners '
                                  'sought denser zoning, developers demanded predictability, and '
                                  'community groups insisted on affordable units near transit. '
                                  'Evidence from neighbouring cities suggested (3)___ effects — '
                                  'informal subletting, deferred repairs, and a flight of capital '
                                  'into holiday lets. The recommended package therefore paired '
                                  'modest caps with tax credits for long-term leases and faster '
                                  'permits for mid-rise projects. Ministers were urged to publish '
                                  'a monitoring dashboard so that (4)___ could be adjusted before '
                                  'political pressure froze a flawed design in place. Without such '
                                  'feedback, the brief warned, goodwill would evaporate faster '
                                  'than any waiting (5)___ could shrink.',
                   'answers': ['incentives', 'stakeholders', 'unintended', 'policy', 'list'],
                   'word_bank': ['incentives',
                                 'stakeholders',
                                 'unintended',
                                 'policy',
                                 'list',
                                 'subsidy'],
                   'questions': [{'q': 'What risk do rent caps pose for landlords according to the '
                                       'brief?',
                                  'accept': ['distort incentives',
                                             'distort incentives for landlords',
                                             'incentives to maintain and expand supply',
                                             'reduce supply incentives'],
                                  'hint_ru': 'Как потолки аренды влияют на стимулы арендодателей?',
                                  'quote': '…distort incentives for landlords to maintain and '
                                           'expand supply.',
                                  'model_en': 'They may distort incentives for landlords to '
                                              'maintain and expand supply.'},
                                 {'q': 'Name one unintended effect observed in neighbouring '
                                       'cities.',
                                  'accept': ['informal subletting',
                                             'deferred repairs',
                                             'flight of capital into holiday lets',
                                             'holiday lets',
                                             'subletting'],
                                  'hint_ru': 'Какой побочный эффект уже видели в соседних городах?',
                                  'quote': '…informal subletting, deferred repairs, and a flight '
                                           'of capital…',
                                  'model_en': 'Examples include informal subletting, deferred '
                                              'repairs, or capital fleeing into holiday lets.'},
                                 {'q': 'What did the recommended package pair with modest rent '
                                       'caps?',
                                  'accept': ['tax credits for long-term leases',
                                             'tax credits',
                                             'faster permits',
                                             'tax credits and faster permits'],
                                  'hint_ru': 'С чем сочетали умеренные потолки аренды?',
                                  'quote': '…paired modest caps with tax credits for long-term '
                                           'leases and faster permits…',
                                  'model_en': 'It paired modest caps with tax credits for '
                                              'long-term leases and faster permits.'},
                                 {'q': 'Why should ministers publish a monitoring dashboard?',
                                  'accept': ['so policy could be adjusted',
                                             'adjust policy',
                                             'adjust before political pressure',
                                             'to adjust policy'],
                                  'hint_ru': 'Зачем нужен мониторинговый дашборд?',
                                  'quote': '…so that policy could be adjusted before political '
                                           'pressure froze a flawed design…',
                                  'model_en': 'So that policy could be adjusted before politics '
                                              'froze a flawed design.'}],
                   'plan': ['Trade-off of rent caps and landlord incentives',
                            'Stakeholder map and unintended effects',
                            'Recommended mixed package',
                            'Monitoring to allow policy adjustment'],
                   'facts': ["Rent caps may distort landlords' incentives to maintain and expand "
                             'supply.',
                             'Stakeholders include planners, developers, and community groups; '
                             'unintended effects include subletting and holiday lets.',
                             'The package pairs modest caps with tax credits and faster mid-rise '
                             'permits.',
                             'A monitoring dashboard is urged so policy can be adjusted before '
                             'politics locks errors in.']},
        'lit': {'full_text': 'In her slim review of the coastal novella, Mira argued that the '
                             'central theme is not nostalgia but the ethics of witnessing: who is '
                             "entitled to narrate a drowning town. The narrator's tone shifts from "
                             'wry detachment to something almost liturgical whenever the tide '
                             'tables appear, a rhythm that critics once dismissed as ornamental. '
                             'Mira instead reads the recurring lighthouse as symbolism of withheld '
                             'rescue — light without intervention. Her critique is sharpest where '
                             "the plot romanticises silence: the absent father's letters are "
                             'beautiful, she grants, yet they excuse complicity rather than expose '
                             'it. Still, she praises the prose for refusing neat catharsis. The '
                             'review closes by urging readers to sit with unresolved grief instead '
                             'of hunting for a moral that the text deliberately withholds.',
                'gapped_text': 'In her slim review of the coastal novella, Mira argued that the '
                               'central (1)___ is not nostalgia but the ethics of witnessing: who '
                               "is entitled to narrate a drowning town. The narrator's (2)___ "
                               'shifts from wry detachment to something almost liturgical whenever '
                               'the tide tables appear, a rhythm that critics once dismissed as '
                               'ornamental. Mira instead reads the recurring lighthouse as (3)___ '
                               'of withheld rescue — light without intervention. Her (4)___ is '
                               "sharpest where the plot romanticises silence: the absent father's "
                               'letters are beautiful, she grants, yet they excuse complicity '
                               'rather than expose it. Still, she praises the prose for refusing '
                               'neat catharsis. The review closes by urging readers to sit with '
                               'unresolved grief instead of hunting for a (5)___ that the text '
                               'deliberately withholds.',
                'answers': ['theme', 'tone', 'symbolism', 'critique', 'moral'],
                'word_bank': ['theme', 'tone', 'symbolism', 'critique', 'moral', 'epilogue'],
                'questions': [{'q': 'What does Mira say the central theme is?',
                               'accept': ['ethics of witnessing',
                                          'the ethics of witnessing',
                                          'witnessing',
                                          'who is entitled to narrate'],
                               'hint_ru': 'Какова, по Мире, центральная тема?',
                               'quote': '…the central theme is not nostalgia but the ethics of '
                                        'witnessing…',
                               'model_en': 'She says the central theme is the ethics of '
                                           'witnessing.'},
                              {'q': "How does the narrator's tone change when tide tables appear?",
                               'accept': ['from wry detachment to almost liturgical',
                                          'wry detachment to liturgical',
                                          'becomes liturgical',
                                          'almost liturgical'],
                               'hint_ru': 'Как меняется тон рассказчика у таблиц приливов?',
                               'quote': '…tone shifts from wry detachment to something almost '
                                        'liturgical…',
                               'model_en': 'It shifts from wry detachment to something almost '
                                           'liturgical.'},
                              {'q': 'What does Mira say the lighthouse symbolises?',
                               'accept': ['withheld rescue',
                                          'light without intervention',
                                          'rescue withheld',
                                          'withheld rescue — light without intervention'],
                               'hint_ru': 'Что символизирует маяк?',
                               'quote': '…symbolism of withheld rescue — light without '
                                        'intervention.',
                               'model_en': 'It symbolises withheld rescue: light without '
                                           'intervention.'},
                              {'q': "Why does Mira criticise the father's letters?",
                               'accept': ['they excuse complicity',
                                          'excuse complicity rather than expose it',
                                          'romanticises silence',
                                          'excuse complicity'],
                               'hint_ru': 'За что она критикует письма отца?',
                               'quote': '…they excuse complicity rather than expose it.',
                               'model_en': 'She says they excuse complicity rather than expose '
                                           'it.'}],
                'plan': ['Central theme: ethics of witnessing',
                         'Tone shift and lighthouse symbolism',
                         'Critique of romanticised silence',
                         'Refusal of neat moral closure'],
                'facts': ['Mira locates the theme in the ethics of witnessing, not nostalgia.',
                          'Tone turns almost liturgical at tide tables; the lighthouse symbolises '
                          'withheld rescue.',
                          'Her critique targets silence that excuses complicity, including the '
                          "father's letters.",
                          'She praises the refusal of neat catharsis and a withheld moral.']},
        'finance': {'full_text': "Tuesday's note to clients opened with a blunt admission: equity "
                                 'markets had priced a soft landing too neatly, leaving little '
                                 'cushion against fresh volatility in energy and currency pairs. '
                                 'The desk expected policy rates to stay restrictive longer than '
                                 'consensus forecasts implied, which would keep refinancing costs '
                                 'elevated for highly leveraged issuers across emerging and '
                                 'developed markets alike. Their baseline outlook still favoured '
                                 'selective credit over broad equity beta, but only with explicit '
                                 'hedges on duration and foreign exchange. Caution, the '
                                 'strategists insisted, was not pessimism; it was recognition that '
                                 'liquidity could vanish faster than models assumed once margin '
                                 'calls cascaded through prime brokerage. Positions were trimmed '
                                 'in cyclical names and rotated toward shorter-duration sovereign '
                                 'paper until clearer data arrived on wage growth and inventory '
                                 'rebuilds.',
                    'gapped_text': "Tuesday's note to clients opened with a blunt admission: "
                                   'equity markets had priced a soft landing too neatly, leaving '
                                   'little cushion against fresh (1)___ in energy and currency '
                                   'pairs. The desk expected policy (2)___ to stay restrictive '
                                   'longer than consensus forecasts implied, which would keep '
                                   'refinancing costs elevated for highly leveraged issuers across '
                                   'emerging and developed markets alike. Their baseline (3)___ '
                                   'still favoured selective credit over broad equity beta, but '
                                   'only with explicit hedges on duration and foreign exchange. '
                                   '(4)___, the strategists insisted, was not pessimism; it was '
                                   'recognition that liquidity could vanish faster than models '
                                   'assumed once margin calls cascaded through prime brokerage. '
                                   'Positions were trimmed in cyclical names and rotated toward '
                                   'shorter-duration sovereign paper until clearer (5)___ arrived '
                                   'on wage growth and inventory rebuilds.',
                    'answers': ['volatility', 'rates', 'outlook', 'Caution', 'data'],
                    'word_bank': ['volatility', 'rates', 'outlook', 'Caution', 'data', 'dividend'],
                    'questions': [{'q': 'What had equity markets priced too neatly?',
                                   'accept': ['a soft landing',
                                              'soft landing',
                                              'soft landing too neatly'],
                                   'hint_ru': 'Что рынки акций заложили слишком гладко?',
                                   'quote': '…equity markets had priced a soft landing too neatly…',
                                   'model_en': 'They had priced a soft landing too neatly.'},
                                  {'q': 'How long did the desk expect policy rates to stay '
                                        'restrictive?',
                                   'accept': ['longer than consensus',
                                              'longer than consensus forecasts',
                                              'longer than forecasts implied',
                                              'longer than consensus forecasts implied'],
                                   'hint_ru': 'Как долго, по мнению деска, ставки останутся '
                                              'жёсткими?',
                                   'quote': '…policy rates to stay restrictive longer than '
                                            'consensus forecasts implied…',
                                   'model_en': 'Longer than consensus forecasts implied.'},
                                  {'q': 'What did their baseline outlook favour?',
                                   'accept': ['selective credit over broad equity beta',
                                              'selective credit',
                                              'credit over equity beta'],
                                   'hint_ru': 'Что предпочитал базовый outlook?',
                                   'quote': '…outlook still favoured selective credit over broad '
                                            'equity beta…',
                                   'model_en': 'It favoured selective credit over broad equity '
                                               'beta.'},
                                  {'q': 'Where were positions rotated after trimming cyclicals?',
                                   'accept': ['shorter-duration sovereign paper',
                                              'sovereign paper',
                                              'shorter-duration sovereign'],
                                   'hint_ru': 'Куда переложили позиции после сокращения '
                                              'циклических бумаг?',
                                   'quote': '…rotated toward shorter-duration sovereign paper…',
                                   'model_en': 'Toward shorter-duration sovereign paper.'}],
                    'plan': ['Soft-landing pricing and volatility risk',
                             'Restrictive rates and refinancing costs',
                             'Outlook: selective credit with hedges',
                             'Rotation into shorter sovereign paper'],
                    'facts': ['Markets had priced a soft landing with little cushion against '
                              'volatility.',
                              'Policy rates were expected to stay restrictive longer than '
                              'consensus implied.',
                              'Baseline outlook favoured selective credit with hedges; caution ≠ '
                              'pessimism.',
                              'Cyclicals were trimmed in favour of shorter-duration sovereign '
                              'paper pending clearer data.']},
        'diplomacy': {'full_text': 'The communiqué after midnight talks avoided naming the '
                                   'disputed corridor, substituting a studied ambiguity that both '
                                   'capitals could sell as progress to restless domestic '
                                   'audiences. Negotiators spent hours on wording: whether '
                                   "'provisional access' implied recognition, and whether "
                                   "'security guarantees' bound third parties not present at the "
                                   'table. National interests remained asymmetrical — one side '
                                   'sought trade corridors, the other buffer zones — yet neither '
                                   'could afford a public rupture before elections. A narrow '
                                   'compromise emerged: observers for ninety days, a freeze on new '
                                   'fortifications, and a technical committee on customs and water '
                                   'rights. Envoys privately conceded the deal was fragile, but '
                                   'argued that silence had become more dangerous than an '
                                   'imperfect text. The note closed with a pledge to resume '
                                   'negotiations within a fortnight if verification stalled.',
                      'gapped_text': 'The communiqué after midnight (1)___ avoided naming the '
                                     'disputed corridor, substituting a studied ambiguity that '
                                     'both capitals could sell as progress to restless domestic '
                                     'audiences. Negotiators spent hours on (2)___: whether '
                                     "'provisional access' implied recognition, and whether "
                                     "'security guarantees' bound third parties not present at the "
                                     'table. National (3)___ remained asymmetrical — one side '
                                     'sought trade corridors, the other buffer zones — yet neither '
                                     'could afford a public rupture before elections. A narrow '
                                     '(4)___ emerged: observers for ninety days, a freeze on new '
                                     'fortifications, and a technical committee on customs and '
                                     'water rights. Envoys privately conceded the deal was '
                                     'fragile, but argued that silence had become more dangerous '
                                     'than an imperfect text. The note closed with a pledge to '
                                     'resume negotiations within a fortnight if (5)___ stalled.',
                      'answers': ['talks', 'wording', 'interests', 'compromise', 'verification'],
                      'word_bank': ['talks',
                                    'wording',
                                    'interests',
                                    'compromise',
                                    'verification',
                                    'embargo'],
                      'questions': [{'q': 'What did the communiqué avoid naming?',
                                     'accept': ['the disputed corridor',
                                                'disputed corridor',
                                                'corridor'],
                                     'hint_ru': 'Что коммюнике намеренно не назвало?',
                                     'quote': '…avoided naming the disputed corridor…',
                                     'model_en': 'It avoided naming the disputed corridor.'},
                                    {'q': 'What asymmetrical interests did the two sides pursue?',
                                     'accept': ['trade corridors and buffer zones',
                                                'trade corridors / buffer zones',
                                                'trade corridors',
                                                'buffer zones'],
                                     'hint_ru': 'Какие асимметричные интересы были у сторон?',
                                     'quote': '…one side sought trade corridors, the other buffer '
                                              'zones…',
                                     'model_en': 'One sought trade corridors; the other sought '
                                                 'buffer zones.'},
                                    {'q': 'What elements made up the narrow compromise?',
                                     'accept': ['observers, freeze, customs committee',
                                                'observers for ninety days',
                                                'freeze on fortifications',
                                                'observers, freeze on fortifications, technical '
                                                'committee'],
                                     'hint_ru': 'Из чего состоял узкий компромисс?',
                                     'quote': '…observers for ninety days, a freeze on new '
                                              'fortifications, and a technical committee…',
                                     'model_en': 'Observers for ninety days, a freeze on '
                                                 'fortifications, and a customs committee.'},
                                    {'q': 'When would talks resume if verification stalled?',
                                     'accept': ['within a fortnight',
                                                'in a fortnight',
                                                'fortnight',
                                                'within two weeks'],
                                     'hint_ru': 'Когда возобновят переговоры, если верификация '
                                                'застопорится?',
                                     'quote': '…resume negotiations within a fortnight if '
                                              'verification stalled.',
                                     'model_en': 'Within a fortnight.'}],
                      'plan': ['Ambiguous communiqué after midnight talks',
                               'Disputes over wording and asymmetrical interests',
                               'Narrow compromise package',
                               'Pledge to resume if verification stalls'],
                      'facts': ['Midnight talks produced ambiguity instead of naming the disputed '
                                'corridor.',
                                'Hours went into wording; national interests were trade corridors '
                                'vs buffer zones.',
                                'Compromise: ninety-day observers, freeze on fortifications, '
                                'customs committee.',
                                'Talks would resume within a fortnight if verification stalled.']},
        'science': {'full_text': "The laboratory's public briefing on the antiviral trial stressed "
                                 'what the data could and could not show. Preliminary evidence '
                                 'suggested a meaningful reduction in hospitalisation among '
                                 'high-risk adults, yet sample sizes for older cohorts remained '
                                 'thin and secondary endpoints were exploratory. Researchers '
                                 'foregrounded uncertainty rather than burying confidence '
                                 'intervals in an appendix, arguing that public trust erodes when '
                                 'caveats arrive only after headlines have hardened into '
                                 'certainty. Journalists were given access to anonymised protocols '
                                 'and invited to ask how endpoints had been pre-registered before '
                                 'unblinding. The director refused to call the compound a '
                                 "breakthrough, preferring 'promising under defined conditions.' "
                                 'She noted that replication across climates and comorbidities '
                                 'would decide whether the signal survived outside controlled '
                                 'wards and specialised hospital ICUs.',
                    'gapped_text': "The laboratory's public briefing on the antiviral trial "
                                   'stressed what the data could and could not show. Preliminary '
                                   '(1)___ suggested a meaningful reduction in hospitalisation '
                                   'among high-risk adults, yet sample sizes for older cohorts '
                                   'remained thin and secondary endpoints were exploratory. '
                                   'Researchers foregrounded (2)___ rather than burying confidence '
                                   'intervals in an appendix, arguing that public (3)___ erodes '
                                   'when caveats arrive only after headlines have hardened into '
                                   'certainty. Journalists were given access to anonymised '
                                   'protocols and invited to ask how endpoints had been '
                                   'pre-registered before unblinding. The director refused to call '
                                   "the compound a breakthrough, preferring 'promising under "
                                   "defined conditions.' She noted that (4)___ across climates and "
                                   'comorbidities would decide whether the (5)___ survived outside '
                                   'controlled wards and specialised hospital ICUs.',
                    'answers': ['evidence', 'uncertainty', 'trust', 'replication', 'signal'],
                    'word_bank': ['evidence',
                                  'uncertainty',
                                  'trust',
                                  'replication',
                                  'signal',
                                  'patent'],
                    'questions': [{'q': 'What did preliminary evidence suggest?',
                                   'accept': ['reduction in hospitalisation',
                                              'meaningful reduction in hospitalisation',
                                              'fewer hospitalisations among high-risk adults',
                                              'hospitalisation reduction'],
                                   'hint_ru': 'На что указывали предварительные данные?',
                                   'quote': '…meaningful reduction in hospitalisation among '
                                            'high-risk adults…',
                                   'model_en': 'A meaningful reduction in hospitalisation among '
                                               'high-risk adults.'},
                                  {'q': 'Why did researchers foreground uncertainty?',
                                   'accept': ['public trust erodes when caveats arrive after '
                                              'headlines',
                                              'public trust',
                                              'trust erodes',
                                              'caveats after headlines'],
                                   'hint_ru': 'Почему учёные выносили неопределённость на первый '
                                              'план?',
                                   'quote': '…public trust erodes when caveats arrive only after '
                                            'headlines.',
                                   'model_en': 'Because public trust erodes when caveats arrive '
                                               'only after headlines.'},
                                  {'q': 'How did the director describe the compound?',
                                   'accept': ['promising under defined conditions',
                                              'not a breakthrough',
                                              'refused to call it a breakthrough'],
                                   'hint_ru': 'Как директор назвала препарат?',
                                   'quote': "…preferring 'promising under defined conditions.'",
                                   'model_en': "She preferred 'promising under defined "
                                               "conditions,' not 'breakthrough.'"},
                                  {'q': 'What would decide whether the signal survived outside '
                                        'wards?',
                                   'accept': ['replication across climates and comorbidities',
                                              'replication',
                                              'replication across climates'],
                                   'hint_ru': 'Что решит, сохранится ли сигнал вне палат?',
                                   'quote': '…replication across climates and comorbidities would '
                                            'decide…',
                                   'model_en': 'Replication across climates and comorbidities.'}],
                    'plan': ['What trial data can and cannot show',
                             'Foregrounding uncertainty for public trust',
                             'Access to protocols and careful wording',
                             'Need for replication beyond controlled wards'],
                    'facts': ['Preliminary evidence suggested reduced hospitalisation in high-risk '
                              'adults; older cohorts were thin.',
                              'Researchers foregrounded uncertainty to protect public trust.',
                              'The director called the compound promising under defined '
                              'conditions, not a breakthrough.',
                              'Replication across climates and comorbidities would test whether '
                              'the signal survived.']},
        'art': {'full_text': 'The biennale essay on the mirrored plaza installation refuses a '
                             'single interpretation, inviting visitors to treat reflection as both '
                             'vanity and surveillance under a civic sky. Context matters: the '
                             'plaza once hosted immigration hearings, and the polished steel still '
                             'catches courthouse windows at dusk, folding bureaucracy into the '
                             'spectacle. Controversy erupted when a sponsor demanded softer '
                             'lighting after protesters used the mirrors to project slogans '
                             'overnight. Curators held firm, arguing that sanitising the work '
                             'would convert critique into décor for weekend tourism. Critics split '
                             'between those who saw manipulative spectacle and those who praised '
                             'the piece for making complicity visible to ordinary pedestrians. The '
                             'essay concludes that contemporary art rarely settles arguments; it '
                             'stages them where passers-by cannot pretend neutrality.',
                'gapped_text': 'The biennale essay on the mirrored plaza installation refuses a '
                               'single (1)___, inviting visitors to treat reflection as both '
                               'vanity and surveillance under a civic sky. (2)___ matters: the '
                               'plaza once hosted immigration hearings, and the polished steel '
                               'still catches courthouse windows at dusk, folding bureaucracy into '
                               'the spectacle. (3)___ erupted when a sponsor demanded softer '
                               'lighting after protesters used the mirrors to project slogans '
                               'overnight. Curators held firm, arguing that sanitising the work '
                               'would convert critique into décor for weekend tourism. Critics '
                               'split between those who saw manipulative spectacle and those who '
                               'praised the piece for making complicity visible to ordinary '
                               'pedestrians. The essay concludes that contemporary (4)___ rarely '
                               'settles arguments; it stages them where passers-by cannot pretend '
                               '(5)___.',
                'answers': ['interpretation', 'Context', 'Controversy', 'art', 'neutrality'],
                'word_bank': ['interpretation',
                              'Context',
                              'Controversy',
                              'art',
                              'neutrality',
                              'auction'],
                'questions': [{'q': 'How does the essay invite visitors to treat reflection?',
                               'accept': ['as both vanity and surveillance',
                                          'vanity and surveillance',
                                          'vanity',
                                          'surveillance'],
                               'hint_ru': 'Как эссе предлагает воспринимать отражение?',
                               'quote': '…treat reflection as both vanity and surveillance.',
                               'model_en': 'As both vanity and surveillance.'},
                              {'q': 'What historical use of the plaza does the essay mention?',
                               'accept': ['immigration hearings',
                                          'hosted immigration hearings',
                                          'hearings'],
                               'hint_ru': 'Какое историческое использование площади упоминается?',
                               'quote': '…the plaza once hosted immigration hearings…',
                               'model_en': 'It once hosted immigration hearings.'},
                              {'q': 'Why did controversy erupt with the sponsor?',
                               'accept': ['demanded softer lighting',
                                          'softer lighting after protesters',
                                          'sponsor demanded softer lighting',
                                          'protesters projected slogans'],
                               'hint_ru': 'Из-за чего разгорелся спор со спонсором?',
                               'quote': '…sponsor demanded softer lighting after protesters used '
                                        'the mirrors…',
                               'model_en': 'The sponsor demanded softer lighting after protesters '
                                           'projected slogans.'},
                              {'q': 'What do curators say sanitising the work would do?',
                               'accept': ['convert critique into décor',
                                          'turn critique into décor',
                                          'critique into décor'],
                               'hint_ru': 'Во что, по кураторам, превратится критика при '
                                          '«смягчении» работы?',
                               'quote': '…sanitising the work would convert critique into décor.',
                               'model_en': 'It would convert critique into décor.'}],
                'plan': ['Refusal of a single interpretation',
                         'Historical context of the plaza',
                         'Sponsor controversy and curatorial stance',
                         'Art as staging unresolved arguments'],
                'facts': ['Reflection is framed as vanity and surveillance; no single '
                          'interpretation.',
                          'Context: former immigration hearings; steel catches courthouse windows.',
                          'Controversy after a sponsor sought softer lighting post-protest '
                          'projections.',
                          'Curators refused sanitising; the essay says art stages arguments, not '
                          'settles them.']},
        'philosophy': {'full_text': 'The seminar on the trolley variant asked whether rescue '
                                    'drones should prioritise the many strangers or the single '
                                    'identified child whose face fills the live feed during a '
                                    'flood. Students defending utilitarianism cited aggregate '
                                    'consequences, while deontologists insisted that some '
                                    'principles forbid treating any person as expendable '
                                    'arithmetic for the sake of a cleaner spreadsheet. A third '
                                    'camp stressed judgment under uncertainty: operators rarely '
                                    'know probabilities cleanly, so moral theory must leave room '
                                    'for tragic choice without demanding omniscience. The tutor '
                                    'refused a neat ranking, noting that public institutions still '
                                    'need decision rules even when philosophy remains divided in '
                                    'the seminar room. Homework required each student to state '
                                    'which principle they would stake a career on — and which '
                                    'results they were prepared to own if that principle failed in '
                                    'the field.',
                       'gapped_text': 'The seminar on the trolley variant asked whether rescue '
                                      'drones should prioritise the many strangers or the single '
                                      'identified child whose face fills the live feed during a '
                                      'flood. Students defending utilitarianism cited aggregate '
                                      '(1)___, while deontologists insisted that some (2)___ '
                                      'forbid treating any person as expendable arithmetic for the '
                                      'sake of a cleaner spreadsheet. A third camp stressed (3)___ '
                                      'under uncertainty: operators rarely know probabilities '
                                      'cleanly, so moral theory must leave room for tragic choice '
                                      'without demanding omniscience. The tutor refused a neat '
                                      'ranking, noting that public institutions still need '
                                      'decision rules even when philosophy remains divided in the '
                                      'seminar room. Homework required each student to state which '
                                      'principle they would stake a career on — and which results '
                                      'they were prepared to (4)___ if that principle failed in '
                                      'the (5)___.',
                       'answers': ['consequences', 'principles', 'judgment', 'own', 'field'],
                       'word_bank': ['consequences',
                                     'principles',
                                     'judgment',
                                     'own',
                                     'field',
                                     'syllabus'],
                       'questions': [{'q': 'What dilemma did the trolley-variant seminar pose for '
                                           'rescue drones?',
                                      'accept': ['many strangers or single identified child',
                                                 'prioritise the many or the child',
                                                 'many strangers vs identified child',
                                                 'strangers or child'],
                                      'hint_ru': 'Какую дилемму ставил семинар для дронов '
                                                 'спасения?',
                                      'quote': '…prioritise the many strangers or the single '
                                               'identified child…',
                                      'model_en': 'Whether to prioritise many strangers or one '
                                                  'identified child.'},
                                     {'q': 'What did deontologists insist some principles forbid?',
                                      'accept': ['treating any person as expendable arithmetic',
                                                 'expendable arithmetic',
                                                 'treating a person as expendable'],
                                      'hint_ru': 'Что, по деонтологам, запрещают некоторые '
                                                 'принципы?',
                                      'quote': '…forbid treating any person as expendable '
                                               'arithmetic.',
                                      'model_en': 'Treating any person as expendable arithmetic.'},
                                     {'q': 'What did the third camp stress?',
                                      'accept': ['judgment under uncertainty',
                                                 'judgment',
                                                 'tragic choice without omniscience'],
                                      'hint_ru': 'На чём настаивал третий лагерь?',
                                      'quote': 'A third camp stressed judgment under uncertainty…',
                                      'model_en': 'Judgment under uncertainty.'},
                                     {'q': 'What did homework ask students to stake a career on?',
                                      'accept': ['which principle',
                                                 'a principle',
                                                 'which principle they would stake a career on',
                                                 'principle and consequences they would own'],
                                      'hint_ru': 'Что домашнее задание просило «поставить на карту '
                                                 'карьеры»?',
                                      'quote': '…state which principle they would stake a career '
                                               'on…',
                                      'model_en': 'Which principle they would stake a career on — '
                                                  'and which consequences they would own.'}],
                       'plan': ['Drone trolley dilemma setup',
                                'Utilitarian vs deontological clash',
                                'Judgment under uncertainty',
                                'Homework: own a principle and its failures'],
                       'facts': ['The dilemma: many strangers versus one identified child on the '
                                 'feed.',
                                 'Utilitarians cited aggregate consequences; deontologists invoked '
                                 'non-expendable principles.',
                                 'A third camp stressed judgment under uncertainty without '
                                 'demanding omniscience.',
                                 'Students had to stake a career on a principle and own '
                                 'consequences if it failed in the field.']}}}


def get_reading_pack(level: str, topic_id: str) -> dict | None:
    lvl = (level or "A1").upper()
    tid = (topic_id or "").strip()
    block = READING_PACKS.get(lvl) or {}
    pack = block.get(tid)
    if not pack:
        return None
    return {
        "full_text": pack["full_text"],
        "gapped_text": pack["gapped_text"],
        "answers": list(pack["answers"]),
        "word_bank": list(pack["word_bank"]),
        "questions": [dict(q) for q in pack["questions"]],
        "plan": list(pack["plan"]),
        "facts": list(pack["facts"]),
    }
