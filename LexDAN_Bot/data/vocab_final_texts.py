"""
Заранее подготовленные тексты для итогового теста Vocabulary (EN → RU).
По 2 варианта на уровень — выбираем случайно.
"""

FINAL_TEXTS: dict[str, list[dict[str, str]]] = {
    "A0": [
        {
            "en": (
                "Hello! My name is Anna. I have a friend. "
                "Today is a good morning. Please help me. Thank you!"
            ),
            "ru": (
                "Привет! Меня зовут Анна. У меня есть друг. "
                "Сегодня хорошее утро. Пожалуйста, помоги мне. Спасибо!"
            ),
        },
        {
            "en": (
                "Good evening! Nice to meet you. "
                "I am fine. See you tomorrow. Bye!"
            ),
            "ru": (
                "Добрый вечер! Приятно познакомиться. "
                "У меня всё хорошо. Увидимся завтра. Пока!"
            ),
        },
    ],
    "A1": [
        {
            "en": (
                "I live in a small flat near the park. "
                "Every morning I drink coffee and go to work by bus. "
                "In the evening I cook dinner and watch a film with my family."
            ),
            "ru": (
                "Я живу в маленькой квартире рядом с парком. "
                "Каждое утро я пью кофе и еду на работу на автобусе. "
                "Вечером я готовлю ужин и смотрю фильм с семьёй."
            ),
        },
        {
            "en": (
                "My brother likes music and sports. "
                "On weekends we play football in the park. "
                "After that we buy food in the shop and talk about our day."
            ),
            "ru": (
                "Мой брат любит музыку и спорт. "
                "По выходным мы играем в футбол в парке. "
                "После этого мы покупаем еду в магазине и говорим о своём дне."
            ),
        },
    ],
    "A2": [
        {
            "en": (
                "Last summer I travelled to another city with my friends. "
                "We stayed in a cheap hotel and visited many museums. "
                "Although the weather was rainy, we still enjoyed the trip a lot."
            ),
            "ru": (
                "Прошлым летом я ездил в другой город с друзьями. "
                "Мы остановились в дешёвом отеле и посетили много музеев. "
                "Хотя погода была дождливой, мы всё равно очень насладились поездкой."
            ),
        },
        {
            "en": (
                "I usually wake up early because I have important meetings. "
                "Sometimes I feel tired, but I try to stay positive. "
                "In the evening I prefer to read a book instead of scrolling on my phone."
            ),
            "ru": (
                "Я обычно встаю рано, потому что у меня важные встречи. "
                "Иногда я чувствую себя уставшим, но стараюсь оставаться позитивным. "
                "Вечером я предпочитаю читать книгу, а не листать ленту в телефоне."
            ),
        },
    ],
    "B1": [
        {
            "en": (
                "Working remotely has changed how people manage their time. "
                "Some enjoy the flexibility, while others miss office conversations. "
                "In my opinion, a mixed schedule can offer the best of both worlds."
            ),
            "ru": (
                "Удалённая работа изменила то, как люди управляют своим временем. "
                "Кому-то нравится гибкость, а кто-то скучает по разговорам в офисе. "
                "На мой взгляд, смешанный график может дать лучшее из обоих миров."
            ),
        },
        {
            "en": (
                "Learning a language requires patience and regular practice. "
                "Mistakes are normal, and they often help you improve faster. "
                "If you stay curious, progress will come sooner than you expect."
            ),
            "ru": (
                "Изучение языка требует терпения и регулярной практики. "
                "Ошибки — это нормально, и они часто помогают улучшаться быстрее. "
                "Если оставаться любопытным, прогресс придёт раньше, чем ты ожидаешь."
            ),
        },
    ],
    "B2": [
        {
            "en": (
                "Many cities struggle to balance economic growth with environmental protection. "
                "Public transport investments can reduce pollution and improve daily life. "
                "However, lasting change also depends on citizens' everyday choices."
            ),
            "ru": (
                "Многие города пытаются совместить экономический рост с защитой окружающей среды. "
                "Инвестиции в общественный транспорт могут снизить загрязнение и улучшить повседневную жизнь. "
                "Однако устойчивые изменения также зависят от ежедневных решений самих жителей."
            ),
        },
        {
            "en": (
                "Social media can connect people across cultures, yet it also spreads misleading information quickly. "
                "Developing media literacy helps users question sources before sharing. "
                "In the long run, critical thinking may matter more than speed."
            ),
            "ru": (
                "Соцсети могут связывать людей разных культур, но также быстро распространяют вводящую в заблуждение информацию. "
                "Медиаграмотность помогает пользователям проверять источники перед тем, как делиться. "
                "В долгосрочной перспективе критическое мышление может быть важнее скорости."
            ),
        },
    ],
    "C1": [
        {
            "en": (
                "Technological innovation often outpaces regulation, creating ethical grey areas. "
                "Policymakers must weigh privacy against convenience without stifling progress. "
                "Transparent public debate remains essential if societies hope to trust emerging tools."
            ),
            "ru": (
                "Технологические инновации часто опережают регулирование, создавая этические серые зоны. "
                "Законодателям приходится взвешивать приватность и удобство, не подавляя прогресс. "
                "Прозрачные общественные дискуссии остаются необходимыми, если общества хотят доверять новым инструментам."
            ),
        },
        {
            "en": (
                "Cultural identity is rarely fixed; it evolves through migration, education and shared stories. "
                "Rather than treating tradition as a museum piece, communities can reinterpret it creatively. "
                "This approach preserves continuity while remaining open to change."
            ),
            "ru": (
                "Культурная идентичность редко бывает фиксированной: она меняется через миграцию, образование и общие истории. "
                "Вместо того чтобы считать традицию музейным экспонатом, сообщества могут творчески её переосмыслять. "
                "Такой подход сохраняет преемственность и при этом остаётся открытым к переменам."
            ),
        },
    ],
    "C2": [
        {
            "en": (
                "Despite sophisticated forecasting models, uncertainty remains an unavoidable feature of complex systems. "
                "Leaders who acknowledge ambiguity tend to communicate more honestly with the public. "
                "Paradoxically, admitting limits of knowledge can strengthen institutional credibility."
            ),
            "ru": (
                "Несмотря на сложные прогнозные модели, неопределённость остаётся неизбежной чертой сложных систем. "
                "Лидеры, которые признают неоднозначность, обычно честнее общаются с обществом. "
                "Парадоксально, но признание пределов знания может укрепить доверие к институтам."
            ),
        },
        {
            "en": (
                "Literary translation is never a mechanical transfer of words; it is a negotiation of tone, rhythm and cultural resonance. "
                "A faithful rendering may still feel alien if it ignores the reader's expectations. "
                "The finest translations therefore recreate effect rather than merely mirror form."
            ),
            "ru": (
                "Литературный перевод — это никогда не механический перенос слов, а согласование тона, ритма и культурных оттенков. "
                "Даже верный перевод может ощущаться чужим, если игнорирует ожидания читателя. "
                "Поэтому лучшие переводы воссоздают эффект, а не просто зеркалят форму."
            ),
        },
    ],
}


def pick_final_text(level: str) -> dict[str, str]:
    import random

    items = FINAL_TEXTS.get(level) or FINAL_TEXTS["A1"]
    return dict(random.choice(items))
