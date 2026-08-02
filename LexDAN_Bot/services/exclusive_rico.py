"""
Эксклюзивные задания Рико (призы 1–3 места): старт пака, проверка, прогресс.
"""

from __future__ import annotations

import re
from typing import Any

from data.exclusive_rico_packs import get_pack, pack_task_count, PACKS_BY_PLACE

BTN_EX_PLACE_1 = "🥇 1 место · Легенда"
BTN_EX_PLACE_2 = "🥈 2 место · Мастер"
BTN_EX_PLACE_3 = "🥉 3 место · Охотник"
BTN_EX_NEXT = "➡️ Далее"
BTN_EX_HINT = "💡 Подсказка"
BTN_EX_SKIP = "⏭ Пропустить"
BTN_EX_EXIT = "🚪 Выйти из эксклюзива"

PLACE_BUTTONS = {
    BTN_EX_PLACE_1: 1,
    BTN_EX_PLACE_2: 2,
    BTN_EX_PLACE_3: 3,
}


def _norm(s: str) -> str:
    t = (s or "").strip().lower().replace("ё", "е")
    t = t.replace("’", "'").replace("`", "'").replace("'", "")
    t = re.sub(r"[.!?,;:\"«»()\[\]{}]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def ensure_exclusive(user: dict) -> dict:
    raw = user.get("exclusive_rico")
    if not isinstance(raw, dict):
        raw = {}
    raw.setdefault("active", None)
    raw.setdefault("done_ids", [])
    user["exclusive_rico"] = raw
    return raw


def get_active(user: dict) -> dict | None:
    ensure_exclusive(user)
    active = user["exclusive_rico"].get("active")
    return active if isinstance(active, dict) else None


def clear_active(user: dict) -> None:
    ensure_exclusive(user)
    user["exclusive_rico"]["active"] = None


def start_pack(user: dict, place: int, *, test_mode: bool = False) -> dict:
    """Запустить пак места. test_mode — не списывает prize remaining."""
    pack = get_pack(place)
    if not pack:
        raise ValueError(f"no pack for place {place}")
    ensure_exclusive(user)
    tasks = list(pack.get("tasks") or [])
    user["exclusive_rico"]["active"] = {
        "place": int(place),
        "index": 0,
        "total": len(tasks),
        "test_mode": bool(test_mode),
        "title": pack.get("title") or "",
    }
    if not test_mode:
        ep = user.get("event_prizes")
        if not isinstance(ep, dict):
            ep = {}
        ep["place"] = int(place)
        ep["exclusive_tasks"] = len(tasks)
        ep["exclusive_tasks_remaining"] = len(tasks)
        ep["title"] = pack.get("title")
        user["event_prizes"] = ep
        user["profile_title"] = pack.get("title") or user.get("profile_title") or ""
    return user["exclusive_rico"]["active"]


def current_task(user: dict) -> dict | None:
    active = get_active(user)
    if not active:
        return None
    pack = get_pack(int(active.get("place") or 0))
    if not pack:
        return None
    tasks = pack.get("tasks") or []
    idx = int(active.get("index") or 0)
    if idx < 0 or idx >= len(tasks):
        return None
    return dict(tasks[idx])


def advance(user: dict) -> bool:
    """True — есть следующее; False — пак закончен."""
    active = get_active(user)
    if not active:
        return False
    task = current_task(user)
    if task:
        done = list(user["exclusive_rico"].get("done_ids") or [])
        tid = task.get("id")
        if tid and tid not in done:
            done.append(tid)
        user["exclusive_rico"]["done_ids"] = done
        if not active.get("test_mode"):
            ep = user.get("event_prizes")
            if isinstance(ep, dict):
                left = int(ep.get("exclusive_tasks_remaining") or 0)
                ep["exclusive_tasks_remaining"] = max(0, left - 1)
    active["index"] = int(active.get("index") or 0) + 1
    if active["index"] >= int(active.get("total") or 0):
        clear_active(user)
        return False
    return True


def format_task_card(user: dict, task: dict) -> str:
    active = get_active(user) or {}
    n = int(active.get("index") or 0) + 1
    total = int(active.get("total") or 0)
    place_title = active.get("title") or ""
    chapter = task.get("chapter_title") or ""
    title = task.get("title_ru") or ""
    body = task.get("prompt_html") or ""
    kind = task.get("kind") or "write"
    kind_hint = {
        "write": "✍️ Напиши ответ текстом",
        "fix": "🛠 Исправь и напиши верный вариант",
        "voice": "🎙 Голосом или текстом — как удобнее",
        "mcq": "🔘 Выбери вариант кнопкой ниже",
    }.get(kind, "✍️ Ответь текстом")
    return (
        f"🦜 <b>{place_title}</b>\n"
        f"Задание <b>{n}/{total}</b>\n"
        f"<i>{chapter}</i>\n\n"
        f"<b>{title}</b>\n\n"
        f"{body}\n\n"
        f"{kind_hint}"
    )


def mcq_options(task: dict) -> list[str]:
    return [str(x) for x in (task.get("options") or []) if str(x).strip()]


def check_answer(task: dict, user_text: str) -> dict[str, Any]:
    """
    {"correct": bool, "explain_ru": str}
    """
    kind = task.get("kind") or "write"
    raw = (user_text or "").strip()
    if not raw:
        return {"correct": False, "explain_ru": "Пусто 😅 Напиши хоть что-нибудь — я в тебя верю."}

    if kind == "mcq":
        gold = (task.get("answer") or "").strip()
        if raw == gold or _norm(raw) == _norm(gold):
            return {"correct": True, "explain_ru": ""}
        return {
            "correct": False,
            "explain_ru": f"Не тот вариант. Верный ориентир: <b>{gold}</b>",
        }

    if kind == "fix":
        gold = task.get("answer") or ""
        accept = list(task.get("accept") or [])
        if _norm(raw) == _norm(gold) or any(_norm(raw) == _norm(a) for a in accept):
            return {"correct": True, "explain_ru": ""}
        # мягкий GPT
        gpt = _gpt_fix_or_write(task, raw, mode="fix")
        if gpt.get("correct"):
            return {"correct": True, "explain_ru": ""}
        return {
            "correct": False,
            "explain_ru": (gpt.get("explain_ru") or f"Почти! Ориентир: <b>{gold}</b>"),
        }

    if kind == "voice":
        target = task.get("voice_text") or ""
        if _norm(raw) == _norm(target):
            return {"correct": True, "explain_ru": ""}
        # достаточно близко по словам
        tw = set(_norm(target).split())
        uw = set(_norm(raw).split())
        if tw and len(tw & uw) / max(1, len(tw)) >= 0.7:
            return {"correct": True, "explain_ru": ""}
        gpt = _gpt_fix_or_write(task, raw, mode="voice")
        if gpt.get("correct"):
            return {"correct": True, "explain_ru": ""}
        return {
            "correct": False,
            "explain_ru": gpt.get("explain_ru")
            or f"Давай ближе к фразе:\n<b>{target}</b>",
        }

    # write
    check = task.get("check") or "free_write"
    if check == "must_include":
        nraw = _norm(raw)
        words = nraw.split()
        min_w = int(task.get("min_words") or 0)
        if min_w and len(words) < min_w:
            return {
                "correct": False,
                "explain_ru": f"Чуть разверни мысль — хотя бы ~{min_w} слов 💪",
            }
        needles = [_norm(x) for x in (task.get("must_include") or []) if x]
        if needles and not any(n in nraw for n in needles):
            return {
                "correct": False,
                "explain_ru": "В ответе должно быть целевое слово/оборот из задания.",
            }
        forb = [_norm(x) for x in (task.get("forbid") or []) if x]
        if any(f and f in nraw for f in forb):
            return {
                "correct": False,
                "explain_ru": (task.get("hint_ru") or "Там затесалась запрещённая конструкция."),
            }
        return {"correct": True, "explain_ru": ""}

    if check == "paraphrase":
        source = _norm(task.get("source") or "")
        if source and _norm(raw) == source:
            return {
                "correct": False,
                "explain_ru": "Это копия исходника — нужен перефраз своими словами ✨",
            }
        min_w = int(task.get("min_words") or 4)
        if len(_norm(raw).split()) < min_w:
            return {"correct": False, "explain_ru": "Чуть длиннее — хотя бы короткое предложение."}
        gpt = _gpt_fix_or_write(task, raw, mode="paraphrase")
        if gpt.get("correct"):
            return {"correct": True, "explain_ru": ""}
        return {
            "correct": False,
            "explain_ru": gpt.get("explain_ru")
            or "Смысл рядом, но перефраз пока слабоват. Попробуй ещё раз — тебе по плечу 💪",
        }

    # free_write
    min_w = int(task.get("min_words") or 8)
    if len(_norm(raw).split()) < min_w:
        return {
            "correct": False,
            "explain_ru": f"Давай чуть объёмнее — от ~{min_w} слов. Ты справишься 🔥",
        }
    # лёгкая проверка: нет сплошной кириллицы без латиницы
    if not re.search(r"[a-zA-Z]", raw):
        return {"correct": False, "explain_ru": "Нужен ответ <b>на английском</b> 🙂"}
    return {"correct": True, "explain_ru": ""}


def _gpt_fix_or_write(task: dict, user_text: str, *, mode: str) -> dict:
    try:
        from services.gpt import _ask_json
    except Exception:
        return {"correct": False, "explain_ru": ""}

    if mode == "fix":
        gold = task.get("answer") or ""
        hint = (
            "Student must FIX the sentence. Accept any correct rewrite with same meaning. "
            "Ignore punctuation/apostrophes/case."
        )
        task_line = f"Broken prompt context. Model answer: {gold}\nStudent: {user_text}"
    elif mode == "voice":
        target = task.get("voice_text") or ""
        hint = (
            "Student repeats a spoken line. Accept close paraphrase with same meaning. "
            "Be lenient on tiny pronunciation/spelling differences."
        )
        task_line = f"Target: {target}\nStudent: {user_text}"
    else:
        source = task.get("source") or ""
        hint = (
            "Student must PARAPHRASE: same meaning, not a copy, natural English. "
            "Keep similar tense/time frame. Be reasonably strict on meaning."
        )
        task_line = f"Original: {source}\nStudent: {user_text}"

    data = _ask_json(
        [
            {
                "role": "system",
                "content": (
                    "You are Rico grading an exclusive English prize task. "
                    f"{hint} "
                    "If wrong, explain briefly in warm Russian (2 short sentences). "
                    'Return ONLY JSON: {"correct":bool,"explain_ru":"..."}'
                ),
            },
            {"role": "user", "content": task_line},
        ],
        {"correct": False, "explain_ru": ""},
        temperature=0.2,
        max_tokens=180,
    )
    if not isinstance(data, dict):
        return {"correct": False, "explain_ru": ""}
    return {
        "correct": bool(data.get("correct")),
        "explain_ru": str(data.get("explain_ru") or "").strip(),
    }


def pack_summary(place: int) -> str:
    pack = get_pack(place)
    if not pack:
        return "Пакета нет."
    n = pack_task_count(place)
    return (
        f"{pack.get('title')}\n"
        f"<i>{pack.get('subtitle')}</i>\n"
        f"Заданий: <b>{n}</b>"
    )


__all__ = [
    "BTN_EX_PLACE_1",
    "BTN_EX_PLACE_2",
    "BTN_EX_PLACE_3",
    "BTN_EX_NEXT",
    "BTN_EX_HINT",
    "BTN_EX_SKIP",
    "BTN_EX_EXIT",
    "PLACE_BUTTONS",
    "PACKS_BY_PLACE",
    "get_pack",
    "ensure_exclusive",
    "get_active",
    "clear_active",
    "start_pack",
    "current_task",
    "advance",
    "format_task_card",
    "mcq_options",
    "check_answer",
    "pack_summary",
]
