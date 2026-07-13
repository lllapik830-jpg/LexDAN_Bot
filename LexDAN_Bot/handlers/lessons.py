"""
Раздел «Уроки» + входной тест уровня.
В тесте: без объявления уровня и без объяснений — только задания.
"""

import logging
import os
import tempfile

from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from handlers.filters import ModeFilter
from handlers.keyboards import (
    lessons_home_first,
    lessons_home_levels,
    assess_translate_kb,
    assess_simple_kb,
)
from data.assessment_data import LEVELS, lower_level
from services.database import load_users, get_user, MODE_LESSONS
from services.assessment import (
    ensure_user_fields,
    start_assessment,
    set_translation_item,
    set_translate_estimate,
    begin_vocab,
    next_vocab,
    begin_listen,
    next_listen,
    begin_write,
    finish_assessment,
    adjust_level,
    average_level,
)
from services.assessment_gen import estimate_level_from_translation
from services.gpt import judge_translation, judge_vocab, judge_listening, judge_writing
from services.elevenlabs import elevenlabs_tts, mp3_to_ogg_opus

router = Router()

BTN_CHECK = "🎯 Проверить уровень"
BTN_AGAIN = "🎯 Пройти тест снова"
BTN_EASIER = "⬇️ Дай текст проще"
BTN_SKIP = "⏭️ Пропустить задание"


def lessons_keyboard_for(user: dict):
    ensure_user_fields(user)
    if user.get("assessment_done"):
        return lessons_home_levels()
    return lessons_home_first()


async def send_lessons_home(m: Message, intro: str | None = None):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_user_fields(user)

    if intro is None:
        if user.get("assessment_done"):
            intro = (
                f"📚 Уроки\n\n"
                f"Твой уровень: {user.get('level', 'A1')}.\n"
                f"Выбери уровень ниже."
            )
        else:
            intro = (
                "📚 Уроки\n\n"
                "Давай сначала быстро проверим твой уровень — минут 10.\n"
                "Перевод, слова, аудирование и короткое письмо.\n\n"
                "Когда будешь готов — жми «Проверить уровень»."
            )

    await m.reply(intro, reply_markup=lessons_keyboard_for(user))


def _is_nav_button(text: str) -> bool:
    return text in {
        BTN_CHECK,
        BTN_AGAIN,
        BTN_EASIER,
        BTN_SKIP,
        "🔙 Вернуться в меню",
        *LEVELS,
    }


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "да"}
    return False


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_CHECK)
@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_AGAIN)
async def start_level_test(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)

    if user.get("assessment_done"):
        await m.reply(
            "Тест уровня уже пройден — повторно его пройти нельзя.\n"
            "Выбери уровень для занятий ниже.",
            reply_markup=lessons_home_levels(),
        )
        return

    await m.reply("Секунду, готовлю тебе тест…")
    user = start_assessment(str(m.from_user.id))
    a = user["assessment"]
    await m.reply(
        "🎯 Тест уровня — задание 1/4: перевод\n\n"
        "Переведи текст на русский.\n"
        "Если сложно — нажми «Дай текст проще».\n\n"
        f"🇬🇧 Текст:\n{a['translate_source_en']}",
        reply_markup=assess_translate_kb(show_skip=False),
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_EASIER)
async def easier_text(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)
    a = user["assessment"]

    if a.get("phase") != "translate":
        await m.reply("Сейчас это недоступно.", reply_markup=lessons_keyboard_for(user))
        return

    cur = a.get("translate_level", "B2")
    if cur == "A0":
        if not a.get("a0_second_shown"):
            await m.reply("Готовлю другой текст…")
            user = set_translation_item(str(m.from_user.id), "A0", 1)
            a = user["assessment"]
            await m.reply(
                f"🇬🇧 Текст:\n{a['translate_source_en']}",
                reply_markup=assess_translate_kb(show_skip=True),
            )
        else:
            await m.reply(
                "Больше упрощать некуда. Переведи или нажми «Пропустить задание».",
                reply_markup=assess_translate_kb(show_skip=True),
            )
        return

    await m.reply("Готовлю текст проще…")
    new_level = lower_level(cur)
    user = set_translation_item(str(m.from_user.id), new_level, 0)
    a = user["assessment"]
    await m.reply(
        f"🇬🇧 Текст:\n{a['translate_source_en']}",
        reply_markup=assess_translate_kb(show_skip=False),
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_SKIP)
async def skip_translate(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)
    a = user["assessment"]

    if a.get("phase") != "translate":
        await m.reply("Сейчас нечего пропускать.", reply_markup=lessons_keyboard_for(user))
        return

    if a.get("translate_level") != "A0" or not a.get("a0_second_shown"):
        await m.reply(
            "Пропуск доступен после второго текста.",
            reply_markup=assess_translate_kb(show_skip=bool(a.get("a0_second_shown"))),
        )
        return

    set_translate_estimate(str(m.from_user.id), "A0")
    await _start_vocab_flow(m, "A0")


@router.message(ModeFilter(MODE_LESSONS), F.text.in_(LEVELS))
async def choose_level(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)

    if not user.get("assessment_done"):
        await m.reply("Сначала пройди проверку уровня.", reply_markup=lessons_home_first())
        return

    await m.reply(
        f"📚 Уровень {m.text}\n\nУроки по этому уровню скоро появятся.",
        reply_markup=lessons_home_levels(),
    )


@router.message(ModeFilter(MODE_LESSONS), F.text)
async def lessons_text(m: Message):
    text = (m.text or "").strip()
    if not text or _is_nav_button(text) or text.startswith("/"):
        return

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)
    phase = user["assessment"].get("phase")

    if not phase:
        await m.reply("Выбери действие кнопкой ниже.", reply_markup=lessons_keyboard_for(user))
        return

    if phase == "translate":
        await _handle_translate_answer(m, user, text)
    elif phase == "vocab":
        await _handle_vocab_answer(m, user, text)
    elif phase == "listen":
        await _handle_listen_answer(m, user, text)
    elif phase == "write":
        await _handle_write_answer(m, user, text)
    else:
        await send_lessons_home(m)


@router.message(ModeFilter(MODE_LESSONS))
async def lessons_other(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)
    phase = user["assessment"].get("phase")
    await m.reply(
        "Пришли текстовый ответ или нажми кнопку.",
        reply_markup=assess_simple_kb() if phase else lessons_keyboard_for(user),
    )


async def _handle_translate_answer(m: Message, user: dict, text: str):
    """Любой ответ на перевод → сразу дальше (это тест, без объяснений)."""
    await m.reply("Принято. Дальше…")
    a = user["assessment"]
    result = judge_translation(
        a["translate_source_en"],
        a["translate_reference_ru"],
        text,
    )
    score = int(result.get("score") or 0)
    text_level = a.get("translate_level") or "B2"
    gpt_est = result.get("cefr_estimate") or text_level
    rule_est = estimate_level_from_translation(text_level, score)
    # строже: берём более низкий из двух
    from data.assessment_data import level_index

    if gpt_est not in LEVELS:
        gpt_est = rule_est
    final_est = LEVELS[min(level_index(gpt_est), level_index(rule_est))]

    set_translate_estimate(str(m.from_user.id), final_est)
    await _start_vocab_flow(m, final_est)


async def _start_vocab_flow(m: Message, level: str):
    await m.reply("Готовлю слова…")
    user = begin_vocab(str(m.from_user.id), level)
    a = user["assessment"]
    await m.reply(
        "🎯 Задание 2/4: словарь\n\n"
        "Переведи слово на русский. Всего 4 слова.\n\n"
        f"1/4 🇬🇧 {a['vocab_en']}",
        reply_markup=assess_simple_kb(),
    )


async def _handle_vocab_answer(m: Message, user: dict, text: str):
    a = user["assessment"]
    result = judge_vocab(a["vocab_en"], a.get("vocab_ru") or [], text)
    correct = _as_bool(result.get("correct"))
    level = a.get("vocab_level") or "A2"
    level = adjust_level(level, correct)

    idx = int(a.get("vocab_i", 0))
    if idx >= 3:
        await _start_listen_flow(m, level)
        return

    user = next_vocab(str(m.from_user.id), level)
    a = user["assessment"]
    await m.reply(f"{a['vocab_i'] + 1}/4 🇬🇧 {a['vocab_en']}", reply_markup=assess_simple_kb())


async def _start_listen_flow(m: Message, level: str):
    await m.reply(
        "🎯 Задание 3/4: аудирование\n\n"
        "Слушай голосовое и напиши, что услышал(а), на английском.\n"
        "Всего 3 голосовых."
    )
    user = begin_listen(str(m.from_user.id), level)
    a = user["assessment"]
    await _send_listen_audio(m, a["listen_text"], 1)


async def _send_listen_audio(m: Message, text: str, number: int):
    await m.reply(f"🎧 {number}/3")
    mp3 = elevenlabs_tts(text)
    if not mp3:
        logging.error("Listen TTS failed")
        await m.reply("Аудио не создалось. Напиши любой ответ, чтобы продолжить.")
        return

    ogg = mp3_to_ogg_opus(mp3)
    path = None
    try:
        data = ogg or mp3
        suffix = ".ogg" if ogg else ".mp3"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(data)
            path = f.name
        if ogg:
            await m.reply_voice(FSInputFile(path))
        else:
            await m.reply_audio(FSInputFile(path), title=f"Listen {number}")
    finally:
        if path and os.path.exists(path):
            os.ulink(path)


async def _handle_listen_answer(m: Message, user: dict, text: str):
    a = user["assessment"]
    result = judge_listening(a.get("listen_text") or "", text)
    score = int(result.get("score") or 0)
    correct = _as_bool(result.get("correct")) and score >= 85
    level = a.get("listen_level") or "A2"
    level = adjust_level(level, correct)

    idx = int(a.get("listen_i", 0))
    if idx >= 2:
        await _start_write_flow(m, level)
        return

    user = next_listen(str(m.from_user.id), level)
    a = user["assessment"]
    await _send_listen_audio(m, a["listen_text"], a["listen_i"] + 1)


async def _start_write_flow(m: Message, level: str):
    user = begin_write(str(m.from_user.id), level)
    a = user["assessment"]
    await m.reply(
        "🎯 Задание 4/4: письмо\n\n"
        f"Тема: {a['write_topic']}\n\n"
        "Напиши текст на английском — до 10 предложений.",
        reply_markup=assess_simple_kb(),
    )


async def _handle_write_answer(m: Message, user: dict, text: str):
    await m.reply("Проверяю…")
    a = user["assessment"]
    current = a.get("write_level") or a.get("cefr") or "A2"
    translate_est = a.get("translate_estimate") or current
    result = judge_writing(a.get("write_topic") or "", text, current)
    writing_level = result.get("cefr_estimate") or current
    if writing_level not in LEVELS:
        writing_level = current

    final = average_level([translate_est, current, writing_level])
    finish_assessment(str(m.from_user.id), final)

    await m.reply(
        f"Готово! Тест позади 🙂\n\n"
        f"Ваш предполагаемый и предпочитаемый уровень для изучения — {final}. "
        f"Но вы можете пройти и уроки уровнем ниже — для закрепления знаний."
    )
    await send_lessons_home(
        m,
        intro=(
            f"📚 Уроки\n\n"
            f"Твой уровень: {final}.\n"
            f"Выбери уровень ниже."
        ),
    )
