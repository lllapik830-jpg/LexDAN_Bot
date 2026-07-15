"""
A2–C2 словари (слова + фразы). Собираются из raw-данных при импорте.
"""
from __future__ import annotations

from data.vocabulary_words import _e
from data.build_vocab_banks_high import A2_RAW
from data._vocab_high_b1_c2 import B1_RAW, B2_RAW, C1_RAW, C2_RAW, PHRASES_RAW


def _dedupe(items: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen: set[str] = set()
    out: list[tuple[str, str, str]] = []
    for en, ru, em in items:
        k = (en or "").strip().lower()
        if not k or k in seen:
            continue
        seen.add(k)
        out.append((en.strip(), (ru or "").strip(), (em or "📘").strip()))
    return out


def _base_en() -> set[str]:
    # только A0/A1 — без ленивой подгрузки high (иначе цикл)
    from data import vocabulary_words as vw

    s: set[str] = set()
    for lv in ("A0", "A1"):
        for lst in (vw.WORDS.get(lv) or {}).values():
            for w in lst:
                s.add(w["en"].strip().lower())
    return s


def _pack(items: list[tuple[str, str, str]]) -> list[dict]:
    return [_e(en, ru, em) for en, ru, em in items]


def _build_words() -> dict[str, dict[str, list[dict]]]:
    known = _base_en()
    raw_all = {"A2": A2_RAW, "B1": B1_RAW, "B2": B2_RAW, "C1": C1_RAW, "C2": C2_RAW}
    result: dict[str, dict[str, list[dict]]] = {}
    for level, topics in raw_all.items():
        result[level] = {}
        for topic, raw in topics.items():
            items = _dedupe(list(raw))
            clean = []
            for en, ru, em in items:
                k = en.lower()
                if k in known:
                    continue
                known.add(k)
                clean.append((en, ru, em))
            # если после фильтра мало — оставить topic-local без A0/A1
            if len(clean) < 28:
                a0a1 = _base_en()
                clean = []
                local: set[str] = set()
                for en, ru, em in items:
                    k = en.lower()
                    if k in a0a1 or k in local:
                        continue
                    local.add(k)
                    known.add(k)
                    clean.append((en, ru, em))
            result[level][topic] = _pack(clean[:45])
    return result


# Фразы B2–C2 (12 на тему) — дополнение к A2/B1 в PHRASES_RAW
_EXTRA_PHRASES: dict[str, dict[str, list[tuple[str, str, str]]]] = {
    "B2": {
        "society": [
            ("Bridge the social divide", "Преодолеть социальный разрыв", "🌉"),
            ("Challenge gender stereotypes", "Бросать вызов гендерным стереотипам", "⚖️"),
            ("Fight for equal rights", "Бороться за равные права", "✊"),
            ("Raise public awareness", "Повышать общественную осведомлённость", "📢"),
            ("Live in a diverse community", "Жить в разнообразном сообществе", "🌍"),
            ("Tackle discrimination head-on", "Прямо бороться с дискриминацией", "🛡️"),
            ("Promote social mobility", "Способствовать социальной мобильности", "📈"),
            ("Exclude minorities unfairly", "Несправедливо исключать меньшинства", "❌"),
            ("Support vulnerable groups", "Поддерживать уязвимые группы", "🤝"),
            ("Demand civic engagement", "Требовать гражданской активности", "🗳️"),
            ("Address systemic inequality", "Решать системное неравенство", "⚖️"),
            ("Foster community cohesion", "Укреплять сплочённость сообщества", "🏘️"),
        ],
        "business": [
            ("Secure venture capital funding", "Получить венчурное финансирование", "💰"),
            ("Scale up the business model", "Масштабировать бизнес-модель", "📈"),
            ("Launch a marketing campaign", "Запустить маркетинговую кампанию", "📢"),
            ("Negotiate a merger deal", "Договариваться о слиянии", "🤝"),
            ("Maximize return on investment", "Максимизировать ROI", "📊"),
            ("Build a loyal customer base", "Построить лояльную базу клиентов", "👥"),
            ("Disrupt an established market", "Перевернуть устоявшийся рынок", "💥"),
            ("Cut operating costs sharply", "Резко сократить операционные расходы", "✂️"),
            ("Pitch to angel investors", "Питчить инвесторам", "🎤"),
            ("Manage supply chain risks", "Управлять рисками цепочки поставок", "🔗"),
            ("Deliver a quarterly report", "Сдать квартальный отчёт", "📄"),
            ("Protect brand reputation", "Защищать репутацию бренда", "🛡️"),
        ],
        "science": [
            ("Conduct a controlled experiment", "Провести контролируемый эксперимент", "🔬"),
            ("Publish peer-reviewed research", "Опубликовать рецензируемое исследование", "📰"),
            ("Test a working hypothesis", "Проверить рабочую гипотезу", "💡"),
            ("Analyze statistical data carefully", "Аккуратно анализировать статистику", "📊"),
            ("Make a scientific breakthrough", "Сделать научный прорыв", "🚀"),
            ("Collaborate across disciplines", "Сотрудничать междисциплинарно", "🔗"),
            ("Challenge outdated theories", "Оспаривать устаревшие теории", "⚔️"),
            ("Observe cause and effect", "Наблюдать причину и следствие", "🔍"),
            ("Collect empirical evidence", "Собирать эмпирические доказательства", "📋"),
            ("Replicate previous findings", "Повторить предыдущие результаты", "🔁"),
            ("Use cutting-edge technology", "Использовать передовые технологии", "⚡"),
            ("Question the methodology", "Ставить под вопрос методологию", "❓"),
        ],
        "law": [
            ("File a formal complaint", "Подать официальную жалобу", "📄"),
            ("Plead not guilty in court", "Заявить о невиновности в суде", "⚖️"),
            ("Reach an out-of-court settlement", "Прийти к внесудебному соглашению", "🤝"),
            ("Uphold the rule of law", "Соблюдать верховенство закона", "📜"),
            ("Protect civil liberties", "Защищать гражданские свободы", "🗽"),
            ("Serve a prison sentence", "Отбывать тюремный срок", "🔒"),
            ("Appeal against the verdict", "Обжаловать приговор", "↩️"),
            ("Hire a defence attorney", "Нанять адвоката защиты", "🧑‍⚖️"),
            ("Enforce contract terms", "Обеспечивать исполнение договора", "📋"),
            ("Respect due process", "Соблюдать должную процедуру", "✅"),
            ("Violate human rights", "Нарушать права человека", "⚠️"),
            ("Seek justice for victims", "Добиваться справедливости для жертв", "✊"),
        ],
        "psychology": [
            ("Cope with emotional trauma", "Справляться с эмоциональной травмой", "🩹"),
            ("Build emotional resilience", "Развивать эмоциональную устойчивость", "💪"),
            ("Recognize cognitive bias", "Распознавать когнитивные искажения", "🧠"),
            ("Seek professional counselling", "Обратиться за профессиональной помощью", "🛋️"),
            ("Recover from burnout slowly", "Медленно восстанавливаться после выгорания", "🔥"),
            ("Practice mindfulness daily", "Ежедневно практиковать осознанность", "🧘"),
            ("Overcome social anxiety", "Преодолеть социальную тревожность", "😰"),
            ("Understand subconscious motives", "Понимать подсознательные мотивы", "💭"),
            ("Form healthier habits", "Формировать более здоровые привычки", "✅"),
            ("Deal with peer pressure", "Справляться с давлением сверстников", "👥"),
            ("Strengthen self-esteem", "Укреплять самооценку", "⭐"),
            ("Break destructive patterns", "Разрушать деструктивные паттерны", "🔄"),
        ],
        "arts": [
            ("Curate a modern exhibition", "Курировать современную выставку", "🖼️"),
            ("Perform on the main stage", "Выступать на главной сцене", "🎭"),
            ("Capture light in a painting", "Передавать свет в картине", "💡"),
            ("Compose an original soundtrack", "Написать оригинальный саундтрек", "🎵"),
            ("Critically review a play", "Критически разобрать спектакль", "📝"),
            ("Explore abstract expressionism", "Изучать абстрактный экспрессионизм", "🎨"),
            ("Attend a gallery opening", "Посетить открытие галереи", "🥂"),
            ("Master classical technique", "Освоить классическую технику", "🎻"),
            ("Break artistic conventions", "Ломать художественные условности", "💥"),
            ("Interpret symbolism in art", "Толковать символизм в искусстве", "🔮"),
            ("Draft a screenplay outline", "Набросать план сценария", "🎬"),
            ("Support emerging artists", "Поддерживать начинающих художников", "🌱"),
        ],
        "global_issues": [
            ("Combat extreme poverty", "Бороться с крайней бедностью", "🌍"),
            ("Respond to a humanitarian crisis", "Реагировать на гуманитарный кризис", "🆘"),
            ("Negotiate a ceasefire agreement", "Договариваться о прекращении огня", "🕊️"),
            ("Reduce greenhouse gas emissions", "Сокращать выбросы парниковых газов", "🌡️"),
            ("Defend freedom of speech", "Защищать свободу слова", "🗣️"),
            ("Fight institutional corruption", "Бороться с институциональной коррупцией", "🕵️"),
            ("Promote sustainable development", "Продвигать устойчивое развитие", "♻️"),
            ("Welcome refugees with dignity", "Принимать беженцев с достоинством", "🤝"),
            ("Address food insecurity", "Решать проблему отсутствия продовольственной безопасности", "🍞"),
            ("Strengthen international cooperation", "Укреплять международное сотрудничество", "🌐"),
            ("Monitor human rights violations", "Мониторить нарушения прав человека", "👁️"),
            ("Prevent further escalation", "Предотвращать дальнейшую эскалацию", "⛔"),
        ],
        "lifestyle": [
            ("Maintain a healthy work-life balance", "Сохранять баланс работы и жизни", "⚖️"),
            ("Adopt a minimalist lifestyle", "Перейти к минималистичному образу жизни", "🤍"),
            ("Practice digital detox regularly", "Регулярно устраивать цифровой детокс", "📵"),
            ("Invest in personal growth", "Инвестировать в личный рост", "📈"),
            ("Follow a flexible routine", "Следовать гибкому распорядку", "📅"),
            ("Prioritize mental wellbeing", "Ставить ментальное здоровье в приоритет", "🧠"),
            ("Reduce daily stress levels", "Снижать уровень ежедневного стресса", "😌"),
            ("Cook from scratch more often", "Чаще готовить с нуля", "🍳"),
            ("Cut down on social media", "Сократить время в соцсетях", "📱"),
            ("Travel for self-discovery", "Путешествовать ради самопознания", "🧳"),
            ("Build lasting friendships", "Строить прочные дружеские связи", "🤝"),
            ("Live more intentionally", "Жить более осознанно", "🎯"),
        ],
    },
    "C1": {
        "academic": [
            ("Fill a research gap", "Закрыть пробел в исследованиях", "🔍"),
            ("Conduct a literature review", "Провести обзор литературы", "📚"),
            ("Operationalize key variables", "Операционализировать ключевые переменные", "🔧"),
            ("Ensure academic integrity", "Обеспечивать академическую честность", "⚖️"),
            ("Present empirical findings", "Представить эмпирические результаты", "📊"),
            ("Contextualize the results", "Поместить результаты в контекст", "🧩"),
            ("Challenge prevailing paradigms", "Оспаривать господствующие парадигмы", "🔬"),
            ("Write a peer-reviewed paper", "Написать рецензируемую статью", "📰"),
            ("Defend a doctoral thesis", "Защитить докторскую диссертацию", "🎓"),
            ("Cite authoritative sources", "Ссылаться на авторитетные источники", "📝"),
            ("Avoid confirmation bias", "Избегать confirmation bias", "⚠️"),
            ("Synthesize competing theories", "Синтезировать конкурирующие теории", "🧠"),
        ],
        "professional": [
            ("Engage key stakeholders early", "Вовлекать ключевых стейкхолдеров заранее", "🤝"),
            ("Streamline operational processes", "Оптимизировать операционные процессы", "⚡"),
            ("Deliver measurable KPIs", "Обеспечивать измеримые KPI", "📈"),
            ("Assess residual risk carefully", "Осторожно оценивать остаточный риск", "⚠️"),
            ("Prepare an executive summary", "Подготовить резюме для руководства", "📄"),
            ("Uphold corporate compliance", "Соблюдать корпоративный комплаенс", "✅"),
            ("Leverage competitive advantage", "Использовать конкурентное преимущество", "🏆"),
            ("Negotiate under an NDA", "Вести переговоры под NDA", "🔒"),
            ("Drive organizational change", "Продвигать организационные изменения", "🔄"),
            ("Protect brand equity", "Защищать стоимость бренда", "🏷️"),
            ("Align strategy with governance", "Согласовывать стратегию с управлением", "🏛️"),
            ("Scale with operational efficiency", "Масштабироваться с операционной эффективностью", "📊"),
        ],
        "politics": [
            ("Defend national sovereignty", "Защищать национальный суверенитет", "🏛️"),
            ("Form a governing coalition", "Сформировать правящую коалицию", "🔗"),
            ("Win a narrow referendum", "Выиграть референдум с небольшим перевесом", "🗳️"),
            ("Apply diplomatic pressure", "Оказывать дипломатическое давление", "🤝"),
            ("Impose economic sanctions", "Вводить экономические санкции", "🚫"),
            ("Respect separation of powers", "Уважать разделение властей", "⚖️"),
            ("Mobilize soft power abroad", "Использовать soft power за рубежом", "🌐"),
            ("Counter rising populism", "Противостоять росту популизма", "📢"),
            ("Increase voter turnout", "Повышать явку избирателей", "🗳️"),
            ("Lobby for policy reform", "Лоббировать реформу политики", "💼"),
            ("Guarantee checks and balances", "Гарантировать систему сдержек", "⚖️"),
            ("Address political polarization", "Решать проблему политической поляризации", "↔️"),
        ],
        "economics": [
            ("Stimulate aggregate demand", "Стимулировать совокупный спрос", "📈"),
            ("Tighten monetary policy", "Ужесточать монетарную политику", "🏦"),
            ("Contain runaway inflation", "Сдерживать галопирующую инфляцию", "💹"),
            ("Avoid a prolonged recession", "Избежать затяжной рецессии", "📉"),
            ("Balance the fiscal budget", "Сбалансировать фискальный бюджет", "💰"),
            ("Raise the interest rate", "Повысить процентную ставку", "📊"),
            ("Reduce the trade deficit", "Сократить торговый дефицит", "📉"),
            ("Attract foreign investment", "Привлекать иностранные инвестиции", "🌍"),
            ("Stabilize exchange rates", "Стабилизировать обменные курсы", "💱"),
            ("Tax luxury goods heavily", "Жёстко облагать люксовые товары", "💎"),
            ("Measure GDP growth carefully", "Аккуратно измерять рост ВВП", "📈"),
            ("Address wealth inequality", "Решать проблему неравенства богатства", "⚖️"),
        ],
        "philosophy": [
            ("Question absolute truths", "Сомневаться в абсолютных истинах", "❓"),
            ("Examine moral relativism", "Рассматривать моральный релятивизм", "⚖️"),
            ("Defend free will", "Защищать свободу воли", "🗽"),
            ("Explore existential meaning", "Исследовать экзистенциальный смысл", "🌌"),
            ("Apply Occam's razor", "Применять бритву Оккама", "✂️"),
            ("Seek epistemic humility", "Стремиться к эпистемической скромности", "🧘"),
            ("Distinguish ethics from law", "Отличать этику от закона", "📜"),
            ("Argue from first principles", "Аргументировать от первых принципов", "🧩"),
            ("Challenge metaphysical claims", "Оспаривать метафизические утверждения", "💭"),
            ("Pursue practical wisdom", "Стремиться к практической мудрости", "🦉"),
            ("Reflect on consciousness", "Размышлять о сознании", "🧠"),
            ("Balance reason and emotion", "Балансировать разум и эмоции", "❤️"),
        ],
        "literature": [
            ("Trace the character arc", "Проследить дугу персонажа", "📈"),
            ("Unpack narrative symbolism", "Раскрыть нарративный символизм", "🔮"),
            ("Unreliable first-person narrator", "Ненадёжный рассказчик от 1-го лица", "❓"),
            ("Build tension toward climax", "Наращивать напряжение к кульминации", "🎬"),
            ("Read between the metaphors", "Читать между метафорами", "📖"),
            ("Compare genre conventions", "Сравнивать жанровые условности", "📚"),
            ("Detect authorial irony", "Улавливать авторскую иронию", "😏"),
            ("Analyze stream of consciousness", "Анализировать поток сознания", "💭"),
            ("Map intertextual references", "Картировать интертекстуальные отсылки", "🔗"),
            ("Critique canonical texts", "Критиковать канонические тексты", "📜"),
            ("Appreciate poetic imagery", "Ценить поэтическую образность", "🖼️"),
            ("Rewrite the denouement", "Переписать развязку", "✅"),
        ],
        "debate": [
            ("Refute a straw-man argument", "Опровергнуть аргумент «соломенного чучела»", "🎭"),
            ("Concede a minor point", "Уступить в незначительном пункте", "🤝"),
            ("Spot a logical fallacy", "Заметить логическую ошибку", "⚠️"),
            ("Deliver a closing argument", "Произнести заключительную речь", "🎤"),
            ("Play devil's advocate", "Выступать адвокатом дьявола", "😈"),
            ("Stay rigorously on topic", "Строго держаться темы", "📌"),
            ("Cross-examine the evidence", "Перекрёстно проверить доказательства", "🔍"),
            ("Build a nuanced argument", "Строить нюансированный аргумент", "🎯"),
            ("Avoid false dichotomies", "Избегать ложных дихотомий", "↔️"),
            ("Persuade with compelling data", "Убеждать убедительными данными", "📊"),
            ("Challenge circular reasoning", "Оспаривать круговую аргументацию", "🔄"),
            ("Seek reasoned consensus", "Искать обоснованный консенсус", "🤝"),
        ],
        "innovation": [
            ("Build a minimum viable product", "Создать минимально жизнеспособный продукт", "📦"),
            ("Iterate based on feedback", "Итерировать на основе обратной связи", "🔄"),
            ("Secure seed funding", "Получить seed-финансирование", "🌱"),
            ("Disrupt legacy industries", "Переворачивать устоявшиеся отрасли", "💥"),
            ("Patent a novel approach", "Запатентовать новый подход", "📜"),
            ("Apply design thinking", "Применять design thinking", "💡"),
            ("Scale an agile team", "Масштабировать agile-команду", "👥"),
            ("Pursue a moonshot idea", "Преследовать moonshot-идею", "🌙"),
            ("Automate repetitive workflows", "Автоматизировать рутинные процессы", "⚙️"),
            ("Open-source the core library", "Открыть исходники основной библиотеки", "📂"),
            ("Prove the concept quickly", "Быстро доказать концепцию", "✅"),
            ("Find product-market fit", "Найти product-market fit", "🎯"),
        ],
    },
    "C2": {
        "nuance": [
            ("Capture subtle shades of meaning", "Передавать тонкие оттенки смысла", "🎨"),
            ("Avoid blunt categorical claims", "Избегать грубых категоричных утверждений", "⚠️"),
            ("Qualify your assertion carefully", "Осторожно уточнять своё утверждение", "🧩"),
            ("Prefer understatement to hype", "Предпочитать сдержанность хайпу", "🤫"),
            ("Read the subtext accurately", "Точно читать подтекст", "📖"),
            ("Distinguish nearly synonymous terms", "Различать почти синонимичные термины", "🔤"),
            ("Hedge politely in formal speech", "Вежливо смягчать формальную речь", "🕊️"),
            ("Signal nuance with adverbs", "Обозначать нюанс наречиями", "✍️"),
            ("Reject false precision", "Отвергать ложную точность", "❌"),
            ("Name the caveat explicitly", "Явно назвать оговорку", "📌"),
            ("Honor semantic boundaries", "Соблюдать семантические границы", "🧱"),
            ("Prefer precise collocations", "Предпочитать точные коллокации", "🔗"),
        ],
        "rhetoric": [
            ("Deploy anaphora for emphasis", "Использовать анафору для усиления", "🔁"),
            ("Craft a memorable epigram", "Создать запоминающуюся эпиграмму", "✨"),
            ("Avoid hollow rhetoric", "Избегать пустой риторики", "🎈"),
            ("Appeal to ethos carefully", "Осторожно апеллировать к этосу", "🛡️"),
            ("Balance pathos and logos", "Балансировать пафос и логос", "⚖️"),
            ("Use parallelism elegantly", "Элегантно использовать параллелизм", "📐"),
            ("End with a resonant cadence", "Завершать резонансной каденцией", "🎵"),
            ("Reframe the audience's frame", "Переформулировать рамку аудитории", "🖼️"),
            ("Resist demagogic flourishes", "Сопротивляться демагогическим украсам", "🚫"),
            ("Layer irony without confusion", "Накладывать иронию без путаницы", "😏"),
            ("Anchor claims in evidence", "Заякорить утверждения доказательствами", "📌"),
            ("Speak with rhetorical restraint", "Говорить с риторической сдержанностью", "🧘"),
        ],
        "specialized": [
            ("Translate jargon into plain English", "Переводить жаргон на простой английский", "🔤"),
            ("Master domain-specific terminology", "Освоить предметную терминологию", "📚"),
            ("Avoid opaque technicalese", "Избегать непрозрачного технического языка", "🌫️"),
            ("Define terms before arguing", "Определять термины до спора", "📋"),
            ("Bridge specialist and lay audiences", "Связывать специалистов и неспециалистов", "🌉"),
            ("Use precise legal wording", "Использовать точные юридические формулировки", "⚖️"),
            ("Flag methodological constraints", "Отмечать методологические ограничения", "🚧"),
            ("Cite the primary literature", "Ссылаться на первичную литературу", "📰"),
            ("Prefer operational definitions", "Предпочитать операционные определения", "🔧"),
            ("Keep notation consistent", "Сохранять единую нотацию", "🔢"),
            ("Audit terminology drift", "Отслеживать дрейф терминологии", "📊"),
            ("Write for peer specialists", "Писать для коллег-специалистов", "🎓"),
        ],
        "idioms_advanced": [
            ("Throw down the gauntlet", "Бросить перчатку", "🧤"),
            ("Bite the bullet reluctantly", "Неохотно стиснуть зубы", "😬"),
            ("Burn the midnight oil", "Работать допоздна", "🕯️"),
            ("Jump on the bandwagon late", "Поздно прыгнуть в чужой поезд", "🚂"),
            ("Cut to the chase immediately", "Сразу перейти к делу", "✂️"),
            ("Read the writing on the wall", "Видеть письмо на стене", "🧱"),
            ("Have a chip on your shoulder", "Иметь комплекс", "💪"),
            ("Steal someone's thunder", "Украсть чью-то славу", "⛈️"),
            ("Paint yourself into a corner", "Загнать себя в угол", "🎨"),
            ("Keep your powder dry", "Держать порох сухим", "🔫"),
            ("Play devil's advocate skillfully", "Умело играть адвоката дьявола", "😈"),
            ("Take it with a grain of salt", "Принимать с долей скепсиса", "🧂"),
        ],
        "register": [
            ("Shift register without awkwardness", "Менять регистр без неловкости", "🎚️"),
            ("Avoid mixing slang and legalese", "Не смешивать сленг и юрид. язык", "⚠️"),
            ("Prefer formal diction in memos", "В докладных предпочитать формальный стиль", "📄"),
            ("Sound appropriately colloquial", "Звучать уместно разговорно", "💬"),
            ("Tone down aggressive wording", "Смягчать агрессивные формулировки", "🕊️"),
            ("Match register to audience", "Подбирать регистр под аудиторию", "👥"),
            ("Drop archaic phrasing", "Отказаться от архаичных оборотов", "📜"),
            ("Elevate style for ceremonial speech", "Приподнять стиль для торжественной речи", "🎤"),
            ("Keep emails professionally concise", "Держать письма кратко и профессионально", "✉️"),
            ("Avoid overly florid prose", "Избегать излишне цветистой прозы", "🌸"),
            ("Signal deference politely", "Вежливо обозначать deferентность", "🙇"),
            ("Choose elevated synonyms wisely", "Мудро выбирать возвышенные синонимы", "📚"),
        ],
        "collocations": [
            ("Make a compelling case", "Привести убедительный аргумент", "🎯"),
            ("Draw a sharp distinction", "Провести чёткую грань", "✏️"),
            ("Pose a probing question", "Задать проницательный вопрос", "❓"),
            ("Reach a tentative conclusion", "Прийти к предварительному выводу", "🧩"),
            ("Carry significant weight", "Иметь значительный вес", "⚖️"),
            ("Exert gentle pressure", "Оказывать мягкое давление", "🤏"),
            ("Hold strong views", "Придерживаться твёрдых взглядов", "📌"),
            ("Gain widespread traction", "Получить широкую поддержку", "📈"),
            ("Mount a vigorous defence", "Возвести энергичную защиту", "🛡️"),
            ("Spark heated debate", "Вызвать жаркие дебаты", "🔥"),
            ("Warrant close scrutiny", "Заслуживать внимательной проверки", "🔍"),
            ("Offer a nuanced take", "Предложить нюансированный взгляд", "🎨"),
        ],
        "abstract": [
            ("Grasp abstract frameworks", "Схватывать абстрактные рамки", "🧩"),
            ("Move from concrete to abstract", "Идти от конкретного к абстрактному", "⬆️"),
            ("Avoid reifying ideas", "Не овеществлять идеи", "🚫"),
            ("Model complex systems simply", "Просто моделировать сложные системы", "📐"),
            ("Treat concepts as tools", "Считать концепции инструментами", "🔧"),
            ("Question ontological assumptions", "Ставить под вопрос онтологические допущения", "❓"),
            ("Tolerate productive ambiguity", "Допускать продуктивную неоднозначность", "🌫️"),
            ("Map relations not things", "Картировать отношения, а не вещи", "🗺️"),
            ("Keep taxonomy provisional", "Держать таксономию предварительной", "📋"),
            ("Prioritize explanatory power", "Приоритизировать объяснительную силу", "💡"),
            ("Resist premature abstraction", "Сопротивляться преждевременной абстракции", "🧱"),
            ("Test ideas against cases", "Проверять идеи на кейсах", "✅"),
        ],
        "mastery": [
            ("Sound almost native in debate", "Звучать почти как носитель в дебатах", "🌟"),
            ("Switch styles on demand", "Переключать стили по требованию", "🎚️"),
            ("Crush idiomatic gaps", "Убирать пробелы в идиомах", "💬"),
            ("Write with surgical precision", "Писать с хирургической точностью", "🎯"),
            ("Speak with effortless fluency", "Говорить с лёгкой беглостью", "🗣️"),
            ("Edit ruthlessly for clarity", "Жёстко править ради ясности", "✂️"),
            ("Internalize advanced collocations", "Усваивать продвинутые коллокации", "🔗"),
            ("Control pragmatic softeners", "Контролировать прагматические смягчители", "🕊️"),
            ("Perform under scrutiny", "Работать под пристальным вниманием", "👁️"),
            ("Teach nuance to others", "Обучать других нюансам", "🧑‍🏫"),
            ("Maintain lexical discipline", "Сохранять лексическую дисциплину", "📚"),
            ("Aim for near-native command", "Стремиться к почти носительскому уровню", "👑"),
        ],
    },
}


def _build_phrases() -> dict[str, dict[str, list[dict]]]:
    combined = dict(PHRASES_RAW)
    for level, topics in _EXTRA_PHRASES.items():
        combined[level] = topics
    result: dict[str, dict[str, list[dict]]] = {}
    for level, topics in combined.items():
        result[level] = {}
        for topic, raw in topics.items():
            result[level][topic] = _pack(_dedupe(list(raw))[:15])
    return result


HIGH_WORDS = _build_words()
HIGH_PHRASES = _build_phrases()
