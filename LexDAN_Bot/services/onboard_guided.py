"""
Направляемый онбординг (пока только имитация /imit_start).

Стадии:
  daily_fire  — тур по 4 разделам Огня дня
  grammar_cta — CTA «Начать» → тема to be
  slides      — интерактивные слайды + Уточнить
  tasks_menu  — экран заданий, кнопка «Начать»
  tasks       — задания 1→8 подряд
  done        — путь завершён
"""

from __future__ import annotations

import re
from typing import Any

ONBOARD_TOPIC_LEVEL = "A0"
ONBOARD_TOPIC_ID = "pronouns_be"
ONBOARD_TOPIC_TITLE = "I / You + to be / Я есть…"

BTN_ONBOARD_START_TASKS = "✅ Начать"
BTN_NAVIGATION = "🗺 Навигация"

PRAISE_OK = [
    "✅ Молодец! 💪",
    "✅ Так держать! 🔥",
    "✅ Вот это темп! ⚡",
    "✅ Красава! 🦜",
    "✅ Супер! Идём дальше ✨",
    "✅ Отлично! Ты в ударе 💚",
    "✅ Йес! Правильно 🙌",
    "✅ Класс! Продолжаем 🚀",
]

DF_TOUR_HTML = ""  # тур-текст отключён по сценарию


DF_DONE_HTML = (
    "🦜 <b>Рико:</b> Отлично, так держать! 👏\n\n"
    "Возьми себе в привычку заходить сюда <b>каждый день</b> и изучать "
    "новые и необычные слова и фразы — ну и конечно же тренировать слух 🎧\n\n"
    "А чтобы непосредственно учить правила и практиковаться, есть раздел "
    "<b>📚 Уроки</b>.\n"
    "Предлагаю пройти первую тему по грамматике, чтобы ты понял, как работает бот, "
    "и убедился в качестве контента:\n\n"
    f"<b>{ONBOARD_TOPIC_TITLE}</b>"
)

SLIDES: list[str] = [
    (
        "🦜 <b>Рико:</b> А теперь — легендарный глагол <b>to be</b> (быть)!\n"
        "Без него в английском почти никуда: ни представиться, ни сказать "
        "«я студент», ни спросить «ты дома?»."
    ),
    (
        "Смотри, как он работает <b>сейчас</b>, в настоящем:\n"
        "<b>I am, you are, he/she/it is, we/you/they are.</b>\n\n"
        "Пример:\n"
        "• I am Danil — <i>Я Данил / Меня зовут Данил.</i>\n"
        "• She is a student — <i>Она студентка.</i>\n"
        "• They are friends — <i>Они друзья.</i>"
    ),
    (
        "В вопросе порядок меняется: <b>Are you OK?</b> — <i>Ты в порядке?</i>\n"
        "А после <b>he/she/it</b> всегда <b>is</b>, не are — это частая ошибка!"
    ),
    (
        "Формулы <b>to be</b> сейчас:\n"
        "<b>I am, you are, he/she/it is, we/you/they are.</b>\n\n"
        "Отрицание: <b>I'm not, isn't, aren't.</b>\n"
        "Вопрос: <b>Am I…? Is she…? Are you…?</b>\n"
        "Порядок в вопросе меняется — глагол впереди!"
    ),
    (
        "Дальше будут задания — там есть кнопка <b>🌍 Перевести</b>, "
        "если не понимаешь слова в предложении. Я помогу 💪"
    ),
]

TASKS_OVERVIEW_HTML = (
    "📝 <b>Задания по теме</b>\n\n"
    "Сложность растёт от 1 к 8:\n\n"
    "✅ Задание 1 — Выбор правильного ответа\n"
    "✅ Задание 2 — Выбор правильного ответа\n"
    "✅ Задание 3 — Выбор правильного ответа\n"
    "✅ Задание 4 — Напиши форму слова\n"
    "✅ Задание 5 — Напиши форму слова\n"
    "✅ Задание 6 — Напиши форму слова\n"
    "✅ Задание 7 — Перевод: русский → английский\n"
    "✅ Задание 8 — Перевод: английский → русский\n\n"
    "🦜 <b>8 заданий на тему:</b>\n"
    "1–3 — выбор кнопкой · 4–6 — напиши форму слова · 7 — RU→EN · 8 — EN→RU\n"
    "В переводах можно спросить «как переводится слово …».\n"
    "Все 8 заданий → тема с ✅. Все темы → откроется тест по Grammar."
)

PATH_DONE_HTML = (
    "🦜 <b>Рико:</b> Отлично — вот ты и вошёл в русло и понимаешь, что к чему! 💚\n\n"
    "У нас ещё много разделов с разными навыками — можешь исследовать их "
    "по ходу обучения.\n\n"
    "А пока отправляю тебя в <b>главное меню</b> — оттуда уже выбирай, "
    "чем займёшься.\n"
    "В профиле есть кнопка <b>🗺 Навигация</b>: она покажет, за что отвечает "
    "каждый раздел."
)


def _blank() -> dict[str, Any]:
    return {
        "active": False,
        "imit": False,
        "stage": "",
        "slide": 0,
        "awaiting_clarify": False,
        "df_intro_sent": False,
        "df_done_sent": False,
        "slide_msg_id": None,
        "slide_chat_id": None,
        "clarify_ids": [],
    }


def ensure_onboard(user: dict) -> dict:
    ob = user.get("onboard")
    if not isinstance(ob, dict):
        ob = _blank()
        user["onboard"] = ob
    for k, v in _blank().items():
        ob.setdefault(k, v)
    return ob


def is_guided_onboard(user: dict) -> bool:
    """Спец-флоу после теста: Огонь дня → to be → задания."""
    ob = ensure_onboard(user)
    if not ob.get("active"):
        return False
    return onboard_stage(user) in {
        "daily_fire",
        "grammar_cta",
        "slides",
        "tasks_menu",
        "tasks",
    }


def is_imit_onboard(user: dict) -> bool:
    return bool(ensure_onboard(user).get("imit"))


def is_imit_active(user: dict) -> bool:
    """Любая стадия полной имитации (включая привет / имя / тест)."""
    ob = ensure_onboard(user)
    return bool(ob.get("active") and ob.get("imit"))


def onboard_stage(user: dict) -> str:
    return str(ensure_onboard(user).get("stage") or "")


def advance_imit_after_test(user: dict) -> None:
    """После вступительного теста → стадия Огня дня."""
    from services.daily_fire import KINDS, ensure_daily_fire

    ob = ensure_onboard(user)
    if not (ob.get("active") and ob.get("imit")):
        return
    ob["stage"] = "daily_fire"
    ob["slide"] = 0
    ob["awaiting_clarify"] = False
    ob["df_intro_sent"] = False
    ob["df_done_sent"] = False
    df = ensure_daily_fire(user)
    df["opened"] = {k: False for k in KINDS}
    df["celebrated"] = False
    df["cache"] = {}


def start_imit_onboard(user: dict) -> None:
    """Полная имитация онбординга с нуля: привет → имя → тест → огонь → to be."""
    from services.daily_fire import KINDS, ensure_daily_fire
    from services.growth import ensure_growth
    from services.lesson_state import ensure_progress, progress_key

    ensure_growth(user)
    ensure_progress(user)

    # Бэкап, чтобы /imit_finish вернул профиль
    user["onboard_imit_backup"] = {
        "name": user.get("name") or "",
        "pending_name": user.get("pending_name") or "",
        "assessment_done": bool(user.get("assessment_done")),
        "level": user.get("level") or "A0",
        "grammar_unlock_ceiling": user.get("grammar_unlock_ceiling") or "A0",
        "step": user.get("step") or "ready",
        "dev_unlock": bool(user.get("dev_unlock")),
        "reg_full_trial_granted": bool(user.get("reg_full_trial_granted")),
    }

    ob = ensure_onboard(user)
    ob.update(
        {
            "active": True,
            "imit": True,
            "stage": "intro",
            "slide": 0,
            "awaiting_clarify": False,
            "df_intro_sent": False,
            "df_done_sent": False,
        }
    )

    df = ensure_daily_fire(user)
    df["opened"] = {k: False for k in KINDS}
    df["celebrated"] = False
    df["cache"] = {}

    key = progress_key(ONBOARD_TOPIC_LEVEL, ONBOARD_TOPIC_ID)
    ce = user["grammar_progress"].setdefault("completed_exercises", {})
    ce.pop(key, None)
    topics = list(user["grammar_progress"].get("completed_topics") or [])
    user["grammar_progress"]["completed_topics"] = [t for t in topics if t != key]

    # Как новый пользователь
    user["name"] = ""
    user["pending_name"] = ""
    user["assessment_done"] = False
    user["assessment"] = {}
    user["dev_unlock"] = False
    user["rules_accepted"] = True
    user["step"] = "awaiting_onboard_cta"
    user["level"] = "A0"
    user["grammar_unlock_ceiling"] = "A0"
    # чтобы подарок после теста снова выдался в имитации
    user["reg_full_trial_granted"] = False


def finish_imit_onboard(user: dict) -> None:
    """Выключить имитацию и вернуть бэкап профиля."""
    bak = user.pop("onboard_imit_backup", None) or {}
    ob = ensure_onboard(user)
    ob.update(_blank())

    if bak:
        if bak.get("name"):
            user["name"] = bak["name"]
        user["pending_name"] = bak.get("pending_name") or ""
        user["assessment_done"] = bool(bak.get("assessment_done"))
        if bak.get("level"):
            user["level"] = bak["level"]
        if bak.get("grammar_unlock_ceiling"):
            user["grammar_unlock_ceiling"] = bak["grammar_unlock_ceiling"]
        user["step"] = bak.get("step") or "ready"
        user["dev_unlock"] = bool(bak.get("dev_unlock"))
        user["reg_full_trial_granted"] = bool(bak.get("reg_full_trial_granted"))


def complete_guided_path(user: dict) -> None:
    """Путь пройден — обычный режим бота; imit-маркер до /imit_finish."""
    ob = ensure_onboard(user)
    was_imit = bool(ob.get("imit"))
    ob.update(_blank())
    if was_imit:
        ob["imit"] = True
        ob["stage"] = "done"


def plain_for_tts(html: str) -> str:
    t = re.sub(r"<[^>]+>", " ", html or "")
    t = re.sub(r"\s+", " ", t).strip()
    return t[:450]


def praise_ok(index: int | None = None) -> str:
    import random

    if index is None:
        return random.choice(PRAISE_OK)
    return PRAISE_OK[int(index) % len(PRAISE_OK)]


def clarify_rico(question: str, user_name: str = "друг") -> str:
    """Ответ Рико строго по теме to be — коротко, по-человечески, без голоса."""
    from services.gpt import chat_completion
    import logging

    fallback = (
        "🦜 Коротко: сейчас — I am / you are / he-she-it is / we-you-they are. "
        "Спроси ещё раз чуть конкретнее — разберём на примере."
    )
    try:
        text = chat_completion(
            [
                {
                    "role": "system",
                    "content": (
                        "Ты попугай Рико 🦜 — живой репетитор. "
                        "Отвечай ТОЛЬКО по Present Simple of to be "
                        "(I am / you are / he-she-it is / we-you-they are, "
                        "отрицания, вопросы). Не уходи в другие темы. "
                        "По-русски, 2–4 коротких предложения максимум. "
                        "Один короткий EN-пример + перевод <i>…</i>. "
                        "Без воды, без длинных списков, как человек в чате. "
                        "HTML: только <b> и <i>."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Ученика зовут {user_name}. Уровень A0. "
                        f"Тема: {ONBOARD_TOPIC_TITLE}.\nВопрос: {question}"
                    ),
                },
            ],
            max_tokens=120,
            temperature=0.4,
            timeout=12,
        )
        if not text.startswith("🦜"):
            text = f"🦜 {text}"
        return text
    except Exception as e:
        logging.error("onboard clarify error: %s", e)
        return fallback
