# -*- coding: utf-8 -*-
"""Пилот A0.T1 Lesson 1 v2 — /a0_curs (только MANAGER)."""

from __future__ import annotations

import asyncio
import logging
import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from config import MANAGER_ID
from handlers.filters import ModeFilter
from services.a0_lesson1 import (
    LISTENINGS,
    MINI_CHECK,
    PRACTICE,
    check_item,
    elapsed_min,
    ensure_a0_pilot,
    listen_item,
    practice_item,
    rico_explain_reply,
    shuffle_mcq,
    speaking_ok,
    start_lesson1,
)
from services.database import (
    MODE_A0_COURSE,
    MODE_MENU,
    get_user,
    save_users,
    set_mode,
    users_for,
)

log = logging.getLogger(__name__)
router = Router()

BTN_READY = "✅ Готов, поехали"
BTN_PAUSE = "⏸ Выйти из пилота"
BTN_CLEAR = "✅ Ок, ясно"
BTN_UNCLEAR = "❓ Непонятно — напишу"
BTN_SHOW_TEXT = "📄 Показать текст"
BTN_SKIP_NOTE = "⏭ Без заметки"
BTN_MIC = "🎙 Жду твоё голосовое"
BTN_HEARD = "👂 Услышал — дальше"


def _is_manager(m: Message) -> bool:
    return bool(m.from_user and int(m.from_user.id) == int(MANAGER_ID))


def _kb(rows: list[list[str]]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t) for t in row] for row in rows],
        resize_keyboard=True,
    )


def _mcq_kb(options: list[str], extra: list[str] | None = None) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=f"{i + 1}. {opt}")] for i, opt in enumerate(options)]
    if extra:
        for t in extra:
            rows.append([KeyboardButton(text=t)])
    rows.append([KeyboardButton(text=BTN_PAUSE)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def _parse_choice(text: str, n: int) -> int | None:
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


async def _voice_only(m: Message, text: str, p: dict) -> None:
    """Только голосовое — без текста фразы над ним."""
    p["last_audio"] = text
    try:
        from services.elevenlabs import synthesize_speech, send_voice_from_mp3

        mp3, _ = await asyncio.to_thread(synthesize_speech, text, slow=True)
        if mp3:
            await send_voice_from_mp3(m, mp3, title="A0 L1")
            return
    except Exception as e:
        log.warning("a0 tts fail: %s", e)
    # fallback если TTS умер — тогда текст, иначе урок встанет
    await m.answer(f"(голос недоступен) <code>{text}</code>", parse_mode="HTML")


def _arm_mcq(p: dict, item: dict) -> list[str]:
    disp, corr = shuffle_mcq(list(item["options"]), int(item["correct"]))
    p["mcq_opts"] = disp
    p["mcq_correct"] = corr
    return disp


@router.message(Command("a0_curs"))
@router.message(Command("a0_course"))
async def cmd_a0_curs(m: Message):
    if not _is_manager(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    start_lesson1(user)
    set_mode(uid, MODE_A0_COURSE)
    save_users(users, only=uid)
    await m.answer(
        "🦜 Эй. Это пилот первого урока A0 — я Рико, буду вести как на занятии, "
        "не как меню из кнопок.\n\n"
        "⏱ Ориентир ~час, но сегодня проверяем ощущение. "
        "Выдели спокойное время, без параллельных чатов.\n\n"
        "Как к тебе обращаться? Напиши имя ✍️",
        reply_markup=_kb([[BTN_PAUSE]]),
    )


@router.message(ModeFilter(MODE_A0_COURSE), F.text == BTN_PAUSE)
async def a0_exit(m: Message):
    if not _is_manager(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    p = ensure_a0_pilot(user)
    mins = elapsed_min(p)
    p["finished"] = True
    set_mode(uid, MODE_MENU)
    save_users(users, only=uid)
    await m.answer(f"Ок, стоп. Прошло ~<b>{mins:.1f} мин</b>. /a0_curs когда снова.", parse_mode="HTML")


async def _send_practice(m: Message, p: dict) -> None:
    item = practice_item(p)
    if not item:
        p["step"] = "listening"
        p["listen_i"] = 0
        await m.answer(
            "🎧 Теперь уши. Сначала только голос — текста не будет.\n"
            "Не расслышал? Жми «Показать текст». "
            "Повторить аудио можно тапом по самому голосовому в чате 👆",
            reply_markup=_kb([[BTN_PAUSE]]),
        )
        await _send_listening(m, p)
        return
    i = int(p.get("practice_i") or 0)
    opts = _arm_mcq(p, item)
    await m.answer(
        f"🧩 Давай проверим, {p.get('name') or 'друг'} — {i + 1}/{len(PRACTICE)}\n\n{item['q']}",
        reply_markup=_mcq_kb(opts),
    )


async def _send_listening(m: Message, p: dict) -> None:
    item = listen_item(p)
    if not item:
        p["step"] = "speaking"
        p["speak_round"] = 1
        name = p.get("name") or "Alex"
        await m.answer(
            f"🎙 Твоя очередь, {name}.\n"
            "Сейчас модель без текста — слушай. Потом скажи голосом:\n"
            "<b>Hi, I'm …</b> (своё имя)\n\n"
            "Аудио можно переслушать тапом по сообщению.",
            parse_mode="HTML",
            reply_markup=_kb([[BTN_SHOW_TEXT], [BTN_MIC], [BTN_PAUSE]]),
        )
        await _voice_only(m, f"Hi, I'm {name}.", p)
        return
    i = int(p.get("listen_i") or 0)
    p["step"] = "listening"
    await m.answer(
        f"🎧 Кусок {i + 1}/{len(LISTENINGS)} — слушай 👇",
        reply_markup=_kb([[BTN_SHOW_TEXT], [BTN_PAUSE]]),
    )
    await _voice_only(m, item["audio"], p)
    opts = _arm_mcq(p, item)
    await m.answer(item["q"], reply_markup=_mcq_kb(opts, [BTN_SHOW_TEXT]))


async def _send_check(m: Message, p: dict) -> None:
    item = check_item(p)
    if not item:
        ok = int(p.get("check_ok") or 0)
        tot = max(1, int(p.get("check_tot") or 0))
        pct = int(round(100 * ok / tot))
        p["step"] = "note"
        vibe = "Красава 🔥" if pct >= 70 else "Норм заход, но дырки есть — зафиксируем 💪"
        await m.answer(
            f"{vibe}\nMini-check: <b>{ok}/{tot}</b> ({pct}%)\n\n"
            "📝 Кинь мне в одно сообщение: <b>что сегодня было сложно?</b>\n"
            "Это для тебя и для меня на следующие уроки.\n"
            "Или «Без заметки».",
            parse_mode="HTML",
            reply_markup=_kb([[BTN_SKIP_NOTE], [BTN_PAUSE]]),
        )
        return
    i = int(p.get("check_i") or 0)
    opts = _arm_mcq(p, item)
    await m.answer(
        f"✅ Финальный мини-чек {i + 1}/{len(MINI_CHECK)}\n\n{item['q']}",
        reply_markup=_mcq_kb(opts),
    )


async def _finish(m: Message, user: dict, users: dict, uid: str) -> None:
    p = ensure_a0_pilot(user)
    p["finished"] = True
    p["step"] = "done"
    mins = elapsed_min(p)
    note = (p.get("note") or "").strip()
    set_mode(uid, MODE_MENU)
    save_users(users, only=uid)
    await m.answer(
        f"🏁 Урок 1 пилота закрыт, {p.get('name') or 'чемпион'}.\n\n"
        f"⏱ Сессия: <b>~{mins:.1f} мин</b>\n"
        f"Заметка: <i>{note or '—'}</i>\n\n"
        "Если снова вышло слишком быстро — пиши, будем наращивать «живые» куски "
        "(диалог, паузы, добивки), а не кнопки.\n"
        "Ещё раз: /a0_curs",
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_A0_COURSE), F.voice)
async def a0_voice(m: Message):
    if not _is_manager(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    p = ensure_a0_pilot(user)
    step = p.get("step")
    if step not in ("warmup_speak", "speaking"):
        await m.answer("Сейчас голос не жду — давай по шагу урока 😊")
        return

    text = None
    try:
        from services.stt import recognize_english

        f = await m.bot.get_file(m.voice.file_id)
        raw = await m.bot.download_file(f.file_path)
        raw = raw.read() if hasattr(raw, "read") else raw
        text = await asyncio.wait_for(asyncio.to_thread(recognize_english, raw), timeout=35)
    except Exception as e:
        log.warning("a0 stt: %s", e)

    name = p.get("name") or ""
    need_nice = step == "speaking" and int(p.get("speak_round") or 1) >= 2
    ok, tip = speaking_ok(text, name, need_nice=need_nice)
    safe = (text or "").replace("<", " ").replace(">", " ")[:200]
    if not text:
        await m.answer("Не разобрал 🙈 Переслушай голосовое выше тапом и скажи ещё раз четче.")
        return
    await m.answer(f"{'✅' if ok else '🧐'} Я услышал: <i>{safe}</i>", parse_mode="HTML")
    if not ok:
        await m.answer(tip)
        return

    if step == "warmup_speak":
        p["step"] = "explain_iam"
        p["explain_topic"] = "I am / I'm"
        save_users(users, only=uid)
        await m.answer(
            f"Есть! {name}, уже по-английски 🔥\n\n"
            "Смотри, в чём фокус сегодня.\n"
            "<b>I am</b> = я есть / я являюсь.\n"
            "В живой речи почти всегда коротко: <b>I'm</b>.\n"
            "Смысл один. I'm — не «другой глагол», а удобная форма.\n\n"
            "Сейчас два голосовых подряд (без текста). Потом скажи, ясно ли.",
            parse_mode="HTML",
            reply_markup=_kb([[BTN_CLEAR], [BTN_UNCLEAR], [BTN_PAUSE]]),
        )
        await _voice_only(m, f"I am {name}.", p)
        await _voice_only(m, f"I'm {name}.", p)
        return

    # speaking rounds
    rnd = int(p.get("speak_round") or 1)
    if rnd < 2:
        p["speak_round"] = 2
        save_users(users, only=uid)
        await m.answer(
            "Красиво. Второй заход — чуть длиннее:\n"
            "<b>Hi, I'm … Nice to meet you.</b>\n"
            "Снова модель без текста 👇",
            parse_mode="HTML",
            reply_markup=_kb([[BTN_SHOW_TEXT], [BTN_MIC], [BTN_PAUSE]]),
        )
        await _voice_only(m, f"Hi, I'm {name}. Nice to meet you.", p)
        return

    p["step"] = "check"
    p["check_i"] = 0
    p["check_ok"] = 0
    p["check_tot"] = 0
    save_users(users, only=uid)
    await m.answer(f"Мощно, {name}. Последний рывок — мини-чек, и свободен 💪")
    await _send_check(m, p)
    save_users(users, only=uid)


@router.message(ModeFilter(MODE_A0_COURSE), F.text)
async def a0_text(m: Message):
    if not _is_manager(m):
        return
    text = (m.text or "").strip()
    if not text or text == BTN_PAUSE:
        return

    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    p = ensure_a0_pilot(user)
    step = p.get("step")
    name = p.get("name") or "друг"

    if step == "ask_name":
        nm = re.sub(r"[^\w\s\-']", "", text, flags=re.UNICODE).strip()[:32] or "Friend"
        # латиница для speaking предпочтительнее
        if re.search(r"[а-яё]", nm, re.I):
            await m.answer(
                f"Принял, {nm} 😊 Для говорения лучше латиницей "
                f"(как будешь представляться англичанину). Напиши имя английскими буквами?"
            )
            return
        p["name"] = nm
        p["step"] = "intro"
        save_users(users, only=uid)
        await m.answer(
            f"Рад, {nm} 🦜\n"
            "Сегодня научимся здороваться и говорить кто ты: Hi / I'm …\n"
            "Это база — без неё всё остальное шатается.\n\n"
            "Готов начать?",
            reply_markup=_kb([[BTN_READY], [BTN_PAUSE]]),
        )
        return

    if step == "intro" and text == BTN_READY:
        p["step"] = "warmup_listen"
        save_users(users, only=uid)
        await m.answer(
            "Поехали.\n"
            "По-русски мы говорим: «Привет, я …».\n"
            "По-английски почти то же — сейчас услышишь. "
            "Текста не даю специально: тренируем ухо.\n"
            "Повторить = тап по голосовому. Потом жми «Услышал».",
            reply_markup=_kb([[BTN_HEARD], [BTN_SHOW_TEXT], [BTN_PAUSE]]),
        )
        await _voice_only(m, f"Hi, I'm {p['name']}.", p)
        return

    if step == "warmup_listen":
        if text == BTN_SHOW_TEXT:
            await m.answer(f"📄 <code>{p.get('last_audio') or ''}</code>", parse_mode="HTML")
            return
        if text == BTN_HEARD:
            p["step"] = "warmup_speak"
            save_users(users, only=uid)
            await m.answer(
                f"Твой ход, {name}. Голосом: <b>Hi, I'm {name}.</b>\n"
                "Не идеально — нормально. Главное сказать.",
                parse_mode="HTML",
                reply_markup=_kb([[BTN_SHOW_TEXT], [BTN_MIC], [BTN_PAUSE]]),
            )
            return

    if step in ("warmup_speak", "speaking") and text == BTN_SHOW_TEXT:
        await m.answer(f"📄 <code>{p.get('last_audio') or ''}</code>", parse_mode="HTML")
        return

    if step == "explain_iam":
        if text == BTN_UNCLEAR:
            p["step"] = "explain_q"
            p["explain_topic"] = "I am / I'm"
            save_users(users, only=uid)
            await m.answer(
                "Пиши прямо: что не кликает? "
                "Например «зачем I'm» / «как читать» / «чем отличается от I am».",
                reply_markup=_kb([[BTN_CLEAR], [BTN_PAUSE]]),
            )
            return
        if text == BTN_CLEAR:
            p["step"] = "explain_you"
            p["explain_topic"] = "you are / you're / Are you"
            save_users(users, only=uid)
            await m.answer(
                "Отлично.\n"
                "Теперь про собеседника: <b>you are</b> → в речи <b>you're</b>.\n"
                "Вопрос: <b>Are you …?</b>\n"
                "Слушай два куска 👇",
                parse_mode="HTML",
                reply_markup=_kb([[BTN_CLEAR], [BTN_UNCLEAR], [BTN_PAUSE]]),
            )
            await _voice_only(m, "You're Alex.", p)
            await _voice_only(m, "Are you Alex?", p)
            return
        # свободный текст в объяснении
        p["step"] = "explain_q"
        p["explain_topic"] = "I am / I'm"
        save_users(users, only=uid)
        # fall through handled below if we set step - actually need to handle now
        reply = await asyncio.to_thread(rico_explain_reply, text, "I am / I'm", name)
        await m.answer(reply or "Ок, давай ещё раз проще — жми «Непонятно» и сформулируй вопрос.")
        p["step"] = "explain_iam"
        save_users(users, only=uid)
        return

    if step == "explain_q":
        if text == BTN_CLEAR:
            # вернуться к текущей теме
            topic = p.get("explain_topic") or ""
            if "you" in topic.lower():
                p["step"] = "explain_you"
            else:
                p["step"] = "explain_iam"
            save_users(users, only=uid)
            await m.answer("Супер. Тогда идём дальше — жми «Ок, ясно» когда готов.", reply_markup=_kb([[BTN_CLEAR], [BTN_UNCLEAR], [BTN_PAUSE]]))
            return
        reply = await asyncio.to_thread(
            rico_explain_reply, text, p.get("explain_topic") or "I am / I'm", name
        )
        await m.answer((reply or "Понял вопрос. Если ок — жми «Ок, ясно».") + "\n\nЕщё вопрос — пиши. Или «Ок, ясно».")
        save_users(users, only=uid)
        return

    if step == "explain_you":
        if text == BTN_UNCLEAR:
            p["step"] = "explain_q"
            p["explain_topic"] = "you are / you're / Are you"
            save_users(users, only=uid)
            await m.answer("Пиши, что именно с You're / Are you непонятно ✍️", reply_markup=_kb([[BTN_CLEAR], [BTN_PAUSE]]))
            return
        if text == BTN_CLEAR:
            p["step"] = "practice"
            p["practice_i"] = 0
            save_users(users, only=uid)
            await m.answer(f"Погнали потренируем кнопками — но правильный ответ каждый раз в разном месте, не читерь 😄")
            await _send_practice(m, p)
            save_users(users, only=uid)
            return
        reply = await asyncio.to_thread(rico_explain_reply, text, "you are / you're / Are you", name)
        await m.answer(reply or "Ок. Жми ясно или напиши ещё вопрос.")
        return

    if step == "practice":
        item = practice_item(p)
        if not item:
            return
        opts = p.get("mcq_opts") or item["options"]
        idx = _parse_choice(text, len(opts))
        if idx is None:
            await m.answer("Жми номер варианта 😉")
            return
        corr = int(p.get("mcq_correct") if p.get("mcq_correct") is not None else item["correct"])
        if idx == corr:
            await m.answer(random_ok())
        else:
            await m.answer(f"Не-а. Верно: <b>{opts[corr]}</b> — запомни ощущение.", parse_mode="HTML")
        p["practice_i"] = int(p.get("practice_i") or 0) + 1
        save_users(users, only=uid)
        await _send_practice(m, p)
        save_users(users, only=uid)
        return

    if step == "listening":
        item = listen_item(p)
        if not item:
            return
        if text == BTN_SHOW_TEXT:
            await m.answer(f"📄 <code>{p.get('last_audio') or item['audio']}</code>", parse_mode="HTML")
            return
        opts = p.get("mcq_opts") or item["options"]
        idx = _parse_choice(text, len(opts))
        if idx is None:
            await m.answer("Вариант кнопкой, или «Показать текст».")
            return
        corr = int(p.get("mcq_correct") if p.get("mcq_correct") is not None else item["correct"])
        if idx == corr:
            await m.answer(random_ok())
        else:
            await m.answer(f"Близко, но верно: <b>{opts[corr]}</b>", parse_mode="HTML")
        p["listen_i"] = int(p.get("listen_i") or 0) + 1
        save_users(users, only=uid)
        await _send_listening(m, p)
        save_users(users, only=uid)
        return

    if step == "check":
        item = check_item(p)
        if not item:
            return
        opts = p.get("mcq_opts") or item["options"]
        idx = _parse_choice(text, len(opts))
        if idx is None:
            await m.answer("Кнопку, пожалуйста 🙂")
            return
        corr = int(p.get("mcq_correct") if p.get("mcq_correct") is not None else item["correct"])
        p["check_tot"] = int(p.get("check_tot") or 0) + 1
        if idx == corr:
            p["check_ok"] = int(p.get("check_ok") or 0) + 1
            await m.answer(random_ok())
        else:
            await m.answer(f"Верно было: <b>{opts[corr]}</b>", parse_mode="HTML")
        p["check_i"] = int(p.get("check_i") or 0) + 1
        save_users(users, only=uid)
        await _send_check(m, p)
        save_users(users, only=uid)
        return

    if step == "note":
        p["note"] = "" if text == BTN_SKIP_NOTE else text[:500]
        save_users(users, only=uid)
        await _finish(m, user, users, uid)
        return

    await m.answer("Я тут, но сейчас жду шаг урока / кнопку. Или /a0_curs заново.")


def random_ok() -> str:
    import random

    return random.choice(["✅ Есть!", "🔥 Да!", "💪 Точно", "👏 Красиво", "✅ В точку"])
