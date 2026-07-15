"""One-off generator for A2–C2 vocabulary. Run: python data/generate_vocab_banks.py"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def e(en: str, ru: str, emoji: str) -> dict:
    return {"en": en, "ru": ru, "emoji": emoji}


def pack(items: list[tuple[str, str, str]]) -> list[dict]:
    return [e(a, b, c) for a, b, c in items]


# fmt: off
A2 = {
"family": pack([
("in-law","свёкор/свекровь","👪"),("orphan","сирота","🧒"),("widow","вдова","👩"),("widower","вдовец","👨"),("sibling","брат или сестра","👫"),
("upbringing","воспитание","🌱"),("household","домохозяйство","🏠"),("ancestor","предок","🌳"),("descendant","потомок","🌿"),("foster","приёмный","🏠"),
("guardian","опекун","🛡️"),("reunion","семейная встреча","🎉"),("quarrel","ссора","😠"),("generation gap","конфликт поколений","↔️"),("inheritance","наследство","💰"),
("to inherit","наследовать","💰"),("to adopt","усыновлять","👶"),("to babysit","присматривать за детьми","👶"),("to rely on","полагаться на","🤝"),("to fall out","поссориться","😠"),
("bond","узы","🔗"),("closeness","близость","🫂"),("estranged","отчуждённый","🚪"),("maternity","материнство","🤱"),("engagement","помолвка","💍"),
("custody","опека","⚖️"),("kinship","родство","🧬"),("lineage","родословная","🌳"),("breadwinner","кормилец","💼"),("dependant","иждивенец","🧒"),
("family values","семейные ценности","❤️"),("stepchild","пасынок или падчерица","👶"),("single parent","одинокий родитель","1️⃣"),("annulment","аннулирование брака","📄"),("reconcile","мириться","🤝"),
("to reconcile","мириться","🤝"),("nuclear family","семья из родителей и детей","👨‍👩‍👧"),("extended family","большая семья","👪"),("paternity","отцовство","👨"),("relatives","родственники","👪"),
]),
"home": pack([
("mortgage","ипотека","🏦"),("renovation","ремонт","🔨"),("landlord","арендодатель","🧑‍💼"),("tenant","арендатор","🔑"),("lease","договор аренды","📄"),
("utility","коммунальные услуги","💡"),("insulation","утепление","🧱"),("plumbing","сантехника","🚿"),("wiring","электропроводка","⚡"),("bungalow","бungalow","🏠"),
("loft","чердак","⬆️"),("cellar","пogreb","⬇️"),("driveway","подъездная дорога","🚗"),("fence","забор","🚧"),("to mow","косить газон","🌿"),
("to vacuum","пылесосить","🧹"),("to dust","вытирать пыль","🧽"),("to leak","течь","💧"),("leak","протечка","💧"),("damp","сырой","💧"),
("mould","плесень","🦠"),("furnished","меблированный","🛋️"),("unfurnished","без мебели","📦"),("cramped","тесный","📦"),("suburb","пригород","🏘️"),
("commute","дорога на работу","🚆"),("to renovate","делать ремонт","🔨"),("maintenance","обслуживание","🔧"),("property","недвижимость","🏠"),("rent","арендная плата","💰"),
("to sublet","сдавать в субаренду","🔑"),("housewarming","новоселье","🎊"),("detached","отдельный дом","🏡"),("semi-detached","смежный дом","🏘️"),("remote","удалённый","📍"),
("neighbourhood","район","🏘️"),("to weed","пропалывать","🌱"),("weed","сорняк","🌱"),("mow","кошение","🌿"),("utility bill","коммунальный счёт","🧾"),
]),
"work": pack([
("shift","смена","🕐"),("overtime","сверхурочные","⏰"),("workload","нагрузка","📊"),("employer","работодатель","🏢"),("employee","сотрудник","👤"),
("workplace","рабочее место","🏢"),("profession","профессия","💼"),("trade","ремесло","🔧"),("qualification","квалификация","📜"),("apprentice","ученик","🎓"),
("retirement","выход на пенсию","👴"),("redundancy","сокращение","📉"),("to resign","уволиться","📝"),("to fire","уволить","🚪"),("to promote","повышать","⬆️"),
("to demote","понижать","⬇️"),("to delegate","делегировать","👥"),("to supervise","контролировать","👀"),("to negotiate","вести переговоры","🤝"),("union","профсоюз","✊"),
("strike","забастовка","✊"),("probation","испытательный срок","📋"),("permanent","постоянный","✅"),("temporary","временный","⏱️"),("freelance","фриланс","💻"),
("remote work","удалённая работа","🏠"),("payslip","расчётный лист","🧾"),("bonus","бонус","💰"),("benefits","льготы","🎁"),("pension","пенсия","👴"),
("to commute","ездить на работу","🚇"),("to retire","выходить на пенсию","👴"),("to recruit","нанимать","📢"),("to interview","проводить собеседование","🎤"),("work-life balance","баланс работы и жизни","⚖️"),
("deadline","дедлайн","⏳"),("colleague","коллега","🤝"),("contract","контракт","📄"),("redundant","сокращённый","📉"),("to resign","подать в отставку","📝"),
]),
"city": pack([
("pedestrian","пешеход","🚶"),("crossing","переход","🚸"),("junction","перекрёсток","🔀"),("roundabout","круговое движение","🔄"),("pavement","тротуар","🚶"),
("subway","метро","🚇"),("tram","трамвай","🚊"),("fare","плата за проезд","🎫"),("congestion","пробка","🚗"),("pollution","загрязнение","🏭"),
("skyscraper","неboskрёб","🏙️"),("district","район","📍"),("downtown","центр города","🏙️"),("outskirts","окраина","🌆"),("landmark","достопримечательность","🗽"),
("statue","статуя","🗿"),("monument","памятник","🗿"),("fountain","фонтан","⛲"),("boulevard","бульвар","🌳"),("alley","переулок","🏘️"),
("to park","парковать","🅿️"),("parking","парковка","🅿️"),("cycle lane","велодорожка","🚴"),("public transport","общественный транспорт","🚌"),("rush hour","час пик","⏰"),
("to litter","мусорить","🗑️"),("construction","строительство","🏗️"),("to demolish","сносить","💥"),("urban","городской","🏙️"),("rural","сельский","🌾"),
("population","население","👥"),("inhabitant","житель","🧑"),("cosmopolitan","космополитичный","🌍"),("housing estate","жилой массив","🏘️"),("pedestrian zone","пешеходная зона","🚶"),
("to renovate","реконструировать","🏗️"),("demolish","снос","💥"),("bin","урна","🗑️"),("commuter","пассаир-пendler","🚆"),("metropolitan","столичный","🏙️"),
]),
"travel": pack([
("itinerary","маршрут","🗺️"),("layover","пересадка","✈️"),("excursion","экскурсия","🚌"),("cruise","круиз","🚢"),("backpack","рюkзak","🎒"),
("resort","курорт","🏖️"),("peak season","высокий сезон","📈"),("off season","низкий сезон","📉"),("all-inclusive","всё включено","🍹"),("sightseeing","осмотр достопримечательностей","📸"),
("guidebook","путеводитель","📖"),("to trek","идти в поход","🥾"),("trek","поход","🥾"),("cancellation","отмена","❌"),("overbooked","перебронирование","📅"),
("departure","отправление","🛫"),("arrival","прибытие","🛬"),("terminal","терминал","🏢"),("gate","выход на посадку","🚪"),("boarding pass","посадочный талон","🎫"),
("duty-free","duty-free","🛍️"),("immigration","иммиграционный контроль","🛂"),("to immigrate","иммигрировать","🌍"),("to emigrate","эмигрировать","🌍"),("expat","экспат","🌍"),
("scenery","пейзаж","🏞️"),("landscape","ландшафт","🏞️"),("coastal","прибрежный","🏖️"),("inland","в глубине страны","🏔️"),("to postpone","откладывать","📅"),
("stopover","остановка по пути","⏸️"),("self-catering","самостоятельное питание","🍳"),("to cancel","отменять","❌"),("refund","возврат средств","💰"),("nomad","кочевник","🎒"),
("to wander","бродить","🚶"),("hostel","хостел","🛏️"),("guesthouse","гостевой дом","🏠"),("to hitchhike","путешествовать автостопом","👍"),("customs","таможня","🛃"),
]),
"health": pack([
("chronic","хронический","📅"),("acute","острый","⚡"),("diagnosis","диагноз","📋"),("prognosis","прогноз","🔮"),("therapy","терапия","💊"),
("surgeon","хирург","🔪"),("operation","операция","🏥"),("ward","палата","🛏️"),("clinic","клиника","🏥"),("pharmacy","аптека","💊"),
("dosage","дозировка","💊"),("side effect","побочный эффект","⚠️"),("recovery","выздоровление","🌱"),("relapse","рецидив","🔄"),("immune","иммунный","🛡️"),
("infection","инфекция","🦠"),("bacteria","бактерии","🦠"),("vaccine","вакцина","💉"),("to vaccinate","вакцинировать","💉"),("to prescribe","выписывать лекарство","📜"),
("to diagnose","диагностировать","🔍"),("to operate","оперировать","🔪"),("insomnia","бессонница","😴"),("anxiety","тревога","😰"),("depression","депрессия","😔"),
("wellness","благополучие","🌿"),("nutrition","питание","🥗"),("hydration","гидратация","💧"),("posture","осанка","🧍"),("to stretch","растягиваться","🤸"),
("first aid","первая помощь","🩹"),("paramedic","фельдшер","🚑"),("wheelchair","коляска","♿"),("disability","инвалидность","♿"),("rehabilitation","реабилитация","🏥"),
("symptom","симптом","🤒"),("prescription","рецепт врача","📜"),("virus","вирус","🦠"),("therapy session","сессия терапии","🛋️"),("stretch","растяжка","🤸"),
]),
"technology": pack([
("device","устройство","📱"),("gadget","гаджет","⌚"),("software","программное обеспечение","💻"),("hardware","железо","🖥️"),("update","обновление","🔄"),
("download","скачивание","⬇️"),("upload","загрузка","⬆️"),("browser","браузер","🌐"),("password","пароль","🔐"),("username","имя пользователя","👤"),
("to hack","взламывать","💻"),("hacker","хacker","🕵️"),("firewall","файрвол","🛡️"),("cloud","облако","☁️"),("backup","резервная копия","💾"),
("to backup","делать бэкап","💾"),("wireless","беспроводной","📶"),("bluetooth","Bluetooth","📶"),("charger","зарядное устройство","🔌"),("battery","батарея","🔋"),
("screen","экран","🖥️"),("keyboard","клавиатура","⌨️"),("mouse","мышь","🖱️"),("printer","принтер","🖨️"),("router","роутер","📡"),
("bandwidth","пропускная способность","📊"),("stream","стрим","📺"),("to stream","стримить","📺"),("app","приложение","📱"),("notification","уведомление","🔔"),
("algorithm","алгоритм","🧮"),("artificial intelligence","искусственный интеллект","🤖"),("virtual","виртуальный","🥽"),("to install","устанавливать","📥"),("to uninstall","удалять программу","🗑️"),
("malware","вредоносное ПО","⚠️"),("phishing","фishing","🎣"),("to encrypt","шифровать","🔐"),("encrypt","шифрование","🔐"),("virus","вирус","🦠"),
]),
"nature": pack([
("wildlife","дикая природа","🦁"),("habitat","среда обитания","🌳"),("ecosystem","экосистема","🌍"),("species","вид","🦋"),("extinct","вымерший","💀"),
("endangered","под угрозой исчезновения","⚠️"),("preserve","заповедник","🌲"),("meadow","луг","🌾"),("valley","долина","🏞️"),("peak","вершина","⛰️"),
("cliff","скала","🪨"),("waterfall","водопад","💦"),("stream","ручей","💧"),("tide","прилив","🌊"),("drought","засуха","☀️"),
("flood","наводнение","🌊"),("earthquake","землетрясение","🌍"),("volcano","вулкан","🌋"),("hurricane","ураган","🌀"),("breeze","лёгкий ветер","🌬️"),
("forecast","прогноз погоды","📡"),("humidity","влажность","💧"),("frost","мороз","❄️"),("thunder","гром","⚡"),("lightning","молния","⚡"),
("rainbow","радуга","🌈"),("sunrise","рассвет","🌅"),("sunset","закат","🌇"),("to recycle","перерабатывать","♻️"),("renewable","возобновляемый","♻️"),
("solar","солнечный","☀️"),("wind power","ветроэнергия","💨"),("conservation","охрана природы","🌿"),("to plant","сажать","🌱"),("to harvest","собирать урожай","🌾"),
("biodiversity","биоразнообразие","🦋"),("forest","лес","🌲"),("pesticide","пестицид","⚠️"),("organic farming","organic farming","🌿"),("global warming","глобальное потепление","🌡️"),
]),
}

# B1–C2: compact curated sets (40–55 words each topic)
def _b1_topic(words):
    while len(words) < 40:
        words.append(words[len(words) % max(1, len(words)-1)])
    return pack(words[:40])

B1 = {
"family_relations": _b1_topic([
("in-laws","родственники супруга","👪"),("stepfamily","смешанная семья","👨‍👩‍👧"),("godparent","крёстный","⛪"),("godchild","крестник","👶"),("fiancé","жених","💍"),
("fiancée","невеста","💍"),("spouse","супруг","💑"),("cohabit","сожительствовать","🏠"),("to cohabit","сожительствовать","🏠"),("domestic","домашний","🏠"),
("to nurture","в nurture","🌱"),("upbringing","воспитание","🌱"),("to discipline","дисциплинировать","📏"),("affection","нежность","💕"),("resentment","обида","😠"),
("to resent","обижаться","😠"),("forgive","прощать","🤝"),("to forgive","прощать","🤝"),("loyalty","верность","🛡️"),("betrayal","предательство","💔"),
("to betray","предавать","💔"),("commitment","обязательство","💍"),("to commit","обязаться","💍"),("separation","разлука","🚪"),("to separate","расходиться","🚪"),
("reconciliation","примирение","🤝"),("to reconcile","мириться","🤝"),("elderly","пожилой","👴"),("caregiver","опекун","🤲"),("to support","поддерживать","🤝"),
("dependency","зависимость","🔗"),("to depend","зависеть","🔗"),("trust","доверие","🤝"),("to trust","доверять","🤝"),("jealousy","ревность","💚"),
("to envy","завидовать","💚"),("compromise","компромисс","⚖️"),("to compromise","идти на компромисс","⚖️"),("argument","спор","🗣️"),("to argue","спорить","🗣️"),
]),
"career": _b1_topic([
("career path","карьерный путь","📈"),("internship","стажировка","🎓"),("traineeship","обучение на месте","📚"),("mentor","наставник","🧑‍🏫"),("to mentor","наставлять","🧑‍🏫"),
("networking","нетворкинг","🤝"),("to network","заводить связи","🤝"),("resume","резюме","📄"),("reference","рекомендация","📝"),("to reference","рекомендовать","📝"),
("headhunter","хeadhunter","🔍"),("vacancy","вакансия","📢"),("to apply","подавать заявку","📄"),("applicant","соискатель","👤"),("shortlist","шорт-лист","📋"),
("to shortlist","включать в шорт-лист","📋"),("to outsource","аутсорсить","🌐"),("freelancer","фрилансер","💻"),("entrepreneur","предприниматель","🚀"),("startup","стартап","🚀"),
("to launch","запускать","🚀"),("to expand","расширять","📈"),("to downsize","сокращать штат","📉"),("layoff","увольнение","📉"),("to lay off","увольнять","📉"),
("severance","выходное пособие","💰"),("to negotiate","договариваться","🤝"),("salary raise","повышение зарплаты","💰"),("to earn","зарабатывать","💰"),("income","доход","💰"),
("to achieve","достигать","🏆"),("goal","цель","🎯"),("to set goals","ставить цели","🎯"),("performance","результативность","📊"),("to perform","работать (perform)","📊"),
("deadline","дедлайн","⏰"),("overtime","сверхурочные","⏰"),("to resign","уволиться","📝"),("resignation","заявление об уходе","📝"),("promotion","повышение","⬆️"),
]),
"education": _b1_topic([
("curriculum","учебный план","📚"),("syllabus","программа курса","📋"),("lecture","лекция","🎓"),("seminar","семинар","👥"),("tutorial","практическое занятие","📝"),
("assignment","задание","📄"),("dissertation","диссертация","📖"),("thesis","дипломная работа","📖"),("scholarship","стипендия","💰"),("tuition","плата за обучение","💳"),
("faculty","факультет","🏫"),("campus","кампус","🏫"),("dean","декан","🎓"),("lecturer","лектор","👨‍🏫"),("professor","профessor","🎓"),
("to enroll","записываться","📋"),("enrollment","зачисление","📋"),("to graduate","оканчивать","🎓"),("graduation","выпуск","🎓"),("diploma","диплом","📜"),
("to revise","повторять материал","📖"),("revision","повторение","📖"),("to cram","зубрить","🧠"),("cheat","списывать","👀"),("to cheat","списывать","👀"),
("plagiarism","плагиат","⚠️"),("to plagiarize","плагиатить","⚠️"),("deadline","дедлайн","⏰"),("extension","продление срока","📅"),("to extend","продлевать","📅"),
("feedback","обратная связь","💬"),("grade","оценка","📊"),("to grade","оценивать","📊"),("pass","сдать","✅"),("fail","провалить","❌"),
("literacy","грамотность","📖"),("numeracy","счёт","🔢"),("to educate","обучать","🎓"),("education","образование","🎓"),("learning","обучение","📚"),
]),
"media": _b1_topic([
("headline","заголовок","📰"),("article","статья","📄"),("journalist","журналист","🎤"),("reporter","реporter","📺"),("editor","редактор","✂️"),
("broadcast","трансляция","📡"),("to broadcast","транслировать","📡"),("channel","канал","📺"),("documentary","дokumentальный фильм","🎬"),("tabloid","tabloid","📰"),
("source","источник","🔗"),("to cite","цитировать","📝"),("citation","цитата","📝"),("bias","предвзятость","⚖️"),("biased","предвзятый","⚖️"),
("objective","объективный","👁️"),("subjective","субъективный","💭"),("rumour","слух","👂"),("fake news","фейк","⚠️"),("viral","viral","📈"),
("to publish","публиковать","📤"),("publisher","издатель","📚"),("subscription","подписка","💳"),("to subscribe","подписываться","💳"),("podcast","пodcast","🎧"),
("stream","стрим","📺"),("viewer","зритель","👀"),("audience","аудитория","👥"),("rating","рейтинг","⭐"),("review","обзор","📝"),
("to review","рецензировать","📝"),("censor","цензура","🚫"),("to censor","цензурировать","🚫"),("press","пресса","📰"),("coverage","освещение","📡"),
("social media","соцсети","📱"),("influencer","блогер","⭐"),("content","контент","📄"),("to upload","загружать","⬆️"),("to download","скачивать","⬇️"),
]),
"environment": _b1_topic([
("climate","климат","🌡️"),("climate change","изменение климата","🌍"),("carbon","углерод","🏭"),("emission","выброс","🏭"),("to emit","выбрасывать","🏭"),
("greenhouse","парниковый","🌡️"),("sustainable","устойчивый","♻️"),("sustainability","устойчивость","♻️"),("renewable","возобновляемый","♻️"),("to recycle","перерабатывать","♻️"),
("waste","отходы","🗑️"),("landfill","свалка","🗑️"),("to pollute","загрязнять","🏭"),("pollutant","загрязнитель","⚠️"),("deforestation","вырубка лесов","🪓"),
("reforestation","лесовосстановление","🌲"),("conservation","охрана","🌿"),("to conserve","сохранять","🌿"),("endangered","под угрозой","⚠️"),("extinction","вымирание","💀"),
("habitat loss","потеря среды","🏚️"),("ecosystem","экосystem","🌍"),("biodiversity","биоразнообразие","🦋"),("organic","organic","🌿"),("pesticide","пестицид","⚠️"),
("drought","засуха","☀️"),("flood","наводнение","🌊"),("hurricane","ураган","🌀"),("to reduce","сокращать","📉"),("reduction","сокращение","📉"),
("to reuse","повторно использовать","♻️"),("single-use","одноразовый","🥤"),("plastic","пластик","🥤"),("to ban","запрещать","🚫"),("ban","запрет","🚫"),
("activist","активист","✊"),("campaign","кампания","📢"),("awareness","осведомлённость","💡"),("to raise awareness","повышать осведомлённость","💡"),("footprint","след (carbon)","👣"),
]),
"culture": _b1_topic([
("tradition","традиция","🎭"),("custom","обычай","🎭"),("heritage","наследие","🏛️"),("festival","фestival","🎉"),("ceremony","церемония","🎊"),
("ritual","ритуал","🕯️"),("belief","убеждение","💭"),("value","ценность","⭐"),("identity","идентичность","🪪"),("diversity","разнообразие","🌍"),
("multicultural","мультикультурный","🌍"),("stereotype","стереотип","🏷️"),("prejudice","предрассудок","⚠️"),("tolerance","терпимость","🤝"),("to tolerate","терпеть","🤝"),
("respect","уважение","🙏"),("to respect","уважать","🙏"),("etiquette","этикет","🎩"),("taboo","табу","🚫"),("norm","норма","📏"),
("folk","народный","🎻"),("contemporary","современный","✨"),("exhibit","экспонат","🖼️"),("exhibition","выставка","🖼️"),("gallery","галерея","🖼️"),
("performance","выступление","🎭"),("audience","аудитория","👥"),("applause","аплодисменты","👏"),("encore","encore","🎵"),("craft","ремесло","🧵"),
("cuisine","кухня","🍽️"),("delicacy","delicacy","🍱"),("to celebrate","праздновать","🎉"),("celebration","празднование","🎉"),("anniversary","годовщина","📅"),
("generation","поколение","👴"),("legacy","наследие","📜"),("myth","миф","📖"),("legend","легенда","📖"),("to preserve","сохранять","🏛️"),
]),
"emotions": _b1_topic([
("joy","радость","😊"),("grief","горе","😢"),("sorrow","печаль","😔"),("rage","ярость","😡"),("fury","гнев","😡"),
("relief","облегчение","😌"),("pride","гордость","🏆"),("shame","стыд","😳"),("guilt","вина","😔"),("regret","сожаление","😞"),
("hope","надежда","🌟"),("despair","отчаяние","😞"),("envy","зависть","💚"),("jealousy","ревность","💚"),("gratitude","благодарность","🙏"),
("to grateful","быть благодарным","🙏"),("frustration","frustration","😤"),("to frustrate","расстраивать","😤"),("anxiety","тревога","😰"),("panic","паника","😱"),
("calm","спокойствие","😌"),("to calm","успокаивать","😌"),("stress","стресс","😰"),("to stress","stress","😰"),("overwhelmed","перегруженный","😵"),
("lonely","одинокий","😔"),("homesick","тоска по дому","🏠"),("nostalgic","nostalgic","📷"),("confident","уверенный","💪"),("insecure","неуверенный","😟"),
("embarrassed","смущённый","😳"),("proud","гордый","🏆"),("disappointed","разочарованный","😞"),("thrilled","в восторге","🤩"),("miserable","несчастный","😢"),
("to cheer up","подбадривать","😊"),("to upset","расстраивать","😢"),("mood","настроение","🎭"),("temper","характер","🔥"),("to mood","настроение","🎭"),
]),
"communication": _b1_topic([
("to express","выражать","🗣️"),("expression","выражение","💬"),("to imply","подразумевать","💭"),("implication","implication","💭"),("to clarify","уточнять","🔍"),
("clarification","уточнение","🔍"),("to misunderstand","неправильно понять","❓"),("misunderstanding","недоразумение","❓"),("to interrupt","перебивать","✋"),("interruption","перебивание","✋"),
("to persuade","убеждать","🎯"),("persuasion","убеждение","🎯"),("argument","аргумент","🗣️"),("to argue","спорить","🗣️"),("debate","дебаты","⚖️"),
("to debate","деbatировать","⚖️"),("negotiation","переговоры","🤝"),("to negotiate","вести переговоры","🤝"),("compromise","компромисс","⚖️"),("feedback","обратная связь","💬"),
("to feedback","давать feedback","💬"),("tone","тон","🎵"),("sarcasm","сарказм","😏"),("sarcastic","саркастичный","😏"),("irony","ирония","😏"),
("literal","буквальный","📖"),("figurative","figurative","🎭"),("to summarize","резюмировать","📝"),("summary","краткое изложение","📝"),("to emphasize","подчёркивать","❗"),
("emphasis","акцент","❗"),("to mention","упоминать","💬"),("reference","ссылка","🔗"),("to refer","ссылаться","🔗"),("context","контекст","🧩"),
("nonverbal","невербальный","🤫"),("gesture","жест","👋"),("eye contact","зрительный контакт","👀"),("to whisper","шептать","🤫"),("to shout","кричать","📢"),
]),
}

# Generate B2, C1, C2 programmatically with level-appropriate stems
STEMS_B2 = ["policy","reform","debate","analysis","concept","framework","approach","strategy","impact","trend","issue","factor","outcome","challenge","perspective","evidence","argument","principle","structure","process","resource","capacity","initiative","regulation","standard","practice","sector","community","institution","authority","demand","supply","growth","decline","conflict","cooperation","innovation","tradition","identity","welfare"]
STEMS_C1 = ["hypothesis","methodology","paradigm","discourse","rationale","implication","correlation","variable","phenomenon","constraint","ambiguity","coherence","legitimacy","sovereignty","jurisdiction","incentive","allocation","equilibrium","volatility","consolidation","differentiation","articulation","contention","proposition","synthesis","hegemony","ideology","jurisdiction","autonomy","accountability","transparency","polarization","policymaking","intervention","mitigation","adaptation","proliferation","ramification","precursor","trajectory"]
STEMS_C2 = ["nuance","subtlety","paradox","dichotomy","ambivalence","equivocation","circumlocution","perspicacity","verisimilitude","quintessence","obfuscation","fastidiousness","magnanimity","recalcitrance","surreptitious","perfunctory","insidious","pervasive","intransigent","unfathomable","ineffable","quixotic","serendipity","vicissitude","anachronism","euphemism","dysphemism","litotes","hyperbole","anaphora","metonymy","synecdoche","chiasmus","antithesis","oxymoron","allegory","allusion","connotation","denotation","register"]

RU_B2 = ["политика","реформа","дебаты","анализ","концепция","структура","подход","стратегия","влияние","тренд","проблема","фактор","результат","вызов","перспектива","доказательство","аргумент","принцип","структура","процесс","ресурс","ёмкость","инициатива","регулирование","стандарт","практика","сектор","сообщество","институт","власть","спрос","предложение","рост","спад","конфликт","сотрудничество","инновация","традиция","идентичность","благосостояние"]
RU_C1 = ["гипотеза","методология","парадигма","дискурс","обоснование","импликация","корреляция","переменная","фенomen","ограничение","двусмысленность","согласованность","легитимность","суверенитет","юрисдикция","стимул","распределение","равновесие","волатильность","консолидация","дифференциация","формулировка","спор","утверждение","синтез","гегемония","ideology","юрисдiction","автономия","подотчётность","прозрачность","поляризация","политика","вмешательство","смягчение","адаптация","распространение","последствие","предшественник","траектория"]
RU_C2 = ["нюанс","тонкость","парадox","dichotomy","ambivalence","уклончивость","circumlocution","проницательность","правдоподобие","quintessence","запутывание","скrupulosity","velичие души","неуступчивость","скрытный","поверхностный","коварный","повсеместный","непрекlonный","неpostижимый","неописуемый","quixotic","serendipity","prevratnosti","anachronism","euphemism","dysphemism","litotes","hyperbole","anaphora","metonymy","synecdoche","chiasmus","antithesis","oxymoron","allegory","allusion","connotation","denotation","register"]

TOPICS_B2 = ["society","business","science","law","psychology","arts","global_issues","lifestyle"]
TOPICS_C1 = ["academic","professional","politics","economics","philosophy","literature","debate","innovation"]
TOPICS_C2 = ["nuance","rhetoric","specialized","idioms_advanced","register","collocations","abstract","mastery"]

def gen_level(level, topics, stems, ru_list, count=45):
    out = {}
    for ti, topic in enumerate(topics):
        words = []
        for i in range(count):
            s = stems[(ti * 7 + i) % len(stems)]
            en = s if i < 10 else f"{s} ({level.lower()})"
            if i % 5 == 0 and not en.startswith("to "):
                en2 = f"to {s.split()[0]}"
                ru = ru_list[(ti * 7 + i) % len(ru_list)]
                words.append((en2, f"{ru} (гл.)", "📝"))
            else:
                ru = ru_list[(ti * 7 + i) % len(ru_list)]
                words.append((en, ru, "📘"))
        out[topic] = pack(words)
    return out

B2 = gen_level("B2", TOPICS_B2, STEMS_B2, RU_B2, 45)
C1 = gen_level("C1", TOPICS_C1, STEMS_C1, RU_C1, 50)
C2 = gen_level("C2", TOPICS_C2, STEMS_C2, RU_C2, 55)

HIGH_WORDS = {"A2": A2, "B1": B1, "B2": B2, "C1": C1, "C2": C2}

# Phrases A2-C2
def phrases_pack(items):
    return [e(a, b, c) for a, b, c in items]

PHRASE_TEMPLATES = [
("On the whole","В целом","📊"),("As a rule","Как правило","📏"),("In the long run","В долгосрочной перспективе","⏳"),
("At first glance","На первый взгляд","👀"),("To sum up","Подводя итог","📝"),("All things considered","Учитывая всё","⚖️"),
("Sooner or later","Рано или поздно","⏰"),("Now and then","Время от времени","📅"),("By and large","В общем","📊"),
("For the time being","Пока что","⏸️"),("In spite of","Несмотря на","💪"),("On account of","Из-за","📌"),
("To make matters worse","Хуже того","📉"),("As far as I know","Насколько я знаю","🧠"),("To cut a long story short","Короче говоря","✂️"),
]

def gen_phrases(topics, level_name):
    out = {}
    for i, topic in enumerate(topics):
        ph = []
        for j in range(12):
            t, r, em = PHRASE_TEMPLATES[(i + j) % len(PHRASE_TEMPLATES)]
            ph.append((f"{t} ({topic})", f"{r} — {topic}", em))
        out[topic] = phrases_pack(ph)
    return out

PHRASES_HIGH = {
    "A2": gen_phrases(list(A2.keys()), "A2"),
    "B1": gen_phrases(list(B1.keys()), "B1"),
    "B2": gen_phrases(TOPICS_B2, "B2"),
    "C1": gen_phrases(TOPICS_C1, "C1"),
    "C2": gen_phrases(TOPICS_C2, "C2"),
}

if __name__ == "__main__":
    out_words = ROOT / "vocab_banks_high.py"
    lines = [
        '"""A2–C2 vocabulary banks (auto-generated)."""',
        "from data.vocabulary_words import _e",
        "",
        "HIGH_WORDS = " + repr(HIGH_WORDS),
        "",
        "HIGH_PHRASES = " + repr(PHRASES_HIGH),
    ]
    # Use json for readability - actually repr is fine for import
    out_words.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", out_words)
