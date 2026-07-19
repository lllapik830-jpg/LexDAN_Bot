"""
Раздел «Уроки» + входной тест уровня.
"""

import logging

from aiogram import Router, F
from aiogram.types import Message

from handlers.filters import ModeFilter
from handlers.keyboards import (
    lessons_home_first,
    lessons_home_levels,
    assess_translate_kb,
    assess_simple_kb,
    assess_dont_know_kb,
    assess_write_kb,
)
from data.assessment_data import LEVELS, level_index, lower_level, max_accessible_level, is_level_accessible
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
from services.elevenlabs import send_voice_reply

router = Router()

BTN_CHECK = "🎯 Проверить уровень"
BTN_AGAIN = "🎯 Пройти тест снова"
BTN_EASIER = "⬇️ Дай текст проще"
BTN_SKIP = "⏭️ Пропустить задание"
BTN_DONT_KNOW = "🙈 Не знаю"
BTN_REPLACE = "🔄 Заменить текст"

RICO_BEFORE_TEST = (
    "🦜 <b>Рико:</b> Эй! Перед стартом одна просьба 🫶\n\n"
    "Сделай его честно, без переводчиков и подсказок. "
    "Так мы сможем подобрать идеальный темп лично для тебя.\n\n"
    "Не переживай, если что-то покажется сложным — это просто отправная точка, а не экзамен.\n\n"
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
        "Но поверь: здесь мне есть чему тебя научить — стиль, нюансы и живая разговорная практика.\n\n"
        "И да… надеюсь, ты никуда не подглядывал и не списывал? 👀😂\n\n"
        "Ну что, начнём на высокой ноте? 🚀"
    ),
    "C2": (
        "🦜 <b>Рико:</b>\n"
        "Вау. Настоящий мастер воплоти! 👑✨\n"
        "Но не расслабляйся: даже на вершине есть куда расти — естественность, богатство речи и скорость.\n\n"
        "Только скажи честно: надеюсь, ты не списывал и никуда не подглядывал? 👀😂\n\n"
        "Ну что, начнём? 💪"
    ),
}


def lessons_keyboard_for(user: dict, *, show_start_today: bool = False):
    ensure_user_fields(user)
    if user.get("assessment_done") or user.get("dev_unlock"):
        from services.vocabulary_state import ensure_vocab_progress
        ensure_vocab_progress(user)
        has_learned = bool(user.get("vocabulary_progress", {}).get("words") or user.get("vocabulary_progress", {}).get("phrases"))
        return lessons_home_levels(
            user.get("level"),
            show_global_tasks=has_learned or user.get("dev_unlock"),
            user=user,
            show_start_today=show_start_today,
        )
    return lessons_home_first()


async def send_lessons_home(
    m: Message,
    intro: str | None = None,
    *,
    show_start_today: bool = False,
):
    user_id = str(m.from_user.id)
    users = load_users()
    user = get_user(users, user_id)
    ensure_user_fields(user)

    from services.growth import ensure_growth
    from services.database import save_users

    ensure_growth(user)
    save_users(users)

    if intro is None:
        if user.get("assessment_done") or user.get("dev_unlock"):
            unlock = " 🔓 DEV" if user.get("dev_unlock") else ""
            ceiling = max_accessible_level(user.get("level") or "A1")
            intro = (
                f"📚 Уроки{unlock}\n\n"
                f"Твой уровень: <b>{user.get('level', 'A1')}</b>.\n"
                f"Открыты уровни до <b>{ceiling}</b> (свой + один выше + всё ниже).\n"
                f"Остальные видны, но закрыты 🔒 — жми любой."
            )
        else:
            intro = (
                "📚 <b>Уроки</b>\n\n"
                "Давай сначала проверим твой уровень — это займёт минут 10.\n\n"
                "Тебя ждёт перевод, слова, аудирование и короткое письмо.\n\n"
                "🔑 <b>Важный момент:</b> правильные ответы мы не будем показывать — "
                "этот тест нужен не для оценки, а чтобы я понял, с чего тебе комфортнее начать занятия.\n\n"
                "Когда будешь готов — жми «Проверить уровень»."
            )

    from services.tg_out import say

    await say(
        m,
        intro,
        reply_markup=lessons_keyboard_for(user, show_start_today=show_start_today),
        parse_mode="HTML",
    )



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
    from services.growth import ensure_growth, touch_activity, grant_safe
    from services.database import load_users, get_user, save_users
    from handlers.keyboards import BTN_START_TODAY

    finish_assessment(user_id, final)
    users = load_users()
    user = get_user(users, user_id)
    ensure_growth(user)
    # Стартовый сейф один раз после теста (без 7-дневного безлимита)
    if not user.get("post_test_safe_granted"):
        grant_safe(user, 1)
        user["post_test_safe_granted"] = True
    touch_activity(user)
    save_users(users)

    rico = RICO_AFTER_LEVEL.get(final, RICO_AFTER_LEVEL["A1"])
    msg = (
        f"🏁 <b>Тест позади!</b> 🙂\n\n"
        f"{note}"
        f"Ваш предполагаемый уровень — <b>{final}</b>.\n"
        f"Можно брать и уровень ниже — для закрепления.\n\n"
        f"{rico}\n\n"
        "Рецепт: <b>~15 минут в день</b>. Серия дней и друзья дают бустеры — смотри в профиле 🔥\n"
        "🛡️ В подарок: <b>+1 стрик-сейф</b> на случай пропуска дня.\n\n"
        f"👇 Лучший старт прямо сейчас — жми <b>{BTN_START_TODAY}</b>\n"
        "(открою Vocabulary и первую тему твоего уровня)."
    )
    await m.answer(msg, parse_mode="HTML")
    await send_lessons_home(
        m,
        intro=f"📚 Уроки\n\nТвой уровень: {final}.\nЖми «Начать сегодня» или выбери уровень 👇",
        show_start_today=True,
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_CHECK)
@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_AGAIN)
async def start_level_test(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)

    if user.get("assessment_done"):
        await m.answer(
            "Тест уровня уже пройден — повторно его пройти нельзя.\n"
            "Выбери уровень для занятий ниже.",
            reply_markup=lessons_home_levels(user.get("level"), user=user),
        )
        return

    await m.answer(RICO_BEFORE_TEST, parse_mode="HTML")
    from services.tg_out import status

    async with status(m, "Секунду, готовлю тебе тест… 🦜"):
        user = start_assessment(str(m.from_user.id))
    a = user["assessment"]
    await m.answer(
        "🎯 Тест уровня — задание 1/4: перевод\n\n"
        "Переведи текст на русский.\n"
        "Если сложно — нажми «Дай текст проще» или «Пропустить задание».\n\n"
        f"🇬🇧 Текст:\n{a['translate_source_en']}",
        reply_markup=assess_translate_kb(show_skip=True),
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_EASIER)
async def easier_text(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)
    a = user["assessment"]

    if a.get("phase") != "translate":
        await m.answer("Сейчас это недоступно.", reply_markup=lessons_keyboard_for(user))
        return

    cur = a.get("translate_level", "B2")
    if cur == "A0":
        if not a.get("a0_second_shown"):
            from services.tg_out import status

            async with status(m, "Готовлю другой текст…"):
                user = set_translation_item(str(m.from_user.id), "A0", 1)
            a = user["assessment"]
            await m.answer(
                f"🇬🇧 Текст:\n{a['translate_source_en']}",
                reply_markup=assess_translate_kb(show_skip=True),
            )
        else:
            await m.answer(
                "Больше упрощать некуда. Переведи или нажми «Пропустить задание».",
                reply_markup=assess_translate_kb(show_skip=True),
            )
        return

    from services.tg_out import status

    async with status(m, "Готовлю текст проще…"):
        new_level = lower_level(cur)
        user = set_translation_item(str(m.from_user.id), new_level, 0)
    a = user["assessment"]
    await m.answer(
        f"🇬🇧 Текст:\n{a['translate_source_en']}",
        reply_markup=assess_translate_kb(show_skip=True),
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_SKIP)
async def skip_translate(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)
    a = user["assessment"]

    if a.get("phase") != "translate":
        await m.answer("Сейчас нечего пропускать.", reply_markup=lessons_keyboard_for(user))
        return

    # Пропуск без оценки — берём текущий уровень текста как оценку
    est = a.get("translate_level") or "A1"
    set_translate_estimate(str(m.from_user.id), est)
    await m.answer("⏭️ Ок, пропускаем перевод без оценки.")
    await _start_vocab_flow(m, est)


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_DONT_KNOW)
async def dont_know(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)
    a = user["assessment"]
    phase = a.get("phase")

    if phase == "vocab":
        # Просто скип без показа правильного ответа
        await _advance_vocab(m, user, success=False)
    elif phase == "listen":
        await _advance_listen(m, user, success=False)
    else:
        await m.answer("Сейчас эта кнопка недоступна.", reply_markup=lessons_keyboard_for(user))


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_REPLACE)
async def replace_write(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)
    a = user["assessment"]

    if a.get("phase") != "write":
        await m.answer("Сейчас нечего менять.", reply_markup=lessons_keyboard_for(user))
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
        await m.answer("Замен больше нет.", reply_markup=assess_write_kb())
        return

    left = int(a.get("write_replacements_left", 0))
    from services.tg_out import try_delete

    status_msg = await m.answer("Меняю текст…")
    await try_delete(m.bot, m.chat.id, status_msg.message_id)
    await m.answer(
        _write_prompt(a["write_topic"], left),
        reply_markup=assess_write_kb(),
    )


@router.message(ModeFilter(MODE_LESSONS), F.text.regexp(r"^(A0|A1|A2|B1|B2|C1|C2)(?:\s*🔒)?$"))
async def choose_level(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_user_fields(user)

    if user["assessment"].get("phase"):
        return

    if not user.get("assessment_done") and not user.get("dev_unlock"):
        await m.answer("Сначала пройди проверку уровня.", reply_markup=lessons_home_first())
        return

    import re as _re

    m_lv = _re.match(r"^(A0|A1|A2|B1|B2|C1|C2)", m.text or "")
    selected = m_lv.group(1) if m_lv else (m.text or "").replace("🔒", "").strip()
    user_level = user.get("level") or "A1"
    if not user.get("dev_unlock") and not is_level_accessible(user_level, selected):
        ceiling = max_accessible_level(user_level)
        await m.answer(
            f"🦜 <b>Рико:</b> Твой уровень по тесту — <b>{user_level}</b>.\n"
            f"Тебе открыты уровни до <b>{ceiling}</b> включительно "
            f"(свой уровень + один выше + всё ниже).\n"
            f"Уровень <b>{selected}</b> пока закрыт 🔒\n\n"
            f"Освой доступные — и откроется следующий! 💪",
            reply_markup=lessons_home_levels(user_level, user=user),
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
        await m.answer("Выбери действие кнопкой ниже.", reply_markup=lessons_keyboard_for(user))
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
            await m.answer(VOICE_ONLY_TEXT, reply_markup=_kb_for_user(user), parse_mode="HTML")
        else:
            await m.answer(
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
    await m.answer("Пришли текстовый ответ или нажми кнопку.", reply_markup=kb)


async def _handle_translate_answer(m: Message, user: dict, text: str):
    await m.answer("Принято. Дальше…")
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
    from services.tg_out import status

    async with status(m, "Готовлю слова…"):
        user = begin_vocab(str(m.from_user.id), level)
    a = user["assessment"]
    await m.answer(
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
    if correct:
        await m.answer("✅ Верно!")
    else:
        # В тесте уровня ответы не показываем
        await m.answer("❌ Не совсем — идём дальше.")
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
    await m.answer(
        f"{a['vocab_i'] + 1}/4 🇬🇧 {a['vocab_en']}",
        reply_markup=assess_dont_know_kb(),
    )


async def _start_listen_flow(m: Message, level: str):
    await m.answer(
        "🎯 Задание 3/4: аудирование\n\n"
        "Слушай голосовое и напиши, что услышал(а), на английском.\n"
        "Всего 3 голосовых. Если не распознал — жми «Не знаю».",
        reply_markup=assess_dont_know_kb(),
    )
    user = begin_listen(str(m.from_user.id), level)
    a = user["assessment"]
    await _send_listen_audio(m, a["listen_text"], 1)


async def _send_listen_audio(m: Message, text: str, number: int):
    await m.answer(f"🎧 {number}/3", reply_markup=assess_dont_know_kb())
    await send_voice_reply(m, text, title=f"Listen {number}")


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
    await m.answer(
        _write_prompt(a["write_topic"], left),
        reply_markup=assess_write_kb(),
    )


async def _handle_write_answer(m: Message, user: dict, text: str):
    from services.tg_out import status

    async with status(m, "Проверяю…"):
        a = user["assessment"]
        current = a.get("write_level") or a.get("cefr") or "A2"
        translate_est = a.get("translate_estimate") or current
        result = judge_writing(a.get("write_topic") or "", text, current)
        writing_level = result.get("cefr_estimate") or current
        if writing_level not in LEVELS:
            writing_level = current
        final = average_level([translate_est, current, writing_level])
    await _finish_test(m, str(m.from_user.id), final)
