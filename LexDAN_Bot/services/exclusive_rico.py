"""
Эксклюзивные задания Рико (призы 1–3 места): паки 2/3 + сказка-легенда для 1 места.
"""

from __future__ import annotations

import random
import re
from typing import Any

from data.exclusive_rico_packs import get_pack, pack_task_count, PACKS_BY_PLACE
from data.exclusive_legend_story import (
    LEGEND_SCENES,
    READY_HTML,
    TITLE as LEGEND_TITLE,
    TOTAL_TASKS as LEGEND_TOTAL_TASKS,
    BTN_READY,
    BTN_STORY_NEXT,
    BTN_STORY_TRANSLATE,
    BTN_STORY_HINT,
    BTN_STORY_SKIP,
    BTN_STORY_EXIT,
    VOICE_NARRATOR,
    VOICE_BUNNY,
    VOICE_FOX,
    VOICE_OWL,
    VOICE_SQUIRREL,
    VOICE_HEDGEHOG,
    VOICE_DRAGON,
    VOICE_BUTTERFLY,
    get_scene,
    count_story_tasks,
)

BTN_EX_PLACE_1 = "🥇 1 место · Легенда"
BTN_EX_PLACE_2 = "🥈 2 место · Мастер"
BTN_EX_PLACE_3 = "🥉 3 место · Охотник"
BTN_EX_NEXT = BTN_STORY_NEXT
BTN_EX_HINT = BTN_STORY_HINT
BTN_EX_SKIP = BTN_STORY_SKIP
BTN_EX_EXIT = BTN_STORY_EXIT
BTN_EX_TRANSLATE = BTN_STORY_TRANSLATE
BTN_EX_READY = BTN_READY

PLACE_BUTTONS = {
    BTN_EX_PLACE_1: 1,
    BTN_EX_PLACE_2: 2,
    BTN_EX_PLACE_3: 3,
}

SPEAKER_VOICE = {
    "narrator": VOICE_NARRATOR,
    "rico": None,  # runtime → RICO_VOICE_ID
    "bunny": VOICE_BUNNY,
    "fox": VOICE_FOX,
    "owl": VOICE_OWL,
    "squirrel": VOICE_SQUIRREL,
    "hedgehog": VOICE_HEDGEHOG,
    "dragon": VOICE_DRAGON,
    "butterfly": VOICE_BUTTERFLY,
}

SPEAKER_LABEL = {
    "narrator": "📖 Рассказчик",
    "rico": "🦜 Рико",
    "bunny": "🐰 Зайчик",
    "fox": "🦊 Лиса",
    "owl": "🦉 Сова",
    "squirrel": "🐿️ Белка",
    "hedgehog": "🦔 Ёж",
    "dragon": "🐉 Дракон",
    "butterfly": "🦋 Бабочка",
}


def _norm(s: str) -> str:
    t = (s or "").strip().lower().replace("ё", "е")
    t = t.replace("’", "'").replace("`", "'").replace("'", "")
    t = re.sub(r"[.!?,;:\"«»()\[\]{}\-—–]", " ", t)
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


def is_story_mode(user: dict) -> bool:
    active = get_active(user)
    return bool(active and active.get("mode") == "story")


def resolve_voice_id(speaker: str) -> str:
    from services.voices import RICO_VOICE_ID

    key = (speaker or "narrator").lower()
    if key == "rico":
        return RICO_VOICE_ID
    vid = SPEAKER_VOICE.get(key)
    if vid:
        return vid
    return VOICE_NARRATOR


def start_pack(user: dict, place: int, *, test_mode: bool = False) -> dict:
    """Запустить пак места. place=1 → сказка; 2/3 → классический пак."""
    place = int(place)
    if place == 1:
        return start_legend_story(user, test_mode=test_mode)

    pack = get_pack(place)
    if not pack:
        raise ValueError(f"no pack for place {place}")
    ensure_exclusive(user)
    tasks = list(pack.get("tasks") or [])
    user["exclusive_rico"]["active"] = {
        "place": place,
        "mode": "pack",
        "index": 0,
        "total": len(tasks),
        "test_mode": bool(test_mode),
        "title": pack.get("title") or "",
    }
    if not test_mode:
        _grant_prize_meta(user, place, pack, len(tasks))
    return user["exclusive_rico"]["active"]


def start_legend_story(user: dict, *, test_mode: bool = False) -> dict:
    ensure_exclusive(user)
    user["exclusive_rico"]["active"] = {
        "place": 1,
        "mode": "story",
        "phase": "ready",  # ready | line | task | done
        "scene_index": 0,
        "tasks_done": 0,
        "total_tasks": LEGEND_TOTAL_TASKS,
        "test_mode": bool(test_mode),
        "title": LEGEND_TITLE,
        "last_en": "",
        "last_ru": "",
    }
    if not test_mode:
        _grant_prize_meta(
            user,
            1,
            {"title": LEGEND_TITLE},
            LEGEND_TOTAL_TASKS,
        )
    return user["exclusive_rico"]["active"]


def _grant_prize_meta(user: dict, place: int, pack: dict, n_tasks: int) -> None:
    ep = user.get("event_prizes")
    if not isinstance(ep, dict):
        ep = {}
    ep["place"] = int(place)
    ep["exclusive_tasks"] = n_tasks
    ep["exclusive_tasks_remaining"] = n_tasks
    ep["title"] = pack.get("title")
    user["event_prizes"] = ep
    user["profile_title"] = pack.get("title") or user.get("profile_title") or ""


def ready_html() -> str:
    return READY_HTML


def story_begin(user: dict) -> dict | None:
    """После «Я готов!» — перейти к первой сцене."""
    active = get_active(user)
    if not active or active.get("mode") != "story":
        return None
    active["phase"] = "line"
    active["scene_index"] = 0
    return _sync_phase_from_scene(user)


def _sync_phase_from_scene(user: dict) -> dict | None:
    active = get_active(user)
    if not active:
        return None
    scene = get_scene(int(active.get("scene_index") or 0))
    if not scene:
        active["phase"] = "done"
        return None
    if scene.get("type") == "task":
        active["phase"] = "task"
    else:
        active["phase"] = "line"
        active["last_en"] = scene.get("en") or ""
        active["last_ru"] = scene.get("ru") or ""
    return scene


def current_scene(user: dict) -> dict | None:
    active = get_active(user)
    if not active or active.get("mode") != "story":
        return None
    if active.get("phase") == "ready":
        return {"type": "ready"}
    if active.get("phase") == "done":
        return None
    return get_scene(int(active.get("scene_index") or 0))


def format_line_html(scene: dict) -> str:
    speaker = (scene.get("speaker") or "narrator").lower()
    label = scene.get("label") or SPEAKER_LABEL.get(speaker) or "📖"
    en = (scene.get("en") or "").strip()
    return f"{label}\n\n🇬🇧 {en}"


def scramble_words_display(task: dict) -> str:
    """Слова вразнобой (стабильно по id задания, но не в правильном порядке)."""
    words = [str(w) for w in (task.get("words") or []) if str(w).strip()]
    if not words:
        return ""
    order = list(range(len(words)))
    rng = random.Random(str(task.get("id") or "scramble"))
    rng.shuffle(order)
    # гарантируем, что не совпало с исходным порядком
    if order == list(range(len(words))) and len(words) > 1:
        order[0], order[-1] = order[-1], order[0]
    # ещё одна перестановка, если всё ещё «почти по порядку»
    shuffled = [words[i] for i in order]
    if shuffled == words and len(words) > 2:
        shuffled = words[1:] + words[:1]
    return " · ".join(shuffled)


def _task_body_html(task: dict) -> str:
    body = (task.get("prompt_html") or "").strip()
    if (task.get("kind") or "") == "scramble":
        bank = scramble_words_display(task)
        if bank:
            body = f"{body}\n\n<code>{bank}</code>"
    return body


def format_story_task_card(user: dict, task: dict) -> str:
    active = get_active(user) or {}
    done = int(active.get("tasks_done") or 0)
    total = int(active.get("total_tasks") or LEGEND_TOTAL_TASKS)
    n = done + 1
    chapter = task.get("chapter_title") or ""
    title = task.get("title_ru") or ""
    body = _task_body_html(task)
    kind = task.get("kind") or "write"
    kind_hint = {
        "write": "✍️ Напиши ответ текстом",
        "fix": "🛠 Исправь и напиши верный вариант",
        "voice": "🎙 Голосом или текстом — как удобнее",
        "mcq": "🔘 Выбери вариант кнопкой ниже",
        "scramble": "🧩 Собери предложение и напиши его целиком",
    }.get(kind, "✍️ Ответь текстом")
    return (
        f"🦜 <b>{active.get('title') or LEGEND_TITLE}</b>\n"
        f"Задание <b>{n}/{total}</b>\n"
        f"<i>{chapter}</i>\n\n"
        f"<b>{title}</b>\n\n"
        f"{body}\n\n"
        f"{kind_hint}"
    )


def story_next(user: dict) -> dict | None:
    """Далее со строки → следующая сцена. None = история окончена."""
    active = get_active(user)
    if not active or active.get("mode") != "story":
        return None
    if active.get("phase") == "ready":
        return story_begin(user)
    idx = int(active.get("scene_index") or 0) + 1
    active["scene_index"] = idx
    scene = _sync_phase_from_scene(user)
    if scene is None:
        clear_active(user)
    return scene


def story_complete_task(user: dict) -> dict | None:
    """Успех/пропуск задания → следующая сцена после task."""
    active = get_active(user)
    if not active or active.get("mode") != "story":
        return None
    scene = get_scene(int(active.get("scene_index") or 0))
    if scene and scene.get("type") == "task":
        tid = scene.get("id")
        done = list(user["exclusive_rico"].get("done_ids") or [])
        if tid and tid not in done:
            done.append(tid)
        user["exclusive_rico"]["done_ids"] = done
        active["tasks_done"] = int(active.get("tasks_done") or 0) + 1
        if not active.get("test_mode"):
            ep = user.get("event_prizes")
            if isinstance(ep, dict):
                left = int(ep.get("exclusive_tasks_remaining") or 0)
                ep["exclusive_tasks_remaining"] = max(0, left - 1)
    return story_next(user)


def current_task(user: dict) -> dict | None:
    active = get_active(user)
    if not active:
        return None
    if active.get("mode") == "story":
        if active.get("phase") != "task":
            return None
        scene = get_scene(int(active.get("scene_index") or 0))
        if not scene or scene.get("type") != "task":
            return None
        return dict(scene)

    pack = get_pack(int(active.get("place") or 0))
    if not pack:
        return None
    tasks = pack.get("tasks") or []
    idx = int(active.get("index") or 0)
    if idx < 0 or idx >= len(tasks):
        return None
    return dict(tasks[idx])


def advance(user: dict) -> bool:
    """Для паков 2/3. True — есть следующее."""
    active = get_active(user)
    if not active:
        return False
    if active.get("mode") == "story":
        scene = story_complete_task(user)
        return scene is not None

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
    if is_story_mode(user):
        return format_story_task_card(user, task)
    active = get_active(user) or {}
    n = int(active.get("index") or 0) + 1
    total = int(active.get("total") or 0)
    place_title = active.get("title") or ""
    chapter = task.get("chapter_title") or ""
    title = task.get("title_ru") or ""
    body = _task_body_html(task)
    kind = task.get("kind") or "write"
    kind_hint = {
        "write": "✍️ Напиши ответ текстом",
        "fix": "🛠 Исправь и напиши верный вариант",
        "voice": "🎙 Голосом или текстом — как удобнее",
        "mcq": "🔘 Выбери вариант кнопкой ниже",
        "scramble": "🧩 Собери предложение и напиши его целиком",
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

    if kind in {"fix", "scramble"}:
        gold = task.get("answer") or ""
        accept = list(task.get("accept") or [])
        if _norm(raw) == _norm(gold) or any(_norm(raw) == _norm(a) for a in accept):
            return {"correct": True, "explain_ru": ""}
        if kind == "scramble":
            return {
                "correct": False,
                "explain_ru": (
                    "Порядок слов ещё не тот. Собери фразу заново — "
                    f"ориентир начинается с «{(gold.split() or [''])[0]}…»"
                ),
            }
        gpt = _gpt_fix_or_write(task, raw, mode="fix")
        if gpt.get("correct"):
            return {"correct": True, "explain_ru": ""}
        return {
            "correct": False,
            "explain_ru": (gpt.get("explain_ru") or f"Почти! Ориентир: <b>{gold}</b>"),
        }

    if kind == "voice":
        target = task.get("voice_text") or ""
        accept = list(task.get("accept") or [])
        if _norm(raw) == _norm(target) or any(_norm(raw) == _norm(a) for a in accept):
            return {"correct": True, "explain_ru": ""}
        tw = set(_norm(target).split())
        uw = set(_norm(raw).split())
        if tw and len(tw & uw) / max(1, len(tw)) >= 0.55:
            return {"correct": True, "explain_ru": ""}
        tw2 = {w for w in tw if len(w) > 2}
        uw2 = {w for w in uw if len(w) > 2}
        if tw2 and len(tw2 & uw2) / max(1, len(tw2)) >= 0.6:
            return {"correct": True, "explain_ru": ""}
        gpt = _gpt_fix_or_write(task, raw, mode="voice")
        if gpt.get("correct"):
            return {"correct": True, "explain_ru": ""}
        return {
            "correct": False,
            "explain_ru": gpt.get("explain_ru")
            or f"Услышал: <i>{raw}</i>\nДавай ближе к:\n<b>{target}</b>",
        }

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
        # достаточно одного совпадения из списка, если это альтернативы одного понятия;
        # если несколько разных ключей — требуем хотя бы один (OR), кроме явного all
        require_all = bool(task.get("require_all"))
        if needles:
            hits = sum(1 for n in needles if n in nraw)
            if require_all and hits < len(needles):
                return {
                    "correct": False,
                    "explain_ru": "В ответе должны быть все целевые слова из задания.",
                }
            if not require_all and hits < 1:
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
        if not re.search(r"[a-zA-Z]", raw):
            return {"correct": False, "explain_ru": "Нужен ответ <b>на английском</b> 🙂"}
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

    min_w = int(task.get("min_words") or 8)
    if len(_norm(raw).split()) < min_w:
        return {
            "correct": False,
            "explain_ru": f"Давай чуть объёмнее — от ~{min_w} слов. Ты справишься 🔥",
        }
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
    if int(place) == 1:
        return (
            f"{LEGEND_TITLE}\n"
            f"<i>Сказка о Рико-учителе · {LEGEND_TOTAL_TASKS} заданий в сюжете</i>"
        )
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
    "BTN_EX_TRANSLATE",
    "BTN_EX_READY",
    "PLACE_BUTTONS",
    "PACKS_BY_PLACE",
    "LEGEND_SCENES",
    "get_pack",
    "ensure_exclusive",
    "get_active",
    "clear_active",
    "is_story_mode",
    "start_pack",
    "start_legend_story",
    "ready_html",
    "story_begin",
    "story_next",
    "story_complete_task",
    "current_scene",
    "format_line_html",
    "resolve_voice_id",
    "current_task",
    "advance",
    "format_task_card",
    "mcq_options",
    "check_answer",
    "pack_summary",
    "count_story_tasks",
]
