"""
Раздел «Курсы»: intro + вступительный placement-тест.
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
from data.course_placement_bank import LISTENING, WRITING
from services.course_placement import (
    BTN_COURSE_ABOUT,
    BTN_COURSE_BUY,
    BTN_COURSE_CONTINUE,
    BTN_COURSE_RESULTS,
    BTN_COURSE_START_TEST,
    BTN_COURSES,
    courses_allowed,
    BTN_SKIP_SPEAKING,
    INTRO_HTML,
    answer_listening,
    answer_lk,
    answer_reading,
    after_lk1_choose_round2,
    begin_listening,
    begin_reading,
    begin_speaking,
    begin_writing,
    current_listening_q,
    current_lk_item,
    current_reading_q,
    current_speaking,
    ensure_course,
    finalize_placement,
    listening_done,
    lk_round_done,
    placement,
    progress_label,
    reading_done,
    results_html,
    score_speaking_utterance,
    score_writing,
    skip_speaking_item,
    speaking_done,
    start_placement,
)
from services.growth import ensure_growth

log = logging.getLogger(__name__)
router = Router()

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
    elif p.get("phase") and p.get("phase") not in (None, "done", "intro"):
        rows.append([KeyboardButton(text=BTN_COURSE_CONTINUE)])
        rows.append([KeyboardButton(text=BTN_COURSE_START_TEST)])
    else:
        rows.append([KeyboardButton(text=BTN_COURSE_START_TEST)])
    rows.append([KeyboardButton(text=BTN_COURSE_ABOUT)])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _mcq_kb(options: list[str], *, extra: list[str] | None = None) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=f"{i + 1}. {opt}")] for i, opt in enumerate(options)]
    if extra:
        rows.append([KeyboardButton(text=x) for x in extra])
    rows.append([KeyboardButton(text="⏸ Пауза · в меню курсов")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _parse_mcq(text: str, n: int) -> int | None:
    t = (text or "").strip()
    if not t:
        return None
    # "1." / "1" / "1. answer"
    if t[0].isdigit():
        try:
            idx = int(t.split(".", 1)[0].strip()) - 1
            if 0 <= idx < n:
                return idx
        except ValueError:
            pass
    return None


def _pause_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏸ Пауза · в меню курсов")],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


async def _send_lk(m: Message, p: dict) -> None:
    item = current_lk_item(p)
    if not item:
        return
    i = int(p.get("lk_i") or 0) + 1
    total = len(p.get("lk_ids") or [])
    await m.answer(
        f"📝 <b>Language Knowledge</b> · {progress_label(p)}\n"
        f"Вопрос {i}/{total}\n\n"
        f"{item['prompt']}",
        parse_mode="HTML",
        reply_markup=_mcq_kb(item["options"]),
    )


async def _send_reading(m: Message, p: dict) -> None:
    cur = current_reading_q(p)
    if not cur:
        return
    block, q = cur
    i = int(p.get("reading_i") or 0)
    if i == 0:
        await m.answer(
            f"📖 <b>Reading</b> · уровень текста {p.get('reading_level')}\n\n"
            f"{block['text']}",
            parse_mode="HTML",
        )
    await m.answer(
        f"Вопрос {i + 1}/{len(block['questions'])}\n\n{q['prompt']}",
        reply_markup=_mcq_kb(q["options"]),
    )


async def _send_listening_audio(m: Message, p: dict) -> None:
    script = (p.get("listening_script") or "").strip()
    if not script:
        return
    await m.answer(
        f"🎧 <b>Listening</b> · уровень {p.get('listening_level')}\n"
        "Сейчас пришлю аудио. Слушай внимательно, затем ответь на вопросы.",
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


async def _send_listening_q(m: Message, p: dict) -> None:
    q = current_listening_q(p)
    if not q:
        return
    block = LISTENING.get(p.get("listening_level") or "A2") or LISTENING["A2"]
    block_n = len(block.get("questions") or [])
    i = int(p.get("listening_i") or 0)
    await m.answer(
        f"Вопрос {i + 1}/{block_n}\n\n{q['prompt']}",
        reply_markup=_mcq_kb(q["options"]),
    )


async def _send_writing(m: Message, p: dict) -> None:
    meta = WRITING.get(p.get("writing_level") or "A2") or WRITING["A2"]
    await m.answer(
        f"✍️ <b>Writing</b> · {p.get('writing_level')}\n\n"
        f"{meta['prompt']}\n\n"
        "Напиши ответ <b>одним сообщением</b> на английском.",
        parse_mode="HTML",
        reply_markup=_pause_kb(),
    )


async def _send_speaking(m: Message, p: dict) -> None:
    item = current_speaking(p)
    if not item:
        return
    i = int(p.get("speaking_i") or 0) + 1
    await m.answer(
        f"🗣 <b>Speaking</b> · задание {i}\n\n"
        f"{item['prompt']}\n\n"
        "Отправь <b>голосовое</b> на английском.",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=BTN_SKIP_SPEAKING)],
                [KeyboardButton(text="⏸ Пауза · в меню курсов")],
                [KeyboardButton(text="🔙 Вернуться в меню")],
            ],
            resize_keyboard=True,
        ),
    )


async def _advance_after_lk(m: Message, user: dict, p: dict) -> None:
    if not lk_round_done(p):
        await _send_lk(m, p)
        return
    if p.get("phase") == "lk1":
        after_lk1_choose_round2(p)
        await m.answer(
            "Ок, уточняем уровень — второй раунд посложнее или полегче 👇"
        )
        await _send_lk(m, p)
        return
    # lk2 done → reading
    begin_reading(p)
    await m.answer("Дальше — <b>чтение</b>.", parse_mode="HTML")
    await _send_reading(m, p)


async def _finish_and_show(m: Message, user: dict, users: dict, uid: str) -> None:
    p = placement(user)
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
    if not p.get("finished"):
        await m.answer("Сначала пройди тест.", reply_markup=_courses_home_kb(user))
        return
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
    start_placement(user)
    save_users(users, only=uid)
    p = placement(user)
    await m.answer(
        "▶️ <b>Вступительный тест</b> (~25–35 мин)\n"
        "Часть 1/5 — Language Knowledge (грамматика и лексика).\n"
        "Выбирай номер ответа. Можно поставить паузу.",
        parse_mode="HTML",
    )
    await _send_lk(m, p)


@router.message(ModeFilter(MODE_COURSES), F.text == BTN_COURSE_CONTINUE)
async def course_test_continue(m: Message):
    if await _deny_if_closed(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_course(user)
    p = placement(user)
    phase = p.get("phase")
    if not phase or phase in (None, "intro", "done") or p.get("finished"):
        await m.answer(
            "Нет теста в процессе — нажми «Пройти вступительный тест».",
            reply_markup=_courses_home_kb(user),
        )
        return
    await m.answer(f"Продолжаем: <b>{progress_label(p)}</b>", parse_mode="HTML")
    if phase in ("lk1", "lk2"):
        await _send_lk(m, p)
    elif phase == "reading":
        await _send_reading(m, p)
    elif phase == "listening":
        if int(p.get("listening_i") or 0) == 0:
            await _send_listening_audio(m, p)
        await _send_listening_q(m, p)
    elif phase == "writing":
        await _send_writing(m, p)
    elif phase == "speaking":
        await _send_speaking(m, p)
    else:
        await m.answer("Начни тест заново.", reply_markup=_courses_home_kb(user))


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
    if speaking_done(p):
        await _finish_and_show(m, user, users, uid)
        return
    await _send_speaking(m, p)


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
    try:
        file = await m.bot.get_file(m.voice.file_id)
        data = await m.bot.download_file(file.file_path)
        raw = data.read() if hasattr(data, "read") else data
        text = await asyncio.to_thread(recognize_english, raw)
    except Exception as e:
        log.warning("course STT fail: %s", e)
        text = None
    ok = score_speaking_utterance(p, text)
    save_users(users, only=uid)
    if text:
        await m.answer(
            f"{'✅' if ok else '⚠️'} Распознал: <i>{text}</i>",
            parse_mode="HTML",
        )
    else:
        await m.answer(
            "Не удалось распознать речь — засчитал как слабый ответ. "
            "Можно следующее задание или пропуск."
        )
    if speaking_done(p):
        await _finish_and_show(m, user, users, uid)
        return
    await _send_speaking(m, p)


@router.message(ModeFilter(MODE_COURSES), F.text)
async def course_text(m: Message):
    if await _deny_if_closed(m):
        return
    text = (m.text or "").strip()
    if not text or text in {
        BTN_COURSES,
        BTN_COURSE_START_TEST,
        BTN_COURSE_CONTINUE,
        BTN_COURSE_RESULTS,
        BTN_COURSE_BUY,
        BTN_COURSE_ABOUT,
        BTN_SKIP_SPEAKING,
        "⏸ Пауза · в меню курсов",
        "🔙 Вернуться в меню",
    }:
        return

    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    p = placement(user)
    phase = p.get("phase")

    if phase in ("lk1", "lk2"):
        item = current_lk_item(p)
        if not item:
            return
        idx = _parse_mcq(text, len(item["options"]))
        if idx is None:
            await m.answer("Выбери вариант кнопкой (1, 2, 3…).")
            return
        answer_lk(p, idx)
        save_users(users, only=uid)
        await _advance_after_lk(m, user, p)
        save_users(users, only=uid)
        return

    if phase == "reading":
        cur = current_reading_q(p)
        if not cur:
            return
        _b, q = cur
        idx = _parse_mcq(text, len(q["options"]))
        if idx is None:
            await m.answer("Выбери вариант кнопкой.")
            return
        answer_reading(p, idx)
        if reading_done(p):
            begin_listening(p)
            save_users(users, only=uid)
            await m.answer("Дальше — <b>аудирование</b>.", parse_mode="HTML")
            await _send_listening_audio(m, p)
            await _send_listening_q(m, p)
        else:
            save_users(users, only=uid)
            await _send_reading(m, p)
        return

    if phase == "listening":
        q = current_listening_q(p)
        if not q:
            return
        idx = _parse_mcq(text, len(q["options"]))
        if idx is None:
            await m.answer("Выбери вариант кнопкой.")
            return
        answer_listening(p, idx)
        if listening_done(p):
            begin_writing(p)
            save_users(users, only=uid)
            await m.answer("Дальше — <b>письмо</b>.", parse_mode="HTML")
            await _send_writing(m, p)
        else:
            save_users(users, only=uid)
            await _send_listening_q(m, p)
        return

    if phase == "writing":
        score_writing(p, text)
        begin_speaking(p)
        save_users(users, only=uid)
        await m.answer(
            "Принял текст. Финал — <b>говорение</b> (голосовые).",
            parse_mode="HTML",
        )
        await _send_speaking(m, p)
        return

    if phase == "speaking":
        await m.answer("Нужно именно <b>голосовое</b> сообщение.", parse_mode="HTML")
        return
