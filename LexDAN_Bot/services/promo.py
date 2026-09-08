"""
Промокоды LexDAN.
ENGRICO77 — 7 дней полного доступа (= тариф 799) включая Listening.
Срок действия ENGRICO77 истёк — новые активации закрыты.

LIFETIME FULL 399 — одноразовые коды: полный безлимит навсегда по 399₽/мес.
Прогресс (задания, слова, стрик) не сбрасывается после окончания триала.
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from typing import Any

from services.growth import ensure_growth, is_premium, start_trial

log = logging.getLogger(__name__)

# Вечная цена полного тарифа по промокоду (не зависит от каталога 799 и акций).
LIFETIME_FULL_PRICE_RUB = 399

# code → meta
# active=False — код известен, но больше не активируется («действие закончилось»).
# once_global=True — код сгорает после первой активации любым пользователем.
PROMO_CODES: dict[str, dict] = {
    "ENGRICO77": {
        "days": 7,
        "kind": "full_trial",
        "title": "7 дней полного доступа (как тариф 799₽), включая Listening",
        "listening": True,
        "active": False,
    },
    # 10 одноразовых кодов: полный безлимит навсегда за 399₽/мес
    "459FGEZRQP": {
        "kind": "lifetime_full_price",
        "price_rub": LIFETIME_FULL_PRICE_RUB,
        "title": "Безлимит ко всему навсегда по цене 399₽/мес",
        "active": True,
        "once_global": True,
    },
    "4XSLACCA62": {
        "kind": "lifetime_full_price",
        "price_rub": LIFETIME_FULL_PRICE_RUB,
        "title": "Безлимит ко всему навсегда по цене 399₽/мес",
        "active": True,
        "once_global": True,
    },
    "AFWD46VCF6": {
        "kind": "lifetime_full_price",
        "price_rub": LIFETIME_FULL_PRICE_RUB,
        "title": "Безлимит ко всему навсегда по цене 399₽/мес",
        "active": True,
        "once_global": True,
    },
    "AQYB5PFRHS": {
        "kind": "lifetime_full_price",
        "price_rub": LIFETIME_FULL_PRICE_RUB,
        "title": "Безлимит ко всему навсегда по цене 399₽/мес",
        "active": True,
        "once_global": True,
    },
    "EJTVGEC6FP": {
        "kind": "lifetime_full_price",
        "price_rub": LIFETIME_FULL_PRICE_RUB,
        "title": "Безлимит ко всему навсегда по цене 399₽/мес",
        "active": True,
        "once_global": True,
    },
    "JSWYNYCFCW": {
        "kind": "lifetime_full_price",
        "price_rub": LIFETIME_FULL_PRICE_RUB,
        "title": "Безлимит ко всему навсегда по цене 399₽/мес",
        "active": True,
        "once_global": True,
    },
    "KMDUJ6QHLA": {
        "kind": "lifetime_full_price",
        "price_rub": LIFETIME_FULL_PRICE_RUB,
        "title": "Безлимит ко всему навсегда по цене 399₽/мес",
        "active": True,
        "once_global": True,
    },
    "LEBUXHAMQU": {
        "kind": "lifetime_full_price",
        "price_rub": LIFETIME_FULL_PRICE_RUB,
        "title": "Безлимит ко всему навсегда по цене 399₽/мес",
        "active": True,
        "once_global": True,
    },
    "LWGVYYE3YX": {
        "kind": "lifetime_full_price",
        "price_rub": LIFETIME_FULL_PRICE_RUB,
        "title": "Безлимит ко всему навсегда по цене 399₽/мес",
        "active": True,
        "once_global": True,
    },
    "VW54JPQ5SK": {
        "kind": "lifetime_full_price",
        "price_rub": LIFETIME_FULL_PRICE_RUB,
        "title": "Безлимит ко всему навсегда по цене 399₽/мес",
        "active": True,
        "once_global": True,
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

_REDEEMS_FILE = "promo_redeems.json"
_REDEEMS_META_KEY = "promo_redeems"
_redeems_lock = threading.Lock()


def normalize_promo(code: str) -> str:
    return (code or "").strip().upper().replace(" ", "")


def has_lifetime_full_price(user: dict | None) -> bool:
    if not user:
        return False
    return int(user.get("lifetime_full_price_rub") or 0) > 0


def lifetime_full_price_rub(user: dict | None) -> int | None:
    """Зафиксированная цена полного тарифа или None."""
    if not user:
        return None
    rub = int(user.get("lifetime_full_price_rub") or 0)
    return rub if rub > 0 else None


def lifetime_price_lines_html(user: dict) -> str:
    rub = lifetime_full_price_rub(user) or LIFETIME_FULL_PRICE_RUB
    return (
        f"🏷 <b>Твоя персональная цена</b> — безлимит ко всему за "
        f"<b>{rub}₽/мес</b> навсегда\n"
        "• уроки без лимита (включая Живую речь)\n"
        "• безлимит общения\n"
        "• Listening, Reading, все голоса и темы\n"
        "Даже если цены в каталоге вырастут — для тебя останется эта сумма.\n\n"
    )


def _use_postgres() -> bool:
    return bool((os.getenv("DATABASE_URL") or "").strip())


def _default_redeems() -> dict:
    return {"redeems": {}}


def _load_redeems_file() -> dict:
    if not os.path.exists(_REDEEMS_FILE):
        return _default_redeems()
    try:
        with open(_REDEEMS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return _default_redeems()
        out = _default_redeems()
        out.update(data)
        if not isinstance(out.get("redeems"), dict):
            out["redeems"] = {}
        return out
    except (json.JSONDecodeError, OSError):
        return _default_redeems()


def _save_redeems_file(state: dict) -> None:
    with open(_REDEEMS_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def _pg_connect():
    import psycopg

    url = (os.getenv("DATABASE_URL") or "").strip()
    if "sslmode=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return psycopg.connect(url)


def _ensure_meta_table(cur) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS app_meta (
            key TEXT PRIMARY KEY,
            data JSONB NOT NULL DEFAULT '{}'::jsonb,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )


def _claim_global_promo(code: str, user_id: str) -> tuple[bool, str]:
    """
    Глобально сжечь одноразовый код.
    Returns (ok, error_html_if_failed).
    """
    key = normalize_promo(code)
    uid = str(user_id).strip()
    if not key or not uid:
        return False, "Не удалось применить промокод. Попробуй ещё раз."

    with _redeems_lock:
        if _use_postgres():
            try:
                return _claim_global_promo_pg(key, uid)
            except Exception as e:
                log.error("promo redeem pg failed: %s", e)
                # fallback на файл, чтобы не потерять активацию локально
        return _claim_global_promo_file(key, uid)


def _claim_global_promo_file(key: str, uid: str) -> tuple[bool, str]:
    state = _load_redeems_file()
    redeems: dict[str, Any] = state.setdefault("redeems", {})
    existing = redeems.get(key)
    if isinstance(existing, dict):
        if str(existing.get("user_id") or "") == uid:
            return True, ""
        return False, (
            f"🔒 Промокод <b>{key}</b> уже использован другим человеком.\n"
            "У каждого кода только одна активация."
        )
    redeems[key] = {"user_id": uid, "at": time.time()}
    _save_redeems_file(state)
    return True, ""


def _claim_global_promo_pg(key: str, uid: str) -> tuple[bool, str]:
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            _ensure_meta_table(cur)
            cur.execute(
                "SELECT data FROM app_meta WHERE key = %s FOR UPDATE",
                (_REDEEMS_META_KEY,),
            )
            row = cur.fetchone()
            if not row:
                state = _default_redeems()
            else:
                data = row[0]
                if not isinstance(data, dict):
                    data = json.loads(data)
                state = _default_redeems()
                state.update(data)
                if not isinstance(state.get("redeems"), dict):
                    state["redeems"] = {}

            redeems: dict[str, Any] = state.setdefault("redeems", {})
            existing = redeems.get(key)
            if isinstance(existing, dict):
                if str(existing.get("user_id") or "") == uid:
                    conn.commit()
                    return True, ""
                conn.commit()
                return False, (
                    f"🔒 Промокод <b>{key}</b> уже использован другим человеком.\n"
                    "У каждого кода только одна активация."
                )

            redeems[key] = {"user_id": uid, "at": time.time()}
            cur.execute(
                """
                INSERT INTO app_meta (key, data, updated_at)
                VALUES (%s, %s::jsonb, now())
                ON CONFLICT (key) DO UPDATE
                SET data = EXCLUDED.data, updated_at = now()
                """,
                (_REDEEMS_META_KEY, json.dumps(state, ensure_ascii=False)),
            )
        conn.commit()
    return True, ""


def apply_promo(
    user: dict, code: str, *, user_id: str | None = None
) -> tuple[bool, str]:
    """
    Применить промокод. Returns (ok, html_message).
    Каждый код — строго один раз на пользователя.
    Коды с once_global — ещё и один раз на весь бот.
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
        if key not in used:
            used.append(key)
            user["used_promos"] = used
        return False, (
            f"🔒 Промокод <b>{key}</b> уже был активирован на этом аккаунте.\n"
            "Повторно использовать его нельзя."
        )

    kind = str(meta.get("kind") or "")
    uid = str(
        user_id
        or user.get("tg_id")
        or user.get("telegram_id")
        or user.get("id")
        or ""
    ).strip()

    if kind == "lifetime_full_price":
        if has_lifetime_full_price(user):
            return False, (
                "🏷 У тебя уже закреплена персональная цена на полный доступ.\n"
                "Повторный промокод этого типа не нужен."
            )
        if meta.get("once_global"):
            if not uid:
                return False, "Не удалось применить промокод. Напиши в поддержку."
            ok_claim, err = _claim_global_promo(key, uid)
            if not ok_claim:
                return False, err

        price = int(meta.get("price_rub") or LIFETIME_FULL_PRICE_RUB)
        user["lifetime_full_price_rub"] = price
        user["lifetime_full_promo"] = key
        user["lifetime_full_locked_at"] = time.time()
        used.append(key)
        user["used_promos"] = used
        return True, (
            f"🎉 Промокод <b>{key}</b> активирован!\n\n"
            f"🏷 <b>Твоя цена навсегда:</b> полный безлимит за <b>{price}₽/мес</b>\n\n"
            "Входит всё, что есть на тарифе безлимита:\n"
            "• уроки без лимита (Grammar, Vocabulary, Listening, Reading, Живая речь)\n"
            "• безлимит общения и все голоса\n"
            "• премиальные награды серии\n\n"
            "Когда цены в каталоге вырастут или изменятся — тебе по-прежнему "
            f"предложат оплатить <b>{price}₽</b> (и при продлении тоже).\n\n"
            "Подписка сама не включается — оформи её в профиле → Подписка 💎"
        )

    if kind == "full_trial":
        days = int(meta["days"])
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

    return False, "Этот промокод пока нельзя применить. Напиши в поддержку."


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
    # Персональная цена 399 важнее стандартного оффера
    if has_lifetime_full_price(user):
        rub = lifetime_full_price_rub(user) or LIFETIME_FULL_PRICE_RUB
        return (
            "🦜 <b>Рико на связи</b>\n\n"
            "Пробный период закончился — прогресс на месте 💚\n\n"
            f"🏷 У тебя закреплена цена <b>{rub}₽/мес</b> на полный безлимит.\n"
            "Оформи подписку в профиле — цена не вырастет."
        )
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


def scan_promo_users(code: str) -> list[tuple[str, dict]]:
    """Пользователи с этим промокодом (текущий trial или used_promos)."""
    from services.database import load_users, get_user
    from services.growth import ensure_growth

    key = normalize_promo(code)
    users = load_users()
    out: list[tuple[str, dict]] = []
    for uid, raw in users.items():
        if not isinstance(raw, dict):
            continue
        user = get_user(users, str(uid))
        ensure_growth(user)
        used = [normalize_promo(x) for x in list(user.get("used_promos") or []) if x]
        cur = normalize_promo(str(user.get("promo_trial_code") or ""))
        locked = normalize_promo(str(user.get("lifetime_full_promo") or ""))
        if key in used or cur == key or locked == key:
            out.append((str(uid), user))
    return out


def revoke_promo_trial(user: dict, code: str) -> bool:
    """
    Снять активный триал этого промокода.
    premium_until обнуляем только если in_promo_trial ещё True
    (чтобы не снести оплаченную подписку).
    """
    from services.growth import ensure_growth

    ensure_growth(user)
    key = normalize_promo(code)
    cur = normalize_promo(str(user.get("promo_trial_code") or ""))
    used = [normalize_promo(x) for x in list(user.get("used_promos") or []) if x]
    if cur != key and not (user.get("in_promo_trial") and key in used):
        return False
    changed = False
    if user.get("in_promo_trial") and (cur == key or not cur):
        user["premium_until"] = 0
        user["in_promo_trial"] = False
        user["trial_end_notified"] = True
        changed = True
    if cur == key:
        user["promo_trial_code"] = ""
        user["promo_listening"] = False
        changed = True
    if changed:
        maybe_cleanup_expired_trial_voice(user)
    return changed
