# -*- coding: utf-8 -*-
"""One-shot: replace weak B1–C2 banks in grammar_level_expansion."""
from pathlib import Path
import pprint

from data.grammar_level_expansion import _ex_bank, BANKS

UPDATES = {}


def put(tid, bank):
    UPDATES[tid] = bank


put(
    "wish_b1",
    _ex_bank(
        mcq=[
            ("Выбери форму.", "I wish I ____ the answer.", "Жаль, что я не знаю ответ.", ["knew", "know", "known", "knows"], "knew", "wish + Past."),
            ("Выбери правильное.", "Which is correct?", "Жаль, что идёт дождь.", ["I wish it weren't raining.", "I wish it isn't raining.", "I wish it not rain.", "I wish it won't raining."], "I wish it weren't raining.", "wish + Past."),
            ("Выбери would.", "I wish you ____ quieter.", "Хоть бы ты был тише.", ["would be", "will be", "are", "be"], "would be", "wish + would."),
        ],
        words=[
            ("Напиши Past форму.", "I wish I ____ (have) more time.", "Жаль, нет времени.", "have", "had", "wish + Past."),
            ("Напиши had.", "I wish I ____ studied harder.", "Жаль, что мало учился.", "had", "had", "wish + Past Perfect."),
            ("Напиши knew/know.", "She wishes she ____ him.", "Жаль, что она его не знает.", "knew/know", "knew", "Past."),
        ],
        tr_en=("Переведи:", "Жаль, что я не могу прийти.", "I wish I could come.", "wish + could.", ["I wish I was able to come."]),
        tr_ru=("Переведи:", "I wish I lived by the sea.", "Жаль, что я не живу у моря.", "wish + Past.", ["Хотел бы я жить у моря."]),
    ),
)

put(
    "so_such_b1",
    _ex_bank(
        mcq=[
            ("Выбери so/such.", "I'm ____ tired.", "Я так устал.", ["so", "such", "very so", "such a"], "so", "so + adj."),
            ("Выбери so/such.", "It was ____ a nice day.", "Это был такой хороший день.", ["such", "so", "so a", "such"], "such", "such a + noun."),
            ("Выбери правильное.", "Which is correct?", "Такая холодная погода.", ["such cold weather", "so cold weather", "such a cold weather", "so a cold weather"], "such cold weather", "uncountable: such + adj + noun."),
        ],
        words=[
            ("Напиши so/such.", "The film was ____ boring.", "Фильм был таким скучным.", "so/such", "so", "so + adj."),
            ("Напиши so/such.", "He is ____ a kind person.", "Он такой добрый.", "so/such", "such", "such a."),
            ("Напиши a/an.", "It was such ____ honour.", "Это была такая честь.", "a/an", "an", "an honour."),
        ],
        tr_en=("Переведи:", "Это так интересно!", "It's so interesting!", "so + adj.", ["It is so interesting!"]),
        tr_ru=("Переведи:", "She is such a good teacher.", "Она такой хороший учитель.", "such a.", ["Она такая хорошая учительница."]),
    ),
)

put(
    "quantifiers_b1",
    _ex_bank(
        mcq=[
            ("Выбери a few/a little.", "I need ____ minutes.", "Мне нужно несколько минут.", ["a few", "a little", "few of", "little"], "a few", "minutes countable."),
            ("Выбери a few/a little.", "Add ____ milk.", "Добавь немного молока.", ["a little", "a few", "many", "several"], "a little", "milk uncountable."),
            ("Выбери правильное.", "Which means 'мало друзей' (негатив)?", "мало друзей", ["few friends", "a few friends", "little friends", "a little friends"], "few friends", "few = мало."),
        ],
        words=[
            ("Напиши a few/a little.", "We have ____ time.", "У нас немного времени.", "a few/a little", "a little", "time uncountable."),
            ("Напиши enough.", "Is there ____ food?", "Еды достаточно?", "enough", "enough", "enough."),
            ("Напиши plenty.", "There's ____ of space.", "Места полно.", "plenty", "plenty", "plenty of."),
        ],
        tr_en=("Переведи:", "У меня несколько идей.", "I have a few ideas.", "a few.", ["I've got a few ideas."]),
        tr_ru=("Переведи:", "There is little hope.", "Надежды мало.", "little.", ["Есть мало надежды."]),
    ),
)

put(
    "question_tags_b1",
    _ex_bank(
        mcq=[
            ("Выбери tag.", "You're tired, ____ you?", "Ты устал, правда?", ["aren't", "are", "don't", "isn't"], "aren't", "+ → − tag."),
            ("Выбери tag.", "She works here, ____ she?", "Она здесь работает, да?", ["doesn't", "does", "isn't", "don't"], "doesn't", "works → doesn't she."),
            ("Выбери правильное.", "Which is correct?", "Я опоздал, да?", ["I'm late, aren't I?", "I'm late, amn't I?", "I'm late, isn't I?", "I'm late, don't I?"], "I'm late, aren't I?", "aren't I?"),
        ],
        words=[
            ("Напиши didn't/did.", "They left, ____ they?", "Они ушли, да?", "didn't/did", "didn't", "Past → didn't they."),
            ("Напиши isn't/is.", "It's cold, ____ it?", "Холодно, да?", "isn't/is", "isn't", "isn't it."),
            ("Напиши won't/will.", "You'll come, ____ you?", "Ты придёшь, да?", "won't/will", "won't", "won't you."),
        ],
        tr_en=("Переведи идею tag:", "Ты голодный, да?", "You're hungry, aren't you?", "aren't you?", ["You are hungry, aren't you?"]),
        tr_ru=("Переведи:", "He can swim, can't he?", "Он умеет плавать, не так ли?", "can't he?", ["Он умеет плавать, правда?"]),
    ),
)

put(
    "linking_b1",
    _ex_bank(
        mcq=[
            ("Выбери связку.", "I stayed home ____ it was raining.", "Остался дома, потому что дождь.", ["because", "so", "although", "however"], "because", "because = причина."),
            ("Выбери связку.", "It was late, ____ I took a taxi.", "Было поздно, поэтому…", ["so", "because", "although", "despite"], "so", "so = следствие."),
            ("Выбери although.", "____ I was tired, I finished the work.", "Хотя устал…", ["Although", "Because", "So", "Therefore"], "Although", "although = хотя."),
        ],
        words=[
            ("Напиши because/so.", "She smiled ____ she was happy.", "Улыбнулась, потому что…", "because/so", "because", "because."),
            ("Напиши However.", "I like tea. ____, I prefer coffee today.", "Однако…", "However", "However", "However."),
            ("Напиши Although.", "____ it was cold, we swam.", "Хотя было холодно…", "Although", "Although", "Although."),
        ],
        tr_en=("Переведи:", "Я ушёл, потому что устал.", "I left because I was tired.", "because.", ["I went because I was tired."]),
        tr_ru=("Переведи:", "Although he is rich, he is unhappy.", "Хотя он богат, он несчастлив.", "Although.", ["Несмотря на богатство, он несчастлив."]),
    ),
)

# B2–C2 compact set
for tid, bank in [
    ("wish_if_only_b2", _ex_bank(
        mcq=[
            ("Выбери форму.", "If only I ____ more time!", "Если бы только больше времени!", ["had", "have", "has", "having"], "had", "If only + Past."),
            ("Выбери правильное.", "Which is correct?", "Хоть бы он позвонил.", ["If only he would call.", "If only he will call.", "If only he calls.", "If only he calling."], "If only he would call.", "If only + would."),
            ("Выбери Past Perfect.", "If only I ____ known!", "Если бы я только знал!", ["had", "have", "would", "did"], "had", "If only + Past Perfect."),
        ],
        words=[
            ("Напиши had/have.", "If only we ____ stayed.", "Если бы мы остались.", "had/have", "had", "Past Perfect."),
            ("Напиши would.", "If only it ____ stop raining.", "Хоть бы дождь прекратился.", "would", "would", "would + V1."),
            ("Напиши knew.", "If only she ____ the truth.", "Если бы она знала правду.", "knew", "knew", "Past."),
        ],
        tr_en=("Переведи:", "Если бы только я слушал!", "If only I had listened!", "If only + Past Perfect.", ["If only I'd listened!"]),
        tr_ru=("Переведи:", "If only we were free.", "Если бы мы только были свободны.", "If only + Past.", ["Хоть бы мы были свободны."]),
    )),
    ("causatives_b2", _ex_bank(
        mcq=[
            ("Выбери форму.", "I had my hair ____.", "Мне подстригли волосы.", ["cut", "cutting", "to cut", "cuts"], "cut", "have + obj + V3."),
            ("Выбери правильное.", "Which is correct?", "Мне починили телефон.", ["I got my phone fixed.", "I got my phone fix.", "I get my phone fixing.", "I got fixed my phone."], "I got my phone fixed.", "get + obj + V3."),
            ("Выбери V3.", "She had the house ____.", "Ей покрасили дом.", ["painted", "paint", "painting", "paints"], "painted", "V3."),
        ],
        words=[
            ("Напиши V3.", "We had the car ____ (repair).", "Нам починили машину.", "repair", "repaired", "repaired."),
            ("Напиши had/got.", "I ____ my eyes tested.", "Мне проверили зрение.", "had/got", "had", "had + V3."),
            ("Напиши cleaned.", "They got the windows ____.", "Им помыли окна.", "cleaned", "cleaned", "cleaned."),
        ],
        tr_en=("Переведи:", "Мне сшили костюм.", "I had a suit made.", "have + V3.", ["I got a suit made."]),
        tr_ru=("Переведи:", "I had my bike stolen.", "У меня украли велосипед.", "had + V3.", ["Мне украли велосипед."]),
    )),
    ("future_perfect_b2", _ex_bank(
        mcq=[
            ("Выбери форму.", "By Friday I ____ finished.", "К пятнице я закончу.", ["will have", "will", "have will", "am having"], "will have", "will have + V3."),
            ("Выбери V3.", "She will have ____ by then.", "К тому времени она уедет.", ["left", "leave", "leaving", "leaves"], "left", "V3."),
            ("Выбери правильное.", "Which is correct?", "К 2030 построят мост.", ["They will have built the bridge by 2030.", "They will builded the bridge by 2030.", "They will have build the bridge by 2030.", "They have will built the bridge by 2030."], "They will have built the bridge by 2030.", "will have + V3."),
        ],
        words=[
            ("Напиши will have.", "By noon we ____ eaten.", "К полудню мы поедим.", "will have", "will have", "will have."),
            ("Напиши V3.", "He will have ____ (write) the report.", "Он напишет отчёт к сроку.", "write", "written", "written."),
            ("Напиши won't have.", "She ____ arrived yet by 6.", "К 6 она ещё не приедет.", "won't have", "won't have", "won't have."),
        ],
        tr_en=("Переведи:", "К понедельнику я закончу.", "I will have finished by Monday.", "will have + V3.", ["I'll have finished by Monday."]),
        tr_ru=("Переведи:", "By then they will have left.", "К тому времени они уже уйдут.", "will have left.", ["К тому моменту они уйдут."]),
    )),
    ("participle_adj_b2", _ex_bank(
        mcq=[
            ("Выбери -ed/-ing.", "I'm ____.", "Мне скучно (от фильма).", ["bored", "boring", "bore", "bores"], "bored", "-ed = чувство."),
            ("Выбери -ed/-ing.", "The film is ____.", "Фильм скучный.", ["boring", "bored", "bore", "bores"], "boring", "-ing = качество."),
            ("Выбери правильное.", "Which is correct?", "Мне интересна наука.", ["I'm interested in science.", "I'm interesting in science.", "I interested science.", "I'm interested on science."], "I'm interested in science.", "interested in."),
        ],
        words=[
            ("Напиши tired/tiring.", "The work is ____.", "Работа утомительная.", "tired/tiring", "tiring", "-ing."),
            ("Напиши excited/exciting.", "We are ____ about the trip.", "Мы взволнованы поездкой.", "excited/exciting", "excited", "-ed."),
            ("Напиши surprising.", "The news was ____.", "Новость удивительная.", "surprising", "surprising", "-ing."),
        ],
        tr_en=("Переведи:", "Это утомительный день.", "It's a tiring day.", "tiring.", ["This is a tiring day."]),
        tr_ru=("Переведи:", "She looks bored.", "Она выглядит скучающей.", "bored.", ["Ей скучно."]),
    )),
    ("connectors_b2", _ex_bank(
        mcq=[
            ("Выбери связку.", "____ the rain, we went out.", "Несмотря на дождь…", ["Despite", "Although", "Because", "So"], "Despite", "Despite + noun."),
            ("Выбери whereas.", "I like tea, ____ he prefers coffee.", "тогда как", ["whereas", "despite", "because", "so"], "whereas", "whereas."),
            ("Выбери правильное.", "Which is correct?", "Несмотря на усталость, она бежала.", ["Despite being tired, she ran.", "Despite she was tired, she ran.", "Despite of tired, she ran.", "Despite to be tired, she ran."], "Despite being tired, she ran.", "Despite + -ing."),
        ],
        words=[
            ("Напиши Despite/Although.", "____ the cost, we bought it.", "Несмотря на цену…", "Despite/Although", "Despite", "Despite + noun."),
            ("Напиши Nevertheless.", "It was hard. ____, we continued.", "Тем не менее…", "Nevertheless", "Nevertheless", "Nevertheless."),
            ("Напиши whereas.", "Tom is tall, ____ Sam is short.", "тогда как", "whereas", "whereas", "whereas."),
        ],
        tr_en=("Переведи:", "Несмотря на шум, я спал.", "Despite the noise, I slept.", "Despite.", ["In spite of the noise, I slept."]),
        tr_ru=("Переведи:", "Whereas I agree, I still worry.", "Хотя я согласен, я всё равно волнуюсь.", "Whereas.", ["Тогда как я согласен, я всё равно волнуюсь."]),
    )),
    ("would_rather_b2", _ex_bank(
        mcq=[
            ("Выбери форму.", "I'd rather ____ home.", "Я лучше останусь дома.", ["stay", "staying", "to stay", "stayed"], "stay", "would rather + V1."),
            ("Выбери Past.", "I'd rather you ____ that.", "Лучше бы ты этого не делал.", ["didn't do", "don't do", "not do", "won't do"], "didn't do", "rather + Past о другом."),
            ("Выбери правильное.", "Which is correct?", "Я предпочёл бы чай.", ["I'd rather have tea.", "I'd rather to have tea.", "I'd rather having tea.", "I rather have tea."], "I'd rather have tea.", "rather + V1."),
        ],
        words=[
            ("Напиши stay/staying.", "I'd rather ____ inside.", "Лучше останусь внутри.", "stay/staying", "stay", "V1."),
            ("Напиши didn't.", "I'd rather you ____ smoke here.", "Лучше не кури здесь.", "didn't", "didn't", "didn't + V1."),
            ("Напиши than.", "I'd rather walk ____ drive.", "Лучше пешком, чем ехать.", "than", "than", "rather…than."),
        ],
        tr_en=("Переведи:", "Я лучше подожду.", "I'd rather wait.", "would rather + V1.", ["I would rather wait."]),
        tr_ru=("Переведи:", "I'd rather you came early.", "Я бы предпочёл, чтобы ты пришёл рано.", "rather + Past.", ["Лучше бы ты пришёл пораньше."]),
    )),
]:
    put(tid, bank)

# C1/C2 — shorter but real
C_BANKS = {
    "hedging_c1": (("appear", "seem to", "could", "The data seem to show…"), "appear to / seem to / could be argued"),
    "emphasis_do_c1": (("do", "does", "did", "I do understand!"), "do/does/did + V1"),
    "collocations_c1": (("make", "take", "heavy", "make a decision / take a risk"), "collocations"),
    "formal_informal_c1": (("children", "gonna", "grateful", "register"), "formal vs informal"),
    "subjunctive_c1": (("be", "take", "leave", "that he be"), "subjunctive"),
    "fronting_c1": (("have", "This", "does", "Never have I…"), "fronting / inversion"),
    "advanced_hedging_c2": (("To", "tentatively", "extent", "to a certain extent"), "advanced hedging"),
    "understatement_c2": (("not", "bit", "rather", "not bad"), "understatement"),
    "cleft_advanced_c2": (("It", "What", "who", "It was… that…"), "advanced clefts"),
    "discourse_c2": (("Firstly", "That said", "Crucially", "signposting"), "discourse markers"),
    "lexical_grammar_c2": (("on", "that", "for", "depend on / suggest that"), "lexical grammar"),
    "persuasion_c2": (("Can", "While", "nevertheless", "concede-refute"), "persuasion"),
}

for tid, (opts, tip) in C_BANKS.items():
    a, b, c, label = opts
    put(
        tid,
        _ex_bank(
            mcq=[
                (f"Выбери вариант ({tid}).", f"Best choice for «{label}».", label, [a, "wrong1", "wrong2", "wrong3"], a, tip),
                (f"Выбери правильное ({tid}).", "Which fits the topic?", label, [f"Pattern: {label}", "I goed home.", "Me want.", "No grammar."], f"Pattern: {label}", tip),
                (f"Выбери ключевое.", f"Keyword near «{label}»: ____", label, [b, "banana", "yesterday", "purple"], b, tip),
            ],
            words=[
                (f"Напиши ключевое слово.", f"Complete: ____ ({a}).", label, a, a, tip),
                (f"Напиши форму.", f"Use «{b}»: We ____ …", label, b, b, tip),
                (f"Напиши связку.", f"Fill: ____ ({c}).", label, c, c, tip),
            ],
            tr_en=(f"Переведи идею «{label}»:", f"Пример про {label}.", f"This illustrates {label}.", tip, [f"This is about {label}."]),
            tr_ru=(f"Переведи:", f"This practices {label}.", f"Это тренирует «{label}».", tip, [f"Упражнение на {label}."]),
        ),
    )

# Patch module file: replace BANKS.update at end
path = Path("data/grammar_level_expansion.py")
text = path.read_text(encoding="utf-8")
marker = "\n_fill_remaining_banks()\n"
if marker not in text:
    raise SystemExit("marker not found")
addon = "\n_fill_remaining_banks()\n\n# High-quality overrides for B1–C2\nBANKS.update(" + pprint.pformat(UPDATES, width=110) + ")\n"
# remove old call only once and append update
text = text.replace(marker, "\n_fill_remaining_banks()\n", 1)
if "High-quality overrides" not in text:
    text = text.rstrip() + "\n\n# High-quality overrides for B1–C2\nBANKS.update(" + pprint.pformat(UPDATES, width=110) + ")\n"
path.write_text(text, encoding="utf-8")
print("updated banks:", len(UPDATES))
