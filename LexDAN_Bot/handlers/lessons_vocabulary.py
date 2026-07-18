"""
Раздел Vocabulary (A0–C2).
"""

import random

from aiogram import F, Router
from aiogram.types import Message

from aiogram.dispatcher.event.bases import SkipHandler

from handlers.filters import ModeFilter
from handlers.lesson_filters import LessonHubFilter
from handlers.lesson_keyboards import level_sections_kb
from handlers.vocabulary_keyboards import (
    BTN_VOCABULARY,
    BTN_LEARN_PHRASES,
    BTN_ALL_LEVELS,
    BTN_REPEAT_WORDS,
    BTN_REPEAT_PHRASES,
    BTN_DONT_REMEMBER,
    BTN_BACK_DRILL,
    vocab_topics_kb,
    vocab_topic_kb,
    vocab_phrase_topic_kb,
    vocab_practice_kb,
    global_drill_menu_kb,
    drill_kb,
    topic_progress_line,
)
from data.vocabulary_curriculum import (
    format_vocab_topics_list,
    get_vocab_topic,
    get_vocab_topic_by_index,
    get_vocab_topics,
)
from data.vocabulary_words import (
    get_words,
    get_word_entry,
    words_total,
    has_vocabulary_level,
)
from data.vocabulary_phrases import (
    get_phrases,
    get_phrase_entry,
    phrases_total,
)
from services.database import MODE_LESSONS, get_user, load_users, save_users, set_mode
from services.lesson_state import assessment_busy, ensure_lesson
from services.vocabulary_state import (
    ensure_vocab_progress,
    is_word_learned,
    is_phrase_learned,
    mark_word_learned,
    mark_phrase_learned,
    finish_word_practice,
    finish_phrase_practice,
    sync_vocab_counters,
    topic_words_progress,
    topic_phrases_progress,
    set_vocab_hub,
    update_vocab_lesson,
    clear_vocab_session,
    get_all_learned_word_entries,
    get_all_learned_phrase_entries,
)
from services.vocabulary_tutor import (
    generate_vocab_text,
    rico_word_card,
    rico_phrase_card,
    check_vocab_sentence,
    rico_dont_remember,
)
from handlers.keyboards import BTN_START_TODAY
from services.growth import note_lesson_activity, touch_activity

router = Router()
VOCAB_INTRO = (
    "📗 <b>Vocabulary</b>\n\n"
    "🦜 Учим слова по темам: текст → карточки → 2 предложения.\n"
    "Есть устойчивые фразы отдельной кнопкой."
)


def _strip_mark(text: str) -> str:
    return (text or "").replace("✅ ", "").strip()


def _topic_progress(user: dict, level: str, topic_id: str):
    wt = words_total(level, topic_id)
    pt = phrases_total(level, topic_id)
    wl, _, wd = topic_words_progress(user, level, topic_id, wt)
    pl, _, pd = topic_phrases_progress(user, level, topic_id, pt)
    done = wd and (pt == 0 or pd)
    return wl, wt, pl, pt, done


def _pick_unlearned_words(user: dict, level: str, topic_id: str, n: int = 5) -> list[dict]:
    pool = [w for w in get_words(level, topic_id) if not is_word_learned(user, level, topic_id, w["en"])]
    random.shuffle(pool)
    return pool[:n]


def _pick_unlearned_phrases(user: dict, level: str, topic_id: str, n: int = 2) -> list[dict]:
    pool = [p for p in get_phrases(level, topic_id) if not is_phrase_learned(user, level, topic_id, p["en"])]
    random.shuffle(pool)
    return pool[:n]


async def _send_word_story(m: Message, user: dict, *, count_toward_limit: bool = True):
    from services.growth import (
        can_start_vocab_text,
        note_vocab_text_started,
        ensure_growth,
    )
    from handlers.lesson_keyboards import lesson_limit_inline_kb

    level = user["lesson"]["level"]
    topic_id = user["lesson"]["vocab_topic_id"]
    topic = get_vocab_topic(level, topic_id)
    batch = _pick_unlearned_words(user, level, topic_id, 5)
    if not batch:
        users = load_users()
        user = get_user(users, str(m.from_user.id))
        ensure_growth(user)
        save_users(users)
        wt = words_total(level, topic_id)
        wl, _, _, _, _ = _topic_progress(user, level, topic_id)
        await m.reply(
            f"🎉 <b>Молодец!</b> Новые слова по теме «{topic['title']}» изучены ({wl}/{wt}) ✅\n\n"
            "Можешь закрепить в <b>📋 Задания по всем уровням</b> → повтор слов.",
            reply_markup=vocab_topics_kb(level, user),
            parse_mode="HTML",
        )
        set_vocab_hub(str(m.from_user.id), "vocab_list")
        return

    if count_toward_limit:
        users = load_users()
        user = get_user(users, str(m.from_user.id))
        ensure_growth(user)
        ok, tip = can_start_vocab_text(user)
        if not ok:
            save_users(users)
            await m.reply(tip or "", reply_markup=lesson_limit_inline_kb(), parse_mode="HTML")
            set_vocab_hub(str(m.from_user.id), "vocab_list", level=level)
            return
        note_vocab_text_started(user)
        save_users(users)

    await m.reply("🦜 Пишу текст…")
    story = generate_vocab_text(level, topic["title"], batch, kind="words")
    # ВАЖНО: кнопки = выбранный батч слов, а не «highlighted» от ИИ (там часто 1 слово)
    batch_en = [w["en"] for w in batch]

    update_vocab_lesson(
        str(m.from_user.id),
        hub="vocab_topic",
        vocab_mode="words",
        vocab_batch=batch_en,
        vocab_text_en=story["text_en"],
        vocab_text_ru=story["text_ru"],
        vocab_active_item=None,
        vocab_practice_step=0,
        vocab_practice_done=0,
        vocab_last_sentence="",
        vocab_used_sentences=[],
    )
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    prog = topic_progress_line(user, level, topic_id)
    text = (
        f"📗 <b>{topic['title']}</b> · {prog}\n\n"
        f"{story['text_en']}\n\n"
        f"{story['text_ru']}\n\n"
        f"🦜 В этом тексте <b>{len(batch_en)}</b> новых слов. "
        "Нажми слово на кнопке, чтобы изучить его."
    )
    await m.reply(text, reply_markup=vocab_topic_kb(level, topic_id, user, batch_en), parse_mode="HTML")


async def _send_phrase_story(m: Message, user: dict, *, count_toward_limit: bool = True):
    from services.growth import (
        can_start_vocab_text,
        note_vocab_text_started,
        ensure_growth,
    )
    from handlers.lesson_keyboards import lesson_limit_inline_kb

    level = user["lesson"]["level"]
    topic_id = user["lesson"]["vocab_topic_id"]
    topic = get_vocab_topic(level, topic_id)
    batch = _pick_unlearned_phrases(user, level, topic_id, 2)
    if not batch:
        pt = phrases_total(level, topic_id)
        pl, _, pd = topic_phrases_progress(user, level, topic_id, pt)
        await m.reply(
            f"🎉 Фразы по теме «{topic['title']}» изучены ({pl}/{pt}) ✅",
            reply_markup=vocab_topics_kb(level, user),
            parse_mode="HTML",
        )
        set_vocab_hub(str(m.from_user.id), "vocab_list")
        return

    if count_toward_limit:
        users = load_users()
        user = get_user(users, str(m.from_user.id))
        ensure_growth(user)
        ok, tip = can_start_vocab_text(user)
        if not ok:
            save_users(users)
            await m.reply(tip or "", reply_markup=lesson_limit_inline_kb(), parse_mode="HTML")
            return
        note_vocab_text_started(user)
        save_users(users)

    await m.reply("🦜 Готовлю текст с фразами…")
    story = generate_vocab_text(level, topic["title"], batch, kind="phrases")
    batch_en = [p["en"] for p in batch]

    update_vocab_lesson(
        str(m.from_user.id),
        hub="vocab_phrases",
        vocab_mode="phrases",
        vocab_batch=batch_en,
        vocab_text_en=story["text_en"],
        vocab_text_ru=story["text_ru"],
        vocab_active_item=None,
        vocab_practice_step=0,
        vocab_practice_done=0,
        vocab_last_sentence="",
        vocab_used_sentences=[],
    )
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    text = (
        f"📌 <b>Фразы · {topic['title']}</b>\n\n"
        f"{story['text_en']}\n\n"
        f"{story['text_ru']}\n\n"
        "🦜 Нажми на фразу, чтобы разобрать её подробнее."
    )
    await m.reply(text, reply_markup=vocab_phrase_topic_kb(level, topic_id, user, batch_en), parse_mode="HTML")


def _next_drill_item(user: dict) -> dict | None:
    lesson = user.get("lesson") or {}
    kind = lesson.get("drill_kind")
    queue = list(lesson.get("drill_queue") or [])
    idx = int(lesson.get("drill_index") or 0)
    if idx >= len(queue):
        random.shuffle(queue)
        idx = 0
    if not queue:
        return None
    level, topic_id, en = queue[idx]
    if kind == "words":
        entry = get_word_entry(level, topic_id, en)
    else:
        entry = get_phrase_entry(level, topic_id, en)
    if not entry:
        return None
    dirs = list(lesson.get("drill_dirs") or [])
    direction = random.choice(["ru_en", "en_ru"])
    if len(dirs) >= 4 and len(set(dirs[-4:])) == 1:
        direction = "en_ru" if dirs[-1] == "ru_en" else "ru_en"
    return {
        "kind": kind,
        "level": level,
        "topic_id": topic_id,
        "entry": entry,
        "direction": direction,
        "queue": queue,
        "index": idx,
        "dirs": dirs + [direction],
    }


async def _send_drill_question(m: Message, user: dict):
    pack = _next_drill_item(user)
    if not pack:
        await m.reply("🦜 Пока нет изученных слов/фраз для повтора.", reply_markup=global_drill_menu_kb())
        return
    entry = pack["entry"]
    if pack["direction"] == "ru_en":
        prompt = f"🇷🇺 Переведи на английский:\n<b>{entry['ru']}</b>"
        answer = entry["en"]
    else:
        prompt = f"🇬🇧 Переведи на русский:\n<b>{entry['en']}</b>"
        answer = entry["ru"]
    update_vocab_lesson(
        str(m.from_user.id),
        drill_current={
            "answer": answer,
            "entry": entry,
            "direction": pack["direction"],
            "kind": pack["kind"],
        },
        drill_queue=pack["queue"],
        drill_index=pack["index"] + 1,
        drill_dirs=pack["dirs"],
    )
    await m.reply(prompt, reply_markup=drill_kb(), parse_mode="HTML")


@router.message(F.text == BTN_START_TODAY)
async def start_today(m: Message):
    """Онбординг после теста / из напоминания: сразу Vocabulary → первая незакрытая тема."""
    uid = str(m.from_user.id)
    set_mode(uid, MODE_LESSONS)
    users = load_users()
    user = get_user(users, uid)
    ensure_lesson(user)
    ensure_vocab_progress(user)
    touch_activity(user)
    note_lesson_activity(user)
    save_users(users)

    level = user.get("level") or user.get("lesson", {}).get("level") or "A1"
    if not get_vocab_topics(level):
        for lv in ("A0", "A1", "A2", "B1"):
            if get_vocab_topics(lv):
                level = lv
                break
    has_vocabulary_level(level)

    topics = get_vocab_topics(level) or []
    pick = None
    for topic in topics:
        wt = words_total(level, topic["id"])
        if wt <= 0:
            continue
        wl, _, wd = topic_words_progress(user, level, topic["id"], wt)
        if not wd:
            pick = topic
            break
    if pick is None and topics:
        pick = topics[0]

    if not pick:
        await m.reply(
            "🦜 Пока нет тем Vocabulary. Открой 📚 Уроки и выбери уровень.",
            parse_mode="HTML",
        )
        return

    from services.growth import can_start_vocab_text, ensure_growth
    from handlers.lesson_keyboards import lesson_limit_inline_kb

    users = load_users()
    user = get_user(users, uid)
    ensure_growth(user)
    wt = words_total(level, pick["id"])
    _, _, wd = topic_words_progress(user, level, pick["id"], wt)
    if not wd:
        ok, tip = can_start_vocab_text(user)
        if not ok:
            await m.reply(tip or "", reply_markup=lesson_limit_inline_kb(), parse_mode="HTML")
            return

    set_vocab_hub(
        uid,
        "vocab_topic",
        level=level,
        vocab_topic_id=pick["id"],
        vocab_topic_title=pick["title"],
    )
    users = load_users()
    user = get_user(users, uid)
    await m.reply(
        f"🦜 Отлично! Старт дня: Vocabulary · <b>{level}</b> · «{pick['title']}».\n"
        "Читай текст и жми слова — 15 минут, и день засчитан 💪",
        parse_mode="HTML",
    )
    await _send_word_story(m, user)


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_VOCABULARY)
async def open_vocabulary(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if assessment_busy(user):
        return
    ensure_lesson(user)
    level = user["lesson"].get("level") or user.get("level") or "A1"
    if not get_vocab_topics(level):
        await m.reply(
            f"🦜 Нет тем Vocabulary для уровня <b>{level}</b>.",
            reply_markup=level_sections_kb(),
            parse_mode="HTML",
        )
        return
    # лениво подтянуть банки A2–C2
    has_vocabulary_level(level)
    set_vocab_hub(str(m.from_user.id), "vocab_list", level=level)
    users = load_users()
    user = get_user(users, str(m.from_user.id))

    def prog(lv, tid):
        wt = words_total(lv, tid)
        pt = phrases_total(lv, tid)
        wl, _, wd = topic_words_progress(user, lv, tid, wt)
        pl, _, pd = topic_phrases_progress(user, lv, tid, pt)
        learned = wl + pl
        total = wt + pt
        done = wd and (pt == 0 or pd)
        return learned, total, done

    await m.reply(VOCAB_INTRO, parse_mode="HTML")
    await m.reply(
        format_vocab_topics_list(level, prog),
        reply_markup=vocab_topics_kb(level, user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("vocab_list"), F.text.regexp(r"^\d+$"))
async def vocab_choose_topic(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    from services.growth import can_start_vocab_text, ensure_growth
    from handlers.lesson_keyboards import lesson_limit_inline_kb

    ensure_growth(user)
    level = user["lesson"]["level"] or "A1"
    topic = get_vocab_topic_by_index(level, int(m.text))
    if not topic:
        await m.reply("Нет такой темы.", reply_markup=vocab_topics_kb(level, user))
        return

    wt = words_total(level, topic["id"])
    wl, _, wd = topic_words_progress(user, level, topic["id"], wt)
    if wd:
        await m.reply(
            f"✅ Тема «{topic['title']}» по словам пройдена ({wl}/{wt}).\n"
            "Повтори в <b>📋 Задания по всем уровням</b>.",
            reply_markup=vocab_topics_kb(level, user),
            parse_mode="HTML",
        )
        return

    ok, tip = can_start_vocab_text(user)
    if not ok:
        save_users(users)
        await m.reply(tip or "", reply_markup=lesson_limit_inline_kb(), parse_mode="HTML")
        return

    set_vocab_hub(
        str(m.from_user.id),
        "vocab_topic",
        level=level,
        vocab_topic_id=topic["id"],
        vocab_topic_title=topic["title"],
    )
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await _send_word_story(m, user, count_toward_limit=True)


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_LEARN_PHRASES)
async def vocab_open_phrases(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    lesson = user.get("lesson") or {}
    if lesson.get("hub") not in {"vocab_topic", "vocab_word_practice"}:
        return
    level = lesson.get("level") or "A1"
    topic_id = lesson.get("vocab_topic_id")
    if not topic_id:
        return
    set_vocab_hub(str(m.from_user.id), "vocab_phrases", level=level, vocab_topic_id=topic_id)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await _send_phrase_story(m, user)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("vocab_topic"), F.text)
async def vocab_word_button(m: Message):
    """Выбор слова из батча (только hub=vocab_topic — не перехватывать практику!)."""
    text = _strip_mark(m.text or "")
    if text in {BTN_LEARN_PHRASES, "⬅️ К темам", "🔙 Вернуться в меню", "⬅️ К словам", "⬅️ К теме (слова)"}:
        raise SkipHandler
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    lesson = user["lesson"]
    level = lesson["level"]
    topic_id = lesson["vocab_topic_id"]
    topic_title = lesson.get("vocab_topic_title") or "Vocabulary"
    word = get_word_entry(level, topic_id, text)
    if not word:
        batch = lesson.get("vocab_batch") or []
        await m.reply("Выбери слово кнопкой из списка.", reply_markup=vocab_topic_kb(level, topic_id, user, batch))
        return
    if is_word_learned(user, level, topic_id, word["en"]):
        await m.reply("Это слово уже изучено ✅", reply_markup=vocab_topic_kb(level, topic_id, user, lesson.get("vocab_batch") or []))
        return
    update_vocab_lesson(
        str(m.from_user.id),
        hub="vocab_word_practice",
        vocab_active_item=word["en"],
        vocab_practice_done=0,
        vocab_practice_step=0,
        vocab_last_sentence="",
        vocab_used_sentences=[],
    )
    card = rico_word_card(level, topic_title, word)
    await m.reply(card, reply_markup=vocab_practice_kb(), parse_mode="HTML")


def _vocab_check_reply(result: dict) -> str:
    fb = (result.get("feedback_ru") or "Попробуй ещё раз.").strip()
    errors = (result.get("errors_ru") or "").strip()
    better = (result.get("better_en") or "").strip()
    lines = [f"🦜 {fb}"]
    if errors:
        lines.append(f"<b>Что не так:</b> {errors}")
    if better:
        lines.append(f"<b>Исправленный вариант:</b> <i>{better}</i>")
        lines.append("Напиши <b>своё новое</b> предложение — не копируй это и не повторяй прошлое.")
    else:
        lines.append("Напиши другое предложение с этим словом.")
    return "\n".join(lines)


def _normalize_sentence(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def _is_repeat_sentence(lesson: dict, text: str) -> bool:
    norm = _normalize_sentence(text)
    if not norm:
        return True
    last = _normalize_sentence(lesson.get("vocab_last_sentence") or "")
    if last and norm == last:
        return True
    used = lesson.get("vocab_used_sentences") or []
    return norm in {_normalize_sentence(x) for x in used}


def _remember_sentence(user_id: str, text: str, *, done: int | None = None) -> None:
    users = load_users()
    user = get_user(users, user_id)
    lesson = user.get("lesson") or {}
    used = list(lesson.get("vocab_used_sentences") or [])
    norm = _normalize_sentence(text)
    if norm and norm not in used:
        used.append(norm)
    fields = {
        "vocab_last_sentence": text,
        "vocab_used_sentences": used[-20:],
    }
    if done is not None:
        fields["vocab_practice_done"] = done
    update_vocab_lesson(user_id, **fields)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("vocab_word_practice"), F.text)
async def vocab_word_practice(m: Message):
    """2 правильных предложения → слово засчитывается, кнопка убирается."""
    text = (m.text or "").strip()
    if text in {"⬅️ К словам", "🔙 Вернуться в меню", BTN_LEARN_PHRASES, "⬅️ К темам", "⬅️ К теме (слова)"}:
        raise SkipHandler
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    lesson = user["lesson"]
    level = lesson["level"]
    topic_id = lesson["vocab_topic_id"]
    active = lesson.get("vocab_active_item")
    done = int(lesson.get("vocab_practice_done") or 0)
    word = get_word_entry(level, topic_id, active) if active else None
    if not word:
        await _send_word_story(m, user, count_toward_limit=False)
        return

    if _is_repeat_sentence(lesson, text):
        await m.reply(
            "🦜 Это уже было. Напиши <b>другое</b> предложение — не копируй прошлое.",
            reply_markup=vocab_practice_kb(),
            parse_mode="HTML",
        )
        return

    result = check_vocab_sentence(level, word["en"], text)
    if not result.get("correct"):
        _remember_sentence(str(m.from_user.id), text)
        await m.reply(_vocab_check_reply(result), reply_markup=vocab_practice_kb(), parse_mode="HTML")
        return

    done += 1
    _remember_sentence(str(m.from_user.id), text, done=done)
    if done < 2:
        await m.reply(
            f"✅ Молодец! ({done}/2)\n"
            "Теперь напиши <b>ещё одно новое</b> предложение с этим словом "
            "(не повторяй предыдущее).",
            reply_markup=vocab_practice_kb(),
            parse_mode="HTML",
        )
        return

    finish_word_practice(str(m.from_user.id), level, topic_id, word["en"])
    from services.growth import note_word_learned, ensure_growth

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    wrap = note_word_learned(user)
    save_users(users)

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    wl, wt, _, _, _ = _topic_progress(user, level, topic_id)
    batch = list((user.get("lesson") or {}).get("vocab_batch") or [])
    # убрать уже изученные на всякий случай
    batch = [w for w in batch if not is_word_learned(user, level, topic_id, w)]

    await m.reply(
        f"✅ Отлично! Слово <b>{word['en']}</b> изучено! "
        f"Прогресс по теме: <b>{wl}/{wt}</b>\n{wrap}",
        parse_mode="HTML",
    )
    if batch:
        update_vocab_lesson(str(m.from_user.id), vocab_batch=batch, hub="vocab_topic")
        story_en = (user.get("lesson") or {}).get("vocab_text_en") or ""
        tip = f"Осталось в этом тексте: <b>{len(batch)}</b> — выбери следующее слово 👇"
        if story_en:
            tip = f"{tip}\n\n<i>Текст тот же — можно опереться на него.</i>"
        await m.reply(
            tip,
            reply_markup=vocab_topic_kb(level, topic_id, user, batch),
            parse_mode="HTML",
        )
    else:
        await m.reply("Все слова из этого текста изучены ✅")
        await _send_word_story(m, user, count_toward_limit=True)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("vocab_phrases", "vocab_phrase_practice"), F.text)
async def vocab_phrase_flow(m: Message):
    text = _strip_mark(m.text or "")
    nav = {BTN_LEARN_PHRASES, "⬅️ К темам", "⬅️ К теме (слова)", "🔙 Вернуться в меню", "⬅️ К словам"}
    if text in nav or (m.text or "").startswith("⬅️"):
        # Навигацию отдают dedicated-хендлерам (К темам / К словам / меню).
        raise SkipHandler

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    lesson = user["lesson"]
    level = lesson["level"]
    topic_id = lesson["vocab_topic_id"]
    topic_title = lesson.get("vocab_topic_title") or ""
    hub = lesson.get("hub")

    phrase = None
    # Подбирать фразу кнопкой только на экране выбора, не во время практики.
    if hub == "vocab_phrases":
        for p in get_phrases(level, topic_id):
            if p["en"].lower() == text.lower():
                phrase = p
                break
            short = p["en"] if len(p["en"]) <= 40 else p["en"][:37] + "..."
            if text == short or (m.text or "").replace("✅ ", "") == short:
                phrase = p
                break

    if hub == "vocab_phrases" and phrase:
        update_vocab_lesson(
            str(m.from_user.id),
            hub="vocab_phrase_practice",
            vocab_active_item=phrase["en"],
            vocab_practice_done=0,
            vocab_practice_step=0,
            vocab_last_sentence="",
            vocab_used_sentences=[],
        )
        await m.reply(rico_phrase_card(level, topic_title, phrase), reply_markup=vocab_practice_kb(), parse_mode="HTML")
        return

    if hub != "vocab_phrase_practice":
        batch = lesson.get("vocab_batch") or []
        await m.reply("Выбери фразу кнопкой.", reply_markup=vocab_phrase_topic_kb(level, topic_id, user, batch))
        return

    active = lesson.get("vocab_active_item")
    phrase = get_phrase_entry(level, topic_id, active) if active else None
    if not phrase:
        await _send_phrase_story(m, user, count_toward_limit=False)
        return

    done = int(lesson.get("vocab_practice_done") or 0)
    raw = (m.text or "").strip()
    if _is_repeat_sentence(lesson, raw):
        await m.reply(
            "🦜 Это уже было. Напиши <b>другое</b> предложение — не копируй прошлое.",
            reply_markup=vocab_practice_kb(),
            parse_mode="HTML",
        )
        return

    result = check_vocab_sentence(level, phrase["en"], raw, is_phrase=True)
    if not result.get("correct"):
        _remember_sentence(str(m.from_user.id), raw)
        await m.reply(_vocab_check_reply(result), reply_markup=vocab_practice_kb(), parse_mode="HTML")
        return

    done += 1
    _remember_sentence(str(m.from_user.id), raw, done=done)
    if done < 2:
        await m.reply(
            f"✅ Молодец! ({done}/2)\n"
            "Теперь напиши <b>ещё одно новое</b> предложение с этой фразой.",
            reply_markup=vocab_practice_kb(),
            parse_mode="HTML",
        )
        return

    finish_phrase_practice(str(m.from_user.id), level, topic_id, phrase["en"])
    from services.growth import note_phrase_learned, ensure_growth

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    ensure_growth(user)
    wrap = note_phrase_learned(user)
    save_users(users)

    users = load_users()
    user = get_user(users, str(m.from_user.id))
    pt = phrases_total(level, topic_id)
    pl, _, _ = topic_phrases_progress(user, level, topic_id, pt)
    batch = list((user.get("lesson") or {}).get("vocab_batch") or [])
    batch = [p for p in batch if not is_phrase_learned(user, level, topic_id, p)]

    await m.reply(
        f"✅ Фраза изучена! Прогресс: <b>{pl}/{pt}</b>\n{wrap}",
        parse_mode="HTML",
    )
    if batch:
        update_vocab_lesson(str(m.from_user.id), vocab_batch=batch, hub="vocab_phrases")
        await m.reply(
            f"Осталось фраз в тексте: <b>{len(batch)}</b> 👇",
            reply_markup=vocab_phrase_topic_kb(level, topic_id, user, batch),
            parse_mode="HTML",
        )
    else:
        await m.reply("Все фразы из этого текста изучены ✅")
        await _send_phrase_story(m, user, count_toward_limit=True)


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_ALL_LEVELS)
async def global_tasks_menu(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    if not user.get("assessment_done") and not user.get("dev_unlock"):
        await m.reply("Сначала пройди тест уровня.")
        return
    set_vocab_hub(str(m.from_user.id), "global_drill_menu")
    await m.reply(
        "🦜 <b>Решили закрепить результат?</b> Выбери задание:",
        reply_markup=global_drill_menu_kb(),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_REPEAT_WORDS)
async def start_word_drill(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    entries = get_all_learned_word_entries(user)
    if not entries:
        await m.reply("🦜 Пока нет изученных слов.", reply_markup=global_drill_menu_kb())
        return
    random.shuffle(entries)
    set_vocab_hub(
        str(m.from_user.id),
        "vocab_drill",
        drill_kind="words",
        drill_queue=entries,
        drill_index=0,
        drill_dirs=[],
    )
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await _send_drill_question(m, user)


@router.message(ModeFilter(MODE_LESSONS), F.text == BTN_REPEAT_PHRASES)
async def start_phrase_drill(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    entries = get_all_learned_phrase_entries(user)
    if not entries:
        await m.reply("🦜 Пока нет изученных фраз.", reply_markup=global_drill_menu_kb())
        return
    random.shuffle(entries)
    set_vocab_hub(
        str(m.from_user.id),
        "vocab_drill",
        drill_kind="phrases",
        drill_queue=entries,
        drill_index=0,
        drill_dirs=[],
    )
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await _send_drill_question(m, user)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("vocab_drill"), F.text == BTN_DONT_REMEMBER)
async def drill_dont_remember(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    cur = (user.get("lesson") or {}).get("drill_current") or {}
    entry = cur.get("entry")
    is_phr = cur.get("kind") == "phrases"
    if entry:
        await m.reply(rico_dont_remember(entry, is_phrase=is_phr), parse_mode="HTML")
    # Сразу следующее задание (слово или фраза)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await _send_drill_question(m, user)


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("vocab_drill"), F.text == BTN_BACK_DRILL)
async def drill_back(m: Message):
    clear_vocab_session(str(m.from_user.id))
    set_vocab_hub(str(m.from_user.id), "global_drill_menu")
    await m.reply("Выбери задание:", reply_markup=global_drill_menu_kb())


@router.message(ModeFilter(MODE_LESSONS), LessonHubFilter("vocab_drill"), F.text)
async def drill_answer(m: Message):
    if m.text in {BTN_DONT_REMEMBER, BTN_BACK_DRILL, "🔙 Вернуться в меню"}:
        raise SkipHandler
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    cur = (user.get("lesson") or {}).get("drill_current") or {}
    ans = (cur.get("answer") or "").strip().lower()
    given = (m.text or "").strip().lower()
    entry = cur.get("entry") or {}
    is_phr = cur.get("kind") == "phrases"
    if given == ans or (ans and (ans in given or given in ans)):
        await m.reply("✅ Верно!")
    else:
        if entry:
            await m.reply(rico_dont_remember(entry, is_phrase=is_phr), parse_mode="HTML")
        else:
            await m.reply(f"🦜 Почти! Правильно: <b>{cur.get('answer')}</b>", parse_mode="HTML")
    # Сразу следующее задание
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await _send_drill_question(m, user)


@router.message(ModeFilter(MODE_LESSONS), F.text.in_({"⬅️ К словам", "⬅️ К теме (слова)"}))
async def vocab_back_to_words(m: Message):
    """Вернуться к списку слов текущей темы (из практики или фраз)."""
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    hub = (user.get("lesson") or {}).get("hub") or ""
    if not hub.startswith("vocab"):
        raise SkipHandler
    lesson = user.get("lesson") or {}
    level = lesson.get("level") or "A1"
    topic_id = lesson.get("vocab_topic_id")
    if not topic_id:
        raise SkipHandler

    was_phrases = lesson.get("vocab_mode") == "phrases"
    batch = list(lesson.get("vocab_batch") or [])
    batch_are_words = bool(batch) and all(get_word_entry(level, topic_id, w) for w in batch)
    text_en = lesson.get("vocab_text_en") or ""
    text_ru = lesson.get("vocab_text_ru") or ""

    update_vocab_lesson(
        str(m.from_user.id),
        hub="vocab_topic",
        vocab_active_item=None,
        vocab_practice_step=0,
        vocab_mode="words",
    )

    if was_phrases or not batch_are_words:
        users = load_users()
        user = get_user(users, str(m.from_user.id))
        await _send_word_story(m, user, count_toward_limit=True)
        return

    batch = [w for w in batch if not is_word_learned(user, level, topic_id, w)] or batch
    update_vocab_lesson(str(m.from_user.id), vocab_batch=batch)
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    topic = get_vocab_topic(level, topic_id) or {"title": lesson.get("vocab_topic_title") or "Vocabulary"}
    prog = topic_progress_line(user, level, topic_id)
    if text_en:
        body = (
            f"📗 <b>{topic['title']}</b>\n"
            f"{prog}\n\n"
            f"{text_en}\n\n"
            f"<i>{text_ru}</i>\n\n"
            "Выбери слово 👇"
        )
    else:
        body = f"📗 <b>{topic['title']}</b>\n{prog}\n\nВыбери слово 👇"
    await m.reply(body, reply_markup=vocab_topic_kb(level, topic_id, user, batch), parse_mode="HTML")


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К темам")
async def vocab_back_to_topics(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    hub = (user.get("lesson") or {}).get("hub") or ""
    if not hub.startswith("vocab"):
        raise SkipHandler
    level = user["lesson"].get("level") or "A1"
    clear_vocab_session(str(m.from_user.id))
    set_vocab_hub(str(m.from_user.id), "vocab_list", level=level)
    users = load_users()
    user = get_user(users, str(m.from_user.id))

    def prog(lv, tid):
        wt = words_total(lv, tid)
        pt = phrases_total(lv, tid)
        wl, _, _ = topic_words_progress(user, lv, tid, wt)
        pl, _, _ = topic_phrases_progress(user, lv, tid, pt)
        done = (wt > 0 and wl >= wt) and (pt == 0 or pl >= pt)
        return wl, wt, done

    await m.reply(
        format_vocab_topics_list(level, prog),
        reply_markup=vocab_topics_kb(level, user),
        parse_mode="HTML",
    )


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К разделам")
async def vocab_back_sections(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    hub = (user.get("lesson") or {}).get("hub") or ""
    if not (hub.startswith("vocab") or hub in {"global_drill_menu", "vocab_drill"}):
        raise SkipHandler
    from services.lesson_state import set_level_hub

    level = user["lesson"].get("level") or user.get("level") or "A1"
    clear_vocab_session(str(m.from_user.id))
    set_level_hub(str(m.from_user.id), level)
    await m.reply(f"🎓 Уровень {level} — выбери раздел:", reply_markup=level_sections_kb())


@router.message(ModeFilter(MODE_LESSONS), F.text == "⬅️ К уровням")
async def vocab_drill_back_levels(m: Message):
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    hub = (user.get("lesson") or {}).get("hub") or ""
    if hub not in {"global_drill_menu", "vocab_drill"}:
        raise SkipHandler
    from handlers.lessons import lessons_keyboard_for
    from services.lesson_state import clear_lesson

    clear_vocab_session(str(m.from_user.id))
    clear_lesson(str(m.from_user.id))
    users = load_users()
    user = get_user(users, str(m.from_user.id))
    await m.reply("Выбери уровень:", reply_markup=lessons_keyboard_for(user))
