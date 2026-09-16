"""
Выгрузка воронки рекламы / онбординга в файл на компьютер.

Запуск (из корня проекта или из LexDAN_Bot_remote/LexDAN_Bot):
  python scripts/export_funnel_report.py

Читает users.json или DATABASE_URL из .env.
Пишет на Desktop:
  LexDAN_funnel_YYYY-MM-DD_HHMM.txt
  LexDAN_funnel_YYYY-MM-DD_HHMM.csv

Что обычно смотрят после рекламы:
  • Spend — сколько потратили
  • CPI (Cost Per Install / Start) = Spend / число людей, нажавших /start
  • CPR / CPA — цена регистрации / целевого действия
  • CTR объявления, CR старт→регистрация, старт→оплата
Этот отчёт даёт знаменатели воронки внутри бота (кол-во и %).
Spend/CPI считаешь сам: CPI = spend_руб / starts.
"""

from __future__ import annotations

import csv
import os
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

# корень приложения
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# подхватить .env (локально / remote)
try:
    from dotenv import load_dotenv

    for p in (
        ROOT / ".env",
        ROOT.parent / ".env",
        ROOT / "LexDAN_Bot" / ".env",
        Path.home() / "Desktop" / "LexDAN_Bot" / ".env",
        Path.home() / "Desktop" / "LexDAN_Bot" / "LexDAN_Bot_remote" / "LexDAN_Bot" / ".env",
    ):
        if p.is_file():
            load_dotenv(p)
except Exception:
    pass

# config.py требует токены при импорте — для отчёта достаточно заглушек
os.environ.setdefault("BOT_TOKEN", "export-report-dummy")
os.environ.setdefault("OPENROUTER_API_KEY", "export-report-dummy")
os.environ.setdefault("ELEVENLABS_API_KEY", "export-report-dummy")


def _desktop() -> Path:
    home = Path.home()
    desk = home / "Desktop"
    if desk.is_dir():
        return desk
    # RU Windows
    desk_ru = home / "Рабочий стол"
    if desk_ru.is_dir():
        return desk_ru
    return home


def _pct(part: int, whole: int) -> str:
    if whole <= 0:
        return "—"
    return f"{100.0 * part / whole:.1f}%"


def _ts(v) -> str:
    try:
        t = float(v or 0)
        if t <= 0:
            return ""
        return datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""


def _iter_users() -> list[tuple[str, dict]]:
    from services.database import load_users, get_user
    from services.growth import ensure_growth

    users = load_users()
    out: list[tuple[str, dict]] = []
    for uid, raw in users.items():
        if not isinstance(raw, dict):
            continue
        if str(uid).startswith("__"):
            continue
        if raw.get("imitating_registration"):
            continue
        # активная имитация онбординга — в рекламной воронке не нужна
        ob = raw.get("onboard") if isinstance(raw.get("onboard"), dict) else {}
        if ob.get("imit") and ob.get("active"):
            continue
        u = get_user(users, str(uid))
        ensure_growth(u)
        out.append((str(uid), u))
    out.sort(key=lambda x: float(x[1].get("first_seen_at") or 0) or 0)
    return out


def _onboard_stage(u: dict) -> str:
    ob = u.get("onboard") if isinstance(u.get("onboard"), dict) else {}
    return str(ob.get("stage") or "")


def _has_event(u: dict, name: str) -> bool:
    f = u.get("funnel") if isinstance(u.get("funnel"), dict) else {}
    for ev in f.get("events") or []:
        if isinstance(ev, dict) and ev.get("e") == name:
            return True
    return False


def _chat_msgs(u: dict) -> int:
    return int(u.get("chat_text_total") or 0) + int(u.get("chat_voice_total") or 0)


def _listening_done(u: dict) -> int:
    from services.listening_state import ensure_listening

    ensure_listening(u)
    prog = (u.get("listening") or {}).get("progress") or {}
    return sum(1 for v in prog.values() if v)


def _grammar_be_started(u: dict) -> bool:
    gp = u.get("grammar_progress") if isinstance(u.get("grammar_progress"), dict) else {}
    ce = gp.get("completed_exercises") or {}
    for k in ce:
        if "pronouns_be" in str(k):
            return True
    topics = gp.get("completed_topics") or []
    if any("pronouns_be" in str(t) for t in topics):
        return True
    les = u.get("lesson") or {}
    if les.get("topic_id") == "pronouns_be":
        return True
    stage = _onboard_stage(u)
    return stage in {"slides", "tasks", "tasks_menu", "grammar_cta", "done"} and bool(
        u.get("assessment_done") or stage == "done"
    )


def _reached_daily_fire(u: dict) -> bool:
    stage = _onboard_stage(u)
    if stage in {"daily_fire", "grammar_cta", "slides", "tasks_menu", "tasks", "done"}:
        return True
    if _has_event(u, "assessment_done") or u.get("assessment_done"):
        # после теста почти всегда идут на огонь в locked-онбординге
        ob = u.get("onboard") if isinstance(u.get("onboard"), dict) else {}
        if ob.get("df_done_sent") or ob.get("df_intro_sent"):
            return True
        df = u.get("daily_fire") if isinstance(u.get("daily_fire"), dict) else {}
        opened = df.get("opened") or {}
        if any(opened.values()):
            return True
    return False


def _reached_to_be(u: dict) -> bool:
    stage = _onboard_stage(u)
    if stage in {"grammar_cta", "slides", "tasks_menu", "tasks", "done"}:
        return True
    return _grammar_be_started(u)


def build_report(rows: list[tuple[str, dict]]) -> tuple[str, list[dict]]:
    n = len(rows)
    named = sum(1 for _, u in rows if (u.get("name") or "").strip())
    assessed = sum(1 for _, u in rows if u.get("assessment_done"))
    levels = Counter(
        (u.get("placement") or {}).get("level") or u.get("level") or "?"
        for _, u in rows
        if u.get("assessment_done")
    )
    translate_est = Counter()
    translate_scores = []
    for _, u in rows:
        p = u.get("placement") if isinstance(u.get("placement"), dict) else {}
        if p.get("translate_estimate"):
            translate_est[str(p["translate_estimate"])] += 1
        if p.get("translate_score") is not None:
            try:
                translate_scores.append(int(p["translate_score"]))
            except Exception:
                pass

    daily_fire = sum(1 for _, u in rows if _reached_daily_fire(u))
    to_be = sum(1 for _, u in rows if _reached_to_be(u))
    onboard_done = sum(
        1
        for _, u in rows
        if _onboard_stage(u) == "done" or _has_event(u, "onboard_done")
    )
    chat_cta = sum(
        1
        for _, u in rows
        if (u.get("funnel") or {}).get("chat_cta_sent") or _has_event(u, "chat_cta_sent")
    )
    chat_ever = sum(1 for _, u in rows if _chat_msgs(u) > 0)
    chat_3plus = sum(1 for _, u in rows if _chat_msgs(u) >= 3)
    listen_cta = sum(
        1
        for _, u in rows
        if (u.get("funnel") or {}).get("listen_cta_sent")
        or _has_event(u, "listen_cta_sent")
    )
    listen_opened = sum(
        1
        for _, u in rows
        if (u.get("funnel") or {}).get("listen_opened_after_cta")
        or _has_event(u, "listen_opened_funnel")
        or _listening_done(u) > 0
        or ((u.get("lesson") or {}).get("hub") or "").startswith("listening")
    )
    listen_done = sum(1 for _, u in rows if _listening_done(u) > 0)
    paidish = sum(
        1
        for _, u in rows
        if (u.get("premium_until") or u.get("chat_until") or u.get("lessons_until"))
    )

    base = named or n  # для % от стартов
    lines = [
        "=" * 64,
        "LexDAN — воронка / реклама (выгрузка)",
        f"Дата выгрузки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Источник: {'PostgreSQL' if os.getenv('DATABASE_URL') else 'users.json'}",
        "=" * 64,
        "",
        "Как считать CPI после рекламы:",
        "  CPI = сумма_рекламы_₽ / число_Start",
        "  Пример: 10 000 ₽ / 200 Start = 50 ₽ за старт",
        "  Дальше смотри CR по шагам ниже (сколько % дошло).",
        "",
        "── Сводка ──",
        f"Start (в базе):              {n}",
        f"Указали имя:                 {named}  ({_pct(named, n)})",
        f"Дошли до конца теста:        {assessed}  ({_pct(assessed, n)})",
        f"До Огня дня:                 {daily_fire}  ({_pct(daily_fire, n)})",
        f"До темы to be:               {to_be}  ({_pct(to_be, n)})",
        f"Завершили онбординг:         {onboard_done}  ({_pct(onboard_done, n)})",
        f"Получили CTA «Общаться»:     {chat_cta}  ({_pct(chat_cta, n)})",
        f"Писали в Общаться (≥1):      {chat_ever}  ({_pct(chat_ever, n)})",
        f"Общаться ≥3 сообщ.:          {chat_3plus}  ({_pct(chat_3plus, n)})",
        f"Получили CTA Listening:      {listen_cta}  ({_pct(listen_cta, n)})",
        f"Заходили в Listening:        {listen_opened}  ({_pct(listen_opened, n)})",
        f"Прошли ≥1 тему Listening:    {listen_done}  ({_pct(listen_done, n)})",
        f"Есть подписка/пасс (флаги):  {paidish}  ({_pct(paidish, n)})",
        "",
        "── Уровни после теста ──",
    ]
    for lv, c in sorted(levels.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"  {lv}: {c}  ({_pct(c, assessed)})")
    lines.append("")
    lines.append("── Оценка с перевода (если сохранена) ──")
    if translate_est:
        for lv, c in sorted(translate_est.items()):
            lines.append(f"  {lv}: {c}")
    else:
        lines.append("  (пока пусто — появится у новых после обновления бота)")
    if translate_scores:
        avg = sum(translate_scores) / len(translate_scores)
        lines.append(f"  Средний score перевода: {avg:.0f} (n={len(translate_scores)})")
    lines.append("")
    lines.append("── По пользователям ──")
    lines.append(
        "uid | name | first_seen | level | translate_est | "
        "assessed | daily_fire | to_be | onboard_done | "
        "chat_msgs | listen_topics | stage | plan_flags"
    )

    csv_rows: list[dict] = []
    for uid, u in rows:
        name = (u.get("name") or "").strip() or "—"
        p = u.get("placement") if isinstance(u.get("placement"), dict) else {}
        level = p.get("level") or u.get("level") or ""
        te = p.get("translate_estimate") or ""
        stage = _onboard_stage(u)
        chat_n = _chat_msgs(u)
        listen_n = _listening_done(u)
        flags = []
        if u.get("premium_until"):
            flags.append("premium")
        if u.get("chat_until"):
            flags.append("chat")
        if u.get("lessons_until"):
            flags.append("lessons")
        line = (
            f"{uid} | {name} | {_ts(u.get('first_seen_at'))} | {level} | {te} | "
            f"{'Y' if u.get('assessment_done') else 'N'} | "
            f"{'Y' if _reached_daily_fire(u) else 'N'} | "
            f"{'Y' if _reached_to_be(u) else 'N'} | "
            f"{'Y' if stage == 'done' or _has_event(u, 'onboard_done') else 'N'} | "
            f"{chat_n} | {listen_n} | {stage or '—'} | {','.join(flags) or '—'}"
        )
        lines.append(line)
        csv_rows.append(
            {
                "uid": uid,
                "name": name,
                "first_seen": _ts(u.get("first_seen_at")),
                "last_start": _ts(u.get("last_start_at")),
                "level": level,
                "translate_estimate": te,
                "translate_score": p.get("translate_score", ""),
                "assessment_done": int(bool(u.get("assessment_done"))),
                "daily_fire": int(_reached_daily_fire(u)),
                "to_be": int(_reached_to_be(u)),
                "onboard_done": int(stage == "done" or _has_event(u, "onboard_done")),
                "chat_cta": int(
                    bool((u.get("funnel") or {}).get("chat_cta_sent"))
                    or _has_event(u, "chat_cta_sent")
                ),
                "chat_messages": chat_n,
                "listen_cta": int(
                    bool((u.get("funnel") or {}).get("listen_cta_sent"))
                    or _has_event(u, "listen_cta_sent")
                ),
                "listen_topics_done": listen_n,
                "onboard_stage": stage,
                "plan_flags": ",".join(flags),
            }
        )

    lines.append("")
    lines.append("Конец отчёта.")
    return "\n".join(lines), csv_rows


def main() -> None:
    os.chdir(ROOT)
    db = (os.getenv("DATABASE_URL") or "").strip()
    has_json = (ROOT / "users.json").is_file() or (Path.cwd() / "users.json").is_file()
    if not db and not has_json:
        print(
            "Нет DATABASE_URL и нет users.json.\n"
            "1) Скопируй External Database URL из Render в файл .env:\n"
            "   DATABASE_URL=postgres://...\n"
            "   рядом с ботом или в переменные среды, затем снова:\n"
            "   python scripts/export_funnel_report.py\n"
            "2) Либо положи users.json в папку бота."
        )
        sys.exit(1)

    rows = _iter_users()
    text, csv_rows = build_report(rows)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    out_dir = _desktop()
    txt_path = out_dir / f"LexDAN_funnel_{stamp}.txt"
    csv_path = out_dir / f"LexDAN_funnel_{stamp}.csv"
    txt_path.write_text(text, encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        if csv_rows:
            w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            w.writeheader()
            w.writerows(csv_rows)
        else:
            f.write("uid\n")
    print(f"OK users={len(rows)}")
    print(f"TXT: {txt_path}")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
