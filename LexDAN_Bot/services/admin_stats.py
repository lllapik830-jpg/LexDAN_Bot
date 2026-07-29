"""
Отчёты для админа: воронка рекламы, лимиты, прогресс.
"""

from __future__ import annotations

from services.database import get_user, load_users
from services.growth import (
    FREE_CHAT_PER_DAY,
    FREE_GRAMMAR_EXERCISES_PER_DAY,
    FREE_VOCAB_ITEMS_PER_DAY,
    backfill_chat_totals,
    ensure_growth,
    has_chat_pass,
    vocab_items_used_today,
)
from services.lesson_state import count_completed_tasks
from services.listening_state import ensure_listening
from services.rewards import (
    count_grammar_exercises_done,
    grammar_daily_cap,
    has_lessons_pass,
    user_plan,
    vocab_daily_cap,
)
from services.vocabulary_state import sync_vocab_counters
from config import MANAGER_ID


def _iter_users(*, persist_backfill: bool = False) -> list[tuple[str, dict]]:
    users = load_users()
    out: list[tuple[str, dict]] = []
    for uid, raw in users.items():
        if not isinstance(raw, dict):
            continue
        u = get_user(users, str(uid))
        before = int(u.get("chat_text_total") or 0) + int(u.get("chat_voice_total") or 0)
        ensure_growth(u)
        after = int(u.get("chat_text_total") or 0) + int(u.get("chat_voice_total") or 0)
        if persist_backfill and after > before:
            from services.database import save_users

            save_users(users, only=str(uid))
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


def _chat_totals(u: dict) -> tuple[int, int, int]:
    """(text_total, voice_total, all_messages) за всё время."""
    backfill_chat_totals(u)
    tot_t = int(u.get("chat_text_total") or 0)
    tot_v = int(u.get("chat_voice_total") or 0)
    daily = u.get("daily") or {}
    today = int(daily.get("chat_messages_today") or daily.get("chat_count") or 0)
    today_t = int(daily.get("chat_text_today") or 0)
    today_v = int(daily.get("chat_voice_today") or 0)
    all_msg = tot_t + tot_v
    # Если totals ещё пустые, но сегодня уже писали — считаем сегодня
    if all_msg == 0 and (today_t or today_v or today):
        tot_t = today_t or (today if not today_v else 0)
        tot_v = today_v
        all_msg = tot_t + tot_v if (tot_t or tot_v) else today
        if all_msg and not tot_t and not tot_v:
            tot_t = all_msg
    return tot_t, tot_v, all_msg


def report_funnel() -> str:
    rows = _iter_users(persist_backfill=True)
    n = len(rows)
    assessed = sum(1 for _, u in rows if u.get("assessment_done"))
    chat_ever = 0
    chat_msgs_all = 0
    chat_text_all = 0
    chat_voice_all = 0
    chat_today = 0
    chat_hit = 0
    chat_hit_ever = 0
    grammar_hit = 0
    vocab_hit = 0
    for _, u in rows:
        daily = u.get("daily") or {}
        tt, vt, all_msg = _chat_totals(u)
        ct = int(daily.get("chat_text_today") or 0)
        cv = int(daily.get("chat_voice_today") or 0)
        cm = int(daily.get("chat_messages_today") or daily.get("chat_count") or 0)
        if all_msg > 0:
            chat_ever += 1
            chat_msgs_all += all_msg
            chat_text_all += tt
            chat_voice_all += vt
        if ct + cv + cm > 0:
            chat_today += 1
        if _hit_chat_limit(u):
            chat_hit += 1
        if u.get("hit_chat_limit_ever") or _hit_chat_limit(u):
            chat_hit_ever += 1
        if _hit_grammar_limit(u):
            grammar_hit += 1
        if _hit_vocab_limit(u):
            vocab_hit += 1

    return (
        "📊 <b>Воронка / сводка</b>\n\n"
        f"▶️ Нажали Start (в базе): <b>{n}</b>\n"
        f"📝 Прошли входной тест: <b>{assessed}</b>\n\n"
        f"💬 <b>Общаться — за всё время</b>\n"
        f"  писали: <b>{chat_ever}</b>\n"
        f"  сообщений: <b>{chat_msgs_all}</b> "
        f"(текст {chat_text_all} / голос {chat_voice_all})\n"
        f"  упирались в лимит (хотя бы раз): <b>{chat_hit_ever}</b>\n\n"
        f"📅 <b>Сегодня</b>\n"
        f"  писали: <b>{chat_today}</b>\n"
        f"  ⛔ лимит чата: <b>{chat_hit}</b>\n"
        f"  ⛔ Grammar: <b>{grammar_hit}</b>\n"
        f"  ⛔ Vocabulary: <b>{vocab_hit}</b>\n\n"
        "Команды: /starts (сегодня) /chat_stats /assessed /limits /progress"
    )


def report_starts(*, limit: int = 100) -> str:
    """Кто нажал /start сегодня (по last_start_at / first_seen_at)."""
    from datetime import date
    import time

    today = date.today().isoformat()
    rows = _iter_users()
    today_rows: list[tuple[str, dict, float]] = []
    for uid, u in rows:
        ts = float(u.get("last_start_at") or 0) or float(u.get("first_seen_at") or 0)
        if not ts:
            continue
        try:
            day = time.strftime("%Y-%m-%d", time.localtime(ts))
        except (OverflowError, OSError, ValueError):
            continue
        if day == today:
            today_rows.append((uid, u, ts))
    today_rows.sort(key=lambda x: x[2], reverse=True)

    lines = [
        f"▶️ <b>Кто нажал /start сегодня</b> ({today})\n",
        f"Всего: <b>{len(today_rows)}</b>\n",
    ]
    if not today_rows:
        lines.append("Пока никто не жал /start сегодня.")
        return "\n".join(lines)

    for i, (uid, u, ts) in enumerate(today_rows[:limit], 1):
        plan = user_plan(u)
        hhmm = time.strftime("%H:%M", time.localtime(ts))
        new = " · 🆕" if not u.get("name") else ""
        lines.append(
            f"{i}. <code>{uid}</code> {_name(u)} · {hhmm} · {plan}{new}"
        )
    if len(today_rows) > limit:
        lines.append(f"\n…и ещё {len(today_rows) - limit}")
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
    rows = _iter_users(persist_backfill=True)
    lines = [
        "💬 <b>Общаться — за всё время</b>\n",
        f"Лимит free: <b>{FREE_CHAT_PER_DAY}</b> сообщ./день (текст+голос).\n",
    ]
    active: list[tuple[str, dict]] = []
    sum_t = sum_v = sum_all = 0
    for uid, u in rows:
        tot_t, tot_v, all_msg = _chat_totals(u)
        daily = u.get("daily") or {}
        mixed = int(daily.get("chat_messages_today") or daily.get("chat_count") or 0)
        if all_msg or mixed or _hit_chat_limit(u) or u.get("hit_chat_limit_ever"):
            active.append((uid, u))
            sum_t += tot_t
            sum_v += tot_v
            sum_all += all_msg

    if not active:
        lines.append("Пока никто не писал в чат (или счётчики ещё пустые).")
        return "\n".join(lines)

    lines.append(
        f"Всего писали: <b>{len(active)}</b> · "
        f"сообщений <b>{sum_all}</b> (текст {sum_t} / голос {sum_v})\n"
    )

    hit_ever = [
        (uid, u)
        for uid, u in active
        if u.get("hit_chat_limit_ever") or _hit_chat_limit(u)
    ]
    if hit_ever:
        lines.append(f"⛔ <b>Упирались в лимит ({len(hit_ever)}):</b>")
        for uid, u in hit_ever:
            daily = u.get("daily") or {}
            used = int(daily.get("chat_messages_today") or daily.get("chat_count") or 0)
            flag = "сегодня" if _hit_chat_limit(u) else "раньше"
            lines.append(_line(uid, u, f"{flag} · сегодня {used}/{FREE_CHAT_PER_DAY}"))
        lines.append("")

    def _sort_key(item: tuple[str, dict]) -> tuple[int, int]:
        _, u = item
        tot_t, tot_v, all_msg = _chat_totals(u)
        daily = u.get("daily") or {}
        today = (
            int(daily.get("chat_text_today") or 0)
            + int(daily.get("chat_voice_today") or 0)
            + int(daily.get("chat_messages_today") or 0)
        )
        return (-all_msg, -today)

    lines.append("<b>По пользователям (всё время → сегодня):</b>")
    for uid, u in sorted(active, key=_sort_key)[:60]:
        daily = u.get("daily") or {}
        tt = int(daily.get("chat_text_today") or 0)
        vt = int(daily.get("chat_voice_today") or 0)
        mixed = int(daily.get("chat_messages_today") or 0)
        tot_t, tot_v, all_msg = _chat_totals(u)
        ever = f"всего {all_msg} (т{tot_t}/г{tot_v})"
        if tt or vt:
            today = f"сегодня т{tt}/г{vt}"
        else:
            today = f"сегодня {mixed}"
        lines.append(_line(uid, u, f"{ever} · {today}"))
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
    from services.growth import (
        FREE_LESSON_POINTS_PER_DAY,
        POINT_GRAMMAR_EXERCISE,
        POINT_VOCAB_ITEM,
        lesson_points_cap,
        lesson_points_used_today,
    )

    rows = _iter_users()
    chat_hit = [(uid, u) for uid, u in rows if _hit_chat_limit(u)]
    lesson_hit = [
        (uid, u)
        for uid, u in rows
        if (_hit_grammar_limit(u) or _hit_vocab_limit(u))
    ]

    lines = [
        "⛔ <b>Лимиты сегодня (бесплатные)</b>\n",
        f"Уроки: общий пул <b>{FREE_LESSON_POINTS_PER_DAY}</b> баллов "
        f"(Grammar {POINT_GRAMMAR_EXERCISE} / Vocab {POINT_VOCAB_ITEM}).\n",
    ]

    lines.append(f"💬 Чат ({len(chat_hit)}), лимит {FREE_CHAT_PER_DAY}:")
    if chat_hit:
        for uid, u in chat_hit:
            daily = u.get("daily") or {}
            used = int(daily.get("chat_messages_today") or 0)
            lines.append(_line(uid, u, f"{used}/{FREE_CHAT_PER_DAY}"))
    else:
        lines.append("— никого")

    lines.append(f"\n📘📗 Уроки — упёрлись в баллы ({len(lesson_hit)}):")
    if lesson_hit:
        for uid, u in lesson_hit:
            used = lesson_points_used_today(u)
            cap = lesson_points_cap(u)
            lines.append(_line(uid, u, f"{used}/{cap} баллов"))
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
    tot_t, tot_v, tot_all = _chat_totals(u)
    return (
        f"assessment_done: {bool(u.get('assessment_done'))}\n"
        f"заданий Grammar: {count_completed_tasks(u)}\n"
        f"слов/фраз: {int(u.get('words_learned') or 0)}/{int(u.get('phrases_learned') or 0)}\n"
        f"чат сегодня: текст {tt} / голос {vt} / всего {cm}\n"
        f"чат всего: {tot_all} (текст {tot_t} / голос {tot_v})\n"
        f"hit_chat_limit_ever: {bool(u.get('hit_chat_limit_ever') or _hit_chat_limit(u))}\n"
        f"grammar сегодня: {int(daily.get('grammar_exercises_today') or 0)}/{grammar_daily_cap(u)}\n"
        f"vocab сегодня: {vocab_items_used_today(u)}/{vocab_daily_cap(u)}\n"
        f"лимиты: chat={_hit_chat_limit(u)} grammar={_hit_grammar_limit(u)} vocab={_hit_vocab_limit(u)}"
    )


def _fmt_last_active(u: dict) -> str:
    raw = (u.get("last_active_at") or "").strip()
    if not raw:
        return "неизвестно"
    try:
        from datetime import datetime

        dt = datetime.fromisoformat(raw)
        return dt.strftime("%d.%m.%Y %H:%M") + " МСК"
    except Exception:
        return raw[:19]


def describe_last_action(u: dict) -> str:
    """Человекочитаемо: где был и что делал."""
    section = (u.get("last_section") or "").strip()
    mode = (u.get("mode") or "").strip()
    lesson = u.get("lesson") if isinstance(u.get("lesson"), dict) else {}
    hub = (lesson.get("hub") or "").strip()
    bits: list[str] = []
    if section:
        bits.append(section)
    elif mode:
        bits.append(mode)
    if hub:
        bits.append(f"hub={hub}")
    if lesson.get("level"):
        bits.append(f"ур.урока {lesson.get('level')}")
    if lesson.get("topic_title"):
        bits.append(str(lesson.get("topic_title"))[:40])
    chat_last = (u.get("chat_last_user_text") or "").strip()
    if chat_last and (mode == "chat" or section == "общение"):
        bits.append(f"чат: «{chat_last[:60]}»")
    step = (u.get("step") or "").strip()
    if step and step not in {"ready", ""}:
        bits.append(f"step={step}")
    return " · ".join(bits) if bits else "—"


def format_user_card(uid: str, u: dict) -> str:
    """Полная карточка пользователя для /user."""
    ensure_growth(u)
    sync_vocab_counters(u)
    from services.growth import is_premium, premium_days_left, premium_time_label
    from services.rewards import plan_label, user_plan
    from services.pricing import lottery_status_lines, discount_percent

    plan = user_plan(u)
    tot_t, tot_v, tot_all = _chat_totals(u)
    ceiling = u.get("grammar_unlock_ceiling") or u.get("level") or "—"
    lot = lottery_status_lines(u)
    promo = u.get("promo_trial_code") or "—"
    return (
        f"👤 <b>{_name(u)}</b> · <code>{uid}</code>\n\n"
        f"⏰ Последний визит: <b>{_fmt_last_active(u)}</b>\n"
        f"📍 Последнее: {describe_last_action(u)}\n\n"
        f"📈 Уровень в профиле: <b>{u.get('level') or '—'}</b>\n"
        f"🔓 Потолок Grammar: <b>{ceiling}</b>\n"
        f"✅ Заданий Grammar: <b>{count_completed_tasks(u)}</b>\n"
        f"📝 Слов: <b>{int(u.get('words_learned') or 0)}</b> · "
        f"фраз: <b>{int(u.get('phrases_learned') or 0)}</b>\n"
        f"🔥 Серия: <b>{int(u.get('streak') or 0)}</b> · "
        f"сейфы: {int(u.get('streak_safes') or 0)}\n\n"
        f"💎 Подписка: <b>{plan_label(plan)}</b> ({plan})\n"
        f"   доступ: {premium_time_label(u)}\n"
        f"   premium дн≈ {premium_days_left(u) if is_premium(u) else 0}\n"
        f"   скидка: {discount_percent(u)}%\n"
        f"   промо: {promo}\n"
        f"   assessment: {'да' if u.get('assessment_done') else 'нет'}\n"
        f"{lot}\n"
        f"💬 Общение всего: текст <b>{tot_t}</b> · голос <b>{tot_v}</b> · "
        f"сумма <b>{tot_all}</b>\n"
        f"💬 Сегодня: "
        f"т{int((u.get('daily') or {}).get('chat_text_today') or 0)} / "
        f"г{int((u.get('daily') or {}).get('chat_voice_today') or 0)}\n"
        f"🎯 Цель дня: "
        f"{'✅' if (u.get('daily') or {}).get('goal_done') else '⏳'}\n"
        f"🎁 Реф: приглашено {int(u.get('invite_count') or 0)}, "
        f"засчитано {int(u.get('referral_qualified') or 0)}"
    )


def _count_listening_topics(u: dict) -> int:
    sm = ensure_listening(u)
    prog = sm.get("progress") or {}
    return sum(1 for v in prog.values() if v)


def _usage_metrics(u: dict) -> dict[str, int]:
    """Счётчики разделов за всё время."""
    sync_vocab_counters(u)
    text_n, voice_n, _ = _chat_totals(u)
    grammar_n = count_grammar_exercises_done(u)
    words_n = int(u.get("words_learned") or 0)
    phrases_n = int(u.get("phrases_learned") or 0)
    listening_n = _count_listening_topics(u)
    total = text_n + voice_n + grammar_n + words_n + phrases_n + listening_n
    return {
        "text": text_n,
        "voice": voice_n,
        "grammar": grammar_n,
        "words": words_n,
        "phrases": phrases_n,
        "listening": listening_n,
        "sum": total,
    }


def _plan_top_label(u: dict) -> str:
    """Для /top и /others: free | full (chat тоже показываем явно)."""
    plan = user_plan(u)
    if plan == "full":
        return "full"
    if plan == "chat":
        return "chat"
    return "free"


def report_top(*, limit: int = 80) -> str:
    """
    Топ по сумме: чат (текст+голос) + grammar задания + слова + фразы + listening темы.
    Админ (MANAGER) не включается. Без активности — в /others.
    """
    rows = _iter_users(persist_backfill=True)
    scored: list[tuple[str, dict, dict[str, int]]] = []
    for uid, u in rows:
        if str(uid) == str(MANAGER_ID):
            continue
        m = _usage_metrics(u)
        if m["sum"] <= 0:
            continue
        scored.append((uid, u, m))

    scored.sort(key=lambda x: (-x[2]["sum"], -x[2]["grammar"], -x[2]["text"]))

    lines = [
        "🏆 <b>Топ по использованию</b>\n",
        f"В топе: <b>{len(scored)}</b> · без активности → /others\n",
        "Сумма = голос + текст + grammar + слова + фразы + listening\n",
    ]
    if not scored:
        lines.append("Пока никого с активностью.")
        return "\n".join(lines)

    for i, (uid, u, m) in enumerate(scored[:limit], 1):
        lines.append(
            f"<b>{i}.</b> <code>{uid}</code> {_name(u)} · {_plan_top_label(u)}\n"
            f"   🎤{m['voice']} · 💬{m['text']} · 📘{m['grammar']} · "
            f"📝{m['words']}+{m['phrases']} · 🎧{m['listening']} · "
            f"Σ<b>{m['sum']}</b>"
        )
    if len(scored) > limit:
        lines.append(f"\n…и ещё {len(scored) - limit}")
    return "\n".join(lines)


def report_others(*, limit: int = 120) -> str:
    """Юзеры без действий в разделах (чат/grammar/vocab/listening). Без админа."""
    rows = _iter_users(persist_backfill=True)
    idle: list[tuple[str, dict]] = []
    for uid, u in rows:
        if str(uid) == str(MANAGER_ID):
            continue
        m = _usage_metrics(u)
        if m["sum"] <= 0:
            idle.append((uid, u))

    idle.sort(key=lambda x: float(x[1].get("first_seen_at") or 0) or 0, reverse=True)

    lines = [
        "👻 <b>Без активности в разделах</b>\n",
        f"Всего: <b>{len(idle)}</b> · как только сделают что-то → /top\n",
    ]
    if not idle:
        lines.append("Всех уже видно в /top.")
        return "\n".join(lines)

    for uid, u in idle[:limit]:
        lines.append(f"• <code>{uid}</code> {_name(u)} · {_plan_top_label(u)}")
    if len(idle) > limit:
        lines.append(f"\n…и ещё {len(idle) - limit}")
    return "\n".join(lines)


def report_admin_home() -> str:
    """Сводка для /admin: чат + список пользователей с id."""
    rows = _iter_users(persist_backfill=True)
    text_all = voice_all = 0
    for _, u in rows:
        t, v, _ = _chat_totals(u)
        text_all += t
        voice_all += v

    lines = [
        "🛠 <b>Админ LexDAN</b>\n",
        f"Пользователей: <b>{len(rows)}</b>\n",
        "<b>Общение (все юзеры, всё время)</b>",
        f"• текстовых: <b>{text_all}</b>",
        f"• голосовых: <b>{voice_all}</b>",
        f"• всего сообщ.: <b>{text_all + voice_all}</b>\n",
        "Команды: /users · /purge_blocked · /top · /others · /user <code>id</code> · "
        "/grant_chat · /grant_full · /revoke · /unlock_levels · /paid\n",
        "<b>Пользователи</b>",
    ]
    # свежие сверху
    sorted_rows = sorted(
        rows,
        key=lambda x: x[1].get("last_active_at") or "",
        reverse=True,
    )
    for uid, u in sorted_rows:
        plan = user_plan(u)
        t, v, _ = _chat_totals(u)
        lines.append(
            f"• <code>{uid}</code> {_name(u)} · {u.get('level') or '—'} · "
            f"{plan} · чат т{t}/г{v}"
        )
    return "\n".join(lines)
