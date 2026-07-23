"""
Отчёты для админа: воронка рекламы, лимиты, прогресс.
"""

from __future__ import annotations

from services.database import get_user, load_users
from services.growth import (
    FREE_CHAT_PER_DAY,
    FREE_GRAMMAR_EXERCISES_PER_DAY,
    FREE_VOCAB_ITEMS_PER_DAY,
    ensure_growth,
    has_chat_pass,
    vocab_items_used_today,
)
from services.lesson_state import count_completed_tasks
from services.rewards import grammar_daily_cap, has_lessons_pass, user_plan, vocab_daily_cap
from services.vocabulary_state import sync_vocab_counters


def _iter_users() -> list[tuple[str, dict]]:
    users = load_users()
    out: list[tuple[str, dict]] = []
    for uid, raw in users.items():
        if not isinstance(raw, dict):
            continue
        u = get_user(users, str(uid))
        ensure_growth(u)
        out.append((str(uid), u))
    out.sort(key=lambda x: float(x[1].get("first_seen_at") or 0) or 0)
    return out


def _name(u: dict) -> str:
    return (u.get("name") or "—").strip() or "—"


def _line(uid: str, u: dict, extra: str = "") -> str:
    bit = f" · {extra}" if extra else ""
    return f"• <code>{uid}</code> {_name(u)}{bit}"


def chunk_html(text: str, limit: int = 3500) -> list[str]:
    """Режет длинный HTML-отчёт на куски под лимит Telegram."""
    if len(text) <= limit:
        return [text]
    parts: list[str] = []
    buf: list[str] = []
    size = 0
    for line in text.split("\n"):
        add = len(line) + (1 if buf else 0)
        if buf and size + add > limit:
            parts.append("\n".join(buf))
            buf = [line]
            size = len(line)
        else:
            buf.append(line)
            size += add
    if buf:
        parts.append("\n".join(buf))
    return parts or [text]


def report_funnel() -> str:
    rows = _iter_users()
    n = len(rows)
    assessed = sum(1 for _, u in rows if u.get("assessment_done"))
    chat_today = 0
    chat_hit = 0
    grammar_hit = 0
    vocab_hit = 0
    for _, u in rows:
        daily = u.get("daily") or {}
        ct = int(daily.get("chat_text_today") or 0)
        cv = int(daily.get("chat_voice_today") or 0)
        cm = int(daily.get("chat_messages_today") or daily.get("chat_count") or 0)
        if ct + cv + cm > 0:
            chat_today += 1
        if _hit_chat_limit(u):
            chat_hit += 1
        if _hit_grammar_limit(u):
            grammar_hit += 1
        if _hit_vocab_limit(u):
            vocab_hit += 1

    return (
        "📊 <b>Воронка / сводка</b>\n\n"
        f"▶️ Нажали Start (в базе): <b>{n}</b>\n"
        f"📝 Прошли входной тест: <b>{assessed}</b>\n"
        f"💬 Писали в «Общаться» сегодня: <b>{chat_today}</b>\n"
        f"⛔ Упёрлись в лимит чата сегодня: <b>{chat_hit}</b>\n"
        f"⛔ Лимит Grammar сегодня: <b>{grammar_hit}</b>\n"
        f"⛔ Лимит Vocabulary сегодня: <b>{vocab_hit}</b>\n\n"
        "Команды: /starts /chat_stats /assessed /limits /progress"
    )


def report_starts(*, limit: int = 80) -> str:
    rows = _iter_users()
    lines = [f"▶️ <b>Кто запустил бота</b> (всего {len(rows)})\n"]
    for i, (uid, u) in enumerate(rows[:limit], 1):
        plan = user_plan(u)
        test = "✅тест" if u.get("assessment_done") else "—"
        lines.append(f"{i}. <code>{uid}</code> {_name(u)} · {plan} · {test}")
    if len(rows) > limit:
        lines.append(f"\n…и ещё {len(rows) - limit}. Смотри /progress или /user id")
    return "\n".join(lines)


def _hit_chat_limit(u: dict) -> bool:
    if has_chat_pass(u):
        return False
    daily = u.get("daily") or {}
    if daily.get("hit_chat_limit"):
        return True
    used = int(daily.get("chat_messages_today") or daily.get("chat_count") or 0)
    return used >= FREE_CHAT_PER_DAY


def _hit_grammar_limit(u: dict) -> bool:
    if has_lessons_pass(u):
        return False
    daily = u.get("daily") or {}
    if daily.get("hit_grammar_limit"):
        return True
    cap = grammar_daily_cap(u)
    done = int(daily.get("grammar_exercises_today") or 0)
    return done >= cap


def _hit_vocab_limit(u: dict) -> bool:
    if has_lessons_pass(u):
        return False
    daily = u.get("daily") or {}
    if daily.get("hit_vocab_limit"):
        return True
    return vocab_items_used_today(u) >= vocab_daily_cap(u)


def report_chat_stats() -> str:
    rows = _iter_users()
    lines = [
        "💬 <b>Общаться — текст / голос</b>\n",
        f"Лимит free: <b>{FREE_CHAT_PER_DAY}</b> сообщ./день (текст+голос).\n",
    ]
    active: list[tuple[str, dict]] = []
    for uid, u in rows:
        daily = u.get("daily") or {}
        tt = int(daily.get("chat_text_today") or 0)
        vt = int(daily.get("chat_voice_today") or 0)
        mixed = int(daily.get("chat_messages_today") or daily.get("chat_count") or 0)
        tot_t = int(u.get("chat_text_total") or 0)
        tot_v = int(u.get("chat_voice_total") or 0)
        if tt or vt or mixed or tot_t or tot_v or _hit_chat_limit(u):
            active.append((uid, u))

    if not active:
        lines.append("Пока никто не писал в чат (или счётчики ещё пустые).")
        return "\n".join(lines)

    hit = [(uid, u) for uid, u in active if _hit_chat_limit(u)]
    if hit:
        lines.append(f"⛔ <b>Упёрлись в лимит сегодня ({len(hit)}):</b>")
        for uid, u in hit:
            daily = u.get("daily") or {}
            used = int(daily.get("chat_messages_today") or daily.get("chat_count") or 0)
            lines.append(_line(uid, u, f"сегодня {used}/{FREE_CHAT_PER_DAY}"))
        lines.append("")

    def _sort_key(item: tuple[str, dict]) -> int:
        uid, u = item
        daily = u.get("daily") or {}
        return -(
            int(daily.get("chat_text_today") or 0)
            + int(daily.get("chat_voice_today") or 0)
            + int(daily.get("chat_messages_today") or 0)
            + int(u.get("chat_text_total") or 0)
            + int(u.get("chat_voice_total") or 0)
        )

    lines.append("<b>Активность:</b>")
    for uid, u in sorted(active, key=_sort_key)[:60]:
        daily = u.get("daily") or {}
        tt = int(daily.get("chat_text_today") or 0)
        vt = int(daily.get("chat_voice_today") or 0)
        mixed = int(daily.get("chat_messages_today") or 0)
        tot_t = int(u.get("chat_text_total") or 0)
        tot_v = int(u.get("chat_voice_total") or 0)
        if tt or vt:
            today = f"сегодня текст {tt} / голос {vt}"
        else:
            today = f"сегодня всего {mixed}"
        lines.append(_line(uid, u, f"{today} · всего т{tot_t}/г{tot_v}"))
    return "\n".join(lines)


def report_assessed() -> str:
    rows = [(uid, u) for uid, u in _iter_users() if u.get("assessment_done")]
    lines = [f"📝 <b>Прошли входной тест</b> ({len(rows)})\n"]
    if not rows:
        lines.append("Пока никого.")
        return "\n".join(lines)
    for uid, u in rows:
        lvl = u.get("level") or "—"
        lines.append(_line(uid, u, f"уровень {lvl}"))
    return "\n".join(lines)


def report_limits() -> str:
    rows = _iter_users()
    chat_hit = [(uid, u) for uid, u in rows if _hit_chat_limit(u)]
    gram_hit = [(uid, u) for uid, u in rows if _hit_grammar_limit(u)]
    vocab_hit = [(uid, u) for uid, u in rows if _hit_vocab_limit(u)]

    lines = ["⛔ <b>Лимиты сегодня (бесплатные)</b>\n"]

    lines.append(f"💬 Чат ({len(chat_hit)}), лимит {FREE_CHAT_PER_DAY}:")
    if chat_hit:
        for uid, u in chat_hit:
            daily = u.get("daily") or {}
            used = int(daily.get("chat_messages_today") or 0)
            lines.append(_line(uid, u, f"{used}/{FREE_CHAT_PER_DAY}"))
    else:
        lines.append("— никого")

    lines.append(f"\n📘 Grammar ({len(gram_hit)}), обычно {FREE_GRAMMAR_EXERCISES_PER_DAY}:")
    if gram_hit:
        for uid, u in gram_hit:
            daily = u.get("daily") or {}
            done = int(daily.get("grammar_exercises_today") or 0)
            cap = grammar_daily_cap(u)
            lines.append(_line(uid, u, f"{done}/{cap}"))
    else:
        lines.append("— никого")

    lines.append(f"\n📗 Vocabulary ({len(vocab_hit)}), обычно {FREE_VOCAB_ITEMS_PER_DAY}:")
    if vocab_hit:
        for uid, u in vocab_hit:
            used = vocab_items_used_today(u)
            cap = vocab_daily_cap(u)
            lines.append(_line(uid, u, f"{used}/{cap}"))
    else:
        lines.append("— никого")

    return "\n".join(lines)


def report_progress(*, limit: int = 50) -> str:
    rows = _iter_users()
    scored: list[tuple[str, dict, int, int, int]] = []
    for uid, u in rows:
        sync_vocab_counters(u)
        tasks = count_completed_tasks(u)
        words = int(u.get("words_learned") or 0)
        phrases = int(u.get("phrases_learned") or 0)
        if tasks or words or phrases or u.get("assessment_done"):
            scored.append((uid, u, tasks, words, phrases))

    lines = [
        "📈 <b>Прогресс: задания и слова</b>\n",
        f"С активностью: <b>{len(scored)}</b> из {len(rows)}\n",
    ]
    if not scored:
        lines.append("Пока пусто.")
        return "\n".join(lines)

    by_tasks = sorted(scored, key=lambda x: (-x[2], -x[3], -x[4]))[:limit]
    lines.append("<b>По заданиям Grammar:</b>")
    for uid, u, tasks, words, phrases in by_tasks:
        lines.append(_line(uid, u, f"заданий {tasks} · слов {words} · фраз {phrases}"))

    by_words = sorted(scored, key=lambda x: (-(x[3] + x[4]), -x[2]))[:limit]
    lines.append("\n<b>По словам+фразам Vocabulary:</b>")
    for uid, u, tasks, words, phrases in by_words:
        lines.append(_line(uid, u, f"слов {words} · фраз {phrases} · заданий {tasks}"))

    return "\n".join(lines)


def user_card_extra(u: dict) -> str:
    """Доп. строки для /user."""
    ensure_growth(u)
    sync_vocab_counters(u)
    daily = u.get("daily") or {}
    tt = int(daily.get("chat_text_today") or 0)
    vt = int(daily.get("chat_voice_today") or 0)
    cm = int(daily.get("chat_messages_today") or daily.get("chat_count") or 0)
    return (
        f"assessment_done: {bool(u.get('assessment_done'))}\n"
        f"заданий Grammar: {count_completed_tasks(u)}\n"
        f"слов/фраз: {int(u.get('words_learned') or 0)}/{int(u.get('phrases_learned') or 0)}\n"
        f"чат сегодня: текст {tt} / голос {vt} / всего {cm}\n"
        f"чат всего: т{int(u.get('chat_text_total') or 0)} / г{int(u.get('chat_voice_total') or 0)}\n"
        f"grammar сегодня: {int(daily.get('grammar_exercises_today') or 0)}/{grammar_daily_cap(u)}\n"
        f"vocab сегодня: {vocab_items_used_today(u)}/{vocab_daily_cap(u)}\n"
        f"лимиты: chat={_hit_chat_limit(u)} grammar={_hit_grammar_limit(u)} vocab={_hit_vocab_limit(u)}"
    )
