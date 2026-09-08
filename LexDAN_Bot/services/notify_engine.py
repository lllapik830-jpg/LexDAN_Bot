"""Движок уведомлений: кандидаты, приоритет, отправка."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services.database import get_user, load_users, save_users
from services.growth import ensure_growth, is_premium
from services.notify_copy import (
    EXCLUSIVE_PACKS,
    FREE_REMIND,
    FREE_REVIEW,
    FREE_TRIAL_DISCOUNT,
    FREE_TRIAL_LIFETIME,
    FREE_VOICE,
    PAID_EXCL,
    PAID_PLAN,
    PAID_STATS,
    PAID_STREAK_VOICE,
)
from services.notify_state import (
    P_FREE_REMIND,
    P_PAID_EXCL,
    P_PAID_PLAN,
    P_PAID_STATS,
    P_REVIEW,
    P_STREAK_VOICE,
    P_TRIAL_END,
    P_VOICE_MISS,
    already_sent_today,
    carousel_pick,
    days_inactive,
    ensure_notify,
    iso_week_id,
    mark_sent,
    mark_voice_sent,
    now_msk,
    today_msk,
    user_hour_slot,
    voice_ok,
    was_active_today,
    yesterday_msk,
)
from services.promo import has_lifetime_full_price
from services.rewards import user_plan

log = logging.getLogger(__name__)


@dataclass
class Candidate:
    kind: str
    priority: int
    text: str = ""
    voice: bool = False
    kb: InlineKeyboardMarkup | None = None
    prep: Callable[[dict], None] | None = None
    # Текст/карусель только у победителя — иначе крутятся все кандидаты зря.
    fill: Callable[[dict], str] | None = None


def _kb(rows: list[list[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
    out = list(rows)
    out.append([InlineKeyboardButton(text="🏠 В меню", callback_data="ntf:menu")])
    return InlineKeyboardMarkup(inline_keyboard=out)


def _topic_completed_yesterday(user: dict) -> tuple[str, str, str] | None:
    from data.grammar_curriculum import get_topic
    from services.grammar_review import completed_practice_topics

    dates = user.get("topic_completed_at")
    if not isinstance(dates, dict):
        return None
    y = yesterday_msk()
    keys = [k for k, d in dates.items() if str(d)[:10] == y]
    if not keys:
        return None
    practice = {(lv, tid): title for lv, tid, title in completed_practice_topics(user)}
    for key in reversed(keys):
        if ":" not in str(key):
            continue
        level, tid = str(key).split(":", 1)
        if (level, tid) in practice:
            return level, tid, practice[(level, tid)]
        topic = get_topic(level, tid)
        if topic:
            return level, tid, topic.get("title") or tid
    return None


def _pick_plan(user: dict) -> tuple[str, dict]:
    from data.grammar_curriculum import get_topics
    from services.lesson_state import ensure_progress, progress_key

    ensure_progress(user)
    level = (user.get("level") or "A1").strip() or "A1"
    done = set(user["grammar_progress"].get("completed_topics") or [])
    for t in get_topics(level) or []:
        tid = t.get("id") or ""
        if not tid:
            continue
        if progress_key(level, tid) in done:
            continue
        title = t.get("title") or tid
        return (
            f"Добей тему Grammar «{title}»",
            {"action": "grammar", "level": level, "topic_id": tid, "title": title},
        )
    return "Открой Огонь дня — коротко и полезно", {"action": "fire"}


def _stats_snapshot(user: dict) -> tuple[int, int, int, int]:
    ntf = ensure_notify(user)
    win = ntf.get("stats_window") if isinstance(ntf.get("stats_window"), dict) else {}
    tasks = int(win.get("tasks") or 0)
    words = int(win.get("words") or 0)
    w = user.get("notify_week") if isinstance(user.get("notify_week"), dict) else {}
    if tasks <= 0:
        tasks = int(w.get("tasks") or 0)
    if words <= 0:
        words = int(w.get("words") or 0)
    streak = int(user.get("streak") or 0)
    pct = 15 if tasks + words >= 10 else (35 if tasks + words >= 3 else 55)
    return tasks, words, streak, pct


def _excl_pack(user: dict) -> dict | None:
    ntf = ensure_notify(user)
    wid = iso_week_id()
    if ntf.get("last_excl_week") == wid:
        return None
    if not EXCLUSIVE_PACKS:
        return None
    try:
        week_num = int(wid.split("W")[-1])
    except Exception:
        week_num = 0
    return EXCLUSIVE_PACKS[week_num % len(EXCLUSIVE_PACKS)]


def _is_trial_ending(user: dict) -> bool:
    from services.trial_last_day import is_trial_access_user, premium_seconds_left

    if not is_trial_access_user(user) or not is_premium(user):
        return False
    left = premium_seconds_left(user)
    return 0 < left <= 24 * 3600


def build_candidate(uid: str, user: dict, hour: int) -> Candidate | None:
    ensure_growth(user)
    ensure_notify(user)
    if user.get("tg_blocked"):
        return None
    if not user.get("name") or user.get("step") != "ready":
        return None
    if user.get("imitating_registration"):
        return None
    if already_sent_today(user):
        return None
    if was_active_today(user):
        return None

    plan = user_plan(user)
    inactive = days_inactive(user)
    cands: list[Candidate] = []

    # ── Триал заканчивается ──
    if _is_trial_ending(user):
        ntf = ensure_notify(user)
        if ntf.get("trial_offer_date") != today_msk():
            lifetime = has_lifetime_full_price(user)

            def fill_trial(u: dict, _life=lifetime) -> str:
                variants = FREE_TRIAL_LIFETIME if _life else FREE_TRIAL_DISCOUNT
                key = "trial_life" if _life else "trial_disc"
                text, _ = carousel_pick(u, key, variants)
                return text

            def prep_trial(u: dict, _life=lifetime) -> None:
                ensure_notify(u)["trial_offer_date"] = today_msk()
                if not _life:
                    from services.trial_last_day import apply_last_day_discount

                    apply_last_day_discount(u)

            cands.append(
                Candidate(
                    "trial_end",
                    P_TRIAL_END,
                    kb=_kb(
                        [
                            [
                                InlineKeyboardButton(
                                    text="💳 Оформить доступ",
                                    callback_data="ntf:tariff",
                                )
                            ]
                        ]
                    ),
                    prep=prep_trial,
                    fill=fill_trial,
                )
            )

    # ── Голос «куда пропал» (free/chat, 2–3+ дня) ──
    if plan != "full" and inactive >= 2.0 and voice_ok(user):
        if 11 <= hour <= 20:

            def fill_voice(u: dict) -> str:
                text, _ = carousel_pick(u, "free_voice", FREE_VOICE)
                return text

            cands.append(
                Candidate(
                    "free_voice",
                    P_VOICE_MISS,
                    voice=True,
                    fill=fill_voice,
                )
            )

    # ── Повтор темы ──
    topic = _topic_completed_yesterday(user)
    if topic and inactive >= 0.5:
        level, tid, title = topic

        def fill_rev(u: dict, _title=title) -> str:
            tmpl, _ = carousel_pick(u, "free_review", FREE_REVIEW)
            return tmpl.format(topic=_title)

        def prep_rev(u: dict, _lv=level, _tid=tid, _title=title) -> None:
            ensure_notify(u)["pending_review"] = {
                "level": _lv,
                "topic_id": _tid,
                "title": _title,
            }

        cands.append(
            Candidate(
                "review",
                P_REVIEW,
                kb=_kb(
                    [
                        [
                            InlineKeyboardButton(
                                text="🔁 Повторить тему",
                                callback_data=f"ntf:review:{level}:{tid}",
                            )
                        ]
                    ]
                ),
                prep=prep_rev,
                fill=fill_rev,
            )
        )

    # ── Free remind (≥1 день) ──
    if plan != "full" and inactive >= 1.0:
        slot = user_hour_slot(uid, morning=True)
        slot2 = user_hour_slot(uid, morning=False)
        if hour in (slot, slot2) or (11 <= hour <= 13) or (17 <= hour <= 19):

            def fill_remind(u: dict) -> str:
                text, _ = carousel_pick(u, "free_remind", FREE_REMIND)
                return text

            cands.append(
                Candidate(
                    "free_remind",
                    P_FREE_REMIND,
                    kb=_kb(
                        [
                            [
                                InlineKeyboardButton(
                                    text="🔥 Огонь дня", callback_data="ntf:fire"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="▶️ Продолжить", callback_data="ntf:cont"
                                )
                            ],
                        ]
                    ),
                    fill=fill_remind,
                )
            )

    # ── Paid: план дня ~12:00 ──
    if plan == "full" and inactive >= 0.2:
        if hour == 12 or (hour == user_hour_slot(uid, morning=True)):
            plan_text, payload = _pick_plan(user)

            def fill_plan(u: dict, _pt=plan_text) -> str:
                tmpl, _ = carousel_pick(u, "paid_plan", PAID_PLAN)
                return tmpl.format(plan=_pt)

            def prep_plan(u: dict, _p=payload) -> None:
                ensure_notify(u)["pending_plan"] = _p

            cands.append(
                Candidate(
                    "paid_plan",
                    P_PAID_PLAN,
                    kb=_kb(
                        [
                            [
                                InlineKeyboardButton(
                                    text="▶️ Начать", callback_data="ntf:plan"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="🔥 Огонь дня", callback_data="ntf:fire"
                                )
                            ],
                        ]
                    ),
                    prep=prep_plan,
                    fill=fill_plan,
                )
            )

    # ── Paid: голос за streak ──
    if plan == "full" and int(user.get("streak") or 0) >= 5 and voice_ok(user):
        ntf = ensure_notify(user)
        wid = iso_week_id()
        if ntf.get("last_streak_voice_week") != wid and 12 <= hour <= 19:

            def fill_sv(u: dict) -> str:
                name = (u.get("name") or "друг").strip() or "друг"
                tmpl, _ = carousel_pick(u, "paid_streak_voice", PAID_STREAK_VOICE)
                return tmpl.format(name=name, streak=int(u.get("streak") or 0))

            def prep_sv(u: dict, _w=wid) -> None:
                ensure_notify(u)["last_streak_voice_week"] = _w

            cands.append(
                Candidate(
                    "paid_streak_voice",
                    P_STREAK_VOICE,
                    voice=True,
                    prep=prep_sv,
                    fill=fill_sv,
                )
            )

    # ── Paid: статистика раз в 3 дня ~18:00 ──
    if plan == "full" and hour == 18:
        ntf = ensure_notify(user)
        last = str(ntf.get("last_stats_date") or "")
        due = True
        if last:
            try:
                from datetime import date

                d0 = date.fromisoformat(last)
                due = (now_msk().date() - d0).days >= 3
            except Exception:
                due = True
        if due:
            tasks, words, streak, pct = _stats_snapshot(user)

            def fill_st(u: dict, _t=tasks, _w=words, _s=streak, _p=pct) -> str:
                tmpl, _ = carousel_pick(u, "paid_stats", PAID_STATS)
                return tmpl.format(tasks=_t, words=_w, streak=_s, pct=_p)

            def prep_st(u: dict) -> None:
                ensure_notify(u)["last_stats_date"] = today_msk()
                ensure_notify(u)["stats_window"] = {
                    "tasks": 0,
                    "words": 0,
                    "since": today_msk(),
                }

            cands.append(
                Candidate(
                    "paid_stats",
                    P_PAID_STATS,
                    kb=_kb(
                        [
                            [
                                InlineKeyboardButton(
                                    text="▶️ Продолжить", callback_data="ntf:cont"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="📊 Профиль", callback_data="ntf:profile"
                                )
                            ],
                        ]
                    ),
                    prep=prep_st,
                    fill=fill_st,
                )
            )

    # ── Paid: еженедельный эксклюзив (ср 15:00) ──
    if plan == "full" and hour == 15 and now_msk().weekday() == 2:
        pack = _excl_pack(user)
        if pack:

            def fill_ex(u: dict, _title=pack.get("title") or "бонус") -> str:
                tmpl, _ = carousel_pick(u, "paid_excl", PAID_EXCL)
                return tmpl.format(title=_title)

            def prep_ex(u: dict, _id=pack.get("id") or "") -> None:
                n = ensure_notify(u)
                n["pending_excl"] = _id
                n["last_excl_week"] = iso_week_id()

            cands.append(
                Candidate(
                    "paid_excl",
                    P_PAID_EXCL,
                    kb=_kb(
                        [
                            [
                                InlineKeyboardButton(
                                    text="🎁 Открыть", callback_data="ntf:excl"
                                )
                            ]
                        ]
                    ),
                    prep=prep_ex,
                    fill=fill_ex,
                )
            )

    if not cands:
        return None
    cands.sort(key=lambda c: -c.priority)
    winner = cands[0]
    if winner.fill:
        winner.text = winner.fill(user)
    return winner


async def send_due_notifications(bot, *, limit: int = 40) -> dict[str, Any]:
    """Главный тик: выбрать и отправить до limit уведомлений."""
    from services.elevenlabs import send_rico_voice
    from services.notify_week import finalize_week_and_notify

    hour = now_msk().hour
    # Сначала попытка недельных итогов (пн 18:00)
    week_res = await finalize_week_and_notify(bot)

    users = load_users()
    sent = 0
    fail = 0
    touched: list[str] = []

    for uid, raw in list(users.items()):
        if sent >= limit:
            break
        if not isinstance(raw, dict) or str(uid).startswith("__"):
            continue
        user = get_user(users, str(uid))
        ensure_growth(user)
        cand = build_candidate(str(uid), user, hour)
        if not cand:
            continue
        try:
            if cand.prep:
                cand.prep(user)
            if cand.voice:
                class _MsgProxy:
                    def __init__(self, b, chat_id: int):
                        self._bot = b
                        self._chat_id = int(chat_id)

                    async def answer(self, *a, **k):
                        return await self._bot.send_message(self._chat_id, *a, **k)

                    async def answer_voice(self, *a, **k):
                        return await self._bot.send_voice(self._chat_id, *a, **k)

                    async def answer_audio(self, *a, **k):
                        return await self._bot.send_audio(self._chat_id, *a, **k)

                ok = await send_rico_voice(
                    _MsgProxy(bot, int(uid)),
                    cand.text,
                    user=user,
                    title="Рико",
                )
                if not ok:
                    await bot.send_message(int(uid), f"🦜 {cand.text}")
                mark_voice_sent(user)
            else:
                await bot.send_message(
                    int(uid),
                    cand.text,
                    parse_mode="HTML",
                    reply_markup=cand.kb,
                )
            mark_sent(user, cand.kind)
            sent += 1
            touched.append(str(uid))
        except Exception as e:
            log.warning("notify fail uid=%s kind=%s: %s", uid, cand.kind, e)
            err = str(e).lower()
            if "blocked" in err or "deactivated" in err or "forbidden" in err:
                user["tg_blocked"] = True
                touched.append(str(uid))
            fail += 1

    if touched:
        save_users(users, only=list(dict.fromkeys(touched)))
    return {
        "ok": True,
        "sent": sent,
        "fail": fail,
        "week": week_res,
    }


def bump_stats_task(user: dict, n: int = 1) -> None:
    ntf = ensure_notify(user)
    win = ntf.get("stats_window")
    if not isinstance(win, dict):
        win = {"tasks": 0, "words": 0, "since": today_msk()}
        ntf["stats_window"] = win
    win["tasks"] = int(win.get("tasks") or 0) + n


def bump_stats_words(user: dict, n: int = 1) -> None:
    ntf = ensure_notify(user)
    win = ntf.get("stats_window")
    if not isinstance(win, dict):
        win = {"tasks": 0, "words": 0, "since": today_msk()}
        ntf["stats_window"] = win
    win["words"] = int(win.get("words") or 0) + n
