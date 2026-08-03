"""
Голосовые поздравления Рико для призов 1 / 2 / 3 места (~30 сек озвучки).
"""

from __future__ import annotations

CONGRATS_BY_PLACE: dict[int, dict[str, str]] = {
    1: {
        "title_ru": "🏆 Легенда LexDan",
        "en": (
            "My dear friend… Stop for a moment and feel this. "
            "You did not simply win a contest — you became a Legend of LexDan. "
            "Day after day you chose patience when quitting looked easier. "
            "You chose quiet strength when English felt heavy. "
            "You chose courage when nobody was watching. "
            "That is how legends are written — not with noise, but with heart. "
            "From this day the kingdom remembers your name. "
            "Wear your title with pride. I am Rico — and I am endlessly proud of you."
        ),
        "ru": (
            "Мой дорогой друг… Остановись на мгновение и почувствуй это. "
            "Ты не просто выиграл состязание — ты стал Легендой LexDan. "
            "День за днём ты выбирал терпение, когда сдаться казалось проще. "
            "Ты выбирал тихую силу, когда английский казался тяжёлым. "
            "Ты выбирал смелость, когда никто не смотрел. "
            "Так пишутся легенды — не шумом, а сердцем. "
            "С этого дня королевство помнит твоё имя. "
            "Носи свой титул с гордостью. Я Рико — и я бесконечно тобой горжусь."
        ),
    },
    2: {
        "title_ru": "🥈 Мастер коллекции",
        "en": (
            "Listen closely. Do you hear that sparkle in your voice? "
            "That is mastery. You are a true Master of LexDan. "
            "You collected rare words like treasures, and you practiced with patience. "
            "When others rushed, you stayed focused. When it was hard, you returned again. "
            "Real power is not loud — it is steady, curious, and kind. "
            "Keep polishing your English like a jewel. "
            "I am Rico, and I see a Master standing right in front of me."
        ),
        "ru": (
            "Послушай внимательно. Слышишь этот блеск в своём голосе? "
            "Это мастерство. Ты настоящий Мастер LexDan. "
            "Ты собирал редкие слова как сокровища и тренировался с терпением. "
            "Когда другие торопились — ты оставался собранным. Когда было трудно — ты возвращался снова. "
            "Настоящая сила не кричит — она устойчива, любопытна и добра. "
            "Продолжай шлифовать английский, как драгоценный камень. "
            "Я Рико, и я вижу Мастера прямо перед собой."
        ),
    },
    3: {
        "title_ru": "🥉 Охотник за картами",
        "en": (
            "There you are — sharp-eyed and brave. "
            "You are a true Hunter of LexDan. "
            "You chased mistakes through the fog and caught the truth with patience. "
            "You did not fear the riddles. You did not fear the climb. "
            "Hunters win with focus, courage, and a calm heart. "
            "Keep following the trail of better English — card by card, day by day. "
            "I am Rico, and the forest cheers for its Hunter."
        ),
        "ru": (
            "Вот ты — зоркий и смелый. "
            "Ты настоящий Охотник LexDan. "
            "Ты преследовал ошибки сквозь туман и ловил правду терпением. "
            "Ты не испугался загадок. Ты не испугался подъёма. "
            "Охотники побеждают вниманием, отвагой и спокойным сердцем. "
            "Продолжай след лучшего английского — карта за картой, день за днём. "
            "Я Рико, и лес рукоплещет своему Охотнику."
        ),
    },
}


def get_congrats(place: int) -> dict[str, str] | None:
    return CONGRATS_BY_PLACE.get(int(place))
