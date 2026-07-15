"""
Дополнительные связные блоки с формулами — добавляются к темам, где базового рассказа мало.
"""

FORMULA_DEEP_DIVE: dict[str, str] = {
    "pronouns_be": (
        "\n\n<b>Формулы to be</b> сейчас: I am, you are, he/she/it is, we/you/they are. "
        "Отрицание: I'm not, isn't, aren't. Вопрос: Am I…? Is she…? Are you…? "
        "Порядок в вопросе меняется — глагол впереди!"
    ),
    "can_ability": (
        "\n\nПовторим формулы: <b>can + V1</b> (без to!). Can't = cannot. "
        "Could — прошлое или вежливость: Could you help? — <i>Не мог бы помочь?</i>"
    ),
    "past_perfect": (
        "\n\n<b>Формула:</b> had + V3. When I arrived, the train had left — "
        "<i>Когда я приехал, поезд уже ушёл</i>. Before, by the time — подсказки."
    ),
    "past_continuous": (
        "\n\n<b>Формула:</b> was/were + V-ing. I was sleeping when you called — "
        "<i>Я спал, когда ты позвонил</i>. Длинное действие + короткое (Past Simple)."
    ),
    "articles_a_an": (
        "\n\n<b>Правило:</b> a + согласный звук, an + гласный звук. "
        "An hour (/aʊ/), a university (/juː/). A book — <i>книга (какая-то)</i>."
    ),
    "there_is_are": (
        "\n\n<b>Формулы:</b> There is + ед.ч.; There are + мн.ч. "
        "Is there…? / Are there…? There is a cat — <i>Есть кот</i> (не It is a cat!)."
    ),
    "plurals": (
        "\n\n<b>Формулы:</b> +s (book→books), +es (box→boxes), "
        "неправильные: man→men, child→children, foot→feet."
    ),
    "much_many_some_any": (
        "\n\nMany + исчисл., much + неисчисл., some в +, any в ?/−. "
        "How many books? How much water?"
    ),
    "comparatives": (
        "\n\nShort: +er (taller); long: more + adj. Good→better, bad→worse. "
        "Than после сравнения: bigger than me."
    ),
    "modals_a2": (
        "\n\nMust/have to/should + V1. Must not = запрет. "
        "Should = совет; have to = правило."
    ),
    "conditionals_0_1": (
        "\n\nZero: If + Present, Present. First: If + Present, will + V1. "
        "Не пиши will сразу после if!"
    ),
    "gerund_infinitive": (
        "\n\nEnjoy + V-ing; want + to V. Stop smoking ≠ stop to smoke — разный смысл!"
    ),
    "passive_basic": (
        "\n\n<b>Формула:</b> be + V3. The letter was sent — <i>Письмо отправили</i>. "
        "Is made, was built — пассив."
    ),
    "relative_clauses_b1": (
        "\n\nWho — люди; which/that — вещи. The man who called — <i>Человек, который позвонил</i>."
    ),
    "present_perfect_continuous": (
        "\n\nHave/has been + V-ing. I've been waiting — <i>Я жду (уже какое-то время)</i>."
    ),
    "conditionals_2_3": (
        "\n\n2nd: If + Past, would + V1. 3rd: If + Past Perfect, would have + V3."
    ),
    "reported_speech": (
        "\n\nHe said (that) he was tired — <i>Он сказал, что устал</i>. "
        "Say + слова; tell + кому."
    ),
    "passives_advanced": (
        "\n\nIs being done, has been done, will be sent — пассив во всех временах."
    ),
    "modals_deduction": (
        "\n\nMust be — уверен; might/could — возможно; can't be — невозможно. "
        "Must have + V3 — про прошлое."
    ),
    "relative_advanced": (
        "\n\nWhose, where, when. Non-defining — запятые: Paris, where I lived, …"
    ),
    "inversion": (
        "\n\nNever have I…, Rarely does he… — после негативных наречий инверсия."
    ),
    "cleft_sentences": (
        "\n\nIt was John who…, What I need is… — выделяем главное."
    ),
    "advanced_modals": (
        "\n\nShould have, needn't have, might have been — оттенки сожаления."
    ),
    "participle_clauses": (
        "\n\nWalking down the street, I saw… — подлежащее должно совпадать!"
    ),
    "nominalisation": (
        "\n\nDecide → decision — для формального стиля."
    ),
    "discourse_markers": (
        "\n\nHowever, furthermore, in conclusion — связки для эссе."
    ),
    "stylistic_inversion": (
        "\n\nLittle did he know… — стиль и эмфаза на C2."
    ),
    "subtle_modality": (
        "\n\nMay have / might have — сила догадки. It would seem… — хеджирование."
    ),
    "mixed_conditionals": (
        "\n\nIf I had taken that job, I would be in London now — смешение времён."
    ),
    "ellipsis_substitution": (
        "\n\nSo do I, I think so — экономия слов как у носителей."
    ),
    "register_control": (
        "\n\nGet vs obtain — informal vs formal. Один смысл, разный «костюм»."
    ),
    "pragmatic_softening": (
        "\n\nI was wondering if…, Would you mind… — смягчение просьб."
    ),
    "this_that": (
        "\n\nThis + is (близко), That + is (далеко). What's this? — <i>Что это?</i>"
    ),
    "simple_phrases": (
        "\n\nHello — <i>Привет</i>. What's your name? — My name is… "
        "How are you? — I'm fine. Thank you / Please / Sorry."
    ),
}


def append_formula_deep_dive(topic_id: str, intro: str) -> str:
    extra = FORMULA_DEEP_DIVE.get(topic_id, "")
    if extra and extra.strip() not in intro:
        return intro + extra
    return intro
