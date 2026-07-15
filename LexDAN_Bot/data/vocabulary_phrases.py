"""
Устойчивые фразы Vocabulary A0–C2.
"""

from __future__ import annotations

from data.vocabulary_words import _e as _p


PHRASES: dict[str, dict[str, list[dict]]] = {
    "A0": {
        "greetings": [
            _p("Nice to meet you", "Приятно познакомиться", "🤝"),
            _p("How are you?", "Как дела?", "👋"),
            _p("See you later", "Увидимся позже", "👋"),
            _p("Good morning", "Доброе утро", "🌅"),
            _p("Good night", "Спокойной ночи", "🌙"),
            _p("You're welcome", "Пожалуйста (на спасибо)", "😊"),
            _p("Excuse me", "Извините", "🙇"),
            _p("What's your name?", "Как тебя зовут?", "📛"),
            _p("My name is...", "Меня зовут...", "🙂"),
            _p("Have a nice day", "Хорошего дня", "☀️"),
            _p("Long time no see", "Давно не виделись", "⏰"),
            _p("Take care", "Береги себя", "💛"),
        ],
        "family": [
            _p("I love my family", "Я люблю свою семью", "❤️"),
            _p("How old are you?", "Сколько тебе лет?", "🎂"),
            _p("This is my mother", "Это моя мама", "👩"),
            _p("We live together", "Мы живём вместе", "🏠"),
            _p("Family first", "Семья — главное", "👨‍👩‍👧"),
            _p("Happy birthday!", "С днём рождения!", "🎉"),
            _p("I miss you", "Я скучаю по тебе", "💭"),
            _p("Call me later", "Позвони мне позже", "📞"),
            _p("My big brother", "Мой старший брат", "👦"),
            _p("She is my sister", "Она моя сестра", "👧"),
            _p("We are friends", "Мы друзья", "🤝"),
            _p("Come here", "Иди сюда", "👋"),
        ],
        "home": [
            _p("At home", "Дома", "🏠"),
            _p("Open the door", "Открой дверь", "🚪"),
            _p("Close the window", "Закрой окно", "🪟"),
            _p("I'm at home", "Я дома", "🏡"),
            _p("Make yourself at home", "Чувствуй себя как дома", "🛋️"),
            _p("Turn on the light", "Включи свет", "💡"),
            _p("Go to bed", "Иди спать", "🛏️"),
            _p("In the kitchen", "На кухне", "🍳"),
            _p("Clean the room", "Убери комнату", "🧹"),
            _p("Home sweet home", "Дом, милый дом", "🏠"),
            _p("Upstairs", "Наверху", "⬆️"),
            _p("Sit down, please", "Садись, пожалуйста", "🪑"),
        ],
        "food": [
            _p("I'm hungry", "Я голоден", "😋"),
            _p("I'm thirsty", "Мне хочется пить", "🥤"),
            _p("Bon appetit", "Приятного аппетита", "🍽️"),
            _p("A cup of tea", "Чашка чая", "☕"),
            _p("For breakfast", "На завтрак", "🌅"),
            _p("I like pizza", "Мне нравится пицца", "🍕"),
            _p("Can I have water?", "Можно воды?", "💧"),
            _p("It's delicious", "Это вкусно", "😋"),
            _p("Too hot", "Слишком горячее", "🔥"),
            _p("Fast food", "Фастфуд", "🍔"),
            _p("Eat well", "Хорошо ешь", "🥗"),
            _p("Help yourself", "Угощайся", "🍽️"),
        ],
        "colors_numbers": [
            _p("What color is it?", "Какого это цвета?", "🎨"),
            _p("How many?", "Сколько?", "🔢"),
            _p("A lot of", "Много", "📦"),
            _p("A little", "Немного", "🤏"),
            _p("Red and blue", "Красный и синий", "🔴"),
            _p("Number one", "Номер один", "1️⃣"),
            _p("Count to ten", "Сосчитай до десяти", "🔟"),
            _p("The first time", "В первый раз", "1️⃣"),
            _p("Black and white", "Чёрно-белый", "⬛"),
            _p("Light green", "Светло-зелёный", "🟢"),
            _p("Too many", "Слишком много", "📈"),
            _p("Not enough", "Недостаточно", "📉"),
        ],
    },
    "A1": {
        "family": [
            _p("Blood is thicker than water", "Семья — главнее всего", "❤️"),
            _p("Like father, like son", "Яблоко от яблони", "👨‍👦"),
            _p("Get along with", "Ладить с", "🤝"),
            _p("Fall out with", "Поссориться с", "😠"),
            _p("Bring up children", "Воспитывать детей", "👶"),
            _p("Extended family", "Расширенная семья", "👪"),
            _p("Immediate family", "Близкие родственники", "🏠"),
            _p("Family gathering", "Семейная встреча", "🎉"),
            _p("Keep in touch", "Поддерживать связь", "📱"),
            _p("Split up", "Расстаться", "💔"),
            _p("Get married", "Пожениться", "💍"),
            _p("Grow up together", "Расти вместе", "🌱"),
        ],
        "home": [
            _p("Make yourself comfortable", "Устраивайся поудобнее", "🛋️"),
            _p("Run out of", "Закончиться (о запасах)", "📦"),
            _p("Fix the tap", "Починить кран", "🔧"),
            _p("Move house", "Переехать", "📦"),
            _p("Rent a flat", "Снять квартиру", "🔑"),
            _p("Pay the bills", "Платить по счетам", "🧾"),
            _p("Spring cleaning", "Генеральная уборка", "🧹"),
            _p("Out of order", "Не работает", "⚠️"),
            _p("On the top floor", "На верхнем этаже", "⬆️"),
            _p("Next door", "По соседству", "🚪"),
            _p("Housewarming party", "Новоселье", "🎊"),
            _p("Feel at home", "Чувствовать себя как дома", "🏠"),
        ],
        "work_school": [
            _p("Apply for a job", "Подать заявку на работу", "📄"),
            _p("Work overtime", "Работать сверхурочно", "⏰"),
            _p("Hand in homework", "Сдать домашку", "📓"),
            _p("Pass an exam", "Сдать экзамен", "✅"),
            _p("Fail a test", "Провалить тест", "❌"),
            _p("On time", "Вовремя", "⏰"),
            _p("Day off", "Выходной", "📅"),
            _p("Team player", "Командный игрок", "👥"),
            _p("Learn by heart", "Выучить наизусть", "🧠"),
            _p("Make progress", "Делать успехи", "📈"),
            _p("Drop out", "Бросить (учёбу)", "🚪"),
            _p("Career path", "Карьерный путь", "🛤️"),
        ],
        "food": [
            _p("Help yourself to", "Угощайся", "🍽️"),
            _p("Eat out", "Есть вне дома", "🍽️"),
            _p("Fast food", "Фастфуд", "🍔"),
            _p("Home-cooked meal", "Домашняя еда", "🏠"),
            _p("Cut down on sugar", "Меньше сахара", "🍬"),
            _p("Allergic to nuts", "Аллергия на орехи", "🥜"),
            _p("Split the bill", "Разделить счёт", "🧾"),
            _p("Book a table", "Забронировать стол", "📞"),
            _p("Grab a bite", "Перекусить", "🥪"),
            _p("Comfort food", "Еда для души", "🍲"),
            _p("Go on a diet", "Сесть на диету", "🥗"),
            _p("Spoil your appetite", "Испортить аппетит", "🍬"),
        ],
        "travel": [
            _p("Check in", "Зарегистрироваться (отель/рейс)", "✅"),
            _p("Set off", "Отправиться", "🚀"),
            _p("Look forward to", "С нетерпением ждать", "✈️"),
            _p("Get lost", "Заблудиться", "🗺️"),
            _p("Travel light", "Путешествовать налегке", "🎒"),
            _p("Off the beaten track", "Вдали от туристов", "🏕️"),
            _p("Culture shock", "Культурный шок", "🌍"),
            _p("Jet lag", "Джетлаг", "😴"),
            _p("Round trip", "Туда и обратно", "🔄"),
            _p("Travel agency", "Тур агентство", "🏢"),
            _p("Border control", "Погранконтроль", "🛂"),
            _p("Once in a lifetime", "Раз в жизни", "⭐"),
        ],
        "body_health": [
            _p("Feel under the weather", "Чувствовать себя плохо", "🤒"),
            _p("Get over a cold", "Оправиться от простуды", "🤧"),
            _p("See a doctor", "Пойти к врачу", "👨‍⚕️"),
            _p("Take medicine", "Принимать лекарство", "💊"),
            _p("Stay in shape", "Быть в форме", "💪"),
            _p("Work out", "Тренироваться", "🏋️"),
            _p("Burn out", "Выгореть", "🔥"),
            _p("Get some rest", "Отдохнуть", "😴"),
            _p("Break a leg", "Удачи! (театр.)", "🍀"),
            _p("Pain in the neck", "Боль в шее / зануда", "😤"),
            _p("Fit as a fiddle", "В отличной форме", "💪"),
            _p("An apple a day", "Яблоко в день — и здоров", "🍎"),
        ],
        "hobbies": [
            _p("Free time", "Свободное время", "⏰"),
            _p("Take up a hobby", "Начать хобби", "🎯"),
            _p("Kill time", "Убить время", "⏳"),
            _p("Hang out", "Тусоваться", "👥"),
            _p("Chill out", "Расслабиться", "😌"),
            _p("Passion for music", "Страсть к музыке", "🎵"),
            _p("Pick up a skill", "Освоить навык", "🛠️"),
            _p("Once in a while", "Время от времени", "📅"),
            _p("On weekends", "По выходным", "📅"),
            _p("Creative outlet", "Творческий выход", "🎨"),
            _p("Team spirit", "Командный дух", "⚽"),
            _p("Break a record", "Побить рекорд", "🏆"),
        ],
        "shopping": [
            _p("On sale", "На распродаже", "🏷️"),
            _p("Bargain price", "Выгодная цена", "💸"),
            _p("Try it on", "Примерить", "👕"),
            _p("Fit perfectly", "Идеально сидит", "✨"),
            _p("Cash or card?", "Наличные или карта?", "💳"),
            _p("Keep the receipt", "Сохрани чек", "🧾"),
            _p("Return policy", "Политика возврата", "↩️"),
            _p("Out of stock", "Нет в наличии", "❌"),
            _p("Window shopping", "Просто смотреть витрины", "🪟"),
            _p("Impulse buy", "Импульсная покупка", "🛍️"),
            _p("Shop around", "Сравнивать цены", "🔍"),
            _p("Good value for money", "Хорошая цена/качество", "👍"),
        ],
    },
}


def has_vocabulary_level(level: str) -> bool:
    _ensure_high_phrases()
    return level in PHRASES and bool(PHRASES[level])


def get_phrases(level: str, topic_id: str) -> list[dict]:
    _ensure_high_phrases()
    return list(PHRASES.get(level, {}).get(topic_id, []))


def get_phrase_entry(level: str, topic_id: str, en: str) -> dict | None:
    key = (en or "").strip().lower()
    for p in get_phrases(level, topic_id):
        if p["en"].lower() == key:
            return p
    return None


def phrases_total(level: str, topic_id: str) -> int:
    return len(get_phrases(level, topic_id))


_HIGH_PHRASES_LOADED = False


def _ensure_high_phrases() -> None:
    global _HIGH_PHRASES_LOADED
    if _HIGH_PHRASES_LOADED:
        return
    from data.vocab_high import HIGH_PHRASES

    PHRASES.update(HIGH_PHRASES)
    _HIGH_PHRASES_LOADED = True
