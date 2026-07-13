"""
Раздел «Уроки» + входной тест уровня.
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
from services.database import (
    load_users,
    get_user,
    MODE_LESSONS,
)
from services.assessment import (
    ensure_user_fields,
    start_assessment,
    set_translation_item,
    begin_vocab,
    next_vocab,
    begin_listen,
    next_listen,
    begin_write,
    finish_assessment,
    adjust_level,
    average_level,
)
from services.gpt import (
    judge_translation,
    judge_vocab,
    judge_listening,
    judge_writing,
)
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
                f"Твой уровень сейчас: {user.get('level', 'A1')}.\n"
                f"Выбери уровень ниже или пройди тест снова."
            )
        else:
            intro = (
                "📚 Уроки\n\n"
                "Сначала нужно проверить твой уровень английского.\n"
                "Тест займёт около 10 минут: перевод, слова, аудирование и короткое письмо.\n\n"
                "Нажми «Проверить уровень»."
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


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_CHECK)
@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_AGAIN)
async def start_level_test(m: Message):
    user = start_assessment(str(m.from_user.id))
    a = user["assessment"]
    await m.reply(
        "🎯 Тест уровня — задание 1/4: перевод\n\n"
        "Переведи текст на русский письменно.\n"
        "Стартовый уровень текста: B2.\n"
        "Если сложно — жми «Дай текст проще».\n\n"
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
        # уже A0 → второй текст A0, потом skip
        if not a.get("a0_second_shown"):
            user = set_translation_item(str(m.from_user.id), "A0", 1)
            a = user["assessment"]
            await m.reply(
                "Это самый простой уровень (A0). Вот другой текст:\n\n"
                f"🇬🇧 Текст:\n{a['translate_source_en']}\n\n"
                "Если совсем не получается — нажми «Пропустить задание».",
                reply_markup=assess_translate_kb(show_skip=True),
            )
        else:
            await m.reply(
                "Больше упрощать некуда. Попробуй перевести или нажми «Пропустить задание».",
                reply_markup=assess_translate_kb(show_skip=True),
            )
        return

    new_level = lower_level(cur)
    user = set_translation_item(str(m.from_user.id), new_level, 0)
    a = user["assessment"]
    show_skip = new_level == "A0" and a.get("a0_second_shown")
    await m.reply(
        f"Ок, упрощаю до {new_level}.\n\n"
        f"🇬🇧 Текст:\n{a['translate_source_en']}",
        reply_markup=assess_translate_kb(show_skip=show_skip),
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
            "Пропуск доступен только после второго текста A0.",
            reply_markup=assess_translate_kb(show_skip=a.get("a0_second_shown", False)),
        )
        return

    # нулевой уровень
    await m.reply("Понял: база пока очень слабая. Идём дальше со словами уровня A0.")
    await _start_vocab_flow(m, "A0")


@router.message(ModeFilter(MODE_LESSONS), F.text.in_(LEVELS))
async def choose_level(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)

    if not user.get("assessment_done"):
        await m.reply(
            "Сначала пройди проверку уровня.",
            reply_markup=lessons_home_first(),
        )
        return

    level = m.text
    await m.reply(
        f"📚 Уровень {level}\n\n"
        "Уроки по этому уровню скоро появятся.\n"
        "Пока можно выбрать другой уровень или пройти тест снова.",
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
    a = user["assessment"]
    phase = a.get("phase")

    if not phase:
        await m.reply(
            "Выбери действие кнопкой ниже.",
            reply_markup=lessons_keyboard_for(user),
        )
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
    await m.reply(
        "В уроках пришли текстовый ответ или нажми кнопку.",
        reply_markup=lessons_keyboard_for(user) if not user["assessment"].get("phase") else assess_simple_kb(),
    )


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "да"}
    return False


async def _handle_translate_answer(m: Message, user: dict, text: str):
    await m.reply("Проверяю перевод…")
    a = user["assessment"]
    result = judge_translation(
        a["translate_source_en"],
        a["translate_reference_ru"],
        text,
    )
    score = int(result.get("score") or 0)
    passed = _as_bool(result.get("passed")) and score >= 78
    estimate = result.get("cefr_estimate") or a.get("translate_level") or "A2"
    if estimate not in LEVELS:
        estimate = a.get("translate_level") or "A2"

    feedback = result.get("feedback_ru") or ""

    if passed:
        level = estimate
        await m.reply(
            f"✅ Отличный перевод!\n"
            f"Схожесть: {score}/100\n"
            f"{feedback}\n\n"
            f"Черновой уровень после задания 1: {level}"
        )
        await _start_vocab_flow(m, level)
        return

    await m.reply(
        f"❌ Пока недостаточно близко к смыслу оригинала.\n"
        f"Схожесть: {score}/100\n"
        f"{feedback}\n\n"
        "Можешь перевести ещё раз текущий текст или нажать «Дай текст проще»."
    )


async def _start_vocab_flow(m: Message, level: str):
    user = begin_vocab(str(m.from_user.id), level)
    a = user["assessment"]
    await m.reply(
        "🎯 Задание 2/4: словарь\n\n"
        "Переведи слово на русский.\n"
        "Всего 4 слова: верно → слово сложнее, неверно → проще.\n\n"
        f"1/4 🇬🇧 {a['vocab_en']}",
        reply_markup=assess_simple_kb(),
    )


async def _handle_vocab_answer(m: Message, user: dict, text: str):
    await m.reply("Проверяю…")
    a = user["assessment"]
    result = judge_vocab(a["vocab_en"], a.get("vocab_ru") or [], text)
    correct = _as_bool(result.get("correct"))
    feedback = result.get("feedback_ru") or ""
    level = a.get("vocab_level") or "A2"

    if correct:
        level = adjust_level(level, True)
        await m.reply(f"✅ Верно!\n{feedback}")
    else:
        level = adjust_level(level, False)
        expected = ", ".join(a.get("vocab_ru") or [])
        await m.reply(f"❌ Неверно.\nПравильные варианты: {expected}\n{feedback}")

    idx = int(a.get("vocab_i", 0))
    if idx >= 3:
        # 4 words done (0..3)
        await m.reply(f"Словарь завершён. Текущая оценка: {level}")
        await _start_listen_flow(m, level)
        return

    user = next_vocab(str(m.from_user.id), level)
    a = user["assessment"]
    await m.reply(
        f"{a['vocab_i'] + 1}/4 🇬🇧 {a['vocab_en']}",
        reply_markup=assess_simple_kb(),
    )


async def _start_listen_flow(m: Message, level: str):
    user = begin_listen(str(m.from_user.id), level)
    a = user["assessment"]
    await m.reply(
        "🎯 Задание 3/4: аудирование\n\n"
        "Сейчас пришлю голосовое (до ~10 секунд).\n"
        "Напиши текстом, что услышал(а) на английском.\n"
        "Всего 3 голосовых.",
        reply_markup=assess_simple_kb(),
    )
    await _send_listen_audio(m, a["listen_text"], a["listen_i"] + 1)


async def _send_listen_audio(m: Message, text: str, number: int):
    await m.reply(f"🎧 Голосовое {number}/3…")
    mp3 = elevenlabs_tts(text)
    if not mp3:
        # fallback: show text if TTS fails? No - for listening hide text.
        await m.reply("Не удалось создать аудио. Попробуй ответить на фразу позже или /start.")
        logging.error("Listen TTS failed")
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
            os.unlink(path)


async def _handle_listen_answer(m: Message, user: dict, text: str):
    await m.reply("Проверяю…")
    a = user["assessment"]
    result = judge_listening(a.get("listen_text") or "", text)
    score = int(result.get("score") or 0)
    correct = _as_bool(result.get("correct")) or score >= 75
    feedback = result.get("feedback_ru") or ""
    level = a.get("listen_level") or "A2"

    if correct:
        level = adjust_level(level, True)
        await m.reply(f"✅ Хорошо!\n{feedback}")
    else:
        level = adjust_level(level, False)
        await m.reply(
            f"❌ Не совсем.\nБыло: {a.get('listen_text')}\n{feedback}"
        )

    idx = int(a.get("listen_i", 0))
    if idx >= 2:
        await m.reply(f"Аудирование завершено. Текущая оценка: {level}")
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
        "Напиши текст на английском — до 10 предложений.\n"
        "Когда закончишь, просто отправь сообщение.",
        reply_markup=assess_simple_kb(),
    )


async def _handle_write_answer(m: Message, user: dict, text: str):
    await m.reply("Читаю твой текст…")
    a = user["assessment"]
    current = a.get("write_level") or a.get("cefr") or "A2"
    result = judge_writing(a.get("write_topic") or "", text, current)
    writing_level = result.get("cefr_estimate") or current
    if writing_level not in LEVELS:
        writing_level = current

    # итог: среднее от оценки перевода/слов/слушания (текущий cefr после listen) и письма
    final = average_level([current, writing_level])
    feedback = result.get("feedback_ru") or ""

    finish_assessment(str(m.from_user.id), final)

    await m.reply(
        f"🏁 Тест завершён!\n\n"
        f"{feedback}\n\n"
        f"Рекомендуемый уровень: {final}\n"
        f"Теперь можешь выбрать этот уровень в разделе уроков."
    )
    await send_lessons_home(
        m,
        intro=(
            f"📚 Уроки\n\n"
            f"Твой уровень: {final}.\n"
            f"Выбери уровень ниже."
        ),
    )
