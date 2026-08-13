"""🔥 Огонь дня — хаб в главном меню."""

from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from handlers.filters import ModeFilter
from handlers.keyboards import main_menu
from services.database import (
    MODE_DAILY_FIRE,
    MODE_MENU,
    MODE_LESSONS,
    users_for,
    get_user,
    save_users,
    set_mode,
)
from services.growth import ensure_growth, note_lesson_activity
from services.daily_fire import (
    BTN_DAILY_FIRE,
    BTN_DF_WORD,
    BTN_DF_PHRASE,
    BTN_DF_VOICE,
    BTN_DF_FACT,
    BTN_DF_BACK,
    BTN_TO_KIND,
    ensure_daily_fire,
    is_opened,
    mark_opened,
    hub_intro,
    get_or_create_content,
    format_word_or_phrase,
    format_voice,
    format_fact,
    tts_parts_for,
    pick_practice_offer,
    format_ritual_done,
    should_celebrate_ritual,
    mark_ritual_celebrated,
)
from services.elevenlabs import send_rico_voice
from data.assessment_data import is_level_accessible_for_user

router = Router()

BTN_BACK_MENU = "🔙 Вернуться в меню"


def daily_fire_kb(user: dict) -> ReplyKeyboardMarkup:
    ensure_daily_fire(user)

    def mark(btn: str, kind: str) -> str:
        return f"✅ {btn}" if is_opened(user, kind) else btn

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=mark(BTN_DF_WORD, "word")), KeyboardButton(text=mark(BTN_DF_PHRASE, "phrase"))],
            [KeyboardButton(text=mark(BTN_DF_VOICE, "voice")), KeyboardButton(text=mark(BTN_DF_FACT, "fact"))],
            [KeyboardButton(text=BTN_BACK_MENU)],
        ],
        resize_keyboard=True,
    )


def _offer_kb(offer: dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=offer.get("label") or "Перейти →", callback_data=offer["cb"])]
        ]
    )


def _kind_from_text(text: str) -> str | None:
    t = (text or "").strip()
    if t.startswith("✅ "):
        t = t[2:].strip()
    return BTN_TO_KIND.get(t)


def _uid(m: Message | CallbackQuery) -> str:
    return str(m.from_user.id)


async def _maybe_celebrate(m: Message, user: dict, users: dict, uid: str) -> None:
    from services.onboard_guided import is_guided_onboard
    from handlers.onboard_guided import maybe_send_df_done_cta

    # Направляемый онбординг: своё сообщение + CTA на to be
    if await maybe_send_df_done_cta(m, user, users, uid):
        return

    if not should_celebrate_ritual(user):
        return
    if is_guided_onboard(user):
        return
    offer = pick_practice_offer(user)
    mark_ritual_celebrated(user)
    user["daily_fire_offer"] = {
        "section": offer.get("section"),
        "level": offer.get("level"),
        "target_id": offer.get("target_id") or "",
        "title": offer.get("title") or "",
        "cb": offer.get("cb") or "",
    }
    save_users(users, only=uid)
    await m.answer(
        format_ritual_done(offer),
        reply_markup=_offer_kb(offer),
        parse_mode="HTML",
    )


@router.message(F.text == BTN_DAILY_FIRE)
async def open_daily_fire(m: Message):
    uid = _uid(m)
    set_mode(uid, MODE_DAILY_FIRE)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    note_lesson_activity(user)
    ensure_daily_fire(user)
    save_users(users, only=uid)
    await m.answer(hub_intro(user), reply_markup=daily_fire_kb(user), parse_mode="HTML")
    from handlers.onboard_guided import send_df_tour_intro

    users = users_for(uid)
    user = get_user(users, uid)
    await send_df_tour_intro(m, user)
    save_users(users, only=uid)


@router.message(ModeFilter(MODE_DAILY_FIRE), F.text == BTN_DF_BACK)
async def back_to_fire_hub(m: Message):
    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    await m.answer(hub_intro(user), reply_markup=daily_fire_kb(user), parse_mode="HTML")


@router.message(ModeFilter(MODE_DAILY_FIRE), F.text == BTN_BACK_MENU)
async def leave_daily_fire(m: Message):
    uid = _uid(m)
    set_mode(uid, MODE_MENU)
    users = users_for(uid)
    user = get_user(users, uid)
    await m.answer("Главное меню:", reply_markup=main_menu(user))


@router.message(ModeFilter(MODE_DAILY_FIRE))
async def daily_fire_item(m: Message):
    if not m.text or m.text.startswith("/"):
        return
    kind = _kind_from_text(m.text)
    if not kind:
        uid = _uid(m)
        users = users_for(uid)
        user = get_user(users, uid)
        await m.answer(
            "Выбери одну из четырёх кнопок огня дня 👇",
            reply_markup=daily_fire_kb(user),
        )
        return

    uid = _uid(m)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)
    note_lesson_activity(user)
    first_open = not is_opened(user, kind)

    await m.answer("🦜 Рико колдует контент… секунду ✨", parse_mode="HTML")

    data = get_or_create_content(user, kind)
    if first_open:
        mark_opened(user, kind)
    save_users(users, only=uid)

    if kind in {"word", "phrase"}:
        text = format_word_or_phrase(kind, data, first_open=first_open)
    elif kind == "voice":
        text = format_voice(data, first_open=first_open)
    else:
        text = format_fact(data, first_open=first_open)

    # Все аудио в огне дня — только голос Рико
    tts_parts = tts_parts_for(kind, data)
    await m.answer(text, reply_markup=daily_fire_kb(user), parse_mode="HTML")
    for chunk in tts_parts:
        await send_rico_voice(m, chunk, user=user, title="Огонь дня · Rico")

    if first_open:
        users = users_for(uid)
        user = get_user(users, uid)
        await _maybe_celebrate(m, user, users, uid)


@router.callback_query(F.data.startswith("dfgo:"))
async def daily_fire_go(cq: CallbackQuery):
    uid = str(cq.from_user.id)
    users = users_for(uid)
    user = get_user(users, uid)
    ensure_growth(user)

    parts = (cq.data or "").split(":", 3)
    if len(parts) < 4:
        await cq.answer("Ссылка устарела", show_alert=True)
        return
    _, sec, level, raw_idx = parts
    topic_index: int | None
    if raw_idx in {"_", ""}:
        topic_index = None
    else:
        try:
            topic_index = int(raw_idx)
        except ValueError:
            topic_index = None

    if not is_level_accessible_for_user(user, level):
        await cq.answer("Этот уровень ещё закрыт 🔒", show_alert=True)
        return

    await cq.answer()
    set_mode(uid, MODE_LESSONS)
    m = cq.message
    if m is None:
        return

    try:
        if sec == "g":
            await _go_grammar(m, uid, user, level, topic_index)
        elif sec == "v":
            await _go_vocab(m, uid, user, level, topic_index)
        elif sec == "l":
            await _go_listening(m, uid, user, level, topic_index)
        else:
            await m.answer(
                "Не понял раздел — открой Уроки из меню 📚",
                reply_markup=main_menu(user),
            )
    except Exception as e:
        import logging

        logging.exception("daily_fire_go failed: %s", e)
        await m.answer(
            "Не удалось открыть раздел. Зайди через 📚 Уроки — там всё на месте.",
            reply_markup=main_menu(user),
        )


async def _go_grammar(m: Message, uid: str, user: dict, level: str, topic_index: int | None) -> None:
    from services.lesson_state import set_grammar_list, open_topic, assessment_busy, set_level_hub
    from data.grammar_curriculum import get_topics, is_ack_topic, format_topics_list
    from handlers.lesson_keyboards import grammar_topics_kb, topic_chat_kb, level_sections_kb
    from handlers.lessons_grammar import _completed_topic_ids
    from services.lesson_state import is_grammar_topic_done

    if assessment_busy(user):
        await m.answer("Сначала закончи тест уровня 🙂")
        return

    topics = get_topics(level) or []
    topic = None
    if topic_index is not None and 0 <= topic_index < len(topics):
        topic = topics[topic_index]
    if topic is None and topic_index is not None:
        for t in topics:
            if not is_grammar_topic_done(user, level, t):
                topic = t
                break

    if topic is None:
        set_level_hub(uid, level)
        set_grammar_list(uid, level)
        users = users_for(uid)
        user = get_user(users, uid)
        await m.answer(
            f"📘 Grammar · <b>{level}</b>\n\n" + format_topics_list(level, _completed_topic_ids(user, level)),
            reply_markup=grammar_topics_kb(level, user),
            parse_mode="HTML",
        )
        return

    set_grammar_list(uid, level)
    open_topic(uid, topic["id"], topic.get("title") or topic["id"])
    await m.answer(
        f"🦜 Переходим в Grammar · <b>{level}</b>\n\n" + (topic.get("rico_intro") or topic.get("title") or ""),
        reply_markup=topic_chat_kb(ack=is_ack_topic(topic)),
        parse_mode="HTML",
    )


async def _go_vocab(m: Message, uid: str, user: dict, level: str, topic_index: int | None) -> None:
    from services.lesson_state import assessment_busy
    from services.vocabulary_state import (
        set_vocab_hub,
        topic_words_progress,
        topic_phrases_progress,
        is_word_learned,
    )
    from data.vocabulary_curriculum import get_vocab_topics, format_vocab_topics_list
    from data.vocabulary_words import get_words, words_total
    from data.vocabulary_phrases import phrases_total
    from handlers.vocabulary_keyboards import vocab_topics_kb
    from data.vocabulary_words import has_vocabulary_level
    from handlers.lessons_vocabulary import _send_word_story, VOCAB_INTRO

    if assessment_busy(user):
        await m.answer("Сначала закончи тест уровня 🙂")
        return

    has_vocabulary_level(level)
    topics = get_vocab_topics(level) or []
    topic = None
    if topic_index is not None and 0 <= topic_index < len(topics):
        topic = topics[topic_index]
    if topic is None and topic_index is not None:
        for t in topics:
            words = get_words(level, t["id"]) or []
            if any(not is_word_learned(user, level, t["id"], w.get("en") or "") for w in words):
                topic = t
                break

    if topic is None:
        set_vocab_hub(uid, "vocab_list", level=level)
        users = users_for(uid)
        user = get_user(users, uid)

        def prog(lv, tid):
            wt = words_total(lv, tid)
            pt = phrases_total(lv, tid)
            wl, _, wd = topic_words_progress(user, lv, tid, wt)
            pl, _, pd = topic_phrases_progress(user, lv, tid, pt)
            return wl + pl, wt + pt, wd and (pt == 0 or pd)

        await m.answer(VOCAB_INTRO, parse_mode="HTML")
        await m.answer(
            format_vocab_topics_list(level, prog),
            reply_markup=vocab_topics_kb(level, user),
            parse_mode="HTML",
        )
        return

    set_vocab_hub(
        uid,
        "vocab_topic",
        level=level,
        vocab_topic_id=topic["id"],
        vocab_topic_title=topic.get("title") or topic["id"],
    )
    users = users_for(uid)
    user = get_user(users, uid)
    await m.answer(
        f"🦜 Переходим в Vocabulary · <b>{level}</b>\nТема: <b>{topic.get('title') or topic['id']}</b>",
        parse_mode="HTML",
    )
    await _send_word_story(m, user, count_toward_limit=True)


async def _go_listening(m: Message, uid: str, user: dict, level: str, topic_index: int | None) -> None:
    from services.listening_state import (
        set_listening_list,
        set_listening_hub,
        set_session,
        is_topic_done,
        can_start_listening,
        ensure_listening,
    )
    from data.listening_topics import topics_for_level
    from handlers.lessons_listening import (
        open_listening_for_level,
        listening_topics_kb,
        intro_kb,
        _roles_phrase,
    )
    from services.lesson_state import assessment_busy

    if assessment_busy(user):
        await m.answer("Сначала закончи тест уровня 🙂")
        return

    ensure_listening(user)
    topics = topics_for_level(level) or []
    topic = None
    if topic_index is not None and 0 <= topic_index < len(topics):
        topic = topics[topic_index]
    if topic is None and topic_index is not None:
        topic = next((t for t in topics if not is_topic_done(user, level, t["id"])), None)

    if topic is None:
        await open_listening_for_level(m, user, level)
        return

    already_done = is_topic_done(user, level, topic["id"])
    if not already_done:
        ok, limit_msg = can_start_listening(user)
        if not ok:
            set_listening_list(uid, level)
            users = users_for(uid)
            user = get_user(users, uid)
            await m.answer(
                limit_msg or "Лимит Listening на сегодня.",
                reply_markup=listening_topics_kb(level, user),
                parse_mode="HTML",
            )
            return

    roles = _roles_phrase(topic)
    set_listening_list(uid, level)
    set_session(
        uid,
        {
            "level": level,
            "topic_id": topic["id"],
            "topic_title": topic.get("title_ru") or topic.get("title") or topic["id"],
            "topic_roles": roles,
            "phase": "intro",
            "content": None,
            "slot_consumed": False,
        },
    )
    set_listening_hub(uid, "listening_play")
    await m.answer(
        f"🦜 Переходим в Listening · <b>{level}</b>\n"
        f"Тема: «{topic.get('title_ru') or topic.get('title')}».\n\n"
        f"Сейчас услышишь короткий диалог (<i>{roles}</i>).\n"
        "Нажми <b>Готов</b>, когда будешь готов(а).",
        reply_markup=intro_kb(),
        parse_mode="HTML",
    )
