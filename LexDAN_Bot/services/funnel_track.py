"""Лёгкий трекинг воронки + снимок placement-теста (для выгрузки в файл)."""

from __future__ import annotations

import time
from typing import Any


def ensure_funnel(user: dict) -> dict:
    f = user.get("funnel")
    if not isinstance(f, dict):
        f = {}
        user["funnel"] = f
    f.setdefault("events", [])
    f.setdefault("chat_cta_sent", False)
    f.setdefault("chat_opened_after_cta", False)
    f.setdefault("chat_msgs_after_cta", 0)
    f.setdefault("listen_cta_sent", False)
    f.setdefault("listen_opened_after_cta", False)
    return f


def record_event(user: dict, name: str, **meta: Any) -> None:
    """Append-only, capped. Не ломает существующие поля."""
    f = ensure_funnel(user)
    ev = {"t": time.time(), "e": str(name)}
    if meta:
        ev["m"] = {k: v for k, v in meta.items() if v is not None}
    events = list(f.get("events") or [])
    events.append(ev)
    f["events"] = events[-80:]


def ensure_placement(user: dict) -> dict:
    p = user.get("placement")
    if not isinstance(p, dict):
        p = {}
        user["placement"] = p
    return p


def note_placement(user: dict, **fields: Any) -> None:
    p = ensure_placement(user)
    for k, v in fields.items():
        if v is not None:
            p[k] = v
