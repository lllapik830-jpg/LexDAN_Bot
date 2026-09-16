"""Состояние уведомлений на пользователе."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

MSK = timezone(timedelta(hours=3))

# Приоритеты (больше = важнее). В день уходит только один тип.
P_TRIAL_END = 100
P_ONBOARD_DRIP = 95
P_VOICE_MISS = 90
P_WEEK_RESULTS = 85
P_REVIEW = 80
P_STREAK_VOICE = 65
P_FREE_REMIND = 50
P_PAID_PLAN = 50
P_PAID_STATS = 40
P_PAID_EXCL = 35


def now_msk() -> datetime:
    return datetime.now(MSK)


def today_msk() -> str:
    return now_msk().date().isoformat()


def yesterday_msk() -> str:
    return (now_msk().date() - timedelta(days=1)).isoformat()


def iso_week_id(dt: datetime | None = None) -> str:
    d = (dt or now_msk()).date()
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def ensure_notify(user: dict) -> dict:
    raw = user.get("notify")
    if not isinstance(raw, dict):
        raw = {}
    raw.setdefault("carousel", {})
    raw.setdefault("sent_date", "")
    raw.setdefault("sent_type", "")
    raw.setdefault("last_voice_at", 0.0)
    raw.setdefault("last_stats_date", "")
    raw.setdefault("last_excl_week", "")
    raw.setdefault("last_streak_voice_week", "")
    raw.setdefault("trial_offer_date", "")
    raw.setdefault("pending_plan", {})
    raw.setdefault("pending_excl", "")
    raw.setdefault("pending_review", {})
    raw.setdefault("stats_window", {"tasks": 0, "words": 0, "since": today_msk()})
    user["notify"] = raw
    return raw


def carousel_pick(user: dict, kind: str, variants: tuple[str, ...] | list[str]) -> tuple[str, int]:
    ntf = ensure_notify(user)
    car = ntf["carousel"]
    if not isinstance(car, dict):
        car = {}
        ntf["carousel"] = car
    idx = int(car.get(kind) or 0) % max(1, len(variants))
    text = variants[idx]
    car[kind] = (idx + 1) % max(1, len(variants))
    return text, idx


def already_sent_today(user: dict) -> bool:
    ntf = ensure_notify(user)
    return str(ntf.get("sent_date") or "") == today_msk()


def mark_sent(user: dict, kind: str) -> None:
    ntf = ensure_notify(user)
    ntf["sent_date"] = today_msk()
    ntf["sent_type"] = kind


def _parse_last_active(user: dict) -> datetime | None:
    """last_active_at: ISO-строка (основной формат) или unix timestamp."""
    raw = user.get("last_active_at")
    if raw is None or raw == "":
        return None
    if isinstance(raw, (int, float)):
        try:
            ts = float(raw)
            if ts <= 0:
                return None
            return datetime.fromtimestamp(ts, tz=MSK)
        except Exception:
            return None
    s = str(raw).strip()
    if not s:
        return None
    try:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=MSK)
        return dt.astimezone(MSK)
    except Exception:
        return None


def was_active_today(user: dict) -> bool:
    dt = _parse_last_active(user)
    if not dt:
        return False
    return dt.date().isoformat() == today_msk()


def days_inactive(user: dict) -> float:
    """Сколько суток без активности по last_active_at. Нет метки → 0 (не пингуем вслепую)."""
    dt = _parse_last_active(user)
    if not dt:
        return 0.0
    return max(0.0, (now_msk() - dt).total_seconds() / 86400.0)


def voice_ok(user: dict, *, min_days: float = 3.5) -> bool:
    ntf = ensure_notify(user)
    last = float(ntf.get("last_voice_at") or 0)
    if last <= 0:
        return True
    return (now_msk().timestamp() - last) >= min_days * 86400


def mark_voice_sent(user: dict) -> None:
    ntf = ensure_notify(user)
    ntf["last_voice_at"] = now_msk().timestamp()


def user_hour_slot(uid: str, morning: bool = True) -> int:
    """Стабильный час для юзера (11–13 или 17–19)."""
    h = abs(hash(str(uid))) % 3
    return (11 + h) if morning else (17 + h)


def in_hour_window(hour: int, target: int, *, widen: int = 0) -> bool:
    return abs(int(hour) - int(target)) <= int(widen)
