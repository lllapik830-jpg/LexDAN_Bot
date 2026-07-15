"""Генерация словарей A2–C2 для Vocabulary. Запуск: python scripts/build_vocab_a2_c2.py"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _parse_block(lines: list[str]) -> list[tuple[str, str, str]]:
    out = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            raise ValueError(f"Bad line: {line}")
        out.append((parts[0], parts[1], parts[2]))
    return out


# en|ru|emoji — уникальные слова по уровням, глаголы с to
DATA: dict[str, dict[str, list[str]]] = {
    "A2": {
        "family": """
orphan|сирота|👶
foster|приёмный ( ребёнок )|🏠
in-law|родственник супруга|💍
stepchild|пасынок/падчерица|👧
half-brother|единокровный брат|👦
widow|вдова|🖤
widower|вдовец|🖤
sibling|брат или сister|👫
upbringing|воспитание|🌱
household|домашнее хозяйство|🏠
quarrel|ссора|😠
reconcile|мириться|🤝
to adopt|усыновлять|👶
to babysit|присматривать за детьми|👶
to inherit|наследовать|📜
to rely on|полагаться на|🤝
to get on with|ладить с|😊
to fall out|поссориться|😠
strict|строгий|📏
warm-hearted|добросердечный|❤️
distant|холодный/отдалённый|🧊
close-knit|сплочённый|🫂
blended family|смешанная семья|👨‍👩‍👧
single parent|одинокий родитель|1️⃣
extended family|большая семья|👪
family reunion|семейная встреча|🎉
generation gap|конфликт поколений|👴👦
bring up|воспитывать|🌱
look after|присматривать|👀
run the house|вести хозяйство|🏠
family values|семейные ценности|💎
domestic|домашний|🏠
relative by marriage|родственник по браку|💍
family bond|семейная связь|🔗
""",
        "home": """
attic|чердак|⬆️
basement|подвал|⬇️
chimney|труба|🏠
driveway|подъездная дорога|🚗
fence|забор|🚧
gate|калитка|🚪
hedge|живая изгородь|🌳
lawn|газон|🌿
mattress|матрас|🛏️
duvet|одеяло-пуховик|🛏️
laundry|стирка|🧺
ironing|глажка|👔
vacuum cleaner|пылесос|🧹
detergent|моющее средство|🧴
plumber|сантехник|🔧
electrician|электрик|⚡
leak|протечка|💧
mould|плесень|🦠
renovation|ремонт|🔨
landlord|арендодатель|🧑‍💼
tenant|арендатор|🔑
mortgage|ипотека|🏦
utility bill|коммунальный счёт|🧾
to renovate|ремонтировать|🔨
to leak|течь|💧
to install|устанавливать|🔧
to unplug|выключить из розетки|🔌
to mow|косить газон|🌿
cozy|уютный|🕯️
spacious|просторный|📐
cramped|тесный|📦
furnished|меблированный|🛋️
unfurnished|без мебели|📦
detached house|отдельный дом|🏡
semi-detached|дуплекс|🏘️
""",
        "work": """
employee|работник|👷
employer|работодатель|🧑‍💼
workplace|место работы|🏢
shift|смена|⏰
overtime|сверхурочные|⏰
promotion|повышение|⬆️
resignation|увольнение по желанию|📄
dismissal|увольнение|❌
interview|собеседование|🎤
CV|резюме|📄
reference|рекомендация|📝
contract|контракт|📜
wage|зарплата (почасовая)|💰
bonus|бонус|🎁
deadline|дедлайн|⏰
colleague|коллега|🤝
intern|стажёр|🎓
apprentice|ученик (проф.)|🛠️
retirement|выход на пенсию|👴
to apply|подавать заявку|📄
to resign|уволиться|🚪
to fire|увольнять|❌
to hire|нанимать|✅
to promote|повышать|⬆️
to retire|выходить на пенсию|👴
to commute|ездить на работу|🚆
part-time|неполный день|⏱️
full-time|полный день|🕘
self-employed|самозанятый|💼
unemployed|безработный|📉
skilled|квалифицированный|⭐
unskilled|неквалифицированный|🔧
work-life balance|баланс работы и жизни|⚖️
job satisfaction|удовлетворённость работой|😊
career change|смена карьеры|🔄
""",
        "city": """
downtown|центр города|🏙️
suburb|пригород|🏘️
pedestrian|пешеход|🚶
crosswalk|переход|🚸
junction|перекрёсток|🚦
roundabout|круговое движение|🔄
pavement|тротуар|🚶
 alley|алleya|🏘️
skyscraper|небоскрёб|🏙️
landmark|достопримечательность|📍
monument|памятник|🗿
statue|статуя|🗽
town hall|ратуша|🏛️
council|муниципалитет|🏛️
traffic jam|пробка|🚗
rush hour|час пик|⏰
public transport|общественный транспорт|🚌
commuter|пассажир-пendelnик|🚆
pollution|загрязнение|🏭
litter|мусор (на улице)|🗑️
to park|парковаться|🅿️
to fine|штрафовать|💸
to bypass|объезжать|🛣️
crowded|переполненный|👥
lively|оживлённый|🎉
run-down|запущенный|🏚️
gentrified|обновлённый район|✨
urban|городской|🏙️
rural|сельский|🌾
metropolitan|столичный|🌆
city centre|центр|📍
outskirts|окраина|🛣️
pedestrian zone|пешеходная зона|🚶
local council|местная власть|🏛️
""",
        "travel": """
backpack|рюкзак|🎒
suitcase|чемодан|🧳
guidebook|путеводитель|📖
itinerary|маршрут|🗺️
excursion|экскурсия|🚌
cruise|круиз|🚢
hostel|хостел|🛏️
motel|мотель|🏨
resort|курорт|🏖️
landmark|ориентир|📍
souvenir shop|магазин сувениров|🎁
border control|погранконтроль|🛂
duty-free|беспошлинная зона|🛍️
stopover|остановка по пути|✈️
layover|пересадка|🔄
jet lag|джетлаг|😴
travel insurance|страховка|🛡️
visa application|заявка на визу|📄
to book|бронировать|📱
to cancel|отменять|❌
to reschedule|переносить|📅
to explore|исследовать|🔍
to wander|бродить|🚶
to get lost|заблудиться|🗺️
scenic|живописный|🏞️
remote|отдалённый|🏕️
touristy|туристический|📸
off-season|не сезон|📉
peak season|высокий сезон|📈
all-inclusive|всё включено|🏖️
self-catering|самостоятельное питание|🍳
travel sickness|укачивание|🤢
customs declaration|таможенная декларация|📋
return ticket|обратный билет|🔄
""",
        "health": """
symptom|симптом|📋
diagnosis|диагноз|🩺
prescription|рецепт|📜
pharmacy|аптека|💊
surgeon|хирург|⚕️
dentist|стоматолог|🦷
therapist|терапевт|👨‍⚕️
ward|палата|🏥
clinic|клиника|🏥
emergency room|приёмное отделение|🚨
ambulance|скорая|🚑
bandage|бинт|🩹
injection|укол|💉
vaccine|вакцина|💉
allergy|аллергия|🤧
asthma|астма|🫁
insomnia|бессонница|😴
anxiety|тревога|😰
depression|депрессия|🌧️
obesity|ожирение|⚖️
to prescribe|прописывать лекарство|📜
to recover|выздоравливать|🌱
to sprain|растянуть (связки)|🦵
to bleed|кровоточить|🩸
to cough|кашлять|😷
chronic|хронический|📅
acute|острый|⚡
contagious|заразный|🦠
preventive|профилактический|🛡️
well-being|благополучие|🌿
side effect|побочный эффект|⚠️
check-up|осмотр|🩺
first aid|первая помощь|🆘
healthcare|здравоохранение|🏥
""",
        "technology": """
device|устройство|📱
gadget|гаджет|⌚
smartphone|смартфон|📱
laptop|ноутбук|💻
tablet|планшет|📱
charger|зарядка|🔌
battery|батарея|🔋
software|ПО|💾
hardware|железо|🖥️
update|обновление|🔄
download|скачивание|⬇️
upload|загрузка|⬆️
password|пароль|🔐
username|имя пользователя|👤
browser|браузер|🌐
website|сайт|🌍
link|ссылка|🔗
Wi-Fi|вай-фай|📶
bluetooth|бluetooth|📡
to install|устанавливать|💾
to delete|удалять|🗑️
to reboot|перезагружать|🔄
to hack|взламывать|🕵️
to backup|делать резервную копию|💾
wireless|беспроводной|📶
digital|цифровой|💻
offline|офлайн|📴
online|онлайн|🌐
user-friendly|удобный|👍
outdated|устаревший|📼
cutting-edge|передовой|🚀
tech-savvy|разбирающийся в технике|🧠
social media|соцсети|📱
cybersecurity|кибербезопасность|🛡️
""",
        "nature": """
forest|лес|🌲
meadow|луг|🌾
valley|долина|🏞️
waterfall|водопад|💧
cliff|скала|⛰️
cave|пещера|🕳️
island|остров|🏝️
coast|побережь|🌊
desert|пустыня|🏜️
volcano|вулкан|🌋
glacier|ледник|🧊
wildlife|дикая природа|🦌
habitat|среда обитания|🌍
ecosystem|экосистема|♻️
species|вид (биол.)|🐾
predator|хищник|🦁
prey|добыча|🐭
to bloom|цвести|🌸
to migrate|мигрировать|🦅
to extinct|вымереть|💀
renewable|возобновляемый|♻️
sustainable|устойчивый|🌱
biodiversity|биоразнообразие|🦋
pollution|загрязнение|🏭
recycle|перерабатывать|♻️
organic|органический|🌿
picturesque|живописный|📸
remote|глухой|🏕️
threatened|под угрозой|⚠️
conservation|охрана природы|🛡️
national park|нац. парк|🏞️
carbon footprint|углеродный след|👣
climate change|изменение климата|🌡️
natural disaster|стихийное бедствие|🌪️
""",
    },
}

# Extend script output - for brevity in build, we'll append B1-C2 in the same script via exec of part 2
# Run builds words only for A2 first; B1-C2 added in vocabulary_a2_c2_data.py import

if __name__ == "__main__":
    print("Topics A2:", list(DATA["A2"].keys()))
    for tid, block in DATA["A2"].items():
        n = len(_parse_block(block.strip().split("\n")))
        print(f"  {tid}: {n}")
