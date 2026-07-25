"""
Промокоды LexDAN.
ENGRICO77 — 7 дней полного доступа (= тариф 799).
Прогресс (задания, слова, стрик) не сбрасывается после окончания.
"""

from __future__ import annotations

from services.growth import ensure_growth, is_premium, start_trial

# code → (days_full, label)
PROMO_CODES: dict[str, dict] = {
    "ENGRICO77": {
        "days": 7,
        "kind": "full_trial",
        "title": "7 дней полного доступа (как тариф 799₽)",
    },
}

BTN_SKIP_PROMO = "⏭ Пропустить"
BTN_ENTER_PROMO = "🎟 Промокод"

TRIAL_ENDED_HTML = (
    "🦜 <b>Рико на связи</b>\n\n"
    "Пробный период закончился — но ты ничего не потерял(а)! 💚\n\n"
    "✅ Все задания, слова и серия дней на месте\n"
    "🎙 Голос озвучки снова обычный (Adam)\n"
    "🗂 Библиотека тем и дневные лимиты — как на бесплатном тарифе\n"
    "🔥 Серия сохранена; новые награды теперь по бесплатной лестнице\n\n"
    "Хочешь снова безлимит уроков, все голоса и большую библиотеку тем?\n"
    "Я рядом — выбери тариф ниже 😊👇"
)


def normalize_promo(code: str) -> str:
    return (code or "").strip().upper().replace(" ", "")


def apply_promo(user: dict, code: str) -> tuple[bool, str]:
    """
    Применить промокод. Returns (ok, html_message).
    Один код — один раз на пользователя (по списку used_promos).
    """
    ensure_growth(user)
    key = normalize_promo(code)
    if not key:
        return False, "Введи промокод текстом или нажми «Пропустить»."

    meta = PROMO_CODES.get(key)
    if not meta:
        return False, "🤔 Такой промокод не найден. Проверь написание или нажми «Пропустить»."

    used = list(user.get("used_promos") or [])
    if key in used:
        return False, "Этот промокод ты уже активировал(а)."

    days = int(meta["days"])
    if meta["kind"] == "full_trial":
        start_trial(user, days=days)
        user["promo_trial_code"] = key
        user["in_promo_trial"] = True
        user["trial_end_notified"] = False

    used.append(key)
    user["used_promos"] = used
    return True, (
        f"🎉 Промокод <b>{key}</b> активирован!\n\n"
        f"{meta['title']}.\n"
        "Доступны уроки без лимита, общение без лимита, все голоса и библиотека тем.\n"
        "Стрик и рефералка в этот период работают как на тарифе 799₽.\n\n"
        "Когда 7 дней закончатся — прогресс (задания, слова, стрик) сохранится, "
        "просто вернёшься на бесплатный тариф."
    )


def maybe_cleanup_expired_trial_voice(user: dict) -> None:
    """Если полный доступ кончился — сбросить выбор премиум-голоса."""
    from services.rewards import user_plan

    ensure_growth(user)
    if user_plan(user) == "free" and user.get("chat_voice_key"):
        user["chat_voice_key"] = ""


def pop_trial_ended_notice(user: dict) -> str | None:
    """
    Один раз вернуть текст о конце пробного периода.
    Вызывать при активности пользователя или из фонового цикла.
    """
    ensure_growth(user)
    if not user.get("in_promo_trial"):
        return None
    if is_premium(user):
        return None

    user["in_promo_trial"] = False
    user["trial_end_notified"] = True
    maybe_cleanup_expired_trial_voice(user)
    return TRIAL_ENDED_HTML


def collect_trial_ended_users() -> list[tuple[str, str]]:
    """
    Найти пользователей с истёкшим промо-триалом без уведомления.
    Returns [(user_id, html_message), ...].
    """
    from services.database import load_users, get_user, save_users

    users = load_users()
    out: list[tuple[str, str]] = []
    touched: list[str] = []
    for uid, raw in list(users.items()):
        if not isinstance(raw, dict):
            continue
        if not raw.get("in_promo_trial"):
            continue
        user = get_user(users, str(uid))
        msg = pop_trial_ended_notice(user)
        if msg:
            out.append((str(uid), msg))
            touched.append(str(uid))
    if touched:
        save_users(users, only=touched)
    return out
