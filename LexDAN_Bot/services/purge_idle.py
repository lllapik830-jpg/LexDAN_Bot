"""
Чистка мёртвых аккаунтов: не заходили > N дней и ни разу не сделали задание.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from config import MANAGER_ID
from services.admin_stats import _count_listening_topics, _count_reading_topics, _iter_users, _name
from services.database import delete_users
from services.notify_state import _parse_last_active
from services.rewards import count_grammar_exercises_done, user_plan
from services.vocabulary_state import sync_vocab_counters

MSK = timezone(timedelta(hours=3))
DEFAULT_IDLE_DAYS = 30


def _now() -> datetime:
    return datetime.now(MSK)


def _ts_to_dt(raw) -> datetime | None:
    if raw is None or raw == "":
        return None
    try:
        ts = float(raw)
    except (TypeError, ValueError):
        return None
    if ts <= 0:
        return None
    try:
        return datetime.fromtimestamp(ts, tz=MSK)
    except Exception:
        return None


def last_visit_at(user: dict) -> datetime | None:
    """Последний визит: last_active_at → last_start_at → first_seen_at."""
    dt = _parse_last_active(user)
    if dt:
        return dt
    for key in ("last_start_at", "first_seen_at"):
        dt = _ts_to_dt(user.get(key))
        if dt:
            return dt
    return None


def days_since_visit(user: dict) -> float | None:
    """Сколько суток с последнего визита. None = даты нет, не трогаем."""
    dt = last_visit_at(user)
    if not dt:
        return None
    return max(0.0, (_now() - dt).total_seconds() / 86400.0)


def _any_truthy_progress(mapping) -> bool:
    if not isinstance(mapping, dict):
        return False
    return any(bool(v) for v in mapping.values())


def _nonempty_list_map(mapping) -> bool:
    if not isinstance(mapping, dict):
        return False
    for v in mapping.values():
        if isinstance(v, (list, tuple, set)) and len(v) > 0:
            return True
        if isinstance(v, dict) and v:
            return True
        if v and not isinstance(v, (list, dict)):
            return True
    return False


def ever_completed_assignment(user: dict) -> bool:
    """
    Хоть одно задание где угодно (уроки / огонь / курс / тест уровня…).
    Чат сам по себе заданием не считаем.
    """
    if user.get("assessment_done"):
        return True

    gp = user.get("grammar_progress") or {}
    if not isinstance(gp, dict):
        gp = {}
    if count_grammar_exercises_done(user) > 0:
        return True
    if gp.get("completed_topics"):
        return True
    if _any_truthy_progress(gp.get("grammar_test_passed") or {}):
        return True
    if _nonempty_list_map(gp.get("extra_done") or {}):
        return True
    if int(user.get("lessons_done") or 0) > 0:
        return True

    sync_vocab_counters(user)
    if int(user.get("words_learned") or 0) > 0:
        return True
    if int(user.get("phrases_learned") or 0) > 0:
        return True
    vp = user.get("vocabulary_progress") or {}
    if isinstance(vp, dict) and _any_truthy_progress(vp.get("final_test_passed") or {}):
        return True

    if _count_listening_topics(user) > 0:
        return True
    if _count_reading_topics(user) > 0:
        return True

    street = (user.get("street_talk") or {}).get("progress") or {}
    if _any_truthy_progress(street):
        return True

    fire_seen = user.get("daily_fire_seen") or {}
    if _nonempty_list_map(fire_seen):
        return True

    path = user.get("path") or {}
    if isinstance(path, dict):
        if path.get("last_done"):
            return True
        if int(path.get("lesson") or 1) > 1:
            return True

    a0 = user.get("a0_pilot") or {}
    if isinstance(a0, dict) and a0.get("finished"):
        return True

    course = user.get("course") or {}
    if isinstance(course, dict):
        placement = course.get("placement") or {}
        if isinstance(placement, dict) and placement.get("finished"):
            return True

    secret = user.get("secret_missions") or {}
    if isinstance(secret, dict) and secret.get("done"):
        return True

    return False


def _has_paid_or_boost(user: dict) -> bool:
    if user_plan(user) != "free":
        return True
    now = _now().timestamp()
    for key in ("premium_until", "chat_until", "lessons_until", "sections_unlock_until"):
        if float(user.get(key) or 0) > now:
            return True
    return False


def is_idle_purge_candidate(uid: str, user: dict, *, idle_days: int = DEFAULT_IDLE_DAYS) -> bool:
    if str(uid) == str(MANAGER_ID):
        return False
    if str(uid).startswith("__"):
        return False
    if user.get("imitating_registration"):
        return False
    if _has_paid_or_boost(user):
        return False
    if ever_completed_assignment(user):
        return False
    days = days_since_visit(user)
    if days is None:
        return False
    return days >= float(idle_days)


def list_idle_purge_candidates(*, idle_days: int = DEFAULT_IDLE_DAYS) -> list[tuple[str, dict, float]]:
    """[(uid, user, days_inactive), ...] от самых старых."""
    out: list[tuple[str, dict, float]] = []
    for uid, u in _iter_users(persist_backfill=False):
        if not is_idle_purge_candidate(uid, u, idle_days=idle_days):
            continue
        days = days_since_visit(u) or float(idle_days)
        out.append((uid, u, days))
    out.sort(key=lambda x: -x[2])
    return out


def format_idle_purge_preview(*, idle_days: int = DEFAULT_IDLE_DAYS, limit: int = 40) -> str:
    rows = list_idle_purge_candidates(idle_days=idle_days)
    lines = [
        "🧹 <b>Чистка неактивных</b>\n",
        f"Критерий: не заходили ≥ <b>{idle_days}</b> дн. "
        "и ни одного задания (уроки / огонь / курс / тест уровня).\n",
        "Не трогаем: админ, платные/триал, сервисные ключи.\n",
        f"Кандидатов: <b>{len(rows)}</b>\n",
    ]
    if not rows:
        lines.append("Некого удалять.")
        return "\n".join(lines)

    for uid, u, days in rows[:limit]:
        visit = last_visit_at(u)
        when = visit.strftime("%Y-%m-%d") if visit else "?"
        lines.append(
            f"• <code>{uid}</code> {_name(u)} · ~{int(days)}д · last {when}"
        )
    if len(rows) > limit:
        lines.append(f"\n…и ещё {len(rows) - limit}")
    lines.append(
        "\nУдалить: <code>/purge_idle confirm</code>\n"
        "Только превью: <code>/purge_idle</code>"
    )
    return "\n".join(lines)


def purge_idle_users(*, idle_days: int = DEFAULT_IDLE_DAYS) -> dict:
    rows = list_idle_purge_candidates(idle_days=idle_days)
    ids = [uid for uid, _u, _d in rows]
    deleted = delete_users(ids) if ids else 0
    return {
        "candidates": len(ids),
        "deleted": deleted,
        "ids": ids,
        "idle_days": idle_days,
    }
