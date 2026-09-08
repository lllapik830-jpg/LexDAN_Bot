"""Недельный рейтинг платных подписчиков (пн–вс, итоги в пн 18:00 за прошлую неделю)."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from services.database import get_user, load_users, save_users
from services.growth import ensure_growth, extend_premium
from services.notify_state import iso_week_id, now_msk, today_msk
from services.rewards import user_plan

log = logging.getLogger(__name__)

CHAT_POINTS_PER_MSG = 2
CHAT_POINTS_CAP_DAY = 6
ACTIVE_DAY_BONUS = 2
PRIZES = {1: 7, 2: 3, 3: 1}


def prev_iso_week_id() -> str:
    d = (now_msk() - timedelta(days=7)).date()
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def ensure_week(user: dict) -> dict:
    ensure_growth(user)
    wid = iso_week_id()
    raw = user.get("notify_week")
    if not isinstance(raw, dict) or raw.get("week_id") != wid:
        # сохраняем прошлую неделю отдельно для итогов
        if isinstance(raw, dict) and raw.get("week_id") and raw.get("week_id") != wid:
            user["notify_week_prev"] = dict(raw)
        raw = {
            "week_id": wid,
            "points": 0,
            "tasks": 0,
            "words": 0,
            "chat_points_today": 0,
            "chat_day": "",
            "active_days": [],
        }
        user["notify_week"] = raw
    if not isinstance(raw.get("active_days"), list):
        raw["active_days"] = []
    return raw


def _bump(user: dict, points: int, *, tasks: int = 0, words: int = 0) -> None:
    w = ensure_week(user)
    w["points"] = int(w.get("points") or 0) + int(points)
    if tasks:
        w["tasks"] = int(w.get("tasks") or 0) + int(tasks)
    if words:
        w["words"] = int(w.get("words") or 0) + int(words)
    day = today_msk()
    days = list(w.get("active_days") or [])
    if day not in days:
        days.append(day)
        w["active_days"] = days
        w["points"] = int(w.get("points") or 0) + ACTIVE_DAY_BONUS


def note_task_points(user: dict, n: int = 1) -> None:
    if user_plan(user) != "full":
        return
    _bump(user, n, tasks=n)


def note_word_points(user: dict, n: int = 1) -> None:
    if user_plan(user) != "full":
        return
    _bump(user, n, words=n)


def note_chat_points(user: dict) -> None:
    if user_plan(user) != "full":
        return
    w = ensure_week(user)
    day = today_msk()
    if w.get("chat_day") != day:
        w["chat_day"] = day
        w["chat_points_today"] = 0
    used = int(w.get("chat_points_today") or 0)
    if used >= CHAT_POINTS_CAP_DAY:
        days = list(w.get("active_days") or [])
        if day not in days:
            days.append(day)
            w["active_days"] = days
            w["points"] = int(w.get("points") or 0) + ACTIVE_DAY_BONUS
        return
    add = min(CHAT_POINTS_PER_MSG, CHAT_POINTS_CAP_DAY - used)
    w["chat_points_today"] = used + add
    _bump(user, add)


def _board_for_week(week_id: str, *, limit: int = 10) -> list[tuple[str, dict, int]]:
    users = load_users()
    rows: list[tuple[str, dict, int]] = []
    for uid, raw in users.items():
        if not isinstance(raw, dict) or str(uid).startswith("__"):
            continue
        if raw.get("imitating_registration"):
            continue
        user = get_user(users, str(uid))
        ensure_growth(user)
        if user_plan(user) != "full":
            continue
        # текущая или сохранённая прошлая
        candidates = []
        if isinstance(user.get("notify_week"), dict):
            candidates.append(user["notify_week"])
        if isinstance(user.get("notify_week_prev"), dict):
            candidates.append(user["notify_week_prev"])
        pts = 0
        for w in candidates:
            if w.get("week_id") == week_id:
                pts = max(pts, int(w.get("points") or 0))
        if pts <= 0:
            continue
        rows.append((str(uid), user, pts))
    rows.sort(key=lambda x: (-x[2], x[0]))
    return rows[:limit]


def week_leaderboard(*, limit: int = 10) -> list[tuple[str, dict, int]]:
    return _board_for_week(iso_week_id(), limit=limit)


def format_top10_html(rows: list[tuple[str, dict, int]] | None = None) -> str:
    rows = rows if rows is not None else week_leaderboard(limit=10)
    if not rows:
        return "🏆 Пока пусто — будь первым(ой) на этой неделе!"
    lines = ["🏆 <b>Топ-10 недели</b>\n"]
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for i, (_uid, user, pts) in enumerate(rows, start=1):
        name = (user.get("name") or "Игрок").strip() or "Игрок"
        m = medals.get(i, f"{i}.")
        lines.append(f"{m} {name} — <b>{pts}</b>")
    return "\n".join(lines)


async def finalize_week_and_notify(bot) -> dict[str, Any]:
    """Понедельник 18:00 МСК — итоги ПРОШЛОЙ недели."""
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

    from services.notify_copy import WEEK_PLACE, WEEK_RESULTS
    from services.notify_state import already_sent_today, mark_sent

    now = now_msk()
    if now.weekday() != 0 or now.hour != 18:
        return {"ok": False, "reason": "wrong_slot"}

    users = load_users()
    meta = users.get("__notify_week__")
    if not isinstance(meta, dict):
        meta = {}
    target = prev_iso_week_id()
    if meta.get("finalized_week") == target:
        return {"ok": False, "already": True}

    board = _board_for_week(target, limit=100)
    for place, (_uid, user, _pts) in enumerate(board[:3], start=1):
        days = PRIZES.get(place) or 0
        if days:
            extend_premium(user, days)

    def _name(idx: int) -> str:
        if idx >= len(board):
            return "—"
        return (board[idx][1].get("name") or "Игрок").strip() or "Игрок"

    def _pts(idx: int) -> int:
        if idx >= len(board):
            return 0
        return int(board[idx][2])

    base = WEEK_RESULTS.format(
        n1=_name(0),
        p1=_pts(0),
        n2=_name(1),
        p2=_pts(1),
        n3=_name(2),
        p3=_pts(2),
        winner=_name(0),
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏆 Таблица лидеров", callback_data="ntf:week")],
            [InlineKeyboardButton(text="🏠 В меню", callback_data="ntf:menu")],
        ]
    )

    sent = 0
    fail = 0
    place_map = {uid: i + 1 for i, (uid, _, _) in enumerate(board)}
    pts_map = {uid: pts for uid, _, pts in board}
    touched: list[str] = ["__notify_week__"]

    for uid, raw in list(users.items()):
        if not isinstance(raw, dict) or str(uid).startswith("__"):
            continue
        user = get_user(users, str(uid))
        ensure_growth(user)
        if user_plan(user) != "full" or user.get("tg_blocked"):
            continue
        text = base
        pl = place_map.get(str(uid))
        if pl:
            text += WEEK_PLACE.format(place=pl, points=pts_map.get(str(uid), 0))
        try:
            await bot.send_message(int(uid), text, parse_mode="HTML", reply_markup=kb)
            # недельные итоги имеют право занять слот дня
            mark_sent(user, "week_results")
            sent += 1
            touched.append(str(uid))
        except Exception as e:
            log.warning("week notify fail %s: %s", uid, e)
            fail += 1

    meta["finalized_week"] = target
    meta["finalized_at"] = now.isoformat()
    users["__notify_week__"] = meta
    save_users(users, only=list(dict.fromkeys(touched)))
    log.info("Week %s finalized sent=%s fail=%s top=%s", target, sent, fail, len(board[:3]))
    return {"ok": True, "sent": sent, "fail": fail, "week": target}
