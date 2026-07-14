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
    assess_dont_know_kb,
    assess_write_kb,
)
from data.assessment_data import LEVELS, level_index, lower_level, lower_level, level_index
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
    replace_write_topic,
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
BTN_DONT_KNOW = "🙈 Не знаю"
BTN_REPLACE = "🔄 Заменить текст"

RICO_BEFORE_TEST = (
    "🦜 <b>Рико:</b>\n"
    "Эй! Перед тестом одна просьба 🫶\n\n"
    "Пройди его <b>добросовестно и честно</b> — без подсказок и переводчиков.\n"
    "Твои знания — в твоих интересах: так мы подберём правильный уровень "
    "и не будем зря терять время.\n\n"
    "Готов? Поехали! 🚀"
)

RICO_AFTER_LEVEL = {
    "A0": (
        "🦜 <b>Рико:</b>\n"
        "Вот и начинается твой путь в английском! 🌱\n"
        "Сейчас всё новое — и это нормально. Мы вместе многого добьёмся: "
        "шаг за шагом, без давления и со смехом.\n"
        "Я буду рядом и подталкивать, когда нужно.\n\n"
        "Ну что, начнём? ✨"
    ),
    "A1": (
        "🦜 <b>Рико:</b>\n"
        "Ты уже кое-что знаешь — это круто! 👏\n"
        "Правда, для свободного общения пока маловато, но мы с тобой натренируемся: "
        "слова, простые фразы и уверенность.\n"
        "Скоро заметишь прогресс.\n\n"
        "Ну что, начнём? 💪"
    ),
    "A2": (
        "🦜 <b>Рико:</b>\n"
        "Неплохо! База уже есть 🔥\n"
        "Ты понимаешь простые вещи, но ещё спотыкаешься — "
        "сейчас как раз время укрепить фундамент и заговорить смелее.\n"
        "Я помогу не растеряться.\n\n"
        "Ну что, начнём? 🚀"
    ),
    "B1": (
        "🦜 <b>Рико:</b>\n"
        "Ого, ты уже уверенно держишься! 😊\n"
        "Можно общаться на бытовые темы, но хочется больше точности и свободы.\n"
        "Потренируем грамматику, словарь и живую речь — и уровень заметно вырастет.\n\n"
        "Ну что, начнём? ✨"
    ),
    "B2": (
        "🦜 <b>Рико:</b>\n"
        "Серьёзный уровень! 😎\n"
        "Ты уже почти свободно понимаешь и говоришь, но иногда не хватает оттенков и уверенности.\n"
        "Подкинем живые темы, разговорную практику и тонкости — станет ещё круче.\n\n"
        "Ну что, начнём? 🔥"
    ),
    "C1": (
        "🦜 <b>Рико:</b>\n"
        "Ого… мне достался мастер на полставки! 👑\n"
        "Но поверь: здесь мне есть чему тебя научить — стиль, нюансы и живая разговорная практика.\n"
        "А позже, как самому талантливому «почти-носителю», ты получишь особенный бонус… "
        "но об этом потом 😉\n\n"
        "И да… надеюсь, ты никуда не подглядывал и не списывал? 👀😂\n\n"
        "Ну что, начнём на высокой ноте? 🚀"
    ),
    "C2": (
        "🦜 <b>Рико:</b>\n"
        "Вау. Настоящий мастер воплоти! 👑✨\n"
        "Но не расслабляйся: даже на вершине есть куда расти — естественность, богатство речи и скорость.\n"
        "Позже самому талантливому носителю языка я готовлю особенный бонус… секрет пока 🤫\n\n"
        "Только скажи честно: надеюсь, ты не списывал и никуда не подглядывал? 👀😂\n\n"
        "Ну что, начнём? 💪"
    ),
}


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
        BTN_DONT_KNOW,
        BTN_REPLACE,
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


def _write_prompt(topic: str, left: int) -> str:
    text = (
        "🎯 Задание 4/4: письмо\n\n"
        f"Тема: {topic}\n\n"
        "Напиши текст на английском — до 10 предложений.\n"
        f"🔄 Осталось замен текста: {left}"
    )
    if left == 1:
        text += (
            "\n\n⚠️ Внимание: осталась последняя замена текста. "
            "В случае её пропуска задание будет закончено и оценено как невыполненное."
        )
    return text


async def _finish_test(m: Message, user_id: str, final: str, note: str = ""):
    finish_assessment(user_id, final)
    rico = RICO_AFTER_LEVEL.get(final, RICO_AFTER_LEVEL["A1"])
    msg = (
        f"🏁 <b>Тест позади!</b> 🙂\n\n"
        f"{note}"
        f"Ваш предполагаемый и предпочитаемый уровень для изучения — <b>{final}</b>.\n"
        f"Но вы можете пройти и уроки уровнем ниже — для закрепления знаний.\n\n"
        f"{rico}"
    )
    await m.reply(msg, parse_mode="HTML")
    await send_lessons_home(
        m,
        intro=f"📚 Уроки\n\nТвой уровень: {final}.\nВыбери уровень ниже.",
    )


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

    await m.reply(RICO_BEFORE_TEST, parse_mode="HTML")
    await m.reply("Секунду, готовлю тебе тест… 🦜")
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


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_DONT_KNOW)
async def dont_know(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)
    a = user["assessment"]
    phase = a.get("phase")

    if phase == "vocab":
        await _advance_vocab(m, user, success=False)
    elif phase == "listen":
        await _advance_listen(m, user, success=False)
    else:
        await m.reply("Сейчас эта кнопка недоступна.", reply_markup=lessons_keyboard_for(user))


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_REPLACE)
async def replace_write(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)
    a = user["assessment"]

    if a.get("phase") != "write":
        await m.reply("Сейчас нечего менять.", reply_markup=lessons_keyboard_for(user))
        return

    user, status = replace_write_topic(str(m.from_user.id))
    a = user["assessment"]

    if status == "ended":
        current = a.get("write_level") or a.get("cefr") or "A2"
        translate_est = a.get("translate_estimate") or current
        final = average_level([translate_est, current, "A0"])
        await _finish_test(
            m,
            str(m.from_user.id),
            final,
            note="Задание 4 не выполнено (израсходованы все замены текста).\n\n",
        )
        return

    if status == "none":
        await m.reply("Замен больше нет.", reply_markup=assess_write_kb())
        return

    left = int(a.get("write_replacements_left", 0))
    await m.reply("Меняю текст…")
    await m.reply(
        _write_prompt(a["write_topic"], left),
        reply_markup=assess_write_kb(),
    )


@router.message(ModeFilter(MODE_LESSONS), F.text.in_(LEVELS))
async def choose_level(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)

    if user["assessment"].get("phase"):
        return

    if not user.get("assessment_done"):
        await m.reply("Сначала пройди проверку уровня.", reply_markup=lessons_home_first())
        return

    selected = m.text
    user_level = user.get("level") or "A1"
    if level_index(selected) > level_index(user_level):
        need = (
            user_level
            if level_index(selected) == level_index(user_level) + 1
            else lower_level(selected)
        )
        await m.reply(
            f"🦜 <b>Рико:</b> Твой уровень по тесту — <b>{user_level}</b>.\n"
            f"Уровень <b>{selected}</b> пока закрыт 🔒\n\n"
            f"Для начала освой уровень <b>{need}</b> — "
            f"шаг за шагом, без спешки! Когда будешь готов — вернёшься сюда 💪",
            reply_markup=lessons_home_levels(),
            parse_mode="HTML",
        )
        return

    from handlers.lessons_grammar import open_level_hub

    await open_level_hub(m, selected)


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
        # Если человек внутри раздела грамматики — пусть отвечает lessons_grammar
        hub = (user.get("lesson") or {}).get("hub")
        if hub:
            return
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

    # Внутри Grammar не сбрасываем клавиатуру на выбор уровня
    if not phase and (user.get("lesson") or {}).get("hub"):
        from handlers.lessons_grammar import _kb_for_user, VOICE_ONLY_TEXT

        if m.voice:
            await m.reply(VOICE_ONLY_TEXT, reply_markup=_kb_for_user(user), parse_mode="HTML")
        else:
            await m.reply(
                "Напиши текст или нажми кнопку ниже.",
                reply_markup=_kb_for_user(user),
            )
        return

    kb = lessons_keyboard_for(user)
    if phase in {"vocab", "listen"}:
        kb = assess_dont_know_kb()
    elif phase == "write":
        kb = assess_write_kb()
    elif phase:
        kb = assess_simple_kb()
    await m.reply("Пришли текстовый ответ или нажми кнопку.", reply_markup=kb)


async def _handle_translate_answer(m: Message, user: dict, text: str):
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
        "Переведи слово на русский. Всего 4 слова.\n"
        "Если не знаешь — жми «Не знаю».\n\n"
        f"1/4 🇬🇧 {a['vocab_en']}",
        reply_markup=assess_dont_know_kb(),
    )


async def _handle_vocab_answer(m: Message, user: dict, text: str):
    a = user["assessment"]
    result = judge_vocab(a["vocab_en"], a.get("vocab_ru") or [], text)
    correct = _as_bool(result.get("correct"))
    await _advance_vocab(m, user, success=correct)


async def _advance_vocab(m: Message, user: dict, success: bool):
    a = user["assessment"]
    level = a.get("vocab_level") or "A2"
    level = adjust_level(level, success)
    idx = int(a.get("vocab_i", 0))

    if idx >= 3:
        await _start_listen_flow(m, level)
        return

    user = next_vocab(str(m.from_user.id), level)
    a = user["assessment"]
    await m.reply(
        f"{a['vocab_i'] + 1}/4 🇬🇧 {a['vocab_en']}",
        reply_markup=assess_dont_know_kb(),
    )


async def _start_listen_flow(m: Message, level: str):
    await m.reply(
        "🎯 Задание 3/4: аудирование\n\n"
        "Слушай голосовое и напиши, что услышал(а), на английском.\n"
        "Всего 3 голосовых. Если не распознал — жми «Не знаю».",
        reply_markup=assess_dont_know_kb(),
    )
    user = begin_listen(str(m.from_user.id), level)
    a = user["assessment"]
    await _send_listen_audio(m, a["listen_text"], 1)


async def _send_listen_audio(m: Message, text: str, number: int):
    await m.reply(f"🎧 {number}/3", reply_markup=assess_dont_know_kb())
    mp3 = elevenlabs_tts(text)
    if not mp3:
        logging.error("Listen TTS failed")
        await m.reply("Аудио не создалось. Напиши ответ или нажми «Не знаю».")
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
    a = user["assessment"]
    result = judge_listening(a.get("listen_text") or "", text)
    score = int(result.get("score") or 0)
    correct = _as_bool(result.get("correct")) and score >= 85
    await _advance_listen(m, user, success=correct)


async def _advance_listen(m: Message, user: dict, success: bool):
    a = user["assessment"]
    level = a.get("listen_level") or "A2"
    level = adjust_level(level, success)
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
    left = int(a.get("write_replacements_left", 3))
    await m.reply(
        _write_prompt(a["write_topic"], left),
        reply_markup=assess_write_kb(),
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
    await _finish_test(m, str(m.from_user.id), final)
