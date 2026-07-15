"""Build data/vocab_banks_high.py with validated A2–C2 words and phrases."""
from __future__ import annotations

from pathlib import Path

from data.vocabulary_words import WORDS as A0A1_WORDS, _e

ROOT = Path(__file__).resolve().parent


def pack(items: list[tuple[str, str, str]]) -> list[dict]:
    return [_e(en, ru, em) for en, ru, em in items]


def dedupe_topic(items: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen: set[str] = set()
    out: list[tuple[str, str, str]] = []
    for en, ru, em in items:
        key = en.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        out.append((en, ru, em))
    return out


def load_existing_en() -> set[str]:
    seen: set[str] = set()
    for level_words in A0A1_WORDS.values():
        for topic_words in level_words.values():
            for w in topic_words:
                seen.add(w["en"].strip().lower())
    return seen


def filter_global(
    items: list[tuple[str, str, str]], global_seen: set[str]
) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for en, ru, em in items:
        key = en.strip().lower()
        if key in global_seen:
            continue
        global_seen.add(key)
        out.append((en, ru, em))
    return out


# ── A2 words (fixed typos, deduped) ────────────────────────────────────────
A2_RAW: dict[str, list[tuple[str, str, str]]] = {
    "family": [
        ("in-law", "свёкор/свекровь", "👪"), ("orphan", "сирота", "🧒"), ("widow", "вдова", "👩"),
        ("widower", "вдовец", "👨"), ("sibling", "брат или сестра", "👫"), ("upbringing", "воспитание", "🌱"),
        ("household", "домохозяйство", "🏠"), ("ancestor", "предок", "🌳"), ("descendant", "потомок", "🌿"),
        ("foster", "приёмный", "🏠"), ("guardian", "опекун", "🛡️"), ("reunion", "семейная встреча", "🎉"),
        ("quarrel", "ссора", "😠"), ("generation gap", "конфликт поколений", "↔️"), ("inheritance", "наследство", "💰"),
        ("to inherit", "наследовать", "💰"), ("to adopt", "усыновлять", "👶"), ("to babysit", "присматривать за детьми", "👶"),
        ("to rely on", "полагаться на", "🤝"), ("to fall out", "поссориться", "😠"), ("bond", "узы", "🔗"),
        ("closeness", "близость", "🫂"), ("estranged", "отчуждённый", "🚪"), ("maternity", "материнство", "🤱"),
        ("engagement", "помолвка", "💍"), ("custody", "опека", "⚖️"), ("kinship", "родство", "🧬"),
        ("lineage", "родословная", "🌳"), ("breadwinner", "кормилец", "💼"), ("dependant", "иждивенец", "🧒"),
        ("family values", "семейные ценности", "❤️"), ("stepchild", "пасынок или падчерица", "👶"),
        ("single parent", "одинокий родитель", "1️⃣"), ("annulment", "аннулирование брака", "📄"),
        ("to reconcile", "мириться", "🤝"), ("nuclear family", "семья из родителей и детей", "👨‍👩‍👧"),
        ("paternity", "отцовство", "👨"), ("relatives", "родственники", "👪"), ("stepfather", "отчим", "👨"),
        ("stepmother", "мачеха", "👩"), ("twins", "близнецы", "👯"), ("only child", "единственный ребёнок", "1️⃣"),
    ],
    "home": [
        ("mortgage", "ипотека", "🏦"), ("renovation", "ремонт", "🔨"), ("landlord", "арендодатель", "🧑‍💼"),
        ("tenant", "арендатор", "🔑"), ("lease", "договор аренды", "📄"), ("utility", "коммунальные услуги", "💡"),
        ("insulation", "утепление", "🧱"), ("plumbing", "сантехника", "🚿"), ("wiring", "электропроводка", "⚡"),
        ("bungalow", "бунгало", "🏠"), ("loft", "чердак", "⬆️"), ("cellar", "погреб", "⬇️"),
        ("driveway", "подъездная дорога", "🚗"), ("fence", "забор", "🚧"), ("to mow", "косить газон", "🌿"),
        ("to vacuum", "пылесосить", "🧹"), ("to dust", "вытирать пыль", "🧽"), ("to leak", "течь", "💧"),
        ("leak", "протечка", "💧"), ("damp", "сырой", "💧"), ("mould", "плесень", "🦠"),
        ("furnished", "меблированный", "🛋️"), ("unfurnished", "без мебели", "📦"), ("cramped", "тесный", "📦"),
        ("suburb", "пригород", "🏘️"), ("commute", "дорога на работу", "🚆"), ("to renovate", "делать ремонт", "🔨"),
        ("maintenance", "обслуживание", "🔧"), ("property", "недвижимость", "🏠"), ("rent", "арендная плата", "💰"),
        ("to sublet", "сдавать в субаренду", "🔑"), ("housewarming", "новоселье", "🎊"), ("detached", "отдельный дом", "🏡"),
        ("semi-detached", "смежный дом", "🏘️"), ("neighbourhood", "район", "🏘️"), ("to weed", "пропалывать", "🌱"),
        ("weed", "сорняк", "🌱"), ("utility bill", "коммунальный счёт", "🧾"), ("garage", "гараж", "🚗"),
        ("attic fan", "чердачный вентилятор", "💨"), ("doorbell", "дверной звонок", "🔔"), ("radiator", "радиатор", "🔥"),
    ],
    "work": [
        ("shift", "смена", "🕐"), ("overtime", "сверхурочные", "⏰"), ("workload", "нагрузка", "📊"),
        ("employer", "работодатель", "🏢"), ("employee", "сотрудник", "👤"), ("workplace", "рабочее место", "🏢"),
        ("profession", "профессия", "💼"), ("trade", "ремесло", "🔧"), ("qualification", "квалификация", "📜"),
        ("apprentice", "ученик", "🎓"), ("retirement", "выход на пенсию", "👴"), ("redundancy", "сокращение", "📉"),
        ("to resign", "уволиться", "📝"), ("to fire", "уволить", "🚪"), ("to promote", "повышать", "⬆️"),
        ("to demote", "понижать", "⬇️"), ("to delegate", "делегировать", "👥"), ("to supervise", "контролировать", "👀"),
        ("to negotiate", "вести переговоры", "🤝"), ("union", "профсоюз", "✊"), ("strike", "забастовка", "✊"),
        ("probation", "испытательный срок", "📋"), ("permanent", "постоянный", "✅"), ("temporary", "временный", "⏱️"),
        ("freelance", "фриланс", "💻"), ("remote work", "удалённая работа", "🏠"), ("payslip", "расчётный лист", "🧾"),
        ("bonus", "бонус", "💰"), ("benefits", "льготы", "🎁"), ("pension", "пенсия", "👴"),
        ("to commute", "ездить на работу", "🚇"), ("to retire", "выходить на пенсию", "👴"), ("to recruit", "нанимать", "📢"),
        ("to interview", "проводить собеседование", "🎤"), ("work-life balance", "баланс работы и жизни", "⚖️"),
        ("deadline", "дедлайн", "⏳"), ("colleague", "коллега", "🤝"), ("contract", "контракт", "📄"),
        ("redundant", "сокращённый", "📉"), ("part-time", "неполный рабочий день", "⏱️"), ("full-time", "полный рабочий день", "💼"),
        ("job interview", "собеседование", "🎤"), ("CV", "резюме", "📄"),
    ],
    "city": [
        ("pedestrian", "пешеход", "🚶"), ("crossing", "переход", "🚸"), ("junction", "перекрёсток", "🔀"),
        ("roundabout", "круговое движение", "🔄"), ("pavement", "тротуар", "🚶"), ("subway", "метро", "🚇"),
        ("tram", "трамвай", "🚊"), ("fare", "плата за проезд", "🎫"), ("congestion", "пробка", "🚗"),
        ("pollution", "загрязнение", "🏭"), ("skyscraper", "небоскрёб", "🏙️"), ("district", "район", "📍"),
        ("downtown", "центр города", "🏙️"), ("outskirts", "окраина", "🌆"), ("landmark", "достопримечательность", "🗽"),
        ("statue", "статуя", "🗿"), ("monument", "памятник", "🗿"), ("fountain", "фonтан", "⛲"),
        ("boulevard", "бульвар", "🌳"), ("alley", "переулок", "🏘️"), ("to park", "парковать", "🅿️"),
        ("parking", "парковка", "🅿️"), ("cycle lane", "велодорожка", "🚴"), ("public transport", "общественный транспорт", "🚌"),
        ("rush hour", "час пик", "⏰"), ("to litter", "мусорить", "🗑️"), ("construction", "строительство", "🏗️"),
        ("to demolish", "сносить", "💥"), ("urban", "городской", "🏙️"), ("rural", "сельский", "🌾"),
        ("population", "население", "👥"), ("inhabitant", "житель", "🧑"), ("cosmopolitan", "космополитичный", "🌍"),
        ("housing estate", "жилой массив", "🏘️"), ("pedestrian zone", "пешеходная зона", "🚶"),
        ("commuter", "пассажир-пendler", "🚆"), ("metropolitan", "столичный", "🏙️"), ("town hall", "ратуша", "🏛️"),
        ("street vendor", "уличный торговец", "🛒"), ("one-way street", "улица с односторонним движением", "➡️"),
        ("city council", "городской совет", "🏛️"), ("streetlight", "фонарь", "💡"),
    ],
    "travel": [
        ("itinerary", "маршрут", "🗺️"), ("layover", "пересадка", "✈️"), ("excursion", "экскурсия", "🚌"),
        ("cruise", "круиз", "🚢"), ("backpack", "рюкзак", "🎒"), ("resort", "курорт", "🏖️"),
        ("peak season", "высокий сезон", "📈"), ("off season", "низкий сезон", "📉"), ("all-inclusive", "всё включено", "🍹"),
        ("sightseeing", "осмотр достопримечательностей", "📸"), ("guidebook", "путеводитель", "📖"),
        ("to trek", "идти в поход", "🥾"), ("trek", "поход", "🥾"), ("cancellation", "отмена", "❌"),
        ("overbooked", "перебронирование", "📅"), ("departure", "отправление", "🛫"), ("arrival", "прибытие", "🛬"),
        ("terminal", "терминал", "🏢"), ("gate", "выход на посадку", "🚪"), ("boarding pass", "посадочный талон", "🎫"),
        ("duty-free", "duty-free", "🛍️"), ("immigration", "иммиграционный контроль", "🛂"),
        ("to immigrate", "иммигрировать", "🌍"), ("to emigrate", "эмигрировать", "🌍"), ("expat", "экспат", "🌍"),
        ("scenery", "пейзаж", "🏞️"), ("landscape", "ландшафт", "🏞️"), ("coastal", "прибрежный", "🏖️"),
        ("inland", "в глубине страны", "🏔️"), ("to postpone", "откладывать", "📅"), ("stopover", "остановка по пути", "⏸️"),
        ("self-catering", "самостоятельное питание", "🍳"), ("to cancel", "отменять", "❌"), ("nomad", "кочевник", "🎒"),
        ("to wander", "бродить", "🚶"), ("hostel", "хостел", "🛏️"), ("guesthouse", "гостевой дом", "🏠"),
        ("to hitchhike", "путешествовать автостопом", "👍"), ("customs", "таможня", "🛃"), ("visa", "виза", "📄"),
        ("travel insurance", "страховка для путешествий", "🛡️"),
    ],
    "health": [
        ("chronic", "хронический", "📅"), ("acute", "острый", "⚡"), ("diagnosis", "диагноз", "📋"),
        ("prognosis", "прогноз", "🔮"), ("therapy", "терапия", "💊"), ("surgeon", "хирург", "🔪"),
        ("operation", "операция", "🏥"), ("ward", "палата", "🛏️"), ("clinic", "клиника", "🏥"),
        ("pharmacy", "аптека", "💊"), ("dosage", "дозировка", "💊"), ("side effect", "побочный эффект", "⚠️"),
        ("recovery", "выздоровление", "🌱"), ("relapse", "рецидив", "🔄"), ("immune", "иммунный", "🛡️"),
        ("infection", "инфекция", "🦠"), ("bacteria", "бактерии", "🦠"), ("vaccine", "вакцина", "💉"),
        ("to vaccinate", "вакцинировать", "💉"), ("to prescribe", "выписывать лекарство", "📜"),
        ("to diagnose", "диагностировать", "🔍"), ("to operate", "оперировать", "🔪"), ("insomnia", "бессонница", "😴"),
        ("anxiety", "тревога", "😰"), ("depression", "депрессия", "😔"), ("wellness", "благополучие", "🌿"),
        ("nutrition", "питание", "🥗"), ("hydration", "гидратация", "💧"), ("posture", "осанка", "🧍"),
        ("to stretch", "растягиваться", "🤸"), ("first aid", "первая помощь", "🩹"), ("paramedic", "фельдшер", "🚑"),
        ("wheelchair", "коляска", "♿"), ("disability", "инвалидность", "♿"), ("rehabilitation", "реабилитация", "🏥"),
        ("symptom", "симптом", "🤒"), ("prescription", "рецепт врача", "📜"), ("virus", "вирус", "🦠"),
        ("therapy session", "сессия терапии", "🛋️"), ("stretch", "растяжка", "🤸"), ("blood pressure", "кровяное давление", "❤️"),
        ("check-up", "медосмотр", "🩺"),
    ],
    "technology": [
        ("device", "устройство", "📱"), ("gadget", "гаджет", "⌚"), ("software", "программное обеспечение", "💻"),
        ("hardware", "железо", "🖥️"), ("update", "обновление", "🔄"), ("download", "скачивание", "⬇️"),
        ("upload", "загрузка", "⬆️"), ("browser", "браузер", "🌐"), ("password", "пароль", "🔐"),
        ("username", "имя пользователя", "👤"), ("to hack", "взламывать", "💻"), ("hacker", "хacker", "🕵️"),
        ("firewall", "файрвол", "🛡️"), ("cloud", "облако", "☁️"), ("backup", "резервная копия", "💾"),
        ("to backup", "делать бэкап", "💾"), ("wireless", "беспроводной", "📶"), ("bluetooth", "Bluetooth", "📶"),
        ("charger", "зарядное устройство", "🔌"), ("battery", "батарея", "🔋"), ("screen", "экран", "🖥️"),
        ("keyboard", "клавиатура", "⌨️"), ("mouse", "мышь", "🖱️"), ("printer", "принтер", "🖨️"),
        ("router", "роутер", "📡"), ("bandwidth", "пропускная способность", "📊"), ("stream", "стрим", "📺"),
        ("to stream", "стримить", "📺"), ("app", "приложение", "📱"), ("notification", "уведомление", "🔔"),
        ("algorithm", "алгоритм", "🧮"), ("artificial intelligence", "искусственный интеллект", "🤖"),
        ("virtual", "виртуальный", "🥽"), ("to install", "устанавливать", "📥"), ("to uninstall", "удалять программу", "🗑️"),
        ("malware", "вредоносное ПО", "⚠️"), ("phishing", "фишинг", "🎣"), ("to encrypt", "шифровать", "🔐"),
        ("encrypt", "шифрование", "🔐"), ("smartphone", "смартфон", "📱"), ("laptop", "ноутбук", "💻"),
        ("touchscreen", "сенсорный экран", "👆"), ("Wi-Fi", "Wi-Fi", "📶"),
    ],
    "nature": [
        ("wildlife", "дикая природа", "🦁"), ("habitat", "среда обитания", "🌳"), ("ecosystem", "экосистема", "🌍"),
        ("species", "вид", "🦋"), ("extinct", "вымерший", "💀"), ("endangered", "под угрозой исчезновения", "⚠️"),
        ("preserve", "заповедник", "🌲"), ("meadow", "луг", "🌾"), ("valley", "долина", "🏞️"),
        ("peak", "вершина", "⛰️"), ("cliff", "скала", "🪨"), ("waterfall", "водопад", "💦"),
        ("creek", "ручей", "💧"), ("tide", "прилив", "🌊"), ("drought", "засуха", "☀️"),
        ("flood", "наводнение", "🌊"), ("earthquake", "землетрясение", "🌍"), ("volcano", "вулкан", "🌋"),
        ("hurricane", "ураган", "🌀"), ("breeze", "лёгкий ветер", "🌬️"), ("forecast", "прогноз погоды", "📡"),
        ("humidity", "влажность", "💧"), ("frost", "мороз", "❄️"), ("thunder", "гром", "⚡"),
        ("lightning", "молния", "⚡"), ("rainbow", "радуга", "🌈"), ("sunrise", "рассвет", "🌅"),
        ("sunset", "закат", "🌇"), ("to recycle", "перерабатывать", "♻️"), ("renewable", "возобновляемый", "♻️"),
        ("solar", "солнечный", "☀️"), ("wind power", "ветроэнергия", "💨"), ("conservation", "охрана природы", "🌿"),
        ("to plant", "сажать", "🌱"), ("to harvest", "собирать урожай", "🌾"), ("biodiversity", "биоразнообразие", "🦋"),
        ("forest", "лес", "🌲"), ("pesticide", "пестицид", "⚠️"), ("organic farming", "органическое farming", "🌿"),
        ("global warming", "глобальное потепление", "🌡️"), ("glacier", "ледник", "🏔️"), ("coral reef", "коралловый риф", "🪸"),
    ],
}

# Import remaining level data from companion module (keeps file manageable)
from data._vocab_high_b1_c2 import B1_RAW, B2_RAW, C1_RAW, C2_RAW, PHRASES_RAW  # noqa: E402

ALL_WORD_RAW = {"A2": A2_RAW, "B1": B1_RAW, "B2": B2_RAW, "C1": C1_RAW, "C2": C2_RAW}


def build_words() -> dict:
    global_seen = load_existing_en()
    result: dict = {}
    for level, topics in ALL_WORD_RAW.items():
        result[level] = {}
        for topic, raw in topics.items():
            items = dedupe_topic(raw)
            items = filter_global(items, global_seen)
            if len(items) < 35:
                raise ValueError(f"{level}/{topic}: only {len(items)} words after dedup")
            result[level][topic] = pack(items[:45])
    return result


def build_phrases() -> dict:
    result: dict = {}
    for level, topics in PHRASES_RAW.items():
        result[level] = {}
        for topic, raw in topics.items():
            items = dedupe_topic(raw)
            if len(items) < 12:
                raise ValueError(f"phrases {level}/{topic}: only {len(items)}")
            result[level][topic] = pack(items[:12])
    return result


def write_output(high_words: dict, high_phrases: dict) -> None:
    out = ROOT / "vocab_banks_high.py"
    lines = [
        '"""A2–C2 vocabulary banks (words and phrases)."""',
        "from __future__ import annotations",
        "",
        "from data.vocabulary_words import _e",
        "",
        "HIGH_WORDS: dict[str, dict[str, list[dict]]] = " + repr(high_words),
        "",
        "HIGH_PHRASES: dict[str, dict[str, list[dict]]] = " + repr(high_phrases),
        "",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


def print_stats(high_words: dict) -> None:
    for level in "A2 B1 B2 C1 C2".split():
        total = sum(len(v) for v in high_words[level].values())
        print(f"{level}: {total} words ({len(high_words[level])} topics)")


if __name__ == "__main__":
    words = build_words()
    phrases = build_phrases()
    write_output(words, phrases)
    print_stats(words)
