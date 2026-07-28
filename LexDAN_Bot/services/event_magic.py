"""Ивент «Магические элементы»: окно, баллы, топ-10, зал славы, призы."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any

log = logging.getLogger(__name__)

# Москва = UTC+3 (как в database.set_mode); без зависимости от tzdata на Windows
MSK = timezone(timedelta(hours=3))

EVENT_ID = "magic_elements_2026_07"
EVENT_TITLE = "Магические элементы"

# Старт уже начался (опоздание) — окно держим до EVENT_END.
EVENT_START = datetime(2026, 7, 29, 0, 0, 0, tzinfo=MSK)
EVENT_END = datetime(2026, 8, 5, 0, 0, 0, tzinfo=MSK)

EVENT_START_ANNOUNCE_TEXT = (
    "🦜✨ <b>Ивент «Магические элементы» начался!</b>\n\n"
    "Выполняй задания, открывай новые магические элементы "
    "и выигрывай призы! 🎴🏆\n\n"
    "⏰ Конец: <b>05.08 в 00:00</b> (МСК)\n\n"
    "📋 Подробные условия в канале:\n"
    "👉 https://t.me/LexDan_Rico"
)

POINTS_GRAMMAR = 0.5
POINTS_VOCAB = 2.0
POINTS_LISTENING = 5.0

BTN_LEADERBOARD = "🏆Гонка Лидеров🏆"
BTN_HALL_OF_FAME = "🏛️ Зал славы LexDan"

TITLE_PLACE_1 = "🏆 Легенда LexDan"
TITLE_PLACE_2 = "🥈 Мастер коллекции"
TITLE_PLACE_3 = "🥉 Охотник за картами"
TITLE_PLACE_4_10 = "📦 Коллекционер"

# place -> prize flags / counters (assets later)
PRIZE_BY_PLACE: dict[int, dict[str, Any]] = {
    1: {
        "title": TITLE_PLACE_1,
        "exclusive_tasks": 20,
        "custom_rico_art": True,
        "exclusive_voice": False,
        "voice_congrats": False,
        "sticker_pack": False,
        "sticker_single": False,
        "hall_of_fame": True,
    },
    2: {
        "title": TITLE_PLACE_2,
        "exclusive_tasks": 8,
        "custom_rico_art": False,
        "exclusive_voice": True,
        "voice_congrats": True,
        "sticker_pack": False,
        "sticker_single": False,
        "hall_of_fame": False,
    },
    3: {
        "title": TITLE_PLACE_3,
        "exclusive_tasks": 8,
        "custom_rico_art": False,
        "exclusive_voice": False,
        "voice_congrats": True,
        "sticker_pack": True,
        "sticker_single": False,
        "hall_of_fame": False,
    },
}

for _p in range(4, 11):
    PRIZE_BY_PLACE[_p] = {
        "title": TITLE_PLACE_4_10,
        "exclusive_tasks": 0,
        "custom_rico_art": False,
        "exclusive_voice": False,
        "voice_congrats": False,
        "sticker_pack": False,
        "sticker_single": True,
        "hall_of_fame": False,
    }

_STATE_FILE = "magic_event_state.json"
_META_KEY = "magic_event"


def now_msk() -> datetime:
    return datetime.now(MSK)


def _use_postgres() -> bool:
    return bool((os.getenv("DATABASE_URL") or "").strip())


def _default_state() -> dict:
    return {
        "force_active": False,
        "finalized": False,
        "finalized_at": "",
        "frozen_top": [],
        "hall_of_fame": [],
        "announce_sent": False,
    }


def load_event_state() -> dict:
    if _use_postgres():
        try:
            return _load_state_pg()
        except Exception as e:
            log.error("magic event state pg load failed: %s", e)
    return _load_state_file()


def save_event_state(state: dict) -> None:
    if _use_postgres():
        try:
            _save_state_pg(state)
            return
        except Exception as e:
            log.error("magic event state pg save failed: %s", e)
    _save_state_file(state)


def _load_state_file() -> dict:
    if not os.path.exists(_STATE_FILE):
        return _default_state()
    try:
        with open(_STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return _default_state()
        out = _default_state()
        out.update(data)
        if not isinstance(out.get("frozen_top"), list):
            out["frozen_top"] = []
        if not isinstance(out.get("hall_of_fame"), list):
            out["hall_of_fame"] = []
        return out
    except (json.JSONDecodeError, OSError):
        return _default_state()


def _save_state_file(state: dict) -> None:
    with open(_STATE_FILE, "w", encoding="utf-8") as f:
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


def _load_state_pg() -> dict:
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            _ensure_meta_table(cur)
            cur.execute("SELECT data FROM app_meta WHERE key = %s", (_META_KEY,))
            row = cur.fetchone()
        conn.commit()
    if not row:
        return _default_state()
    data = row[0]
    if not isinstance(data, dict):
        data = json.loads(data)
    out = _default_state()
    out.update(data)
    if not isinstance(out.get("frozen_top"), list):
        out["frozen_top"] = []
    if not isinstance(out.get("hall_of_fame"), list):
        out["hall_of_fame"] = []
    return out


def _save_state_pg(state: dict) -> None:
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            _ensure_meta_table(cur)
            cur.execute(
                """
                INSERT INTO app_meta (key, data, updated_at)
                VALUES (%s, %s::jsonb, now())
                ON CONFLICT (key) DO UPDATE SET
                    data = EXCLUDED.data,
                    updated_at = now()
                """,
                (_META_KEY, json.dumps(state, ensure_ascii=False)),
            )
        conn.commit()


def in_scheduled_window(when: datetime | None = None) -> bool:
    t = when or now_msk()
    return EVENT_START <= t < EVENT_END


def is_event_active(state: dict | None = None) -> bool:
    """Окно ивента или force_active (для теста до/после)."""
    st = state if state is not None else load_event_state()
    if st.get("force_active"):
        return True
    return in_scheduled_window()


def is_event_ended(state: dict | None = None) -> bool:
    st = state if state is not None else load_event_state()
    if st.get("finalized"):
        return True
    return now_msk() >= EVENT_END and not st.get("force_active")


def ensure_user_event(user: dict) -> dict:
    if "magic_event" not in user or not isinstance(user.get("magic_event"), dict):
        user["magic_event"] = {}
    me = user["magic_event"]
    if me.get("event_id") != EVENT_ID:
        # новый ивент — обнуляем очки (титул/призы прошлых не трогаем)
        me["event_id"] = EVENT_ID
        me["points"] = 0.0
        me["grammar"] = 0.0
        me["vocab"] = 0.0
        me["listening"] = 0.0
    me.setdefault("points", 0.0)
    me.setdefault("grammar", 0.0)
    me.setdefault("vocab", 0.0)
    me.setdefault("listening", 0.0)
    return me


def get_points(user: dict) -> float:
    me = ensure_user_event(user)
    try:
        return float(me.get("points") or 0)
    except (TypeError, ValueError):
        return 0.0


def can_show_points(user: dict) -> bool:
    from services.collection import is_complete

    return is_complete(user)


def add_points(user: dict, amount: float, *, kind: str) -> float:
    """
    Начислить баллы, если ивент активен и ещё не финализирован.
    Возвращает новое значение points (или текущее, если не начислили).
    """
    state = load_event_state()
    if state.get("finalized"):
        return get_points(user)
    if not is_event_active(state):
        return get_points(user)
    me = ensure_user_event(user)
    me["points"] = float(me.get("points") or 0) + float(amount)
    if kind in ("grammar", "vocab", "listening"):
        me[kind] = float(me.get(kind) or 0) + float(amount)
    return float(me["points"])


def add_grammar_points(user: dict) -> float:
    return add_points(user, POINTS_GRAMMAR, kind="grammar")


def add_vocab_points(user: dict) -> float:
    return add_points(user, POINTS_VOCAB, kind="vocab")


def add_listening_points(user: dict) -> float:
    return add_points(user, POINTS_LISTENING, kind="listening")


def format_points(n: float) -> str:
    if abs(n - round(n)) < 1e-9:
        return str(int(round(n)))
    return f"{n:.1f}".rstrip("0").rstrip(".")


def _display_name(user: dict, user_id: str) -> str:
    name = (user.get("name") or "").strip()
    if name:
        return name
    return f"id{user_id}"


def _username_label(user: dict) -> str:
    un = (user.get("tg_username") or "").strip().lstrip("@")
    if un:
        return f"@{un}"
    return ""


def remember_tg_username(user: dict, username: str | None) -> None:
    if username:
        user["tg_username"] = str(username).lstrip("@")


def build_live_top(users: dict, *, limit: int = 10) -> list[dict]:
    rows: list[dict] = []
    for uid, payload in users.items():
        if not isinstance(payload, dict):
            continue
        if str(uid).startswith("__"):
            continue
        me = payload.get("magic_event")
        if not isinstance(me, dict) or me.get("event_id") != EVENT_ID:
            continue
        try:
            pts = float(me.get("points") or 0)
        except (TypeError, ValueError):
            pts = 0.0
        if pts <= 0:
            continue
        rows.append(
            {
                "user_id": str(uid),
                "points": pts,
                "name": _display_name(payload, str(uid)),
                "username": (payload.get("tg_username") or "").strip().lstrip("@"),
            }
        )
    rows.sort(key=lambda r: (-float(r["points"]), str(r["user_id"])))
    out = []
    for i, r in enumerate(rows[:limit], start=1):
        r = dict(r)
        r["place"] = i
        out.append(r)
    return out


def get_leaderboard_rows(users: dict | None = None) -> tuple[list[dict], bool]:
    """
    Returns (rows, is_frozen).
    After finalize — frozen snapshot; else live top.
    """
    state = load_event_state()
    if state.get("finalized") and state.get("frozen_top"):
        return list(state["frozen_top"]), True
    if users is None:
        from services.database import load_users

        users = load_users()
    return build_live_top(users), False


def format_leaderboard_text_for(
    user: dict, user_id: str, users: dict | None = None
) -> str:
    if users is None:
        from services.database import load_users

        users = load_users()
    rows, frozen = get_leaderboard_rows(users)
    lines = [
        f"🏆 <b>Лидеры ивента «{EVENT_TITLE}»</b>\n",
    ]
    if frozen:
        lines.append("<i>Итоги подведены</i>\n")
    elif is_event_active():
        lines.append("<i>Ивент идёт — топ обновляется</i>\n")
    else:
        if now_msk() < EVENT_START:
            lines.append("<i>Ивент ещё не стартовал</i>\n")
        else:
            lines.append("<i>Ивент завершён</i>\n")

    if not rows:
        lines.append("Пока никого в топе — будь первым!")
    else:
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        for r in rows:
            place = int(r.get("place") or 0)
            medal = medals.get(place, f"{place}.")
            un = (r.get("username") or "").strip()
            name = r.get("name") or r.get("user_id")
            who = f"@{un}" if un else name
            pts = format_points(float(r.get("points") or 0))
            mark = " ← ты" if str(r.get("user_id")) == str(user_id) else ""
            lines.append(f"{medal} {who} — <b>{pts}</b>{mark}")

    lines.append("")
    if can_show_points(user):
        my = format_points(get_points(user))
        place = _place_of(user_id, users, frozen_rows=rows if frozen else None)
        if place:
            lines.append(f"Ты: <b>{my}</b> балл. · место <b>{place}</b>")
        else:
            lines.append(f"Твои баллы: <b>{my}</b>")
    else:
        lines.append(
            "🔒 Твои баллы откроются, когда соберёшь все 15 элементов."
        )
    return "\n".join(lines)


def _place_of(
    user_id: str, users: dict, *, frozen_rows: list[dict] | None = None
) -> int | None:
    if frozen_rows is not None:
        for r in frozen_rows:
            if str(r.get("user_id")) == str(user_id):
                return int(r.get("place") or 0) or None
        return None
    all_rows = build_live_top(users, limit=10_000)
    for r in all_rows:
        if str(r.get("user_id")) == str(user_id):
            return int(r.get("place") or 0) or None
    return None


def format_hall_of_fame_text() -> str:
    state = load_event_state()
    entries = list(state.get("hall_of_fame") or [])
    lines = [
        "🏛️ <b>Зал славы LexDan</b>\n",
        "Победители ивентов (1 место):\n",
    ]
    if not entries:
        lines.append("Пока пусто — первый чемпион появится после итогов.")
        return "\n".join(lines)

    # wins total per user_id
    wins: dict[str, int] = {}
    for e in entries:
        uid = str(e.get("user_id") or "")
        wins[uid] = wins.get(uid, 0) + 1

    # chronological (as stored); show last win date per row = that event's won_at
    for e in entries:
        uid = str(e.get("user_id") or "")
        un = (e.get("username") or "").strip().lstrip("@")
        who = f"@{un}" if un else (e.get("name") or uid)
        title = e.get("title") or TITLE_PLACE_1
        won_at = e.get("won_at") or "—"
        event_title = e.get("event_title") or EVENT_TITLE
        total = wins.get(uid, 1)
        lines.append(
            f"• <b>{event_title}</b>\n"
            f"  {who} — {title}\n"
            f"  Побед: <b>{total}</b> · Дата победы: <b>{won_at}</b>"
        )
    return "\n".join(lines)


def profile_title_line(user: dict) -> str:
    title = (user.get("profile_title") or "").strip()
    if not title:
        return ""
    return f"🎖 {title}\n"


def grant_prize_to_user(user: dict, place: int, *, event_id: str = EVENT_ID) -> dict:
    prize = dict(PRIZE_BY_PLACE.get(int(place)) or {})
    if not prize:
        return {}
    user["profile_title"] = prize.get("title") or ""
    ep = user.get("event_prizes")
    if not isinstance(ep, dict):
        ep = {}
    ep["event_id"] = event_id
    ep["place"] = int(place)
    ep["title"] = prize.get("title")
    ep["exclusive_tasks"] = int(prize.get("exclusive_tasks") or 0)
    ep["exclusive_tasks_remaining"] = int(prize.get("exclusive_tasks") or 0)
    ep["custom_rico_art"] = bool(prize.get("custom_rico_art"))
    ep["exclusive_voice"] = bool(prize.get("exclusive_voice"))
    ep["voice_congrats"] = bool(prize.get("voice_congrats"))
    ep["sticker_pack"] = bool(prize.get("sticker_pack"))
    ep["sticker_single"] = bool(prize.get("sticker_single"))
    user["event_prizes"] = ep
    return prize


def finalize_event(
    users: dict | None = None, *, force: bool = False
) -> dict[str, Any]:
    """
    Зафиксировать топ-10, выдать призы, записать 1 место в зал славы.
    Идемпотентно: повторный вызов без force не перезаписывает.
    """
    state = load_event_state()
    if state.get("finalized") and not force:
        return {"ok": True, "already": True, "top": state.get("frozen_top") or []}

    if users is None:
        from services.database import load_users

        users = load_users()

    top = build_live_top(users, limit=10)
    state["frozen_top"] = top
    state["finalized"] = True
    state["finalized_at"] = now_msk().isoformat()
    state["force_active"] = False

    touched: list[str] = []
    for r in top:
        uid = str(r.get("user_id") or "")
        place = int(r.get("place") or 0)
        user = users.get(uid)
        if not isinstance(user, dict) or place < 1:
            continue
        prize = grant_prize_to_user(user, place, event_id=EVENT_ID)
        touched.append(uid)
        if prize.get("hall_of_fame") and place == 1:
            won_at = now_msk().strftime("%d.%m.%Y")
            state.setdefault("hall_of_fame", []).append(
                {
                    "event_id": EVENT_ID,
                    "event_title": EVENT_TITLE,
                    "user_id": uid,
                    "username": (r.get("username") or user.get("tg_username") or ""),
                    "name": r.get("name") or _display_name(user, uid),
                    "title": prize.get("title") or TITLE_PLACE_1,
                    "won_at": won_at,
                }
            )

    save_event_state(state)
    if touched:
        from services.database import save_users

        save_users(users, only=touched)
    log.info("Magic event finalized: top=%s touched=%s", len(top), len(touched))
    return {"ok": True, "already": False, "top": top, "touched": touched}


def maybe_auto_finalize() -> dict | None:
    """Вызвать из фонового цикла: если окно закончилось и ещё не финализировали."""
    state = load_event_state()
    if state.get("finalized"):
        return None
    if state.get("force_active"):
        return None
    if now_msk() < EVENT_END:
        return None
    return finalize_event()


def set_force_active(on: bool) -> dict:
    state = load_event_state()
    state["force_active"] = bool(on)
    if on:
        # для теста снимаем finalized, чтобы снова копить баллы
        state["finalized"] = False
    save_event_state(state)
    return state


def status_text() -> str:
    state = load_event_state()
    active = is_event_active(state)
    return (
        f"🎴 <b>{EVENT_TITLE}</b>\n"
        f"id: <code>{EVENT_ID}</code>\n"
        f"Конец: <b>{EVENT_END.strftime('%d.%m.%Y %H:%M')}</b> МСК\n"
        f"Сейчас МСК: {now_msk().strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"Активен (дропы/баллы): {'да' if active else 'нет'}\n"
        f"force_active: {'да' if state.get('force_active') else 'нет'}\n"
        f"Финализирован: {'да' if state.get('finalized') else 'нет'}\n"
        f"Анонс разослан: {'да' if state.get('announce_sent') else 'нет'}\n"
        f"Записей в зале славы: {len(state.get('hall_of_fame') or [])}"
    )


def build_event_points_breakdown(users: dict | None = None) -> list[dict]:
    """Участники ивента с разбивкой баллов по Grammar / Vocab / Listening."""
    if users is None:
        from services.database import load_users

        users = load_users()
    rows: list[dict] = []
    for uid, payload in (users or {}).items():
        if not isinstance(payload, dict) or str(uid).startswith("__"):
            continue
        me = payload.get("magic_event")
        if not isinstance(me, dict) or me.get("event_id") != EVENT_ID:
            continue
        try:
            pts = float(me.get("points") or 0)
            g = float(me.get("grammar") or 0)
            v = float(me.get("vocab") or 0)
            li = float(me.get("listening") or 0)
        except (TypeError, ValueError):
            continue
        if pts <= 0 and g <= 0 and v <= 0 and li <= 0:
            continue
        rows.append(
            {
                "user_id": str(uid),
                "points": pts,
                "grammar": g,
                "vocab": v,
                "listening": li,
                "name": _display_name(payload, str(uid)),
                "username": (payload.get("tg_username") or "").strip().lstrip("@"),
            }
        )
    rows.sort(key=lambda r: (-float(r["points"]), str(r["user_id"])))
    return rows


def format_event_admin_chunks(*, limit_per_chunk: int = 35) -> list[str]:
    """Тексты для /event: статус + кто сколько набрал по типам заданий."""
    chunks = [status_text()]
    rows = build_event_points_breakdown()
    if not rows:
        chunks.append("📊 <b>Баллы участников</b>\nПока никто не набрал баллов.")
        return chunks

    header = (
        f"📊 <b>Баллы участников</b> ({len(rows)})\n"
        "<i>всего | Grammar | Vocab | Listening</i>\n"
    )
    lines: list[str] = []
    for i, r in enumerate(rows, start=1):
        un = (r.get("username") or "").strip()
        who = f"@{un}" if un else (r.get("name") or r.get("user_id"))
        lines.append(
            f"{i}. {who} <code>{r.get('user_id')}</code>\n"
            f"   ∑ {format_points(float(r['points']))} | "
            f"G {format_points(float(r['grammar']))} | "
            f"V {format_points(float(r['vocab']))} | "
            f"L {format_points(float(r['listening']))}"
        )

    buf = header
    for line in lines:
        candidate = buf + ("\n" if buf != header else "") + line
        if len(candidate) > 3500 or (
            buf != header and (buf.count("\n") // 2) >= limit_per_chunk
        ):
            chunks.append(buf)
            buf = header + line
        else:
            buf = candidate
    if buf.strip():
        chunks.append(buf)
    return chunks


async def broadcast_event_start(bot, *, force: bool = False) -> dict:
    """Разослать анонс старта всем пользователям бота (один раз, если не force)."""
    state = load_event_state()
    if state.get("announce_sent") and not force:
        return {"ok": False, "already": True, "sent": 0, "fail": 0}

    from services.database import load_users
    import asyncio

    users = load_users()
    sent = 0
    fail = 0
    for uid, payload in users.items():
        if not isinstance(payload, dict) or str(uid).startswith("__"):
            continue
        try:
            chat_id = int(uid)
        except (TypeError, ValueError):
            fail += 1
            continue
        try:
            await bot.send_message(
                chat_id, EVENT_START_ANNOUNCE_TEXT, parse_mode="HTML",
                disable_web_page_preview=True,
            )
            sent += 1
        except Exception as e:
            fail += 1
            log.warning("event announce fail uid=%s: %s", uid, e)
        await asyncio.sleep(0.05)

    state["announce_sent"] = True
    save_event_state(state)
    log.info("Event start announce: sent=%s fail=%s force=%s", sent, fail, force)
    return {"ok": True, "already": False, "sent": sent, "fail": fail}
