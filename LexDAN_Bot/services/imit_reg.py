"""
Имитация регистрации нового пользователя (только MANAGER).

Гарантии:
- трогает только карточку админа (и служебный ключ бэкапа);
- бэкап лежит отдельно от рабочей карточки → восстановление надёжное;
- во время имитации флаги исключают топы/статы/реферальные побочки на других;
- /imit_finish полностью откатывает карточку к снимку и стирает имитационные данные.
"""

from __future__ import annotations

import copy
import logging
from typing import Any

from services.database import MODE_MENU, delete_users, get_user, save_users

log = logging.getLogger(__name__)

BACKUP_PREFIX = "__imit_backup__"
FLAG = "imitating_registration"


def backup_key(uid: str) -> str:
    return f"{BACKUP_PREFIX}{str(uid)}"


def is_meta_uid(uid: str | None) -> bool:
    """Служебные ключи в users (не реальные аккаунты)."""
    s = str(uid or "")
    return s.startswith("__")


def is_imitating(user: dict | None) -> bool:
    return bool(user and user.get(FLAG))


def is_imitating_uid(users: dict, uid: str) -> bool:
    raw = users.get(str(uid))
    return isinstance(raw, dict) and is_imitating(raw)


def _fresh_card(*, tg_username: str = "") -> dict[str, Any]:
    """Карточка как у только что зашедшего пользователя."""
    card: dict[str, Any] = {
        "name": None,
        "pending_name": "",
        "step": "awaiting_name",
        "mode": MODE_MENU,
        "level": "A1",
        "lessons_done": 0,
        "words_learned": 0,
        "phrases_learned": 0,
        "last_bot_reply": None,
        "premium_until": 0,
        "chat_until": 0,
        "assessment_done": False,
        "dev_unlock": False,
        "assessment": {},
        "grammar_progress": {
            "completed_exercises": {},
            "completed_topics": [],
        },
        "vocabulary_progress": {"words": [], "phrases": []},
        "streak": 0,
        "streak_last_date": "",
        "daily": {},
        "referral_code": "",
        "referred_by": None,
        "invite_count": 0,
        "trial_started_at": 0,
        "growth_onboarded": False,
        "referral_bonus_granted": False,
        "streak_safes": 0,
        "streak_safe_milestones_claimed": [],
        "streak_pending_restore": 0,
        "streak_burned": False,
        "streak_burn_date": "",
        "last_active_at": "",
        "reminder_sent_date": "",
        "first_seen_at": 0,
        "chat_text_total": 0,
        "chat_voice_total": 0,
        "rules_accepted": False,
        "pending_promo_msg": "",
        "lesson": {},
        "used_promos": [],
        "promo_trial_code": "",
        "in_promo_trial": False,
        "promo_listening": False,
        FLAG: True,
    }
    if tg_username:
        card["tg_username"] = tg_username.lstrip("@")
    return card


def start_imitation(users: dict, uid: str, *, tg_username: str = "") -> tuple[bool, str]:
    """
    Сохранить полный снимок админа и подменить карточку на «нового юзера».
    Returns (ok, message_html).
    """
    uid = str(uid)
    user = get_user(users, uid)
    bk = backup_key(uid)

    if is_imitating(user) and isinstance(users.get(bk), dict):
        return False, (
            "🧪 Имитация уже запущена.\n"
            "Пройди этапы или выйди через /imit_finish"
        )

    # Снимок: всё текущее состояние, без старых бэкапов внутри
    snapshot = copy.deepcopy(user)
    snapshot.pop("_imit_backup", None)
    snapshot.pop(FLAG, None)
    users[bk] = snapshot

    fresh = _fresh_card(tg_username=tg_username or (user.get("tg_username") or ""))
    fresh["tg_id"] = uid
    # Маркер, что бэкап лежит отдельно (на всякий случай и внутри карточки — путь id)
    fresh["_imit_backup_key"] = bk
    users[uid] = fresh

    save_users(users, only=[uid, bk])
    log.info("imit_start uid=%s backup=%s", uid, bk)
    return True, (
        "🧪 <b>Имитация регистрации включена</b>\n\n"
        "Сейчас ты видишь то же, что новый пользователь.\n"
        "Этапы: имя → промокод → правила → welcome → "
        "(в уроках — тест уровня).\n\n"
        "• Другие аккаунты не затрагиваются\n"
        "• Имитация не идёт в топы / рейтинги / админ-статы\n"
        "• Рефералка и побочки на друзей выключены\n\n"
        "Выход: /imit_finish — аккаунт восстановится, "
        "имитационные данные сотрутся."
    )


def finish_imitation(users: dict, uid: str) -> tuple[bool, str, dict | None]:
    """
    Восстановить снимок и удалить служебный бэкап + имитационный мусор.
    Returns (ok, message_html, restored_user_or_None).
    """
    uid = str(uid)
    bk = backup_key(uid)
    current = users.get(uid) if isinstance(users.get(uid), dict) else {}
    backup = users.get(bk)
    if not isinstance(backup, dict):
        # fallback: старый формат — бэкап внутри карточки
        nested = (current or {}).get("_imit_backup")
        if isinstance(nested, dict):
            backup = nested
        else:
            if current:
                current.pop(FLAG, None)
                current.pop("_imit_backup", None)
                current.pop("_imit_backup_key", None)
                save_users(users, only=uid)
            return False, "Имитация не активна (бэкап не найден). Запуск: /imit_start", None

    restored = copy.deepcopy(backup)
    restored.pop("_imit_backup", None)
    restored.pop("_imit_backup_key", None)
    restored.pop(FLAG, None)
    restored["mode"] = MODE_MENU
    if restored.get("name") and restored.get("rules_accepted"):
        restored["step"] = "ready"
    users[uid] = restored

    # Стереть имитационную карточку (заменена снимком) + служебный бэкап из БД
    save_users(users, only=uid)
    try:
        delete_users([bk])
    except Exception as e:
        log.warning("imit_finish delete backup failed uid=%s: %s", uid, e)
    users.pop(bk, None)

    log.info("imit_finish uid=%s restored, backup wiped", uid)
    name = restored.get("name") or "админ"
    return (
        True,
        f"✅ Имитация завершена. Аккаунт восстановлен, {name}. "
        "Имитационные данные стёрты.",
        restored,
    )
