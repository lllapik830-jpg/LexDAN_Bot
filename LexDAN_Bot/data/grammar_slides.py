"""
Слайды теории Grammar (как в онбординге to be).

Пока прототип: A0 · this_that.
Формат — список HTML-строк; навигация Далее/Назад/Уточнить.
"""

from __future__ import annotations

# Ключ: "LEVEL:topic_id"
GRAMMAR_SLIDES: dict[str, list[str]] = {
    "A0:this_that": [
        (
            "🦜 <b>Рико:</b> Сегодня разберём <b>this</b> и <b>that</b> — "
            "два маленьких слова, которые показывают «это рядом» или «то там».\n\n"
            "Без них сложно ткнуть на предмет и спросить «а что это?» 👆"
        ),
        (
            "<b>This</b> — когда предмет <b>близко</b> к тебе.\n"
            "<b>That</b> — когда <b>дальше</b> / вон там.\n\n"
            "• <b>This is a book.</b>\n"
            "<i>• Это книга. (вот она, рядом)</i>\n\n"
            "• <b>That is a car.</b>\n"
            "<i>• То — машина. (машина вон там)</i>"
        ),
        (
            "В разговоре часто слышишь вопросы:\n\n"
            "• <b>What's this?</b> — <i>Что это?</i> (рядом)\n"
            "• <b>What's that?</b> — <i>Что это там?</i> (дальше)\n\n"
            "Запомни коротко:\n"
            "<b>this</b> = «вот это» · <b>that</b> = «вон то» ✨"
        ),
        (
            "🦜 Готово с объяснением!\n\n"
            "Дальше — задания: выберешь форму, напишешь слово, "
            "переведёшь туда-сюда.\n"
            "Если что-то непонятно на слайде — жми <b>❓ Уточнить</b>.\n\n"
            "Когда будешь готов — <b>📝 Перейти к заданиям</b> 💚"
        ),
    ],
}


def slides_key(level: str, topic_id: str) -> str:
    return f"{level}:{topic_id}"


def get_grammar_slides(level: str, topic_id: str) -> list[str] | None:
    slides = GRAMMAR_SLIDES.get(slides_key(level, topic_id))
    if slides and len(slides) >= 2:
        return list(slides)
    return None


def has_grammar_slides(level: str, topic_id: str) -> bool:
    return get_grammar_slides(level, topic_id) is not None
