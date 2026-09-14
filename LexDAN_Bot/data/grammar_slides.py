"""
Слайды теории Grammar.

Ручные оверрайды — в GRAMMAR_SLIDES.
Остальные темы собираются из rico_intro (narrative) автоматически.
"""

from __future__ import annotations

import re

# Ключ: "LEVEL:topic_id" или просто "topic_id"
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


def _strip_trailing_cta(chunk: str) -> str:
    """Убрать хвостики «пиши сюда / дальше задания» — CTA будет на последнем слайде."""
    t = chunk.strip()
    patterns = [
        r"\n*Дальше[^\n]*задан[^\n]*$",
        r"\n*Пиши вопрос[^\n]*$",
        r"\n*Я рядом[^\n]*$",
        r"\n*Вопросы пиши[^\n]*$",
    ]
    for p in patterns:
        t = re.sub(p, "", t, flags=re.I | re.M).strip()
    return t


def intro_to_slides(intro: str, *, ack: bool = False) -> list[str]:
    """
    Разбить rico_intro на 3–6 слайдов по абзацам.
    Последний слайд — короткий CTA.
    """
    text = (intro or "").strip()
    if not text:
        text = "🦜 <b>Рико:</b> Сейчас разберём эту тему шаг за шагом."

    parts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    parts = [_strip_trailing_cta(p) for p in parts if _strip_trailing_cta(p)]

    if not parts:
        parts = [text]

    # Слишком много кусков — склеиваем попарно
    while len(parts) > 5:
        merged: list[str] = []
        i = 0
        while i < len(parts):
            if i + 1 < len(parts) and len(parts) - i > 5 - len(merged):
                merged.append(parts[i] + "\n\n" + parts[i + 1])
                i += 2
            else:
                merged.append(parts[i])
                i += 1
        parts = merged

    # Один огромный абзац — режем по предложениям / буллетам
    if len(parts) == 1 and len(parts[0]) > 700:
        raw = parts[0]
        bullets = re.split(r"(?=\n• )", raw)
        bullets = [b.strip() for b in bullets if b.strip()]
        if len(bullets) >= 2:
            parts = bullets[:5]
        else:
            sents = re.split(r"(?<=[.!?…])\s+", raw)
            chunk: list[str] = []
            buf = ""
            for s in sents:
                if len(buf) + len(s) > 450 and buf:
                    chunk.append(buf.strip())
                    buf = s
                else:
                    buf = (buf + " " + s).strip()
            if buf:
                chunk.append(buf)
            parts = chunk[:5] or [raw]

    # Минимум 2 слайда теории + CTA
    if len(parts) == 1:
        mid = max(80, len(parts[0]) // 2)
        # режем по ближайшему пробелу/переносу
        cut = parts[0].rfind("\n", 0, mid)
        if cut < 40:
            cut = parts[0].rfind(" ", 0, mid)
        if cut > 40:
            parts = [parts[0][:cut].strip(), parts[0][cut:].strip()]

    if ack:
        cta = (
            "🦜 Готово с объяснением!\n\n"
            "Если что-то непонятно — жми <b>❓ Уточнить</b>.\n"
            "Когда ознакомишься — жми <b>✅ Ознакомился</b> ниже 💚"
        )
    else:
        cta = (
            "🦜 Готово с объяснением!\n\n"
            "Дальше — задания по теме.\n"
            "Если что-то непонятно — жми <b>❓ Уточнить</b>.\n\n"
            "Когда будешь готов — <b>📝 Перейти к заданиям</b> 💚"
        )

    # Не дублировать CTA, если уже похожий хвост
    if "Перейти к заданиям" not in parts[-1] and "Ознакомился" not in parts[-1]:
        parts.append(cta)
    else:
        parts[-1] = cta

    return parts


def get_manual_slides(level: str, topic_id: str) -> list[str] | None:
    for key in (slides_key(level, topic_id), topic_id):
        slides = GRAMMAR_SLIDES.get(key)
        if slides and len(slides) >= 2:
            return list(slides)
    return None
