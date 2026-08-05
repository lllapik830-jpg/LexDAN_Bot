# -*- coding: utf-8 -*-
"""Пилот A0.T1 Lesson 1 — только MANAGER. Команда: /a0_curs"""

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

BTN_READY = "✅ Готов"
BTN_PAUSE = "⏸ Выйти из пилота"
BTN_CLEAR = "✅ Ясно"
BTN_UNCLEAR = "❓ Непонятно"
BTN_LISTEN_AGAIN = "🔊 Прослушать ещё раз"
BTN_SHOW_TEXT = "📄 Показать текст"
BTN_NEXT = "➡️ Дальше"
BTN_SKIP_NOTE = "⏭ Без заметки"
BTN_MIC_HINT = "🎙 Отправь голосовое"


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


async def _say_en(m: Message, text: str) -> None:
    await m.answer(f"🔊 <b>{text}</b>", parse_mode="HTML")
    try:
        from services.elevenlabs import synthesize_speech, send_voice_from_mp3

        mp3, _ = await asyncio.to_thread(synthesize_speech, text, slow=True)
        if mp3:
            await send_voice_from_mp3(m, mp3, title="A0 L1")
    except Exception as e:
        log.warning("a0 tts fail: %s", e)


@router.message(Command("a0_curs"))
@router.message(Command("a0_course"))
async def cmd_a0_curs(m: Message):
    if not _is_manager(m):
        return
    uid = str(m.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    p = start_lesson1(user)
    set_mode(uid, MODE_A0_COURSE)
    save_users(users, only=uid)
    await m.answer(
        "🧪 <b>Пилот A0.T1 · Урок 1</b>\n"
        "Только для тайминга и качества. Не финальный продукт.\n\n"
        "Выдели спокойное время. Цель: представиться — "
        "<i>Hi, I'm … / Nice to meet you</i>.\n\n"
        "Как к тебе обращаться на уроках? Напиши имя одним сообщением.",
        parse_mode="HTML",
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
    await m.answer(
        f"Пилот прерван. Прошло ~<b>{mins:.1f} мин</b>.",
        parse_mode="HTML",
    )


async def _send_practice(m: Message, p: dict) -> None:
    item = practice_item(p)
    if not item:
        p["step"] = "listening"
        p["listen_i"] = 0
        p["listen_show"] = False
        await _send_listening(m, p)
        return
    i = int(p.get("practice_i") or 0)
    await m.answer(
        f"🧩 Практика {i + 1}/{len(PRACTICE)}\n\n{item['q']}",
        reply_markup=_mcq_kb(item["options"]),
    )


async def _send_listening(m: Message, p: dict) -> None:
    item = listen_item(p)
    if not item:
        p["step"] = "speaking"
        await m.answer(
            "🎙 <b>Speaking</b>\n"
            "Сначала модель — слушай сколько нужно, потом своё голосовое.\n\n"
            f"Скажи примерно:\n<code>Hi, I'm {p.get('name') or 'Alex'}. Nice to meet you.</code>",
            parse_mode="HTML",
            reply_markup=_kb([[BTN_LISTEN_AGAIN], [BTN_MIC_HINT], [BTN_PAUSE]]),
        )
        await _say_en(m, f"Hi, I'm {p.get('name') or 'Alex'}. Nice to meet you.")
        return
    i = int(p.get("listen_i") or 0)
    p["listen_show"] = False
    p["step"] = "listening"
    await m.answer(
        f"🎧 Listening {i + 1}/{len(LISTENINGS)}\nСначала ухом. Если тяжело — «Показать текст».",
        reply_markup=_kb([[BTN_SHOW_TEXT], [BTN_LISTEN_AGAIN], [BTN_PAUSE]]),
    )
    await _say_en(m, item["audio"])
    await m.answer(item["q"], reply_markup=_mcq_kb(item["options"], [BTN_SHOW_TEXT, BTN_LISTEN_AGAIN]))


async def _send_check(m: Message, p: dict) -> None:
    item = check_item(p)
    if not item:
        # score
        ok = int(p.get("check_ok") or 0)
        tot = max(1, int(p.get("check_tot") or 0))
        pct = int(round(100 * ok / tot))
        p["step"] = "note"
        await m.answer(
            f"Mini-check: <b>{ok}/{tot}</b> ({pct}%)\n"
            f"{'✅ хватает (≥70%)' if pct >= 70 else '⚠️ ниже 70% — в финале темы будет добивка'}\n\n"
            "📝 <b>Заметка для себя</b> (что было сложно) — одним сообщением\n"
            "или жми «Без заметки».",
            parse_mode="HTML",
            reply_markup=_kb([[BTN_SKIP_NOTE], [BTN_PAUSE]]),
        )
        return
    i = int(p.get("check_i") or 0)
    await m.answer(
        f"✅ Mini-check {i + 1}/{len(MINI_CHECK)}\n\n{item['q']}",
        reply_markup=_mcq_kb(item["options"]),
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
        "🏁 <b>Урок 1 пилота завершён</b>\n\n"
        f"⏱ Чистое время сессии: <b>~{mins:.1f} мин</b>\n"
        f"(цель каркаса ~55–60′; если сильно меньше — блоки ещё жидкие)\n\n"
        f"Имя в системе: <b>{p.get('name') or '—'}</b>\n"
        f"Заметка: <i>{note or '—'}</i>\n\n"
        "Напиши, что по таймингу/скуке/ясности — правим скрипт.\n"
        "Снова: /a0_curs",
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
        await m.answer("Сейчас голосовое не жду — иди по кнопкам урока.")
        return

    raw = None
    text = None
    try:
        from services.stt import recognize_english

        f = await m.bot.get_file(m.voice.file_id)
        raw = await m.bot.download_file(f.file_path)
        raw = raw.read() if hasattr(raw, "read") else raw
        text = await asyncio.wait_for(
            asyncio.to_thread(recognize_english, raw),
            timeout=35,
        )
    except Exception as e:
        log.warning("a0 stt: %s", e)

    name = p.get("name") or ""
    ok = speaking_ok(text, name)
    safe = (text or "").replace("<", " ").replace(">", " ")[:200]
    if text:
        await m.answer(
            f"{'✅' if ok else '⚠️'} Распознал: <i>{safe}</i>",
            parse_mode="HTML",
        )
    else:
        await m.answer("Не разобрал речь. Нажми «Прослушать ещё раз» и попробуй снова.")
        return

    if step == "warmup_speak":
        if not ok:
            await m.answer("Ещё раз медленнее. Нужно что-то вроде: Hi, I'm …")
            await _say_en(m, f"Hi, I'm {name}.")
            return
        p["step"] = "explain_iam"
        save_users(users, only=uid)
        await m.answer(
            "🔥 Есть контакт.\n\n"
            "📖 <b>I am / I'm</b>\n"
            "I am = я есть / я являюсь.\n"
            "I'm = короткая разговорная форма. Смысл тот же; в речи чаще I'm.\n\n"
            "Примеры сейчас голосом.",
            parse_mode="HTML",
            reply_markup=_kb([[BTN_CLEAR], [BTN_UNCLEAR], [BTN_PAUSE]]),
        )
        await _say_en(m, f"I am {name}.")
        await _say_en(m, f"I'm {name}.")
        return

    # speaking final
    if not ok:
        await m.answer("Почти. Слушай модель и повтори целиком.")
        await _say_en(m, f"Hi, I'm {name}. Nice to meet you.")
        return
    p["step"] = "check"
    p["check_i"] = 0
    p["check_ok"] = 0
    p["check_tot"] = 0
    save_users(users, only=uid)
    await m.answer("Сильно. Мини-проверка — и можно к заметке.")
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

    if step == "ask_name":
        name = re.sub(r"[^\w\s\-']", "", text, flags=re.UNICODE).strip()[:32] or "Friend"
        p["name"] = name
        p["step"] = "intro"
        save_users(users, only=uid)
        await m.answer(
            f"Ок, {name}.\n\n"
            "Перед уроком: без параллельных чатов — иначе растянется больше часа.\n"
            "Жми «Готов», когда можно начать.",
            reply_markup=_kb([[BTN_READY], [BTN_PAUSE]]),
        )
        return

    if step == "intro" and text == BTN_READY:
        p["step"] = "warmup_listen"
        save_users(users, only=uid)
        await m.answer(
            "👋 Warm-up\n"
            "По-русски знакомство: «Привет, я …».\n"
            "По-английски почти то же. Слушай:",
            reply_markup=_kb([[BTN_LISTEN_AGAIN], [BTN_NEXT], [BTN_PAUSE]]),
        )
        await _say_en(m, f"Hi, I'm {p['name']}.")
        return

    if step == "warmup_listen":
        if text == BTN_LISTEN_AGAIN:
            await _say_en(m, f"Hi, I'm {p.get('name') or 'Alex'}.")
            return
        if text == BTN_NEXT:
            p["step"] = "warmup_speak"
            save_users(users, only=uid)
            await m.answer(
                "Теперь твоё голосовое: <b>Hi, I'm …</b>\n"
                "Можно «Прослушать ещё раз» перед записью.",
                parse_mode="HTML",
                reply_markup=_kb([[BTN_LISTEN_AGAIN], [BTN_MIC_HINT], [BTN_PAUSE]]),
            )
            return

    if step == "warmup_speak" and text == BTN_LISTEN_AGAIN:
        await _say_en(m, f"Hi, I'm {p.get('name') or 'Alex'}.")
        return

    if step == "explain_iam":
        if text == BTN_UNCLEAR:
            await m.answer(
                "Проще: I am Anna и I'm Anna — это одно и то же. "
                "I'm короче, так говорят чаще. Как “я есть Анна”, только по-английски."
            )
            await _say_en(m, "I'm Anna.")
            return
        if text == BTN_CLEAR:
            p["step"] = "explain_you"
            save_users(users, only=uid)
            await m.answer(
                "📖 <b>you are / you're</b>\n"
                "Про собеседника: you are → в речи you're.\n"
                "Вопрос: Are you …?",
                parse_mode="HTML",
                reply_markup=_kb([[BTN_CLEAR], [BTN_UNCLEAR], [BTN_PAUSE]]),
            )
            await _say_en(m, "You're Alex.")
            await _say_en(m, "Are you Alex?")
            return

    if step == "explain_you":
        if text == BTN_UNCLEAR:
            await m.answer(
                "You = ты/вы. Are you Tom? = Ты Том? "
                "You're Tom. = Ты Том (утверждение)."
            )
            return
        if text == BTN_CLEAR:
            p["step"] = "practice"
            p["practice_i"] = 0
            save_users(users, only=uid)
            await _send_practice(m, p)
            save_users(users, only=uid)
            return

    if step == "practice":
        item = practice_item(p)
        if not item:
            return
        idx = _parse_choice(text, len(item["options"]))
        if idx is None:
            await m.answer("Жми вариант кнопкой 1–4.")
            return
        if idx == int(item["correct"]):
            await m.answer("✅")
        else:
            right = item["options"][int(item["correct"])]
            await m.answer(f"Не то. Верно: <b>{right}</b>", parse_mode="HTML")
        p["practice_i"] = int(p.get("practice_i") or 0) + 1
        save_users(users, only=uid)
        await _send_practice(m, p)
        save_users(users, only=uid)
        return

    if step == "listening":
        item = listen_item(p)
        if not item:
            return
        if text == BTN_LISTEN_AGAIN:
            await _say_en(m, item["audio"])
            return
        if text == BTN_SHOW_TEXT:
            p["listen_show"] = True
            save_users(users, only=uid)
            await m.answer(f"📄 <code>{item['audio']}</code>", parse_mode="HTML")
            return
        idx = _parse_choice(text, len(item["options"]))
        if idx is None:
            await m.answer("Выбери ответ кнопкой, или «Показать текст» / «Прослушать ещё раз».")
            return
        if idx == int(item["correct"]):
            await m.answer("✅")
        else:
            await m.answer(f"Верно: <b>{item['options'][int(item['correct'])]}</b>", parse_mode="HTML")
        p["listen_i"] = int(p.get("listen_i") or 0) + 1
        p["listen_show"] = False
        save_users(users, only=uid)
        await _send_listening(m, p)
        save_users(users, only=uid)
        return

    if step == "speaking" and text == BTN_LISTEN_AGAIN:
        await _say_en(m, f"Hi, I'm {p.get('name') or 'Alex'}. Nice to meet you.")
        return

    if step == "check":
        item = check_item(p)
        if not item:
            return
        idx = _parse_choice(text, len(item["options"]))
        if idx is None:
            await m.answer("Выбери вариант кнопкой.")
            return
        p["check_tot"] = int(p.get("check_tot") or 0) + 1
        if idx == int(item["correct"]):
            p["check_ok"] = int(p.get("check_ok") or 0) + 1
            await m.answer("✅")
        else:
            await m.answer(f"Верно: <b>{item['options'][int(item['correct'])]}</b>", parse_mode="HTML")
        p["check_i"] = int(p.get("check_i") or 0) + 1
        save_users(users, only=uid)
        await _send_check(m, p)
        save_users(users, only=uid)
        return

    if step == "note":
        if text == BTN_SKIP_NOTE:
            p["note"] = ""
        else:
            p["note"] = text[:500]
        save_users(users, only=uid)
        await _finish(m, user, users, uid)
        return

    await m.answer("Жми кнопки урока или /a0_curs чтобы начать заново.")
