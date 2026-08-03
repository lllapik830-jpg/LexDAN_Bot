"""Эксклюзивные задания Рико — /test_winners, сказка 1 места, паки 2/3."""

from __future__ import annotations

import random

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import MANAGER_ID
from handlers.filters import ModeFilter
from handlers.keyboards import main_menu
from services.database import (
    MODE_EXCLUSIVE,
    MODE_MENU,
    users_for,
    get_user,
    save_users,
    set_mode,
)
from services.growth import ensure_growth, is_premium
from services.exclusive_rico import (
    BTN_EX_PLACE_1,
    BTN_EX_PLACE_2,
    BTN_EX_PLACE_3,
    BTN_EX_NEXT,
    BTN_EX_HINT,
    BTN_EX_SKIP,
    BTN_EX_EXIT,
    BTN_EX_TRANSLATE,
    BTN_EX_READY,
    BTN_EX_RESUME,
    BTN_EX_RESTART,
    PLACE_BUTTONS,
    get_pack,
    start_pack,
    get_active,
    clear_active,
    park_active,
    has_resumable_progress,
    resume_checkpoint,
    ensure_exclusive,
    is_story_mode,
    ready_html,
    story_begin,
    story_next,
    current_scene,
    current_task,
    format_line_html,
    format_task_card,
    resolve_voice_id,
    mcq_options,
    check_answer,
    advance,
    grant_task_vocab,
)
from services.elevenlabs import send_voice_reply
from services.stt import recognize_english

router = Router()


def _uid(m: Message) -> str:
    return str(m.from_user.id)


def _can_test(m: Message, user: dict) -> bool:
    if m.from_user and m.from_user.id == MANAGER_ID:
        return True
    if user.get("in_promo_trial") or user.get("reg_full_trial_granted"):
        return True
    return bool(is_premium(user))


def _hub_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_EX_PLACE_1)],
            [KeyboardButton(text=BTN_EX_PLACE_2)],
            [KeyboardButton(text=BTN_EX_PLACE_3)],
            [KeyboardButton(text="🔙 Вернуться в меню")],
        ],
        resize_keyboard=True,
    )


def _ready_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_EX_READY)],
            [KeyboardButton(text=BTN_EX_EXIT)],
        ],
        resize_keyboard=True,
    )


def _resume_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_EX_RESUME)],
            [KeyboardButton(text=BTN_EX_RESTART)],
            [KeyboardButton(text=BTN_EX_EXIT)],
        ],
        resize_keyboard=True,
    )


def _line_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_EX_NEXT), KeyboardButton(text=BTN_EX_TRANSLATE)],
            [KeyboardButton(text=BTN_EX_EXIT)],
        ],
        resize_keyboard=True,
    )


def _play_kb(task: dict | None) -> ReplyKeyboardMarkup:
    rows: list[list[KeyboardButton]] = []
    if task and (task.get("kind") or "") == "mcq":
        for opt in mcq_options(task):
            rows.append([KeyboardButton(text=opt)])
    rows.append([KeyboardButton(text=BTN_EX_HINT), KeyboardButton(text=BTN_EX_SKIP)])
    rows.append([KeyboardButton(text=BTN_EX_TRANSLATE)])
    rows.append([KeyboardButton(text=BTN_EX_EXIT)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


async def _send_story_scene(m: Message, user: dict, scene: dict | None) -> None:
    if not scene:
        clear_active(user)
        await m.answer(
            "🏁 <b>Конец сказки.</b>\n"
            "Рико стал учителем — а ты прошёл легенду. "
            "Можно выбрать другое место или выйти в меню.",
            reply_markup=_hub_kb(),
            parse_mode="HTML",
        )
        return

    if scene.get("type") == "task":
        await m.answer(
            format_task_card(user, scene),
            reply_markup=_play_kb(scene),
            parse_mode="HTML",
        )
        if (scene.get("kind") or "") == "voice":
            line = (scene.get("voice_text") or "").strip()
            if line:
                await send_voice_reply(
                    m,
                    line,
                    title="Легенда · задание",
                    voice_id=resolve_voice_id("rico"),
                )
        return

    html = format_line_html(scene)
    await m.answer(html, reply_markup=_line_kb(), parse_mode="HTML")
    en = (scene.get("en") or "").strip()
    if en:
        speaker = (scene.get("speaker") or "narrator").lower()
        await send_voice_reply(
            m,
            en,
            title=scene.get("label") or speaker,
            voice_id=resolve_voice_id(speaker),
        )


async def _send_pack_task(m: Message, user: dict, *, resumed: bool = False) -> None:
    task = current_task(user)
    if not task:
        clear_active(user)
        await m.answer(
            "🦜 Пак пройден или пуст. Выбери место снова или выйди в меню.",
            reply_markup=_hub_kb(),
            parse_mode="HTML",
        )
        return
    if resumed:
        active = get_active(user) or {}
        n = int(active.get("index") or 0) + 1
        total = int(active.get("total") or 0)
        await m.answer(
            f"▶️ Продолжаем с задания <b>{n}/{total}</b>",
            parse_mode="HTML",
        )
    await m.answer(format_task_card(user, task), reply_markup=_play_kb(task), parse_mode="HTML")
    if (task.get("kind") or "") == "voice":
        line = (task.get("voice_text") or "").strip()
        if line:
            from services.voices import RICO_VOICE_ID

            await send_voice_reply(m, line, title="Эксклюзив Рико", voice_id=RICO_VOICE_ID)


async def _resume_story_into(m: Message, user: dict) -> None:
    active = resume_checkpoint(user, 1)
    if not active:
        start_pack(user, 1, test_mode=True)
        await m.answer(ready_html(), reply_markup=_ready_kb(), parse_mode="HTML")
        return
    phase = active.get("phase")
    if phase == "ready":
        await m.answer(ready_html(), reply_markup=_ready_kb(), parse_mode="HTML")
        return
    await m.answer(
        "▶️ Продолжаем сказку с того места, где остановился.",
        parse_mode="HTML",
    )
    await _send_story_scene(m, user, current_scene(user))


@router.message(Command("test_winners"))
async def cmd_test_winners(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    if not _can_test(m, user):
        return
    park_active(user)
    ensure_exclusive(user)
    user["exclusive_rico"]["pending_place"] = None
    set_mode(uid, MODE_EXCLUSIVE)
    users = users_for(uid)
    user = get_user(users, uid)
    save_users(users, only=uid)
    await m.answer(
        "🧪 <b>Тест призов ивента</b>\n\n"
        "Выбери место:\n"
        "🥇 <b>1</b> — Легенда · сказка (прогресс сохраняется)\n"
        "🥈 <b>2</b> — Мастер · сленг + карты слов → в повторение\n"
        "🥉 <b>3</b> — Охотник · ошибки + загадки → в повторение\n\n"
        "Выход сохраняет прогресс 2/3 и сказки 1 места.",
        reply_markup=_hub_kb(),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text.in_(set(PLACE_BUTTONS)))
async def pick_place(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    place = PLACE_BUTTONS.get((m.text or "").strip())
    if not place:
        return

    park_active(user)
    ensure_exclusive(user)

    if place == 1 and has_resumable_progress(user, 1):
        user["exclusive_rico"]["pending_place"] = 1
        save_users(users, only=uid)
        cp = user["exclusive_rico"]["checkpoints"].get("1") or {}
        done = int(cp.get("tasks_done") or 0)
        await m.answer(
            "📖 У тебя есть сохранённая сказка.\n"
            f"Сделано заданий: <b>{done}/20</b>.\n\n"
            "Продолжить с места остановки или начать сначала?",
            reply_markup=_resume_kb(),
            parse_mode="HTML",
        )
        return

    if place in (2, 3) and has_resumable_progress(user, place):
        resume_checkpoint(user, place)
        save_users(users, only=uid)
        users = users_for(uid)
        user = get_user(users, uid)
        await _send_pack_task(m, user, resumed=True)
        return

    start_pack(user, place, test_mode=True)
    user["exclusive_rico"]["pending_place"] = None
    save_users(users, only=uid)

    if place == 1:
        await m.answer(ready_html(), reply_markup=_ready_kb(), parse_mode="HTML")
        return

    pack = get_pack(place)
    await m.answer(pack.get("intro_html") or pack.get("title") or "Старт!", parse_mode="HTML")
    users = users_for(uid)
    user = get_user(users, uid)
    await _send_pack_task(m, user)


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_RESUME)
async def resume_place(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_exclusive(user)
    place = int(user["exclusive_rico"].get("pending_place") or 1)
    user["exclusive_rico"]["pending_place"] = None
    if place == 1:
        await _resume_story_into(m, user)
        save_users(users, only=uid)
        return
    if has_resumable_progress(user, place):
        resume_checkpoint(user, place)
        save_users(users, only=uid)
        users = users_for(uid)
        user = get_user(users, uid)
        await _send_pack_task(m, user)
        return
    await m.answer("Сохранённого прогресса нет — выбери место заново.", reply_markup=_hub_kb())


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_RESTART)
async def restart_place(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_exclusive(user)
    place = int(user["exclusive_rico"].get("pending_place") or 1)
    user["exclusive_rico"]["pending_place"] = None
    start_pack(user, place, test_mode=True)
    save_users(users, only=uid)
    if place == 1:
        await m.answer(ready_html(), reply_markup=_ready_kb(), parse_mode="HTML")
        return
    pack = get_pack(place)
    await m.answer(pack.get("intro_html") or "Старт!", parse_mode="HTML")
    users = users_for(uid)
    user = get_user(users, uid)
    await _send_pack_task(m, user)


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_READY)
async def story_ready(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    if not is_story_mode(user):
        return
    active = get_active(user)
    if not active or active.get("phase") != "ready":
        await m.answer("Нажми «1 место», чтобы начать сказку.", reply_markup=_hub_kb())
        return
    scene = story_begin(user)
    save_users(users, only=uid)
    await _send_story_scene(m, user, scene)


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_NEXT)
async def story_or_pack_next(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    if is_story_mode(user):
        active = get_active(user)
        if active and active.get("phase") == "task":
            await m.answer(
                "Сейчас задание — ответь, возьми подсказку или пропусти.",
                reply_markup=_play_kb(current_task(user)),
            )
            return
        scene = story_next(user)
        save_users(users, only=uid)
        users = users_for(uid)
        user = get_user(users, uid)
        await _send_story_scene(m, user, scene)
        return
    await exclusive_skip(m)


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_TRANSLATE)
async def exclusive_translate(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    active = get_active(user)
    if is_story_mode(user) and active:
        ru = (active.get("last_ru") or "").strip()
        if ru:
            await m.answer(
                f"🌐 <b>Перевод:</b>\n{ru}",
                reply_markup=_line_kb() if active.get("phase") == "line" else _play_kb(current_task(user)),
                parse_mode="HTML",
            )
            return
        await m.answer(
            "Пока нечего переводить — дождись реплики на английском.",
            reply_markup=_line_kb() if active.get("phase") == "line" else _hub_kb(),
        )
        return
    await m.answer("Перевод доступен в сказке 1 места 🌍", reply_markup=_hub_kb())


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_EXIT)
@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == "🔙 Вернуться в меню")
async def exit_exclusive(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    saved = park_active(user)
    ensure_exclusive(user)
    user["exclusive_rico"]["pending_place"] = None
    set_mode(uid, MODE_MENU)
    users = users_for(uid)
    user = get_user(users, uid)
    save_users(users, only=uid)
    note = "\n\n💾 Прогресс сохранён — можно продолжить позже." if saved else ""
    await m.answer(f"Главное меню:{note}", reply_markup=main_menu(user))


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_HINT)
async def exclusive_hint(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    task = current_task(user)
    if not task:
        await m.answer("Сначала выбери место 👇", reply_markup=_hub_kb())
        return
    hint = (task.get("hint_ru") or "Думай про смысл и конструкцию — ответ за тебя не скажу 💛").strip()
    await m.answer(f"💡 {hint}", reply_markup=_play_kb(task), parse_mode="HTML")


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text == BTN_EX_SKIP)
async def exclusive_skip(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    if not get_active(user):
        await m.answer("Сначала выбери место 👇", reply_markup=_hub_kb())
        return

    if is_story_mode(user):
        if get_active(user).get("phase") != "task":
            await m.answer("Пропуск только на заданиях. Жми «Далее».", reply_markup=_line_kb())
            return
        advance(user)
        save_users(users, only=uid)
        users = users_for(uid)
        user = get_user(users, uid)
        await m.answer("⏭ Ок, история идёт дальше…", parse_mode="HTML")
        if not get_active(user):
            await _send_story_scene(m, user, None)
            return
        await _send_story_scene(m, user, current_scene(user))
        return

    more = advance(user)
    save_users(users, only=uid)
    if not more:
        await m.answer(
            "🏁 Пак пройден (с пропусками). Можно выбрать другое место или выйти.",
            reply_markup=_hub_kb(),
            parse_mode="HTML",
        )
        return
    await m.answer("⏭ Ок, дальше — не зависаем 🚀", parse_mode="HTML")
    users = users_for(uid)
    user = get_user(users, uid)
    task = current_task(user)
    if task:
        await m.answer(format_task_card(user, task), reply_markup=_play_kb(task), parse_mode="HTML")


@router.message(ModeFilter(MODE_EXCLUSIVE), F.voice)
async def exclusive_voice(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    task = current_task(user)
    if not task:
        return
    if (task.get("kind") or "") != "voice":
        await m.answer("Здесь пока текстом 🙂", reply_markup=_play_kb(task))
        return
    await m.answer("🎧 Слушаю…", reply_markup=_play_kb(task))
    try:
        file = await m.bot.get_file(m.voice.file_id)
        buf = await m.bot.download_file(file.file_path)
        heard = (recognize_english(buf.read()) or "").strip()
    except Exception:
        heard = ""
    if not heard:
        await m.answer(
            "Не разобрал голос 😅 Попробуй ещё раз чуть чётче или напиши текстом.",
            reply_markup=_play_kb(task),
        )
        return
    await _grade_and_advance(m, uid, user, users, task, heard)


@router.message(ModeFilter(MODE_EXCLUSIVE), F.text)
async def exclusive_answer(m: Message):
    text = (m.text or "").strip()
    if not text or text.startswith("/"):
        return
    if text in {
        BTN_EX_PLACE_1,
        BTN_EX_PLACE_2,
        BTN_EX_PLACE_3,
        BTN_EX_HINT,
        BTN_EX_SKIP,
        BTN_EX_NEXT,
        BTN_EX_EXIT,
        BTN_EX_TRANSLATE,
        BTN_EX_READY,
        BTN_EX_RESUME,
        BTN_EX_RESTART,
        "🔙 Вернуться в меню",
    }:
        return

    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)

    if is_story_mode(user):
        active = get_active(user)
        if active and active.get("phase") == "ready":
            await m.answer("Нажми «Я готов!», когда будешь готов ✨", reply_markup=_ready_kb())
            return
        if active and active.get("phase") == "line":
            await m.answer("Жми «Далее», чтобы продолжить сказку ➡️", reply_markup=_line_kb())
            return

    task = current_task(user)
    if not task:
        await m.answer("Выбери место кнопкой 👇", reply_markup=_hub_kb())
        return
    await _grade_and_advance(m, uid, user, users, task, text)


async def _grade_and_advance(
    m: Message, uid: str, user: dict, users: dict, task: dict, answer: str
) -> None:
    result = check_answer(task, answer)
    if not result.get("correct"):
        save_users(users, only=uid)
        await m.answer(
            "😅 " + (result.get("explain_ru") or "Почти! Попробуй ещё раз — тебе по плечу 💪"),
            reply_markup=_play_kb(task),
            parse_mode="HTML",
        )
        return

    cheers = [
        "✅ Есть! Красава 🦜",
        "✅ В яблочко 🎯",
        "✅ Супер, так держать ✨",
    ]
    await m.answer(random.choice(cheers), parse_mode="HTML")

    # слова/фразы 2–3 места → повторение + счётчики
    if not is_story_mode(user):
        notes = grant_task_vocab(user, task)
        for note in notes:
            wl = int(user.get("words_learned") or 0)
            pl = int(user.get("phrases_learned") or 0)
            await m.answer(
                f"{note}\n📊 Выучено: слова <b>{wl}</b> · фразы <b>{pl}</b>",
                parse_mode="HTML",
            )

    if is_story_mode(user):
        advance(user)
        save_users(users, only=uid)
        users = users_for(uid)
        user = get_user(users, uid)
        if not get_active(user):
            await _send_story_scene(m, user, None)
            return
        await _send_story_scene(m, user, current_scene(user))
        return

    more = advance(user)
    save_users(users, only=uid)
    if not more:
        await m.answer(
            "🏆 <b>Пак закрыт!</b> Рико гордится.\n"
            "Новые слова и фразы уже в «🔁 Повторить изученные…».\n"
            "Можно прогнать другое место или вернуться в меню.",
            reply_markup=_hub_kb(),
            parse_mode="HTML",
        )
        return
    users = users_for(uid)
    user = get_user(users, uid)
    task2 = current_task(user)
    if task2:
        await m.answer(format_task_card(user, task2), reply_markup=_play_kb(task2), parse_mode="HTML")
