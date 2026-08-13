# -*- coding: utf-8 -*-
"""Fixed Reading packs for CEFR levels A0 and A1 only."""

from __future__ import annotations

PACKS: dict[str, dict[str, dict]] = {
    "A0": {
        "family": {
            "full_text": (
                "My name is Tom. I live with my family in a small house. "
                "I have one brother. His name is Max. He is eight years old and he likes football. "
                "My mother is a nurse. Mum helps sick people at the hospital. "
                "My father is a driver. Dad drives a big bus in the city. "
                "In the evening we eat dinner in the kitchen. "
                "I love my family very much. Next Sunday we will visit grandpa."
            ),
            "gapped_text": (
                "My name is Tom. I live with my family in a small house. "
                "I have one brother. His name is (1)___. He is eight years old and he likes (2)___. "
                "My mother is a (3)___. Mum helps sick people at the hospital. "
                "My father is a driver. Dad drives a big bus in the city. "
                "In the evening we eat dinner in the (4)___. "
                "I love my family very much. Next Sunday we will visit (5)___."
            ),
            "answers": ["Max", "football", "nurse", "kitchen", "grandpa"],
            "word_bank": ["Max", "football", "nurse", "kitchen", "grandpa", "bus"],
            "questions": [
                {
                    "q": "How old is Max?",
                    "accept": ["eight", "8", "eight years old"],
                    "hint_ru": "Сколько лет Максу?",
                    "quote": "He is eight years old…",
                    "model_en": "Max is eight years old.",
                },
                {
                    "q": "What is Tom's mother's job?",
                    "accept": ["nurse", "a nurse"],
                    "hint_ru": "Кем работает мама?",
                    "quote": "My mother is a nurse…",
                    "model_en": "Tom's mother is a nurse.",
                },
                {
                    "q": "What does Dad drive?",
                    "accept": ["a big bus", "bus", "a bus"],
                    "hint_ru": "Что водит папа?",
                    "quote": "Dad drives a big bus…",
                    "model_en": "Dad drives a big bus.",
                },
                {
                    "q": "Where do they eat dinner?",
                    "accept": ["in the kitchen", "kitchen"],
                    "hint_ru": "Где они ужинают?",
                    "quote": "…eat dinner in the kitchen.",
                    "model_en": "They eat dinner in the kitchen.",
                },
            ],
            "plan": [
                "Who Tom lives with",
                "Facts about Max",
                "Parents' jobs",
                "Evening dinner and Sunday visit",
            ],
            "facts": [
                "Tom has a brother named Max.",
                "Max is eight and likes football.",
                "Mum is a nurse; Dad is a driver.",
                "They eat in the kitchen; next Sunday they visit grandpa.",
            ],
        },
        "colors": {
            "full_text": (
                "Nina draws with crayons at the table. She colours a big red apple first. "
                "Then she paints the sky blue on the paper. The grass under the tree is green. "
                "Her favourite crayon is the colour of the sun — yellow. She keeps the crayons in a small box. "
                "She shows the picture to her friend Sam. Sam says the apple looks real. "
                "Nina puts the crayons away carefully. She likes bright colours every day."
            ),
            "gapped_text": (
                "Nina draws with crayons at the table. She colours a big (1)___ apple first. "
                "Then she paints the sky (2)___ on the paper. The grass under the tree is (3)___. "
                "Her favourite crayon is the colour of the sun — (4)___. She keeps the crayons in a small (5)___. "
                "She shows the picture to her friend Sam. Sam says the apple looks real. "
                "Nina puts the crayons away carefully. She likes bright colours every day."
            ),
            "answers": ["red", "blue", "green", "yellow", "box"],
            "word_bank": ["red", "blue", "green", "yellow", "box", "dog"],
            "questions": [
                {
                    "q": "What colour is the apple in Nina's picture?",
                    "accept": ["red", "a red apple"],
                    "hint_ru": "Какого цвета яблоко на рисунке?",
                    "quote": "…a big red apple…",
                    "model_en": "The apple is red.",
                },
                {
                    "q": "What colour does she paint the sky?",
                    "accept": ["blue"],
                    "hint_ru": "Каким цветом она красит небо?",
                    "quote": "…paints the sky blue…",
                    "model_en": "She paints the sky blue.",
                },
                {
                    "q": "What colour is Nina's favourite crayon?",
                    "accept": ["yellow"],
                    "hint_ru": "Какого цвета любимый мелок Нины?",
                    "quote": "…the colour of the sun — yellow.",
                    "model_en": "Nina's favourite crayon is yellow.",
                },
                {
                    "q": "Where does she keep the crayons?",
                    "accept": ["in a small box", "box", "a small box"],
                    "hint_ru": "Где она хранит мелки?",
                    "quote": "…keeps the crayons in a small box.",
                    "model_en": "She keeps the crayons in a small box.",
                },
            ],
            "plan": [
                "Red apple on the paper",
                "Blue sky and green grass",
                "Yellow crayon like the sun",
                "Crayons in a box; showing Sam",
            ],
            "facts": [
                "Nina colours a red apple first.",
                "The sky is blue and the grass is green.",
                "Her favourite crayon is yellow like the sun.",
                "She keeps the crayons in a small box.",
            ],
        },
        "food": {
            "full_text": (
                "Anna likes simple food. For breakfast she eats bread and cheese. "
                "She drinks tea with lemon, not coffee. At lunch she takes an apple and a sandwich. "
                "In the evening her family cooks soup together. Anna does not like fish, but she loves fruit. "
                "On Sundays they buy fresh bread at the shop. Anna puts the bread in a basket on the table. "
                "Then they sit and eat slowly. After dinner Anna washes the cups."
            ),
            "gapped_text": (
                "Anna likes simple food. For breakfast she eats bread and cheese. "
                "She drinks (1)___ with lemon, not coffee. At lunch she takes an (2)___ and a sandwich. "
                "In the evening her family cooks (3)___ together. Anna does not like fish, but she loves fruit. "
                "On Sundays they buy fresh bread at the shop. Anna puts the bread in a (4)___ on the table. "
                "Then they sit and eat slowly. After dinner Anna washes the (5)___."
            ),
            "answers": ["tea", "apple", "soup", "basket", "cups"],
            "word_bank": ["tea", "apple", "soup", "basket", "cups", "pencil"],
            "questions": [
                {
                    "q": "What does Anna drink with lemon?",
                    "accept": ["tea", "tea with lemon"],
                    "hint_ru": "Что Анна пьёт с лимоном?",
                    "quote": "She drinks tea with lemon…",
                    "model_en": "Anna drinks tea with lemon.",
                },
                {
                    "q": "What fruit does she take at lunch?",
                    "accept": ["apple", "an apple"],
                    "hint_ru": "Какой фрукт она берёт в обед?",
                    "quote": "…takes an apple and a sandwich.",
                    "model_en": "She takes an apple at lunch.",
                },
                {
                    "q": "What do they cook in the evening?",
                    "accept": ["soup"],
                    "hint_ru": "Что они готовят вечером?",
                    "quote": "…cooks soup together.",
                    "model_en": "They cook soup in the evening.",
                },
                {
                    "q": "Where does Anna put the bread?",
                    "accept": ["in a basket", "basket", "on the table"],
                    "hint_ru": "Куда Анна кладёт хлеб?",
                    "quote": "…in a basket on the table.",
                    "model_en": "Anna puts the bread in a basket on the table.",
                },
            ],
            "plan": [
                "Breakfast drinks and food",
                "Lunch",
                "Evening cooking",
                "Sunday shop and dinner",
            ],
            "facts": [
                "Anna drinks tea with lemon, not coffee.",
                "At lunch she takes an apple and a sandwich.",
                "In the evening they cook soup.",
                "On Sundays they buy bread; she puts it in a basket.",
            ],
        },
        "pets": {
            "full_text": (
                "Rita has two pets at home. Her cat is soft and grey. Its name is Mimi. "
                "Rita also has a small brown dog. Its name is Buddy. "
                "Every morning Buddy wants to play with a ball in the garden. "
                "Mimi sleeps on a soft chair near the window. "
                "Rita gives water to them after school. "
                "On Friday they visit the vet for a short check. Rita loves her pets very much."
            ),
            "gapped_text": (
                "Rita has two animals at home. Her (1)___ is soft and grey. Its name is Mimi. "
                "Rita also has a small brown (2)___. Its name is Buddy. "
                "Every morning Buddy wants to play with a (3)___ in the garden. "
                "Mimi sleeps on a soft chair near the window. "
                "Rita gives water to them after school. "
                "On Friday they visit the (4)___ for a short check. Rita loves her (5)___ very much."
            ),
            "answers": ["cat", "dog", "ball", "vet", "pets"],
            "word_bank": ["cat", "dog", "ball", "vet", "pets", "car"],
            "questions": [
                {
                    "q": "What is the cat's name?",
                    "accept": ["Mimi"],
                    "hint_ru": "Как зовут кошку?",
                    "quote": "Its name is Mimi.",
                    "model_en": "The cat's name is Mimi.",
                },
                {
                    "q": "What colour is the dog?",
                    "accept": ["brown", "small brown"],
                    "hint_ru": "Какого цвета собака?",
                    "quote": "…a small brown dog.",
                    "model_en": "The dog is brown.",
                },
                {
                    "q": "What does Buddy play with in the garden?",
                    "accept": ["a ball", "ball"],
                    "hint_ru": "С чем играет Бадди в саду?",
                    "quote": "…play with a ball in the garden.",
                    "model_en": "Buddy plays with a ball in the garden.",
                },
                {
                    "q": "Where do they go on Friday?",
                    "accept": ["the vet", "vet", "to the vet"],
                    "hint_ru": "Куда они идут в пятницу?",
                    "quote": "…visit the vet for a short check.",
                    "model_en": "They visit the vet on Friday.",
                },
            ],
            "plan": [
                "Rita's cat Mimi",
                "Rita's dog Buddy",
                "Morning play and rest",
                "Friday visit to the vet",
            ],
            "facts": [
                "Rita has a grey cat named Mimi.",
                "She has a brown dog named Buddy.",
                "Buddy plays with a ball in the garden.",
                "On Friday they visit the vet.",
            ],
        },
        "home": {
            "full_text": (
                "Leo lives in a small flat with two rooms. The kitchen is bright because of a big window. "
                "His bedroom has a bed, a desk and a blue chair at the desk. Near the entrance there is a green plant. "
                "In the evening Leo reads a book on the soft sofa. His sister draws pictures at the desk. "
                "Mum opens it when it is hot. Dad fixes the door when it makes a noise. "
                "They keep shoes next to it. Leo likes his home because it is peaceful and quiet."
            ),
            "gapped_text": (
                "Leo lives in a small flat with two rooms. The kitchen is bright because of a big (1)___. "
                "His bedroom has a bed, a desk and a blue (2)___ at the desk. Near the entrance there is a green plant. "
                "In the evening Leo reads a book on the soft (3)___. His sister draws pictures at the desk. "
                "Mum opens it when it is hot. Dad fixes the (4)___ when it makes a noise. "
                "They keep shoes next to it. Leo likes his home because it is peaceful and (5)___."
            ),
            "answers": ["window", "chair", "sofa", "door", "quiet"],
            "word_bank": ["window", "chair", "sofa", "door", "quiet", "garden"],
            "questions": [
                {
                    "q": "Why is the kitchen bright?",
                    "accept": ["big window", "window", "because of a big window"],
                    "hint_ru": "Почему кухня светлая?",
                    "quote": "…because of a big window.",
                    "model_en": "The kitchen is bright because of a big window.",
                },
                {
                    "q": "What colour is the chair?",
                    "accept": ["blue", "blue chair"],
                    "hint_ru": "Какого цвета стул?",
                    "quote": "…a blue chair at the desk.",
                    "model_en": "The chair is blue.",
                },
                {
                    "q": "Where does Leo read in the evening?",
                    "accept": ["on the soft sofa", "on the sofa", "sofa"],
                    "hint_ru": "Где Лео читает вечером?",
                    "quote": "…reads a book on the soft sofa.",
                    "model_en": "Leo reads a book on the soft sofa in the evening.",
                },
                {
                    "q": "Why does Leo like his home?",
                    "accept": ["peaceful and quiet", "quiet", "because it is peaceful and quiet"],
                    "hint_ru": "Почему Лео нравится дом?",
                    "quote": "…peaceful and quiet.",
                    "model_en": "Leo likes his home because it is peaceful and quiet.",
                },
            ],
            "plan": [
                "Flat and kitchen",
                "Bedroom chair at the desk",
                "Evening on the soft sofa",
                "Door, shoes, peaceful quiet home",
            ],
            "facts": [
                "Kitchen is bright because of a big window.",
                "Bedroom has a bed, desk and blue chair at the desk.",
                "Leo reads on the soft sofa; sister draws at the desk.",
                "Dad fixes the door; Leo likes the peaceful quiet home.",
            ],
        },
        "school": {
            "full_text": (
                "Omar goes to school every morning with a blue bag. In the bag he has a pen and a book. "
                "His teacher is kind and smiles in the classroom. Today the class reads a short story. "
                "Omar writes new words in his notebook. At break he talks with his friend Kate. "
                "In the afternoon Omar does homework at the desk. He puts it next to the book. "
                "Tomorrow someone will check his work carefully. Omar likes school very much."
            ),
            "gapped_text": (
                "Omar goes every morning with a blue bag. In the bag he has a (1)___ and a notebook. "
                "His (2)___ is kind and smiles in the classroom. Today the class reads a short story. "
                "Omar writes new words in his notebook. At break he talks with his friend Kate. "
                "In the afternoon Omar does (3)___ at the desk. He puts it next to the (4)___. "
                "Tomorrow someone will check his work carefully. Omar likes (5)___ very much."
            ),
            "answers": ["pen", "teacher", "homework", "book", "school"],
            "word_bank": ["pen", "teacher", "homework", "book", "school", "banana"],
            "questions": [
                {
                    "q": "What colour is Omar's bag?",
                    "accept": ["blue", "a blue bag"],
                    "hint_ru": "Какого цвета сумка Омара?",
                    "quote": "…with a blue bag.",
                    "model_en": "Omar's bag is blue.",
                },
                {
                    "q": "Who smiles in the classroom?",
                    "accept": ["his teacher", "the teacher", "teacher"],
                    "hint_ru": "Кто улыбается в классе?",
                    "quote": "His teacher is kind and smiles…",
                    "model_en": "His teacher smiles in the classroom.",
                },
                {
                    "q": "What does Omar do in the afternoon?",
                    "accept": ["homework", "does homework", "homework at the desk"],
                    "hint_ru": "Что Омар делает днём?",
                    "quote": "…does homework at the desk.",
                    "model_en": "Omar does homework in the afternoon.",
                },
                {
                    "q": "What will happen to his work tomorrow?",
                    "accept": ["someone will check", "check his work", "will check his work carefully"],
                    "hint_ru": "Что будет с его работой завтра?",
                    "quote": "Tomorrow someone will check his work carefully.",
                    "model_en": "Someone will check his work carefully tomorrow.",
                },
            ],
            "plan": [
                "Bag with pen and book",
                "Teacher and classroom",
                "Break with Kate",
                "Homework after school",
            ],
            "facts": [
                "Omar carries a pen and a book in a blue bag.",
                "His teacher is kind in the classroom.",
                "At break he talks with Kate.",
                "After school he does homework at the desk.",
            ],
        },
        "days": {
            "full_text": (
                "Today is Monday, the first school day of the week. Eva goes to school and has English class. "
                "On Tuesday she plays tennis with her sister. Wednesday is a busy day with maths. "
                "On Thursday Eva helps Mum in the shop. Friday is her favourite day because school ends early. "
                "On Saturday the family goes to the market. Sunday is a quiet day at home with no lessons. "
                "Eva writes the days in her calendar. She likes the week when it is clear."
            ),
            "gapped_text": (
                "Today is (1)___, the first school day of the week. Eva goes to school and has English class. "
                "On Tuesday she plays (2)___ with her sister. Wednesday is a busy day with maths. "
                "On Thursday Eva helps Mum in the shop. (3)___ is her favourite day because school ends early. "
                "On Saturday the family goes to the (4)___. (5)___ is a quiet day at home with no lessons. "
                "Eva writes the days in her calendar. She likes the week when it is clear."
            ),
            "answers": ["Monday", "tennis", "Friday", "market", "Sunday"],
            "word_bank": ["Monday", "tennis", "Friday", "market", "Sunday", "Thursday"],
            "questions": [
                {
                    "q": "What day is today?",
                    "accept": ["Monday"],
                    "hint_ru": "Какой сегодня день?",
                    "quote": "Today is Monday…",
                    "model_en": "Today is Monday.",
                },
                {
                    "q": "When does Eva play tennis?",
                    "accept": ["on Tuesday", "Tuesday"],
                    "hint_ru": "Когда Эва играет в теннис?",
                    "quote": "On Tuesday she plays tennis…",
                    "model_en": "Eva plays tennis on Tuesday.",
                },
                {
                    "q": "Which day is Eva's favourite?",
                    "accept": ["Friday"],
                    "hint_ru": "Какой день любимый у Эвы?",
                    "quote": "Friday is her favourite day…",
                    "model_en": "Friday is Eva's favourite day.",
                },
                {
                    "q": "What do they do on Saturday?",
                    "accept": ["go to the market", "market", "goes to the market"],
                    "hint_ru": "Что они делают в субботу?",
                    "quote": "…the family goes to the market.",
                    "model_en": "The family goes to the market on Saturday.",
                },
            ],
            "plan": [
                "Monday first school day",
                "Tuesday tennis",
                "Favourite Friday",
                "Saturday market and quiet Sunday",
            ],
            "facts": [
                "Today is Monday, the first school day.",
                "On Tuesday Eva plays tennis.",
                "Friday is her favourite day.",
                "Saturday is market day; Sunday is quiet at home.",
            ],
        },
        "hello": {
            "full_text": (
                "Ben meets a new girl near the school gate. He says hello with a big smile. "
                "The girl says her name is Lara. Ben says he is Ben. "
                "They say nice to meet you and laugh a little. Lara is a new student in class. "
                "Ben shows Lara the classroom door. The teacher says welcome to Lara. "
                "At break Ben and Lara sit together. Ben is happy to have a new friend."
            ),
            "gapped_text": (
                "Ben meets a new girl near the school gate. He says (1)___ with a big (2)___. "
                "The girl says her (3)___ is Lara. Ben says he is Ben. "
                "They say nice to (4)___ you and laugh a little. Lara is a new student in class. "
                "Ben shows Lara the classroom door. The teacher says welcome to Lara. "
                "At break Ben and Lara sit together. Ben is happy to have a new (5)___."
            ),
            "answers": ["hello", "smile", "name", "meet", "friend"],
            "word_bank": ["hello", "smile", "name", "meet", "friend", "goodbye"],
            "questions": [
                {
                    "q": "Where does Ben meet the new girl?",
                    "accept": ["near the school gate", "school gate", "gate"],
                    "hint_ru": "Где Бен встречает новую девочку?",
                    "quote": "…near the school gate.",
                    "model_en": "Ben meets her near the school gate.",
                },
                {
                    "q": "What is the girl's name?",
                    "accept": ["Lara"],
                    "hint_ru": "Как зовут девочку?",
                    "quote": "…her name is Lara.",
                    "model_en": "The girl's name is Lara.",
                },
                {
                    "q": "What do they say after names?",
                    "accept": ["nice to meet you", "nice to meet"],
                    "hint_ru": "Что они говорят после имён?",
                    "quote": "They say nice to meet you…",
                    "model_en": "They say nice to meet you.",
                },
                {
                    "q": "Who says welcome to Lara?",
                    "accept": ["the teacher", "teacher"],
                    "hint_ru": "Кто говорит Ларе welcome?",
                    "quote": "The teacher says welcome to Lara.",
                    "model_en": "The teacher says welcome to Lara.",
                },
            ],
            "plan": [
                "Meeting near the gate",
                "Saying names",
                "Nice to meet you",
                "New friend at break",
            ],
            "facts": [
                "Ben says hello near the school gate.",
                "The girl's name is Lara.",
                "They say nice to meet you.",
                "Ben is happy to have a new friend.",
            ],
        },
    },
    "A1": {
        "family_a1": {
            "full_text": (
                "My name is Carlos. I live with my parents and my sister Rosa in a flat near the park. "
                "She is fourteen years old and she studies art after school. "
                "My father is an engineer. Dad designs bridges for the city. "
                "My mother is a dentist. Mum works in a small clinic and looks after teeth. "
                "At weekends Uncle Pedro visits us with fresh fruit. "
                "We cook together and talk about our week. I am proud of my family."
            ),
            "gapped_text": (
                "My name is Carlos. I live with my parents and my sister (1)___ in a flat near the park. "
                "She is (2)___ years old and she studies art after school. "
                "My father is an (3)___. Dad designs bridges for the city. "
                "My mother is a (4)___. Mum works in a small clinic and looks after teeth. "
                "At weekends Uncle (5)___ visits us with fresh fruit. "
                "We cook together and talk about our week. I am proud of my family."
            ),
            "answers": ["Rosa", "fourteen", "engineer", "dentist", "Pedro"],
            "word_bank": ["Rosa", "fourteen", "engineer", "dentist", "Pedro", "teacher"],
            "questions": [
                {
                    "q": "How old is Rosa?",
                    "accept": ["fourteen", "14", "fourteen years old"],
                    "hint_ru": "Сколько лет Росе?",
                    "quote": "She is fourteen years old…",
                    "model_en": "Rosa is fourteen years old.",
                },
                {
                    "q": "What is Carlos's father's job?",
                    "accept": ["engineer", "an engineer"],
                    "hint_ru": "Кем работает папа Карлоса?",
                    "quote": "My father is an engineer…",
                    "model_en": "Carlos's father is an engineer.",
                },
                {
                    "q": "Where does Mum work?",
                    "accept": ["in a small clinic", "clinic", "a small clinic"],
                    "hint_ru": "Где работает мама?",
                    "quote": "Mum works in a small clinic…",
                    "model_en": "Mum works in a small clinic.",
                },
                {
                    "q": "Who visits at weekends?",
                    "accept": ["Uncle Pedro", "Pedro", "uncle"],
                    "hint_ru": "Кто приходит в выходные?",
                    "quote": "…Uncle Pedro visits us…",
                    "model_en": "Uncle Pedro visits them at weekends.",
                },
            ],
            "plan": [
                "Carlos and sister Rosa",
                "Father's job as engineer",
                "Mother's job as dentist",
                "Weekend visit from Uncle Pedro",
            ],
            "facts": [
                "Carlos lives with parents and sister Rosa.",
                "Rosa is fourteen and studies art.",
                "Dad is an engineer; Mum is a dentist.",
                "Uncle Pedro visits at weekends.",
            ],
        },
        "cafe": {
            "full_text": (
                "Sara and Dan sit at a small café near the station. The waiter brings a list of drinks and food to their table. "
                "Sara orders a cup of black coffee and a piece of chocolate cake. "
                "Dan chooses green tea and a cheese sandwich. "
                "They look at the menu again and share one small cookie. "
                "The café is quiet and the table by the window is free. "
                "Sara pays eight pounds for the order. They thank him and leave happy."
            ),
            "gapped_text": (
                "Sara and Dan sit at a small café near the station. The (1)___ brings a list of drinks and food to their table. "
                "Sara orders a cup of black (2)___ and a piece of chocolate (3)___. "
                "Dan chooses green (4)___ and a cheese sandwich. "
                "They look at the (5)___ again and share one small cookie. "
                "The café is quiet and the table by the window is free. "
                "Sara pays eight pounds for the order. They thank him and leave happy."
            ),
            "answers": ["waiter", "coffee", "cake", "tea", "menu"],
            "word_bank": ["waiter", "coffee", "cake", "tea", "menu", "juice"],
            "questions": [
                {
                    "q": "Who brings the list of drinks and food?",
                    "accept": ["the waiter", "waiter"],
                    "hint_ru": "Кто приносит список напитков и еды?",
                    "quote": "The waiter brings a list of drinks and food…",
                    "model_en": "The waiter brings a list of drinks and food.",
                },
                {
                    "q": "What does Sara order to drink?",
                    "accept": ["coffee", "black coffee", "a cup of black coffee", "a cup of coffee"],
                    "hint_ru": "Что Сара заказывает выпить?",
                    "quote": "Sara orders a cup of black coffee…",
                    "model_en": "Sara orders a cup of black coffee.",
                },
                {
                    "q": "What does Dan choose to drink?",
                    "accept": ["green tea", "a green tea", "green tea and a cheese sandwich"],
                    "hint_ru": "Что выбирает Дэн?",
                    "quote": "Dan chooses green tea…",
                    "model_en": "Dan chooses green tea.",
                },
                {
                    "q": "How much does Sara pay?",
                    "accept": ["eight pounds", "8 pounds", "eight", "£8"],
                    "hint_ru": "Сколько платит Сара?",
                    "quote": "Sara pays eight pounds…",
                    "model_en": "Sara pays eight pounds.",
                },
            ],
            "plan": [
                "Sitting at the café",
                "Sara's black coffee and cake",
                "Dan's tea and sandwich",
                "Payment and thanking the waiter",
            ],
            "facts": [
                "The waiter brings a list of drinks and food.",
                "Sara orders black coffee and chocolate cake.",
                "Dan chooses green tea and a cheese sandwich.",
                "Sara pays eight pounds.",
            ],
        },
        "daily": {
            "full_text": (
                "Every morning Kate wakes up at seven. She washes her face and eats breakfast quickly. "
                "Then she takes the bus to work and listens to music on the way. "
                "At one o'clock she has a short lunch at the office with a sandwich. "
                "In the afternoon Kate answers emails and calls clients. "
                "In the evening she cooks a simple dinner and reads a book. "
                "Before bed she checks her plan for tomorrow. Kate likes a clear daily routine."
            ),
            "gapped_text": (
                "Every morning Kate (1)___ up at seven. She washes her face and eats (2)___ quickly. "
                "Then she takes the (3)___ to work and listens to music on the way. "
                "At one o'clock she has a short (4)___ at the office with a sandwich. "
                "In the afternoon Kate answers emails and calls clients. "
                "In the (5)___ she cooks a simple dinner and reads a book. "
                "Before bed she checks her plan for tomorrow. Kate likes a clear daily routine."
            ),
            "answers": ["wakes", "breakfast", "bus", "lunch", "evening"],
            "word_bank": ["wakes", "breakfast", "bus", "lunch", "evening", "shower"],
            "questions": [
                {
                    "q": "What time does Kate wake up?",
                    "accept": ["seven", "at seven", "7"],
                    "hint_ru": "Во сколько Кейт просыпается?",
                    "quote": "…wakes up at seven.",
                    "model_en": "Kate wakes up at seven.",
                },
                {
                    "q": "How does she go to work?",
                    "accept": ["by bus", "bus", "takes the bus"],
                    "hint_ru": "Как она добирается на работу?",
                    "quote": "…takes the bus to work…",
                    "model_en": "She takes the bus to work.",
                },
                {
                    "q": "When does she have lunch?",
                    "accept": ["at one o'clock", "one o'clock", "1 o'clock", "at one"],
                    "hint_ru": "Когда у неё обед?",
                    "quote": "At one o'clock she has a short lunch…",
                    "model_en": "She has lunch at one o'clock.",
                },
                {
                    "q": "What does she do in the evening?",
                    "accept": [
                        "cooks dinner and reads",
                        "cooks a simple dinner",
                        "reads a book",
                        "cooks and reads",
                    ],
                    "hint_ru": "Что она делает вечером?",
                    "quote": "…cooks a simple dinner and reads a book.",
                    "model_en": "In the evening she cooks dinner and reads a book.",
                },
            ],
            "plan": [
                "Morning wake-up and breakfast",
                "Bus to work",
                "Lunch at the office",
                "Evening dinner and reading",
            ],
            "facts": [
                "Kate wakes up at seven.",
                "She takes the bus to work.",
                "She has lunch at one o'clock.",
                "In the evening she cooks and reads.",
            ],
        },
        "hobbies": {
            "full_text": (
                "In his free time Alex plays football with friends in the park near his house. "
                "On rainy days he plays the guitar at home and writes short songs. "
                "Alex also likes films and watches one every Friday night with popcorn. "
                "His sister prefers reading long stories on the sofa. "
                "At the weekend Alex goes swimming at the sports centre for one hour. "
                "These hobbies help him relax after a busy week at school."
            ),
            "gapped_text": (
                "In his free time Alex plays (1)___ with friends in the park near his house. "
                "On rainy days he plays the (2)___ at home and writes short songs. "
                "Alex also likes (3)___ and watches one every Friday night with popcorn. "
                "His sister prefers (4)___ long stories on the sofa. "
                "At the weekend Alex goes (5)___ at the sports centre for one hour. "
                "These hobbies help him relax after a busy week at school."
            ),
            "answers": ["football", "guitar", "films", "reading", "swimming"],
            "word_bank": ["football", "guitar", "films", "reading", "swimming", "kitchen"],
            "questions": [
                {
                    "q": "What does Alex play in the park?",
                    "accept": ["football"],
                    "hint_ru": "Во что Алекс играет в парке?",
                    "quote": "…plays football with friends in the park…",
                    "model_en": "Alex plays football in the park.",
                },
                {
                    "q": "What does he play on rainy days?",
                    "accept": ["the guitar", "guitar"],
                    "hint_ru": "На чём он играет в дождливые дни?",
                    "quote": "…plays the guitar at home…",
                    "model_en": "He plays the guitar on rainy days.",
                },
                {
                    "q": "When does Alex watch a film?",
                    "accept": ["every Friday night", "Friday night", "Friday"],
                    "hint_ru": "Когда Алекс смотрит фильм?",
                    "quote": "…watches one every Friday night…",
                    "model_en": "Alex watches a film every Friday night.",
                },
                {
                    "q": "Where does Alex go swimming?",
                    "accept": ["at the sports centre", "sports centre"],
                    "hint_ru": "Где Алекс плавает?",
                    "quote": "…swimming at the sports centre…",
                    "model_en": "Alex goes swimming at the sports centre.",
                },
            ],
            "plan": [
                "Football in the park",
                "Guitar on rainy days",
                "Films and sister's reading",
                "Weekend swimming",
            ],
            "facts": [
                "Alex plays football with friends.",
                "On rainy days he plays the guitar.",
                "He watches films on Friday night.",
                "At the weekend he goes swimming.",
            ],
        },
        "shopping": {
            "full_text": (
                "Maya goes to a clothes shop on High Street after school. She needs new jeans for school. "
                "The assistant asks about the size. Maya tries a medium pair in the fitting room. "
                "The price is twenty pounds. Maya likes the colour and decides to pay by card. "
                "She also buys a small scarf for her mum as a gift. "
                "The assistant puts everything in a paper bag. Maya leaves with a smile."
            ),
            "gapped_text": (
                "Maya goes to a clothes (1)___ on High Street after school. She needs new (2)___ for school. "
                "The assistant asks about the (3)___. Maya tries a medium pair in the fitting room. "
                "The (4)___ is twenty pounds. Maya likes the colour and decides to (5)___ by card. "
                "She also buys a small scarf for her mum as a gift. "
                "The assistant puts everything in a paper bag. Maya leaves with a smile."
            ),
            "answers": ["shop", "jeans", "size", "price", "pay"],
            "word_bank": ["shop", "jeans", "size", "price", "pay", "lemon"],
            "questions": [
                {
                    "q": "What does Maya need for school?",
                    "accept": ["new jeans", "jeans"],
                    "hint_ru": "Что нужно Майе для школы?",
                    "quote": "She needs new jeans for school.",
                    "model_en": "Maya needs new jeans for school.",
                },
                {
                    "q": "What size does she try?",
                    "accept": ["medium", "a medium pair"],
                    "hint_ru": "Какой размер она примеряет?",
                    "quote": "Maya tries a medium pair…",
                    "model_en": "She tries a medium pair.",
                },
                {
                    "q": "How much are the jeans?",
                    "accept": ["twenty pounds", "20 pounds", "twenty", "£20"],
                    "hint_ru": "Сколько стоят джинсы?",
                    "quote": "The price is twenty pounds.",
                    "model_en": "The jeans cost twenty pounds.",
                },
                {
                    "q": "How does Maya pay?",
                    "accept": ["by card", "card"],
                    "hint_ru": "Как Майя платит?",
                    "quote": "…pay by card.",
                    "model_en": "Maya pays by card.",
                },
            ],
            "plan": [
                "Clothes shop on High Street",
                "Trying jeans and size",
                "Price and payment",
                "Scarf for mum",
            ],
            "facts": [
                "Maya needs new jeans for school.",
                "She tries a medium size.",
                "The price is twenty pounds.",
                "She pays by card and buys a scarf.",
            ],
        },
        "weekend": {
            "full_text": (
                "On Saturday morning Nora meets her friends at the bus stop near the station. "
                "They go to the cinema and watch a funny film together. "
                "After the film they walk in the park and buy ice cream. "
                "On Sunday Nora stays at home and calls her grandma for a long chat. "
                "In the afternoon the family has a small picnic in the garden. "
                "Nora likes weekends because she can rest and see friends."
            ),
            "gapped_text": (
                "On (1)___ morning Nora meets them at the bus stop near the station. "
                "They go to the (2)___ and watch a funny film together. "
                "After the film they walk in the (3)___ and buy ice cream. "
                "On Sunday Nora stays at home and calls her grandma for a long chat. "
                "In the afternoon the family has a small (4)___ in the garden. "
                "Nora likes weekends because she can rest and see (5)___."
            ),
            "answers": ["Saturday", "cinema", "park", "picnic", "friends"],
            "word_bank": ["Saturday", "cinema", "park", "picnic", "friends", "museum"],
            "questions": [
                {
                    "q": "Where do they watch a film?",
                    "accept": ["at the cinema", "cinema", "the cinema"],
                    "hint_ru": "Где они смотрят фильм?",
                    "quote": "They go to the cinema…",
                    "model_en": "They watch a film at the cinema.",
                },
                {
                    "q": "Where do they walk after the film?",
                    "accept": ["in the park", "park", "the park"],
                    "hint_ru": "Где они гуляют после фильма?",
                    "quote": "…walk in the park…",
                    "model_en": "They walk in the park after the film.",
                },
                {
                    "q": "What does Nora do on Sunday at home?",
                    "accept": ["calls her grandma", "calls grandma", "stays at home"],
                    "hint_ru": "Что Нора делает дома в воскресенье?",
                    "quote": "…stays at home and calls her grandma…",
                    "model_en": "Nora stays at home and calls her grandma.",
                },
                {
                    "q": "Where is the picnic?",
                    "accept": ["in the garden", "garden"],
                    "hint_ru": "Где проходит пикник?",
                    "quote": "…picnic in the garden.",
                    "model_en": "The picnic is in the garden.",
                },
            ],
            "plan": [
                "Saturday meet friends",
                "Cinema and park",
                "Sunday call to grandma",
                "Garden picnic",
            ],
            "facts": [
                "On Saturday they go to the cinema.",
                "After the film they walk in the park.",
                "On Sunday Nora calls her grandma.",
                "The family has a picnic in the garden.",
            ],
        },
        "school_day": {
            "full_text": (
                "Yesterday was a long school day for Jade. She had five lessons before lunch. "
                "In the morning she had maths and English with her class. "
                "At break she ate an apple in the yard with her friends. "
                "After lunch there was history and art. The teacher gave tasks in three subjects. "
                "Jade wrote the tasks in her diary carefully. "
                "In the evening she finished the homework at her desk. She felt tired but happy."
            ),
            "gapped_text": (
                "Yesterday was a long school day for Jade. She had five (1)___ before lunch. "
                "In the morning she had (2)___ and English with her class. "
                "At (3)___ she ate an apple in the yard with her friends. "
                "After lunch there was history and art. The (4)___ gave tasks in three subjects. "
                "Jade wrote the tasks in her diary carefully. "
                "In the evening she finished the (5)___ at her desk. She felt tired but happy."
            ),
            "answers": ["lessons", "maths", "break", "teacher", "homework"],
            "word_bank": ["lessons", "maths", "break", "teacher", "homework", "garden"],
            "questions": [
                {
                    "q": "How many lessons did Jade have before lunch?",
                    "accept": ["five", "5", "five lessons"],
                    "hint_ru": "Сколько уроков было до обеда?",
                    "quote": "She had five lessons before lunch.",
                    "model_en": "Jade had five lessons before lunch.",
                },
                {
                    "q": "What subjects did she have in the morning?",
                    "accept": ["maths and English", "maths", "English"],
                    "hint_ru": "Какие предметы были утром?",
                    "quote": "…she had maths and English…",
                    "model_en": "In the morning she had maths and English.",
                },
                {
                    "q": "What did she eat at break?",
                    "accept": ["an apple", "apple"],
                    "hint_ru": "Что она ела на перемене?",
                    "quote": "…ate an apple in the yard…",
                    "model_en": "She ate an apple at break.",
                },
                {
                    "q": "When did she finish the homework?",
                    "accept": ["in the evening", "evening"],
                    "hint_ru": "Когда она закончила домашнее задание?",
                    "quote": "In the evening she finished the homework…",
                    "model_en": "She finished the homework in the evening.",
                },
            ],
            "plan": [
                "Five lessons before lunch",
                "Morning subjects and break",
                "Afternoon history and art",
                "Evening homework",
            ],
            "facts": [
                "Jade had five lessons before lunch.",
                "Morning subjects were maths and English.",
                "At break she ate an apple.",
                "She finished homework in the evening.",
            ],
        },
        "weather": {
            "full_text": (
                "Yesterday the weather was rainy — water fell from the sky — and cold. "
                "Mia wore a warm coat and took an umbrella. "
                "She walked to the bus stop slowly. Today the sky is blue and the sun is bright. "
                "Mia puts it back in the hall. She chooses a light jacket instead of the coat. "
                "Her brother wants to play football outside. Mum says they can go if it stays sunny. "
                "In the evening it may become windy. Mia checks the weather again before dinner."
            ),
            "gapped_text": (
                "Yesterday the weather was (1)___ — water fell from the sky — and (2)___. "
                "Mia wore a warm coat and took an (3)___. "
                "She walked to the bus stop slowly. Today the sky is blue and the sun is bright. "
                "Mia puts it back in the hall. She chooses a light (4)___ instead of the coat. "
                "Her brother wants to play football outside. Mum says they can go if it stays (5)___. "
                "In the evening it may become windy. Mia checks the weather again before dinner."
            ),
            "answers": ["rainy", "cold", "umbrella", "jacket", "sunny"],
            "word_bank": ["rainy", "cold", "umbrella", "jacket", "sunny", "snowy"],
            "questions": [
                {
                    "q": "What was the weather like yesterday?",
                    "accept": ["rainy and cold", "rainy", "cold"],
                    "hint_ru": "Какая была погода вчера?",
                    "quote": "Yesterday the weather was rainy — water fell from the sky — and cold.",
                    "model_en": "Yesterday the weather was rainy and cold.",
                },
                {
                    "q": "What does Mia choose today instead of the coat?",
                    "accept": ["light jacket", "jacket", "a light jacket"],
                    "hint_ru": "Что она выбирает вместо пальто?",
                    "quote": "…a light jacket instead of the coat.",
                    "model_en": "Mia chooses a light jacket instead of the coat.",
                },
                {
                    "q": "When can her brother play outside?",
                    "accept": ["if it stays sunny", "if sunny", "when sunny"],
                    "hint_ru": "Когда брат может играть на улице?",
                    "quote": "…if it stays sunny.",
                    "model_en": "They can go if it stays sunny.",
                },
                {
                    "q": "What may the evening become?",
                    "accept": ["windy", "become windy"],
                    "hint_ru": "Каким может стать вечер?",
                    "quote": "In the evening it may become windy.",
                    "model_en": "The evening may become windy.",
                },
            ],
            "plan": [
                "Yesterday rainy and cold",
                "Umbrella and coat",
                "Today jacket and sunny plans",
                "Evening may be windy",
            ],
            "facts": [
                "Yesterday was rainy and cold; Mia took an umbrella.",
                "Today she chooses a light jacket.",
                "Brother can play outside if it stays sunny.",
                "Evening may become windy.",
            ],
        },
    },
}
