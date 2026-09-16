"""
Направляемый онбординг для новых пользователей (и /imit_start).

Стадии:
  intro / pre_test — привет, имя, тест
  daily_fire  — одна искра Огня дня → урок
  grammar_cta — CTA «Начать» → тема to be
  slides      — интерактивные слайды + Уточнить
  tasks_menu  — экран заданий, кнопка «Начать»
  tasks       — задания 1→8 подряд
  done        — путь завершён
"""

from __future__ import annotations

import re
from typing import Any

from services.lesson_state import GRAMMAR_TASKS_OVERVIEW_HTML as TASKS_OVERVIEW_HTML

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
    "🦜 <b>Рико:</b> Класс, одну искру уже поймал! 🔥✨\n\n"
    "Остальные искры — после короткого знакомства с уроком.\n\n"
    "Давай попробуем тему <b>to be</b> — один слайд и одно задание 💚\n\n"
    "⚡ Сейчас короткий вариант: обычно темы объясняются подробнее. "
    "Полный разбор всегда можно пройти позже в <b>📚 Уроках</b>.\n\n"
    f"<b>{ONBOARD_TOPIC_TITLE}</b>"
)

SLIDES: list[str] = [
    (
        "🦜 <b>Рико:</b> Легендарный глагол <b>to be</b> (быть)!\n"
        "Без него ни представиться, ни сказать «я студент».\n\n"
        "⚡ <i>Это короткий вариант темы.</i> В уроках объяснения обычно длиннее "
        "и подробнее — туда можно вернуться позже.\n\n"
        "Сейчас: <b>I am · you are · he/she/it is · we/you/they are</b>\n\n"
        "• <b>I am Danil</b> — <i>Я Данил.</i>\n"
        "• <b>She is a student</b> — <i>Она студентка.</i>\n"
        "• <b>Are you OK?</b> — <i>Ты в порядке?</i>\n\n"
        "Дальше — одно короткое задание 💪"
    ),
]

PATH_DONE_HTML = (
    "🦜 <b>Рико:</b> Отлично — ты уже в русле и понимаешь, что к чему! 💚\n\n"
    "Уроки дальше так же: объяснение → задания. "
    "А чтобы язык ожил, загляни в <b>🗣️ Общаться</b> — "
    "там можно болтать со мной на любые темы.\n\n"
    "Завтра просто открой бота — я буду ждать. Так появляется привычка."
)

PATH_NAV_HTML = (
    "🗺 <b>Куда жать из меню</b>\n\n"
    "🗣️ <b>Общаться</b> — живой чат с Рико на любые темы\n"
    "📚 <b>Уроки</b> — грамматика, слова, слух, чтение\n"
    "🔥 <b>Огонь дня</b> — ежедневная порция\n"
    "📊 <b>Профиль</b> — подписка, стрик, карта разделов\n\n"
    "Полная карта всегда в профиле: кнопка <b>🗺 Навигация</b>."
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
        "stage_at": 0.0,
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


def is_onboard_locked(user: dict) -> bool:
    """Сценарий знакомства идёт — меню закрыто (и живой путь, и имитация)."""
    ob = ensure_onboard(user)
    if not ob.get("active"):
        return False
    return onboard_stage(user) not in {"", "done"}


def onboard_stage(user: dict) -> str:
    return str(ensure_onboard(user).get("stage") or "")


def set_onboard_stage(user: dict, stage: str) -> None:
    """Сменить стадию и сбросить таймер «застрял с …» для drip-уведомлений."""
    import time

    ob = ensure_onboard(user)
    prev = str(ob.get("stage") or "")
    ob["stage"] = stage
    if prev != stage or not ob.get("stage_at"):
        ob["stage_at"] = time.time()


def path_channel_html() -> str:
    from config import CHANNEL_URL, CHANNEL_USERNAME

    channel = CHANNEL_URL or f"https://t.me/{CHANNEL_USERNAME}"
    return (
        "📣 Если хочешь следить за обновлениями бота — можно подписаться "
        f"на канал <b>@{CHANNEL_USERNAME}</b>: {channel}"
    )


def ensure_live_onboard(user: dict) -> None:
    """Включить направляемый путь для нового пользователя (без сброса профиля)."""
    import time

    ob = ensure_onboard(user)
    if ob.get("active") or ob.get("stage") == "done":
        return
    if user.get("assessment_done"):
        return
    prev = str(ob.get("stage") or "")
    ob.update(
        {
            "active": True,
            "imit": bool(ob.get("imit")),
            "stage": ob.get("stage") or "intro",
            "slide": 0,
            "awaiting_clarify": False,
            "df_intro_sent": False,
            "df_done_sent": False,
        }
    )
    if prev != str(ob.get("stage") or "") or not ob.get("stage_at"):
        ob["stage_at"] = time.time()


def advance_imit_after_test(user: dict) -> None:
    """После вступительного теста → стадия Огня дня."""
    from services.daily_fire import KINDS, ensure_daily_fire

    ob = ensure_onboard(user)
    if not ob.get("active"):
        return
    set_onboard_stage(user, "daily_fire")
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
    import time

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
            "stage_at": time.time(),
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
    set_onboard_stage(user, "done")
    if was_imit:
        ob["imit"] = True


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
    """Ответ Рико на вопрос ученика — по делу, без голоса."""
    from services.gpt import chat_completion
    import logging

    fallback = (
        "🦜 Скажи ещё раз, что именно хочешь сказать по-английски — "
        "дам готовую фразу и коротко почему так."
    )
    try:
        text = chat_completion(
            [
                {
                    "role": "system",
                    "content": (
                        "Ты попугай Рико 🦜. Отвечай на ТО, что спросил ученик.\n"
                        "«Как будет …» = переведи его фразу, не выдумывай вопрос/отрицание.\n"
                        "Пример: «как будет он ест бургер» → "
                        "<b>He eats a burger</b> — <i>Он ест бургер.</i> "
                        "Если уместно, одним предложением: "
                        "прямо сейчас — <b>He is eating a burger</b>.\n"
                        "НЕЛЬЗЯ: Is he eating…? / He is not eating… / He is a student.\n"
                        "Тема урока to be — используй am/is/are только если это нужно для ЕГО фразы.\n"
                        "2–4 коротких предложения. HTML: только <b> и <i>."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Ученика зовут {user_name}. Уровень A0. "
                        f"Тема урока: {ONBOARD_TOPIC_TITLE}.\n"
                        f"Вопрос ученика: {question}"
                    ),
                },
            ],
            max_tokens=180,
            temperature=0.2,
            timeout=12,
        )
        if not text.startswith("🦜"):
            text = f"🦜 {text}"
        return text
    except Exception as e:
        logging.error("onboard clarify error: %s", e)
        return fallback
