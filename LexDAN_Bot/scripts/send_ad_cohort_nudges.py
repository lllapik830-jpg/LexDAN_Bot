"""
DEPRECATED: разовые волны по CSV-когорте.

Живые пинги по стадии онбординга теперь в notify_engine
(services/onboard_drip.py) — таймеры от захода каждого юзера,
новые люди подхватываются сами. Этот скрипт оставляем только
для ручного канала / dry-run текстов.

Сегментные пинги когорте рекламы 16.09 + пост в канал.

Запуск:
  set DATABASE_URL=...
  set BOT_TOKEN=...
  python scripts/send_ad_cohort_nudges.py --wave now
  python scripts/send_ad_cohort_nudges.py --wave cold
  python scripts/send_ad_cohort_nudges.py --channel-only
  python scripts/send_ad_cohort_nudges.py --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import logging
import os
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv

    for p in (ROOT / ".env", ROOT.parent / ".env"):
        if p.is_file():
            load_dotenv(p)
except Exception:
    pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("ad_nudges")

MANAGER_ID = "1809897303"
COHORT_SINCE = "2026-09-16"
FLAG_PREFIX = "ad_nudge_20260916"

# ── тексты ──────────────────────────────────────────────────────────

CHANNEL_POST_HTML = (
    "🦜 <b>Рико:</b> Сегодня в LexDAN уже <b>десятки людей</b> "
    "прошли тест уровня 🎯\n\n"
    "Кто-то только начал, кто-то уже поймал первую искру Огня дня "
    "и попробовал болтать с Рико.\n\n"
    "💚 15 минут в день — без стресса, в своём темпе.\n\n"
    "👉 Заходи в бота и проверь свой уровень:\n"
    "https://t.me/LexDAN_bot"
)

MSG_INTRO = (
    "🦜 <b>Рико:</b> Ты уже нажал Start — круто!\n\n"
    "Давай за <b>3–4 минуты</b> проверим уровень? "
    "После теста будет подарок: <b>3 дня безлимита</b> 🎁\n\n"
    "Открой бота и жми <b>🎯 Проверить уровень</b> 👇"
)

MSG_PRE_TEST = (
    "🦜 <b>Рико:</b> Мы уже почти знакомы!\n\n"
    "Осталось пройти короткий тест — "
    "перевод, слова и одно аудио. Минут 5–6.\n\n"
    "После него — <b>3 дня полного доступа</b>. "
    "Жми <b>✅ Погнали!</b> в боте 🚀"
)

MSG_DAILY_FIRE = (
    "🔥 <b>Рико:</b> Тест позади, одна искра Огня уже близко!\n\n"
    "Загляни в <b>🔥 Огонь дня</b>, поймай искру — "
    "дальше будет короткий кусочек темы <b>to be</b> "
    "(1 слайд + 1 задание).\n\n"
    "Это быстро, обещаю 💚"
)

MSG_TO_BE = (
    "🦜 <b>Рико:</b> Ты уже у темы <b>to be</b> — осталось совсем чуть-чуть!\n\n"
    "Один слайд и одно задание — и ты поймёшь, как устроены уроки.\n\n"
    "Открой бота и дожми 💪 Это 2–3 минуты."
)

MSG_DONE_NO_CHAT = (
    "🗣️ <b>Рико:</b> Ты уже прошёл знакомство — респект!\n\n"
    "Заходи в <b>Общаться</b>: я сразу предложу тему, "
    "а у тебя сейчас <b>безлимит на триале</b>.\n\n"
    "Напиши хоть одно предложение про свой день 💬 "
    "Именно на общении язык растёт быстрее всего."
)

MSG_CHATTED = (
    "🦜 <b>Рико:</b> Класс, что уже поболтали!\n\n"
    "Завтра зайди снова на минутку — так появляется привычка. "
    "Можно ещё заглянуть в <b>Listening</b> и выбрать тему сам 🎧\n\n"
    "Я на связи 💚"
)


def _kb_chat():
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗣️ Общаться", callback_data="ofu:chat")]
        ]
    )


def _kb_open_bot():
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🦜 Открыть бота",
                    url="https://t.me/LexDAN_bot",
                )
            ]
        ]
    )


def _day_start_ts(day: str) -> float:
    from datetime import timezone, timedelta

    d = datetime.strptime(day, "%Y-%m-%d")
    tz = timezone(timedelta(hours=3))
    return d.replace(tzinfo=tz).timestamp()


def load_cohort_from_db() -> list[tuple[str, dict]]:
    os.environ.setdefault("BOT_TOKEN", os.getenv("BOT_TOKEN") or "x")
    os.environ.setdefault("OPENROUTER_API_KEY", "x")
    os.environ.setdefault("ELEVENLABS_API_KEY", "x")
    from services.database import load_users, get_user
    from services.growth import ensure_growth

    since = _day_start_ts(COHORT_SINCE)
    users = load_users()
    out = []
    for uid, raw in users.items():
        if not isinstance(raw, dict) or str(uid).startswith("__"):
            continue
        if raw.get("imitating_registration"):
            continue
        ob = raw.get("onboard") if isinstance(raw.get("onboard"), dict) else {}
        if ob.get("imit") and ob.get("active"):
            continue
        u = get_user(users, str(uid))
        ensure_growth(u)
        ts = float(u.get("first_seen_at") or 0) or float(u.get("last_start_at") or 0)
        if ts < since:
            continue
        out.append((str(uid), u))
    return out


def segment(uid: str, u: dict) -> str | None:
    if uid == MANAGER_ID:
        return None
    stage = str((u.get("onboard") or {}).get("stage") or "")
    assessed = bool(u.get("assessment_done"))
    name = (u.get("name") or "").strip()
    chat_n = int(u.get("chat_text_total") or 0) + int(u.get("chat_voice_total") or 0)

    if not assessed and stage in {"", "intro"} and not name:
        return "intro"
    if not assessed and stage in {"pre_test", "intro"} and name:
        return "pre_test"
    if not assessed:
        return "pre_test" if name else "intro"
    if stage == "daily_fire":
        return "daily_fire"
    if stage in {"grammar_cta", "slides", "tasks", "tasks_menu"}:
        return "to_be"
    if stage == "done" or (assessed and stage in {"", "done"}):
        # done path: complete_guided sets stage done
        if chat_n <= 0:
            return "done_no_chat"
        return "chatted"
    # assessed but stage empty/weird — treat as mid
    if assessed and stage in {"daily_fire"}:
        return "daily_fire"
    if assessed:
        return "to_be"
    return None


SEGMENT_COPY = {
    "intro": (MSG_INTRO, "open_bot"),
    "pre_test": (MSG_PRE_TEST, "open_bot"),
    "daily_fire": (MSG_DAILY_FIRE, "open_bot"),
    "to_be": (MSG_TO_BE, "open_bot"),
    "done_no_chat": (MSG_DONE_NO_CHAT, "chat"),
    "chatted": (MSG_CHATTED, "open_bot"),
}

WAVES = {
    # утро — самый ценный недожим (после 10:00 МСК)
    "morning_hot": ("daily_fire", "to_be", "done_no_chat"),
    # день — холодные, кто не дошёл до теста
    "day_cold": ("intro", "pre_test"),
    # вечер — кто уже болтал + мягкий повтор done без чата
    "eve": ("chatted", "done_no_chat"),
}


def already_sent(u: dict, seg: str) -> bool:
    return bool(u.get(f"{FLAG_PREFIX}_{seg}"))


def mark_sent(u: dict, seg: str) -> None:
    u[f"{FLAG_PREFIX}_{seg}"] = True
    u[f"{FLAG_PREFIX}_{seg}_at"] = time.time()


async def send_channel(bot) -> dict:
    from config import CHANNEL_USERNAME

    channel = f"@{CHANNEL_USERNAME.lstrip('@')}"
    try:
        await bot.send_message(
            channel,
            CHANNEL_POST_HTML,
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
        return {"ok": True, "channel": channel}
    except Exception as e:
        return {"ok": False, "error": str(e), "channel": channel}


async def send_wave(bot, wave: str, *, dry: bool = False) -> dict:
    from services.database import save_users, users_for

    segs = WAVES[wave]
    cohort = load_cohort_from_db()
    buckets: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for uid, u in cohort:
        seg = segment(uid, u)
        if seg in segs:
            buckets[seg].append((uid, u))

    stats = {"wave": wave, "sent": 0, "skip": 0, "fail": 0, "by_seg": {}}
    for seg in segs:
        text, kb_kind = SEGMENT_COPY[seg]
        kb = _kb_chat() if kb_kind == "chat" else _kb_open_bot()
        n_ok = n_skip = n_fail = 0
        for uid, u in buckets.get(seg, []):
            if already_sent(u, seg) and wave != "eve":
                # eve may re-ping done_no_chat once with different flag
                n_skip += 1
                continue
            if wave == "eve" and seg == "done_no_chat" and u.get(f"{FLAG_PREFIX}_done_no_chat_eve"):
                n_skip += 1
                continue
            if dry:
                n_ok += 1
                continue
            try:
                await bot.send_message(
                    int(uid), text, parse_mode="HTML", reply_markup=kb
                )
                users = users_for(uid)
                uu = users.get(uid) or u
                if wave == "eve" and seg == "done_no_chat":
                    uu[f"{FLAG_PREFIX}_done_no_chat_eve"] = True
                else:
                    mark_sent(uu, seg)
                save_users(users, only=uid)
                n_ok += 1
                await asyncio.sleep(0.05)
            except Exception as e:
                log.warning("fail %s %s: %s", seg, uid, e)
                n_fail += 1
        stats["by_seg"][seg] = {"ok": n_ok, "skip": n_skip, "fail": n_fail}
        stats["sent"] += n_ok
        stats["skip"] += n_skip
        stats["fail"] += n_fail
    return stats


def preview_counts() -> dict[str, int]:
    cohort = load_cohort_from_db()
    c: dict[str, int] = defaultdict(int)
    for uid, u in cohort:
        seg = segment(uid, u)
        if seg:
            c[seg] += 1
    c["total_cohort"] = len(cohort)
    return dict(c)


async def amain():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--wave",
        choices=["morning_hot", "day_cold", "eve"],
        default=None,
    )
    ap.add_argument("--channel-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()

    token = (os.getenv("BOT_TOKEN") or "").strip()
    if args.preview or args.dry_run:
        print("COUNTS", preview_counts())
        print("CHANNEL:\n", CHANNEL_POST_HTML)
        for k, (t, _) in SEGMENT_COPY.items():
            print(f"\n=== {k} ===\n{t}")
        if args.preview and not args.wave and not args.channel_only:
            return

    if not token or token == "x":
        raise SystemExit("Нужен BOT_TOKEN в env")

    from aiogram import Bot

    bot = Bot(token=token)
    try:
        if args.channel_only or args.wave == "morning_hot":
            if not args.dry_run:
                ch = await send_channel(bot)
                print("CHANNEL", ch)
            else:
                print("CHANNEL dry-run ok")
        if args.wave:
            st = await send_wave(bot, args.wave, dry=args.dry_run)
            print("WAVE", st)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(amain())
