"""
Онбординг-drip: пинги по факту «что сделал / где застрял», не по старому CSV.

Таймеры — часы с момента входа в стадию (stage_at) или first_seen.
Тихие часы МСК: 22:00–10:00 — не шлём.
Один drip-kind на юзера один раз; не чаще 1 уведомления в сутки (общий mark_sent).
"""

from __future__ import annotations

import time

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Часы «застрял в стадии» → можно слать (после тихих часов)
DRIP_HOURS = {
    "intro": 2.0,  # Start, нет имени
    "pre_test": 1.5,  # имя есть / pre_test, тест не закончен
    "daily_fire": 2.0,  # после теста, ещё не to be
    "to_be": 2.0,  # grammar_cta / slides / tasks
    "done_no_chat": 1.0,  # онбординг done, в чат не писал
    "chatted": 20.0,  # уже болтал — мягко вернуть на след. день
}

QUIET_START = 22  # включительно с 22
QUIET_END = 10  # до 10:00 не шлём

# Не пинговать, если был активен последние N минут (сидит в боте)
ACTIVE_GRACE_MIN = 25

CHANNEL_SOCIAL_KEY = "ad_social_proof_v1"
CHANNEL_POST_HTML = (
    "🦜 <b>Рико:</b> Уже <b>десятки людей</b> прошли тест уровня в LexDAN 🎯\n\n"
    "Кто-то только начал, кто-то уже поймал искру Огня дня "
    "и поболтал с Рико.\n\n"
    "💚 15 минут в день — без стресса, в своём темпе.\n\n"
    "👉 Проверь свой уровень:\n"
    "https://t.me/LexDAN_bot"
)

MSG = {
    "intro": (
        "🦜 <b>Рико:</b> Ты уже нажал Start — круто!\n\n"
        "Давай за <b>3–4 минуты</b> проверим уровень? "
        "После теста будет подарок: <b>3 дня безлимита</b> 🎁\n\n"
        "Открой бота и жми <b>🎯 Проверить уровень</b> 👇"
    ),
    "pre_test": (
        "🦜 <b>Рико:</b> Мы уже почти знакомы!\n\n"
        "Осталось пройти короткий тест — "
        "перевод, слова и одно аудио. Минут 5–6.\n\n"
        "После него — <b>3 дня полного доступа</b>. "
        "Жми <b>✅ Погнали!</b> в боте 🚀"
    ),
    "daily_fire": (
        "🔥 <b>Рико:</b> Тест позади, одна искра Огня уже близко!\n\n"
        "Загляни в <b>🔥 Огонь дня</b>, поймай искру — "
        "дальше будет короткий кусочек темы <b>to be</b> "
        "(1 слайд + 1 задание).\n\n"
        "Это быстро, обещаю 💚"
    ),
    "to_be": (
        "🦜 <b>Рико:</b> Ты уже у темы <b>to be</b> — осталось совсем чуть-чуть!\n\n"
        "Один слайд и одно задание — и ты поймёшь, как устроены уроки.\n\n"
        "Открой бота и дожми 💪 Это 2–3 минуты."
    ),
    "done_no_chat": (
        "🗣️ <b>Рико:</b> Ты уже прошёл знакомство — респект!\n\n"
        "Заходи в <b>Общаться</b>: я сразу предложу тему, "
        "а у тебя сейчас <b>безлимит на триале</b>.\n\n"
        "Напиши хоть одно предложение про свой день 💬 "
        "Именно на общении язык растёт быстрее всего."
    ),
    "chatted": (
        "🦜 <b>Рико:</b> Класс, что уже поболтали!\n\n"
        "Зайди снова на минутку — так появляется привычка. "
        "Можно ещё заглянуть в <b>Listening</b> и выбрать тему сам 🎧\n\n"
        "Я на связи 💚"
    ),
}


def ensure_drip(user: dict) -> dict:
    d = user.get("onboard_drip")
    if not isinstance(d, dict):
        d = {}
        user["onboard_drip"] = d
    d.setdefault("sent", {})  # kind -> unix ts
    return d


def touch_stage(user: dict, stage: str | None = None) -> None:
    """Вызвать при смене стадии онбординга — ставит таймер «застрял с …»."""
    from services.onboard_guided import onboard_stage, set_onboard_stage

    st = stage if stage is not None else onboard_stage(user)
    if not st:
        return
    set_onboard_stage(user, st)


def _first_seen_ts(user: dict) -> float:
    return float(user.get("first_seen_at") or 0) or float(user.get("last_start_at") or 0)


def _last_active_ts(user: dict) -> float:
    raw = user.get("last_active_at")
    if isinstance(raw, (int, float)):
        return float(raw) if raw else 0.0
    if isinstance(raw, str) and raw.strip():
        try:
            from datetime import datetime

            s = raw.strip()
            if s.endswith("Z"):
                s = s[:-1] + "+00:00"
            dt = datetime.fromisoformat(s)
            return dt.timestamp()
        except Exception:
            return 0.0
    return 0.0


def _stage_stuck_since(user: dict) -> float:
    ob = user.get("onboard") if isinstance(user.get("onboard"), dict) else {}
    at = float(ob.get("stage_at") or 0)
    if at > 0:
        return at
    p = user.get("placement") if isinstance(user.get("placement"), dict) else {}
    fin = float(p.get("finished_at") or 0)
    stage = str(ob.get("stage") or "")
    if user.get("assessment_done") and fin > 0 and stage in {
        "daily_fire",
        "grammar_cta",
        "slides",
        "tasks",
        "tasks_menu",
        "done",
        "",
    }:
        return fin
    return _first_seen_ts(user)


def detect_drip_kind(user: dict) -> str | None:
    """Какой пинг сейчас уместен по факту прогресса (живой стейт)."""
    from services.onboard_guided import ensure_onboard, is_imit_active

    if user.get("tg_blocked") or user.get("imitating_registration"):
        return None
    if is_imit_active(user):
        return None

    ob = ensure_onboard(user)
    stage = str(ob.get("stage") or "")
    name = (user.get("name") or "").strip()
    assessed = bool(user.get("assessment_done"))
    chat_n = int(user.get("chat_text_total") or 0) + int(user.get("chat_voice_total") or 0)

    # Ещё не закончил тест
    if not assessed:
        if not name or stage in {"", "intro"}:
            return "intro"
        return "pre_test"

    # Тест есть — смотрим онбординг-путь
    if stage == "daily_fire":
        return "daily_fire"
    if stage in {"grammar_cta", "slides", "tasks", "tasks_menu"}:
        return "to_be"
    if stage == "done" or (ob.get("active") is False and stage == "done"):
        if chat_n <= 0:
            return "done_no_chat"
        # уже болтал — мягкий возврат
        return "chatted"

    # assessment_done, stage пустой/странный (старые карточки)
    if assessed and stage in {"", "intro", "pre_test"}:
        if chat_n <= 0:
            return "done_no_chat"
        return "chatted"
    return None


def in_quiet_hours(hour: int | None = None) -> bool:
    from services.notify_state import now_msk

    h = int(hour if hour is not None else now_msk().hour)
    return h >= QUIET_START or h < QUIET_END


def recently_active(user: dict, *, minutes: float = ACTIVE_GRACE_MIN) -> bool:
    ts = _last_active_ts(user)
    if ts <= 0:
        return False
    return (time.time() - ts) < minutes * 60


def drip_due(user: dict, *, hour: int | None = None) -> str | None:
    """Вернуть kind, если пора слать; иначе None."""
    if in_quiet_hours(hour):
        return None
    if recently_active(user):
        return None

    kind = detect_drip_kind(user)
    if not kind:
        return None

    drip = ensure_drip(user)
    sent = drip.get("sent") if isinstance(drip.get("sent"), dict) else {}
    if sent.get(kind):
        return None
    # done_no_chat после chatted не шлём наоборот — ок
    if kind == "chatted" and sent.get("done_no_chat") and int(
        user.get("chat_text_total") or 0
    ) + int(user.get("chat_voice_total") or 0) <= 0:
        return None

    need_h = float(DRIP_HOURS.get(kind) or 2.0)
    stuck = _stage_stuck_since(user)
    if stuck <= 0:
        return None
    hours = (time.time() - stuck) / 3600.0
    if hours < need_h:
        return None
    return kind


def mark_drip_sent(user: dict, kind: str) -> None:
    drip = ensure_drip(user)
    sent = drip.setdefault("sent", {})
    sent[kind] = time.time()


def kb_for_kind(kind: str) -> InlineKeyboardMarkup:
    if kind == "done_no_chat":
        rows = [
            [InlineKeyboardButton(text="🗣️ Общаться", callback_data="ofu:chat")],
            [InlineKeyboardButton(text="🏠 В меню", callback_data="ntf:menu")],
        ]
    else:
        rows = [
            [
                InlineKeyboardButton(
                    text="🦜 Открыть бота",
                    url="https://t.me/LexDAN_bot",
                )
            ],
            [InlineKeyboardButton(text="🏠 В меню", callback_data="ntf:menu")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def text_for_kind(kind: str) -> str:
    return MSG.get(kind) or ""


def should_post_channel_social(*, hour: int | None = None) -> bool:
    """Один соцдок-пост в канал утром (10–12 МСК), один раз за кампанию."""
    from services.notify_state import now_msk

    h = int(hour if hour is not None else now_msk().hour)
    if h < 10 or h > 12:
        return False
    from services.database import load_users

    users = load_users()
    meta = users.get("__broadcasts__")
    if not isinstance(meta, dict):
        return True
    return not bool(meta.get(CHANNEL_SOCIAL_KEY))


def mark_channel_social_posted() -> None:
    from services.database import load_users, save_users

    users = load_users()
    meta = users.get("__broadcasts__")
    if not isinstance(meta, dict):
        meta = {}
    meta[CHANNEL_SOCIAL_KEY] = True
    meta[f"{CHANNEL_SOCIAL_KEY}_at"] = time.time()
    users["__broadcasts__"] = meta
    save_users(users, only=["__broadcasts__"])


def drip_rules_summary() -> str:
    lines = [
        "Таймеры (с момента входа в стадию / first_seen):",
        f"  intro (Start, нет имени):      {DRIP_HOURS['intro']} ч",
        f"  pre_test (есть имя, нет теста): {DRIP_HOURS['pre_test']} ч",
        f"  daily_fire:                    {DRIP_HOURS['daily_fire']} ч",
        f"  to_be (слайды/задания):        {DRIP_HOURS['to_be']} ч",
        f"  done без чата:                 {DRIP_HOURS['done_no_chat']} ч",
        f"  уже болтал (мягкий возврат):   {DRIP_HOURS['chatted']} ч",
        f"Тихие часы МСК: {QUIET_START}:00–{QUIET_END}:00 (не шлём)",
        f"Не пингуем, если активен последние {ACTIVE_GRACE_MIN} мин",
        "Новые люди подхватываются сами — без фиксированного списка.",
    ]
    return "\n".join(lines)
