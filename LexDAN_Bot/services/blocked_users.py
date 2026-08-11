"""
Живые / заблокировавшие бота пользователи.
"""

from __future__ import annotations

import asyncio
import logging

from config import MANAGER_ID
from services.database import delete_users, get_user, load_users, save_users
from services.growth import ensure_growth

log = logging.getLogger(__name__)


def is_registered(user: dict) -> bool:
    """Прошёл регистрацию (есть имя и step=ready)."""
    if not (user.get("name") or "").strip():
        return False
    return (user.get("step") or "") == "ready"


def _is_blocked_flag(user: dict) -> bool:
    return bool(user.get("tg_blocked"))


def iter_registered() -> list[tuple[str, dict]]:
    users = load_users()
    out: list[tuple[str, dict]] = []
    for uid, raw in users.items():
        if not isinstance(raw, dict):
            continue
        if str(uid).startswith("__"):
            continue
        if raw.get("imitating_registration"):
            continue
        u = get_user(users, str(uid))
        ensure_growth(u)
        if is_registered(u):
            out.append((str(uid), u))
    out.sort(key=lambda x: x[1].get("last_active_at") or "", reverse=True)
    return out


def list_alive_registered() -> list[tuple[str, dict]]:
    """Зарегистрированные, у кого нет флага tg_blocked."""
    return [(uid, u) for uid, u in iter_registered() if not _is_blocked_flag(u)]


def list_flagged_blocked() -> list[tuple[str, dict]]:
    users = load_users()
    out: list[tuple[str, dict]] = []
    for uid, raw in users.items():
        if not isinstance(raw, dict):
            continue
        u = get_user(users, str(uid))
        if _is_blocked_flag(u) and str(uid) != str(MANAGER_ID):
            out.append((str(uid), u))
    return out


def format_alive_list() -> str:
    rows = list_alive_registered()
    blocked_n = len(list_flagged_blocked())
    lines = [
        "👥 <b>Живые пользователи</b> (не блокировали бота)\n",
        f"Зарегистрированы и активны: <b>{len(rows)}</b>",
        f"В базе с флагом «заблокировал»: <b>{blocked_n}</b>",
        "Команды: /purge_blocked — проверить Telegram и удалить блоки\n",
    ]
    if not rows:
        lines.append("Пока никого.")
        return "\n".join(lines)

    for i, (uid, u) in enumerate(rows, 1):
        name = (u.get("name") or "—").strip() or "—"
        level = u.get("level") or "—"
        active = (u.get("last_active_at") or "")[:16].replace("T", " ")
        lines.append(
            f"{i}. <code>{uid}</code> · {name} · {level}"
            + (f" · {active}" if active else "")
        )
    return "\n".join(lines)


def purge_flagged_blocked() -> list[str]:
    """Удалить из БД тех, у кого уже tg_blocked=True. Не трогает админа."""
    ids = [uid for uid, _ in list_flagged_blocked()]
    if not ids:
        return []
    delete_users(ids)
    return ids


def _looks_blocked_error(err: BaseException) -> bool:
    s = str(err).lower()
    return (
        "blocked" in s
        or "deactivated" in s
        or "forbidden" in s
        or "chat not found" in s
        or "user is deactivated" in s
    )


async def probe_user_blocked(bot, user_id: str) -> bool:
    """True = пользователь недоступен (блок / удалён)."""
    try:
        await bot.send_chat_action(chat_id=int(user_id), action="typing")
        return False
    except Exception as e:
        if _looks_blocked_error(e):
            return True
        log.warning("probe %s: %s", user_id, e)
        # неизвестная ошибка — не удаляем
        return False


async def scan_and_purge_blocked(bot) -> dict:
    """
    1) Удалить уже помеченных tg_blocked.
    2) Проверить остальных зарегистрированных через Telegram.
    3) Удалить тех, кто заблокировал.
    """
    removed_flagged = purge_flagged_blocked()

    alive = list_alive_registered()
    newly_blocked: list[str] = []
    still_ok = 0

    users = load_users()
    dirty_ids: list[str] = []

    for uid, _ in alive:
        if uid == str(MANAGER_ID):
            still_ok += 1
            continue
        blocked = await probe_user_blocked(bot, uid)
        if blocked:
            newly_blocked.append(uid)
            u = get_user(users, uid)
            u["tg_blocked"] = True
            dirty_ids.append(uid)
        else:
            u = get_user(users, uid)
            if u.pop("tg_blocked", None) is not None:
                dirty_ids.append(uid)
            still_ok += 1
        await asyncio.sleep(0.05)

    if dirty_ids:
        save_users(users, only=dirty_ids)

    removed_new = []
    if newly_blocked:
        delete_users(newly_blocked)
        removed_new = list(newly_blocked)

    return {
        "removed_flagged": removed_flagged,
        "removed_scanned": removed_new,
        "alive_left": still_ok,
        "checked": len(alive),
    }
