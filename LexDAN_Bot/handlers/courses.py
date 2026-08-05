"""
Раздел «Курсы»: intro + вступительный placement-тест (v2).
"""

from __future__ import annotations

import asyncio
import logging

from aiogram import F, Router
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from handlers.filters import ModeFilter
from services.database import (
    MODE_COURSES,
    get_user,
    save_users,
    set_mode,
    users_for,
)
from data.course_placement_bank import WRITING_PROMPTS
from services.course_placement import (
    BTN_COURSE_ABOUT,
    BTN_COURSE_BUY,
    BTN_COURSE_CONTINUE,
    BTN_COURSE_FINISH_NOW,
    BTN_COURSE_RESULTS,
    BTN_COURSE_START_TEST,
    BTN_COURSES,
    BTN_SKIP_SPEAKING,
    INTRO_HTML,
    PROCESSING_STEPS,
    SPEAKING_TARGET,
    answer_grammar_mcq,
    answer_grammar_text,
    answer_listening,
    answer_reading,
    answer_vocab,
    begin_listening,
    begin_reading,
    begin_speaking,
    begin_vocab,
    begin_writing,
    can_finalize_early,
    courses_allowed,
    current_grammar,
    current_listening,
    current_reading,
    current_speaking,
    current_vocab,
    ensure_course,
    finalize_placement,
    grammar_done,
    grammar_progress,
    listening_done,
    listening_progress,
    placement,
    progress_label,
    reading_done,
    reading_progress,
    repair_placement_queues,
    reopen_mcq_sections_after_zero_bug,
    results_html,
    score_speaking_utterance,
    score_writing,
    skip_speaking_item,
    speaking_done,
    start_placement,
    vocab_done,
    vocab_progress,
)
from services.growth import ensure_growth

log = logging.getLogger(__name__)
router = Router()

_GRAMMAR_MCQ = {"mcq", "gap_choice"}
_GRAMMAR_TEXT = {"word_form", "rewrite", "order"}

_NAV_TEXTS = {
    BTN_COURSES,
    BTN_COURSE_START_TEST,
    BTN_COURSE_CONTINUE,
    BTN_COURSE_FINISH_NOW,
    BTN_COURSE_RESULTS,
    BTN_COURSE_BUY,
    BTN_COURSE_ABOUT,
    BTN_SKIP_SPEAKING,
    "⏸ Пауза · в меню курсов",
    "🔙 Вернуться в меню",
}


def _unfinished_placement(p: dict) -> bool:
    """Есть незавершённый тест (включая phase=analyzing)."""
    if p.get("finished"):
        return False
    phase = p.get("phase")
    return bool(phase) and phase not in (None, "done", "intro")


async def _deny_if_closed(m: Message) -> bool:
    """True = доступ закрыт, уже ответили/молчали."""
    if courses_allowed(m.from_user.id if m.from_user else None):
        return False
    from handlers.keyboards import main_menu
    from services.database import MODE_MENU, set_mode, users_for, get_user, save_users

    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    set_mode(uid, MODE_MENU)
    await m.answer(
        "🎓 Раздел «Курсы» пока в закрытом тесте — скоро откроем.",
        reply_markup=main_menu(user, user_id=uid),
    )
    return True


def _courses_home_kb(user: dict) -> ReplyKeyboardMarkup:
    p = placement(user)
    rows = []
    if p.get("finished"):
        rows.append([KeyboardButton(text=BTN_COURSE_RESULTS)])
        if int(p.get("price") or 0) > 0:
            rows.append([KeyboardButton(text=BTN_COURSE_BUY)])
        rows.append([KeyboardButton(text=BTN_COURSE_START_TEST)])
    elif _unfinished_placement(p):
        # включая analyzing — Continue всегда виден
        rows.append([KeyboardButton(text=BTN_COURSE_CONTINUE)])
        if can_finalize_early(p):
            rows.append([KeyboardButton(text=BTN_COURSE_FINISH_NOW)])
        rows.append([KeyboardButton(text=BTN_COURSE_START_TEST)])
    else:
        rows.append([KeyboardButton(text=BTN_COURSE_START_TEST)])
    rows.append([KeyboardButton(text=BTN_COURSE_ABOUT)])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _mcq_kb(options: list[str]) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=f"{i + 1}. {opt}")] for i, opt in enumerate(options)]
    rows.append([KeyboardButton(text="⏸ Пауза · в меню курсов")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _parse_mcq(text: str, n: int) -> int | None:
    t = (text or "").strip()
    if not t:
        return None
    if t[0].isdigit():
        try:
            idx = int(t.split(".", 1)[0].strip()) - 1
            if 0 <= idx < n:
                return idx
        except ValueError:
            pass
    return None


def _resolve_choice(text: str, options: list[str]) -> int | None:
    """Match by number or by exact option text (strip leading 'N. ')."""
    n = len(options)
    idx = _parse_mcq(text, n)
    if idx is not None:
        return idx
    t = (text or "").strip()
    stripped = t
    if t and t[0].isdigit() and "." in t[:5]:
        stripped = t.split(".", 1)[1].strip()
    for i, opt in enumerate(options):
        if t == opt or stripped == opt:
            return i
    return None


def _pause_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏸ Пауза · в меню курсов")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def _write_kb() -> ReplyKeyboardMarkup:
    return _pause_kb()


def _speaking_kb(p: dict | None = None) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=BTN_SKIP_SPEAKING)]]
    if p is not None and can_finalize_early(p):
        rows.append([KeyboardButton(text=BTN_COURSE_FINISH_NOW)])
    rows.append([KeyboardButton(text="⏸ Пауза · в меню курсов")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _vocab_options(item: dict) -> list[str]:
    if (item.get("direction") or "en_ru") == "ru_en":
        return list(item.get("options_en") or [])
    return list(item.get("options_ru") or [])


def _vocab_prompt(item: dict) -> str:
    if (item.get("direction") or "en_ru") == "ru_en":
        return str(item.get("prompt_ru") or "")
    return str(item.get("prompt_en") or "")


async def _send_grammar(m: Message, p: dict) -> None:
    item = current_grammar(p)
    if not item:
        return
    cur, total = grammar_progress(p)
    subtype = item.get("subtype") or "mcq"
    head = (
        f"📝 <b>Грамматика</b> · {progress_label(p)}\n"
        f"Вопрос {cur}/{total}\n\n"
        f"{item.get('prompt') or ''}"
    )
    if subtype in _GRAMMAR_MCQ:
        opts = list(item.get("options") or [])
        await m.answer(head, parse_mode="HTML", reply_markup=_mcq_kb(opts))
        return
    if subtype == "order":
        words = list(item.get("words") or [])
        head += f"\n\n<code>{' / '.join(words)}</code>"
    await m.answer(
        head + "\n\nНапиши ответ <b>одним сообщением</b>.",
        parse_mode="HTML",
        reply_markup=_write_kb(),
    )


async def _send_vocab(m: Message, p: dict) -> None:
    item = current_vocab(p)
    if not item:
        return
    cur, total = vocab_progress(p)
    opts = _vocab_options(item)
    direction = item.get("direction") or "en_ru"
    label = "EN → RU" if direction == "en_ru" else "RU → EN"
    await m.answer(
        f"📚 <b>Словарь</b> · {label}\n"
        f"Вопрос {cur}/{total}\n\n"
        f"<b>{_vocab_prompt(item)}</b>",
        parse_mode="HTML",
        reply_markup=_mcq_kb(opts),
    )


async def _send_reading(m: Message, p: dict, *, users: dict | None = None, uid: str | None = None) -> None:
    cur = current_reading(p)
    if not cur:
        return
    pid = cur.get("passage_id")
    if p.get("reading_last_passage") != pid:
        title = cur.get("passage_title") or ""
        text = cur.get("passage_text") or ""
        await m.answer(
            f"📖 <b>Reading</b> · {cur.get('passage_level') or ''}\n"
            f"<b>{title}</b>\n\n{text}",
            parse_mode="HTML",
        )
        p["reading_last_passage"] = pid
        if users is not None and uid is not None:
            save_users(users, only=uid)
    q = cur.get("q") or {}
    ri, total = reading_progress(p)
    opts = list(q.get("options") or [])
    await m.answer(
        f"Вопрос {ri}/{total}\n\n{q.get('prompt') or ''}",
        reply_markup=_mcq_kb(opts),
    )


async def _send_listening_audio(m: Message, item: dict) -> None:
    script = (item.get("script") or "").strip()
    if not script:
        return
    await m.answer(
        f"🎧 <b>Listening</b> · уровень {item.get('level') or ''}\n"
        "Сейчас пришлю аудио. Слушай внимательно, затем ответь на вопрос.",
        parse_mode="HTML",
    )
    try:
        from services.elevenlabs import synthesize_speech, send_voice_from_mp3

        mp3, _ = await asyncio.to_thread(synthesize_speech, script)
        if mp3:
            await send_voice_from_mp3(m, mp3, title="Listening")
            return
    except Exception as e:
        log.warning("course listening TTS fail: %s", e)
    await m.answer(f"<i>Аудио временно недоступно. Текст:</i>\n{script}", parse_mode="HTML")


async def _send_listening(
    m: Message,
    p: dict,
    *,
    force_audio: bool = False,
    users: dict | None = None,
    uid: str | None = None,
) -> None:
    item = current_listening(p)
    if not item:
        return
    lid = item.get("id")
    already = p.get("listening_audio_sent")
    # re-send audio only if this item wasn't sent yet, or force / just started
    if force_audio or already != lid:
        await _send_listening_audio(m, item)
        p["listening_audio_sent"] = lid
        if users is not None and uid is not None:
            save_users(users, only=uid)
    q = item.get("question") or {}
    li, total = listening_progress(p)
    opts = list(q.get("options") or [])
    await m.answer(
        f"Вопрос {li}/{total}\n\n{q.get('prompt') or ''}",
        reply_markup=_mcq_kb(opts),
    )


async def _send_writing(m: Message, p: dict) -> None:
    lvl = p.get("writing_level") or "A2"
    meta = WRITING_PROMPTS.get(lvl) or WRITING_PROMPTS.get("A2") or {}
    await m.answer(
        f"✍️ <b>Writing</b> · {lvl}\n\n"
        f"{meta.get('prompt') or ''}\n\n"
        "Напиши <b>8 предложений</b> одним сообщением на английском.",
        parse_mode="HTML",
        reply_markup=_write_kb(),
    )


async def _send_speaking(m: Message, p: dict) -> bool:
    """Отправить вопрос speaking. False = нечего слать → caller должен завершить."""
    if speaking_done(p):
        return False
    item = current_speaking(p)
    if not item:
        return False
    n = int(p.get("speaking_answers") or 0) + 1
    prompt = (item.get("prompt") or "").replace("<", "&lt;").replace(">", "&gt;")
    await m.answer(
        f"🗣 <b>Speaking</b> · ответ {n}/{SPEAKING_TARGET}\n\n"
        f"{prompt}\n\n"
        "Отправь <b>голосовое</b> на английском.",
        parse_mode="HTML",
        reply_markup=_speaking_kb(p),
    )
    return True


async def _resume_phase(m: Message, user: dict, users: dict, uid: str) -> None:
    p = placement(user)
    repair_placement_queues(p)
    phase = p.get("phase")
    if phase == "analyzing" or (phase == "speaking" and speaking_done(p)):
        await _finish_and_show(m, user, users, uid)
        return
    if phase == "grammar":
        await _send_grammar(m, p)
    elif phase == "vocab":
        await _send_vocab(m, p)
    elif phase == "reading":
        await _send_reading(m, p, users=users, uid=uid)
    elif phase == "listening":
        # mid-listening continue: don't re-send audio if already sent for this item
        await _send_listening(m, p, force_audio=False, users=users, uid=uid)
    elif phase == "writing":
        await _send_writing(m, p)
    elif phase == "speaking":
        if not await _send_speaking(m, p):
            await _finish_and_show(m, user, users, uid)
    else:
        await m.answer("Начни тест заново.", reply_markup=_courses_home_kb(user))


async def _finish_and_show(m: Message, user: dict, users: dict, uid: str) -> None:
    p = placement(user)
    if p.get("finished"):
        if reopen_mcq_sections_after_zero_bug(p):
            save_users(users, only=uid)
            await m.answer(
                "⚠️ Ошибка проверки MCQ: вариант №1 всегда считался неверным. "
                "Лексику/чтение/аудирование нужно пройти заново "
                "(грамматика, письмо и говорение сохранены).",
                reply_markup=_courses_home_kb(user),
            )
            await m.answer("Дальше — <b>словарь</b> (50 слов).", parse_mode="HTML")
            await _send_vocab(m, p)
            return
        # пересчёт отображения (месяцы / «не пройдено») без потери ответов
        finalize_placement(p)
        save_users(users, only=uid)
        await m.answer(results_html(p), parse_mode="HTML", reply_markup=_courses_home_kb(user))
        return

    p["phase"] = "analyzing"
    save_users(users, only=uid)

    status: Message | None = None
    try:
        for step in PROCESSING_STEPS:
            if status is None:
                status = await m.answer(step)
            else:
                try:
                    await status.edit_text(step)
                except Exception:
                    status = await m.answer(step)
            await asyncio.sleep(1.2)
    finally:
        # всегда finalize при незавершённом — skill scores не трогаем
        p = placement(user)
        if not p.get("finished"):
            finalize_placement(p)
            save_users(users, only=uid)

    await m.answer(results_html(p), parse_mode="HTML", reply_markup=_courses_home_kb(user))


@router.message(F.text == BTN_COURSES)
async def open_courses(m: Message):
    if await _deny_if_closed(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    ensure_course(user)
    set_mode(uid, MODE_COURSES)
    save_users(users, only=uid)
    await m.answer(INTRO_HTML, parse_mode="HTML", reply_markup=_courses_home_kb(user))
    p = placement(user)
    if p.get("phase") == "analyzing" and not p.get("finished"):
        await m.answer(
            "Анализ ещё не завершён — нажми «Продолжить тест», чтобы получить результат.",
            reply_markup=_courses_home_kb(user),
        )


@router.message(ModeFilter(MODE_COURSES), F.text == BTN_COURSE_ABOUT)
async def course_about(m: Message):
    if await _deny_if_closed(m):
        return
    await m.answer(
        "ℹ️ <b>Как устроен курс</b>\n\n"
        "1) Вступительный тест → уровень и слабые места\n"
        "2) Персональный план до <b>B2</b>\n"
        "3) Темы по 4-дневному циклу: изучение → закрепление → "
        "практика → экзамен (≥80%)\n"
        "4) Дальше только после сдачи темы\n\n"
        "Сейчас открыта подготовка: тест и оффер. "
        "Сами уроки курса подключим следующим этапом.",
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_COURSES), F.text == "⏸ Пауза · в меню курсов")
async def course_pause(m: Message):
    if await _deny_if_closed(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_course(user)
    await m.answer(
        "Пауза. Прогресс теста сохранён — жми «Продолжить тест».",
        reply_markup=_courses_home_kb(user),
    )


@router.message(ModeFilter(MODE_COURSES), F.text == BTN_COURSE_RESULTS)
async def course_results(m: Message):
    if await _deny_if_closed(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    p = placement(user)
    if reopen_mcq_sections_after_zero_bug(p):
        save_users(users, only=uid)
        await m.answer(
            "⚠️ Нашлась ошибка в проверке тестов с вариантами: правильный ответ №1 "
            "всегда считался неверным. Из‑за этого лексика/чтение/аудирование "
            "получили 0%, хотя ты мог отвечать правильно.\n\n"
            "Грамматику, письмо и говорение сохранили. "
            "Сейчас нужно заново пройти <b>словарь → чтение → аудирование</b> "
            "(потом результат пересчитается).",
            parse_mode="HTML",
            reply_markup=_courses_home_kb(user),
        )
        await m.answer("Дальше — <b>словарь</b> (50 слов).", parse_mode="HTML")
        await _send_vocab(m, p)
        return
    if not p.get("finished"):
        await m.answer("Сначала пройди тест.", reply_markup=_courses_home_kb(user))
        return
    # пересчёт из skill_scores — старые 0% / одинаковые месяцы правятся
    finalize_placement(p)
    save_users(users, only=uid)
    await m.answer(results_html(p), parse_mode="HTML", reply_markup=_courses_home_kb(user))


@router.message(ModeFilter(MODE_COURSES), F.text == BTN_COURSE_BUY)
async def course_buy(m: Message):
    if await _deny_if_closed(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    p = placement(user)
    price = int(p.get("price") or 0)
    if not p.get("finished") or price <= 0:
        await m.answer(
            "Для твоего результата покупка курса сейчас не нужна "
            "или тест ещё не завершён.",
            reply_markup=_courses_home_kb(user),
        )
        return
    from config import SUPPORT_USERNAME

    contact = f"@{SUPPORT_USERNAME}" if SUPPORT_USERNAME else "поддержку"
    await m.answer(
        f"💳 Курс до B2 с уровня <b>{p.get('entry_level')}</b> — "
        f"<b>{price}₽</b>.\n\n"
        "Автооплату курса подключим сразу после теста (в работе).\n"
        f"Пока напиши {contact} код <code>COURSE-{uid}</code> — "
        "активируем вручную.",
        parse_mode="HTML",
        reply_markup=_courses_home_kb(user),
    )


@router.message(ModeFilter(MODE_COURSES), F.text == BTN_COURSE_START_TEST)
async def course_test_start(m: Message):
    if await _deny_if_closed(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_course(user)
    p = placement(user)
    if _unfinished_placement(p):
        tip = (
            "⚠️ У тебя уже есть незавершённый тест — прогресс сохранён.\n\n"
            "Нажми «Продолжить тест», чтобы идти дальше."
        )
        if can_finalize_early(p) or p.get("phase") in ("speaking", "analyzing"):
            tip += (
                "\nИли «Завершить и показать результат» — "
                "посчитаем уровень по текущим ответам (без сброса)."
            )
        await m.answer(tip, reply_markup=_courses_home_kb(user))
        return
    start_placement(user)
    save_users(users, only=uid)
    p = placement(user)
    await m.answer(
        "▶️ <b>Вступительный тест</b> (~30–40 мин)\n\n"
        "Части:\n"
        "· грамматика (40)\n"
        "· словарь (50)\n"
        "· чтение\n"
        "· аудирование\n"
        "· письмо (8 предложений)\n"
        "· говорение (до 20 ответов)\n\n"
        "Часть 1 — грамматика. Можно поставить паузу.",
        parse_mode="HTML",
    )
    await _send_grammar(m, p)


@router.message(ModeFilter(MODE_COURSES), F.text == BTN_COURSE_CONTINUE)
async def course_test_continue(m: Message):
    if await _deny_if_closed(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_course(user)
    p = placement(user)
    if p.get("finished") or not _unfinished_placement(p):
        await m.answer(
            "Нет теста в процессе — нажми «Пройти вступительный тест».",
            reply_markup=_courses_home_kb(user),
        )
        return
    repair_placement_queues(p)
    save_users(users, only=uid)
    if p.get("phase") == "analyzing":
        await m.answer("Досчитываю результат…")
        await _finish_and_show(m, user, users, uid)
        return
    await m.answer(f"Продолжаем: <b>{progress_label(p)}</b>", parse_mode="HTML")
    await _resume_phase(m, user, users, uid)


@router.message(ModeFilter(MODE_COURSES), F.text == BTN_COURSE_FINISH_NOW)
async def course_finish_now(m: Message):
    if await _deny_if_closed(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_course(user)
    p = placement(user)
    phase = p.get("phase")
    if not (can_finalize_early(p) or phase in ("speaking", "analyzing")):
        await m.answer(
            "Досрочное завершение доступно на этапе говорения "
            "(после нескольких ответов) или во время анализа.",
            reply_markup=_courses_home_kb(user),
        )
        return
    if p.get("finished"):
        await m.answer(results_html(p), parse_mode="HTML", reply_markup=_courses_home_kb(user))
        return
    await m.answer("Считаю результат по текущим ответам (прогресс не сбрасываю)…")
    await _finish_and_show(m, user, users, uid)


@router.message(ModeFilter(MODE_COURSES), F.text == BTN_SKIP_SPEAKING)
async def skip_speak(m: Message):
    if await _deny_if_closed(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    p = placement(user)
    if p.get("phase") != "speaking":
        return
    skip_speaking_item(p)
    save_users(users, only=uid)
    if speaking_done(p) or not await _send_speaking(m, p):
        await _finish_and_show(m, user, users, uid)


@router.message(ModeFilter(MODE_COURSES), F.voice)
async def course_voice(m: Message):
    if await _deny_if_closed(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    p = placement(user)
    if p.get("phase") != "speaking":
        await m.answer("Сейчас голосовое не нужно — смотри задание на экране.")
        return
    from services.stt import recognize_english

    await m.answer("Слушаю…")
    text = None
    try:
        file = await m.bot.get_file(m.voice.file_id)
        data = await m.bot.download_file(file.file_path)
        raw = data.read() if hasattr(data, "read") else data
        text = await asyncio.wait_for(
            asyncio.to_thread(recognize_english, raw),
            timeout=35,
        )
    except asyncio.TimeoutError:
        log.warning("course STT timeout uid=%s", uid)
        text = None
    except Exception as e:
        log.warning("course STT fail: %s", e)
        text = None
    ok = score_speaking_utterance(p, text)
    save_users(users, only=uid)
    if text:
        safe = str(text).replace("<", "&lt;").replace(">", "&gt;")
        await m.answer(
            f"{'✅' if ok else '⚠️'} Распознал: <i>{safe}</i>",
            parse_mode="HTML",
        )
    else:
        await m.answer(
            "Не удалось распознать речь — засчитал как слабый ответ. "
            "Можно следующее задание или пропуск."
        )
    if speaking_done(p) or not await _send_speaking(m, p):
        await _finish_and_show(m, user, users, uid)


@router.message(ModeFilter(MODE_COURSES), F.text)
async def course_text(m: Message):
    if await _deny_if_closed(m):
        return
    text = (m.text or "").strip()
    if not text or text in _NAV_TEXTS:
        return

    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    p = placement(user)
    phase = p.get("phase")

    if phase == "grammar":
        item = current_grammar(p)
        if not item:
            return
        subtype = item.get("subtype") or "mcq"
        if subtype in _GRAMMAR_MCQ:
            opts = list(item.get("options") or [])
            idx = _resolve_choice(text, opts)
            if idx is None:
                await m.answer("Выбери вариант кнопкой (1, 2, 3…).")
                return
            answer_grammar_mcq(p, idx)
        elif subtype in _GRAMMAR_TEXT:
            answer_grammar_text(p, text)
        else:
            await m.answer("Непонятный тип задания — напиши в поддержку.")
            return
        save_users(users, only=uid)
        if grammar_done(p):
            begin_vocab(p)
            save_users(users, only=uid)
            await m.answer("Дальше — <b>словарь</b> (50 слов).", parse_mode="HTML")
            await _send_vocab(m, p)
        else:
            await _send_grammar(m, p)
        return

    if phase == "vocab":
        item = current_vocab(p)
        if not item:
            return
        opts = _vocab_options(item)
        idx = _resolve_choice(text, opts)
        if idx is None:
            await m.answer("Выбери вариант кнопкой.")
            return
        answer_vocab(p, idx)
        save_users(users, only=uid)
        if vocab_done(p):
            begin_reading(p)
            save_users(users, only=uid)
            await m.answer("Дальше — <b>чтение</b>.", parse_mode="HTML")
            await _send_reading(m, p, users=users, uid=uid)
        else:
            await _send_vocab(m, p)
        return

    if phase == "reading":
        cur = current_reading(p)
        if not cur:
            return
        q = cur.get("q") or {}
        opts = list(q.get("options") or [])
        idx = _resolve_choice(text, opts)
        if idx is None:
            await m.answer("Выбери вариант кнопкой.")
            return
        answer_reading(p, idx)
        save_users(users, only=uid)
        if reading_done(p):
            begin_listening(p)
            p["listening_audio_sent"] = None
            save_users(users, only=uid)
            await m.answer("Дальше — <b>аудирование</b>.", parse_mode="HTML")
            await _send_listening(m, p, force_audio=True, users=users, uid=uid)
        else:
            await _send_reading(m, p, users=users, uid=uid)
        return

    if phase == "listening":
        item = current_listening(p)
        if not item:
            return
        q = item.get("question") or {}
        opts = list(q.get("options") or [])
        idx = _resolve_choice(text, opts)
        if idx is None:
            await m.answer("Выбери вариант кнопкой.")
            return
        answer_listening(p, idx)
        save_users(users, only=uid)
        if listening_done(p):
            begin_writing(p)
            save_users(users, only=uid)
            await m.answer("Дальше — <b>письмо</b>.", parse_mode="HTML")
            await _send_writing(m, p)
        else:
            # next item — send new audio
            await _send_listening(m, p, force_audio=True, users=users, uid=uid)
        return

    if phase == "writing":
        score_writing(p, text)
        begin_speaking(p)
        save_users(users, only=uid)
        await m.answer(
            "Принял текст. Финал — <b>говорение</b> (голосовые).",
            parse_mode="HTML",
        )
        if speaking_done(p) or not await _send_speaking(m, p):
            await _finish_and_show(m, user, users, uid)
        return

    if phase == "speaking":
        await m.answer("Нужно именно <b>голосовое</b> сообщение.", parse_mode="HTML")
        return
