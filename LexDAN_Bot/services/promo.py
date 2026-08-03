"""
Промокоды LexDAN.
ENGRICO77 — 7 дней полного доступа (= тариф 799) включая Listening.
Срок действия ENGRICO77 истёк — новые активации закрыты.
Прогресс (задания, слова, стрик) не сбрасывается после окончания триала.
"""

from __future__ import annotations

from services.growth import ensure_growth, is_premium, start_trial

# code → meta
# active=False — код известен, но больше не активируется («действие закончилось»).
PROMO_CODES: dict[str, dict] = {
    "ENGRICO77": {
        "days": 7,
        "kind": "full_trial",
        "title": "7 дней полного доступа (как тариф 799₽), включая Listening",
        "listening": True,
        "active": False,
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
    "🎧 Listening снова только в премиум-подписке\n"
    "🔥 Серия сохранена; новые награды теперь по бесплатной лестнице\n\n"
    "Хочешь снова безлимит уроков, Listening, все голоса и большую библиотеку тем?\n"
    "Я рядом — выбери тариф ниже 😊👇"
)


def normalize_promo(code: str) -> str:
    return (code or "").strip().upper().replace(" ", "")


def apply_promo(user: dict, code: str) -> tuple[bool, str]:
    """
    Применить промокод. Returns (ok, html_message).
    Каждый код — строго один раз на пользователя.
    """
    ensure_growth(user)
    key = normalize_promo(code)
    if not key:
        return False, "Введи промокод текстом или нажми «Пропустить»."

    meta = PROMO_CODES.get(key)
    if not meta:
        return False, "🤔 Такой промокод не найден. Проверь написание или нажми «Пропустить»."

    if meta.get("active") is False:
        return False, (
            f"⌛ Промокод <b>{key}</b> больше не действует — срок акции закончился.\n"
            "Следи за новыми промо в канале: https://t.me/LexDan_Rico"
        )

    used = [normalize_promo(x) for x in list(user.get("used_promos") or []) if x]
    already = key in used or normalize_promo(str(user.get("promo_trial_code") or "")) == key
    if already:
        # на всякий случай зафиксируем в used_promos
        if key not in used:
            used.append(key)
            user["used_promos"] = used
        return False, (
            f"🔒 Промокод <b>{key}</b> уже был активирован на этом аккаунте.\n"
            "Повторно использовать его нельзя."
        )

    days = int(meta["days"])
    if meta["kind"] == "full_trial":
        start_trial(user, days=days)
        user["promo_trial_code"] = key
        user["in_promo_trial"] = True
        user["trial_end_notified"] = False
        if meta.get("listening"):
            user["promo_listening"] = True

    used.append(key)
    user["used_promos"] = used
    listen_line = (
        "\n🎧 Раздел <b>Listening</b> доступен на время пробного периода."
        if meta.get("listening")
        else ""
    )
    return True, (
        f"🎉 Промокод <b>{key}</b> активирован!\n\n"
        f"{meta['title']}.{listen_line}\n"
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
    if user_plan(user) == "free":
        user["promo_listening"] = False


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
    user["promo_listening"] = False
    # Оффер −15% действует только пока жив триал
    if (user.get("discount_note") or "") == "last_day_trial":
        from services.pricing import clear_discount

        clear_discount(user)
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
