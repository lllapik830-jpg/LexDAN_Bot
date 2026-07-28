"""Магические элементы: дропы, дубликаты, pity, финал."""

from __future__ import annotations

import logging
import random
from typing import Any

from data.collection_catalog import (
    COLLECTION_ELEMENTS,
    TOTAL_ELEMENTS,
    RARITY_WEIGHTS,
    RARITY_LABEL_RU,
    element_by_id,
    elements_by_rarity,
    asset_path,
)

log = logging.getLogger(__name__)

BTN_COLLECTION = "🎴 Магические элементы"
DUP_PITY_NEED = 5
VOCAB_DROP_EVERY = 3
# Шанс дубликата при любом дропе (остальное — новая карта, если есть)
DUP_DROP_CHANCE = 0.20


def collection_allowed(user_id: str | int | None) -> bool:
    """Коллекция и кнопки ивента доступны всем пользователям."""
    return user_id is not None


def event_drops_allowed(user_id: str | int | None = None) -> bool:
    """Дропы карт только во время активного ивента (+ доступ)."""
    if user_id is not None and not collection_allowed(user_id):
        return False
    from services.event_magic import is_event_active

    return is_event_active()

def ensure_collection(user: dict) -> dict:
    if "collection" not in user or not isinstance(user.get("collection"), dict):
        user["collection"] = {}
    c = user["collection"]
    if not isinstance(c.get("owned"), dict):
        c["owned"] = {}
    c.setdefault("dup_count", 0)
    c.setdefault("vocab_since_drop", 0)
    c.setdefault("complete", False)
    c.setdefault("finale_granted", False)
    # нормализовать ключи owned в str
    owned = {}
    for k, v in list(c["owned"].items()):
        if v:
            owned[str(int(k))] = True
    c["owned"] = owned
    if len(owned) >= TOTAL_ELEMENTS:
        c["complete"] = True
    return c


def owned_ids(user: dict) -> set[int]:
    c = ensure_collection(user)
    out = set()
    for k in c["owned"]:
        try:
            out.add(int(k))
        except (TypeError, ValueError):
            continue
    return out


def owned_count(user: dict) -> int:
    return len(owned_ids(user))


def is_complete(user: dict) -> bool:
    c = ensure_collection(user)
    return bool(c.get("complete")) or owned_count(user) >= TOTAL_ELEMENTS


def missing_ids(user: dict) -> list[int]:
    have = owned_ids(user)
    return [int(e["id"]) for e in COLLECTION_ELEMENTS if int(e["id"]) not in have]


def _roll_rarity() -> str:
    r = random.randint(1, 100)
    acc = 0
    for rarity, weight in RARITY_WEIGHTS:
        acc += weight
        if r <= acc:
            return rarity
    return RARITY_WEIGHTS[0][0]


def _pick_id_for_rarity(rarity: str, pool_ids: set[int] | None = None) -> int | None:
    """Случайный id нужной редкости; pool_ids ограничивает выбор (для pity)."""
    candidates = [int(e["id"]) for e in elements_by_rarity(rarity)]
    if pool_ids is not None:
        candidates = [i for i in candidates if i in pool_ids]
    if not candidates:
        return None
    return random.choice(candidates)


def _pick_any_from(ids: list[int]) -> int | None:
    if not ids:
        return None
    return random.choice(ids)


def roll_element_id(*, missing_only: bool = False, user: dict | None = None) -> int:
    """Обычный ролл 60/30/10. Если missing_only — только недостающие."""
    miss: set[int] | None = None
    if missing_only and user is not None:
        miss = set(missing_ids(user))
        if not miss:
            raise ValueError("no missing elements")
    rarity = _roll_rarity()
    el_id = _pick_id_for_rarity(rarity, miss)
    if el_id is not None:
        return el_id
    # в выбранной редкости нет кандидатов — любая из пула
    if miss is not None:
        picked = _pick_any_from(list(miss))
        if picked is not None:
            return picked
    # полный пул по редкостям с fallback
    for rar, _ in RARITY_WEIGHTS:
        el_id = _pick_id_for_rarity(rar, None)
        if el_id is not None:
            return el_id
    return int(COLLECTION_ELEMENTS[0]["id"])


def apply_drop(user: dict) -> dict[str, Any]:
    """
    Применить один дроп к user (мутирует collection).
    Returns:
      kind: "none" | "new" | "duplicate" | "pity_new" | "complete"
      element: dict каталога или None
      dup_count: int
      owned_count: int
      finale: bool — нужно показать финальный хук
    """
    c = ensure_collection(user)
    if c.get("complete") or owned_count(user) >= TOTAL_ELEMENTS:
        c["complete"] = True
        return {
            "kind": "none",
            "element": None,
            "dup_count": int(c.get("dup_count") or 0),
            "owned_count": owned_count(user),
            "finale": False,
        }

    have = owned_ids(user)
    miss = missing_ids(user)
    finale = False

    # ~20% дубликат (если уже есть карты), иначе новая из недостающих
    if have and miss and random.random() < DUP_DROP_CHANCE:
        el_id = random.choice(list(have))
    elif miss:
        el_id = roll_element_id(missing_only=True, user=user)
    else:
        el_id = roll_element_id(missing_only=False, user=user)

    if el_id not in have:
        c["owned"][str(el_id)] = True
        kind = "new"
        if owned_count(user) >= TOTAL_ELEMENTS:
            c["complete"] = True
            kind = "complete"
            if not c.get("finale_granted"):
                c["finale_granted"] = True
                finale = True
                grant_collection_finale(user)
        return {
            "kind": kind,
            "element": element_by_id(el_id),
            "dup_count": int(c.get("dup_count") or 0),
            "owned_count": owned_count(user),
            "finale": finale,
        }

    # дубликат
    c["dup_count"] = int(c.get("dup_count") or 0) + 1
    dup_n = c["dup_count"]
    if dup_n < DUP_PITY_NEED:
        return {
            "kind": "duplicate",
            "element": element_by_id(el_id),
            "dup_count": dup_n,
            "owned_count": owned_count(user),
            "finale": False,
        }

    # pity
    c["dup_count"] = 0
    miss = missing_ids(user)
    if not miss:
        c["complete"] = True
        if not c.get("finale_granted"):
            c["finale_granted"] = True
            finale = True
            grant_collection_finale(user)
        return {
            "kind": "complete",
            "element": element_by_id(el_id),
            "dup_count": 0,
            "owned_count": owned_count(user),
            "finale": finale,
        }

    pity_id = roll_element_id(missing_only=True, user=user)
    c["owned"][str(pity_id)] = True
    kind = "pity_new"
    if owned_count(user) >= TOTAL_ELEMENTS:
        c["complete"] = True
        kind = "complete"
        if not c.get("finale_granted"):
            c["finale_granted"] = True
            finale = True
            grant_collection_finale(user)
    return {
        "kind": kind,
        "element": element_by_id(pity_id),
        "dup_count": 0,
        "owned_count": owned_count(user),
        "finale": finale,
        "from_duplicate": element_by_id(el_id),
    }


def grant_collection_finale(user: dict) -> None:
    """
    Финальная награда за 15/15 — содержание решим позже.
    Сейчас только помечаем флаги / место для приза.
    """
    c = ensure_collection(user)
    c["finale_granted"] = True
    c["complete"] = True
    log.info("Collection finale granted for user (prize TBD)")


def note_vocab_word_learned(user: dict, user_id: str | None = None) -> bool:
    """
    Учесть +1 выученное слово. True = пора дропать (каждые 3).
    Если коллекция полная / нет доступа / ивент неактивен — False.
    """
    if not event_drops_allowed(user_id):
        return False
    c = ensure_collection(user)
    if c.get("complete"):
        return False
    c["vocab_since_drop"] = int(c.get("vocab_since_drop") or 0) + 1
    if c["vocab_since_drop"] >= VOCAB_DROP_EVERY:
        c["vocab_since_drop"] = 0
        return True
    return False


def _unlock_comment(rarity: str, title: str) -> str:
    """Мини-комментарий Рико при открытии нового элемента."""
    from data.collection_catalog import RARITY_COMMON, RARITY_RARE, RARITY_VERY_RARE

    if rarity == RARITY_VERY_RARE:
        return (
            f"🦜 <b>Рико:</b> ВОУ!!! 🌟🌟🌟 Это <b>очень редкий</b> элемент «{title}»!\n"
            "Такую карточку ловят единицы — ты сейчас на другом уровне! "
            "Сохрани её и гордись, это почти легенда 👑✨"
        )
    if rarity == RARITY_RARE:
        return (
            f"🦜 <b>Рико:</b> Ого, смотри! 💎 Выпал <b>редкий</b> элемент «{title}».\n"
            "Это уже серьёзный кусочек «Магических элементов» — Рико впечатлён!"
        )
    return (
        f"🦜 <b>Рико:</b> Класс! Открыт новый элемент «{title}». "
        "Ещё один шаг к полной коллекции магических элементов 💚"
    )


def format_drop_caption(result: dict) -> str:
    el = result.get("element") or {}
    el_id = el.get("id")
    title = el.get("title_ru") or "?"
    rarity_key = el.get("rarity") or ""
    rarity = RARITY_LABEL_RU.get(rarity_key, "")
    owned_n = int(result.get("owned_count") or 0)
    dup = int(result.get("dup_count") or 0)
    kind = result.get("kind")

    if kind == "none":
        return ""

    if kind == "duplicate":
        return (
            f"♻️ Дубликат <b>#{int(el_id):02d}</b> · {title}\n"
            f"Прогресс дубликатов: <b>{dup}/{DUP_PITY_NEED}</b>\n"
            f"Магические элементы: {owned_n}/{TOTAL_ELEMENTS}"
        )

    if kind == "pity_new":
        msg = (
            f"🎁 За 5 дубликатов — новый элемент!\n"
            f"✨ <b>#{int(el_id):02d}</b> · {rarity}: {title}\n"
            f"Магические элементы: {owned_n}/{TOTAL_ELEMENTS}\n\n"
            f"{_unlock_comment(rarity_key, title)}"
        )
        if result.get("finale"):
            msg += (
                "\n\n🏆 <b>Все 15 элементов собраны!</b>\n"
                "🦜 Теперь тебе открыты баллы ивента в альбоме и в «Гонке лидеров» 💚"
            )
        return msg

    if kind in {"new", "complete"}:
        head = "✨ Новый элемент открыт!"
        if kind == "complete":
            head = "🏆 Все элементы собраны! Последний:"
        msg = (
            f"{head}\n"
            f"<b>#{int(el_id):02d}</b> · {rarity}: {title}\n"
            f"Магические элементы: {owned_n}/{TOTAL_ELEMENTS}\n\n"
            f"{_unlock_comment(rarity_key, title)}"
        )
        if result.get("finale"):
            msg += (
                "\n\n🦜 <b>Рико:</b> Ты собрал(а) все 15 магических элементов! "
                "Баллы ивента теперь видны — продолжай занятия и поднимайся в топ 💚"
            )
        return msg

    return f"✨ #{int(el_id):02d} · {title}"


def format_album_text(user: dict) -> str:
    from services.event_magic import (
        can_show_points,
        format_points,
        get_points,
        is_event_active,
    )

    c = ensure_collection(user)
    have = owned_ids(user)
    lines = [
        "🎴 <b>Магические элементы</b>\n",
        f"Собрано: <b>{len(have)}/{TOTAL_ELEMENTS}</b>",
        f"Дубликаты до бонуса: <b>{int(c.get('dup_count') or 0)}/{DUP_PITY_NEED}</b>\n",
    ]
    if c.get("complete"):
        lines.append("✅ Альбом полный — новые карточки больше не выпадают.\n")
    elif not is_event_active():
        lines.append("⏳ Карты выпадают только во время ивента.\n")
    if can_show_points(user):
        lines.append(f"🏅 Баллы ивента: <b>{format_points(get_points(user))}</b>\n")
    else:
        lines.append("🔒 Баллы ивента откроются после всех 15 элементов.\n")
    for e in COLLECTION_ELEMENTS:
        i = int(e["id"])
        rar = RARITY_LABEL_RU.get(e["rarity"], "")
        if i in have:
            lines.append(f"#{i:02d} ✅ {e['title_ru']} · <i>{rar}</i>")
        else:
            lines.append(f"#{i:02d} 🔒 ???")
    lines.append("\nНажми номер, чтобы посмотреть карточку (если уже есть).")
    return "\n".join(lines)


def album_numbers_kb():
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    rows = []
    row = []
    for i in range(1, TOTAL_ELEMENTS + 1):
        row.append(KeyboardButton(text=str(i)))
        if len(row) == 5:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text="⬅️ В профиль")])
    rows.append([KeyboardButton(text="🔙 Вернуться в меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


async def send_drop_result(message, user: dict, result: dict) -> None:
    """Отправить фото/текст по результату дропа. Не сохраняет user — caller save_users."""
    kind = result.get("kind")
    if kind == "none":
        return
    el = result.get("element")
    caption = format_drop_caption(result)
    if not el:
        if caption:
            await message.answer(caption, parse_mode="HTML")
        return
    path = asset_path(int(el["id"]))
    try:
        import os
        from aiogram.types import FSInputFile

        if os.path.isfile(path):
            await message.answer_photo(
                FSInputFile(path),
                caption=caption,
                parse_mode="HTML",
            )
            return
    except Exception as e:
        log.error("collection photo send failed: %s", e)
    await message.answer(caption, parse_mode="HTML")


def try_grant_drop(user: dict, user_id: str | int | None = None) -> dict | None:
    """Если доступ есть, ивент активен и коллекция неполная — применить дроп."""
    if not event_drops_allowed(user_id):
        return None
    ensure_collection(user)
    if is_complete(user):
        return None
    return apply_drop(user)


async def grant_collection_drop_message(message, user_id: str) -> None:
    """Загрузить user, дропнуть если можно, сохранить, отправить фото+комментарий."""
    if not event_drops_allowed(user_id):
        return
    from services.database import load_users, get_user, save_users
    from services.growth import ensure_growth

    users = load_users()
    user = get_user(users, str(user_id))
    ensure_growth(user)
    result = try_grant_drop(user, user_id=user_id)
    if not result:
        return
    save_users(users, only=str(user_id))
    await send_drop_result(message, user, result)
