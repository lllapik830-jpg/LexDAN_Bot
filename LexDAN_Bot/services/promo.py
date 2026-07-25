"""
Промокоды LexDAN.
ENGRICO77 — 7 дней полного доступа (= тариф 799).
Прогресс (задания, слова, стрик) не сбрасывается после окончания.
"""

from __future__ import annotations

from services.growth import ensure_growth, start_trial

# code → (days_full, label)
PROMO_CODES: dict[str, dict] = {
    "ENGRICO77": {
        "days": 7,
        "kind": "full_trial",
        "title": "7 дней полного доступа (как тариф 799₽)",
    },
}

BTN_SKIP_PROMO = "⏭ Пропустить"


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
        # голос после истечения сбросит maybe_cleanup_expired_trial_voice

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
